# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/security]   # --src enables citation verification
Exit 0 if all pass. The conceptual cases (which need the agent) are in tests/casos-de-teste.md.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL = []
OK = []


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
    if a.src:
        a.src = os.path.abspath(a.src)

    L = os.path.join("scripts", "infosec_lookup.py")
    T = os.path.join("scripts", "threat_model_session.py")
    C = os.path.join("scripts", "strategy_checklist.py")
    R = os.path.join("scripts", "risk_matrix.py")
    FX = os.path.join("tests", "fixtures")

    # --- lookup
    c, o = run([L, "quatro perguntas", "--top", "2"])
    check("S01 lookup quatro perguntas (pt) -> TMM p.1", "TMM p.1" in o and "tmm-manifesto.md" in o, o)
    c, o = run([L, "apetite de risco", "--top", "1"])
    check("S02 lookup apetite de risco (pt) -> DZ p.33-34", "DZ p.33-34" in o and "risco-e-governanca.md" in o, o)
    c, o = run([L, "STRIDE"])
    check("S03 lookup STRIDE -> NOT COVERED + absent term", "NOT COVERED" in o and "does NOT appear" in o, o)
    c, o = run([L, "ASVS"])
    check("S04 lookup ASVS -> boundary owasp-asvs-code-review-expert", "owasp-asvs-code-review-expert" in o, o)
    c, o = run([L, "lgpd"])
    check("S05 lookup LGPD -> NOT COVERED and privacy-lgpd-engineering-expert", "NOT COVERED" in o and "privacy-lgpd-engineering-expert" in o, o)
    c, o = run([L, "--page", "33"])
    check("S06 --page 33 -> printed 16 Ch.1", "printed page 16" in o and "Ch.1" in o, o)
    c, o = run([L, "--printed", "16"])
    check("S07 --printed 16 -> PDF 33", "PDF p.33" in o, o)
    c, o = run([L, "--gaps"])
    check("S08 --gaps lista STRIDE, DFD, SBOM", all(t in o for t in ("STRIDE", "DFD", "SBOM")), o)
    c, o = run([L, "--tmm"])
    check("S09 --tmm lista 9 topicos do manifesto", o.count("TMM p.") >= 8, o)
    c, o = run([L, "--chapters"])
    check("S10 --chapters shows 8 chapters and TMM", o.count("DZ Ch.") == 8 and "TMM p.1-3" in o, o)
    c, o = run([L, "threat modeling no dz"])
    check("S11 lookup threat modeling no DZ -> ponte", "modelagem-de-ameacas-no-dz-e-ponte-com-tmm.md" in o, o)
    c, o = run([L, "zero trust", "--source", "DZ", "--top", "1"])
    check("S12 lookup zero trust -> DZ p.104-105", "DZ p.104-105" in o, o)

    # --- threat modeling session
    c, o = run([T, "questions"])
    check("S13 questions traz as 4 perguntas com TMM p.1", all(x in o for x in ("What are we working on?", "What can go wrong?", "What are we going to do about it?", "Did we do a good enough job?")) and "TMM p.1" in o, o)
    c, o = run([T, "template", "--system", "API X"])
    check("S14 template without extrapolation does NOT cite STRIDE/DFD", "STRIDE" not in o and "data flow diagram" not in o and "API X" in o and "TMM p.1, question 4" in o, o)
    c, o = run([T, "template", "--extrapolation", "--dz-bridge"])
    check("S15 template --extrapolation labels [extrapolation] and --dz-bridge cites DZ p.34", "[extrapolation]" in o and "STRIDE" in o and "DZ p.34" in o, o)
    c, o = run([T, "agenda", "--minutes", "60"])
    check("S16 agenda 60 min sums to 60", "Total allocated: 60" in o, o)
    for mm in ("15", "37", "90"):
        c, o = run([T, "agenda", "--minutes", mm])
        check("S16b agenda %s min exact sum" % mm, "Total allocated: %s min" % mm in o, o)
    c, o = run([T, "agenda", "--minutes", "5"])
    check("S17 agenda 5 min -> error exit 2", c == 2, o)
    c, o = run([T, "evaluate", os.path.join(FX, "sessao-exemplo.json")])
    check("S18 evaluate session: adherence 68% and gap AP4", "68%" in o and "AP4" in o and "PT3" in o, o)
    c, o = run([T, "evaluate", os.path.join(FX, "ids-invalidos.json")])
    check("S19 evaluate invalid ids -> exit 2", c == 2 and "Unknown IDs" in o, o)
    c, o = run([T, "antipatterns"])
    check("S20 antipatterns lists the 4 anti-patterns", all(x in o for x in ("Hero Threat Modeler", "Admiration for the Problem", "Tendency to Overfocus", "Perfect Representation")), o)

    # --- strategy checklist
    c, o = run([C, "areas"])
    check("S21 areas: 11 areas and 108 items", "Total: 108 items" in o and o.count("items)") == 11, o)
    c, o = run([C, "list", "--area", "IR"])
    check("S22 list IR contains R03 with DZ p.62", "R03" in o and "DZ p.62" in o, o)
    c, o = run([C, "list", "--area", "ZZ"])
    check("S23 invalid area -> exit 2", c == 2, o)
    c, o = run([C, "evaluate", os.path.join(FX, "estrategia-exemplo.json")])
    check("S24 evaluate strategy: gaps G02, I03, R03", all(x in o for x in ("G02", "I03", "R03")) and "Gaps (5)" in o, o)
    c, o = run([C, "markdown", "--area", "GOV"])
    check("S25 markdown GOV has 12 checkboxes", o.count("- [ ] ") == 12, o)

    # --- risk matrix
    c, o = run([R, "scales"])
    check("S26 scales: impact 5 catastrophic and likelihood 1", "Catastrophic" in o and "Improbable" in o, o)
    c, o = run([R, "matrix"])
    check("S27 matrix: 25 on the diagonal and 1x1 row", "25*" in o and "   1       1" in o, o)
    c, o = run([R, "rank", os.path.join(FX, "riscos-exemplo.csv")])
    first = [l for l in o.splitlines() if l.startswith("R")]
    check("S28 rank: R1 (25) first and 3 of 4 above the appetite", first and first[0].startswith("R1") and "3 of 4 risks above" in o, o)
    c, o = run([R, "rank", os.path.join(FX, "riscos-exemplo.csv"), "--appetite", "12"])
    check("S29 rank appetite 12: 1 of 4 above", "1 of 4 risks above" in o, o)
    c, o = run([R, "rank", os.path.join(FX, "riscos-invalido.csv")])
    check("S30 rank with impact 6 -> exit 2", c == 2 and "outside 1-5" in o, o)
    c, o = run([R, "rank", os.path.join(FX, "riscos-exemplo-en.csv")])
    first = [l for l in o.splitlines() if l.startswith("R")]
    check("S30b rank with English headers/treatments: R1 (25) first and 3 of 4 above", first and first[0].startswith("R1") and "3 of 4 risks above" in o, o)

    # --- citations
    if a.src:
        c, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("S31 verify_citations passes (range, positive, negative)", c == 0, o)
    else:
        print("SKIP S31 verify_citations (use --src)")

    print("\nTotal: %d PASS, %d FAIL" % (len(OK), len(FAIL)))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
