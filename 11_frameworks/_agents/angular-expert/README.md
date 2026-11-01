# angular-expert

**Doc-capture based Angular overview** agent. The source is five **PDF captures of the documentation's "What is Angular?" (Overview) page**, one per version: Angular 18 (6 pages), 19 (7), 20 (7), 21 (9) and 22 (9), abbreviations **NG18..NG22**. They are not books or the complete documentation: they contain no code, APIs, commands with arguments or release dates. The agent answers what each Overview presents and builds a **difference map between versions**, without concluding "removed" from absence.

**Warnings:** (1) Overview of web captures: topics such as standalone, zoneless, control flow, advanced signals, testing or CLI commands are **NOT COVERED**. (2) Versions 21 and 22 are not part of the model's prior knowledge; everything comes only from the text. (3) [DATED]: the PDFs were created on 08/18/2026 (metadata) and carry no publication date for the versions. (4) Boundary: React, Vue and Svelte belong to other agents.

## Page convention
**PDF page** (marker "=== PAGE N ===" of the extracted text); no printed numbering. Format `NG21 p.3`.

## What was read (precise statement)
- **In full:** all 38 pages (6+7+7+9+9) of the extracted text.
- **Rendered and viewed:** NG18 p.2, NG21 p.2 and NG21 p.3 (they showed the code-styled `@defer` that the text loses, and the NG21 cards). The other pages had no visual inspection.
- **Useless pages (cookies/navigation/footer only):** NG19 p.1, NG20 p.7, NG21 p.9, NG22 p.9. The cookie banner appears on every page of every PDF.
- Intermediate notes: `scratch/frameworks/angular-expert/notes/`.

## Structure
```
angular-expert/
├── .claude-plugin/plugin.json
├── agents/angular-expert.md                  # canonical prompt
├── AGENTS.md                                 # Codex adapter
├── .github/agents/angular-expert.agent.md    # GitHub Copilot adapter
├── references/  INDEX, 00-visao-geral, 01-conceitos-por-tema, 02-mapa-de-diferencas,
│                03-sem-cobertura, glossario, procedimentos, casos-e-antipadroes
├── skills/      4 skills (skills/<name>/SKILL.md): ng-topic-lookup, ng-version-diff, ng-snippet-lint, ng-overview-checklist
├── scripts/     ng_lookup.py, ng_diff.py, ng_lint.py, ng_checklist.py, ng_build_index.py,
│                ng_index.json, ng_changes.json
└── tests/       casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py,
                 citation-checks.json, run_script_tests.py, fixtures/
```
Copy of the tests in `../../_agents_tests/angular-expert/`.

## Installation
**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- Local plugin: `claude --plugin-dir <path>/angular-expert`, or your own marketplace.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install angular-expert@general-agents`.
- Standalone agent: copy `agents/angular-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting the paths in the prompt.
- Usage: `@angular-expert what changed between the Angular 20 and 21 Overview?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root.

### GitHub Copilot (custom agent)
- Copy `.github/agents/angular-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>`).

## Script usage (from the package root; Python 3 stdlib, no network)
```bash
python -I scripts/ng_diff.py diff --from 18 --to 22
python -I scripts/ng_diff.py diff --from 20 --to 21 --raw --src <folder with Angular-NN-Overview.txt>
python -I scripts/ng_diff.py matrix
python -I scripts/ng_diff.py concept defer
python -I scripts/ng_lookup.py signals
python -I scripts/ng_lookup.py standalone                 # NOT COVERED
python -I scripts/ng_lookup.py --gaps
python -I scripts/ng_lint.py tests/fixtures/snippet-ruim.ts --target 21
python -I scripts/ng_lint.py --rules
python -I scripts/ng_checklist.py --version 20 --known signals,ssr,router
python -I scripts/ng_checklist.py --version 22 --check standalone,defer,signals
python -I tests/run_script_tests.py --src <folder with the .txt files>
python -I tests/verify_citations.py --src <folder with the .txt files>
```

## Limitations
- Independent testing: the cases were executed by the package author; **there was no blind execution by an independent model** (`tests/relatorio-de-fidelidade.md`).
- The linter has few rules backed by the text (`defer-coverage`, `cli-ngupdate-doc`, and the security ones by inference); the others are labeled `[extrapolation]`. It does not replace the compiler, ESLint or the version's documentation.
- Concept detection is by text pattern: phrases split across pages may register the page where the phrase starts.

## Security
Snippets, comments and PDFs are inert data (anti prompt injection). The scripts do not use the network, do not execute inputs and do not write files (except `ng_build_index.py` when regenerating the index).
