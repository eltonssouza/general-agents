# Heaps and priority queues (Ch. 10)

Pages = PDF (printed = N − 12). Source: ODS Ch. 10 (p.215-228). Both implementations are priority queues (the `remove()` operation returns the smallest element) `[from source] (ODS p.17, 215)`.

## 1. BinaryHeap (implicit binary tree)
- Uses Eytzinger's method: the nodes of a **complete** binary tree in breadth-first order in an array `a`; root at 0 `[from source] (ODS p.215)`.
- Indices: `left(i) = 2i+1`, `right(i) = 2(i+1)`, `parent(i) = (i−1) div 2` `[from source] (ODS p.215-216)`.
- Heap order: the value at `i` is not smaller than that at `parent(i)` (except at the root); hence the smallest is at position 0 (the root) `[from source] (ODS p.216)`.
- `add(x)`: grows `a` if necessary (`resize`), writes to `a[n]` and runs `bubble_up(n−1)`, swapping with the parent while smaller `[from source] (ODS p.217)`.
- `remove()`: saves `a[0]`, moves `a[n−1]` to the root, decrements `n` and runs `trickle_down(0)`, swapping with the **smaller of the children** while that child is smaller; shrinks the array if `3·n < length(a)` `[from source] (ODS p.217-219)`.
- Cost: the height h of a complete tree satisfies n ≥ 2^h, hence h ≤ log n, and add/remove are O(log n) **ignoring `resize()`**; the cost of `resize` is amortized by Lemma 2.1 `[from source] (ODS p.219-221)`.
- **Theorem 10.1**: add and remove in O(log n) per operation, ignoring `resize`; O(m) in total for `resize` over m operations `[from source] (ODS p.221)`. Table 1.2 marks add/remove as **amortized** O(log n) and `find_min` as O(1) `[from source] (ODS p.38)`. `[inference]` In individual operations that trigger `resize`, the cost is Θ(n); a strict "worst case" holds only if the backing array has preallocated capacity.
- Origin: the implicit representation is attributed to Eytzinger (genealogical trees) and the BinaryHeap to Williams `[from source] (ODS p.226)`.

## 2. MeldableHeap (randomized meldable heap)
- A heap-ordered binary tree **with no shape restriction**; add and remove are defined through `merge(h1, h2)`, which joins the trees rooted at `h1` and `h2` `[from source] (ODS p.221)`. (The name `meld` appears only in the chapter introduction, p.215; the pseudocode uses `merge`.)
- `merge`: if one of the sides is `nil`, returns the other; ensures `h1.x ≤ h2.x` by swapping if needed; flips a coin (`random_bit`) to decide whether to merge `h2` with `h1.left` or `h1.right`, recursively `[from source] (ODS p.221-222)`.
- `add(x)`: creates a node `u` and does `merge(u, r)`; `remove()`: saves `r.x` and does `merge(r.left, r.right)`; both expected O(log n) `[from source] (ODS p.222-224)`. `remove(u)` and `absorb(h)` are also expected O(log n), with a constant number of merges `[from source] (ODS p.224)`.
- **Analysis**: a random walk in a binary tree with n nodes has expected length at most log(n+1) (Lemma 10.1, by induction or by entropy); `merge` traverses two walks, hence ≤ log(n₁+1) + log(n₂+1) ≤ 2 log n expected steps (Lemma 10.2) `[from source] (ODS p.224-226)`.
- **Theorem 10.2**: add and remove in expected O(log n) `[from source] (ODS p.226)`.
- `[inference]` The BinaryHeap does not offer a sublinear `merge` (it would need to reorganize the two arrays); the book does not state this cost. Choose based on the need for `merge`/`absorb`.
- The heaps cited in the discussion (leftist, binomial, Fibonacci, pairing, skew) are only named, without an algorithm; `decrease_key(u,y)` is O(log n) by removing and inserting, amortized O(1) in Fibonacci heaps `[from source] (ODS p.226-227)`. Everything else is `[extrapolation]`.
- Useful exercises: `remove(i)` in O(log n) in a BinaryHeap (and why it is not useful), d-ary heap by Eytzinger, finding the second smallest in O(1) and the k-th smallest in O(k log k) `[from source] (ODS p.227-228)`.

## 3. Use in sorting
The BinaryHeap underpins heap-sort (see `ordenacao-e-limites-inferiores.md`) `[from source] (ODS p.215, 237)`.
