# Security policy

MiniSamantha is a limited installation starter, not an audited security product. The repository's tests cover code and documentation; live model, channel, sandbox and restore tests remain the operator's responsibility. T1–T5 are project conventions, not OpenClaw security classifications.

## Report a vulnerability privately

Use [GitHub's private vulnerability reporting form](https://github.com/samimiettinen/minisamantha/security/advisories/new). Private reporting was verified enabled on 2026-10-12. Do not open a public issue with exploit details or sensitive evidence. If the form is unavailable, do not fall back to publishing the details; wait for the private route to be restored.

Include:

- the affected commit and OpenClaw/plugin versions;
- expected versus observed behavior and the security impact;
- minimal reproduction steps using synthetic identities and disposable profiles;
- whether the issue is in this kit's configuration/guidance or in an upstream component.

Never send passwords, tokens, login QR codes, real phone/group identifiers, customer records, or complete conversations, even in the initial private report. Offer a redacted reproduction instead. Revoke any exposed credential from a trusted device. Do not probe other people's accounts, production gateways, or third-party services without their authorization.

## Scope and response

Reports are reviewed against the current `main` revision. Historical version pins are compatibility evidence, not promises of upstream support or security updates. There is no guaranteed response time, paid support commitment, or bug bounty. The maintainer coordinates fixes and disclosure case by case; upstream defects should also use the upstream project's private reporting process.

If a boundary fails in a deployment, close the affected channel/capability and preserve evidence privately. Do not relax tool, sender, model, or sandbox restrictions to make a test pass. See the [acceptance checklist](skills/install-minisamantha/references/acceptance.md) and [incident/stop procedure](skills/install-minisamantha/references/install.md#kill-switch-three-levels).
