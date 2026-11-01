# Backtracking (Ch. 2)

Source: **JE** (*Algorithms*, Erickson, 2019). Pages = **PDF** (printed = PDF − 18). Ch. 2 = PDF p.89-111 (exercises p.111-114). Ch. 2 is the "parent" of the dynamic programming algorithms of Ch. 3: the same recurrences, only evaluated without memory.

## 1. The general idea (JE p.89, 97-98)
- `[from source]` A *backtracking* algorithm builds the solution incrementally, one piece at a time; when it must decide among alternatives, it recursively evaluates **all** of them and picks the best (JE p.89).
- `[from source]` General pattern (2.4): make a sequence of decisions to build a recursively defined structure; **each recursive call makes exactly one decision**, consistent with the previous ones, and receives what remains of the input plus a minimal summary of the decisions already made (JE p.97). The summary changes from problem to problem: in $n$ Queens it is all the previous positions; in the game, only the current state; in Subset Sum, only the remaining target (JE p.97-98).
- `[from source]` Recipe: figure out in advance what information from the past is needed (the recursive problem may be more general than the original) and then "try everything", without being clever ("First make it work; then make it fast") (JE p.98, 102).
- `[from source]` Most backtracking algorithms have exponential worst-case time; the exact analysis usually does not matter because they are intermediate steps toward faster algorithms (JE p.102).
- `[from source]` Variants: almost always the same strategy solves the count, construct or optimize versions; design for the simplest variant (a number or a boolean) (JE p.96).

## 2. $n$ Queens (JE p.89-91)
- `[from source]` Place $n$ queens on an $n\times n$ board so that no two attack each other (same row, column or diagonal) (JE p.89-90). The algorithm of Gauss and Laquière places one queen **per row**, from top to bottom; for each column $j$ of row $r$ it tests whether it is attacked by earlier queens; if not, it places the queen provisionally and recurses (JE p.90-91). The vector $Q[1..n]$ stores the column of each row.
- `[from source]` The execution forms a recursion tree whose nodes are partial solutions; the search is equivalent to a DFS of that tree (JE p.91).
- `[inference]` Counting the "$n^n$ placements" that pruning avoids is not in the book; what the book says is that attacked squares are ignored before recursing (JE p.90).

## 3. Game trees (JE p.92-94)
- `[from source]` For any finite two-player game with no randomness or hidden information, there is a backtracking algorithm that plays perfectly (JE p.93). State = position of the pieces + player to move; **game tree**: an edge from $x$ to $y$ if the current player can move from $x$ to $y$ (JE p.93).
- `[from source]` States are defined as *good* or *bad*: good if the current player has already won or can move to a bad state of the opponent; bad if already lost or all moves lead to good states. Equivalent: an internal node is good if it has at least one bad child and bad if all its children are good (Zermelo's definition, 1913) (JE p.93). The `PlayAnyGame` algorithm is a DFS of this tree (JE p.94).
- `[from source]` In practice only part of the tree is traversed: heuristics prune "obviously" good or bad states and/or cut the tree at a certain depth (*ply*), evaluating the leaves heuristically (JE p.94).
- `[extrapolation]` **Minimax with numeric values, a "Max/Min" player and alpha-beta pruning do not appear in the book** (the term *minimax* does not occur). The v1 package described Max/Min nodes with scores as if they were from the book; that was removed. It is the usual generalization of the good/bad definition.

## 4. Subset Sum (JE p.94-96)
- `[from source]` Input: a set $X$ of positive integers and a target $T$; is there a subset that sums to $T$? Trivial cases: $T=0$ ⇒ True (the empty set sums to 0); $T<0$, or $T\ne 0$ with $X$ empty ⇒ False (JE p.94). General case: for an element $x$, there is a subset summing to $T$ iff there is one that includes $x$ (and sums to $T-x$ on the rest) or one that excludes it (sums to $T$ on the rest) (JE p.94-95).
- `[from source]` In indices: $SS(X, i, T)$ with `with` $=SS(X,i-1,T-X[i])$ and `wout` $=SS(X,i-1,T)$; returns `with` $\lor$ `wout` (JE p.96).
- `[from source]` Time $T(n)\le 2T(n-1)+O(1)$, hence $O(2^n)$; in the worst case (for example $T$ larger than the sum of $X$) the tree is a complete binary tree of depth $n$ (JE p.96). Variants: construct the subset, count subsets, choose the best (JE p.96-97).

## 5. Text segmentation, *Interpunctio Verborum* (JE p.98-104)
- `[from source]` Given a string without spaces and a subroutine `IsWord`, can it be split into words? One decides where the first word ends and recurses on the suffix; the empty string has a unique segmentation into zero words (base case True) (JE p.100-101).
- `[from source]` Index form: $Splittable(i)$ is True if $i>n$; otherwise $\bigvee_{j=i}^{n}(IsWord(i,j)\land Splittable(j+1))$; passing indices instead of subarrays is an important habit for DP too (JE p.101-102).
- `[from source]` Analysis in number of calls to `IsWord`: $T(n)\le\sum_{i=0}^{n-1}T(i)+O(n)$, which becomes $T(n)=2T(n-1)+\alpha$, hence $O(2^n)$; this is tight because there are $2^{n-1}$ possible segmentations (JE p.102-103).
- `[from source]` Variant with a `Score` for each piece: replace $\lor,\land$ by $\max,+$ (JE p.103-104).

## 6. Longest increasing subsequence, LIS (JE p.104-108)
- `[from source]` Subsequence (non-contiguous elements, order preserved) vs substring (contiguous) (JE p.104).
- `[from source]` First strategy: decide, for each $A[j]$, whether to include it or not; it is enough to remember the **last number chosen**. The book defines $LISbigger(i,j)$ = length of the longest increasing subsequence of $A[j..n]$ with all elements greater than $A[i]$; it is $0$ if $j>n$; $LISbigger(i,j+1)$ if $A[i]\ge A[j]$; and $\max\{LISbigger(i,j+1),\ 1+LISbigger(j,j+1)\}$ otherwise; a sentinel $A[0]=-\infty$ is used (JE p.105-107). Time $O(2^n)$ (JE p.107).
- `[from source]` Second strategy: decide *where the next element* of the output is. $LISfirst(i)$ = longest increasing subsequence of $A[i..n]$ that **starts** at $A[i]$: $LISfirst(i)=1+\max\{LISfirst(j)\mid j>i,\ A[j]>A[i]\}$ with $\max\emptyset=0$ (JE p.107-108).
- `[inference]` The $LIS(i,j)$ form of the v1 package (with $i+1$) is equivalent to $LISbigger$, but the notation is the package's, not the book's.

## 7. Optimal binary search trees (JE p.109-111)
- `[from source]` Given sorted keys $A[1..n]$ and frequencies $f[1..n]$, build the search tree that minimizes the total cost $\sum f[i]\cdot(\text{number of ancestors of } v_i)$ (JE p.109). If $v_r$ is the root, the left and right subtrees are optimal for their intervals; $OptCost(i,k)=0$ if $i>k$, otherwise $\sum_{j=i}^k f[j]+\min_{i\le r\le k}\{OptCost(i,r-1)+OptCost(r+1,k)\}$ (JE p.110).
- `[from source]` The backtracking algorithm has time $T(n)=3T(n-1)+\alpha$, hence $O(3^n)$ — it does not enumerate all trees, whose number is $\Theta(4^n/\sqrt n)$ (JE p.111). Here the book combines backtracking with divide and conquer (JE p.109).

## 8. Bridge to DP
- `[from source]` The recurrences in this part are the same ones that Ch. 3 memoizes: Splittable (JE p.123), LIS (JE p.127-129), Subset Sum (JE p.134), Optimal BST (JE p.135-138); the exponential cost comes from solving the same subproblem many times (JE p.123). See `programacao-dinamica.md`.

## Outside the book
Pruning by bounds (*branch and bound*), alpha-beta, branch-ordering heuristics, DPLL SAT solvers, and analysis of $n$ Queens beyond counting solutions (the book cites 92 solutions for $n=8$, JE p.90).
