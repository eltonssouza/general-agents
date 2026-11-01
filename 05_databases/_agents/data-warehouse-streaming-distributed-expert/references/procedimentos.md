# Procedures (derived checklists)

> Convention: `(KIMBALL p.N)` and `(STREAM p.N)` = PDF page. These procedures are **syntheses by the agent**: each step gives what comes from the book (with page) and what is external practice `[extrapolation]`. Engine syntax (Flink etc.) varies by version: confirm in the current documentation.

## P1. Design a dimensional model (four steps)
1. [from source] Gather requirements and data realities; hold collaborative workshops (KIMBALL p.4).
2. [from source] Choose the business process (KIMBALL p.4).
3. [from source] Declare the grain, preferably atomic; one grain per physical table (KIMBALL p.5).
4. [from source] Choose dimensions consistent with the grain and facts consistent with the grain (KIMBALL p.5).
5. [from source] Ensure surrogate keys on the dimensions (except date), default rows for unknown and flattened dimensions (KIMBALL p.7, p.10-11).
6. [from source] Record the process in the bus matrix; conform dimensions; deliver one row at a time (KIMBALL p.13-14).

## P2. Choose the SCD type (the agent's decision tree)
Ask, for each attribute: should the value change?
- No, never: type 0 [from source] (KIMBALL p.15).
- Yes, without needing the history: type 1; remember to recalculate aggregates and cubes [from source] (KIMBALL p.15).
- Yes, with full history: type 2; at least 3 columns (effective, expiration, current) and a new surrogate [from source] (KIMBALL p.15).
- Only the previous value: type 3, "relatively little" used [from source] (KIMBALL p.15).
- A group of attributes that changes fast in a huge dimension: type 4 (mini-dimension) [from source] (KIMBALL p.15).
- Needs history and the current value: type 5, 6 or 7 [from source] (KIMBALL p.15-16).
The choice among these is the agent's [inference]; the book describes each technique, it does not prescribe a tree.

Type 2 SQL example `[extrapolation]` (generic dialect; values such as `9999-12-31` are an external convention):
```sql
UPDATE dim_cliente SET row_expiration_date = CURRENT_DATE, is_current = 'N'
WHERE cliente_natural_id = 'X' AND is_current = 'Y';
INSERT INTO dim_cliente (cliente_natural_id, cidade, row_effective_date, row_expiration_date, is_current)
VALUES ('X', 'Nova Cidade', CURRENT_DATE, DATE '9999-12-31', 'Y');
```
[from source] When loading the fact, the surrogate valid on the event date is used (late arriving facts require looking up the key that was valid at the time) (KIMBALL p.15, p.20).

## P3. Report that crosses two processes
1. [from source] Do not join facts directly (KIMBALL p.20).
2. [from source] Choose attributes of conformed dimensions as headers (KIMBALL p.13).
3. [from source] One query per fact; merge by sort-merge on the headers (KIMBALL p.13, p.20).
4. [extrapolation] In SQL, a `FULL OUTER JOIN` of two aggregated subqueries; alternative: a consolidated fact table if the grain is the same (consolidated: KIMBALL p.9).

## P4. Checklist for a streaming pipeline
1. Which time mode? [from source] event, processing or ingestion (STREAM p.4); processing time produces nondeterminism (STREAM p.17).
2. How is progress measured and late data handled? [from source] slack, heartbeat, low-watermark, triggers/revision (STREAM p.6-9). Numeric value of the allowed lateness: measure the distribution of actual lateness in your stream [extrapolation].
3. State: memory, out-of-core (LSM/RocksDB) or external; partitioned by key (STREAM p.13-14).
4. Persistence: per record, epoch or batch (STREAM p.13, p.15); aligned/unaligned snapshots (STREAM p.16).
5. Semantics: at-least-once or exactly-once on state; and the output? output commit problem and sink (STREAM p.17-20).
6. Load: back-pressure with a persistent queue, shedding only if approximation is acceptable, elasticity with policy/mechanism (STREAM p.21-25).
7. Engine configuration (checkpoint intervals, state backend, side outputs): [extrapolation] per the documentation of the version in use. v1 brought Flink Java code and `state.backend: rocksdb` as if from the book; it was removed because it is not in the survey and varies by version.

## P5. Bridge to Helland (source absent)
[extrapolation] Architecture review questions: where are the consistency boundaries? is there a distributed transaction? do receivers tolerate duplicates? Use `scripts/entity_boundary_auditor.py` as a checklist, not as an authority.
