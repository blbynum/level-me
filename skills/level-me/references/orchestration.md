# Orchestration tools

What the orchestrators and multi-agent tools in use provide, part by
part, so the report can name the right kind of tool for the next step.
Read this at step 6 when the current level is 6 or above, or when the
user asks about a named tool. Facts are as of late 2026; check a tool's
own documentation before recommending it, since several have been
archived or replaced within a year.

## Contents

- Full orchestrators
- Native multi-agent features of the harnesses
- Work ledgers and queues
- Session managers for parallel work by hand
- Vendor cloud agents
- Loops for a single unattended agent
- Choosing

## Full orchestrators

| Tool | Provides | Notes for the report |
|---|---|---|
| Gas Town | A coordinator agent, worker agents, a per-repository merge-queue agent, a lifecycle monitor, a background supervisor; work as bundles of ledger items; many agent CLIs | Scales to 20 to 30 agents; its author says 4 to 10 become chaotic and calls it a cash guzzler needing several accounts. In maintenance; its ideas moved into Gas City, an SDK |
| Gas City | The same ideas as composable infrastructure: runtime providers (terminal multiplexer, subprocess, Kubernetes), ledger-backed work, optional hosting-service gates | Needs the ledger tool and a terminal multiplexer; configured by one file per "city" |
| Hive | A supervisor over role-specialized executors (scanner, reviewer, architect, outreach), a governor that sets cadence from backlog, a merge queue that auto-merges verified changes, risk-gated human review, push-notification escalation, policy files read on every run, per-agent service units | The reference implementation of the maturity model's level 6; a sandbox project under a cloud-native foundation; intake from issue trackers; budgets, retry limits, a prompt-injection filter |
| Symphony | Polls a project board and spawns one isolated run per item; agents report status, review feedback, and walkthroughs; accepted work lands as a pull request | An engineering preview from a model vendor, spec-first with a reference implementation |
| Paperclip | An organization chart of agents with roles and reporting lines, approval stages, and budgets that pause work at a limit; many agent types through heartbeat adapters | Aimed at running a whole operation, not only code |
| Overstory | Coordinator, scout, builder, reviewer, merger, monitor roles; a merge queue with conflict resolution; a worktree per agent | Archived mid-2026; its author warns that compounding errors, cost amplification, and merge conflicts "are the normal case" |

## Native multi-agent features of the harnesses

| Feature | Provides | Limits |
|---|---|---|
| Subagents | Parallel workers inside one session, each with its own context; optional worktree isolation | Parallelism or a fresh pair of eyes, not a smarter answer |
| Agent teams | A lead session that coordinates peers with a shared task list and mailboxes; hooks that can refuse a teammate's completion | Experimental; "significantly more tokens"; start with three to five; one team per session |
| Scripted workflows | A script that fans out dozens to hundreds of subagents through phases and pipelines | No mid-run input; a cost warning above a few dozen agents |
| Worktrees | One checkout per task or session; edits to the main checkout blocked from inside | The desktop harness makes one per session on its own |
| Batch | Splits a task into units, runs each in a worktree, opens pull requests | — |

## Work ledgers and queues

| Tool | Provides |
|---|---|
| Beads | A dependency-aware issue graph for agents on an embedded version-controlled database; hash-based identifiers that avoid merge collisions; atomic claims; a ready-list of unblocked items; threaded messages between agents. Required by Gas Town, Gas City, Hive, and Overstory |
| Issue trackers | GitHub issues and projects, Linear, Jira: intake for Hive, Symphony, Devin, cloud agents |

## Session managers for parallel work by hand

For level 6: several agents, each in its own checkout, routed by a
person.

| Tool | Provides |
|---|---|
| Claude Squad | A terminal app; one multiplexer session and one worktree per agent; review and check out before push; works with several agent CLIs |
| Conductor | A desktop app; a workspace, branch, terminal, diff, and review path per task; opens the pull request and archives the workspace |
| ccmanager | A terminal manager for many agent CLIs; create, merge, and delete worktrees in place; experimental auto-approval that falls back to manual on errors |
| vibe-kanban | A board where each issue gets a workspace with a branch, terminal, and dev server; sunsetting |
| Cursor Agents Window | Parallel agents in isolated checkouts inside the editor |

## Vendor cloud agents

Each gives one agent one isolated environment per task, returns a pull
request for human review, and takes intake from chat, tickets, or
mentions. They are level 5 tooling (unattended, bounded runs) and
support level 6 by running many at once; none provides a merge queue
or a supervisor on its own.

| Vendor agent | Notes |
|---|---|
| Cursor cloud agents | Isolated virtual machines; intake from the editor, web, chat, tickets, and an API; a spend limit on first use |
| Codex cloud | A workspace per task that keeps working while the computer sleeps; environment settings for network and credentials |
| Copilot in the cloud | A cloud sandbox or a CI runner; one branch and one pull request per task; a 59-minute cap per CI session; branch rules can block it |
| Jules | A virtual machine per task; plan approval before any code change; scheduled tasks and an API |
| Devin | Intake from chat threads and tickets; many tasks in parallel; draft pull requests |
| OpenHands | Self-hosted control center for several agent CLIs; decomposes issues; schedules and webhooks; a container per conversation |
| Factory droids, Amp | Cloud sessions per thread; an orchestrator of parallel agents in one case, a launcher that coordinates agents in the other |

## Loops for a single unattended agent

| Tool | Provides |
|---|---|
| The Ralph loop | A shell loop that re-feeds a prompt file until the plan is done; back pressure from tests, type checks, or any check that rejects bad output; a tag on green. Its author uses it on new codebases only |
| Stop-hook loops | A harness hook that refuses completion until a promise or a check is met, with an iteration cap |

## Choosing

- Levels 5 and 6: a vendor cloud agent or worktrees plus a session
  manager. No orchestrator yet.
- Level 7: a ledger or tracker with claims, a merge queue, and
  measurement. Native agent teams or workflows for bursts.
- Level 8: Hive or Gas City when the work is many repositories and a
  queue; Symphony when a project board is the source of truth and the
  agent is Codex; Paperclip when roles beyond engineering matter. Read
  the tool's current status first; the field turns over within months.
- At any level: pick the lowest rung whose cost the work can pay. More
  agents without more verification is the shape every source warns
  against.
