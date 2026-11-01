# rails-getting-started-expert

**Ruby on Rails overview agent based on a single source**: the official guide *Getting Started with Rails* (abbreviation **RGS**), captured from the website as a 72-page PDF. The guide builds the **"store"** app (a simple e-commerce), not a "blog", and ends with deploy via Kamal. Version declared in the text: **Rails 8.1.0 or newer, Ruby 3.2 or newer**; the publication date **is not printed**. Everything is **[DATED]** relative to Rails 8.1.x.

It cites the page in every rule: `[from source] (RGS p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Warnings:** (1) it is an introductory tutorial, not a complete reference: what it does not cover is **NOT COVERED** (`has_many :through`, API-only, PostgreSQL, Devise, RSpec, changes between Rails versions...). (2) The Ruby language belongs to **ruby-expert** (`01_programming_languages/_agents/`); databases belong to other agents. (3) It does not replace the current Rails documentation.

## Page convention
**PDF page = printed "Page N of 72"**; no offset (p.1 has no header, but the numbering matches). Details in `references/INDEX.md`.

## What was read (precise statement)
- **In full:** the 72 pages of the extracted text (~96 thousand characters), in sequential blocks; notes in `scratch/frameworks/rails-getting-started-expert/notes/`.
- **Capture quality:** all pages have useful content; none is a 404. Images (welcome page, browser screenshots) have no text; they were not rendered because the text describes them and the code appears in full in the extracted text. **No page rendering was done.**

## Structure
```
rails-getting-started-expert/
├── .claude-plugin/plugin.json
├── agents/rails-getting-started-expert.md        # canonical prompt
├── AGENTS.md                                     # Codex adapter
├── .github/agents/rails-getting-started-expert.agent.md   # Copilot adapter
├── references/  INDEX.md, 01..11 (by topic), comandos-do-guia.md, checklist-store.md,
│                glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md
├── skills/      rails-topic-lookup, rails-command-plan, rails-snippet-lint, rails-store-checklist   (SKILL.md; they use the scripts in scripts/)
├── scripts/     rails_lookup.py + rails_index.json, rails_plan.py, rails_lint.py, rails_store_checklist.py
└── tests/       casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py + citation-checks.json,
                 run_script_tests.py, fixtures/
```
Copy of the tests in `../../_agents_tests/rails-getting-started-expert/` (relative to `14_frameworks/_agents/`).

## Installation
**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform.

- **Claude Code:** local plugin (`claude --plugin-dir <path>/rails-getting-started-expert`) or copy `agents/rails-getting-started-expert.md` to `~/.claude/agents/` and keep `references/` and `scripts/` accessible (adjust the paths in the prompt). Usage: `@rails-getting-started-expert what does resources :products do?`
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install rails-getting-started-expert@general-agents`.
- **OpenAI Codex (and agents that read `AGENTS.md`):** copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root.
- **GitHub Copilot:** copy `.github/agents/rails-getting-started-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root.

## Scripts (from the package root; Python 3 stdlib; no network; they never run Rails)
```bash
python -I scripts/rails_lookup.py "strong parameters"      # topic -> pages
python -I scripts/rails_lookup.py --gaps                   # NOT COVERED
python -I scripts/rails_plan.py plan --fases app,banco,model,controller --model Product:name:string
python -I scripts/rails_plan.py commands                   # all commands of the guide with page
python -I scripts/rails_lint.py app/controllers/products_controller.rb [--extrapolacoes]
python -I scripts/rails_store_checklist.py APP_PATH        # S01-S30 (read-only)
```
The linter has 17 rules (L01-L17), all with origin and page; L14 and L16 are `[extrapolation]` and only appear with `--extrapolacoes`. Phase names for `--fases` and search terms accept Portuguese or English.

## Verification
```bash
python -I tests/verify_citations.py --src <ROOT>/scratch/frameworks   # 74 positive, 20 negative + range
python -I tests/run_script_tests.py                                   # 36 script tests
```
The cases in `tests/casos-de-teste.md` were run by the author against the agent, references and scripts; **there was no blind run by an independent model**. See `tests/relatorio-de-fidelidade.md`.
