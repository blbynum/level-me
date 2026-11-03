# Operations asked of the ticket skill

What level-up asks of the skill named in `ticket-skill`, in the vocabulary
of the ticket platform contract that a ticket-working skill also relies
on. Read this at step 6 when `ticket-skill` is set. The ticket skill does
each operation in its tracker's own way and says how in its own body;
level-up speaks only in the vocabulary below, so a change of tracker
changes one config value.

## Contents

- Vocabulary
- Operations
- Order of calls
- The brief in a ticket
- When an operation is not possible

## Vocabulary

- **Project**: where the plan's tickets live, named by the user in step 2.
- **Container**: one per rung. A module in Plane; an epic, a milestone, or
  a label elsewhere. The ticket skill says which its tracker has.
- **Ticket**: one per task, with an identifier of the form PROJECT-N that
  the tracker assigns.
- **Brief**: the ticket's description: Scope, Files, Acceptance, Do not
  touch.
- **States**: *claimable* (open, a run may start from it) and *not yet
  open* (waits on another ticket or on a rung that has not opened). The
  ticket skill maps each to its tracker's state names.
- **Priority**: `high`, `medium`, `low`, by rung.
- **Link**: a stable URL for a ticket, or its identifier when the tracker
  has none configured.

## Operations

| Operation | What level-up sends | What it expects back |
|---|---|---|
| Find project | The project's name or identifier | The project, or that it does not exist |
| Create project | A name, an identifier, a one-paragraph description | The project, or that the platform cannot create one, so the user creates it by hand |
| Create container | The project; the name `Rung <n>: <name>`; a description that states the gate; a status of planned for rung 1 and not started for the rest | The container, with its identifier or name |
| Create ticket | The project; the container; the title; the brief in Markdown; the priority; the state: claimable for a rung 1 task that waits on nothing, not yet open for every other; the labels where the project has them (the mechanism kind, and `gate` for a gate task) | The identifier |
| Record waits-on | The ticket and the identifiers it waits on | A dependency where the tracker has them, else a comment that says "Blocked by" and names them |
| Set description | The project: a paragraph that names the assessment, the design document, and the conventions (claimable and claimed states, the order carried by priority and container) | The read-back |
| Link | A ticket | The link |

## Order of calls

1. Find the project; create it when the user named one that does not
   exist and the platform can.
2. One container per rung, in rung order.
3. The tickets rung by rung, in the plan's order, the gate last in each,
   so that the tracker's identifiers follow the order of work.
4. The waits-on records, after every ticket exists, because they name
   identifiers.
5. The project description, once the design document has a link.
6. Read back: the containers, and the ticket count per container. A write
   that returns nothing, such as adding a ticket to a container, is
   confirmed only by the read-back. Report the counts.

## The brief in a ticket

The ticket's description is the task file's body from the first field
line down, without the title line: the field list, then the four parts
under their headings, then the assessment link. The identifier in the
"Waits on" line is the tracker's, not the file numbering, so write the
waits-on lines after step 3 assigns the identifiers. The file numbering
`LVLUP-N` does not appear in the tracker.

## When an operation is not possible

The ticket skill says so and offers the nearest alternative, with its
cost. It does not do something else in silence. level-up takes the
alternative when it keeps the plan whole (a label in place of a
container; a comment in place of a dependency), and otherwise reports the
gap to the user with the operation the ticket skill lacks, so that a
follow-up for that skill can be opened.
