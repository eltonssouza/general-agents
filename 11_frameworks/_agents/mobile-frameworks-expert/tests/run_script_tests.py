# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic test cases for the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]   # --src enables verify_citations.py
Exit 0 if all pass. Conceptual cases (which need the agent) are in tests/casos-de-teste.md.
"""
import argparse
import json
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL, OK = [], []
L = os.path.join("scripts", "mob_lookup.py")
CMP = os.path.join("scripts", "mob_compare.py")
LINT = os.path.join("scripts", "swift_lint.py")
CK = os.path.join("scripts", "swift_tour_checklist.py")
FX = os.path.join("tests", "fixtures")


def run(args, stdin=None):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG, input=stdin)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def has(out, *subs):
    return all(s in out for s in subs)


def rules_of(out):
    return set(re.findall(r"\b(SWF-[X0-9]+)\b", out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()

    # ---- lookup
    rc, o = run([L, "optional"])
    check("lookup optional -> SWT p.4", "[SWT p.4]" in o, o)
    rc, o = run([L, "swiftui"])
    check("lookup swiftui -> NOT COVERED (and finds FLT p.1)", has(o, "NOT COVERED", "FLT p.1"), o)
    rc, o = run([L, "snack"])
    check("lookup snack -> RN p.2,3", "RN p.2,3" in o, o)
    rc, o = run([L, "constraints", "--source", "FLT"])
    check("lookup constraints in FLT", has(o, "FLT p.1,2") and "SWT" not in o, o)
    rc, o = run([L, "hot", "reload"])
    check("lookup hot reload -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "kubernetes"])
    check("lookup out-of-scope term -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "async", "await"])
    check("lookup async await -> SWT p.14", "SWT p.14" in o, o)
    rc, o = run([L, "--page", "SWT", "19"])
    check("lookup --page SWT 19 -> generics and license", has(o, "Generics", "License"), o)
    rc, o = run([L, "--page", "RN", "4"])
    check("lookup --page RN 4 -> version/date", "Version 0.87" in o, o)
    rc, o = run([L, "--page", "SWT", "20"])
    check("lookup --page SWT 20 -> error", rc == 1, o)
    rc, o = run([L, "--gaps"])
    check("lookup --gaps lists SwiftUI and Dart", has(o, "swiftui", "dart"), o)
    rc, o = run([L, "--sources"])
    check("lookup --sources shows 0.87 and version not stated", has(o, "0.87", "NOT stated"), o)
    rc, o = run([L, "enum", "--json"])
    try:
        check("lookup --json valid", len(json.loads(o)["achados"]) >= 1)
    except Exception as ex:
        check("lookup --json valid", False, str(ex))

    # ---- compare
    rc, o = run([CMP, "list"])
    check("compare list has 22 criteria", len([x for x in o.splitlines() if x.strip()]) == 22, o)
    rc, o = run([CMP, "show", "layout"])
    check("compare show layout: only FLT covers", o.count("NOT COVERED") == 2 and "FLT p.1-2" in o, o)
    rc, o = run([CMP, "show", "concorrencia"])
    check("compare show concorrencia: only SWT covers", "SWT p.14-15" in o and o.count("NOT COVERED") == 2, o)
    rc, o = run([CMP, "ask", "qual é melhor para performance?"])
    check("compare ask recommendation -> NOT COVERED", "NOT COVERED: the sources do not compare" in o, o)
    rc, o = run([CMP, "ask", "which is the best option?"])
    check("compare ask recommendation (English) -> NOT COVERED", "NOT COVERED: the sources do not compare" in o, o)
    rc, o = run([CMP, "show", "nao-existe"])
    check("compare show nonexistent -> NOT COVERED and rc 1", rc == 1 and "NOT COVERED" in o, o)
    rc, o = run([CMP, "table", "--md"])
    check("compare table --md has header and footer", has(o, "| Criterion |", "NOT COVERED", "No ranking"), o)
    rc, o = run([CMP, "show", "versao"])
    check("compare show versao: 0.87 and Swift without a version", has(o, "0.87", "not stated"), o)

    # ---- lint
    rc, o = run([LINT, os.path.join(FX, "bom.swift")])
    check("lint bom.swift no findings, rc 0", rc == 0 and "No findings" in o, o)
    rc, o = run([LINT, os.path.join(FX, "tour-like.swift")])
    check("lint tour-like.swift no findings (tour structure)", rc == 0 and "No findings" in o, o)
    rc, o = run([LINT, os.path.join(FX, "ruim.swift")])
    want = {f"SWF-{n:02d}" for n in range(1, 20)} | {"SWF-X1", "SWF-X2", "SWF-X3"}
    got = rules_of(o)
    check("lint ruim.swift triggers the 22 rules, rc 1", rc == 1 and want <= got, f"missing {sorted(want - got)}")
    check("lint ruim.swift: SWF-01 [from source] SWT p.1", "SWF-01" in o and "SWT p.1" in o, o)
    check("lint: rules outside the tour are [extrapolation]", all(("[extrapolation]" in l) for l in o.splitlines() if "SWF-X" in l), o)
    rc, o = run([LINT, os.path.join(FX, "ruim.swift"), "--no-info"])
    check("lint --no-info removes SWF-15/16/18/X1", not ({"SWF-15", "SWF-16", "SWF-18", "SWF-X1", "SWF-05"} & rules_of(o)), o)
    rc, o = run([LINT, os.path.join(FX, "ruim.swift"), "--json"])
    try:
        d = json.loads(o)
        check("lint --json valid with origin and page", len(d) >= 22 and all("origem" in x and "pagina" in x for x in d))
    except Exception as ex:
        check("lint --json valid with origin and page", False, str(ex))
    rc, o = run([LINT, os.path.join(FX, "injecao.swift")])
    check("lint treats instructions in comments/strings as data (injection)", "SWF-01" in o and rc == 1 and "No findings" not in o, o)
    rc, o = run([LINT, "-"], stdin="let a = 1\na = 2\n")
    check("lint stdin: let reassignment", "SWF-01" in o and rc == 1, o)
    rc, o = run([LINT, "-"], stdin="if x > 1 { print(\"let z = []\") }\n// let q = []\n")
    check("lint ignores strings and comments", "SWF-06" not in o, o)
    rc, o = run([LINT, "--rules"])
    check("lint --rules lists 22 rules", len([x for x in o.splitlines() if x.startswith("SWF-")]) == 22, o)
    rc, o = run([LINT, "nao_existe.swift"])
    check("lint nonexistent file -> rc 2", rc == 2, o)

    # ---- checklist
    rc, o = run([CK, "list"])
    check("checklist list: 38 topics", "38 topics" in o, o)
    rc, o = run([CK, "experiments"])
    check("checklist experiments: 20 exercises", "20 exercises" in o, o)
    rc, o = run([CK, "scan", os.path.join(FX, "tour-like.swift")])
    check("checklist scan tour-like: >= 85%", re.search(r"\((\d+)%\)", o) and int(re.search(r"\((\d+)%\)", o).group(1)) >= 85, o)
    check("checklist scan: flags multiline (p.2) as missing", "[ ]  6." in o, o)
    rc, o = run([CK, "next", "--done", "1,2,3"])
    check("checklist next --done 1,2,3 -> starts at 4", o.strip().startswith("4."), o)
    rc, o = run([CK, "next", "--done", "x"])
    check("checklist next with invalid id -> rc 2", rc == 2, o)
    rc, o = run([CK, "next", "--done", ",".join(str(i) for i in range(1, 39))])
    check("checklist next all done -> tour complete", "Tour complete" in o, o)

    # ---- citations
    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations no failures", rc == 0 and "total failures: 0" in o, o)
        m = re.search(r"Checks: (\d+) positive, (\d+) negative", o)
        check("verify_citations >= 60 positive and >= 15 negative", bool(m) and int(m.group(1)) >= 60 and int(m.group(2)) >= 15, o)

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
