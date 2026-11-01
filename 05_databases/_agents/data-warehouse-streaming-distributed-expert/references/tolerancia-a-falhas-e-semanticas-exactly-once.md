# Fault Tolerance, Exactly-Once and the Output Commit Problem

> Convention: `(STREAM p.N)` = PDF page = printed page. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Four dimensions of the survey (Table 4)
[from source] The survey analyzes 18 systems by: (1) processing semantics, (2) replication (active or passive), (3) recovery data (state, output), (4) storage medium (local or remote resilient store, memory) (STREAM p.17-18). Observed patterns: passive replication with state storage is the most popular; storing in-flight tuples has fallen out of use; older systems sought exactly-once on output, recent ones opt for exactly-once on state and outsource output deduplication; a remote resilient store is the most common (STREAM p.18).

## 2. Processing semantics
[from source] The field settled on the terms *at-least-once* and *exactly-once*; *at-most-once* is part of the nomenclature, but is "mostly obsolete", since systems prefer one of the two stronger levels (STREAM p.17).
- **At-least-once**: the same results as a failure-free execution, plus duplicate records as a side effect of recovery (STREAM p.17).
- **Exactly-once** has **two interpretations** (STREAM p.17-18):
  - *Exactly-once on state*: within the system's boundaries, inconsistencies or duplicate execution from recovery are not part of the state. Even so, many systems assume deterministic computations, which is often not the case (processing-time windows and operators with several sources are examples of nondeterminism); Clonos offers exactly-once with nondeterministic computation through causal consistency.
  - *Exactly-once on output*: the system produces the same output as a failure-free execution.
- [from source] A system with exactly-once on state **will still produce duplicate output** on recovery: this is the *output commit problem* (STREAM p.17).
- [inference] v1 said that exactly-once "requires replayable sources + snapshots + transactional or idempotent sinks". The survey says that sources are typically replayable (p.5, p.14-15), that state is restored by snapshot (p.15-16) and that duplicate output is handled by separate techniques (p.18-20); the "end-to-end" combination is a reasonable synthesis by the agent, not a sentence of the book.

## 3. Output commit problem
[from source] It specifies that the system should publish output to the outside world only when it is sure it can recover the state from the point of publication, so that each output is published once, because the output cannot be retracted after it is sent (STREAM p.18). Equivalent terms: *precise recovery*, *strong productions* (STREAM p.18-19).
Solutions, in five categories (STREAM p.19-20):
1. **Transaction-based** (tuple identity): Millwheel (unique id per record, commit in highly available storage, discards retries by id) and Trident (transaction id per batch, assuming ordering of transactions).
2. **Progress-based** (order/timestamps): SEEP, with state and output checkpointing and timestamp vectors; assumes determinism.
3. **Lineage-based** (input-output dependencies): Timestream and Streamscope; assume deterministic input and computation. The progress/lineage solutions are vulnerable to failures of the last operator(s), since they depend on downstream operators to filter duplicates (STREAM p.19).
4. **Special sink operators**: the "Streams" system has sinks that retract output in files/databases; not general.
5. **External sinks**: Streams, Flink and Spark provide exactly-once on state and **outsource** the problem to external sinks with **idempotent** writes, such as Apache Kafka (STREAM p.20).
- [from source] Alternative classification: *optimistic* techniques (publish and retract/update: modifiable or versioned destinations, analogous to MVCC) and *pessimistic* ones (use a kind of write-ahead log of the output until the final commit: transactional sinks) (STREAM p.20).
- [inference] The "2PC sink with pre-commit at the checkpoint" described by v1 is **not** in the survey, which only cites transactional sinks as a pessimistic technique (STREAM p.20) and two-phase commit in the epochs section (STREAM p.15). If the user asks about Kafka transactions, label it [extrapolation].
- [from source] Open problem: the survey considers that the five categories suffer from computational cost, strong assumptions, limited applicability and output freshness (STREAM p.21).

## 4. High availability
[from source] **Active** replication (two instances in parallel; Flux, Borealis), **passive** (checkpoints sent to a standby; SGuard, Clonos checkpoint asynchronously to a distributed file system) and **hybrid** (STREAM p.20). Hwang et al. compare active standby (near-zero recovery, high cost), passive standby, upstream backup (lowest overhead, longer recovery) and amnesia (STREAM p.20). 1st generation: focus on HA with a preference for active replication; modern: passive replication, with on-demand allocation in the cloud (STREAM p.20-21).
- [from source] The survey notes that there is no definition of high availability in the streaming literature and proposes measuring availability by the *slack* between processing time and event time (STREAM p.17, p.21).

## 5. Secondary facts
- [from source] The survey says that "99.999%" is an example of high availability ("like 99.999% or higher") (STREAM p.17); it does not define SLAs.
- [from source] Values such as "90% less overhead" and "66% less recovery time" are results of specific studies cited (STREAM p.20), not general rules.

## Terms from the original (checked by tests/audit_tokens.py)
- `at-least-once`, `exactly-once`, `nondeterminism`, `obsolete` (STREAM p.17)
- `replication`, `retracted` (STREAM p.18)
- `precise`, `transaction-based`, `progress-based`, `lineage-based`, `Trident`, `Timestream` (STREAM p.19)
- `idempotent`, `optimistic`, `pessimistic`, `Kafka` (STREAM p.20)
