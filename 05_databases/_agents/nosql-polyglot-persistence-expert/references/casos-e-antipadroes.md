# Cases and anti-patterns supported by the sources

Convention: `(SIGLA p.N)` = PDF page (see INDEX). Each item carries the page; whatever is external knowledge is labeled. Ages: STRAUCH 2010, MONGO-PAT 2013, REDIS ~2015 (`[DATED]` where indicated).

## 1. Unbounded-growth embedded array (MongoDB)
- **Problem**: embedding comments, messages or logs in an array of the parent document `[from source]` (MONGO-PAT p.26-27, 128-131).
- **Consequences in the book**: a larger document takes more RAM and reduces how many fit in cache (more page faults and random I/O); growing documents are copied to larger spaces, which slows updates; the 16 MB cap exists; the text says that memory and copying usually hurt **before** the cap (MONGO-PAT p.26-27). Embedding all comments also limits their number to the document size (p.125).
- **Remediation in the book**: one document per comment, or the **hybrid** design of "buckets" of about 100 (MONGO-PAT p.125, 131-133). Naming this "Parent-Referencing" or "Subset Pattern" is `[extrapolation]`.

## 2. Monotonically increasing shard key (time or ObjectId)
- A key based on timestamp or `ObjectId` sends all inserts to the "high" chunk, therefore to a single shard; write throughput becomes that of a single instance; recent reads also concentrate `[from source]` (MONGO-PAT p.62-63).
- A hashed key distributes writes, but queries without the key go to all shards (p.63). A key with few values produces an indivisible chunk (MONGO-PAT p.63-64; STRAUCH p.103). Natural+synthetic combination (p.64).
- "Never use X" is interpretation; the book says there are no definitive best practices and that you should test with real data (p.64) `[from source]`. v1's claim of "100% of writes" and "9 idle shards" is `[extrapolation]`.

## 3. Weak quorum and a write that "seems" to have worked
- For a model such as *read-your-own-writes*, R + W > N is needed; with R + W ≤ N, reads may go to replicas lacking the write `[from source]` (STRAUCH p.46; Dynamo p.61-62, where choosing R + W < N for latency is acknowledged).
- A write that fails (fewer than W nodes) leaves an **unspecified** state: the client must reissue it (STRAUCH p.46). Writing with W = 0 gives no guarantee of success (p.46, note 5). In MongoDB 2.x, `w=0` does not wait for acknowledgment and may lose events without warning (MONGO-PAT p.54).

## 4. Redis: `keys` in production, duplicating objects, long scripts
- `keys` does a linear scan and **must not be used in production code**; alternatives: organize into hashes or use `scan` (2.8) (REDIS p.19, 23-24) `[from source]`.
- Duplicating the object under two keys (id and e-mail) is "a nightmare to maintain and doubles memory"; use a hash as a secondary index (REDIS p.16).
- `monitor` is for debugging, be careful in production; `slowlog` lives in memory (p.21). Lua: `lua-time-limit` limit (5 s by default), consider reducing it (p.27).
- `[DATED]`: there is no automatic slave failover (p.29); Redis Cluster did not yet exist in the book (p.29-30).
- Eviction and `maxmemory`: **not** in the collection (`[extrapolation]`).

## 5. Over-normalizing in MongoDB
The book warns against reproducing in MongoDB the design one would use in a relational database (not "super-normalizing") and says polymorphic schemas and good embedding take advantage of the model (MONGO-PAT p.22, 37). But it also shows when referencing is better (flexible querying, high arity, M:N) (p.25-28). The figure "10 to 50 round-trips per screen" from v1 is not in the book. The extra latency of two trips to the database when referencing is described in p.23.

## 6. Implementing 2PC in the application unnecessarily
The book warns that it is "very easy" to forget failure scenarios and race conditions when designing 2PC in the application; rule of thumb: structure the schema so that atomic updates stay within a single document (MONGO-PAT p.44) `[from source]`. `[DATED]`: today MongoDB has multi-document transactions (MONGO-MAN-H p.3).

## 7. Treating a CAP/PACELC label as a property of the product
Labels such as "Cassandra is PA/EL" are `[extrapolation]`: behavior depends on configuration and version (see `teorema-cap-e-teorema-pacelc.md`). In STRAUCH, mechanisms such as write quorum and choice of consistency on reads (p.120) and majority in the replica set (p.100) are what describe the behavior.

## 8. Using a single database "for everything" or "NoSQL for everything"
STRAUCH insists that no solution serves everything and cites choices by need (reporting and ACID: relational; counters: Redis; etc.) (STRAUCH p.5, 8, 25-26). Polyglot persistence is the associated idea (p.26); the price is dealing with different consistency and operational models `[inference]`.

## 9. NoSQL query injection
Building queries by string concatenation or accepting operators coming from user input (`$where`, `$gt`) is an injection risk. The sources do **not** address this (v1 had no page): `[extrapolation]`, general good practice: type and validate parameters and block operators.
