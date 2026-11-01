# Fidelity and audit report: relational-dbms-internals-expert (v1 -> v2)

- **Scope**: audit of the v1 package (never audited before) and production of v2. Page convention adopted: **PDF** (`=== PAGE N ===` markers of the text extracted with PyMuPDF). Printed ARCH = PDF + 140; printed PG16 = PDF − 38 (verified on 3,011 pages); printed ANTI-INT = PDF − 4.
- **Method**: (1) inventory and full extraction of the 7 PDFs; (2) backup of v1; (3) automatic audit (extraction of all citations, page range, terms between backticks, curated positive and negative checks); (4) manual audit by reading the cited pages (82 claims of v1); (5) rewrite; (6) tests. **There was no blind run by an independent model** (see section 8).

## 1. Sources: what each PDF really contains
| Sigla | PDF | Pages | Complete? |
|---|---|---|---|
| ARCH | Architecture-of-a-Database-System | 119 | Yes (complete paper, printed 141-259) |
| PG16 | PostgreSQL-16-Docs | 3,057 | Yes (complete 16.15 manual; v1 said "341 canonical pages", unsupported) |
| REDBK | Readings-in-Database-Systems-RedBook-5th | 46 | **No**: only the chapter introductions, out of order (v1 cited "REDBK p.12-18" for write skew/SSI; in the PDF p.10-13 is data integration) |
| ANTI-INJ | SQL-Antipatterns-injection-chapter | 14 | **Excerpt**: content on p.5-14; without section 21.5 "Solution" |
| ANTI-TREE | SQL-Antipatterns-trees-chapter | 11 | **Excerpt**: content on p.5-11; without section 3.5 (alternative models) |
| ANTI-INT / ANTI-TOC | introduction-chapter / toc-chapter | 14 / 9 | Excerpt of ch. 1; table of contents only |
The other PDFs in `05_databases` belong to other agents.

## 2. Page convention of v1
**Inconsistent.** The numbers were "plausible", with no systematic relation to the PDF: for ARCH they match neither the PDF page nor the printed one (e.g., "2PL, ARCH p.55-62": in the PDF p.53-62 is access methods and data warehouses; the transactions section is p.78-99). For PG16 they looked like approximate printed pages of chapters (indexes "p.420-445" ~ printed 429-445, which in the PDF is the functions and operators chapter; internals "p.2450-2515" ~ printed 2450-2527, which in the PDF is NLS and the access method interface), without the offset of 38 and often in the wrong chapters ("MVCC, PG16 p.461": PDF p.461 is type conversion; MVCC is on p.525-531; "VACUUM p.810-835": PDF p.810-835 is backup/restore and high availability/replication; VACUUM is on p.788-798). v2 redid **all** the pages and declares the convention in `INDEX.md`, in the prompt, in the three adapters and in the scripts.

## 3. Results of the v1 audit
### 3.1 Automatic (on the v1 files)
| Metric | Result |
|---|---|
| Citations extracted (agent, 14 references, scripts, INDEX) | **405** (ARCH 143, PG16 171, ANTI-TREE 40, ANTI-INJ 37, REDBK 14) |
| Outside the page range | 0 (the range check does not detect content errors) |
| Wide ranges (> 12 pages) | **36** (e.g., PG16 p.420-835, 416 pages; PG16 p.420-890, 471 pages) |
| Terms between backticks checked against the cited page | 88 |
| FAIL (term absent from the cited page and the neighboring ones) | **66 (75%)** |
| NEARBY (only on a neighboring page) | 8 |
| OK | 14 |

### 3.2 Manual: 82 claims of v1 compared with the cited page and with the real page (full table in `scratch/audit/relational-dbms-internals-expert/notes/manual_audit.md`; covers 13 of the 14 reference files; the glossary repeats claims from the others)
| Classification | Count |
|---|---|
| OK | 1 |
| Wrong page (content supported on another page) | 35 |
| Claim unsupported or contradicted by the source | 29 |
| Overstatement / partial | 17 |

### 3.3 Relevant examples of what was unsupported (all written in v1 as `[from source]`)
1. "ARIES with Dirty Page Table, CLR and `UndoNextLSN`" attributed to ARCH p.70-78: ARCH only refers to the paper (p.88) and the Red Book summarizes three phases (REDBK p.18).
2. "Closure Table is the solution recommended by Karwin" (ANTI-TREE p.8-11) and descriptions of Path Enumeration and Nested Sets: the excerpt ends on p.11, **before** the solution; only the title exists in the table of contents (ANTI-TOC p.5).
3. "CLOCK solves cache pollution from Seq Scan" (ARCH p.51-54): ARCH p.75 says that LRU and CLOCK **do poorly** on this pattern.
4. "`autovacuum = off` leads to a forced shutdown and requires single-user mode" (PG16 p.816-821): the manual says the system refuses new XIDs below 3 million and that single-user mode is **not** necessary (PG16 p.794-795); the prevention vacuum runs even with the daemon turned off (p.702).
5. "Prepared statements are the only definitive defense" (ANTI-INJ p.6-10): the book says **no single technique** is enough (p.8) and that parameters are not universal (p.10-11). The allow-list "canonical Karwin solution" is not in the excerpt.
6. "A 100 GB B-tree uses 20 GB, BRIN less than 10 MB (99.9%)" and "256 KB to 16 MB ring for Seq Scan" (PG16 p.435, p.815-820): nonexistent numbers; PG16's ring is for VACUUM/ANALYZE (p.655).
7. "Write skew and SSI in REDBK p.12-18": the Red Book (introductions) carries neither SSI nor write skew; the term does not exist in ARCH, REDBK or PG16.
8. "SQL Server is thread per user": ARCH says the default is a thread pool (p.22); "PgBouncer and 500-1000 connections": absent from the sources.
9. "Cost formula = pages × I/O + tuples × CPU", "Grace Hash Join" and join complexities "from the book": they are not in ARCH (PG16 describes the three joins on p.2294, without complexities).

### 3.4 v1 scripts (actually run)
- `injection_auditor.py`: **false "COMPLIANT/SAFE"** for `cur.execute('... %s' % x) -- ts::int` (the regex `:\w+` treated `::int` as a parameter); remediation with `$1` in psycopg code; it attributed the use of an allow-list to "Karwin's prescription"; emojis in the output.
- `index_advisor.py`: unreachable Hash branch (`hash_equality_only` outside the `choices`), `temporal_log` not handled, invented "99%", wrong pages, no origin declared for the 10 GB threshold.
- `tree_evaluator.py`: attributed to Karwin three models that the excerpt does not carry, with "Critical/Very High" costs without a source, and the recommendation as fact.
- `relational_lookup.py`/`relational_index.json`: invented page lists (e.g., `[65, 66, 68, 70, 72, 75]`), "closure table" topic "covered", no "NOT COVERED".
- Structure: README without installation on the 3 platforms, no AGENTS.md or `.github/agents`, prompt without a response-format or boundary section, no citation verifier or script tests.
- Encoding: no BOM or mojibake; the v1 README carried an absolute user path (removed).

## 4. What was fixed in v2
- **14 references rewritten** (same file names) with checked PDF pages; unsupported claims were removed, corrected with what the text says or downgraded to `[inference]`/`[extrapolation]`; coverage warnings in the files about trees and SQL injection; a "What the sources do NOT say" section in each.
- `INDEX.md` with a source inventory (complete vs. excerpt), convention, chapter map of ARCH/PG16/REDBK and boundary.
- **Prompt** (`agents/*.md`) with page convention, 4 labels, 8 corrections of frequent premises, boundary, [DATED] content, when to consult real references/scripts, anti prompt-injection and response format.
- **Scripts**: `relational_index.json` redone (43 topics, verified pages, 16 terms "outside the sources"); `relational_lookup.py` with NOT COVERED (exit 1); `index_advisor.py`, `tree_evaluator.py`, `injection_auditor.py` rewritten with a **declared origin for each rule** and labels; the auditor never declares "safe", detects `%`, `.format`, `+`, `${}`, PHP and incorrect parameter use (IN, ORDER BY, FROM, ASC/DESC), and has a regression test for the `::int` false negative.
- **Structure**: README with installation (Claude Code, Codex, GitHub Copilot) and a warning to check the current documentation; `AGENTS.md`; `.github/agents/relational-dbms-internals-expert.agent.md` (valid YAML frontmatter, `<PKG>` paths); `plugin.json` 2.0.0.
- **Tests**: `verify_citations.py` + `citation-checks.json`, `audit_tokens.py`, `extract_pdfs.py`, `run_script_tests.py`, 28 cases in `casos-de-teste.md`.

## 5. v2 results (executed)
| Check | Result |
|---|---|
| `verify_citations.py`: curated checks | **156 positive, 22 negative, 0 failures** |
| `verify_citations.py --audit-ranges` | 807 citations extracted (ARCH 177, PG16 475, ANTI-INJ 76, ANTI-TREE 37, REDBK 36, ANTI-TOC 5, ANTI-INT 1): **0 out of range**, 3 warnings (ARCH p.9-24 = whole section 2, declared) |
| `audit_tokens.py` (terms between backticks in the references) | 219 checked, 0 NEARBY, **0 FAIL** (the first round found 8 slips of mine, already fixed: bracketed labels treated as terms, `servidor.banco...` instead of `server.database...`, two citations on a neighboring page and three terms cited on the wrong page) |
| `run_script_tests.py --src` | 25 script cases + 2 verifiers, **0 failures** |
| Reproducibility | `extract_pdfs.py` regenerates the .txt files; the tests pass on the re-extracted text |
While building the 178 checks the verifier itself flagged 10 initial failures (term on the wrong page or with a line break/quotes), which were fixed; one negative check flagged a false positive due to comparison without spaces on short terms, which led the verifier to use that tolerance only for terms of 12+ characters.

## 6. Audit coverage (what was and was not audited)
- **PG16 (3,057 pages)**: text **fully extracted**; audit by declared **stratified sampling**. Strata read in full: Ch. 11 Indexes (p.467-482), Ch. 13 Concurrency (p.525-533), Ch. 25.1-25.3 Maintenance/VACUUM (p.788-798), Ch. 30 WAL (p.896-902), Ch. 72-73 Hash and Physical storage (p.2565-2577), 71.1 and 70.4-70.5 (BRIN/GIN, p.2548-2553), 67.4 (p.2512-2513), Ch. 52 (p.2291-2294), 7.8 (p.173-177), JSON/GIN (p.223-225), libpq (p.971-972, p.984-985), PL/pgSQL EXECUTE (p.1363-1365), 20.4/20.5/20.7/20.10 (p.653-659, p.662, p.682-683, p.702-704), EXPLAIN (p.546-547), statistics (p.554), 14.5 (p.563), partitioning (p.132-133), `pg_stat_all_tables` (p.868-869), `pg_buffercache` (p.2885), CREATE INDEX (p.1758). In addition, **searches across the whole PDF** for each negative term (write skew, dangerous structure, PgBouncer, forced shutdown, undo log etc.). The package cites **121 distinct PG16 pages (4.0%)**; all pass `audit_tokens`/checks, 72 have a positive curated check. **Not audited**: ~96% of PG16 (SQL reference, replication, security, release notes, etc.), which the package does not cite.
- **ARCH**: read in full, **except p.61-69** (end of the data warehouse section and sections 4.7-4.9) and the bibliographic references (p.113-119). 94 of 119 pages cited; 62 with a curated check.
- **REDBK**: p.14-22 and p.28-36 (chapters 2, 3, 4, 6 and 7) and the beginning of chapter 1 read in full; chapters 5, 8, 9, 10, 11 and 12 (p.3-13, p.23-27, p.37-46) **not read**; the package cites only p.2, 14-18, 21-22, 28-29, 33-35 (12 pages). The PDF does not contain the papers, only the introductions.
- **SQL Antipatterns**: the 4 excerpts were read in full. The content that the full book carries and the excerpt does not (solutions) is **outside** what the package can attribute.
- **Not verified**: no SQL from `procedimentos.md` was run on a real PostgreSQL; behavior of versions later than 16.15 was not evaluated.

## 7. Limitations and honesty
- The manual audit compares claims with pages read by **one auditor** (the same one who rewrote the package); the automatic verifiers reduce, but do not eliminate, the bias.
- The positive checks verify the presence of terms on the page, not the full truth of the sentence; hence the complementary manual reading.
- The `[inference]` and `[extrapolation]` labels are the auditor's judgments; the BRIN threshold (10 GB) and the injection auditor's regexes are declared `[extrapolation]`.

## 8. Blind test
**There was no blind run by an independent model.** The 28 cases of `casos-de-teste.md` were derived from the references and checked against the pages and the scripts; they measure the package's consistency, not the answer of a model that has not seen the material. As a pending item, a blind round is recommended: give the questions to a model with the agent installed and compare with the "Expected answer" column.

## 9. Pending items
1. Blind round by an independent model.
2. Run the SQL of `procedimentos.md` on PostgreSQL 16.
3. Obtain the full chapter of "Naive Trees" (section 3.5) and of "SQL Injection" (section 21.5), if the agent needs to treat Path Enumeration, Nested Sets, Closure Table and allow-list as `[from source]`.
4. Obtain the full Red Book papers, if the agent needs ARIES/Selinger in detail `[from source]`.
5. Read ARCH p.61-69 and the other PG16 chapters if the agent's scope grows.

## 10. Fixes after the blind test (round 1)
Origin: independent blind evaluation (14 cases, provisional approval, average correctness 2.93; 84/85 citations OK, 1 overstatement). Each fix was confirmed on the PDF page before editing (PG16 PDF 528-530, 548-551, 555-557, 563, 841, 870). Backup of the previous state: `scratch/blind/backups_round1/relational-dbms-internals-expert/`.

Evaluation defects (6 of 6 handled):
1. Incomplete EXPLAIN ANALYZE (C07): `references/otimizacao-de-consultas-e-planos-de-execucao.md` §6 gained the reading of `loops` (per-execution averages, multiply), costs in arbitrary units, `Rows Removed by Filter`/`Index Recheck`, BUFFERS, and that execution is real, with `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;` (PG16 p.548-551). WAL/locks even with rollback labeled `[inference]`.
2. Extended statistics: new section in §6 (CREATE STATISTICS, dependencies/ndistinct/mcv, ANALYZE collects, limits, PG16 p.555-557) and `[inference]` linking a very low estimate to correlation; cross-reference in `postgresql-16-tipos-de-indices-e-estrategias.md`.
3. Operational rule: `references/procedimentos.md` gained P4b (EXPLAIN ANALYZE of DML only in a transaction with ROLLBACK) and steps 5-6 in P4.
4. Retry in Repeatable Read/Serializable (C02): confirmed in PG16 p.528-529. The rule already existed in `postgresql-16-mvcc-e-niveis-de-isolamento.md` §4; it was made explicit ("rule for the application"), reinforced in P5 and included in the Concurrency line of the three prompt files (`agents/`, `.github/agents/`, `AGENTS.md`).
5. Overstatement C13 (PG16 p.563): the manual text is "sites that do not require the durability guarantee" and only an abrupt OS crash creates risk; `casos-e-antipadroes.md` §7 and `wal-recuperacao-e-algoritmo-aries.md` now say so and mark "disposable load" as `[inference]`.
6. Minor: `pg_stat_user_indexes` (PG16 p.841, p.870, with columns `idx_scan` etc.) in `postgresql-16-tipos-de-indices-e-estrategias.md`; latch coupling and granularity nuances of the answer key do not change the package.

Extras: `scripts/index_advisor.py` now prints two warnings labeled `[from source]` (ROLLBACK on DML, CREATE STATISTICS); `scripts/relational_index.json` (topic `planner-costs-statistics`) gained pages and keywords.

Verification after the fixes: `verify_citations.py` **170 positive (+14), 25 negative (+3), 0 failures**; `--audit-ranges` 871 citations, 0 out of range, 3 already declared warnings; `audit_tokens.py` 243 terms, 0 NEARBY, 0 failures; `run_script_tests.py --src` 0 failures. New negatives: "disposable", "pg_hint_plan/hypopg", "retry is optional/analyze is read-only".
Limit: the independent validation of the fixes is round 2 (new cases); this round was verified by the same author and by the automatic verifiers.

## 11. Fixes after the blind test (round 2)
Origin: independent blind evaluation of round 2 (14 new cases, "PROVISIONALLY APPROVED", average correctness 2.21; 59/59 citations OK; 12 of 14 cases with a mandatory point available in the sources but delivered as `[extrapolation]` or "NOT COVERED"). Diagnosis: v2 was audited by the pages it cites, not by the pages the sources have; the description promised "complete" ARCH and "complete" PG16, but several references had only page pointers, and the lookup denied coverage that exists. Backup of the previous state: `scratch/blind/backups_round2/relational-dbms-internals-expert/` (32 files, checked equal to the original). **The package's coverage was fixed from the sources**, not the performance on the 14 cases (the cases and the answer key of round 2 were not used to draft the answers).

### 11.1 Pointers converted into content (19 topics, all reread on the PDF page before writing)
| # | Topic | Pages | Where it ended up |
|---|---|---|---|
| 1 | Parallelism: shared-memory, shared-nothing, partial failure (bring everything down, Data Skip, redundancy), **chained declustering** (n-1 nodes do n/(n-1)), shared-disk (does not require partitioning, corruption reaches all, distributed lock manager), NUMA, threads, practice, redundancy at scale | ARCH p.25-35 (and p.106) | `modelos-de-processos-e-concorrencia-sgbd.md` §5 |
| 2 | **Halloween** (solutions, footnote "nothing to do with phantom"; PG16 without a described technique, `t_cid` only a hint) | ARCH p.51-53; PG16 p.2575 | `otimizacao-de-consultas-e-planos-de-execucao.md` §4.1 |
| 3 | Rewriter: partition elimination, transitive predicates, redundant join, flattening of correlated subqueries | ARCH p.39-42 | same §4.2 |
| 4 | Access methods, SARG, RID and primary storage | ARCH p.53-55 | `data-warehouse-colunar-bitmap-e-extensibilidade.md` §1 |
| 5 | Data warehouses: **bitmap (1 bit x ~40 bits)**, fast load, materialized views, OLAP, snowflake | ARCH p.56-62 | same §2 |
| 6 | Columnar: **factor 16 = 100/6** and **"50-100x"** as a `[DATED]` opinion | REDBK p.21-22; ARCH p.62, p.77 | same §3 |
| 7 | Extensibility (ADT, XML, text), standard practice, discussion | ARCH p.62-69 | same §4-5 |
| 8 | **"Well-tuned OLTP is not I/O-bound"**, mmap/DIO, flash, compression, page | ARCH p.72-77 | `buffer-pool-storage-engine-e-acesso-a-disco.md` §4b |
| 9 | **RAID 5, write cache, SAN**, mapping of tables to files | ARCH p.104-106 | same §4b |
| 10 | Catalog and context-based memory allocator | ARCH p.100-104 | `componentes-compartilhados-catalogo-memoria-replicacao.md` §1-2 |
| 11 | Physical, trigger-based and log-based **replication** (two techniques) | ARCH p.106-108 | same §4 |
| 12 | Online utilities, fuzzy backup, bulk load, governors | ARCH p.108-111 | same §5-6 |
| 13 | **Partitioning** (PK includes the key, ATTACH with CHECK, DETACH CONCURRENTLY, pruning, inheritance, best practices) | PG16 p.132-145 | `postgresql-16-particionamento.md` |
| 14 | **Backup, WAL archiving, `archive_timeout`, PITR, timelines** | PG16 p.800-813 | `postgresql-16-backup-pitr-e-replicacao-ha.md` §1-2 |
| 15 | **Replication and HA** (comparison of solutions, log shipping, limitations of logical replication) | PG16 p.815-818, p.924 | same §3 |
| 16 | **json x jsonb**, containment/existence, GIN `jsonb_ops`/`jsonb_path_ops`, row lock | PG16 p.218-225 | `postgresql-16-json-jsonb-e-gin.md` |
| 17 | **Triggers** (`RETURN NULL`, BEFORE/AFTER, WHEN, recursion) and **RLS** (owner, FORCE, OR/AND, covert channel, `row_security`, race) | PG16 p.1302-1304, p.118-124 | `postgresql-16-triggers-e-row-level-security.md` |
| 18 | **BRIN**: entries = pages / `pages_per_range` (1 TiB: 134,217,728 pages; 1,048,576 and 4,194,304 entries `[derived]`) | PG16 p.2552, p.1758 | `postgresql-16-tipos-de-indices-e-estrategias.md` §6.1; `procedimentos.md` P10 |
| 19 | **SQL Antipatterns**: scope (does not cover performance, backups, security or NoSQL) and table of contents with the solution titles | ANTI-INT p.9; ANTI-TOC p.5-9 | `casos-e-antipadroes.md` §13 |

**Wrong answer key (C07)**: "at most 2 partitions" only holds with an upper bound in the `WHERE`; without it the query touches the partitions of the window, all the future ones already created and the DEFAULT. Recorded in `postgresql-16-particionamento.md` §5 with the base page (PG16 p.142-144) and labeled `[inference]` (the page defines pruning as proof that the partition cannot contain rows of the `WHERE`; the manual does not talk about `now()` or an open interval). Also in `procedimentos.md` P9.

**Scope inconsistency (README x prompt)**: resolved by **including** RLS, triggers, backup/PITR and replication/HA (the pages are in the sources) in the prompt of the three adapters, in the README and in `INDEX.md`; `INDEX.md` gained the **real coverage map (section 1b)** with deep/summary/pointer-only per source and the boundary in two categories (outside the sources, verified; pointer only). pgvector/HNSW and MongoDB/shard key entered the boundary.

### 11.2 Lookup (`relational_lookup.py`, `relational_index.json`, `source_terms.json`)
- Output in **three levels**: COVERED (exit 0; summary + pages), POINTER ONLY (exit 3; there is content/occurrences in the sources without a summary in the package; suggests reading and forbids saying "the book does not cover it") and NOT COVERED (exit 1; only terms from the curated list of things outside the sources, or with no occurrence in the term index, with the warning that this does not prove absence).
- **Term index** `scripts/source_terms.json` (1.2 MB): inverted term -> pages index generated by `scripts/build_term_index.py` from the text extracted from the 7 sources (deterministic generator; the test checks that the versioned file is reproduced byte for byte).
- 64 topics (were 43), all with `summary`; 5 curated "pointer" topics (streaming/hot standby, logical replication, JSON/jsonpath functions, command reference pages, Red Book chapters outside the focus); synonyms added (chained declustering, data skip, raw device, raid, pitr, archive_timeout, rls, row level security, trigger, partition, pruning, bitmap, fator 16, 50-100x...). The curated list of things outside the sources now has 35 terms and **was checked against the term index** (removed those that appear in passing: newsql, embeddings, "distributed sql"; honest notes for kimball, postgis, timescaledb).
- False "NOT COVERED" results from round 2 resolved: `chained declustering`, `raw device`, `PITR`, `row level security`, `trigger`.

### 11.3 Verification after the fixes
| Check | Result |
|---|---|
| `verify_citations.py` (curated checks) | **276 positive (+106), 35 negative (+10), 0 failures** |
| `verify_citations.py --audit-ranges` | 1,456 citations (ARCH 371, PG16 866, REDBK 69, ANTI-* 150), **0 out of range**, 25 wide-range warnings (declared: whole sections or whole chapters) |
| `audit_tokens.py` | 477 terms checked, 0 NEARBY, **0 FAIL** (while writing, the verifier flagged 2 slips of mine: `get_next` cited on a page where the extraction has "get next"; fixed) |
| `run_script_tests.py --src` | 52 checks OK (script and three-level lookup cases, integrity of the curated index, 2 verifiers and reproducibility of the term index; there were 27): **0 failures** |
New positive checks (`C2-A*`, `C2-P*`, `C2-B*`, `C2-N*`) cover each new content item; new negatives (`C2-X*`): pgvector, HNSW/IVFFlat/ef_construction, shard key/sharding/mongos, Data Skip and chained declustering absent from PG16, Halloween absent from PG16, third-party tools, modern PG terms absent from ARCH, Closure Table, write skew, Oracle RAC/SYSPLEX absent from PG16.

### 11.4 What remains pointer only (and why)
- PG16: streaming replication, replication slots, synchronous replication, failover and hot standby in detail (p.821-835); logical replication chapter 31 outside p.924 (p.905-927); JSON functions/operators and `jsonpath` (p.227-229, p.361-380); command references (CREATE POLICY p.1775, CREATE TRIGGER p.1852, pg_basebackup p.2099, pg_dump p.2135, pg_restore p.2168); and the rest of the 3,057 pages. Reason: outside the "internals" focus or beyond what is needed for the requested topics; the lookup returns the page and the agent suggests reading it.
- REDBK: chapters 5, 8, 9, 10, 11 and 12 (p.3-13, p.23-27, p.37-46), outside the focus.
- ARCH: only the bibliographic references (p.113-119) were not summarized.
- SQL Antipatterns: the text of the chapters that are not in the PDFs (only the table of contents exists); chapters 21 and 3 remain without the solution sections.
- Not verified: no new SQL was run on a real PostgreSQL; calculations labeled `[derived]` were redone by hand; correction by an independent model requires a third round with new cases on the same topics (partition, PITR, JSON, RB p.21, ARCH p.29/52/57/74/107).


## 12. Fixes after the blind test (round 3)
Origin: independent blind evaluation of round 3 (14 new cases by random draw of pages; "PROVISIONALLY APPROVED"; average correctness F = 2.36, backing L = 2.93 with 75/77 citations OK, 1 wrong page by the solver and 1 overstatement by the solver; **11 of 14 cases** with a point available in the sources but delivered as `[extrapolation]` or pointer; **1 content error in the package**: HOT without the BRIN exception). The evaluator's diagnosis: rounds 1 and 2 expanded the package by the passages the author knew were missing, not by systematic sweeping; the lookup returned COVERED for topics whose reference did not have the text. Backup of the previous state: `scratch/blind/backups_round3/relational-dbms-internals-expert/` (40 files, checked by count). Each page was reread in the extract (`scratch/audit/.../src/*.txt`) before writing. The answer key of the cases and the page sample were **not read**: coverage was fixed, not performance on the 14 cases.

### 12.1 Errors fixed (first)
1. **HOT and BRIN** (content error): the summary said only "when the update does not change indexed columns". PG16 p.2576 says: it does not count **summarizing indexes (the only one in core is BRIN)**; new index entries are not needed, but **summarizing indexes may still need an update**; old versions can be removed in normal operation, **including in SELECT**; lowering `fillfactor` only increases the chance (without it HOT still occurs); monitor `pg_stat_all_tables` (`n_tup_hot_upd` and `n_tup_newpage_upd`, p.868-869). Fixed in `postgresql-16-vacuum-autovacuum-e-armazenamento.md` §4, `glossario.md`, `postgresql-16-mvcc-e-niveis-de-isolamento.md`, `casos-e-antipadroes.md` (from "may prevent HOT" to "an index on an updated column prevents it; BRIN does not") and `postgresql-16-tipos-de-indices-e-estrategias.md`; the lookup topic `pg-hot` now carries the exception in the summary.
2. **"New entries in all indexes"** (solver overstatement): the saving holds for indexes that are not summarizing ones (same source).
3. **BUFFERS on p.548** (solver): the option is described on p.550; p.548 deals with `loops` and costs in arbitrary units. The package already cited p.550; it gained an explicit warning in `otimizacao-de-consultas-e-planos-de-execucao.md` and in the prompt (rule 13).
4. **Other findings along the way**: the `archive_timeout` calculation (1,440 files/day) now says the forced switch only occurs with activity in the database (PG16 p.668); the manual **cites pgBadger and check_postgres** (PG16 p.799), which I was going to classify as "outside the sources" (the negative `C3-X03` failed and was fixed; see `C3-P92`).
5. **Topic `index-locking-phantoms` marked COVERED without content**: filled in (§12.2, item 13); the lookup now verifies the term in the reference (§12.4).

### 12.2 Topics converted from pointer/omission into paraphrased content with a page (pt-BR, `[from source]` only what was read)
| # | Topic | Pages | Where it ended up |
|---|---|---|---|
| 1 | Synchronous replication: `FIRST`/`ANY` (quorum), "commits may never complete", several candidates, streaming state, waiting commits marked confirmed, `synchronous_commit` levels, who does not wait, network bandwidth > WAL rate (calculation `[derived]` 200 Mbit/s = 25 MB/s < 40 MB/s) | PG16 p.824-827, p.663-664, p.675-676 | `postgresql-16-replicacao-streaming-sincrona-hot-standby-e-failover.md` §2 |
| 2 | Failover, STONITH, witness server, degenerate state, PG does not provide the failure detector | PG16 p.827-828 | same §3 |
| 3 | Log shipping standby, streaming (lag < 1 s), slots (`max_slot_wal_keep_size` -1), cascading, `REPLICATION` authentication, lag monitoring | PG16 p.819-823 | same §1 |
| 4 | Hot standby: what is allowed, conflicts and `max_standby_*_delay` (30 s), `hot_standby_feedback`, memory parameters >= primary, limitations (Serializable) | PG16 p.828-835 | same §4 |
| 5 | Replication parameters and defaults | PG16 p.672-679 | same §5 |
| 6 | `pg_rewind` (prerequisites, `--no-ensure-shutdown`, failure leaves the target unrecoverable, role with `EXECUTE`), `wal_log_hints`, `wal_compression` | PG16 p.2256-2259, p.665 | same §6 |
| 7 | Complete logical replication (publication, subscription, replica identity, filters, column lists, conflicts and `SKIP`, restrictions, architecture, security, parameters) | PG16 p.905-927, p.679 | `postgresql-16-replicacao-logica.md` |
| 8 | Parallel aggregation (Partial/Finalize, DISTINCT/ORDER BY/ordered-set/GROUPING SETS, combine/serial, joins in the parallel part), parallel query, parallel safety, `PARALLEL UNSAFE` by default | PG16 p.564-568, p.660-661, p.1713-1714 | `postgresql-16-estatisticas-planner-paralelismo-e-snapshots-antigos.md` §4 |
| 9 | `old_snapshot_threshold` (startup, -1, minutes, does not guarantee the error, does not return space) and `pg_old_snapshot_time_mapping` (and the absence of reset functions) | PG16 p.661-662, p.2872 | same §5 |
| 10 | `SET STATISTICS` (0-10000/-1, lock), `n_distinct`/`n_distinct_inherited`, ANALYZE on inheritance/partitioned tables, no sampling formula | PG16 p.1644, p.1678-1679 | same §1 |
| 11 | `CREATE STATISTICS` and the limit on joins | PG16 p.1807-1808 | same §2 |
| 12 | `COMMIT PREPARED`, `ROLLBACK PREPARED`, `PREPARE TRANSACTION`, `pg_prepared_xacts`, GID | PG16 p.1695, p.1989-1990, p.2008, p.2577 | `postgresql-16-locks-explicitos-advisory-locks-e-transacoes-preparadas.md` §7 |
| 13 | Latch coupling/crabbing, right-link, GiST, 2PL on indexes, nested top actions, interdependencies | ARCH p.92-93, p.96-97 | `controle-de-concorrencia-2pl-e-mvcc.md` §3b |
| 14 | Red Book p.22 (US$ 25,000/TB, active-active x active-passive factor 3, "MVCC does not do that") and p.29-30 (ORMs, `SELECT FOR UPDATE`, NoSQL irony, Dynamo) | REDBK p.22, p.29-30 | `data-warehouse-colunar-bitmap-e-extensibilidade.md` §3; `controle-de-concorrencia-2pl-e-mvcc.md` §5b and §6 |

### 12.3 Systematic sweep for omissions of the same class (beyond the list)
The PG16 chapters most tied to internals and administration that the references only pointed to were gone through page by page, prioritizing default values, warnings and numeric limits:
| Chapter/section | Pages read | Result |
|---|---|---|
| Replication (whole ch. 27; whole ch. 31) | p.818-835, p.905-927 | new replication files (items 1-7) |
| Configuration (ch. 20): connections, memory, vacuum cost, bgwriter, WAL, checkpoints, archiving, replication, planner, logging, autovacuum, timeouts/ages, locks | p.646-668, p.672-686, p.690-697, p.702-710, p.715 | `postgresql-16-configuracao-memoria-wal-checkpoint-timeouts-e-locks.md` (defaults and warnings: `shared_buffers` 25%/40%, `fsync`, THP, `statement_timeout` outside `postgresql.conf` etc.) |
| Explicit locks (13.3), `LOCK`, `SELECT ... FOR`, advisory locks | p.531-537, p.1972-1974, p.2029-2030 | locks file |
| Monitoring statistics (ch. 28) | p.837-884 | `postgresql-16-monitoramento-views-pg-stat-e-extensoes-contrib.md` §1-4 |
| Contrib (appendix F) | `pg_stat_statements`, `auto_explain`, `pg_prewarm`, `pgstattuple`, `amcheck`, `pg_trgm`, `old_snapshot` | same §5 |
| Data types (ch. 8) and constraints (5.4) | p.100-110, p.184-205, p.216 | `postgresql-16-tipos-de-dados-limites-e-constraints.md` |
| Planner (20.7) | p.680-686 | statistics/planner file §3 |
Result of the sweep: **7 new reference files** (from 21 to 28), 21 new topics in the lookup, 5 new honest pointers (`ptr-pg-contrib-other`, `ptr-pg-arrays-composite-range`, `ptr-pg-fulltext-search`, `ptr-pg-auth-roles`, `ptr-pg-localization-collation`) and 2 old pointers removed (streaming and logical replication).

### 12.4 Lookup
- `relational_lookup.py`: a curated topic is only COVERED if the queried term **appears in the topic's reference file** (whole phrase, or all tokens as a word prefix); otherwise it is **downgraded to POINTER ONLY** with the note "the term does not appear in references/...". Matching by `id` now respects word boundaries (the term "hot" no longer matches "snapshot"). A term exactly equal to an item of the "outside the sources" list prevails as NOT COVERED even if there is a neighboring topic (`incremental backup`).
- `relational_index.json` v2.2: 88 topics (were 64); new true NOT COVERED terms: `pg_combinebackup`, `incremental backup`, `backup incremental`, `pg_old_snapshot_reset`, `pg_old_snapshot_set_threshold`; `patroni`, `repmgr`, `pg_auto_failover` now point to the failover topic.
- `source_terms.json` **did not need to be regenerated**: it depends only on the text of the sources, which did not change; the `IDX` test confirms that `build_term_index.py` reproduces it byte for byte.
- `IDX-INT` now requires every COVERED topic to have an existing reference with at least one key term. Two terms that stayed COVERED without the English term (`partial index`, `raw device`) gained the term (in parentheses) in the reference; the same for `extended statistics`, `prepared transactions` and `main memory`.
- Labels that changed: COVERED (were POINTER ONLY): `pg_rewind`, `wal_log_hints`, `synchronous_standby_names`, `quorum commit`, `n_distinct`, `SET STATISTICS`, `old_snapshot_threshold`, `COMMIT PREPARED`, `pg_prepared_xacts`, `parallel aggregate`, `count(DISTINCT`, `active-active`, `main memory`, `streaming replication`, `logical replication`; NOT COVERED (true): `incremental backup`, `pg_old_snapshot_reset`.

### 12.5 Verification after the fixes
| Check | Result |
|---|---|
| `verify_citations.py` (curated checks) | **368 positive (+92), 43 negative (+8), 0 failures** (ids `C3-P01` to `C3-P92` and `C3-X01` to `C3-X08`) |
| `verify_citations.py --audit-ranges` | 2,176 citations (ARCH 396, PG16 1,542, REDBK 88, ANTI-* 150), **0 out of range**, 49 wide-range warnings (declared) |
| `audit_tokens.py` | 1,250 terms checked, 0 NEARBY, **0 FAIL** (while writing, the verifier flagged ~50 slips of mine, such as a citation placed after the list of terms or terms with a slash; all were fixed by rewriting, not by relaxing the verifier) |
| `run_script_tests.py --src` | 77 checks OK (25 new lookup cases `R3-01` to `R3-25`, index integrity with the rule "COVERED requires content", 2 verifiers, reproducibility of the term index): **0 failures** |
New negatives: nonexistent `old_snapshot` functions, native incremental backup, third-party tools (pganalyze, pg_cron, pgbouncer, pg_auto_failover, pgvector), "300 × target" formula, `uuidv7`, PG17 features (`failover slots`, `pg_createsubscriber`, `pg_stat_checkpointer`).

### 12.6 What remains pointer only
PG16: JSON functions/operators and `jsonpath` (p.227-229, p.361-380); authentication, `pg_hba.conf`, roles and database management (p.727-763); full-text search (p.483-523); arrays, composites and ranges (p.229-247); localization/collations (p.764-787); contrib modules without a summary (`pageinspect`, `pg_visibility`, `pg_walinspect`, `postgres_fdw`, `dblink`, `pgcrypto`, `hstore`...); command references (CREATE POLICY, CREATE TABLE, pg_dump, pg_restore...); replication protocol (ch. 55); recovery administration functions (Table 9.93). REDBK: chapters 5, 8-12 (p.3-13, p.23-27, p.37-46). ARCH: bibliographic references. SQL Antipatterns: what is not in the excerpts.
Limit: no new SQL was run on a real PostgreSQL; the `[derived]` calculations were done by hand; commands and values come from the 16.15 manual (some parameters, such as `output_plugin_libraries`, only exist in this minor revision). The independent validation of these fixes requires a **round 4** with new cases on the same topics (synchronous/quorum replication, `pg_rewind`, `n_distinct`, parallel aggregation, `old_snapshot_threshold`, COMMIT PREPARED, HOT/BRIN, latch coupling/right-link, Red Book p.22 and p.29-30) and on the configuration and monitoring chapters.

## 13. Fix after the blind test of round 4

**Serious defects fixed** (new summaries in Portuguese, paraphrased, with PDF page and labels; each claim checked on the page):
- `CREATE SUBSCRIPTION` (PG16 p.1811-1814): `postgresql-16-replicacao-logica.md` section 3b (defaults of `connect`, `create_slot`, `enabled`, `copy_data`, `binary`, `slot_name`/`NONE`, `streaming`, `two_phase`, notes).
- `CREATE INDEX CONCURRENTLY` and INVALID index (PG16 p.1758-1760): `postgresql-16-tipos-de-indices-e-estrategias.md` section 7b, **including that the unique INVALID index keeps enforcing uniqueness**.
- `VACUUM` command (PG16 p.2063-2067): `postgresql-16-vacuum-autovacuum-e-armazenamento.md` section 1b (PARALLEL, TRUNCATE, INDEX_CLEANUP x failsafe, FULL). Fixed "VACUUM p.2066" to p.2063-2067 in INDEX.
- Red Book p.14-15 and p.18-19: `controle-de-concorrencia-2pl-e-mvcc.md` section 6b (System R, Postgres/ADT/time travel, Gamma, AC x consensus, Paxos Commit). INDEX §1b now reflects what is actually summarized (p.20 is only a reference list).

**Minor defects fixed**: rules/`security_barrier`/`LEAKPROOF` (p.1343-1344), full-text search 12.9 and `ts_lexize` (p.519-520), ANTI-INJ p.5 (Gonzalez; the dollar loss is **not stated**), `pg_stat_subscription`/`_stats` (p.860, p.874), `pg_collation` (p.2309; the qualified name is enough), `cert`/`clientcert`/RADIUS (p.732, p.746-747), `wal_buffers` and `wal_compression` lines (p.665). PT/EN equivalences in the glossary (46 terms validated against the pages).

**Lookup**: `relational_lookup.py` was redone. COVERED only when the term (whole phrase, simple plural tolerated) is the **subject of a summary excerpt** of `references/*.md` (section title or start of the excerpt), via `ref_terms.json` generated by `build_ref_index.py` only from the content of the references; a passing mention in the middle of a sentence becomes POINTER ONLY (the excerpt is shown). File name, topic id/title/keyword, maps (INDEX, "navigation map"), metadata blocks, `[extrapolation]` lines and "do NOT say" sections do not decide COVERED (the first two and the maps give at most POINTER ONLY). With the OLD references (round 4 backup), the new lookup gives POINTER ONLY for `CREATE SUBSCRIPTION` and `CREATE INDEX CONCURRENTLY` (only mentioned in passing), COVERED for `System R` (the "Selinger / System R" bullet of the optimizer is a genuine summary) and POINTER ONLY for `INDEX_CLEANUP`, `Paxos Commit` and `security_barrier`; with the new references all six give COVERED. Declared cost: terms that no summary treats as a subject (490 of 1056 old topic keywords) become POINTER ONLY, with the passing excerpts shown; the glossary gained PT/EN equivalences for the most used ones.

**Verification**: see `tests/run_script_tests.py` (cases `R4-01` to `R4-27`, 12 synthetic `SYN` cases, `REFIDX` reproducibility), `verify_citations.py` (35 new positive `R4-P01..` and 3 negative `R4-X01..`) and `audit_tokens.py`.

**Still without a summary**: the rest of the PG16 manual listed in INDEX §1b "Pointer only" (JSON functions, arrays/ranges, `pg_hba.conf` beyond cert/RADIUS, collations beyond the catalog, secondary contrib modules, command references beyond `CREATE INDEX`, `CREATE SUBSCRIPTION` and `VACUUM`) and Red Book chs. 5, 8-12.

## Fix after round 5 (missing summaries and citation adjustments)
Origin: blind evaluation of round 5 (cases C03, C04, C06, C09, C13, C14 depended only on a pointer; C02, C07, C08 partially). All the pages below were reread in the text extracted from the PDF before summarizing.
- **COPY (PG16 p.1700, and p.1697)**: new summary in `postgresql-16-copy-window-functions-arrays-drop-owned-e-dict-xsyn.md`. The point the solver got wrong was checked: p.1700 says that, for identity columns, `COPY FROM` **always writes** the input values, like `OVERRIDING SYSTEM VALUE`; it does **not** say it rejects the file value and does **not** mention "GENERATED ALWAYS" (checks `R5-P05` and negative `R5-X01`). Without a column list, `COPY` skips generated columns (p.1697, `R5-P08`).
- **Window functions (p.168)**: summary of the evaluation order (after GROUP BY/HAVING) and of ordering; the "window function" lookup is now COVERED and returns p.168 (cases `R5-01`, `R5-01b`).
- **GREATEST/LEAST, arrays, intarray (p.385, p.2854)**, **DROP OWNED (p.1913)**, **dict_xsyn (p.2832-2833)**: summaries with the details that cases C09, C13 and C14 asked for (NULL ignored, `@>` and duplicates, `uniq` only for adjacent ones, current database, RESTRICT x CASCADE, REASSIGN OWNED, options and `.rules` file).
- **Red Book ch. 9 (p.41-44)**: new `redbook-cap9-linguagens-orm-cql-bloom-datalog.md` (ORMs, CQL, Bloom/CALM, Datalog). p.44 says only "a cool billion dollars" for Nicira; the value US$ 1.26 bi does not come from the text (negative `R5-X04`). PDF p.46 is the book's preface (not ch. 9) and p.45 is only references.
- **WAL p.899-900 and p.903**: `commit_delay` ignored in asynchronous commit, per-transaction mode, `DROP TABLE`/2PC always synchronous, immediate shutdown = crash, checkpoint skipped without new WAL; LSN, 16 MB segments in `pg_wal`, 8 kB block only at compile time, numbering with no way back, moving `pg_wal` with the server stopped and a symbolic link.
- **Update message (p.2428)**: 'K' only if an index column of the replica identity changed; 'O' only with `FULL` identity; never both.
- **Overstatement "compile-time constant" (p.665-666)**: confirmed: those pages only say "typically 8kB" for `XLOG_BLCKSZ`; that the WAL block size is a compile-time option is on p.903 (`--with-wal-blocksize`). The package did not assert that; the `wal_buffers` line now separates the two sources and the negative `R5-X02` (restricted to p.665-666) prevents the wrong attribution.
- **numeric, negative scale (p.186, not p.185)**: the package already cited p.186 for negative scale; the detail is now in its own excerpt with the citation p.186 and the negative `R5-X03` (restricted to p.185) establishes that the `NUMERIC(2,-3)` example is not there.
- **Verification**: `run_script_tests.py` cases `R5-01` to `R5-12`; `verify_citations.py` 32 positive `R5-P01..P32` and 5 negative `R5-X01..X05` (negatives now accept the `pages` field); `audit_tokens.py` without failures.

## Fix after round 6 (D1-D12: missing summaries, lookup and command map)
Evaluation: `scratch/blind/runs6/.../avaliacao.md` (10 of 14 cases depended on pages only pointed to). All the summaries below are paraphrases checked against the PDF text (PDF pages).
- **D1 `CREATE POLICY` (PG16 p.1776-1779)**: section 5d of `postgresql-16-triggers-e-row-level-security.md`: permissive (OR) x restrictive (AND), only restrictive = nothing accessible, `SELECT` without `WITH CHECK`, `INSERT` only `WITH CHECK`, `DELETE` only `USING`, `UPDATE`/`DELETE` that read columns also require a `SELECT` policy, `ON CONFLICT DO UPDATE`/`MERGE` raise an error instead of filtering, Table 292 (filter x check). Pointer fixed: the per-command detail is on p.1776-1779 (the synopsis starts on p.1775).
- **D2 `pg_stat_database_conflicts` (PG16 p.868; cross-reference on p.867)**: one row per database, standby only, six `confl_*` counters. The columns `confl_vacuum_cleanup` and `confl_hot_standby_feedback` do not exist (negative `R6-X01`; lookup: NOT COVERED). Imprecision fixed: the table is on p.868 (p.867 only refers to it); `hot_standby_feedback` is on p.677 and `max_standby_*_delay` on p.676-677, not "p.677-678".
- **D3 Red Book (REDBK p.5-9, p.10-12, p.3-4, p.23-26)**: `redbook-cap10-11-12-web-analitica-complexa-e-integracao-de-dados.md`. p.8 resolves case C04: SAS bills "multiple billions" (no exact value; negative `R6-X02` for "3.2 bi"), SAS/R users are not database users ("swimming against the current"), three threats to SAS; p.9 is only references.
- **D4 `REINDEX` (PG16 p.1995-1997) and `reindexdb` (p.2226-2227)**: `postgresql-16-comandos-reindex-drop-tablespace-truncate-e-utilitarios.md`. `reindexdb` is only a wrapper, `-j` opens `njobs` connections and is incompatible with `--index`/`--system`; with `TABLESPACE`, TOAST indexes are rebuilt and not moved; no "control connection" (negative `R6-X03`).
- **D5 `pageinspect`/BRIN (PG16 p.2873-2881)**: section 6.2 of the indexes file and 5b of the monitoring one. **Manual inconsistency (p.2879)**: `brin_revmap_data` returns TIDs `(6,137)`..`(6,141)` (page 6), but the `brin_page_items` example reads `get_raw_page('brinidx', 5)` (page 5) and shows offsets 137-139; recorded as `[inference]`, without correcting the manual (negative `R6-X05`).
- **D6 aggregates (PG16 p.395-402)**: `postgresql-16-funcoes-agregadas.md` (NULL on zero rows, `sum`, `every` x `any`/`some`, order without `ORDER BY`, `count(*)` proportional to the table, Partial Mode, statistics, ordered-set/hypothetical, `GROUPING`). The MVCC reason for `count(*)` is `[inference]`, not from the page (negative `R6-X06`).
- **D7 `DROP PUBLICATION` (p.1918), `DROP SERVER` (p.1925)**, besides `DROP SUBSCRIPTION` (p.1927), `DROP TABLE` (p.1929) and `DROP TABLESPACE` (p.1930). **D8 `CREATE TRIGGER` (p.1854-1855)**. **D9 `include_dir` (p.644) and the parameter definition (p.641-645)**. **D10 `CREATE TABLESPACE` (p.1842-1843)**, `TRUNCATE`, `CLUSTER`, `CHECKPOINT`, `EXPLAIN`.
- **D11 lookup**: (a) `aliases` field in `relational_index.json` (validated PT/EN equivalences: `standard practice`, `full-text search`, `recovery conflict`), with a "PT/EN equivalence applied" line in the output; (b) `count(*)` requires the literal call (`lit` field of `ref_terms.json`), so it does not match "pin count"; (c) `partition key` gained its own summary in partitioning; (d) `Cassandra`, TWCS, `LOCAL_QUORUM`, `scylladb`, `clustering key` and the invented columns entered the curated list of things outside the sources (NOT COVERED).
- **D12 INDEX.md**: section 3b with the page map of 183 SQL commands and 32 applications (one `R6-MAP-<page>` check per entry, 215 in total), updated real coverage and the list of what remains pointer only.
- **Verification**: `run_script_tests.py` (`R6-*` cases and `ALIAS`), `verify_citations.py` 708 positive and 60 negative (272 positive and 9 negative new), `--audit-ranges` without failures, `audit_tokens.py` without failures. The `IDX` failure (hash of `source_terms.json`) is environmental: the terms and pages of the reproduced index are identical, only the fingerprint of the extracted text differs according to the extractor version.


## Fix after round 7 (blind test, Role C)
- **New summaries** (previously pointer only), each checked on the page: PG16 p.719 (read-only parameters: `max_index_keys` 32, `max_function_args` 100, `max_identifier_length` 63, `segment_size` 1 GB, `integer_datetimes`, `in_hot_standby`; `max_partition_keys` is not there), p.669-670 (`recovery_prefetch`, `wal_decode_buffer_size`, `standby.signal` x `recovery.signal`, `restore_command` with `%f %p %r`), p.436-437 (WAL name functions, `pg_split_walfile_name` and the example `C001/AB000100`, `pg_last_wal_*`), p.2357-2359 (`pg_locks`: 12 `locktype` values, NULL columns, advisory key), p.2178-2180 (`pg_verifybackup`: `-m` and `-i` on p.2179, `-s` on p.2179, examples on p.2180).
- **Additions**: p.818 (no solution makes a query use several servers; partitioning; commercial ones "not discussed"), p.641 (case-sensitive unit, case-insensitive enum, boolean prefix, octal), p.568 (Halting Problem and "does not even try"), ARCH p.32 (definition of pod; NUMA SMP very common), ARCH p.80 (consistency by executor checks, with abort).
- **Page fixed**: defaults of `max_parallel_workers_per_gather` (2), `max_worker_processes` (8) and `max_parallel_workers` (8) are PG16 p.660-661, not p.564-565 (which carry the limits mechanism). Negative `R7-X04`.
- **Authorship**: the MapReduce/Spark/Rasmussen/McSherry passage (REDBK p.25) is by Peter Bailis (ch. 5, p.23); the "70% SparkSQL" is from Stonebraker's comment. Hellerstein does not appear on p.23-26 (`R7-X05`). Summary wording adjusted: Bailis says Spark still needs to evolve and that the gaps close.
- **Lookup**: "parallel safe/restricted/unsafe" is now COVERED (dedicated bullet); "Data Guard" and "Oracle Data Guard" enter the curated `not_in_book` list (NOT COVERED); the header now carries the ANTI-INJ page conversion (printed = PDF).
- **Verification**: `verify_citations.py` +23 positive and +6 negative (`R7-*`), `--audit-ranges` without failures, `audit_tokens.py` without failures, `run_script_tests.py` with `R7-*` cases.


## Fix after round 10 (blind test, defects P1-P11 and P13)
Evaluation: `scratch/blind/runs10/.../avaliacao.md`. Each fact was checked in the PDF text (PDF pages; printed PG16 = N-38, printed ARCH = N+140). Paraphrases, without copying passages.
- **P1 PG16 p.538-539 (13.4.2, 13.5, 13.6)**: section 3a of `postgresql-16-locks-explicitos-advisory-locks-e-transacoes-preparadas.md` and a note in `postgresql-16-mvcc-e-niveis-de-isolamento.md`. Exact caveat: `SELECT FOR UPDATE` only blocks while the lock lasts; after the owner's commit/rollback the blocked one proceeds, unless there was a real UPDATE of the row. Also: `SELECT sum()` in RC, single RR, `SHARE`+, locks before the first query in RR (snapshot freezes at the first SELECT/INSERT/UPDATE/DELETE/MERGE), 40001/40P01/23505/23P01, retry of the whole transaction, 13.6 (TRUNCATE/ALTER TABLE not MVCC-safe; no Serializable on hot standby). Checks `R10-P01..P07`, negative `R10-X01`.
- **P2 `pg_waldump` (PG16 p.2274-2277)**: section 8c of the utilities file. `.partial` is not read (the suffix must be removed; "on a copy" is `[inference]`); only the requested timeline is shown; `-t` default = startseg or 1. `R10-P08..P12`, `R10-X02`, `R10-X11`.
- **P3 `COPY` Notes/WHERE (PG16 p.1699)**: section 1a of the COPY file. **Discrepancy with the round 10 solver**: `COPY partitioned_table TO` does NOT return the partitions (equivalent to `SELECT * FROM ONLY`; use `COPY (SELECT ...)`); `COPY FROM` is not supported with RLS; `WHERE` without a subquery or generated column. `R10-P13..P15`, `R10-X03`.
- **P4 `pg_dumpall` (PG16 p.2150-2156)**: section 1.1a of the backup file (one excerpt per option on p.2153: `--no-role-passwords`, `--no-sync`, `--on-conflict-do-nothing`). `R10-P16..P20`, `R10-X04`.
- **P5 p.692-693**: `log_startup_progress_interval` (10 s, 0 disables, ms without unit, example 25 s/8 s), `application_name`, Table 20.2. **P6 p.2620-2622**: section 3c of the types file (POSIX TZ: sign opposite to ISO, `Jn`/`n`/`Mm.n.d`, fallback `M3.2.0,M11.1.0` = US 2020, `EST5EDT` etc. = named zones, `FOOBAR0`). **P7 p.2665**: D.2 (T176 without `NEXT VALUE FOR`, T180/T181 without comment, T218 omitted on purpose). **P8 p.266-267**: `round`/`trunc`/`scale`/`trim_scale`/`width_bucket`/`random`. **P9 p.829**: pre-14 note (`SHOW transaction_read_only`), `transaction_read_only` always true, LISTEN/NOTIFY. **P10 REDBK p.1-2**: section 0 of the Red Book file. **P11 ARCH p.72**: `mmap`/`msync` and vendors do not recommend raw. `R10-P21..P34`, `R10-X05..X10`.
- **P13**: `INDEX.md` marks `COPY` Notes, `pg_dumpall`, `pg_waldump` and `SELECT FOR UPDATE` as "read before stating". **P12 (p.1366, `quote_nullable`)** was not handled in this round.
- **Indexes**: `ref_terms.json` regenerated by `build_ref_index.py`; `relational_index.json` gained 6 topics (`pg-for-update-caveat`, `pg-waldump`, `pg-dumpall`, `pg-log-startup-progress`, `pg-numeric-functions`, `pg-sql-conformance-unsupported`) and extended 7 (locks, COPY, date/time, hot standby, RED, storage, commands pointer).
- **Verification**: `verify_citations.py --src` 806 positive and 90 negative (34 + 11 new), 0 failures; `--audit-ranges` and `--audit-index` without failures; `audit_tokens.py --src` without failures; `run_script_tests.py` with the `R10-*` cases (and `R5-02` updated to include p.1699).

## Fix after round 11 (blind test, evaluator defects)
- **New summaries, all checked in the PDF** (each claim has a `R11-P*`/`R11-X*` check in `citation-checks.json`): PG16 p.428-430 (Tables 9.80-9.83: `txid_*` deprecated and replacements, commit timestamp only with `track_commit_timestamp` and removed by vacuum; no `_retention` or `_batch()`), p.1648-1649 (`REPLICA IDENTITY`: USING INDEX requires unique, not partial, not deferrable, NOT NULL; dropped becomes NOTHING; TOAST always logged), p.1786-1788 (`CREATE PUBLICATION`: unlogged/matview/view excluded, column list x schema, implicit partitions, `publish`, `publish_via_partition_root` default false), p.950 and p.958-959 (libpq `connect_timeout` minimum 2 s, per host, 0 = indefinite, ignored with `PQconnectPoll`; `keepalives*`), p.648 (server `tcp_keepalives_*`), p.677 (30 s default), p.762-763 and p.1658 (tablespaces), p.1930, p.2360 (`pg_matviews`, `pg_policies`), p.2389-2390, p.2412-2413 and p.2434 (COPY messages), p.539-540 (13.6 and 13.7), ARCH p.49-50 (iterator without queues or rate matching).
- **Discrepancy fixed**: the COPY version note that the summary cited as p.2403 is on p.2434 (p.2403 carries the base backup). p.906 was already correct (default = primary key).
- **Lookup**: `hash index deadlock` and `hot standby TRUNCATE` lead to p.539-540 (likely summary, page to read first); page ordering prefers those that a summary cites and that talk about the terms; `Snowflake` (product) = curated NOT COVERED with `except_when` for `snowflake schema`; `track_commit_timestamp_retention` and `pg_xact_commit_timestamp_batch` = curated NOT COVERED; the excerpt whose subject is exactly the term weighs more in the topic ranking; `R11-*` cases in `run_script_tests.py`.

## Fix after round 12 (blind test, defects P1-P4)
- **P1** (hot standby): `postgresql-16-replicacao-streaming-sincrona-hot-standby-e-failover.md` gained the notes of PG16 p.834: `DROP DATABASE` or `ALTER DATABASE ... SET TABLESPACE` on the primary immediately disconnects the database's users on the standby, whatever `max_standby_streaming_delay` is; `ALTER DATABASE ... RENAME` does not disconnect; `DROP USER`/`DROP ROLE` does not drop the connected session (it only prevents reconnection). The sentence that put `DROP DATABASE` among the conflicts canceled "after a maximum delay" was fixed.
- **P2** (pointer only): new summaries, checked page by page in the PDF, of PG16 p.2513-2514 (B-tree deduplication), p.1322 and p.1332-1333 (rule system), p.86-88 (window function calls), p.2135-2136 and p.2169-2170 (`pg_dump`/`pg_restore`), p.202-204 (`interval`), p.188-189 (`extra_float_digits`, special values), p.2649-2650 (SQL conformance, D and D.1), p.2157-2158 (`pg_isready`), p.2058-2062 (`UPDATE ... FROM`, `SAVEPOINT`, compatibility) and REDBK p.33 (two reasons why there is no optimal plan, join of two tables, System R x Exodus/Volcano/Cascades, Orca and Calcite). `interval` calculations and the conclusion on `pg_restore --create -d` are labeled `[derived]`/`[inference]`. Nine new curated topics in `relational_index.json`; `ref_terms.json` regenerated; the terms that used to be POINTER ONLY (`deduplication`, `rule system`, `CREATE RULE`, `window frame`, `ROWS BETWEEN`, `FILTER clause`, `pg_restore --create`, `IntervalStyle`, `extra_float_digits`, `SQL conformance`, `Core features`, `CHARACTER_LENGTH`, `pg_isready`, `UPDATE FROM`, `savepoint`, `Volcano`, `Cascades`, `Orca`, `Calcite`) now give COVERED.
- **P3**: "Volcano" appears in ARCH only in the reference list, p.114 (title of Graefe's paper [23]); p.49-50 cite Graefe (iterators; exchange iterators) without the word. The Red Book (p.33) uses Volcano as an optimizer generator.
- **P4**: rule 19 of the three prompts (Claude Code, Codex, Copilot): with access to the PDF/text, read the page and only then label `[from source]`; without access, declare the gap and answer labeling `[not verified]` or `[inference]`, without stating it as from the book. The Copilot prompt did not have rules 17-18; they were added for consistency. New label `[not verified]` in the label list.
- **Tests**: 29 new positive and 4 new negative checks in `citation-checks.json` (R12-P01..P29, R12-X01..X04), 14 new `R12-*` cases in `run_script_tests.py`.

## Fix after round 13 (blind test, coverage defects)
- **Multixact (PG16 p.795-796)**: section 2b of `postgresql-16-vacuum-autovacuum-e-armazenamento.md` with members of ~10 GB (more frequent aggressive vacuum) and ~20 GB until wraparound, warnings at 40 million, refusal below 3 million, `relminmxid`/`mxid_age`, the four recovery differences (p.796) and the rest of p.795 (VACUUM FULL, VACUUM FREEZE, single-user mode).
- **Configuration (p.658, p.707)**: vacuum delay formula (`delay * balance / limit`, ceiling of 4 x delay, operations with critical locks do not sleep, delay < 1 ms); `session_replication_role` with `local` = `origin` internally, who can change it (superuser / `SET` privilege), discarding of cached plans and use in logical replication.
- **Table C.1 (p.2624-2648)**: real classifications grouped by PostgreSQL class (reserved without mark, reserved with "requires AS", reserved "can be function or type", non-reserved "cannot be function or type", non-reserved "requires AS", PostgreSQL only), the six words on p.2633 (`HAVING`, `INCLUDE`, `INDEX`, `INITIALLY`, `INNER`, `INOUT`); fixes the solver's imprecision (`INNER` is reserved). Catalog `pg_rewrite` (p.2333), `relhasrules` (p.2308), `pg_rules` (p.2365) and `pg_tables.hasrules` (p.2374).
- **Minor**: version notes E.16 (p.2753-2754) in `postgresql-16-replicacao-logica.md` (section 7b) and `...comandos-reindex...` (section 8g); `REINDEX` p.1998 (exclusion constraint, `SYSTEM`, progress); `postgres -C` p.2279 (section 8f; stopped server for `shared_memory_size_in_huge_pages`); single-expression form of `CREATE STATISTICS` without type (p.1807-1808); exit status 3 and the restore pipe (p.801).
- **Indexes**: 8 new curated topics in `relational_index.json` (`pg-multixact-members-wraparound`, `pg-vacuum-cost-delay-formula`, `pg-session-replication-role`, `pg-catalog-pg-rewrite`, `pg-release-16-logical-replication`, `pg-release-16-utility-commands`, `pg-postgres-c-option`, `pg-psql-restore-exit-status`), `pg-sql-key-words` and `pg-reindex-command` extended; `ref_terms.json` regenerated.
- **Tests**: 18 new positive and 2 new negative checks in `citation-checks.json` (R13-P01..P18, R13-X01..X02) and 22 `R13-*` cases in `run_script_tests.py` (lookups that become COVERED). Environment note: the `IDX` test (reproducibility of `source_terms.json`) fails on this machine only because the fingerprints of the extracted text change with the PyMuPDF version; the content of the indexes is identical.
