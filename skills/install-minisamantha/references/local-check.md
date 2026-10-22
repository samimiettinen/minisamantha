# Check the starter with your installed OpenClaw

After installing a reviewed Node/OpenClaw pair, run this optional check from the skill directory:

```sh
python3 scripts/check_install.py
```

It uses the installed Node executable and npm-style OpenClaw JavaScript entry point on `PATH`. If you manage several installations, select the intended pair explicitly:

```sh
python3 scripts/check_install.py \
  --node /absolute/path/to/node \
  --openclaw /absolute/path/to/openclaw.mjs
```

Only run trusted installed binaries. This is not an installer, an advisory scanner, or a sandbox for an untrusted CLI. The dated version gate accepts stable OpenClaw 2026.10.6 or newer and patched Node 24.22.1+ or 26.12.1+ on those respective major lines. Recheck upstream requirements; passing an old minimum does not establish that later vulnerabilities are fixed.

## What it does

The script generates a temporary profile with synthetic owner/T2/T3 identities, closed channels, isolated OpenClaw state/home/config paths, and a minimal environment without inherited provider credentials or `NODE_OPTIONS`. It runs:

```text
node --version
openclaw --version
openclaw config validate --json
openclaw secrets audit --check --json
openclaw doctor --lint --json
openclaw security audit --json
```

Every OpenClaw invocation uses the selected Node executable and disposable profile. No gateway is started, model called, account linked, package installed, or repair applied. The temporary profile is deleted afterward. Use `--scratch-dir /absolute/private/directory` to select an existing parent for temporary files, and `--json` for a report containing versions, a combined SHA-256 of the checker/scaffold source, statuses, finding IDs and counts. Raw CLI output and token values are withheld.

The report intentionally does **not** inspect or certify your running installation. It marks the service runtime, model authentication, live messages/mentions, Docker containment and backup restore `NOT RUN`. Complete the [operator acceptance tests](acceptance.md) for those. Deep audit belongs to that explicitly targeted deployment review; it is not used by this disposable check.

## Read the result

| Status | Meaning |
| --- | --- |
| `PASS` | This bounded CLI check met its criteria; live boundaries remain untested |
| `WARN` / overall `REVIEW` | Findings need review; the script has not repaired or suppressed them |
| `FAIL` | Unsupported/unverified version, invalid config, unresolved credentials, critical audit finding, inspection failure, or inconsistent CLI output |
| `NOT RUN` | No test evidence; never substitute this for a pass |

Exit code `0` means the bounded checks passed without warnings. Exit `1` means `REVIEW` or `FAIL`; exit `2` means the checker could not prepare the run. Inspect the statuses rather than treating every nonzero exit as an installation failure.

On the tested **OpenClaw 2026.10.6 / Node 24.22.1** combination, the fresh disabled starter returns `REVIEW`:

| Finding ID | Disposition for this exact starter |
| --- | --- |
| `core/doctor/browser` | Doctor reports even explicitly disabled system-profile import as a warning. Keep both browser enablement and `allowSystemProfileImport` false; do not import personal cookies |
| `core/doctor/heartbeat-cadence-migration` | Fresh state has no scheduler rows for the disabled heartbeats. `heartbeat.every: "0m"` is still supported. Keep it off; this check does not run Doctor fixes or initialize a gateway |
| `core/doctor/node-hosting-preconditions` | Loopback-only access prevents remote node hosting, which this starter does not need. Keep loopback binding |
| `core/doctor/skill-workshop-tool-policy` | The sandbox/tool limits prevent autonomous skill authoring. Keep those limits |
| `gateway.trusted_proxies_missing` | Expected only while access is direct loopback and there is no reverse proxy. Reassess if exposure changes; never trust arbitrary proxies |

These explanations apply to the exact generated profile, not any finding with a matching ID in an existing deployment. Recheck new warnings or changed releases privately. Do not enable browsers, remote binding, tools, or automatic fixes just to obtain a green report. [Validation evidence](../../../VALIDATION.md) records the actual run and its limits.

## Gateway credential storage

New profiles store the random token in `secrets/gateway-token` (mode `600`, parent `700`), outside every agent workspace. `openclaw.json` contains a supported file `SecretRef`, not the token value. This reduces accidental disclosure when handling config; it is not a vault. The token is plaintext in its protected file, and the same OS account or a compromised host can read it. Keep FileVault and account separation, and never publish the profile or its backups.

Back up the config **and** referenced file with encryption and preserved permissions. A moved/restored profile needs its absolute secret/workspace paths reviewed before activation. Do not replace the file with a symlink or hardlink, or relax permissions. Existing installations need a separately reviewed secrets migration; this scaffold still refuses to overwrite them.

Production groups remain disabled until native-mention, untagged/reply-only/quote-only, denied-sender, unknown-room and cross-room canary tests pass. Passing schema validation or setting `requireMention` does not prove filtering happens before model/context access. This update supplies no custom ingress patch or additional group permissions.
