---
name: verify-citations
description: Audits the package's curated citations against the text extracted from the PDFs (positive checks of terms per page and negative checks of terms the sources do NOT contain). Use when the maintainer asks "verify the citations", "audit the cited pages" or after editing references/. Do not use to answer end-user questions about CI/CD; it requires the folder with the extracted .txt files.
---

# Citation audit

Convention: `.txt` files with `=== PAGE N ===` markers (N = PDF page). Expected in `--src`: `CICD.txt`, `GRADLE.txt`, `GHA.txt`, `SWEG.txt`. Checks in `../../tests/citation-checks.json`.

## Procedure

1. Run (read-only, no network):
   ```bash
   python -I <PKG>/tests/verify_citations.py --src <folder with the .txt files> [--checks <file.json>] [-v]
   ```
   (`<PKG>` = package root; from this skill, `../../`.)
2. Ask the user for the folder with the `.txt` files if it was not given; do not invent a path.
3. Interpret: positive checks require all the terms on the cited pages; negative checks require that NO term appears (prefix `re:` = regex). Exit 0 = everything passed; 1 = there are failures (list each one).
4. Do not fix `references/` or `tests/` without an explicit request; report the failures.

## Response format

Summary (passed/failed) — list of failures with source, pages and terms — cause hypothesis (wrong page, ligature, missing term) labeled `[inference]`.

## Limits

Verifies the presence of terms, not the meaning of the sentence. Depends on the quality of the PDF text extraction.
