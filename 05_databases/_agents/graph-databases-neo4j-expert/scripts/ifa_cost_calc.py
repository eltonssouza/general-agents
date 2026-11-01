# -*- coding: utf-8 -*-
"""
ifa_cost_calc.py - compares the COUNT of traversal operations: index-free adjacency (IFA) vs. index.

What is from the book (NEO4J, PDF p.168-170):
  - following a relationship with IFA costs O(1); an index lookup costs O(log n);
  - traversing m steps costs O(m) with IFA and O(m log n) with an index.
What is NOT from the book (labeled in the output):
  - the "k^d" variant (m = number of visited nodes = sum of k^i for i=1..d) is [inference];
  - the index fan-out (log base) is a PARAMETER [extrapolation]; the book does not mention B+ trees;
  - the computed ratio is a counting model, not a measured time. The book's measured times are in
    Table 2-1 (PDF p.38-39): use --table21.

Usage:
  python -I ifa_cost_calc.py -N 1000000 -d 3 -k 50 [--fanout 100]
  python -I ifa_cost_calc.py --steps 1000 -N 1000000          (m steps, no k^d)
  python -I ifa_cost_calc.py --table21
No network; read-only.
"""
import argparse
import math
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

TABLE_2_1 = [
    (2, "0.016", "0.01", "~2500"),
    (3, "30.267", "0.168", "~110,000"),
    (4, "1543.505", "1.359", "~600,000"),
    (5, "unfinished", "2.132", "~800,000"),
]


def index_levels(n, fanout):
    """Search levels in an index of n entries with the given fan-out ([extrapolation] model)."""
    if n <= 1:
        return 1.0
    return max(1.0, math.log(n) / math.log(fanout))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-N", "--nodes", type=int, default=1000000, help="total size (n) [default 1,000,000]")
    ap.add_argument("-d", "--depth", type=int, help="traversal depth")
    ap.add_argument("-k", "--degree", type=float, help="average degree per node")
    ap.add_argument("--steps", type=int, help="number m of steps (alternative to -d/-k)")
    ap.add_argument("--fanout", type=float, default=2.0,
                    help="index log base [extrapolation; default 2 = log2 n, the simplest model]")
    ap.add_argument("--table21", action="store_true", help="print the book's Table 2-1")
    a = ap.parse_args()

    if a.table21:
        print("Book Table 2-1 (NEO4J p.39): friends of friends, 1,000,000 people, ~50 friends each.")
        print("Origin: experiment by Partner and Vukotic (Neo4j in Action) [DATED: old Neo4j version].")
        print("%-6s %-14s %-14s %s" % ("Depth", "RDBMS (s)", "Neo4j (s)", "Records"))
        for row in TABLE_2_1:
            print("%-6s %-14s %-14s %s" % row)
        return 0

    if a.steps is not None:
        m = a.steps
        origem = "m = %d (given)" % m
    elif a.depth is not None and a.degree is not None:
        m = sum(a.degree ** i for i in range(1, a.depth + 1))
        origem = "m = sum of k^i, i=1..d = %.0f visited nodes [inference, not in the book]" % m
    else:
        ap.error("provide --steps, or -d and -k, or --table21")
    lv = index_levels(a.nodes, a.fanout)
    ifa = m
    idx = m * lv
    print("Parameters: n=%d  %s  index fan-out=%.0f" % (a.nodes, origem, a.fanout))
    print("")
    print("[from source] (NEO4J p.168-170): IFA = O(m); index = O(m log n); immediate relationship O(1) vs lookup O(log n).")
    print("  IFA    : %.0f pointer operations" % ifa)
    print("  Index  : %.0f elementary lookups (m x %.2f levels)  [log base fan-out: extrapolation]" % (idx, lv))
    print("  Ratio  : %.2fx (counting model; NOT a measured time)" % (idx / ifa if ifa else 1.0))
    print("")
    print("Limits: the book also shows that IFA makes queries without traversal harder (NEO4J p.24)")
    print("and that performance can be worse than the theory because of cache contention (NEO4J p.169).")
    print("Measured times from the book: use --table21.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
