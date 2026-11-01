# MongoDB: replica sets, sharding and shard key (STRAUCH 2010, MONGO-PAT 2013, MONGO-MAN-H 8.3)

Convention: `(SIGLA p.N)` = PDF page (see INDEX). **Three eras**: STRAUCH describes MongoDB 1.6/1.7 (2010); MONGO-PAT, 2.x (2013); MONGO-MAN-H, version 8.3 (overview, no details). Everything about 2010-2013 internals is `[DATED]`. v1 attributed to "MONGO_MAN_I p.18-25" details (oplog `local.oplog.rs`, idempotence, 2 s heartbeat, 10 s, "Raft-like", `{campo:"hashed"}`, MD5) that **none of the sources contain**.

## 1. Current view (MONGO-MAN-H, 8.3)
Replication with **automatic failover**: if the primary becomes unavailable, the cluster elects a new primary, keeping writes available; several copies on different servers give durability and read capacity. **Sharding** distributes collections by **shard key**, with automatic distribution, *zone sharding* (geographic zones by key ranges) and shard key refinement `[from source]` (MONGO-MAN-H p.3-4; Portuguese version: MONGO-MAN-I p.19-23). No protocol details.

## 2. Replication in 2010 (STRAUCH p.98-100) `[DATED]`
- Asynchronous replication; only one node (the primary) receives writes; reads can go to the primary (strong consistency) or to peers (eventual) (p.98).
- Two approaches: **master-slave** (two servers; permanent failover requires shutting down and restarting both) and **replica sets** ("an elaboration of master/slave with automatic failover and recovery") (p.98-99).
- In a replica set, operations are propagated to the secondaries (operation transfer model) and recorded in a **capped collection**; each operation is identified by the primary server's id and an increasing ordinal number (p.99). Data that must not replicate lives in the special `local` database (p.100).
- Up to **seven** servers per replica set: standard, passive or **arbiter** (votes, stores no data) (p.100).
- Consistency and durability: a write is confirmed only if replicated to the **majority**; the data is already visible on the primary before being confirmed (*read uncommitted* semantics); in a failover, whatever was not replicated is discarded, and the old primary's data requires manual merge; during failover there is no strongly consistent write or read; a primary that does not receive *heartbeats* from at least half of the nodes stops being primary and does not handle writes (p.100). The new primary may force *rollback* on the secondaries (p.100).
- No authentication in replica sets in 1.6 (p.100, 101). MongoDB offers no multiversioning, multi-master or conflict reconciliation, by a decision stated in the documentation of the time (p.104).
- In MONGO-PAT: write concern (`w=0`, `w=1`, `j=True`, `w=N`); the journal writes in "group commits" every 100 ms; the journal does not protect against disk failure, and **replication is the recommended way to obtain real durability** (p.54-55); `read_preference` lets `mongos` read from secondaries when the query is not routable (p.98).

## 3. Sharding in 2010 (STRAUCH p.101-104) `[DATED]`
- Since 1.6: automatic sharding "for thousands of nodes", per collection, preserving **order**; based on replica sets (p.101).
- Components: **shards** (mongod, typically one replica set each), **config servers** (chunk metadata, maintained by 2PC; without them the metadata becomes read-only: writes still happen, but no redistribution) and **mongos** (stateless routers, which query the config servers and merge results) (p.101-102). Minimum setup: 2 shards, 1 config, 1 mongos (p.102).
- *Chunks* are contiguous ranges identified by (collection, minkey, maxkey); they split on reaching the configured size; the **balancer** migrates chunks in the background (p.102).
- The key must be "granular enough": a chunk whose minkey and maxkey are equal cannot be split; compound keys help (p.103). 1.6 limitations: the shard key cannot be changed; writes must include the shard key (p.104).

## 4. Shard key in MONGO-PAT (2013) (p.61-64)
The two criteria of a good key: **balanced inserts** across shards and **routable queries** to a subset of shards. For the event-log case (p.62-64):
- **By time** (timestamp or `ObjectId`): all inserts go to the "high" chunk, that is, to a single shard; write throughput equals that of a single instance, and recent reads concentrate as well (p.62-63).
- **Semi-random key** (hash of `_id`): distributes writes (five shards ≈ five times the capacity), but queries without the key go to **all** shards, and the key and index take extra space (p.62-63).
- **Well-distributed key from the data** (e.g. `path`): balanced writes and selective reads; but all traffic for one `path` falls on the same chunk, which cannot be split (p.63-64).
- **Compound natural + synthetic** (`{path: 1, ssk: 1}`, `ssk` = hash of `_id`): usually balances distribution and routing (p.64).
- "There are no definitive best practices"; the decision is high-impact and **hard or impossible to change later**; test with real data; pre-splitting chunks is an option for very high, predictable insert patterns (p.64).
- Other cases: comments (`node_id` + `slug`/`page`, p.133-134); ads (`site_id`, `zone_id`, p.138); in aggregation, the ideal is for a `$group` to land on a single server (p.61). **Capped** collections cannot be sharded, and the alternative is **TTL** indexes (p.65).

## 5. What the sources do not say
"Raft-like" election and votes of `⌊N/2⌋+1`; 2 s heartbeat, 10 s timeout; the name `local.oplog.rs` and idempotent operations (`$inc` → `$set`); "minimum of three nodes" as a rule; `readPreference = secondaryPreferred`; MD5 in hashed sharding; "range × hashed" as MongoDB 8.3 terms. If the user asks about them, use `[extrapolation]` and the current documentation.
