---
name: java-jdk-features
description: Answers "in which JDK did X ship?" and "what does JDK N bring?" from the JEP list in the OpenJDK 11, 17, 21, 22 and 26 release notes (number and title only, no description). Covers sealed classes, pattern matching for switch, record patterns, virtual threads, FFM API, structured concurrency, scoped values, string templates, Vector API and others; reports what the pages say about LTS and declares which JDKs have no source. Use when the user asks for a feature's minimum version, what is in JDK 21/22/26, whether a JDK is LTS or to compare versions. Do not use to explain how a feature works (the sources do not describe it), nor for JDK 9, 10, 12–16, 18–20, 23–25 or above 26 (no source).
---

# Features by JDK (sources: OpenJDK 11, 17, 21, 22, 26 release notes)

Full table in `../../references/versoes-e-datado.md`. The data comes **only** from the "Features" section of each page: JEP number, title and GA date. **No page describes what a JEP does.**

## Procedure

1. **Find out the user's JDK** (or the target). Without it, answer conditionally.
2. **Query the index** (read-only, no network):
   ```bash
   python -I scripts/jdk_lookup.py "virtual"
   python -I scripts/jdk_lookup.py sealed
   python -I scripts/jdk_lookup.py --jdk 21
   python -I scripts/jdk_lookup.py --coverage
   ```
   Several terms mean "all must match"; a number is treated as a JEP number.
3. **Answer with JDK + JEP + title**, as they appear, and the state the **title** indicates (Preview, Second Preview, Incubator…). Cite `(RN JDK N)`.
4. **A title without a mark does not prove it is final**: say "no Preview mark in the title" and treat "final" as **[inference]**.
5. **Do not describe the feature** (how it works, syntax, motivation) as if it came from the sources. If you explain from your own knowledge, label it **[extrapolation]** and recommend checking the user's JDK documentation.
6. **A feature with no JEP on the pages** (for example `record` as a class, `var`, text blocks, switch expressions, streams, modules): answer **"version not stated in the sources"** — do not say it does not exist, and do not state the version from memory without a label. The script warns that "no result" does not mean nonexistence.
7. **LTS**: only what the pages say counts. The JDK 17 page states LTS and calls 11 the "previous LTS release"; the JDK 21 page states LTS and calls 17 the "previous LTS". The 11, 22 and 26 pages say nothing about LTS; there is no JDK 25 page. Any other claim is **[extrapolation]**.
8. **JDKs with no page** (9, 10, 12–16, 18–20, 23–25, >26): say the sources do not cover them. A feature that appears as Preview in JDK 21 may have changed state in JDKs you cannot consult.

## Recurring families (examples from the table)

Structured Concurrency (Preview in 21, Second Preview in 22, Sixth Preview in 26), Vector API (Second Incubator in 17, Sixth in 21, Seventh in 22, Eleventh in 26), FFM API (Incubator in 17, Third Preview in 21, no mark in 22), Pattern Matching for switch (Preview in 17, no mark in 21), Scoped Values and String Templates (Preview in 21, Second Preview in 22).

## Response format

Feature → JDK(s) and JEP(s) with title and the title's state → what the sources do **not** say → version gaps. Never list "news" for JDKs without a page.

## Limits

- The sources are OpenJDK status pages; they may have been updated since (the JDK 26 one is from 2026).
- The books (Java 7/8) and the handbook (PermGen) are from earlier eras; they do not fill the gaps of JDKs 9–10 and 12–25.
