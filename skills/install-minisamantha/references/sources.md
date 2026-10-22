# Sources, compatibility, and deliberate deviations

Prepared 2026-10-10; quality, companion-workflow, and first-jobs review updated 2026-10-12; public security sources refreshed 2026-10-22. Product details change: recheck the installed version and authoritative documentation before executing an installation. This kit contains newly written templates and policies, not private source files or a redistribution of the presentation.

## User-supplied design sources

- Sami Miettinen, **What Samantha does all day — and what I never let her touch**, Vibe Coding Finland meetup, Verk, 7 October 2026, 17-page presentation. Especially pp. 3–4 (the three tests and her daily work, which shaped the starter playbooks), pp. 6–8 (tiers, routing, boundaries), p. 9 and p. 15 (the box and the kill switch), p. 11 (memory), pp. 12–13 (rules/starter), pp. 14–15 (Q&A).
- Operating experience from the author's own Samantha deployment and the installed OpenClaw 2026.9.8 documentation informed the conservative policy. No real group IDs, owner contact data, credentials, operational configs, or private memories are copied into this kit.
- Operational lessons from Samantha's October 2026 updates on context, recovery, strict mentions, and image attribution informed the 2026-10-12 refresh. Their portable lessons and new acceptance scenarios are included; version-specific runtime patches and production privileges are not. The documented production results were not rerun as part of this documentation update.

Presentation claims are historical design context, not evidence that a new deployment has the same controls. The talk describes both a compact two-agent architecture and stronger separate-machine isolation in Q&A; this kit does not claim one Mac with Docker reproduces the latter. Historical prices, hardware aspirations, and red-team results are not guarantees or current product specifications.

## Authoritative implementation references

- [OpenClaw hardened baseline](https://docs.openclaw.ai/gateway/security/hardened-baseline) and [security overview](https://docs.openclaw.ai/gateway/security): local authentication, tool restrictions, requester controls and trust boundaries.
- [Per-agent entries and routing](https://docs.openclaw.ai/gateway/config-agents/entries-and-multi-agent): `agents.entries`, exact peer bindings, explicit ownership, and multi-agent behavior.
- [Tool policy](https://docs.openclaw.ai/gateway/config-tools/tool-policy): allow/deny precedence, tool groups, and sandbox gates.
- [Docker sandbox](https://docs.openclaw.ai/gateway/sandboxing/docker-backend) and [image setup](https://docs.openclaw.ai/gateway/sandboxing/images-and-setup): tool containment and host/runtime limitations.
- [WhatsApp](https://docs.openclaw.ai/channels/whatsapp): room admission, sender authorization, account overrides, mention/reply activation, and self-chat behavior.
- [OpenClaw skills](https://docs.openclaw.ai/tools/skills): workspace skill discovery and per-agent allowlists.
- [OpenClaw context engines](https://docs.openclaw.ai/concepts/context-engine) and [Lossless Claw](https://github.com/martian-engineering/lossless-claw): recommended optional context management, not a preinstalled component or a security audit.
- [YouTube transcript plugin candidate](https://github.com/JonFerminBot/openclaw-youtube-transcript) and [yt-dlp](https://github.com/yt-dlp/yt-dlp): upstream references for a reviewed transcript retrieval backend. Documentation inspected; code/dependencies and MiniSamantha compatibility have not been audited or tested. No automatic installation is recommended.
- [OpenAI runtimes in OpenClaw](https://docs.openclaw.ai/providers/openai/runtimes) and [authentication](https://docs.openclaw.ai/providers/openai/authentication): model references, runtime selection and separate authentication/billing routes.
- [OpenAI GPT‑5.6 Sol documentation](https://developers.openai.com/api/docs/models/gpt-5.6-sol): official model identity. It does not establish access for a particular operator's account or subscription.
- [Backups](https://docs.openclaw.ai/install/backups), [updates](https://docs.openclaw.ai/cli/update), and [restart recovery](https://docs.openclaw.ai/gateway/restart-recovery): verify against the installed release before use.
- [Claude Code skills](https://code.claude.com/docs/en/skills): project-local skill wrapper and manual-only invocation.
- [Tailscale on macOS](https://tailscale.com/docs/install/mac): supported remote-administration installation choices.
- [tekoalyasetus](https://github.com/samimiettinen/tekoalyasetus): recommended operator-side organisational-use assessment workflows; documentation reviewed, not executed or certified here.
- [suomen-kieli](https://github.com/samimiettinen/suomen-kieli): recommended Finnish-language companion; upstream README and skill source consulted, not installed or runtime-tested here.
- [Commission AI Act scope guidance / Article 2](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-2) and [risk overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai): sources for the brief organisational-use caution, checked 2026-10-12. Reassess applicable law at deployment time; this kit supplies no legal opinion.

OpenClaw details above were checked against the documentation bundled with installed release `2026.9.8`; the web references are the corresponding live pages. Claude Code skill discovery/manual invocation and the exact GPT‑5.6 Sol model page were also checked online. Online docs can move ahead of that local version.

QR/publication refresh, 2026-10-12: local OpenClaw `2026.10.2` version and `channels login --help` inspected without starting login. The [current CLI guide](https://docs.openclaw.ai/cli/channels) and [WhatsApp guide](https://docs.openclaw.ai/channels/whatsapp) support the documented QR, profile/account, exec restriction and proxy caveats. This does not revalidate the scaffold against 2026.10.2 or exercise live login. Current documentation describes WhatsApp as a separately packaged plugin; when changing releases, verify that release's official plugin packaging/version rather than installing an unpinned dependency or assuming the historical layout still applies.

## Security-source refresh — 2026-10-22

- [Node.js October security release](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases): published fixes and release-line floors, including CVE-2026-111497. This is upstream vulnerability information, not evidence of exploitation in a MiniSamantha deployment.
- [OpenClaw v2026.10.6 stable release](https://github.com/openclaw/openclaw/releases/tag/v2026.10.6) and [exact npm package metadata](https://registry.npmjs.org/openclaw/2026.10.6): patched Node engine requirement and released Docker-runtime update. The npm `latest` tag resolved to 2026.10.6 on the review date; no beta/main-only change is presented as a released fix.
- [Plugin lifecycle and hooks](https://docs.openclaw.ai/tools/plugin), [exec approvals](https://docs.openclaw.ai/tools/exec-approvals), [update CLI](https://docs.openclaw.ai/cli/update), and [Doctor CLI](https://docs.openclaw.ai/cli/doctor): operator diagnostics and the distinction between tool policies, host hooks, and approval behavior.
- [OSV](https://osv.dev/) and [GitHub Advisory Database](https://github.com/advisories): lookup sources for exact installed dependencies; neither an exhaustive MiniSamantha bill of materials nor a clean deployment scan is claimed here.

The [maintenance checklist](security-maintenance.md) derives conservative operator requirements from these sources. The two-decision admission workflow is this project's procedural recommendation, not an upstream guarantee of prompt count. Deployment changes are guidance only: no additional runtime, plugin, tool, private configuration, or deployment-specific patch is included. A publication-check compatibility fix is recorded separately in [validation evidence](../../../VALIDATION.md). Live schema/channel/model/sandbox/restore validation on 2026.10.6 remains the operator's responsibility.

## What this kit does not claim

- No MemoriLabs: the optional file graph is a replacement data convention, not the same engine.
- Native transcripts plus backups by default; Lossless Claw and a transcript-first YouTube reader are recommended optional additions, not installed or live-tested components.
- Read-only owner tools and **zero group tools**, narrower than full Samantha.
- T4/T5 blocked, rather than interacting with hostile users.
- No browser automation, email, M365, eToro, media generation, specialist agents, or autonomous recurring tasks.
- No live channel, model, Docker-isolation, restore, or Claude Code execution certification from static tests. Those belong to the operator's acceptance run.

The skill-creation workflow influenced the packaging: a small operator workflow with separately loaded references, reusable assets, an explicit-invocation adapter, and an offline-tested scaffold. No safety claim depends on skill text alone.
