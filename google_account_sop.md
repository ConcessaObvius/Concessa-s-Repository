# Google Account + YouTube Channel SOP (v1 – 2026-03-08)

## 1. Prep Environment (Before Signup)
- **Network:** Create the account on Master’s residential ISP (no VPN/proxy). After the account is seasoned (~48h), reintroduce Mullvad using a fixed city/server.
- **Device hygiene:** Use the Harbor Mac with all macOS updates installed and no automation tools running.
- **Browser:** Chrome or Safari with cleared cookies/cache. Disable any suspicious extensions.

## 2. Account Creation Steps
1. Visit <https://accounts.google.com/signup> on the trusted network.
2. Use the chosen username/email (single-purpose for YouTube).
3. Add recovery email (privacy provider) + mobile number immediately.
4. Complete CAPTCHA manually.
5. Enable **2-Step Verification** right away (SMS now, hardware key later).
6. Fill basic profile info (name, birthday) to avoid “blank account” flags.

## 3. Hardening Checklist
- Security Checkup: <https://myaccount.google.com/security-checkup>
- Turn on **Advanced Protection** once a hardware key is available (optional but recommended).
- Under “Less secure app access”: keep OFF.
- Review connected devices; remove anything you don’t control.
- Document the public IP used for creation + date/time in `security/logs.md` for future appeals.

## 4. YouTube Setup
1. Accept YouTube terms, set channel name/branding.
2. Upload a single, original intro video after 24h (avoid mass uploads on day one).
3. Configure Brand Account only if needed; otherwise keep everything under the primary Google identity.
4. Log every upload/setting change in `youtube/SETUP.md` with timestamps.

## 5. Ongoing Usage Rules
- Always connect via the same Mullvad exit (e.g., us-chi multihop) after the initial warm-up period.
- No automated channel creation or bulk uploads; schedule content manually or via YouTube Studio’s scheduler.
- Avoid copy/paste metadata from other creators; keep keywords original.
- Check Policy notifications weekly; archive screenshots in `youtube/COMPLIANCE.md`.

## 6. Privacy Mail Stack (Non-Google)
- Primary communications: Proton Mail (custom domain) or Skiff. Use this for all business/email tasks.
- Reserve Gmail strictly for Google/YouTube login + recovery messages. Do not use it for general correspondence.

## 7. Incident Response
- If Google flags the account, immediately capture the notification, timestamp, and recent actions from the log file.
- Pause uploads until the issue is resolved; respond via the appeal form using the documented evidence.

---
Next step: await Master’s confirmation of the new Gmail address + recovery email/phone so I can update all configs.
