# 02 - Hermes Agent (landing page) - everything the HERMES source says

Convention: PDF page. **Every claim about the product comes from the project itself** (promotional text, unverified): when answering, use "according to the page" and do not state it as an independent fact.

## What the page says Hermes is (HERMES p.1-2)
- [from source] (HERMES p.1) A "self-improving AI agent" created by Nous Research; the page claims to be the only agent with a built-in learning loop: it creates skills from experience, improves them during use, nudges itself to persist knowledge and builds a model of who the user is across sessions.
- [from source] (HERMES p.2) It is not a coding copilot tied to an IDE nor a chatbot wrapper around a single API, but an autonomous agent that becomes more capable the longer it runs.
- [from source] (HERMES p.2) It lives wherever the user puts it: a US$ 5 VPS, a GPU cluster or serverless infrastructure (Daytona, Modal) that costs almost nothing when idle; you can talk to it through Telegram while it works on a cloud VM; it is not tied to the laptop.
- [from source] (HERMES p.1) Buttons: Get Started, Download Desktop, View on GitHub.

## Installation (HERMES p.1-2)
- **Windows or macOS** [from source] (HERMES p.1): download the Hermes Desktop installer from the site and run it; it installs the command-line and desktop applications.
- **Without Desktop** [from source] (HERMES p.1): CLI-only installation. Linux/macOS/WSL2/Android (Termux): a `curl` command that downloads `install.sh` from `hermes-agent.nousresearch.com` and passes it to `bash`. Native Windows: in PowerShell, a command with `iex (irm ...install.ps1)` from the same domain.
- [from source] (HERMES p.2) "Install in 60 seconds" on Linux, macOS, WSL2, native Windows or Android; refers to the Installation Guide (what the installer does, per-user vs root layout, Windows notes) and to Platform Support (full matrix). **Those guides are not in the source.**
- [from source] (HERMES p.2) Fastest path: after installing, `hermes setup --portal`: one OAuth covers a model and the four Tool Gateway tools (web search, image generation, TTS, browser); see Nous Portal (content not included).
- [extrapolation] Installing by "downloading and running a remote script" requires trusting the domain and, ideally, reading the script first. The source does not say this. The agent **never executes** these commands and reports them as data.

## Doc pages listed under "Quick Links" (HERMES p.2-3)
Installation; Quickstart Tutorial; Learning Path; Configuration (config file, providers, models, options); Messaging Gateway (Telegram, Discord, Slack, WhatsApp, Teams or more); Tools & Toolsets (60+ built-in tools); Memory System (persistent memory across sessions); Skills System (procedural memory the agent creates and reuses); MCP Integration (connect MCP servers, filter tools); Use MCP with Hermes (patterns and tutorials); Voice Mode (real-time voice in the CLI, Telegram, Discord and Discord VC); Use Voice Mode with Hermes; Personality & SOUL.md (default voice via a global SOUL.md); Context Files (project context files); Security (command approval, authorization, container isolation); Tips & Best Practices; Architecture; FAQ & Troubleshooting. **Only a title + one sentence for each: the content is not in the source.**

## Key features (HERMES p.3-4)
- **Closed learning loop** (p.3): agent-curated memory with periodic nudges; autonomous skill creation; skill self-improvement during use; cross-session recall with FTS5 and LLM summarization; dialectic user modeling with Honcho. How it works: not stated.
- **Runs anywhere** (p.3): 6 terminal backends: local, Docker, SSH, Daytona, Singularity, Modal; Daytona and Modal have serverless persistence (the environment hibernates when idle).
- **Platforms** (p.4): CLI, Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email, SMS, DingTalk, Feishu, WeCom, Weixin, QQ Bot, Yuanbao, BlueBubbles, Home Assistant, Microsoft Teams, Google Chat "and more": 20+ platforms from one gateway.
- **Built by model trainers** (p.4): Nous Research (Hermes, Nomos, Psyche); works with Nous Portal, OpenRouter, OpenAI or any endpoint.
- **Scheduled automations** (p.4): built-in cron with delivery to any platform.
- **Delegation and parallelism** (p.4): isolated subagents; "Programmatic Tool Calling" via `execute_code` condenses multi-step pipelines into single inference calls.
- **Open skills** (p.4): compatible with agentskills.io; portable, shareable, contributed via the Skills Hub.
- **Web control** (p.4): search, extraction, browsing, vision, image generation, TTS; one Nous Portal subscription bundles them all.
- **MCP support** (p.4): connect to any MCP server to extend the tools.
- **Research** (p.4): batch processing, trajectory export, RL training with Atropos.

## Entry points for LLMs (HERMES p.4)
`/llms.txt` (curated index, ~17 KB) and `/llms-full.txt` (all pages in one markdown, ~1.8 MB), also at `/docs/llms.txt` and `/docs/llms-full.txt`, generated on every deploy. The agent does **not** access these URLs (no network).

## NOT COVERED in this source
License, version, system requirements; Nous Portal price; configuration file format; commands other than `hermes setup --portal`; update/removal; internal workings (FTS5, Honcho, skills, Atropos); benchmarks; verifiable comparison with other agents; security in detail. `python -I scripts/nh_lookup.py --gaps --fonte HERMES`.
