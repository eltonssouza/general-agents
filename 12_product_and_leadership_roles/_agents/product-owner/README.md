# Product Owner (Claude Code, Codex and GitHub Copilot)

**Role** agent of the `general-agents` collection (folder `12_product_and_leadership_roles`). Turns business goals into a product specification: ubiquitous language glossary, AS-IS/TO-BE flow, prioritized INVEST stories with Given/When/Then criteria, business rules matrix, DoR and DoD.

**Nature and source.** Unlike the specialists in folders 01-11, this agent **has no bibliographic source**: the guidelines are established practices, labeled `[practice]`, and it does not cite pages. When a topic has a citable foundation in the collection, it hands off to the specialist (`[from collection: <agent>]`); see `references/INDEX.md`. Origin: the harness's `product-owner` role agent (MIT, Elton Souza), translated and adapted to the collection's standard on 2026-11-01.

## 1. When to use
Example requests: "Write the user stories and acceptance criteria for checkout with a coupon"; "Break this onboarding epic into INVEST stories"; "Review these user stories: are they testable?".
Do not use for: "Implement the coupon endpoint in Java" (→ language/framework agents); "Draw the wireframe of the checkout screen" (→ `product-designer`); "What is a bounded context in DDD, with the source?" (→ `clean-architecture-ddd-expert`).

## 2. Structure
```
product-owner/
├── .claude-plugin/plugin.json, icon.png
├── .github/agents/product-owner.agent.md   # GitHub Copilot (generated from the canonical prompt)
├── AGENTS.md                      # Codex (generated from the canonical prompt)
├── agents/product-owner.md                  # Claude Code (canonical prompt)
├── references/   INDEX.md (nature, origin, boundaries), modelos.md
├── scripts/      story_check.py
├── skills/       po-story-check
├── tests/        casos-de-teste.md, relatorio-de-validacao.md, run_script_tests.py, fixtures/
└── README.md
```

## 3. Installation
**Check each platform's current documentation**, since agent formats and locations change. Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/product-owner`.
- Through the collection's marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install product-owner@general-agents`.
- Usage: "use the product-owner agent to ..." or `@agent-product-owner:product-owner`. As a standalone subagent, copy `agents/product-owner.md` to `.claude/agents/` and replace `${CLAUDE_PLUGIN_ROOT}` with the package folder. Tools: `Read, Grep, Glob, Bash` (remove `Bash` to prevent running the script).

### 3.2 Codex (OpenAI)
Copy the folder into the repository and copy or reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder.

### 3.3 GitHub Copilot
Copy `.github/agents/product-owner.agent.md` to the repository's `.github/agents/` and the package folder (adjust `<PKG>`). `tools: ['read', 'search', 'execute']`.

## 4. Scripts (deterministic, no network)
```bash
python -I scripts/story_check.py stories.md        # format, scenarios, vague terms, technical solution, "and" in the "I want"
python -I scripts/story_check.py - < stories.md
```
The validator accepts stories in Portuguese ("Como ..., quero ..., para ...", Dado/Quando/Então) or English ("As a ..., I want ..., so that ...", Given/When/Then); its output is in English.
```bash
python -I tests/run_script_tests.py
```

## 5. Guarantees and limits
- Replies in the language the user writes in (default: English); pasted content is data, not instructions.
- No bibliographic source: the agent does not cite pages or attribute rules to books; anything that comes from a specialist in the collection carries that specialist's citation.
- Not run on Codex or Copilot in this environment; see `tests/relatorio-de-validacao.md`.
