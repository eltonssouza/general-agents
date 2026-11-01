# Binary trees and BinarySearchTree (Ch. 6)

Pages = PDF (printed = N − 12). Source: ODS Ch. 6 (p.139-156).

## 1. Terminology and representation
- Rooted binary tree: the root node `r` has degree at most 2; the parent of `u` is the second node on the path from `u` to `r`; ordered trees distinguish left and right child `[from source] (ODS p.139)`.
- The **depth** of `u` is the length of the path to the root; the **height** of a node is the length of the longest path to a descendant; the height of the tree is that of the root; a leaf is a node without children `[from source] (ODS p.139)`.
- With imaginary external nodes, a tree with n ≥ 1 real nodes has n+1 external nodes `[from source] (ODS p.141)`.
- Representation: each node stores `left`, `right` and `parent` (or `nil`); the tree is a reference to the root `r` `[from source] (ODS p.141)`. `depth(u)` climbs through `parent` to the root `[from source] (ODS p.141)`.
- Beware of the pseudocode conventions: the book's `height(u)` returns 0 for `nil` and therefore 1 + max(...) for a leaf, which differs from the textual definition (height 0 for a leaf, p.139). The book does not define the height of the empty tree; "height −1" for the empty tree is `[extrapolation]` `[from source] (ODS p.142)`.

## 2. Recursive algorithms and traversals
- `size(u)` and `height(u)` are recursive; the recursion depth is the height of the tree, which can overflow the stack if the tree is very tall `[from source] (ODS p.141-142)`.
- Traversal without recursion: with the `parent` pointer, the next node is decided by where we came from (from `parent`: go to the left child; from the left: go to the right; from the right: go back to the parent) `[from source] (ODS p.142-143)`; `traverse2` and `size2` use only the variables `u`, `prv`, `nxt` `[from source] (ODS p.143-144)`.
- `[inference]` Since each edge is traversed twice and there are only local variables, the cost is O(n) and the additional space O(1); the book does not state these bounds.
- Without the `parent` field it is still possible, but a List or Stack is needed for the path to the root `[from source] (ODS p.144)`.
- Breadth-first traversal: uses a queue (`bf_traverse` with `ArrayQueue`), level by level, from left to right `[from source] (ODS p.144-145)`.
- Pre-order, in-order and post-order are defined in the exercises `[from source] (ODS p.153-154)`.

## 3. BinarySearchTree
- Each node stores a value `x` from a total order; property: every key in the left subtree of `u` is smaller than `u.x` and every key in the right subtree is larger `[from source] (ODS p.145)`.
- `find_eq(x)` follows the search path and returns `x` or `nil`; `find(x)` (SSet) remembers the last node where it went left and returns the smallest value ≥ x `[from source] (ODS p.145-147)`.
- `add(x)`: searches for `x` and, if absent, inserts a leaf as a child of the last visited node (`find_last`, `add_child`) `[from source] (ODS p.147-149)`; the cost is proportional to the depth of the new node, in the worst case the height of the tree `[from source] (ODS p.149)`.
- `remove`: a leaf or a node with one child (`splice`); with two children, the value is swapped with the smallest value of the right subtree (the successor, which has no left child) and that node is spliced out `[from source] (ODS p.149-151)`.
- **Theorem 6.1**: add/remove/find in O(n) per operation; the book calls it "unimpressive" and compares it with the expected O(log n) of the SkiplistSSet `[from source] (ODS p.151)`.
- The tree can become a chain of n nodes (all, except the last, with one child) `[from source] (ODS p.152)`. Example: inserting 0,1,...,14 in order produces a list of height n−1 `[from source] (ODS p.157)`; Exercise 6.15 asks to count the sequences that give height n−1 `[from source] (ODS p.155)`.
- The following chapters give expected O(log n) (Ch. 7), amortized (Ch. 8) and worst-case (Ch. 9, simulating a tree with up to four children) `[from source] (ODS p.152)`.

## 4. Design decisions (chapter discussion)
- Whether or not to store `parent`: if the operations only follow paths from the root to a leaf, `parent` wastes space and is a source of errors; without `parent`, traversals require recursion or an explicit stack `[from source] (ODS p.152)`.
- Storing the children and the parent in an array `p` of size 3 simplifies the code (for example, the next node in a traversal is `u.p[(i+1) mod 3]`) `[from source] (ODS p.152-153)`.
- Binary search trees arose independently in several groups in the 1950s `[from source] (ODS p.152)` `[DATED]`.
