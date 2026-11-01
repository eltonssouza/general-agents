# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/ai]   # --src enables verify_citations.py
Exit 0 if all pass. The conceptual cases (which need the agent) are in tests/casos-de-teste.md.
The expected numbers come from numeric examples in the MLY itself (pages cited in each test).
"""
import argparse
import json
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL = []
OK = []
L = os.path.join("scripts", "mly_lookup.py")
D = os.path.join("scripts", "mly_diagnose.py")
E = os.path.join("scripts", "mly_errorsheet.py")
C = os.path.join("scripts", "mly_devtest_check.py")
FX = os.path.join("tests", "fixtures")


def run(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:400]))


def has(out, *subs):
    return all(s in out for s in subs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()

    # ---- lookup
    rc, o = run([L, "viés", "evitável"])
    check("lookup (Portuguese input) viés evitável -> p.46,47", rc == 0 and "p.46,47" in o, o)
    rc, o = run([L, "avoidable", "bias"])
    check("lookup avoidable bias -> p.46,47", rc == 0 and "p.46,47" in o, o)
    rc, o = run([L, "transformer"])
    check("lookup transformer -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "kaggle"])
    check("lookup nonexistent term -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "learning", "curve", "--top", "3"])
    check("lookup learning curve does not raise a false gap", "NOT COVERED" not in o and "p.56" in o, o)
    rc, o = run([L, "--page", "76"])
    check("lookup --page 76 -> cap 39", has(o, "cap 39", "beta"), o)
    rc, o = run([L, "--page", "13"])
    check("lookup --page 13 section divider", "section divider" in o, o)
    rc, o = run([L, "--page", "200"])
    check("lookup --page 200 error", rc == 1, o)
    rc, o = run([L, "--chapter", "44"])
    check("lookup --chapter 44 -> p.85-86", has(o, "85-86", "07-depuracao"), o)
    rc, o = run([L, "--chapters"])
    check("lookup --chapters lists 58 chapters", len(re.findall(r"^cap\s+\d+", o, re.M)) == 58, o[-200:])
    rc, o = run([L, "--gaps"])
    check("lookup --gaps lists Transformers and MLOps", has(o, "Transformers", "MLOps"), o)
    rc, o = run([L, "end-to-end", "--json"])
    try:
        j = json.loads(o)
        check("lookup --json valid", len(j["matches"]) >= 1)
    except Exception as ex:
        check("lookup --json valid", False, str(ex))

    # ---- diagnose bv (numeric examples from the book)
    rc, o = run([D, "bv", "--train", "1", "--dev", "11", "--json"])
    j = json.loads(o)
    check("bv 1/11 -> variance 10 (p.44)", j["components"]["variance"] == 10 and j["dominant"] == "variance", o)
    rc, o = run([D, "bv", "--train", "15", "--dev", "16", "--json"])
    j = json.loads(o)
    check("bv 15/16 -> bias 15, variance 1, bias dominant (p.44)", j["components"]["avoidable_bias"] == 15 and j["components"]["variance"] == 1 and j["dominant"] == "avoidable_bias", o)
    rc, o = run([D, "bv", "--train", "15", "--dev", "30", "--json"])
    j = json.loads(o)
    check("bv 15/30 -> bias 15 and variance 15 (p.44)", j["components"]["variance"] == 15 and j["components"]["avoidable_bias"] == 15, o)
    rc, o = run([D, "bv", "--train", "15", "--dev", "30", "--optimal", "14", "--json"])
    j = json.loads(o)
    c = j["components"]
    check("bv 15/30 optimal 14 -> avoidable 1, variance 15 (p.46-47)", c["avoidable_bias"] == 1 and c["variance"] == 15 and c["optimal_error_unavoidable_bias"] == 14 and c["total_bias_(optimal+avoidable)"] == 15, o)
    rc, o = run([D, "bv", "--train", "15", "--dev", "16", "--optimal", "14", "--json"])
    j = json.loads(o)
    check("bv 15/16 optimal 14 -> 1 and 1 (p.47)", j["components"]["avoidable_bias"] == 1 and j["components"]["variance"] == 1, o)
    rc, o = run([D, "bv", "--train", "10", "--dev", "20", "--human", "2"])
    check("bv --human 2, training 10 -> avoidable >= 8 (p.66 uses dev 10 vs human 2)", "8%" in o and "at least" in o, o)
    rc, o = run([D, "bv", "--train", "1", "--dev", "5", "--traindev", "5", "--human", "0", "--json"])
    c = json.loads(o)["components"]
    check("bv 1/5/5 -> variance 4, mismatch 0 (p.79)", c["variance"] == 4 and c["data_mismatch"] == 0, o)
    rc, o = run([D, "bv", "--train", "10", "--dev", "12", "--traindev", "11", "--human", "0", "--json"])
    j = json.loads(o)
    check("bv 10/11/12 -> avoidable bias dominant (p.79)", j["dominant"] == "avoidable_bias" and j["components"]["data_mismatch"] == 1, o)
    rc, o = run([D, "bv", "--train", "10", "--dev", "20", "--traindev", "11", "--human", "0", "--json"])
    c = json.loads(o)["components"]
    check("bv 10/11/20 -> avoidable 10, variance 1, mismatch 9 (p.79-80)", c["avoidable_bias"] == 10 and c["variance"] == 1 and c["data_mismatch"] == 9, o)
    rc, o = run([D, "bv", "--train", "1", "--dev", "10", "--traindev", "1.5", "--human", "0", "--json"])
    c = json.loads(o)["components"]
    check("bv 1/1.5/10 -> mismatch 8.5 (p.77)", abs(c["data_mismatch"] - 8.5) < 1e-9, o)
    rc, o = run([D, "bv", "--train", "1", "--dev", "5", "--optimal", "2"])
    check("bv negative avoidable bias warns of overfitting (p.47 note 8)", has(o, "negative", "p.47"), o)
    rc, o = run([D, "bv", "--train", "10", "--dev", "20", "--optimal", "1", "--human", "2"])
    check("bv --optimal and --human together -> error 2", rc == 2, o)
    rc, o = run([D, "bv", "--train", "10", "--dev", "20", "--tol", "5", "--optimal", "0"])
    check("bv --tol flags above the user threshold as [inference]", has(o, "user threshold", "inference"), o)
    rc, o = run([D, "bv", "--train", "10", "--dev", "20"])
    check("bv without threshold states the book fixes no threshold", "defines no numeric threshold" in o, o)
    rc, o = run([D, "bv", "--train", "10", "--dev", "20", "--optimal", "0"])
    check("bv high avoidable bias does not recommend more data", has(o, "does NOT help: more training data") or "p.51" in o, o)

    # ---- diagnose utilities
    rc, o = run([D, "f1", "--precision", "95", "--recall", "90"])
    check("f1 A = 92.4 (p.21)", "92.4" in o, o)
    rc, o = run([D, "f1", "--precision", "98", "--recall", "85"])
    check("f1 B = 91.0 (p.21)", "91.0" in o, o)
    rc, o = run([D, "weights", "--n-target", "5000", "--n-extra", "200000"])
    check("weights 5,000/200,000 -> 1/40 (p.76)", "1/40" in o and "0.025" in o, o)
    rc, o = run([D, "eyeball", "--error-rate", "5", "--errors", "100"])
    check("eyeball 5% and 100 errors -> ~2000 (p.38)", "2000" in o, o)
    rc, o = run([D, "optverify", "--pairs", "3:1;2:5;4:2;1:1;9:3"])
    j = None
    check("optverify counts search 3 / scoring 2 (p.86)", "3 (60.0%)" in o and "2 (40.0%)" in o, o)
    rc, o = run([D, "optverify", "--pairs", "1:2;1:2;1:2;1:2;5:1", "--json"])
    j = json.loads(o)
    check("optverify 80% scoring / 20% search", j["pct_scoring"] == 80.0 and j["pct_search"] == 20.0, o)
    rc, o = run([D, "optverify", "--pairs", "2:2"])
    check("optverify tie -> scoring function (<=, p.86)", "scoring function" in o.split("Where to focus:")[1], o)

    # ---- errorsheet
    rc, o = run([E, "analyze", os.path.join(FX, "planilha-p32.csv"), "--error-rate", "10", "--json"])
    j = json.loads(o)
    pct = {r["category"]: r["pct"] for r in j["categories"]}
    check("analyze p.32 sheet -> 25/50/50", pct == {"Dog": 25.0, "Big cat": 50.0, "Blurry": 50.0}, o)
    rest = {r["category"]: r["remaining_error_if_eliminated_%"] for r in j["categories"]}
    check("analyze ceiling: 10% and 50% -> 5% (p.31); 25% -> 7.5%", rest["Blurry"] == 5.0 and rest["Dog"] == 7.5, o)
    rc, o = run([E, "mislabeled", "--error", "10", "--mislabeled-pct", "6"])
    check("mislabeled 10% and 6% -> 0.6 and 9.4 (p.34)", has(o, "0.6%", "9.4%"), o)
    rc, o = run([E, "mislabeled", "--error", "2", "--mislabeled-error", "0.6"])
    check("mislabeled 2% and 0.6 -> 30% and 1.4 (p.35)", has(o, "30%", "1.4%"), o)
    rc, o = run([E, "mislabeled", "--error", "2"])
    check("mislabeled without fraction -> error 2", rc == 2, o)
    rc, o = run([E, "attribute", os.path.join(FX, "atribuicao.json"), "--order", "detector,classifier", "--json"])
    j = json.loads(o)
    check("attribute: 3 detector / 1 classifier (p.111)", j["attribution"]["detector"]["count"] == 3 and j["attribution"]["classifier"]["count"] == 1, o)
    rc, o = run([E, "template", "--cats", "a,b", "--rows", "3"])
    check("template CSV with 3 rows", o.strip().splitlines()[0] == "id,a,b,comment" and len(o.strip().splitlines()) == 4, o)

    # ---- devtest
    rc, o = run([C, "check", os.path.join(FX, "config-exemplo.json")])
    check("devtest good example: same distribution OK, no HIGH", "[OK" in o and "[HIGH" not in o, o)
    rc, o = run([C, "check", os.path.join(FX, "config-ruim.json"), "--json"])
    j = json.loads(o)
    highs = [f for f in j if f["severity"] == "high"]
    check("devtest bad config: 4 HIGH findings (p.17-18, 15, 20/22, 26)", len(highs) == 4, o)
    rc, o = run([C, "example"])
    check("devtest example is valid JSON", isinstance(json.loads(o), dict), o)

    # ---- package consistency
    idx = json.load(open(os.path.join(PKG, "scripts", "mly_index.json"), encoding="utf-8"))
    caps = idx["capitulos"]
    check("index has 58 chapters", len(caps) == 58 and [c["cap"] for c in caps] == list(range(1, 59)))
    check("chapters in page order, no overlap", all(caps[i]["pdf_fim"] < caps[i + 1]["pdf_ini"] for i in range(57)))
    check("index reference files exist", all(os.path.exists(os.path.join(PKG, "references", c["ref"])) for c in caps))
    check("topics with pages within 1-118", all(1 <= p <= 118 for t in idx["topicos"] for p in t["paginas"]))

    # ---- citations
    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations without failures", rc == 0, o[-600:])
        print(o.strip().splitlines()[-1])

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
