# 2-4 trees and RedBlackTree (Ch. 9)

Pages = PDF (printed = N − 12). Source: ODS Ch. 9 (p.189-213). Note: the book implements **one** variant (left-leaning); "classic" descriptions of red-black trees with red/black uncle and rotation counts from other texts are `[extrapolation]`.

## 1. Why red-black trees (the book's motivation)
Height at most 2 log n; add/remove in worst-case O(log n); a constant **amortized** number of rotations per operation `[from source] (ODS p.189)`. They contrast with skiplists and treaps (expected time) and scapegoat (amortized) `[from source] (ODS p.189)`. The price is implementation complexity: a mistake in a rotation or color produces hard-to-find bugs `[from source] (ODS p.189-190)`. The book states that they are used in libraries (Java Collections Framework, C++ STL) and in the Linux kernel `[from source] (ODS p.189)` `[DATED]`.

## 2. 2-4 trees
- Properties: all leaves have the same depth (height); every internal node has 2, 3 or 4 children `[from source] (ODS p.190)`. **Lemma 9.1**: with n leaves, height ≤ log n `[from source] (ODS p.190)`.
- Adding a leaf: if the parent ends up with 5 children, it is split into nodes with 2 and 3 children and the process repeats upward; if the root splits, a new root is created (all leaves gain depth) `[from source] (ODS p.191)`.
- Removing a leaf: if the parent is left with 1 child, borrow from the sibling (if it has 3 or 4) or merge (if it has 2); if the root is left with one child, it is removed `[from source] (ODS p.191-193)`.
- Both operations end in at most log n steps `[from source] (ODS p.191-194)`. The 2-4 tree is the case B = 2 of a B-tree `[from source] (ODS p.290)`.

## 3. RedBlackTree
- Each node has a color: red = 0, black = 1 `[from source] (ODS p.194)`. Two properties:
  - **9.3 black-height**: the same number of black nodes on every path from the root to a leaf (constant sum of colors);
  - **9.4 no-red-edge**: two red nodes are not adjacent (`u.colour + u.parent.colour ≥ 1`, except at the root) `[from source] (ODS p.194)`.
- Conventions: the root can always be painted black and the algorithms keep it black; external nodes (`nil`) count as black `[from source] (ODS p.194)`. That is, "black root" and "black nil" are conventions, not numbered properties.
- Variant in this book: property **9.5 left-leaning** (if `u.left` is black, `u.right` is black), which reduces cases and gives a unique representation of each 2-4 tree: degree 2 = black node with two black children; degree 3 = black with a red left child and a black right child; degree 4 = black with two red children `[from source] (ODS p.198)`.
- Relation to the 2-4 tree: removing each red node by linking its children to the black parent gives a 2-4 tree with n+1 leaves `[from source] (ODS p.195-196)`.
- **Lemma 9.2**: height ≤ 2 log n. The book's computation: the path has at most log(n+1) black nodes and log(n+1) − 1 red ones, hence length ≤ 2 log(n+1) − 2 ≤ 2 log n for n ≥ 1 `[from source] (ODS p.196)`.
- Subroutines (colors as numbers): `push_black(u)` (u black with two red children: u becomes red, children black), `pull_black(u)` (inverse), `flip_left(u)` and `flip_right(u)` (swap the colors of u and the child and rotate) `[from source] (ODS p.198-199)`.
- `add(x)`: inserts a red leaf as in the BST; `add_fixup(u)` fixes violations of no-red-edge and left-leaning: if `u` is the root, paint it black; if the sibling is also red, nothing to do; otherwise it may use `flip_left(w)` and, with grandparent `g`, `flip_right(g)` (stops) or `push_black(g)` (climbs with `u = g`) `[from source] (ODS p.200-202)`. Each iteration costs O(1) and `add_fixup` ends in O(log n) iterations `[from source] (ODS p.202)`.
- `remove(x)`: reduces to taking out (`splice`) a node `w` with one child `u` and adding `w.colour` to `u.colour`, which can produce "double black" (color 2) or violate left-leaning; `remove_fixup(u)` is a loop with cases 0 (root: paint black), 1 (red sibling), 2 (black sibling and `u` is a left child) and 3 (`u` is a right child) `[from source] (ODS p.203-208)`. Each iteration costs O(1); cases 2 and 3 terminate or climb, case 1 leads to case 3 which terminates; hence O(log n) `[from source] (ODS p.208)`.
- **Theorem 9.1**: add/remove/find in worst-case O(log n) `[from source] (ODS p.208)`. **Theorem 9.2**: starting from the empty tree, m operations spend O(m) in total in `add_fixup` and `remove_fixup` `[from source] (ODS p.208)`. Proof sketch by the potential of the 2-4 tree (Φ = 1, 0, 3 for nodes with 2, 3 and 4 children): at most 3m/2 splits/merges `[from source] (ODS p.209)`.
- **The book does not state** "at most 2 rotations on insertion and 3 on removal" or any other fixed cap on rotations per operation; only the amortized result above. If the user cites those numbers, label them `[extrapolation]` (a known result in the literature on other variants) or count rotations in the book's pseudocode `[inference]`.

## 4. Comparisons cited in the book
- AVL: height balanced per node (subtrees differ by at most 1); the Fibonacci recurrence leads to h ≤ log_φ n ≈ 1.44 log n, lower than the red-black tree; the book shows no pseudocode and says that AVL and the Andersson and Sedgewick variants are simpler, but **without** the analogue of Theorem 9.2 (amortized O(1) rebalancing) `[from source] (ODS p.210-212)`.
- Variants: Guibas and Sedgewick introduced red-black trees; Andersson describes a left-leaning variant that simulates 2-3 trees; Sedgewick describes two recursive versions `[from source] (ODS p.210)`.
- Exercise 9.4/9.6: there are red-black trees with n nodes and height 2 log n − O(1) `[from source] (ODS p.212)`.

## 5. Summary table of tree SSets (see also `arvores-balanceadas-e-treaps.md`)
| Structure | find | add/remove | Source |
|---|---|---|---|
| BinarySearchTree | O(n) | O(n) | `[from source] (ODS p.151)` |
| Treap | O(log n) expected | O(log n) expected | `[from source] (ODS p.38)` |
| ScapegoatTree | O(log n) worst case | O(log n) amortized | `[from source] (ODS p.38)` |
| RedBlackTree | O(log n) worst case | O(log n) worst case | `[from source] (ODS p.38, 208)` |
The per-node metadata size (color 0/1; numeric priority; nothing) is in `[from source] (ODS p.163, 194)` and in the Scapegoat section.
