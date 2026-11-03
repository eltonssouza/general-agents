---
name: morin-topic-lookup
description: Looks up topics, structures and pages in Open Data Structures (Morin, Edition 0.1Gβ, 326 pages) using a JSON index (the PDF table of contents plus curated topics in English and Portuguese). Terms the book does not use (tombstone, primary clustering, 2-independent, real-time) return NOT COVERED.
allowed-tools: Bash, Read
---

# morin-topic-lookup

Deterministic, read-only tool with no network access. Pages = PDF (printed = N − 12); the pages of the book's subject index are printed numbers.

```bash
python -I skills/morin-topic-lookup/scripts/morin_lookup.py "treap"
python -I skills/morin-topic-lookup/scripts/morin_lookup.py "linear" --chapter "Hash Tables"
python -I skills/morin-topic-lookup/scripts/morin_lookup.py "del"
python -I skills/morin-topic-lookup/scripts/morin_lookup.py "tombstone"      # NOT COVERED (exit 1)
```

## Output
`[toc]` lines (table-of-contents section, starting page) and `[topic]` lines (curated topic, page range). Cite in answers as `[from source] (ODS p.N)` only with the printed page shown in the output. `NOT COVERED` means the book does not use the term or does not cover the topic: label it `[extrapolation]`.
The index was generated from the PDF table of contents (143 of 145 entries checked automatically; Bibliography and Index corrected to p.313 and p.321) and the curated topics were checked by reading; `tests/run_script_tests.py` repeats the check.
