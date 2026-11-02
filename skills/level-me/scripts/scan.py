#!/usr/bin/env python3
"""Collect observable signals of AI coding tool usage from local harness
configuration and session transcripts, and print them as JSON.

Execute this script; do not read it as reference.

The output holds counts, file names, and setting values. It never holds
transcript content, prompts, or code. Pass --json to also write the report
to a file.

Usage:
    python3 scan.py [--home DIR] [--project DIR] [--days N]
                    [--max-sessions N] [--json PATH] [--quiet]

Runs on Python 3.8 or later with the standard library only.
"""
import argparse
import glob
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone

# A transcript window of 30 days covers a typical month of work and keeps
# the scan under a minute on a machine with a few thousand sessions.
DEFAULT_DAYS = 30
# Parsing stops once this many interactive sessions have been read, or at
# the newest DEFAULT_MAX_SESSIONS files, whichever comes first. Eighty
# interactive sessions give stable counts; scripted sessions are small
# and cheap to skip past.
DEFAULT_MIN_INTERACTIVE = 80
DEFAULT_MAX_SESSIONS = 2000
# Two sessions count as parallel when both receive a human turn inside the
# same bin. Ten minutes is long enough to catch a person who alternates
# between sessions and short enough that an idle session does not count.
ACTIVITY_BIN_SECONDS = 600

# A session whose working directory sits under a temporary directory was
# started by a script (an eval runner, a batch job), not by a person at a
# keyboard. Such sessions are counted but kept out of the practice scores.
SCRIPTED_CWD_PREFIXES = ("/tmp/", "/private/tmp/", "/var/folders/", "/private/var/folders/")
INTERRUPT_MARK = "[Request interrupted by user"
# An eval runner sends the same first prompt to many sessions. A first
# prompt shared by this many sessions marks all of them as scripted; a
# person rarely types the same opening three times in a month.
REPEATED_FIRST_PROMPT_MIN = 3

TEST_TOKENS = re.compile(
    r"\b(pytest|npm test|pnpm test|yarn test|bun test|go test|cargo test|"
    r"jest|vitest|mocha|rspec|phpunit|mvn test|gradle test|make test|"
    r"dotnet test|swift test|ctest|tox|nox)\b")
GIT_COMMIT = re.compile(r"\bgit commit\b")
GIT_PUSH = re.compile(r"\bgit push\b")
PR_CREATE = re.compile(r"\bgh pr (create|merge)\b")
LINT_TOKENS = re.compile(
    r"\b(eslint|ruff|flake8|pylint|mypy|pyright|tsc|golangci-lint|"
    r"clippy|rubocop|prettier|black)\b")


def expand(p):
    return os.path.expanduser(os.path.expandvars(p))


def read_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        return {"_error": "%s: %s" % (type(exc).__name__, exc)}


def count_lines(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return None


def exists(path):
    return os.path.exists(path)


def list_dir(path, pattern="*"):
    if not os.path.isdir(path):
        return []
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(path, pattern)))


def instruction_file_report(path):
    if not exists(path):
        return None
    lines = count_lines(path)
    test_hint = None
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if TEST_TOKENS.search(line) or ("test" in line.lower() and "`" in line):
                    test_hint = line.strip()[:120]
                    break
    except OSError:
        pass
    return {"path": path, "lines": lines, "test_command_hint": test_hint}


# --- Claude Code -----------------------------------------------------------

def claude_settings_summary(path):
    d = read_json(path)
    if d is None:
        return None
    if "_error" in d:
        return {"path": path, "error": d["_error"]}
    perms = d.get("permissions") or {}
    hooks = d.get("hooks") or {}
    env = d.get("env") or {}
    return {
        "path": path,
        "defaultMode": perms.get("defaultMode"),
        "allow_rules": len(perms.get("allow") or []),
        "deny_rules": len(perms.get("deny") or []),
        "ask_rules": len(perms.get("ask") or []),
        "disableBypassPermissionsMode": perms.get("disableBypassPermissionsMode"),
        "disableAutoMode": perms.get("disableAutoMode"),
        "hook_events": sorted(hooks.keys()) if isinstance(hooks, dict) else [],
        "hook_count": sum(len(v) if isinstance(v, list) else 1 for v in hooks.values()) if isinstance(hooks, dict) else 0,
        "agent_teams_env": env.get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"),
        "disableWorkflows": d.get("disableWorkflows"),
        "enabledPlugins": len(d.get("enabledPlugins") or {}),
        "model": d.get("model"),
    }


def scan_claude_code(home, project):
    root = os.path.join(home, ".claude")
    if not os.path.isdir(root):
        return {"present": False}
    out = {"present": True, "root": root}
    out["user_settings"] = claude_settings_summary(os.path.join(root, "settings.json"))
    out["user_settings_local"] = claude_settings_summary(os.path.join(root, "settings.local.json"))
    out["project_settings"] = claude_settings_summary(os.path.join(project, ".claude", "settings.json"))
    out["project_settings_local"] = claude_settings_summary(os.path.join(project, ".claude", "settings.local.json"))
    out["user_claude_md"] = instruction_file_report(os.path.join(root, "CLAUDE.md"))
    out["project_claude_md"] = instruction_file_report(os.path.join(project, "CLAUDE.md")) or \
        instruction_file_report(os.path.join(project, ".claude", "CLAUDE.md"))
    out["user_rules"] = list_dir(os.path.join(root, "rules"), "*.md")
    out["project_rules"] = list_dir(os.path.join(project, ".claude", "rules"), "*.md")
    out["user_skills"] = len(list_dir(os.path.join(root, "skills")))
    out["project_skills"] = len(list_dir(os.path.join(project, ".claude", "skills")))
    out["user_agents"] = len(list_dir(os.path.join(root, "agents"), "*.md"))
    out["project_agents"] = len(list_dir(os.path.join(project, ".claude", "agents"), "*.md"))
    out["user_workflows"] = len(list_dir(os.path.join(root, "workflows")))
    out["project_workflows"] = len(list_dir(os.path.join(project, ".claude", "workflows")))
    out["project_worktrees"] = len(list_dir(os.path.join(project, ".claude", "worktrees")))
    out["teams_dir"] = exists(os.path.join(root, "teams"))
    out["tasks_dir"] = exists(os.path.join(root, "tasks"))
    cj = read_json(os.path.join(home, ".claude.json"))
    out["user_mcp_servers"] = len((cj or {}).get("mcpServers") or {}) if isinstance(cj, dict) else 0
    pm = read_json(os.path.join(project, ".mcp.json"))
    out["project_mcp_servers"] = len((pm or {}).get("mcpServers") or {}) if isinstance(pm, dict) else 0
    plugins = read_json(os.path.join(root, "plugins", "installed_plugins.json"))
    out["installed_plugins"] = len(plugins.get("plugins") or plugins) if isinstance(plugins, dict) else 0
    return out


def iter_records(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except OSError:
        return


def parse_ts(s):
    if not isinstance(s, str):
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def human_text(rec):
    m = rec.get("message")
    content = m.get("content") if isinstance(m, dict) else None
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                return str(c.get("text") or "")
    return ""


def is_human_turn(rec):
    """A user record typed by a person: not a tool result, not an injected
    meta record, and not a turn another agent or a notification started."""
    if "toolUseResult" in rec or rec.get("isMeta") or rec.get("isCompactSummary"):
        return False
    if "turnOrigin" in rec and rec.get("turnOrigin") != "human":
        return False
    m = rec.get("message")
    content = m.get("content") if isinstance(m, dict) else None
    if isinstance(content, str):
        return bool(content.strip())
    if isinstance(content, list):
        return any(isinstance(c, dict) and c.get("type") == "text" for c in content)
    return False


def scan_claude_transcripts(home, days, max_sessions, min_interactive=DEFAULT_MIN_INTERACTIVE):
    base = os.path.join(home, ".claude", "projects")
    if not os.path.isdir(base):
        return {"present": False}
    cutoff = time.time() - days * 86400
    files = [p for p in glob.glob(os.path.join(base, "*", "*.jsonl")) if os.path.getmtime(p) > cutoff]
    files.sort(key=os.path.getmtime, reverse=True)
    total = len(files)
    files = files[:max_sessions]
    out = {"present": True, "window_days": days, "sessions_in_window": total}
    modes = Counter()
    entrypoints = Counter()
    tools = Counter()
    session_rows = []
    sessions_with_subagents = 0
    subagent_files = 0
    sessions_with_skill = 0
    sessions_with_agent_tool = 0
    sessions_with_workflow = 0
    sessions_with_teams = 0
    sessions_in_worktree = 0
    plan_sessions = 0
    test_runs = 0
    lint_runs = 0
    commits = 0
    pushes = 0
    prs = 0
    user_turns = []
    sessions_with_test_runs = 0
    interactive_sessions = 0
    newest_interactive = []
    scripted_sessions = 0
    scripted_tools = Counter()
    interrupts = 0
    # bin start -> set of session file names with a human turn in that bin
    active_bins = defaultdict(set)
    parsed = 0
    pending = []  # per-session records, classified after the loop
    first_prompt_count = Counter()
    for path in files:
        if interactive_sessions >= min_interactive:
            break
        parsed += 1
        first = None
        last = None
        sess_modes = Counter()
        sess_tools = Counter()
        sess_user = 0
        sess_tests = 0
        sess_interrupts = 0
        sess_scripted = False
        sess_first_prompt = None
        sess_bins = set()
        cwd_worktree = False
        for rec in iter_records(path):
            t = rec.get("type")
            ts = parse_ts(rec.get("timestamp"))
            if ts is not None:
                first = ts if first is None or ts < first else first
                last = ts if last is None or ts > last else last
            if t == "user":
                if rec.get("isSidechain"):
                    continue
                cwd = rec.get("cwd") or ""
                if "/.claude/worktrees/" in cwd:
                    cwd_worktree = True
                if cwd.startswith(SCRIPTED_CWD_PREFIXES):
                    sess_scripted = True
                if not is_human_turn(rec):
                    continue
                pm = rec.get("permissionMode")
                if pm:
                    sess_modes[pm] += 1
                ep = rec.get("entrypoint")
                if ep:
                    entrypoints[ep] += 1
                sess_user += 1
                text = human_text(rec)
                if sess_first_prompt is None:
                    sess_first_prompt = text.strip()[:200]
                if text.startswith(INTERRUPT_MARK):
                    sess_interrupts += 1
                if ts is not None:
                    sess_bins.add(int(ts // ACTIVITY_BIN_SECONDS))
            elif t == "assistant":
                m = rec.get("message")
                content = m.get("content") if isinstance(m, dict) else None
                if not isinstance(content, list):
                    continue
                for c in content:
                    if not isinstance(c, dict) or c.get("type") != "tool_use":
                        continue
                    name = c.get("name") or "?"
                    sess_tools[name] += 1
                    inp = c.get("input") or {}
                    if name == "Bash" and isinstance(inp, dict):
                        cmd = str(inp.get("command") or "")
                        if TEST_TOKENS.search(cmd):
                            sess_tests += 1
                        if LINT_TOKENS.search(cmd):
                            lint_runs += 1
                        if GIT_COMMIT.search(cmd):
                            commits += 1
                        if GIT_PUSH.search(cmd):
                            pushes += 1
                        if PR_CREATE.search(cmd):
                            prs += 1
        if sess_first_prompt:
            first_prompt_count[sess_first_prompt] += 1
        # No human turn at all (every turn came from a runner or another
        # agent), a temp-dir working directory, or a one-turn dontAsk run:
        # scripted.
        if sess_scripted or sess_user == 0 or (sess_user <= 1 and "dontAsk" in sess_modes):
            scripted_sessions += 1
            scripted_tools.update(sess_tools)
            continue
        # Counted as interactive for the stop condition; a repeated first
        # prompt can still move it to scripted below.
        interactive_sessions += 1
        pending.append(dict(path=path, modes=sess_modes, tools=sess_tools, user=sess_user,
                            tests=sess_tests, interrupts=sess_interrupts, worktree=cwd_worktree,
                            first_prompt=sess_first_prompt, bins=sess_bins, first=first, last=last))

    interactive_sessions = 0
    for rec in pending:
        fp = rec["first_prompt"]
        if fp and first_prompt_count[fp] >= REPEATED_FIRST_PROMPT_MIN:
            scripted_sessions += 1
            scripted_tools.update(rec["tools"])
            continue
        interactive_sessions += 1
        path = rec["path"]
        sess_modes, sess_tools = rec["modes"], rec["tools"]
        newest_interactive.append(path)
        interrupts += rec["interrupts"]
        modes.update(sess_modes)
        tools.update(sess_tools)
        user_turns.append(rec["user"])
        test_runs += rec["tests"]
        for b in rec["bins"]:
            active_bins[b].add(path)
        if rec["tests"]:
            sessions_with_test_runs += 1
        if sess_modes.get("plan"):
            plan_sessions += 1
        if rec["worktree"]:
            sessions_in_worktree += 1
        sub = glob.glob(os.path.join(path[:-6], "subagents", "*.jsonl"))
        if sub:
            sessions_with_subagents += 1
            subagent_files += len(sub)
        if sess_tools.get("Skill"):
            sessions_with_skill += 1
        if sess_tools.get("Agent") or sess_tools.get("Task"):
            sessions_with_agent_tool += 1
        if sess_tools.get("Workflow"):
            sessions_with_workflow += 1
        if any(k.startswith("Teammate") for k in sess_tools):
            sessions_with_teams += 1
        if rec["first"] is not None and rec["last"] is not None:
            session_rows.append((rec["first"], rec["last"], os.path.basename(path)))

    # Concurrency: the most sessions that received a human turn inside one
    # activity bin, and the number of days on which two or more did.
    max_concurrent = 0
    days_with_parallel = set()
    for b, names in active_bins.items():
        n = len(names)
        if n > max_concurrent:
            max_concurrent = n
        if n > 1:
            days_with_parallel.add(datetime.fromtimestamp(b * ACTIVITY_BIN_SECONDS, timezone.utc).date().isoformat())
    if session_rows:
        pass

    user_turns.sort()
    median_turns = user_turns[len(user_turns) // 2] if user_turns else 0
    out.update({
        "sessions_parsed": parsed,
        "interactive_sessions": interactive_sessions,
        "scripted_sessions": scripted_sessions,
        "scripted_session_tool_calls": sum(scripted_tools.values()),
        "interrupts_by_user": interrupts,
        "permission_modes_by_user_turn": dict(modes.most_common()),
        "entrypoints": dict(entrypoints.most_common()),
        "tool_calls": dict(tools.most_common(30)),
        "sessions_with_subagents": sessions_with_subagents,
        "subagent_transcripts": subagent_files,
        "sessions_with_skill_calls": sessions_with_skill,
        "sessions_with_agent_tool": sessions_with_agent_tool,
        "sessions_with_workflow_tool": sessions_with_workflow,
        "sessions_with_team_tools": sessions_with_teams,
        "sessions_in_worktree": sessions_in_worktree,
        "sessions_with_plan_mode": plan_sessions,
        "sessions_with_test_runs": sessions_with_test_runs,
        "test_runs": test_runs,
        "lint_runs": lint_runs,
        "git_commits": commits,
        "git_pushes": pushes,
        "pr_create_or_merge": prs,
        "median_user_turns_per_session": median_turns,
        "max_concurrent_sessions": max_concurrent,
        "days_with_parallel_sessions": len(days_with_parallel),
        "newest_sessions": [os.path.relpath(p, base) for p in newest_interactive[:8]],
        "note": "scores use interactive sessions only; scripted sessions (temp-dir working directory, one turn in dontAsk mode, or a first prompt repeated in %d or more sessions) are counted apart" % REPEATED_FIRST_PROMPT_MIN,
    })
    return out


# --- Other harnesses -------------------------------------------------------

def toml_top_level(path):
    """Read top-level key = value lines before the first [table]."""
    vals = {}
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                s = line.strip()
                if s.startswith("["):
                    break
                m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$', s)
                if m:
                    vals[m.group(1)] = m.group(2).strip().strip('"')
    except OSError:
        return None
    return vals


def scan_codex(home, project, days):
    root = os.path.join(home, ".codex")
    if not os.path.isdir(root):
        return {"present": False}
    cfg = toml_top_level(os.path.join(root, "config.toml")) or {}
    cutoff = time.time() - days * 86400
    sessions = [p for p in glob.glob(os.path.join(root, "sessions", "*", "*", "*", "*.jsonl"))
                if os.path.getmtime(p) > cutoff]
    return {
        "present": True,
        "approval_policy": cfg.get("approval_policy"),
        "sandbox_mode": cfg.get("sandbox_mode"),
        "model": cfg.get("model"),
        "user_agents_md": instruction_file_report(os.path.join(root, "AGENTS.md")),
        "project_agents_md": instruction_file_report(os.path.join(project, "AGENTS.md")),
        "sessions_in_window": len(sessions),
        "hooks_dir": exists(os.path.join(root, "hooks")),
    }


def scan_cursor(home, project):
    root = os.path.join(home, ".cursor")
    if not os.path.isdir(root):
        return {"present": False}
    cfg = read_json(os.path.join(root, "cli-config.json")) or {}
    perms = cfg.get("permissions") or {} if isinstance(cfg, dict) else {}
    sandbox = cfg.get("sandbox") or {} if isinstance(cfg, dict) else {}
    return {
        "present": True,
        "cli_approval_mode": cfg.get("approvalMode") if isinstance(cfg, dict) else None,
        "cli_allow_rules": len(perms.get("allow") or []),
        "cli_deny_rules": len(perms.get("deny") or []),
        "cli_sandbox_mode": sandbox.get("mode"),
        "user_rules": list_dir(os.path.join(root, "rules")),
        "project_rules": list_dir(os.path.join(project, ".cursor", "rules")),
        "project_cursorrules": exists(os.path.join(project, ".cursorrules")),
        "project_hooks_json": exists(os.path.join(project, ".cursor", "hooks.json")),
        "project_environment_json": exists(os.path.join(project, ".cursor", "environment.json")),
        "projects_known": len(list_dir(os.path.join(root, "projects"))),
    }


def scan_gemini(home, project):
    root = os.path.join(home, ".gemini")
    if not os.path.isdir(root):
        return {"present": False}
    settings = read_json(os.path.join(root, "settings.json"))
    return {
        "present": True,
        "settings_keys": sorted(settings.keys()) if isinstance(settings, dict) else [],
        "user_gemini_md": instruction_file_report(os.path.join(root, "GEMINI.md")),
        "project_gemini_md": instruction_file_report(os.path.join(project, "GEMINI.md")),
        "tmp_entries": len(list_dir(os.path.join(root, "tmp"))),
    }


def vscode_settings_path(home):
    if sys.platform == "darwin":
        return os.path.join(home, "Library", "Application Support", "Code", "User", "settings.json")
    if os.name == "nt":
        return os.path.join(os.environ.get("APPDATA", ""), "Code", "User", "settings.json")
    return os.path.join(home, ".config", "Code", "User", "settings.json")


def scan_copilot(home, project):
    vs = read_json(vscode_settings_path(home))
    chat_keys = {}
    if isinstance(vs, dict):
        for k, v in vs.items():
            if k.startswith("chat.tools") or k.startswith("chat.permissions") or k.startswith("github.copilot"):
                chat_keys[k] = v if isinstance(v, (bool, int, str)) else type(v).__name__
    gh = os.path.join(project, ".github")
    return {
        "present": bool(chat_keys) or exists(os.path.join(gh, "copilot-instructions.md")) or os.path.isdir(os.path.join(home, ".copilot")),
        "vscode_chat_settings": chat_keys,
        "project_copilot_instructions": instruction_file_report(os.path.join(gh, "copilot-instructions.md")),
        "project_instruction_files": len(list_dir(os.path.join(gh, "instructions"), "*.instructions.md")),
        "project_agents_dir": len(list_dir(os.path.join(gh, "agents"))),
        "copilot_home": os.path.isdir(os.path.join(home, ".copilot")),
    }


# --- Project and orchestration markers --------------------------------------

def scan_project(home, project):
    out = {"path": project, "is_git": exists(os.path.join(project, ".git"))}
    out["agents_md"] = instruction_file_report(os.path.join(project, "AGENTS.md"))
    out["ci_workflows"] = len(list_dir(os.path.join(project, ".github", "workflows"), "*.y*ml"))
    out["gitlab_ci"] = exists(os.path.join(project, ".gitlab-ci.yml"))
    test_cfg = []
    for name in ("pytest.ini", "tox.ini", "noxfile.py", "jest.config.js", "jest.config.ts",
                 "vitest.config.ts", "vitest.config.js", "Makefile", "Cargo.toml", "go.mod"):
        if exists(os.path.join(project, name)):
            test_cfg.append(name)
    pkg = read_json(os.path.join(project, "package.json"))
    if isinstance(pkg, dict) and isinstance(pkg.get("scripts"), dict) and "test" in pkg["scripts"]:
        test_cfg.append("package.json:scripts.test")
    pyproject = os.path.join(project, "pyproject.toml")
    if exists(pyproject):
        try:
            with open(pyproject, encoding="utf-8", errors="replace") as fh:
                if "[tool.pytest" in fh.read():
                    test_cfg.append("pyproject.toml:[tool.pytest]")
        except OSError:
            pass
    out["test_config"] = test_cfg
    markers = []
    checks = [
        ("beads", os.path.join(project, ".beads")),
        ("beads-home", os.path.join(home, ".beads")),
        ("gastown-default-root", os.path.join(home, "gt")),
        ("gascity", os.path.join(project, "city.toml")),
        ("overstory", os.path.join(project, ".overstory")),
        ("symphony", os.path.join(project, "WORKFLOW.md")),
        ("ralph", os.path.join(project, "fix_plan.md")),
        ("ralph-prompt", os.path.join(project, "PROMPT.md")),
        ("hive", os.path.join(project, "hive.yaml")),
        ("claude-workflows", os.path.join(project, ".claude", "workflows")),
        ("claude-worktrees", os.path.join(project, ".claude", "worktrees")),
        ("ccmanager", os.path.join(home, ".config", "ccmanager")),
        ("claude-squad", os.path.join(home, ".claude-squad")),
        ("openhands", os.path.join(home, ".openhands")),
    ]
    for name, p in checks:
        if exists(p):
            markers.append(name)
    out["orchestration_markers"] = markers
    return out


# --- Derived, provisional placement ------------------------------------------

def derive(report):
    cc = report["harnesses"].get("claude_code") or {}
    tr = report["transcripts"].get("claude_code") or {}
    cx = report["harnesses"].get("codex") or {}
    cu = report["harnesses"].get("cursor") or {}
    proj = report["project"]
    reasons = defaultdict(list)

    # Agency: 0 none .. 5 unattended runs with self-checks.
    agency = 0
    modes = tr.get("permission_modes_by_user_turn") or {}
    total_turns = sum(modes.values()) or 0
    if total_turns:
        agency = 1
        reasons["agency"].append("%d human turns across %d interactive sessions (%d scripted sessions set aside)" % (
            total_turns, tr.get("interactive_sessions") or 0, tr.get("scripted_sessions") or 0))
    dominant = max(modes, key=modes.get) if modes else None
    if dominant:
        reasons["agency"].append("dominant permission mode: %s (%d of %d turns)" % (dominant, modes[dominant], total_turns))
    if dominant in ("acceptEdits",):
        agency = max(agency, 2)
    if dominant in ("auto",):
        agency = max(agency, 3)
    if dominant in ("bypassPermissions", "dontAsk"):
        agency = max(agency, 4)
    for s in (cc.get("user_settings"), cc.get("project_settings"), cc.get("user_settings_local"), cc.get("project_settings_local")):
        if s and s.get("defaultMode") in ("bypassPermissions", "dontAsk"):
            agency = max(agency, 4)
            reasons["agency"].append("settings defaultMode %s in %s" % (s["defaultMode"], s["path"]))
    if cx.get("present"):
        ap = (cx.get("approval_policy") or "").lower()
        if ap in ("never",):
            agency = max(agency, 4)
        elif ap in ("on-request", "on_request"):
            agency = max(agency, 3)
        elif ap:
            agency = max(agency, 1)
        if ap:
            reasons["agency"].append("Codex approval_policy=%s" % ap)
    if cu.get("present"):
        am = (cu.get("cli_approval_mode") or "").lower()
        if am in ("run-everything", "run_everything", "all", "yolo"):
            agency = max(agency, 3)
        elif am == "allowlist":
            agency = max(agency, 2)
        elif am:
            agency = max(agency, 1)
        if am:
            reasons["agency"].append("Cursor CLI approvalMode=%s" % am)
    headless = sum(v for k, v in (tr.get("entrypoints") or {}).items() if k in ("sdk-cli", "sdk", "cli-print", "headless"))
    if headless:
        agency = max(agency, 4)
        reasons["agency"].append("%d headless user turns" % headless)

    # Orchestration: 0 one session .. 5 external orchestrator.
    orch = 0
    mc = tr.get("max_concurrent_sessions") or 0
    if mc >= 2:
        orch = 1
        reasons["orchestration"].append("up to %d sessions received human turns in the same ten minutes, on %d days" % (mc, tr.get("days_with_parallel_sessions") or 0))
    if tr.get("interrupts_by_user"):
        reasons["agency"].append("%d user interrupts (close steering)" % tr["interrupts_by_user"])
    if tr.get("sessions_with_subagents") or tr.get("sessions_with_agent_tool"):
        orch = max(orch, 1)
        reasons["orchestration"].append("%d sessions used subagents" % max(tr.get("sessions_with_subagents") or 0, tr.get("sessions_with_agent_tool") or 0))
    if mc >= 4:
        orch = max(orch, 2)
    if tr.get("sessions_in_worktree") or (cc.get("project_worktrees") or 0) > 0:
        orch = max(orch, 1)
        reasons["orchestration"].append("worktree isolation in use")
    if tr.get("sessions_with_workflow_tool") or tr.get("sessions_with_team_tools") or cc.get("teams_dir"):
        orch = max(orch, 3)
        reasons["orchestration"].append("agent teams or workflow runs present")
    if mc >= 10:
        orch = max(orch, 4)
    external = [m for m in proj.get("orchestration_markers") or [] if m not in ("claude-worktrees",)]
    if external:
        orch = max(orch, 4 if len(external) == 1 else 5)
        reasons["orchestration"].append("orchestration markers: %s" % ", ".join(external))

    # Feedback infrastructure: 0 none .. 5 closed loop with gates.
    fb = 0
    has_instr = any([cc.get("user_claude_md"), cc.get("project_claude_md"), proj.get("agents_md"),
                     cx.get("user_agents_md"), cx.get("project_agents_md"), cc.get("user_rules"), cc.get("project_rules")])
    if has_instr:
        fb = 1
        reasons["feedback"].append("instruction files present")
    test_hint = any((x or {}).get("test_command_hint") for x in (cc.get("user_claude_md"), cc.get("project_claude_md"), proj.get("agents_md")))
    if test_hint or proj.get("test_config"):
        fb = max(fb, 2)
        reasons["feedback"].append("test command or test config present")
    hooks = set()
    for s in (cc.get("user_settings"), cc.get("project_settings"), cc.get("user_settings_local"), cc.get("project_settings_local")):
        if s:
            hooks.update(s.get("hook_events") or [])
    if hooks:
        fb = max(fb, 2)
        reasons["feedback"].append("hook events: %s" % ", ".join(sorted(hooks)))
    if proj.get("ci_workflows") or proj.get("gitlab_ci"):
        fb = max(fb, 3)
        reasons["feedback"].append("CI configuration present")
    if tr.get("sessions_with_test_runs"):
        reasons["feedback"].append("tests run in %d of %d interactive sessions" % (tr["sessions_with_test_runs"], tr.get("interactive_sessions") or 0))
        if fb < 2:
            fb = 2
    if "Stop" in hooks or "SubagentStop" in hooks:
        fb = max(fb, 3)
    if external:
        fb = max(fb, 4)

    # Provisional mapping. Levels that the script cannot separate are
    # given as a range; the skill reads transcripts to settle them.
    if total_turns == 0 and not cx.get("sessions_in_window") and not cu.get("projects_known"):
        yegge = "1"
        shapiro = "0"
    elif agency <= 1:
        yegge, shapiro = "2", "1-2"
    elif agency == 2:
        yegge, shapiro = "2-3", "2"
    elif agency == 3:
        yegge, shapiro = "3-4 (read transcripts: are diffs still reviewed?)", "2-3"
    else:
        yegge, shapiro = "4-5 (read transcripts: unattended runs, IDE abandoned?)", "3-4"
    # Orchestration sets the Yegge level; the Shapiro level follows the
    # human's role, so parallel agents under close review stay at 3.
    if orch >= 1 and agency >= 3:
        yegge = "6" if orch <= 2 else yegge
        shapiro = "4" if agency >= 4 else "3 (4 needs specs and unattended, outcome-judged runs)"
    if orch >= 3:
        yegge = "7" if orch < 5 else "8"
        if orch >= 5:
            shapiro = "4-5 (5 only when no human reads code)"
    needs_reading = [
        "whether diffs are read before acceptance (Yegge 3 vs 4; Shapiro 2 vs 3)",
        "whether work starts from a spec or plan (Shapiro 4)",
        "whether runs finish unattended with a self-check (Yegge 5; Osmani L3)",
        "whether corrections repeat across sessions (feedback L1 vs L2)",
    ]
    return {
        "agency_0_to_5": agency,
        "orchestration_0_to_5": orch,
        "feedback_0_to_5": fb,
        "yegge_provisional": yegge,
        "shapiro_provisional": shapiro,
        "reasons": dict(reasons),
        "needs_transcript_reading": needs_reading,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", default="~", help="home directory to scan (default: ~)")
    ap.add_argument("--project", default=".", help="project directory to scan (default: current directory)")
    ap.add_argument("--days", type=int, default=DEFAULT_DAYS, help="transcript window in days (default %d)" % DEFAULT_DAYS)
    ap.add_argument("--max-sessions", type=int, default=DEFAULT_MAX_SESSIONS, help="newest sessions to parse at most (default %d)" % DEFAULT_MAX_SESSIONS)
    ap.add_argument("--min-interactive", type=int, default=DEFAULT_MIN_INTERACTIVE, help="stop after this many interactive sessions (default %d)" % DEFAULT_MIN_INTERACTIVE)
    ap.add_argument("--json", help="also write the report to this path")
    ap.add_argument("--quiet", action="store_true", help="print only the derived summary")
    args = ap.parse_args()
    home = os.path.abspath(expand(args.home))
    project = os.path.abspath(expand(args.project))
    if not os.path.isdir(home):
        print("home directory not found: %s" % home, file=sys.stderr)
        return 2
    if not os.path.isdir(project):
        print("project directory not found: %s" % project, file=sys.stderr)
        return 2
    report = {
        "meta": {"scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "home": home, "project": project, "days": args.days,
                 "python": sys.version.split()[0]},
        "harnesses": {
            "claude_code": scan_claude_code(home, project),
            "codex": scan_codex(home, project, args.days),
            "cursor": scan_cursor(home, project),
            "gemini_cli": scan_gemini(home, project),
            "copilot": scan_copilot(home, project),
        },
        "transcripts": {"claude_code": scan_claude_transcripts(home, args.days, args.max_sessions, args.min_interactive)},
        "project": scan_project(home, project),
    }
    report["derived"] = derive(report)
    text = json.dumps(report["derived"] if args.quiet else report, indent=2, sort_keys=True)
    print(text)
    if args.json:
        try:
            with open(expand(args.json), "w", encoding="utf-8") as fh:
                json.dump(report, fh, indent=2, sort_keys=True)
        except OSError as exc:
            print("could not write %s: %s" % (args.json, exc), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
