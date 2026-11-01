# Array-based lists (Ch. 2)

Pages = PDF (printed = N − 12). Source: ODS Ch. 2 (p.43-71). The book's costs **ignore** the cost of growing/shrinking the backing array; a separate lemma shows that this cost sums to O(m) over m operations `[from source] (ODS p.43-44)`.

## 1. ArrayStack
- Implements List with a backing array `a`; `n` counts the elements and `length(a) ≥ n` `[from source] (ODS p.44)`. `get(i)` and `set(i,x)` access `a[i]` `[from source] (ODS p.44-45)`.
- `add(i,x)` shifts the elements of `a` at indices i to n−1 one position to the right and costs O(n−i) without counting the resize; `remove(i)` shifts left, also O(n−i) `[from source] (ODS p.45-47)`.
- **Resize rule**: in `add`, if `n = length(a)` it calls `resize()`; in `remove`, if `length(a) ≥ 3·n` it calls `resize()`; `resize()` allocates a new array of size `max(1, 2n)` and copies the `n` elements `[from source] (ODS p.45, 47)`.
- **Lemma 2.1**: starting from empty, any sequence of m calls to `add`/`remove` spends O(m) in total in `resize()`. The proof shows that between two `resize()` calls there are at least nᵢ/2 − 1 operations (nᵢ = n at the i-th call) `[from source] (ODS p.47-48)`.
- **Theorem 2.1**: get/set O(1); add/remove O(1+n−i) ignoring resize; push as `add(n,x)` and pop as `remove(n-1)` run in amortized O(1) `[from source] (ODS p.49)`.
- `[inference]` After a `resize()` the array has size 2n; since shrinking only occurs at `length(a) ≥ 3n`, the unused space stays below 2n positions. The book only says that there are moments with one third occupancy `[from source] (ODS p.62)`.
- `[extrapolation]` Growing by +c (instead of doubling) leads to quadratic total cost for n insertions (Θ(n²/c)); the book does not analyze this case. `scripts/structure_simulator.py` and `calculate_amortized.py --growth additive` simulate the comparison as a teaching tool.

## 2. FastArrayStack
- Same structure, replacing the copy loops with optimized routines (`memcpy`, `memmove`, `System.arraycopy`) `[from source] (ODS p.49)`. Asymptotically the same; in the author's C++ and Java implementations the gain was a factor between 2 and 3 `[from source] (ODS p.49-50)`.
- `[extrapolation]` In Python, slice assignment (`a[i+1:n+1] = a[i:n]`) is the analogue; the book presents pseudocode with subarray assignment (ODS p.34, 45), whose cost remains O(size of the segment) `[from source] (ODS p.34)`.

## 3. ArrayQueue (FIFO queue in a circular array)
- ArrayStack is a poor choice for FIFO because one of the sides requires `i = 0`, a cost proportional to n `[from source] (ODS p.50)`.
- It stores `j` (index of the next to leave) and `n`; the elements are at `a[(j+i) mod length(a)]`, simulating an infinite array through modular arithmetic `[from source] (ODS p.50-51)`.
- `add(x)` writes to `a[(j+n) mod length(a)]`; `remove()` reads `a[j]` and does `j ← (j+1) mod length(a)`; `resize()` copies starting at `j` to the beginning of the new array (size `max(1, 2n)`) and resets `j`; it shrinks when `length(a) ≥ 3n` `[from source] (ODS p.51-53)`.
- **Theorem 2.2**: add/remove O(1) ignoring resize; over m operations the total resize cost is O(m) `[from source] (ODS p.53)`.

## 4. ArrayDeque
- Same circular array, now as a List: `get`/`set` access `a[(j+i) mod length(a)]` `[from source] (ODS p.54)`.
- `add(i,x)`: if `i < n/2` it shifts the first `i` elements one position to the left (decrementing `j`); otherwise it shifts the elements at indices i to n−1 to the right. Thus it never shifts more than `min{i, n−i}` elements `[from source] (ODS p.54-55)`.
- **Theorem 2.3**: get/set O(1); add/remove O(1+min{i, n−i}) ignoring resize; O(m) in total in resize `[from source] (ODS p.56)`.

## 5. DualArrayDeque (two stacks)
- Two ArrayStacks, `front` (indices 0..front.size()−1, **in reverse order**) and `back` (normal order); `n = front.size() + back.size()` is not stored `[from source] (ODS p.56-57)`.
- `balance()` ensures, if `size() ≥ 2`, that `3·front.size() ≥ back.size()` and `3·back.size() ≥ front.size()`; when the condition fails, it redistributes to ⌊n/2⌋ and ⌈n/2⌉ elements in O(n) `[from source] (ODS p.59-60)`.
- **Lemma 2.2** (potential Φ = absolute difference between `front.size()` and `back.size()`): m operations spend O(m) in total in `balance()` `[from source] (ODS p.60-62)`.
- **Theorem 2.4**: get/set O(1); add/remove O(1+min{i, n−i}) ignoring resize and balance; O(m) in total in them `[from source] (ODS p.62)`. The book says it is asymptotically equal to ArrayDeque and serves as an example of combining two simple structures `[from source] (ODS p.56-57)`.

## 6. RootishArrayStack
- Motivation: the previous arrays are often not very full; RootishArrayStack stores n elements in O(√n) arrays and wastes O(√n) positions `[from source] (ODS p.62)`.
- Block `b` has `b+1` positions; r blocks hold `r(r+1)/2` elements `[from source] (ODS p.62-63)`.
- Given `i`, the block is `b = ⌈(−3 + √(9+8i))/2⌉` and the internal position is `j = i − b(b+1)/2` `[from source] (ODS p.63-64)`. `get`/`set` cost O(1) if the list of blocks has O(1) access `[from source] (ODS p.64-65)`.
- `add` calls `grow()` (a new block of size `blocks.size()+1`) when `r(r+1)/2 < n+1`; `remove` calls `shrink()` when `(r−2)(r−1)/2 ≥ n`, removing unused blocks `[from source] (ODS p.65-66)`.
- Cost: shifting O(1+n−i) in add and O(n−i) in remove; `grow`/`shrink` do not copy data and are amortized over at least r−1 operations `[from source] (ODS p.66-67)`.
- **Space**: there are never more than two blocks that are not completely full; `(r−2)(r−1) ≤ n` holds, hence `r ≤ (3+√(1+4n))/2`; the last two blocks have sizes r and r−1, waste ≤ 2r−1 = O(√n); the list of blocks adds O(r) `[from source] (ODS p.67)`.
- **Optimality**: any structure that starts empty and accepts insertions one by one wastes √n at some point `[from source] (ODS p.67-68)`.
- **Theorem 2.5**: space `n + O(√n)` words `[from source] (ODS p.68)`.
- Discussion: the idea comes from Brodnik et al. (Rootish) and from Goodrich and Kloss (tiered-vector) `[from source] (ODS p.69)`.

## 7. Comparative summary (Ch. 2; costs without resize) `[from source] (ODS p.43)`
| Structure | get/set | add/remove |
|---|---|---|
| ArrayStack | O(1) | O(n−i) |
| ArrayDeque | O(1) | O(min{i, n−i}) |
| DualArrayDeque | O(1) | O(min{i, n−i}) |
| RootishArrayStack | O(1) | O(n−i) |
