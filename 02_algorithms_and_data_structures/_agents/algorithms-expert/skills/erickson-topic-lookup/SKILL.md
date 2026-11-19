---
name: erickson-topic-lookup
description: Deterministic lookup of topics, algorithms and theorems of the book "Algorithms" (Jeff Erickson, 2019, 472 p.) with PDF pages (printed = PDF − 18). Answers "NOT COVERED" when the book does not treat the subject (Master Theorem, minimax, alpha-beta, König, KMP, etc.). Use before citing a page.
allowed-tools: Bash, Read
---

# Erickson Topic Lookup

Read-only tool, no network, Python 3 (stdlib). The index `scripts/erickson_index.json` was curated from reading the pages and is checked by `tests/verify_citations.py`. Convention: `(JE p.N)` = **PDF** page; printed page = N − 18. Queries are accepted in English or Portuguese (accents ignored).

## Usage
```bash
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py "dijkstra"
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py "subset sum" --chapter 3
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py "master theorem"     # NOT COVERED (the book uses recursion trees); "teorema mestre" also works
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py --list               # chapters, topics and what the book does NOT cover
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py --page 307           # topic and section of the PDF page
python -I skills/erickson-topic-lookup/scripts/erickson_lookup.py --printed 112        # converts printed -> PDF
```

## Output
Topic title (English), kind (topic, algorithm, theorem, section), chapter and `(JE p.N-M)`; caution notes when the book diverges from usual practice. **"NOT COVERED"** (exit code 1) when the topic is on the list of what the book does not treat or when no indexed topic matches; in that case the index may be incomplete — check `references/INDEX.md` before stating that the book does not treat the subject.

## Limits
- The index covers 88 curated topics + 102 table-of-contents sections; it is not a full-text search.
- The script result is a pointer to **where to read**; only mark as `[from source]` what you read on the page.
