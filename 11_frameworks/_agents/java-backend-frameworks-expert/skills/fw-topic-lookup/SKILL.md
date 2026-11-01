---
name: fw-topic-lookup
description: Locates the PDF pages where a topic is addressed in the package's three sources (Mastering Spring Boot 3.0, Quarkus Serverless Refcard and MapStruct 1.6.3 Reference Guide), and lists the topics that are NOT COVERED. Use before citing a page about Spring Boot, JPA, security, tests, Quarkus serverless or MapStruct, and when the user asks "does the source talk about Resilience4j/Flyway/custom starter?". Do not use to answer the question itself: use the result to cite.
---

# Topic lookup with pages

Sources: SB3G (256 pp.; printed = PDF − 19 in the chapters), QRK (9 pp., Quarkus serverless 2.x only; p.2 is an ad) and MPS (96 pp., no printed numbering). Pages = PDF. The index is `../../scripts/fw_index.json`.

## Procedure

1. Run the query (read-only, no network):
   ```bash
   python -I <PKG>/scripts/fw_lookup.py "cache" [--source SB3G|QRK|MPS] [--top 6] [--json]
   python -I <PKG>/scripts/fw_lookup.py --page 104 --source SB3G
   python -I <PKG>/scripts/fw_lookup.py --sources
   python -I <PKG>/scripts/fw_lookup.py --gaps
   ```
   (`<PKG>` = package root; from this skill, `../../`.) `--page N` requires `--source`. Exit 0 = answer; 1 = page outside the source's range; 2 = `--page` without `--source`.
2. Interpret: each line gives the topic, source, pages and the file in `../../references/`; open the file (start with `INDEX.md`) before asserting details. For a page, the script warns if it is blank, promotional or has no indexed topic.
3. **NOT COVERED** (`--gaps`): extensive official Spring Boot reference (refer to `spring-boot-reference-expert`), Spring Boot 3.3+, custom starters, Quarkus beyond serverless, Quarkus vs Spring benchmark, Resilience4j, Flyway, Redis/Caffeine, Helm, advanced Kafka. Answer only as `[extrapolation]` and only if requested. Internal divergences in the sources (Java 11 vs 17 in SB3G) are in `../../references/00-fontes-e-lacunas.md`.

## Response format

Topic — `[from source] (SB3G p.N)`, `(QRK p.N)` or `(MPS p.N)` — reference file — labels (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`).

## Limits

The index summarizes, it does not replace the text. SB3G is not the official Spring Boot reference; QRK is vendor material; everything is `[DATED]` (2021-2024).
