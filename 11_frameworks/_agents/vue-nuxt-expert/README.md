# vue-nuxt-expert

**Overview agent based on documentation captures** on **Vue and Nuxt**, built from three short sources (folder `14_frameworks`):

| Abbr. | Source | Pages | Version/date (from the text itself) |
|---|---|---|---|
| **VUEHB** | *The Vue Handbook* (Flavio Copes, freeCodeCamp) | 133 | 5 Jul 2018; **Vue 2 by inference** (the text never says "Vue 2") [DATED] |
| **VUE3G** | Vue 3 documentation introduction (vuejs.org) | 8 | "Vue 3"; Vue 2 EOL on 31/12/2023 (p.1); 2026 capture with no printed date |
| **NUXT** | *Get Started with Nuxt v4* introduction (nuxt.com) | 6 (useful 1-4) | **v4.5.2** (p.1); footer 2016-2026 |

**Not a complete reference** for Vue/Nuxt. What the sources do not cover is **NOT COVERED** (Pinia, Vue Router 4, Vue 2->3 migration, Vite, `:key`, `defineProps`, computed/watch in the Composition API, `useFetch`, Nuxt installation/deployment etc.; `python -I scripts/vue_lookup.py --gaps`). Prior knowledge about versions **does not apply**: only the text read, with `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Svelte, React/Next and Angular have other agents.

## Page convention
PDF page (marker `=== PAGE N ===`); the sources have no printed numbering. Map and capture quality (truncated code, image-only pages): `references/INDEX.md`.

## What was read
- **In full:** VUEHB (133 pp), VUE3G (8), NUXT (6). Texts extracted with PyMuPDF.
- **Rendered:** VUEHB p.116 and p.126 (truncated code), NUXT p.1 and p.5.
- **Not checked against images:** Vue CLI/DevTools/Vetur screenshots (VUEHB p.20-25, 36-54) and the VUE3G p.2 demo.
- Notes: `scratch/frameworks/vue-nuxt-expert/notes/`.

## Structure
```
vue-nuxt-expert/
├── .claude-plugin/plugin.json
├── agents/vue-nuxt-expert.md                 # canonical prompt + frontmatter
├── AGENTS.md                                 # Codex adapter
├── .github/agents/vue-nuxt-expert.agent.md   # GitHub Copilot adapter
├── references/  INDEX.md, 01..10 (by real topic), glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md
├── skills/       4 skills (SKILL.md per folder): vue-topic-lookup, vue-static-lint, vue-options-vs-composition, nuxt-project-checklist
├── scripts/     vue_lookup.py + vue_index.json, vue_lint.py, vue_compare.py, nuxt_checklist.py
└── tests/       casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py, citation-checks.json,
                 run_script_tests.py, fixtures/
```
Copy of the tests: `14_frameworks/_agents_tests/vue-nuxt-expert/`.

## Installation
**Important:** formats and fields change between versions. Check each platform's current documentation (Claude Code, OpenAI Codex, GitHub Copilot) before installing.

### Claude Code
- Local plugin: `claude --plugin-dir <path>/vue-nuxt-expert`; or copy `agents/vue-nuxt-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting paths.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install vue-nuxt-expert@general-agents`.
- Usage: `@vue-nuxt-expert what is the difference between computed and watch?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root.

### GitHub Copilot (custom agent)
- Copy `.github/agents/vue-nuxt-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>` in the file).

## Script usage (from the package root; Python 3 stdlib, no network, they never execute the analyzed code)
```bash
python -I scripts/vue_lookup.py computed
python -I scripts/vue_lookup.py pinia                      # NOT COVERED
python -I scripts/vue_lookup.py --page VUEHB 116
python -I scripts/vue_lint.py tests/fixtures/ruim-vue2.vue
python -I scripts/vue_lint.py MyComponent.vue --json --no-info
python -I scripts/vue_compare.py table
python -I scripts/vue_compare.py detect MyComponent.vue
python -I scripts/vue_compare.py recommend --build-tools yes --complexity high
python -I scripts/nuxt_checklist.py scan tests/fixtures/nuxt-bom
python -I scripts/nuxt_checklist.py modes
python -I tests/run_script_tests.py --src <folder with the 3 extracted .txt files>
python -I tests/verify_citations.py --src <folder with the 3 extracted .txt files>
```
Files expected in `--src`: `Vue-Handbook-freeCodeCamp.txt`, `Vue3-Guide-Introduction.txt`, `Nuxt-Getting-Started.txt` (text per page with `=== PAGE N ===`).

## Limitations
- Short/dated sources; handbook with truncated code; VUE3G and NUXT are introductions.
- Heuristic linter (not a Vue parser); rules only with textual support; VUE3-01/02 are [inference].
- No Vue 2 -> 3 migration guide in the collection.
- **Independent testing:** the cases were executed by the author; there was no blind run by an independent model (`tests/relatorio-de-fidelidade.md`).
- Copyright: content in own words, no extensive reproduction.

## Security
Code, templates, logs and the content of the PDFs are inert data (anti prompt injection). The scripts do not use the network, do not execute inputs and do not write files.
