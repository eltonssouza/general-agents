# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic test cases for the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]   # --src enables verify_citations.py
Exit 0 if all pass. Conceptual cases (which require the agent) are in tests/casos-de-teste.md.
"""
import argparse
import json
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL, OK = [], []
L = os.path.join("scripts", "svelte_lookup.py")
LINT = os.path.join("scripts", "svelte_lint.py")
CMP = os.path.join("scripts", "framework_compare.py")
CK = os.path.join("scripts", "svelte_checklist.py")
FX = os.path.join("tests", "fixtures")


def run(args, stdin=None):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG, input=stdin)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def has(out, *subs):
    return all(s in out for s in subs)


def rules_of(out):
    return set(re.findall(r"\b(SVL-[A-Z]+\d+)\b", out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()

    # ---- lookup
    rc, o = run([L, "stores"])
    check("lookup stores -> SVHB p.23-25", has(o, "SVHB p.23,24,25"), o)
    rc, o = run([L, "runes"])
    check("lookup runes -> NOT COVERED", "NOT COVERED: Svelte 5" in o, o)
    rc, o = run([L, "page.svelte"])
    check("lookup page.svelte -> NOT COVERED file-based routing", "NOT COVERED: File-based routing" in o, o)
    rc, o = run([L, "npm", "create", "astro"])
    check("lookup npm create astro -> ASTRO p.2", "ASTRO p.2" in o, o)
    rc, o = run([L, "ssr", "--source", "SKGS"])
    check("lookup ssr em SKGS", has(o, "SKGS p.2") and "SVHB" not in o, o)
    rc, o = run([L, "kubernetes"])
    check("lookup out-of-scope term -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "typescript"])
    check("lookup typescript -> NOT COVERED", "NOT COVERED: TypeScript" in o, o)
    rc, o = run([L, "astro", "vs", "sveltekit"])
    check("lookup astro vs sveltekit -> NOT COVERED choice", "NOT COVERED: Choice between Astro and SvelteKit" in o, o)
    rc, o = run([L, "--page", "SVHB", "33"])
    check("lookup --page SVHB 33 -> bind:value", has(o, "bind:value", "p.32,33"), o)
    rc, o = run([L, "--page", "SKGS", "3"])
    check("lookup --page SKGS 3 -> no useful text", "no useful technical text" in o, o)
    rc, o = run([L, "--page", "ASTRO", "4"])
    check("lookup --page ASTRO 4 -> error", rc == 1, o)
    rc, o = run([L, "--gaps"])
    check("lookup --gaps lists runes and Astro v7", has(o, "runes", "v7"), o)
    rc, o = run([L, "--sources"])
    check("lookup --sources shows 2019 and v7", has(o, "2019", "v7"), o)
    rc, o = run([L, "slot", "--json"])
    try:
        check("lookup --json valid", len(json.loads(o)["achados"]) >= 1)
    except Exception as ex:
        check("lookup --json valid", False, str(ex))

    # ---- lint
    rc, o = run([LINT, os.path.join(FX, "bom.svelte")])
    check("lint bom.svelte no findings, exit 0", rc == 0 and "No findings" in o, o)
    rc, o = run([LINT, os.path.join(FX, "ruim.svelte")])
    exp = {"SVL-A01", "SVL-B01", "SVL-E01", "SVL-L01", "SVL-L02", "SVL-S01", "SVL-S02", "SVL-ST01", "SVL-ST02",
           "SVL-M01", "SVL-P01", "SVL-D01", "SVL-AW01", "SVL-EV01", "SVL-EV02", "SVL-SL01"}
    check("lint ruim.svelte finds the expected rules and exit 1", rc == 1 and exp <= rules_of(o), o + str(exp - rules_of(o)))
    check("lint ruim: findings carry origin and page", has(o, "[from source]", "SVHB p.15-16", "SVHB p.33"), o)
    rc, o = run([LINT, os.path.join(FX, "ruim.svelte"), "--no-info"])
    check("lint --no-info hides info", "[info]" not in o and "[error]" in o, o)
    rc, o = run([LINT, os.path.join(FX, "ruim.svelte"), "--json"])
    try:
        js = json.loads(o)
        check("lint --json valid with origin", len(js) > 10 and all("origem" in r and "citacao" in r for r in js))
    except Exception as ex:
        check("lint --json valid with origin", False, str(ex))
    rc, o = run([LINT, os.path.join(FX, "runes.svelte")])
    check("lint runes -> SVL-X01 NOT COVERED, no state rules", "SVL-X01" in o and "SVL-S02" not in o and rc == 0, o)
    rc, o = run([LINT, os.path.join(FX, "+page.svelte")])
    check("lint +page.svelte -> SVL-X02", "SVL-X02" in o, o)
    rc, o = run([LINT, os.path.join(FX, "pagina.astro")])
    check(".astro -> only SVL-X02 (NOT COVERED)", rules_of(o) == {"SVL-X02"}, o)
    rc, o = run([LINT, os.path.join(FX, "ignora-instrucoes.svelte")])
    check("lint with injection in comments: ignores instruction and reports A01", "SVL-A01" in o and rc == 0 and "rm -rf" not in o, o)
    rc, o = run([LINT, "-"], stdin="<script>\n  let n = 1\n  const k = 2\n</script>\n<input bind:value={k}>\n")
    check("lint stdin: bind:value on const -> error", rc == 1 and "SVL-B01" in o, o)
    rc, o = run([LINT, "--rules"])
    check("lint --rules lists rules with page", has(o, "SVL-A01", "SVHB p.15-16", "SVL-X01"), o)
    rc, o = run([LINT, "arquivo-que-nao-existe.svelte"])
    check("lint nonexistent file -> exit 2", rc == 2, o)
    rc, o = run([LINT])
    check("lint without arguments -> exit 2", rc == 2, o)

    # ---- compare
    rc, o = run([CMP, "table"])
    check("compare table cites the 3 sources", has(o, "NOT COVERED", "SVHB", "SKGS", "ASTRO", "2019"), o)
    rc, o = run([CMP, "show", "roteamento"])
    check("compare show roteamento: Svelte partial, Kit router, Astro NOT COVERED", has(o, "SVHB p.49", "SKGS p.2", "NOT COVERED"), o)
    rc, o = run([CMP, "show", "typescript"])
    check("compare show typescript -> Astro partial, rest NOT COVERED", "ASTRO p.2" in o and o.count("NOT COVERED") == 2, o)
    rc, o = run([CMP, "show", "inexistente-xyz"])
    check("compare show nonexistent criterion -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([CMP, "compare", "svelte", "astro"])
    check("compare svelte astro -> no documented relation", has(o, "no relation", "NOT COVERED"), o)
    rc, o = run([CMP, "compare", "react", "astro"])
    check("compare invalid framework -> exit 2", rc == 2, o)
    rc, o = run([CMP, "which", "qual", "escolher", "astro", "ou", "sveltekit"])
    check("compare which choice -> DECISION NOT COVERED", has(o, "DECISION", "NOT COVERED", "extrapolation"), o)
    rc, o = run([CMP, "coverage"])
    check("compare coverage lists uncovered criteria", has(o, "testes", "deploy"), o)
    rc, o = run([CMP, "commands"])
    check("compare commands prints the 2 cited commands", has(o, "npm create vite@latest", "npm create astro@latest", "are NOT executed"), o)

    # ---- checklist
    rc, o = run([CK, "list"])
    check("checklist list has SVHB/SKGS/ASTRO items", has(o, "CK05", "SVHB p.15-16", "SKGS p.2", "ASTRO p.2"), o)
    rc, o = run([CK, "list", "astro"])
    check("checklist list astro -> NOT COVERED .astro", "NOT COVERED" in o and "CK17" in o, o)
    rc, o = run([CK, "scan", os.path.join(FX, "projeto-vite")])
    check("scan projeto-vite: template structure and exit 0", has(o, "'src/App.svelte': True", "no findings") and rc == 0, o)
    rc, o = run([CK, "scan", os.path.join(FX, "projeto-kit")])
    check("scan projeto-kit: SvelteKit NOT COVERED and exit 1 (lint errors)", has(o, "@sveltejs/kit", "NOT COVERED") and rc == 1, o)
    rc, o = run([CK, "scan", os.path.join(FX, "nao-existe")])
    check("scan nonexistent folder -> exit 2", rc == 2, o)
    rc, o = run([CK, "scan", os.path.join(FX, "projeto-kit"), "--json"])
    try:
        js = json.loads(o)
        check("scan --json valid", "lint" in js and js["package_json"].get("@sveltejs/kit"))
    except Exception as ex:
        check("scan --json valid", False, str(ex))

    # ---- citations
    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations passes", rc == 0, o)
        m = re.search(r"Checks: (\d+) positive, (\d+) negative", o)
        check("verify_citations: >=60 positive and >=15 negative", bool(m) and int(m.group(1)) >= 60 and int(m.group(2)) >= 15, o)
    else:
        print("INFO: --src not provided; verify_citations.py was not run.")

    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
