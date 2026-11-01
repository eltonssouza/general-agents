# Random binary search trees, Treap and ScapegoatTree (Chs. 7 and 8)

Pages = PDF (printed = N − 12). Sources: ODS Ch. 7 (p.157-176) and Ch. 8 (p.177-188). `log` is log₂; `ln` is the natural logarithm (ODS p.22).

## 1. Random binary search tree
- Built by inserting a random permutation of 0,...,n−1 into a BinarySearchTree; each of the n! permutations is equally likely `[from source] (ODS p.157-158)`.
- Book example: there are 21,964,800 insertion sequences that produce the perfectly balanced 15-node tree and only one that produces the list `[from source] (ODS p.157-158)`.
- Harmonic numbers: ln k < Hₖ ≤ ln k + 1 `[from source] (ODS p.159)`.
- **Lemma 7.1**: the expected length of the search path for x is H_{x+1} + H_{n−x} − O(1) (x in the tree); the consequence is at most 2 ln n + O(1) `[from source] (ODS p.159-160)`. The proof: node i is on the search path of x if and only if i appears before the others in the range between i and x in the permutation `[from source] (ODS p.160-162)`.
- **Theorem 7.1**: it is built in O(n log n) and `find(x)` takes expected O(log n), over the permutation (it does not depend on x) `[from source] (ODS p.162-163)`.

## 2. Rotations
- A rotation is a local modification that makes the child `w` the parent of `u`, preserving the BST property; the depth of `w` decreases by 1 and that of `u` increases by 1 `[from source] (ODS p.165-166)`.
- `rotate_left(u)` raises `w = u.right`; `rotate_right(u)` raises `w = u.left`; the code handles the case where `u` is the root and updates `parent` `[from source] (ODS p.165-166)`.
- `[inference]` Only a constant number of pointers change, so the rotation is O(1); the book does not count the pointers. `scripts/simulate_rotation.py` checks the in-order sequence and the depths.

## 3. Treap
- Each node has a key `x` and a **numeric, unique, randomly drawn priority `p`**; besides being a BST, the **heap property** holds: except at the root, `u.parent.p < u.p` (parent with smaller priority, i.e. a min-heap) `[from source] (ODS p.163)`.
- Given the keys and priorities, the shape is determined: the node with the smallest priority is the root; equivalently, the Treap is the BST obtained by inserting the keys in increasing order of priority; hence it has the shape of a random binary search tree `[from source] (ODS p.163-164)`.
- **Lemma 7.2**: for x in S, the expected search path has H_{r(x)+1} + H_{n−r(x)} − O(1); the expectation is over the priorities, with no assumption about the keys `[from source] (ODS p.164-165)`.
- `add(x)`: inserts as a leaf (as in the BST) with a random priority and moves up with rotations (`bubble_up`) while `u.parent.p > u.p` `[from source] (ODS p.166-167)`. Cost: expected search path ≤ 2 ln n + O(1) plus a number of rotations that does not exceed the path length; Exercise 7.5 shows that the expected number of rotations is O(1) `[from source] (ODS p.167, 174)`.
- `remove(x)`: moves the node down with rotations (`trickle_down`), choosing the child with the smaller priority, until it becomes a leaf, and then does `splice`. It is the inverse operation of `add` with the same priority, which gives the analysis `[from source] (ODS p.169-170)`.
- **Theorem 7.2**: add/remove/find in expected O(log n) `[from source] (ODS p.170)`.
- Book comparison: expected path 2 ln n + O(1) ≈ 1.386 log n + O(1) in the Treap, against 2 log n + O(1) in the SkiplistSSet and ≈ 1.884 log n + O(1) with a biased coin; the Treap is "noticeably" faster `[from source] (ODS p.170-172)`.
- Height: the book only cites Reed's result (expected height α ln n − β ln ln n + O(1), α ≈ 4.31107) for random binary search trees `[from source] (ODS p.172)`. `[inference]` The phrase "expected height 2 ln n" is imprecise: 2 ln n is the expected length of the search path.
- The name Treap comes from Seidel and Aragon (1996); the basic structure was studied earlier by Vuillemin ("Cartesian trees") `[from source] (ODS p.172, 319-320)`.
- Variants: storing only a hash of the address as priority (requires a min-wise independent function; tabulation hashing is an example) and the random tree of Martínez and Roura, which stores subtree sizes `[from source] (ODS p.172-174)`.

## 4. ScapegoatTree (partial rebuilding)
- `rebuild(u)`: gathers the nodes of the subtree into an array (in-order) and recursively rebuilds a perfectly balanced subtree, with `a[m]`, `m = length(a)/2`, as the root; it costs O(size(u)) and gives minimum height `[from source] (ODS p.177-178)`.
- It stores `n` (nodes) and `q`, an upper bound, with the invariant `q/2 ≤ n ≤ q`; the height never exceeds `log_{3/2} q ≤ log_{3/2} 2n < log_{3/2} n + 2` `[from source] (ODS p.178-179)`. The constant 2/3 is fixed in the book; the generalization to a base b (1 < b < 2) is Exercise 8.4 and the WeightBalancedTree is Exercise 8.8 `[from source] (ODS p.186-187)`.
- `find(x)`: standard BST search, worst-case O(log n) because of the height `[from source] (ODS p.179)`.
- `add(x)`: increments `n` and `q`, inserts the leaf `u`; if `depth(u) > log_{3/2} q`, it climbs looking for the **scapegoat** `w` with `size(w.child)/size(w) > 2/3` and rebuilds `w.parent` `[from source] (ODS p.180)`. **Lemma 8.1**: that node exists `[from source] (ODS p.182)`.
- `remove(x)`: removes as in the BST (the height does not increase), decrements `n` and, if `2n < q`, rebuilds the whole tree and sets `q ← n` `[from source] (ODS p.181)`.
- **Lemma 8.2**: finding the scapegoat and rebuilding costs O(size(w)) `[from source] (ODS p.182-183)`. **Lemma 8.3**: m operations spend O(m log m) in `rebuild`, by a credit scheme `[from source] (ODS p.183-184)`.
- **Theorem 8.1**: add/remove/find in O(log n) ignoring `rebuild`; total O(m log m) in rebuilds over m operations `[from source] (ODS p.184-185)`. The book's table summarizes it as find worst-case O(log n) and add/remove amortized O(log n) `[from source] (ODS p.38)`.
- Subtree sizes are **not** stored in the book: `size(u)` is computed while looking for the scapegoat; the book suggests storing them as an optimization (Exercises 8.5 and 8.6) `[from source] (ODS p.180-182, 186)`. `[inference]` Hence the basic ScapegoatTree has no color, height or priority in its nodes; "zero metadata" and "3 pointers per node" are the package's summary, not claims by the book.
- Practical performance: the book warns that the implementation is usually **much slower** than the other SSets; there are sequences of n operations with Θ(n log n) time in `rebuild` (Exercise 8.3), unlike other structures that make only O(n) structural changes; it can be worthwhile when data associated with the nodes cannot be updated in constant time during a rotation `[from source] (ODS p.185-186)`. The names: Galperin and Rivest (1993), Andersson's "general balanced trees" `[from source] (ODS p.185, 316)`.

## 5. When to use what (book summary; see also `arvores-rubro-negras.md`)
| Structure | find | add/remove | Source |
|---|---|---|---|
| Treap | O(log n) expected | O(log n) expected | `[from source] (ODS p.38, 170)` |
| ScapegoatTree | O(log n) worst case | O(log n) amortized | `[from source] (ODS p.38, 184)` |
| RedBlackTree | O(log n) worst case | O(log n) worst case | `[from source] (ODS p.38, 208)` |
- Choose by guarantee: Ch. 9 contrasts that skiplists and treaps have only expected times and the scapegoat tree only amortized times for add/remove `[from source] (ODS p.189)`.
