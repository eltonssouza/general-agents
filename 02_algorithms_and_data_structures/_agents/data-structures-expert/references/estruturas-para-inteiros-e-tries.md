# Data structures for integers: BinaryTrie, XFastTrie and YFastTrie (Ch. 13)

Pages = PDF (printed = N − 12). Source: ODS Ch. 13 (p.269-286). All implement SSet for `w`-bit integers in {0,...,2^w − 1}; the code uses `int_value(x)` to associate an integer with an element `[from source] (ODS p.269)`.

## 1. Overview
- BinaryTrie: add/remove/find in O(w). Since n ≤ 2^w, log n ≤ w, and the book's comparison-based SSets are at least as fast as it; XFastTrie: find in O(log w), add/remove in O(w), space O(n·w); YFastTrie: add/remove in O(log w) and space O(n) `[from source] (ODS p.269)`.
- `[inference]` Beating O(log n) only makes sense when log w < log n, that is, when n is large relative to w; for small sets of 64-bit integers, comparison-based structures (for example Treap or RedBlackTree) are usually enough.
- The book cites van Emde Boas trees (size 2^w) and fusion trees (O((log n)/(log w)) for find; combined with the YFastTrie they give O(√log n)) as context `[from source] (ODS p.284-285)`.

## 2. BinaryTrie
- A binary tree in which all leaves have depth `w`; each integer is a path from the root to a leaf: level i turns left if the i-th most significant bit is 0 and right if it is 1 (example w = 4 with 3, 9, 12, 13) `[from source] (ODS p.270)`.
- The `child[0]`/`child[1]` pointers of the leaves are reused as `prev`/`next` of a doubly linked list of the leaves in order, with a `dummy` node before the first and after the last `[from source] (ODS p.270)`.
- Each node has `jump`: if the left child is missing, `jump` points to the **smallest** leaf of the subtree; if the right child is missing, it points to the **largest** leaf `[from source] (ODS p.270-271)`.
- `find(x)`: follows the path of x; if it reaches a leaf, it found it; if it cannot continue, it follows `u.jump` and, depending on whether the left or the right child is missing, uses the list of leaves to reach the successor; cost O(w) `[from source] (ODS p.271-272)`.
- `add(x)`: follows the path as far as it can, creates the rest down to the leaf, inserts it in the list of leaves and climbs updating `jump`; `remove(x)`: undoes this; both O(w) `[from source] (ODS p.272-276)`.
- **Theorem 13.1**: add/remove/find in O(w) and space O(n·w) `[from source] (ODS p.276)`.

## 3. XFastTrie
- A BinaryTrie plus `w+1` hash tables `t[0],...,t[w]`: `t[i]` stores the nodes of level i, labeled by the i most significant bits, in a hash-based USet (Ch. 5) `[from source] (ODS p.276-277)`.
- `find(x)`: binary search over the levels (`l = 0`, `h = w+1`) using `t[i].find(x ≫ (w−i))` to know whether the node is at the level or below; on finding the deepest node, it completes with `u.jump` and the list of leaves; expected O(log w) `[from source] (ODS p.277-278)`.
- `add`/`remove` are almost the same as those of the BinaryTrie, maintaining the hash tables; **Theorem 13.2**: add/remove expected O(w), find expected O(log w), space O(n·w) `[from source] (ODS p.278-279)`.

## 4. YFastTrie
- Idea: an XFastTrie `xft` stores only a **random sample** of the data (each element enters with probability 1/w; the value 2^w − 1 is always in `xft`); the remaining elements are in Treaps (Section 7.2), one per sampled element `xᵢ`, storing the keys in {xᵢ₋₁+1,...,xᵢ} `[from source] (ODS p.279-280)`.
- `find(x)`: looks in `xft` for the correct Treap and does `find` in the Treap; O(log w) + O(log r), with r the size of the Treap `[from source] (ODS p.280-281)`.
- `add(x)`: inserts into the Treap and, with probability 1/w, splits the Treap (`split`, Exercise 7.12) and inserts the pair into `xft` at cost O(w); expected O(log w) + (1/w)·O(w) = O(log w) `[from source] (ODS p.281)`. `remove(x)`: removes from the Treap; if x was in `xft`, merges (`absorb`) its Treap into the successor's Treap and removes from `xft` `[from source] (ODS p.281-283)`.
- **Lemma 13.1**: the expected number of elements of the Treap that contains x is ≤ 2w − 1 (two biased coin experiments, p = 1/w) `[from source] (ODS p.283-284)`.
- **Theorem 13.3**: add/remove/find in expected O(log w); space O(n + w) (the w term comes from the always-present value 2^w − 1; it can be eliminated with extra cases in the code) `[from source] (ODS p.284)`. Table 1.2 marks O(log w) amortized and expected `[from source] (ODS p.38)`.
- `[extrapolation]` Descriptions of the y-fast trie with blocks of size between w/4 and 2w, deterministic split/merge and amortized cost come from other texts; they are **not** the book's structure, which uses 1/w random sampling and expected sizes.
- Origin: the XFastTrie and YFastTrie are by Willard (1983) `[from source] (ODS p.285, 320)`.

## 5. Useful exercises (all in the book)
A BinaryTrie variant without list or `jump` (13.1), an XFastTrie with only a linked list and hash tables (13.2), a trie for variable-length strings (13.3), `find` in O(1 + log d(x)) and O(1 + log log d(x)) (13.4) `[from source] (ODS p.285-286)`.

## 6. Cautions
- `[extrapolation]` log₂ 32 = 5 and log₂ 64 = 6 are arithmetic; the book does not make this comparison.
- Expected/amortized time: the guarantees of the three structures depend on hashing (XFast) and coins (YFast); the book gives no worst-case bounds for them.
