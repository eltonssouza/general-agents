# statistical-learning-expert

Specialist agent in **statistical learning**, built from two books in the collection:

- **ISLR**: *An Introduction to Statistical Learning with Applications in R* (James, Witten, Hastie, Tibshirani), **1st edition** (© 2013, "Corrected 8th printing 2017"), 441 PDF pages, 10 chapters, **R labs `[DATED]`**. The entry point.
- **ESL**: *The Elements of Statistical Learning* (Hastie, Tibshirani, Friedman), **2nd edition** ("Corrected 12th printing, Jan 13, 2017"), 764 PDF pages, 18 chapters. The in-depth version.

The agent organizes references by topic (bias-variance, linear regression, classification, resampling, selection and regularization, non-linearity, trees/ensembles, SVM, unsupervised learning, high dimensions and multiple testing, one-hidden-layer neural networks), documents **where the ESL goes deeper than the ISLR with the pages of both books** and cites the page in each rule: `[from source] (ISLR p.N)` or `(ESL p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Warning:** it does not replace validation on your dataset; no rule from the books is a theorem. The ISLR 1st ed. has **no** deep learning, survival analysis or multiple testing; the ESL (2009) does not cover modern deep learning, LLMs, XGBoost, SHAP, etc. (NOT COVERED). The ISLR code labs are in R from 2013-2017 and must **not** be treated as current.

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). **Printed ISLR = PDF − 15** and **printed ESL = PDF − 19** (uniform offsets). Conversion: `python -I scripts/slr_lookup.py --printed ISLR 175` (→ PDF 190) or `--page ESL 249`.

## What was read (precise statement)
Neither book was read in full; reading was by chapter with notes on disk (`scratch/ai/statistical-learning-expert/notes/`), outside the package.
- **ISLR**: main text of chs. 2-10 read (ch. 1 by sampling). **R labs and exercises not read.**
- **ESL**: read ch. 2 (2.3-2.9), much of ch. 7, excerpts of chs. 3, 4, 8 (8.7-8.8), 9 (9.2 trees), 10 (almost all), 11 (model and backpropagation), 12 (SVM, in part), 14 (K-means, hierarchical, PCA), 15 (random forest, in part) and 18 (18.1-18.2 and 18.7). **Not read**: chs. 1, 5, 6, 13, 16, 17 and parts of the others.
- Per-chapter detail in `references/INDEX.md` §3 and `python -I scripts/slr_lookup.py --coverage` / `--gaps`.

## Structure

```
statistical-learning-expert/
├── .claude-plugin/plugin.json                         # manifest (Claude Code)
├── agents/statistical-learning-expert.md              # canonical prompt + frontmatter
├── AGENTS.md                                          # Codex adapter
├── .github/agents/statistical-learning-expert.agent.md  # GitHub Copilot adapter
├── references/                                        # loaded on demand
│   ├── INDEX.md                                       # page convention, coverage per chapter, when to open each file
│   ├── 01 to 11: topic references; 12: ISLR⇄ESL map (pages of both); 13: method-selection guide;
│   │   14: R labs [DATED]
│   └── glossario.md, procedimentos.md (P1-P7), casos-e-antipadroes.md, datado-edicoes.md
├── skills/                                            # slr-topic-lookup, slr-calculators, slr-method-guide (SKILL.md per folder)
├── scripts/                                           # Python 3, stdlib, no network, read-only
│   ├── slr_lookup.py + slr_index.json                 # search by topic/page/chapter; ISLR⇄ESL map; NOT COVERED
│   ├── slr_calc.py                                    # calculators (formulas checked on the pages)
│   └── slr_guide.py + slr_guide.json                  # method-selection guide (52 rules with pages)
└── tests/
    ├── casos-de-teste.md                              # 38 cases (conceptual, practical, edge, out of scope, injection)
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json     # 260 positive and 27 negative checks against the extracted text
    ├── audit_numbers.py                               # heuristic audit of numbers in the references
    ├── check_case_citations.py                        # checks that the expected pages of the cases are in the references
    ├── run_script_tests.py                            # 72 deterministic cases (with --src it includes the verifications)
    └── fixtures/
```
A copy of the tests is also in `../_agents_tests/statistical-learning-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point the `statistical-learning-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/statistical-learning-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install statistical-learning-expert@general-agents`.
- As a standalone agent: copy `agents/statistical-learning-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@statistical-learning-expert which method should I use with n = 80 and p = 2000?` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root (Codex combines `AGENTS.md` per directory). `AGENTS.md` points to `agents/statistical-learning-expert.md` as the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/statistical-learning-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Using the scripts (run from the package folder)

```bash
python -I scripts/slr_lookup.py lasso                       # where ISLR and ESL cover the topic (PDF pages)
python -I scripts/slr_lookup.py --map boosting              # where the ESL goes deeper than the ISLR
python -I scripts/slr_lookup.py "deep learning"             # NOT COVERED (with occurrence count)
python -I scripts/slr_lookup.py --printed ISLR 175          # printed -> PDF
python -I scripts/slr_calc.py criteria --rss 100 --n 50 --d 3 --sigma2 2 --tss 400   # Cp/AIC/BIC in both conventions
python -I scripts/slr_calc.py confusion --tp 81 --fp 23 --fn 252 --tn 9644
python -I scripts/slr_calc.py multtest bh --pvalues "0.001,0.008,0.039" --alpha 0.05
python -I scripts/slr_guide.py recommend --goal prediction --response binary --n 80 --p 2000
```
Negative arguments in `--option` need `=` (e.g., `--mu=-1.25,1.25`). Queries to `slr_lookup.py` work in English and Portuguese (e.g., `validacao cruzada`).

## Verification
```bash
python -I tests/run_script_tests.py --src <ROOT>/scratch/ai    # 72 cases; includes verify_citations and audit_numbers
python -I tests/verify_citations.py --src <ROOT>/scratch/ai    # requires the per-page extracted texts
python -I tests/check_case_citations.py
```
Without the extracted texts (`--src`), only the script cases run. **There was no blind run by an independent model**: the cases in `casos-de-teste.md` were run by the package author itself (see the report).

## Copyright
The references paraphrase; no long excerpts, tables or figures are copied. Verbatim quotes only short (< 15 words) and rare. Do not copy the labs.
