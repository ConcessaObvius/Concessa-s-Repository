#!/bin/zsh
set -euo pipefail

PLIST_SOURCE="$(cd "$(dirname "$0")" && pwd)/com.concessa.backup.plist"
PLIST_TARGET="/Library/LaunchDaemons/com.concessa.backup.plist"
LOG_DIR="/Users/concessaobvius/.openclaw/workspace/logs/automation"
SCRIPT="/Users/concessaobvius/.openclaw/workspace/scripts/nightly_backup.sh"

if [[ $EUID -ne 0 ]]; then
  echo "This installer must be run with sudo (writes to /Library/LaunchDaemons)." >&2
  exit 1
fi

if [[ ! -x "$SCRIPT" ]]; then
  echo "nightly_backup.sh is not executable; run 'chmod +x $SCRIPT' and retry." >&2
  exit 1
fi

install -m 644 "$PLIST_SOURCE" "$PLIST_TARGET"
chown root:wheel "$PLIST_TARGET"

mkdir -p "$LOG_DIR"
chown concessaobvius:staff "$LOG_DIR"

launchctl unload "$PLIST_TARGET" 2>/dev/null || true
launchctl load "$PLIST_TARGET"
launchctl list | grep -q "com.concessa.backup" && echo "com.concessa.backup loaded."
