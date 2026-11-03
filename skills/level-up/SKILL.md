---
name: level-up
description: Plans a person's or team's move up the AI coding ladder from their latest level-me assessment, to a target rung the user names and under the constraints they state - one container per rung, one mechanism per task with a four-part brief (Scope, Files, Acceptance, Do not touch), a gate task per rung that re-runs level-me, and a short design document. Writes the plan as Markdown ticket files in a directory per rung with todo, in-progress, review, and done, or as tickets in a tracker when a ticket skill is configured. Use when the user asks "plan my move up the ladder", "level up", "turn my level-me assessment into tickets or tasks", "make a backlog to get to Yegge 8", "plan the next level from the assessment", or "make the ladder from my assessment into task files". Not for the assessment itself (the level-me skill - "what level am I at", "how do I get to the next level"), for doing a task in the plan (a ticket-working skill), or for a plan with no assessment behind it.
compatibility: Needs no command-line tool. Reads the references of the level-me skill, installed beside it.
metadata:
  harness: portable
  last-verified: "2026-11-03"
---

# Level up

level-me says where a person's AI coding practice is. This skill plans the
move up from that assessment the way a tracker holds work: one container
per rung, one mechanism per task, a gate task at the end of each rung that
re-runs level-me, and on every task a brief that a person or an agent can
act on without the conversation that produced it. Three things void such
a plan, and each rule below exists to stop one of them:

- **Several mechanisms in one task.** A ticket that adds a Stop hook and
  a lint hook is done when both work, so it is done never, or half. Every
  task here is one mechanism, done when it exists at a path and was
  exercised once.
- **A gate that is a trial, not a measurement.** "Three runs finish
  unattended" is a rehearsal the person judges. Every rung here ends with
  a task that re-runs level-me and closes the rung only when the new
  assessment shows the rung's level.
- **A constraint reread or dropped.** "No cloud sessions" becomes "no
  CI", and branch protection falls out of the plan. Every task here
  states whether a constraint changed it, and the design document lists
  what each constraint changed.

## Config

| Key | Required | Default | Purpose |
|---|---|---|---|
| ticket-skill | no | | skill that implements the ticket platform contract; when set, the plan is created in that tracker instead of as files |
| docs-skill | no | | skill that files the design document; when unset, write it to `design.md` in the plan directory |

Read `config.local.yaml` in this skill's directory before anything else.
A key missing there takes its Default from the table. If a required key is
missing or empty, stop: name the key and its purpose, and offer to write
`config.local.yaml` with the values the user gives. If a configured
directory does not exist, stop and say so; do not create it.

Read the reference for the harness you run in, `references/<harness-id>.md`,
before step 1. It says how the request arrives, where the level-me
references and the assessment are, and how a gate task re-runs level-me
there.

## Workflow

Copy this checklist into the response and check items off as you go:

```
- [ ] 1. Find the latest assessment, or stop and offer level-me
- [ ] 2. Take the target rung, the constraints, and the plan's home
- [ ] 3. Lay out the rungs: one gate each, from the next level to the target
- [ ] 4. Write the tasks: one mechanism each, a four-part brief, order, waits-on, the gate last
- [ ] 5. Apply the constraints and record where each changed a task
- [ ] 6. Write the plan out: ticket files, or tickets through the ticket skill
- [ ] 7. Write the design document and file it
- [ ] 8. Report
```

### 1. Find the assessment

The input is the latest level-me assessment: a document with a placement
table, the scores and their evidence, a "Next level" section with steps,
and "The ladder from here". Find it in this order:

1. The one the user names, by path or link.
2. When `docs-skill` is set, ask that skill to find the newest document
   whose title says it is an AI coding level assessment.
3. A Markdown file in the project directory whose first lines say when
   it was assessed and that carries a placement table.

Say which assessment the plan uses and its date. When none is found, say
so and offer to run level-me first; do not plan from memory of the
person's setup, and do not plan from a description the user types in
place of an assessment. When the assessment is older than the window it
names, say so and offer a fresh run; plan from it if the user wants.

### 2. Take the inputs

Three things decide the plan, and the user decides them. When the request
already states a thing, do not ask about it again. Ask for the open ones
in one message, with the default beside each, so that one reply settles
it. When no reply can come, as in an unattended run, take the defaults
and say so in the report.

- **The target rung**: how far up to plan. Default: the next level the
  assessment names. "The next level" is the one the assessment's
  next-level heading names, and it is one rung with one gate; when the
  ladder row for it also names a second gate ("Shapiro 4, agency 4 to
  5"), that second gate is the rung after it, outside a next-level-only
  plan. The top of the ladder is Yegge 8. Shapiro 5 is the far end and
  not a target; when the user names it, say so and plan to Yegge 8
  unless they insist.
- **The constraints**: which tools and harnesses the person has and which
  they do not; whether runs stay on their own machine; a tracker, a
  hosting service, a budget. Default: none. A constraint is kept in the
  user's words.
- **The plan's home**: with no ticket skill, the directory that receives
  the plan, default `level-up-plan` under the project directory; with a
  ticket skill, the project in the tracker, default a new project named
  `level-up`. Also where new mechanisms (scripts, rules, hooks, skills)
  will live: a repository the user names, default a new repository
  named after the plan, which the first task creates.

### 3. Lay out the rungs

Read the assessment's "Next level" section and "The ladder from here"
table, then the level-me next-steps reference for each level the plan
reaches (`../level-me/references/next-steps.md`, where the two skills are
installed side by side; the harness reference says where that is). At
Yegge 7 and 8 read the orchestration reference beside it as well.

- Rung 1 is the next level the assessment names. Each further row of the
  ladder table, up to the target, is one more rung.
- A rung has one gate: one level on one scale, or one score on one
  dimension, that the placement table of the next assessment can show.
  Where a ladder row names two ("Shapiro 4, agency 4 to 5"), make two
  rungs in the order the row names them.
- Name each rung by what it adds, not by its level alone: "Trusted check",
  "Unattended runs", "Ledger and merge queue". Record the gate with the
  name.
- Priority follows the rung: rung 1 high, rung 2 medium, the rest low.
- A rung's tasks open when the previous rung's gate closes. Never a
  calendar: the ladder has no dates, and the gate is a measurement.

### 4. Write the tasks

For each rung, take the steps from the assessment (rung 1) and from the
next-steps reference (later rungs), and turn each into tasks. The exact
setting, flag, hook, or file for the person's harness is in the level-me
harness reference for that harness.

- **One mechanism per task**: a script, a rule or instruction file, a
  hook, a skill, a subagent definition, a CI workflow, a setting on a
  service, a repository, or a policy the person keeps. A step that names
  two mechanisms is two tasks. Done means the mechanism exists at a path
  and was exercised once, with the result recorded on the task. An
  outcome is not a task; the mechanism that produces it is.
- **The brief**, four parts on every task:
  - *Scope*: what the mechanism does and what done looks like, in two to
    six sentences. For a mechanism the ladder names only by its effect
    ("an independent reviewer"), name the artifact: a subagent definition
    at a path, briefed with what it checks first.
  - *Files*: the repository or place, and the paths the task may change,
    as real paths. When the assessment names a repository without its
    path, find it on the machine by its name, or ask; a placeholder such
    as `<repo>` makes the brief one the agent cannot act on. New
    mechanisms go in the home from step 2.
  - *Acceptance*: how the result is checked: a command and its expected
    output; for code, a test that fails before the change and passes
    after; for a setting, the read-back; for a hook, one run that it
    blocked. "Record the output on this task" closes every acceptance.
  - *Do not touch*: what stays as it is, named.
- **Order and waits-on**: inside a rung, order the tasks so that each
  waits only on earlier ones, and name what it waits on by identifier.
  The first task of a rung waits on the previous gate. The gate waits on
  every other task of its rung.
- **The gate task**, last in every rung: run level-me; the assessment is
  updated in place; the rung closes when the placement table shows the
  gate; if it does not, the report names the missing mechanism, which
  becomes a new task in the rung, and the gate stays open. The ticket
  file reference shows the whole brief.
- **A check per kind of work.** The assessment says what kinds of work
  fill the window: code, documents, skills, operations. A check that
  covers only code leaves the rest unverified, so a rung whose gate needs
  a trusted check carries one check task per kind of work seen.
- **A decision the person must make** (which orchestrator, a spend
  threshold) is not a flag on another task. It is a task of its own
  whose mechanism is the record of the decision: a research note with
  the options and a choice, or a figure measured for long enough to set
  a threshold. Its Acceptance is that the record exists.
- **Rungs beyond the next two** still get every part of the brief, but
  Scope stays at the mechanism and its done condition, and the design
  document says those tasks are rewritten when their rung opens, because
  the tools at those rungs turn over within months.

Keep the counts honest: a rung with one task per mechanism the ladder
names is a plan; a rung with four tasks that each say "set up CI and a
merge queue and budgets" is a wish.

### 5. Apply the constraints

For every task, check every constraint. Where a constraint removes a
mechanism ("no cloud sessions" removes a cloud entry point), drop the
mechanism or replace it with the local form, and write the change in the
task's Constraint line in one sentence. Where a constraint leaves a ladder
step with no mechanism at all, say so in the design document's "Still
open" section rather than keeping a task the person cannot do. A task
the constraints forbid never appears in the plan. The design document
lists each constraint and the tasks it changed.

### 6. Write the plan out

With no ticket skill, write the directory tree and one file per task as
[references/ticket-file.md](references/ticket-file.md) says: one
directory per rung, the four state directories in each, every task in
`todo`, named `LVLUP-<N>.md` and numbered across the whole plan. Agree
the directory in step 2 and create nothing outside it.

With a ticket skill (`ticket-skill`), create the same plan in the
tracker as [references/ticket-operations.md](references/ticket-operations.md)
says: one container per rung, one ticket per task with the brief in its
description, the priority by rung, waits-on carried the way the tracker
can, and a read-back that counts what was made. The ticket skill's own
body says how each operation is done there.

When a plan already exists at the home, say so and ask before writing
over it; a new assessment usually means new tasks added to the existing
plan, not a second plan.

### 7. The design document

Write the document as [references/design-doc.md](references/design-doc.md)
says: the problem the assessment found, the constraints, the target, the
decisions and why, the ladder with its gates and task identifiers, the
consequences, and what is still open. File it through the configured docs
skill (`docs-skill`) as a design document under the project the
assessment is about, linked to the assessment; when unset, write it to
`design.md` in the plan directory.

### 8. Report

In the reply: the assessment used and its date; the ladder as a table
(rung, gate, number of tasks); where the plan is (the directory, or the
project and containers) and the design document's link or path; each
constraint and the tasks it changed; what is still open; and the first
task to take, by identifier. The person takes a task by hand or with a
ticket-working skill, where one is installed; this skill plans and does
not do the tasks.

## Judgment calls

- **The assessment is the input, not the author.** Its steps are the
  rungs' spine; the plan adds the mechanism, the path, the check, and the
  order. Where the assessment and the next-steps reference disagree on
  what the next level needs, the assessment wins: it saw this machine.
- **Several harnesses.** When the assessment shows sessions in more than
  one harness, each mechanism is one portable task plus one thin adapter
  task per harness with sessions. A harness with no sessions gets no
  tasks; the design document says a mirror opens on evidence of sessions.
- **A team.** The assessment is of one machine. Team mechanisms the
  assessment lists under what it could not see (branch protection, CI,
  required reviews) are tasks whose Files name the hosting service, with
  the read-back as acceptance.
- **Freedom before the check.** The order inside a rung always puts the
  check before the freedom it makes safe: the deny rule before
  auto-approval, the Stop hook before unattended runs, isolation before a
  second parallel writer. A plan never carries a task that turns prompts
  off, leaves runs unattended, or adds agents ahead of the task that
  makes it safe.
- **Size.** Fewer tasks than the mechanisms the ladder names for a rung
  means steps were merged; a task per sub-part of one mechanism means it
  was split. Either way the gate cannot close on it.

## Bounds

- Never change the assessment. The gate task updates it later, through
  level-me.
- Never write tasks into a project, a directory, or a repository the
  user did not name in step 2.
- Never do a task. The plan is the output.
- Never set a date on a task or a rung.
