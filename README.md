# ai-scaling-skills

One Agent Skill, `level-me`, that assesses how a person or a team uses AI
coding tools. It reads the harness configuration and the recent session
transcripts on a machine, places the setup on the AI coding maturity
scales (Yegge's eight levels, Shapiro's Levels 0 to 5, and three scored
dimensions: agency per agent, orchestration across agents, and feedback
infrastructure), and gives the practical next steps, level by level, up to
a full orchestration pipeline. The skill is a directory in `skills/` with
a `SKILL.md` under the [Agent Skills standard](https://agentskills.io/).
The repository is not installed into a harness; `link.sh` links it into
one.

## Contents

- [Install](#install)
- [Use the skill](#use-the-skill)
- [Update](#update)
- [What is here](#what-is-here)
- [Per-machine configuration](#per-machine-configuration)
- [Portability](#portability)
- [The provenance ledger](#the-provenance-ledger)
- [Requirements](#requirements)
- [Versioning](#versioning)

## Install

1. Clone the repository to a location that stays. The links point into
   the clone, so they break if you move or delete it.

   ```sh
   git clone git@github.com:blbynum/ai-scaling-skills.git ~/src/ai-scaling-skills
   cd ~/src/ai-scaling-skills
   ```

2. Run the link script for your harness. For Claude Code:

   ```sh
   ./link.sh --harness claude-code
   ```

   Output for a clone at `~/src/ai-scaling-skills`:

   ```text
   Repository: /Users/you/src/ai-scaling-skills
   Harness:    Claude Code (claude-code)
   Skills:     /Users/you/.claude/skills
     linked level-me

   The links point into /Users/you/src/ai-scaling-skills.
   The files stay there; the harness reads them through the links.
   To change a skill's settings on this machine, edit config.local.yaml in
   the skill's directory, /Users/you/src/ai-scaling-skills/skills/<name>/. Git ignores that file.
   To get updates, run "git pull" in /Users/you/src/ai-scaling-skills, then run this command again:
     /Users/you/src/ai-scaling-skills/link.sh --harness claude-code
   It links added skills and rules, and removes the links to deleted ones.
   ```

3. To link the skill into one more harness, run the script again with
   that harness's id. `./link.sh --list` shows the ids and their
   directories:

   ```text
     ID           HARNESS         SKILLS                    RULES
     claude-code  Claude Code     ~/.claude/skills          ~/.claude/rules
     codex        Codex           ~/.agents/skills          none
     cursor       Cursor          ~/.cursor/skills          none
     copilot      GitHub Copilot  ~/.copilot/skills         ~/.copilot/instructions
     gemini-cli   Gemini CLI      ~/.gemini/skills          none
     antigravity  Antigravity     ~/.gemini/config/skills   ~/.gemini/config/rules
     custom       (you choose)    --skills-dir <dir>        --rules-dir <dir>
   ```

   Run `./link.sh` with no arguments for a menu, and `./link.sh --help`
   for the full reference.

To unlink, delete the symbolic link `level-me` in the harness's skills
directory, for example `~/.claude/skills/level-me`. The clone does not
change.

## Use the skill

In a session, ask for an assessment in your own words, for example "what
level of AI coding am I at?" or "level me". In Claude Code, `/level-me`
invokes it by name. The skill runs its scanner, reads a sample of recent
sessions, and reports a placement with the evidence behind it, what is
already in place, the next level's missing prerequisite and steps, the
ladder from there, and what it could not observe from the machine. The
report names files, settings, counts, and session identifiers, and never
quotes a prompt, a message, or code from a transcript.

The scanner also runs on its own. It prints counts, file names, and
setting values, never transcript content:

```sh
python3 skills/level-me/scripts/scan.py --project <project-dir> --quiet
```

`<project-dir>` is the project to assess; the default is the current
directory. `--quiet` prints only the derived summary. The output is
similar to the following:

```text
{
  "agency_0_to_5": 3,
  "feedback_0_to_5": 2,
  "needs_transcript_reading": [
    "whether diffs are read before acceptance (Yegge 3 vs 4; Shapiro 2 vs 3)",
    "whether work starts from a spec or plan (Shapiro 4)",
    "whether runs finish unattended with a self-check (Yegge 5; Osmani L3)",
    "whether corrections repeat across sessions (feedback L1 vs L2)"
  ],
  "orchestration_0_to_5": 2,
  ...
}
```

The scores are heuristics from configuration and counts. The skill treats
them as the starting point and settles the open questions by reading
transcripts. Sessions that an eval runner or a batch job started are
counted apart from interactive ones, so a machine that runs many headless
sessions is not scored on them.

## Update

Run `git pull` in the clone. A pull changes the linked skill at once.
Then run the command that the last run of `link.sh` printed; it links
added skills and removes links to deleted ones:

```sh
~/src/ai-scaling-skills/link.sh --harness claude-code
```

## What is here

| Path | What it does | Config keys |
|---|---|---|
| `skills/level-me/` | Assesses AI coding tool usage from harness configuration and session transcripts, places it on the maturity scales, and gives next steps up to an orchestration pipeline. Its `references/` hold the scales, the scoring rubric, the next steps per level, the orchestration tools, and one file per harness. Its `scripts/scan.py` collects the signals. | none |
| `link.sh` | Links the skills in `skills/` and the rules in `rules/` into a harness's user-level directories. A copy of the link script from [meta-skills](https://github.com/blbynum/meta-skills/blob/master/link.sh). | |
| `AGENTS.md` | Instructions for agents that work on this repository: the versioning procedure. `CLAUDE.md` and `GEMINI.md` import it. | |
| `VERSION` | The repository version, `major.minor.snapshot`. | |

## Per-machine configuration

A skill reads its values from `config.local.yaml` in its own directory,
which git ignores. A skill whose required key is missing stops and offers
to write the file. `level-me` has no config keys, so there is nothing to
configure.

## Portability

`level-me` is a portable skill (`metadata.harness: portable`,
`last-verified: 2026-11-02`). Its body names actions, not tools, and
every harness fact lives in `references/<harness-id>.md`: `claude-code`,
`cursor`, `codex`, `gemini-cli`, and `copilot`. The portability check ran
on 2026-11-02 with zero hits.

Limits as of 2026-11-02: the skill has run only in Claude Code (2.1.287
and 2.1.309). The scanner parses Claude Code transcripts in detail; for
Codex it counts sessions, and for Cursor, Gemini CLI, and Copilot it reads
configuration only. An assessment in another harness therefore rests on
that harness's configuration plus what the person reads by hand.

## The provenance ledger

The sources behind the skill's guidance, with the date each was last
read, are in `skills/level-me/sources.md`. The skill never links that
file, so it costs no context when the skill loads.

## Requirements

- A harness that reads the Agent Skills standard.
- `link.sh`: a POSIX shell and `git`.
- The scanner, `skills/level-me/scripts/scan.py`: Python 3.8 or later,
  standard library only. Tested on Python 3.9.6 and 3.12; no 3.8 was
  available for a test run. Without Python, the skill's harness
  references give the manual inspection steps.

## Versioning

`VERSION` holds the version as `major.minor.snapshot`. `master` is the
development branch. The level comes from the change's effect on a person
who already has the repository linked into a harness: major when
something they had stops working after `git pull` and a new run of
`link.sh`; minor when the install gains something and nothing breaks;
snapshot for every other change. A branch named after each version marks
its last state, so `git checkout 1.0` gives the last state of version 1.0.
`AGENTS.md` holds the procedure for agents.

`link.sh` has a version of its own, from its source, which `./link.sh
--version` prints. This repository replaces the script whole when it
updates it and never edits it.
