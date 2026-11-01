# ml-engineering-strategy-expert

Expert agent in **machine learning engineering strategy**, built from *Machine Learning Yearning* (Andrew Ng, deeplearning.ai, © 2018), abbreviated **MLY**: a **draft ("Draft")** of 118 PDF pages with native text and 58 short chapters.

The agent helps decide "what to try next" in a supervised ML project: it defines dev/test sets and the metric, prioritizes ideas through error analysis, diagnoses bias/variance/data mismatch, reads learning curves, uses human performance as a reference, applies the optimization verification test and analyzes error by pipeline component. It cites the page for every rule: `[from source] (MLY p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Warnings:** (1) the book is a **2018 draft**: [DATED]; it does not cover Transformers, LLMs, MLOps, drift, A/B etc. (NOT COVERED). (2) The book **does not fix thresholds** for "high" bias/variance, % of mislabeled data or exact dev size; the scripts make this explicit. (3) It does not replace statistical validation or an ML professional.

## Page convention
**PDF page = printed number** ("Page N"); no offset. Chapter -> pages map in `references/INDEX.md` and `python -I scripts/mly_lookup.py --chapters`.

## What was read (precise statement)
- **In full:** the 118 pages of the extracted text, in 3 sequential blocks.
- **Checked visually (render):** p.32 (spreadsheet), p.62 (curves), p.76 (formula with beta), p.80 (error table).
- **Figures:** curves (p.10-11, 56-62) and pipeline diagrams (p.91-116) have no extractable text; claims about them come from the book's text.
- Intermediate notes: `scratch/ai/ml-engineering-strategy-expert/notes/`.

## Structure

```
ml-engineering-strategy-expert/
├── .claude-plugin/plugin.json
├── agents/ml-engineering-strategy-expert.md       # canonical prompt + frontmatter
├── AGENTS.md                                      # Codex adapter
├── .github/agents/ml-engineering-strategy-expert.agent.md   # GitHub Copilot adapter
├── references/
│   ├── INDEX.md (page convention, coverage, chapter->page map)
│   ├── 00-visao-geral.md ... 09-analise-de-erro-por-partes.md
│   └── glossario.md, procedimentos.md (P1-P8), casos-e-antipadroes.md, datado.md
├── scripts/                                       # Python 3, stdlib, no network
│   ├── mly_lookup.py + mly_index.json             # search; NOT COVERED
│   ├── mly_diagnose.py                            # bias/variance/mismatch, optverify, F1, beta, eyeball
│   ├── mly_errorsheet.py                          # error sheet, ceiling, mislabeled data, attribution by parts
│   └── mly_devtest_check.py                       # dev/test/metric coherence
├── skills/      mly-topic-lookup, mly-bias-variance-diagnose, mly-error-analysis-sheet, mly-devtest-check (each in skills/<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md, relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json
    ├── run_script_tests.py
    └── fixtures/
```
A copy of the tests is also in `../_agents_tests/ml-engineering-strategy-expert/`.

## Installation
**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- Local plugin: `claude --plugin-dir <path>/ml-engineering-strategy-expert`, or publish to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install ml-engineering-strategy-expert@general-agents`.
- Standalone agent: copy `agents/ml-engineering-strategy-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting the paths in the prompt.
- Usage: `@ml-engineering-strategy-expert my training error is 15% and dev is 16%; what should I do?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root; `AGENTS.md` points to the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/ml-engineering-strategy-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>`).

## Script usage (from the package root)
```bash
python -I scripts/mly_lookup.py "learning curve"
python -I scripts/mly_lookup.py transformer                     # NOT COVERED
python -I scripts/mly_diagnose.py bv --train 15 --dev 30 --optimal 14        # avoidable bias 1, variance 15 (MLY p.46-47)
python -I scripts/mly_diagnose.py bv --train 10 --dev 20 --traindev 11 --human 0   # MLY p.79-80
python -I scripts/mly_diagnose.py optverify --pairs "3:1;2:5;4:2"
python -I scripts/mly_errorsheet.py template --cats "Dog,Big cat,Blurry" --rows 100 > errors.csv
python -I scripts/mly_errorsheet.py analyze tests/fixtures/planilha-p32.csv --error-rate 10
python -I scripts/mly_errorsheet.py attribute tests/fixtures/atribuicao.json --order detector,classifier
python -I scripts/mly_devtest_check.py example > cfg.json && python -I scripts/mly_devtest_check.py check cfg.json
python -I tests/run_script_tests.py --src <folder with ML-Machine-Learning-Yearning-Ng.txt>
python -I tests/verify_citations.py --src <folder with ML-Machine-Learning-Yearning-Ng.txt>
```

## Boundaries and limitations
- **Not covered:** Transformers, LLMs, fine-tuning, MLOps/drift/monitoring, A/B tests, fairness/privacy, AUC/calibration, ensembles, k-fold, unsupervised learning (`--gaps`).
- Statistical bias-variance theory, ISLR/ESL and in-depth deep learning: other books in the `09_ai_and_llm` collection.
- **Independent testing:** the cases were run by the package author; there was no blind run by an independent model (`tests/relatorio-de-fidelidade.md`).
- Copyright: content in the package's own words, no extensive reproduction.

## Security
Code, logs, spreadsheets and the PDF are inert data (anti prompt injection). The scripts do not use the network, do not execute user input and do not write files.
