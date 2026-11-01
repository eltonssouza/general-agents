---
name: verify-citations
description: Audits the package's page citations against the Google SRE book text extracted from the PDF, with positive checks (terms on the cited page), negative checks (terms the book does not contain) and per-page negative checks. Use when the user asks "verify the package citations", "do the pages still match?" or after swapping the PDF extraction. Requires the text with page markers. Do not use to look up topics (that is sre-topic-lookup).
---

# Citation audit

Source: `../../scripts/citation-checks.json` (identical copy in `../../tests/`); PDF pages (printed = N − 12). Positive: all terms must appear, on any of the cited pages. Negative: no term may appear on any page (prefix `re:` = regular expression). Per-page negative: guard against an already-fixed wrong page.

## Procedure

1. Ask the user for the path of the extracted text (markers `=== PAGE N ===`); do not invent paths. Run (read-only, offline):
   ```bash
   python -I <PKG>/scripts/verify_citations.py --text /path/Google-SRE-Book.txt -v
   python -I <PKG>/scripts/verify_citations.py --text /path/Google-SRE-Book.txt --checks other-citation-checks.json
   ```
   (`<PKG>` = package root; from this skill, `../../`.) `--text` is required; `-v` also lists the ones that passed. Exit 0 = all passed; 1 = there are failures.
2. Interpret: each `FAIL` carries the id, the pages, the claim and the missing terms (positive) or where the term appeared (negative). The summary gives positives, negatives and failures.
3. Do not fix citations on your own: report the failure, open the page in `../../references/` and propose the fix to the user.

## Response format

Summary (positives, negatives, failures) — list of failures with id and probable cause — next step.

## Limits

Checks the presence of terms on the page, not the truth of the claim. Depends on the quality of the PDF text extraction.
