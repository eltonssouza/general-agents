---
name: build-book-index
description: Generates and verifies the inverted term-to-pages index (book_term_index.json) from the per-page extracted text of the Google SRE book, and the term index of the references/ summaries (ref_term_index.json). Use when the user asks "check that the term index is up to date", "regenerate book_term_index", or after the PDF extraction or the summaries change. Requires the text with page markers. Do not use to look up topics (that is sre-topic-lookup).
---

# Book term index

Source: the book text extracted per page, with `=== PAGE N ===` markers (PDF pages; printed = N − 12). `sre_lookup.py` uses `../../scripts/book_term_index.json` for the POINTER ONLY level and `ref_term_index.json` for the COVERED level. The JSON stores only terms and page numbers, no book excerpts; it is deterministic (same text, same file).

## Procedure

1. Ask the user for the path of the extracted text; do not invent paths. Always prefer verifying before generating:
   ```bash
   python -I <PKG>/scripts/build_book_index.py --text /path/Google-SRE-Book.txt --check
   python -I <PKG>/scripts/build_ref_index.py --check
   ```
   (`<PKG>` = package root; from this skill, `../../`.) Exit 0 = the versioned JSON matches; 1 = it differs.
2. Only regenerate if the user asks, since this OVERWRITES a package file. To leave the versioned file untouched, point the output elsewhere:
   ```bash
   python -I <PKG>/scripts/build_book_index.py --text /path/Google-SRE-Book.txt --out /tmp/book_term_index.json
   python -I <PKG>/scripts/build_ref_index.py [--refs <dir>] [--out <file>]
   ```
   Without `--out`, the default is `scripts/book_term_index.json` (and `scripts/ref_term_index.json` for the second script).
3. Interpret: the check prints the number of terms, common terms and pages, and the start of the source sha256. After regenerating, suggest running `python -I <PKG>/tests/run_script_tests.py`.

## Response format

Command run — result (OK or FAILURE) — affected file — next step.

## Limits

Depends on the text extracted from the PDF: a different extraction may change the index. The absence of a term from the index does not prove the book does not address it.
