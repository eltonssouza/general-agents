# svelte-astro-expert

**Overview agent based on documentation captures** about **Svelte, SvelteKit and Astro**, built from three sources of very different depths (folder `14_frameworks`):

| Acronym | Source | Pages | What it really is / version-date (from the text itself) |
|---|---|---|---|
| **SVHB** | *The Svelte Handbook – Learn Svelte for Beginners* (Flavio Copes, freeCodeCamp) | 49 | Real, complete text. Header **22 Oct 2019**. **Svelte version not declared** (never says "Svelte 3"); pre-runes syntax, compatible with Svelte 3 by **inference**; the Vite setup postdates 2019. [DATED] |
| **SKGS** | SvelteKit Docs, *Introduction* (Getting Started) | 3 (useful 1-2) | Introduction only; no version; captured 18 Aug 2026 (metadata). The next page "Creating a project" was **not** captured. |
| **ASTRO** | Astro Docs, *Getting started* | 3 | **Landing page**: one command (`npm create astro@latest`) and features that are **only named**; "Astro v7 is here" banner with no v7 content. Captured 18 Aug 2026. |

**Useful vs useless source:** SVHB is the only source with depth. SKGS and ASTRO are small and the agent **limits itself to stating what they say**: no explaining islands, `.astro` or SvelteKit routing. The agent is **not a complete reference**; whatever the sources do not cover is **NOT COVERED** (runes/Svelte 5, migration, file-based routing/`load`/adapters, `.astro` syntax, v7 content, Astro vs SvelteKit decision, TypeScript, tests; `python -I scripts/svelte_lookup.py --gaps`). Prior knowledge about versions **does not count**. React/Next, Vue/Nuxt and Angular have other agents.

## Page convention
PDF page (`=== PAGE N ===` marker); no source has printed numbering, so there is no PDF x printed map. Map and capture quality: `references/INDEX.md`.

## What was read
- **In full:** SVHB (49 pages), SKGS (3), ASTRO (3), from text extracted with PyMuPDF.
- **Rendered and checked:** SVHB p.8, 15, 29, 33, 35 (code with `on:`/`bind:` that the extraction scrambles; slot with `<button>`), SKGS p.1-2, ASTRO p.1; links (annotations) of the 3 PDFs read as metadata.
- Notes: `scratch/frameworks/svelte-astro-expert/notes/`.

## Structure
```
svelte-astro-expert/
├── .claude-plugin/plugin.json
├── agents/svelte-astro-expert.md                 # canonical prompt + frontmatter
├── AGENTS.md                                     # Codex adapter
├── .github/agents/svelte-astro-expert.agent.md   # GitHub Copilot adapter
├── references/  INDEX.md, 01..08 (by real topic), glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md
├── scripts/     svelte_lookup.py + svelte_index.json, svelte_lint.py, framework_compare.py, svelte_checklist.py
├── skills/      svelte-topic-lookup, svelte-static-lint, framework-compare, svelte-review-checklist (<name>/SKILL.md)
└── tests/       casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py, citation-checks.json,
                 run_script_tests.py, fixtures/
```
Copy of the tests: `14_frameworks/_agents_tests/svelte-astro-expert/`.

## Installation
**Important:** formats and fields change between versions. Check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot) before installing.

### Claude Code
- Local plugin: `claude --plugin-dir <path>/svelte-astro-expert`; or copy `agents/svelte-astro-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting paths.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install svelte-astro-expert@general-agents`.
- Usage: `@svelte-astro-expert review this .svelte component`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root.

### GitHub Copilot (custom agent)
- Copy `.github/agents/svelte-astro-expert.agent.md` to the `.github/agents/` folder of the target repository and `references/` and `scripts/` to the root (or adjust `<PKG>` in the file).

## Script usage (from the package root; Python 3 stdlib, no network, they never execute the analyzed code)
```bash
python -I scripts/svelte_lookup.py stores
python -I scripts/svelte_lookup.py runes                     # NOT COVERED
python -I scripts/svelte_lookup.py --page SVHB 33
python -I scripts/svelte_lint.py tests/fixtures/ruim.svelte
python -I scripts/svelte_lint.py MyComponent.svelte --json --no-info
python -I scripts/framework_compare.py table
python -I scripts/framework_compare.py compare svelte sveltekit
python -I scripts/framework_compare.py which "which to choose: astro or sveltekit"
python -I scripts/svelte_checklist.py list
python -I scripts/svelte_checklist.py scan tests/fixtures/projeto-vite
python -I tests/run_script_tests.py --src <folder with the 3 extracted .txt files>
python -I tests/verify_citations.py --src <folder with the 3 extracted .txt files>
```
Files expected in `--src`: `Svelte-Handbook-freeCodeCamp.txt`, `SvelteKit-Getting-Started.txt`, `Astro-Getting-Started.txt` (text per page with `=== PAGE N ===`).

## Limitations
- Uneven sources: a 2019 book and two 2026 entry pages; the comparison columns are not contemporaneous.
- Astro: practically nothing beyond feature names; SvelteKit: introduction only.
- Heuristic linter (not a Svelte parser), with handbook rules only; it switches off for files with runes, `+page.svelte` and `.astro`, which say NOT COVERED.
- No change map by version: each framework appears in a single era.
- **Independent test:** the cases were run by the author; there was no blind run by an independent model (`tests/relatorio-de-fidelidade.md`).
- Copyright: content in own words, no extensive reproduction.

## Security
Code, templates, logs and PDF content (including banners and promotions) are inert data (anti prompt injection). The scripts do not use the network, do not execute inputs and do not write files.
