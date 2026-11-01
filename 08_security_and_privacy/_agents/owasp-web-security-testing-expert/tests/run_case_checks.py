# -*- coding: utf-8 -*-
"""
run_case_checks.py - verifies, for each case in tests/casos.json, whether the PACKAGE (agent + references + scripts) contains what is needed
to answer: (1) the reference exists; (2) each expected page is covered by some citation (WSTG p.N / (p.N-M)) in the file;
(3) the expected terms appear in the reference (the "termos" are literal English terms from the references);
(4) the agent contains the expected phrases/rules; (5) the script (if any) runs and prints the expected output.
This does NOT replace a blind test with a model: it is a deterministic check of the material's coverage and fidelity.

Usage: python -I tests/run_case_checks.py [--md tests/casos-de-teste.md]   (generates the cases markdown with the result)
Exit 0 if all pass.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT = os.path.join(PKG, "agents", "owasp-web-security-testing-expert.md")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower())


def covered_pages(text):
    pages = set()
    for m in re.finditer(r"(?:WSTG\s+p{1,2}\.\s*|\(p{1,2}\.\s*)(\d[\d\s,\-–]*)", text):
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
    cases = json.load(open(os.path.join(PKG, "tests", "casos.json"), encoding="utf-8"))
    agent = norm(open(AGENT, encoding="utf-8").read())
    out = []
    fails = 0
    for c in cases:
        probs = []
        if c.get("ref"):
            rp = os.path.join(PKG, "references", c["ref"])
            if not os.path.exists(rp):
                probs.append(f"missing reference: {c['ref']}")
            else:
                txt = open(rp, encoding="utf-8").read()
                cov = covered_pages(txt)
                pg = c.get("paginas", [])
                exp = set()
                if len(pg) == 2 and pg[1] - pg[0] > 3:
                    exp = set(pg)  # wide range: only the endpoints are required
                else:
                    exp = set(pg)
                    if len(pg) == 2:
                        exp = set(range(pg[0], pg[1] + 1))
                miss = sorted(p for p in exp if p not in cov)
                if miss:
                    probs.append(f"pages not cited in the reference: {miss}")
                nt = norm(txt)
                for t in c.get("termos", []):
                    if norm(t) not in nt:
                        probs.append(f"term missing from the reference: {t}")
        for ph in c.get("agent", []) or []:
            if norm(ph) not in agent:
                probs.append(f"phrase missing from the agent: {ph}")
        if c.get("cmd"):
            p = subprocess.run([sys.executable, "-I", "-X", "utf8"] + c["cmd"], capture_output=True, text=True, encoding="utf-8", cwd=PKG)
            o = p.stdout + p.stderr
            if p.returncode != c.get("exit", 0):
                probs.append(f"exit {p.returncode} != {c.get('exit', 0)}")
            for e in c.get("espera_cmd", []):
                if norm(e) not in norm(o):
                    probs.append(f"script output without '{e}'")
        c["_res"] = "PASS" if not probs else "FAIL"
        c["_probs"] = probs
        fails += bool(probs)
        print(f"{c['id']} {c['tipo']:<15} {c['_res']}" + ("" if not probs else " :: " + "; ".join(probs)))
    print(f"{len(cases) - fails}/{len(cases)} PASS")
    if a.md:
        L = ["# Test cases of owasp-web-security-testing-expert", "",
             f"{len(cases)} cases: conceptual, practical, edge, out of scope and injection. Each case points to what the agent should answer, where the content is and how it was verified. Source: `tests/casos.json`; verification: `python -I tests/run_case_checks.py` (deterministic package coverage) and `python -I tests/run_script_tests.py` (scripts). The case questions are written in English; the `terms` they check are literal English terms from the references.", "",
             f"Result of the last run: **{len(cases) - fails}/{len(cases)} PASS**. It was not a blind run by an independent model (see `relatorio-de-fidelidade.md`).", ""]
        for c in cases:
            L.append(f"## {c['id']} ({c['tipo']}) {c['_res']}")
            L.append(f"- **Question/input:** {c['pergunta']}")
            L.append(f"- **Expected answer:** {c['esperado']}")
            if c.get("ref"):
                L.append(f"- **Where it is:** `references/{c['ref']}` (pages {', '.join(str(x) for x in c.get('paginas', []))})")
            if c.get("cmd"):
                L.append(f"- **Script:** `python -I {' '.join(c['cmd'])}`")
            if c.get("agent"):
                L.append(f"- **In the agent:** {', '.join(c['agent'])}")
            L.append("")
        open(a.md, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
