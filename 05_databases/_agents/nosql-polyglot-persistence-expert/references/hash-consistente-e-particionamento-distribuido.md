# Consistent hashing, replication by N/R/W and membership

Convention: `(SIGLA p.N)` = PDF page (see INDEX). Main source: STRAUCH (~2010-2011); Dynamo (2007) and Cassandra (2008-2010) described as there.

## 1. Naive partitioning
- Simple mapping `partition = hash(o) mod n`: when nodes join or leave, at least part of the data must be redistributed. In a cache, redistribution can happen implicitly through *cache misses*; in **persistent** storage this is not acceptable, since data missing from the available nodes cannot be reconstructed `[from source]` (STRAUCH p.43).
- "Almost 100% of keys change" is **not** stated by the text. For uniform hashing and n → n+1, the remapped fraction is n/(n+1) (≈ 91% for 10 → 11) `[extrapolation]` (arithmetic).

## 2. Consistent hashing
- Idea by Karger et al. (1997), originally for cache protocols; adopted in distributed hash tables (Chord), some memcached clients and, in the NoSQL world, in Dynamo and Voldemort `[from source]` (STRAUCH p.43).
- Principle (White): hash **objects and machines** with the same function; each machine receives an interval of the function's image; neighbors take over the interval of a departing node and give up part of theirs when a new node joins; the object is assigned to the first node **clockwise** on the ring. Clients compute which node to contact, with no metadata server (like the one in GFS) (STRAUCH p.43-44, figures 3.4-3.5).
- Without refinement, positions are random and the intervals can become unbalanced. Solution: several **virtual nodes** per physical node; the number may depend on CPU, memory and disk capacity. In the White simulation cited (10,000 objects on 10 physical nodes), the standard deviation of the distribution drops from 100% without virtual nodes to 50% with 2-5 and to 5-10% with 500 per physical node `[from source]` (STRAUCH p.44).
- Replication on the ring: with **replication factor r**, the next r **physical** nodes clockwise are responsible for the object (figure 3.7, r = 3) (STRAUCH p.44-45).
- K/N fraction of moved keys: **not** present; "only part of the objects needs to be remapped" is what the text says (p.43). `[extrapolation]` for K/N.
- The output interval 0 to 2^128−1 is **not** cited in STRAUCH; in Dynamo the key is hashed with MD5 (p.59) `[from source]`; the 128-bit conclusion is `[inference]`.

## 3. N, R and W
According to the Voldemort team `[from source]` (STRAUCH p.45-46):
- N = number of replicas; R = machines contacted on a read; W = machines that must participate (block) on a write.
- For a model such as *read-your-own-writes*, **R + W > N** is required.
- A write completed without error guarantees that at least W nodes executed it; if it fails (fewer than W), the state of the data is **unspecified**: if at least one node wrote it, the value tends to propagate to the replicas; if none did, it is lost; for consistency, the client must **reissue** the write. W can be zero for a non-blocking write (note 5, p.46).
- Reading from a quorum of servers (when there are versions to choose from) reduces the ability to balance reads (p.45).
- Dynamo: R + W > N for a "quorum-like" system; since the slowest replica dictates latency, R + W < N is often chosen; for an "authoritative cache" of data in heavier stores, R = 1 and W = N; typical Amazon configuration: **N = 3, R = 2, W = 2**; successful writes require at least W−1 responses besides the coordinator `[from source]` (STRAUCH p.61-62).
- **"Strict" quorum = ⌊N/2⌋+1** and the level names ONE/TWO/QUORUM/ALL do **not** appear in the sources: `[extrapolation]` (modern Cassandra). The "pigeonhole principle" is not there either (it is an `[extrapolation]` argument).
- Dynamo uses **sloppy quorum** and **hinted handoff**: if a node is not reachable during a write, the coordinator replicates to another node, with a hint of the original recipient, which delivers the data when the node returns (STRAUCH p.63).
- *Read repair* (Dynamo): if the coordinator receives an old version from a node, it updates it with the most recent one (p.64). Anti-entropy with **Merkle trees** synchronizes diverging replicas in the background (p.64).

## 4. Membership
- Node join: it announces itself, neighbors adjust ownership, the new node copies data (in bulk, asynchronously) (STRAUCH p.46). Leave: detection (e.g. by gossip, since the node stops responding) and neighbors readjust intervals and replicas (p.47).
- Dynamo: node addition and removal are **explicit** (administrator), propagated by gossip protocol every second; "seed" nodes avoid logical partitions (p.62). Token strategies: T random tokens, T tokens with equal-size partitions, Q/S tokens with equal-size partitions (the current one) (p.63).

## 5. Cassandra in this collection `[DATED]`
- Cassandra partitions by a consistent hash function **that preserves key order** (important for range scans). Unlike Dynamo, it **does not use virtual nodes**: it measures load and **moves nodes** on the ring to balance `[from source]` (STRAUCH p.120). v1's claim, "Cassandra uses VNodes (STRAUCH p.46-48)", contradicts the text. That later versions of Cassandra adopted vnodes is `[extrapolation]`.
- Replication strategies: *Rack Unaware*, *Rack Aware* and *Datacenter Aware*; the last two use ZooKeeper to elect a leader (STRAUCH p.121). The preference list is built to spread replicas across several datacenters (p.64, 121).
