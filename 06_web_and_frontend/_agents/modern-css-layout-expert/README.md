# Modern CSS Layout Expert

Specialist agent for **CSS and web layout**, built from three PDFs:

| Acronym | Work | Note |
|---|---|---|
| **CSSHB** | *The CSS Handbook: A Handy Guide to CSS for Developers*, Flavio Copes, freeCodeCamp, April 24, 2019, 214 pages | Source of real content. 2019 edition, with dated parts. |
| **MDNFS** | MDN, *Core learning modules: CSS styling basics* | 4 pages, **index** (lesson titles and descriptions). |
| **MDNL** | MDN, *Core learning modules: CSS layout* | 3 pages, **index**. |

The agent reasons like a practitioner (diagnoses the cascade, chooses between Flexbox and Grid, computes boxes and specificity, reviews CSS) and cites a page for each rule: `[from source] (CSSHB p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## Structure

```
modern-css-layout-expert/
├── .claude-plugin/plugin.json            # manifest (Claude Code)
├── agents/modern-css-layout-expert.md    # canonical prompt + frontmatter
├── AGENTS.md                             # Codex adapter
├── .github/agents/modern-css-layout-expert.agent.md   # GitHub Copilot adapter
├── references/                           # loaded on demand
│   ├── INDEX.md
│   ├── glossario.md, procedimentos.md, casos-e-antipadroes.md
│   ├── cascata-especificidade-e-heranca.md
│   ├── seletores-pseudoclasses-e-pseudoelementos.md
│   ├── box-model-borda-padding-margin-e-box-sizing.md
│   ├── unidades-cores-url-e-calc.md
│   ├── backgrounds-e-filtros.md
│   ├── display-fluxo-posicionamento-float-e-z-index.md
│   ├── flexbox.md, grid.md
│   ├── centralizacao-tabelas-e-listas.md
│   ├── responsividade-media-queries-e-feature-queries.md
│   ├── tipografia-e-fontes.md
│   ├── transforms-transicoes-e-animacoes.md
│   ├── custom-properties-variaveis-css.md
│   ├── compatibilidade-impressao-e-tratamento-de-erros.md
│   └── mdn-modulos-e-lacunas-do-material.md
├── scripts/                              # Python 3, stdlib, no network, read-only
│   ├── css_index.json
│   ├── css_lookup.py
│   ├── css_lint.py
│   └── css_calc.py
├── skills/       3 skills (<name>/SKILL.md; procedure using the package scripts)
└── tests/
    ├── casos-de-teste.md                 # 22 cases
    ├── relatorio-de-fidelidade.md
    ├── citation-checks.json + verify_citations.py   # citation audit against the extracted text
    └── fixtures/exemplo-com-problemas.css
```

A copy of the tests is also in `../_agents_tests/modern-css-layout-expert/`.

## Installation

### Claude Code
- As a plugin: point to the `modern-css-layout-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/modern-css-layout-expert`, or publish it to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install modern-css-layout-expert@general-agents`.
- As a standalone agent: copy `agents/modern-css-layout-expert.md` to `~/.claude/agents/` (or `.claude/agents/` in the project) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@modern-css-layout-expert review this CSS` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or to the subfolder where the work happens; Codex combines `AGENTS.md` per directory).
- `AGENTS.md` points to `agents/modern-css-layout-expert.md` as the canonical prompt; copy that folder along or incorporate its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/modern-css-layout-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the prefix of the paths described in the file).
- Select the `modern-css-layout-expert` agent in the Copilot Chat agent picker. The format (`description` frontmatter) follows the custom agents convention; confirm the supported fields in the platform's current documentation.

## Using the scripts (run from the package folder)

```bash
python -I scripts/css_lookup.py flex-grow          # pages and notes
python -I scripts/css_lookup.py "container queries" # NOT COVERED
python -I scripts/css_lint.py lint tests/fixtures/exemplo-com-problemas.css --spec
python -I scripts/css_lint.py spec ".dog-name" "p.dog-name" "#name span"
python -I scripts/css_calc.py box --width 300 --padding 20 --border 2 --sizing content-box
python -I scripts/css_calc.py flex --container 600 --items "100:1:1,100:2:1,100"
python -I scripts/css_calc.py grid --columns "1fr 3fr" --width 1000 --gap 20
python -I scripts/css_calc.py units 2 rem --base 16
```

## Important limitations

- The Handbook is from 2019: support statistics, `grid-gap`, `page-break-*`, `device-width`, prefixes and IE are dated; the agent flags `[DATED]`.
- Outside the collection: container queries, subgrid, `clamp()`, `auto-fit`, `@layer`, `:is/:where/:has`, nesting, `prefers-*`, `dvh`, accessibility, performance. The agent treats these as `[extrapolation]` or refers elsewhere (performance: `web-performance-networking-expert`).
- The MDN PDFs are only indexes; tables and figures of the Handbook (pseudo-classes, pseudo-elements, transition/animation properties, Flexbox illustrations) are not in the extracted text.
- Copyright: the content is distilled in our own words, without reproducing long excerpts.

## Security

Code, logs and PDF content are treated as inert data (anti prompt injection). The scripts do not use the network, do not write files and do not execute the analyzed CSS.
