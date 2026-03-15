# Agent Dashboard (Work in Progress)

## Goals
- Show live status cards for each agent (Concessa, Dex, Pecunia, Xtra, etc.).
- Display current tasks, next actions, KPIs, and last update timestamp.
- Provide quick message inputs so Master can leave directives per agent.
- Host as a static page (GitHub Pages once repo is ready).

## Status
- Structure defined, initial HTML/JS scaffold in progress.
- Data source: `dashboard/status.json` (to be generated via scripts).

## Next
1. Build `status.json` schema and auto-update script.
2. Implement basic HTML/CSS cards + message placeholders.
3. Add avatar + office-style backgrounds for each agent.
4. Integrate TTS hooks in a later iteration.
