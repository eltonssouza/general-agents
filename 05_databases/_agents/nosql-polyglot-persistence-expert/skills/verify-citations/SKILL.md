---
name: verify-citations
description: Audits the NoSQL package citations (115 positive checks, 22 negative) against the per-page text extracted from the source PDFs. Use when the user asks "verify the package citations", "check that the cited pages match the PDFs" or after editing references/ or scripts/. Do not use to answer content questions and do not run without the extracted .txt files (exit 2).
---

# Package citation audit

The script `../../tests/verify_citations.py` checks the package citations against the text extracted from the PDFs. Convention: N = PDF page. Fidelity details: `../../tests/relatorio-de-fidelidade.md`.

## Procedure

1. Prerequisite: a folder with one `.txt` per source PDF, with `=== PAGE N ===` markers (N = PDF page; PyMuPDF generation described in the script docstring). Expected names: `NoSQL-Databases-Strauch.txt`, `NoSQL-Redis-The-Little-Redis-Book.txt`, `NoSQL-MongoDB-Applied-Design-Patterns.txt`, `NoSQL-MongoDB-Manual-Home.txt`, `NoSQL-MongoDB-Manual-Introduction.txt`, `NoSQL-Cassandra-Overview.txt`, `NoSQL-CouchDB-Introduction.txt`, `NoSQL-Elasticsearch-Guide-Index.txt`, `NoSQL-Neo4j-Graph-Databases-2e.txt`. If the user does not have the texts, say it cannot be run and do not invent a result.
2. Run (read-only, no network):
   ```bash
   python -I <PKG>/tests/verify_citations.py --src FOLDER_WITH_THE_TXT_FILES
   python -I <PKG>/tests/verify_citations.py --src FOLDER_WITH_THE_TXT_FILES -v
   ```
   (`<PKG>` = package root; from this skill, `../../`.) The `--checks` option swaps the checks file (default `citation-checks.json`).
3. Interpret: **positive** checks require all terms to appear on the cited pages of the source (prefix `re:` = regex); **negative** checks require the term not to appear on any page of the listed sources (this guarantees the "not covered" statements). Exit 0 = all passed; 1 = there are failures (list each with the citation and page); 2 = source text missing.
4. A positive failure means a citation to fix in `references/`; a negative failure means a "not covered" statement may be wrong. Report, do not change package files unless asked.

## Response format

Summary (passed/failed per type) — list of failures with source, page and term — probable cause — verifiable next step.

## Limits

It checks the presence of terms on the pages, not the correct interpretation of the text. Complementary: `../../tests/audit_tokens.py`.
