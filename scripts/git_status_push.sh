#!/bin/zsh
set -euo pipefail

WORKSPACE="/Users/concessaobvius/.openclaw/workspace"
REPO="$WORKSPACE"
LOG_DIR="$WORKSPACE/logs/automation"
LOG_FILE="$LOG_DIR/git_status_push.log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
COMMIT_MSG=${1:-"Automation snapshot $TIMESTAMP"}
INCLUDE_PATHS=(
  "plans"
  "dashboard"
  "memory"
  "analysis"
  "transcripts"
  "scripts"
  "logs/automation"
)
NOTIFIER="$WORKSPACE/scripts/notify_discord.py"
STATE_UPDATER="$WORKSPACE/scripts/update_state_index.py"
JOB_NAME="git_status_push"

mkdir -p "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" | tee -a "$LOG_FILE"
}

notify() {
  local status message
  status="$1"
  message="$2"
  if [[ -x "$NOTIFIER" ]]; then
    python3 "$NOTIFIER" --event "$JOB_NAME" --status "$status" --message "$message" || true
  fi
}

update_state() {
  local status notes
  status="$1"
  notes="$2"
  if [[ -x "$STATE_UPDATER" ]]; then
    python3 "$STATE_UPDATER" --job "$JOB_NAME" --status "$status" --notes "$notes" || true
  fi
}

on_error() {
  local exit_code=$?
  local line=$1
  log "git_status_push failed at line $line (exit $exit_code)"
  notify "failure" "git_status_push failed (exit $exit_code)"
  update_state "failure" "exit $exit_code"
  exit $exit_code
}

trap 'on_error $LINENO' ERR

cd "$REPO"

for path in "$INCLUDE_PATHS[@]"; do
  if [[ -e "$path" ]]; then
    git add -A -- "$path"
  fi
done

if git diff --cached --quiet; then
  log "No changes to commit"
  update_state "noop" "No tracked changes"
  notify "noop" "No changes detected"
  exit 0
fi

log "Committing changes"
git commit -m "$COMMIT_MSG"
log "Pushing to origin/main"
git push origin main
log "Push complete"
update_state "success" "Committed + pushed"
notify "success" "Committed and pushed automation snapshot"
