# Hash tables (Ch. 5)

Pages = PDF (printed = N − 12). Source: ODS Ch. 5 (p.113-138). The chapter stores `w`-bit integers from the universe {0,...,2^w − 1}; for other types, an integer **hash code** is associated `[from source] (ODS p.113)`.
Terms that do **not** appear in the book: "tombstone"/"lápide", "primary clustering", "2-independent". The book uses "`del` values". Use those labels only as `[extrapolation]`.

## 1. ChainedHashTable (chaining)
- An array `t` of lists; `n` counts the items; maintains the invariant `n ≤ length(t)`, so that the average list length is ≤ 1 `[from source] (ODS p.113-114)`. The size is a power of 2 (`d` bits) `[from source] (ODS p.113)`.
- `add(x)`: if `find(x)` already finds it, returns false; if `n+1 > length(t)` calls `resize()` (doubles); appends `x` to `t[hash(x)]` `[from source] (ODS p.114)`. The growth analysis is that of ArrayStack (Lemma 2.1) `[from source] (ODS p.114-115)`.
- `remove(x)`: searches the list at `t[hash(x)]`; after removing, if `3·n < length(t)` calls `resize()` `[from source] (ODS p.115)`.
- Performance depends on the hash function: a good one spreads the elements; a bad one puts everything in the same position and the list has size n `[from source] (ODS p.115-116)`.

## 2. Multiplicative hashing
- Table of size 2^d; `hash(x) = ((z·x) mod 2^w) div 2^(w−d)`, with odd `z` drawn from {1,...,2^w − 1}; efficient implementation: multiply in `w` bits (modulo 2^w is automatic in C, C++, Java) and shift right `w−d` bits (`≫`) `[from source] (ODS p.116)`. In Python and Ruby, the result of an operation that overflows `w` bits is promoted to a variable-size integer `[from source] (ODS p.116)`; `[inference]` therefore, in those languages, the reduction modulo 2^w must be done explicitly (mask).
- **Lemma 5.1**: for x ≠ y, `Pr{hash(x) = hash(y)} ≤ 2/2^d` `[from source] (ODS p.116)`. The proof uses Lemma 5.3 (there is a unique odd z with zq mod 2^w = i, for odd q) `[from source] (ODS p.118-120)`. Exercise 5.3 asks to show that the bound 2/2^d is the best possible `[from source] (ODS p.136)`.
- **Lemma 5.2**: the expected length of the list `t[hash(x)]` is at most `n_x + 2`, with `n_x` the number of occurrences of x `[from source] (ODS p.117)`.
- **Theorem 5.1**: add/remove/find in expected O(1) ignoring `grow()`; over m operations the total of `grow()` is O(m) `[from source] (ODS p.120)`.
- `[extrapolation]` "universal" and "2-independent" are labels from the literature; the book cites Carter and Wegman (universal hashing) only in the discussion (ODS p.135).

## 3. LinearHashTable (open addressing)
- All elements are in `t`; on collision, it tries `t[(i+1) mod length(t)]`, `t[(i+2) mod length(t)]` etc. `[from source] (ODS p.120)`.
- Three kinds of entry: data values, `nil` (never held data) and `del` (held data and was erased) `[from source] (ODS p.121)`. `n` counts the data and `q` counts data plus `del`; the invariant is `length(t) ≥ 2q` and `length(t) = 2^d` `[from source] (ODS p.121)`.
- `find(x)`: probes until it finds `x` or `nil`; `del` does not stop the search `[from source] (ODS p.121-122)`.
- `add(x)`: first `find(x)`; if `2·(q+1) > length(t)`, `resize()`; probes until `nil` or `del` and writes `x` there; only increments `q` if the cell was `nil` `[from source] (ODS p.122)`.
- `remove(x)`: on finding `x` writes `del`, decrements `n` and, if `8·n < length(t)`, `resize()` `[from source] (ODS p.122-123)`.
- Correctness: no operation changes a non-`nil` entry to `nil`; hence, finding `nil` is proof that `x` was never written beyond that point `[from source] (ODS p.123)`. `[inference]` Therefore erasing by writing `nil` instead of `del` can interrupt the search for keys that passed through that cell.
- `resize()` is triggered by `add` when the non-`nil` entries exceed `length(t)/2` and by `remove` when the data fall below `length(t)/8`; it chooses the smallest `d` with `2^d ≥ 3n`, reallocates, reinserts only the data and sets `q ← n` (the `del` entries vanish) `[from source] (ODS p.123)`.

## 4. Analysis of linear probing
- The intuition "half the table is `nil`, so few probes" leads to the wrong conclusion that the expected number of positions examined is at most 2 `[from source] (ODS p.124)`.
- The analysis **assumes independent and uniform hash values** in {0,...,length(t) − 1} (an unrealistic assumption, according to the book) and uses the concept of a "run" (a sequence of non-`nil` entries) `[from source] (ODS p.124)`.
- **Lemma 5.4**: the probability that a run of size k starts at i is O(c^k) for some constant 0 < c < 1 (the proof uses the invariant `length(t) ≥ 2q` and arrives at (√e/2)^k) `[from source] (ODS p.124-125)`.
- Conclusion: ignoring `resize()`, add/remove/find in expected O(1); **Theorem 5.2** `[from source] (ODS p.126-127)`.
- `[inference]` The expected O(1) bound holds under the independence hypothesis above; with a merely "good" hash function (such as the multiplicative one) the book does not prove this result for linear probing. The book resolves it with **tabulation hashing**, saying that the bound of Theorem 5.2 continues to hold, with references at the end of the chapter `[from source] (ODS p.127-128, 135)`.
- `[extrapolation]` What the book does not prove: that without the invariant `length(t) ≥ 2q` performance degrades. Exercise 5.5 asks to show that a simplified version of `add` can take time on the order of n² `[from source] (ODS p.136-137)`.

## 5. Tabulation hashing and hash codes
- Tabulation hashing: split the hash code into `w/r` pieces of r bits, index `w/r` tables of random integers and combine by exclusive-or; the hash values of pairs of keys are independent, but not those of arbitrary sets of n keys `[from source] (ODS p.127-128)`.
- Hash codes must be equal for equal elements and have a small collision probability (≈ 1/2^w) among different ones `[from source] (ODS p.129)`.
- Small primitive types: the binary representation itself is used; types larger than `w` bits are treated as composite objects `[from source] (ODS p.129)`.
- Composite objects: naive combinations (for example exclusive-or) are easy to defeat; robust method with 2w bits of precision and **Theorem 5.3**: `Pr ≤ 3/2^w` `[from source] (ODS p.129-131)`.
- Variable-size arrays and strings: polynomials over prime fields; **Theorem 5.4** (at most r−1 roots) and **Theorem 5.5/5.6**: `Pr ≤ max{r, r′}/p`; the term `(p−1)zʳ` acts as an end-of-sequence marker `[from source] (ODS p.131-133)`.
- Discussion: hashing with chaining goes back to an IBM memo (H. P. Luhn, January 1953) `[from source] (ODS p.134)` `[DATED]`; perfect hashing, FKS and cuckoo are only mentioned `[from source] (ODS p.134-135)`.
- Exercise 5.11 and the note on denial-of-service attacks: a set of keys can be constructed to collide (algorithmic complexity attack) `[from source] (ODS p.138)`.
