# -*- coding: utf-8 -*-
"""
analyze_dp.py - worksheet for analyzing dynamic programming formulations from Erickson's book ("Algorithms", 2019).

Follows the book's procedure (JE p.124-125): subproblems, memoization structure, dependencies, evaluation order,
space and time. Each problem carries its page (PDF; printed = PDF - 18) and labels [from source]/[inference]/[extrapolation].
--custom mode: only applies the book's rule "time = sum of the times per subproblem" (JE p.125), with the number of
subproblems computed from the given sizes [inference]. No network; read-only.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROBLEMS = {
    "fibonacci": {
        "nome": "Fibonacci / Matravritta (Ch. 3.1)",
        "subproblemas": "F[0..n]: n+1 values [from source] (JE p.119)",
        "dependencias": "F[i] depends on F[i-1] and F[i-2] [from source] (JE p.116-117)",
        "ordem": "increasing in i (bottom-up) [from source] (JE p.118-119)",
        "tempo": "O(n) additions [from source] (JE p.119); with arbitrary-precision arithmetic O(n^2) [from source] (JE p.122)",
        "espaco": "O(n) integers [from source] (JE p.119)",
        "otimizado": "O(1) keeping only the last two values [from source] (JE p.120-121); O(log n) arithmetic operations by matrix power [from source] (JE p.121); real cost O(M(n)) [from source] (JE p.122)",
        "paginas": "JE p.115-123",
    },
    "text_segmentation": {
        "nome": "Text segmentation / Interpunctio Verborum (Ch. 3.3)",
        "subproblemas": "SplitTable[1..n+1] (one per suffix) [from source] (JE p.123)",
        "dependencias": "Splittable(i) depends on Splittable(j), j > i [from source] (JE p.123)",
        "ordem": "decreasing in i [from source] (JE p.123-124)",
        "tempo": "O(n^2) calls to IsWord (cost of IsWord not included) [from source] (JE p.123)",
        "espaco": "O(n) [inference] (table size)",
        "otimizado": "-",
        "paginas": "JE p.123-124",
    },
    "lis_bigger": {
        "nome": "LIS, 1st recurrence LISbigger(i,j) (Ch. 3.6)",
        "subproblemas": "LISbigger[0..n,1..n]: O(n^2) [from source] (JE p.127)",
        "dependencias": "LISbigger[i,j] depends on LISbigger[i,j+1] and LISbigger[j,j+1] [from source] (JE p.127)",
        "ordem": "columns from right to left; within a column the order does not matter [from source] (JE p.127-128)",
        "tempo": "O(n^2) [from source] (JE p.128)",
        "espaco": "O(n^2); O(n) keeping only two columns [from source] (JE p.127-128)",
        "otimizado": "O(n log n) by binary search: [extrapolation] (the book does not cover it)",
        "paginas": "JE p.127-128",
    },
    "lis_first": {
        "nome": "LIS, 2nd recurrence LISfirst(i) (Ch. 3.6)",
        "subproblemas": "LISfirst[1..n] (plus sentinel A[0]) [from source] (JE p.128-129)",
        "dependencias": "LISfirst[i] depends on LISfirst[j], j > i and A[j] > A[i] [from source] (JE p.128-129)",
        "ordem": "decreasing index [from source] (JE p.129)",
        "tempo": "O(n^2) [from source] (JE p.129)",
        "espaco": "O(n) [from source] (JE p.129)",
        "otimizado": "O(n log n) by binary search: [extrapolation] (the book does not cover it)",
        "paginas": "JE p.128-129",
    },
    "edit_distance": {
        "nome": "Edit distance (Ch. 3.7)",
        "subproblemas": "Edit[0..m,0..n]: (m+1)(n+1) [from source] (JE p.131-132)",
        "dependencias": "Edit[i,j] depends on Edit[i-1,j], Edit[i,j-1], Edit[i-1,j-1] [from source] (JE p.132)",
        "ordem": "row by row (other orders work) [from source] (JE p.132)",
        "tempo": "O(mn) [from source] (JE p.132)",
        "espaco": "O(mn) [from source] (JE p.132); reconstructing the sequence of edits costs O(n+m) more [from source] (JE p.134)",
        "otimizado": "O(min(m,n)) keeping two rows: [extrapolation] (the book does not state this for edit distance)",
        "paginas": "JE p.129-134",
    },
    "subset_sum": {
        "nome": "Subset Sum (Ch. 3.8)",
        "subproblemas": "S[1..n+1,0..T] [from source] (JE p.135)",
        "dependencias": "S[i,t] depends on S[i+1,t] and S[i+1,t-X[i]] [from source] (JE p.134-135)",
        "ordem": "rows from bottom to top; any order within a row [from source] (JE p.135)",
        "tempo": "O(nT) [from source] (JE p.135); pseudopolynomial time, not polynomial in the number of bits [from source] (JE p.422)",
        "espaco": "O(nT) [from source] (JE p.135)",
        "otimizado": "O(T) with a 1D vector scanned backwards: [extrapolation] (the book does not state it)",
        "paginas": "JE p.134-135, 422",
    },
    "optimal_bst": {
        "nome": "Optimal binary search tree (Ch. 3.9)",
        "subproblemas": "OptCost[1..n+1,0..n]: O(n^2) [from source] (JE p.137-138)",
        "dependencias": "OptCost[i,k] depends on OptCost[i,r-1] and OptCost[r+1,k], i<=r<=k [from source] (JE p.137)",
        "ordem": "diagonals, or rows from bottom to top, or columns from left to right [from source] (JE p.137-138)",
        "tempo": "O(n^3) (3 variables i,k,r) [from source] (JE p.138); F[i,k] precomputed in O(n^2) [from source] (JE p.136)",
        "espaco": "O(n^2) [from source] (JE p.138)",
        "otimizado": "O(n^2) by Knuth-Yao: [extrapolation] (the book does not cover it)",
        "paginas": "JE p.135-138",
    },
    "tree_independent_set": {
        "nome": "Maximum independent set in a tree (Ch. 3.10)",
        "subproblemas": "one per vertex (MIS(v), or MISyes/MISno) [from source] (JE p.139-140)",
        "dependencias": "MIS(v) depends on the children and grandchildren of v [from source] (JE p.139)",
        "ordem": "postorder [from source] (JE p.139)",
        "tempo": "O(n) (each vertex contributes constant time to its parent and grandparent) [from source] (JE p.139-140)",
        "espaco": "O(n) [inference] (one field per vertex)",
        "otimizado": "-",
        "paginas": "JE p.138-140",
    },
    "bellman_ford_dp": {
        "nome": "Bellman-Ford as DP (Ch. 8.7)",
        "subproblemas": "dist[i,v], i = maximum number of edges [from source] (JE p.312-313)",
        "dependencias": "dist[i,v] depends on dist[i-1,v] and dist[i-1,u] + w(uv) [from source] (JE p.312-313)",
        "ordem": "i increasing from 1 to V-1 [from source] (JE p.313)",
        "tempo": "O(VE) [from source] (JE p.313)",
        "espaco": "O(V^2) in the original table; the book's version keeps only dist(v) [from source] (JE p.313)",
        "otimizado": "-",
        "paginas": "JE p.312-313",
    },
    "floyd_warshall": {
        "nome": "Floyd-Warshall (Ch. 9.8)",
        "subproblemas": "dist(u,v,r), r = intermediate vertices <= r [from source] (JE p.336-337)",
        "dependencias": "dist(u,v,r) depends on dist(u,v,r-1), dist(u,r,r-1), dist(r,v,r-1) [from source] (JE p.337)",
        "ordem": "r in the outer loop, then u and v [from source] (JE p.337-338)",
        "tempo": "O(V^3) [from source] (JE p.337)",
        "espaco": "O(V^2) by removing the 3rd dimension [from source] (JE p.337)",
        "otimizado": "-",
        "paginas": "JE p.336-338",
    },
    "dag_longest_path": {
        "nome": "Longest path in a DAG (Ch. 6.4)",
        "subproblemas": "LLP(v), one per vertex [from source] (JE p.254)",
        "dependencias": "LLP(v) depends on LLP(w) for each edge vw [from source] (JE p.254)",
        "ordem": "DFS postorder [from source] (JE p.254-255)",
        "tempo": "O(V+E) [from source] (JE p.254)",
        "espaco": "O(V) [inference]",
        "otimizado": "-",
        "paginas": "JE p.253-255",
    },
}

ROTEIRO = ("Book procedure (JE p.124-125): (a) subproblems, (b) memoization structure, (c) dependencies, "
           "(d) evaluation order (linear extension of the partial order), (e) space and time, (f) write the algorithm; "
           "before that, specify the subproblem in English and give the recurrence.")


def show(name, d):
    print("=== DYNAMIC PROGRAMMING WORKSHEET (pages = PDF; printed = PDF - 18) ===")
    print("Problem:         %s" % d["nome"])
    for key, lab in (("subproblemas", "Subproblems"), ("dependencias", "Dependencies"), ("ordem", "Evaluation order"),
                     ("tempo", "Time"), ("espaco", "Space"), ("otimizado", "Optimizations")):
        print("%-16s %s" % (lab + ":", d[key]))
    print("Pages:           %s" % d["paginas"])
    print(ROTEIRO)


def main():
    ap = argparse.ArgumentParser(description="DP analysis worksheet (problems from Erickson's book).")
    ap.add_argument("--problem", choices=sorted(PROBLEMS))
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--custom", action="store_true", help="applies the book's rule: time = number of subproblems x cost per subproblem")
    ap.add_argument("--sizes", default="100,100", help="size of each table dimension, e.g. 1000,500 or 50,50,50")
    ap.add_argument("--cost-per-cell", default="1", help="cost per cell excluding recursion, e.g.: 1, log n, n")
    a = ap.parse_args()
    if a.list:
        for k, v in sorted(PROBLEMS.items()):
            print("%-22s %s (%s)" % (k, v["nome"], v["paginas"]))
        return 0
    if a.problem:
        show(a.problem, PROBLEMS[a.problem])
        return 0
    if a.custom:
        try:
            sizes = [int(x) for x in a.sizes.split(",")]
        except ValueError:
            print("--sizes must be a list of integers, e.g. 100,50")
            return 2
        cells = 1
        for s in sizes:
            cells *= s
        print("=== CUSTOM FORMULATION (book rule, JE p.125) ===")
        print("Dimensions:      %s" % " x ".join(str(s) for s in sizes))
        print("Subproblems:     %d [inference]: product of the sizes (check that the whole table is actually used, JE p.127 note 12)" % cells)
        print("Space:           O(%d) [inference]: the number of distinct subproblems determines the space (JE p.125)" % cells)
        print("Time:            O(%d * (%s)) [inference]: sum of the times per subproblem (JE p.125)" % (cells, a.cost_per_cell))
        print("Dependencies and order: you must provide and verify them; the dependency graph must be acyclic (JE p.252).")
        print(ROTEIRO)
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
