# Cases, pitfalls and antipatterns

Pages = PDF (printed = N − 12). Each item separates what the book says (`[from source]`) from deduction (`[inference]`) or external knowledge (`[extrapolation]`). Nothing below should be attributed to the book beyond what is marked.

## 1. Growing the array by a fixed amount instead of doubling
- `[from source]` ArrayStack doubles to `max(1, 2n)` when full and shrinks when `length(a) ≥ 3n`; any sequence of m operations spends O(m) in total in `resize()` (Lemma 2.1); the proof depends on there being at least nᵢ/2 − 1 operations between two resizes `(ODS p.45, 47-48)`.
- `[extrapolation]` With a constant increment c, the number of copies for n insertions sums to Θ(n²/c). The book does not analyze this case; use `scripts/calculate_amortized.py --mode resize --growth additive` only as a numerical demonstration.
- `[inference]` The proof of Lemma 2.1 shows why doubling works; shrinking at `length(a) ≥ 2n` would be a design error (the book's ratio of 3 avoids resizing again right after the `resize`, which leaves the array with size 2n).

## 2. Deleting in linear probing by writing `nil` instead of `del`
- `[from source]` LinearHashTable uses three kinds of entry (data, `nil`, `del`); `find` and `remove` stop on finding `nil`; no operation changes a non-null entry to `nil`, and therefore finding `nil` proves that the key is not beyond that point; removal writes `del` `(ODS p.121-123)`.
- `[inference]` If a removal wrote `nil` into a cell that was part of another key's probe sequence, the search for that key would stop there and report "absent".
- `[from source]` `q` counts data plus `del`, the invariant is `length(t) ≥ 2q`, and `resize()` reinserts only the data (the `del` entries disappear) `(ODS p.121, 123)`.
- `[extrapolation]` In general texts, `del` is called a "tombstone" and the effect of accumulating occupied cells is "primary clustering"; neither term is in the book.

## 3. Believing that expected O(1) holds for any hash function
- `[from source]` The proof of the expected O(1) of linear probing assumes independent and uniform hash values, "not realistic"; the book proposes tabulation hashing as a "good enough" function `(ODS p.124, 127-128)`. The proof for ChainedHashTable uses the collision probability 2/2^d of multiplicative hashing `(ODS p.116-117)`.
- `[from source]` A set of keys can be constructed to collide (denial-of-service attacks) `(ODS p.138)`.

## 4. Treating amortized or expected as worst case
- `[from source]` Amortized: a sequence of m operations costs at most m·f(n), but individual operations may cost more; expected: average over random choices of the structure; worst case: never exceeds f(n) `(ODS p.32)`.
- `[from source]` Table 1.2 marks ScapegoatTree (add/remove) and BinaryHeap (add/remove) as amortized, Treap/SkiplistSSet/MeldableHeap as expected and RedBlackTree as worst case `(ODS p.38)`. Chapter 9 uses this difference to justify the red-black tree `(ODS p.189)`.
- `[inference]` An operation that triggers `resize()` or `rebuild()` costs Θ(n) in that call; if a latency spike is unacceptable, prefer worst-case guarantees (RedBlackTree, DLList) or preallocated capacity.
- `[extrapolation]` The book does not cover real time, tail latency or embedded systems; the recommendation above is general engineering.

## 5. Using BinarySearchTree without balancing
- `[from source]` add/remove/find are O(n) in the worst case; the tree can become a chain; inserting 0,1,...,14 in order produces a list of height n−1 `(ODS p.151-152, 157)`.
- `[from source]` Alternatives and their guarantees: Treap (expected), ScapegoatTree (amortized), RedBlackTree (worst case) `(ODS p.152)`.
- `[inference]` Data that arrives sorted (timestamps, sequential keys) is the classic case of degeneration.

## 6. Writing a DLList without a sentinel
- `[from source]` In DLList the number of special cases increases considerably compared to SLList, and the circular `dummy` node removes those exceptions; the `add_before` and `remove` operations need no boundary checks `(ODS p.76-79)`.
- `[extrapolation]` Phrases such as "exponentially increases bugs" are not in the book; it is enough to say that there are more special cases.

## 7. Choosing SEList with a poorly calibrated b
- `[from source]` b = 2 makes SEList approach a DLList and b > n turns it into an array; between the extremes there is a trade-off between the cost of add/remove (O(b + min{i,n−i}/b)) and of locating the element `(ODS p.89-90)`. The space approaches the √n bound when b is of the order of √n `(ODS p.81)`.

## 8. Confusing "expected height" with "expected path length"
- `[from source]` For the Treap, the expected search path is ≈ 2 ln n ≈ 1.386 log n; for the SkiplistSSet it is 2 log n + O(1) `(ODS p.170-172)`; the expected height of a random binary search tree comes from Reed's result `(ODS p.172)`.
- `[extrapolation]` "2 ln n" for the skiplist or the MeldableHeap is a unit error (log₂ vs ln); for the MeldableHeap the book proves at most 2 log n expected steps `(ODS p.225-226)`.

## 9. Assuming that the book's red-black tree is the "classic" red-black tree
- `[from source]` The book presents two properties (black-height and no-red-edge) and a left-leaning variant, with `push_black`, `pull_black` and `flip`; it admits that "there is no single definition" `(ODS p.194, 198-199)`.
- `[extrapolation]` Rotation caps (2 on insertion, 3 on removal) and "red uncle/black uncle" cases belong to other presentations; the book only gives the amortized result of Theorem 9.2 `(ODS p.208)`.

## 10. Choosing YFastTrie/XFastTrie without comparing with comparison-based trees
- `[from source]` BinaryTrie O(w) is worse than or equal to comparison-based structures because log n ≤ w; XFastTrie gives find O(log w) but add/remove O(w) and space O(n·w); YFastTrie fixes both time and space `(ODS p.269, 276-279, 284)`.
- `[inference]` For small n or w large relative to n, comparison-based trees win in simplicity and may win in time.

## 11. Expecting O(1) for all three kinds of graph operation
- `[from source]` AdjacencyLists have `in_edges` in O(n+m); the matrix has `out_edges` and `in_edges` in O(n) and space O(n²) `(ODS p.255, 258-259)`. The BFS/DFS traversals are analyzed only for AdjacencyLists `(ODS p.259-260)`.
- `[from source]` Recursive DFS can overflow the stack on large graphs `(ODS p.262-263)`.

## 12. B-tree with pointers to the parent
- `[from source]` If nodes stored `parent`, a split would need to update B+1 children (from 3 to B+4 accesses); for that reason the book's B-tree does not store the parent and implements `add`/`remove` recursively `(ODS p.294)`.
