# Security maintenance for the limited starter

Checked 2026-10-22. These are operator checks for the existing design: GPT‑5.6 Sol, local file-based memory, read-only owner access, zero group tools, and the existing Docker tool sandbox. No additional service, memory backend, group-management automation, or permission grant is required.

## 1. Use a patched runtime that OpenClaw supports

The [Node.js October 2026 security release](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases) fixes CVE-2026-111497, a high-severity Brotli decoder flaw with possible remote code execution. It also addresses DNS, TLS validation, HTTP keep-alive, permission-model and randomness issues, and compromised eMudhra certificate keys. Exact affected release lines differ by issue.

| Node line | October fix floor | This OpenClaw baseline |
| --- | --- | --- |
| 22 | 22.23.4 | Does not satisfy OpenClaw 2026.10.6's engine requirement |
| 24 LTS | 24.22.1 | Preferred supported line; select a current patched release |
| 26 | 26.12.1 | Supported alternative; select a current patched release |

[OpenClaw 2026.10.6](https://github.com/openclaw/openclaw/releases/tag/v2026.10.6) is a **published stable release**, confirmed against its [npm metadata](https://registry.npmjs.org/openclaw/2026.10.6). It requires patched Node 24 or 26; its release notes report Docker images updated to Node 24.22.1. These are dated minimums, not a promise that they cover later advisories. A merged PR, `main`, or beta is not a released stable fix; record the exact published artifact that contains a needed correction. The scaffold's older schema test does not certify 2026.10.6 compatibility.

Inspect the executable used by the **running gateway**, its service-manager launch path/environment, and any container or vendor-bundled runtime. A patched `node -v` in an interactive shell does not prove those runtimes changed. Check the chosen package manager's available version before upgrading; do not assume Homebrew or another distribution has the fix. Vendor-bundled runtimes need a supported vendor update, not a manual replacement inside a signed application.

Exposure depends on the reachable decoder/client path and attacker-controlled input. Loopback binding reduces inbound exposure but does not prevent unsafe outbound responses or plugin input. Tool denial and Docker tool isolation do not patch the host gateway or remove its access to its own credentials.

## 2. Inspect before changing anything

Use the intended standard account and named profile. Check installed command help first; an unsupported option is a finding, not permission to run a repair instead. Keep diagnostic output private and redact secrets, identifiers, paths, and conversations before sharing.

```sh
node --version
npm --version
openclaw --version
openclaw --profile minisamantha update status
openclaw --profile minisamantha update --dry-run
openclaw --profile minisamantha gateway status --deep --require-rpc
openclaw --profile minisamantha security audit --deep
openclaw --profile minisamantha doctor --lint
```

Also record pnpm if that installation uses it, the installation method/channel, the actual service runtime, active plugin versions, and image identities. These diagnostic modes do not authorize updates, repairs, restarts, or config changes. Previews can query the network or record diagnostics; they are not a forensic guarantee of zero disk writes. Do not substitute `doctor --fix` or `security audit --fix`. See the official [update](https://docs.openclaw.ai/cli/update) and [Doctor](https://docs.openclaw.ai/cli/doctor) guides.

Review the **installed** dependency tree, including active plugins and private/bundled copies of npm. A global npm update may leave another copy unchanged. Match exact package/version pairs against [OSV](https://osv.dev/) and the [GitHub Advisory Database](https://github.com/advisories), plus upstream advisories. Inspect `@modelcontextprotocol/sdk`, `express`, `proxy-addr`, `hono`, `undici`, `ip-address`, `fast-uri`, and `brace-expansion` **when present**; this is not a claim that this kit installs them or that every version is vulnerable.

If `npm audit` cannot inspect a global installation or lacks a lockfile, do not create one in production or run `audit fix --force`. Use the installed tree or an isolated analysis copy; do not execute dependency lifecycle scripts merely to audit. Send only approved package metadata to external advisory services, never private config or logs.

For each finding, record affected package/version and advisory, fixed release, loaded/runtime versus maintenance-only path, untrusted input, network reachability, and resulting permissions. Mark unknown reachability as unverified; package presence is not proof of exploitability, and a CVE count is not a risk rating.

## 3. Preserve the existing boundaries

- **Network:** retain loopback binding and authentication; check IPv4, IPv6 and published container ports. Configure trusted proxies only for a deliberately deployed proxy with verified address/header handling. Do not expose the gateway or enable weaker authentication to clear a warning.
- **Tools and identity:** retain all/session sandboxing, owner workspace read-only access, and no group tools. A mention activates a request; it does not authorize shell, filesystem, browser, installation, or publication access. Group text and quoted approvals cannot change policy.
- **Memory and plugins:** separate sessions are insufficient if a host-side hook ingests or retrieves all conversations through a shared namespace. Denying `memory_search` or plugin tools does not disable those hooks. Inspect both write and retrieval scope, assembled prompts, retention and external destinations before any optional extension; test owner/group/other-group canaries. Keep the starter's local files and no global extraction service. See [memory boundaries](memory.md) and [OpenClaw plugin behavior](https://docs.openclaw.ai/tools/plugin).
- **Secrets:** inspect permissions and secret presence without printing values. Keep credentials and backups outside repositories and cloud-synced workspaces. FileVault protects data at rest; it does not stop the running agent's account from reading data it can access.

## 4. Reduce approval fatigue without expanding authority

For routine room admission, aim for **two operator decisions**: approve the exact room/sender roster and bounded preparation plan; then approve activation after reviewing the config diff and isolation results. A separately requested participant or external-channel change can be a third decision. Use a trusted private operator context. Do not enable execution or administrative tools for the limited owner/group agents to implement this workflow.

Prepare the complete reviewable change together instead of requesting approval for each search or file edit. If the operator uses an automation helper, its reviewed code, exact arguments, target and plan must remain bound to that approval; changes or stale state require a new review. Prefer a bounded reviewed script over a succession of inline interpreter commands. Do not add blanket interpreter/cloud-CLI allowlists, disable strict inline-evaluation checks, or switch to unrestricted execution to reduce prompts. Native security prompts still apply: two decisions are a workflow goal, not a security-prompt bypass or guaranteed count. See [exec approvals](https://docs.openclaw.ai/tools/exec-approvals).

This kit does not implement an admission helper or change its scaffold. The operator applies the reviewed configuration using the existing [runbook](install.md#3-generate-a-protected-disabled-profile).

## 5. Update, recover, and prove the result

1. **Prioritise reachable high-impact flaws.** Keep affected capabilities closed while resolving unsupported runtimes, exposed listeners, or failed data boundaries. Prefer a published supported fix over a local dependency rewrite; review the whole installed application/plugin combination.
2. **Before an approved update:** verify consistent backup coverage of config, credentials, sessions/databases, workspaces and external plugin stores. Record versions, install source, image digests and any local patch provenance privately. Confirm free space and test restoration in isolation; archive verification alone is insufficient.
3. **Apply the reviewed target in a maintenance window.** Update Node through the selected installation method and OpenClaw through its supported updater. For this dated baseline, preview `openclaw --profile minisamantha update --tag 2026.10.6 --dry-run`, then, only after approval, use the same command without `--dry-run`. Verify the service's runtime; allow for managed activation/restart behavior rather than treating `--no-restart` as a blanket guarantee.
4. **Docker:** the starter uses Docker for tool sandboxes; replacing that image does not patch a native host gateway. Rebuild or pull each affected image from a corrected base, verify its digest/runtime, and recreate the corresponding containers. If an operator separately runs the gateway in Docker, its gateway image needs the same treatment. A container restart alone keeps the old runtime.
5. **Rollback:** keep channels closed on a failed upgrade. Restore a mutually compatible application/plugin/config/state set using the release's recovery procedure and an isolated restore test first. Keep a patched supported Node where compatible. If recovery requires a vulnerable runtime or unresolved data migration, remain offline rather than reopening channels. Retain evidence; do not delete state to make startup succeed.
6. **Verify after activation:** repeat the diagnostic commands above, run `openclaw --profile minisamantha config validate` and `openclaw --profile minisamantha channels status`, and repeat the [acceptance tests](acceptance.md). Check actual process/image identity, authentication/listeners, effective tools, sandbox failure behavior and memory canaries. Have an authorized person send a fresh native mention and confirm the answer targets that message; also test denied senders and quote-only activation. Health/RPC checks and offline tests do not prove channel behavior.

Record `PASS`, `FAIL`, or `NOT RUN` with redacted evidence. Recheck local patches and optional extensions after every upgrade; do not infer compatibility from a successful install or reuse a version-specific patch blindly.
