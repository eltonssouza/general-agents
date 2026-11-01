# Greedy algorithms (Ch. 4)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 4 = PDF p.177-194 (exercises p.194-204). The book's advance warning: greedy algorithms rarely work and require a formal proof (JE p.125-126; see `programacao-dinamica.md`).

## 1. General pattern and the exchange proof (4.3, JE p.182-183)
- `[from source]` The book presents the same proof structure for the tape, scheduling and Huffman problems and calls it the **inductive exchange argument** (*exchange argument*) (JE p.178, 181-183):
  1. assume an optimal solution that differs from the greedy one;
  2. find the "first" difference between the two;
  3. argue that the optimal choice can be swapped for the greedy one **without making the solution worse** (the swap may not improve it);
  4. by induction, some optimal solution contains the entire greedy solution, hence equals it. Sometimes an extra step is needed showing that no optimal solution strictly improves on the greedy one (JE p.182-183).
- `[inference]` "Greedy choice property" and "optimal substructure" as a pair of formal properties come from other texts. In the book the term *optimal substructure* appears only in the edit-distance section (JE p.130), and *greedy choice* only as "the greedy choice $g_j$" (JE p.182). If you use the names, label them.

## 2. Storing files on tape (4.1, JE p.177-179)
- `[from source]` With lengths $L[1..n]$, the cost of accessing file $k$ is $\sum_{i\le k}L[i]$ (JE p.177). The expected cost is minimized by sorting by **increasing length** (Lemma 4.1); the proof swaps an adjacent out-of-order pair: the swap changes the expected cost by $(L[b]-L[a])/n<0$ (JE p.178). Time $O(n\log n)$ plus writing the files (JE p.178).
- `[from source]` With different frequencies $F[i]$, sort by increasing ratio $L/F$ (Lemma 4.2), with the same adjacent-swap proof (JE p.178-179).

## 3. Interval scheduling, *Scheduling Classes* (4.2, JE p.179-182)
- `[from source]` Given classes with start $S[i]$ and finish $F[i]$, choose the largest conflict-free subset (JE p.179-180). There is a "take or skip class 1" recurrence that becomes an $O(n^3)$ DP (improvable to $O(n^2)$ with another recurrence) (JE p.180).
- `[from source]` Greedy: scan the classes in **order of finish time** and accept every class that does not conflict with the last accepted one; after sorting, the loop is linear, total $O(n\log n)$ (JE p.180-181).
- `[from source]` Lemma 4.3: at least one maximum solution includes the class that finishes first (swap $X'=X\cup\{f\}\setminus\{g\}$); Theorem 4.4 by induction; and the "unrolled" version generalizes the swap to the $j$-th point of divergence (JE p.181-182). The greedy solution is not the only maximum one (JE p.181).
- `[from source]` Greedy only works when "best" means "largest"; DP serves for other definitions of "best" (JE p.180, note 2).
- `[extrapolation]` The book does **not** list counterexamples to the criteria "earliest start", "shortest duration" or "fewest conflicts" in the text (this was marked `[from source]` p.180 in v1). The usual counterexamples are good for teaching, but label them. The book directly proposes the intuition of "finish the first one as early as possible" (JE p.180). There is an exercise on alternative greedy strategies (JE p.194-195).

## 4. Huffman codes (4.4, JE p.183-188)
- `[from source]` Binary *prefix-free* code: no codeword is a prefix of another; visualized as a binary tree with the characters at the leaves; cost $\sum f[i]\cdot depth(i)$ (JE p.183). It is not a binary search tree: the order of the leaves does not matter (JE p.183).
- `[from source]` Algorithm (Huffman, 1951): "merge the two least frequent symbols and recurse" (ties arbitrary); in Sallows's example the 649-bit message has the same size for any Huffman code (JE p.184-185).
- `[from source]` Proof: Lemma 4.5 (the two least frequent symbols are deepest siblings in some optimal tree, by exchange) and Theorem 4.6 (by induction, with $cost(T)=cost(T')+f[1]+f[2]$) (JE p.186-187).
- `[from source]` Implementation with a priority queue: $2n-1$ `Insert` and $2n-2$ `ExtractMin` operations, $O(n\log n)$ with a binary heap; encoding/decoding costs $O(m)$ for an $m$-bit message (JE p.187-188).
- `[inference]` v1 claimed $\Theta(n\log n)$ time and $\Theta(n)$ space (JE p.186); the book gives only $O(n\log n)$ (JE p.187).

## 5. Stable matching (4.5, JE p.188-194)
- `[from source]` Context: the NRMP (doctors × hospitals). A matching is **unstable** if there is a pair (doctor $\alpha$, hospital $B$) not matched to each other who prefer each other to their current partners (JE p.189). The book assumes $n$ doctors and $n$ hospitals, each hospital with one position, complete lists and no ties (JE p.189).
- `[from source]` "Bad ideas": swapping to fix instabilities can loop forever (Knuth's example); greedy rounds of simultaneous offers can also leave instabilities (JE p.190).
- `[from source]` **Gale-Shapley (as the book presents it): it is the HOSPITALS that make offers.** In each round, an unmatched hospital offers the position to the best doctor who has not yet rejected it; the doctor provisionally accepts if free or if they prefer the new offer, rejecting the current one (JE p.191). "Hospitals offer greedily; doctors accept greedily" (JE p.191). The choice of which hospital makes the offer does not change the result (JE p.193).
- `[from source]` Time: each hospital offers to each doctor at most once, hence at most $n^2$ offers/rounds; with a suitable representation, $O(n^2)$, and this bound is tight ($\Omega(n^2)$ offers on some inputs) (JE p.192). Correctness: every doctor who receives an offer is at least provisionally matched; at the end the matching is perfect and stable (JE p.193).
- `[from source]` Optimality: with hospitals offering, each hospital $A$ gets $best(A)$, the best *feasible* doctor (one who appears in some stable matching) — the best stable matching from the hospitals' point of view (Cor. 4.8); and each doctor gets the worst feasible hospital $worst(\alpha)$ (Cor. 4.9) (JE p.193-194). The proposing side wins: the NRMP reversed the algorithm in 1998 (JE p.194).
- `[inference]` "Optimal for the proposers and worst for the receivers" is the general reading of Cor. 4.8-4.9, **but in the book the proposers are the hospitals**. v1 swapped the roles (applicants proposing) and claimed an "invariant: the institution only improves, the proposer only gets worse" that is not on p.189-192 (nor does the book use the terms *applicant-optimal*/*institution-pessimal*). Removed as `[from source]`.

## 6. When to use greedy (synthesis)
- `[from source]` Use greedy only with an exchange proof; when in doubt, DP (JE p.126). Problems in this chapter: tape (sort by $L$ or $L/F$), intervals (sort by finish time), Huffman (merge the two minima), stable matching (deferred acceptance).
- `[from source]` Another use of greedy appears in the MST (JE p.259-286) and in the "fattest path" Edmonds-Karp (JE p.358).

## Outside the book
Matroids, general theory of greedy algorithms, adaptive Huffman, greedy approximations (set cover), versions of Gale-Shapley with ties or capacities (the book warns that reality is more complicated, JE p.189 note 9).
