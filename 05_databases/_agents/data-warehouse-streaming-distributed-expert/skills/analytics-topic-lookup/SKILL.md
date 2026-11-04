---
name: analytics-topic-lookup
description: "Finds in the collection (Kimball Dimensional Modeling Techniques and the stream processing survey) on which PDF pages a topic is covered and confirms whether the collection does NOT cover it. Use before citing a page about grain, dimensions, SCD, drill-across, watermarks, state, exactly-once or back-pressure, and when the user asks \"does the collection talk about X?\" (Data Vault, lakehouse, Saga, Flink/Kafka APIs); Portuguese keywords (grão, marca d'água, estado) also work. Do not use to answer the question itself: use the result to cite."
---

# Topic lookup with pages

Sources: KIMBALL (24-page PDF; printed page = N − 3) and STREAM (PDF = printed). Helland has no pages: the collection PDF is a different paper. The index is `../../scripts/analytics_index.json`.

## Procedure

1. Run the query (read-only, no network):
   ```bash
   python -I <PKG>/scripts/analytics_lookup.py "watermark"
   python -I <PKG>/scripts/analytics_lookup.py --list
   python -I <PKG>/scripts/analytics_lookup.py --not-covered
   ```
   (`<PKG>` = package root; from this skill, `../../`.) With no term and no option, the script prints the help and exits with 2.
2. Interpret the output (exit 0 = found or listed; 1 = nothing found; 2 = usage):
   - topic found: use the title, abbreviation and PDF pages and the `../../references/` file indicated; open the file (start with `INDEX.md`) before stating details.
   - "Collection boundary" block or **NOT COVERED** (exit 1): the collection does not cover the subject. Answer as `[extrapolation]` or say "the collection does not cover this". Do not invent a page.
   - "NO PAGES (source absent from the corpus)": this is the Helland case; all content is `[extrapolation]`.
3. Before saying "the collection does not say", Grep the term in `../../references/`.

## Response format

Topic — abbreviation and PDF pages (say that KIMBALL printed = N − 3) — summary — reference file — label of each claim (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`).

## Limits

The index summarizes, it does not replace the text. The survey portrays systems up to 2020-2023 (`[DATED]`). It does not cover relational DBMS internals, NoSQL or graphs.
