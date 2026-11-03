---
name: level-me
description: Assesses how a person or team currently uses AI coding tools, from the harness configuration, instruction files, hooks, and recent session transcripts on this machine, and places the setup on the AI coding levels scales - Yegge's eight levels, Shapiro's Levels 0 to 5, and three measured dimensions (agency per agent, orchestration across agents, feedback infrastructure). Reports the evidence behind the placement and the practical next steps, level by level, up to a full orchestration pipeline. Use when the user asks "what level am I at", "level me", "assess my AI coding setup", "rate how I use Claude Code, Cursor, or Codex", "am I using AI coding tools well", "how do I get to the next level", or "how do I move toward agent orchestration or a software factory". Not for auditing one session's conduct (the retrospective skill), changing one harness setting, or writing a skill or rule.
compatibility: The bundled scanner needs Python 3.8 or later on the path; without it, follow the manual steps in the harness references.
metadata:
  harness: portable
  last-verified: "2026-11-02"
---

# Level me

Place a developer's or team's AI coding practice on the known maturity
scales from what is observable on this machine, then say what the next
level needs. Two failures make such an assessment worthless, and both are
the default under plain prompting:

- **Flattery.** A stage label is a compliment unless every placement names
  the evidence behind it. Every level claimed in the report cites an
  observation: a setting, a file, a count, or a session.
- **Treating higher as better.** Each level up trades review capacity,
  token spend, and the human's own understanding for throughput. The
  report says what the next step costs, and recommends it only when the
  verification machinery that makes it safe is in place or is the step.

## Config

| Key | Required | Default | Purpose |
|---|---|---|---|
| docs-skill | no | | skill that files the assessment as a document; when unset, write it to a Markdown file in the project directory |

Read `config.local.yaml` in this skill's directory before anything else.
A key missing there takes its Default from the table. If a required key is
missing or empty, stop: name the key and its purpose, and offer to write
`config.local.yaml` with the values the user gives. If a configured
directory does not exist, stop and say so; do not create it.

## Workflow

Copy this checklist into the response and check items off as you go:

```
- [ ] 1. Scope: whose setup, which harnesses, which window
- [ ] 2. Collect signals with the scanner
- [ ] 3. Read a sample of transcripts
- [ ] 4. Score the three dimensions
- [ ] 5. Place on the scales and state confidence
- [ ] 6. Write the next steps, from this level to a full pipeline
- [ ] 7. Report
```

### 1. Scope

- Decide the home directory and the project directory to assess. Default:
  the current user's home and the current working directory. If the user
  names another project, use it; if they ask about a team or another
  machine, say what this machine cannot show (other people's sessions,
  CI gates, branch protection) and assess what it can.
- Detect which harnesses are present: a configuration directory or an
  instruction file for each. The scanner in step 2 reports them with
  their session counts. Read the reference for the primary harness, the
  one with the most sessions in the window, before step 3, and the
  reference for any other harness only when it shows sessions or
  project files: [claude-code.md](references/claude-code.md),
  [cursor.md](references/cursor.md), [codex.md](references/codex.md),
  [gemini-cli.md](references/gemini-cli.md),
  [copilot.md](references/copilot.md). Each says where that harness keeps
  configuration and transcripts, what its permission modes mean, and how
  each next step is set up there. An installed harness with no sessions
  in the window gets one line in the report, not a reference read.
- The window is the last 30 days of transcripts unless the user asks for
  another. Say which window the report covers.

### 2. Collect signals

Run the scanner from the skill directory, or by its full path, where
`<skill-dir>` is the directory that holds this file. It prints counts,
file names, and setting values, and never prints transcript content:

```
python3 <skill-dir>/scripts/scan.py --project <project-dir> --json <scratch-path>/scan.json
```

Add `--home <dir>` for another home and `--days N` for another window.
If Python is not on the path, say so and collect the same signals by hand
with the manual steps in each harness reference; the report then says
the counts are approximate.

Read the `derived` block first: three scores from 0 to 5 with the reasons
behind each, a provisional placement, and a `needs_transcript_reading`
list. The scores are heuristics from configuration and counts. They are
the starting point for step 4, not the answer. Then read the harness and
transcript blocks for the facts the report will cite.

The scanner sets scripted sessions apart from interactive ones: a session
started from a temporary working directory, a one-turn session in a
no-prompt mode, or a session whose first prompt repeats in three or more
other sessions, came from an eval runner or a batch job, not from a
person. Scores and counts in the report use the interactive sessions, and
the report states both numbers, because a machine that runs evals or
batch jobs can hold ten scripted sessions for every interactive one.

### 3. Read a sample of transcripts

Open the newest five to eight sessions the scanner lists under
`newest_sessions`, and two subagent transcripts when any exist. Read the
user turns, the tool calls, and the final messages; skip tool results.
Look for the markers in the table and note each one as evidence with the
session it came from. Keep transcript content out of the report: counts,
paraphrase, and the session identifier only. Paraphrase means no words
from a user turn appear in the report, however short: write "one-word
approvals" or "asks for a summary instead of the diff", not the words
the person typed. The report's examples in the marker table below are
illustrations, not quotes to reuse.

| Marker | Bears on |
|---|---|
| Who writes the code: the person pastes code in, or the agent edits files | Agency; Shapiro 0 to 1 versus 2 and up |
| The person reads diffs before accepting ("change line 12", "looks good") versus checks outcomes ("do the tests pass?") | Agency; Yegge 3 versus 4; Shapiro 2 versus 3 |
| Work starts from a spec, plan, or goal condition, or from a one-line ask | Shapiro 4; Osmani L2 to L3 |
| The agent runs tests, lint, or a build before reporting done | Feedback infrastructure |
| Runs finish unattended: headless entry points, long gaps between turns, a stop condition | Yegge 5; Osmani L3 |
| The same correction appears in several sessions | Feedback L1 versus L2: a missing instruction file |
| Several sessions receive turns in the same minutes; subagents or teammates are dispatched | Orchestration; Yegge 6 and up |
| The agent commits, pushes, or opens pull requests itself | Agency and feedback gates |
| The person interrupts the agent often, or expresses fatigue or confusion over which session does what | Close steering; the cost of the current level |

### 4. Score the three dimensions

Use the rubric in [signals.md](references/signals.md). Each dimension
gets a score from 0 to 5 and the two or three observations that decide
it. When the scanner and the transcripts disagree, the transcripts win,
and the report says why.

- **Agency per agent**: how much one agent does between human decisions,
  from suggestions through approved actions, auto-approved actions,
  unattended runs, to runs with their own stop condition and self-check.
- **Orchestration**: how many agents run at once and who coordinates
  them, from one session through several by hand, isolated parallel
  workers, a shared work queue, to an external orchestrator with a merge
  gate.
- **Feedback infrastructure**: what the codebase encodes and enforces,
  from nothing through instruction files, a test command the agent runs,
  measurement in CI, closed loops that act on their own signals, to a
  pipeline that proposes and merges under policy.

### 5. Place on the scales

Map the three scores to the named scales with the tables in
[scales.md](references/scales.md). Report one Yegge level and one Shapiro
level. When the evidence cannot separate two adjacent levels, report the
range and the one question that would settle it; a range beats a false
point. State confidence as high, moderate, or low with the reason: how
many sessions were read, whether the harness references covered every
tool in use, and whether anything important is unobservable from this
machine.

Levels are a diagnostic vocabulary, not a ranking of worth. No scale in
use has a measured population behind it, and the published estimates of
where most developers sit are guesses; say so when the user asks.

### 6. Write the next steps

Use [next-steps.md](references/next-steps.md). For the current level:

1. Name the prerequisite the next level needs that the evidence shows
   missing. Each move up is an added feedback mechanism, never only more
   freedom for the agent: the check the agent can run itself, the
   instruction file, the isolation per worker, the work queue, the gate.
2. Give one to three concrete steps for the next level, each naming the
   mechanism and pointing at the harness reference for the exact setting,
   flag, or file.
3. Say what the step costs: review load, token spend, hours of attention,
   loss of understanding of the code.
4. Then compress the rest of the ladder up to the full orchestration
   pipeline into one short section, so the reader sees the whole path.
   [orchestration.md](references/orchestration.md) describes the
   pipeline's parts and the tools that provide each.

Do not recommend turning approval prompts off, leaving runs unattended,
or adding agents without the check that makes that step safe. If the
check is missing, the check is the step.

### 7. Report

Use this shape, and adapt section depth to what was found:

```
## Placement
| Scale | Level | Deciding evidence |
| Yegge | ... | ... |
| Shapiro | ... | ... |
| Agency / Orchestration / Feedback | n / n / n | ... |
Confidence: ... because ...

## What is already in place
(the settings, files, and practices observed, each with where it was seen)

## Next level: <name>
Missing prerequisite: ...
Steps: 1. ... 2. ... 3. ...
Cost: ...

## The ladder from here
(one line per further level, with its gate)

## Not observable from this machine
(what the assessment could not see)
```

The assessment is a document for a reader who will act on it. File it
through the configured docs skill (`docs-skill`) as a report, under the
project the assessment is about; when unset, write it to a Markdown file
in the project directory. The reply carries the placement table and the
next level; the filed report carries all of it.
End the reply by suggesting a run of level-up to plan the move.

## Judgment calls

- **A team versus a person.** This machine shows one person's practice.
  When the user asks about a team, assess the person, then list the
  team-level signals the report could not see: shared instruction files
  in the repository, CI gates, branch rules, review policy, and the
  organization's stated stance on AI use. Add the organization-level
  prerequisites from next-steps.md to the next steps, and suggest the
  same assessment on two or three other machines, because the gap
  between people tells a team more than any one number.
- **One harness or several.** Score the harness with the most sessions in
  the window as the primary; mention the others in one line each.
- **Old sessions.** A level reached once months ago and not since is not
  the current level. Weight the newest sessions.
- **Privacy.** The report may name files, settings, counts, and session
  identifiers. It never quotes prompts, code, or messages from a
  transcript.
- **Scope.** Assess what bears on the three dimensions. A stale
  permission entry, a missing command-line tool, or a duplicate link
  noticed on the way is not a level signal; mention at most one such
  item in one line, or leave it out. The assessment is not a general
  audit of the machine.
- **Cost of the assessment.** Reading five to eight sessions is enough
  to settle the questions the scanner leaves open. Reading more raises
  cost without changing the placement; say how many were read.

## Old patterns

- A single trust axis for everything. The earlier ladders put one agent's
  autonomy and many-agent coordination on one line, so a person running
  five supervised agents and a person running one unattended agent got
  the same number. Score agency and orchestration apart.
- Reading "most developers are at level N" as data. Those figures are the
  scale authors' estimates. Report them as estimates or not at all.
