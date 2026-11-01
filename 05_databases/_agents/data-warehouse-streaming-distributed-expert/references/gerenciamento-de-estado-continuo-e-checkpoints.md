# Continuous State, Persistence and Checkpoints

> Convention: `(STREAM p.N)` = PDF page = printed page. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. What state is
[from source] State captures the internal side effects of a continuous computation: active windows, record buckets, partial/incremental aggregates and user-defined variables (STREAM p.11). In DSMSs, state was "synopses" defined by the system for internal operators; in post-MapReduce systems such as Storm, there was often no state management, which was left to the programmer (local memory or external storage such as Redis) (STREAM p.12). Today most allow user-defined state managed by the system, with the limitation of less direct control over the structures (STREAM p.12-13).

## 2. Three state architectures (Fig. 4)
[from source] (STREAM p.13)
- **In-memory**: state in in-memory structures; limited to the main memory available on each node.
- **Out-of-core**: several storage tiers (including non-volatile memory); keeps fast memory access and supports a growing number of entries archived in secondary storage. The survey notes that the structure chosen in most systems is a variant of the **LSM-Tree**, such as FASTER or **RocksDB**/LevelDB.
- **External**: decouples computation and state, delegating to an external key-value database/store; reuses database properties (ACID transactions, consistency), is more modular and cloud-friendly; however, the operator has to query the external system, "dramatically" increasing latency. Storm made heavy use of external state; Millwheel (the Dataflow cloud engine) is an example of system-managed external state, on top of BigTable and Spanner, with a transactional commit of each output and state update.

[inference] The points "RocksDB runs outside the JVM heap" and "eliminates garbage collector pauses" are general knowledge about Flink/RocksDB, **not** from the survey (which only cites garbage collection as a stall factor in availability, STREAM p.21). Label them [extrapolation]. "Multiple terabytes per node", "nanosecond latency" and Cassandra are also **not** in the text.

## 3. Persistence granularity (Table 3)
[from source] (STREAM p.12-13): some older systems do not persist state (Aurora/Borealis relied on duplicated/standby operators); most today use coarse-grained persistence:
- **Epoch-level**: application-level snapshots, typically asynchronous consistent ones (Chandy-Lamport): at each epoch (periodically or after N records) each operator copies its state. Table 3 classifies Flink, Kafka Streams, Samza, Naiad, SEEP, TimeStream, Streamscope as epoch-level.
- **Batch-level**: strict micro-batching (Spark Streaming, Trident); S-Store orchestrates batches as ACID transactions on a relational database.
- **Record-level**: Millwheel persists each operator's state transition at every output.

## 4. Partitioned and global state
[from source] **Partitioned** (keyed) state is the de facto form for data-parallel computation: an operation such as keyBy (Flink) or groupBy (Beam, Kafka Streams) raises the scope from task to key; at the physical level, several keys or ranges go to one task. **Non-partitioned** (global) state is a singleton per physical task (global aggregates, read offsets); it does not scale and must be used with caution (STREAM p.14).

## 5. Consistency and persistence
- [from source] Before coordinated snapshots, the *lambda architecture* separated layers: Hadoop and transactional databases for what needed guarantees; streaming for low latency, without clear guarantees (e.g. Storm only knew which events had been processed and re-executed on timeout) (STREAM p.14).
- [from source] A stream processor is a distributed system of tasks: sources (read from replayable partitioned logs, such as Kafka), sinks (output commit) and per-task state; if an action is lost or occurs twice, the system becomes inconsistent (STREAM p.14-15).
- [from source] **Per-event persistence** (Millwheel/BigTable): one transaction per local action (inputs, state transitions, generated outputs, the "strong production"); it seems to cause high latency, but WAL, blind writes, bloom filters and batch commits reduce the cost; since the order is defined at commit, execution is deterministic (STREAM p.15). [inference] v1 said "a few thousand events/s": an invented number.
- [from source] **Per-epoch persistence**: divides the computation into mini-batches (epochs); the state of the whole graph is committed after each epoch; on a failure, it rolls back to the previously committed epoch. "Exactly-once" here means each epoch being committed atomically ("exactly-once on state") (STREAM p.15).
  - *Strict two-phase commit*: phase 1 = process the epoch; phase 2 = persist the state; popularized by Spark (micro-batching); drawback: low utilization due to synchronous execution; Drizzle chains epochs into one commit; S-Store uses one database transaction per epoch (STREAM p.15).
  - *Asynchronous commit by consistent snapshot*: for pure dataflow; snapshot algorithms do not require pausing the application (STREAM p.15-16).
- [from source] **Unaligned snapshots (Chandy-Lamport)**: a marker in the stream separates actions before and after the snapshot; supported by IBM Streams and Flink; requires recording *in-flight* events and reprocessing them on recovery. **Aligned**: prioritizes the channels expected before the snapshot, so that the state reflects a complete epoch with no in-flight events; Flink's mechanism resembles Chandy-Lamport but adds an alignment phase that partially blocks input channels until all channels deliver the epoch's messages; unaligned = better runtime performance, slower recovery; aligned = slower commits, lower reconfiguration cost (STREAM p.16).
- [inference] The name "ABS (Asynchronous Barrier Snapshotting)" comes from the Flink literature; the survey speaks of "Flink's epoch snapshotting" (STREAM p.16) and does not use the term ABS.

## 6. Practical configuration
[extrapolation] Checkpoint intervals (e.g. 10 s), S3/HDFS directories, the `state.backend` and `enableCheckpointing` flags are engine parameters, depend on the version and are **not** in the survey. Consult the engine's current documentation (see `procedimentos.md`).

## Terms from the original (checked by tests/audit_tokens.py)
- `programmability` (STREAM p.11)
- `synopses`, `Redis` (STREAM p.12)
- `LSM-Tree`, `RocksDB`, `LevelDB`, `FASTER`, `BigTable`, `Spanner`, `epoch-level` (STREAM p.13)
- `keyBy`, `groupBy`, `lambda` (STREAM p.14)
- `Millwheel`, `Drizzle`, `epochs`, `blind` (STREAM p.15)
- `unaligned`, `aligned`, `in-flight`, `Chandy-Lamport`, `alignment` (STREAM p.16)
