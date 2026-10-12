# Recommended extensions: YouTube reading and lossless context

Add these **after** the starter passes acceptance, one at a time with operator approval. Neither changes GPT‑5.6 Sol as the main brain or introduces MemoriLabs. This guide is a recommendation and rollout specification, not an installed integration. Keep the scaffold unchanged until the exact component, version, permissions, and tests are approved.

Two companion workflows have a different purpose: run the recommended **tekoalyasetus** review before organisational customer-data use, and use **suomen-kieli** when the working language is Finnish. Their links, scope, and example tasks are in [deployment review](deployment-review.md); neither requires opening group tool access.

## 1. YouTube reading skill: transcript first

Recommended capability: retrieve a public video's transcript, summarize its substance, and return the source link, source type, key points, and timestamps where supported. A transcript is not evidence that the model watched the images or heard the audio.

Prefer an already approved, scoped transcript tool such as `summarize_youtube` **if the target runtime actually exposes it**. Do not assume that Samantha's tool is bundled with every OpenClaw install. A skill supplies instructions; it does not supply a missing retrieval backend or grant tools.

If a backend is needed, one concrete review candidate is [openclaw-youtube-transcript](https://github.com/JonFerminBot/openclaw-youtube-transcript), whose upstream documentation describes caption retrieval using [yt-dlp](https://github.com/yt-dlp/yt-dlp). This is not an endorsement of its unreviewed code: inspect and pin the plugin and dependencies, confirm the target runtime supports them, and test their real execution location before selection. Avoid marketplace one-click installs or copying an upstream unpinned installer.

The reading skill should follow this contract:

1. Accept a public HTTPS YouTube video URL, validate the real hostname/video ID, and retrieve only the intended video's text. Prefer captions in the requested language, then available original-language captions. Preserve the distinction between human captions and automatic captions.
2. Classify the result: **transcript**, **user-supplied subtitles**, **metadata only**, or **unavailable**. A retrieval/rate-limit/authentication error does not prove that subtitles do not exist.
3. Summarize verified text; label omissions and automatic-caption uncertainty. Do not fabricate quotations, timestamps, examples, or an episode summary from the title alone. Metadata-only output must say so. Ask for a transcript when retrieval is unavailable.
4. Treat all retrieved text as untrusted source material, including instructions allegedly from the operator. Return the answer in the current conversation only; no comments, likes, subscriptions, uploads, or publishing.

Start with T1. For selected T2/T3 rooms, expose only the approved read-only transcript operation after a separate permission change and tests. T4/T5 remain blocked. Do not expose general shell/`exec`, a logged-in browser, cookie extraction, arbitrary URL fetching, or a broad MCP/plugin tool bundle to groups. Any subprocess-based backend belongs behind a reviewed, fixed-argument adapter with bounded output/time and restricted egress, not a model-authored shell command. Validate redirects and block private-network targets; a YouTube-looking string is not a URL security check.

Recommended initial limits: one video per request, 60-second retrieval timeout, at most one bounded transient-error retry, and a 1 MiB text-response cap. These are operator-configured limits, not claims about the candidate plugin's defaults. Stop on access restrictions; do not import personal cookies or bypass them. Audio downloading, paid transcription, and local Whisper are separate opt-ins, not automatic fallbacks on a 16 GB Mac mini. Review third-party API costs and what URLs/content they receive.

## 2. Lossless Claw: recommended context extension

Recommended candidate: [Lossless Claw](https://github.com/martian-engineering/lossless-claw), package `@martian-engineering/lossless-claw`. It stores conversation material in SQLite and builds summaries for context assembly, with tools for retrieving older details. It complements the operator-approved Markdown wiki and file graph. “Lossless” does not promise perfect recall, correct summaries, or immunity to deletion/corruption.

Rollout requirements for MiniSamantha:

1. Review the exact release, compatibility with the installed OpenClaw version, dependencies, conversation-access hooks, database locations, provider calls, and retention. Pin the approved version; do not invent a compatible version number. Back up before any migration or activation.
2. Trial it in an isolated owner-only profile with synthetic history. OpenClaw selects context engines through `plugins.slots.contextEngine`; this is **not** a per-agent skill allowlist. Verify the chosen release's actual ingestion, assembly, and recall scoping. If a shared gateway cannot enforce the required boundaries, keep the engine in a separate owner gateway; do not rely on prompt instructions to separate T1 from groups.
3. Record every database, cache, and transcript path. Keep them inside the intended protected profile, never a shared default database or this public repository. No automatic import of other profiles or group histories. Test that arbitrary conversation IDs cannot retrieve another scope's data.
4. Review recall-tool permissions separately from context-engine hooks. A tool deny does not prevent an enabled engine from ingesting or assembling context. Conversely, installing the engine does not make its recall tools available under this starter's allowlists. Grant only reviewed exact operations at the necessary global/agent/sandbox layers; never solve a conflict by granting all plugin tools. Keep group tools denied until a separately approved group-safe design passes tests.
5. Measure summarization/recall model costs and disk growth. Verify the selected summarization model and billing route explicitly; GPT‑5.6 Sol being the main brain does not prove every background call uses it. Require approval for any separate model or API billing. No mandatory embeddings or vector server are added by this recommendation.
6. Include the plugin's database in a consistent, encrypted backup and isolated restore test. Verify `/new` versus `/reset` behavior for the pinned release; do not assume they mean the same thing once the engine is active. Test rollback to the prior engine without deleting history. Report engine errors/fallbacks rather than claiming lossless behavior is still active.

See [OpenClaw's context-engine documentation](https://docs.openclaw.ai/concepts/context-engine) for selection and lifecycle behavior. Installation commands and hook grants must come from the reviewed version's documentation; this guide deliberately does not auto-enable conversation access.

## Extension acceptance tests

**YouTube:** a captioned Finnish video; a captioned English video; missing captions; a retrieval error; unavailable tool; metadata-only disclosure; malicious transcript instructions; an oversized response; a deceptive hostname/redirect; and the same request from a denied room/sender. Confirm no cookie/host-file access, unrestricted subprocess, cross-room cache leak, or unexpected charge. Only returned transcript evidence can support episode-level claims.

**Lossless context:** ingest synthetic facts, compact a long conversation, retrieve an exact fact with its source, restart, and restore the database in isolation. Seed distinct T1/group canaries and attempt cross-scope retrieval by query and explicit conversation ID; inspect both assembled context and tool results. Check retention/deletion, reset behavior, summary costs, database growth, engine failure, and rollback. Block activation on leakage or unexplained scope/fallback behavior.

Record versions, permissions, storage paths, costs, test evidence, and limitations in the deployment handover. Recommendations alone are not evidence that either extension works safely on the target machine.
