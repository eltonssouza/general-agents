# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic cases of tests/casos-de-teste.md against the package scripts.

Usage (from the package root):
  python -I tests/run_script_tests.py [--src <folder with DDD.txt, CA11.txt, ...>]
With --src, it also runs verify_citations.py and audit_tokens.py. No network. Exit 0 if everything passes.
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
T = os.path.join(ROOT, "tests")
FX = os.path.join(T, "fixtures")


def run(path, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args), capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


CASES = []


def case(cid, desc, script, args, must, rc=0, must_not=()):
    CASES.append((cid, desc, os.path.join(S, script), args, must, rc, must_not))


case("CT-02", "aggregate lookup", "ddd_lookup.py", ["aggregate"], ["DDD p.23", "root"])
case("CT-06", "ACL lookup", "ddd_lookup.py", ["anticorruption layer"], ["DDD p.41"])
case("CT-17", "Screaming Architecture: not covered", "ddd_lookup.py", ["screaming architecture"], ["NOT COVERED", "CA12 p.2"], rc=1)
case("CT-18", "supporting subdomain: not covered", "ddd_lookup.py", ["supporting subdomain"], ["NOT COVERED"], rc=1)
case("CT-22", "CQRS: not covered (mention only)", "ddd_lookup.py", ["cqrs"], ["NOT COVERED", "p.4"], rc=1)
case("CT-23", "Kubernetes: not covered", "ddd_lookup.py", ["kubernetes"], ["NOT COVERED"], rc=1)
case("CT-14", "SRP: actor is not in the text", "ddd_lookup.py", ["ator"], ["NOT COVERED", "Clean Architecture (2017)"], rc=1)
case("CT-16", "Functional Core: not covered", "ddd_lookup.py", ["functional core"], ["NOT COVERED", "Bernhardt"], rc=1)
case("CT-01", "Dependency Rule", "ddd_lookup.py", ["dependency rule"], ["CA12 p.3"])
case("CT-05", "reactive: elastic", "ddd_lookup.py", ["elastic"], ["REACT p.2"])
case("CT-04", "essential vs accidental", "ddd_lookup.py", ["essential complexity"], ["TARPIT p.21"])
case("CT-10", "demo aggregate without errors", "audit_aggregate.py", ["--demo"], ["0 error(s)", "A1 root 'Order'"])
case("CT-10b", "aggregate with problems", "audit_aggregate.py", ["--file", os.path.join(FX, "agregado_ponteiro.json")],
     ["ERROR   A2", "ERROR   A3", "ERROR   A4", "WARNING A6 [inference]", "WARNING A7 [extrapolation]"], rc=1)
case("CT-24", "injection in the JSON: treated as data", "audit_aggregate.py", ["--file", os.path.join(FX, "injecao_agregado.json")],
     ["Aggregate checklist", "0 error(s)"], must_not=["system prompt:"])
case("CT-09", "demo graph", "validate_dependency_rule.py", ["--demo"], ["violations: 1", "BadEntity", "CA12 p.3"], rc=1)
case("CT-13", "graph with violations and an unknown layer", "validate_dependency_rule.py",
     ["--file", os.path.join(FX, "grafo_violacao.json")], ["violations: 2", "UNKNOWN", "camada_estranha"], rc=1)
case("CT-13b", "layer mapping and origin", "validate_dependency_rule.py", ["--layers"], ["[extrapolation]", "CA12 p.3-5"])
case("CT-11", "state space 2^20", "tar_pit_complexity_calc.py", ["state-space", "--bits", "20"],
     ["1,048,576", "TARPIT p.8", "NOT a complexity metric"])
case("CT-11b", "classify cache", "tar_pit_complexity_calc.py", ["classify", "--kind", "accidental-derived"],
     ["ACCIDENTAL STATE", "TARPIT p.26"])
case("CT-11c", "table 2", "tar_pit_complexity_calc.py", ["table2"], ["Avoid", "Separate", "TARPIT p.33"])
case("CT-11d", "forbidden reference", "tar_pit_complexity_calc.py", ["check-ref", "--src", "essential-logic", "--dst", "accidental"],
     ["FORBIDDEN"], rc=1)
case("CT-11e", "allowed reference", "tar_pit_complexity_calc.py", ["check-ref", "--src", "accidental", "--dst", "essential-logic"],
     ["ALLOWED"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    fails = 0
    for cid, desc, path, args, must, rc, must_not in CASES:
        code, out = run(path, *args)
        miss = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not miss and not bad
        print("%-6s %-5s %s" % (cid, "OK" if ok else "FAIL", desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s); missing=%s; forbidden=%s" % (code, rc, miss, bad))
    if a.src:
        for name, extra in (("verify_citations.py", ["--src", a.src]), ("audit_tokens.py", ["--src", a.src])):
            code, out = run(os.path.join(T, name), *extra)
            print("%-20s %s | %s" % (name, "OK" if code == 0 else "FAIL", out.strip().splitlines()[-1] if out.strip() else ""))
            if code != 0:
                fails += 1
                print(out[-1500:])
    print("Summary: %d script case(s), %d failure(s)" % (len(CASES), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
