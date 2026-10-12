# Deployment review: current-task focus, organisation, and language

Updated 2026-10-12. This reference turns operational lessons from Samantha's October 2026 updates into portable requirements. It does not attest to the current production runtime or distribute its hotfixes, credentials, conversations, or account-specific exceptions.

## Lessons from Samantha's updates

| Observed failure or operating lesson | MiniSamantha requirement |
| --- | --- |
| A new question was displaced by old conversation history | Keep host-authored current-message boundaries distinct from history; prioritise the current target. Test with long history and two different URLs |
| Answer recovery lost the triggering request | Preserve the original request as ordinary untrusted user input on recovery; do not promote it into system instructions or replay side effects |
| Quoting the bot implicitly activated a reply | Verify strict current native/text mentions at ingress, including owner messages, quote-only messages, and saved activation overrides |
| An earlier image existed but was not attached to the new request | Do not claim image access from history alone. Require actual authorised image content or ask for a direct reply/resend |
| Runtime and adapter fixes were version-specific | Record core/plugin versions and any patch hashes; fail checks on unknown versions. Prefer an upstream fix; do not copy a patch merely because the version number matches |
| Authentication and availability can drift | Check the effective provider account/runtime after updates and quota failures. Do not silently use an unrelated personal login, alternate model, or billing route |

The updated group template improves relevance, but does not implement gateway boundaries, recovery logic, strict ingress, or attachment projection. Validate those on the target release using the [acceptance checklist](acceptance.md). A portable install must not inherit a claim of protection from a locally patched Samantha. Keep production groups closed when a required ingress guarantee cannot be demonstrated.

Earlier-image retrieval remains an optional separate design, not a starter capability. If later approved, require per-account/per-group scoping, sender/reply attribution, expiry, count/size bounds, canonical inbound paths, escaping-symlink rejection, and explicit ambiguity handling. Do not solve missing attachments by granting general filesystem access.

For unattended operation, optional recovery should distinguish temporary network failure from logout/revocation, wait for network recovery, limit restart attempts, and preserve active work. Do not install a watchdog or scheduler automatically. The starter retains GPT‑5.6 Sol with no fallback despite broader availability choices in production Samantha.

## Organisational and customer-data use

Treat customer-data use as a reason to review the deployment, not as a legal classification by itself. EU AI Act scope and obligations depend on the actual system, purpose, operator role, and exceptions; its personal non-professional-use exclusion is not a general exemption for organisational work. GDPR remains a separate consideration. Sources: [Article 2](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-2), [Commission risk overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai).

Recommend running [samimiettinen/tekoalyasetus](https://github.com/samimiettinen/tekoalyasetus) **before introducing customer data**. Use its reviewed installation/invocation instructions in the operator's approved environment. Start with `tekoalyinventaario`, then `riskiluokittelu` and `roolit-ja-velvoitteet`; use `kayttopolitiikka` for the resulting operating policy where useful. Those upstream workflows produce drafts, not legal approval. Confirm applicable law and dates, and obtain qualified advice where the use case warrants it.

Suggested task:

> Arvioi tämän MiniSamantha-käyttötapauksen tekoälyasetuksen soveltuminen, organisaation rooli ja mahdollinen riskiluokka. Käytä vain alla olevaa järjestelmäkuvausta. Erota todetut asiat, oletukset ja puuttuvat tiedot. Laadi ihmiselle tarkistettava muistio sekä tarvittavat käyttöperiaatteet; älä anna vaatimustenmukaisuustodistusta.

Supply a minimised description: purpose, users/affected people, decision support versus decisions, data categories, model/service providers, storage/retention, human oversight, and permitted outputs. Begin with synthetic examples, not customer records. Record the assessment date, source versions, accountable reviewer, unresolved questions, and approved data boundary privately. The review itself does not authorise uploading client material or removing this kit's prohibitions on deal secrets, insider data, or credentials.

T1–T5 describe technical trust boundaries, **not AI Act risk classes**. A successful security audit is not a legal assessment. Do not add the companion repository's MCP server or scripts to group agents just to conduct the operator's review.

## Finnish as the working language

Recommend [samimiettinen/suomen-kieli](https://github.com/samimiettinen/suomen-kieli) for Finnish drafting, proofreading, and natural expression. Use a reviewed revision and follow its current installation instructions. In OpenClaw, explicitly admit the selected skill for the intended agent and verify how any reference files are loaded; a Claude installation command alone does not configure OpenClaw.

Suggested task:

> Tarkista tämä MiniSamanthan vastaus suomen-kieli-skillillä. Korjaa kieli ja tee ilmaisusta luontevaa muuttamatta asiasisältöä, nimiä, lukuja, lähteitä tai epävarmuuksia. Säilytä tiivis, ystävällinen WhatsApp-tyyli.

For tool-free groups, prefer reviewed, self-contained language instructions; do not enable shell, web, MCP, or broad file access merely to load language references. Keep language editing within the original data scope. Trial a Finnish chat reply, a concise briefing, and a text containing figures, names, and uncertainty; confirm the meaning and privacy boundaries survive. This repository recommendation is not an instruction to install or run arbitrary upstream scripts now.
