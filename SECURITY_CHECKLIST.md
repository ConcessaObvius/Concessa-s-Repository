# OpenClaw Security Checklist (v2026-03-08)

1. **Always-on secure network**
   - Mullvad VPN: autoconnect ON, lockdown ON, multihop entry Sweden → exit Chicago (owned hardware only).
   - Verify tunnel before any agent work; alert immediately if the tunnel drops.

2. **Secrets isolation**
   - Store API keys, PATs, and credentials only in encrypted vaults or `.env` files with `600` permissions.
   - Reference secrets via environment variables; never commit or expose raw tokens.

3. **Least-privilege agents**
   - Each agent confined to its project directory with read-only access outside its scope.
   - No agent runs with sudo/admin. Sensitive actions require Concessa approval.

4. **Access logging & monitoring**
   - Log every Git push, token use, external API call, and environment change with timestamp + purpose.
   - Tail system logs for failed auth attempts or unusual processes; trigger Discord alert if detected.

5. **Weekly rotation & patching**
   - Rotate OpenAI, Anthropic, GitHub, and other API tokens weekly (or immediately if compromise suspected).
   - Run nightly cron to check OpenClaw releases/security advisories; apply patches ASAP.

6. **Device & file hygiene**
   - Lock down laptops/VMs with disk encryption, auto-lock, and biometric/2FA.
   - Keep agent workspaces clean: no cached downloads, clear tmp files, and verify file integrity before execution.

7. **Operational safeguards**
   - Maintain daily backup to GitHub (private repo) + encrypted local snapshot.
   - Require dual-confirmation before enabling new integrations, webhooks, or automation that touches external services.

_All agents (current and future) must import this checklist into their workflow and confirm compliance during daily standups/security checks._
