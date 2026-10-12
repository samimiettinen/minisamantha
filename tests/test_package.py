from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_relative_markdown_links_resolve(self):
        for document in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(document=document.name, target=target):
                    self.assertTrue((document.parent / target.split("#")[0]).exists())

    def test_claude_wrapper_is_manual_and_resolves(self):
        wrapper = ROOT / ".claude/skills/install-minisamantha/SKILL.md"
        text = wrapper.read_text()
        self.assertIn("disable-model-invocation: true", text)
        canonical = (wrapper.parent / "../../../skills/install-minisamantha/SKILL.md").resolve()
        self.assertTrue(canonical.is_file())
        self.assertIn("# Install MiniSamantha", canonical.read_text())

    def test_playbooks_state_contract(self):
        books = sorted((ROOT / "skills/install-minisamantha/assets/playbooks").glob("*.md"))
        self.assertTrue(books)
        for book in books:
            text = book.read_text()
            for heading in ("## Input", "## Output", "## Quality bar", "## Never"):
                with self.subTest(playbook=book.name, heading=heading):
                    self.assertIn(heading, text)

    def test_license_is_mit(self):
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text())

    def test_no_private_identifiers_in_shipped_text(self):
        # Generic checks only. Never publish private names, their hashes, or a
        # private denylist in the repository; run those checks outside the kit.
        forbidden = ("/" + "Users/", "+" + "358", "120" + "363")
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(part in (".git", "__pycache__") for part in path.relative_to(ROOT).parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                self.fail(f"Unexpected binary file requires manual privacy review: {path.name}")
            for value in forbidden:
                with self.subTest(path=path.name, pattern=value):
                    self.assertNotIn(value, text)
            for address in re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
                domain = address.rsplit("@", 1)[1].lower()
                with self.subTest(path=path.name, check="email or room identifier"):
                    self.assertIn(domain, ("example.com", "example.org", "users.noreply.github.com", "g.us"))
                    if domain == "g.us":
                        self.assertRegex(address, r"^([1-4])\1+@g\.us$")


if __name__ == "__main__":
    unittest.main()
