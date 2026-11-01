#!/usr/bin/env python3
"""run_script_tests.py - deterministic tests of the graphql-expert scripts. Usage: python -I run_script_tests.py"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "..", "scripts")
FX = os.path.join(HERE, "fixtures")
fails = 0

def run(*a):
    p = subprocess.run([sys.executable, "-I", *a], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr

def check(name, ok, extra=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " :: " + extra[:200]))
    if not ok:
        fails += 1

L = os.path.join(S, "gql_lookup.py")
C = os.path.join(S, "gql_checklist.py")
rc, o = run(L, "mutations"); check("lookup mutations -> learn-l4 p.2", "learn-l4" in o and "p.2" in o, o)
rc, o = run(L, "fragments variables"); check("lookup fragments/variables -> learn-l3", "learn-l3" in o, o)
rc, o = run(L, "federated"); check("lookup federated -> sg-l1 p.3", "sg-l1" in o and "p.3" in o, o)
rc, o = run(L, "subscriptions"); check("lookup subscriptions -> NOT COVERED", "NOT COVERED" in o and rc == 1 or "NOT COVERED (detail)" in o, o)
rc, o = run(L, "dataloader n+1"); check("lookup dataloader -> NOT COVERED", "NOT COVERED" in o, o)
rc, o = run(L, "kubernetes helm"); check("lookup off-topic -> NOT COVERED, exit 1", "NOT COVERED" in o and rc == 1, o)
rc, o = run(L, "rest x graphql"); check("lookup REST x GraphQL -> bp-l2 + warning", "bp-l2" in o and "NOT COVERED" in o, o)
rc, o = run(L, "--gaps"); check("gaps lists subscriptions and pagination", "Subscriptions" in o and "Pagination" in o, o)
rc, o = run(L, "--page", "3"); check("page 3 -> governance", "sg-l4" in o and "bp-l4" in o, o)
rc, o = run(L, "--page", "9"); check("page 9 -> NOT COVERED", "NOT COVERED" in o and rc == 1, o)
rc, o = run(L, "--json", "uploads"); check("json uploads valid", json.loads(o)["entries"][0]["id"] == "bp-l4", o)
rc, o = run(L, "--list"); check("list 20 entries", len([l for l in o.splitlines() if l.strip()]) == 20, o)
rc, o = run(C, "list"); check("checklist list has T4 Hasura", "Hasura" in o, o)
rc, o = run(C, "check", os.path.join(FX, "notas-boas.md")); check("check notas-boas covers L3a,G1b,T4", "[x] L3a" in o and "[x] G1b" in o and "[x] T4" in o and "[ ] L4" not in o, o)
rc, o = run(C, "check", os.path.join(FX, "notas-pt.md")); check("check notas-pt (Portuguese keywords) covers L3a,G1b,T4", "[x] L3a" in o and "[x] G1b" in o and "[x] T4" in o and "[ ] L4" not in o, o)
rc, o = run(C, "check", os.path.join(FX, "notas-curtas.md")); check("check notas-curtas points out gaps", "[ ] G4" in o and "[x] L4" in o, o)
rc, o = run(C, "check", os.path.join(FX, "notas-injecao.md")); check("check injection: only detects mutations and does not execute", "[x] L4" in o and rc == 0, o)
rc, o = run(C, "check", os.path.join(FX, "nao-existe.md")); check("check nonexistent -> exit 2", rc == 2, o)
src_txt = os.path.join(HERE, "..", "..", "..", "..", "scratch", "frameworks", "GraphQL-Learn-Official.txt")
if os.path.exists(src_txt):
    rc, o = run(os.path.join(HERE, "verify_citations.py")); check("verify_citations passes", rc == 0, o)
else:
    print("SKIP verify_citations (extracted text not found; use verify_citations.py --txt)")
print("failures:", fails)
sys.exit(1 if fails else 0)
