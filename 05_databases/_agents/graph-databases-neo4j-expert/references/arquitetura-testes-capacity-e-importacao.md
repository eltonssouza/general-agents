# Application architecture, testing, capacity planning and import (Neo4j 2.x)

Source: NEO4J ch. 4. Pages = **PDF** (printed = N − 18). Everything here is Neo4j 2.x: [DATED] at several points (legacy REST, server extensions, master-slave HA, `neo4j-import`, `PERIODIC COMMIT`). See `versoes-e-conteudo-datado.md`.

## 1. Embedded vs server
- Neo4j can run embedded (same process as the application) or as a server; embedded is **not** an in-memory database, the data remains durable on disk [from source] (NEO4J p.94).
- Embedded: low latency (no network), choice of APIs (Core API, Traversal Framework and Cypher), explicit transactions; but it is JVM-only, subject to the host application's GC (long pauses affect queries and, in HA, can trigger a new master election) and the application controls the lifecycle [from source] (NEO4J p.94-95).
- Server (the most common mode): REST API with JSON over HTTP, platform independence, scaling independent of the application server, isolation from the application's GC [from source] (NEO4J p.95-96).
- Points of attention: network overhead, the transactional Cypher endpoint that keeps state and recovers orphaned transactions after 60 seconds by default [from source] (NEO4J p.96).
- Server extensions (JAX-RS annotated classes): complex transactions, choice of APIs, encapsulation and response formats; they require a JVM and GC monitoring [from source] (NEO4J p.96-99).
- [DATED] The REST API and server extensions described were replaced in later versions by the Bolt protocol, drivers and procedures; check the current documentation.

## 2. Clustering and load balancing
- Master-slave HA; all writes are coordinated by the master; writing through slaves is up to an order of magnitude slower [from source] (NEO4J p.99).
- Write buffering through queues; multi-region cluster; exclusion from election through `ha.slave_coordinator_update_mode=none` [from source] (NEO4J p.99-100).
- Neo4j does not ship a native load balancer; separate read and write traffic (two balancers if using REST for Cypher, since it uses `POST` for both); the server exposes a URI that indicates who the master is [from source] (NEO4J p.100).
- *Cache sharding* and *read your own writes* [from source] (NEO4J p.101-102).

## 3. Testing
- Develop the model test-first; small example graphs (~10 nodes) describe the normal and the exceptional; tests document the model and become regression tests [from source] (NEO4J p.103-104).
- Example: a network of 10 nodes and 8 `FRIEND`, a distance query with `shortestPath`, expected 4 between Ben and Mike and no result between Ben and Arnold (limit `*..4`) [from source] (NEO4J p.104-107).
- `ImpermanentGraphDatabase` (in memory, for tests only) and tests of server extensions with `ServerControls` [from source] (NEO4J p.105-109).
- Query performance tests: a registered suite, run frequently (CI), in a single thread in-process, with random starting nodes to watch the cold cache warming up [from source] (NEO4J p.109-110).
- Application performance tests: specify percentiles, not averages; example "98% of requests in under 200 ms"; "walking skeleton"; tools Grinder, JMeter and Gatling [from source] (NEO4J p.110-111).
- Representative data: reproduce invariants (min, max and average relationships per node, types, ranges); if possible exceed memory; the Neode tool in the example [from source] (NEO4J p.111-113).

## 4. Capacity planning
- Optimization criteria: cost, performance, redundancy and load [from source] (NEO4J p.113-114).
- Spinning disk: seek of ~6 ms; an SSD gives a gain of roughly 20 times [from source] (NEO4J p.114).
- Three performance levers: JVM heap, the portion of the store mapped in the page cache, faster disks; the "sweet spot" is to map the entire files in the page cache with a modest heap; heaps of 4 to 8 GB are not uncommon and sometimes a smaller heap improves performance (less GC) [from source] (NEO4J p.114-115).
- Guidelines: use the page cache to the maximum; tune the heap by monitoring GC; use fast disks when disk access is unavoidable [from source] (NEO4J p.116).
- If the graph does not fit in memory, consider *cache sharding* [from source] (NEO4J p.115).
- Redundancy: with a protocol that requires a majority, redundancy 1 with 3 or 4 instances and redundancy 2 with 5 [from source] (NEO4J p.116).
- Load (the book's rule of thumb): `concurrent = (1000 / average request time in ms) × cores per machine × number of machines` [from source] (NEO4J p.116).
- Beware of "inflated expectations" when estimating peak requests [from source] (NEO4J p.117).
- The numbers "2-4 GB for the OS", "8-16 GB of heap", "44 GB of page cache on 64 GB" and the v1 `dbms.memory.*` are **not from the book**; any current sizing is [extrapolation].

## 5. Bulk import
- Initial load: `neo4j-import` tool, about 1,000,000 records per second, from CSVs, building the store files outside the transactional path (only consistent at the end) [from source] (NEO4J p.117).
- CSV: headers such as `:ID`, `title`, `year:int`, `:LABEL` (labels separated by `;`); relationships with `:START_ID`, `:END_ID`, `:TYPE` [from source] (NEO4J p.117-118).
- Batch import with `LOAD CSV` for intermediate loads (~1 million items); uses `WITH HEADERS`, `split`, `UNWIND` and `MERGE` in parts [from source] (NEO4J p.118-119).
- Index on properties used by `MERGE` (O(n) vs O(log n)); `DROP INDEX` if it only served the import; temporary IDs removed with `REMOVE` at the end [from source] (NEO4J p.120-121).
- A single `LOAD CSV` transaction can hold gigabytes of state; `USING PERIODIC COMMIT` breaks it into smaller transactions (1000 rows by default, or `USING PERIODIC COMMIT 100`) [from source] (NEO4J p.121).
- [DATED] `neo4j-import` and `USING PERIODIC COMMIT` were replaced by other tools and by the `CALL { } IN TRANSACTIONS` syntax in later versions: check the current documentation.
