# Using OpenClaw

Notes and how-to from testing [OpenClaw](https://openclaw.ai/) — an open-source AI assistant that runs on your own machine and that you operate through chat apps (WhatsApp, Telegram, Discord, iMessage, Slack) rather than a dedicated console.

## What it is

OpenClaw has access to your filesystem, your browser, and a shell. Its power comes from **Skills**: community-built plugins that OpenClaw can also write for itself.

- Site: https://openclaw.ai/
- Docs: https://docs.openclaw.ai/getting-started
- Community skills: https://clawhub.ai

## Prerequisites

```bash
node --version     # v20.12+ required
which node
npm --version
```

If you need to upgrade Node:

```bash
brew upgrade node@22
```

## Install

```bash
curl -fsSL https://openclaw.ai/install.sh | bash

openclaw onboard   # wizard: pick an LLM, connect a chat app, installs the daemon
openclaw doctor    # health check, can auto-fix some issues
openclaw doctor --fix
```

Follow-up steps the doctor command suggests:

```bash
openclaw configure                                                  # set gateway.mode (local or remote)
openclaw config set commands.ownerAllowFrom '["telegram:YOUR_ID"]'  # set command owner
openclaw gateway start                                              # once configured
```

Alternative install path (if you prefer managing Node yourself via nvm):

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
npm install -g openclaw@latest
```

## Local dashboard

```bash
openclaw dashboard
# http://127.0.0.1:18789/
```

If it's not reachable, reconfigure explicitly for local mode and check status:

```bash
openclaw onboard --mode local

openclaw status
openclaw status --all
openclaw gateway probe
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

Config/env file location:

```
~/.openclaw/service-env/ai.openclaw.gateway.env
```

## Running fully local (Ollama)

```bash
ollama launch openclaw
```

See: https://docs.ollama.com/integrations/openclaw — works with any locally installed model (tested with `llama3.1:latest`).

## What it feels like to use

Plain sentences, verb + object + context, no special syntax:

```
"Summarize my last 10 emails and tell me what needs a reply today"
"Schedule a call with Pierre tomorrow at 3pm, 30 minutes, send him the invite"
"Check if my-site.com is up and tell me the load time"
"Write a tweet about AI coordination in newsrooms, post it"
"Remind me in 2 hours to review the pipeline script"
```

### Example pipeline — blog publishing

```
1. Idea & brief   → describe topic, audience, tone, target length once
2. Write post     → ask for the draft with a fixed structure (hook → problem → solution → example → CTA), save as .md
3. Generate image → ask for a featured image in a defined style, save as .png
4. Publish        → push to WordPress via its REST API, draft status first
```

### Example pipeline — turning a post into a video

```
1. Script          → scene-by-scene from the blog draft (visual + narrator text)
2. Screen capture  → browser skill or a local capture tool (ffmpeg / screencapture / OBS)
3. Thumbnail       → generate a YouTube thumbnail image
4. Upload          → YouTube Data API v3, OAuth credentials configured once, unlisted first
```

## Mental model for delegation

| Level | What you do | Example |
|---|---|---|
| Simple | One instruction, one result | "Summarize my emails" |
| Sequential | You drive each step yourself | The blog pipeline above, run manually |
| Automated pipeline | You ask it to run the whole thing, showing outputs before continuing | "Do the full blog process end to end" |
| Custom skill | It writes its own skill from a process you describe once | "Build a skill that does this pipeline in one command" |

## Visual identity note

Concept, in the author's own words:

> Start on a lobster claw icon.

A single open lobster pincer — literal, not a robotic arm. It also happens to be accurate: OpenClaw's own favicon (`openclaw.ai/favicon.svg`) is a red lobster with two claws, antennae, and eyes, not a mechanical claw. The name is meant literally.

## Sources

- Official site: https://openclaw.ai/
- Docs: https://docs.openclaw.ai/
- Community skills hub: https://clawhub.ai
- Beginner tutorial + automation commands: https://imastudio.com/blog/how-to-use-openclaw-beginner-tutorial
- Step-by-step guide: https://openclawhub.tools/tutorial/how-to-use-openclaw-step-by-step-guide/
- Mac setup walkthrough (video): https://www.youtube.com/watch?v=YSJ61RiO7As
- Ollama integration: https://docs.ollama.com/integrations/openclaw
- Uninstall guide: https://www.nxcode.io/fr/resources/news/how-to-uninstall-openclaw-complete-guide-2026
