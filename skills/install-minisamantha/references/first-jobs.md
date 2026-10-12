# First jobs: from safe installation to useful work

A deployment that passes every isolation test but does no work is a chatbot with a name. This reference gives MiniSamantha a small set of real, repeatable jobs that fit inside the starter's limits. None of them needs a new tool, a memory write, or an outbound message.

## Three tests for an AI employee

| Test | Meaning | How the starter meets it |
| --- | --- | --- |
| Complex | Multi-step work from several sources, not one-shot answers | Playbooks ask for structured outputs that combine supplied material, check it, and list gaps |
| Repeatable | The same workflow every week without re-explaining it | Playbooks live in the owner workspace and are read on request; the operator maintains them |
| Reliable | Output you would accept from a junior analyst | Each playbook states a quality bar; the operator reviews a sample of outputs weekly |

Fail one test and the deployment needs a better playbook or better inputs, not wider permissions.

## Starter playbooks

The scaffold copies these into the owner workspace at `playbooks/` with private permissions. T1 can read them with its existing `read` tool. Group agents cannot read files, so playbooks have no effect there.

| Playbook | Typical use | Output | Human step |
| --- | --- | --- | --- |
| [question-set](../assets/playbooks/question-set.md) | Podcast guest, interview, or meeting prep | Question arc with sourced premises | Owner edits and shares with the guest |
| [challenge-memo](../assets/playbooks/challenge-memo.md) | Board or investment decision prep | One-page devil's advocate memo | Owner takes it into the meeting |
| [newsletter-draft](../assets/playbooks/newsletter-draft.md) | Newsletter, article, or post from transcripts | Draft with source map and checklist | Owner edits and publishes |
| [research-note](../assets/playbooks/research-note.md) | Short research note or market map | Answer-first note with sourced table | Owner decides where it goes |

All four follow the same pattern: answer first, sources visible, gaps listed, nothing sent. She drafts; the owner presses.

To trigger a playbook, name it or describe the job: "Tee kysymyspatteri huomisen vieraan kanssa, alla hänen kirjansa johdanto." The agent reads the matching playbook and follows its output format.

## Changing or adding playbooks

Playbooks are operator-maintained files, like `AGENTS.md`. The running agent can propose a change as a diff; the operator applies it. Keep them in a private local Git history so you can see what changed when output quality moves.

A good playbook states the input, the output format, the quality bar, and what never happens. It describes work; it grants nothing. Text in a playbook that asks for a tool, a send, or a memory write has no effect on the starter's configuration and should be removed.

Converting a playbook into an OpenClaw skill is a configuration change: the scaffold sets `skills: []` for every agent. Admit a reviewed skill explicitly for the owner agent only, then rerun the acceptance tests.

## Jobs in groups

Group agents have no tools, so they cannot read playbooks. They can still do ordinary T2/T3 work from text in the room: answer tagged questions, summarise a discussion, draft a reply, or review pasted code.

For a recurring group job, such as agreeing questions with a guest in a dedicated room, the operator can add a short job note to **that room's** `AGENTS.md`. Keep it under ten lines, describe the output format only, and rerun that room's isolation tests. Do not copy owner memory, playbooks with private context, or other rooms' material into it.

Adding a guest as an authorized sender is a roster change, not a room setting. In the starter, `groupAllowFrom` applies to every admitted room: a guest admitted for one room can tag MiniSamantha in all of them. Use a dedicated deployment for guest rooms, a verified per-room sender control in your release, or let the owner relay the guest's questions. See the [runbook](install.md#6-connect-the-channel-in-two-stages).

## Weekly quality review

Once a week, pick five recent outputs and score each against its playbook's quality bar:

- facts and figures match the supplied sources
- uncertainty and gaps are marked, not smoothed over
- the output was usable after light editing
- nothing claimed a send, save, search, or check that did not happen.

Record the result in the owner workspace's `records/` as an operator note. Fix recurring failures in the playbook or the inputs. A persistent need for current data, files, or publishing is a reason to plan an extension under [security.md](security.md), one at a time with tests, not to loosen the baseline.

## Not first jobs

Email, publishing, scheduling, trading, client or deal material, browsing with personal sign-ins, and image or voice generation are outside the starter. Some are reasonable later, each as a separately reviewed extension. Customer-data use also needs the organisational review in [deployment-review.md](deployment-review.md).
