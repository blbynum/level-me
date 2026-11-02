# Gemini CLI

Where Gemini CLI keeps configuration, what its approval modes mean for
the scores, and how each next step is set up. Read this when a
`~/.gemini` directory or a `GEMINI.md` file is present. Facts are from
the vendor documentation as of mid-2026; note that free individual
access moved to a successor product in June 2026, so check which CLI
the user runs.

## Where things live

| Item | Path |
|---|---|
| Settings | `~/.gemini/settings.json` |
| Instruction files | `~/.gemini/GEMINI.md` (user); `GEMINI.md` in the project; reloaded with `/memory reload` |
| Sessions | Listed with `--list-sessions`; temporary data under `~/.gemini/tmp/` |

## Approval modes

`--approval-mode` takes `default` (prompts), `auto_edit` (edit tools
auto-approved), `yolo` (everything auto-approved; only from the command
line), and `plan` (read-only). The bare `--yolo` flag is deprecated.
`-p` forces non-interactive mode; `--sandbox` runs in a sandbox.

| Mode | Agency score |
|---|---|
| `default`, `plan` | 1 |
| `auto_edit` | 2 |
| `yolo` | 3; 4 when used with `-p` for unattended bounded runs |

## Setting up each next step

| Step | In Gemini CLI |
|---|---|
| Name the check | A line in `GEMINI.md` |
| Enforce a rule | `--sandbox`; hooks where the installed version documents them |
| Turn prompts off | `--approval-mode auto_edit`, then `yolo` |
| Unattended bounded runs | `-p` with `--approval-mode yolo` inside a sandbox |
