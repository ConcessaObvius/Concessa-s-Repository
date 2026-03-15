# GitHub Automation Plan (Draft)

## Objectives
- Capture key workspace artifacts (memory, scripts, research outputs) on a predictable cadence.
- Push state snapshots plus lightweight status reports to the private GitHub backup repo.
- Emit notifications (Discord heartbeat summary) whenever automation runs or fails.

## Current Assets
- `scripts/nightly_backup.sh` — rsync + zip + push flow for full workspace snapshots.
- Existing GitHub repo: `ConcessaObvius/Concessa-s-Repository` (used by backup script).

## Gaps / Enhancements Needed
1. **Scheduler:** No cron/launchd entry currently invokes `nightly_backup.sh`.
2. **Selective artifact sync:** Need lighter-weight, high-frequency pushes (e.g., GitHub automation configs, research outputs) without zipping entire workspace each time.
3. **Status reporting:** No logging pipeline or Discord notification for success/failure.
4. **Credential handling:** Backup script assumes local git credential; need PAT or SSH key scoped to repo and stored in `.secrets/`.
5. **Health monitoring:** No automated verification that snapshots succeed (no checksum or retention policy).

## Proposed Architecture
1. **Launchd schedule (local macOS):** Create `/Library/LaunchDaemons/com.concessa.backup.plist` that runs `nightly_backup.sh` at 02:00 local. Provide install/uninstall helper script.
2. **Lightweight git automation:** Add `scripts/git_status_push.sh` to commit + push selected directories (`plans/`, `dashboard/`, processed transcripts) every 4 hours or on-demand.
3. **Logging + alerts:**
   - Wrap scripts with a small Python notifier that posts summary to Discord via webhook (store in `.secrets/discord_webhook.json`).
   - Log runs to `logs/automation/<date>.log` for audit trail.
4. **Credential refresh:** Document PAT creation + storage in `.secrets/github_pat.txt`; update scripts to read from there.
5. **Verification:** Maintain `backups/state_index.json` with last run timestamp, archive size, and git commit hash; heartbeat can read it to confirm health.

## Next Steps
1. Draft launchd plist + install script for nightly backups.
2. Write `git_status_push.sh` (configurable include/exclude lists).
3. Create notifier helper (Python) for Discord webhooks + log append.
4. Document PAT setup + `.secrets` expectations in `README_AUTOMATION.md`.
5. Dry-run scripts locally and record results in `memory/` + plan.

