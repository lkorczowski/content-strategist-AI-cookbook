#!/bin/bash
# git-sync: keeps the repos listed in repos.txt in sync with GitHub (pull, then push). It never commits for you.
# Run every hour by launchd (see install.sh). Cost: zero tokens, a few seconds of CPU. macOS.
# Rules:
#  - uncommitted changes: fetch only, no pull (nothing is overwritten)
#  - git lock present (.git/*.lock, e.g. left by an agent session): repo skipped and reported
#  - behind origin: pull --ff-only; diverged: pull --rebase, clean abort on conflict
#  - ahead of origin: push, except on main (reported, never pushed: main only takes pull requests)
#  - any problem: one log line + a macOS notification
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
LIST="$DIR/repos.txt"
LOG="$HOME/Library/Logs/git-sync.log"
GIT=/usr/bin/git
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin"
export GIT_TERMINAL_PROMPT=0
mkdir -p "$(dirname "$LOG")"
ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "$(ts) $*" >> "$LOG"; }
notify() { /usr/bin/osascript -e "display notification \"$2\" with title \"git-sync\" subtitle \"$1\"" >/dev/null 2>&1; }
problem() { log "WARN $1: $2"; notify "$1" "$2"; }

[ -f "$LIST" ] || { problem "config" "repos.txt missing in $DIR"; exit 1; }

while IFS= read -r line || [ -n "$line" ]; do
  repo="${line%%#*}"; repo="$(echo "$repo" | xargs)"; [ -z "$repo" ] && continue
  repo="${repo/#\~/$HOME}"; name="$(basename "$repo")"
  [ -d "$repo/.git" ] || { problem "$name" "not a git repo: $repo"; continue; }
  cd "$repo" || continue
  if [ -n "$(find .git -maxdepth 4 -name '*.lock' 2>/dev/null | head -1)" ]; then
    problem "$name" "git lock present, repo skipped (remove .git/*.lock if no git command is running)"; continue
  fi
  branch="$($GIT symbolic-ref --short -q HEAD)" || { problem "$name" "detached HEAD, skipped"; continue; }
  $GIT rev-parse --abbrev-ref -q "@{u}" >/dev/null 2>&1 || { log "skip $name ($branch): no upstream branch"; continue; }
  if ! out="$($GIT fetch --quiet --prune 2>&1)"; then problem "$name" "fetch failed: ${out:0:120}"; continue; fi
  ahead="$($GIT rev-list --count '@{u}..HEAD')"; behind="$($GIT rev-list --count 'HEAD..@{u}')"
  dirty="$($GIT status --porcelain --untracked-files=no | head -1)"
  if [ "$behind" -gt 0 ]; then
    if [ -n "$dirty" ]; then
      problem "$name" "$behind commit(s) to pull but local changes are uncommitted: pull postponed"
      continue
    fi
    if [ "$ahead" -eq 0 ]; then
      out="$($GIT pull --ff-only --quiet 2>&1)" || { problem "$name" "fast-forward pull failed: ${out:0:120}"; continue; }
      log "pull $name ($branch) +$behind"
    else
      if ! out="$($GIT pull --rebase --quiet 2>&1)"; then
        $GIT rebase --abort >/dev/null 2>&1
        problem "$name" "diverged branches, rebase conflict: resolve by hand"; continue
      fi
      log "rebase $name ($branch) +$behind"
    fi
  fi
  ahead="$($GIT rev-list --count '@{u}..HEAD')"
  if [ "$ahead" -gt 0 ] && [ "$branch" = "main" ]; then
    problem "$name" "$ahead local commit(s) on main: not pushed, main only takes pull requests"
  elif [ "$ahead" -gt 0 ]; then
    if out="$($GIT push --quiet 2>&1)"; then log "push $name ($branch) $ahead commit(s)"
    else problem "$name" "push refused: ${out:0:120}"; fi
  fi
  [ -n "$dirty" ] && log "info $name: uncommitted changes (not pushed)"
done < "$LIST"
log "run ok"
