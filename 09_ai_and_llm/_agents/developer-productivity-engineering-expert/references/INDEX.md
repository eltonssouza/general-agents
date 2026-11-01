# INDEX: DPE collection (The Developer Productivity Engineering Handbook, Gradle Inc., 2022)

## 1. What the PDF really is (name discrepancy recorded)

The file is named `Data-Platform-Engineering-Handbook-2022.pdf` and sits in the `09_ai_and_llm` folder, but it **is not about data platform engineering** (pipelines, data lakes, ETL, MLOps etc.). The metadata and the title page (DPE p.2, p.6) say:

| Field | Value in the PDF |
|---|---|
| Title | *The Developer Productivity Engineering Handbook: A Complete Guide to Developer Productivity Engineering for Practitioners* |
| Author | Hans Dockter et al. (Dockter is the founder of the Gradle Build Tool and CEO of Gradle Inc.; Gradle Inc. co-authors: p.9-10) |
| Publisher | Gradle Inc. (© 2022; "Version 2.0-local, 2022-03-11"; p.2, p.6) |
| Edition | 2nd major update of a document published in 2019 (p.8) |
| Nature | **Vendor material**: the book promotes Gradle Enterprise (now marketed under another name: `[DATED]`/`[extrapolation]`), Build Scan, Test Distribution and Gradle's ROI calculator (p.8, p.10, p.90) |

The acronym **DPE** in this documentation means *Developer Productivity Engineering*. Whenever the user says "Data Platform Engineering", the agent must correct the premise and declare **NOT COVERED** for data platform engineering.

## 2. Page convention

Every `DPE p.N` citation uses the **PDF page** (the `=== PAGE N ===` marker in the extracted text). The printed page is **N − 5** throughout the body (PDF p.6 = printed 1; PDF p.91 = printed 86). PDF pages 1-5 are a blank cover, title page and table of contents. The book's table of contents uses printed numbering. Use `python -I scripts/dpe_lookup.py --page N` or `--printed N`.

## 3. Chapter map (PDF pages) and reading coverage

Reading: **all 91 pages were read in full** in the extracted text. Pages 30, 74 and 82 were also rendered to check formulas and the cost table. Figures and screenshots (Figs. 1-16, Build Scan and dashboard screenshots) have **no** extractable text; the package only states what the surrounding text says.

| Ch. | Topic | PDF | Printed | Reference file |
|---|---|---|---|---|
| Preface, about the book, authors, introduction | scope, audience | 8-12 | 3-7 | 01 |
| 1 | DPE defined | 14 | 9 | 01 |
| 2 | Intuitive case | 15-18 | 10-13 | 01 |
| 3 | Forming a DPE team | 19-20 | 14-15 | 01 |
| 4 | DPE vs productivity management (DPM) | 21-25 | 16-20 | 01 |
| 5 | Solutions overview | 26 | 21 | 01 |
| 6 | Feedback cycles | 28-33 | 23-28 | 02 |
| 7 | Build cache | 34-42 | 29-37 | 03 |
| 8 | Test distribution | 43-50 | 38-45 | 04 |
| 9 | Profiling and analytics | 51-58 | 46-53 | 05 |
| 10-11 | Failure types and troubleshooting | 60-65 | 55-60 | 06 |
| 12 | Toolchain reliability | 66-69 | 61-64 | 07 |
| 13 | Failure analytics | 70-72 | 65-67 | 07 |
| 14 | Flaky tests | 73-76 | 68-71 | 07 |
| 15 | Build costs | 78-85 | 73-80 | 08 |
| 16 | ROI calculator | 86-90 | 81-85 | 08 |
| Next steps | vendor links | 91 | 86 | 01 |

## 4. When to open each file

| Trigger | Open |
|---|---|
| DPE definition, why, dedicated team, DPM vs DPE, JVM/Android | `01-definicao-caso-e-dpm.md` |
| fast feedback, creative flow, context switching, merge conflict, "shift right" | `02-ciclos-de-feedback.md` |
| build cache, local/remote cache, cache key, modularization, volatile inputs | `03-build-cache.md` |
| test parallelism, CI fanout, test distribution, Jetty case | `04-distribuicao-de-testes.md` |
| MABP vs ABP, instrumentation, percentiles, Build Scan as profiling | `05-profiling-e-analytics.md` |
| verification vs non-verification failure, troubleshooting, comparing builds | `06-falhas-e-troubleshooting.md` |
| reliability, reproducible vs reliable, prioritization, flaky, fix-it day, P_pass formula | `07-confiabilidade-e-flaky.md` |
| build cost, ROI, calculator, 200-engineer example | `08-economia-custo-e-roi.md` |
| promotional claims, what is vendor data, [DATED] | `09-vies-de-fornecedor-e-datado.md` |
| terms | `glossario.md` |
| diagnosis and adoption steps | `procedimentos.md` |
| cases and antipatterns | `casos-e-antipadroes.md` |

## 5. Labels

`[from source]` (checked on the cited page), `[inference]` (direct deduction from the text, e.g. checklist items), `[extrapolation]` (outside the collection; no page), `[DATED]` (something in the 2022 book that has changed or may have changed), `[vendor claim]` (promotional statement or one without a verifiable source in the book).

## 6. Gaps in the book (NOT COVERED)

The book does **not** contain: a formal DPE maturity model; the DORA/SPACE metrics by name; details of generic CI/CD (GitHub Actions, Jenkins config); test strategy (pyramid, TDD); data platform engineering; AI/LLM for productivity; productivity measurement by satisfaction survey. Terms such as "Develocity", "DORA", "SPACE", "platform engineering", "GitHub Actions", "Bazel" or "Copilot" do not appear in the text (see negative checks in `tests/citation-checks.json`). Verify with `python -I scripts/dpe_lookup.py --gaps`.
