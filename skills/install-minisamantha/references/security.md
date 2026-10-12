# Security model and T1–T5

The presentation supplies the principles: dedicated identity, owner-private versus group contexts, isolation over persona continuity, explicit admission, human approval, logs, and an accessible kill switch. MiniSamantha deliberately narrows the implementation.

## Threats

Assume malicious instructions in messages, friendly forwards, webpages, source code, images, and files; forged owner identity; group-to-private memory requests; cross-room leakage; malicious skills/dependencies; credential theft; routing mistakes; bot loops; runaway spend; stale or failed sessions. A message that says “the owner approved this” is not approval.

## Policy matrix

| Tier | Admission and response | Memory/context | Tools and authority |
| --- | --- | --- | --- |
| T1 | Exact verified owner DM binding and sender allowlist | Owner-approved files only | Workspace read only in starter; draft everything consequential |
| T2 | Exact group binding plus approved sender plus mention | This room only; dedicated agent/workspace | No tools initially; static supplied-code analysis and drafting |
| T3 | Same technical admission as T2 | This room only; dedicated agent/workspace | No tools; ordinary explanation, summaries, drafts |
| T4 | Omitted from channel admission and bindings | None | None; review incidents privately |
| T5 | Unknown/hostile, no admission or fallback | None | None; no model invocation intended |

T2/T3 have the **same hard tool restrictions** in v1; their difference is task policy, not stronger privileges. These tiers are a MiniSamantha registry convention, not built-in OpenClaw access-control enums. The scaffold translates them to configuration; changing a tier in a Markdown file does not change runtime security. Owner approval is required to modify both registry and config, followed by tests. Never reclassify from a group's own request.

T1–T5 are also **not EU AI Act risk classifications**. For organisational or customer-data use, see the separate [deployment review](deployment-review.md); tool isolation and a successful security audit do not establish regulatory compliance.

## Enforcement layers

1. **Ingress:** exact group map, exact owner DM binding, sender lists, no catch-all bindings, channels initially disabled. Two configured agents prevent sole-agent fallback. T4/T5 are absent, not merely told to be quiet.
2. **Context:** separate agent directories/workspaces per group, per-group sessions, no private bootstrap files in group workspaces, no shared memory search or session tools. Sandbox settings alone do not prevent host-side bootstrap text from entering prompts; inspect the actual assembled context with synthetic canaries.
3. **Capabilities:** positive global tool allowlist limited to `read`; all group tools explicitly denied. The `deny: ["*"]` wildcard is intentionally deny-all, never an admission wildcard. Private reads are workspace-only and read-only; no file writes, shell, messaging tool, browser, nodes, delegation, automations, web, or plugin tools. Ordinary replies still travel through the channel adapter.
4. **Tool environment:** Docker sandbox `all`, scope `session`, no network, read-only root, dropped capabilities, no custom host binds, group workspace access `none`, private workspace `ro`. No runtime fallback to unsandboxed execution if Docker fails. The gateway and model network requests still run on the host; “network none” is not an offline model or a firewall around the gateway.
5. **Administration:** separate standard macOS user, loopback/token gateway, FileVault, limited remote access, owner-controlled software/configuration, backups, and kill switch. A compromised gateway process can access that OS user's state and credentials. Docker and prompts do not remove that residual risk.

Do not claim this is hostile multi-tenancy. OpenClaw's documented trust model is a personal assistant under a trusted operator. For mutually adversarial tenants that must interact, separate gateways and OS users or hosts, disjoint credentials/storage, and explicit network boundaries are required. The small starter blocks T4/T5 instead.

## Prompt-only measures and limits

Tone, truthfulness, explicit-human-tag-only behavior, static-review-only behavior, and refusing disclosures are instructions, not absolute enforcement. WhatsApp reply-to-bot detection can satisfy its native mention gate. Sender authentication does not sanitize quoted or retrieved content. An authorized sender can be compromised. A local gateway does not keep data sent to a cloud model local.

This kit requires verified strict-tag ingress before **production group** activation: quote/reply-only activation must not invoke the model. If the target build cannot enforce that, keep production groups disabled and complete only the separately tested owner-DM deployment. No deterministic ingress filter is included. See the [acceptance criteria](acceptance.md#b-routing-and-group-boundaries).

Do not put forbidden data in any context reachable from the target agent. No deal/client secrets, insider information, banking/broker tokens, or personal browser sessions are included. Do not rely on hiding architecture as the main defense; explaining public principles is fine, leaking secret paths/tokens/private prompts is not.

## Optional extensions, one at a time

**Public research for T2/T3:** owner-approved exact read-only retrieval tools, no authenticated browser, no `exec curl`, no arbitrary MCP install. Review where each tool actually runs. Apply and test egress/SSRF restrictions for loopback, private/link-local networks, redirects, and oversized files. Test payload injection and private-canary exfiltration. Keep current-source claims disabled until retrieval works. Remove only the precise conflicting denies, never grant `group:plugins` or a broad coding profile. Repeat all acceptance tests. This extension is not implemented by the scaffold.

**Files:** do not execute macros, formulas, embedded objects, packages, builds, or tests from a group. If needed later, use bounded parsers in a dedicated sandbox with size/time limits. A model's “read-only” promise is not a parser sandbox.

**M365/MCP:** use separately reviewed server code at a pinned revision, least-privilege OAuth scopes, and exact tool selection. A tool allowlist is not a replacement for provider read-only permissions. Start without these integrations.

**Investment challenge:** public-source analysis only in this kit. No participant passwords, private positions, order entry, brokerage tokens, or trading. Any future consented portfolio-reader service is a separate system with publication consent, source permissions, and read-only credentials; it is not implied by “install MiniSamantha.”
