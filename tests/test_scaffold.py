import copy
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "skills/install-minisamantha/scripts/scaffold.py"
SPEC = importlib.util.spec_from_file_location("scaffold", SCRIPT)
kit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kit)
OWNER = "+15555550100"
GROUPS = [{"slug": f"test-{tier.lower()}", "jid": f"11111111111111111{i}@g.us", "tier": tier}
          for i, tier in enumerate(("T2", "T3", "T4", "T5"))]


class ScaffoldTests(unittest.TestCase):
    def config(self, groups=None):
        return kit.build_config(Path("/synthetic/minisamantha"), OWNER,
                                GROUPS if groups is None else groups)

    def test_strict_requested_model_everywhere(self):
        config = self.config()
        for agent in [config["agents"]["defaults"], *config["agents"]["entries"].values()]:
            self.assertEqual(agent["model"], {"primary": "openai/gpt-5.6-sol", "fallbacks": []})

    def test_initial_channels_closed(self):
        channel = self.config()["channels"]["whatsapp"]
        self.assertFalse(channel["enabled"])
        self.assertEqual(channel["dmPolicy"], "disabled")
        self.assertEqual(channel["groupPolicy"], "disabled")
        self.assertEqual(channel["groupAllowFrom"], [OWNER])
        self.assertFalse(channel["selfChatMode"])

    def test_t4_t5_no_routes_or_admission(self):
        config = self.config()
        self.assertEqual(len(config["bindings"]), 3)
        for group in GROUPS[2:]:
            self.assertNotIn(group["jid"], config["channels"]["whatsapp"]["groups"])
            self.assertNotIn("group-" + group["slug"], config["agents"]["entries"])

    def test_no_sole_agent_fallback_or_catchall(self):
        config = self.config([])
        self.assertEqual(len(config["agents"]["entries"]), 2)
        for binding in config["bindings"]:
            self.assertIn("peer", binding["match"])
            self.assertNotIn("*", json.dumps(binding))

    def test_group_separation_and_tool_denial(self):
        entries = self.config()["agents"]["entries"]
        self.assertEqual(len({a["workspace"] for a in entries.values()}), len(entries))
        self.assertEqual(len({a["agentDir"] for a in entries.values()}), len(entries))
        for name, agent in entries.items():
            if name != "owner":
                self.assertEqual(agent["tools"]["deny"], ["*"])
                self.assertEqual(agent["sandbox"]["workspaceAccess"], "none")
            self.assertEqual(agent["skills"], [])

    def test_sandbox_no_host_or_network(self):
        config = self.config()
        sb = config["agents"]["defaults"]["sandbox"]
        self.assertEqual((sb["mode"], sb["scope"]), ("all", "session"))
        self.assertEqual(sb["docker"]["network"], "none")
        self.assertTrue(sb["docker"]["readOnlyRoot"])
        self.assertNotIn("binds", sb["docker"])
        self.assertEqual(config["gateway"]["bind"], "loopback")
        self.assertEqual(config["tools"]["allow"], ["read"])
        self.assertFalse(config["browser"]["enabled"])
        self.assertFalse(config["browser"]["allowSystemProfileImport"])
        self.assertEqual(config["agents"]["defaults"]["heartbeat"]["every"], "0m")

    def test_invalid_identity_or_tier_rejected(self):
        for field, value in [("slug", "../../owner"), ("jid", "*"), ("tier", "T1"), ("tier", "T6")]:
            bad = copy.deepcopy(GROUPS)
            bad[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.config(bad)
        with self.assertRaises(ValueError):
            kit.build_config(Path("/synthetic"), "*", [])

    def test_duplicate_and_extra_config_rejected(self):
        with self.assertRaises(ValueError):
            self.config([GROUPS[0], GROUPS[0]])
        bad = copy.deepcopy(GROUPS)
        bad[0]["tools"] = {"allow": ["*"]}
        with self.assertRaises(ValueError):
            self.config(bad)

    def test_new_profile_private_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / "profile"
            kit.scaffold(root, OWNER, GROUPS)
            config_path = root / "openclaw.json"
            original = config_path.read_bytes()
            self.assertEqual(stat.S_IMODE(root.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(config_path.stat().st_mode), 0o600)
            self.assertNotIn("MemoriLabs", original.decode())
            self.assertTrue((root / "workspaces/owner/wiki").is_dir())
            self.assertFalse((root / "workspaces/group-test-t2/MEMORY.md").exists())
            with self.assertRaises(ValueError):
                kit.scaffold(root, OWNER, GROUPS)
            self.assertEqual(original, config_path.read_bytes())

    def test_playbooks_owner_only_and_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / "profile"
            kit.scaffold(root, OWNER, GROUPS)
            shipped = sorted(p.name for p in (SCRIPT.parent.parent / "assets/playbooks").glob("*.md"))
            self.assertGreaterEqual(len(shipped), 3)
            owner_books = root / "workspaces/owner/playbooks"
            self.assertEqual(sorted(p.name for p in owner_books.iterdir()), shipped)
            for book in owner_books.iterdir():
                self.assertEqual(stat.S_IMODE(book.stat().st_mode), 0o600)
            for agent_id in ("unbound", "group-test-t2", "group-test-t3"):
                self.assertFalse((root / "workspaces" / agent_id / "playbooks").exists())

    def test_gateway_secret_reference_permissions_and_no_disclosure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / "profile"
            canary = "synthetic-private-token-" + "x" * 48
            stdout, stderr = io.StringIO(), io.StringIO()
            with mock.patch.object(kit.secrets, "token_urlsafe", return_value=canary), \
                    mock.patch("sys.argv", ["scaffold.py", "--output", str(root), "--owner", OWNER]), \
                    redirect_stdout(stdout), redirect_stderr(stderr):
                kit.main()
            secret_file = root / "secrets" / "gateway-token"
            self.assertEqual(secret_file.read_text().strip(), canary)
            self.assertEqual(stat.S_IMODE(secret_file.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(secret_file.parent.stat().st_mode), 0o700)
            self.assertEqual(secret_file.stat().st_nlink, 1)
            config = json.loads((root / "openclaw.json").read_text())
            self.assertEqual(config["gateway"]["auth"]["token"], {
                "source": "file", "provider": "local_gateway", "id": "value"})
            self.assertEqual(config["secrets"]["providers"]["local_gateway"], {
                "source": "file", "path": str(secret_file), "mode": "singleValue"})
            for path in root.rglob("*"):
                if path.is_file() and path != secret_file:
                    self.assertNotIn(canary, path.read_text())
            self.assertNotIn(canary, stdout.getvalue() + stderr.getvalue())

    def test_symlink_target_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp).resolve()
            link = parent / "link"
            link.symlink_to(parent / "missing")
            with self.assertRaises(ValueError):
                kit.scaffold(link, OWNER, [])


if __name__ == "__main__":
    unittest.main()
