# Dynamic programming, "smart recursion" (Ch. 3 + 6.4)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 3 = PDF p.115-140 (exercises p.141-176). The DP ↔ DAG relationship is in Ch. 5 (p.211) and in Ch. 6 (p.252-255).

## 1. What DP is according to the book
- `[from source]` "In a nutshell, dynamic programming is recursion without repetition": the solutions to intermediate subproblems are stored, usually (but not always) in an array or table (JE p.123).
- `[from source]` The focus should be on the **correct recurrence**, not on the table: "DP is not about filling in tables, it's about smart recursion"; if the recurrence is wrong, the algorithm fails (JE p.124).
- `[from source]` The name comes from Bellman (1950s, RAND); "programming" in the sense of planning/tabulation, not code (JE p.119-120).

## 2. Fibonacci / *Mātrāvṛtta* as a guiding example (JE p.115-123)
- `[from source]` The number $M(n)$ of meters with $n$ beats obeys $M(n)=M(n-1)+M(n-2)$ (Virahāṅka, 7th century), $M(n)=F_{n+1}$ (JE p.115-116).
- `[from source]` Naive recursion `RecFibo`: number of calls $T(n)=2F_{n+1}-1$; $F_n=\Theta(\varphi^n)$ with $\varphi\approx1.618$; exponential time (JE p.117). Each $F_{n-k}$ is recomputed $F_{k-1}$ times (JE p.117).
- `[from source]` Memoization (Michie 1967; earlier Samuel 1959) fills the array bottom-up and does $O(n)$ additions (JE p.118). Replacing the recursion with a loop (`IterFibo`) is "the first explicit DP algorithm": $O(n)$ additions and $O(n)$ integers (JE p.119). Keeping only the two most recent values greatly reduces space (`IterFibo2`) (JE p.120-121); `[inference]`: the space becomes constant.
- `[from source]` With the matrix $\begin{pmatrix}0&1\\1&1\end{pmatrix}$ and repeated squaring, $F_n$ is obtained in $O(\log n)$ arithmetic operations (JE p.121). *(The v1 package used the matrix $\begin{pmatrix}1&1\\1&0\end{pmatrix}$; the identity is true, but the book's matrix is the first one. Label the other as `[inference]`.)*
- `[from source]` Caveat: $F_n$ has about $2n/3$ bits; it cannot be computed in logarithmic time, and the correct accounting replaces $O(1)$ with the multiplication cost $M(n)$: `FastRecFibo` costs $O(M(n))$ and the iterative ones cost $O(n^2)$ (JE p.122-123).

## 3. Memoization vs tabulation
- `[from source]` Memoize: store the results of recursive calls and look them up later (JE p.117-118). Tabulate ("fill deliberately"): replace the recursion with a loop that fills the structure in the order in which the recursion would fill it (JE p.119).
- `[from source]` Memoization is depth-first search on the dependency graph; DP is traversing the subproblems in postorder (JE p.252-253).
- `[from source]` But "DP doesn't always help": if the Subset Sum target $T$ is much larger than $2^n$, the iterative algorithm is slower than the naive recursive one (JE p.135).

## 4. The book's playbook (Section 3.4, JE p.124-125)
The book describes **two stages**, not "five steps":
1. **Formulate recursively.** (a) *Specification*: describe in precise English which problem is being solved (without it, it is impossible to know whether it is correct); (b) *Solution*: a recursive formula or algorithm in terms of smaller instances of the same problem (JE p.124).
2. **Build bottom-up**, in mechanical steps: (a) identify the subproblems; (b) choose the memoization structure (generally a multidimensional array); (c) identify dependencies; (d) find an evaluation order (a *linear extension* of the partial order of dependencies); (e) analyze space and time (number of subproblems = space; time = sum of the times per subproblem, assuming the deeper ones are already memoized); (f) write the algorithm (JE p.124-125).
- `[from source]` The dependency graph of a recurrence has one vertex per subproblem and is acyclic (JE p.211, 252). If it were cyclic, the naive recursion would never stop (JE p.252).
- `[from source]` When the structure is regular (grid, triangle), the evaluation order is fixed by nested loops and there is no need to sort topologically at run time (JE p.253).
- `[from source]` Exercises: in the author's classes, a DP solution without the English specification of the subproblems receives a zero (JE p.141, note 18).

## 5. "Greed is Stupid" (3.5, JE p.125-126)
- `[from source]` A greedy algorithm is always a series of decisions made directly, without recursive subproblems; it "almost never works", and problems truly solved by a greedy algorithm are rare (JE p.125). Greedy intuitions for text segmentation (shortest/longest prefix that is a word) and LIS (start with the smallest element) "aren't even close" (JE p.125-126).
- `[from source]` The author's policy: no credit for a greedy algorithm, even a correct one, without a **formal proof** of correctness; and "whenever you write or think the word *greedy*, your subconscious is asking for DP". The techniques for proving greedy algorithms come in Ch. 4 (JE p.126).
- `[from source]` **The coin-change example with coins $\{1,4,5,6\}$ for 8 is NOT in the book** (v1 cited it at p.125-127). The book has Nadiria's notes exercise ($1, 4, 7, 13, 28, 52, 91, 365$), asking for a case in which the greedy algorithm fails (JE p.141). If you use $\{1,4,5,6\}$ with change for 8 (greedy: 6+1+1; optimal: 4+4), label it `[extrapolation]`.

## 6. LIS (3.6, JE p.127-129)
- `[from source]` The recurrence $LISbigger(i,j)$ has $O(n^2)$ subproblems, each $O(1)$; it is filled by columns from right to left; time $O(n^2)$ and, keeping only two columns, space $O(n)$ (JE p.127-128).
- `[from source]` The recurrence $LISfirst(i)$: a one-dimensional array filled in decreasing index order; time $O(n^2)$, space $O(n)$ (JE p.128-129).
- `[extrapolation]` The $O(n\log n)$ algorithm by binary search (*patience sorting*) is **not** covered in the book (the term *patience sorting* does not occur in it).

## 7. Edit distance (3.7, JE p.129-134)
- `[from source]` Definition, names (Levenshtein 1965, Vintsyuk 1968, Ulam 1972) and the FOOD → MONEY example (JE p.129). Optimal-substructure property of the alignment: removing the last column leaves the optimal alignment of the remaining prefixes (JE p.130).
- `[from source]` Recurrence: $Edit(i,j)=i$ if $j=0$; $=j$ if $i=0$; otherwise $\min\{Edit(i,j-1)+1,\ Edit(i-1,j)+1,\ Edit(i-1,j-1)+[A[i]\ne B[j]]\}$ (insertion, deletion, substitution) (JE p.130-131).
- `[from source]` Array $Edit[0..m,0..n]$, row-by-row order, time $O(mn)$ and space $O(mn)$ (JE p.131-132). An optimal edit sequence is recovered in $O(n+m)$ additional time by reading the values (JE p.134). Attribution of names (Wagner-Fischer) in a note (JE p.132-133).
- `[extrapolation]` Reducing the space to $O(\min(m,n))$ by keeping two rows is customary knowledge, but **the book does not state it** for edit distance (only for LIS, p.128, and Fibonacci, p.120-121). The v1 package cited p.130-134; downgraded.

## 8. Subset Sum (3.8, JE p.134-135)
- `[from source]` $SS(i,t)$ for the suffix $X[i..n]$: True if $t=0$; False if $i>n$; $SS(i+1,t)$ if $t<X[i]$; otherwise $SS(i+1,t)\lor SS(i+1,t-X[i])$ (JE p.134). Array $S[1..n+1,0..T]$, filled bottom-up; **space and time $O(nT)$** (JE p.135).
- `[from source]` Note 16: the problem is NP-hard and the $O(nT)$ time does not imply P=NP because $T$ is not polynomially bounded (JE p.135). The terms *pseudo-polynomial time* and *weakly NP-hard* appear in Ch. 12 (JE p.422).
- `[extrapolation]` The version with a one-dimensional vector swept from back to front and $O(T)$ space is not in the book.

## 9. Optimal binary search trees (3.9, JE p.135-138)
- `[from source]` With $F(i,k)=\sum_{j=i}^k f[j]$ precomputed in $O(n^2)$ (`InitF`), $OptCost(i,k)=F[i,k]+\min_{i\le r\le k}\{OptCost(i,r-1)+OptCost(r+1,k)\}$ (JE p.136). There are at least three valid evaluation orders (diagonals, row by row from bottom to top, column by column) (JE p.137-138).
- `[from source]` Space $O(n^2)$ and time $O(n^3)$: two parameters ⇒ $O(n^2)$ subproblems, three variables ($i,k,r$) ⇒ $O(n^3)$ (JE p.138).
- `[extrapolation]` The reduction to $O(n^2)$ via Knuth-Yao monotonicity is **not** covered in the book (Knuth appears in the book only in other contexts, p.59 and p.190).

## 10. DP on trees (3.10, JE p.138-140)
- `[from source]` Largest independent set of a tree with $n$ vertices in $O(n)$ (the general problem is NP-hard, Ch. 12) (JE p.138-139). $MIS(v)=\max\{\sum_{w\downarrow v} MIS(w),\ 1+\sum_{w\downarrow v}\sum_{x\downarrow w} MIS(x)\}$, memoized in the node itself, evaluated in postorder (JE p.139). Each vertex contributes constant time to its parent and grandparent, hence $O(n)$ (JE p.139-140).
- `[from source]` Version with two functions, $MISyes(v)=1+\sum MISno(w)$ and $MISno(v)=\sum\max\{MISyes(w),MISno(w)\}$ (JE p.140). *(v1 called them $MIS(u,in/out)$.)*
- `[from source]` "Tree-shaped" problems (optimal BST, independent set on trees) do **not** reduce to an optimal path in a DAG (JE p.255).

## 11. DP as a path in a DAG (6.4, JE p.253-255)
- `[from source]` Longest path in a DAG in $O(V+E)$ with the recurrence $LLP(v)$; in general graphs the problem is NP-hard (JE p.253-254). Segmentation, Subset Sum, LIS and edit distance can be seen as longest/shortest paths in the dependency DAG (JE p.255).

## Outside the book
Knapsack in general, bitmask DP, Knuth's optimization, divide-and-conquer optimization, classic LCS (appears only as an exercise), Hirschberg.
