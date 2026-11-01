# Graphs: representations and traversals (Ch. 12)

Pages = PDF (printed = N − 12). Source: ODS Ch. 12 (p.251-267). **Directed** graph G = (V, E), V = {0,...,n−1}, n = |V| and m = |E|; undirected edges appear only in the exercises (edge (i,j) present if and only if (j,i) present) `[from source] (ODS p.251-252, 265)`.

## 1. Graph-type operations
`add_edge(i,j)`, `remove_edge(i,j)`, `has_edge(i,j)`, `out_edges(i)` and `in_edges(i)` `[from source] (ODS p.252)`. The first three could use a USet (hash, expected O(1)) and the last two per-vertex adjacency lists; different applications call for different representations `[from source] (ODS p.252-253)`.

## 2. AdjacencyMatrix
- An n × n boolean matrix `a`; `a[i][j]` is true if (i,j) ∈ E `[from source] (ODS p.253)`.
- `add_edge`, `remove_edge` and `has_edge` are O(1) `[from source] (ODS p.253)`. `out_edges(i)` and `in_edges(i)` scan a row or column: O(n) `[from source] (ODS p.253, 255)`.
- Space: at least n² bits; the book's implementation uses on the order of n² bytes; packing `w` booleans per word, O(n²/w) words `[from source] (ODS p.255)`. **Theorem 12.1**: O(n²) space `[from source] (ODS p.255)`.
- Useful when the graph is dense (close to n² edges) and because algebraic operations on the matrix compute graph properties (for example, a² counts paths of length 2) `[from source] (ODS p.255-256)`.

## 3. AdjacencyLists
- An array `adj` of lists; `adj[i]` contains every j with (i,j) ∈ E; in the book's implementation each list is an ArrayStack (constant-time access by position); it could be a DLList `[from source] (ODS p.256)`.
- `add_edge(i,j)`: `adj[i].append(j)`, constant time `[from source] (ODS p.256)`.
- `remove_edge(i,j)` and `has_edge(i,j)`: traverse `adj[i]`, O(deg(i)) (out-degree) `[from source] (ODS p.256-258)`.
- `out_edges(i)`: just returns `adj[i]` (the ready-made list) `[from source] (ODS p.258)`. `[inference]` Reading the neighbors costs O(deg(i)), but handing over the list is O(1).
- `in_edges(i)`: examines all vertices (`has_edge(j,i)` for each j): O(n + m) `[from source] (ODS p.258)`.
- **Theorem 12.2**: add_edge O(1); remove_edge and has_edge O(deg(i)); in_edges O(n + m); space O(n + m) `[from source] (ODS p.259)`.
- Design choices: the collection type of each `adj[i]` (array, linked list, hash), a second list `inadj` for fast `in_edges`, linking between entries of `adj` and `inadj`, edges as objects `[from source] (ODS p.259)`.

## 4. Comparison table (the book's costs)
| Operation | AdjacencyMatrix | AdjacencyLists |
|---|---|---|
| space | O(n²) (p.255) | O(n+m) (p.259) |
| `has_edge` | O(1) (p.253) | O(deg(i)) (p.258) |
| `add_edge` | O(1) (p.253) | O(1) (p.256) |
| `remove_edge` | O(1) (p.253) | O(deg(i)) (p.256-258) |
| `out_edges` | O(n) (p.253, 255) | returns `adj[i]` (p.258) |
| `in_edges` | O(n) (p.253, 255) | O(n+m) (p.258-259) |

## 5. Traversals (assume AdjacencyLists)
- Both traversals find the vertices reachable from a vertex i; they are analyzed **assuming AdjacencyLists** `[from source] (ODS p.259-260)`. The book does not analyze BFS/DFS on the matrix; Θ(n²) in that case is `[inference]` (scanning the row of each visited vertex).
- **BFS**: uses a queue `q` (in the pseudocode, `SLList`) and a boolean array `seen` to avoid enqueuing twice; it visits vertices in increasing order of distance from the root; with a parent array `p` it reconstructs shortest paths (in number of edges) `[from source] (ODS p.260-262)`. **Theorem 12.3**: O(n + m) `[from source] (ODS p.261)`.
- **DFS**: colors each vertex (`white` never seen, `grey` being visited, `black` finished) and recursively visits the white neighbors; the recursive version can overflow the stack on large graphs, so the book shows `dfs2` with an explicit stack `[from source] (ODS p.262-264)`. **Theorem 12.4**: `dfs` and `dfs2` in O(n + m) `[from source] (ODS p.264)`.
- DFS property: if when painting i grey there is a path through white vertices only to j, then j becomes black before i; this allows detecting cycles `[from source] (ODS p.264)`.
- **Theorem 12.5** (more precise): O(n_r + m_r), with n_r reachable vertices and m_r edges originating in them `[from source] (ODS p.265)`.
- Origin: BFS is attributed to Moore and Lee; adjacency lists and DFS to Hopcroft and Tarjan `[from source] (ODS p.265)`.

## 6. Boundary
The chapter covers only representations and BFS/DFS. Weighted shortest paths (Dijkstra) appear only as an application of heaps with `decrease_key` (p.227); strongly connected components, flow and NP-completeness are outside the book and are routed to the algorithms agent.
