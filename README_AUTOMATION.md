# Automation Setup Guide

## 1. GitHub Credentials
1. Create a fine-scoped PAT (classic) with `repo` access for `ConcessaObvius/Concessa-s-Repository`.
2. Save it to `~/.openclaw/workspace/.secrets/github_pat.txt` (600 perms).
3. Configure git to use the PAT for that remote:
   ```bash
   git config credential.helper store
   printf 'https://%s:x-oauth-basic@github.com\n' "$(cat .secrets/github_pat.txt)" > ~/.git-credentials
   ```
4. Test with `git ls-remote origin`.

## 2. Discord Webhook
1. Create an incoming webhook in the private ops channel.
2. Store it in `.secrets/discord_webhook.json`:
   ```json
   { "url": "https://discord.com/api/webhooks/..." }
   ```
3. Ensure the file is `chmod 600`.

## 3. Nightly Backup LaunchDaemon
1. Mark `scripts/nightly_backup.sh` executable (`chmod +x`).
2. Run `sudo scripts/install_backup_launchd.sh`.
3. Verify with `launchctl list | grep com.concessa.backup` and inspect logs in `logs/automation/nightly_backup.log`.

## 4. Daytime Git Sync
- Trigger manually: `./scripts/git_status_push.sh "Automation snapshot $(date -u)"`
- Script will:
  - Add/update `plans/`, `dashboard/`, `memory/`, `analysis/`, `transcripts/`, `scripts/`, and `logs/automation/`.
  - Commit and push to `origin/main`.
  - Send a Discord notification via `scripts/notify_discord.py`.

## 5. Future Cron / Launchd
- Once scripts are tested manually, add a second LaunchDaemon or cron entry to run `git_status_push.sh` every 4 hours for incremental updates.

## 6. Health Checks
- Heartbeat should read `logs/automation/*.log` or a future `backups/state_index.json` to confirm last run timestamp and exit codes.
