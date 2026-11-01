# Graph theory and predictive analysis

Source: NEO4J ch. 7. Pages = **PDF** (printed = N − 18). The chapter is treated "without resorting to mathematics" for the curious reader [from source] (NEO4J p.189).

## 1. Depth-first and breadth-first search
- Most of the book's queries are depth-first: they follow from a starting node to an end node before repeating along another path; good for following a path and discovering discrete pieces of information [from source] (NEO4J p.189).
- Classic DFS is "uninformed"; since graph databases are semantically rich, a branch can be terminated early; the earlier Cypher queries and Java traversals are of this "informed" kind [from source] (NEO4J p.190).
- BFS explores the graph layer by layer (depth 1, 2, 3...); it is the basis for iterating over the whole graph and for path algorithms; most useful algorithms are not pure BFS, but informed [from source] (NEO4J p.190-191).

## 2. Dijkstra
- Finds the shortest path between two nodes; published in 1956 [from source] (NEO4J p.191).
- Five steps: mark the start as solved (value 0); traverse neighbors breadth-first recording lengths; solve the neighbor with the shortest path (arbitrary tie-break); from the solved set, visit neighbors without revisiting solved ones; repeat until the destination is solved [from source] (NEO4J p.191).
- Efficiency: the best known worst-case implementation is O(|R| + |N| log |N|); the original was O(|R|²) [from source] (NEO4J p.191).
- Guided example: Sydney→Perth in hours, with Canberra, Brisbane, Melbourne, Adelaide, Alice Springs, Cairns and Darwin; result: 50 hours via Adelaide [from source] (NEO4J p.192-198).
- Limitation: the exploration is undirected and may, in pathological topologies, explore the entire graph [from source] (NEO4J p.199).
- In the book Dijkstra is used via Java (`GraphAlgoFactory.dijkstra`, NEO4J p.164), not via Cypher.

## 3. A*
- Improves on Dijkstra by using a heuristic; it combines Dijkstra (nodes close to the origin) and best-first search (nodes close to the destination) and is "provably" optimal for the shortest path [from source] (NEO4J p.199).
- Cost f(n) = g(n) + h(n): g is the cost from the origin to n; h is the heuristic estimate from n to the destination [from source] (NEO4J p.199).
- The book does not cite Euclidean/geodesic distance as a heuristic; it is a common [extrapolation].

## 4. Triadic closure
- In social graphs, if two nodes are connected by a path through a third, the probability that they will connect directly in the future increases [from source] (NEO4J p.200).
- Strong triadic closure property (Granovetter): if A has strong relationships with B and C, then B and C have at least a weak relationship, possibly strong; it is a "bold" claim that does not always hold, but serves as a predictive indicator [from source] (NEO4J p.201).
- Weak/strong is domain-specific; the book does not define them [from source] (NEO4J p.201).
- Example: Alice manages Bob and Charlie; Bob and Charlie are expected to connect (`WORKS_WITH` or `PEER_OF`) [from source] (NEO4J p.201-202).

## 5. Structural balance
- With positive (`WORKS_WITH`, `PEER_OF`) and negative (`MANAGES`, by the book's hypothesis) sentiments, a balanced triadic closure has three positive relationships **or** two negative and one positive [from source] (NEO4J p.205).
- Uncomfortable closures: Alice manages Bob and Charlie and Bob also manages Charlie; or Alice manages Bob who works with Charlie, who also works with Alice [from source] (NEO4J p.203-204).
- Suggested applications: mining electronic communication to predict organizational evolution and possible misconduct [from source] (NEO4J p.206).

## 6. Local bridges
- The book defines informally: Alice and Davina form the only communication channel between two groups; the local bridge conflicts with strong triadic closure if the relationship is strong (`MANAGES`), so the bridge relationship is weak (`PEER_OF`) [from source] (NEO4J p.207-208).
- Job search: the best contact usually comes from an acquaintance, on the other side of a local bridge, who has different access to information [from source] (NEO4J p.208).
- The formal definition "edge whose removal takes the distance to more than 2" is from graph theory [extrapolation]; the book does not state it in those terms.
- Granovetter and Easley/Kleinberg are cited as the theoretical basis (footnote) [from source] (NEO4J p.200).
- The book warns that theory usually ignores relationship direction and labels; the chapter adopts a hybrid approach [from source] (NEO4J p.200).

## 7. What the book does NOT say
- It does not present PageRank, centrality, community detection or the GDS library; the `NEO_START` page merely lists "centrality algorithms" and "Graph Data Science" as topics (NEO_START p.2). All of that is [extrapolation].
- The v1 application "cartels and geopolitical alliances" is not from the book.
