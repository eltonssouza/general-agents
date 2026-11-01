# Index-free adjacency (IFA) and performance

Source: NEO4J. Pages = **PDF** (printed = N − 18).

## 1. Definition and the book's position
- There are two properties to evaluate in a graph database: the storage (native, or serialized into another database) and the processing engine. Some definitions require *index-free adjacency* (connected nodes physically "point" to each other); the book takes a broader view and calls **native graph processing** whatever uses IFA [from source] (NEO4J p.23).
- Native storage and processing are "neither good nor bad", they are engineering trade-offs: the native one is built for performance and scalability; the non-native one relies on a mature backend (the book cites MySQL) that operations teams already know [from source] (NEO4J p.24).
- IFA benefits traversal performance, **but at the cost of making some queries that do not use traversal difficult or memory-intensive** [from source] (NEO4J p.24).

## 2. Mechanism and costs the book states
- In an engine with IFA each node keeps direct references to its neighbors and acts as a local "micro-index", much cheaper than a global index; query time does not depend on the total size of the graph, but on the part traversed [from source] (NEO4J p.167-168).
- A non-native engine links nodes through (global) indexes; each traversal gains a layer of indirection [from source] (NEO4J p.168).
- Costs cited: an index lookup may cost O(log n) versus O(1) to obtain immediate relationships; traversing m steps costs O(m log n) with an index versus O(m) with IFA [from source] (NEO4J p.168).
- Reverse direction: "who is Alice's friend" costs O(log n) for her friends, but O(m log n) in the opposite direction with indexes; without a reverse index, it is an O(n) scan. With IFA, following incoming or outgoing relationships costs O(1) each [from source] (NEO4J p.169-170).
- In practice performance can be worse than the theory, because the graph and the indexes compete for caches and I/O [from source] (NEO4J p.169).
- The book states that, for 2nd- or 3rd-degree queries, the gain shows up with sets of a few thousand nodes [from source] (NEO4J p.185).

## 3. The book's empirical evidence
- Experiment by Partner and Vukotic (*Neo4j in Action*): friends of friends up to depth 5, 1,000,000 people, ~50 friends each (Table 2-1). RDBMS: 0.016 s (depth 2), 30.267 s (3), 1543.505 s (4), did not finish (5). Neo4j: 0.01 s, 0.168 s, 1.359 s, 2.132 s [from source] (NEO4J p.38-39).
- At depth 5 "almost the entire network is a friend"; in real cases the results would be filtered [from source] (NEO4J p.39).
- [DATED] The experiment uses the Traversal Framework of an old Neo4j version and hardware of the time; do not use the numbers as a current benchmark.

## 4. Indexes still exist
- In most queries the index only locates the starting node(s); the rest is "pointer chasing" and pattern matching, so performance does not depend on the total dataset size [from source] (NEO4J p.185-186).
- It is also sensible to tune the graph structure to the queries even with little data [from source] (NEO4J p.186).

## 5. What the book does NOT say
- It does not use the notation O(k^d), nor O(k^d · log N); the "k^d" form is [inference] (average degree k, depth d: number of nodes visited) and the script `scripts/ifa_cost_calc.py` labels it as [extrapolation].
- It does not mention a "B+ tree" or index page fan-out. Any B-tree height calculation is [extrapolation].
- The book does not claim that traversal cost is "exactly the same" at any graph size: it says "relatively constant" and "proportional to the part traversed" (NEO4J p.26).
