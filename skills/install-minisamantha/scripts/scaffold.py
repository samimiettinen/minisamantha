#!/usr/bin/env python3
"""Create a NEW, disabled MiniSamantha profile. No subprocesses or network I/O."""

import argparse
import json
import os
from pathlib import Path
import re
import secrets

MODEL = "openai/gpt-5.6-sol"
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def validate_groups(groups):
    if not isinstance(groups, list):
        raise ValueError("Group registry must be a JSON array")
    slugs, jids = set(), set()
    for group in groups:
        if not isinstance(group, dict) or set(group) != {"slug", "jid", "tier"}:
            raise ValueError("Each group needs exactly slug, jid, tier")
        slug, jid, tier = group["slug"], group["jid"], group["tier"]
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,39}", slug):
            raise ValueError("Invalid group slug")
        if not isinstance(jid, str) or not re.fullmatch(r"[0-9]{5,30}(?:-[0-9]{5,30})?@g\.us", jid):
            raise ValueError("Use an exact verified WhatsApp group JID")
        if tier not in ("T2", "T3", "T4", "T5"):
            raise ValueError("Groups may not be T1; expected T2 through T5")
        if slug in slugs or jid in jids:
            raise ValueError("Duplicate group identity")
        slugs.add(slug)
        jids.add(jid)
    return groups


def build_config(root, owner, groups, token, port=19789):
    root = Path(root)
    if not root.is_absolute():
        raise ValueError("Profile path must be absolute")
    if not re.fullmatch(r"\+[1-9][0-9]{7,14}", owner):
        raise ValueError("Owner must be an exact E.164 number, not a wildcard")
    if not 1024 <= port <= 65535:
        raise ValueError("Use an unprivileged TCP port")
    validate_groups(groups)
    if not isinstance(token, str) or len(token) < 32:
        raise ValueError("Gateway token must have at least 32 characters")
    sandbox = {
        "mode": "all", "backend": "docker", "scope": "session",
        "workspaceAccess": "none",
        "docker": {"image": "openclaw-sandbox:bookworm-slim", "network": "none",
                   "readOnlyRoot": True, "capDrop": ["ALL"]},
        "browser": {"enabled": False},
    }

    def agent(agent_id, private=False):
        return {
            "name": "MiniSamantha", "workspace": str(root / "workspaces" / agent_id),
            "agentDir": str(root / "agents" / agent_id / "agent"),
            "model": {"primary": MODEL, "fallbacks": []},
            "utilityModel": MODEL,
            "skills": [],
            "sandbox": {"workspaceAccess": "ro" if private else "none"},
            "groupChat": {"mentionPatterns": ["@MiniSamantha\\b"]},
            "tools": {"allow": ["read"]} if private else {"deny": ["*"]},
        }

    # Two agents even with zero groups: no sole-agent implicit routing to T1.
    entries = {"owner": agent("owner", True), "unbound": agent("unbound")}
    bindings = [{"agentId": "owner", "match": {
        "channel": "whatsapp", "accountId": "default",
        "peer": {"kind": "direct", "id": owner}}}]
    admitted = {}
    for group in groups:
        if group["tier"] not in ("T2", "T3"):
            continue
        agent_id = "group-" + group["slug"]
        entries[agent_id] = agent(agent_id)
        admitted[group["jid"]] = {
            "requireMention": True,
            "systemPrompt": f"MiniSamantha {group['tier']}. This room only. "
                            "Explicit human tag required; never owner/private powers.",
        }
        bindings.append({"agentId": agent_id, "match": {
            "channel": "whatsapp", "accountId": "default",
            "peer": {"kind": "group", "id": group["jid"]}}})
    return {
        "gateway": {"mode": "local", "bind": "loopback", "port": port,
                    "auth": {"mode": "token", "token": token}},
        "agents": {"ownership": "explicit", "defaults": {
            "model": {"primary": MODEL, "fallbacks": []},
            "utilityModel": MODEL, "skills": [], "maxConcurrent": 1,
            "models": {MODEL: {"agentRuntime": {"id": "openclaw"}}},
            "heartbeat": {"every": "0m"}, "sandbox": sandbox,
        }, "entries": entries},
        "session": {"dmScope": "per-account-channel-peer", "groupScope": "per-group",
                    "maintenance": {"mode": "warn"}},
        "bindings": bindings,
        "tools": {
            "allow": ["read"],
            "deny": ["group:runtime", "group:automation", "group:sessions",
                     "group:messaging", "group:nodes", "group:ui", "group:plugins",
                     "group:web", "group:media", "group:agents", "group:memory",
                     "write", "edit", "apply_patch", "bundle-mcp"],
            "fs": {"workspaceOnly": True}, "exec": {"security": "deny", "ask": "always"},
            "elevated": {"enabled": False}, "agentToAgent": {"enabled": False},
            "codeMode": {"enabled": False},
            "sandbox": {"tools": {"allow": ["read"], "deny": ["exec", "process", "write", "edit", "apply_patch"]}},
        },
        "browser": {"enabled": False},
        "commands": {"config": False, "debug": False, "bash": False, "restart": False,
                     "ownerAllowFrom": [owner]},
        "channels": {"whatsapp": {
            "enabled": False, "dmPolicy": "disabled", "allowFrom": [owner],
            "selfChatMode": False, "groupPolicy": "disabled", "groupAllowFrom": [owner],
            "groups": admitted, "configWrites": False, "sendReadReceipts": False,
        }},
    }


def private_write(path, content):
    # Never overwrite; no existing destination tree is accepted by scaffold().
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(content)


def scaffold(output, owner, groups, port=19789):
    output = Path(output).expanduser()
    if not output.is_absolute() or output.is_symlink() or output.exists():
        raise ValueError("Choose a new absolute profile directory; existing paths are refused")
    if not output.parent.is_dir() or output.parent.resolve() != output.parent:
        raise ValueError("Parent must exist and must not traverse symlinks")
    config = build_config(output, owner, groups, secrets.token_urlsafe(48), port)
    soul = (ASSETS / "SOUL.md").read_text(encoding="utf-8")
    owner_rules = (ASSETS / "OWNER-AGENTS.md").read_text(encoding="utf-8")
    group_rules = (ASSETS / "GROUP-AGENTS.md").read_text(encoding="utf-8")
    playbooks = {path.name: path.read_text(encoding="utf-8")
                 for path in sorted((ASSETS / "playbooks").glob("*.md"))}
    old_umask = os.umask(0o077)
    try:
        output.mkdir(mode=0o700, exist_ok=False)
        private_write(output / "openclaw.json", json.dumps(config, indent=2) + "\n")
        private_write(output / "groups.local.json", json.dumps(groups, indent=2) + "\n")
        for agent_id in config["agents"]["entries"]:
            workspace = output / "workspaces" / agent_id
            rules = owner_rules if agent_id == "owner" else group_rules
            if agent_id == "unbound":
                rules = "# Unbound safety placeholder\nNever answer channel messages. Return NO_REPLY. No tools or memory.\n"
            private_write(workspace / "AGENTS.md", rules)
            private_write(workspace / "SOUL.md", soul)
        owner_ws = output / "workspaces" / "owner"
        private_write(owner_ws / "USER.md", "# Owner preferences\nAdd only owner-approved, non-sensitive preferences.\n")
        private_write(owner_ws / "MEMORY.md", "# Approved memory index\nNo memories imported. Link approved records here.\n")
        for folder in ("memory", "sources", "wiki", "graph", "records", "drafts"):
            (owner_ws / folder).mkdir(mode=0o700)
        # Owner-only job descriptions. Group agents cannot read files.
        for name, text in playbooks.items():
            private_write(owner_ws / "playbooks" / name, text)
    finally:
        os.umask(old_umask)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="NEW absolute profile path, normally ~/.openclaw-minisamantha")
    parser.add_argument("--owner", required=True, help="Verified owner's E.164 number")
    parser.add_argument("--groups", type=Path, help="Local JSON registry; omitted means no groups")
    parser.add_argument("--port", type=int, default=19789)
    args = parser.parse_args()
    try:
        groups = json.loads(args.groups.read_text()) if args.groups else []
        path = scaffold(args.output, args.owner, groups, args.port)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Refused: {error}\n")
    print(f"Created protected profile at {path}. Channels DISABLED. Nothing installed or started.")
    print("A random gateway token is in the protected config; do not print or commit that file.")


if __name__ == "__main__":
    main()
