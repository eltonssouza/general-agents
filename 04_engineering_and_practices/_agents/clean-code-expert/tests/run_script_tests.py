# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic cases of tests/casos-de-teste.md against the scripts and checks
data, pages, references, skills and adapters of the clean-code-expert package.
Usage (from the package root):
  python -I tests/run_script_tests.py [--src <folder with CL.txt>]
With --src (or with the text in the default folder <collection>/scratch/engineering), it also runs
verify_citations.py; without the text, that step is marked SKIP. No network. Exit code 0 if everything passes.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
T = os.path.join(ROOT, "tests")
FX = os.path.join(T, "fixtures")
DEFAULT_SRC = os.path.normpath(os.path.join(ROOT, "..", "..", "..", "scratch", "engineering"))
MAX_PAGE = 398

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run(path, *args, stdin=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args), input=stdin,
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


CASES = []


def case(cid, desc, script, args, must, rc=0, must_not=(), stdin=None):
    CASES.append((cid, desc, os.path.join(S, script), args, must, rc, must_not, stdin))


# cc_lookup.py
case("LK-01", "flag -> function arguments", "cc_lookup.py", ["flag", "--max", "1"],
     ["parametros-de-funcoes", "CL p.48-51", "[from source]"])
case("LK-02", "YAGNI -> NOT COVERED", "cc_lookup.py", ["YAGNI"], ["NOT COVERED"], rc=1)
case("LK-03", "Mockito -> NOT COVERED with a note", "cc_lookup.py", ["Mockito"], ["NOT COVERED", "NOTE"], rc=1)
case("LK-04", "SOLID -> principles, without the acronym in the book", "cc_lookup.py", ["SOLID", "--max", "1"],
     ["principios-srp-ocp-dip", "SOLID acronym does not appear", "Inversão da Independência"])
case("LK-05", "one assert per test -> one concept per test", "cc_lookup.py", ["um assert por teste", "--max", "1"],
     ["uma-afirmacao-um-conceito", "CL p.132-134"])
case("LK-05b", "English query: one assert per test", "cc_lookup.py", ["one assert per test", "--max", "1"],
     ["uma-afirmacao-um-conceito", "CL p.132-134"])
case("LK-06", "Law of Demeter", "cc_lookup.py", ["--topic", "lei-de-demeter"], ["CL p.102"])
case("LK-07", "nonexistent topic -> exit 2", "cc_lookup.py", ["--topic", "nao-existe"], ["Unknown topic"], rc=2)
case("LK-08", "chapter 9 list has F.I.R.S.T.", "cc_lookup.py", ["--list", "--chapter", "9"], ["first", "tres-leis-do-tdd"])
case("LK-09", "three laws of TDD", "cc_lookup.py", ["--topic", "tres-leis-do-tdd"], ["CL p.125", "First Law"])
case("LK-10", "four rules of simple design", "cc_lookup.py", ["--topic", "projeto-simples-quatro-regras"], ["CL p.169"])
# cc_smells.py
case("SM-01", "G5 duplication", "cc_smells.py", ["G5"], ["G5 - Duplication (Duplicação)", "CL p.284"])
case("SM-02", "code in lowercase and with a zero", "cc_smells.py", ["g05"], ["G5 - Duplication (Duplicação)"])
case("SM-03", "G37 does not exist -> NOT COVERED", "cc_smells.py", ["G37"], ["NOT COVERED", "G1-G36"], rc=1)
case("SM-04", "family T has T1-T9", "cc_smells.py", ["--family", "T"], ["T1 ", "T9 "], must_not=["T10"])
case("SM-05", "magic numbers -> G25 (Portuguese query)", "cc_smells.py", ["números mágicos", "--max", "1"], ["G25", "CL p.294"])
case("SM-05b", "magic numbers -> G25 (English query)", "cc_smells.py", ["magic numbers", "--max", "1"], ["G25", "CL p.294"])
case("SM-06", "F1 and F3 together", "cc_smells.py", ["F1", "F3"],
     ["Too Many Arguments (Parâmetros em excesso)", "Flag Arguments (Parâmetros lógicos)", "CL p.283"])
case("SM-07", "G34 with the title cut off in the edition", "cc_smells.py", ["G34"], ["G34", "CL p.299", "Descend Only One Level"])
case("SM-08", "unknown family -> exit 2", "cc_smells.py", ["--family", "X"], ["Unknown family"], rc=2)
# cc_audit.py
case("AU-01", "Java with smells", "cc_audit.py", [os.path.join(FX, "Ruim.java")],
     ["F1 Too Many Arguments (CL p.283)", "F3 Flag Arguments", "C5 Commented-Out Code", "G36",
      "G25", "N6", "G23", "nesting", "returns null", "closing brace"], rc=1, must_not=["not indexed"])
case("AU-02", "clean Java -> no candidates", "cc_audit.py", [os.path.join(FX, "Limpo.java")], ["0 candidate"], rc=0)
case("AU-03", "Python with smells", "cc_audit.py", [os.path.join(FX, "ruim.py")],
     ["F1 Too Many Arguments", "F3 Flag Arguments", "C5 Commented-Out Code", "urgent=False"], rc=1)
case("AU-04", "stdin without --lang -> exit 2", "cc_audit.py", ["-"], ["--lang"], rc=2, stdin="int x = 1;")
case("AU-05", "stdin with --lang", "cc_audit.py", ["-", "--lang", "ts"], ["F3 Flag Arguments", "<stdin>:1"], rc=1,
     stdin="function render(isSuite: boolean) {\n  return 1;\n}\n")
case("AU-05b", "UTF-8 stdin with accents (Windows/-I)", "cc_audit.py", ["-", "--lang", "java"], ["F3 Flag Arguments", "'renderização'"], rc=1,
     stdin="public String renderização(boolean éSuite) {\n  return \"ação\";\n}\n")
case("AU-06", "--min MEDIUM filters LOW", "cc_audit.py", [os.path.join(FX, "Ruim.java"), "--min", "MEDIUM"], ["HIGH"], rc=1,
     must_not=["LOW "])
case("AU-06b", "--min MEDIO (Portuguese spelling) filters LOW", "cc_audit.py", [os.path.join(FX, "Ruim.java"), "--min", "MEDIO"], ["HIGH"], rc=1,
     must_not=["LOW "])
case("AU-07", "hostile text in the code is data, not instruction", "cc_audit.py", [os.path.join(FX, "injecao.py")],
     ["candidate"], rc=0, must_not=["prompt", "deleted"])
case("AU-08", "unsupported extension -> exit 2", "cc_audit.py", [os.path.join(T, "casos-de-teste.md")], ["unsupported language"], rc=2)
# cc_checklist.py
case("CK-01", "areas detected in Java", "cc_checklist.py", ["--file", os.path.join(FX, "Ruim.java")],
     ["Meaningful names", "Functions", "Classes", "always applicable", "CL p.43"])
case("CK-02", "tests area", "cc_checklist.py", ["--area", "testes"], ["F.I.R.S.T.", "CL p.134-135", "CL p.125"])
case("CK-03", "unknown area -> exit 2", "cc_checklist.py", ["--area", "xyz"], ["Unknown area"], rc=2)
case("CK-04", "list has 12 areas", "cc_checklist.py", ["--list"], ["concorrencia", "design-simples", "limites"])


def check_data():
    out = []
    idx = json.load(open(os.path.join(S, "cc_index.json"), encoding="utf-8"))
    out.append(("IDX", "cc_index.json: >=100 topics and a list of uncovered topics",
                len(idx["topics"]) >= 100 and len(idx["uncovered"]) >= 20))
    sm = json.load(open(os.path.join(S, "cc_smells.json"), encoding="utf-8"))
    counts = {}
    for s in sm["smells"]:
        counts[s["code"][0]] = counts.get(s["code"][0], 0) + 1
    out.append(("SML", "cc_smells.json: 66 heuristics (C5 E2 F4 G36 J3 N7 T9), each with title and title_en",
                counts == {"C": 5, "E": 2, "F": 4, "G": 36, "J": 3, "N": 7, "T": 9}
                and all(s.get("title") and s.get("title_en") for s in sm["smells"])))
    ck = json.load(open(os.path.join(S, "cc_checklist.json"), encoding="utf-8"))
    out.append(("CKL", "cc_checklist.json: 12 areas, items with a page",
                len(ck["areas"]) == 12 and all(re.match(r"p\.\d", i["ref"]) for a in ck["areas"].values() for i in a["items"])))
    return out


def check_pages():
    files = glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True) + glob.glob(os.path.join(S, "*.json"))
    n = bad = 0
    for f in files:
        t = open(f, encoding="utf-8").read()
        for m in re.finditer(r"CL p\.(\d{1,4})(?:-(\d{1,4}))?|p\.(\d{1,4})(?:-(\d{1,4}))?", t):
            for g in m.groups():
                if g:
                    n += 1
                    bad += not (1 <= int(g) <= MAX_PAGE)
    return n, bad


def check_package():
    out = []
    agent = open(os.path.join(ROOT, "agents", "clean-code-expert.md"), encoding="utf-8").read()
    refs = set(re.findall(r"`([\w-]+\.md)`", agent))
    missing = [r for r in refs if not os.path.exists(os.path.join(ROOT, "references", r))]
    out.append(("REF", "every reference cited by the agent exists (%d)" % len(refs), not missing))
    sk_bad = []
    for sk in glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md")):
        t = open(sk, encoding="utf-8").read()
        m = re.match(r"---\nname: ([\w-]+)\ndescription: (.+?)\n---\n", t)
        if not m or m.group(1) != os.path.basename(os.path.dirname(sk)) or len(m.group(2)) > 1024:
            sk_bad.append(sk)
    out.append(("SKL", "4 skills with valid frontmatter (name = folder, description <= 1024)",
                not sk_bad and len(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))) == 4))
    m = re.match(r"---\nname: clean-code-expert\ndescription: (.+?)\ntools: Read, Grep, Glob, Bash\nmodel: (opus|sonnet|haiku)\n---\n", agent)
    out.append(("AGT", "agent: Claude Code frontmatter with minimal tools and a model (collection policy)", bool(m)))
    heads = re.findall(r"^## .+$", agent, re.M)
    cop = open(os.path.join(ROOT, ".github", "agents", "clean-code-expert.agent.md"), encoding="utf-8").read()
    cdx = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8").read()
    ok = (re.findall(r"^## .+$", cop, re.M) == heads == re.findall(r"^## .+$", cdx, re.M)
          and "tools: ['read', 'search', 'execute']" in cop and "<PKG>" in cop and "<PKG>" in cdx)
    out.append(("ADP", "Codex/Copilot adapters with the same sections as the canonical one", ok))
    pj = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"))
    out.append(("PLG", "plugin.json: name, author object, license",
                pj.get("name") == "clean-code-expert" and isinstance(pj.get("author"), dict) and pj.get("license") == "MIT"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    fails = 0
    for cid, desc, script, args, must, rc, must_not, stdin in CASES:
        code, out = run(script, *args, stdin=stdin)
        missing = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not missing and not bad
        print("%s %-6s %s" % ("OK   " if ok else "FAIL ", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (code, rc, missing, bad))
    for cid, desc, ok in check_data() + check_package():
        print("%s %-6s %s" % ("OK   " if ok else "FAIL ", cid, desc))
        fails += 0 if ok else 1
    n, bad = check_pages()
    print("%s %-6s cited pages within 1-%d (%d citations, %d outside)" % ("OK   " if not bad else "FAIL ", "RNG", MAX_PAGE, n, bad))
    fails += 1 if bad else 0
    src = a.src or DEFAULT_SRC
    if a.src or os.path.exists(os.path.join(src, "CL.txt")):
        code, out = run(os.path.join(T, "verify_citations.py"), "--src", src)
        last = out.strip().splitlines()[-1] if out.strip() else ""
        print("%s %-6s verify_citations.py: %s" % ("OK   " if code == 0 else "FAIL ", "VC", last))
        fails += 0 if code == 0 else 1
    else:
        print("SKIP   VC     verify_citations (book text not found; use --src)")
    print("Summary: %d script cases + checks, %d failures" % (len(CASES), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
