# Index and page map: nosql-polyglot-persistence-expert (v2, audited)

This collection brings together **nine sources** of very different nature and age. Before citing, check the nature of the source (table below): several are **short web page captures** without the technical content that v1 attributed to them.

## Page convention
`(SIGLA p.N)` = **PDF page** (the same numbering as the `=== PAGE N ===` markers of the extracted text). Printed page where one exists:

| Sigla | Work | PDF | Printed page | Nature and age |
|---|---|---|---|---|
| STRAUCH | *NoSQL Databases* (C. Strauch, HdM Stuttgart) | 149 p. | printed = PDF − 4 (from PDF 5 onward; Roman numerals before) | Course paper, ~2010-2011. Describes MongoDB 1.6/1.7, Cassandra 2008-2010, Dynamo 2007. **[DATED]** on products |
| REDIS | *The Little Redis Book* (K. Seguin) | 31 p. | printed = PDF − 1 | Short book; Redis 2.6/2.8/3.0.3 (PDF 4); no Cluster/Sentinel. **[DATED]** |
| MONGO-PAT | *MongoDB Applied Design Patterns* (R. Copeland, O'Reilly, 2013) | 175 p. | printed = PDF − 14 (from PDF 17 onward) | Patterns book; MongoDB 2.x, **no multi-document transactions** |
| MONGO-MAN-H | MongoDB docs: "What is MongoDB?" | 7 p. | n/a | Web capture of the landing page (version 8.3), 2026. Overview only |
| MONGO-MAN-I | same page, in Portuguese | 25 p. | n/a | **It is not the manual's Introduction**: it is the same page as MONGO-MAN-H in pt-BR, with ~1 word per line spread over 25 PDFs. No extra content |
| CASS | Apache Cassandra docs (landing) | 4 p. | n/a | Capture of the landing page of the 5.0 documentation (*prerelease*): section index only. **No technical content** (no LSM, gossip, quorum) |
| COUCH | Apache CouchDB docs, "1.1 Technical Overview" | 8 p. | n/a | Real technical text (p.1-7; p.8 blank); "stable" version with no number |
| ELAST | Elasticsearch Reference (landing) | 4 p. | n/a | Capture of the landing page (9.0+): summary and index only. **No** inverted index, shards or NRT |
| NEO4J-GDB | *Graph Databases*, 2nd ed. (Robinson, Webber, Eifrem, 2015) | 238 p. | printed = PDF − 18 (from PDF 23 onward) | Book; Appendix A (PDF 211-228) is an overview of NoSQL. Source **added in v2** for the graph family |

Other PDFs in folder 05 not used here: `NoSQL-Neo4j-Getting-Started.pdf` (4 p. landing), PostgreSQL 16 (v1 cited "PG16 p.865-875" without support; removed) and `Life-Beyond-Distributed-Transactions.pdf` (the file in the folder is an astrophysics paper, not Helland's article; v1 cited "HELLAND p.1-2").

## Labels
`[from source]` (read on the cited page) · `[inference]` (deduction from what the book says) · `[extrapolation]` (knowledge external to the sources) · `[DATED]` (2010-2015 version/practice that has changed). Literal quotation: at most one, <15 words.

## Reference map
| File | Topics | Key pages |
|---|---|---|
| [origens-e-motivacao-do-nosql.md](origens-e-motivacao-do-nosql.md) | motivations, Stonebraker, criticisms, polyglot persistence | STRAUCH p.5-26; NEO4J-GDB p.211-213 |
| [teorema-cap-e-teorema-pacelc.md](teorema-cap-e-teorema-pacelc.md) | CAP (Brewer), what the book does NOT say (PACELC) | STRAUCH p.34-35 |
| [modelo-base-vs-acid-e-consistencia-eventual.md](modelo-base-vs-acid-e-consistencia-eventual.md) | BASE, eventual consistency, versioning, vector clocks | STRAUCH p.35-41, 60-61; NEO4J-GDB p.213-214 |
| [hash-consistente-e-particionamento-distribuido.md](hash-consistente-e-particionamento-distribuido.md) | consistent hashing, vnodes, N/R/W, membership | STRAUCH p.43-47, 59-64, 120-121 |
| [taxonomia-das-quatro-familias-nosql.md](taxonomia-das-quatro-familias-nosql.md) | classifications, families, graphs | STRAUCH p.27-33; NEO4J-GDB p.23-24, 167-169, 211-225 |
| [redis-estruturas-de-dados-em-memoria.md](redis-estruturas-de-dados-em-memoria.md) | 5 structures, transactions, expiration, Lua | REDIS p.7-27 |
| [redis-persistencia-rdb-e-aof.md](redis-persistencia-rdb-e-aof.md) | persistence, replication, backup, cluster [DATED] | REDIS p.9, 29-30; STRAUCH p.32, 71 |
| [mongodb-modelo-de-documentos-e-bson.md](mongodb-modelo-de-documentos-e-bson.md) | documents, BSON, polymorphism, 16 MB, GridFS | MONGO-PAT p.17-37, 117; MONGO-MAN-H p.2-3 |
| [mongodb-padroes-de-modelagem-embedding-vs-referencing.md](mongodb-padroes-de-modelagem-embedding-vs-referencing.md) | embed × reference, simulated transactions, hybrid comments | MONGO-PAT p.17-29, 39-47, 125-134 |
| [mongodb-alta-disponibilidade-e-sharding.md](mongodb-alta-disponibilidade-e-sharding.md) | replica set, sharding, shard key, current × 2010-2013 | STRAUCH p.98-104; MONGO-PAT p.62-64; MONGO-MAN-H p.3-4 |
| [apache-cassandra-wide-column-e-quorum.md](apache-cassandra-wide-column-e-quorum.md) | Cassandra 2008-2010, Dynamo, Bigtable, quorum | STRAUCH p.60-64, 108-124; CASS p.2 |
| [couchdb-e-elasticsearch-visoes-especializadas.md](couchdb-e-elasticsearch-visoes-especializadas.md) | CouchDB, Elasticsearch (limits of the source) | COUCH p.1-7; STRAUCH p.73-79; ELAST p.1-2 |
| [casos-e-antipadroes.md](casos-e-antipadroes.md) | anti-patterns with support in the sources | various |
| [procedimentos.md](procedimentos.md) | decision and review playbooks | various |
| [glossario.md](glossario.md) | terms | various |

## What the sources do NOT contain (`not_in_book`)
PACELC/Abadi and the PA/EL, PC/EC classification of products; "P is non-negotiable"; the Gilbert-Lynch proof (only in the bibliography, p.126); *monotonic write consistency*; the K/N fraction of moved keys; Redis: event loop/epoll, fork/copy-on-write, BGSAVE, `appendfsync` and BGREWRITEAOF, SkipList, the 512 MB limit, `maxmemory`/eviction policies, Sentinel, Redis Cluster (the book says it does not exist yet); MongoDB: the 12-byte ObjectId and its fields, Decimal128, the `local.oplog.rs` oplog and idempotence, 2 s heartbeats and 10 s timeout, "Raft-like" election, hash sharding `{field:"hashed"}`, WiredTiger, `$lookup`, "Subset Pattern" and "Extended Reference Pattern" under those names; Cassandra: Memtable/SSTable/CommitLog in CASS (they are in STRAUCH p.48, 122), tombstones, hinted handoff **of Cassandra** (it is in STRAUCH p.63 for Dynamo), ONE/QUORUM/ALL levels, vnodes in Cassandra (the book says Cassandra moves nodes on the ring, p.120); CouchDB: the `_rev` field, HTTP 409, `/_replicate`; Elasticsearch: inverted index, analyzers, primary/replica shards, 1 s `refresh`, BM25; graphs: "fraud detection" as a listed use case (only an occasional example in NEO4J-GDB p.36, 42), knowledge graphs, GBAC; Fowler as author of polyglot persistence (STRAUCH p.26 attributes the suggestion to Scofield, who says he did not coin the term).

## Scripts (`scripts/`, Python 3 stdlib, no network; use `python -I`)
`nosql_lookup.py` (+ `nosql_index.json`), `cap_classifier.py`, `quorum_calc.py`, `mongo_selector.py`, `verify_citations.py` (+ `citation-checks.json`). Tests in `tests/` (`run_script_tests.py`, `audit_tokens.py`).
