# -*- coding: utf-8 -*-
"""
run_cases.py - runs the cases in tests/casos.json: (a) checks that the pages cited in the expected answer
contain the given terms (fidelity to the extracted text) and (b) runs the package scripts and checks the output.
Read-only, no network. Cases without a script/pages are for manual evaluation of the agent's behavior.

Usage (from the package folder):  python -I tests/run_cases.py --src CAMINHO/scratch/devops
"""
import argparse
import json
import os
import re
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s.lower()).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    txt = open(os.path.join(a.src, "Linux-Introduction-to-Linux-TLDP.txt"), encoding="utf-8").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    pages = {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}
    cases = json.load(open(os.path.join(a.pkg, "tests", "casos.json"), encoding="utf-8"))["casos"]
    fails = 0
    manual = 0
    for c in cases:
        res = []
        ok = True
        if c.get("paginas"):
            body = " ".join(pages.get(p, "") for p in c["paginas"])
            miss = [t for t in c.get("termos_na_pagina", []) if norm(t) not in body]
            if miss:
                ok = False
                res.append(f"pages {c['paginas']} missing terms {miss}")
            bad = [t for t in c.get("ausentes_na_pagina", []) if norm(t) in body]
            if bad:
                ok = False
                res.append(f"pages {c['paginas']} CONTAIN terms that should be absent {bad}")
        sc = c.get("script")
        if sc:
            r = subprocess.run([sys.executable, "-I"] + sc["args"], input=sc.get("stdin"), capture_output=True,
                               text=True, encoding="utf-8", cwd=a.pkg, env=dict(os.environ, MSYS_NO_PATHCONV="1"))
            out = (r.stdout or "") + (r.stderr or "")
            want = sc.get("exit", 0)
            if r.returncode != want:
                ok = False
                res.append(f"exit {r.returncode} (expected {want})")
            for s in sc.get("espera", []):
                if s not in out:
                    ok = False
                    res.append(f"output missing '{s}'")
            for s in sc.get("espera_ausente", []):
                if s in out:
                    ok = False
                    res.append(f"output contains '{s}'")
        if not c.get("paginas") and not sc:
            manual += 1
            print(f"MANUAL {c['id']} [{c['tipo']}] {c['pergunta'][:70]}")
            continue
        if not ok:
            fails += 1
        print(f"{'PASS' if ok else 'FAIL'}   {c['id']} [{c['tipo']}] {c['pergunta'][:70]}" + ("" if ok else " :: " + "; ".join(res)))
    total = len(cases)
    print(f"\n{total} cases: {total - fails - manual} automatic OK, {fails} failures, {manual} for manual evaluation")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
