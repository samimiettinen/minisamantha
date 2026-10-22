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

## Publication hardening — 2026-10-12

Base revision: `220d52124253e04e37805c2f0d2605ba7213e0be` (the new public repository, two reachable commits), plus the publication-hardening working tree. Added SECURITY.md, full-history/working-tree/metadata scanning, QR linking instructions, version/evidence labels, rights-review responsibilities, and network-stop clarification. GitHub private vulnerability reporting was verified enabled. The scaffold and generated permissions/model/routing are unchanged.

- Gitleaks 8.30.1, verified official macOS arm64 archive: all reachable base history, the changed working tree, raw commit metadata and noreply email policy passed with zero findings. The pinned CI workflow repeats the scan on the published revision; its run identifies that exact SHA. Historical private archives, inaccessible old objects/caches and other people's clones are outside this scan.
- All 25 tests passed with the pinned scanner available; this includes clean-history success, detection of a deleted fake secret, an uncommitted fake secret, a secret on another branch, a fake secret in commit metadata, private-email rejection, and refusal of shallow history. Without the scanner, seven integration tests are explicitly skipped, not passed. The portable skill validator and whitespace checks also passed.
- An independent AI-assisted desk review found three documentation ambiguities: account/profile verification after QR login, conflicting strict-mention activation criteria, and shared npm-install destinations. All were corrected and rereviewed. This was not an external human audit and did not exercise a live gateway.
- OpenClaw 2026.10.2 version and channel-login help were inspected read-only. The earlier 2026.9.8 schema/audit evidence is historical; it was not repeated against the newer runtime. No QR login, model call, service or production configuration change was performed.

Live deployment acceptance, independent external human review and independent rights clearance: **NOT RUN / NOT ESTABLISHED**. The maintainer must resolve publication rights for any new third-party material or name/endorsement claims; automated review cannot approve them.

## Security guidance refresh — 2026-10-22

Base revision: `5422569e9d9300c3f9cbc0b326a39a8fe2f157a1`, plus this documentation change. Reviewer role: implementing AI assistant; no independent human or live deployment audit. Public Node.js release information, OpenClaw's published 2026.10.6 release/npm engine metadata, and upstream operator documentation were checked. The installation example now selects 2026.10.6 with a supported patched Node line instead of the historical 2026.9.8 schema reference.

Added a maintenance checklist for actual service runtimes, installed dependency reachability, host-side memory hooks, bounded operator approvals, image replacement, backup/rollback and channel verification. Linked it from the installer and existing controls, and extended the operator acceptance checklist. The scaffold code, generated model/tool/sandbox/routing configuration, persona and playbooks are unchanged. No private deployment configuration, identifiers, logs, conversations or runtime patches were added.

- All 25 offline tests passed with the pinned Gitleaks scanner available, including privacy checks and all seven scanner integration tests; no skipped tests.
- Gitleaks 8.30.1 from the verified official macOS arm64 archive passed the full fetched base history, changed working tree, commit metadata and noreply email policy with zero findings. Final-commit scanning and the published CI run identify the exact revision being released. These checks do not establish anonymity or runtime security.
- The documentation diff and relative links were reviewed, and whitespace checks passed. Published stable fixes, dated minimums, procedural recommendations and unverified deployment behavior are labeled separately.

New-release scaffold schema validation, live model/channel/group isolation, optional plugin behavior, Docker containment and restore tests: **NOT RUN** in this documentation refresh. The earlier compatibility evidence remains historical. Complete the updated acceptance checklist on the chosen release before activating a deployment.
