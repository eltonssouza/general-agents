# developer-productivity-engineering-expert

**Developer Productivity Engineering (DPE)** specialist agent, built from *The Developer Productivity Engineering Handbook: A Complete Guide to Developer Productivity Engineering for Practitioners* (Hans Dockter et al., Gradle Inc., version 2.0-local, 2022-03-11), abbreviated **DPE**: 91 PDF pages, native text, 16 chapters in 4 parts.

The agent reasons like a productivity engineer: it assesses feedback loops, build cache, test distribution, toolchain profiling, failures, reliability and flaky tests, calculates the cost and ROI of build time and applies a maturity checklist. It cites the page for every rule: `[from source] (DPE p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`, `[vendor claim]`.

## ATTENTION: discrepancy between the file name and the content

The source PDF is in the collection as `09_ai_and_llm/Data-Platform-Engineering-Handbook-2022.pdf`. The name suggests "Data Platform Engineering", but **the content is different**. Checked in the PDF metadata, on the title page and across the whole text (DPE p.2, 6, 8-12):

| Item | What the PDF says |
|---|---|
| Title | *The Developer Productivity Engineering Handbook: A Complete Guide to Developer Productivity Engineering for Practitioners* |
| Author | Hans Dockter et al. (Dockter: founder of the Gradle Build Tool and CEO of Gradle Inc.) |
| Publisher | Gradle Inc., © 2022 (p.6); version 2.0-local, 2022-03-11 (p.2); 2nd major update of a 2019 edition (p.8) |
| Subject | developer productivity: builds, tests, CI, cache, flaky, cost |
| Nature | **vendor material**: promotes Gradle Enterprise, Build Scan and Test Distribution (p.10, 90-91) |

Consequences: (1) **the agent does not cover data platform engineering** (pipelines, data lakes, ETL, MLOps): it answers NOT COVERED; (2) the agent is named `developer-productivity-engineering-expert`; (3) because it is a vendor book, the agent flags promotional claims (50-90% savings with cache, "hard" ROI, Netflix spending 25% of its time on builds, builds 15% slower per year...) as `[vendor claim]`. Suggestion to the collection curator: rename the file to something like `Developer-Productivity-Engineering-Handbook-2022.pdf` and reconsider its placement in the `09_ai_and_llm` folder (the subject is software engineering/DevOps). I did not change the PDF or its name.

## Boundary with other agents
- **General CI/CD, pipelines, build automation:** `cicd-build-automation-expert` (`04_engineering_and_practices/_agents/`).
- **Testing strategy, quality, test frameworks:** `software-testing-qa-expert` (same folder). Here only the DPE angle on slow and flaky tests.
- **NOT COVERED:** data platform engineering, DORA/SPACE, platform engineering, Develocity (later name of the product), GitHub Actions, Kubernetes, Bazel, TDD, AI/LLM for productivity (verified absent from the text; `python -I scripts/dpe_lookup.py --gaps`).

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). Printed page = N − 5 throughout the body (PDF p.6 = printed 1; p.91 = 86); pages 1-5 are the cover, title page and table of contents. Conversion: `python -I scripts/dpe_lookup.py --page N` or `--printed N`.

## What was read (precise statement)
- **Full:** the 91 pages, in the extracted text (~181 thousand characters), plus a visual rendering of p.30, 74 and 82 (formulas and cost table).
- **Not covered:** figures and screenshots (Figs. 1-16, Build Scan dashboards) have no extractable text; the package only asserts what the surrounding text says. The book's equations are in plain text (no complex mathematical notation).
- **The book's own inconsistencies** (flagged by the agent): TCI 90 min (table p.82) vs 120 min (calculation p.83, US$ 60.000 and total US$ 300.000); 180 builds per developer for Team 2 (1010 ÷ 6 ≈ 168, p.28); "scales exponentially" with linear numbers (p.29); factor 2 vs "number of switches" in the context-switch formula (p.30 vs p.67).

## Structure

```
developer-productivity-engineering-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/developer-productivity-engineering-expert.md   # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/developer-productivity-engineering-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # loaded on demand
│   ├── INDEX.md                                # name discrepancy, page convention, chapter map, gaps
│   ├── 01-definicao-caso-e-dpm.md ... 08-economia-custo-e-roi.md, 09-vies-de-fornecedor-e-datado.md
│   └── glossario.md, procedimentos.md (P1-P7), casos-e-antipadroes.md
├── scripts/                                    # Python 3, stdlib, no network, read-only
│   ├── dpe_lookup.py + dpe_index.json          # search by topic/page/chapter; NOT COVERED
│   ├── dpe_cost.py                             # cost/ROI of waiting and debugging; flaky P_pass; 200-engineer example
│   └── dpe_checklist.py + dpe_checklist_items.json   # 50 items, 9 areas, with pages
├── skills/       dpe-topic-lookup, dpe-cost-roi-calculator, dpe-maturity-checklist   # one SKILL.md per entry (skills/<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md                       # 33 conceptual cases
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # 87 positive and 21 negative checks against the text
    ├── run_script_tests.py                     # 45 deterministic cases
    └── fixtures/
```
A copy of the tests is also in `09_ai_and_llm/_agents_tests/developer-productivity-engineering-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point the `developer-productivity-engineering-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/developer-productivity-engineering-expert`, or publish it in your own marketplace.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install developer-productivity-engineering-expert@general-agents`.
- As a standalone agent: copy `agents/developer-productivity-engineering-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@developer-productivity-engineering-expert how much does our 6-minute local build cost?` or let Claude delegate via the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root (Codex merges `AGENTS.md` per directory). `AGENTS.md` points to `agents/developer-productivity-engineering-expert.md` as the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/developer-productivity-engineering-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Using the scripts (run from the package folder)

```bash
python -I scripts/dpe_lookup.py "build cache"
python -I scripts/dpe_lookup.py --page 74
python -I scripts/dpe_lookup.py --gaps
python -I scripts/dpe_cost.py example                          # reproduces the 200-engineer example (US$ 3.2 M/year, p.84)
python -I scripts/dpe_cost.py example --faulty-ci-min 90       # shows the TCI 90 vs 120 inconsistency (p.82-83)
python -I scripts/dpe_cost.py wait --kind local --builds-year 500000 --wait-frac 0.8 --cm 1 --minutes 3
python -I scripts/dpe_cost.py flaky --tests 200 --builds-day 500 --retries 1     # maximum rate per test (p.74)
python -I scripts/dpe_cost.py savings --cost-per-min 1 --builds-year 500000 --build-min 3 --reduction-pct 50
python -I scripts/dpe_checklist.py markdown --area CA
python -I scripts/dpe_checklist.py evaluate tests/fixtures/respostas-exemplo.json
```

## Tests and verification
```bash
python -I tests/run_script_tests.py --src <ROOT>/scratch/ai     # 45 deterministic cases + citation verification
python -I tests/verify_citations.py --src <ROOT>/scratch/ai     # 87 positive and 21 negative
```
`--src` points to the folder that contains `Data-Platform-Engineering-Handbook-2022.txt` (text extracted per page). **No conceptual case was run blind by an independent model**; see `tests/relatorio-de-fidelidade.md`.

## Limitations
Vendor book (pro-instrumentation and pro-acceleration bias), from 2022 (`[DATED]`), centered on JVM/Android; no formal maturity model, no online-calculator formulas and no payback; figures not read. The 50-item checklist and the score bands are creations of the package (`[inference]`/`[extrapolation]`), not of the book. The example values (US$ 1/min, 80% waiting) are illustrative and unsourced.

## Language
The scripts accept Portuguese and English input (lookup terms and the checklist answers `sim|parcial|nao|na` as well as `yes|partial|no|na`). The `references/` folder is still in Portuguese.
