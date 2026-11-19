# Delegation by platform

[DATED] Checked against the official documentation on 2026-10-31 (models: 2026-11-01; Relay: 2026-11-19). Formats change; check again if something does not work.

## Claude Code
- **`Agent`** tool (formerly `Task`, which remains as an alias). `subagent_type` = the agent identifier.
- Plugin agents have a scoped name: `<plugin>:<agent>` (e.g. `python-expert:python-expert`); copied to `.claude/agents/`, they use only `<agent>`. Use the identifier **exactly** as it appears in the list of available agents.
- Running as the **main thread** (`claude --agent general-agents-orchestrator`, or `"agent"` in `.claude/settings.json`), the orchestrator creates subagents if `Agent` is in `tools`.
- As a **subagent**, it can also delegate: by default there are up to 3 levels below the main conversation (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). At the limit, the `Agent` tool is removed; then deliver the delegation plan.
- Optional restriction: `tools: Agent(name1, name2), ...` works as an allowlist **only** when the agent is the main thread. It is not configured, because the name changes with the installation (plugin vs copy).
- Plugin agents ignore `hooks`, `mcpServers` and `permissionMode` in the frontmatter.
- **Model:** the `model` frontmatter field accepts `sonnet`, `opus`, `haiku`, `fable`, a full ID (`claude-opus-5-5`) or `inherit`. Resolution order: the `model` parameter of the call → the frontmatter `model` → `CLAUDE_CODE_SUBAGENT_MODEL` → the conversation model. Only aliases fit in the `Agent` tool call. `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` makes it ignore the frontmatter. The page does not say whether plugin agents respect `model`: checked in practice on 2026-11-01 (see `tests/relatorio-de-validacao.md`).
- Source: https://code.claude.com/docs/en/sub-agents

## OpenAI Codex
- Reads `AGENTS.md`. Local versions delegate to subagents when the user asks or when the applicable `AGENTS.md`/skill asks. This package's `AGENTS.md` asks.
- Codex custom agents are TOML files in `.codex/agents/` (required fields `name`, `description`, `developer_instructions`). The collection's specialists have **no** TOML; delegate to a generic subagent with the brief starting with "Read `<ROOT>/<path>/AGENTS.md` and `agents/<name>.md` and follow them".
- **Model:** the collection's packages have no TOML; each one's `AGENTS.md` carries the recommended model (block `<!-- modelo:inicio -->`), and the orchestrator uses the agent's OpenAI model when creating the subagent if the platform allows.
- Concurrency limits in `[agents]` of `config.toml` (`max_concurrent_threads_per_session`; `max_threads` is a legacy alias).
- Source: https://learn.chatgpt.com/docs/agent-configuration/subagents (redirected from developers.openai.com/codex/subagents)

## GitHub Copilot (VS Code / Copilot)
- Custom agents in `.github/agents/*.agent.md` (workspace) or `~/.copilot/agents/` (user).
- To delegate: include the **`agent`** tool set in `tools` and list the allowed ones in **`agents`** (`['*']` = all; `[]` blocks). Names are case-sensitive.
- Tool aliases: `execute`, `read`, `edit`, `search`, `agent`, `web`, `todo`.
- **Model:** `model` accepts text or a preference-ordered list (uses the first available); the values are Copilot runtime IDs. The collection writes `['claude-<model>-5.5', '<gpt>']` (IDs from the `github-copilot` model catalog).
- Specialist not installed as a custom agent: delegate to a generic subagent with the "read the canonical prompt" brief.
- Sources: https://code.visualstudio.com/docs/copilot/customization/custom-agents and https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference

## Relay
- Install the collection with `relay agents install` (a commit pinned in Relay; `--from <path>` installs a local copy offline). `/agents` and `relay agents list` show the agents that loaded and the ones that did not, with the reason.
- **`agent`** tool with Claude Code's arguments (`subagent_type`, `description`, `prompt`). `subagent_type` = the agent's `name` from its frontmatter, with no plugin prefix. The subagent runs in the same process with the tools and system prompt of its definition; `<PKG>` and `<ROOT>` are replaced with the package and collection folders.
- **Routing without Python:** the `route_agent` tool returns the same answer as `scripts/route.py --json` (Relay runs the same ranking in its Rust core, checked against the script). Use it in place of `python -I <PKG>/scripts/route.py` when Python is not available.
- **Depth:** up to 3 sessions in a chain (main, orchestrator, specialist; `subagents.maxDepth`). At the limit the `agent` tool is removed; then deliver the delegation plan. Also limited per subagent: concurrency, tokens and time (`subagents.*`).
- **Tools:** `Read`, `Grep`, `Glob`, `Bash`, `Edit`, `Write` and `Agent` map to Relay's tools; a definition naming any other tool is not loaded.
- **Model:** `haiku`, `sonnet` and `opus` are capability tiers (`fast`, `balanced`, `strong`), resolved by the `modelTiers` setting or from catalog prices on the session's provider; `inherit` or no `model` uses the session's model.
- **Harness:** the brief does not authorize anything (a brief saying "push the branch" does not allow the push) and records no constraint; the developer's constraints reach the subagent. Authorization requests open in the developer's session, with the agent's name. The subagent's edits and checks count in the main session's evidence, so a delegated edit without a check is still flagged.
- Source: Relay's `packages/coding-agent/docs/subagents.md`

## No delegation available
Do not simulate specialist answers. Deliver the plan: a `subtask → agent → ready brief` table (template in `protocolo.md`), for execution by the main agent or the user.
