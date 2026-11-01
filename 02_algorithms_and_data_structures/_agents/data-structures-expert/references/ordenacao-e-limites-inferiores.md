# Sorting and lower bound (Ch. 11)

Pages = PDF (printed = N − 12). Source: ODS Ch. 11 (p.229-249). All the sorting algorithms in the chapter take an array `a` and sort it in non-decreasing order.

## 1. Context
- Two of the sorts (quicksort and heap-sort) are tied to structures already seen (random binary search trees and heaps) `[from source] (ODS p.229)`. One can also sort by inserting n elements into a BinaryHeap/MeldableHeap and removing, or by inserting into a search tree and traversing in-order, but with a lot of overhead; hence it is worth developing direct methods `[from source] (ODS p.229)`.
- Three comparison-based O(n log n) algorithms and two (counting sort and radix sort) that use array indexing `[from source] (ODS p.229-230)`.

## 2. Merge-sort
- Divide and conquer: splits `a` into two halves, sorts recursively and merges (`merge`); returns if `length(a) ≤ 1` `[from source] (ODS p.230-231)`.
- `merge` makes at most n−1 comparisons for n elements in total `[from source] (ODS p.231-232)`.
- **Theorem 11.1**: O(n log n) time and at most n log n comparisons `[from source] (ODS p.233-234)`.
- It uses an auxiliary array in the merging phase, which can be expensive and is a point of failure if memory is limited; it is the "clear winner" for sorting linked lists, where it needs no auxiliary array (Exercise 11.2) `[from source] (ODS p.247)`. The stability of merge-sort is not discussed in the book; it is `[extrapolation]` (the pseudocode's merge uses `≤`, which in practice preserves the order of equal elements `[inference]`).

## 3. Quicksort
- Chooses a **random** pivot `x`, partitions in the array itself (in-place) into smaller than `x`, equal to `x` and larger than `x`, and recursively sorts the first and third groups `[from source] (ODS p.234-235)`.
- The recursion of quicksort is a random binary search tree (Section 7.1); Lemma 7.1 becomes **Lemma 11.1**: the expected number of comparisons of element i with pivots is ≤ H_{i+1} + H_{n−i} `[from source] (ODS p.235-236)`.
- **Theorem 11.2/11.3**: expected number of comparisons ≤ 2n ln n + O(n); with duplicates the result is at least as good; expected O(n log n) time `[from source] (ODS p.236-237)`. The book's table gives `1.38 n log n + O(n)` expected comparisons `[from source] (ODS p.247)`.
- Guarantee: it is randomized, "the time is not always guaranteed"; implementations with a fixed pivot (first element, middle element) have bad inputs that cause C(n,2) comparisons (Exercises 11.3-11.5) `[from source] (ODS p.247-248)`.
- `[extrapolation]` Θ(n²) as the worst case, O(log n) recursion stack and instability are not stated in the book.

## 4. Heap-sort
- In-place: converts `a` into a BinaryHeap (min-heap, smallest at the root) and repeatedly swaps `a[0]` with `a[n−1]`, decrements `n` and runs `trickle_down(0)`; at the end the array is in decreasing order and is reversed (`a.reverse()`) `[from source] (ODS p.237-238)`. The book notes that `compare` can be redefined to obtain increasing order directly `[from source] (ODS p.237)`.
- Bottom-up heap construction in O(n) (calls `trickle_down(i)` for i from ⌊n/2⌋−1 down to 0; half the nodes have no children), better than n calls to `add` `[from source] (ODS p.238-239)`.
- **Theorem 11.4**: O(n log n) time and at most 2n log n + O(n) comparisons `[from source] (ODS p.239)`.
- `[extrapolation]` The book does not use a max-heap nor discuss the stability of heap-sort.

## 5. Book comparison (table, ODS p.247)
| Algorithm | Comparisons | In-place |
|---|---|---|
| Merge-sort | n log n, worst case | No |
| Quicksort | 1.38 n log n + O(n), expected | Yes |
| Heap-sort | 2 n log n + O(n), worst case | Yes |
The book summarizes: merge-sort makes fewer comparisons and uses no randomness, but uses an auxiliary array; quicksort is in-place and close in comparisons, but is randomized; heap-sort makes more comparisons, is in-place and deterministic `[from source] (ODS p.247)`.

## 6. Lower bound for comparison sorting
- Any deterministic comparison-based algorithm, for fixed n, is a binary **comparison tree**: each internal node compares two indices; each leaf labels a permutation `[from source] (ODS p.240)`.
- The tree must have at least n! leaves; otherwise two permutations would lead to the same leaf and one would be sorted incorrectly (Figure 11.6 shows a tree with 4 < 3! leaves) `[from source] (ODS p.241)`.
- **Theorem 11.5**: for every deterministic algorithm and every n ≥ 1 there is an input with at least log(n!) = n log n − O(n) comparisons; a binary tree with k leaves has height at least log k `[from source] (ODS p.241)`.
- **Theorem 11.6**: it also holds for randomized algorithms, in expectation, over a random permutation (fixing the random bits, the algorithm becomes deterministic) `[from source] (ODS p.241-242)`.
- The book states `log(n!) = n log n − O(n)` (ODS p.239) and leaves the proof to Exercise 11.10 (ODS p.249). The comparison of log n! with ∫ log x dx (Stirling) used in some texts is `[extrapolation]`.

## 7. Counting sort
- Input: n integers in {0,...,k−1}. Counts occurrences in `c`, sums prefixes (`c[i] ← c[i] + c[i−1]`), and scans `a` from back to front placing each element at `b[c[a[i]] − 1]` `[from source] (ODS p.243-245)`.
- **Theorem 11.7**: O(n + k) time `[from source] (ODS p.245)`. It is **stable** (preserves the order of equal elements), which radix sort uses `[from source] (ODS p.245)`.
- `[inference]` Extra space: an array of k counters and the output array of n positions. It is efficient when n is not much smaller than the largest value `[from source] (ODS p.245)`.

## 8. Radix sort
- Sorts `w`-bit integers with w/d passes of counting sort, d bits at a time, from least significant to most significant; d is assumed to divide w `[from source] (ODS p.245-246)`.
- Correct because counting sort is stable `[from source] (ODS p.246)`. **Theorem 11.8**: O((w/d)(n + 2^d)) `[from source] (ODS p.246)`.
- **Corollary 11.1**: with the values in {0,...,n^c − 1} and d = ⌈log n⌉, time O(cn) `[from source] (ODS p.246-247)`. "Linear" holds with constant c; it does not hold in general for arbitrary integers.
- Extensions: integers in any range {a,...,b}, and IEEE 754 floating-point numbers, comparable as integers `[from source] (ODS p.248)`. Radix sort as punched-card sorting since the 1920s `[from source] (ODS p.247-248)` `[DATED]`.
