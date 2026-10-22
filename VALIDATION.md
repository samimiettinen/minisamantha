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

Base revision: `5422569e9d9300c3f9cbc0b326a39a8fe2f157a1`, plus this guidance and publication-check change. Reviewer role: implementing AI assistant; no independent human or live deployment audit. Public Node.js release information, OpenClaw's published 2026.10.6 release/npm engine metadata, and upstream operator documentation were checked. The installation example now selects 2026.10.6 with a supported patched Node line instead of the historical 2026.9.8 schema reference.

Added a maintenance checklist for actual service runtimes, installed dependency reachability, host-side memory hooks, bounded operator approvals, image replacement, backup/rollback and channel verification. Linked it from the installer and existing controls, and extended the operator acceptance checklist. The scaffold code, generated model/tool/sandbox/routing configuration, persona and playbooks are unchanged. No private deployment configuration, identifiers, logs, conversations or runtime patches were added.

- All 27 offline tests passed with the pinned Gitleaks scanner available, including privacy checks and all eight scanner integration tests; no skipped tests.
- The first PR check exposed an existing email-policy false positive for GitHub's temporary merge committer. The publication checker now accepts only the exact public system noreply address in addition to user noreply addresses. Regression tests reject lookalike addresses and a private author even when the committer is the allowed system identity; secret scanning still covers the entire commit.
- Gitleaks 8.30.1 from the verified official macOS arm64 archive passed the full fetched base history, changed working tree, commit metadata and noreply email policy with zero findings. Final-commit scanning and the published CI run identify the exact revision being released. These checks do not establish anonymity or runtime security.
- The documentation diff and relative links were reviewed, and whitespace checks passed. Published stable fixes, dated minimums, procedural recommendations and unverified deployment behavior are labeled separately.

New-release scaffold schema validation, live model/channel/group isolation, optional plugin behavior, Docker containment and restore tests: **NOT RUN** in this documentation refresh. The earlier compatibility evidence remains historical. Complete the updated acceptance checklist on the chosen release before activating a deployment.

## Disposable CLI and credential checks — 2026-10-22

Base revision: `f05c10c40dfcf6e33e96662f8f7724468822df8a`, plus this local-check/scaffold update. Reviewer role: implementing AI assistant; no independent external human audit. The exact tested checker/scaffold bytes have combined SHA-256 `55f19828fc9863408bf4f5ba7e845459076bd98ed8d9903d344ee541b3e5ece4` (scaffold bytes followed by checker bytes). The published commit and CI identify the complete repository revision.

New profiles use a file-backed gateway SecretRef and explicitly disable system browser-profile import. Added an optional local checker and plain-language warning dispositions. Model, agent tool restrictions, sandbox policy, loopback binding, disabled heartbeat cadence, and closed channels are preserved. Production groups still require verified ingress tests; no custom runtime patch, new GitHub workflow, scheduled scan, or repository rule was added. No private deployment material was included.

The actual CLI run used official Node **24.22.1** on macOS arm64 (download checked against the official SHA-256 manifest) and isolated npm OpenClaw **2026.10.6**, CLI build `fe06181`. Package install scripts and optional dependencies were omitted for this disposable CLI-only test. No existing installation was updated, gateway started, channel linked, or model authenticated. Synthetic state covered owner, unbound placeholder, T2 and T3 agents, with all channels disabled.

| Check | Result | Observed evidence |
| --- | --- | --- |
| `config validate --json` | `PASS` | Exit 0, valid config, no schema warnings |
| `secrets audit --check --json` | `PASS` | Exit 0; one reference resolved; zero plaintext-config, unresolved, shadowed or residue findings |
| Secret file missing / mode 644 / symlink | `PASS` (rejection tests) | Each separate synthetic case returned exit 2, `REF_UNRESOLVED`, one unresolved reference; normal private file returned exit 0 |
| `doctor --lint --json` | `WARN` | Exit 1; 36 checks run, 30 skipped, 10 warning findings: browser-import-disabled (1), disabled heartbeat rows (4), loopback node hosting (1), restricted skill workshop (4) |
| `security audit --json` | `WARN` | Exit 0; 0 critical, 1 warning (`gateway.trusted_proxies_missing`), 1 informational attack-surface finding |
| Overall local check | `REVIEW` | Exit 1; warnings remain visible and no repair was applied |
| Offline suite | `PASS` | 38 tests, no skips, including secret-file permissions/non-disclosure, isolated environment, failure handling and all eight scanner integration tests |
| Live gateway/model/WhatsApp/strict mentions | `NOT RUN` | No inference from CLI/schema checks to live admission behavior |
| Docker execution, restore, Node 26 runtime | `NOT RUN` | Configuration and upstream requirements are not execution evidence |

See [warning dispositions](skills/install-minisamantha/references/local-check.md#read-the-result). Doctor's skipped checks are not passes. The clean credential result means no plaintext credential was found in the scanned config stores; the separate secret file itself is plaintext protected by local permissions and disk encryption. Missing/permissive/symlink tests verify resolver rejection, not a live gateway startup or authentication exchange.

Publication uses the existing pinned Gitleaks 8.30.1 full-history/working-tree/metadata checks and privacy/link tests; the final-commit scan and existing CI record their result against the published revision. No new automated infrastructure is needed by an ordinary installer. External independent human review and live deployment acceptance remain **NOT RUN**.
