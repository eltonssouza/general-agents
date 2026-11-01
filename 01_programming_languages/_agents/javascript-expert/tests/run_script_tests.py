# -*- coding: utf-8 -*-
"""
run_script_tests.py - ACTUALLY runs the javascript-expert package scripts and checks the expected behavior.

Usage:
  python -I tests/run_script_tests.py                 # tests that do not need the PDF text
  python -I tests/run_script_tests.py --src <folder>  # also checks pages against the extracted text
                                                      # (<folder> = output of tests/extract_pages.py)
No network; stdlib only; runs each script as a subprocess (`python -I`). Exit 0 if everything passed.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
SK = os.path.join(PKG, "skills")
SCRIPTS = os.path.join(PKG, "scripts")
FIX = os.path.join(HERE, "fixtures")
NPAGES = {"Spec": 876, "EJpt": 504, "EJ1": 247}

results = []


def run(args, stdin=None):
    p = subprocess.run([sys.executable, "-I"] + args, capture_output=True, text=True, encoding="utf-8", input=stdin)
    return p.returncode, p.stdout, p.stderr


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(("OK    " if cond else "FAIL  ") + name + ("" if cond else "  -> " + str(detail)[:300]))


def test_spec_lookup(src):
    s = os.path.join(SK, "js-spec-lookup", "scripts", "spec_lookup.py")
    rc, out, _ = run([s, "SameValue"])
    check("spec_lookup SameValue finds the section", rc == 0 and "SameValue" in out and re.search(r"p\.\d+", out), out[:200])
    rc, out, _ = run([s, "--section", "13.11"])
    check("spec_lookup --section 13.11 lists subsections", rc == 0 and "13.11" in out, out[:200])
    rc, out, _ = run([s, "--page", "310"])
    check("spec_lookup --page 310 shows the section in progress", rc == 0 and "Section in progress" in out, out[:200])
    rc, out, _ = run([s, "--top"])
    check("spec_lookup --top lista Annex A..F", rc == 0 and "Annex A" in out and "Annex F" in out, out[-300:])
    rc, out, _ = run([s, "xyzzy-inexistente"])
    check("spec_lookup unknown term does not claim absence", rc == 0 and "does NOT prove" in out, out[:200])
    rc, out, _ = run([s])
    check("spec_lookup without arguments: usage and exit 2", rc == 2, rc)
    toc = json.load(open(os.path.join(SK, "js-spec-lookup", "scripts", "spec_toc.json"), encoding="utf-8"))
    check("spec_toc.json: 2224 sections, pages in 1..876", len(toc) == 2224 and all(1 <= p <= 876 for _, _, p in toc), len(toc))
    if src:
        sys.path.insert(0, HERE)
        import verify_citations as vc
        pages = vc.load_pages(os.path.join(src, "ecma262.txt"))
        sq = {k: re.sub(r"\s+", "", v.lower()) for k, v in pages.items()}
        bad = [t for _, t, p in toc if re.sub(r"\s+", "", vc.norm(t).lower()) not in sq.get(p, "")]
        check("spec_toc.json: each section title appears on the indicated page (2224 checked)", not bad, bad[:5])


def test_scan():
    s = os.path.join(SK, "js-code-review", "scripts", "scan_js_smells.py")
    rc, out, _ = run([s, os.path.join(SK, "js-code-review", "scripts", "fixtures", "sample.js")])
    want = ["var-declaration", "loose-equality", "global-isnan", "async-foreach", "for-in-prototype",
            "eval-or-code-string", "empty-catch", "array-sort-default"]
    missing = [w for w in want if w not in out]
    check("scan_js_smells finds the 8 expected rules in sample.js", rc == 0 and not missing, missing)
    rc, out, _ = run([s, os.path.join(FIX, "clean.js")])
    check("scan_js_smells: clean fixture => 0 findings", rc == 0 and " 0 finding(s)" in out, out[:200])
    rc, out, _ = run([s, os.path.join(FIX, "injection.js")])
    check("scan_js_smells: injection in comments is treated as data (flags var and ==, nothing else)",
          rc == 0 and "var-declaration" in out and "loose-equality" in out and "2 finding(s)" in out, out[:300])
    rc, out, _ = run([s, "--json", os.path.join(FIX, "injection.js")])
    try:
        data = json.loads(out)
        ok = data["files_scanned"] == 1 and len(data["findings"]) == 2
    except Exception as e:  # noqa
        ok = False
    check("scan_js_smells --json valid", ok, out[:200])
    # every rule cites a valid page and label/origin
    src = open(s, encoding="utf-8").read()
    cites = re.findall(r"\b(Spec|EJpt|EJ1) p\.(\d+)(?:[-–](\d+))?", src)
    bad = [c for c in cites if int(c[1]) > NPAGES[c[0]] or (c[2] and int(c[2]) > NPAGES[c[0]])]
    check("scan_js_smells: %d cited pages within the size of the PDFs" % len(cites), cites and not bad, bad)
    rc, out, _ = run([s, "/caminho/que/nao/existe"])
    check("scan_js_smells: nonexistent path does not break", rc == 0, rc)


def test_stack():
    s = os.path.join(SK, "js-error-triage", "scripts", "parse_js_stack.py")
    rc, out, _ = run([s, os.path.join(SK, "js-error-triage", "scripts", "fixtures", "trace.txt")])
    check("parse_js_stack: trace with [cause] => 2 errors (TypeError and ReferenceError)",
          rc == 0 and "2 error(s)" in out and "TypeError" in out and "ReferenceError" in out and "[cause]" in out, out[:300])
    rc, out, _ = run([s, os.path.join(FIX, "trace-injection.txt")])
    check("parse_js_stack: text injected into the trace is ignored (1 error, nothing executed)",
          rc == 0 and "1 error(s)" in out and "IGNORE" not in out, out[:300])
    frames = "RangeError: Maximum call stack size exceeded\n" + "".join("    at recursive (r.js:%d:1)\n" % i for i in range(12))
    rc, out, _ = run([s, "-"], stdin=frames)
    check("parse_js_stack: 12 repeated frames => recursion warning (threshold is an [extrapolation])",
          rc == 0 and "WARNING" in out and "extrapolation" in out, out[:300])
    rc, out, _ = run([s, "-"], stdin="any text without an error\n")
    check("parse_js_stack: input without a JS error is handled", rc == 0 and "No JS error header" in out, out[:200])


def test_version():
    s = os.path.join(SK, "js-version-features", "scripts", "js_version_lookup.py")
    rc, out, _ = run([s, "groupBy"])
    check("js_version_lookup groupBy => unversioned", rc == 0 and "[unversioned]" in out, out[:200])
    rc, out, _ = run([s, "class"])
    check("js_version_lookup class => ECMAScript 2015", rc == 0 and "2015" in out, out[:200])
    rc, out, _ = run([s, "substr"])
    check("js_version_lookup substr => annex-b", rc == 0 and "[annex-b]" in out, out[:200])
    rc, out, _ = run([s, "temporal"])
    check("js_version_lookup temporal => outside the sources (missing)", rc == 0 and "[missing]" in out, out[:200])
    rc, out, _ = run([s, "--summary"])
    check("js_version_lookup --summary", rc == 0 and "EJpt" in out and "504" in out, out[:300])
    rc, out, _ = run([s, "--category", "host"])
    check("js_version_lookup --category host", rc == 0 and "[host]" in out, out[:200])
    rc, out, _ = run([s, "zzzz"])
    check("js_version_lookup unknown term: guides to 'version not stated in the sources'", rc == 0 and "version not stated in the sources" in out, out[:300])
    data = json.load(open(os.path.join(SK, "js-version-features", "scripts", "js_version_data.json"), encoding="utf-8"))
    bad = []
    for it in data["items"]:
        for m in re.finditer(r"\b(Spec|EJpt|EJ1) p\.([^;]*)", it["citations"]):
            for n in re.findall(r"\d+", m.group(2)):
                if int(n) > NPAGES[m.group(1)]:
                    bad.append((it["name"], m.group(1), n))
    check("js_version_data.json: all cited pages exist", not bad, bad[:3])


def test_topic():
    s = os.path.join(SCRIPTS, "js_topic_lookup.py")
    rc, out, _ = run([s, "--exact", "Promise.any"])
    check("js_topic_lookup Promise.any => Spec p.774-775", rc == 0 and "774-775" in out, out[:200])
    rc, out, _ = run([s, "structuredClone"])
    check("js_topic_lookup structuredClone => NOT COVERED (exit 1) and verified-absence note",
          rc == 1 and "NOT COVERED" in out and "Verified as absent" in out, (rc, out[:200]))
    rc, out, _ = run([s, "--missing"])
    check("js_topic_lookup --missing lists what the sources do not cover", rc == 0 and "TypeScript" in out, out[:200])
    rc, out, _ = run([s, "closure"])
    check("js_topic_lookup closure finds an entry with pages from the 3 sources", rc == 0 and "Spec" in out and "EJpt" in out and "EJ1" in out, out[:300])
    rc, out, _ = run([s, "--check"])
    check("js_topic_lookup --check: index up to date with references/", rc == 0, out)
    data = json.load(open(os.path.join(SCRIPTS, "js_topic_index.json"), encoding="utf-8"))
    bad = []
    for e in data["entradas"]:
        for sig, lst in e["paginas"].items():
            for r in lst:
                for n in re.findall(r"\d+", r):
                    if int(n) > NPAGES[sig] or int(n) < 1:
                        bad.append((e["termo"], sig, r))
    check("js_topic_index.json: %d entries, all pages within the PDFs" % len(data["entradas"]), not bad and len(data["entradas"]) > 1000, bad[:3])
    rc, out, _ = run([s])
    check("js_topic_lookup without arguments: usage and exit 2", rc == 2, rc)


def test_verifiers(src):
    v = os.path.join(HERE, "verify_citations.py")
    a = os.path.join(HERE, "audit_tokens.py")
    chk = json.load(open(os.path.join(HERE, "citation-checks.json"), encoding="utf-8"))
    check("citation-checks.json: >=60 positives and >=15 negatives (%d / %d)" % (len(chk["positive"]), len(chk["negative"])),
          len(chk["positive"]) >= 60 and len(chk["negative"]) >= 15)
    if not src:
        print("      (without --src: verify_citations.py and audit_tokens.py not run)")
        return
    rc, out, _ = run([v, "--src", src])
    check("verify_citations.py: 0 failures", rc == 0, out[-300:])
    rc, out, _ = run([a, "--src", src])
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    check("audit_tokens.py: 0 pages out of range and 0 unsupported terms (NEAR = recorded tolerance)", rc == 0, tail)
    # self-test: the verifier must FAIL on a wrong check
    with tempfile.TemporaryDirectory() as d:
        bad = {"positive": [{"id": "X1", "book": "Spec", "pages": [26], "terms": ["Math.round(3.5) returns 4"], "claim": "wrong page"}],
               "negative": [{"id": "X2", "book": "Spec", "terms": ["Promise.all"], "claim": "false negative"}]}
        p = os.path.join(d, "bad.json")
        json.dump(bad, open(p, "w", encoding="utf-8"))
        rc, out, _ = run([v, "--src", src, "--checks", p])
        check("verify_citations.py: detects wrong page and false negative (self-test, exit 1)", rc == 1 and "X1" in out and "X2" in out, out[-200:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=None)
    a = ap.parse_args()
    test_spec_lookup(a.src)
    test_scan()
    test_stack()
    test_version()
    test_topic()
    test_verifiers(a.src)
    nf = [n for n, ok, _ in results if not ok]
    print("\n%d tests, %d failures" % (len(results), len(nf)))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
