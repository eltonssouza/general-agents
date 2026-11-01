# -*- coding: utf-8 -*-
"""
run_case_checks.py - verifies the DETERMINISTIC part of the cases in tests/casos.json:
  - "checks": the pages cited by the rubric contain (or do not contain) the expected terms (text extracted from the PDFs);
  - "cmd"/"expect": the package script runs and its output contains the expected substrings.
Evaluating the answers of the agent (fields "esperado", "nao_deve", "rotulos") is manual and is recorded in tests/relatorio-de-fidelidade.md.

Usage: python -I tests/run_case_checks.py --src PATH/scratch/security
Exit 0 if everything passes.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)

spec = importlib.util.spec_from_file_location("vc", os.path.join(HERE, "verify_citations.py"))
vc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    a = ap.parse_args()
    npages = {}
    for k, (fn, n) in vc.SRC.items():
        pg = vc.load_pages(os.path.join(a.src, fn))
        npages[k] = {p: vc.norm(v) for p, v in pg.items()}
    data = json.load(open(os.path.join(HERE, "casos.json"), encoding="utf-8"))
    fails = 0
    n_checks = n_cmds = 0
    cats = {}
    for c in data["casos"]:
        cats[c["categoria"]] = cats.get(c["categoria"], 0) + 1
        ok = True
        for it in c.get("checks", []):
            n_checks += 1
            m = re.match(r"\s*(DZ|TMM)\s+p\.\s*(\S.*)$", it["cite"])
            src = m.group(1)
            plist = vc.expand(m.group(2))
            blob = " ".join(npages[src].get(p, "") for p in plist)
            for t in it.get("contains", []):
                if vc.norm(t) not in blob:
                    ok = False
                    print("FAIL %s: %s does not contain '%s'" % (c["id"], it["cite"], t))
            for t in it.get("absent", []):
                if re.search(r"(?<![a-z0-9])" + re.escape(vc.norm(t)) + r"(?![a-z0-9])", blob):
                    ok = False
                    print("FAIL %s: %s CONTAINS '%s'" % (c["id"], it["cite"], t))
        if c.get("cmd"):
            n_cmds += 1
            p = subprocess.run([sys.executable, "-I"] + c["cmd"], capture_output=True, text=True, encoding="utf-8", cwd=PKG)
            out = p.stdout + p.stderr
            for e in c.get("expect", []):
                if e not in out:
                    ok = False
                    print("FAIL %s: output of %s does not contain '%s'" % (c["id"], " ".join(c["cmd"]), e))
            for bad in c.get("nao_deve", []):
                pass
        print(("PASS " if ok else "FAIL ") + c["id"] + " [" + c["categoria"] + "]")
        if not ok:
            fails += 1
    print("\n%d cases (%s); %d page checks, %d commands; failures: %d" % (len(data["casos"]), ", ".join("%s=%d" % kv for kv in sorted(cats.items())), n_checks, n_cmds, fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
