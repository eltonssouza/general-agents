# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests of the package scripts (no model, no network).

Usage:  python -I tests/run_script_tests.py [--src PATH/scratch/frameworks]
  --src enables: verify_citations.py and the check that ng_index.json is up to date with the .txt files.
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
OK, FAIL = [], []
S = lambda n: os.path.join("scripts", n)  # noqa: E731
FX = os.path.join("tests", "fixtures")


def run(args, stdin=None):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG, input=stdin)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def has(o, *subs):
    return all(s in o for s in subs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()

    # ---- lookup
    rc, o = run([S("ng_lookup.py"), "signals"])
    check("lookup signals -> NG18 p.1,2 and NG22 p.2", rc == 0 and has(o, "NG18: p.1,2", "NG22: p.2"), o)
    rc, o = run([S("ng_lookup.py"), "sinal"])
    check("lookup sinal (Portuguese keyword) -> signals", rc == 0 and has(o, "signals", "NG18: p.1,2"), o)
    rc, o = run([S("ng_lookup.py"), "@defer"])
    check("lookup @defer -> NG18-20 and 'not detected' in NG21/22", has(o, "NG18: p.2", "NG19: p.3", "NG20: p.2", "NG21: not detected", "NG22: not detected"), o)
    rc, o = run([S("ng_lookup.py"), "standalone"])
    check("lookup standalone -> NOT COVERED", has(o, "NOT COVERED"), o)
    rc, o = run([S("ng_lookup.py"), "zoneless", "control", "flow"])
    check("lookup zoneless -> NOT COVERED", "NOT COVERED: 'zoneless'" in o, o)
    rc, o = run([S("ng_lookup.py"), "kubernetes"])
    check("lookup nonexistent term -> NOT COVERED", has(o, "NOT COVERED"), o)
    rc, o = run([S("ng_lookup.py"), "--gaps"])
    check("--gaps lists standalone/zoneless and no FOUND", has(o, "standalone", "zoneless") and "FOUND" not in o, o)
    rc, o = run([S("ng_lookup.py"), "--page", "19", "1"])
    check("--page 19 1 -> navigation-only class", "navigation-or-footer-only" in o, o)
    rc, o = run([S("ng_lookup.py"), "--page", "21", "99"])
    check("--page outside the collection -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([S("ng_lookup.py"), "--versions"])
    check("--versions: stamps v21.2.20 and v22.1.2", has(o, "v21.2.20", "v22.1.2", "2010-2024"), o)

    # ---- diff
    rc, o = run([S("ng_diff.py"), "diff", "--from", "18", "--to", "22"])
    check("diff 18->22: @defer only in the origin", rc == 0 and "@defer block in templates  (NG18 p.2)" in o, o)
    check("diff 18->22: 'users love' only in the target", "Tagline with 'users love'  (NG22 p.1)" in o, o)
    check("diff 18->22: Bluesky and Community translations in the target", has(o, "Bluesky", "Community translations"), o)
    check("diff 18->22: absence != removal warning", "does NOT mean it was removed" in o, o)
    rc, o = run([S("ng_diff.py"), "diff", "--from", "21", "--to", "22"])
    check("diff 21->22: no concept differences, only the stamp", has(o, "(0)", "identical to NG21"), o)
    rc, o = run([S("ng_diff.py"), "diff", "--from", "18", "--to", "19"])
    check("diff 18->19: only Bluesky/footer", has(o, "Bluesky", "2010-2025") and "[presence]" not in o, o)
    rc, o = run([S("ng_diff.py"), "diff", "--from", "19", "--to", "20"])
    check("diff 19->20: Greek disappears", has(o, "Ελληνικά"), o)
    rc, o = run([S("ng_diff.py"), "diff", "--from", "20", "--to", "21", "--json"])
    j = json.loads(o) if rc == 0 else {}
    ids = [c["id"] for c in j.get("concepts", {}).get("only_from", [])]
    check("diff 20->21 json: defer-block in only_from", "defer-block" in ids and "warning" in j, o[:300])
    rc, o = run([S("ng_diff.py"), "diff", "--from", "20", "--to", "19"])
    check("reverse diff works", rc == 0 and "NG20 -> NG19" in o, o)
    rc, o = run([S("ng_diff.py"), "diff", "--from", "17", "--to", "22"])
    check("diff nonexistent version -> error", rc != 0, o)
    rc, o = run([S("ng_diff.py"), "diff", "--from", "18", "--to", "22", "--group", "recurso"])
    check("diff --group accepts the Portuguese alias 'recurso'", rc == 0 and "@defer block in templates" in o and "Bluesky" not in o.split("== D.")[0], o)
    rc, o = run([S("ng_diff.py"), "concept", "defer"])
    check("concept defer", has(o, "defer-block", "NG21: not detected in the capture"), o)
    rc, o = run([S("ng_diff.py"), "concept", "zoneless"])
    check("concept zoneless -> NOT COVERED", "NOT COVERED" in o, o)
    rc, o = run([S("ng_diff.py"), "matrix", "--group", "meta"])
    check("matrix meta", has(o, "bluesky", "build-stamp"), o)
    rc, o = run([S("ng_diff.py"), "meta"])
    check("meta: useless pages NG19/NG20/NG21", has(o, "NG19", "['1']", "NG20", "['7']"), o)
    if a.src:
        rc, o = run([S("ng_diff.py"), "diff", "--from", "20", "--to", "21", "--raw", "--src", a.src])
        check("diff --raw 20->21 finds 'users love' and 'opinionated'", rc == 0 and has(o, "users love", "opinionated component model"), o)
        rc, o = run([S("ng_diff.py"), "diff", "--from", "21", "--to", "22", "--raw", "--src", a.src])
        check("diff --raw 21->22 only stamps", rc == 0 and has(o, "v21.2.20", "v22.1.2") and "users love" not in o, o)

    # ---- lint
    rc, o = run([S("ng_lint.py"), os.path.join(FX, "snippet-ruim.ts"), "--json"])
    j = json.loads(o) if rc == 0 else {}
    rules = {i["rule"] for items in j.values() for i in items}
    check("lint bad: security rules", {"sec-dom-innerhtml", "sec-bypass-trust"} <= rules, str(rules))
    check("lint bad: labeled extrapolations", {"legacy-structural", "ngmodule", "any-type", "subscribe-leak"} <= rules, str(rules))
    check("lint: [innerHTML] binding is NOT flagged", not any(i["code"].startswith('<div [innerHTML]') for items in j.values() for i in items), o[:300])
    check("lint: injection comment is ignored (not a finding)", not any("ignore all" in i["code"] for items in j.values() for i in items), o[:300])
    check("lint: <img ngSrc> not flagged", sum(1 for items in j.values() for i in items if i["rule"] == "img-ngsrc") == 1, o[:300])
    check("lint: every rule has an origin", all(i["origin"] for items in j.values() for i in items), o[:300])
    rc, o = run([S("ng_lint.py"), os.path.join(FX, "snippet-defer.html"), "--target", "21"])
    check("lint @defer target 21: absence != removal warning", has(o, "does NOT prove removal", "NG21 p.3"), o)
    rc, o = run([S("ng_lint.py"), os.path.join(FX, "snippet-defer.html"), "--target", "20"])
    check("lint @defer target 20: cites the Overview", has(o, "cites @defer"), o)
    rc, o = run([S("ng_lint.py"), os.path.join(FX, "snippet-limpo.html")])
    check("lint clean: 0 findings", "0 finding(s)" in o, o)
    rc, o = run([S("ng_lint.py"), os.path.join(FX, "snippet-ruim.ts"), "--fail-on", "warn"])
    check("lint --fail-on warn -> exit 1", rc == 1, o)
    rc, o = run([S("ng_lint.py"), "-"], stdin="el.innerHTML = x;\n")
    check("lint via stdin", "sec-dom-innerhtml" in o, o)
    rc, o = run([S("ng_lint.py"), "--rules"])
    check("lint --rules lists origin", has(o, "defer-coverage", "[extrapolation]"), o)

    # ---- checklist
    rc, o = run([S("ng_checklist.py"), "--version", "21", "--known", "signals,ssr"])
    check("checklist 21: [x] signals and SSR; pending", has(o, "[x] Signals", "[x] Server-side rendering", "Pending study"), o)
    check("checklist 21: @defer not presented", "@defer" not in o.split("NOT detected")[0], o)
    rc, o = run([S("ng_checklist.py"), "--version", "22", "--check", "standalone,signals,defer"])
    check("checklist --check: NOT COVERED / in the Overview / not detected", has(o, "standalone", "NOT COVERED", "in the Overview (NG22 p.2", "not detected in this capture"), o)
    rc, o = run([S("ng_checklist.py"), "--version", "18", "--group", "feature", "--json"])
    j = json.loads(o) if rc == 0 else {}
    check("checklist 18 json includes defer-block", any(x["id"] == "defer-block" for x in j.get("present", [])), o[:200])
    rc, o = run([S("ng_checklist.py"), "--version", "18", "--group", "recurso", "--json"])
    j = json.loads(o) if rc == 0 else {}
    check("checklist --group accepts the Portuguese alias 'recurso'", any(x["id"] == "defer-block" for x in j.get("present", [])), o[:200])
    rc, o = run([S("ng_checklist.py"), "--version", "17"])
    check("checklist invalid version -> error", rc != 0, o)

    # ---- index up to date + citations
    if a.src:
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "idx.json")
            rc, o = run([S("ng_build_index.py"), "--src", a.src, "--out", out])
            new = json.load(open(out, encoding="utf-8"))
            old = json.load(open(os.path.join(PKG, "scripts", "ng_index.json"), encoding="utf-8"))
            check("ng_index.json up to date with the .txt files", rc == 0 and new == old, o)
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("verify_citations without failures", rc == 0 and "total failures: 0" in o, o)
    print(f"\n{len(OK)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
