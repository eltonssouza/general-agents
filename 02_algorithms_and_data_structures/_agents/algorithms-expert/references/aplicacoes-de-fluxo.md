# Applications of flows and cuts (Ch. 11)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 11 = PDF p.371-386 (exercises p.386-396). Prerequisite: `fluxo-maximo-e-cortes.md`. The book's "$O(VE)$" times use Ford-Fulkerson when $|f^*|\le V$, or Orlin's algorithm as a black box (JE p.372, 374).

## 1. Edge-disjoint paths (11.1, JE p.371-372)
- `[from source]` Give every edge capacity 1; the maximum flow from $s$ to $t$ pushes 0 or 1 along each edge; the flow decomposition shows that the saturated edges form disjoint paths and cycles, and the **number of paths = value of the flow**; therefore any flow algorithm computes the largest set of edge-disjoint paths (JE p.371-372).
- `[from source]` Since $|f^*|\le V-1$ (the cut $(\{s\},V\setminus\{s\})$ has capacity $\le V-1$), Ford-Fulkerson solves it in $O(|f^*|E)=O(VE)$ (JE p.372). For undirected graphs, replace each edge by two directed edges of capacity 1 (JE p.372).
- `[inference]` The name "Menger's Theorem" for this result is customary, but it does **not** appear in the book (v1 cited "(Menger's Theorem) p.371-372").

## 2. Vertex capacities and vertex-disjoint paths (11.2, JE p.372-373)
- `[from source]` Each vertex $v$ becomes $v_{in}$ and $v_{out}$ joined by an edge of capacity $c(v)$; each edge $uv$ becomes $u_{out}v_{in}$ with the same capacity (Ford and Fulkerson, 1962) (JE p.372). With capacity 1 on every vertex, the maximum number of vertex-disjoint paths is computed in $O(VE)$ (JE p.372).

## 3. Maximum bipartite matching (11.3, JE p.373-374)
- `[from source]` A matching is a subgraph in which every vertex has degree $\le1$. Given a bipartite $G$ with $L\cup R$: orient edges from $L$ to $R$, add $s$ with edges to every vertex of $L$ and $t$ with edges from every vertex of $R$, **capacity 1 on all edges**; matchings of size $k$ ⇔ integer flows of value $k$ (JE p.373-374). The integer flow comes from the integrality of Ford-Fulkerson (JE p.373).
- `[from source]` Time $O(VE)$; interpretation as alternating paths (Berge, 1957); *Hopcroft-Karp* (1973) speeds it up to $O(\sqrt V\,E)$ by finding several disjoint paths per iteration (JE p.374).
- `[extrapolation]` **König's theorem** (maximum matching = minimum vertex cover in bipartite graphs) is **not** covered in the book (v1 cited it at p.374; the book only mentions Kőnig as the author of a 1916 algorithm and of the first graph theory book, JE p.208, 374). It holds, but it is outside knowledge.

## 4. Tuple selection (11.4, JE p.375-378)
- `[from source]` Generalization of matching: sets $X_1,\dots,X_d$ of resources, choose the largest set of $d$-tuples subject to constraints $c(x)$ and $c(x,y)$ (between adjacent sets); a network with one vertex per element, $s$ connected to $X_1$, $X_d$ connected to $t$; $s\to t$ paths correspond to tuples and an integer flow to a selection (JE p.375-376). If non-adjacent pairs were also constrained, the problem would be NP-hard (JE p.376, note 3).
- `[from source]` Example of exam scheduling (classes, rooms, time slots, proctors) with time $O(VE)=O(N^3)$ (JE p.376-378).

## 5. Disjoint-path cover (11.5, JE p.378-381)
- `[from source]` In a dag, the minimum vertex-disjoint path cover reduces to maximum bipartite matching: $G'$ with $v^\flat$ and $v^\sharp$ per vertex and an edge $u^\flat v^\sharp$ per edge $uv$; $G$ has a cover with $k$ paths if and only if $G'$ has a matching of size $V-k$; $O(VE)$ (JE p.379-380). In general graphs it is NP-hard (a cover of size 1 exists iff there is a Hamiltonian path) (JE p.378). Application: minimum number of teachers/flights (JE p.380-381).

## 6. Baseball elimination (11.6, JE p.381-384)
- `[from source]` Input: $W[i]$ wins already obtained and $G[i,j]$ games remaining between $i$ and $j$; the question is whether team $n$ can finish in first place (possibly tied) (JE p.382). Assume team $n$ wins all of its $R[n]$ remaining games; it can finish first if and only if every other team $i$ wins at most $W[n]+R[n]-W[i]$ of its $R[i]$ games (JE p.382).
- `[from source]` Network: one vertex per pair of teams (game) $g_{ij}$ and one per team $t_i$ ($i<n$); $s\to g_{ij}$ with capacity $G[i,j]$; $g_{ij}\to t_i$ and $g_{ij}\to t_j$ with capacity $\infty$; $t_i\to t$ with capacity $W[n]-W[i]+R[n]$. **Theorem**: team $n$ can finish first if and only if there is a feasible flow that **saturates every edge leaving $s$** (JE p.382-383). Example (Detroit, 1996): the total capacity leaving $s$ is 27 and entering $t$ is 26, hence eliminated (JE p.383-384).
- `[from source]` $O(n^2)$ vertices and edges; $O(n^4)$ with Orlin; Wayne (2001) finds all eliminated teams in $O(n^3)$ (JE p.384). Note: a team can be eliminated even when the total capacity into $t$ is not less than that out of $s$ (JE p.384, note 12).
- `[inference]` The trivial check "some rival already has more wins than $W[n]+R[n]$" is an obvious special case (the capacity of $t_i$ would be negative); the book does not highlight it.

## 7. Project selection (11.7, JE p.384-386)
- `[from source]` $n$ projects in a dependency dag (edge $uv$: $u$ cannot be done before $v$); each project has profit $\$(v)$, possibly negative (a cost); choose a subset **closed under dependencies** that maximizes profit (JE p.384).
- `[from source]` Network $G'$: $s\to v$ with capacity $\$(v)$ for positive profit; $u\to t$ with capacity $-\$(u)$ for a cost; dependency edges with capacity $\infty$. A cut $(S,T)$ is legal (selecting $S$) if and only if its capacity is finite (JE p.385). **Profit of $S$ = $P-\|S,T\|$**, where $P=\sum\max\{0,\$(v)\}$; hence the minimum cut maximizes profit; $O(VE)$ with Orlin (JE p.385-386). *(v1 called it "maximum-weight closure" and described dependencies "on other projects"; the book uses "Project Selection".)*

## Outside the book
König-Egerváry and Menger theorems in generality, minimum-cost flow, the weighted assignment problem (the book mentions it as "the assignment problem", JE p.375, note 2), image segmentation by minimum cut.
