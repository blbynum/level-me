# Codex

Where the Codex CLI keeps configuration and transcripts, what its
approval policy and sandbox mean for the scores, and how each next step
is set up. Read this when a `~/.codex` directory is present. Facts are
from the vendor documentation as of November 2026 (CLI 0.143 cited),
with the approval values confirmed only through documentation mirrors.

## Where things live

| Item | Path |
|---|---|
| Configuration | `~/.codex/config.toml`: `approval_policy`, `sandbox_mode`, `model`, per-project trust levels |
| Instruction files | `~/.codex/AGENTS.md` (user); `AGENTS.md` in the project (`/init` creates it) |
| Transcripts | `~/.codex/sessions/<year>/<month>/<day>/*.jsonl`; an index in `~/.codex/session_index.jsonl` |
| Managed policy | `requirements.toml` can forbid `approval_policy = "never"` and restrict hooks with `allow_managed_hooks_only` |

## Approval policy and sandbox

Two orthogonal settings: who approves, and what the sandbox allows.

| Approval policy | Meaning | Agency score |
|---|---|---|
| `untrusted` | Ask before most actions | 1 |
| `on-request` | The agent asks when it needs more than the sandbox allows | 2 to 3 |
| `never` | Never ask; works with every sandbox mode; the CI shape is read-only sandbox plus never | 4 |

`--full-auto` is workspace-write sandbox plus on-request approval.
`--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`) removes
both and is not recommended. The `/permissions` command changes the
policy inside a session.

## Multi-agent features

- Codex cloud: hand a task off from the terminal; each task gets its own
  workspace and keeps working while the computer sleeps; the result is
  reviewed and committed or opened as a pull request. Supports agency 4
  and orchestration 2.
- `codex exec` for scripted runs; subagents for focused work; lifecycle
  hooks.
- Symphony, the vendor's orchestrator preview, polls a project board and
  runs one isolated Codex run per item.

## Setting up each next step

| Step | In Codex |
|---|---|
| Name the check | A line in `AGENTS.md` with the test command |
| Enforce a rule | Hooks; sandbox mode `read-only` or `workspace-write`; managed `requirements.toml` |
| Turn prompts off | `approval_policy = "on-request"` with a sandbox, then `never` inside a container |
| Unattended bounded runs | `codex exec` or a cloud task |
| A work queue with isolated runs | Symphony with a project board |
