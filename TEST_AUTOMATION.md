# Automation Dry-Run Checklist

## Prereqs
- `.secrets/github_pat.txt` populated and git credential helper configured (see README_AUTOMATION.md).
- `.secrets/discord_webhook.json` with live webhook URL.
- `scripts/nightly_backup.sh` and `scripts/git_status_push.sh` marked executable.

## 1. Verify Health Tracker Hooks
```bash
python3 scripts/update_state_index.py --job smoke --status success --notes "manual test"
python3 scripts/show_automation_health.py
```
Confirm the new entry appears with the correct timestamp.

## 2. Dry-Run Git Status Push
```bash
./scripts/git_status_push.sh "Dry-run $(date -u +%H:%M)"
```
Expected:
- Commits only whitelisted folders.
- Discord webhook posts success message with timestamp.
- `backups/state_index.json` records `git_status_push` success + notes.
- `logs/automation/git_status_push.log` contains the run log.

## 3. Dry-Run Nightly Backup (manual trigger)
```bash
./scripts/nightly_backup.sh
```
Expected:
- Workspace rsynced into `.backups/state-<timestamp>`.
- Archive pushed to `state/<YYYY-MM-DD>/` in the backup repo.
- Discord webhook posts success/failure.
- `backups/state_index.json` updates `nightly_backup` job entry.

## 4. Log Tail Review
```bash
python3 scripts/show_automation_health.py
```
Confirms both jobs logged with timestamps and displays latest log excerpts.

## 5. LaunchDaemon Validation (after sudo installer)
```bash
sudo scripts/install_backup_launchd.sh
launchctl list | grep com.concessa.backup
```
Check `logs/automation/nightly_backup.log` after the scheduled run to confirm execution.
