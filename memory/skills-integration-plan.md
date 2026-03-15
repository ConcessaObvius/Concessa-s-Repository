# Skill Integration Plan

## Priority 1 – Business Operations
1. **coding-agent** – spin up Codex/Claude Code workers for feature builds, refactors, PR reviews. Trigger whenever coding exceeds simple edits.
2. **gh / gh-issues** – monitor repositories, issues, PRs, CI. Use for status checks, code review automation, issue triage.
3. **blogwatcher + summarize** – ingest RSS/YouTube/website feeds (Master Key Society, market intel), auto-summarize for daily briefings.
4. **himalaya (email)** – terminal-level inbox control for triage, drafting, and filing.
5. **xurl** – Twitter/X API automation (posting, reading, DM handling). Core for upcoming public persona.
6. **tmux** – manage long-lived CLI sessions (coding loops, monitors) remotely.
7. **model-usage** – track and report per-model token/cost usage.
8. **sag / sherpa-onnx-tts / openai-whisper(-api)** – TTS/STT stack: ElevenLabs voice outs, offline TTS, and speech-to-text for voice notes.
9. **summarize / nano-pdf / nano-banana-pro / openai-image-gen** – summarization, PDF editing, and creative asset generation.
10. **peekaboo** – macOS UI automation for GUI-only flows.

## Priority 2 – Productivity Tools (enable when needed)
- **apple-notes, apple-reminders, things-mac, notion, obsidian, bear-notes, trello** – integrate if/when we adopt those ecosystems.
- **gog** – access Google Workspace (Gmail, Drive, Calendar) when accounts are connected.
- **imsg / bluebubbles / wacli / voice-call** – extend messaging/voice reach beyond Discord.

## Priority 3 – Lifestyle/IoT (optional)
- **goplaces, spotify-player, sonoscli, openhue, eightctl** – convenience integrations for later.

## Media / Surveillance / Automation
- **video-frames, songsee, gifgrep** – media extraction + visualization.
- **nano-banana-pro, openai-image-gen** – image generation.
- **camsnap** – capture RTSP/ONVIF feeds if we add cameras.
- **clawhub** – manage skill installations (search/update/publish).
- **healthcheck (ready)** – continue using for host security.
- **mcporter / oracle** – advanced MCP and prompt-safety tooling when required.

## Next Steps
1. Install priority skills sequentially (npx clawhub or bundled install), storing credentials securely (1Password skill when available).
2. Document usage patterns in SOPs—each workflow knows which skill to call.
3. Expand/adjust as we add platforms (Notion, Trello, IoT, etc.).
