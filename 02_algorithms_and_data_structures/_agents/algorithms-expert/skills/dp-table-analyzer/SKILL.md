---
name: dp-table-analyzer
description: Deterministic worksheet of dynamic programming formulations from Erickson's book (subproblems, dependencies, evaluation order, time and space, with page and [from source]/[inference]/[extrapolation] labels) for Fibonacci, text segmentation, LIS, edit distance, Subset Sum, optimal BST, tree DP, Bellman-Ford and Floyd-Warshall; plus a simple calculation for custom formulations.
tools: Bash, Read
---

# DP Table Analyzer

Read-only tool (Python 3, stdlib, no network) based on the book's procedure `[from source] (JE p.124-125)` — **two stages**: (1) formulate recursively (English specification + recurrence); (2) bottom-up: subproblems, memoization structure, dependencies, evaluation order, space and time, algorithm. Pages = PDF (printed = N − 18).

## Usage
```bash
python -I skills/dp-table-analyzer/scripts/analyze_dp.py --list
python -I skills/dp-table-analyzer/scripts/analyze_dp.py --problem edit_distance
python -I skills/dp-table-analyzer/scripts/analyze_dp.py --problem subset_sum
python -I skills/dp-table-analyzer/scripts/analyze_dp.py --custom --sizes 1000,500 --cost-per-cell "1"
```
Problems: `fibonacci`, `text_segmentation`, `lis_bigger`, `lis_first`, `edit_distance`, `subset_sum`, `optimal_bst`, `tree_independent_set`, `bellman_ford_dp`, `floyd_warshall`, `dag_longest_path`.

## Labels and cautions
- Each field states its origin. The `[extrapolation]` optimizations (LIS in `O(n log n)`, edit distance in `O(min(m,n))`, Subset Sum in `O(T)`, optimal BST in `O(n^2)` by Knuth-Yao) are **not** stated in the book and the script marks them as such.
- `--custom` only applies the book's rule (time = number of subproblems × cost per subproblem, JE p.125); the number of subproblems is the product of the given sizes `[inference]`. It does not validate dependencies: the graph must be acyclic (JE p.252).
- It does not replace the correctness proof of the recurrence.
