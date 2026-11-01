# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases (CT-02, CT-09, CT-14, CT-18, CT-20 to CT-23,
CT-25, CT-26) against the scripts and checks that the output contains what the sources say.
Usage (from the package root):  python -I tests/run_script_tests.py [--src DIR_WITH_TXT]
With --src (or PyMuPDF and the PDFs in ../../), it also runs verify_citations.py and audit_tokens.py.
Without --src and without sources available, those two are SKIPPED; with an explicit --src they must pass.
Offline. Exit code 0 if all pass.
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
T = os.path.join(ROOT, "tests")


def run(path, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args), capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


CASES = []


def case(cid, desc, script, args, must, rc=0, must_not=()):
    CASES.append((cid, desc, script, args, must, rc, must_not))


case("CT-02", "lookup Hyrum's Law", "eng_lookup.py", ["hyrum law"], ["SWE-G p.15-17", "hash iteration order"])
case("CT-02b", "Hyrum checklist", "hyrum_evaluator.py", ["--factors", "iteration_order", "default_values"],
     ["SWE-G p.16-17", "SWE-G p.183", "No scoring"], must_not=("risk_score", "Risk Score"))
case("CT-09", "70/20/10 is not in the book", "eng_lookup.py", ["pyramid 70/20/10"],
     ["NOT IN THE SOURCE", "80/15/5", "p.156"])
case("CT-09b", "70/20/10 is not in the book (Portuguese query)", "eng_lookup.py", ["piramide 70/20/10"],
     ["NOT IN THE SOURCE", "80/15/5", "p.156"])
case("CT-14", "lookup Tricorder false positives", "eng_lookup.py", ["tricorder false positive"], ["less than 10%", "SWE-G p.289-296"])
case("CT-14b", "1% is not in the book", "eng_lookup.py", ["tricorder 1%"], ["NOT IN THE SOURCE", "10%"])
case("CT-18", "routine: numbers from the 97TH essay", "routine_quality.py", ["--lines", "40", "--params", "5"],
     ["97TH p.150", "not by Code Complete", "Mario Fusco's essay"], must_not=("CC2 p.77",))
case("CT-20", "450-line CL without tests", "review_audit.py", ["--lines", "450", "--no-tests", "--unresolved", "2"],
     ["SWE-G p.129", "p.117", "SWE-G p.131-132", "Ready to commit by the Critique criterion (p.286): NO"],
     must_not=("Scoring", "score"))
case("CT-20b", "small and complete CL", "review_audit.py", ["--lines", "120"],
     ["Ready to commit by the Critique criterion (p.286): YES", "[OK     ] Size"])
case("CT-21", "Hyrum JSON checklist", "hyrum_evaluator.py", ["--json", "--factors", "iteration_order"], ['"factors"', '"law"'])
case("CT-22", "routine with semantic coupling", "routine_quality.py",
     ["--coupling", "semantic-global", "--leaks-secrets", "--fanout", "9"], ["CC2 p.67", "CC2 p.46", "CC2 p.62"])
case("CT-23", "out of scope", "eng_lookup.py", ["kubernetes"], ["NOT COVERED"], rc=1)
case("CT-23b", "out of scope (SOLID)", "eng_lookup.py", ["solid"], ["NOT IN THE SOURCE", "NOT COVERED"], rc=1)
case("CT-25", "citc is not in the book", "eng_lookup.py", ["citc"], ["NOT IN THE SOURCE", "workspaces"], rc=1)
case("CT-26", "cohesion in Code Complete", "eng_lookup.py", ["functional cohesion"], ["NOT IN THE SOURCE", "Chapter 7"])
case("CT-26b", "cohesion in Code Complete (Portuguese query)", "eng_lookup.py", ["coesao funcional"], ["NOT IN THE SOURCE", "Chapter 7"])
case("CT-19", "Boy Scout", "eng_lookup.py", ["boy scout"], ["SWE-G p.56", "Leave It in a Better State"])
case("CT-06", "Goodhart", "eng_lookup.py", ["goodhart"], ["NOT IN THE SOURCE"], rc=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=None)
    a = ap.parse_args()
    fails = 0
    for cid, desc, script, args, must, rc_exp, must_not in CASES:
        rc, out = run(os.path.join(S, script), *args)
        miss = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = rc == rc_exp and not miss and not bad
        print("%s %s - %s" % ("OK   " if ok else "FAIL ", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s); missing=%s; forbidden=%s" % (rc, rc_exp, miss, bad))
            print("   output: " + out[:300].replace("\n", " | "))
    src = ["--src", a.src] if a.src else []
    for name in ("verify_citations.py", "audit_tokens.py"):
        rc, out = run(os.path.join(T, name), *src)
        tail = out.strip().splitlines()[-1] if out.strip() else ""
        no_source = ("PyMuPDF missing", "Source not found", "source missing for")
        if not a.src and rc == 1 and any(m in out for m in no_source):
            print("SKIPPED %s (source unavailable: no PDF/PyMuPDF; use --src)" % name)
            continue
        ok = rc == 0
        print("%s %s - %s" % ("OK   " if ok else "FAIL ", name, tail))
        if not ok:
            fails += 1
    print("Summary: %d script cases, %d failures" % (len(CASES), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
