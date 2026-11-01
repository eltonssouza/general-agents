---
name: build-term-index
description: Generates scripts/source_terms.json, the inverted term-to-pages index, from the text extracted from the sources. Use when the maintainer asks "regenerate the term index" or after replacing the PDFs or the extracted texts. Requires the extracted texts; overwrites the versioned JSON, so do not use it for end-user queries.
---

# Generating the source term index

The index (`../../scripts/source_terms.json`) is the second line of verification of the lookup: it tells POINTER ONLY apart from NOT COVERED without depending only on the curated topics. Pages = PDF pages.

## Procedure

1. Prepare the folder with the extracted texts (`=== PAGE N ===` markers; the same ones used by `tests/verify_citations.py`, produced by `tests/extract_pdfs.py`).
2. Run the generation (deterministic, no network; it only reads the sources):
   ```bash
   python -I <PKG>/scripts/build_term_index.py --src <folder with the .txt files>
   python -I <PKG>/scripts/build_term_index.py --src <folder> --out <PKG>/scripts/source_terms.json
   ```
   (`<PKG>` = package root; from this skill, `../../`.) `--src` is mandatory; `--out` defaults to `scripts/source_terms.json`. Exit 0 = generated.
3. How it is built: normalizes (ligatures, accents, case); tokens `[a-z][a-z0-9_]{2,}` (identifiers with `_` are kept whole and split); simple plural removed; common terms (above a per-source frequency threshold) keep no pages; pages are written as ranges. The JSON records `generator` and `fingerprint`.
4. After regenerating, run `python -I <PKG>/scripts/build_ref_index.py` only if you edited `references/` (it generates `ref_terms.json`), and run the audit of the verify-citations skill. The index is textual, with no semantics: do not present it as `[from source]`.

## Response format

Source folder — generated file — number of terms/sources — result of the follow-up audit.

## Limits

It overwrites a versioned file: confirm with the maintainer before running and review the diff afterwards. Without the extracted texts it cannot be generated.
