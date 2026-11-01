# CAP theorem (Brewer) and what the collection does not contain on PACELC

Convention: `(SIGLA p.N)` = PDF page (see INDEX). Source: STRAUCH (~2010-2011).

## 1. CAP as it appears in STRAUCH
- Eric Brewer presented CAP in the keynote "Towards Robust Distributed Systems" (ACM PODC, 2000), adopted by large web companies and by the NoSQL community `[from source]` (STRAUCH p.34).
- The three letters, summarized via Gray: **Consistency** (after an update, readers see what the writer wrote; the text warns that there are alternatives to this strict notion), **Availability** (the system keeps accepting reads and writes even with nodes down or being upgraded) and **Partition Tolerance** (continuing to operate with "islands" of nodes unable to communicate). There is also the reading that tolerating partitions includes handling the dynamic joining and leaving of nodes `[from source]` (STRAUCH p.34).
- Brewer states that, in a "shared-data system", it is only possible to choose **at most two** of the three `[from source]` (STRAUCH p.34).
- Brewer's criterion: if part of the system needs consistency and partition tolerance, ACID properties are needed; if availability and partition tolerance take priority over consistency, the system is characterized by BASE. Dynamo is available and partition tolerant, but not strictly consistent; **Bigtable** chooses the third alternative (consistent and available) and, for that reason, does not operate fully in the presence of partitions `[from source]` (STRAUCH p.34).
- Brewer's table (STRAUCH p.35) lists, per choice, characteristics and examples:

| Choice | Characteristics cited | Examples cited |
|---|---|---|
| C + A (gives up partitions) | 2PC, cache-validation protocols | single-site databases, cluster databases, LDAP, xFS file system |
| C + P (gives up availability) | pessimistic locking, making minority partitions unavailable | distributed databases, distributed locks, majority protocols |
| A + P (gives up consistency) | expirations/leases, conflict resolution, optimism | Coda, web caching, DNS |

- Brewer concludes that "databases are better at C than at availability" and that wide-area databases cannot have both `[from source]` (STRAUCH p.35).

## 2. How each system behaves, according to STRAUCH (without its own CAP label)
The book does **not** assign CAP/PACELC labels to Cassandra, MongoDB, CouchDB or Redis. It describes mechanisms:
- MongoDB 1.6, replica set: a write is confirmed only if replicated to a majority; a primary that stops receiving heartbeats from at least half of the nodes relinquishes the primary state and stops accepting writes; during failover, strongly consistent writes and reads are not possible (eventually consistent reads are) `[from source]` `[DATED]` (STRAUCH p.100).
- Cassandra: a write requires acknowledgment from a quorum of replicas; on reads, the client chooses the "degree of eventual consistency" `[from source]` `[DATED]` (STRAUCH p.120).
- CouchDB: all replicas are writable and do not replicate by themselves; "strong" consistency is questionable, and version conflicts are resolved on read by the application `[from source]` (STRAUCH p.78).
- Redis: Seguin's book deals with a single server; replication is asynchronous master-slave and reads on slaves may be slightly stale `[from source]` (REDIS p.29). STRAUCH notes that Redis offers no fault tolerance and loses in-memory data if the server crashes `[from source]` (STRAUCH p.25, footnote 10).

## 3. Product labels and PACELC: only as extrapolation
- **PACELC** (Abadi: if there is a partition, A or C; else, latency or consistency) **is not** in any of the sources (the acronym does not appear in STRAUCH; Abadi's name appears only in bibliographic references on other topics, p.129, 139, 148). `[extrapolation]`
- "P is non-negotiable; the real choice is CP × AP" is a later reading of CAP (post-2010 literature). STRAUCH's text lists the C+A choice as valid for single-site or cluster systems. `[extrapolation]`
- Classifications such as "Cassandra PA/EL", "MongoDB PC/EC", "CouchDB PA/EC", "Redis PA/EL" and "PostgreSQL PC/EC" are **`[extrapolation]`** (external knowledge, depend on configuration and version); v1 presented them as `[from source]` and cited "PG16 p.865-875" without support. `scripts/cap_classifier.py` shows the origin of each line.
- Formal proof (Gilbert and Lynch, 2002) and linearizability: appear only as suggested reading (STRAUCH p.126), without exposition.

## 4. Practical use
Asking "what happens to reads and writes when the network partitions, and who decides?" is a good heuristic `[inference]`; the answer comes from the mechanisms of the version in use, not from the label. For current MongoDB, the behavior differs from that described in 2010 (see `mongodb-alta-disponibilidade-e-sharding.md`).
