# Fidelity report: nosql-polyglot-persistence-expert (v1 → v2 audit)

Audit date: 2026-10-26. Convention: `(SIGLA p.N)` = PDF page (see `references/INDEX.md`). This report **replaces** the one from v1, which declared "19 of 19 passed (100%)" by validating only that the page range existed. That approval had no basis: 82% of the key terms checked automatically were not on the cited page.

## 1. Source inventory
| Acronym | Work | PDF | Real nature |
|---|---|---|---|
| STRAUCH | *NoSQL Databases* (Strauch) | 149 p. | course paper ~2010-2011; printed = PDF − 4 |
| REDIS | *The Little Redis Book* | 31 p. | Redis ~3.0.3; printed = PDF − 1 |
| MONGO-PAT | *MongoDB Applied Design Patterns* (2013) | 175 p. | book; printed = PDF − 14 |
| MONGO-MAN-H | MongoDB "What is MongoDB?" (8.3) | 7 p. | web capture, overview only |
| MONGO-MAN-I | same page in pt-BR | 25 p. | **not** the manual's Introduction; ~1 word per line |
| CASS | Cassandra docs 5.0 | 4 p. | **landing page**, no technical content |
| COUCH | CouchDB Technical Overview | 8 p. | real technical text (p.8 empty) |
| ELAST | Elasticsearch Reference | 4 p. | **landing page**, no technical content |
| NEO4J-GDB | *Graph Databases* 2e | 238 p. | added in v2 (Appendix A: NoSQL overview; graph internals) |

v1 convention: page ranges without declaring PDF × printed; in practice, arbitrary numbers (the CASS text has 4 pages and was cited as "p.1-4" for LSM, gossip and quorum). In v2: **PDF**, with an offset map. Also found: the PDF `Life-Beyond-Distributed-Transactions.pdf` in folder 05 is an astrophysics paper (v1 cited "HELLAND p.1-2"); I did not change PDFs.

## 2. Automatic audit findings (v1)
- 431 citations `(SIGLA p.N[-M])` extracted from the v1 package (STRAUCH 149, MONGO_MAN_I 75, REDIS 70, MONGO_PAT 56, CASS 56, COUCH 14, ELAST 11, PG16 2, HELLAND 1). None outside the page range, **but 98 were ranges of 7 or more pages** (not verifiable).
- Key-term check (names, commands, numbers: `gossip`, `oplog`, `BGSAVE`, `_rev`, `16 MB`, `ObjectId`, `quorum` etc.) against the text of the cited pages: **289 checks, 236 failures (82%)**. By source (failures/checks): MONGO_MAN_I 66/72, CASS 51/51, REDIS 45/52, STRAUCH 44/59, MONGO_PAT 16/33, COUCH 8/12, ELAST 6/10. List in `scratch/audit/.../notes/baseline_termfails.json`.

## 3. Manual sample (91 claims from v1, pages read)
Priority: agent prompt, numbers, "always/never", names of patterns/algorithms, comparisons. Covers all 8 cited sources and all 15 reference files. Full list: `scratch/audit/.../notes/10-amostra-manual.txt`.

| Verdict | Count |
|---|---|
| OK (with corrected page) | 3 |
| Wrong page (content exists on another page) | 19 |
| Wrong source or page | 2 |
| Wrong number | 2 |
| Overstatement | 13 |
| **Claim without basis or wrong attribution** | **52** |

Examples of what had no basis (all written as `[from source]`):
1. **PACELC, Abadi and the PA/EL, PC/EC matrix** of five databases, cited to STRAUCH p.34-35, CASS, MONGO_MAN_I, REDIS and "PG16 p.865-875": no source contains PACELC or labels products.
2. **Redis**: single-threaded with epoll, SkipList, 512 MB strings, `fork()`/copy-on-write, `BGSAVE`, `appendfsync always/everysec/no`, `BGREWRITEAOF`, `maxmemory` (REDIS p.1-31): the book only describes snapshot by number of keys and append mode (p.9), manual failover (p.29).
3. **MongoDB "Introduction"**: BSON, 12-byte ObjectId (4+5+3), Decimal128, idempotent `local.oplog.rs` oplog, 2 s heartbeat, 10 s timeout, "Raft-like" election, hashed sharding with MD5, cited to MONGO_MAN_I p.4-25 (which is the home page in pt-BR).
4. **Cassandra** (CASS p.1-4): LSM, Memtable, SSTable, tombstones, gossip, Bloom filters and consistency levels, cited to a documentation landing page; hinted handoff and read repair are from Dynamo (STRAUCH p.63-64); "Cassandra uses VNodes (STRAUCH p.46-48)" **contradicts** STRAUCH p.120 (Cassandra moves nodes on the ring).
5. **Taxonomy**: "four families from STRAUCH p.50-78, including graphs": STRAUCH excludes graphs (p.5, 33); the quadrants are in NEO4J-GDB p.214.
6. **Polyglot persistence "coined by Martin Fowler"** (STRAUCH p.23-25): the text (p.26) attributes the suggestion to Scofield, who says he did not coin the term.
7. **CAP**: "P is non-negotiable", Gilbert-Lynch proof, "C = linearizability" (p.28-35); STRAUCH uses Gray's definition and Brewer's table admits C+A (p.34-35).
8. **MongoDB patterns**: thresholds "< 100" and "> 100", "Subset Pattern", "Extended Reference", "Parent-Referencing" attributed to Copeland (MONGO_PAT p.10-60; pages 10-25 are the preface). The book has embed × reference (p.17-29) and comments in *buckets* of ~100 (p.131).
9. **CouchDB** `_rev`, HTTP 409, `/_replicate`; **Elasticsearch** inverted index, shards, 1 s `refresh`: absent from the sources (COUCH p.1-7; ELAST is a landing page).
10. Wrong numbers: GridFS "255 KB" (book: 256 kB, MONGO-PAT p.117); `save 900 1 / 300 10 / 60 10000` (book: 60 s for 1000+ keys up to 15 min for 9 or fewer, REDIS p.9).

Also in the v1 package: the agent prompt (47 lines) lacked the final sections (when to consult references and scripts, response format, epistemic honesty, boundary, `[DATED]`, anti-injection in its own section); `README` told users to run `nosql_lookup.py "cap"` (the script required `--topic`) and had no installation section; there was no `AGENTS.md` or `.github/agents/`; the scripts embedded as "deterministic" rules without an origin: `cap_classifier.py` (CAP/PACELC product labels), `quorum_calc.py` (⌊N/2⌋+1 and "pigeonhole" as if from the book) and `mongo_selector.py` (rules with nonexistent pages).

## 4. What was fixed (v2)
- **15 `references/` files rewritten** from the pages read (INDEX with page map, nature of each source and `not_in_book` list). The 15 file names were preserved.
- Claims without basis were **removed** or **downgraded** to `[extrapolation]` (PACELC, product labels, ⌊N/2⌋+1, Cassandra levels, Redis persistence details, MongoDB pattern names) or marked `[DATED]` (MongoDB 1.6 and 2013, Redis without Cluster, 2010 Cassandra). Pages corrected to PDF. Real content that was missing was **added**: vector clocks, N/R/W and Dynamo (STRAUCH p.37-46, 56-65), data model and architecture of 2010 Cassandra (p.118-124), 2010 replica set and sharding (p.98-104), simulated transactions and hybrid comments (MONGO-PAT p.39-47, 125-134), Redis transactions, expiration and Lua (REDIS p.18-27), quadrants and graphs (NEO4J-GDB).
- **Agent**: complete prompt (9 sections), labels, boundary, `[DATED]`, anti-injection; `AGENTS.md` (Codex) and `.github/agents/*.agent.md` (Copilot) generated from the same text with `<PKG>`; `plugin.json` 2.0.0; `README` with installation on the three platforms and a notice to check current documentation. YAML descriptions checked with `yaml.safe_load`.
- **Scripts** (all run): `nosql_lookup.py` (JSON index with 39 topics and 16 `not_in_book` entries; prints NOT COVERED / NOT IN THE SOURCE), `cap_classifier.py` (only mechanisms [from source] and `[extrapolation]` labels; shows Brewer's table), `quorum_calc.py` (only STRAUCH's R + W > N; ONE/QUORUM/ALL shortcuts labeled), `mongo_selector.py` (rules with a MONGO-PAT page, no invented thresholds).
- UTF-8 without BOM in all files; no absolute user paths.

## 5. Verifier results (v2)
| Verifier | Result |
|---|---|
| `tests/verify_citations.py` (115 positive, 22 negative, 9 sources) | 0 failures |
| `tests/audit_tokens.py` (363 citations, 130 backticked terms; "not/extrapolation" sections ignored) | 0 failures, 0 near |
| `tests/run_script_tests.py` (40 cases: 24 run scripts, 16 check references) | 0 failures |
| v2 citations outside the page range | 0 |
During construction, the verifiers found and I fixed, in v2: terms spelled differently in the PDF ("sloopy", "directionally"), "oplog" that only exists in a bibliographic title (STRAUCH p.143) and several citations without an explicit acronym that inherited the wrong source.

## 6. Audit coverage (what was NOT audited)
- STRAUCH (149 p.) was read at: p.5-19, 25-40, 43-52, 56-68, 71-78, 91, 98-108, 118-128; I **did not read** p.20-24 (criticism), 41-42, 53-55 (MapReduce), 69-70 (Voldemort), 79-90 and 92-97 (CouchDB: storage; MongoDB 1.6 operations), 109-117 (Bigtable) and the appendix/bibliography (term searches only). MONGO-PAT (175 p.): I read p.16-47, 51-56, 61-66, 89, 117, 125-134 and the afterword/index; I **did not read** the pre-aggregation core (p.66-88), e-commerce, advertising, social networks and games (p.89-165) beyond what was necessary. NEO4J-GDB: Appendix A, ch. 5 (use cases) and the start of ch. 6 were read; the rest (Cypher, modeling, algorithms) was **not** audited or cited.
- REDIS, COUCH, CASS, ELAST, MONGO-MAN-H/I and the Neo4j page were read in full.
- The manual sample (91) and the 115 positive checks cover the topics of all reference files; but syntheses not directly cited may have residual inaccuracies.
- `[extrapolation]` and `[DATED]` were not verified against current documentation (no network).
- The content of PostgreSQL 16 and of Helland's paper was not used (wrong/nonexistent PDF for this agent).

## 7. Limits
- **There was no blind execution by an independent model.** The 28 cases in `casos-de-teste.md` were executed by the auditor: scripts actually run, references checked by code and by reading; the conversational behavior of the agent (format, rejection of false premises, injection resistance) was not measured by an external evaluator.
- The automatic verifiers test terms, not semantics; the manual reading covers a sample, not every sentence.
- v1 had a single "19/19 passed" page: the result can only be reproduced with the PDFs and `PyMuPDF`; the extracted texts are not part of the package (authors' rights).

## 8. Pending
Run a blind evaluation with another model on the 28 cases; extend coverage of STRAUCH p.20-25, 53-55 and 108-117 and of MONGO-PAT use cases; check `[extrapolation]` against current documentation; fix Helland's PDF in folder 05 (out of scope).
