#!/bin/sh
# link.sh: link the skills and rules of a git repository into the
# user-level directories of an AI coding harness. The script has nothing
# specific to one repository: copy it into any repository with the shape
# that --help describes. Run ./link.sh --help for usage.
#
# Source: https://github.com/blbynum/meta-skills/blob/master/link.sh
# Keep this header in each copy: the license requires the notice below.
#
# SPDX-License-Identifier: MIT
#
# MIT License
#
# Copyright (c) 2026 Ben Bynum
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
set -eu
unset CDPATH
: "${HOME:?HOME is not set}"

PROG=${0##*/}
# The version of this script.
LINK_SH_VERSION=1.0.0
HARNESS_IDS="claude-code codex cursor copilot gemini-cli antigravity"

# harness ID: set H_NAME and H_SKILLS, and H_RULES (empty when the harness
# has no user-level rules directory, with the reason in H_NORULES).
# Returns 1 for an unknown ID.
# Directories checked against vendor documentation on 2026-11-01:
#   claude-code  code.claude.com/docs/en/skills, /docs/en/memory
#   codex        learn.chatgpt.com/docs/build-skills,
#                learn.chatgpt.com/docs/agent-configuration/agents-md
#   cursor       cursor.com/docs/context/skills, /docs/context/rules
#   copilot      docs.github.com/en/copilot: concepts/agents/about-agent-skills,
#                how-tos/copilot-cli/customize-copilot/add-custom-instructions
#   gemini-cli   geminicli.com/docs/cli/skills, /docs/cli/gemini-md
#   antigravity  antigravity.google/docs/skills, /docs/rules
harness() {
  H_RULES= H_NORULES=
  case $1 in
    claude-code)
      H_NAME="Claude Code" H_SKILLS=$HOME/.claude/skills
      H_RULES=$HOME/.claude/rules ;;
    codex)
      H_NAME=Codex H_SKILLS=$HOME/.agents/skills
      H_NORULES="Codex reads one user rules file, ~/.codex/AGENTS.md, not a directory" ;;
    cursor)
      H_NAME=Cursor H_SKILLS=$HOME/.cursor/skills
      H_NORULES="Cursor keeps user rules in its settings, not in files" ;;
    copilot)
      H_NAME="GitHub Copilot" H_SKILLS=$HOME/.copilot/skills
      H_RULES=$HOME/.copilot/instructions ;;
    gemini-cli)
      H_NAME="Gemini CLI" H_SKILLS=$HOME/.gemini/skills
      H_NORULES="Gemini CLI reads one user rules file, ~/.gemini/GEMINI.md, not a directory" ;;
    antigravity)
      H_NAME=Antigravity H_SKILLS=$HOME/.gemini/config/skills
      H_RULES=$HOME/.gemini/config/rules ;;
    *) return 1 ;;
  esac
}

say() { printf '%s\n' "$*"; }
warn() { printf '%s: %s\n' "$PROG" "$*" >&2; }
die() { warn "error: $1"; exit 1; }
usage_error() {
  warn "error: $1"
  warn "Run '$PROG --help' for usage."
  exit 2
}

# Print a path with $HOME shown as ~.
tilde() {
  case $1 in
    "$HOME"/*) printf '~/%s\n' "${1#"$HOME"/}" ;;
    *) printf '%s\n' "$1" ;;
  esac
}

# Print a path that the user typed, with a leading ~ expanded.
expand_tilde() {
  case $1 in
    "~") printf '%s\n' "$HOME" ;;
    "~/"*) printf '%s/%s\n' "$HOME" "${1#"~/"}" ;;
    *) printf '%s\n' "$1" ;;
  esac
}

list_harnesses() {
  printf '  %-12s %-15s %-25s %s\n' ID HARNESS SKILLS RULES
  for id in $HARNESS_IDS; do
    harness "$id"
    if [ -n "$H_RULES" ]; then rules=$(tilde "$H_RULES"); else rules=none; fi
    printf '  %-12s %-15s %-25s %s\n' "$id" "$H_NAME" "$(tilde "$H_SKILLS")" "$rules"
  done
  printf '  %-12s %-15s %-25s %s\n' custom "(you choose)" "--skills-dir <dir>" "--rules-dir <dir>"
}

usage() {
  cat <<EOF
Usage:
  $PROG
  $PROG --harness <id>
  $PROG [--harness custom] [--skills-dir <dir>] [--rules-dir <dir>]
  $PROG --list
  $PROG --help
  $PROG --version

$PROG links the skills and rules of the git repository that contains it
into the user-level directories of an AI coding harness. Each link is a
symbolic link into the repository, so the harness reads the skills and
rules from the repository. $PROG is not tied to one repository: copy it
into the root of any git repository that has the shape shown under
"Repository shape".

With no arguments, $PROG shows a numbered list of harnesses and asks for
a number. Type 0 for a custom harness; $PROG then asks for the
directories. This mode needs a terminal. If standard input is not a
terminal, $PROG writes this help to standard error and exits with
status 2.

Options:
  --harness <id>      Link into the directories of the harness <id>.
  --skills-dir <dir>  Link the skills into <dir>. This option selects the
                      custom harness. Without it, a custom harness gets
                      no skills.
  --rules-dir <dir>   Link the rules into <dir>. This option selects the
                      custom harness. Without it, a custom harness gets
                      no rules.
  --list              Show the harness ids and directories, then exit.
  -h, --help          Show this help, then exit.
  --version           Show the version of $PROG, then exit.

  <id> is an id from the table below. <dir> is a directory path; $PROG
  makes the directory if it does not exist. The forms --harness=<id>,
  --skills-dir=<dir>, and --rules-dir=<dir> also work.

Harnesses and their user-level directories:
$(list_harnesses)

  codex, gemini-cli: the user rules are one file (~/.codex/AGENTS.md,
    ~/.gemini/GEMINI.md), not a directory. $PROG does not link rules.
  cursor: Cursor keeps user rules in its settings. $PROG does not link
    rules.
  copilot: the rules directory is for Copilot CLI, which reads only
    files whose names end in .instructions.md. $PROG gives each rule
    link that ending: rules/style.md becomes style.instructions.md.
  antigravity: Antigravity ignores a rule file that has no trigger: line
    (always_on, model_decision, glob, or manual) in its frontmatter.
    $PROG warns about each such file.

Repository shape:
  skills/<name>/    One skill, or a shared directory that skills read by
                    a relative path.
  rules/<name>.md   One rule file.

  $PROG links skills only if skills/ exists, and rules only if rules/
  exists. If neither exists, $PROG exits with status 1. Names that start
  with a dot are not linked. The repository is the top level of the git
  repository that contains $PROG; outside git, it is the directory of
  $PROG. You can copy $PROG into any git repository with this shape.

Each run:
  - makes a link for each skill and each rule that has no link;
  - replaces a link that points to a different location;
  - skips a name that exists as a real file or directory, with a message
    on standard error;
  - removes each link into the repository whose source no longer exists;
  - moves <name>/config.local.yaml to skills/<name>/ for a skill that
    moved from the top level of the repository into skills/;
  - writes no line for a link that is already correct.
  You can run $PROG again at any time.

Settings and updates:
  - The skills stay in the repository. The links point there.
  - Each skill reads its settings for this machine from config.local.yaml
    in its own directory: skills/<name>/config.local.yaml. Git ignores
    that file. To change a setting, edit that file. $PROG warns if git
    does not ignore it.
  - To get updates, run git pull in the repository, then run $PROG again.
    The new run links new skills and rules and removes the links to
    deleted ones.

Exit status:
  0  The links are correct. $PROG reports skipped names on standard error.
  1  $PROG cannot continue: there is nothing to link for the harness, or
     a directory or a link cannot be made.
  2  Usage error: an unknown option or harness id, an option without its
     value, or no arguments and no terminal.

Examples:
  Link the repository into Claude Code:
    ./$PROG --harness claude-code
  Link the repository into directories that you choose:
    ./$PROG --skills-dir ~/agent/skills --rules-dir ~/agent/rules
EOF
}

# ---- Arguments --------------------------------------------------------

OPT_HARNESS= OPT_SKILLS= OPT_RULES=
set_opt() {
  [ -n "$2" ] || usage_error "$1 needs a value"
  case $1 in
    --harness) OPT_HARNESS=$2 ;;
    --skills-dir) OPT_SKILLS=$2 ;;
    --rules-dir) OPT_RULES=$2 ;;
  esac
}

INTERACTIVE=0
[ $# -gt 0 ] || INTERACTIVE=1
while [ $# -gt 0 ]; do
  case $1 in
    -h|--help) usage; exit 0 ;;
    --version) say "$PROG $LINK_SH_VERSION"; exit 0 ;;
    --list) list_harnesses; exit 0 ;;
    --harness|--skills-dir|--rules-dir)
      [ $# -ge 2 ] || usage_error "$1 needs a value"
      set_opt "$1" "$2"; shift ;;
    --harness=*|--skills-dir=*|--rules-dir=*) set_opt "${1%%=*}" "${1#*=}" ;;
    -*) usage_error "unknown option: $1" ;;
    *) usage_error "unexpected argument: $1 (to link into a directory, use --skills-dir <dir>)" ;;
  esac
  shift
done

if [ "$INTERACTIVE" = 1 ] && [ ! -t 0 ]; then
  usage >&2
  exit 2
fi
if [ "$INTERACTIVE" = 0 ]; then
  if [ -n "$OPT_SKILLS$OPT_RULES" ]; then
    case $OPT_HARNESS in
      ''|custom) OPT_HARNESS=custom ;;
      *) usage_error "--skills-dir and --rules-dir select the custom harness; do not use them with --harness $OPT_HARNESS" ;;
    esac
  fi
  case $OPT_HARNESS in
    custom) [ -n "$OPT_SKILLS$OPT_RULES" ] ||
      usage_error "--harness custom needs --skills-dir <dir>, --rules-dir <dir>, or both" ;;
    *) harness "$OPT_HARNESS" ||
      usage_error "unknown harness id: $OPT_HARNESS. Valid ids: $HARNESS_IDS custom" ;;
  esac
fi

# ---- Repository -------------------------------------------------------

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd -P)
IN_GIT=0
if command -v git >/dev/null 2>&1 &&
   top=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null); then
  REPO=$(cd "$top" && pwd -P)
  IN_GIT=1
else
  REPO=$SCRIPT_DIR
fi
SKILLS_SRC=$REPO/skills RULES_SRC=$REPO/rules
HAS_SKILLS=0 HAS_RULES=0
if [ -d "$SKILLS_SRC" ]; then HAS_SKILLS=1; fi
if [ -d "$RULES_SRC" ]; then HAS_RULES=1; fi
if [ "$HAS_SKILLS$HAS_RULES" = 00 ]; then
  warn "error: $REPO has no skills/ or rules/ directory."
  {
    say "  The expected shape, with at least one of the two:"
    say "    skills/<name>/    one directory for each skill"
    say "    rules/<name>.md   one file for each rule"
  } >&2
  exit 1
fi

# ---- Interactive menu -------------------------------------------------

if [ "$INTERACTIVE" = 1 ]; then
  {
    say "Repository: $REPO"
    say "Link the skills and rules into which harness?"
    n=0
    for id in $HARNESS_IDS; do
      n=$((n + 1)); harness "$id"
      printf '  %d) %s\n' "$n" "$H_NAME"
    done
    say "  0) Custom: you type the directories"
  } >&2
  while :; do
    printf 'Number (0-%d): ' "$n" >&2
    read -r ans || { printf '\n' >&2; die "no number given"; }
    case $ans in
      ''|*[!0-9]*) ;;
      *) [ "$ans" -le "$n" ] && break ;;
    esac
    warn "type a number from 0 to $n"
  done
  if [ "$ans" -eq 0 ]; then
    OPT_HARNESS=custom
    if [ "$HAS_SKILLS" = 1 ]; then
      printf 'Skills directory (empty: do not link skills): ' >&2
      read -r OPT_SKILLS || OPT_SKILLS=
    fi
    if [ "$HAS_RULES" = 1 ]; then
      printf 'Rules directory (empty: do not link rules): ' >&2
      read -r OPT_RULES || OPT_RULES=
    fi
    [ -n "$OPT_SKILLS$OPT_RULES" ] || die "no directory given; nothing to link"
  else
    n=0
    for id in $HARNESS_IDS; do
      n=$((n + 1))
      if [ "$n" -eq "$ans" ]; then OPT_HARNESS=$id; fi
    done
    harness "$OPT_HARNESS"
  fi
fi

if [ "$OPT_HARNESS" = custom ]; then
  H_NAME=custom H_SKILLS= H_RULES=
  H_NORULES="no rules directory given"
  [ -z "$OPT_SKILLS" ] || H_SKILLS=$(expand_tilde "$OPT_SKILLS")
  [ -z "$OPT_RULES" ] || H_RULES=$(expand_tilde "$OPT_RULES")
fi
H_ID=$OPT_HARNESS

# ---- What to link -----------------------------------------------------

DO_SKILLS=0 DO_RULES=0 SKILLS_NOTE= RULES_NOTE=
if [ "$HAS_SKILLS" = 1 ]; then
  if [ -n "$H_SKILLS" ]; then DO_SKILLS=1
  else SKILLS_NOTE="Skills:     not linked: no skills directory given."; fi
elif [ "$H_ID" = custom ] && [ -n "$H_SKILLS" ]; then
  warn "warning: the repository has no skills/ directory; no skills to link"
fi
if [ "$HAS_RULES" = 1 ]; then
  if [ -n "$H_RULES" ]; then DO_RULES=1
  else RULES_NOTE="Rules:      not linked: $H_NORULES."; fi
elif [ "$H_ID" = custom ] && [ -n "$H_RULES" ]; then
  warn "warning: the repository has no rules/ directory; no rules to link"
fi

# The menu has already shown the repository.
[ "$INTERACTIVE" = 1 ] || say "Repository: $REPO"
if [ "$H_ID" = custom ]; then say "Harness:    custom"
else say "Harness:    $H_NAME ($H_ID)"; fi
if [ "$DO_SKILLS$DO_RULES" = 00 ]; then
  for n in "$SKILLS_NOTE" "$RULES_NOTE"; do [ -z "$n" ] || say "$n"; done
  die "nothing to link for $H_NAME"
fi

# Make a directory and print its absolute path. Refuse the source itself.
target_dir() {
  mkdir -p "$1" || die "cannot make directory $1"
  t_abs=$(cd "$1" && pwd)
  [ "$(cd "$1" && pwd -P)" != "$2" ] || die "$1 is the source directory itself"
  printf '%s\n' "$t_abs"
}

# ---- Linking ----------------------------------------------------------

# Print a link destination with its parent directory as a physical path,
# so that a link made through a symlinked path still matches $REPO.
canon() {
  c_path=${1%/}
  if c_dir=$(cd "$(dirname "$c_path")" 2>/dev/null && pwd -P); then
    printf '%s/%s\n' "$c_dir" "${c_path##*/}"
  else
    printf '%s\n' "$c_path"
  fi
}

CHANGES=0
link_one() {  # source, link path, label
  if [ -L "$2" ]; then
    if [ "$(readlink "$2")" != "$1" ]; then
      rm "$2"
      ln -s "$1" "$2"
      say "  relinked $3"; CHANGES=$((CHANGES + 1))
    fi
  elif [ -e "$2" ]; then
    warn "skipped $3: $2 exists and is not a symbolic link"
  else
    ln -s "$1" "$2"
    say "  linked $3"; CHANGES=$((CHANGES + 1))
  fi
}

# Remove each link in a directory that points into $REPO at a source that
# no longer exists. This also removes links from an older layout.
prune() {
  for p_link in "$1"/*; do
    [ -L "$p_link" ] || continue
    p_dest=$(readlink "$p_link")
    case $p_dest in /*) ;; *) p_dest=$1/$p_dest ;; esac
    p_dest=$(canon "$p_dest")
    case $p_dest in
      "$REPO"/*)
        if [ ! -e "$p_dest" ]; then
          rm "$p_link"
          say "  pruned ${p_link##*/}"; CHANGES=$((CHANGES + 1))
        fi ;;
    esac
  done
}

# A skill that moved from <repo>/<name>/ into skills/<name>/ leaves its
# untracked config.local.yaml behind. Move the file to the new directory.
move_config() {
  m_old=$REPO/$1/config.local.yaml
  [ "$IN_GIT" = 1 ] && [ -f "$m_old" ] &&
    [ ! -e "$SKILLS_SRC/$1/config.local.yaml" ] || return 0
  # Leave a directory that git still tracks: it is not a leftover.
  [ -z "$(git -C "$REPO" --literal-pathspecs ls-files -- "$1" 2>/dev/null)" ] ||
    return 0
  mv "$m_old" "$SKILLS_SRC/$1/config.local.yaml"
  say "  moved $1/config.local.yaml to skills/$1/"
  say "  note: $REPO/$1/ is left from the old layout; check it, then remove it"
  CHANGES=$((CHANGES + 1))
}

# Antigravity discards a rule file without a valid trigger in its
# frontmatter. Return 0 if the file has one.
has_trigger() {
  awk '{ sub(/\r$/, "") }
       NR == 1 { if ($0 !~ /^---[ \t]*$/) exit; next }
       /^---[ \t]*$/ { exit }
       /^trigger:[ \t]*["'\'']?(always_on|model_decision|glob|manual)["'\'']?[ \t]*$/ { found = 1; exit }
       END { exit !found }' "$1"
}

[ -z "$SKILLS_NOTE" ] || say "$SKILLS_NOTE"
if [ "$DO_SKILLS" = 1 ]; then
  dir=$(target_dir "$H_SKILLS" "$SKILLS_SRC")
  H_SKILLS=$dir
  say "Skills:     $dir"
  CHANGES=0
  for src in "$SKILLS_SRC"/*; do
    [ -d "$src" ] || continue
    name=${src##*/}
    case $name in .*) continue ;; esac
    move_config "$name"
    link_one "$src" "$dir/$name" "$name"
  done
  prune "$dir"
  [ "$CHANGES" -gt 0 ] || say "  no changes"
fi

[ -z "$RULES_NOTE" ] || say "$RULES_NOTE"
if [ "$DO_RULES" = 1 ]; then
  dir=$(target_dir "$H_RULES" "$RULES_SRC")
  H_RULES=$dir
  say "Rules:      $dir"
  CHANGES=0
  for src in "$RULES_SRC"/*.md; do
    [ -f "$src" ] || continue
    name=${src##*/}
    case $name in .*) continue ;; esac
    link_name=$name
    case $H_ID:$name in
      copilot:*.instructions.md) ;;
      copilot:*) link_name=${name%.md}.instructions.md ;;
      antigravity:*) has_trigger "$src" ||
        warn "warning: Antigravity ignores rules/$name: its frontmatter has no trigger: line (always_on, model_decision, glob, or manual)" ;;
    esac
    link_one "$src" "$dir/$link_name" "$name"
  done
  prune "$dir"
  [ "$CHANGES" -gt 0 ] || say "  no changes"
fi

# ---- Where things live ------------------------------------------------

# Print an argument for a shell command line, quoted if it needs quotes.
shq() {
  case $1 in
    *[!A-Za-z0-9_./~=-]*) printf "'%s'" "$1" ;;
    *) printf '%s' "$1" ;;
  esac
}
if [ "$H_ID" = custom ]; then
  RERUN=$(shq "$SCRIPT_DIR/$PROG")
  [ -z "$H_SKILLS" ] || RERUN="$RERUN --skills-dir $(shq "$(tilde "$H_SKILLS")")"
  [ -z "$H_RULES" ] || RERUN="$RERUN --rules-dir $(shq "$(tilde "$H_RULES")")"
else
  RERUN="$(shq "$SCRIPT_DIR/$PROG") --harness $H_ID"
fi

say ""
say "The links point into $REPO."
say "The files stay there; the harness reads them through the links."
if [ "$DO_SKILLS" = 1 ]; then
  say "To change a skill's settings on this machine, edit config.local.yaml in"
  say "the skill's directory, $SKILLS_SRC/<name>/. Git ignores that file."
fi
if [ "$IN_GIT" = 1 ]; then
  say "To get updates, run \"git pull\" in $REPO, then run this command again:"
else
  say "After the files in $REPO change, run this command again:"
fi
say "  $RERUN"
say "It links added skills and rules, and removes the links to deleted ones."

if [ "$IN_GIT" = 1 ] && [ "$HAS_SKILLS" = 1 ]; then
  for src in "$SKILLS_SRC"/*; do
    [ -d "$src" ] || continue
    rel=skills/${src##*/}/config.local.yaml
    rc=0
    git -C "$REPO" check-ignore -q -- "$rel" 2>/dev/null || rc=$?
    if [ "$rc" = 1 ]; then
      warn "warning: git does not ignore $rel."
      {
        say "  Add the line config.local.yaml to $REPO/.gitignore,"
        say "  so that the settings of one machine stay out of commits."
      } >&2
      break
    fi
  done
fi
