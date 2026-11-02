# GitHub Copilot

Where Copilot keeps instructions, what its approval settings mean for
the scores, and how each next step is set up. Read this when
`.github/copilot-instructions.md`, `.github/instructions/`, or a
`~/.copilot` directory is present, or when the editor's settings carry
Copilot keys. Facts are from the vendor documentation as of November
2026; the cloud agent was renamed "Copilot in the cloud" for paid plans
in late October 2026.

## Where things live

| Item | Path |
|---|---|
| Repository instructions | `.github/copilot-instructions.md`; `.github/instructions/*.instructions.md`; `AGENTS.md`; the cloud agent also reads `CLAUDE.md` and `GEMINI.md` |
| Custom agents | `.github/agents/` |
| Editor approval settings | The editor's user settings: `chat.tools.terminal.autoApprove`, `chat.permissions.default`, `chat.tools.global.autoApprove`; `/yolo` or `/autoApprove` for one session |

## Modes and the agency score

| Setting | Agency score |
|---|---|
| Agent mode with per-tool approvals | 1 |
| Terminal auto-approve for read-only commands | 2 |
| Global auto-approve or a `/yolo` session | 3 |
| Copilot in the cloud used for bounded tasks | 4 |

## Multi-agent features

Copilot in the cloud researches, plans, and implements in a cloud
sandbox or a CI runner, one branch and one pull request per task, with
a 59-minute cap per CI session. Branch rules can stop it from opening
pull requests; "Logs do not replace your own review and testing." Agent
Merge works a pull request's blockers. Each task is one agent; running
several supports orchestration 2.

## Setting up each next step

| Step | In Copilot |
|---|---|
| Name the check | A line in `.github/copilot-instructions.md` or `AGENTS.md` |
| Enforce a rule | Branch protection and required checks on the repository; the editor's deny settings |
| Turn prompts off | Terminal auto-approve, then global auto-approve |
| Unattended bounded runs | Assign an issue to Copilot in the cloud |
