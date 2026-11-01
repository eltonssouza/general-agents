# Evolution of Stream Systems: 1st vs. 2nd Generation

> Convention: `(STREAM p.N)` = PDF page = printed page (arXiv:2008.00842v2, Jan 14, 2023; 27 pages of text + references through p.30). Authors: Marios Fragkoulis, Paris Carbone, Vasiliki Kalavri, Asterios Katsifodimos (the "s" after "Fragkoulis" in the PDF is an affiliation mark). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. The survey does **not** state the publication venue; it is an arXiv preprint.

## 1. The scope of the survey
[from source] The survey compares the 1st generation (2000s-2010) with the 2nd (2011-2022) on: out-of-order data management, state management, fault tolerance, high availability, load management, elasticity and reconfiguration (STREAM p.1). Fig. 1 draws three generations, but the "3rd generation" appears with a question mark, as a future trend (STREAM p.2). Table 1 groups "2nd-3rd generation" in one column (STREAM p.3).

## 2. 1st generation: DSMS
- [from source] Streaming queries appeared in 1992 (Tapestry); prototypes include TelegraphCQ, Stanford's STREAM, NiagaraCQ, Aurora/Borealis and Gigascope; commercial systems (c. 2004-2010) include IBM System S, Esper, Oracle CQL/CEP and TIBCO, focused on window queries and Complex Event Processing, with *scale-up* architectures and ordered streams (STREAM p.1).
- [from source] The architecture follows that of a DBMS, with an input manager, scheduler, quality monitor and *load shedder* (which drops tuples to meet a target latency); queries compiled into a shared plan; goal of fast results, **possibly approximate** (STREAM p.4).
- [from source] Relational streaming model: the stream is a relation that changes over a common schema (STREAM p.4).

## 3. 2nd generation: distributed dataflow
- [from source] It comes after MapReduce and the popularization of the cloud; focus on distributed, *shared-nothing*, *data-parallel* engines on commodity hardware; Millwheel, Storm, Spark Streaming and Flink expose primitives for computations as dataflow graphs; the Google Dataflow model reintroduced out-of-order processing and *punctuations* (STREAM p.1). Queries are independent, with their own state and dedicated resources; sources are typically replayable and state is persisted in embedded or external storage; they prioritize throughput, robustness and result correctness over low latency (STREAM p.4-5).
- [from source] In the dataflow model, the system imposes no schema beyond the timestamp; three time modes (event, processing, ingestion) (STREAM p.4).

## 4. Table 1 of the survey (faithful summary)
[from source] (STREAM p.3)

| Aspect | 1st generation | 2nd-3rd generation |
|---|---|---|
| Results | approximate or exact | exact |
| Language | SQL extensions, CQL | heavy use of UDFs: Java, Scala, Python, SQL-like |
| Query plans | global, optimized, predefined operators | independent, custom operators |
| Execution | (mostly) scale-up | distributed |
| Parallelism | pipeline | data, pipeline, tasks |
| Time and progress | heartbeats, slack, punctuations | low-watermark, frontiers |
| State | shared in-memory synopses | per query, partitioned, persistent, larger than memory |
| Fault tolerance | focus on HA, limited correctness guarantees | distributed snapshots, exactly-once |
| Load management | load shedding, load-aware scheduling | backpressure, elasticity |

## 5. Notes of caution
- [inference] The survey does not claim "unlimited scale-out", "multi-terabyte states per node", "strict DAG" (it even covers cyclic queries and loops, STREAM p.8) nor that 1st-generation clusters were "static and tightly coupled". These formulations from package v1 were removed.
- [from source] The survey's conclusion: modern systems prioritized correctness and "largely rejected" approximation; SQL extensions for streaming are reappearing; most modern systems build independent per-query plans with little optimization and sharing (STREAM p.26).
- [DATED] The survey is from 2020-2023 (website access dates in July 2020, STREAM p.27); versions, APIs and the systems cited have changed since. Treat system names as a snapshot of their time.

## Terms from the original (checked by tests/audit_tokens.py)
- `scale-up`, `scale-out`, `shared-nothing`, `Millwheel`, `Tapestry`, `punctuations` (STREAM p.1)
- `approximate`, `heartbeats`, `low-watermark`, `frontiers`, `backpressure`, `elasticity` (STREAM p.3)
- `load`, `shedder`, `scheduler` (STREAM p.4)
