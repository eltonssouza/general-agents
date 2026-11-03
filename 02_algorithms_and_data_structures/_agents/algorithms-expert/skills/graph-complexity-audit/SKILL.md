---
name: graph-complexity-audit
description: Complexity worksheet for graph algorithms according to Erickson's book (BFS, DFS, topological sort, SCC, Borůvka, Jarník, Kruskal, shortest paths in a dag, Dijkstra, Bellman-Ford, Johnson, Floyd-Warshall, flow and matching), with page, conditions and labels. Highlights what the book says about Dijkstra with negative edges.
allowed-tools: Bash, Read
---

# Graph Complexity Audit

Read-only tool (Python 3, stdlib, no network). Book convention: running times assume the standard adjacency list `[from source] (JE p.217)`. Pages = PDF (printed = N − 18). Each line carries the label (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`).

## Usage
```bash
python -I skills/graph-complexity-audit/scripts/audit_graph_complexity.py --list
python -I skills/graph-complexity-audit/scripts/audit_graph_complexity.py --algo dijkstra
python -I skills/graph-complexity-audit/scripts/audit_graph_complexity.py --algo johnson --v 1000 --e 5000
python -I skills/graph-complexity-audit/scripts/audit_graph_complexity.py --algo ford_fulkerson --v 100 --e 400 --flow 50
```
Algorithms: `bfs`, `dfs`, `whatever_first`, `topological_sort`, `scc_kosaraju`, `scc_tarjan`, `boruvka`, `jarnik_prim`, `kruskal`, `dag_sssp`, `dijkstra`, `bellman_ford`, `johnson`, `floyd_warshall`, `ford_fulkerson`, `edmonds_karp_fattest`, `edmonds_karp_shortest`, `bipartite_matching`, `orlin`.

## Cautions
- **Dijkstra and negative edges**: `NonnegativeDijkstra` is wrong; the full `Dijkstra` is correct without negative cycles but may be exponential `[from source] (JE p.306-307)`. Do not summarize it as "always fails".
- **Johnson**: `O(VE log V)` with a binary heap and `O(VE + V^2 log V)` only with a Fibonacci heap `[from source] (JE p.329-330)`.
- **Edmonds-Karp (fattest path)**: `O(E^2 log E log|f*|)` is the **running time** (iterations `E ln|f*|`), with integer capacities `[from source] (JE p.358-359)`.
- The numeric estimate (`--v`, `--e`) is only an order of magnitude (constant 1, base-2 logarithm) `[inference]`. There are no adjacency-matrix times beyond those the book gives (JE p.219, 306).
- Memory is not tabulated: the book does not analyze it algorithm by algorithm; derive it carefully and label it `[inference]`.
