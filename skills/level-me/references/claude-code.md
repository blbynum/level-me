# Claude Code

Where Claude Code keeps configuration and transcripts, what its
permission modes and multi-agent features mean for the scores, how to
inspect them by hand, and how each next step is set up here. Read this
when Claude Code is present. Facts are from the vendor documentation as
of November 2026 (versions 2.1.283 to 2.1.314 cited there).

## Contents

- Where things live
- Permission modes and the agency score
- Hooks and the feedback score
- Multi-agent features and the orchestration score
- Transcript fields the scanner reads
- Manual inspection without the scanner
- Setting up each next step

## Where things live

| Item | Path |
|---|---|
| User settings | `~/.claude/settings.json`; local overrides in `~/.claude/settings.local.json` |
| Project settings | `.claude/settings.json`; local overrides in `.claude/settings.local.json` |
| Instruction files | `~/.claude/CLAUDE.md` (user); `CLAUDE.md` or `.claude/CLAUDE.md` (project); `~/.claude/rules/*.md` and `.claude/rules/*.md` |
| Skills | `~/.claude/skills/<name>/SKILL.md`; `.claude/skills/<name>/SKILL.md` |
| Subagent definitions | `~/.claude/agents/*.md`; `.claude/agents/*.md` |
| MCP servers | `~/.claude.json` (`mcpServers`); `.mcp.json` in the project |
| Plugins | `~/.claude/plugins/installed_plugins.json` |
| Worktrees | `.claude/worktrees/<name>/` on branch `worktree-<name>` |
| Agent teams state | `~/.claude/teams/<team>/` (config and inboxes, removed at session end); `~/.claude/tasks/<team>/` (kept) |
| Workflows | `.claude/workflows/`, `~/.claude/workflows/`; results under `~/.claude/projects/` |
| Transcripts | `~/.claude/projects/<cwd-slug>/<session>.jsonl`; subagent transcripts in `<session>/subagents/agent-*.jsonl` |
| Prompt history | `~/.claude/history.jsonl` |

## Permission modes and the agency score

Six modes, set per session with `--permission-mode`, as the start mode
with `permissions.defaultMode` in a settings file, or interactively.

| Mode | Behavior | Agency score it supports |
|---|---|---|
| `default` (labeled Manual) | Prompts on first use of each tool | 1 |
| `plan` | Read-only planning; no edits or commands | 1 (a planning habit also supports Shapiro 4) |
| `acceptEdits` | File edits auto-approved; commands still ask | 2 |
| `auto` | A background classifier approves routine actions; the start mode for interactive sessions since v2.1.283 | 3 |
| `dontAsk` | Denies anything that would need a prompt | 4 in unattended runs; in scripted eval runs it is tooling, not practice |
| `bypassPermissions` (`--dangerously-skip-permissions`) | No prompts; the vendor says to use it only in containers or VMs | 4 |

Headless runs, `claude -p`, start in Manual since v2.1.302 unless a
mode is passed; a headless entry point in transcripts therefore shows
unattended use only when its mode was raised. Instruction files do not
change what is allowed; `permissions.allow`, `deny`, and `ask` rules do.
Policy keys `permissions.disableBypassPermissionsMode` and
`permissions.disableAutoMode` can forbid the high modes.

## Hooks and the feedback score

Hooks live under `hooks` in any settings file, in plugin hook files, and
in skill or subagent frontmatter. Events include `PreToolUse`,
`PostToolUse`, `Stop`, `SubagentStop`, `WorktreeCreate`, `WorktreeRemove`,
`TeammateIdle`, `TaskCreated`, `TaskCompleted`. A `Stop` hook that exits
with code 2 keeps the session working, which is the mechanism for "the
check must pass before done".

| Hook shape | Feedback score it supports |
|---|---|
| `PostToolUse` on `Edit\|Write` running lint or format | 2 |
| `Stop` running the test command and exiting 2 on failure | 4 |
| `PreToolUse` deny on dangerous commands, with `permissions.deny` | Enforcement that makes agency 3 safe |

The sandbox is a separate OS-level layer for filesystem and network
limits.

## Multi-agent features and the orchestration score

| Feature | How it shows | Score it supports |
|---|---|---|
| Subagents (`Agent` tool, `.claude/agents`) | `subagents/` transcripts under a session | 1 |
| Worktrees (`claude --worktree <name>`, `isolation: worktree` in a subagent, `/batch`) | Session `cwd` under `.claude/worktrees/`; the desktop app also makes one per session on its own | 2 with parallel human activity |
| Agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `env`) | `~/.claude/teams/`; teammate tool calls | 3 |
| Workflow tool (`ultracode`, saved workflows) | `Workflow` tool calls; `.claude/workflows/` | 3 |
| Cross-session messaging and the desktop's linked sessions | `turnOrigin: peer` records | 1 to 2 |

Agent teams cost "significantly more tokens", scale linearly, and the
vendor suggests three to five teammates. Workflows default to 16
concurrent agents and warn above 25 agents or 1.5 million projected
tokens.

## Transcript fields the scanner reads

Each line of a session file is a JSON record. The scanner uses:

- `type`: `user`, `assistant`, and bookkeeping types. A `user` record is
  a human turn only when it carries text content, has no
  `toolUseResult`, is not `isMeta`, and has `turnOrigin` absent or
  `human`. Other `user` records are tool results, injected notices, or
  turns from another session.
- `permissionMode` on user records: the mode in force for that turn.
- `entrypoint`: `claude-desktop`, `cli`, or an SDK marker.
- `isSidechain`: true in subagent transcripts.
- `cwd`: a temporary directory marks a scripted session.
- `message.content` tool_use blocks on assistant records: tool names and,
  for `Bash`, the command text, which the scanner matches for test
  runners, linters, commits, pushes, and pull requests.
- A user turn beginning `[Request interrupted by user` is an interrupt.

## Manual inspection without the scanner

1. Read the four settings files for `permissions.defaultMode`, the
   `allow`, `deny`, and `ask` lists, `hooks`, and `env`.
2. List the instruction files and count their lines; look for a test or
   check command in them.
3. List `~/.claude/projects/*/` by modification time; count files in the
   window; open the newest ten and read the user turns.
4. Count the sessions whose first user record has `permissionMode`
   `auto`, `bypassPermissions`, or `dontAsk`.
5. Look for `subagents/` directories, `.claude/worktrees/`,
   `~/.claude/teams/`, and `.claude/workflows/`.

## Setting up each next step

| Step | In Claude Code |
|---|---|
| Name the check | A line in `CLAUDE.md`: the command that runs the project's tests |
| Encode a preference | A rule file in `.claude/rules/` or a line in `CLAUDE.md`; a skill for a workflow |
| Enforce a zero-exception rule | `permissions.deny` for a tool or command pattern; a `PreToolUse` hook; the sandbox |
| Lint on every edit | A `PostToolUse` hook with matcher `Edit\|Write` |
| Block "done" until the check passes | A `Stop` hook that runs the tests and exits 2 on failure; or a goal condition set for the session |
| Independent review | A code-review subagent or command that never saw the conversation |
| Turn prompts off | `permissions.defaultMode: auto` after the above; `bypassPermissions` only inside a container |
| Unattended bounded runs | `claude -p "<task>" --permission-mode <mode>` with allow rules, or a cloud session; branch protection on the hosting service |
| One checkout per agent | `claude --worktree <name>`; `isolation: worktree` on subagents; `/batch` for many units |
| A shared task list | Agent teams for a burst; a tracker or ledger for ongoing work |
| Fan out dozens of agents | The Workflow tool, with its concurrency cap and cost warning |
| Loop until done | The Ralph-style plugin with an iteration cap and a completion promise |
