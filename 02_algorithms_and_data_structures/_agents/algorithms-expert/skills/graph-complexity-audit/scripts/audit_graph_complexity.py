# -*- coding: utf-8 -*-
"""
audit_graph_complexity.py - complexity worksheet for graph algorithms according to Erickson's book ("Algorithms", 2019).

Book convention: running times assume the standard ADJACENCY LIST unless noted (JE p.217). Pages = PDF (printed = PDF - 18).
Each piece of information carries its origin: [from source] (JE p.N) | [inference] | [extrapolation] | [DATED].
Numeric estimate (--v, --e): order of magnitude only, with constant 1 and log2; NOT real running time [inference].
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

ALGOS = {
    "bfs": {
        "nome": "Breadth-first search (BFS)",
        "tempo": ["O(V+E) [from source] (JE p.220, 299)", "with an adjacency matrix, O(V^2+ET) in the generic skeleton [from source] (JE p.219)"],
        "condicoes": "unweighted graphs (shortest paths in number of edges) [from source] (JE p.296-300)",
        "formula": lambda v, e, f: v + e,
    },
    "dfs": {
        "nome": "Depth-first search (DFS)",
        "tempo": ["O(V+E) [from source] (JE p.219, 244)"],
        "condicoes": "any graph; in directed graphs the forest covers the graph with DFSAll [from source] (JE p.244-245)",
        "formula": lambda v, e, f: v + e,
    },
    "whatever_first": {
        "nome": "Whatever-First Search (skeleton)",
        "tempo": ["O(V+ET), T = cost of insert/remove in the bag [from source] (JE p.219)",
                  "stack or queue: O(V+E); priority queue: O(V+E log E) [from source] (JE p.219-220)"],
        "condicoes": "it is O(V+E) only when T=O(1) [inference]",
        "formula": lambda v, e, f: v + e * math.log2(max(e, 2)),
    },
    "topological_sort": {
        "nome": "Topological sort (reverse of the DFS postorder)",
        "tempo": ["O(V+E) [from source] (JE p.250-251)"],
        "condicoes": "dags only; if there is a cycle, it fails by finding an edge to an active vertex [from source] (JE p.249, 251)",
        "formula": lambda v, e, f: v + e,
    },
    "scc_kosaraju": {
        "nome": "Strong components: Kosaraju-Sharir",
        "tempo": ["O(V+E) [from source] (JE p.258-259)"],
        "condicoes": "phase 1: DFS on rev(G) pushing in postorder; phase 2: search in G in stack order [from source] (JE p.258-259)",
        "formula": lambda v, e, f: v + e,
    },
    "scc_tarjan": {
        "nome": "Strong components: Tarjan",
        "tempo": ["O(V+E) [from source] (JE p.262)"],
        "condicoes": "a single DFS with low(v) and an auxiliary stack [from source] (JE p.260-262)",
        "formula": lambda v, e, f: v + e,
    },
    "boruvka": {
        "nome": "MST: Boruvka",
        "tempo": ["O(E log V) [from source] (JE p.280)"],
        "condicoes": "connected, undirected graph, distinct weights (or consistent tie-breaking) [from source] (JE p.276-277)",
        "formula": lambda v, e, f: e * math.log2(max(v, 2)),
    },
    "jarnik_prim": {
        "nome": "MST: Jarnik (Prim)",
        "tempo": ["O(E log V) with a binary heap [from source] (JE p.282)", "O(E + V log V) with a Fibonacci heap [from source] (JE p.283)"],
        "condicoes": "the book warns that the Fibonacci heap rarely pays off in practice [from source] (JE p.283)",
        "formula": lambda v, e, f: e * math.log2(max(v, 2)),
    },
    "kruskal": {
        "nome": "MST: Kruskal",
        "tempo": ["O(E log V), dominated by the O(E log E) sort [from source] (JE p.285-286)",
                  "union-find with union by rank and compression: O(E alpha(V)) for maintaining the sets [from source] (JE p.285, note 6)"],
        "condicoes": "undirected graph [from source] (JE p.275)",
        "formula": lambda v, e, f: e * math.log2(max(v, 2)),
    },
    "dag_sssp": {
        "nome": "Shortest paths in a dag",
        "tempo": ["O(V+E) [from source] (JE p.300-302)"],
        "condicoes": "accepts negative weights (there are no cycles) [from source] (JE p.300)",
        "formula": lambda v, e, f: v + e,
    },
    "dijkstra": {
        "nome": "Shortest paths: Dijkstra",
        "tempo": ["O(E log V) with a binary heap [from source] (JE p.306)", "O(V^2) in Dijkstra's original version [from source] (JE p.306, note 8)",
                  "O(E + V log V) with a Fibonacci heap [from source] (JE p.306, note 8)"],
        "condicoes": ("Nonnegative weights: correct, and each vertex leaves the queue at most once [from source] (JE p.304-306). "
                      "WITH NEGATIVE EDGES: the NonnegativeDijkstra version does NOT compute correctly [from source] (JE p.306-307); "
                      "the full Dijkstra (Insert + DecreaseKey) is correct if there is no negative cycle, but the worst case is EXPONENTIAL "
                      "(Shier-Witzgall family: Theta(2^(V/2)) relaxations) [from source] (JE p.307). "
                      "For negative edges prefer Bellman-Ford or the dag algorithm [inference]."),
        "formula": lambda v, e, f: e * math.log2(max(v, 2)),
    },
    "bellman_ford": {
        "nome": "Shortest paths: Bellman-Ford",
        "tempo": ["O(VE) [from source] (JE p.310)"],
        "condicoes": "accepts negative weights; if a tense edge still exists after V-1 iterations, there is a negative cycle [from source] (JE p.310)",
        "formula": lambda v, e, f: v * e,
    },
    "johnson": {
        "nome": "All pairs: Johnson",
        "tempo": ["O(VE log V) = O(V^3 log V) with a binary heap [from source] (JE p.330)",
                  "O(VE + V^2 log V) with a Fibonacci heap [from source] (JE p.329, note 3)"],
        "condicoes": "negative weights without a negative cycle; reweighting w'(uv)=dist(s,u)+w(uv)-dist(s,v) [from source] (JE p.330-331)",
        "formula": lambda v, e, f: v * e * math.log2(max(v, 2)),
    },
    "floyd_warshall": {
        "nome": "All pairs: Floyd-Warshall",
        "tempo": ["O(V^3) [from source] (JE p.337)"],
        "condicoes": "negative weights without a negative cycle; a log V factor faster than Leyzorek's DP [from source] (JE p.336)",
        "formula": lambda v, e, f: v ** 3,
    },
    "ford_fulkerson": {
        "nome": "Maximum flow: Ford-Fulkerson",
        "tempo": ["O(E |f*|) with integer capacities [from source] (JE p.352)"],
        "condicoes": ("exponential in the input size in bits; with irrational capacities it may not terminate or converge to the maximum "
                      "[from source] (JE p.353-354). Provide --flow for the estimate."),
        "formula": lambda v, e, f: e * (f if f is not None else float("nan")),
    },
    "edmonds_karp_fattest": {
        "nome": "Maximum flow: Edmonds-Karp, fattest path",
        "tempo": ["O(E^2 log E log|f*|) in total TIME, with integer capacities [from source] (JE p.359)",
                  "number of augmentations: E ln|f*| [from source] (JE p.358-359)"],
        "condicoes": "bottleneck-maximizing path found in O(E log V) [from source] (JE p.358); may not terminate with irrational capacities [from source] (JE p.359)",
        "formula": lambda v, e, f: (e * e * math.log2(max(e, 2)) * math.log2(max(f, 2))) if f else float("nan"),
    },
    "edmonds_karp_shortest": {
        "nome": "Maximum flow: Edmonds-Karp, shortest path (BFS)",
        "tempo": ["O(VE^2) [from source] (JE p.360)", "at most EV/2 augmentations, independent of the capacities [from source] (JE p.359-360)"],
        "condicoes": "each augmentation costs O(E) by BFS in the residual graph [from source] (JE p.359)",
        "formula": lambda v, e, f: v * e * e,
    },
    "bipartite_matching": {
        "nome": "Maximum bipartite matching via flow",
        "tempo": ["O(VE) with Ford-Fulkerson [from source] (JE p.374)", "O(sqrt(V) E) with Hopcroft-Karp (cited) [from source] (JE p.374)"],
        "condicoes": "capacity 1 on all edges of the network [from source] (JE p.373-374)",
        "formula": lambda v, e, f: v * e,
    },
    "orlin": {
        "nome": "Maximum flow: Orlin (black box)",
        "tempo": ["O(VE) [from source] (JE p.361-362)"],
        "condicoes": "[DATED] fastest known as of 2019, according to the book; the book says to cite 'maximum flows in O(VE) time'",
        "formula": lambda v, e, f: v * e,
    },
}


def main():
    ap = argparse.ArgumentParser(description="Complexity worksheet for graph algorithms (Erickson's book).")
    ap.add_argument("--algo", choices=sorted(ALGOS))
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--v", type=int)
    ap.add_argument("--e", type=int)
    ap.add_argument("--flow", type=int, help="value of the maximum flow |f*| (only for the flow algorithms)")
    a = ap.parse_args()
    if a.list or not a.algo:
        for k, v in sorted(ALGOS.items()):
            print("%-24s %s" % (k, v["nome"]))
        return 0 if a.list else 2
    d = ALGOS[a.algo]
    print("=== GRAPH COMPLEXITY WORKSHEET (pages = PDF; printed = PDF - 18; adjacency list, JE p.217) ===")
    print("Algorithm:  %s" % d["nome"])
    for t in d["tempo"]:
        print("Time:       %s" % t)
    print("Conditions: %s" % d["condicoes"])
    if a.v is not None and a.e is not None:
        dens = a.e / (a.v * (a.v - 1) / 2) if a.v > 1 else 0.0
        print("\n--- Order-of-magnitude estimate (constant 1, log2) [inference] ---")
        print("V=%d  E=%d  density (undirected)=%.4f" % (a.v, a.e, dens))
        val = d["formula"](a.v, a.e, a.flow)
        if val != val:
            print("Provide --flow |f*| for this estimate.")
        else:
            print("~ %.3e elementary operations (NOT real running time; no constants)" % val)
    return 0


if __name__ == "__main__":
    sys.exit(main())
