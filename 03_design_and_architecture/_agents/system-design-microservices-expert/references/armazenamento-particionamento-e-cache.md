# Storage, partitioning, replication, and cache

Main source: SDH (System Design Handbook, AlgoMaster; 75 short pages, many in list format) and MS-CLD (ch. 5). Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.
SDH is a concise summary: it does NOT contain the sharding strategies (range/hash/directory), the B-Tree vs. LSM table, thundering herd/XFetch, "write-behind", or the K/n formula that the previous package attributed to it.

## 1. Databases

- Database types listed: relational, NoSQL, in-memory, graph, time series, spatial. [from source] (SDH p.11)
- SQL: predefined schema, complex queries, ACID (e.g., financial systems), structured data; NoSQL: more flexible/scalable, large volumes, free schema, easy horizontal scaling (MongoDB, Cassandra, Redis). [from source] (SDH p.34) In the interview playbook: relational for structured data with complex relations and ACID; NoSQL for unstructured or semi-structured data, high scale, and eventual consistency; combine databases if subsets have distinct requirements. [from source] (SDH p.55)
- NoSQL models in MS-CLD: document store, key-value, wide-column, graph; NoSQL in general does not give ACID beyond a partition; relational databases scale vertically and use primary/secondary replication (write to the primary, read from the secondaries). [from source] (MS-CLD p.106) (MS-CLD p.108)
- Synchronous vs. asynchronous replication: with synchronous replicas and loss of connectivity the cluster rejects writes; in "highly available" NoSQL the write is accepted and the replicas are updated when possible; consistency tuned by consensus/quorum. [from source] (MS-CLD p.108)
- Sharding divides the data into independent pieces across several servers; it reduces the load per server. [from source] (SDH p.19) Costs: sharding greatly increases operational overhead; table joins, transactions, and referential integrity carry high performance penalties in sharded environments. [from source] (MS-CLD p.108) NoSQL embeds partitioning and routes by placement hints called partition keys. [from source] (MS-CLD p.108)
- Sharding strategies (range, hash, directory), range hotspots, and scatter-gather: NOT in the corpus. [extrapolation] (general knowledge of distributed databases).
- NewSQL: equivalent nodes, any node serves any request (e.g., CockroachDB) with the appearance of a single logical database. [from source] (MS-CLD p.117) (MS-CLD p.118)
- Normalization reduces redundancy and improves integrity; denormalization combines tables to improve queries. [from source] (SDH p.42)
- Database index: a lookup table with indexed values and pointers to the rows, avoiding a table scan. [from source] (SDH p.15)
- B-Tree vs. LSM: SDH does not mention them. EDS observes that traditional brokers use indexes (hash tables or B-trees) to manage acks and remove messages, with an in-memory maintenance cost, whereas Kafka's log is O(1); and that compacted topics work "a bit like simple LSM trees". [from source] (EDS p.34) (EDS p.39) The B-Tree/LSM comparison table (Cassandra/RocksDB...) is general knowledge. [extrapolation]
- Polyglot persistence: each microservice chooses the appropriate store (e.g., relational catalog, cart in a distributed key-value cache). [from source] (MS-CLD p.99) (MS-MIC p.44)

## 2. Cache

- Cache = a fast storage layer with copies of data to reduce latency and relieve the main store. Strategies: read-through (the cache fetches from the store and populates itself), write-through (writes to the cache and the store at the same time; the write only completes when both succeed), write-back (writes to the cache and updates the store later), cache-aside (the application manages reading and populating). [from source] (SDH p.16) (SDH p.32)
- SDH uses the term "write-back", not "write-behind". The playbook tips: write-through for write-intensive applications and read-through for read-intensive ones. [from source] (SDH p.63) [inference] It is a rule of thumb from the book; write-through tends to raise write latency and write-back risks losing data if the cache fails before persisting. [extrapolation]
- Eviction policies: LRU, LFU, FIFO, and TTL. [from source] (SDH p.17) The claim "LRU is the most common industry default" is not in the book. [extrapolation]
- MS-CLD: caching is worthwhile for relatively static data, a slow store, or high contention; it is most effective for immutable data or data that changes little; microservices should be stateless, but a distributed cache can hold session state if indispensable; cache calculation results. Typical architecture: distributed cache as a backing service, invoked by the API Gateway, scaling independently. [from source] (MS-CLD p.118) (MS-CLD p.119)
- Cache-aside in MS-CLD: query the cache; on a miss fetch from the downstream service's database, write to the cache, and return; data must be evicted periodically to keep the cache current. Large caches can be partitioned into a cluster, with nodes added/removed and data rebalanced. [from source] (MS-CLD p.119) (MS-CLD p.120)
- Azure Cache for Redis: structured data, broker, optional persistence. [from source] (MS-CLD p.120) [DATED] (product/tiers change)
- Thundering herd/cache stampede and XFetch: the term "thundering herd" appears in JMG only in the context of retries (JMG p.60); stampede mitigation with locking/probabilistic expiration is NOT in the corpus. [extrapolation]
- Cache-aside can also be criticized for invalidation: SDH merely asks "how to handle cache invalidation" in the interview questions. [from source] (SDH p.57)

## 3. Consistent hashing, Bloom filter, and distributed primitives

- Consistent hashing: distributes data across a cluster so that, when a node joins/leaves, only a small part of the data is reassigned; circular hash space (ring `0..2^n-1`), servers and items are mapped onto the ring by a hash function, and the item goes to the first server found walking clockwise. A server can occupy one or more points of the ring. [from source] (SDH p.18)
- "Virtual nodes", `2^32-1`, the K/n formula, and the problem of modulo hashing invalidating ~100% of the cache are NOT in SDH. [extrapolation] (standard explanation of the technique).
- Bloom filter: probabilistic structure; vector of m bits and k hash functions; a query that finds any bit 0 means "definitely absent"; all 1 means "possibly present" (false positive possible). Usage tip: quickly check an item in a large set. [from source] (SDH p.25) (SDH p.63) "Cassandra/RocksDB use Bloom filters" is not stated. [extrapolation]
- Consensus: Paxos (leader proposes, majority accepts) and Raft (leader manages log replication). [from source] (SDH p.20)
- Heartbeat: periodic message to detect failures; checksum: fingerprint to detect corruption; service discovery: registry as the single source of truth; gossip: epidemic dissemination of information. [from source] (SDH p.22) (SDH p.23) (SDH p.24) (SDH p.26)
- CDN, forward/reverse proxies, and object storage (S3) for media: [from source] (SDH p.12) (SDH p.21) (SDH p.63)

## 4. SDH tips related to data

Use sharding to scale SQL horizontally, index to optimize reads, denormalize for read-heavy workloads, replicate data to avoid SPOF, use a data lake/warehouse for analytics, and distribute across data centers. [from source] (SDH p.62) (SDH p.63) (SDH p.64)

## 5. Out of scope

Internal details of storage engines (B+Tree vs. LSM), Redis/Memcached tuning, resharding strategies, CRDTs (EDS p.120 merely mentions them), SQL and execution plans (see the database packages).
