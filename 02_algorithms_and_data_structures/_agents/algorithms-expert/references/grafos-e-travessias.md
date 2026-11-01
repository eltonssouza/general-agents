# Graphs, traversals, DFS, topological sorting and strong components (Chs. 5 and 6)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 5 = PDF p.205-224 (exercises p.225-242); Ch. 6 = PDF p.243-262 (exercises p.262-274).

## 1. Definitions and representations (5.2-5.4, JE p.208-217)
- `[from source]` A graph is a pair of sets $(V,E)$; in undirected graphs the edges are two-element sets of vertices, in directed graphs they are ordered pairs; $V$ and $E$ are also used for the quantities (JE p.208-209). Graphs without loops or parallel edges are simple graphs (*simple graphs*) (JE p.209).
- `[from source]` A *dag* is a directed graph with no directed cycles (JE p.210). The **dependency graph** of a recurrence is a dag (JE p.211).
- `[from source]` **Adjacency list**: array of lists, space $O(V+E)$; list the neighbors of $v$ in $O(1+\deg v)$; test $uv\in E$ in $O(1+\deg u)$ (JE p.213-214). **Adjacency matrix**: $V\times V$, edge test in $\Theta(1)$, list neighbors in $\Theta(V)$, space $\Theta(V^2)$ "only efficient for very dense graphs" (JE p.214-215). Table 5.1 summarizes the operations (JE p.216).
- `[from source]` The book's convention: unless stated otherwise, every running time of a graph algorithm assumes the standard adjacency list (JE p.217). The book gives reasons (implicit graphs) for not preferring a matrix or a hash table (JE p.216-217).
- `[extrapolation]` "Sparse when $E=O(V)$, dense when $E=\Theta(V^2)$" as a selection rule is customary practice, not a sentence from the book.

## 2. *Whatever-First Search* (5.5-5.6, JE p.217-223)
- `[from source]` Reachability: which vertices are reachable from $s$? The generic algorithm keeps candidates in a "bag" (*bag*); `WhateverFirstSearch(s)`: put $s$; while the bag is not empty, remove $v$; if unmarked, mark it and put each neighbor in the bag (JE p.217-218). Lemma 5.1: it marks exactly the reachable vertices and the parent edges form a spanning tree of the component (JE p.218-219).
- `[from source]` Time $O(V+ET)$, with $T$ the cost of inserting/removing in the bag; with an adjacency matrix $O(V^2+ET)$ (JE p.219).
- `[from source]` Stack ⇒ depth-first search, $O(V+E)$ (JE p.219); queue ⇒ breadth-first search, $O(V+E)$, the breadth-first tree contains shortest paths (in number of edges) from $s$ (JE p.220); priority queue ⇒ *best-first search*, $O(V+E\log E)$, which with edge weights gives the MST (Jarník/"Prim") and with distances gives Dijkstra (JE p.220-221). Also *widest paths* (JE p.221).
- `[inference]` The generic skeleton is $O(V+E)$ only when $T=O(1)$ (stack, queue); with a heap, it is $O(V+E\log E)$. v1 wrote $O(V+E)$ for the generic skeleton.
- `[from source]` Disconnected graphs: the *wrapper* `WFSAll`; counting components, labeling them (JE p.221-222). In directed graphs the code does not change; the tree covers the vertices reachable from $s$ (JE p.223).
- `[from source]` *Flood fill* reduces to reachability in a pixel graph, $O(n^2)$ for $n\times n$ (JE p.223-224).

## 3. DFS, pre/postorder and edge classification (6.1, JE p.243-248)
- `[from source]` `DFS(v)` marks $v$, calls `PreVisit`, recurses on unmarked neighbors (parent) and calls `PostVisit` (JE p.244). `DFSAll` traverses the whole graph (JE p.244-245).
- `[from source]` With a global clock: $v.pre$ (start) and $v.post$ (finish); the active intervals $[v.pre,v.post]$ are disjoint or nested, and nesting ⇔ ancestry in the forest (JE p.245-246). States: new, active, finished; the active vertices form a path (JE p.246).
- `[from source]` The edges $uv$ divide into four classes: if $v$ is **new** when $DFS(u)$ starts → $u$ is a proper ancestor of $v$; it is a *tree edge* if $u$ is the parent of $v$, otherwise a *forward edge*; if $v$ is **active** → *back edge* (and there is a path from $v$ to $u$); if $v$ is already **finished** → *cross edge*; the order $u.post<v.pre$ is impossible (JE p.247). Lemma 6.1 characterizes ancestors (JE p.248).
- `[inference]` v1 defined *forward edge* as "to an already finished descendant"; the book's definition is by the state of $v$ when $u$ starts (new) (JE p.247).

## 4. Detecting cycles and topological sorting (6.2-6.3, JE p.249-252)
- `[from source]` Dag: no directed cycles; source (*source*) with no incoming edges, sink (*sink*) with no outgoing edges; every dag has at least one of each (JE p.249).
- `[from source]` If $u.post<v.post$ for some edge $uv$, then the graph has a cycle through that edge; this is checked in $O(V+E)$. Alternative: maintain states and return False upon finding an edge to an **active** vertex (`IsAcyclic`), also $O(V+E)$ (JE p.249). `[inference]`: hence, a directed graph is acyclic if and only if DFS finds no *back edge*.
- `[from source]` Topological order: a total order in which every edge points to the right; impossible if there is a cycle. **In a dag, the reverse of any postorder is a topological order**; $O(V+E)$ (JE p.250-251). Implicit topological order: process in postorder (reverse topological order) without storing it (JE p.251-252). For forward order, use DFS on the reverse graph (JE p.252).

## 5. Memoization, DP and DAGs (6.4, JE p.252-255)
- `[from source]` Memoization is DFS on the dependency graph; DP is traversing the subproblems in postorder; longest path in a DAG in $O(V+E)$ (JE p.252-254). See `programacao-dinamica.md`.

## 6. Strongly connected components (6.5-6.6, JE p.255-262)
- `[from source]` $u$ and $v$ are strongly connected if each reaches the other; this is an equivalence relation; classes = strong components; the component graph $scc(G)$ is always a dag; $G$ is a dag if and only if every strong component is a single vertex (JE p.255-256).
- `[from source]` Computing the component of a vertex $v$ in $O(V+E)$ via $reach(v)\cap reach^{-1}(v)$; the naive version for all components costs $O(VE)$ (JE p.256).
- `[from source]` Lemma 6.2: in a DFS, each strong component has exactly one vertex without a parent inside the component (the "root", the one with smallest $pre$) (JE p.256-257). Lemma 6.3: the last vertex of a postorder is in a source component (JE p.258).
- `[from source]` **Kosaraju-Sharir** (JE p.258-259): phase 1, DFS on $rev(G)$ pushing each vertex onto a stack when it finishes; phase 2, DFS (or search) on $G$ considering the vertices in stack order; each call labels one component; $O(V+E)$. Discovered by Kosaraju (1978, unpublished) and by Sharir (1981) (JE p.258).
- `[inference]` The form "DFS on $G$ first, then on $G^{rev}$ by decreasing postorder" is the most common in other texts and is equivalent to the book's by swapping $G$ and $rev(G)$ (the components of $G$ and $rev(G)$ coincide). v1 presented it as the book's (p.256-257).
- `[from source]` **Tarjan** (1972): uses $low(v)$ and an auxiliary stack in the same DFS; $v$ is a component root when $v.low=v.pre$; $O(V+E)$ (JE p.260-262).

## Outside the book
Bridges and articulation points, biconnected components, Kahn's topological sorting (by in-degree), 2-SAT via SCC, bidirectional BFS and A*.
