# Fidelity report: developer-productivity-engineering-expert

Source: *The Developer Productivity Engineering Handbook* (Hans Dockter et al., Gradle Inc., v2.0-local, 2022-03-11; abbreviated DPE). 91-page PDF; text extracted with `=== PAGE N ===` markers (~181 thousand characters). **Page convention: PDF**; printed = PDF − 5. This report describes what was and what was **not** verified.

## 1. File identity discrepancy
The collection file is named `Data-Platform-Engineering-Handbook-2022.pdf`, but the metadata (title, author), the title page (p.2, p.6) and all the content show a book on **Developer Productivity Engineering** published by **Gradle Inc.**, i.e. **vendor material** that promotes Gradle Enterprise/Build Scan/Test Distribution. There is no data platform engineering content (confirmed by text search: data lake, ETL, Airflow, Spark, Kafka, MLOps, "data platform" have 0 occurrences). The agent was named `developer-productivity-engineering-expert` and declares NOT COVERED for data platforms.

## 2. Honesty about the method
- **Who wrote and who tested:** the same model that read the book built the package and ran all the tests. **There was no blind test by an independent model**: the tables in `casos-de-teste.md` are criteria with the author's self-assessment; "OK" there means the correct answer is derivable from the references and scripts, not that a model was tested.
- **Reading:** full and sequential reading of the 91 pages (extracted text, in blocks of ~700-900 lines), with consolidated notes on disk (`scratch/ai/developer-productivity-engineering-expert/notes/`, outside the package). No subagents. Pages 30, 74 and 82 were rendered (PyMuPDF) to check the formulas and the cost table, per the brief; the other equations are plain text. Figures and screenshots (Figs. 1-16) were **not** interpreted.
- **What the verifier proves and does not prove:** that (a) every `p.N` citation in the package (806 pages cited) falls in the book's valid range (references: 8-91; INDEX/README: 1-91); (b) for 87 positive statements, the terms, names and numbers that the references attribute to those pages **are in fact on them**; (c) for 21 negative statements (DORA, Develocity, Kubernetes, Bazel, data lake, payback, NPV, "formula" on p.86-90 etc.) the terms are **not** on the cited pages. It does not prove that the paraphrase is faithful in every sentence. The positive checks were written from the text that was read (most terms extracted from the pages themselves, some formulas and numbers curated).
- **Independent numeric check of the scripts:** the book's examples were reproduced: CE = 110.400; local waiting 400.000 and CI 100.000; debugging 100.000 + 600.000; build logic 240.000 + 60.000 (with TCI=120); total 3.2 M; Team 2 = 43.8 days (book: 44); Team 3 = 5200 days; flaky: maximum rate 0.0050% without retry and 0.709% with one retry (book: 0.005% and 0.7%).

## 3. Test results (final run)
| Test | Result |
|---|---|
| `tests/run_script_tests.py --src <scratch/ai>` | 45 deterministic cases (lookup 17, calculation 18, checklist 6, index 2, encoding 1, citations 1): **45 passed, 0 failed** |
| `tests/verify_citations.py` | 806 pages cited within range; **87 positive and 21 negative checks, 0 failures** |
| `tests/casos-de-teste.md` | 33 conceptual cases; **not run blind** |

## 4. Errors and inconsistencies found
In the **book** (documented in the references and the agent):
1. **TCI = 90 min** in the "faulty build logic" table (p.82) vs **120 min** used in the calculation (p.83): the CI cost of US$ 60.000 only works out with 120; with 90 it would be US$ 45.000 and the total US$ 285.000 (the example total would go from 3.2 M to 3.185 M).
2. **Team 2: 180 builds per developer** (p.28), but 1010 ÷ 6 ≈ 168.
3. **"Scales exponentially"** (p.29) for examples that scale linearly.
4. **Context-switch formula:** factor 2 (p.30) vs "number of switches" (p.67).
5. **Flaky text vs. formula** (p.74): "product of tests, rate and builds" vs Π(1−P_flaky).
6. "**4.5 engineers** per minute of build growth" (p.79) only works out by adding CI to local.
7. Broken cross-references ("[sec-fragility]", p.44-45) in the text.
In the **package**, fixed during verification:
1. The "Reporting is broken" check was cited on p.45; the text is on p.44 (CI fanout starts on p.44). Fixed.
2. The verifier flagged INDEX p.2 and p.6 as outside the body (8-91); the INDEX correctly cites the title page, so the INDEX range was widened to 1-91.
3. Reference 08 stated that the default of `dpe_cost.py example` uses TCI=90; in fact the default reproduces the book's calculation (120) and warns; text fixed.
4. Test C13 expected "1.00%" for the 0.005%/test rate; the correct result is 0.995% (200 tests); test and label fixed.

## 5. Known limitations
- Figures, charts and screenshots were not interpreted; the references do not assert their content.
- The checklist (50 items) is `[inference]` and the score bands are `[extrapolation]`; the book has no maturity model.
- The retry in the flaky calculation is modeled as p^(r+1) (`[inference]`) from the book's sentence about a "single retry"; the book does not explain its calculation (the 0.7% number is reproduced by this modeling).
- `dpe_cost.py` does not reproduce the online calculator (whose formulas the book does not give); `savings` just applies the p.19/p.24 formula.
- External numbers cited by the book (Google, Facebook, Netflix, TechValidate, IDC) are reported as such and `[DATED]`; they were not verified.
- Antipatterns and procedures are the package's organization (`[inference]`) from the indicated pages.
