---
name: graph-topic-lookup
description: "Locates in the collection of the book Graph Databases (Robinson, Webber, Eifrem, 2015) which PDF pages cover a topic and confirms whether the book does NOT cover it. Use before citing a page about Neo4j, Cypher, IFA, LPG, modeling, internals, transactions, HA or graph theory, and when the user asks \"does the book talk about X?\" (supernodes, Raft, EXPLAIN, GDS, APOC etc.). Do not use it to answer the question itself: use the result to cite."
---

# Topic lookup with pages

Source: NEO4J (238-page PDF; printed page = N − 18). The index is `../../scripts/graph_index.json`; details and fidelity in `../../tests/relatorio-de-fidelidade.md`.

## Procedure

1. Run the lookup (read-only, no network):
   ```bash
   python -I <PKG>/scripts/graph_lookup.py "ifa"
   python -I <PKG>/scripts/graph_lookup.py --list
   python -I <PKG>/scripts/graph_lookup.py --topic storage
   ```
   (`<PKG>` = package root; from this skill, `../../`.) Portuguese and English keywords are both accepted.
2. Interpret the output:
   - topic found: use the title, the PDF pages and the indicated file in `../../references/`; open the file (start with `INDEX.md`) before asserting details.
   - **NOT COVERED** or a `not_in_book` warning ("NOT IN THE SOURCE", exit 1): the book does not cover the subject. Do not invent a page: answer as `[extrapolation]` or say the book does not cover it.
3. Before saying "the book does not say", Grep the term across all files in `../../references/`.

## Response format

Topic — PDF pages (state that printed = N − 18) — summary — reference file — label on each claim (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`).

## Limits

The index summarizes, it does not replace the text. NEO_START (4 pages from a website) has no citable content.
