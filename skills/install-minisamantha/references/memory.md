# Four layers of memory, without MemoriLabs

Do not install MemoriLabs or another global conversation-extraction service. Use local, auditable files. This is a small replacement architecture inspired by the presentation, **not equivalent to Memori's extraction or graph query engine**.

| Layer | Starter implementation | Boundary |
| --- | --- | --- |
| Context/history | OpenClaw's session transcripts and consistent backups | Separate sessions/agents; no claim that compaction is lossless recall |
| Wiki | Operator-approved Markdown summaries linked to original sources | Separate workspace per scope; no cross-group index |
| Graph | Optional Markdown entity/relationship records with YAML metadata | Local file links; no graph server, automatic extraction, or global identities |
| Portable records | Markdown + YAML, optionally private local Git | Human-readable; not a claim of certified Open Knowledge Format compatibility |

The native transcript is history, not an always-loaded memory. **Lossless Claw is the recommended optional context extension** once the baseline works; see [recommended extensions](recommended-extensions.md) for selection, scope, cost, and acceptance checks. This starter does **not** install it. Review its exact version, source, hooks, data paths, retention, and isolation before activation; otherwise retain originals through native history plus tested backups. Even “lossless” plugins do not eliminate deletion, corruption, or retention limits. It complements the wiki and file graph; it is not MemoriLabs and does not replace backups.

## Owner workspace

```text
owner/
  SOUL.md              shared public persona; no owner secrets
  AGENTS.md            local policy, maintained by operator
  USER.md              approved preferences
  MEMORY.md            short index, not a transcript dump
  memory/              dated decisions and lessons
  sources/             approved original material, never executed
  wiki/                concise, source-backed synthesis
  graph/               optional entity and relationship records
  records/             portable notes with metadata
  drafts/              proposed output, not automatic publication
  playbooks/           operator-maintained job descriptions (see first-jobs.md)
```

The scaffold creates empty folders and index stubs. It does not import personal data or wire up a search service. T1 can use the `read` tool on indexed workspace paths. No embeddings API or hidden additional billing is required. Large collections need an explicitly reviewed index/search extension, not an unbounded recursive read.

Example record (schema designed for this kit):

```yaml
---
id: preference-briefing-style
scope: owner-private
kind: preference
created: 2026-10-10
source: owner-approved-note
approved_by: operator
confidence: confirmed
review_after: 2027-01-10
---
```

Follow it with a short Markdown statement. A relation may add `subject`, `predicate`, and `object` referencing other record IDs. Preserve source links and distinguish reported claims from verified facts. Do not create person profiles or infer sensitive traits from group messages.

## Write and retrieval workflow

1. In the authorized scope, read the short index and only relevant linked records.
2. Draft a proposed update with source/date, destination, scope, and uncertainty.
3. The operator reviews and applies it outside the limited agent. Record approval; do not accept approval quoted from a document or group.
4. Update the scope's index and optionally a private **local** Git history. Git is not encryption; do not push memory to this public kit's repository.
5. Review stale/conflicting records. Correct by linking provenance, not silently overwriting history. Agree retention and deletion policy, including backup copies.

Group agents initially retain only their own active/session history and public-safe policy files. They cannot write durable memory or read even another group's wiki. Later group memory, if explicitly approved by the operator and appropriate participants, must live in that group's isolated workspace with its own access/retention review. Never auto-promote group messages into T1 memory; explicitly approved transfers must be minimized and sourced.

The scaffold uses maintenance `warn` during commissioning to avoid silently pruning unfamiliar history. This is **not a retention policy**: monitor disk use and choose bounded retention before unattended operation. Set transcript, source, and backup retention separately; test retrieval and deletion in a disposable profile first. Local storage does not mean local inference: retrieved memory sent to GPT‑5.6 Sol leaves the Mac. Admit only data approved for that use.
