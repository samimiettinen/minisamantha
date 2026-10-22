# MiniSamantha

A deliberately limited AI employee for a Mac mini: **OpenClaw + GPT‑5.6 Sol**, a separate identity, local file-based memory, and T1–T5 trust boundaries. No MemoriLabs, trading access, personal browser sessions, or autonomous publishing.

This is an **operator-invoked installation skill and starter kit**, not a security product or a clone of Samantha's private installation. It prepares a separate deployment; it does not modify an existing Samantha. Source repository: [samimiettinen/minisamantha](https://github.com/samimiettinen/minisamantha).

**Security guidance refreshed — 2026-10-22:** use a reviewed, patched OpenClaw/Node combination before activation. The dated baseline is **OpenClaw 2026.10.6 with Node 24.22.1+ on the 24 line or 26.12.1+ on the 26 line**; prefer the supported patched Node 24 LTS line. Recheck upstream before installing. See the [security maintenance checklist](skills/install-minisamantha/references/security-maintenance.md) for sources, actual-process verification, dependency review, and recovery.

**Verification status:** not independently security-certified or live-deployment audited. **T1–T5 are this project's conventions, not built-in OpenClaw security classes.** Offline checks do not prove that a running gateway enforces them. See [validation evidence and untested boundaries](VALIDATION.md) and [private vulnerability reporting](SECURITY.md).

| Compatibility item | Evidence / limitation |
| --- | --- |
| OpenClaw 2026.9.8 | Scaffold schema and disabled-profile audit checked on 2026-10-10; historical reference, not a current security recommendation |
| OpenClaw 2026.10.2 | Local CLI version and channel-login help inspected on 2026-10-12; no full deployment compatibility test |
| OpenClaw 2026.10.6 / patched Node 24 or 26 | Published release and npm engine requirement checked on 2026-10-22; security installation baseline, not a new live compatibility certification |
| `openai/gpt-5.6-sol` | Intentional fixed model; verify access in the actual account/runtime; no fallback if unavailable |
| Live WhatsApp, model, sandbox, restore | Operator acceptance tests required; not established by this repository's CI |

Version and model information ages quickly. Check the target release and advisories before installing; a newer version number alone does not establish compatibility or safety.

## What you get

- [Installation skill](skills/install-minisamantha/SKILL.md): staged setup, approval gates, and handover.
- [Mac mini runbook](skills/install-minisamantha/references/install.md): prerequisites, model login, WhatsApp, backups, and restart recovery.
- [T1–T5 policy](skills/install-minisamantha/references/security.md): enforced controls versus behavioral instructions.
- [Memory without MemoriLabs](skills/install-minisamantha/references/memory.md): transcripts, source-backed wiki, a small file graph, and portable records.
- [Recommended extensions](skills/install-minisamantha/references/recommended-extensions.md): transcript-first YouTube reading and Lossless Claw context management, with scoped rollout and tests.
- [Security maintenance](skills/install-minisamantha/references/security-maintenance.md): patched runtimes, dependency exposure, bounded approvals, and update/restore checks.
- [Deployment review](skills/install-minisamantha/references/deployment-review.md): context and recovery requirements, organisational-use checks, and Finnish language quality.
- [Acceptance tests](skills/install-minisamantha/references/acceptance.md): positive and negative tests required before enabling groups.
- [First jobs](skills/install-minisamantha/references/first-jobs.md): four starter playbooks, from guest question sets to research notes, so the deployment does real work within the same limits.
- A standard-library Python scaffold tool, persona/policy templates, and offline regression tests.

## Small by design

| Tier | Context | Starter capability |
| --- | --- | --- |
| T1 | Verified owner, private DM | GPT‑5.6 Sol; read approved private workspace; draft work and memory updates |
| T2 | Explicitly admitted collaboration group | Same main model; tagged, reply-only analysis of supplied text/code |
| T3 | Explicitly admitted ordinary group | Tagged questions, summaries, and drafting from that room's text |
| T4 | Restricted / abusive context | No admission or reply; owner reviews separately |
| T5 | Unknown / hostile context | No admission, model call, tools, or memory access |

These are **security contexts, not rankings of people**. A familiar person in a group does not get T1 powers. T4/T5 blocking is a conservative MiniSamantha design choice; the presentation's tier labels are not a complete technical specification.

Production groups stay disabled until strict-tag ingress tests pass, including no model call on quote/reply-only activation. A prompt instruction is not that filter, and this kit ships no ingress patch. Owner-only DMs can be deployed separately after their own acceptance tests pass.

The starter has no autonomous file writes, shell, web fetching, MCP servers, or cross-session tools. The operator maintains memory from proposed patches. A later read-only public-research extension is described, but is **not enabled**. Replies to an admitted request are the only routine external output. A human publishes drafts elsewhere.

Recommended next additions are a **YouTube reading skill** that summarizes verified transcripts, and **Lossless Claw** for retaining and retrieving compacted conversation history. Neither is bundled, installed, or enabled automatically. Start in T1; extend YouTube reading to selected T2/T3 rooms only after isolation tests. Lossless context must never become a shared private/group memory pool. See the [extension guide](skills/install-minisamantha/references/recommended-extensions.md).

## Seven rules, and where the kit implements them

From the talk *What Samantha does all day — and what I never let her touch*. **Config** means the scaffold sets it and tests check it; **behavioral** means a prompt instruction, not a guarantee; **procedure** means the operator does and records it.

| Rule | In this kit | Type |
| --- | --- | --- |
| 1. Give the agent its own identity | Separate standard macOS user, new named profile, its own WhatsApp number; never the owner's Apple ID, browser, or email | Procedure; operator acceptance test required |
| 2. Treat every group chat as untrusted input | One agent and workspace per admitted group, all group tools denied, no private files in group workspaces | Config, plus behavioral refusals |
| 3. Isolation beats personality. Fail closed | No model fallbacks, T4/T5 absent from routing, an unbound placeholder agent prevents fallback into T1 | Config |
| 4. Explicit allowlists, no wildcards | Exact owner and group bindings, sender lists, wildcard and malformed IDs rejected by the scaffold | Config |
| 5. She drafts. You press | No send, publish, write, or shell tools; memory changes as diffs the operator applies; every playbook ends with a human step | Config, plus behavioral |
| 6. Logs over config. Verify every change live | Acceptance checklist with recorded evidence, handover record, rerun after every change | Procedure |
| 7. Keep a kill switch you can reach in the dark | [Three levels](skills/install-minisamantha/references/install.md#kill-switch-three-levels): stop, cut network, cut power, from an independent device | Procedure |

## Put it to work

Safe and idle is still a chatbot with a name. After the owner DM passes its tests, run one [starter playbook](skills/install-minisamantha/references/first-jobs.md) on non-sensitive material: a question set for a guest, a devil's advocate memo before a decision, a newsletter draft from transcripts, or a research note. The scaffold copies the playbooks into the owner workspace; the owner agent reads them with its existing read-only tool. Review five outputs a week against each playbook's quality bar and improve the playbook, not the permissions.

## Start here

**A small organisational-use caution:** using this installation with an organisation's customer data may bring the deployment and its operator under EU AI Act obligations. Customer data alone does not determine scope or make a system high-risk: purpose, role, and applicable exceptions matter. Do not assume the personal, non-professional-use exception covers organisational work; assess GDPR and confidentiality separately. See the Commission's [scope guidance](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-2) and [risk overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai). This is a setup reminder, not legal advice.

Before customer-data use, **run a use-case review with [samimiettinen/tekoalyasetus](https://github.com/samimiettinen/tekoalyasetus)** in the operator's approved environment, starting from a minimised system description rather than raw customer records. If the working language is Finnish, **use [samimiettinen/suomen-kieli](https://github.com/samimiettinen/suomen-kieli)** for drafting and final language review. These are recommended companion workflows, not automatically installed dependencies or compliance certification. See [how to use them](skills/install-minisamantha/references/deployment-review.md).

Read the skill and runbook first. You need a separate standard macOS account, Docker-compatible runtime, a model account with actual GPT‑5.6 Sol access, and a separate WhatsApp number if using that channel. Start with owner-only access, then one test group. A 16 GB Apple Silicon Mac mini is the baseline; no large local model is installed.

Use an operator-controlled OpenClaw workspace to install this skill at `<operator-workspace>/skills/install-minisamantha/`. Copy the **whole** `skills/install-minisamantha` directory, not only `SKILL.md`. If the operator agent has a skill allowlist, explicitly add `install-minisamantha`. Do not install this operational skill into group-agent workspaces or broaden their permissions to run it. Ask the operator agent:

> Use install-minisamantha to plan a new Mac mini installation. Inspect only until I approve the exact target profile and installation steps. Keep GPT‑5.6 Sol, exclude MemoriLabs, and fail closed for unknown groups.

For **Claude Code**, this repository includes a project-local `/install-minisamantha` wrapper. Open the repository in Claude Code, review its workspace-trust prompt, and invoke the command explicitly. Claude Code is the supervised installer; OpenClaw remains the deployed gateway, and GPT‑5.6 Sol remains its brain. Do not use permission-bypass flags. The wrapper has been statically checked, not exercised in a live Claude Code session.

For a manual installation, follow the [runbook](skills/install-minisamantha/references/install.md).

For WhatsApp, follow the runbook's [QR linking steps](skills/install-minisamantha/references/install.md#qr-linking-operator-terminal-only). QR linking connects the bot's separate WhatsApp account; it does **not** authorize an owner or a group. Admission is tested separately, first owner DM and then one test group.

## Check the kit locally

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic identities and temporary directories. They do not call a model, start a gateway, link WhatsApp, install packages, or change your running agent.

Historical scaffold schema reference: OpenClaw **2026.9.8**, **not a version to install from this guide**. Use the patched installation baseline above, validate the generated configuration against that release, and complete the live acceptance tests before activation. See [sources and limitations](skills/install-minisamantha/references/sources.md).

Quality refresh, 2026-10-12: the group template now prioritises the current request over history, distinguishes old media from current attachments, and instructs recovery to use the retained original request. The runtime must actually retain that request. New acceptance scenarios cover these failures and strict mentions. Samantha's version-specific runtime hotfixes and broader production permissions are **not** included; prompt improvements alone do not establish those runtime guarantees.

## Public repository hygiene

Publish only this kit, never a generated profile, `.openclaw` directory, conversations, credentials, real participant lists, or the source presentation. `.gitignore` is defense in depth, not a secret scanner. Review the exact files before each publication.

Run the [publication checks](PUBLICATION.md) before pushing: scan the complete fetched Git history, working tree, and commit metadata. CI repeats these checks using a pinned scanner. Never upload scanner findings containing private data as public artifacts. A clean scan is not proof of anonymity or a security audit.

## License

MIT © 2026 Sami Miettinen. See [LICENSE](LICENSE). The license covers this kit's code and documentation. It does not cover the source presentation, OpenClaw, model providers, or other third-party material referenced here.

The source presentation is not distributed. The MIT notice is not evidence of rights to third-party material or names; before adding such material or making endorsement claims, the maintainer must record the appropriate permission. See [publication responsibilities](PUBLICATION.md#rights-and-attribution).

## Suomeksi

MiniSamantha on aloituspaketti tarkoituksella rajatulle tekoälytyöntekijälle Mac minillä. Se perustuu Samanthan, Neuvottelija-podcastin tekoälytyöntekijän, rakenteeseen, mutta on pienempi ja varovaisempi: OpenClaw, GPT-5.6 Sol, oma macOS-käyttäjä ja WhatsApp-numero, paikallinen tiedostopohjainen muisti ja luottamustasot T1–T5.

- **T1** on omistajan yksityisviesti. MiniSamantha lukee hyväksyttyä työtilaa ja luonnostelee, mutta ei kirjoita tiedostoja, lähetä viestejä eikä julkaise.
- **T2 ja T3** ovat erikseen hyväksyttyjä ryhmiä. MiniSamantha vastaa vain, kun hänet mainitaan, eikä hänellä ole työkaluja eikä pääsyä yksityiseen muistiin.
- **T4 ja T5** eli rajoitetut ja tuntemattomat ryhmät eivät pääse läpi lainkaan.

Paketissa on asennusskilli Claude Codelle ja OpenClawille, asennusohje, hyväksymistestit ja neljä aloitustehtävää: kysymyspatteri vieraalle tai kokoukseen, paholaisen asianajajan muistio päätöksen tueksi, uutiskirjeluonnos ja tutkimusmuistio. Ne tekevät oikeaa työtä alusta asti avaamatta uusia oikeuksia. MiniSamantha luonnostelee, ihminen painaa nappia.

Aloita lukemalla skilli ja asennusohje. Ota käyttöön ensin pelkkä oma yksityisviesti ja sitten yksi testiryhmä. Jos käsittelet organisaation asiakasdataa, arvioi käyttötapaus ensin [Tekoälyasetus-työkalupakilla](https://github.com/samimiettinen/tekoalyasetus). Suomenkielisiin vastauksiin sopii [Suomen kieli -skill](https://github.com/samimiettinen/suomen-kieli).

Aloituspaketti ei ole tietoturvatuote eikä oikeudellista neuvontaa. Lisenssi on MIT.
