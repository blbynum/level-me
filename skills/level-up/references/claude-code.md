# Claude Code

What differs when level-up runs in Claude Code. Read this before step 1.
Nothing here applies in another harness.

- **Invocation.** `/level-up` invokes the skill by name; a prose request
  that the description catches loads it too. The target rung, the
  constraints, and the plan's home can all be in the same message, and
  then step 2 asks nothing.
- **The level-me references.** `link.sh` links both skills into
  `~/.claude/skills/`, so the sibling path `../level-me/references/` from
  this skill's directory resolves to `~/.claude/skills/level-me/references/`.
  The ladder is in `next-steps.md` there, the orchestration tools in
  `orchestration.md`, and the exact setting, flag, or file for each
  mechanism in Claude Code in `claude-code.md`.
- **The assessment.** level-me in Claude Code files its report through
  its own `docs-skill` when one is set, else as a Markdown file in the
  project directory. The skill's own config does not say which; look in
  both places.
- **The gate task.** In Claude Code the gate task's instruction is "run
  `/level-me`". A headless gate run is `claude -p "/level-me"` in the
  project directory, with a permission mode that lets the scanner run.
- **The plan directory.** A file write under the current project is
  auto-approved in the accept-edits and auto modes; a write elsewhere
  prompts, so agree a plan directory inside the project when the run is
  unattended.
