# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/devops]   # --src enables citation verification
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import tempfile

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL = []
OK = []


def run(args, expect_code=0):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    if a.src:
        a.src = os.path.abspath(a.src)

    L = os.path.join("scripts", "bsrs_lookup.py")
    C = os.path.join("scripts", "design_review_checklist.py")
    T = os.path.join("scripts", "incident_templates.py")
    R = os.path.join("scripts", "risk_matrix.py")

    # --- lookup
    code, o = run([L, "menor privilegio", "--top", "3"])
    check("S01 lookup least privilege (pt query) -> ch.5 p.97-98", "menor-privilegio-e-controle-de-acesso.md" in o and "97-98" in o, o)
    code, o = run([L, "MASVN", "--top", "1"])
    check("S02 lookup MASVN -> ch.9", "design-para-recuperacao.md" in o and "231" in o, o)
    code, o = run([L, "proveniencia binaria", "--top", "1"])
    check("S03 lookup binary provenance (pt query) -> ch.14", "implantacao-de-codigo-cicd-e-supply-chain.md" in o and "350-352" in o, o)
    code, o = run([L, "SBOM"])
    check("S04 lookup SBOM -> NOT COVERED and term absent", "NOT COVERED" in o and "does NOT appear" in o, o)
    code, o = run([L, "STRIDE"])
    check("S05 lookup STRIDE -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "SLO", "error budget"])
    check("S06 lookup SLO -> sre-practices-expert boundary", "sre-practices-expert" in o, o)
    code, o = run([L, "--page", "465"])
    check("S07 --page 465 -> printed 429 Ch.18", "429" in o and "Ch.18" in o, o)
    code, o = run([L, "--printed", "3"])
    check("S08 --printed 3 -> PDF 39", "PDF p.39" in o, o)
    code, o = run([L, "--chapter", "14"])
    check("S09 --chapter 14 lists topics", o.count("BSRS p.") >= 10, o)
    code, o = run([L, "--gaps"])
    check("S10 --gaps lists SLSA and Sigstore", "SLSA" in o and "Sigstore" in o, o)
    code, o = run([L, "quantum computing"])
    check("S11 out-of-scope lookup -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "load shedding", "--json"])
    try:
        j = json.loads(o)
        check("S12 lookup --json valid", j["results"] and j["results"][0]["ref"] == "design-para-resiliencia.md", o)
    except Exception as e:
        check("S12 lookup --json valid", False, str(e))

    # --- index
    with io.open(os.path.join(PKG, "scripts", "bsrs_index.json"), encoding="utf-8") as f:
        idx = json.load(f)
    bad_pages = []
    import re
    for e in idx["entradas"]:
        for tok in re.findall(r"\d+(?:-\d+)?", e["pages"]):
            for n in [int(x) for x in tok.split("-")]:
                if not 1 <= n <= 557:
                    bad_pages.append((e["topic"], n))
        if not os.path.exists(os.path.join(PKG, "references", e["ref"])):
            bad_pages.append((e["topic"], "ref missing " + e["ref"]))
    check("S13 index: pages within 1-557 and references exist", not bad_pages, str(bad_pages[:3]))
    check("S14 index: no term absent from the book became a keyword", not any(any(k.lower() == g.lower() for k in e["keywords"]) for e in idx["entradas"] for g in idx["gaps_globais"]), "")

    # --- checklist
    code, o = run([C, "areas"])
    check("S15 checklist areas: 84 items", "Total: 84" in o, o)
    code, o = run([C, "list", "--area", "pipeline"])
    check("S16 checklist list pipeline: 9 items", o.count("PIP") == 9, o)
    code, o = run([C, "markdown", "--areas", "ir"])
    check("S17 checklist markdown ir contains IR08 and pages", "IR08" in o and "BSRS p.459-471" in o, o)
    with tempfile.TemporaryDirectory() as td:
        ans = os.path.join(td, "a.json")
        with io.open(ans, "w", encoding="utf-8") as f:
            json.dump({"REQ01": "sim", "PRI02": "nao", "RES03": "parcial", "ZZZ": "sim", "REQ02": "talvez"}, f)
        code, o = run([C, "evaluate", ans, "--areas", "requisitos,privilegio,resiliencia"])
        check("S18 evaluate: unknown-id and invalid-value warnings, exit 0", code == 0 and "unknown ids" in o and "invalid value" in o, o)
        code, o = run([C, "evaluate", ans, "--areas", "requisitos,privilegio,resiliencia", "--strict"])
        check("S19 evaluate --strict: exit 1 with 'nao'", code == 1, "code=%s" % code)

    # --- templates
    code, o = run([T, "postmortem", "--incident", "INC-9"])
    check("S20 postmortem: INC-9, ch.18 questions and non-literal notice", "INC-9" in o and "BSRS p.472" in o and "does not include a literal postmortem template" in o, o[:300])
    code, o = run([T, "recovery-checklist"])
    check("S21 recovery-checklist: colors, hands off keyboards and p.465", "hands off keyboards" in o and "RED" in o and "p.465" in o, o[:300])
    code, o = run([T, "agenda", "handover"])
    check("S22 agenda handover: 12 hours", "12 hours" in o and "BSRS p.441" in o, o)
    with tempfile.TemporaryDirectory() as td:
        code, o = run([T, "all", "--out", td])
        check("S23 incident_templates all: 9 files", len(os.listdir(td)) == 9, o)

    # --- risk matrix
    with tempfile.TemporaryDirectory() as td:
        csvp = os.path.join(td, "r.csv")
        with io.open(csvp, "w", encoding="utf-8", newline="") as f:
            f.write("theme,risk,probability,impact,systems\nSecurity,A,highly likely,moderate,x\nEnvironmental,B,unlikely,critical,y\nSecurity,C,,,\nSecurity,D,banana,low,\n")
        code, o = run([R, "rank", csvp])
        lines = [l for l in o.splitlines() if l.startswith("| ") and "Theme" not in l]
        check("S24 risk_matrix: A (0.40) before B (0.20) and outlier flagged", lines and "| A |" in lines[0] and "outlier" in o, o)
        check("S25 risk_matrix: blank line and invalid label produce WARNING", o.count("WARNING") >= 2, o)
    code, o = run([R, "scales"])
    check("S26 risk_matrix scales: appendix scales", "0.8" in o and "BSRS p.536" in o, o)

    # --- references
    refs = sorted(os.listdir(os.path.join(PKG, "references")))
    idxmd = io.open(os.path.join(PKG, "references", "INDEX.md"), encoding="utf-8").read() if "INDEX.md" in refs else ""
    missing = [r for r in refs if r != "INDEX.md" and r not in idxmd]
    check("S27 INDEX.md lists all references", "INDEX.md" in refs and not missing, str(missing))

    # --- citations
    if a.src:
        code, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("S28 verify_citations: 0 failures", code == 0 and "total failures: 0" in o, o[-400:])
        m = re.search(r"Checks: (\d+) positive, (\d+) negative", o)
        if m:
            check("S29 >= 60 positive and >= 15 negative", int(m.group(1)) >= 60 and int(m.group(2)) >= 15, m.group(0))
    print("\nSummary: %d passed, %d failed" % (len(OK), len(FAIL)))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
