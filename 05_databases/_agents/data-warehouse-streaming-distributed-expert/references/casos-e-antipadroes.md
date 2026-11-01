# Practical Cases and Anti-Patterns in DW and Streaming

> Convention: `(KIMBALL p.N)` and `(STREAM p.N)` = PDF page (KIMBALL: printed = N − 3; STREAM: PDF = printed). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. When an anti-pattern comes from the book, the item gives the page; when it is the agent's, it is labeled.

## 1. Data warehouse anti-patterns
| # | Anti-pattern | Fix | Origin |
|---|---|---|---|
| A1 | Direct SQL join between two fact tables on their foreign keys | Drill-across: one query per fact, merged by sort-merge on the conformed headers | [from source] (KIMBALL p.20) |
| A2 | Mixing grains in the same fact table (e.g. header freight repeated on the line) | One grain per physical table; allocate header facts to the lines by a business rule | [from source] (KIMBALL p.5, p.19) |
| A3 | Normalizing the hierarchy into several dimensions attached to the fact (centipede) | Collapse to the lowest grain (e.g. date); junk dimension for flags | [from source] (KIMBALL p.18) |
| A4 | Snowflake: hierarchies normalized into secondary tables | Flattened denormalized dimension (same information) | [from source] (KIMBALL p.12) |
| A5 | Operational system natural key as the dimension PK | Sequential integer surrogate; durable key for the lifetime of the member | [from source] (KIMBALL p.10) |
| A6 | Null foreign key in the fact | Default "unknown/n.a." row in the dimension | [from source] (KIMBALL p.7) |
| A7 | Null dimension attributes | "Unknown"/"Not Applicable" text | [from source] (KIMBALL p.11) |
| A8 | Abstract generic dimension (a single "location"/"person") | Specific dimensions, attributes with distinct labels | [from source] (KIMBALL p.23) |
| A9 | Storing YTD in the fact | Compute in the BI/cube layer | [from source] (KIMBALL p.19) |
| A10 | Designing the model isolated from the business | Collaborative workshops, active governance | [from source] (KIMBALL p.4) |
| A11 | Isolated marts without conformed dimensions | Bus matrix + conformed dimensions; one row at a time | [from source] (KIMBALL p.13-14); the label "data islands" is the agent's [inference] |
| A12 | Using type 1 without recalculating the affected aggregates/cubes | Recalculate | [from source] (KIMBALL p.15) |
| A13 | Generic measure type (collapsing sparse columns) without need | Only if there are hundreds of potential facts and few per row | [from source] (KIMBALL p.22) |

## 2. Stream processing anti-patterns
| # | Anti-pattern | Why / fix | Origin |
|---|---|---|---|
| S1 | Processing-time windows when a reproducible result is wanted | The survey cites processing-time windows as a source of nondeterminism that can make the state diverge on recovery (STREAM p.17); prefer event time with a progress mechanism (STREAM p.4, p.7) | [from source] + [inference] (the recommendation) |
| S2 | Assuming the engine's exactly-once avoids duplicates in an external system | Exactly-once on state still produces duplicate output on recovery (output commit problem) (STREAM p.17-18); use a sink with idempotent writes or the transaction/progress/lineage/sinks technique (STREAM p.19-20) | [from source] |
| S3 | Waiting indefinitely for late data | Blocks output and accumulates state; define a lateness bound (slack/watermark) and a policy for late records (STREAM p.6, p.9) | [from source] |
| S4 | Treating the watermark as an absolute guarantee of completeness | It is a progress indicator, probabilistic (STREAM p.7); decide a policy for late records | [from source] + [inference] |
| S5 | Using load shedding when correctness is critical | Trades accuracy for performance (STREAM p.21); prefer back-pressure/buffering with a persistent queue, or elasticity (STREAM p.21-23) | [from source] |
| S6 | Global (non-partitioned) state at large scale | "Does not scale; use with caution" (STREAM p.14) | [from source] |
| S7 | Treating CPU/memory as the only autoscaling trigger in a multi-tenant cloud | They can induce false positives/negatives (STREAM p.23-24) | [from source] |
| S8 | Assuming reconfiguration is always without downtime | Stop-and-restart is common and halts the pipeline (STREAM p.25) | [from source] |
| S9 | External state on the critical path without measuring latency | The operator has to go to the external system; latency grows a lot (STREAM p.13) | [from source] |

## 3. Distributed anti-patterns (general knowledge, Helland source absent)
- Distributed transaction with 2PC across autonomous services: reduces availability under failures [extrapolation].
- Non-idempotent receiver on an at-least-once channel: duplicates corrupt the state [extrapolation]; the survey covers the streaming analogue (idempotent sinks, STREAM p.20).
- Saga/compensation as a pattern for multi-service flows [extrapolation]; Outbox [extrapolation].
