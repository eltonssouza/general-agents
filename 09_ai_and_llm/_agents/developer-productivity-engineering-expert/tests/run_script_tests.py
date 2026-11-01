# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic test cases for the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/ai]   # --src enables citation verification
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
The expected calculation values come from the book's own numeric examples (DPE p.29, 74, 78-84).
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

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL, OK = [], []


def run(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:400]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join("scripts", "dpe_lookup.py")
    C = os.path.join("scripts", "dpe_cost.py")
    K = os.path.join("scripts", "dpe_checklist.py")

    # ---- lookup
    c, o = run([L, "build cache", "--top", "1"])
    check("L01 build cache -> 03 p.34-39", "03-build-cache.md" in o and "34-39" in o, o)
    c, o = run([L, "flaky", "--top", "1"])
    check("L02 flaky -> 07 p.73-74", "07-confiabilidade-e-flaky.md" in o and "73-74" in o, o)
    c, o = run([L, "MABP", "--top", "1"])
    check("L03 MABP -> 05 p.51", "05-profiling-e-analytics.md" in o and "51-52" in o, o)
    c, o = run([L, "Data Platform Engineering"])
    check("L04 Data Platform Engineering -> NOT COVERED + discrepancy", "NOT COVERED" in o and "Data-Platform" in o, o)
    c, o = run([L, "Kubernetes"])
    check("L05 Kubernetes -> NOT COVERED", "NOT COVERED" in o, o)
    c, o = run([L, "DORA"])
    check("L06 DORA -> NOT COVERED", "NOT COVERED" in o, o)
    c, o = run([L, "Develocity"])
    check("L07 Develocity -> NOT COVERED", "NOT COVERED" in o, o)
    c, o = run([L, "xyzzy"])
    check("L08 unknown term -> NOT COVERED", "NOT COVERED" in o, o)
    c, o = run([L, "--page", "74"])
    check("L09 --page 74 -> printed 69, Ch.14", "printed 69" in o and "Ch.14" in o, o)
    c, o = run([L, "--printed", "69"])
    check("L10 --printed 69 -> PDF p.74", "PDF p.74" in o, o)
    c, o = run([L, "--page", "4"])
    check("L11 --page 4 -> no printed number", "no printed number" in o, o)
    c, o = run([L, "--chapters"])
    check("L12 --chapters lists 18 entries", o.count("Ch.") == 18, o)
    c, o = run([L, "--gaps"])
    check("L13 --gaps mentions DORA and data platform", "DORA" in o and "Data Platform" in o, o)
    c, o = run([L, "--datado"])
    check("L14 --datado mentions Gradle Enterprise", "Gradle Enterprise" in o, o)
    c, o = run([L, "--page", "200"])
    check("L15 page outside the PDF", "outside the PDF" in o, o)
    c, o = run([L, "cache de build", "--top", "1"])
    check("L16 Portuguese keyword still resolves (cache de build -> 03 p.34-39)", "03-build-cache.md" in o and "34-39" in o, o)
    c, o = run([L, "plataforma de dados"])
    check("L17 Portuguese gap term -> NOT COVERED", "NOT COVERED" in o, o)

    # ---- calculation (book values)
    c, o = run([C, "engineer-year"])
    check("C01 CE = 110.400 (p.78)", "110.400" in o, o)
    c, o = run([C, "wait", "--kind", "local", "--builds-year", "500000", "--wait-frac", "0.8", "--cm", "1"])
    check("C02 local waiting = 400.000 (p.79)", "400.000" in o, o)
    c, o = run([C, "wait", "--kind", "ci", "--builds-year", "500000", "--wait-frac", "0.2", "--cm", "1"])
    check("C03 CI waiting = 100.000 (p.80)", "100.000" in o and "p.80" in o, o)
    c, o = run([C, "debug", "--builds-year", "500000", "--fail", "0.2", "--invest", "0.05", "--minutes", "20", "--cm", "1"])
    check("C04 local debugging = 100.000 (p.81)", "100.000" in o, o)
    c, o = run([C, "debug", "--builds-year", "500000", "--fail", "0.1", "--invest", "0.2", "--minutes", "60", "--cm", "1"])
    check("C05 CI debugging = 600.000 (p.81)", "600.000" in o, o)
    c, o = run([C, "faulty", "--builds-year", "500000", "--fail", "0.002", "--invest", "1", "--minutes", "240", "--cm", "1"])
    check("C06 local faulty logic = 240.000 (p.83)", "240.000" in o, o)
    c, o = run([C, "example"])
    check("C07 example total = 3.200.000 (p.84)", "TOTAL = US$ 3.200.000" in o and "WARNING" in o, o)
    c, o = run([C, "example", "--faulty-ci-min", "90"])
    check("C08 example with TCI=90 -> 3.185.000 and flags the inconsistency", "3.185.000" in o and "Inconsistency" in o, o)
    c, o = run([C, "team-time", "--builds-week", "1010", "--before", "1", "--after", "0.6"])
    check("C09 Team 2 = ~44 days (p.29)", re.search(r"= 43\.8|= 44", o) is not None, o)
    c, o = run([C, "team-time", "--builds-week", "12000", "--before", "9", "--after", "5", "--devs", "100"])
    check("C10 Team 3 = 5200 days (p.29)", "5200.0" in o, o)
    c, o = run([C, "flaky", "--tests", "200", "--builds-day", "500"])
    check("C11 flaky without retry ~0.005% (p.74)", "0.0050%" in o, o)
    c, o = run([C, "flaky", "--tests", "200", "--builds-day", "500", "--retries", "1"])
    check("C12 flaky 1 retry ~0.7% (p.74) labeled inference", "0.7089%" in o and "[inference]" in o, o)
    c, o = run([C, "flaky", "--tests", "200", "--builds-day", "500", "--rate", "0.00005"])
    check("C13 flaky rate 0.005%/test: failure 0.995% and target OK", "OK" in o and "0.9950%" in o, o)
    c, o = run([C, "feedback", "--build-min", "10", "--fail-rate", "0.2", "--debug-min", "20", "--builds", "100"])
    check("C14 feedback 32 min and 40 switches (p.30)", "32.00" in o and "40.0" in o, o)
    c, o = run([C, "savings", "--cost-per-min", "1", "--builds-year", "500000", "--build-min", "3", "--reduction-pct", "50"])
    check("C15 savings with percentage labeled [extrapolation]", "[extrapolation]" in o and "750.000" in o, o)
    c, o = run([C, "savings", "--cost-per-min", "1", "--builds-year", "500000", "--minutes-saved", "5", "--engineer-year-cost", "110400"])
    check("C16 5 min saved = 2.500.000 / ~22.6 eng (without W; the book uses W: 18 eng, p.79)", "2.500.000" in o, o)
    c, o = run([C, "--json", "example"])
    try:
        j = json.loads(o)
        check("C17 --json valid, total 3.2M", abs(j["result"]["total"] - 3200000) < 1, o)
    except Exception as e:  # noqa
        check("C17 --json valid", False, str(e) + o)
    c, o = run([C, "wait", "--builds-year", "1"])
    check("C18 missing arguments -> error (exit != 0)", c != 0, o)

    # ---- checklist
    c, o = run([K, "areas"])
    check("K01 areas: 9 areas and 50 items", "Total: 50 items" in o and o.count("items)") == 9, o)
    c, o = run([K, "list", "--area", "FK"])
    check("K02 list FK has 8 items with pages", o.count("FK-") == 8 and "DPE p.74" in o, o)
    c, o = run([K, "markdown", "--area", "CA"])
    check("K03 markdown CA with [inference]", "[inference]" in o and "CA-01" in o, o)
    fx = os.path.join("tests", "fixtures", "respostas-exemplo.json")
    c, o = run([K, "evaluate", fx])
    check("K04 evaluate: ORG 75%, FK 0%, unknown ignored, na excluded (Portuguese answer values still accepted)",
          "ORG Organization and culture: 1.5/2 = 75%" in o and "FK Flaky tests: 0.0/1 = 0%" in o and "XX-1" in o and "CA " not in o, o)
    check("K05 evaluate labels bands as extrapolation", "[extrapolation]" in o and "the book defines no levels" in o, o)
    #
    ids_all = json.load(open(os.path.join(PKG, "scripts", "dpe_checklist_items.json"), encoding="utf-8"))["items"]
    check("K06 every checklist item has a page", all(i["pages"] for i in ids_all), "")

    # ---- index
    idx = json.load(open(os.path.join(PKG, "scripts", "dpe_index.json"), encoding="utf-8"))
    refs = os.listdir(os.path.join(PKG, "references"))
    check("I01 all index references exist", all(t["ref"] in refs for t in idx["topics"]) and all(ch["ref"] in refs for ch in idx["chapters"]), "")
    cover = set()
    for ch in idx["chapters"]:
        cover.update(range(ch["pdf"][0], ch["pdf"][1] + 1))
    check("I02 chapters cover PDF 8-91 except p.13,27,59,77 (dividers) and 92+", all(p in cover for p in range(8, 92) if p not in (13, 27, 59, 77)), "")

    # ---- encoding
    bad = []
    for root, _, files in os.walk(PKG):
        for fn in files:
            if fn.endswith((".md", ".json", ".py")):
                raw = open(os.path.join(root, fn), "rb").read()
                try:
                    raw.decode("utf-8")
                except UnicodeDecodeError:
                    bad.append(fn)
                if raw.startswith(b"\xef\xbb\xbf"):
                    bad.append(fn + "(BOM)")
    check("E01 all files are UTF-8 without BOM", not bad, str(bad))

    # ---- citations
    if a.src:
        c, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("V01 verify_citations: 0 failures", c == 0 and "total failures: 0" in o, o)

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
