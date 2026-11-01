# INDEX - Machine Learning Yearning (MLY)

**Source:** *Machine Learning Yearning* (Andrew Ng, deeplearning.ai, © 2018). **Draft** ("Draft"), 118 PDF pages with native text, ~159 thousand characters, 58 short chapters. [DATED] 2018 (pre-Transformers). Abbreviation: **MLY**.

## 1. Page convention
**PDF page = printed number** ("Page N" in the footer). There is no offset. Every "MLY p.N" citation uses this number. P.1 has no extractable text, the copyright is on p.2, the table of contents spans p.3-5. Section divider pages (no content): 13, 28, 41, 55, 65, 70, 84, 90, 105, 117.

## 2. Reading coverage (honest)
- **Read in full:** all 118 pages of the extracted text (sequential blocks), all chapters.
- **Checked visually (PyMuPDF render):** p.76 (formula with beta), p.80 (error table), p.62 (curves), and p.32 (spreadsheet).
- **Figures without extractable text:** curves on p.10-11 and 56-62; pipeline diagrams on p.91-116. Statements about figures come from the book's text, not from a detailed reading of the graphs (except p.62).
- Equations: only those for F1 (p.21 note 4) and the beta weighting (p.76) are used in scripts; both were checked on the page.

## 3. Map chapter -> pages -> file
| Ch. | Title (English, from the book) | MLY p. | Reference |
|---|---|---|---|
| 1-4 | Why ML Strategy; How to use; Prerequisites; Scale drives progress | 6-12 | 00-visao-geral.md |
| 5-12 | Dev/test sets, single metric, optimizing/satisficing, iteration, when to change, summary | 14-27 | 01-dev-test-e-metricas.md |
| 13-19 | Fast system, error analysis, spreadsheet, mislabeled examples, Eyeball/Blackbox | 29-40 | 02-analise-de-erro.md |
| 20-27 | Bias and variance, optimum, trade-off, techniques | 42-54 | 03-vies-e-variancia.md |
| 28-32 | Learning curves | 56-64 | 04-curvas-de-aprendizado.md |
| 33-35 | Comparing with human performance | 66-69 | 05-desempenho-humano.md |
| 36-43 | Different distributions, training-dev, mismatch, synthesis | 71-83 | 06-distribuicoes-diferentes.md |
| 44-46 | Optimization Verification Test, RL | 85-89 | 07-depuracao-de-inferencia.md |
| 47-52 | End-to-end, pipelines, rich outputs | 91-104 | 08-end-to-end-e-pipelines.md |
| 53-57 | Error analysis by parts, flawed pipeline | 106-116 | 09-analise-de-erro-por-partes.md |
| 58 | Superhero team | 118 | 00-visao-geral.md |
Full listing: `python -I scripts/mly_lookup.py --chapters`.

## 4. Cross-cutting files
- `glossario.md`: terms from the book and translations.
- `procedimentos.md`: step-by-step procedures (dev/test, error analysis, diagnosis, curves, mismatch, optimization verification, attribution by parts).
- `casos-e-antipadroes.md`: cases from the book and pitfalls.
- `datado.md`: what has changed since 2018 and what the book does not cover.

## 5. Triggers -> file
| Question | Open |
|---|---|
| "how to set up dev/test? size? same distribution?" | 01 |
| "which metric? precision and recall? latency?" | 01 |
| "is this idea worth 1 month? how to prioritize errors?" | 02 |
| "does my model have bias or variance? what to do?" | 03 (+ `mly_diagnose.py bv`) |
| "does more data help? learning curve?" | 04 |
| "how to use human error?" | 05 |
| "training from a different source than test; mismatch; synthetic; weights" | 06 |
| "wrong output: search's fault or the objective's?" | 07 |
| "end-to-end or pipeline? where did the pipeline go wrong?" | 08, 09 |
| "does the book cover transformers/LLM/MLOps/A-B?" | `datado.md`, `mly_lookup.py --gaps` (NOT COVERED) |

## 6. Scripts (stdlib, `python -I`)
`mly_lookup.py`, `mly_diagnose.py` (bv, optverify, f1, weights, eyeball), `mly_errorsheet.py` (template, analyze, mislabeled, attribute), `mly_devtest_check.py` (check, example), index `mly_index.json`.
