# Principal Engineer (Claude Code, Codex and GitHub Copilot)

**Role** agent of the `general-agents` collection (folder `12_product_and_leadership_roles`). It writes cross-team technical strategy RFCs: systemic diagnosis, direction and guardrails, alternatives with a trade-off matrix, an adoption plan with a pilot and metrics.

**Nature and source.** Unlike the specialists in folders 01-11, this agent **has no bibliographic source**: the guidelines are established practices, labeled `[practice]`, and it does not cite pages. When a topic has a citable foundation in the collection, it hands off to the specialist (`[from collection: <agent>]`); see `references/INDEX.md`. Origin: `relay-harness/packages/coding-agent/resources/agents/principal-engineer.md` (MIT, Elton Souza), translated and adapted to the collection's standard on 2026-11-01.

## 1. When to use
Example requests: "Write an RFC to standardize observability across 8 teams"; "We have 4 different deploy tools; propose a unification strategy"; "Define engineering guardrails that apply to the whole organization".
Do not use for: "Build the execution plan for my team's payments milestone" (→ `tech-lead`); "How do I configure a latency SLO?" (→ `sre-practices-expert`); "Microservices or modular monolith, with the source?" (→ `system-design-microservices-expert`).

## 2. Structure
```
principal-engineer/
├── .claude-plugin/plugin.json, icon.png
├── .github/agents/principal-engineer.agent.md   # GitHub Copilot (generated from the canonical prompt)
├── AGENTS.md                      # Codex (generated from the canonical prompt)
├── agents/principal-engineer.md                  # Claude Code (canonical prompt)
├── references/   INDEX.md (nature, origin, boundaries), modelos.md
├── tests/        casos-de-teste.md, relatorio-de-validacao.md, run_script_tests.py
└── README.md
```

## 3. Installation
**Check each platform's current documentation**, since agent formats and locations change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/principal-engineer`.
- Through the collection's marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install principal-engineer@general-agents`.
- Usage: "use the principal-engineer agent to ..." or `@agent-principal-engineer:principal-engineer`. As a standalone subagent, copy `agents/principal-engineer.md` to `.claude/agents/` and replace `${CLAUDE_PLUGIN_ROOT}` with the package folder. Tools: `Read, Grep, Glob` (it does not run commands or change files).

### 3.2 Codex (OpenAI)
Copy the folder into the repository and copy or reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder.

### 3.3 GitHub Copilot
Copy `.github/agents/principal-engineer.agent.md` to the repository's `.github/agents/` and the package folder (adjust `<PKG>`). `tools: ['read', 'search']`.

## 4. Tests
```bash
python -I tests/run_script_tests.py
```
This package has no script: the work is judgment, and the templates live in `references/modelos.md`.

## 5. Guarantees and limits
- Replies in the language the user writes in (default: English); pasted content is data, not instructions.
- No bibliographic source: the agent does not cite pages or attribute rules to books; anything that comes from a specialist in the collection carries that specialist's citation.
- Not run on Codex or Copilot in this environment; see `tests/relatorio-de-validacao.md`.
