# The scales

The named scales the report places a setup on, with each level in its
author's own words, and the mapping from the three scored dimensions to
those levels. Read this at step 5.

## Contents

- Why three dimensions
- Yegge's eight levels
- Shapiro's Levels 0 to 5
- Osmani's two axes
- The AI Codebase Maturity Model (six levels)
- Berkeley's three levels and three dimensions
- Other scales the user may name
- Mapping scores to levels
- Published estimates of where people sit

## Why three dimensions

No scale is a standard. The two scales people cite most, Yegge's and
Shapiro's, came from a blog post and an interview in January 2026, have
no measurement behind them, and measure different things: Yegge's tracks
tooling posture and agent count on one line, Shapiro's tracks the
human's role by analogy with driving automation. Later scales split what
those two merge. Osmani separates one agent's autonomy from coordination
across agents. The AI Codebase Maturity Model grades what the codebase
encodes and enforces rather than what the human stops doing. The report
scores those three things apart, then names the Yegge and Shapiro levels
because readers know them.

## Yegge's eight levels

Steve Yegge, January 2026; "stages" in the essay, "levels" in the
interview that restated them. The first four are about an agent inside
the IDE; the last four are about agents outside it.

| Level | Yegge's wording |
|---|---|
| 1 | "no AI" |
| 2 | "Coding agent in your IDE, permissions turned on" |
| 3 | "Coding agent in IDE, 'YOLO mode.' Your trust is going up." |
| 4 | "you're starting to not look at the diffs anymore, but at what the agent is doing." |
| 5 | "I just want the agent and I'll look at the code in my IDE later, but I'm not coding with my IDE" |
| 6 | "several agents." The trigger: "You're bored because your agent's busy and you want to do something, so you fire up another agent, then another." |
| 7 | "10+ agents, managed by hand." The symptom: "oh gosh, I've made a mess!" |
| 8 | "you build your own orchestrator to coordinate more agents" |

The essay's own wording for the top three: stage 6 "CLI, multi-agent,
YOLO (3-5 parallel instances)", stage 7 "10+ agents, hand-managed",
stage 8 "Building/using an orchestrator to automate the workflow". An
orchestrator the person adopts counts for 8 as much as one they build.

What the scale does not do: it gives one number for trust in one agent
and the count of agents together, so a person running five supervised
agents and a person running one unattended agent can land on the same
level. Yegge gives no measured distribution; he estimates that most
engineers are not yet past the low levels.

## Shapiro's Levels 0 to 5

Dan Shapiro, January 2026. Six rungs, zero-indexed, by analogy with the
driving-automation levels: "the federal government had been there first
– but for cars." The title says five levels.

| Level | Name | The developer's day |
|---|---|---|
| 0 | Spicy autocomplete | Writes the code; AI as search or occasional completion. "not a character hits the disk without your approval." |
| 1 | The coding intern | "You're writing the important stuff, but you offload specific, discrete tasks to your AI intern." |
| 2 | The junior developer | "You are pairing with the AI like a colleague." Reviews every line. |
| 3 | The developer | "You spend your days reviewing code." "Your coding agent is always running multiple tabs." |
| 4 | The engineering team | "You write a spec. You argue with it about the spec." "You craft skills." "Then you leave for 12 hours, and check to see if the tests pass." |
| 5 | The dark software factory | "a black box that turns specs into software." No human writes or reads the code. |

Two claims to carry into the report as the author's observations, not
data: "level 2, and every level after it, feels like you are done. But
you are not done." And of Level 3: "almost everyone tops out here."
Level 5 is rare: the author knows "a handful of people... small teams,
less than five people."

## Osmani's two axes

Addy Osmani, July 2026. Six levels on an agency axis, with orchestration
as a second axis: "A single rung cannot help you place multi-agent
skill." His rule for moving: "Move up one axis at a time", and "Every
step up the lever requires a new set of safety mechanisms".

| Level | Name | Defining line |
|---|---|---|
| 0 | Assist | Suggestions; the person decides everything |
| 1 | Supervised action | "The agent edits or runs commands on your behalf, asking you before executing anything consequential." |
| 2 | Scoped task delegation | "Hand off a bounded task to the agent." |
| 3 | Goal-driven autonomy | "The agent does whatever it takes to achieve a goal, stopping only when some condition is met." Needs a stopping condition "measurable in a way that can be automated." |
| 4 | Parallel delegation | "Work across many agents in parallel." Needs agents "isolated from one another, each owning their own files and status." |
| 5 | Managed-by-exception orchestration | "Define what success looks like, and which policies should apply." Needs independent verification. |

A recognition signal from the same source: "A single agent kept busy by
human handoffs is Level 4 with a dashboard." Several sessions fed by
hand are orchestration in name only.

## The AI Codebase Maturity Model (six levels)

Andy Anderson, April 2026, from a 100-day single-project case study.
Levels are properties of the codebase, "defined by feedback loop
topology, not by tool choice", and cannot be skipped: "Level 4 requires
Level 3's measurement infrastructure, which requires Level 2's
consistency". Its central claim: "the thing that unlocks each transition
is not giving AI more freedom — it is adding another feedback
mechanism."

| Level | Name | Feedback loop | Key artifacts | Human role | Transition trigger |
|---|---|---|---|---|---|
| 1 | Assisted | Open loop | None | Executor | "keep repeating the same corrections across sessions" |
| 2 | Instructed | One-way, human to AI | Instruction files, style guides, PR templates | Rule-writer | "cannot tell them whether the AI is actually performing well" |
| 3 | Measured | Two-way, human interprets | Acceptance-rate logs, coverage gates, nightly suites | Analyst | "why am I manually adjusting weights when the data tells me what to do?" |
| 4 | Adaptive | Closed loop | Self-tuning configs, closed CI/CD loops, worktree sessions | Governor | "The code is the policy." |
| 5 | Semi-automated | Multi-loop, system proposes, humans approve | The codebase itself | Operator | "The bottleneck is no longer AI quality — it's human availability." |
| 6 | Fully autonomous | Multi-loop with external orchestration; system acts | Agent fleet, policy files, work ledger | Strategist | — |

Anti-patterns per level, useful as diagnoses: L1 "I tried Copilot but it
doesn't understand our codebase"; L2 "Ever-growing instruction files with
contradictory rules"; L3 "Dashboard graveyard"; L4 optimizing a proxy
metric; L5 "Alert fatigue: generating proposals no one reviews"; L6
"Mistaking autonomy for abandonment". On tests: "At Level 2, I had
instructions that made the AI consistent. At Level 3, I had tests that
made the AI trustworthy." Evidence base: one project, its author's own.

## Berkeley's three levels and three dimensions

A twelve-author position paper, July 2026. Three levels by which
lifecycle stages the AI owns: Level I Code Autonomy ("full ownership of
system design and implementation without line-by-line human approval"),
Level II Pipeline Autonomy (design through "testing, auditing, and
deployment"), Level III Demand Autonomy ("decides what should be
built"). Today's AI-assisted coding is "a precursor" to Level I. The
three cross-cutting dimensions are modifiers for any placement:

- **Specification granularity**: from a bug report with reproducing
  tests to an open request such as "add multi-tenancy".
- **Temporal autonomy**: "ticket level, sprint level, release level, or
  continuously".
- **Oversight mode**: from co-specification and action-level approval,
  through pull-request review, to "policy guardrails, monitor-only
  operation, and automated rollback".

## Other scales the user may name

| Scale | Levels | Measures |
|---|---|---|
| Sourcegraph Levels of Code AI (2023) | 0 no AI; 1 code completion; 2 code creation; 3 supervised automation; 4 full automation; 5 AI-led | Autonomy per invocation, driving-levels analogy |
| BlueOptima Coding Automation Framework (2024) | 0 to 5, no through full automation | Automation per developer from telemetry |
| Cloud Security Alliance (2026) | 0 no autonomy; 1 assisted; 2 supervised; 3 conditional; 4 high; 5 full | Who decides, approves, monitors; any agent, not coding only |
| Dash0 six levels (2026) | 1 assisted; 2 generated, human-reviewed; 3 auto-reviewed; 3.5 selective auto-merge; 4 mostly autonomous; 5 dark factory | The review gate type |
| Arden's twelve rungs (2026) | Student, Borrower, Reviewer, Delegator, Director, Juggler, Bottleneck, Dispatcher, Operator, Sponsor, Arbiter, Framer | "What have you given up"; three thresholds: stop writing code, give up presence, give up judgment |
| Swarmia five levels (2026) | assistive; conversational; task agent; autonomous teammate; agentic avalanche | How much work before the agent returns; "not a ranking" |
| ELEKS AI-SDLC (2026) | traditional; AI-supported; AI-assisted; AI-native; AI-autonomous | Organization-wide lifecycle maturity |
| Coder AI Maturity Curve (2026) | chat and completion; local human-directed agents; remote human-supervised agents; autonomous engineers; autonomous teams | Enterprise agent adoption |

When the user names one of these, place them on it in one line by
analogy with the three scores, and say the scale is a vendor's or
author's proposal.

## Mapping scores to levels

Scores come from the rubric in signals.md: agency A, orchestration O,
feedback F, each 0 to 5. Apply the first row that matches; where a row
gives two levels, the transcript question in the last column decides.

| Condition | Yegge | Shapiro | Osmani agency | ACMM | Deciding question |
|---|---|---|---|---|---|
| A0 and O0 | 1 | 0 | 0 | 1 | — |
| A1 | 2 | 1 | 1 | F+1 | Does the person hand off discrete tasks (Shapiro 1) or only snippets (0)? |
| A2 | 2 or 3 | 2 | 1 or 2 | F+1 | Are commands still approved one by one (2) or only edits auto-approved (3)? |
| A3 | 3 or 4 | 2 or 3 | 2 | F+1 | Are diffs read before acceptance (3 and 2) or outcomes checked (4 and 3)? |
| A4 | 4 or 5 | 3 or 4 | 3 | F+1 | Is the IDE abandoned and work left unattended (5)? Does work start from a spec with tests as the check (Shapiro 4)? |
| A5 | 5 | 4 | 3 | max(F+1, 4) | — |
| O1 and A3 or more | 6 | 3, or 4 when A is 4 or more | 4 | F+1 | Several agents at once as a habit, or occasionally? |
| O2 or O3 | 6 or 7 | 3, or 4 when A is 4 or more | 4 | F+1 | Ten or more at once (7), or a shared task list in use (7)? |
| O4 | 7 | 3, or 4 when A is 4 or more | 4 or 5 | max(F+1, 5) | Do agents claim work from a queue without the person routing it? |
| O5 | 8 | 4, or 5 when no human reads code and F is 5 | 5 | 6 | Does any human read the code before merge (4) or none (5)? |

Orchestration rows set the Yegge level; the Shapiro level follows the
human's role, so several agents under close review are still Shapiro 3.
A high orchestration score with a low feedback score is the common
unsafe shape; the report says so and names the feedback gap as the next
step before any further parallelism.

## Published estimates of where people sit

Report these as estimates, never as data, and only when asked:

- Shapiro: "This is where 90% of 'AI-native' developers are living right
  now", said of Level 2. No survey behind it.
- Yegge: "probably still 70% aren't doing it", of engineers not yet
  using agents. No survey behind it.
- BlueOptima telemetry, 2024, about 110,000 developers: 0.49% at its
  Level 3 or above. Dated; before the current agent generation.
- Stack Overflow survey, 2026: 73% of respondents use assistants or
  agents daily; 26% use automated agent workflows; "human-in-the-loop is
  the dominant mode".
- GitHub, September 2026: more than 40% of pull requests started with an
  agent, up from 17% in March 2026; agent detection "is a floor".
- Pragmatic Engineer survey, early 2026, 906 self-selected readers: 55%
  regularly use agents.
