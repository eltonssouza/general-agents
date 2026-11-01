# Interfaces, computation model and analysis (Ch. 1)

Pages = PDF (printed = N − 12). Source: ODS Ch. 1 (p.13-41). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Interface versus implementation
- An interface describes what the structure does (operations and semantics, also called an abstract data type); an implementation describes the internal representation and the algorithms. An interface can have several implementations: the book shows List with arrays (Ch. 2) and with pointers (Ch. 3) `[from source] (ODS p.16)`.

## 2. The book's interfaces
| Interface | Operations | Book notes |
|---|---|---|
| Queue | `add(x)`, `remove()` | The queue discipline decides who leaves: FIFO, priority (the smallest leaves) or LIFO `[from source] (ODS p.17-18)`. |
| Stack | `push(x)`, `pop()` | It is the LIFO queue under other names `[from source] (ODS p.17-18)`. |
| Deque | `add_first`, `remove_first`, `add_last`, `remove_last` | Generalizes FIFO and LIFO `[from source] (ODS p.18)`. |
| List | `size`, `get(i)`, `set(i,x)`, `add(i,x)`, `remove(i)` | Indexed sequence from 0 to n−1; the four Deque operations come from `add(i,x)` and `remove(i)` `[from source] (ODS p.18-19)`. |
| USet | `size`, `add(x)`, `remove(x)`, `find(x)` | Distinct elements, unordered; `find` returns the equal element or `nil`; with key-value pairs it becomes a dictionary `[from source] (ODS p.20)`. |
| SSet | the same | `find(x)` returns the smallest `y ≥ x` (successor search), which costs more; the book recommends USet if order is not needed `[from source] (ODS p.20-21)`. |
- The book says little about Queue, Stack and Deque as interfaces because List subsumes them; classes such as ArrayDeque implement List and all Deque operations in constant time `[from source] (ODS p.18-19)`.
- Names in other texts: `enqueue`/`dequeue` for FIFO and `delete_min` for priority `[from source] (ODS p.17)`.

## 3. Computation model (Word-RAM)
- Memory as cells of `w` bits; arithmetic (+, −, ·, /, mod), comparisons and bitwise boolean operations take constant time; any cell is read or written in constant time `[from source] (ODS p.30-31)`.
- Allocating a block of size k costs O(k) and returns a one-word reference `[from source] (ODS p.31)`.
- The only assumption about `w`: `w ≥ log n`, with n the number of elements `[from source] (ODS p.31)`. Space is measured in words and an element of the generic type occupies one word `[from source] (ODS p.31)`.
- In Ch. 14 the model is replaced by the external memory model (blocks); see `memoria-externa-e-arvores-b.md`.

## 4. Three time guarantees (ODS p.32)
- **Worst case**: no operation takes longer than f(n) `[from source] (ODS p.32)`.
- **Amortized**: a sequence of m operations takes at most m·f(n); some individual operations may exceed f(n) `[from source] (ODS p.32)`.
- **Expected**: the time is a random variable; the expectation is over the structure's random choices, not over the input or the sequence of operations `[from source] (ODS p.29, 32)`.
- The book motivates the last two with financial examples (mortgage versus paying in cash; insurance) and says that, by accepting amortized or expected, one often gets a simpler structure `[from source] (ODS p.32-33)`.

## 5. Where the book uses the potential method
The book does **not** state a general potential method in Ch. 1. It uses potentials in isolated proofs:
- DualArrayDeque: Φ = size difference between `front` and `back` `[from source] (ODS p.61)`.
- SEList: Φ = number of "fragile" nodes (a block without exactly b elements) `[from source] (ODS p.88-89)`.
- 2-4 trees (basis of red-black trees): Φ per node according to 2, 3 or 4 children `[from source] (ODS p.209)`.
- The ArrayStack proof (Lemma 2.1) counts operations between resizes, without a potential `[from source] (ODS p.47-48)`.
- The general formula aᵢ = cᵢ + Φ(Sᵢ) − Φ(Sᵢ₋₁), with a telescoping sum, is standard knowledge `[extrapolation]`.

## 6. Supporting math (Ch. 1)
- `log` without a base is log₂; ln k ≈ 0.693·log k `[from source] (ODS p.22-23)`.
- Stirling's approximation for n! `[from source] (ODS p.23)`; O notation and the inclusions O(1) ⊂ O(log n) ⊂ O(n^b) `[from source] (ODS p.24-25)`; "T(n) = 2 log n + O(1)" is an accepted abuse of notation `[from source] (ODS p.25)`.
- Expected value, linearity of expectation and indicator variables `[from source] (ODS p.27-30)`.

## 7. The book's summary tables (A = amortized, E = expected)
- Table 1.1 (List and USet) `[from source] (ODS p.36)`: ArrayStack get/set O(1) and add/remove O(1+n−i)ᴬ; ArrayDeque and DualArrayDeque O(1+min{i,n−i})ᴬ; RootishArrayStack O(1+n−i)ᴬ; DLList O(1+min{i,n−i}); SEList get/set O(1+min{i,n−i}/b) and add/remove O(b+min{i,n−i}/b)ᴬ; SkiplistList O(log n)ᴱ; ChainedHashTable and LinearHashTable find O(1)ᴱ and add/remove O(1)ᴬ,ᴱ.
- Table 1.2 (SSet and priority queues) `[from source] (ODS p.38)`: SkiplistSSet and Treap O(log n)ᴱ; ScapegoatTree find O(log n) and add/remove O(log n)ᴬ; RedBlackTree O(log n); BinaryTrie O(w); XFastTrie find O(log w)ᴬ,ᴱ and add/remove O(w)ᴬ,ᴱ; YFastTrie O(log w)ᴬ,ᴱ; BinaryHeap find_min O(1) and add/remove O(log n)ᴬ; MeldableHeap find_min O(1) and add/remove O(log n)ᴱ. The integer structures store only `w`-bit integers.
- `scripts/ods_cost_lookup.py` looks up these entries (and those of the theorems in the other chapters) with the page.

## 8. Boundaries
- The book contains no real-time analysis, CPU cache behavior (beyond isolated mentions), concurrency, or systematic empirical comparisons (only observations such as the relative slowness of the Scapegoat tree, ODS p.185). All of this is `[extrapolation]`.
- Numbers in Ch. 1 about web pages, queries per second and processor speeds are illustrations `[DATED]` `[from source] (ODS p.14-15)`.
