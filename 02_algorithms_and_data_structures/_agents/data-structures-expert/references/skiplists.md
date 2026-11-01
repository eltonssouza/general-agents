# Skiplists (Ch. 4)

Pages = PDF (printed = N − 12). Source: ODS Ch. 4 (p.95-111). `log` is log₂ (ODS p.22).

## 1. Structure
- A skiplist is a sequence of singly linked lists L₀,...,L_h; each Lᵣ contains a subset of Lᵣ₋₁, obtained by flipping a coin per element (heads = enters Lᵣ); it ends when an empty list appears `[from source] (ODS p.95)`.
- The height of an element is the largest r such that it is in Lᵣ; it is equivalent to flipping a coin until tails and counting the heads; the expected height of a node is 1 `[from source] (ODS p.96)`. The height of the skiplist is that of the tallest node `[from source] (ODS p.96)`.
- Each list starts with a `sentinel` node; the search path goes from the sentinel of L_h to each node of L₀: it moves right while it does not overshoot the target, otherwise it goes down `[from source] (ODS p.96)`.
- Compact implementation: a node with value `x` and an array `next`, where `u.next[i]` points to the successor in Lᵢ `[from source] (ODS p.96-97)`.
- Promotion probability: the book's version uses a fair coin; Exercise 4.7 generalizes to probability p `[from source] (ODS p.110)`.
- Origin: skiplists were introduced by Pugh `[from source] (ODS p.109)`; the paper is from 1990 according to the bibliography `[from source] (ODS p.319)`.

## 2. SkiplistSSet
- `find(x)`: starts at the sentinel in L_h, moves while `u.next[r].x < x`, goes down to L₀ and returns `u.next[0].x` (the smallest y ≥ x) `[from source] (ODS p.97-98)`.
- `pick_height()`: counts the trailing ones of a random 32-bit integer (limits the height to 32, negligible unless n is much larger than 2³²) `[from source] (ODS p.98)`.
- `add(x)`: searches while storing in `stack[r]` the node where the path goes down from Lᵣ; inserts the new node in L₀,...,L_k, with k = the drawn height; increases `h` if needed `[from source] (ODS p.98-99)`.
- `remove(x)`: needs no `stack`; during the search, each time the path goes down from `u`, if `u.next.x = x`, it removes the node `[from source] (ODS p.99-100)`.
- **Theorem 4.1**: add/remove/find in expected O(log n) `[from source] (ODS p.100)`.

## 3. SkiplistList
- Implements List with L₀ in the order of the list. The **length** of an edge in L₀ is 1; in Lᵣ it is the sum of the lengths below it (equal to the number of L₀ edges under it); stored in `u.length[r]` `[from source] (ODS p.101-102)`.
- To reach position i: tracks the position j of the current node in L₀ and goes right if `j + u.length[r] < i`, otherwise goes down `[from source] (ODS p.101-102)`.
- `add(i,x)`: draws the height, follows the search path incrementing by 1 the lengths of the edges that go down and does the splice at the levels up to the new node's height, computing the new lengths in constant time; `remove(i)` decrements the lengths and removes the node `[from source] (ODS p.102-105)`.
- **Theorem 4.2**: get/set/add/remove in expected O(log n) `[from source] (ODS p.105)`.
- Note: "finger" in the book is something else: the search-path array used in searches starting from a nearby position (Exercise 4.10); the `stack` array of `add` is an example `[from source] (ODS p.110)`.

## 4. Analysis
- **Lemma 4.2**: the expected number of fair coin flips until the first heads is 2 `[from source] (ODS p.105-106)`.
- **Lemma 4.3**: the expected number of nodes (without the sentinel) is 2n, since the expected number in Lᵣ is n/2ʳ `[from source] (ODS p.106)`. **Lemma 4.4**: expected height ≤ log n + 2 `[from source] (ODS p.106-107)`. **Lemma 4.5**: nodes including sentinels: 2n + O(log n) `[from source] (ODS p.107)`.
- **Lemma 4.1/4.6**: the expected length of the search path is at most `2 log n + O(1)`; the proof looks at the **reverse path**: at each step it either goes up (heads) or goes left (tails), and the expected number of left steps per level is bounded by 1 (Lemma 4.2) `[from source] (ODS p.96, 107-108)`.
- **Theorem 4.3**: expected size O(n) and expected search path ≤ 2 log n + O(1) `[from source] (ODS p.109)`.
- `[inference]` The result holds for log₂; writing "2 ln n" would be wrong (2 ln n is the expected path of the Treap, see `arvores-balanceadas-e-treaps.md`). In practice, the constant is larger than that of the Treap (1.386 log n) `[from source] (ODS p.170-172)`.

## 5. Cited comparisons and extensions
- A skiplist and a BST use about two pointers per node; Exercise 4.15 asks to explain why the skiplist uses these pointers better `[from source] (ODS p.112)`.
- Deterministic, biased and self-adjusting versions, and use in open-source database systems and in the HP-UX kernel are cited in the discussion `[from source] (ODS p.109)`. `[DATED]` (text from 2011-2012).
- The book does not compare skiplists with AVL or red-black trees in the chapter; any such comparison is `[extrapolation]`. The only comparison with the Treap is on p.170-172.
