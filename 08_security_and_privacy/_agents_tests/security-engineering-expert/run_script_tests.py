# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/security]   # --src enables the citation verification
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
"""
import argparse
import io
import json
import os
import re
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


def ranges(spec):
    out = []
    for tok in spec.split(","):
        m = re.fullmatch(r"\s*(\d+)(?:-(\d+))?\s*", tok)
        if m:
            a = int(m.group(1))
            out.append((a, int(m.group(2) or a)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join("scripts", "se3_lookup.py")
    C = os.path.join("scripts", "se3_calc.py")
    K = os.path.join("scripts", "se3_checklist.py")

    # ---- lookup
    code, o = run([L, "clark-wilson", "--top", "1"])
    check("L01 clark-wilson -> cap.12 p.447-452", "11-bancos-e-controles-internos.md" in o and "447-452" in o, o)
    code, o = run([L, "birthday", "--top", "2"])
    check("L02 birthday -> cripto p.203-206", "04-criptografia.md" in o and "203-206" in o, o)
    code, o = run([L, "SBOM"])
    check("L03 SBOM -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "WebAuthn"])
    check("L04 WebAuthn -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "terraform"])
    check("L05 off-topic term -> NOT COVERED", "NOT COVERED" in o, o)
    code, o = run([L, "--page", "700"])
    check("L06 --page 700 -> Ch.19, printed 664", "Ch.19" in o and "664" in o, o)
    code, o = run([L, "--page", "720"])
    check("L07 --page 720 -> page NOT READ", "NOT READ" in o, o)
    code, o = run([L, "--printed", "300"])
    check("L08 --printed 300 -> PDF p.344", "PDF p.344" in o, o)
    code, o = run([L, "--chapters"])
    check("L09 --chapters lists 29 chapters", o.count("Ch.") >= 29, o)
    code, o = run([L, "--chapter", "27"])
    check("L10 --chapter 27 lists topics", o.count("SE3 p.") >= 5, o)
    code, o = run([L, "--gaps"])
    check("L11 --gaps lists gaps and unread ranges", "SBOM" in o and "NOT READ" in o and "734-747" in o, o)
    code, o = run([L, "taxa-base", "--json"])
    try:
        j = json.loads(o)
        check("L12 valid --json", j["resultados"] and j["resultados"][0]["ref"].startswith("09-"), o)
    except Exception as e:
        check("L12 valid --json", False, str(e))
    code, o = run([L, "--datado"])
    check("L13 --datado lists blocks", "DATADO" in o or "DATED" in o, o)
    code, o = run([L, "STRIDE"])
    check("L14 STRIDE -> gap with the book's note (p.1006)", "NOT COVERED" in o and "1006" in o, o)
    code, o = run([L, "Spectre", "--top", "1"])
    check("L15 Spectre -> access control/vulnerabilities p.277-284", "05-controle-de-acesso.md" in o and "277-284" in o, o)

    code, o = run([L, "access control", "--top", "1"])
    check("L16 English query -> access control reference", "05-controle-de-acesso.md" in o, o)
    code, o = run([L, "controle de acesso", "--top", "1"])
    check("L17 Portuguese query still recognized", "05-controle-de-acesso.md" in o, o)

    # ---- index: integrity
    with io.open(os.path.join(PKG, "scripts", "se3_index.json"), encoding="utf-8") as f:
        idx = json.load(f)
    caps = {c["cap"]: c for c in idx["capitulos"]}
    bad = []
    for e in idx["entradas"]:
        c = caps[e["cap"]]
        for lo, hi in ranges(e["paginas"]):
            for p in range(lo, hi + 1):
                if not any(x <= p <= y for x, y in c["lido"]):
                    bad.append((e["topico"][:40], p, e["cap"]))
        if not os.path.exists(os.path.join(PKG, "references", e["ref"])):
            bad.append((e["topico"][:40], "ref ausente", e["ref"]))
    check("I01 all index pages are in READ ranges of the chapter and the references exist", not bad, str(bad[:6]))
    check("I02 29 chapters and decreasing offsets from 48 to 31", len(idx["capitulos"]) == 29 and idx["capitulos"][0]["offset"] == 48 and idx["capitulos"][-1]["offset"] == 31, "")
    prev = 99
    mono = True
    for c in idx["capitulos"]:
        if c["offset"] > prev:
            mono = False
        prev = c["offset"]
    check("I03 offsets do not grow along the book", mono, "")

    # ---- calc
    code, o = run([C, "biometric-birthday", "--far", "1e-6"])
    check("C01 biometric-birthday: 1,177 people, 692,076 pairs, ~0.50", "1,177 people" in o and "692,076" in o and "0.500" in o, o)
    code, o = run([C, "bayes-alarm"])
    check("C02 bayes-alarm: ratio 100 and ~0.99%", "ratio false:real = 100.0" in o and "0.99%" in o, o)
    code, o = run([C, "ale", "--sample"])
    check("C03 ale --sample flags the inconsistent row (50,000 vs 100,000)", "DIVERGES" in o and "50,000" in o and "inconsistency in the book itself" in o, o)
    code, o = run([C, "dod-password", "--length", "8", "--alphabet", "96", "--lifetime", "31536000", "--rate", "100"])
    check("C04 dod-password: 96^8 ~ 2^52,7", "2^52.7" in o and "p.157" in o, o)
    code, o = run([C, "entropy", "--words", "6", "--wordlist", "7776"])
    check("C05 entropy: 77.5 bits (book: ~77)", "77.5 bits" in o and "p.147" in o, o)
    code, o = run([C, "birthday", "--space", "365"])
    check("C06 birthday N=365 -> ~22.5 samples", "22.49" in o, o)
    code, o = run([C, "byzantine", "--traitors", "2"])
    check("C07 byzantine t=2 -> n>=7", "minimum n = 7" in o, o)
    code, o = run([C, "amdahl", "--parallel", "0.75", "--cores", "8"])
    check("C08 amdahl 3/4 and 8 cores -> 2.909", "2.909" in o, o)
    code, o = run([C, "bug-race"])
    check("C09 bug-race: 10 vs 100,000 and 9.52%", "9.52%" in o and "100,000" in o, o)
    code, o = run([C, "reliability", "--hours", "1000000", "--k", "1"])
    check("C10 reliability: MTBF = t/k", "MTBF ~ t/k = 1e+06" in o, o)
    code, o = run([C, "risk-register", "--item", "b:2:2", "--item", "a:5:4:4:4"])
    check("C11 risk-register sorts and shows mitigation 20 -> 16", o.index("1. a") < o.index("2. b") and "after mitigation 16" in o, o)
    code, o = run([C, "laplace-scale", "--epsilon", "2", "--sensitivity", "1"])
    check("C12 laplace-scale labelled [extrapolation]", "[extrapolation]" in o and "b = sensitivity/epsilon = 1/2 = 0.5" in o, o)
    code, o = run([C, "hash-collision", "--bits", "128"])
    check("C13 hash-collision 128 bits -> 2^64", "2^64" in o, o)
    code, o = run([C, "bits", "--bits", "80", "--rate", "1e9"])
    check("C14 bits: cites p.202", "p.202" in o, o)
    code, o = run([C, "biometric-birthday", "--far", "2"])
    check("C15 invalid input -> exit 2", code == 2, o)
    code, o = run([C, "hawk-dove", "--value", "2", "--cost", "5", "--json"])
    try:
        j = json.loads(o)
        check("C16 valid --json (hawk-dove p=0.4)", abs(j["valores"]["p"] - 0.4) < 1e-9, o)
    except Exception as e:
        check("C16 valid --json (hawk-dove p=0.4)", False, str(e))
    code, o = run([C, "ale", "--item", "x:100:2:150"])
    check("C17 ale detects divergence from the reported ALE", "DIVERGES" in o and "200" in o, o)

    # ---- checklist
    code, o = run([K, "areas"])
    check("K01 areas: 14 areas", len([l for l in o.splitlines() if " items " in l]) == 14, o)
    code, o = run([K, "list", "--area", "selos"])
    check("K02 list selos has >=5 items with page", o.count("[SE3 p.") >= 5, o)
    code, o = run([K, "markdown", "--area", "protocolos"])
    check("K03 markdown has checkboxes", "- [ ] PRO01" in o, o)
    code, o = run([K, "evaluate", os.path.join("tests", "fixtures", "respostas-exemplo.json")])
    check("K04 evaluate lists NO and PARTIAL", "[NO] OPO02" in o and "[PARTIAL] SEN01" in o, o)
    code, o = run([K, "list", "--area", "inexistente"])
    check("K05 invalid area -> exit 2", code == 2, o)
    with io.open(os.path.join(PKG, "scripts", "se3_checklist_items.json"), encoding="utf-8") as f:
        cl = json.load(f)
    ids = [i["id"] for i in cl["itens"]]
    check("K06 unique ids and >=100 items", len(ids) == len(set(ids)) and len(ids) >= 100, str(len(ids)))
    code, o = run([K, "list", "--area", "seals"])
    check("K07 English area alias (seals) accepted", o.count("[SE3 p.") >= 5, o)
    pt = os.path.join(tempfile.gettempdir(), "se3_respostas_pt.json")
    with io.open(pt, "w", encoding="utf-8") as f:
        json.dump({"OPO01": "sim", "OPO02": "nao", "SEN01": "parcial"}, f)
    code, o = run([K, "evaluate", pt])
    os.remove(pt)
    check("K08 Portuguese answers (sim/nao/parcial) still accepted", "[NO] OPO02" in o and "[PARTIAL] SEN01" in o, o)

    # ---- references encoding (valid UTF-8, no mojibake)
    moj = []
    for fn in os.listdir(os.path.join(PKG, "references")):
        txt = io.open(os.path.join(PKG, "references", fn), encoding="utf-8").read()
        if re.search("Ã[ -¿]|â€", txt):
            moj.append(fn)
    check("E01 references without mojibake", not moj, str(moj))

    # ---- citations (optional)
    if a.src:
        code, o = run([os.path.join("tests", "verify_citations.py"), "--src", os.path.abspath(a.src)])
        check("V01 verify_citations: 0 failures", code == 0, o)

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
