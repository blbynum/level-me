# Ticket files

The plan's default output: one Markdown file per task, in a directory tree
that works as a board. Read this at step 6 when no ticket skill is
configured. The files carry everything a tracker ticket would, so that a
ticket-working skill, or a person, can take one without the conversation
that produced it, and so that the same plan can be loaded into a tracker
later without rewriting.

## Contents

- The tree
- Numbering
- The task file
- The gate task file
- Moving a task

## The tree

```
<plan-dir>/
  design.md                      the design document, when docs-skill is unset
  rung-1-enforced-rules/
    todo/
      LVLUP-1.md
      LVLUP-2.md
      LVLUP-3.md                 the gate task, last in the rung
    in-progress/.keep
    review/.keep
    done/.keep
  rung-2-trusted-check/
    todo/
      LVLUP-4.md
      ...
    in-progress/.keep
    review/.keep
    done/.keep
```

- `<plan-dir>` is the directory agreed in step 2. Create it when it does
  not exist; this is the one directory the skill may create, because the
  user named it.
- One directory per rung, named `rung-<n>-<slug>`: `<n>` counts from 1 at
  the first rung above the current placement, and `<slug>` is the rung's
  name in lowercase with hyphens. The current rung gets no directory:
  there is nothing to do on it.
- Four state directories in each rung: `todo`, `in-progress`, `review`,
  `done`. Every task starts in `todo`. A `.keep` file holds each empty
  directory under version control, because git does not keep an empty
  directory and the board needs all four.

## Numbering

Task files are named `LVLUP-<N>.md`. `<N>` runs across the whole plan: rung
by rung, and inside a rung in the order of work, with the gate task last.
A task's number never changes after the plan is written; a task added
later takes the next free number, whichever rung it joins. The number is
the task's identifier everywhere: in "Waits on" lines, in the design
document, and in the report.

## The task file

The title line carries the identifier and the title. A short list carries
the fields a tracker would hold as columns. Then the four parts of the
brief, each under its own heading, so that a check for a complete brief
is a search for four headings.

```markdown
# LVLUP-2: Deny rule for destructive commands

- Rung: 1, Enforced rules. Closes when the assessment shows Yegge 3.
- Order: 2 of 3 in rung 1
- Waits on: LVLUP-1
- Priority: high
- Mechanism: setting
- Constraint: none

## Scope

A deny rule in the harness's user settings for the commands that must
never run: recursive deletion outside the working directory, a force
push, a history rewrite on the default branch. The rule is the
enforcement that makes auto-approval safe at the next rung. Done means
the rule exists in the settings file and one denied command was tried
once, with the harness's refusal recorded on this task.

## Files

The harness's user settings file (the level-me harness reference names
it); the acme-billing repository is the place to try the denied command,
with no change to its files.

## Acceptance

Run a command the rule covers in a fresh session; the harness refuses it
and the refusal is quoted on this task. Run a command the rule does not
cover; it runs.

## Do not touch

The project settings files; the allow list; the instruction files.

Assessment: ~/src/acme/billing/ai-coding-level-assessment.md
```

Field rules:

- **Rung**: the number, the name, and the gate in one line, copied from
  the rung's definition in step 3.
- **Order**: this task's place among the rung's tasks. The gate task is
  always last.
- **Waits on**: the identifiers this task needs done first, or `none`.
  The first task of a rung waits on the previous rung's gate task; the
  gate task waits on every other task in its rung.
- **Priority**: `high` for rung 1, `medium` for rung 2, `low` for the
  rest, so a tracker's ordering matches the ladder.
- **Mechanism**: one word for the kind: `script`, `rule`, `hook`,
  `skill`, `agent`, `ci`, `setting`, `policy`, `repository`, `gate`.
- **Constraint**: `none`, or the constraint and what it changed in this
  task, in one line: "one machine, no cloud sessions: the cloud entry
  point is dropped; the local launcher is the only path".
- The last line links the assessment the plan came from, as a path or a
  URL.

## The gate task file

The last task of every rung. Its brief has the same four parts.

```markdown
# LVLUP-3: Gate: re-run level-me for Yegge 3

- Rung: 1, Enforced rules. Closes when the assessment shows Yegge 3.
- Order: 3 of 3 in rung 1
- Waits on: LVLUP-1, LVLUP-2
- Priority: high
- Mechanism: gate
- Constraint: none

## Scope

Run level-me on this machine. The assessment document is updated in
place. The rung closes when the placement table shows Yegge 3. If it
does not, the report names the missing mechanism: add a task for it to
this rung, numbered after the plan's last task, and leave this task open.

## Files

The assessment document.

## Acceptance

The placement table of the new assessment shows Yegge 3. This task and
every other task of the rung are in `done`.

## Do not touch

Nothing else.

Assessment: ~/src/acme/billing/ai-coding-level-assessment.md
```

## Moving a task

A task moves between the four state directories by a file move, and its
name never changes. A person or a ticket-working skill claims a task by
moving it to `in-progress` and adding a line `- Claimed by: <session id>`
after the field list; a result goes at the end of the file under
`## Report`; a task that is ready for the person moves to `review`; and
the person moves it to `done`. When the plan directory is under version
control, each move is a commit, which is what makes a second claim of the
same task visible.
