# Kit validation

Date: 2026-10-10. This is a validation of the **starter kit**, not a deployed MiniSamantha.

- Thirteen Python tests passed: ten scaffold tests (requested model/empty fallback lists; initially disabled channels; T4/T5 absence; no sole-agent fallback; separate group workspaces and tool denial; sandbox defaults; invalid identity/tier rejection; duplicate/extra-field rejection; private file permissions/no overwrite; symlink target refusal) and three packaging tests (relative links, manual Claude wrapper, and selected private-identifier checks).
- Portable `install-minisamantha` SKILL.md passed the skill-creator frontmatter/structure validator.
- A generated profile with synthetic owner and T2–T5 identities passed `openclaw config validate --json` on OpenClaw `2026.9.8`, with no schema warnings. Validation used explicit temporary state/config paths, not the running Samantha profile.
- A non-deep security audit of that disabled temporary profile returned 0 critical, 1 warning, and 1 informational finding. The warning concerns unconfigured trusted reverse proxies; the intended baseline stays loopback-only without a reverse proxy. This is not a live-host or active-channel audit.
- The Claude Code wrapper is a manual-invocation project skill; live invocation has not been tested.

Not run: provider authentication/inference, WhatsApp linking or message delivery, live group admission/isolation, sandbox execution, persistent service setup, reboot, backups/restore, or full host security review. The deployment acceptance checklist remains mandatory. No production configuration or channel was changed, and no repository was published.

## Quality refresh — 2026-10-12

Reviewed operational lessons from Samantha's October 2026 updates. Updated the generated group instructions for current-target selection, old-media handling, recovery, and attribution; added deployment acceptance scenarios for the corresponding runtime behavior and strict mentions. Added a brief AI Act caution plus operator-side tekoalyasetus and Finnish-language suomen-kieli recommendations, checked against upstream material and Commission guidance.

All 13 offline tests and the portable skill validator passed again. The scaffold code and model/tool/channel configuration were unchanged; schema validation and the temporary-profile audit above remain results from 2026-10-10, not new live checks. New behavioral scenarios, companion workflows, and the legal assessment itself have **not** been run. No production profile, patch, model, service, or external repository was changed.

## Work and licence refresh — 2026-10-12

Compared the kit with the core of Samantha's role as described in the October 2026 talk (pp. 3–4, 9, 11–13): an AI employee must be complex, repeatable, and reliable, and does recurring drafting work for its owner. Added four owner-only playbooks (question set, challenge memo, newsletter draft, research note), which the scaffold now copies into the owner workspace at mode 600; a `first-jobs.md` reference covering tiers, group jobs, sender-roster limits, and a weekly quality review; a seven-rules table in the README marking each rule as config, behavioral, or procedure; a three-level kill switch in the runbook; matching acceptance items; a Finnish summary; the MIT licence; and a GitHub Actions workflow running the offline tests.

All 16 offline tests passed (three new: owner-only private playbooks, playbook structure, licence present). The model, tool, sandbox, channel, and routing configuration is unchanged apart from the added owner-workspace files. Playbooks, kill-switch levels, and the new acceptance items have **not** been run on a live deployment; schema validation and the temporary-profile audit remain results from 2026-10-10.
