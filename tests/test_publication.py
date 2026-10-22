import importlib.util
import os
from pathlib import Path
import random
import string
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/scan_publication.py"
SPEC = importlib.util.spec_from_file_location("publication", SCRIPT)
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)


class PublicationTests(unittest.TestCase):
    def test_private_email_rejected_without_echo(self):
        self.assertEqual(publication.private_email_count(b"operator@" + b"example.net\0"), 1)

    def test_noreply_only_and_empty_fields(self):
        self.assertEqual(publication.private_email_count(b"\0test@users.noreply.github.com\0"), 0)

    def test_system_noreply_exception_is_exact(self):
        self.assertEqual(publication.private_email_count(b"noreply@github.com\0"), 0)
        for address in (b"employee@" + b"github.com", b"not-noreply@" + b"github.com",
                        b"noreply@" + b"github.com.example.org"):
            with self.subTest(check="other address rejected"):
                self.assertEqual(publication.private_email_count(address + b"\0"), 1)


@unittest.skipUnless(os.environ.get("GITLEAKS_BIN"), "Set GITLEAKS_BIN for scanner integration tests")
class ScannerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="minisamantha-canary-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name).resolve() / "repo"
        self.repo.mkdir()
        self.run_git("init", "-b", "main")
        self.run_git("config", "user.name", "Synthetic test")
        self.run_git("config", "user.email", "test@users.noreply.github.com")
        self.file = self.repo / "example.txt"

    def run_git(self, *args):
        return publication.git(self.repo, *args)

    def commit(self, text):
        self.file.write_text(text, encoding="utf-8")
        self.run_git("add", "example.txt")
        self.run_git("commit", "-m", "Synthetic test commit")

    def scan(self):
        return publication.scan(self.repo, os.environ["GITLEAKS_BIN"])

    def canary(self):
        # Deliberately fake token assembled at runtime, never a real credential.
        return "ghp_" + "".join(random.Random(42).sample(string.ascii_letters + string.digits, 36))

    def test_clean_history_passes(self):
        self.commit("public documentation\n")
        self.assertTrue(self.scan()["pass"])

    def test_deleted_secret_still_fails_history(self):
        canary = self.canary()
        self.commit("token=" + canary + "\n")
        self.commit("public documentation\n")
        result = self.scan()
        self.assertFalse(result["pass"])
        self.assertFalse(result["checks"]["history"]["pass"])
        self.assertTrue(result["checks"]["working_tree"]["pass"])
        self.assertNotIn(canary, str(result))

    def test_uncommitted_secret_fails_working_tree(self):
        self.commit("public documentation\n")
        self.file.write_text("token=" + self.canary(), encoding="utf-8")
        result = self.scan()
        self.assertFalse(result["checks"]["working_tree"]["pass"])
        self.assertTrue(result["checks"]["history"]["pass"])

    def test_secret_in_commit_message_fails_metadata(self):
        self.commit("public documentation\n")
        self.run_git("commit", "--allow-empty", "-m", "Synthetic token=" + self.canary())
        result = self.scan()
        self.assertFalse(result["checks"]["commit_metadata"]["pass"])
        self.assertNotIn(self.canary(), str(result))

    def test_secret_on_other_branch_fails_history(self):
        self.commit("public documentation\n")
        self.run_git("switch", "-c", "synthetic-other")
        self.commit("token=" + self.canary())
        self.run_git("switch", "main")
        result = self.scan()
        self.assertFalse(result["checks"]["history"]["pass"])
        self.assertTrue(result["checks"]["working_tree"]["pass"])

    def test_private_commit_email_fails(self):
        self.run_git("config", "user.email", "operator@" + "example.net")
        self.commit("public documentation\n")
        self.assertFalse(self.scan()["checks"]["commit_email_policy"]["pass"])

    def test_system_committer_does_not_exempt_private_author(self):
        self.commit("public documentation\n")
        self.run_git("-c", "user.email=noreply@github.com", "commit", "--allow-empty",
                     "--author", "Synthetic test <test@users.noreply.github.com>",
                     "-m", "Synthetic GitHub merge identity")
        self.assertTrue(self.scan()["pass"])
        self.run_git("-c", "user.email=noreply@github.com", "commit", "--allow-empty",
                     "--author", "Synthetic test <operator@" + "example.net>",
                     "-m", "Synthetic private author")
        result = self.scan()
        self.assertFalse(result["checks"]["commit_email_policy"]["pass"])
        self.assertNotIn("operator@" + "example.net", str(result))

    def test_shallow_checkout_refused(self):
        self.commit("public documentation\n")
        (self.repo / ".git/shallow").write_bytes(self.run_git("rev-parse", "HEAD"))
        with self.assertRaises(ValueError):
            self.scan()
