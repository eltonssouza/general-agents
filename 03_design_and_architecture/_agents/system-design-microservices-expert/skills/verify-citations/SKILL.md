---
name: verify-citations
description: Audits the package's "(SIGLA p.N)" citations against the text extracted from the source PDFs (page range, terms present, terms absent, and index terms). Use when the maintainer asks "check the package citations", "verify that the index pages match the PDFs" or after editing references/ or the index. Requires the extracted PDFs; do not use to answer architecture questions.
---

# Package citation audit

Maintenance tool. Package convention: PDF page (1 = first page of the file).

## Procedure

1. Extract the text of the PDFs with `tests/extract_sources.py` (PyMuPDF), generating one `SIGLA.txt` file per work (SAP, SDH, MS-MIC, MS-CLD, MS-WEB, EDS, SBC, SOA, APIGW, JMG, REST) with `=== PAGE N ===` markers. The PDFs do not ship with the package: if the user does not have them, say the audit cannot be done.
2. Run (read-only, no network):
   ```bash
   python -I <PKG>/tests/verify_citations.py --src PATH/src [--pkg PACKAGE_ROOT] [--checks file.json ...]
   ```
   (`<PKG>` = package root; from this skill, `../../`. `--src` is required; `--pkg` defaults to the package that contains the script.)
3. Layers checked: (1) every citation fits within the work's page range; (2) `contains` items in `tests/citation-checks.json` are on the page(s); (3) `absent` items do not appear on the cited pages; (4) each entry in `scripts/sysdesign_index.json` has `cite` and `terms` present on the page.
4. Exit codes: 0 = everything passed; 1 = there are failures (list each one with the page); 2 = incorrect usage (e.g., invalid `--src`).
5. Do not fix citations on your own without rereading the page; report the failures to the maintainer.

## Response format

Layer — failures (citation, file, reason) — total checked — which PDFs/SIGLAs were missing from `--src`.

## Limits

Checks the presence of terms, not the correctness of the paraphrase. Depends on the quality of the PDF extraction (tables as images, such as SDH p.7, cannot be verified by text).
