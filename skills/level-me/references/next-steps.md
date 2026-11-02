# Next steps, level by level

What each move up needs, what it costs, and how to tell it is done. Read
this at step 6. Levels are Yegge's, with Shapiro's in brackets. The
mechanism is named here; the exact file, flag, or setting for each
harness is in that harness's reference.

## Contents

- The rule behind every step
- From level 1 to 2 [Shapiro 0 to 1]
- From level 2 to 3 [Shapiro 1 to 2]
- From level 3 to 4 [Shapiro 2 to 3]
- From level 4 to 5 [Shapiro 3 to 4]
- From level 5 to 6 [Shapiro 4]
- From level 6 to 7 [Shapiro 4]
- From level 7 to 8 [Shapiro 4 to 5]
- The full orchestration pipeline
- Team and organization prerequisites
- Why people stall

## The rule behind every step

Each move up adds a feedback mechanism, never only more freedom for the
agent. The sources that have run the top levels agree on it, and the
measured evidence points the same way: where output rises without
verification capacity, review collapses, defects per change rise, and
stability falls. So the report never recommends turning prompts off,
leaving a run unattended, or adding agents unless the check that makes
that step safe is present. When the check is missing, the check is the
step.

## From level 1 to 2 [Shapiro 0 to 1]

Prerequisite: an agent that can edit files and run commands, used with
approval prompts on.

Steps:
1. Install one agent harness and use it for half an hour a day on real
   work, with permissions on. Hand it discrete tasks first: a test, a
   docstring, a refactor of one function.
2. Write the project's instruction file. The most useful line in it is
   the command that runs the project's checks.
3. Learn the vocabulary: context window, instruction file, permission
   mode, hook, worktree. The references here cover what the harness
   docs call them.

Cost: time to learn; early output needs reading.
Done when: the person hands off bounded tasks and reviews the result
rather than typing the code.

## From level 2 to 3 [Shapiro 1 to 2]

Prerequisite: preferences written down so corrections stop repeating,
and the zero-exception rules enforced by the harness rather than by
attention.

Steps:
1. Each time a correction repeats across sessions, add it to the
   instruction file. Keep the file short and free of contradictions; a
   growing file with conflicting rules is the level 2 anti-pattern.
2. Move the rules that must hold every time into deterministic
   enforcement: a deny rule for the command that must never run, a hook
   that lints or formats on every edit, the sandbox for network and
   filesystem limits. Keep that enforced set small.
3. Then turn auto-approval on for the actions the enforcement covers.
   Keep approval prompts for anything outside it.

Cost: the person stops seeing every command; mistakes land in the
working tree before they are seen.
Done when: auto-approval is the default and the person no longer
answers routine prompts.

## From level 3 to 4 [Shapiro 2 to 3]

Prerequisite: a check the agent can run itself, that the person trusts.
Without one, the person is the test suite.

Steps:
1. Name the test command in the instruction file and make the agent run
   it before it reports done. Fix flaky tests first: a flaky check is
   worse than none, because it teaches the person to ignore failures.
2. Add a hook that runs lint, type checks, or the fast tests after each
   edit, so problems surface before the person reads anything.
3. Ask for evidence, not claims: the command the agent ran and its
   output, or a screenshot. Treat "looks done" as not done.
4. Add an independent review step: a reviewer with no view of the
   conversation that produced the change, so it is not swayed by the
   reasoning that produced the code.
5. Start judging low-risk changes by outcomes (the check passed, the
   reviewer found nothing) rather than by reading every line.

Cost: comprehension debt. The measured skill loss for people who
delegate without reading is real; keep deliberate reading for the parts
that matter and say which parts those are.
Done when: for routine changes, the person reads the check result and
the review, not the diff, and nothing breaks that the check should have
caught.

## From level 4 to 5 [Shapiro 3 to 4]

Prerequisite: the agent knows what done looks like, can check its own
work, and knows what it may touch.

Steps:
1. Start each task from a spec, a plan, or a failing test the agent has
   to turn green. Argue the spec before the work, not the code after.
2. Give runs a stop condition: a hook or goal that blocks completion
   until the check passes, or an explicit completion criterion the
   agent must demonstrate.
3. Scope what the run may touch: permission rules, a sandbox, a
   worktree, the one branch it may push to. Protect the main branch
   with a rule on the hosting service that the agent cannot bypass.
4. Watch the first few unattended runs before trusting the setup. Then
   use headless or cloud runs for bounded tasks and leave.
5. Write skills for the recurring workflows so the spec, the check, and
   the scope travel together.

Cost: the person has to specify intent; no sensor supplies it. Runs
that finish without a human are also the runs that burn tokens on the
wrong thing.
Done when: a task can run for hours unattended and the person judges
it by the check, not by reading the code.

## From level 5 to 6 [Shapiro 4]

Prerequisite: isolation per worker, so parallel edits cannot collide.

Steps:
1. Give each concurrent agent its own checkout: a worktree, a cloud
   workspace, or a container. Never two agents in one working tree.
2. Use subagents for read-heavy parallel work inside one task; they buy
   parallelism or a fresh pair of eyes, not a smarter answer.
3. Plan the day as bounded tasks that can run side by side. Keep a
   session manager or a board so the person can see which session is
   doing what.

Cost: attention does not parallelize. The practitioners who work this
way report about three productive hours a day at full pace and real
fatigue; plan around it rather than through it.
Done when: three to five agents run at once as a habit, each in its
own checkout, without merge conflicts between them.

## From level 6 to 7 [Shapiro 4]

Prerequisite: a shared ledger of work that agents claim from, and
measurement in place before anything is automated.

Steps:
1. Put the work in a tracker or ledger with claimable items and
   dependency links, so agents pick the next item and do not collide.
   Hash-based identifiers avoid merge conflicts across branches.
2. Add a merge queue: workers never push to the main branch; their
   changes queue for verification and rebase.
3. Measure before automating: acceptance rate per change category, CI
   on every change, defects traced to changes. Then act on the data.
4. Set a token budget with alerts; the top levels are measured in
   dollars per day per engineer.
5. Give up routing by hand. If the person still assigns every item,
   this is several agents with a dashboard, not level 7.

Cost: money, and the mess Yegge names: unread proposals are noise, not
progress.
Done when: ten or more agents can run with the person reading a
dashboard, not a chat.

## From level 7 to 8 [Shapiro 4 to 5]

Prerequisite: process management, gates, and a kill switch outside the
agents themselves.

Steps:
1. Run agents under a supervisor: a service manager and scheduler keep
   them alive, restart them within a cap, and never trust an agent to
   keep itself alive.
2. Add a governor that sets cadence from backlog size, and budgets that
   pause work at a limit.
3. Auto-merge verified changes on low-risk paths; require a human on
   high-risk paths regardless of the agent's confidence.
4. Keep acceptance scenarios outside the repository as a holdout set,
   because a test inside the repository can be rewritten to match the
   code.
5. Add independent verification, an escalation channel for decisions
   that need a human, an observability runbook for debugging autonomous
   behavior, and a rehearsed rollback.
6. Adopt an orchestrator that provides these parts, or build one; the
   orchestration reference lists what each existing one provides.

Cost: token spend on the order of a thousand dollars a day per
engineer at the leading edge; an accountability gap for code no human
has read; the risk the paper on the model names, mistaking autonomy for
abandonment. The human role becomes strategist and auditor, which is
the most demanding judgment on the ladder.
Done when: the system generates its own issues, dispatches, verifies,
merges, and rolls back under policy, and the person audits after the
fact.

Shapiro's Level 5, the dark factory where no human reads code, adds a
charter (no hand-written code, no human review), specs plus held-out
scenarios scored by satisfaction, and behavioral clones of the services
the software depends on. The teams that have done it are small, senior
in reliability engineering, and have published no outcome data. Report
it as the far end of the ladder, not as a target.

## The full orchestration pipeline

The parts, in the order work flows:

| Part | What it does | Minimum form |
|---|---|---|
| Intake | Work enters as claimable items with acceptance criteria | A tracker or ledger with claims and dependencies |
| Dispatch | A supervisor assigns or agents claim; cadence follows backlog | A scheduler and a governor |
| Workers | Isolated agents, one task each | A worktree or container per task, budgets and retry limits |
| Verification | Checks the agent cannot game | Tests in CI, held-out scenarios, an independent reviewer |
| Merge gate | Verified changes merge; risky paths wait for a human | A merge queue with a risk configuration |
| Escalation | Decisions that need a human reach one | A notification channel with a clear question |
| Observability | Humans can see and debug autonomous behavior | A dashboard, logs, a runbook |
| Rollback | Autonomous changes can be undone fast | A rehearsed procedure and a kill switch |

A setup is ready to adopt a pipeline when levels 3 to 7 hold: a trusted
check, a spec per task, isolation per worker, a ledger, measurement.
Adopting the pipeline first and hoping the checks follow is the shape
that fails.

## Team and organization prerequisites

For a team, the measured organizational capabilities that amplify AI's
effect are: a clear and communicated stance on AI use, healthy internal
data, AI-accessible internal data, strong version control practice,
working in small batches, a user-centric focus, and quality internal
platforms. Small batches and version control matter most at the higher
levels, because agent output is larger and broader than human-paced
work and review capacity does not grow with it. No vendor publishes a
staged rollout playbook; the pattern that recurs is a pilot team at one
level above the rest, then a wave.

## Why people stall

Name the one that fits, in one sentence:

- Each level "feels like you are done". The next level looks like more
  risk for no gain until the check exists.
- Level 3 feels worse than level 2: the day becomes diffs. The way out
  is a check, not more reading.
- Senior engineers have the most invested in the old way; the habit a
  rung asks them to give up is the one they are best at.
- The person keeps steering turn by turn out of distrust; the fix is a
  sensor, not patience.
- Scaling agents before measurement: more output for the same reviewer.
