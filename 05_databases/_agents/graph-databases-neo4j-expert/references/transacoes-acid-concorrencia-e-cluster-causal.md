# Transactions, recovery, high availability and scale (Neo4j 2.x)

Source: NEO4J ch. 6 ("Nonfunctional Characteristics" part), ch. 4 (clustering) and Appendix A. Pages = **PDF** (printed = N − 18). The file name (`...cluster-causal`) comes from v1; the book does **not** cover Causal Clustering: it describes Neo4j 2.x master-slave HA, which is [DATED].

## 1. Transactions and ACID
- Dependability requires guarantees of durability and accessibility; not every graph database is fully ACID, so you need to know the transactional model of the chosen database; Neo4j is ACID [from source] (NEO4J p.180).
- Transactions in Neo4j are semantically identical to traditional ones: writes occur in a transactional context with *write locks* on the nodes and relationships involved; on success, the changes go to disk and the locks are released; on failure, the writes are discarded and the locks released [from source] (NEO4J p.180-181).
- If two or more transactions try to change the same elements, Neo4j detects a possible deadlock and **serializes** the transactions; writes of one transaction are not visible to others, preserving isolation [from source] (NEO4J p.181).
- The book recalls that distributed *two-phase commit* can cause unavailability in pathological cases, and that the effect of transactions on scalability is much smaller than assumed [from source] (NEO4J p.180).
- ACID definitions from Appendix A: atomic (all or rollback), consistent (database structurally sound), isolated (transactions appear sequential), durable (permanent, even with failures) [from source] (NEO4J p.213).

## 2. Implementation
- Each transaction is an in-memory object that represents the writes; a *lock manager* applies write locks on created, updated and removed nodes and relationships; on rollback the object is discarded and the locks released [from source] (NEO4J p.181).
- Commit uses a *Write Ahead Log*: changes are appended to the active transaction log; on commit a commit entry is written and the log is flushed to disk; only then are the changes applied to the graph and the locks released [from source] (NEO4J p.181).
- Recovery after an unclean shutdown: Neo4j replays the transactions of the most recent active log; since the replay is idempotent, the result is consistent [from source] (NEO4J p.182).
- In a cluster, the recovered replica can ask the master for the newest transactions and apply them by replay [from source] (NEO4J p.182).

## 3. High availability (master-slave, DATED)
- The Neo4j of the time uses a master-slave arrangement: each machine keeps a complete replica of the graph; writes go from the master to the slaves at frequent intervals [from source] (NEO4J p.182).
- Classic topology: writes to the master, reads from the slaves; "asymptotic" scalability for writes (up to the capacity of a single disk) and nearly linear for reads [from source] (NEO4J p.182-183).
- Writing through a slave: it first catches up with the master and the write is transacted synchronously on both instances; greater durability, greater latency (can be an order of magnitude slower) [from source] (NEO4J p.99, p.183).
- Today the recommendation, according to the book, is to send all writes to the master and replicate them via `ha.tx_push_factor` and `ha.tx_push_strategy` [from source] (NEO4J p.99).
- Best-effort replication to an arbitrary number of replicas: since version 1.8 [from source] (NEO4J p.183).
- A long GC on an instance embedded in an HA cluster can trigger a new master election [from source] (NEO4J p.95).
- Coordinators require a majority: redundancy 1 with 3 or 4 instances; redundancy 2 with 5; four is no better than three [from source] (NEO4J p.116).
- Global cluster: restrict master election to a region with slave-only instances via `ha.slave_coordinator_update_mode=none` [from source] (NEO4J p.99-100).
- The cluster as a whole is *eventually consistent*; writes on the master are immediately consistent. To "read your own writes" use consistent routing [from source] (NEO4J p.102).
- Write buffering through a queue to regulate load and maintenance [from source] (NEO4J p.99).

## 4. Scale
- Capacity: Neo4j supported "tens of billions" of nodes, relationships and properties in a graph; the intention of 100 billion+ is a roadmap item of the time [from source] (NEO4J p.185).
- Latency: independent of the total dataset size [from source] (NEO4J p.186).
- Throughput: the graph "scales by doing less work"; O(1) example of publications [from source] (NEO4J p.186-187).
- Once the cluster capacity is exceeded, the graph is divided in the application (*sharding* with a synthetic identifier); it works well if there are natural boundaries (e.g., small per-user graphs in Mozilla Pancake) [from source] (NEO4J p.187).
- "Holy Grail": automatically partitioning a graph across several machines is, in general, NP-hard; no database was provably able to support it [from source] (NEO4J p.187-188).
- *Cache sharding*: route queries to the instance whose cache likely already contains the needed region [from source] (NEO4J p.101).

## 5. What the book does NOT say
- It does not cite the "Read Committed" isolation level, lock-free reads, `Wait-For Graph`, "lock on both nodes when creating a relationship" (it only says "write locks on the nodes and relationships involved"), or "deadlock exception" (it says it serializes).
- It does not mention Paxos, Raft, Core Servers or Read Replicas: those belong to Causal Clustering (Neo4j 3.1+), [extrapolation]/[DATED] relative to the book. Check the current documentation.
- It does not claim durability "even with a power outage" in absolute terms; it describes WAL and replay.
