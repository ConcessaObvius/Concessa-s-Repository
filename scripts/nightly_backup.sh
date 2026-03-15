#!/bin/bash
set -euo pipefail

WORKSPACE="/Users/concessaobvius/.openclaw/workspace"
BACKUP_WORKDIR="$WORKSPACE/.backups"
REPO_REMOTE="https://github.com/ConcessaObvius/Concessa-s-Repository.git"
REPO_CLONE="$HOME/.openclaw/concessa-ops"
SNAPSHOT_DATE=$(date -u +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H-%M-%SZ)
SNAPSHOT_DIR="$BACKUP_WORKDIR/state-$TIMESTAMP"
ARCHIVE_NAME="state-$TIMESTAMP.zip"
ARCHIVE_PATH="$SNAPSHOT_DIR/$ARCHIVE_NAME"
LOG_DIR="$WORKSPACE/logs/automation"
LOG_FILE="$LOG_DIR/nightly_backup.log"
NOTIFIER="$WORKSPACE/scripts/notify_discord.py"
STATE_UPDATER="$WORKSPACE/scripts/update_state_index.py"
JOB_NAME="nightly_backup"

mkdir -p "$SNAPSHOT_DIR" "$LOG_DIR"

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
  local status notes artifact
  status="$1"
  notes="$2"
  artifact="$3"
  if [[ -x "$STATE_UPDATER" ]]; then
    python3 "$STATE_UPDATER" --job "$JOB_NAME" --status "$status" --artifact "$artifact" --notes "$notes" || true
  fi
}

on_error() {
  local exit_code=$?
  local line=$1
  log "Backup failed at line $line (exit $exit_code)"
  notify "failure" "Backup job failed (exit $exit_code)"
  update_state "failure" "exit $exit_code" ""
  exit $exit_code
}

trap 'on_error $LINENO' ERR

log "Staging workspace snapshot"
rsync -a \
  --exclude '.git' \
  --exclude '.venv*' \
  --exclude '.openclaw' \
  --exclude '.secrets' \
  --exclude '.DS_Store' \
  --exclude '.backups' \
  "$WORKSPACE"/ "$SNAPSHOT_DIR/workspace/"

log "Compressing snapshot"
( cd "$SNAPSHOT_DIR/workspace" && zip -qr "$ARCHIVE_PATH" . )
rm -rf "$SNAPSHOT_DIR/workspace"

if [ ! -d "$REPO_CLONE/.git" ]; then
  log "Cloning backup repo"
  mkdir -p "$(dirname "$REPO_CLONE")"
  git clone "$REPO_REMOTE" "$REPO_CLONE"
fi

cd "$REPO_CLONE"
log "Syncing latest main"
git pull --ff-only

TARGET_DIR="state/$SNAPSHOT_DATE"
mkdir -p "$TARGET_DIR"
cp "$ARCHIVE_PATH" "$TARGET_DIR/"
rm -rf "$SNAPSHOT_DIR"

log "Committing snapshot"
git add "$TARGET_DIR/$ARCHIVE_NAME"
git commit -m "Automated state snapshot $TIMESTAMP" || true

git push origin main
log "Snapshot pushed"
update_state "success" "Snapshot $ARCHIVE_NAME" "$TARGET_DIR/$ARCHIVE_NAME"
notify "success" "Nightly backup pushed ($ARCHIVE_NAME)"
