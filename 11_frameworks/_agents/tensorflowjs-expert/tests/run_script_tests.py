# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic script tests (no model, no network).
Usage: python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]   (--src enables verify_citations.py)
Exit 0 if all pass. Conceptual cases (which require the agent) are in tests/casos-de-teste.md.
"""
import argparse
import os
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
OK, FAIL = [], []
FX = os.path.join("tests", "fixtures")
S = lambda n: os.path.join("scripts", n)


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
    L, M, C, K = S("tfjs_lookup.py"), S("tfjs_map.py"), S("tfjs_setup_checklist.py"), S("tfjs_snippet_lint.py")

    rc, o = run([L, "tag", "de", "script"])
    check("lookup tag de script (Portuguese input) -> TFJS p.1", "TFJS p.1" in o and "NOT COVERED" not in o, o)
    rc, o = run([L, "tfjs-node-gpu"])
    check("lookup tfjs-node-gpu -> TFJS p.5", "TFJS p.5" in o, o)
    rc, o = run([L, "webgl"])
    check("lookup webgl -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "versao", "do", "tensorflow.js"])
    check("lookup version -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "mobilenet"])
    check("lookup mobilenet -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "quantum", "entanglement"])
    check("lookup nonexistent term -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([L, "--page", "TFJS", "6"])
    check("lookup --page TFJS 6 -> TypeScript", "TypeScript" in o, o)
    rc, o = run([L, "--page", "TFJB", "1"])
    check("lookup --page TFJB 1 -> discarded", "discarded" in o, o)
    rc, o = run([L, "--page", "TFJG", "9"])
    check("lookup page out of range -> error", rc == 1, o)
    rc, o = run([L, "--sources"])
    check("lookup --sources marks TFJB DO NOT USE", "DO NOT USE" in o and "TFJB" in o, o)
    rc, o = run([L, "--gaps"])
    check("lookup --gaps lists backends", "Backends" in o, o)
    rc, o = run([L, "script", "tag"])
    check("lookup script tag (English input) -> TFJS p.1", "TFJS p.1" in o and "NOT COVERED" not in o, o)
    rc, o = run([L, "ml5"])
    check("lookup ml5 -> TFJI p.4", "TFJI p.4" in o, o)

    rc, o = run([M, "--guide"])
    check("map --guide lists 8 sections", o.count("[TFJG p.1]") == 8 and "NOT COVERED" in o, o)
    rc, o = run([M, "--need", "converter modelo keras"])
    check("map need converter keras", "TFJI p.4" in o and "GraphDef" in o, o)
    rc, o = run([M, "--need", "implantar em kubernetes"])
    check("map need without resource -> NOT COVERED", "NOT COVERED" in o, o)

    rc, o = run([M, "--need", "convert keras model"])
    check("map need convert keras (English input)", "TFJI p.4" in o and "GraphDef" in o, o)

    rc, o = run([C, "--target", "node-gpu", "--os", "windows"])
    check("checklist node-gpu windows -> Linux warning", "WARNING" in o and "Linux" in o, o)
    rc, o = run([C, "--target", "node-gpu", "--os", "linux"])
    check("checklist node-gpu linux without warning", "WARNING" not in o and "npm install @tensorflow/tfjs-node-gpu" in o, o)
    rc, o = run([C, "--target", "browser-script"])
    check("checklist browser-script has CDN", "cdn.jsdelivr.net" in o, o)
    rc, o = run([C, "--target", "browser-npm"])
    check("checklist browser-npm marks Yarn NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([C, "--target", "node-pure", "--typescript", "--strict-null"])
    check("checklist typescript strict -> skipLibCheck", "skipLibCheck" in o, o)
    rc, o = run([C, "--quickstart"])
    check("quickstart TFJI commands", "yarn watch" in o and "127.0.0.1:1234" in o, o)

    rc, o = run([K, os.path.join(FX, "ok-browser.html")])
    check("lint ok-browser.html INFO only (L09)", rc == 0 and "WARN" not in o, o)
    rc, o = run([K, os.path.join(FX, "bad-no-tag.html")])
    check("lint bad-no-tag.html -> L01", rc == 1 and "L01" in o, o)
    rc, o = run([K, os.path.join(FX, "bad-order.html")])
    check("lint bad-order.html -> L02", rc == 1 and "L02" in o, o)
    rc, o = run([K, os.path.join(FX, "node-both.js")])
    check("lint node-both.js -> L03 e L04", "L03" in o and "L04" in o and "L06" in o, o)
    rc, o = run([K, os.path.join(FX, "node-nocompile.js")])
    check("lint node-nocompile.js -> L05", "L05" in o, o)
    rc, o = run([K, os.path.join(FX, "node-pure-ok.js")])
    check("lint node-pure-ok.js -> L07 INFO only", rc == 0 and "L07" in o and "WARN" not in o, o)
    rc, o = run([K, os.path.join(FX, "no-import.js")])
    check("lint no-import.js -> L01", rc == 1 and "L01" in o, o)
    rc, o = run([K, os.path.join(FX, "tsconfig-strict.json")])
    check("lint tsconfig strict -> L08", "L08" in o, o)
    rc, o = run([K, os.path.join(FX, "tsconfig-ok.json")])
    check("lint tsconfig with skipLibCheck -> no findings", "L08" not in o, o)
    rc, o = run([K, os.path.join(FX, "package-both.json")])
    check("lint package.json -> L03/L04", rc == 1 and "L03" in o and "L04" in o, o)
    rc, o = run([K, os.path.join(FX, "ok-browser.html"), "--strict"])
    check("lint --strict fails on INFO", rc == 1, o)

    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations", rc == 0, o)
    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
