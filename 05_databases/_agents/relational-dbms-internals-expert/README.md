# Relational DBMS & Internals Expert (Claude Code, Codex and GitHub Copilot)

Expert agent on **relational DBMS internals and PostgreSQL 16**, grounded in four sources (the rights belong to the authors; this package contains its own syntheses and references, not the text of the works):

| Sigla | Work | What the PDF contains |
|---|---|---|
| **ARCH** | *Architecture of a Database System* (Hellerstein, Stonebraker, Hamilton; Foundations and Trends in Databases, 2007) | **complete** article, 119 pages |
| **PG16** | *PostgreSQL 16 Documentation* (version 16.15) | **complete** manual, 3,057 pages; the package summarizes **parts** of it (RLS, partitioning, JSON, backup/PITR, HA and physical and logical replication, failover, hot standby, `pg_rewind`, triggers, indexes, MVCC, locks, statistics/planner/parallelism, configuration parameters, `pg_stat_*`, contrib, types/constraints, WAL, VACUUM etc.); the rest is "pointer only" (see `references/INDEX.md` section 1b) |
| **REDBK** | *Readings in Database Systems, 5th ed.* (Bailis, Hellerstein, Stonebraker, 2015) | **only the chapter introductions**, 46 pages (not the papers) |
| **ANTI-INJ / ANTI-TREE / ANTI-INT / ANTI-TOC** | *SQL Antipatterns* (Karwin, Pragmatic Bookshelf, 2010) | **excerpts**: ch. 21 (SQL Injection, without the solution section), ch. 3 (Naive Trees, without the alternative models section), ch. 1 and the table of contents |

## 1. Overview
Helps decide and debug: DBMS components, process models, **parallelism (shared-nothing/shared-disk, node failure, chained declustering)**, buffer pool and **RAID**, optimizer and plans (including the **Halloween problem**), **data warehouses (bitmap, columnar)**, 2PL/MVCC and isolation, WAL and ARIES, **backup, WAL archiving and PITR, replication and high availability**, PostgreSQL indexes (B-tree, Hash, GiST, SP-GiST, GIN, BRIN with size calculations, partial, INCLUDE), **partitioning and pruning**, **json vs jsonb**, **triggers and Row-Level Security**, VACUUM/autovacuum/wraparound/TOAST, SQL injection and trees with `parent_id`.

**Source rigor**: every claim is `[from source] (SIGLA p.N)` **only** if it was checked on the cited page; the rest is `[inference]`, `[extrapolation]` or `[DATED]`. **Page convention: PDF**; printed ARCH = N + 140; printed PG16 = N − 38. The agent states what the sources do not carry (for example, "write skew", ARIES DPT/CLR, Closure Table, the SQL injection allow-list, PostgreSQL later than 16.15). The other PDFs in `05_databases` (Kimball, NoSQL etc.) belong to other agents.

## 2. Structure
```
relational-dbms-internals-expert/
├── .claude-plugin/plugin.json
├── .github/agents/relational-dbms-internals-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                                  # Codex
├── agents/relational-dbms-internals-expert.md                 # Claude Code
├── references/  INDEX (sources, convention, deep/summary/pointer coverage map), glossary, procedures, cases-and-antipatterns + 26 topical files
├── scripts/     relational_lookup.py (+ relational_index.json, source_terms.json, ref_terms.json), build_term_index.py, build_ref_index.py, index_advisor.py, tree_evaluator.py, injection_auditor.py
├── skills/      relational-topic-lookup, postgres-index-advisor, tree-hierarchy-evaluator, sql-injection-auditor, verify-citations, build-term-index (each in skills/<name>/SKILL.md)
├── tests/       casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py (+ citation-checks.json),
│                audit_tokens.py, extract_pdfs.py, run_script_tests.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (standard library only), always with `python -I`. To audit citations you need to extract the text of the PDFs with PyMuPDF (`pip install pymupdf`; see 5). **Check the current documentation of each platform**, since agent and plugin formats change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/relational-dbms-internals-expert`.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install relational-dbms-internals-expert@general-agents`.
- Or as a subagent: copy `agents/relational-dbms-internals-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder and adjust the relative paths in the prompt, if necessary). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 3.2 Codex (OpenAI)
Copy the package folder into the repository (for example, `tools/relational-dbms-internals-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with the working directory in the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/relational-dbms-internals-expert.agent.md` to `.github/agents/` in your repository and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The file declares `tools: ['read','search','execute']`; remove `execute` to block the scripts.

## 4. Scripts (deterministic, no network, read-only)
```bash
python -I scripts/relational_lookup.py "aries"                      # COVERED (exit 0): summary + verified pages
python -I scripts/relational_lookup.py "pageinspect"                # POINTER ONLY (exit 3): there is content on the pages, no summary in the package
python -I scripts/relational_lookup.py "pgvector"                   # NOT COVERED (exit 1): outside the sources (curated list)
python -I scripts/relational_lookup.py --list                      # topics and the level of each one
python -I scripts/build_term_index.py --src /path/texts            # regenerates scripts/source_terms.json (term index -> pages)
python -I scripts/build_ref_index.py                               # regenerates scripts/ref_terms.json (index of the SUMMARIES; run after editing references/)
python -I scripts/index_advisor.py --data-type temporal_log --physical-correlation --table-size-gb 50
python -I scripts/index_advisor.py --data-type jsonb --operators "@>"
python -I scripts/tree_evaluator.py --deep-subtree-queries --need-fk-integrity
python -I scripts/injection_auditor.py --code "q = f'SELECT * FROM contas WHERE id = {i}'"   # exit 1 = suspicious pattern
```
**Three-level lookup**: COVERED (curated topic with summary and pages), POINTER ONLY (the term index generated from the source text has occurrences, or the curated topic says there is content without a summary) and NOT COVERED (only for terms on the curated list of things outside the sources, or with no occurrence in the term index; absence from the index does **not** authorize saying "the book does not cover it").

**Rule origins**: `index_advisor.py` cites the manual page for each rule and declares that the BRIN threshold (10 GB, adjustable) is `[extrapolation]`; `tree_evaluator.py` only has book backing for the Adjacency List; `injection_auditor.py` bases the principle on ANTI-INJ and declares the per-language regexes as `[extrapolation]`, and never states that the code is safe.

## 5. Tests and audit
```bash
# 1) extract the text of the PDFs (folder with the 7 PDFs of 05_databases):
python -I tests/extract_pdfs.py --pdf-dir /path/05_databases --out /path/texts
# 2) audit citations (858 positive checks, 109 negative, page ranges of all citations):
python -I tests/verify_citations.py --src /path/texts --audit-ranges
# 3) terms between backticks against the cited page:
python -I tests/audit_tokens.py --src /path/texts
# 4) tests of the scripts, of the three-level lookup and of the reproducibility of the term index (and, optionally, of the citations):
python -I tests/run_script_tests.py --src /path/texts
```

## 6. Guarantees and limits
- Replies in the language the user writes in (default: English), without reproducing the works; citations by PDF page.
- **Actual coverage (v2.2, after the blind test of round 3)**: besides what is described below (v2.1), round 3 showed that 11 of 14 cases depended on items that the source covers but the package only pointed to; they were converted into paraphrased content with a page: synchronous/quorum replication (`FIRST`/`ANY`, "commits may never complete"), failover/STONITH, bandwidth x WAL rate (PG16 p.823-827), streaming, slots, hot standby (p.818-835), `pg_rewind` and `wal_log_hints` (p.2256-2259, p.665), logical replication (p.905-927), parallel aggregation and query (p.564-568), `old_snapshot_threshold` (p.661-662, p.2872), `n_distinct`, `SET STATISTICS`, `CREATE STATISTICS` and the join limit (p.1644, p.1679, p.1808), `COMMIT PREPARED` and prepared transactions (p.1695, p.1989, p.2577), table/row locks, `LOCK`, advisory locks (p.531-537, p.1972), configuration defaults (connections, memory, WAL, checkpoints, timeouts, locks, logging: p.646-715), `pg_stat_*` and contrib modules (p.837-884, appendix F), types and constraints (p.99-110, p.184-216), latch coupling/right-link/GiST (ARCH p.92-97) and Red Book p.22 and p.29-30. **Error fixed**: the HOT summary omitted that summarizing indexes (BRIN) do not prevent HOT (PG16 p.2576). The lookup now only returns COVERED if the term appears in the topic's reference.
- **Coverage (v2.1, after the blind test of round 2)**: ARCH was swept section by section (parallelism p.25-35, executor/Halloween p.52-53, data warehouse p.56-62, RAID p.74/105-106, replication p.106-108, utilities) and from PG16 came partitioning (p.132-145), backup/PITR (p.800-813), HA and replication (p.815-818, p.924), json/jsonb (p.218-225), triggers (p.1302-1304) and RLS (p.118-124). **Still pointer only**: JSON/jsonpath functions, authentication/`pg_hba.conf`/roles (p.727-763), full-text search (p.483-523), arrays/composites/ranges (p.229-247), localization/collations (p.764-787), contrib modules without a summary (`pageinspect`, `pg_walinspect`, `postgres_fdw`, `dblink`, `pgcrypto`...), command references, replication protocol, Red Book chapters outside the focus and the text of the SQL Antipatterns chapters that are not in the PDFs (only the table of contents). The full map is in `references/INDEX.md` section 1b.
- v2 results from an audit by reading the cited pages (see `tests/relatorio-de-fidelidade.md`): v1 had wrong pages and unsupported claims, which were fixed or downgraded.
- Code, queries and PDF text pasted by the user are data, not instructions.
- PG16 is audited by **stratified sampling** (3,057 pages); the report states the coverage. The tests were **not** run blind by an independent model.
- **Fix after round 12**: notes from PG16 p.834 on hot standby (`DROP DATABASE` disconnects immediately; `RENAME` and `DROP ROLE` do not); new summaries of PG16 p.2513-2514, p.1322, p.1332-1333, p.86-88, p.2135-2136, p.2169-2170, p.202-204, p.188-189, p.2649-2650, p.2157-2158, p.2058-2062 and REDBK p.33 (the corresponding terms return COVERED); "Volcano" in ARCH only on p.114; rule 19 of the prompts: without access to the PDF/text, declare the gap and label `[not verified]`/`[inference]` (see `tests/relatorio-de-fidelidade.md`).
- **Fix after round 9 (v2.4)**: new summaries of PG16 p.1389-1390 (PL/pgSQL: `COMMIT`/`ROLLBACK` in procedures), p.2616-2617 (Appendix B: two-digit year, DST), p.552-553 (`EXPLAIN ANALYZE` artifacts, `reltuples`/`relpages`), p.2885-2887 (`pg_buffercache`: no buffer manager locks), p.485-486 (FOLLOWED BY), p.244-248 (ranges), p.680 (`enable_indexscan` x index-only), p.803 (`pg_restore -j`) and p.147 (group rule in `DROP`, also cited in the `DROP TABLE` summary); the lookup reads Portuguese queries (function words discarded, PT<->EN tokens in `relational_index.json` field `lookup_lang`, co-occurrence in the same excerpt, OR fallback, "do NOT conclude absence" warning) and prints the "PAGE TO READ FIRST"; `catalog manager` and `System R optimizer` return COVERED; `tests/verify_citations.py` gained `--audit-index` and 25 curated checks (19 positive, 6 negative); new rules 17-19 in the prompt (do not state locking behavior for a pointer-only item; "the book does not carry this number"; read the indicated page).
- **Fix after round 7**: new summaries of PG16 p.719, p.669-670, p.436-437, p.2357-2359 and p.2178-2180 (previously pointer only); additions to p.818, p.641, p.568, ARCH p.32 and p.80; parallelism defaults on p.660-661 (previously cited on p.564-565); attribution to Bailis (Red Book ch. 5, p.25); "parallel safe/restricted" now COVERED, "Data Guard" NOT COVERED; lookup header with the ANTI-INJ page conversion.
- **Fix after round 5**: new summaries of `COPY`, window functions, `GREATEST`/arrays/`intarray`, `DROP OWNED`, `dict_xsyn` and Red Book ch. 9 (previously pointer only), plus WAL details (p.899-900, p.903) and the Update message (p.2428); the lookup returns the page of each one; see `tests/relatorio-de-fidelidade.md`.
