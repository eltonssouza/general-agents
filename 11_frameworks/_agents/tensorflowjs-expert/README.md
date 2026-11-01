# tensorflowjs-expert

**Overview** agent for TensorFlow.js, built from **4 captured web pages** of tensorflow.org/js (pt-br, automatically translated): Guide (TFJG, 2022-01-24), Landing (TFJL), Setup (TFJS, 2023-11-15) and Getting started/tutorial index (TFJI, 2023-11-30). A fifth capture, **Tutorial-Beginner, is a 404 page** and was discarded. The package is proportional to the source: it does **not** include the API, backends, versions or the contents of the guide sections (NOT COVERED). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

Page convention: code + PDF page of the capture (e.g. `TFJS p.4`). Details and inventory in `references/INDEX.md`. The `references/` files are in Portuguese (the captured language).

## What was read
Extracted text of the 5 sources read in full; rendered TFJS p.1-2, TFJI p.2-3 and TFJL p.1 (the y = 2x - 1 equation and the truncated script-tag line). The Landing is fragmented: only what is legible is asserted.

## Installation (check the current documentation of each platform)
- **Claude Code:** copy the folder to the project's `.claude/plugins/` or `~/.claude/plugins/`, or use `agents/tensorflowjs-expert.md` as a subagent in `.claude/agents/`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install tensorflowjs-expert@general-agents`.
- **Codex (OpenAI):** leave `AGENTS.md` at the repository root (or in `~/.codex/`) with the package folder accessible.
- **GitHub Copilot:** copy `.github/agents/tensorflowjs-expert.agent.md` to the repository's `.github/agents/` and keep the package folder available.
Formats and paths change; check the current documentation of Claude Code, Codex and GitHub Copilot.

## Structure
```
tensorflowjs-expert/
├── .claude-plugin/plugin.json
├── agents/tensorflowjs-expert.md
├── AGENTS.md
├── .github/agents/tensorflowjs-expert.agent.md
├── references/ INDEX, 01-visao-geral, 02-guia-secoes, 03-setup, 04-primeiros-passos, 05-mapa-de-tutoriais, glossario, procedimentos, casos-e-antipadroes, datado
├── scripts/ tfjs_lookup.py (+ tfjs_index.json), tfjs_map.py, tfjs_setup_checklist.py, tfjs_snippet_lint.py
├── skills/       tfjs-topic-lookup, tfjs-tutorial-map, tfjs-setup-checklist, tfjs-snippet-lint   # one SKILL.md per entry (skills/<name>/SKILL.md)
└── tests/ casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py + citation-checks.json, run_script_tests.py, fixtures/
```

## Tests
`python -I tests/run_script_tests.py --src <ROOT>/scratch/frameworks` (33 script tests + citation verifier). The conceptual cases were run by the author against agent+references+scripts; **there was no blind test by an independent model**.

## Limits
Small, dated source; it does not replace the current official TensorFlow.js documentation. General ML: agents in the `09_ai_and_llm` folder.
