# Mac mini installation runbook

## 0. Make the installation boundary explicit

This runbook targets a **fresh standard macOS account** and the named profile `minisamantha`, normally at `~/.openclaw-minisamantha`. All commands below are operator commands, not permissions granted to the limited agent. Run them as the new account unless an admin step is explicitly indicated. Never paste a source document's commands without reviewing them.

An existing installation needs a separate migration plan and verified backup, not this scaffold applied over it. Do not run `onboard`, `doctor --fix`, an updater, or a gateway restart against an unspecified profile. The source Samantha installation is out of scope.

Before organisational/customer-data use, follow the [deployment review](deployment-review.md) and run the recommended `tekoalyasetus` use-case assessment in an approved operator environment. If Finnish is the working language, recommend the `suomen-kieli` workflow there as well. Start from a minimised description, not customer records. Neither companion changes this starter's data or tool permissions.

## 1. Prepare the Mac

1. Update macOS. Use Ethernet where possible, FileVault, the firewall, and a separate admin account. Keep the agent's standard account out of the admin group. A standard account can still run programs and reach its own data; it is not a sandbox.
2. Do not sign the agent into the owner's Apple ID, iCloud, browser, email, password manager, or personal cloud drive. Grant no blanket Full Disk Access, Accessibility, screen recording, or passwordless sudo.
3. Plan restart recovery: FileVault can need a person at the keyboard after cold boot; do not disable encryption or enable automatic login to hide that limitation. Test both the supported planned-restart path and a cold boot. An UPS reduces outages but does not solve unlocking.
4. Record RAM and free disk. The baseline is a 16 GB Apple Silicon Mac mini, one active model turn at a time. Start Docker's VM budget around 3–4 GB and measure. This kit installs no 26B/27B local model, image/video pipeline, or always-running embeddings service.
5. Install a supported, security-patched Node.js version, Git, Python 3, and a Docker-compatible runtime from their official distributions. For the 2026-10-22 baseline, prefer patched Node 24 LTS, at least 24.22.1; Node 26 must be at least 26.12.1. Check the target OpenClaw release's requirement and the version actually available from the chosen package source. An administrator should provision shared software if needed. Verify `node --version`, `python3 --version`, and `docker info` under the actual agent account, then verify the running service's executable separately. See [security maintenance](security-maintenance.md).
6. Optional remote administration: use the official [Tailscale macOS installation guide](https://tailscale.com/docs/install/mac), restrict the tailnet to operator devices, and use SSH keys with the intended administrator account. Keep gateway ports off the public internet. Test a second remote connection before disabling password login. Do not enable Tailscale Funnel or router port forwarding.
7. Plan the three-level kill switch in [section 7](#kill-switch-three-levels) before the first channel is linked: stop this gateway, cut its network, cut its power. Record how to stop only this gateway. The agent must not control its own sole emergency stop.

## 2. Pin and inspect OpenClaw

Security installation baseline checked on 2026-10-22: `2026.10.6`, the published stable release requiring patched Node 24.22.1+ or 26.12.1+. A disposable scaffold was validated with the actual 2026.10.6 CLI on Node 24.22.1; this does not test a running deployment. Recheck the latest stable release, advisories, official-plugin packaging, and Node requirements before approving an exact version. Validate the generated config and complete acceptance tests on the selected release before activation.

**Before any package install or authentication**, inspect the executable and install destination under the intended standard user:

```sh
command -v openclaw
npm prefix --global
```

An absent executable is normal on a fresh account. A separate account/profile does not make a shared npm prefix independent. If installing would replace a binary used by another deployment, stop and provision an independent user-local Node/npm prefix first; do not update the shared installation. Privately check for inherited `OPENCLAW_STATE_DIR` and `OPENCLAW_CONFIG_PATH` overrides, and compare the intended profile paths, service identity and port. Resolve conflicting overrides before continuing; `--profile` must not be assumed to neutralize them. Do not dump the environment or a token-bearing config into logs/chat. Record the approved destinations before the first write.

For a fresh install, after approving that version and proving the global prefix belongs exclusively to this new installation:

```sh
npm install --global openclaw@2026.10.6
openclaw --version
openclaw --help
```

Do not use `sudo npm`, `@latest`, auto-update from a group, or third-party installers copied from chat. If global installation would require broad privilege changes, choose an operator-managed user-local Node/npm installation instead.

Optionally run `python3 scripts/check_install.py` from the skill directory. It checks the selected installed CLI against disposable synthetic state, never your live profile. Read [the result and expected warnings](local-check.md); it does not install software, connect channels, or prove service/runtime isolation.

Provision the sandbox image using the target release's [official image instructions](https://docs.openclaw.ai/gateway/sandboxing/images-and-setup). The npm package does not contain the source-checkout `scripts/sandbox-setup.sh`; do not run a guessed path. Review and build the documented Dockerfile, record its base digest and resulting image ID, and use `openclaw-sandbox:bookworm-slim` for this scaffold. Pin the actual deployment image by a verified immutable reference where supported. Rebuild deliberately for security updates. No Docker socket or host home-directory bind belongs inside a tool container.

## 3. Generate a protected, disabled profile

From the skill directory, after approving the destination:

```sh
python3 scripts/scaffold.py --output "$HOME/.openclaw-minisamantha" --owner '+YOUR_VERIFIED_NUMBER'
```

Replace the placeholder; the tool rejects invalid phone numbers. It refuses existing paths. Do not delete an existing profile to get past that protection. For group setup, prepare a local JSON registry using `assets/groups.example.json` as syntax only and add `--groups /absolute/private/path/groups.local.json`. Never use its synthetic IDs for a real deployment. Obtain the real group JID from trusted operator observation, not a screenshot's display name.

The tool creates a mode-600 config and a separate random token at `secrets/gateway-token`, inside protected mode-700 directories. Config contains a file SecretRef, not the token value. The secret file remains plaintext at rest; file permissions are not a vault. Keep the entire profile on encrypted local disk, outside this repository and cloud sync. Config still contains private identities and paths: do not publish it. Back up both files with encryption and preserved permissions; if moved, explicitly repair absolute secret and workspace paths before use. See [credential storage](local-check.md#gateway-credential-storage).

It creates separate workspaces/agent directories, disables channels and heartbeats, and denies group tools. T4/T5 registry entries receive **no route and no channel admission**. Even with no groups, an unbound second agent prevents a sole-agent fallback into the private owner agent. That placeholder must never receive a binding.

If you intend to test a group on the first day, include just that verified room in the initial registry. Adding a room later is an explicit configuration change: back up first, create its separate workspace and agent directory from the group templates, add a strict-model/tool-denied agent entry, an exact binding, and its mention-gated channel entry. Validate and run the room-isolation tests before activation. The scaffold is intentionally not an in-place updater; do not regenerate over an established profile.

```sh
openclaw --profile minisamantha config validate --json
openclaw --profile minisamantha secrets audit --check
```

Review results privately; do not proceed if validation or secret resolution fails. A different destination requires explicitly setting both `OPENCLAW_STATE_DIR` and `OPENCLAW_CONFIG_PATH` for **every** command and service; the examples assume the named profile's standard location.

## 4. Authenticate GPT‑5.6 Sol

Choose one billing/auth route with the operator:

- Supported OpenAI/Codex account sign-in, subject to plan access, quotas, and current terms.
- An OpenAI Platform project API key with separate billing and explicit monitoring/budget controls.

Do not describe a subscription as unlimited or assume it covers API keys, embeddings, or other providers. The presentation's historical monthly cost is not a quote for the reader. Do not silently fall back to paid API billing or another model.

Inspect the current CLI before authorizing:

```sh
openclaw --profile minisamantha models auth login --help
openclaw --profile minisamantha models auth login --provider openai
openclaw --profile minisamantha models status --agent owner
```

Use the supported agent-scoped auth workflow for each activated group agent if profiles are not available there; consult the installed help. Do not symlink authentication directories or copy the operator's Codex home. Never expose tokens in prompts or command arguments.

After any setup wizard or auth operation, compare the non-secret policy fields against the generated baseline and validate again. Do not accept a wizard's broader tool profile, fallback model, workspace, or channel defaults unnoticed.

The scaffold fixes defaults **and every agent** to `openai/gpt-5.6-sol`, with empty fallbacks, and chooses the OpenClaw agent runtime explicitly. This avoids depending on native Codex-host tools for the starter. Authentication and runtime are separate decisions: account sign-in does not require giving a native coding harness host execution. If the exact account/runtime/model combination is unavailable, stop and report it. Do not invent model definitions or switch to GPT‑6.

Before channel connection, start only this profile in the foreground in a dedicated terminal:

```sh
openclaw --profile minisamantha gateway run
```

Then in another terminal:

```sh
openclaw --profile minisamantha gateway status --require-rpc
openclaw --profile minisamantha agent --agent owner --session-key minisamantha-owner-smoke --message 'Reply with MINI_OK. Do not use tools.' --json
```

Do **not** add `--deliver`. Confirm the response, actual model/auth/runtime, and absence of external delivery. Inspect output privately; do not publish transcripts. Repeat for each planned group agent. An API or OAuth failure is a setup failure, not a reason to relax isolation.

## 5. Add approved memory, not a personal-data dump

Use [memory.md](memory.md). Edit the generated owner `USER.md` and `MEMORY.md` with a few approved preferences and source links. Leave group workspaces free of owner data. The running starter cannot write these files: it proposes changes for the operator to apply. Do not confuse transcripts saved by the gateway with an automatically maintained knowledge base.

Do not add Microsoft 365, mail, a broker connection, global browser cookies, MCP servers, or extra plugins on the first weekend. They need separate scopes, source review, version pins, disclosure review, and tests. Broader integrations are optional future work, not prerequisites.

After the baseline passes, the two recommended next additions are [transcript-first YouTube reading and Lossless Claw](recommended-extensions.md). Follow that guide one extension at a time; neither is part of the scaffold or permission to widen group access. Keep the starter model GPT‑5.6 Sol and the no-MemoriLabs requirement.

## 6. Connect the channel in two stages

First perform the offline and local checks in [acceptance.md](acceptance.md). Have the owner approve the number and target channel. Use a separate real WhatsApp number and maintain the SIM/account. OpenClaw's WhatsApp Web connection is not a guarantee against disconnections or platform restrictions; keep a local operator access path.

### QR linking: operator terminal only

QR linking authenticates the **bot's separate WhatsApp account**, not the owner's access to it. The owner sends DMs from their own allowlisted number. Do not scan using the owner's personal WhatsApp account. The scaffold binds account ID `default`; using a different account requires an explicit configuration/routing review, not merely a different login flag.

Before linking, check the standard macOS user, named profile, state/config paths and gateway/service port against the approved target. Keep `dmPolicy` and `groupPolicy` set to `disabled`. Do not proceed on a CLI/gateway path mismatch or an unverifiable target warning. The current CLI has pre-write mismatch checks, but those are not a substitute for selecting the correct profile, especially on remote gateways.

In an **operator-controlled terminal on the gateway host**, inspect the installed help, enable only the adapter, then run login:

```sh
openclaw --profile minisamantha channels login --help
openclaw --profile minisamantha config set channels.whatsapp.enabled true
openclaw --profile minisamantha channels login --channel whatsapp --account default
openclaw --profile minisamantha channels status
```

The login example matches the help inspected on OpenClaw 2026.10.2 and the current [channel CLI documentation](https://docs.openclaw.ai/cli/channels); verify it on the actual release, including the 2026.9.8 reference. Do not run a second gateway if the intended profile is already running from section 4.

1. On the phone using the separate bot number, open WhatsApp → Settings (or the Android menu) → Linked devices → Link a device.
2. Scan the live terminal QR; renew an expired QR through that same supervised login flow. Do not publish, save in the repo, or forward the QR into a group/chat transcript.
3. Verify the linked account is the intended bot number in WhatsApp's linked-device view and local channel status. Keep identifiers and auth files private.
4. Recheck configuration: both ingress policies remain disabled, `selfChatMode: false`, `configWrites: false`, exact sender IDs, account `default`, and no account overrides widening access. Validate again before enabling DMs.

The current OpenClaw agent `exec` blocks interactive `channels login`. Some builds also offer a `whatsapp_login` agent tool; **do not enable it for MiniSamantha**, privately or in groups. Setup belongs to the operator, not the limited agent. For a headless host use a trusted operator terminal/remote-administration session; do not add chat-delivered QR permissions as a workaround.

Successful login may save authentication while the gateway's account start is skipped or delayed. Follow the reported status and verify the correct account's connection; saved auth is not proof of a healthy listener or correct admission. Allow at most one supervised retry after correcting an identified cause; if that fails, stop with both ingress policies disabled and record the unresolved error privately. Do not borrow another account's session, switch profiles, log out unrelated devices, repeatedly restart the whole gateway, or delete auth to conceal an unresolved lifecycle error.

If a login expires before a usable QR, check network reachability, the QR expiry and the specific error first. **Only when a proxy is in use**, check the gateway host's `HTTPS_PROXY`/`HTTP_PROXY`/`NO_PROXY` environment privately; the documented proxy case requires that `NO_PROXY` not bypass `mmg.whatsapp.net`. A 408/TLS error alone does not establish a proxy cause. Do not disable TLS checks, add a proxy, or dump environment variables into chat. See [WhatsApp troubleshooting](https://docs.openclaw.ai/channels/whatsapp#troubleshooting).

### Enable the owner, then one test group

Enable owner DMs only after link verification and the pre-admission checks:

```sh
openclaw --profile minisamantha config set channels.whatsapp.dmPolicy allowlist
```

Prove that the owner gets a reply and a non-owner DM does not. For group testing, the operator adds the **same bot number** to one private test group and verifies that room's exact JID independently. A QR does not select the room or create an agent binding. Check that the reviewed registry, dedicated agent/workspace, binding and channel group map contain that room, with only the owner initially admitted as sender. Then activate ingress for the configured test group(s):

```sh
openclaw --profile minisamantha config set channels.whatsapp.groupPolicy allowlist
```

Initially only the owner is in `groupAllowFrom`. The group map controls **which rooms**; `groupAllowFrom` controls **which senders across those rooms**. Do not treat room admission as participant authorization. To add collaborators, obtain an explicit common sender roster and retest denied senders. If different rooms need different enforceable rosters, use only a verified per-room sender-control feature of your release or separate deployments; do not assume the global list is per-room. No `*` admission entries.

`requireMention` also accepts some reply-to-bot activation in OpenClaw. The prompt's stricter explicit-human-tag rule is behavioral. **For this kit, production groups remain disabled until the strict-tag ingress acceptance tests pass**, including no model invocation on quote-only/reply-only activation. This may require a separately reviewed ingress filter or a verified target-release fix; neither is shipped here. Owner-only DMs may be handed over separately after their own tests pass; private test groups are only for bounded acceptance work. Do not reinterpret a polite model refusal as successful ingress filtering. Prevent bot loops with sender allowlists, not claims that WhatsApp can always detect bots.

Check the actual target build and rerun the current-message, quote-only, native-mention, and recovery tests. A patch or successful test from another deployment does not establish these guarantees here; copying policy prose does not install runtime corrections. See [deployment review](deployment-review.md).

Only after all live tests pass, install the named profile's service using `gateway install --help` and the supported command. Verify its launch environment, paths, identity, token handling, and port. Do not replace another profile's service. Test logout/reboot/remote recovery before unattended operation.

## 7. Operations, backup, and recovery

Inspect after any change:

```sh
openclaw --profile minisamantha config validate
openclaw --profile minisamantha gateway status --require-rpc
openclaw --profile minisamantha channels status
openclaw --profile minisamantha security audit --deep
```

Review every finding. Do not automatically apply `security audit --fix` or `doctor --fix`; either may change configuration. Keep logs and audit exports private and bounded. Use runtime evidence plus adversarial tests, not a “zero critical” screenshot as certification.

Create a consistent backup through [OpenClaw backup](https://docs.openclaw.ai/install/backups), for example:

```sh
openclaw --profile minisamantha backup create --output "$HOME/Backups/MiniSamantha" --verify
```

The backup includes secrets and conversations; keep it encrypted, separate from the public repo, and access-restricted. A compressed archive is not automatically encrypted. A verified archive is not a restore test. Restore into an isolated test destination with channels disabled and no production port/account collision. Follow that release's restore help; confirm config, memory, and session readability before any activation. Never use a live raw directory tar as a database-consistency guarantee.

Before an approved upgrade, follow the [security maintenance checklist](security-maintenance.md): inspect first, verify backup coverage, capture version/image IDs, and approve an exact target and recovery plan. The updater may restart the gateway. Re-run routing, model, sandbox, and real channel tests. Retain a compatible previous application/plugin/config/state backup; downgrading a binary alone may not undo data migrations. Rebuild or pull corrected container images and recreate affected containers; a restart alone does not replace their runtime.

For “session ended during restart recovery”: preserve the transcript, verify the model/auth and gateway, and use `/new` or `/reset` in the **affected conversation** to start a replacement session. In WebChat, use its resume/new-session control. Warn that active working context changes; do not delete session files, reset other conversations, or keep restarting the gateway. A new session must still pass the smoke test.

### Kill switch: three levels

Keep a stop you can reach in the dark, from away from home, without the agent's help. Use the lowest level that contains the problem.

| Level | Action | Use when | Cost |
| --- | --- | --- | --- |
| 1. Stop | `openclaw --profile minisamantha gateway stop`, or the terminal interrupt for a foreground instance. Verify the intended process is down | Misbehaving replies, runaway spend, a test gone wrong | None; state preserved |
| 2. Cut network | Block **all** of the Mac's network paths from an independent device; Ethernet alone is insufficient if Wi-Fi or another uplink remains | You cannot reach the shell, or containment is uncertain | New network traffic stops once containment is verified; already submitted remote work may continue |
| 3. Cut power | Switch off a smart plug or power strip controlled from an independent device or account | Levels 1–2 failed, or you suspect the host itself | Last resort: may damage in-flight writes; FileVault needs a person at the keyboard to restart |

Requirements:

- The stop path must not depend on the Mac itself, the agent's macOS account, its WhatsApp number, or credentials stored on that machine. Keep router and smart-plug credentials off the agent's account.
- Use an independent, always-on device for remote stops, such as a small Linux machine or a home-automation hub on the operator's own tailnet access. Do not grant the agent's account access to it.
- Inventory Ethernet, Wi-Fi, USB/mobile tethering and alternate routers before activation. Disable unused uplinks and verify that cutting the intended path does not fall back to another. Verify loss of channel connectivity and new provider requests; unplugging a cable or losing SSH alone is not proof of containment. Keep the independent power-stop path usable after cutting the Mac's network.
- Test levels 1 and 2 before activation and after major changes, including once from outside the home network. Test level 3 only in a planned window.
- After any level 2 or 3 stop, preserve logs, revoke exposed credentials from a trusted device, and investigate before restarting. Rerun the smoke test before reopening channels.
