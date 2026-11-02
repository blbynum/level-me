# Sources

Subject-matter ledger for the level-me skill. Not linked from SKILL.md.
Each entry: URL, date last read, what in the skill it supports, and the
vintage the finding was measured on. The research synthesis that fed
the first version is `~/projects/ai/ai-coding-levels-research-2026-11-02.md`.

## Scales

### Yegge, "Welcome to Gas Town" (Medium, 2026-01-01)
- URL: https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04
- Last read: 2026-11-02, via a wiki copy (the primary returns 403); stages
  6 to 8 wording and "Gas Town is only for those at Stage 7 or 8".
- Supports: scales.md stage wording for 6 to 8.

### Pragmatic Engineer, "Steve Yegge on AI agents..." (2026-02-10) and podcast transcript (2026-03-11)
- URL: https://newsletter.pragmaticengineer.com/p/steve-yegge-on-ai-agents-and-the ; https://podscripts.co/podcasts/the-pragmatic-engineer/from-ides-to-ai-agents-with-steve-yegge
- Last read: 2026-11-02 (free portion; podcast transcript 100k of 109k chars).
- Supports: the eight levels verbatim; "three productive hours"; "70% aren't doing it"; "half an hour a day"; "I've made a mess".

### O'Reilly Radar, "Steve Yegge wants you to stop looking at your code" (2026-03-12)
- URL: https://www.oreilly.com/radar/steve-yegge-wants-you-to-stop-looking-at-your-code/
- Last read: 2026-11-02.
- Supports: "first four levels are about IDE use"; burnout and exhaustion; "fire up another one".

### Yegge, "Revenge of the Junior Developer" (Sourcegraph, 2025-03-22)
- URL: https://sourcegraph.com/blog/revenge-of-the-junior-developer
- Last read: 2026-11-02.
- Supports: six waves; fleets as supervisors over agents; "Switch to chat. Ditch completions."; the 5x claim (unmeasured).

### Shapiro, "The Five Levels: from Spicy Autocomplete to the Software Factory" (2026-01-23)
- URL: https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/
- Last read: 2026-11-02, in full.
- Supports: Levels 0 to 5 wording; "feels like you are done"; "almost everyone tops out here"; the 90% estimate at Level 2; Level 4 practices; Level 5 rarity ("less than five people").

### Willison, "The Five Levels" link post (2026-01-28) and "software factory" (2026-02-07)
- URL: https://simonwillison.net/2026/jan/28/the-five-levels ; https://simonwillison.net/2026/Feb/7/software-factory
- Last read: 2026-11-02.
- Supports: a real Level 5 team exists; "$20,000/month per engineer" extrapolation; reservations.

### Osmani, "Agentic Autonomy Levels" (2026-07-02)
- URL: https://addyosmani.com/blog/agentic-autonomy-levels/
- Last read: 2026-11-02.
- Supports: six agency levels and the orchestration axis; "Move up one axis at a time"; "Every step up the lever requires a new set of safety mechanisms"; "A single agent kept busy by human handoffs is Level 4 with a dashboard"; Yegge's ladder as "the scale most often mentioned".

### Anderson, "The AI Codebase Maturity Model" (arXiv 2604.09388, v2 2026-04-27)
- URL: https://arxiv.org/abs/2604.09388
- Last read: 2026-11-02, full PDF text.
- Supports: six levels, feedback-loop definitions, artifacts, human roles, triggers, anti-patterns; "cannot skip levels"; "adding another feedback mechanism"; Level 6 criteria; Hive design; throughput table (n=1, author's project; reported as such).

### Berkeley RDI, "Towards Autonomous Software Development" (2026-07-26)
- URL: https://rdi.berkeley.edu/blog/auto-software-dev
- Last read: 2026-11-02 (blog; PDF not read).
- Supports: Levels I to III; specification granularity, temporal autonomy, oversight mode; "advance only when the challenges... have been demonstrably addressed".

### Other scales (read 2026-11-02 unless noted)
- Sourcegraph Levels of Code AI: https://sourcegraph.com/blog/levels-of-code-ai (2023-10-04).
- BlueOptima Coding Automation Framework: https://www.blueoptima.com/ai-access/autonomous-coding-are-we-there-yet (2024; distribution figures).
- Cloud Security Alliance: https://cloudsecurityalliance.org/blog/2026/01/28/levels-of-autonomy
- Dash0 six levels: https://dash0.com/knowledge/the-six-levels-of-agentic-software-engineering (updated 2026-06-02).
- Arden's ladder: https://jedarden.pages.dev/notes/agentic-coding-ladder/ (2026-05-23, updated 2026-10-27).
- Swarmia: https://www.swarmia.com/blog/five-levels-ai-agent-autonomy/ (2026-03-19).
- ELEKS: https://eleks.com/blog/ai-sdlc-maturity-model/ (2026-02-16).
- Coder: https://coder.com/blog/coder-launches-ai-maturity-self-assessment-to-help-enterprises-benchmark-agentic (2026-01-29).
- Phoenix, "The Five Levels Are Gated by Verification": https://understandingdata.com/posts/five-levels-gated-by-verification/ (undated 2026).

## Evidence on practice and outcomes (read 2026-11-02)
- METR 2025 RCT: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ (19% slower; 16 developers).
- METR 2026 update: https://metr.org/blog/2026-02-24-uplift-update/ (weak speedup; time a bad proxy with parallel agents).
- DORA 2025: https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report ; capabilities model https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model (seven capabilities; "amplifies what's already there"; stability down).
- Faros "Speed Trap" (2026-09-18): https://www.faros.ai/blog/ai-speed-trap-takeaways (merged without review 31.3% to 76.3%; review capacity).
- Faros "Acceleration Whiplash" (Q2 2026): https://faros.ai/research/ai-acceleration-whiplash
- Anthropic skill-formation RCT (2026-01-29): https://www.anthropic.com/research/AI-assistance-coding-skills (17-point comprehension gap; 52 developers).
- Anthropic Economic Index (2025-04-28; 2026-01-15): https://www.anthropic.com/research/impact-software-development ; https://www.anthropic.com/news/anthropic-economic-index-january-2026-report
- Stack Overflow 2025 and 2026: https://survey.stackoverflow.co/2025/ai ; https://survey.stackoverflow.co/2026/ai
- GitHub Octoverse 2026 (2026-10-28): https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/
- Pragmatic Engineer AI tooling survey (2026-03-03): https://newsletter.pragmaticengineer.com/p/ai-tooling-2026
- StrongDM software factory (2026-02-06): https://factory.strongdm.ai ($1,000 tokens per engineer per day; holdout scenarios; digital twins).
- Fowler fragments (2026-05-27): https://martinfowler.com/fragments/2026-05-27.html (cognitive endurance; Tornhill quote).
- Böckeler, harness engineering (2026-04-02): https://martinfowler.com/articles/harness-engineering.html (guides and sensors; AI-written tests "not good enough yet").

## Harness documentation (read 2026-11-02; vendor pages undated, versions noted)
- Claude Code permissions and modes: https://code.claude.com/docs/en/permissions ; https://code.claude.com/docs/en/permission-modes (v2.1.283 auto default; v2.1.302 headless Manual; v2.1.314 cited).
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Claude Code best practices: https://code.claude.com/docs/en/best-practices (unattended checklist; "you are the test suite"; "the single most useful line in your CLAUDE.md").
- Claude Code agent teams, worktrees, workflows: https://code.claude.com/docs/en/agent-teams ; https://code.claude.com/docs/en/worktrees ; https://code.claude.com/docs/en/workflows
- Transcript record fields: observed on this machine's `~/.claude/projects` files, Claude Code 2.1.287 to 2.1.309, 2026-11-02 (type, permissionMode, entrypoint, turnOrigin, isSidechain, toolUseResult, isMeta, subagents directory).
- Cursor: https://cursor.com/docs/agent/modes ; https://cursor.com/docs/cloud-agent ; run modes via a documentation mirror snapshot 2026-06-26 (Cursor 3.6); `~/.cursor/cli-config.json` keys observed locally.
- Codex: https://learn.chatgpt.com/docs/codex/cli (v0.143); approval and sandbox values via mirrors and third-party posts (2026-03-26, 2026-04-08), not an official page.
- Copilot: https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent ; instruction files changelog 2025-08-28; editor settings via Microsoft docs (summary only).
- Gemini CLI: https://geminicli.com/docs/cli/cli-reference.md ; https://github.com/google-gemini/gemini-cli (Antigravity note 2026-06-18).
- Aider: https://aider.chat/docs/config/options.html ; OpenCode: https://opencode.ai/docs/permissions/ (2026-11-02); Amp: https://ampcode.com/manual

## Orchestrators (READMEs and docs read 2026-11-02)
- Gas Town: https://github.com/steveyegge/gastown ; Gas City: https://github.com/gastownhall/gascity ; Beads: https://github.com/steveyegge/beads
- Hive: https://github.com/kubestellar/hive (now hivecommons/hive)
- Symphony: https://github.com/openai/symphony
- Ralph: https://ghuntley.com/ralph/ (2025-07-14)
- Overstory: https://github.com/jayminwest/overstory (archived 2026-05-28)
- Paperclip: https://github.com/paperclipai/paperclip
- Claude Squad: https://github.com/smtg-ai/claude-squad ; Conductor: https://conductor.build/docs ; ccmanager: https://github.com/kbwo/ccmanager ; vibe-kanban: https://github.com/BloopAI/vibe-kanban
- Vendor cloud agents: https://learn.chatgpt.com/docs/cloud ; https://jules.google/docs ; https://docs.devin.ai/ ; https://github.com/OpenHands/OpenHands ; https://docs.factory.com/
