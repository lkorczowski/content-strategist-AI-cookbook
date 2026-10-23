#!/bin/bash
# Installs a git pre-push hook that blocks a push when a check fails.
# Usage, once per clone:  COOKBOOK_DENYLIST=/path/to/private/denylist.txt bash scripts/install_hooks.sh
# The denylist path is stored in the hook, never in the repository.
set -e
ROOT="$(git rev-parse --show-toplevel)"
DENY="${COOKBOOK_DENYLIST:-}"
HOOK="$ROOT/.git/hooks/pre-push"
cat > "$HOOK" <<HOOK
#!/bin/bash
cd "\$(git rev-parse --show-toplevel)" || exit 1
python3 scripts/check_skills.py || exit 1
if [ -n "$DENY" ] && [ -f "$DENY" ]; then
  python3 scripts/leak_scan.py --denylist "$DENY" || exit 1
else
  echo "pre-push: no private denylist configured, generic leak scan only"
  python3 scripts/leak_scan.py || exit 1
fi
HOOK
chmod +x "$HOOK"
echo "pre-push hook installed in $HOOK"
