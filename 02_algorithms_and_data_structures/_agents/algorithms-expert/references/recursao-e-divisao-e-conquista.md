# Recursion, divide and conquer and recurrences (Ch. 1)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 1 = PDF p.39-62; exercises p.62-88. The book's notation for recurrences: $T(n) = r\,T(n/c) + f(n)$ (here the scripts use `a`, `b` by tradition; map $a=r$, $b=c$).

## 1. Reduction and "Simplify and Delegate"
- `[from source]` Reduction is the act of solving problem $X$ by writing an algorithm that uses an algorithm for $Y$ as a black box; correctness must not depend on how the black box works (JE p.39-40).
- `[from source]` Recursion is a particular reduction: if the instance can be solved directly, solve it; otherwise reduce to simpler instances of the same problem. The book calls whoever solves the smaller instances the *Recursion Fairy* and identifies it with the Induction Hypothesis (JE p.40-41).
- `[from source]` Technical condition: there must be no infinite sequence of reductions; a base case must be reached (JE p.41).
- `[from source]` On tracing the recursion: when analyzing the Tower of Hanoi the book states explicitly that "unrolling" the recursion is neither necessary nor useful for most recursive algorithms; it is enough to reduce the instance and prove by induction (JE p.44). *(The rule "never trace beyond the first level" was a strong paraphrase by the v1 package; the book says this in the tone of advice, p.43-44.)*

## 2. Tower of Hanoi (JE p.42-44)
- `[from source]` Algorithm: move $n-1$ disks to the auxiliary peg, move the largest to the destination, move the $n-1$ back on top; the base case $n=0$ does nothing (JE p.43-44).
- `[from source]` $T(0)=0$, $T(n)=2T(n-1)+1$ and $T(n)=2^n-1$, which is proved by induction; for 64 disks that is $2^{64}-1$ moves (JE p.44).

## 3. MergeSort and QuickSort (JE p.44-49)
- `[from source]` MergeSort: split in half, sort recursively and merge; correctness proof by two inductions (Merge and MergeSort) (JE p.45-46). Recurrence $T(n)=T(\lceil n/2\rceil)+T(\lfloor n/2\rfloor)+O(n)$, simplified to $2T(n/2)+O(n)$ and solved by the "all levels equal" case of the recursion tree: $O(n \log n)$ (JE p.46, 51).
- `[inference]` The book presents an upper bound $O(n\log n)$; saying "$\Theta$ in best, average and worst case" is a deduction (Merge always traverses all elements), not a sentence from the book. The book states that it does not consider the "best case" (JE p.49).
- `[from source]` QuickSort (Hoare, 1959): choose a pivot, partition (here, Lomuto partition) into smaller, pivot and larger, and sort both sides recursively (JE p.47). Worst case with an always-extreme pivot: $T(n) \le T(n-1)+O(n)$, hence $O(n^2)$; the same holds for "median of three" (JE p.48). With the exact median as pivot it would be $O(n\log n)$ (JE p.48).
- `[from source]` Average case: the intuition that the pivot usually lands in the middle suggests $O(n\log n)$, but the usual formalization assumes all permutations are equally likely, which the book considers unrealistic; with a pivot chosen uniformly at random, the time is $O(n\log n)$ with high probability for every input (note 7), an analysis the book leaves out of scope (JE p.49).

## 4. Divide and conquer and recursion trees (JE p.49-53)
- `[from source]` Pattern: split into smaller independent instances of the same problem, delegate to the *Recursion Fairy*, combine (JE p.49).
- `[from source]` Recursion tree of $T(n) = r\,T(n/c)+f(n)$: each node is worth the non-recursive work; level $i$ has $r^i$ nodes of value $f(n/c^i)$; $T(n)=\sum_{i=0}^{L} r^i f(n/c^i)$ with $L=\log_c n$ and number of leaves $n^{\log_c r}$ (JE p.50-51).
- `[from source]` Three cases (JE p.51): **decreasing** (terms fall by a constant factor) $\Rightarrow T(n)=O(f(n))$, dominated by the root; **equal** $\Rightarrow O(f(n)\log n)$; **increasing** $\Rightarrow O(n^{\log_c r})$, dominated by the leaves.
- `[from source]` The technique also works with subproblems of different sizes: $T(n) \le T(n/3)+T(2n/3)+O(n)$ gives $O(n\log n)$ because each level sums to at most $n$ and the depth is $\log_{3/2} n$; the bound is tight (JE p.51-52). For $T(n)=T(n-1)+T(1)+O(n)$ one obtains $O(n^2)$ (JE p.52).
- `[from source]` Ceilings and floors can be ignored: the "domain transformation" shows why, and from then on the book ignores them (JE p.52-53).
- `[from source]` The **Master Theorem is not presented**: the back-of-book index has only "Master Theorem, see recursion trees" (JE p.454). Any "case 1/2/3 of the Master Theorem" is `[extrapolation]`.
- `[extrapolation]` When $f(n)=\Theta(n^k\log^p n)$ the comparison of $k$ vs $\log_c r$ remains valid (ratio $r/c^k$ per level), and in the equal case the sum of the levels becomes $\Theta(n^k \log^{p+1} n)$ for $p>-1$. The book only treats $f(n)$ without a logarithmic factor. The package's solver flags this.

## 5. Linear-time selection (JE p.53-57)
- `[from source]` Problem: the $k$-th smallest of $A[1..n]$. *QuickSelect* (Hoare, 1961): partitions with the same routine as QuickSort and recurses on **one** side; correctness does not depend on the pivot (JE p.53-54).
- `[from source]` Worst case with an always-extreme pivot: $T(n)=T(n-1)+O(n)=O(n^2)$ (JE p.54). With a "good" pivot ($\ell \le \alpha n$, $\alpha<1$) the recurrence $T(n)\le T(\alpha n)+O(n)$ gives $O(n)$ (JE p.54-55).
- `[from source]` *Median of medians* (Blum, Floyd, Pratt, Rivest, Tarjan): $\lceil n/5\rceil$ blocks of 5, the median of each block by brute force, a recursive call on the medians, and the "mom" is used as the pivot (JE p.55). The mom is greater than at least $3n/10$ elements and smaller than at least $3n/10$; the next recursive call has at most $7n/10$ elements (JE p.55-56).
- `[from source]` $T(n)\le T(n/5)+T(7n/10)+O(n)$; the total per level is at most $9/10$ of the previous one, hence $O(n)$ (JE p.56). The constant is large: in the worst case $\le 16n$ comparisons with the fine count $T(n)\le T(n/5)+T(7n/10)+8n/5$ (JE p.57).
- `[from source]` "Why 5?": 5 is the smallest odd block size that gives exponential decay; with blocks of 3 the recurrence is $T(n/3)+T(2n/3)+O(n)$, which gives $O(n\log n)$ (tight): "no faster than sorting" (JE p.57).
- `[from source]` In practice, choose the pivot uniformly at random; the expected number of comparisons for the median is at most $4n$ (JE p.57, note 9). *(The claim "QuickSelect has expected time $O(n)$" appears in v1 with p.54, but the only textual basis is this note 9 on p.57.)*

## 6. Fast multiplication (JE p.58-60)
- `[from source]` The naive split into four subproducts gives $T(n)=4T(\lceil n/2\rceil)+O(n)=O(n^2)$: "that didn't work" (JE p.58).
- `[from source]` Karatsuba (1960, against Kolmogorov's $n^2$ conjecture): uses the identity $ac+bd-(a-b)(c-d)=bc+ad$ for only 3 recursive calls, $T(n)\le 3T(\lceil n/2\rceil)+O(n)$, hence $O(n^{\log_2 3})=O(n^{1.58496})$ (JE p.58-59). The original form with $(a+b)(c+d)$ appears in note 10 (JE p.59); the version with $(a-b)(c-d)$ is Knuth's simplification.
- `[from source]` Historical citations that follow: Toom-Cook with $2k-1$ recursive multiplications, FFT, Schönhage-Strassen $O(n\log n\log\log n)$ and Harvey-van der Hoeven $O(n\log n)$ in 2019 (JE p.60). `[DATED]` for "fastest known".

## 7. Exponentiation (JE p.60-62)
- `[from source]` Naive method: $n-1$ multiplications; Pingala's method by halving: $T(n)\le T(n/2)+2$, hence $O(\log n)$ multiplications (JE p.61). The "peasant" variant (squaring and halving) is also $O(\log n)$ (JE p.61-62).
- `[from source]` Both are asymptotically optimal: any algorithm needs $\Omega(\log n)$ multiplications because each multiplication at most doubles the largest power computed; for $a^{15}$ both methods use 6 multiplications and the optimum is 5; whether the exact minimum is efficiently computable is an open problem (JE p.62).

## 8. Frequent error patterns (all `[inference]`)
- Forgetting the base case (JE p.41, 43) or making the recursive call on an instance that is not strictly smaller (JE p.41).
- Applying a "case of the Master Theorem" without checking the hypotheses: the book uses recursion trees, which also work for subproblems of different sizes (JE p.51-52).
- Claiming $\Theta(n\log n)$ as the worst case of QuickSort with a fixed pivot: the worst case is $\Theta(n^2)$ (the $O(n^2)$ bound is proved in JE p.48; "tight" in JE p.52).

## Outside the book
Master Theorem and Akra-Bazzi, analysis of randomized QuickSort (referred to the author's lecture notes, JE p.49), Strassen in detail (mentioned on p.335), amortized analysis.
