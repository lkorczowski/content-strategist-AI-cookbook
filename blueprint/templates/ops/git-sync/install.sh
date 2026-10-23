#!/bin/bash
# Installs git-sync as an hourly launchd agent on macOS. Run once from Terminal:
#   GITHUB_OWNER=<your-github-user> bash path/to/ops/git-sync/install.sh
# It discovers the repos cloned under ~/Projects (change ROOTS below) whose origin belongs to GITHUB_OWNER.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL=com.${USER}.git-sync
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
ROOTS="$HOME/Projects"
OWNER="${GITHUB_OWNER:?set GITHUB_OWNER to your GitHub user or organization}"
chmod +x "$DIR/git-sync.sh"

# 1. Discover repos (only if repos.txt does not exist yet)
if [ ! -f "$DIR/repos.txt" ]; then
  echo "# One path per line. Comment a line with # to exclude a repo." > "$DIR/repos.txt"
  for root in $ROOTS; do
    [ -d "$root" ] || continue
    find "$root" -maxdepth 5 -type d -name .git -prune 2>/dev/null | while read -r g; do
      r="$(dirname "$g")"
      url="$(/usr/bin/git -C "$r" remote get-url origin 2>/dev/null || true)"
      case "$url" in *github.com*"$OWNER"/*) echo "$r" >> "$DIR/repos.txt";; *) ;; esac
    done
  done
  echo "Repos found (check $DIR/repos.txt):"
  grep -v '^#' "$DIR/repos.txt"
fi

# 2. launchd agent: every hour and at login
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$DIR/git-sync.sh</string></array>
  <key>StartInterval</key><integer>3600</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/git-sync.out.log</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/git-sync.out.log</string>
</dict></plist>
PL
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Installed. First run in progress. Log: tail -f ~/Library/Logs/git-sync.log"
echo "Uninstall: launchctl bootout gui/\$(id -u)/$LABEL && rm $PLIST"
