# Cassandra, Bigtable and Dynamo: what the collection really contains (2008-2010) `[DATED]`

Convention: `(SIGLA p.N)` = PDF page (see INDEX). **CASS is only the landing page of the 5.0 documentation (*prerelease*)**: a list of sections, with no architecture. All the technical content on Cassandra comes from **STRAUCH p.118-124** (based on Lakshman and Malik, 2008-2010) and is `[DATED]` (Thrift, supercolumns, ZooKeeper, Scuttlebutt etc.). v1 cited "CASS p.1-4" for LSM-tree, gossip, quorum, tombstones and Bloom filters, none of which is in CASS.

## 1. What CASS contains (p.1-4)
Page "Welcome to Apache Cassandra's documentation!": sections Getting started, "What's new in Cassandra 5.0", Overview ("Cassandra's features"), Architecture ("Cassandra's big picture"), Data modeling ("Hint: it's not relational"), CQL, Configuring, Operating, Tools, **Vector Search**, Reference, Troubleshooting, FAQ, Plug-ins, Native Protocols (p.2-3). It also warns that the documentation being viewed is for a pre-release version (p.1). Nothing beyond the index.

## 2. Origin and requirements (STRAUCH p.118-119)
Cassandra adopts ideas from **Dynamo** (Amazon) and **Bigtable** (Google); developed by Facebook for *Inbox Search* and open-sourced in 2008; requirements: large volume and growth, incremental scalability, cost, reliability, hundreds of nodes across several datacenters, high write throughput without sacrificing reads, **no single point of failure**, failures as the norm `[from source]`.

## 3. Data model and API (p.119-120)
Table as a "distributed multi-dimensional map indexed by key"; rows with a string key; per-row operations "atomic per replica"; **column families** defined in advance (few), with columns and **supercolumns** that can be added dynamically; rows may have different numbers of columns; values addressed by (row key, column key, timestamp). API with three operations: `get`, `insert`, `delete`; requests go to any server, which determines the replicas; writes require acknowledgment from a **quorum**; on reads, the client chooses the guarantee: the nearest node or a quorum of responses ("degree of eventual consistency") `[from source]`.

## 4. Architecture (p.120-121)
- **Partitioning**: consistent hashing that **preserves the order** of keys (allows range scans); instead of virtual nodes (as in Dynamo), it measures load and **moves nodes** on the ring (p.120).
- **Replication**: factor per instance; the key's coordinator is the first node clockwise; strategies *Rack Unaware*, *Rack Aware*, *Datacenter Aware* (the last two with a leader elected via **ZooKeeper**); preference list spread across datacenters (p.120-121).
- **Membership and failures**: **Scuttlebutt** gossip protocol and **Φ accrual** failure detector (suspicion level instead of a boolean) (p.121). Node joins and leaves are **explicit** (administrator); a new node computes a random token and announces itself (p.121).

## 5. Persistence and implementation (p.122-123)
Writes go first to a persistent **commit log** and then to an in-memory structure; on reaching a threshold, it is flushed to disk as an **immutable** file; disk writes are sequential and there is a per-key index; background compaction; reads consult memory and files, using one **Bloom filter** per file to avoid useless lookups; the server is "practically lock-free" for reads/writes (p.122). Request routing: identifies the responsible nodes, forwards, fails if they do not answer within the configured time, picks the most recent response by timestamp and **schedules repair** of stale replicas (p.122). Rolling commit log (128 MB at Facebook); "fast-sync" mode risks loss on crash; data files in blocks of 128 keys with a block index (p.123). The names *Memtable*/*SSTable* appear in STRAUCH in the description of LSM-tree (p.32, 48-49) and of Bigtable (p.111, 114-116).
- Lessons learned (p.123-124): add features cautiously; atomic per-row transactions suffice for most cases; the Φ accrual detector detected failures in ~15 s on a 100-node cluster, versus up to 2 minutes in others; monitoring; partial centralization (ZooKeeper) is useful.

## 6. Dynamo and quorum (STRAUCH p.60-64)
**N/R/W**, sloppy quorum, *hinted handoff*, *read repair* and Merkle trees belong to **Dynamo** (STRAUCH p.61-64), described in `hash-consistente-e-particionamento-distribuido.md`. Attributing them to "Cassandra" is `[extrapolation]` (external knowledge about modern Cassandra).

## 7. What is not in the sources
Consistency levels ONE/TWO/QUORUM/ALL and `CONSISTENCY` in CQL; the formula ⌊N/2⌋+1; *tombstones*; vnodes in Cassandra; CQL, SAI, Vector Search in detail (CASS only lists them); "PA/EL". For current Cassandra, use the current documentation.
