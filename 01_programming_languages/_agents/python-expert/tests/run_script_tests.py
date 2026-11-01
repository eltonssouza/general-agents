# -*- coding: utf-8 -*-
"""
run_script_tests.py - tests for the python-expert package scripts (stdlib, no network).

Usage (from the package root):  python -I tests/run_script_tests.py
Actually runs the 3 scripts:
  skills/python-code-review/scripts/scan_python_smells.py   (AST linter; rules with an origin)
  skills/python-stdlib-lookup/scripts/stdlib_lookup.py      (lookup by module; NOT COVERED when there is none)
  skills/python-version-features/scripts/tutorial_versions.py (presence in the 3.10-3.14 Tutorials; NOT COVERED)
Exit 0 if all pass, 1 otherwise.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = os.path.join(ROOT, "skills", "python-code-review", "scripts", "scan_python_smells.py")
FIX = os.path.join(ROOT, "skills", "python-code-review", "scripts", "fixtures")
LOOK = os.path.join(ROOT, "skills", "python-stdlib-lookup", "scripts", "stdlib_lookup.py")
TUTV = os.path.join(ROOT, "skills", "python-version-features", "scripts", "tutorial_versions.py")

results = []


def run(script, *args):
    p = subprocess.run([sys.executable, "-I", script, *args], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if (detail and not cond) else ""))


def scan_json(*paths):
    rc, out, err = run(SCAN, "--json", *paths)
    assert rc == 0, err
    return json.loads(out)


# ---------------- scan_python_smells ----------------
d = scan_json(os.path.join(FIX, "sample.py"))
rules = {f["rule"] for f in d["findings"]}
expected = {"mutable-default", "compare-none", "compare-bool", "is-literal", "bare-except", "except-pass",
            "shadowed-except", "finally-flow", "eq-without-hash", "mutate-while-iterating", "eval-exec",
            "pickle-load", "shell-true", "weak-hash"}
check("scan: sample.py triggers the 14 expected rules", expected <= rules, str(sorted(expected - rules)))

lines = {(f["rule"], f["line"]) for f in d["findings"]}
check("scan: ok_append (None default) is NOT reported", not any(r == "mutable-default" and l in (12, 13, 14) for r, l in lines))
check("scan: class with __eq__ and __hash__ is NOT reported", sum(1 for f in d["findings"] if f["rule"] == "eq-without-hash") == 1)
check("scan: 3 shadowed clauses and only the unreachable ones (2 reported)", sum(1 for f in d["findings"] if f["rule"] == "shadowed-except") == 2,
      str([f["line"] for f in d["findings"] if f["rule"] == "shadowed-except"]))

c = scan_json(os.path.join(FIX, "clean.py"))
check("scan: clean.py (includes break/continue of an inner loop and return of a nested function in finally) has 0 findings",
      len(c["findings"]) == 0, str([(f["rule"], f["line"]) for f in c["findings"]]))

p2 = scan_json(os.path.join(FIX, "sample_py2.py"))
r2 = {f["rule"] for f in p2["findings"]}
check("scan: sample_py2.py falls into the Python 2 branch (syntax-error + py2-* rules)",
      {"syntax-error", "py2-print", "py2-raw-input", "py2-xrange", "py2-iter-dict", "py2-except-comma", "py2-module-names"} <= r2,
      str(sorted(r2)))

allf = d["findings"] + p2["findings"]
check("scan: every finding carries an origin (label) and a source", all(f.get("origin") and f.get("source") for f in allf))
check("scan: weak-hash is labeled extrapolation and except-pass inference",
      all(f["origin"] == "extrapolation" for f in allf if f["rule"] == "weak-hash")
      and all(f["origin"] == "inference" for f in allf if f["rule"] == "except-pass"))
ev = [f for f in d["findings"] if f["rule"] == "eval-exec"][0]["message"]
check("scan: eval message cites the real warning of the Notes (p.505) and does not say 'without a warning'", "p.505" in ev and "without a warning" not in ev)

import hashlib
inj = os.path.join(FIX, "injection.py")
h0 = hashlib.sha256(open(inj, "rb").read()).hexdigest()
ji = scan_json(inj)
check("scan: fixture with prompt injection in a docstring/comment is treated as data (1 legitimate finding, file intact)",
      len(ji["findings"]) == 1 and ji["findings"][0]["rule"] == "mutable-default"
      and hashlib.sha256(open(inj, "rb").read()).hexdigest() == h0)

rc, out, err = run(SCAN, "--json")
check("scan: no argument -> usage error (exit 2)", rc == 2)
rc, out, err = run(SCAN, os.path.join(FIX, "clean.py"))
check("scan: text report carries the warning 'no findings is NOT approval'", rc == 0 and "is NOT approval" in out)

# ---------------- stdlib_lookup ----------------
rc, out, err = run(LOOK, "csv")
check("lookup: csv -> Lib p.665-671 with sections and exact page", rc == 0 and "Lib p.665-671" in out and "Reader Objects (p.670)" in out, out[:200])
rc, out, err = run(LOOK, "pathlib")
check("lookup: pathlib -> Lib p.483-509", "Lib p.483-509" in out)
rc, out, err = run(LOOK, "kubernetes")
check("lookup: term outside the index -> NOT COVERED (no invented page)", rc == 0 and "NOT COVERED" in out and "Lib p." not in out.replace("(Lib p.N)", ""))
rc, out, err = run(LOOK, "--list-chapters")
check("lookup: --list-chapters lists 45 chapters", out.count("- ") >= 45 and "Lib p.29-32" in out, str(out.count("- ")))
rc, out, err = run(LOOK, "--json", "json")
ok = False
try:
    ok = any("json" in r["module"].lower() for r in json.loads(out))
except Exception:
    pass
check("lookup: --json returns a list with the json module", ok)
rc, out, err = run(LOOK)
check("lookup: no term -> exit 2", rc == 2)

# ---------------- tutorial_versions ----------------
rc, out, err = run(TUTV, "add_note")
check("tutorial: add_note absent in 3.10 and present from 3.11 (with an inference label)",
      "Tutorial 3.10: absent" in out and "Tutorial 3.11: body" in out and "[inference]" in out, out[:300])
rc, out, err = run(TUTV, "pathlib")
check("tutorial: pathlib absent from the 5 Tutorials (absence does not prove non-existence)", "none of the 5 Tutorials" in out and "does not prove non-existence" in out)
rc, out, err = run(TUTV, "fantasma_xyz")
check("tutorial: term outside the index -> NOT COVERED", "NOT COVERED" in out)
rc, out, err = run(TUTV, "t-string")
check("tutorial: t-string only in Tutorial 3.14 (glossary/license), never in the body", "Tutorial 3.13: absent" in out and "Tutorial 3.14: glossary" in out)
rc, out, err = run(TUTV, "match")
check("tutorial: match already present in 3.10 -> nothing is concluded about earlier versions", "nothing can be concluded" in out)
rc, out, err = run(TUTV, "--list")
check("tutorial: --list lists the curated terms", rc == 0 and "- match" in out and "terms" in out)
rc, out, err = run(TUTV)
check("tutorial: no term -> exit 2", rc == 2)

failed = [n for n, ok, _ in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} tests passed")
sys.exit(1 if failed else 0)
