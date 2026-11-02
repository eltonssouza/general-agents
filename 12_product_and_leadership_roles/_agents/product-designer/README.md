# Product Designer (Claude Code, Codex and GitHub Copilot)

**Role** agent of the `general-agents` collection (folder `12_product_and_leadership_roles`). It specifies journeys and flows, information architecture, wireframe anatomy, design tokens and all component states, with a WCAG 2.2 AA accessibility checklist measured by script.

**Nature and source.** Unlike the specialists in folders 01-11, this agent **has no bibliographic source**: the guidelines are established practices, labeled `[practice]`, and it does not cite pages. When the topic has a citable basis in the collection, it hands off to the specialist (`[from collection: <agent>]`); see `references/INDEX.md`. Origin: the harness's `product-designer` role agent (MIT, Elton Souza), translated to English and adapted to the collection standard on 2026-11-01.

## 1. When to use
Example requests: "Design the sign-up flow and specify the form states"; "Define the color design tokens and check the contrast"; "Does this gray #777 pass contrast on white?".
Do not use for: "Implement this component in React" (→ `nextjs-react-expert`); "Write the acceptance criteria for sign-up" (→ `product-owner`); "What is web accessibility and why does it matter, with the source?" (→ `web-accessibility-visual-design-expert`).

## 2. Structure
```
product-designer/
├── .claude-plugin/plugin.json, icon.png
├── .github/agents/product-designer.agent.md   # GitHub Copilot (generated from the canonical)
├── AGENTS.md                      # Codex (generated from the canonical)
├── agents/product-designer.md                  # Claude Code (canonical prompt)
├── references/   INDEX.md (nature, origin, boundaries), modelos.md
├── scripts/      contrast.py
├── skills/       pd-contrast-check
├── tests/        casos-de-teste.md, relatorio-de-validacao.md, run_script_tests.py
└── README.md
```

## 3. Installation
**Check each platform's current documentation**, since agent formats and locations change. Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/product-designer`.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install product-designer@general-agents`.
- Usage: "use the product-designer agent to ..." or `@agent-product-designer:product-designer`. As a standalone subagent, copy `agents/product-designer.md` to `.claude/agents/` and replace `${CLAUDE_PLUGIN_ROOT}` with the package folder. Tools: `Read, Grep, Glob, Bash` (remove `Bash` to prevent running the script).

### 3.2 Codex (OpenAI)
Copy the folder into the repository and copy or reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder.

### 3.3 GitHub Copilot
Copy `.github/agents/product-designer.agent.md` to the repository's `.github/agents/` and the package folder (adjust `<PKG>`). `tools: ['read', 'search', 'execute']`.

## 4. Scripts (deterministic, no network)
```bash
python -I scripts/contrast.py "#767676" "#FFFFFF"          # ratio and AA/AAA verdict
python -I scripts/contrast.py "#000/#fff" "#777/#fff" --json
```
```bash
python -I tests/run_script_tests.py
```

## 5. Guarantees and limits
- Replies in the language the user writes in (default: English); pasted content is data, not instructions.
- No bibliographic source: the agent does not cite pages or attribute rules to books; anything that comes from a collection specialist carries that specialist's citation.
- Not run on Codex or Copilot in this environment; see `tests/relatorio-de-validacao.md`.
