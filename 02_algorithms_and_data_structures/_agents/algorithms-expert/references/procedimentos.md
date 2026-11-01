# Procedures (work playbooks) — what comes from the book and what is the package's own organization

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Each playbook says whether the structure comes from the book (`[from source]`) or is a didactic organization by the package (`[inference]`).

## 1. Describe a complete algorithm (Ch. 0.5)
`[from source]` Four components: *What* (problem specification), *How* (description), *Why* (proof), *How fast* (running-time analysis) (JE p.29). To write it: pseudocode + structured English, loops written as loops, recursion written recursively (JE p.31-32).

## 2. Prove the correctness of a recursive algorithm by induction
`[from source]` (structure seen in the proofs for Hanoi, MergeSort, Merge, QuickSort; JE p.43-46, 48). `[inference]` (the "steps" label is the package's):
1. Write the **specification** of what the subroutine returns (in precise English).
2. **Base case**: the smallest size (for example $n=0$ in Hanoi, JE p.43-44; $n\le1$ in MergeSort, JE p.46).
3. **Inductive step**: assume the result for smaller instances (the *Recursion Fairy*, JE p.40-41, 46) and show that the local step produces the correct result.
4. For loops, use an **invariant** (example: Partition, JE p.48).
5. If there is a subroutine (Merge, Partition), prove it by a separate induction (JE p.45-48).

## 3. Solve a divide-and-conquer recurrence (recursion tree)
`[from source]` (JE p.49-52):
1. Write $T(n)=r\,T(n/c)+f(n)$ and draw the first two or three levels.
2. Level $i$ has $r^i$ nodes of value $f(n/c^i)$; $T(n)=\sum_{i=0}^{L} r^i f(n/c^i)$, $L=\log_c n$; leaves: $n^{\log_c r}$ (JE p.50-51).
3. Classify the series: **decreasing** ⇒ $O(f(n))$; **equal** ⇒ $O(f(n)\log n)$; **increasing** ⇒ $O(n^{\log_c r})$ (JE p.51).
4. Unequal subproblems: sum per level ($\le n$ per level) and count the depth (JE p.51-52).
5. Ignore ceilings and floors (domain transformation) (JE p.52-53).
`[extrapolation]`: for $f(n)=n^k\log^p n$ the same comparison holds; and for $\sum a_i T(n/b_i)$ with $\sum a_i b_i^{-k}<1$, $=1$, $>1$ the result is root, balanced, leaves. Tool: `skills/recurrence-solver/scripts/solve_recurrence.py` and `check_recurrence.py`.

## 4. Design a backtracking algorithm
`[from source]` (JE p.97-98): decide which **single decision** each call makes; define what must be remembered from the earlier decisions (the smallest possible summary); try all consistent options and let the *Recursion Fairy* do the rest; design for the simplest variant (boolean or number) (JE p.96, 98).

## 5. Design a DP (the book's playbook)
`[from source]` (JE p.124-125): **Stage 1** formulate recursively (English specification; recursive solution). **Stage 2** bottom-up: (a) subproblems, (b) memoization structure, (c) dependencies, (d) evaluation order (linear extension of the partial order), (e) space and time, (f) write the algorithm. Remember: no DP without the English specification of the subproblems (JE p.124, 141).
`[from source]`: the dependency graph is a dag (JE p.211, 252); time = sum of the times per subproblem (JE p.125).
`[inference]`: support table – number of subproblems × cost per subproblem, as seen in Edit Distance ($O(mn)$, JE p.132) and in the optimal BST ($O(n^2)$ subproblems, $O(n)$ each, $O(n^3)$, JE p.138).

## 6. Prove a greedy algorithm by exchange argument
`[from source]` (JE p.182-183): assume an optimal solution that differs from the greedy one; find the first difference; show that swapping the optimal choice for the greedy one does not make it worse; by induction, an optimal solution contains the entire greedy one. Examples: tape (JE p.178), intervals (JE p.181-182), Huffman (JE p.186-187). If the proof does not work out, use DP (JE p.126).

## 7. Prove that a problem is NP-hard
`[from source]` (JE p.404, 410-411): choose a **known** NP-hard problem $Y_0$; describe a polynomial algorithm that transforms an arbitrary instance of $Y_0$ into a special instance of your problem; prove "forward" (yes ⇒ yes) and "backward" (yes ⇒ yes, only for the instances produced); optionally think in terms of certificates. `[inference]`: tips for choosing the source, summarized from the book (JE p.426): bits/subsets → Sat/Partition; labels from a small set → 3Color; ordering → Hamiltonian cycle/TSP.

## 8. Reduce to maximum flow or minimum cut
`[from source]` (JE p.371-386, a pattern repeated in the examples): (1) build a network with $s$, $t$ and capacities that encode the constraints; (2) use integrality to obtain an integer flow (JE p.352, 373); (3) decompose the flow into paths (JE p.355-357) or read off the cut (JE p.351, 385-386); (4) cite the cost: $O(VE)$ with Orlin as a black box (JE p.361-362) or Ford-Fulkerson when $|f^*|$ is small (JE p.372).

## 9. Analyze a graph algorithm
`[from source]` (convention, JE p.217): running times assume the standard adjacency list. For traversal-based algorithms: $O(V+ET)$ (JE p.219). For shortest paths: classify the graph (unweighted → BFS; dag → topological order; weights $\ge0$ → Dijkstra; negative → Bellman-Ford; all pairs → Johnson or Floyd-Warshall) (JE p.296, 300-302, 304-310, 329-338). `[inference]` – the decision table is the package's.
