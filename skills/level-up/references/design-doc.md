# The design document

The short document that goes with every plan. Read this at step 7. It
holds the reasons, so that any task can be done without the conversation
that produced the plan, and so that the next assessment can be read
against what the plan set out to change. It is a design document in the
docs skill's sense: the problem and its constraints, the decision and
why, the consequences, and what is still open.

## Contents

- Title and opening
- Sections
- Filing

## Title and opening

Title: `<plan name> design: <what rung 1 adds> to <target>`, for example
"Level-up design: enforced rules to Yegge 5". The plan name is the one
agreed in step 2; `level-up` when none was.

The opening paragraph, two or three sentences: the date the plan was
decided; a link to the assessment it came from, with the assessment's
date; where the tasks live (the plan directory, or the tracker project
and its containers).

## Sections

In this order, one heading each. Keep the whole document to what a reader
needs to act: two to four pages.

1. **The problem.** The placement the assessment gives, and the gap it
   names to the next level, in one paragraph. Then the evidence behind the
   gap, as bullets taken from the assessment: the settings, files, counts,
   and sessions it cites. No new claims: everything here is in the
   assessment.
2. **The constraints.** One bullet per constraint the user stated, in
   their words, and one line on what it rules out. When the user stated
   none, say so.
3. **The target.** The rung the user chose and the ladder from the
   current placement to it, one line per rung. Say what was left out and
   why: Shapiro 5 is the far end of the ladder and not a target.
4. **The decisions.** A table with three columns: Decision, Instead of,
   Why. One row per choice the plan makes that a reader could have made
   differently. At least these rows:
   - One mechanism per task, done when it exists at a path and was
     exercised once with the result recorded. Instead of tasks by
     outcome. A mechanism can be checked; an outcome is argued.
   - One container per rung, closed by a gate task that re-runs level-me.
     Instead of dates. The ladder has no calendar; the gate is a
     measurement.
   - Where the new mechanisms live, and why there.
   - How order is carried: numbering and waits-on lines in files, or
     priority, state, and dependency records in the tracker.
   - One row per constraint that changed a task, naming the tasks and
     the change.
   - For a plan that reaches two or more rungs above the next: the tasks
     of the later rungs are written at the mechanism level and are
     rewritten when their rung opens, because the tools at those rungs
     turn over within months.
5. **The ladder and its gates.** A table: Rung, Container or directory,
   Tasks (the identifiers, first to last), What it adds, Closes when the
   assessment shows. Then one line: a rung's tasks open when the previous
   rung's gate closes; inside a rung, a task that needs another's output
   waits on it.
6. **Consequences.** What the plan costs and changes for the person, in
   bullets: review load, token spend, a check added to every session, a
   habit given up. Take the costs from the assessment's next-level section
   and from the level-me next-steps reference for the later rungs.
7. **Still open.** The questions the plan leaves: a tool to choose, a
   figure to measure before a threshold is set, a ladder step a constraint
   left without a mechanism, a rung whose tasks will be rewritten.

## Filing

When `docs-skill` is set, hand the document to that skill as a design
document: the kind, the reader (the person, and the agents that take the
tasks), the title, the body, the project the assessment is about, and the
assessment as the related document to link. The docs skill files it and
returns the link; put the link in the report, and in the tracker
project's description when a ticket skill is set.

When `docs-skill` is unset, write the body to `design.md` in the plan
directory, with the title as a level-1 heading on the first line.
