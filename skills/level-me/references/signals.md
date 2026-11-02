# Signals and scoring rubric

How to turn scanner output and transcript reading into the three scores.
Read this at step 4. Each dimension runs from 0 to 5. Score the highest
row whose evidence is present as a habit in the window, not once.

## Contents

- Agency per agent
- Orchestration
- Feedback infrastructure
- When signals conflict
- What this machine cannot show

## Agency per agent

How much one agent does between human decisions.

| Score | Definition | Configuration signals | Transcript signals |
|---|---|---|---|
| 0 | No agent. Suggestions or pasted snippets only | No harness configuration; no sessions in window | — |
| 1 | The agent acts; the person approves each consequential action | Manual or default permission mode; auto-review or untrusted approval policy | Approval prompts answered turn by turn; the person reads every change |
| 2 | Edits are auto-approved; commands and network still ask | Accept-edits mode; an allowlist of commands | The person reviews diffs and answers command prompts |
| 3 | Actions are auto-approved; the person still reads the diffs | Auto, classifier, or run-everything mode; full-auto or yolo flags | Comments on specific lines; corrections after reading code; frequent interrupts |
| 4 | The person watches outcomes, not diffs; some runs finish unattended | Bypass or no-prompt mode as a session default; headless entry points; cloud agents | "Do the tests pass?"; long gaps between turns; acceptance on a summary |
| 5 | Runs have a stop condition and a self-check the agent runs | A stop hook or goal condition that blocks completion until a check passes; branch protection; a spec file per task | Work starts from a spec; the agent reports the check it ran; the person judges the check, not the code |

Scoring notes. A no-prompt mode used only in scripted sessions is not
level 4 practice; the scanner sets those sessions apart. Many interrupts
with auto mode on means 3, not 4: the person is still the reviewer.
Level 5 needs both the check and the habit of trusting it.

## Orchestration

How many agents run at once and who coordinates them.

| Score | Definition | Configuration signals | Transcript signals |
|---|---|---|---|
| 0 | One session at a time | — | At most one session active in any ten minutes |
| 1 | Two or three sessions by hand, or subagents inside one session | Subagent definitions | Two or more sessions with human turns in the same ten minutes on several days; subagent transcripts |
| 2 | Four or more isolated workers in parallel | Worktree use per task; cloud agents; a session manager | Sessions in separate checkouts; the person routes work between them |
| 3 | A shared task list or a team the agents claim from | Agent teams enabled; workflow runs; a kanban or session board | Teammates or workflow phases in transcripts; tasks claimed, not assigned by hand |
| 4 | Ten or more agents, or a work queue with a merge queue | A work ledger or tracker the agents write to; a merge queue | Agents pick the next item themselves; the person reads a dashboard |
| 5 | An external orchestrator with a supervisor, gates, budgets, and policy | Orchestrator configuration present | The person sets policy and audits; no routing by hand |

Scoring notes. A desktop harness that makes a worktree per session on
its own is not evidence of deliberate isolation; count worktrees only
with parallel human activity. Subagents give parallelism or a fresh pair
of eyes, not a higher level on their own.

## Feedback infrastructure

What the codebase encodes and enforces around the agent.

| Score | Definition | Configuration signals | Transcript signals |
|---|---|---|---|
| 0 | Nothing persists between sessions | No instruction files | The same correction appears in several sessions |
| 1 | Preferences and conventions are written down | Instruction files, rules, skills | Corrections stop repeating; output consistent across sessions |
| 2 | A check the agent can run itself | A test or lint command named in the instruction file; lint-on-edit hooks; test configuration | The agent runs tests or lint before reporting; test runs in most coding sessions |
| 3 | Measurement on every change | CI on every pull request; coverage gates; acceptance or defect tracking | The agent reads CI results; failed checks drive the next turn |
| 4 | Loops close on their own signals | Stop hooks that block completion; automated triage; risk-gated auto-merge for low-risk paths | Runs end only when the check passes; low-risk changes merge without a person |
| 5 | A pipeline proposes and merges under policy | Merge queue; risk configuration; rollback procedure; escalation channel; observability | Humans gate the queue's configuration, not individual merges |

Scoring notes. Instruction files that keep growing with contradictory
rules are still level 1. A flaky test suite does not earn level 2; the
check has to be one the person trusts. Measurement that nobody acts on
(a dashboard graveyard) is level 3, not 4.

## When signals conflict

- Transcripts beat configuration. A bypass mode in settings with a
  person who interrupts every other turn is agency 3.
- Recent beats old. Score the last few weeks; mention an older peak in
  one line.
- The primary harness beats the others. Score the harness with the most
  interactive sessions; list the rest.
- Scripted sessions do not count toward practice scores. An eval runner
  that fans out two thousand headless sessions is tooling, and belongs
  in the "what is in place" section as measurement, not in agency or
  orchestration.
- When two adjacent scores both fit, report the lower one and the
  question that would raise it.

## What this machine cannot show

Say these in the report's last section when they matter:

- Other people's sessions, so a team's level is inferred from shared
  files only.
- Branch protection, required reviews, and merge queues on the hosting
  service.
- CI results and coverage trends over time.
- Cloud agent runs that leave no local transcript.
- Token spend, unless the harness records cost locally.
- Whether the person understands the code the agents wrote.
