# automation-agents-n8n-hermes-expert

**Documentation-capture-based overview** agent for two landing pages: **n8n Docs** (acronym **N8N**, `n8n-Docs.pdf`, 4 pages) and **Hermes Agent** by Nous Research (acronym **HERMES**, `Hermes-Agent-Docs.pdf`, 4 pages). It states only what the pages say (what n8n is, doc sections, n8n MCP connection, what Hermes says about itself, Desktop/CLI installation, `hermes setup --portal`, listed features) and answers **"NOT COVERED"** for the rest. Cites `N8N p.N` / `HERMES p.N`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Notices:** (1) the sources are landing pages: n8n has ~2 thousand useful characters, almost only link titles; Hermes has ~4 thousand, in the project's own promotional text. (2) [DATED]: 2026 captures, no version. (3) It does not replace the current official documentation. (4) AI agents in general: `agentic-ai-context-engineering-expert` (`09_ai_and_llm/_agents/`).

## Page convention
PDF page (marker `=== PAGE N ===`); no offset. Details and the reading statement in `references/INDEX.md`.

## Structure
```
automation-agents-n8n-hermes-expert/
├── .claude-plugin/plugin.json
├── agents/automation-agents-n8n-hermes-expert.md   # canonical prompt
├── AGENTS.md                                       # Codex adapter
├── .github/agents/automation-agents-n8n-hermes-expert.agent.md   # GitHub Copilot adapter
├── references/  INDEX, 01-n8n-docs-landing, 02-hermes-agent-landing, 03-comparacao-e-fronteiras,
│                glossario, procedimentos, casos-e-antipadroes, datado
├── skills/      nh-lookup, nh-map-checklist, nh-compare   (SKILL.md; use the scripts in scripts/)
├── scripts/     nh_lookup.py, nh_map.py, nh_compare.py + nh_index.json   (stdlib, no network)
└── tests/       casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py + citation-checks.json,
                 run_script_tests.py, fixtures/
```
Copy of the tests in `../../_agents_tests/automation-agents-n8n-hermes-expert/`.

## Installation
**Important:** formats and fields change between versions; check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

- **Claude Code:** local plugin `claude --plugin-dir <path>/automation-agents-n8n-hermes-expert`, or copy `agents/automation-agents-n8n-hermes-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting paths. Usage: `@automation-agents-n8n-hermes-expert what does the Hermes doc say about installation?`
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install automation-agents-n8n-hermes-expert@general-agents`.
- **OpenAI Codex (and agents that read `AGENTS.md`):** copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root.
- **GitHub Copilot (custom agent):** copy `.github/agents/automation-agents-n8n-hermes-expert.agent.md` to `.github/agents/` of the target repository and `references/` and `scripts/` to the root (or adjust `<PKG>`).

## Scripts (from the package root)
```bash
python -I scripts/nh_lookup.py "install hermes"           # search; NOT COVERED when there is nothing
python -I scripts/nh_lookup.py --gaps                     # known gaps
python -I scripts/nh_map.py map                           # map by page and depth
python -I scripts/nh_map.py checklist --preset geral      # COVERED / PARTIAL / NOT COVERED per doc
python -I scripts/nh_compare.py --dim mcp installation    # comparator restricted to the sources, no verdict
python -I tests/run_script_tests.py --src <ROOT>/scratch/frameworks
python -I tests/verify_citations.py --src <ROOT>/scratch/frameworks
```
Search terms and checklist items can be written in Portuguese or English. The scripts only read local files, use no network and do not run any command cited in the sources.

## Limitations
Proportional to the source: answers well "what do the pages say" and "is this covered?"; it does not teach how to use n8n or Hermes. The tests were run by the author, not by an independent model.
