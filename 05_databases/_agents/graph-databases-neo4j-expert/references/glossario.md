# Glossary (terms as the book uses them)

Pages = **PDF** of NEO4J (printed = N − 18). Terms that are not in the book are marked.

- **A\***: algorithm that improves on Dijkstra with a heuristic; cost f(n) = g(n) + h(n) [from source] (NEO4J p.199).
- **ACID / BASE**: see `nosql-apendice-e-modelos-de-grafo.md` [from source] (NEO4J p.213-214).
- **Aggregate (aggregate store)**: family that groups document, key-value and column stores [from source] (NEO4J p.222).
- **Anchor**: point in the graph to which part of the pattern is bound by label and properties [from source] (NEO4J p.47).
- **BFS / DFS**: breadth-first / depth-first search [from source] (NEO4J p.189-191).
- **Cache sharding**: routing queries to the instance whose memory likely holds the relevant region of the graph [from source] (NEO4J p.101).
- **Compute engine (graph compute engine)**: technology for global batch algorithms, analogous to data mining and OLAP [from source] (NEO4J p.22, p.25).
- **Core API / Traversal Framework / Kernel API**: Neo4j 2.x stack of programmatic APIs [from source] (NEO4J p.176-179) [DATED].
- **Cypher**: Neo4j's declarative query language, with ASCII patterns [from source] (NEO4J p.45-46).
- **Dijkstra**: shortest path; see `teoria-dos-grafos-e-algoritmos-preditivos.md` [from source] (NEO4J p.191).
- **Structural balance**: preference for balanced triadic closures [from source] (NEO4J p.204-205).
- **Fact (modeling facts as nodes)**: intermediate node that represents the interaction of entities [from source] (NEO4J p.86).
- **Triadic closure**: tendency of two nodes with a common neighbor to connect [from source] (NEO4J p.200).
- **Graph-local query**: query that starts from specific points and traverses the neighborhood [from source] (NEO4J p.126, p.183).
- **Hypergraph / RDF triples**: other graph models [from source] (NEO4J p.225-227).
- **IFA (index-free adjacency)**: each node keeps direct references to its neighbors [from source] (NEO4J p.167).
- **Label**: node role marker, used to group, index and constrain [from source] (NEO4J p.38, p.62).
- **LPG**: labeled property graph [from source] (NEO4J p.22).
- **MERGE**: ensures a pattern is present, reusing or creating [from source] (NEO4J p.49, p.64).
- **Node**: entity with properties and labels [from source] (NEO4J p.44).
- **Pointer chasing**: following pointers in the store during traversal [from source] (NEO4J p.185).
- **Page cache**: off-heap cache (since 2.2), LRU-K [from source] (NEO4J p.175-176).
- **Local bridge**: relationship that is the only channel between groups [from source] (NEO4J p.207).
- **Property**: key-value pair on a node or relationship [from source] (NEO4J p.44-45).
- **Relationship**: named, directed connection between two nodes [from source] (NEO4J p.44).
- **Fixed-size record store**: node, relationship and property files with fixed-size records [from source] (NEO4J p.172).
- **Timeline tree**: Year-Month-Day tree for events [from source] (NEO4J p.90-91).
- **WAL (Write Ahead Log)**: transaction log before applying to the graph [from source] (NEO4J p.181).
- **Supernode / dense node**: the book only mentions "densely connected nodes" as a flag (NEO4J p.172); the concept of supernode is [extrapolation].
- **Read Committed, Raft, Causal Cluster, AllNodesScan**: are **not** in the book [extrapolation]/[DATED].
