# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests of the package scripts (no model, no network, without running the frameworks).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]   # --src enables verify_citations.py
Exit 0 if all pass. Conceptual cases (which need the agent) are in tests/casos-de-teste.md.
The expected values come from the text of the sources themselves (pages cited in each test).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL, OK = [], []
FX = os.path.join("tests", "fixtures")
L = os.path.join("scripts", "fw_lookup.py")
C = os.path.join("scripts", "compare_frameworks.py")
S = os.path.join("scripts", "scaffold.py")
N = os.path.join("scripts", "snippet_lint.py")


def run(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:600]))


def has(out, *subs):
    return all(s in out for s in subs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()

    # ---------------- fw_lookup
    rc, o = run([L, "runserver"])
    check("lookup runserver -> DJT p.2", rc == 0 and "DJT p.2" in o, o)
    rc, o = run([L, "include", "--source", "DJT"])
    check("lookup include -> DJT p.4", "DJT p.4" in o, o)
    rc, o = run([L, "swagger", "redoc"])
    check("lookup swagger redoc -> FAPI p.8-9", "FAPI p.8-9" in o, o)
    rc, o = run([L, "flask blueprint"])
    check("lookup flask blueprint -> NOT COVERED (FLT index only)", has(o, "NOT COVERED", "FLT"), o)
    rc, o = run([L, "fastapi deploy"])
    check("lookup fastapi deploy -> NOT COVERED for the command", has(o, "NOT COVERED", "command"), o)
    rc, o = run([L, "django models"])
    check("lookup django models -> NOT COVERED (part 2)", has(o, "NOT COVERED", "part 2"), o)
    rc, o = run([L, "receita de bolo"])
    check("lookup nonexistent topic -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "--page", "7", "--source", "DJT"])
    check("lookup DJT p.7 -> no technical content", "no technical content" in o, o)
    rc, o = run([L, "--page", "3", "--source", "FAPI"])
    check("lookup FAPI p.3 -> no technical content", "no technical content" in o, o)
    rc, o = run([L, "--page", "9", "--source", "FLT"])
    check("lookup FLT page 9 -> outside 1-3", rc == 1 and "1-3" in o, o)
    rc, o = run([L, "--sources"])
    check("lookup --sources identifies the 3 sources", has(o, "DJT:", "FLT:", "FAPI:", "version 5.0", "v0.141.1"), o)
    rc, o = run([L, "--gaps"])
    check("lookup --gaps lists gaps and non-technical pages", has(o, "NOT COVERED", "Flask", "DJT"), o)
    rc, o = run([L, "include", "--json"])
    check("lookup --json is valid JSON", rc == 0 and isinstance(json.loads(o), dict), o)

    # ---------------- compare_frameworks
    rc, o = run([C, "list"])
    check("compare list has 20 criteria", len([x for x in o.splitlines() if x.strip()]) == 20, o)
    rc, o = run([C, "compare", "instalacao"])
    check("compare instalacao: FLT NOT COVERED and FAPI with citation", has(o, "FLT: NOT COVERED", "FAPI p.4,5,20,21"), o)
    rc, o = run([C, "compare", "installation"])
    check("compare installation (English alias) = instalacao", has(o, "FLT: NOT COVERED", "FAPI p.4,5,20,21"), o)
    rc, o = run([C, "compare", "validacao-conversao"])
    check("compare validation: DJT and FLT NOT COVERED", has(o, "DJT: NOT COVERED", "FLT: NOT COVERED", "FAPI p.16,17"), o)
    rc, o = run([C, "compare", "roteamento", "--only", "DJT,FLT"])
    check("compare roteamento --only: Flask only a section title", has(o, "only as a section title", "DJT p.3,4,5") and "FAPI:" not in o, o)
    rc, o = run([C, "compare", "desempenho"])
    check("compare desempenho: FAPI only, as a claim", has(o, "DJT: NOT COVERED", "FLT: NOT COVERED", "Claim by the project itself"), o)
    rc, o = run([C, "compare", "inexistente"])
    check("compare nonexistent criterion -> NOT COVERED", rc == 1 and "NOT COVERED" in o, o)
    rc, o = run([C, "compare", "--json", "licenca"])
    check("compare --json valid", rc == 0 and json.loads(o)[0]["celulas"]["DJT"] == "NOT COVERED", o)
    rc, o = run([C, "coverage"])
    check("compare coverage lists the 3 frameworks", has(o, "DJT:", "FLT:", "FAPI:", "/20"), o)
    rc, o = run([C, "find", "banco"])
    check("compare find banco -> banco-dados", "banco-dados" in o, o)
    rc, o = run([C, "find", "database"])
    check("compare find database -> banco-dados", "banco-dados" in o, o)
    rc, o = run([C, "compare", "--only", "XXX"])
    check("compare invalid source code -> usage error", rc == 2, o)
    # integrity: every cell with content has a page, and every criterion has the 3 source codes
    with open(os.path.join(PKG, "scripts", "compare_data.json"), encoding="utf-8") as f:
        data = json.load(f)
    ok = all(set(c["celulas"].keys()) == {"DJT", "FLT", "FAPI"} for c in data["criterios"]) and \
        all((v is None) or (len(v) == 3 and v[2]) for c in data["criterios"] for v in c["celulas"].values())
    check("compare_data: 3 source codes per criterion and pages in every cell", ok)

    # ---------------- scaffold
    rc, o = run([S, "django"])
    check("scaffold django: DJT commands", has(o, "python -m django --version", "django-admin startproject mysite", "python manage.py runserver", "python manage.py startapp polls", "include(\"polls.urls\")"), o)
    rc, o = run([S, "django", "--project", "test"])
    check("scaffold django: rejects project 'test' (DJT p.1)", rc == 1 and "DJT p.1" in o, o)
    rc, o = run([S, "django", "--project", "django"])
    check("scaffold django: rejects project 'django'", rc == 1, o)
    rc, o = run([S, "django", "--app", "../x"])
    check("scaffold django: rejects name with a path", rc == 1 and "invalid" in o, o)
    rc, o = run([S, "fastapi"])
    check("scaffold fastapi: uv add and fastapi dev", has(o, "uv add \"fastapi[standard]\"", "fastapi dev", "command NOT COVERED"), o)
    check("scaffold fastapi: does not invent a deploy command", "fastapi deploy" not in o and "fastapi run" not in o, o)
    rc, o = run([S, "fastapi", "--variant", "async"])
    check("scaffold fastapi async: uses async def", "async def read_root" in o and "async def read_item" in o, o)
    rc, o = run([S, "fastapi", "--variant", "body"])
    check("scaffold fastapi body: BaseModel and PUT", has(o, "class Item(BaseModel)", "@app.put(\"/items/{item_id}\")"), o)
    rc, o = run([S, "flask"])
    check("scaffold flask: index only + NOT COVERED", has(o, "NOT COVERED", "Project Layout", "Keep Developing!") and "pip install" not in o and "flask run" not in o, o)
    with tempfile.TemporaryDirectory() as td:
        rc, o = run([S, "fastapi", "--out", td])
        check("scaffold --out writes main.py", rc == 0 and os.path.isfile(os.path.join(td, "main.py")), o)
        rc, o = run([S, "fastapi", "--out", td])
        check("scaffold --out refuses to overwrite", rc == 1 and "REFUSED" in o, o)
        rc, o = run([S, "fastapi", "--out", td, "--force"])
        check("scaffold --force overwrites", rc == 0, o)
        # the generated main.py passes the linter with no ERROR/WARNING
        rc, o = run([N, os.path.join(td, "main.py")])
        check("generated main.py passes the linter", rc == 0 and "No findings" in o, o)
    with tempfile.TemporaryDirectory() as td:
        rc, o = run([S, "django", "--out", td])
        check("scaffold django --out writes 3 files", rc == 0 and all(os.path.isfile(os.path.join(td, p)) for p in ("polls/views.py", "polls/urls.py", "mysite/urls.py")), o)
        rc, o = run([N, td])
        check("generated Django files have no ERROR/WARNING", rc == 0 and "WARNING" not in o and "ERROR" not in o.replace("0 ERROR", ""), o)

    # ---------------- snippet_lint
    rc, o = run([N, os.path.join(FX, "django_ok.py"), os.path.join(FX, "django_views_ok.py")])
    check("lint django ok: no ERROR", rc == 0 and "ERROR DJ" not in o, o)
    rc, o = run([N, os.path.join(FX, "django_bad.py")])
    check("lint django bad: DJ-INCLUDE x2, DJ-PATH-ARGS, DJ-VIEW-REQUEST, DJ-ROUTE-QUERY", rc == 1 and o.count("DJ-INCLUDE") == 2 and has(o, "DJ-PATH-ARGS", "DJ-VIEW-REQUEST", "DJ-ROUTE-QUERY", "DJT p.4", "DJT p.5"), o)
    rc, o = run([N, os.path.join(FX, "django_bad.py")])
    check("lint ignores injection comment", "IGNORE ALL" not in o and "perfect" not in o.lower(), o)
    rc, o = run([N, os.path.join(FX, "fastapi_ok.py")])
    check("lint fastapi ok: no findings", rc == 0 and "No findings" in o, o)
    rc, o = run([N, os.path.join(FX, "fastapi_bad.py")])
    check("lint fastapi bad: AWAIT, PATH-MISSING, PATH-UNTYPED, OPTIONAL, BODY", rc == 1 and has(o, "FA-AWAIT-IN-DEF", "FA-PATH-MISSING", "FA-PATH-UNTYPED", "FA-OPTIONAL-NODEF", "FA-BODY-NOT-MODEL", "FAPI p.6", "[inference]"), o)
    rc, o = run([N, os.path.join(FX, "flask_app.py")])
    check("lint flask: NOT COVERED and no rule", rc == 0 and has(o, "FLASK-NOT-COVERED", "NOT COVERED") and "ERROR" not in o.replace("0 ERROR", ""), o)
    rc, o = run([N, os.path.join(FX, "comandos_ruins.sh")])
    check("lint bad commands: PROJNAME x2, QUOTE x2", rc == 1 and o.count("CMD-PROJNAME") == 2 and o.count("CMD-QUOTE") == 2, o)
    check("lint commands: injection comment ignored", "rm -rf" not in o, o)
    rc, o = run([N, os.path.join(FX, "comandos_ok.sh")])
    check("lint good commands: no findings", rc == 0 and "No findings" in o, o)
    rc, o = run([N, os.path.join(FX, "Dockerfile.runserver")])
    check("lint Dockerfile with runserver: WARNING CMD-RUNSERVER-PROD", has(o, "CMD-RUNSERVER-PROD", "DJT p.2"), o)
    rc, o = run([N, FX, "--json"])
    d = json.loads(o)
    check("lint fixtures folder --json valid and with findings", d["arquivos"] >= 8 and len(d["achados"]) > 10, o)
    rc, o = run([N, "--rules"])
    check("lint --rules lists origin and page", has(o, "DJ-INCLUDE: ERROR [from source] (DJT p.4)", "FA-PATH-MISSING: WARNING [inference]"), o)
    rc, o = run([N])
    check("lint with no arguments -> usage (exit 2)", rc == 2, o)
    rc, o = run([N, os.path.join(FX, "nao_existe.py")])
    check("lint nonexistent file does not crash", "does not exist" in o, o)

    # ---------------- citations
    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations: 0 failures", rc == 0 and "total failures: 0" in o, o)
    else:
        print("SKIP verify_citations (use --src)")

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
