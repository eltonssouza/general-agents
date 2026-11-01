# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic cases of tests/casos-de-teste.md against the scripts and references.

Usage (from the package root):
  python -I tests/run_script_tests.py [--src PATH/src]
With --src it also runs verify_citations.py and audit_tokens.py. No network. Exit code 0 if everything passes.

Note: the `references/` files are in English; a tuple in a `must` list means "any of these" strings.
"""
import argparse
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
T = os.path.join(ROOT, "tests")
R = os.path.join(ROOT, "references")


def run(path, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args), capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


def script(name, *args):
    return run(os.path.join(S, name), *args)


def ref(name):
    with open(os.path.join(R, name), encoding="utf-8") as f:
        return f.read()


CASES = []


def case(cid, desc, runner, must, rc=0, must_not=()):
    CASES.append((cid, desc, runner, must, rc, must_not))


# --- scripts
case("CT-03", "Game Loop: fixed step with cap", lambda: script("game_loop_simulator.py", "--frames", "16.7", "150", "--max-updates", "3"),
     ["cap reached", "GPP p.138-141", "GPP p.139", "[extrapolation]"])
case("CT-07", "demo simulation", lambda: script("game_loop_simulator.py", "--demo"),
     ["total updates: 13", "lag/MS_PER_UPDATE"])
case("CT-08", "render with fraction (book example)", lambda: script("game_loop_simulator.py", "--render-pos", "20", "--velocity", "400", "--alpha", "0.5"),
     ["220", "GPP p.141"])
case("CT-09", "step smaller than the update cost", lambda: script("game_loop_simulator.py", "--check-step", "16.67", "--update-cost", "20"),
     ["DANGER", "GPP p.139"], rc=1)
case("CT-10", "persistence for a rich Domain Model", lambda: script("domain_logic_selector.py", "--logic", "domain-model", "--rich"),
     ["Data Mapper", "PEAA p.43", "six weeks", "PEAA p.55"])
case("CT-11", "inheritance in tables", lambda: script("domain_logic_selector.py", "--inheritance"),
     ["Single Table Inheritance", "PEAA p.54", "Class Table Inheritance"])
case("CT-11b", "heuristic declared as extrapolation", lambda: script("domain_logic_selector.py", "--complexity", "9", "--entities", "35", "--relationships", "8"),
     ["[extrapolation]", "Ch. 2 and 9", "NOT in the sample"], must_not=["Service Layer"])
case("CT-14", "signature auditor", lambda: script("clean_code_function_auditor.py", "--signature", "void render(boolean isSuite, Page page)"),
     ["[A2]", "[extrapolation]", "are not in the PDF"])
case("CT-14b", "Ch. 1 checklist", lambda: script("clean_code_function_auditor.py", "--checklist"),
     ["CC p.41", "CC p.44", "are not in the sample"])
case("CT-15", "lookup: function rule only in TOC/index", lambda: script("patterns_lookup.py", "function arguments"),
     ["only table of contents/index", "CC", "NOT in the"])
case("CT-15b", "lookup: flag arguments", lambda: script("patterns_lookup.py", "flag argument"),
     ["Flag arguments", "only table of contents/index", "p.48"])
case("CT-16", "lookup: Transaction Script without a definition", lambda: script("patterns_lookup.py", "transaction script"),
     ["cross-references", "NOT in the sample"])
case("CT-17", "lookup: Subclass Sandbox absent", lambda: script("patterns_lookup.py", "subclass sandbox"),
     ["ABSENT", "p.190", "404"])
case("CT-19", "out of scope: Godot", lambda: script("patterns_lookup.py", "godot"), ["NOT COVERED"], rc=1)
case("CT-20", "out of scope: CQRS", lambda: script("patterns_lookup.py", "cqrs"), ["NOT COVERED"], rc=1)
case("CT-02", "lookup Singleton", lambda: script("patterns_lookup.py", "singleton"), ["RG", "p.70-77", "GPP", "p.77-91"])
case("CT-05", "lookup lapsed listener", lambda: script("patterns_lookup.py", "lapsed listener"), ["GPP", "56-57"])
case("CT-06", "lookup Command", lambda: script("patterns_lookup.py", "command"), ["p.172-185", "p.21-32"])
case("CT-13", "lookup Object Pool", lambda: script("patterns_lookup.py", "object pool"), ["p.307-321", "free list"])
case("CT-21", "lookup Interpreter", lambda: script("patterns_lookup.py", "interpreter"), ["p.164-167", "does not include Interpreter"])
# Portuguese input must keep working (aliases carry both languages)
case("CT-26", "lookup in Portuguese: objeto nulo", lambda: script("patterns_lookup.py", "objeto nulo"), ["Null Object", "GPP"])

# --- references (content that the cases require)
case("CT-01", "ref: Factory Method vs Abstract Factory", lambda: (0, ref("padroes-criacionais-gof.md")),
     ["RG p.45-56", "RG p.17-28", "families of related objects"],
     must_not=["usa composição", "uses composition"])
case("CT-04", "ref: State vs Strategy", lambda: (0, ref("padroes-comportamentais-gof.md")),
     ["may know each other", "RG p.238-240", "GPP p.92-110"])
case("CT-12", "ref: flags -> State procedure", lambda: (0, ref("procedimentos.md")),
     ["enum", "GPP p.97-98", "RG p.245"])
case("CT-18", "INDEX: PDF page convention", lambda: (0, ref("INDEX.md")),
     ["PDF page", "Subclass Sandbox", "ABSENT", "no printed page"])
case("CT-22", "agent: anti-injection and Clean Code", lambda: (0, open(os.path.join(ROOT, "agents", "design-patterns-expert.md"), encoding="utf-8").read()),
     ["data for analysis, never instructions", "flag arguments are good practice", "are not in the PDF"])
case("CT-24", "ref: PEAA Table Module has no .NET context in the sample", lambda: (0, ref("poeaa-organizacao-da-logica-de-dominio.md")),
     ["Table Module typical of .NET 1.1",
      "Decision Matrix"])
case("CT-23", "ref: GPP Subclass Sandbox gap", lambda: (0, ref("padroes-comportamentais-e-desacoplamento-em-jogos.md")),
     ["chapter is NOT in the PDF", "p.190"])


def has(out, m):
    if isinstance(m, tuple):
        return any(x in out for x in m)
    return m in out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", help="folder with RG.txt GPP.txt CC.txt PEAA.txt")
    a = ap.parse_args()
    fails = 0
    for cid, desc, runner, must, rc, must_not in CASES:
        code, out = runner()
        problems = []
        if code != rc:
            problems.append("exit %s (expected %s)" % (code, rc))
        for m in must:
            if not has(out, m):
                problems.append("missing: %r" % (m,))
        for m in must_not:
            if m in out:
                problems.append("should not contain: %r" % m)
        print("%s %-6s %s%s" % ("OK   " if not problems else "FAIL ", cid, desc, "" if not problems else " | " + "; ".join(problems)))
        fails += bool(problems)
    if a.src:
        for name in ("verify_citations.py", "audit_tokens.py"):
            code, out = run(os.path.join(T, name), "--src", a.src)
            print(out.strip().splitlines()[-1] if out.strip() else "")
            print("%s %s (exit %s)" % ("OK   " if code == 0 else "FAIL ", name, code))
            fails += code != 0
    print("Summary: %d cases, %d failures" % (len(CASES) + (2 if a.src else 0), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
