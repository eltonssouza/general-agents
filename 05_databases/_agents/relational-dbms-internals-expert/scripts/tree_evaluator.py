# -*- coding: utf-8 -*-
"""
tree_evaluator.py - comparative evaluation of hierarchy models in SQL.

ORIGIN AND LIMITS (read before trusting the output):
  - The excerpt of the "Naive Trees" chapter available to the package (ANTI-TREE, PDF p.5-11) covers ONLY the Adjacency List:
    problem and antipattern (p.5-9), how to recognize it (p.10), legitimate uses and SQL-99 recursive queries (p.10-11).
    The section "3.5 Solution: Use Alternative Tree Models" is NOT in the excerpt (only the title, ANTI-TOC p.5).
  - Therefore: Path Enumeration, Nested Sets and Closure Table are described here as [extrapolation] (general
    modeling knowledge), WITHOUT a book page. Do not attribute these three models to Karwin based on this output.
  - WITH RECURSIVE in PostgreSQL 16: PG16 p.174-178 [from source]; SQL-99 recursive syntax: ANTI-TREE p.11.
  - The recommend_model function is a heuristic [extrapolation]/[inference]; it does not come from any source.
Pages = PDF. No network; read-only.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

MODELS = {
    "adjacency_list": {
        "name": "Adjacency List (parent_id column with a foreign key)",
        "origin": "[from source] ANTI-TREE p.6-11",
        "insert_cost": "Simple: inserting a leaf is easy (ANTI-TREE p.9)",
        "move_cost": "Simple: changing parent_id moves a node or subtree (ANTI-TREE p.9)",
        "delete_cost": "More complex: deleting a subtree requires finding descendants and deleting bottom-up, or ON DELETE CASCADE; promoting children requires updating parent_id first (ANTI-TREE p.9)",
        "query_subtree": "Hard without recursion: each level needs another JOIN and the number of JOINs is fixed (ANTI-TREE p.7-8); with WITH RECURSIVE (SQL-99) it becomes feasible (ANTI-TREE p.11; PG16 p.174-175)",
        "referential_integrity": "Native foreign key on parent_id (ANTI-TREE p.6)",
        "summary": "Strength: direct parent/children and insertion (ANTI-TREE p.10). It may be enough; avoid over-engineering (ANTI-TREE p.10-11).",
    },
    "path_enumeration": {
        "name": "Path Enumeration (ancestor path as text)",
        "origin": "[extrapolation] (outside the excerpt)",
        "insert_cost": "Depends on copying the parent's path",
        "move_cost": "Rewrite the paths of the whole subtree",
        "delete_cost": "Depends on the removal model",
        "query_subtree": "By path prefix",
        "referential_integrity": "The database does not enforce path integrity (text)",
        "summary": "General knowledge; check the full book before attributing it to Karwin.",
    },
    "nested_sets": {
        "name": "Nested Sets (left/right bounds per node)",
        "origin": "[extrapolation] (outside the excerpt)",
        "insert_cost": "High: renumbers many rows",
        "move_cost": "High: renumbers many rows",
        "delete_cost": "High: renumbers many rows",
        "query_subtree": "By interval, without recursion",
        "referential_integrity": "No foreign key on the bounds",
        "summary": "General knowledge; suited to nearly static trees and subtree reads.",
    },
    "closure_table": {
        "name": "Closure Table (ancestor/descendant pairs in an auxiliary table)",
        "origin": "[extrapolation] (outside the excerpt)",
        "insert_cost": "Inserts one row per ancestor",
        "move_cost": "Rewrites the subtree's closure rows",
        "delete_cost": "Removes the closure rows",
        "query_subtree": "Simple JOIN on the auxiliary table, without recursion",
        "referential_integrity": "Foreign keys to ancestor and descendant",
        "summary": "General knowledge; higher storage cost; check the full book before attributing it to Karwin.",
    },
}


def recommend_model(frequent_writes, need_fk, deep_subtree_queries, recursive_cte=True):
    """Heuristic [extrapolation]/[inference]. Returns (key, recommendation label)."""
    if not deep_subtree_queries:
        return "adjacency_list", "[from source] ANTI-TREE p.10 (direct parent/children and insertion are the strength)"
    if recursive_cte:
        return "adjacency_list", ("[inference] ANTI-TREE p.11 + PG16 p.174-175: with recursive queries available, "
                                  "Adjacency List + WITH RECURSIVE serves deep subtrees; reassess if the measured performance is not enough")
    if not frequent_writes and not need_fk:
        return "nested_sets", "[extrapolation] nearly static tree with no FK requirement"
    return "closure_table", "[extrapolation] deep subtrees with no recursion available"


def show(key, flag=""):
    m = MODELS[key]
    print("* %s%s  | origin: %s" % (m["name"], flag, m["origin"]))
    print("  - Insert: %s" % m["insert_cost"])
    print("  - Move: %s" % m["move_cost"])
    print("  - Delete: %s" % m["delete_cost"])
    print("  - Subtree: %s" % m["query_subtree"])
    print("  - Referential integrity: %s" % m["referential_integrity"])
    print("  - Summary: %s\n" % m["summary"])


def main():
    ap = argparse.ArgumentParser(description="Evaluator of hierarchy models in SQL (see the limits in the header)")
    ap.add_argument("--model", choices=list(MODELS) + ["all"], default="all")
    ap.add_argument("--frequent-writes", action="store_true", help="frequent writes to the tree")
    ap.add_argument("--need-fk-integrity", action="store_true", help="foreign-key integrity is mandatory")
    ap.add_argument("--deep-subtree-queries", action="store_true", help="frequent queries for subtrees of arbitrary depth")
    ap.add_argument("--no-recursive-cte", action="store_true", help="the target DBMS has no WITH RECURSIVE (PostgreSQL 16 has it, PG16 p.174)")
    a = ap.parse_args()
    print("=" * 68)
    print("EVALUATION OF HIERARCHIES IN SQL (ANTI-TREE p.5-11; pages = PDF)")
    print("WARNING: only the Adjacency List is in the excerpt; the other 3 models are [extrapolation].")
    print("=" * 68)
    if a.model == "all":
        key, why = recommend_model(a.frequent_writes, a.need_fk_integrity, a.deep_subtree_queries, not a.no_recursive_cte)
        print("\nRECOMMENDATION (heuristic): %s\nBasis: %s\n" % (MODELS[key]["name"], why))
        for k in MODELS:
            show(k, " [RECOMMENDED]" if k == key else "")
    else:
        show(a.model)
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
