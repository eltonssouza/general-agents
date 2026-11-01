# Critical cases, false premises and antipatterns (verified synthesis)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Each item says what the book actually states, what is `[inference]`/`[extrapolation]`, and what the v1 package got wrong, so you can correct the user with the right page.

## 1. "A greedy algorithm solves it, it's obvious" (common false premise)
- `[from source]` The book says that greedy algorithms "almost never work", that problems truly solved by a greedy algorithm are rare, and that without a formal proof a greedy algorithm is not even worth anything on an algorithms exam (JE p.125-126). The book's proof technique is the inductive exchange argument (JE p.178, 182-183).
- `[from source]` The author's warning sign: did you think of the word "greedy"? Try DP (JE p.126). Exercise from Nadiria's notes: build a case in which the greedy change-making algorithm fails (JE p.141).
- `[extrapolation]` The example $\{1,4,5,6\}$ with change for 8 (greedy 6+1+1; optimal 4+4): correct, but not an example from the book.
- v1 correction: the example was cited at p.125-127 and p.126 as if it were from the text.

## 2. "Dijkstra works with negative edges if we add a constant" (false premise)
- `[from source]` Adding the same constant to all edges **changes** the shortest paths, because paths with more edges gain more; Fig. 9.1 (JE p.329). The correct alternative is to reweight with vertex prices (Johnson): $w'(uv)=\pi(u)+w(uv)-\pi(v)$ (JE p.329-331).
- `[from source]` "Dijkstra with negative edges" has two readings: `NonnegativeDijkstra` (the textbook version, inserts all vertices at the start) **gives a wrong answer**; the full `Dijkstra` remains correct without negative cycles, but with an exponential worst case (JE p.306-307). With negative edges, Bellman-Ford $O(VE)$ (JE p.310) or the dag algorithm in $O(V+E)$ (JE p.300-302).
- v1 correction: "fails catastrophically with any negative edge" (p.303-304) oversimplified and cited neither the book's distinction nor the exponential case.

## 3. "I reduced my problem to 3SAT, so it is NP-hard" (inverted direction)
- `[from source]` Rule: to prove that $A$ is NP-hard, reduce a **known** NP-hard problem to $A$ (JE p.404). In a proof sketch, the forward direction covers arbitrary instances of the known problem, the backward direction covers the special instances produced (JE p.410-411).
- `[inference]` Reducing $A$ to 3SAT shows only that $A$ is no harder than 3SAT (if the reduction is polynomial). "This proves $A\in NP$" requires the reduction to be a Karp reduction and 3SAT to be in NP; the book does not make this claim.
- v1 correction: v1 attributed the "proof that $X\in NP$" to the book (p.401, 411).

## 4. "QuickSort is $O(n\log n)$ in the worst case" (false premise)
- `[from source]` With an always-extreme pivot, or "median of three", the worst case is $O(n^2)$ (JE p.48); the analysis is tight (JE p.52). With the exact median as pivot it would be $O(n\log n)$ (JE p.48); the average case depends on an unrealistic assumption about the input; with a uniformly random pivot, $O(n\log n)$ with high probability (note 7) (JE p.49).

## 5. "I apply the Master Theorem" (source)
- `[from source]` The book uses recursion trees, which also cover subproblems of different sizes; the "Master Theorem" appears only in the back-of-book index, pointing to "recursion trees" (JE p.51-52, 454). Whoever demands "the book's master theorem" should be corrected.

## 6. Median of medians with blocks of 3
- `[from source]` With blocks of 3 the recurrence becomes $T(n/3)+T(2n/3)+O(n)=O(n\log n)$ and is "no faster than sorting"; 5 is the smallest odd size with exponential decay (JE p.57).

## 7. DP with circular dependency / without a specification / without need
- `[from source]` The dependency graph of a recurrence is acyclic; if it were not, the naive recursion would never stop (JE p.252). For distances in a graph with cycles the trick is to add a parameter that decreases (number of edges in Bellman-Ford, JE p.312-313; intermediate vertex in Floyd-Warshall, JE p.336).
- `[from source]` Without the **English specification** of the subproblem one cannot even in principle know whether the solution is correct (JE p.124); in the author's classes, DP without a specification is worth zero (JE p.141, note 18).
- `[from source]` DP is not always better: with $T\gg 2^n$, the $O(nT)$ of Subset Sum loses to the naive recursion (JE p.135).

## 8. "The $O(nT)$ Subset Sum algorithm is polynomial, so P=NP"
- `[from source]` $T$ is not polynomial in the input size in bits; it is pseudo-polynomial time and the problem is *weakly NP-hard* (JE p.135, note 16; JE p.422).

## 9. Ford-Fulkerson "always terminates" / "any path will do"
- `[from source]` With integer capacities, it terminates in at most $|f^*|$ iterations; the time $O(E|f^*|)$ is exponential in the input size; with irrational capacities it may not terminate and may not converge to the maximum (JE p.352-354). Edmonds-Karp (shortest path) is polynomial regardless of the capacities (JE p.359-360).

## 10. "Fibonacci in $O(\log n)$ time"
- `[from source]` $O(\log n)$ **arithmetic operations**; since $F_n$ has about $2n/3$ bits (so writing the answer already costs $\Omega(n)$), the real time is $O(M(n))$ and the iterative algorithms are $O(n^2)$ (JE p.121-123).

## 11. Tracing the recursion "mentally" beyond what is necessary
- `[from source]` The book advises trusting the induction hypothesis and not "unrolling" the recursion; correctness comes from induction (JE p.44; Recursion Fairy, JE p.40-41).

## 12. Gale-Shapley: who proposes
- `[from source]` In the book, the hospitals make the offers; the result is the best for the hospitals and the worst for the doctors (JE p.191, 193-194). If the user swaps the roles, the optimality statement switches sides.

## 13. Longest path
- `[from source]` In a **dag**, the longest path is linear (JE p.253-254); in general graphs, NP-hard (JE p.253, 424); the shortest path is polynomial (JE p.424).

## 14. Johnson vs Floyd-Warshall without citing the data structure
- `[from source]` Johnson costs $O(VE\log V)$ with a binary heap and $O(VE+V^2\log V)$ with a Fibonacci heap (JE p.329-330); Floyd-Warshall is $O(V^3)$ (JE p.336-338).

## 15. Cook-Levin "proved in the book"
- `[from source]` The book states it and **does not prove it** (JE p.401-402). Do not cite a book page for the proof.

## Outside the book
Classic counterexamples for other greedy criteria, pivot heuristics, average-case analyses, comparison of implementation constants.
