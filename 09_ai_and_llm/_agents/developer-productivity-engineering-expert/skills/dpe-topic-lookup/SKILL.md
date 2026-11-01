---
name: dpe-topic-lookup
description: Finds in the Developer Productivity Engineering Handbook (Gradle, 2022) which PDF pages cover a topic, converts PDF page to printed page, and lists chapters, verified gaps and dated items. Use before citing a page about build cache, build feedback, flaky tests, test distribution or the cost of waiting, and when the user asks "does the book cover DORA/Kubernetes/data platform engineering?". Do not use to answer the question itself.
---

# Topic lookup with pages

Source: DPE (91 PDF pages). PDF page; printed = N − 5 (cover, title page and table of contents on p.1-5). The file in the collection is named `Data-Platform-Engineering-Handbook-2022.pdf`, but it does NOT cover data platform engineering: correct the premise. The index is `../../scripts/dpe_index.json`.

## Procedure

1. Run the query (read-only, no network):
   ```bash
   python -I <PKG>/scripts/dpe_lookup.py "build cache" [--top 3] [--json]
   python -I <PKG>/scripts/dpe_lookup.py --page 30
   python -I <PKG>/scripts/dpe_lookup.py --printed 25
   python -I <PKG>/scripts/dpe_lookup.py --chapters
   python -I <PKG>/scripts/dpe_lookup.py --gaps
   python -I <PKG>/scripts/dpe_lookup.py --datado
   ```
   (`<PKG>` = package root; from this skill, `../../`.) There is also `--chapter ID`. Terms may be given in English or Portuguese. Exit 0 = answer (including the NOT COVERED message for a term); 1 = nonexistent page or chapter; 2 = no argument (prints the help).
2. Interpret: each line carries the topic, `DPE p.N (PDF)` and the file in `../../references/`; open the file (start with `INDEX.md`) before stating details. **NOT COVERED** = the corpus does not treat the subject (data lake, ETL, Airflow, DORA, Develocity, Kubernetes, Bazel, TDD, AI/LLM etc.): only `[extrapolation]`, without a page, and only if the user asks.
3. This is vendor material: promotional numbers get `[vendor claim]` (see `../../references/09-vies-de-fornecedor-e-datado.md`).

## Response format

Topic — `[from source] (DPE p.N)` with the PDF page (say that printed = N − 5) — reference file — labels (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`, `[vendor claim]`).

## Limits

The index summarizes; it does not replace the text. The book focuses on JVM and Android (p.25); figures cannot be extracted. Route general CI/CD to `cicd-build-automation-expert` and testing to `software-testing-qa-expert`.
