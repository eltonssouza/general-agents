# -*- coding: utf-8 -*-
"""
run_case_checks.py - checks, for each case in tests/casos.json, whether the PACKAGE (agent + references + scripts) contains what is needed
to answer: (1) the reference exists; (2) each expected page is covered by some 'BSRS p.N[-M]' citation in the file;
(3) the expected terms appear in the reference (the references keep the Portuguese text of the source edition, so the case terms are Portuguese);
(4) the agent contains the expected phrases/rules; (5) the script (if any) runs and prints the expected output.
This does NOT replace a blind test with a model: it is a deterministic check of coverage and fidelity of the material.

Usage: python -I tests/run_case_checks.py [--md tests/casos-de-teste.md]   (generates the cases markdown with the result)
Exit 0 if all pass.
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
import unicodedata

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower())


def covered_pages(text):
    pages = set()
    for m in re.finditer(r"BSRS\s+p{1,2}\.\s*(\d[\d\s,\-–]*)", text):
        for tok in re.split(r"\s*,\s*", m.group(1).strip()):
            mm = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
            if mm:
                a = int(mm.group(1))
                b = int(mm.group(2) or a)
                pages.update(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md")
    a = ap.parse_args()
    cases = json.load(io.open(os.path.join(PKG, "tests", "casos.json"), encoding="utf-8"))
    agent = io.open(os.path.join(PKG, "agents", "secure-reliable-systems-expert.md"), encoding="utf-8").read()
    agentn = norm(agent)
    results = []
    fails = 0
    for c in cases:
        probs = []
        refp = os.path.join(PKG, "references", c["ref"])
        if not os.path.exists(refp):
            probs.append("reference missing: " + c["ref"])
            text = ""
        else:
            text = io.open(refp, encoding="utf-8").read()
        cov = covered_pages(text)
        miss = [p for p in c["paginas"] if p not in cov]
        if miss:
            probs.append("pages not covered by a citation in the reference: %s" % miss)
        tn = norm(text)
        for t in c["termos"]:
            alts = [norm(x) for x in t.split("|")]
            if not any(x in tn for x in alts):
                probs.append("term missing from the reference: " + t)
        for t in c.get("agent", []):
            if norm(t) not in agentn:
                probs.append("agent does not contain: " + t)
        if c.get("script"):
            p = subprocess.run([sys.executable, "-I"] + c["script"], capture_output=True, text=True, encoding="utf-8", cwd=PKG)
            out = p.stdout + p.stderr
            if p.returncode != 0:
                probs.append("script returned %d" % p.returncode)
            for t in c.get("script_contem", []):
                if norm(t) not in norm(out):
                    probs.append("script output does not contain: " + t)
        status = "PASS" if not probs else "FAIL"
        if probs:
            fails += 1
        results.append((c, status, probs))
        print("%s %s %s %s" % (status, c["id"], c["tipo"], ("; ".join(probs) if probs else "")))
    print("\nSummary: %d cases, %d passed, %d failed" % (len(cases), len(cases) - fails, fails))
    if a.md:
        L = ["# Test cases for secure-reliable-systems-expert", "",
             "%d cases: conceptual, practical, edge, out-of-scope and injection. Each case points to what the agent should answer, where the content is (reference and pages) and how it was verified. Case source: `tests/casos.json`; verification: `python -I tests/run_case_checks.py` (deterministic package coverage) and `python -I tests/run_script_tests.py` (scripts).".replace("%d", str(len(cases))),
             "", "Result of the last run: **%d/%d PASS**. This was not a blind run by an independent model (see `relatorio-de-fidelidade.md`)." % (len(cases) - fails, len(cases)), ""]
        for c, st, pr in results:
            L.append("## %s (%s) %s" % (c["id"], c["tipo"], st))
            L.append("- **Question/input:** %s" % c["pergunta"])
            L.append("- **Expected answer:** %s" % c["esperado"])
            L.append("- **Where it is:** `references/%s`%s" % (c["ref"], (" (pages %s)" % ", ".join(str(p) for p in c["paginas"])) if c["paginas"] else ""))
            if c.get("script"):
                L.append("- **Script:** `python -I %s`" % " ".join(c["script"]))
            if pr:
                L.append("- **Problems:** " + "; ".join(pr))
            L.append("")
        io.open(a.md, "w", encoding="utf-8", newline="\n").write("\n".join(L))
        print("written " + a.md)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
