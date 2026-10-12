# Publication checks

These are operator/maintainer checks, never tools for the deployed MiniSamantha. Run them before pushing: public CI can detect an exposure after publication, not prevent the first disclosure. Do not merge an old clone's removed history back into the current repository.

## Full-history secret scan

Use a fresh full clone, or fetch all authorized branches/tags without a depth limit. The scan refuses shallow clones and scans all **locally reachable** refs, working-tree files, and commit metadata. It cannot inspect unfetched refs, GitHub caches, unreachable objects, deleted repositories, private archives, other people's clones, or LFS payloads not present locally. Git LFS and binary/archive additions need a separate review before publication.

Use official [Gitleaks v8.30.1](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1). Download into a private temporary directory, verify the archive SHA-256 **before extracting/running**, and retain that version for reproducibility:

| Official release asset | SHA-256 |
| --- | --- |
| `gitleaks_8.30.1_darwin_arm64.tar.gz` | `b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5` |
| `gitleaks_8.30.1_linux_x64.tar.gz` | `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb` |

Digests were checked against the official release metadata on 2026-10-12. Other platforms require reviewing their release asset/digest; do not substitute an unverified binary or `latest` tag. The scanner does not need model credentials or customer data.

From the repository root, using the verified binary's path:

```sh
python3 scripts/scan_publication.py --gitleaks /absolute/path/to/gitleaks
GITLEAKS_BIN=/absolute/path/to/gitleaks python3 -m unittest discover -s tests -v
```

The wrapper uses default Gitleaks rules with inline/repository exemptions disabled. It scans historical patches including merges, current files, and raw commit metadata, and rejects non-GitHub-noreply author/committer emails. Set repository-local Git author/committer email to your own GitHub-provided noreply address before committing; do not invent someone else's identity. Commit messages and names still require human privacy review.

Only tool version, HEAD, reachable-commit count and per-check finding counts are printed. Detailed redacted scanner results are temporary and deleted; no reports are uploaded as public artifacts. On failure, keep publication closed and reproduce locally with the pinned scanner in a private terminal; if retaining a detailed report, use an access-restricted location outside the repository. Do not paste it into an issue or broadly suppress findings. Scanner errors are failures, not clean results.

The [security workflow](.github/workflows/security.yml) fetches complete branch/tag history, verifies a pinned scanner archive, tests that a fake secret removed from the current file is still caught in history, and repeats the publication scan. This is a CI check, not a configured branch-protection rule or a claim of complete anonymity. Keep human review of identities, filenames, links, screenshots and publication rights.

## Rights and attribution

- The MIT license applies to this kit's code and documentation, not to the source presentation, third-party software, trademarks or external assets.
- The presentation is cited as design context, not bundled. Do not add slides, logos, private prompts or quoted source passages without the applicable permission.
- The maintainer must confirm and keep a record of rights for any contributed material and proposed use of the Samantha/MiniSamantha name. The repository does not establish exclusive name rights or third-party endorsement. No independent rights clearance is claimed here.
- Automated checks cannot determine ownership or grant permission. Keep unresolved rights questions explicit; do not mark them approved on the maintainer's behalf.

## Review and release evidence

Record the reviewed commit, date, scanner version/results, offline tests, reviewer role and unresolved findings in [VALIDATION.md](VALIDATION.md). Mark live model/channel/sandbox/restore tests and any external human review as `NOT RUN` unless actual evidence exists. See the [negative review checklist](skills/install-minisamantha/references/acceptance.md#independent-negative-review). For suspected vulnerabilities, use [SECURITY.md](SECURITY.md), not a public issue containing sensitive details.
