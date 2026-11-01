# Index and page map

## Sources and page convention
| Abbreviation | Source | File | Pages (PDF) | Convention |
|---|---|---|---|---|
| KIMBALL | *Kimball Dimensional Modeling Techniques* (Kimball Group; extracted from *The Data Warehouse Toolkit*, 3rd ed., 2013) | `05_databases/Kimball-Dimensional-Modeling-Techniques.pdf` | 24 (cover p.1, table of contents p.2-3, text p.4-24) | **`(KIMBALL p.N)` = PDF page; printed page = N − 3** |
| STREAM | *A Survey on the Evolution of Stream Processing Systems* (Fragkoulis, Carbone, Kalavri, Katsifodimos), arXiv:2008.00842v2 | `05_databases/Stream-Processing-Evolution-Survey-arxiv.pdf` | 30 (text p.1-27, references p.27-30) | `(STREAM p.N)` = PDF page = printed page |
| HELLAND | *Life Beyond Distributed Transactions* (Helland, 2007) | `05_databases/Life-Beyond-Distributed-Transactions.pdf` | 4, **but the file is a different paper (astrophysics, HD 30963)** | **no citable pages**; Helland content = `[extrapolation]` |

Audit checks: the text of the PDFs was extracted page by page with PyMuPDF; Helland p.1-4 deals with stellar spectra. Package v1 used **printed** pages for KIMBALL without declaring it (and with a few errors); all were converted to PDF pages.

## Labels
`[from source]` (read on the cited page), `[inference]` (the agent's deduction from what the book says), `[extrapolation]` (knowledge external to the corpus, including Helland, current Flink/Kafka, Saga, Outbox), `[DATED]` (a snapshot of its time, e.g. system names and versions in the survey, 2020-2023).

## Topic references
| File | Content | Source pages |
|---|---|---|
| `kimball-processo-de-quatro-passos-e-grao.md` | requirements, 4 steps, grain, star, grace extensions | KIMBALL p.4-6, p.14 |
| `familias-de-tabelas-fato-e-aditividade.md` | additivity, 3 grains, factless, aggregate, consolidated, fact techniques | KIMBALL p.7-9, p.18-20, p.22, p.24 |
| `tecnicas-de-dimensoes-chaves-substitutas-e-desnormalizacao.md` | surrogate/durable, degenerate, flattening, snowflake, hierarchies, advanced techniques | KIMBALL p.10-12, p.17, p.21-24 |
| `dimensoes-conformadas-matriz-bus-e-drill-across.md` | conformed, drilling across, value chain, bus | KIMBALL p.13-14 |
| `dimensoes-especiais-role-playing-junk-e-degeneradas.md` | role-playing, junk, degenerate | KIMBALL p.10-12, p.22-23 |
| `slowly-changing-dimensions-scd-tipos-0-a-7.md` | SCD 0-7 | KIMBALL p.15-16 (+ p.20-21, p.23) |
| `regras-de-ouro-e-multipass-sql-kimball.md` | fact-to-fact join, multipass, centipede | KIMBALL p.13, p.18, p.20 |
| `evolucao-de-sistemas-de-stream-1a-vs-2a-geracao.md` | generations, Table 1 | STREAM p.1-5, p.26 |
| `tempo-desordem-e-watermarks-em-streams.md` | time, disorder, slack, heartbeat, watermark, triggers | STREAM p.4-11 |
| `gerenciamento-de-estado-continuo-e-checkpoints.md` | state, LSM/RocksDB, epochs, snapshots | STREAM p.11-16 |
| `tolerancia-a-falhas-e-semanticas-exactly-once.md` | semantics, output commit, replication | STREAM p.17-21 |
| `controle-de-fluxo-backpressure-e-elasticidade.md` | shedding, back-pressure, CFC, elasticity | STREAM p.21-26 |
| `pat-helland-fronteiras-transacionais-e-dados-dentro-fora.md` | Helland (no source in the corpus) | none |
| `casos-e-antipadroes.md`, `procedimentos.md`, `glossario.md` | syntheses with the origin of each item | KIMBALL/STREAM, labeled |

## KIMBALL page map (PDF)
p.4 requirements, workshops, 4 steps, processes · p.5 grain, dimensions, facts, star/OLAP · p.6 grace extensions · p.7 fact structure, additivity, nulls, conformed facts, transactional · p.8 periodic snapshot, accumulating, factless, aggregate · p.9 consolidated · p.10 dimension, surrogate, durable, drilling down, degenerate (start) · p.11 degenerate (end), flattened, multiple hierarchies, flags, nulls, calendar · p.12 role-playing, junk, snowflake, outrigger · p.13 conformed, shrunken, drilling across, value chain, bus architecture · p.14 bus matrix, opportunity/stakeholder · p.15 SCD 0-5 · p.16 SCD 5 (end), 6, 7 · p.17 hierarchies · p.18 fact SK, centipede, numeric values, lag, header/line · p.19 allocation, P&L, currency, units, YTD · p.20 multipass, timespan, late arriving facts · p.21 dim-dim, bridge, behavior tags, study groups · p.22 aggregated facts in dimension, banding, comments, time zones, measure type, step · p.23 hot swappable, generic, audit, late arriving dimensions · p.24 supertype/subtype, real-time, error events.

## STREAM page map (PDF = printed)
p.1 intro, generations · p.2 Fig. 1, contributions · p.3 Table 1, requirements · p.4 data models, time (3 modes), DSMS architecture · p.5 modern architecture; disorder: causes, progress, architectures · p.6 effects, slack, heartbeat · p.7 low-watermark, comparison · p.8 punctuations, pointstamps, cyclic queries · p.9 revision, triggers · p.10 replay, partition-consolidate, 1st vs 2nd, open problems · p.11 Table 2; state (intro) · p.12 Table 3, programmability · p.13 state architectures, granularity · p.14 partitioned state, lambda · p.15 consistency, event vs epoch, 2-phase commit · p.16 unaligned/aligned, 1st vs 2nd in state · p.17 fault tolerance, semantics · p.18 Table 4, replication, output commit · p.19 output commit solutions · p.20 sinks, HA · p.21 HA 1st vs 2nd, open problems, load management (intro) · p.22 shedding, scheduling · p.23 back-pressure, CFC, elasticity · p.24 policies, mechanisms, redistribution · p.25 Table 6, reconfiguration, transfer · p.26 1st vs 2nd, open problems, conclusion · p.27 conclusion (end), references.

## What the corpus does NOT contain (not_in_book)
Tumbling/sliding/session taxonomy; "ABS" as a name; RocksDB outside the JVM heap and GC pauses; Flink/Kafka configuration; Kafka transactions; Reactive Streams; the CAP theorem; Saga/Outbox; Helland (data on the inside/outside, 2PC against availability); SCD type 6 as "1+2+3"; average/ending-balance rules for semi-additive facts; negative keys for unknowns; performance benchmarks of surrogate keys; Data Vault, lakehouse, dbt, medallion. For these the agent answers "the collection does not cover it" or labels `[extrapolation]`.

## Scripts
`scripts/analytics_lookup.py` (+ `analytics_index.json`), `scripts/scd_type_selector.py`, `scripts/stream_semantics_calc.py`, `scripts/entity_boundary_auditor.py`; tests and verifiers in `tests/`.
