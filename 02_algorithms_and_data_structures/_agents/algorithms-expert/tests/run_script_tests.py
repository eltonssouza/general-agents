# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic cases (CT-xx from tests/casos-de-teste.md) against the package scripts and
checks that the output contains what the book says (and does NOT contain what v1 claimed without support).
Usage (from the package root):  python -I tests/run_script_tests.py [--text erickson.txt]
With --text it also runs verify_citations.py and audit_tokens.py. No network. Exit 0 if everything passes.
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "skills")
TS = os.path.join(ROOT, "tests")

SCRIPTS = {
    "solve": os.path.join(SK, "recurrence-solver", "scripts", "solve_recurrence.py"),
    "check": os.path.join(SK, "recurrence-solver", "scripts", "check_recurrence.py"),
    "dp": os.path.join(SK, "dp-table-analyzer", "scripts", "analyze_dp.py"),
    "graph": os.path.join(SK, "graph-complexity-audit", "scripts", "audit_graph_complexity.py"),
    "lookup": os.path.join(SK, "erickson-topic-lookup", "scripts", "erickson_lookup.py"),
}


def run(path, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args), capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


CASES = []


def case(cid, desc, key, args, must, rc=0, must_not=()):
    CASES.append((cid, desc, key, args, must, rc, must_not))


case("CT-02", "MergeSort by the recursion tree", "solve", ["--a", "2", "--b", "2", "--k", "1"],
     ["equal", "Theta(n log n)", "JE p.51"])
case("CT-03", "Karatsuba", "solve", ["--a", "3", "--b", "2", "--k", "1"], ["increasing", "Theta(n^1.585)", "JE p.51"])
case("CT-04", "MomSelect (unequal subproblems)", "solve", ["--terms", "1/5,1;7/10,1", "--k", "1"],
     ["decreasing", "Theta(n)", "JE p.56"])
case("CT-05", "blocks of 3 (balanced)", "solve", ["--terms", "1/3,1;2/3,1", "--k", "1"], ["balanced", "Theta(n log n)"])
case("CT-05b", "solver does not use the name Master Theorem", "solve", ["--a", "2", "--b", "2", "--k", "1"], ["RECURSION TREE"],
     must_not=["Master Theorem"])
case("CT-06", "numerical verifier: all the book's recurrences", "check", ["--all"], ["0 failures"])
case("CT-06b", "Hanoi exact 2^n-1", "check", ["--preset", "hanoi", "--max", "20"], ["expected=1048575", "OK"], must_not=["FAIL"])
case("CT-06c", "RecFibo calls = 2F(n+1)-1", "check", ["--preset", "recfibo-calls", "--max", "40"], ["OK"], must_not=["FAIL"])
case("CT-07", "DP: edit distance O(mn) and labeled optimization [extrapolation]", "dp", ["--problem", "edit_distance"],
     ["O(mn)", "JE p.132", "O(min(m,n))", "[extrapolation]"])
case("CT-08", "DP: Subset Sum O(nT) and pseudopolynomial (p.422)", "dp", ["--problem", "subset_sum"],
     ["O(nT)", "JE p.135", "JE p.422", "[extrapolation]"])
case("CT-08b", "DP: LIS n log n and extrapolation", "dp", ["--problem", "lis_first"], ["O(n^2)", "[extrapolation]"])
case("CT-09", "graphs: Dijkstra and negative edges (the book's nuance)", "graph", ["--algo", "dijkstra"],
     ["NonnegativeDijkstra", "EXPONENTIAL", "JE p.307"])
case("CT-10", "graphs: Johnson (binary vs Fibonacci)", "graph", ["--algo", "johnson"],
     ["O(VE log V)", "Fibonacci", "JE p.329"])
case("CT-11", "graphs: Edmonds-Karp fattest path and time", "graph", ["--algo", "edmonds_karp_fattest"],
     ["O(E^2 log E log|f*|)", "TIME", "JE p.359"])
case("CT-12", "lookup: Master Theorem (Portuguese query) = NOT COVERED", "lookup", ["teorema mestre"], ["NOT COVERED in the book", "p.454"])
case("CT-12b", "lookup: Master Theorem (English query) = NOT COVERED", "lookup", ["master theorem"], ["NOT COVERED in the book", "p.454"])
case("CT-13", "lookup: minimax outside the book", "lookup", ["minimax"], ["NOT COVERED"], rc=1)
case("CT-14", "lookup: Levenshtein", "lookup", ["levenshtein"], ["JE p.129-134"])
case("CT-14b", "lookup: edit distance (English query)", "lookup", ["edit distance"], ["JE p.129-134"])
case("CT-14c", "lookup: distancia de edicao (Portuguese query)", "lookup", ["distancia de edicao"], ["JE p.129-134"])
case("CT-15", "lookup: page 307", "lookup", ["--page", "307"], ["Ch. 8", "Bellman-Ford"])
case("CT-16", "lookup: printed 112 -> PDF 130", "lookup", ["--printed", "112"], ["PDF 130"])
case("CT-17", "lookup: nonexistent topic", "lookup", ["xyzzy"], ["NOT COVERED"], rc=1)
case("CT-18", "lookup: list", "lookup", ["--list"], ["Ch. 12", "The book does NOT cover"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    a = ap.parse_args()
    fails = 0
    for cid, desc, key, args, must, rc, must_not in CASES:
        code, out = run(SCRIPTS[key], *args)
        missing = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not missing and not bad
        print("%s %-7s %s" % ("OK   " if ok else "FAIL ", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (code, rc, missing, bad))
    if a.text:
        for nome, args in (("verify_citations", ["--text", a.text]), ("audit_tokens", ["--text", a.text, "--pkg", ROOT])):
            code, out = run(os.path.join(TS, nome + ".py"), *args)
            last = out.strip().splitlines()[-1] if out.strip() else ""
            ok = code == 0
            print("%s %-17s %s" % ("OK   " if ok else "FAIL ", nome, last))
            fails += 0 if ok else 1
    print("Summary: %d script cases, %d failures" % (len(CASES), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
