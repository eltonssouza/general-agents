---
name: sre-topic-lookup
description: "Three-level lookup (COVERED, POINTER ONLY, NOT COVERED) of which pages of the Google SRE book PDF address a topic. Use before citing a page on SLO, error budget, toil, on-call, postmortem, cascading failures or consensus, and when the user asks \"does the book talk about burn rate/circuit breaker/DORA?\". Do not use to answer the question itself: use the result to cite. It does not prove absence when it says it found nothing in the index."
---

# Topic lookup with pages, in three levels

Source: SRE (347 pages); PDF page, printed = N − 12. Indexes: `../../scripts/sre_index.json`, `book_term_index.json` (book terms) and `ref_term_index.json` (terms of the `../../references/` summaries).

## Procedure

1. Run the query (read-only, offline):
   ```bash
   python -I <PKG>/scripts/sre_lookup.py "error budget"
   python -I <PKG>/scripts/sre_lookup.py --list
   python -I <PKG>/scripts/sre_lookup.py --topic toil
   python -I <PKG>/scripts/sre_lookup.py --pages "etcd"
   python -I <PKG>/scripts/sre_lookup.py "retry" --max 5
   ```
   (`<PKG>` = package root; from this skill, `../../`.) `--check` verifies keyword consistency (exit 1 on failure).
2. Interpret by exit code:
   - **COVERED** (exit 0): the term is in the body of a package summary that cites a page. Cite it and open the file in `../../references/` (start with `INDEX.md`) before asserting details.
   - **POINTER ONLY** (exit 3): the book has the term on the pages shown, but the package does not summarize it. Say so and do not invent content.
   - **NOT COVERED** (exit 1): (a) term from the curated list of things outside the book: only then can you say "the book does not cover this" (`[extrapolation]` if you answer); (b) "not found in the index": does not prove absence; check spelling, plural and English with `--pages` and read the page before denying.
   - exit 2: incorrect usage. Ambiguous terms (flow, shadow, dns, config) come with an ALERT block listing the senses.
3. Label: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]` (Borgmon, Borg, Chubby, 2016 numbers).

## Response format

Topic — level (COVERED, POINTER ONLY or NOT COVERED) — PDF pages (printed = N − 12) — summary — reference file — labels.

## Limits

The index summarizes, it does not replace the text. Does not cover modern observability, DORA, security or Kubernetes (other packages).
