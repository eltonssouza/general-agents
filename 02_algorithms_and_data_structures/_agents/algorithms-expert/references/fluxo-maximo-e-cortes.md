# Maximum flow and minimum cut (Ch. 10)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 10 = PDF p.345-362 (exercises p.362-370). Applications in `aplicacoes-de-fluxo.md`.

## 1. Flows and cuts (10.1-10.2, JE p.345-348)
- `[from source]` Historical origin: the Harris-Ross report on the Warsaw Pact railway network (44 vertices, 105 edges), declassified in 1999 (JE p.345-346).
- `[from source]` An $(s,t)$-flow is $f:E\to\mathbb R$ with **conservation** at every vertex except $s$ and $t$; the value $|f|$ is the net flow leaving $s$, equal to what enters $t$ (JE p.346-347). With capacities $c:E\to\mathbb R_{\ge0}$, $f$ is **feasible** if $0\le f(e)\le c(e)$; it *saturates* the edge if $f(e)=c(e)$ (JE p.347).
- `[from source]` $(s,t)$-cut: a partition $(S,T)$ with $s\in S$, $t\in T$; capacity $\|S,T\|=\sum_{v\in S}\sum_{w\in T}c(vw)$ — only edges from $S$ to $T$ count (JE p.347).
- `[from source]` **Lemma 10.1** (weak duality): for every feasible flow $f$ and every cut $(S,T)$, $|f|\le\|S,T\|$; equality holds if and only if $f$ saturates every edge from $S$ to $T$ and avoids (zero flow) every edge from $T$ to $S$. If $|f|=\|S,T\|$, then $f$ is maximum and the cut is minimum (JE p.348-349).

## 2. Max-flow min-cut theorem (10.3, JE p.349-351)
- `[from source]` **Theorem**: in every network, the value of the maximum flow equals the capacity of the minimum cut (Ford-Fulkerson 1954; Elias-Feinstein-Shannon 1956) (JE p.349).
- `[from source]` Proof (JE p.349-351): assume the network is reduced (*reduced*; at most one edge between two vertices; subdividing suffices) (JE p.349); **residual capacity** $c_f(uv)=c(uv)-f(uv)$ if $uv\in E$, $=f(vu)$ if $vu\in E$, otherwise $0$; **residual graph** $G_f$ = edges with $c_f>0$ (JE p.349-350). If there is a path $s\to t$ in $G_f$ (*augmenting path*) with bottleneck $F=\min c_f$, augmenting by $F$ gives a feasible flow of larger value (JE p.350-351). If there is no path, the set $S$ of vertices reachable from $s$ in $G_f$ defines a cut whose capacity equals $|f|$ (JE p.351).
- `[inference]` This is why the three equivalent statements common in other texts hold: ($f$ maximum) ⇔ (no augmenting path in $G_f$) ⇔ ($|f|$ = capacity of some cut). The book uses them in the proof but does not state them as a list of equivalences. The extracted minimum cut is $S$ = vertices reachable from $s$ in the residual graph (JE p.351).

## 3. Ford-Fulkerson (10.4, JE p.352-354)
- `[from source]` Algorithm: start from the zero flow and augment along any $s\to t$ path in the residual graph, until there is none (JE p.352).
- `[from source]` **Integrality theorem**: with integer capacities there is an integer maximum flow (and the algorithm finds it) (JE p.352).
- `[from source]` With integer capacities, at most $|f^*|$ iterations; each costs $O(E)$ for a search; total $O(E\,|f^*|)$ (JE p.352). The Edmonds-Karp example (4 vertices, capacity $X$) shows that the bound is essentially tight, $\Theta(X)$ iterations; the time is exponential in the input size in bits (JE p.352-353).
- `[from source]` Rational capacities: it terminates (still in exponential time). **Irrational capacities**: it may not terminate and the sequence of augmentations may converge to a value much smaller than the maximum (Zwick's example, 6 vertices: converges to $4+\sqrt5<7$ while the maximum is $2X+1$) (JE p.353-354). Floating-point rounding errors can produce the same behavior in practice (JE p.354).

## 4. Combination and decomposition (10.5, JE p.354-358)
- `[from source]` Decomposition theorem: every nonnegative flow is a positive linear combination of $s\to t$ paths and directed cycles, with at most $E$ terms (JE p.355). Consequence: any "pure" flow algorithm (one that builds explicit flows) may cost $\Omega(VE)$ (JE p.357-358).

## 5. The Edmonds and Karp algorithms (10.6, JE p.358-361)
- `[from source]` **Rule 1 – fattest path** (*fattest*, largest bottleneck): found in $O(E\log V)$ by best-first search. Each augmentation multiplies the residual maximum flow by at most $1-1/E$; after $E\ln|f^*|$ iterations the residual is $<1$; with integer capacities the **total time** is $O(E^2\log E\,\log|f^*|)$, polynomial in the input size (JE p.358-359).
- `[inference]` v1 said "$O(E^2\log E)$ augmentations": this confuses time with the number of iterations; the number of iterations is $O(E\log|f^*|)$ and depends on $|f^*|$ (with integers).
- `[from source]` **Rule 2 – shortest path** (fewest edges, by BFS in $O(E)$): terminates in a polynomial number of iterations **regardless of the capacities** (JE p.359). Lemma 10.2: the level $level_i(v)$ of each vertex in the residual graph only increases; Lemma 10.3: each edge disappears from the residual graph at most $V/2$ times; hence at most $EV/2$ iterations and time $O(VE^2)$ (JE p.359-360). The same shortest-path idea appears in Dinitz (with $O(V^2E)$), cited in a note (JE p.359, note 3).
- `[from source]` Later progress (table of algorithms; Orlin 2012 with $O(VE)$, "cite as: maximum flows in $O(VE)$") and for unit-capacity networks (Karzanov $O(\min\{V^{2/3},E^{1/2}\}E)$; Mądry 2013) (JE p.361-362). `[DATED]` regarding "fastest known" (2019).

## 6. Quick checks for answers
- Feasible flow: capacity and conservation (JE p.346-347). Value: net outflow of $s$ (JE p.346).
- Weak duality to bound: $|f|\le\|S,T\|$ for any cut (JE p.348).
- To extract the minimum cut: search from $s$ in the residual graph of the maximum flow (JE p.351).
- If the capacities are irrational, do not use "augment along any path"; use Edmonds-Karp (JE p.353-354, 359).

## Outside the book
Push-relabel in detail, Dinic with a full *blocking flow*, minimum-cost flow, circulations with demands/lower bounds, linear programming (LP duality).
