# Cursor

Where Cursor keeps configuration, what its approval modes mean for the
scores, and how each next step is set up. Read this when a `~/.cursor`
directory or a `.cursor/` project directory is present. Facts are from
the vendor documentation and a documentation mirror as of mid-2026
(Cursor 3 and 3.6 cited).

## Where things live

| Item | Path |
|---|---|
| CLI configuration | `~/.cursor/cli-config.json`: `approvalMode`, `permissions.allow` and `deny`, `sandbox.mode` |
| User rules | `~/.cursor/rules/*.mdc` |
| Project rules | `.cursor/rules/`, the older `.cursorrules`; `AGENTS.md` is also read |
| Hooks | `.cursor/hooks.json` (for example `beforeShellExecution`) |
| Cloud agent environment | `.cursor/environment.json`, optionally a Dockerfile |
| Project records | `~/.cursor/projects/` (not parsed by the scanner) |

## Approval modes and the agency score

In the editor (Cursor 3.6 and later) the run mode sits under Settings,
Agents, Approvals and Execution: Auto-review (the default), Allowlist,
and Run Everything; older builds call it Auto-Run. A `permissions.json`
allowlist of terminal commands applies only when auto-run is on. Modes
are Agent and Plan, switched with Shift+Tab.

| Setting | Agency score |
|---|---|
| Auto-review | 1 |
| Allowlist | 2 |
| Run Everything | 3 |
| Cloud agents used for bounded tasks and left alone | 4 |

## Multi-agent features

- Cloud agents (formerly Background Agents) run in isolated virtual
  machines, "as many agents as you want in parallel", started from the
  editor's Cloud option, the web, chat mentions, tickets, or an API; they
  push a branch and return a merge-ready pull request. A spend limit is
  asked for on first use. Supports orchestration 2.
- The Agents Window runs parallel agents in isolated checkouts.

## Setting up each next step

| Step | In Cursor |
|---|---|
| Encode a preference | A rule in `.cursor/rules/` or `AGENTS.md` |
| Enforce a rule | A hook in `.cursor/hooks.json`; the `permissions.deny` list |
| Turn prompts off | Allowlist, then Run Everything |
| Unattended bounded runs | A cloud agent with `.cursor/environment.json` |
| One checkout per agent | Cloud agents, or the Agents Window with worktrees |
