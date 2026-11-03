---
name: recurrence-solver
description: Solves and numerically VERIFIES divide-and-conquer recurrences with the recursion tree method of Erickson's book (T(n)=r T(n/c)+f(n); decreasing, equal and increasing cases), including subproblems of different sizes and the book's recurrences (Hanoi, MergeSort, Karatsuba, MomSelect, backtracking). The book does NOT present the Master Theorem.
allowed-tools: Bash, Read
---

# Recurrence Solver and numerical verifier

Two read-only tools (Python 3, stdlib, no network). Pages `(JE p.N)` = PDF (printed = N − 18).

## 1. `solve_recurrence.py` — classification by the recursion tree `[from source] (JE p.49-52)`
```bash
python -I skills/recurrence-solver/scripts/solve_recurrence.py --a 2 --b 2 --k 1          # MergeSort: equal -> Theta(n log n)
python -I skills/recurrence-solver/scripts/solve_recurrence.py --a 3 --b 2 --k 1          # Karatsuba: increasing -> Theta(n^1.585)
python -I skills/recurrence-solver/scripts/solve_recurrence.py --terms "1/5,1;7/10,1" --k 1   # MomSelect: decreasing -> Theta(n)
python -I skills/recurrence-solver/scripts/solve_recurrence.py --terms "1/3,1;2/3,1" --k 1    # blocks of 3: balanced -> n log n
python -I skills/recurrence-solver/scripts/solve_recurrence.py --examples
```
- `--a`/`--b` are the book's `r` and `c`; `--k` is the exponent of `f(n)=n^k`; `--p` (the `log^p` factor) is `[extrapolation]`.
- Rules: ratio per level `r/c^k`: `<1` decreasing (root), `=1` equal (`f(n) log n`), `>1` increasing (leaves, `n^(log_c r)`) `[from source] (JE p.51)`.
- `--terms "alpha,coef;..."` handles `T(n)=Σ coef·T(alpha·n)+n^k`: sum `ρ=Σ coef·alpha^k` `<1` root (JE p.56), `=1` balanced (JE p.51-52, 57), `>1` is `[extrapolation]` (Akra-Bazzi type).
- **Master Theorem**: not from the book (the index refers to "recursion trees", JE p.454). The script does not use that name.
- The book proves `O(...)` bounds; the printed `Theta` holds when `f(n)` is `Theta` of the given value `[inference]`.

## 2. `check_recurrence.py` — numerical verifier (before stating a closed form)
```bash
python -I skills/recurrence-solver/scripts/check_recurrence.py --list
python -I skills/recurrence-solver/scripts/check_recurrence.py --all                       # 12 recurrences of the book; exit 1 if anything fails
python -I skills/recurrence-solver/scripts/check_recurrence.py --preset hanoi --max 40      # T(n)=2^n-1 exact (JE p.44)
python -I skills/recurrence-solver/scripts/check_recurrence.py --div --r 3 --c 2 --k 1 --max 14 --claim 1.58496
python -I skills/recurrence-solver/scripts/check_recurrence.py --lin --coef 1,1 --f 1 --base 1,1 --max 40
```
- Presets (with page): Hanoi (p.44), `RecFibo` calls = `2F(n+1)−1` (p.117), MergeSort (p.46), QuickSort worst case (p.48), Karatsuba (p.59), naive multiplication (p.58), MomSelect with the `16n` ceiling (p.56-57), blocks of 3 (p.57), Subset Sum and optimal BST by backtracking (p.96, 110-111), text segmentation (p.102-103), Pingala power (p.61).
- It evaluates `T(n)` exactly (integers, memoization) and compares with the closed form or with the ratio `T(n)/g(n)`. **It is not a proof**: it only tests the requested `n` `[inference]`.
