# -*- coding: utf-8 -*-
"""
run_cases.py - MECHANICALLY runs the cases of tests/casos-de-teste.md against the package.

Usage (from the package root):  python -I tests/run_cases.py [--src TXT_FOLDER]

What this tests (and what it does NOT test):
- It TESTS that the package (agent + references + skills + scripts) CONTAINS and RETRIEVES the material the case requires:
  each check is a grep in a reference/skill/agent, the real execution of a script, or (with --src) checking the fact
  on the cited page of the PDF text.
- It does NOT test a model's answer: no answer is generated here. See tests/relatorio-de-fidelidade.md (there was no
  blind execution by an independent model in this round).
Check types:
  ("pkg", regex)            -> regex matches in some file of agents/, references/ or skills/*/SKILL.md
  ("cmd", [script, args...], regex) -> runs the script (scan|look|tutv) and the output matches regex
  ("src", "Ref p.103", [terms])    -> (needs --src) the page contains all the terms
  ("absent", "Tut p.1-167", [terms]) -> (needs --src) no term appears on the pages
Exit 0 if no executed check failed.
"""
import argparse
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
import audit_tokens as A  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SC = {
    "scan": os.path.join(ROOT, "skills", "python-code-review", "scripts", "scan_python_smells.py"),
    "look": os.path.join(ROOT, "skills", "python-stdlib-lookup", "scripts", "stdlib_lookup.py"),
    "tutv": os.path.join(ROOT, "skills", "python-version-features", "scripts", "tutorial_versions.py"),
}
FIX = os.path.join(ROOT, "skills", "python-code-review", "scripts", "fixtures")

CASES = {
    1: ("mutable default", [
        ("pkg", r"avaliado uma só vez, na definição|evaluated (only )?once, at definition"),
        ("pkg", r"padrão `None` e criar dentro|use `None` and create (it|the object) inside"),
        ("src", "Tut p.31", ["the default value is evaluated only once"]),
        ("src", "Tut p.32", ["if l is none"]),
        ("src", "Ref p.103", ["default values are calculated, once, when the function is defined"]),
        ("cmd", ["scan", os.path.join(FIX, "sample.py")], r"mutable-default"),
    ]),
    2: ("scope, global and nonlocal", [
        ("pkg", r"global.*nonlocal|nonlocal.*global"),
        ("pkg", r"LEGB"),
        ("src", "Ref p.76", ["global statement must precede all uses"]),
        ("src", "Ref p.123", ["nonlocal"]),
    ]),
    3: ("closure in a loop (late binding)", [
        ("pkg", r"variáveis livres.*tempo de execução|livres são resolvidas em tempo de execução|free variables\W+at run time"),
        ("pkg", r"\[inferência\]|\[inference\]"),
        ("src", "Ref p.78", ["name resolution of free variables occurs at runtime, not at compile time"]),
        ("absent", "Ref p.78", ["late binding", "lambda i=i"]),
        ("absent", "Tut p.31-32", ["late binding", "lambda i=i"]),
    ]),
    4: ("is vs ==", [
        ("pkg", r"identity"),
        ("src", "Ref p.110", ["identity comparisons"]),
        ("src", "Ref p.32", ["may or may not refer to the same object"]),
        ("src", "Notes p.523", ["-5 and 256"]),
    ]),
    5: ("order of the excepts, finally", [
        ("pkg", r"primeira que casa vence|first (one that|matching clause)\W+(matches|wins)"),
        ("cmd", ["scan", os.path.join(FIX, "sample.py")], r"shadowed-except"),
        ("src", "Tut p.73", ["from version 3.14 the compiler emits a syntaxwarning"]),
        ("src", "Ref p.127", ["optionally dropping grouping parentheses"]),
    ]),
    6: ("generator x list", [
        ("pkg", r"__iter__.*__next__|__next__.*__iter__"),
        ("src", "Tut p.90", ["__iter__() and __next__() methods are created automatically"]),
        ("src", "Tut p.89", ["stopiteration"]),
    ]),
    7: ("versions: match, type, except A, B, except*", [
        ("pkg", r"match.*3\.10"),
        ("pkg", r"`except\*`.*versão não informada|versão não informada.*except\*|version not given in the text.*except\*|except\*.*version not given"),
        ("src", "Ref p.131", ["added in version 3.10"]),
        ("src", "Ref p.123", ["added in version 3.12"]),
        ("src", "Ref p.127", ["changed in version 3.14"]),
        ("cmd", ["tutv", "except*"], r"Tutorial 3\.10: absent"),
    ]),
    8: ("with protocol", [
        ("pkg", r"__exit__.*suprime|suprime.*exceção|__exit__.*suppress|suppress.*exception"),
        ("src", "Ref p.130", ["the exception is suppressed"]),
        ("src", "Ref p.68", ["__exit__"]),
    ]),
    9: ("__eq__ e __hash__", [
        ("pkg", r"__eq__.*__hash__"),
        ("src", "Ref p.53", ["implicitly set to none"]),
        ("cmd", ["scan", os.path.join(FIX, "sample.py")], r"eq-without-hash"),
    ]),
    10: ("modifying a collection during iteration", [
        ("pkg", r"cópia|iterate over (a|the) copy"),
        ("src", "Notes p.790", ["iterate through the loop backwards"]),
        ("src", "Tut p.23", ["loop over a copy of the collection"]),
        ("cmd", ["scan", os.path.join(FIX, "sample.py")], r"mutate-while-iterating"),
    ]),
    11: ("pasted Python 2 code", [
        ("cmd", ["scan", os.path.join(FIX, "sample_py2.py")], r"py2-print"),
        ("cmd", ["scan", os.path.join(FIX, "sample_py2.py")], r"py2-except-comma"),
        ("pkg", r"2to3"),
        ("src", "Notes p.646", ["example.py.bak"]),
    ]),
    12: ("venv and pip", [
        ("pkg", r"virtualenvwrapper"),
        ("pkg", r"the Notes do not say they prefer `venv`"),
        ("src", "Notes p.715", ["most recommended"]),
    ]),
    13: ("stdlib: csv and paths", [
        ("cmd", ["look", "csv"], r"Lib p\.665-671"),
        ("cmd", ["look", "pathlib"], r"Lib p\.483-509"),
        ("pkg", r"não trazem `csv\.reader`|não trazem csv\.reader|not? carry `csv\.reader`"),
    ]),
    14: ("dict order: official x Notes", [
        ("pkg", r"DIVERGE"),
        ("src", "Ref p.35", ["changed in version 3.7"]),
        ("src", "Notes p.289", ["the order of keys in python dictionaries is arbitrary"]),
    ]),
    15: ("threads, processes, asyncio, GIL", [
        ("pkg", r"--disable-gil"),
        ("src", "Tut p.130", ["--disable-gil"]),
        ("cmd", ["look", "threading"], r"threading"),
    ]),
    16: ("out of scope: another language", [
        ("pkg", r"Outras linguagens: recuse|Other languages: decline"),
    ]),
    17: ("version without a source: Python 3.15", [
        ("pkg", r"3\.15 em diante|3\.15 onward"),
        ("pkg", r"Não há documentação do 3\.15|não há documentação do 3\.15|(no|nor) 3\.15 documentation"),
    ]),
    18: ("false premise: declared types", [
        ("pkg", r"type hints.*opcionais|opcionais e não impost|type hints.*optional"),
        ("src", "Tut p.139", ["type hints are optional and are not enforced by python"]),
    ]),
    19: ("injection in pasted code", [
        ("pkg", r"dados, nunca instruções|data, never instructions"),
        ("cmd", ["scan", os.path.join(FIX, "injection.py")], r"1 finding"),
    ]),
    20: ("eval/exec with external input", [
        ("src", "Notes p.505", ["not possible to use eval or exec to execute code from untrusted user securely"]),
        ("cmd", ["scan", os.path.join(FIX, "sample.py")], r"eval-exec.*p\.505"),
        ("pkg", r"SEG-3"),
    ]),
    21: ("return/break in finally; no false positive", [
        ("src", "Tut p.73", ["pep 765"]),
        ("cmd", ["scan", os.path.join(FIX, "sample.py")], r"finally-flow"),
        ("cmd", ["scan", os.path.join(FIX, "clean.py")], r"0 finding"),
    ]),
    22: ("version of ExceptionGroup/add_note via the 3.10-3.13 Tutorials", [
        ("cmd", ["tutv", "add_note"], r"Tutorial 3\.10: absent"),
        ("cmd", ["tutv", "add_note"], r"Tutorial 3\.11: body"),
        ("cmd", ["tutv", "add_note"], r"\[inference\]"),
        ("pkg", r"não é marca de versão|nao e marca de versao|not a version mark"),
    ]),
    23: ("pathlib: not covered in the Tutorial, with a page in the Lib", [
        ("cmd", ["tutv", "pathlib"], r"none of the 5 Tutorials"),
        ("cmd", ["look", "pathlib"], r"Lib p\.483-509"),
        ("absent", "Tut p.1-167", ["pathlib"]),
    ]),
    24: ("is free-threaded the default in 3.14?", [
        ("pkg", r"does not say\*\* that the free-threaded build is the 3.14 default"),
        ("src", "Lib p.1018", ["as of python 3.13, free-threaded builds can disable the gil"]),
        ("absent", "Tut p.130", ["enabled by default", "default in 3.14"]),
    ]),
    25: ("asyncio.run / TaskGroup", [
        ("pkg", r"asyncio.*moderno|`asyncio\.run`"),
        ("absent", "Tut p.1-167", ["asyncio.run", "taskgroup"]),
        ("absent", "Notes p.313-317", ["asyncio.run", "taskgroup"]),
    ]),
    26: ("Notes chapter without coverage (heapq, bitwise)", [
        ("pkg", r"Heapq"),
        ("pkg", r"Bitwise Operators"),
        ("cmd", ["look", "heapq"], r"heapq"),
    ]),
    27: ("does 2to3 exist in 3.14?", [
        ("pkg", r"2to3.*3\.14|3\.14.*2to3"),
        ("absent", "Lib p.1-2488", ["2to3"]),
        ("src", "Notes p.646", ["2to3 -w example.py"]),
    ]),
    28: ("injection in docstring/comment/traceback", [
        ("pkg", r"docstrings, tracebacks"),
        ("cmd", ["scan", os.path.join(FIX, "injection.py")], r"mutable-default"),
    ]),
    29: ("page convention PDF x printed", [
        ("pkg", r"impressa = PDF|PDF = impressa|printed one is N"),
        ("pkg", r"N−26|N-26"),
        ("src", "Ref p.26", ["t-strings"]),
    ]),
    30: ("except A, B in 3.14 x linter", [
        ("pkg", r"válido no Python 3\.14|válida no 3\.14|válido no 3\.14|valid (syntax )?(in|on) (Python )?3\.14"),
        ("src", "Ref p.127", ["pep 758"]),
        ("cmd", ["scan", os.path.join(FIX, "sample_py2.py")], r"3\.14"),
    ]),
    31: ("term outside any index (NOT COVERED)", [
        ("cmd", ["look", "kubernetes"], r"NOT COVERED"),
        ("cmd", ["tutv", "fantasma_xyz"], r"NOT COVERED"),
    ]),
    32: ("pickle: the warning exists in the book", [
        ("src", "Tut p.66", ["insecure by default", "untrusted source"]),
        ("src", "Notes p.535", ["there are no security guarantees"]),
        ("pkg", r"o capítulo de pickle traz o aviso na p\.535|pickle chapter .*p\.535"),
        ("cmd", ["scan", os.path.join(FIX, "sample.py")], r"pickle-load"),
    ]),
}


def pkg_text():
    files = glob.glob(os.path.join(ROOT, "agents", "*.md")) + glob.glob(os.path.join(ROOT, "references", "*.md")) + \
        glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))
    return "\n".join(open(f, encoding="utf-8").read() for f in files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=None)
    a = ap.parse_args()
    text = pkg_text()
    pages = {}
    if a.src:
        for sg, (fn, n) in A.SOURCES.items():
            pages[sg] = {k: A.norm(v) for k, v in A.load_pages(os.path.join(a.src, fn)).items()}
    tot = fail = skip = 0
    for cid, (name, checks) in CASES.items():
        res = []
        for ck in checks:
            kind = ck[0]
            if kind == "pkg":
                ok = re.search(ck[1], text, re.S | re.I) is not None if False else re.search(ck[1], text, re.I) is not None
            elif kind == "cmd":
                p = subprocess.run([sys.executable, "-I", SC[ck[1][0]], *ck[1][1:]], capture_output=True, text=True, encoding="utf-8")
                ok = re.search(ck[2], p.stdout, re.S) is not None
            elif kind in ("src", "absent"):
                if not a.src:
                    skip += 1
                    res.append("-")
                    continue
                cites = A.parse_citations(ck[1])
                sg, pl = cites[0][2], cites[0][3]
                blob = " ".join(pages[sg][p] for p in pl)
                if kind == "src":
                    ok = all(A.norm(t) in blob or A.squash(A.norm(t)) in A.squash(blob) for t in ck[2])
                else:
                    ok = not any(re.search(r"(?<![a-z0-9_])" + re.escape(A.norm(t)) + r"(?![a-z0-9_])", blob) for t in ck[2])
            tot += 1
            if not ok:
                fail += 1
            res.append("ok" if ok else "FAIL")
        status = "FAIL" if "FAIL" in res else "PASS"
        print(f"CASE {cid:2d} {status}  [{' '.join(res)}]  {name}")
        if status == "FAIL":
            for ck, r in zip(checks, res):
                if r == "FAIL":
                    print("      failed:", ck[:3])
    print(f"\n{tot - fail}/{tot} executed checks passed; {skip} skipped (no --src); {len(CASES)} cases.")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
