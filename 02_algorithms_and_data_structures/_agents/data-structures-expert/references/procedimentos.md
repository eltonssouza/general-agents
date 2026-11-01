# Operating procedures

Pages = PDF (printed = N − 12). Each routine says where it comes from: `[from source]` when it follows the book's pseudocode or proof, `[inference]` when it is a derived method, `[extrapolation]` when it is a general external method.

## 1. How to choose the structure (decision routine) `[inference]` from Tables 1.1 and 1.2 `[from source] (ODS p.36, 38)`
1. Define the interface: access by index (List), by equality (USet) or by order/successor (SSet); priority queue (heap) `[from source] (ODS p.18-21)`.
2. If order is not needed, prefer USet; the book says to use USet unless successor search is really needed `[from source] (ODS p.21)`.
3. Choose the required guarantee: worst case (RedBlackTree, DLList, BinaryTrie), amortized (ArrayStack, ScapegoatTree, BinaryHeap) or expected (hash, Treap, Skiplist, MeldableHeap) `[from source] (ODS p.32, 38)`.
4. Look up the cost with `scripts/ods_cost_lookup.py "<structure>"`; check the page.
5. If the data are `w`-bit integers and `log w` is much smaller than `log n`, consider XFastTrie/YFastTrie `[inference]`; the bounds are in `[from source] (ODS p.269, 276, 284)`.
6. If the data do not fit in RAM, use the external memory model and a B-tree with B chosen for the block `[from source] (ODS p.287-291)`.

## 2. How to prove an amortized cost (three techniques the book uses)
- **Counting between expensive events** (ArrayStack): show that between two `resize()` calls there are at least nᵢ/2 − 1 operations and sum `[from source] (ODS p.47-48)`. The same format applies to `balance()` of the DualArrayDeque `[from source] (ODS p.60-62)`.
- **Potential** (DualArrayDeque, SEList, 2-4 tree): define Φ ≥ 0 that measures "disorder", show that the expensive operation reduces Φ by an amount proportional to its cost and that the cheap operation increases Φ only a little `[from source] (ODS p.61, 88-89, 209)`. SEList example: Φ = number of fragile nodes; each `spread` reduces Φ by b−1 `[from source] (ODS p.88-89)`.
- **Credits** (ScapegoatTree, B-tree): each operation distributes credits that pay for future rebuilds `[from source] (ODS p.183-184, 305-307)`.
- `[extrapolation]` General form: amortized cost aᵢ = cᵢ + Φ(Sᵢ) − Φ(Sᵢ₋₁), with Φ(S₀) = 0 and Φ ≥ 0; the sum of cᵢ does not exceed the sum of aᵢ. The book does not write this formula.
- To test numerically: `scripts/structure_simulator.py arraystack|dualarraydeque|selist|scapegoat --check`.

## 3. Rotation in a binary search tree `[from source] (ODS p.165-166)`
`rotate_left(u)` (raises `w = u.right`):
```
w = u.right
w.parent = u.parent
if w.parent != nil:  if w.parent.left == u: w.parent.left = w  else: w.parent.right = w
u.right = w.left
if u.right != nil:  u.right.parent = u
u.parent = w;  w.left = u
if u == r:  r = w;  r.parent = nil
```
`rotate_right(u)` is symmetric with `w = u.left`. Check: the in-order sequence does not change; the depth of `w` drops by 1 and that of `u` rises by 1 `[from source] (ODS p.166)`. The simulator `scripts/simulate_rotation.py` prints before/after.

## 4. Partial rebuilding in the ScapegoatTree `[from source] (ODS p.177-178, 180)`
1. After inserting the leaf `u`, if `depth(u) > log_{3/2} q`, climb from `u` looking for `w` such that `size(w.child) / size(w) > 2/3` (the book uses `3·size(w) ≤ 2·size(w.parent)` in the loop) `[from source] (ODS p.180)`.
2. `rebuild(w.parent)`: packs the subtree into an in-order array (`pack_into_array`) and rebuilds with `build_balanced`, using `m = ns div 2` as the root `[from source] (ODS p.177-178)`.
3. In `remove`, if `2n < q`, rebuild the root and set `q = n` `[from source] (ODS p.181)`.

## 5. Node split in a B-tree `[from source] (ODS p.294)`
1. The node `u` has 2B keys (2B+1 children).
2. `w` is created, which gets the B largest keys of `u.keys` (indices B to 2B−1) and the children of `u.children` at indices B to 2B.
3. `u` is left with B children; the key `u.keys[B−1]` goes up to the parent, which adopts `w`.
4. If the parent becomes full, repeat; if the root splits, a new root is created with the two nodes `[from source] (ODS p.296-298)`. After the split the nodes have B−1 and B keys `[from source] (ODS p.306)`.

## 6. Auditing a LinearHashTable `[from source] (ODS p.121-123)`
1. Each cell is data, `nil` or `del`; `n` counts data and `q` counts data plus `del`.
2. Check the invariant `length(t) ≥ 2q` and `length(t) = 2^d`.
3. `add`: if `2(q+1) > length(t)`, `resize()`; probe until `nil` or `del`; only increment `q` if the cell was `nil`.
4. `remove`: writes `del`; if `8n < length(t)`, `resize()`.
5. `resize()`: smallest `d` with `2^d ≥ 3n`; reinserts only data; `q = n`.
6. Use `scripts/analyze_hash_probes.py --demo invariant` to see the effect.

## 7. Computing the space of RootishArrayStack and SEList `[from source] (ODS p.63-64, 67, 81)`
- Rootish: `b = ⌈(−3 + √(9+8i))/2⌉`, `j = i − b(b+1)/2`; `r` blocks with `(r−2)(r−1) ≤ n` and waste ≤ 2r−1.
- SEList: at most `n/(b−1) + 1` blocks, waste O(b + n/b); see `scripts/calculate_amortized.py --mode rootish|selist`.
