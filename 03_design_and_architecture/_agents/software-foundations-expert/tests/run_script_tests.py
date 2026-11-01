# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic script tests (ST-01..ST-29; the CT-nn cases of tests/casos-de-teste.md that use scripts point to them).

Usage (from the package root):
  python -I tests/run_script_tests.py [--src FOLDER_WITH_sicp.txt_taup.txt_ci.txt]
With --src, also runs verify_citations.py and audit_tokens.py. No network. Exit code 0 if everything passes.
The tests were NOT run by an independent model (see tests/relatorio-de-fidelidade.md).
"""
import argparse
import json
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
T = os.path.join(ROOT, "tests")
CASES = []


def run(path, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args), capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


def case(cid, desc, script, args, must=(), rc=0, must_not=()):
    CASES.append((cid, desc, os.path.join(S, script), list(args), list(must), rc, list(must_not)))


# --- foundations_lookup.py
case("ST-01", "lookup: substitution model", "foundations_lookup.py", ["substitution model"], ["[SICP p.28-30]", "modelos-de-avaliacao"])
case("ST-02", "lookup: applicative/normal order", "foundations_lookup.py", ["normal order"], ["[SICP p.30-31]"])
case("ST-03", "lookup: tricolor", "foundations_lookup.py", ["tricolor"], ["[CI p.517-518]"])
case("ST-04", "lookup: rule of silence", "foundations_lookup.py", ["rule of silence"], ["[TAUP p.45-46]"])
case("ST-05", "lookup: NaN boxing", "foundations_lookup.py", ["NaN boxing"], ["[CI p.601-604]"])
case("ST-06", "lookup: out of scope", "foundations_lookup.py", ["kubernetes"], ["NOT COVERED"], rc=1)
case("ST-07", "lookup: dynamic scope is not in SICP", "foundations_lookup.py", ["--book", "SICP", "dynamic scoping"],
     ["ALERT (boundary)", "NOT COVERED"], rc=1)
case("ST-08", "lookup: dynamic scope in CI", "foundations_lookup.py", ["--book", "CI", "dynamic scope"], ["[CI p.131]"])
case("ST-09", "lookup: double dispatch is not a CI term", "foundations_lookup.py", ["visitor double dispatch"],
     ["ALERT (boundary)", "NOT COVERED"], rc=1)
case("ST-10", "lookup: list of what the book does not contain", "foundations_lookup.py", ["--not-in-book"], ["homoiconic", "Cheney", "chapter 9"])
case("ST-11", "lookup: the 90/10 rule is in ch. 15", "foundations_lookup.py", ["profiling"], ["[TAUP p.412]"])
case("ST-12", "lookup: json", "foundations_lookup.py", ["--json", "closure property"], ['"book": "SICP"', '"pages": "104-104"'])
# --- evaluator_trace.py
case("ST-13", "applicative substitution of (f 5)", "evaluator_trace.py", ["--mode", "substitution", "--expr", "(f 5)", "--order", "applicative"],
     ["(sum-of-squares (+ 5 1) (* 5 2))", "(+ 36 100)", "Value: 136", "primitive reductions: 5"])
case("ST-14", "normal-order substitution re-evaluates", "evaluator_trace.py", ["--mode", "substitution", "--expr", "(f 5)", "--order", "normal"],
     ["Value: 136", "primitive reductions: 7", "(+ (* (+ 5 1) (+ 5 1))"])
case("ST-15", "orders compared", "evaluator_trace.py", ["--mode", "orders"], ["Same value in both orders: True", "SICP p.31"])
case("ST-16", "set! breaks substitution", "evaluator_trace.py", ["--mode", "mutable_breakdown"],
     ["'(W 10)': -5", "'(D 10)': 15", "SICP p.219", "set! 25"])
case("ST-17", "environment model", "evaluator_trace.py", ["--mode", "environment"],
     ["enclosing = E1 (procedure's env, NOT the caller's)", "'(W2 40)': 60", "E1': 25"])
case("ST-18", "error: unknown operator", "evaluator_trace.py", ["--expr", "(g 3)"], ["unknown operator"], rc=2)
case("ST-19", "own expression with extra define", "evaluator_trace.py",
     ["--expr", "(triplo (+ 1 1))", "--define", "(define (triplo x) (* 3 x))"], ["Value: 6"])
# --- unix_philosophy_checker.py
case("ST-20", "checker: chatty_cli violates silence", "unix_philosophy_checker.py", ["--preset", "chatty_cli"],
     ["[VIOLATION] Rule of Silence", "TAUP p.45-46", "heuristic"])
case("ST-21", "checker: classic_unix = 100", "unix_philosophy_checker.py", ["--preset", "classic_unix"], ["100/100"])
case("ST-22", "checker: 17 rules listed", "unix_philosophy_checker.py", ["--rules"], ["17. Rule of Extensibility", "TAUP p.50"])
case("ST-23", "checker: unknown check", "unix_philosophy_checker.py", ["--set", "foo=1"], ["unknown checks"], rc=2)
# --- compiler_pipeline_audit.py
case("ST-24", "pipeline: tree-walk vs bytecode", "compiler_pipeline_audit.py", ["--topic", "treewalk_vs_bytecode"],
     ["72 s", "CI p.232", "[from source]"], must_not=["5x a 10x", "10x a 50x", "5x to 10x", "10x to 50x"])
case("ST-25", "pipeline: GC", "compiler_pipeline_audit.py", ["--topic", "gc_architecture"], ["tableRemoveWhite", "CI p.523-525"])
case("ST-26", "pipeline: NaN boxing", "compiler_pipeline_audit.py", ["--topic", "value_representation"], ["16 bytes", "51 free bits"])


def check_index():
    ip = os.path.join(S, "foundations_index.json")
    with open(ip, encoding="utf-8") as f:
        d = json.load(f)
    npages = {"SICP": 634, "TAUP": 549, "CI": 630}
    bad = []
    for e in d["entries"]:
        a, _, z = e["pages"].partition("-")
        a, z = int(a), int(z or a)
        if not (1 <= a <= z <= npages[e["book"]]):
            bad.append(e["id"])
        if not os.path.isfile(os.path.join(ROOT, "references", e["ref"])):
            bad.append(e["id"] + ":ref")
    return bad, len(d["entries"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    fails = 0
    for cid, desc, script, args, must, rc, must_not in CASES:
        code, out = run(script, *args)
        missing = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not missing and not bad
        print("%s %-6s %s" % ("OK   " if ok else "FAIL ", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (code, rc, missing, bad))
    bad, n = check_index()
    ok = not bad
    print("%s %-6s index: %d entries with pages in range and existing reference file" % ("OK   " if ok else "FAIL ", "ST-27", n))
    if not ok:
        fails += 1
        print("   problems:", bad)
    if a.src:
        for name, extra in (("verify_citations.py", []), ("audit_tokens.py", [])):
            code, out = run(os.path.join(T, name), "--src", a.src, *extra)
            last = [ln for ln in out.strip().splitlines() if ln.strip()][-1] if out.strip() else ""
            ok = code == 0
            print("%s %-6s %s -> %s" % ("OK   " if ok else "FAIL ", "ST-28" if "verify" in name else "ST-29", name, last))
            if not ok:
                fails += 1
                print(out[-1500:])
    print("Total failures: %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
