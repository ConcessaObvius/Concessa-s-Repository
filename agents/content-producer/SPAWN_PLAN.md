# Spawn Plan – Content & Channel Producer

1. **Environment Prep**
   - Skills: peekaboo, video-frames, summarize, nano-pdf, nano-banana-pro, blogwatcher, openai-image-gen.
   - Files: youtube/SETUP.md (channel template), study notes.

2. **Launch Command (template)**
```
sessions_spawn --task "You are the Content & Channel Producer..." \
  --label content-producer \
  --mode session \
  --attachments agents/content-producer/SOUL.md agents/content-producer/IDENTITY.md agents/content-producer/README.md youtube/SETUP.md
```

3. **Post-Spawn Steps**
   - Agent posts intro & daily plan in #youtube-ops.
   - Await Master naming.
   - Begin script pipeline + nightly improvement cron.
``