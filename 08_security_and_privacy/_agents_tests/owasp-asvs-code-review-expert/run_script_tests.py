# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic test cases for the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/security] [--pdf PATH/09_security_and_privacy]
    --src : enables verify_citations.py and the re-extraction of the ASVS JSON from the text (compares with the package JSON)
    --pdf : (optional, requires PyMuPDF) re-extracts by PDF COORDINATES and compares with the package JSON (0 divergences expected)
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
OK, FAIL = [], []


def run(args, stdin=None):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG, input=stdin)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:400]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    ap.add_argument("--pdf")
    a = ap.parse_args()
    L = os.path.join("scripts", "asvs_lookup.py")
    C = os.path.join("scripts", "asvs_checklist.py")
    X = os.path.join("scripts", "ocrg_lint.py")
    FX = os.path.join("tests", "fixtures")

    # ---------------- lookup
    c, o = run([L, "V2.1.1"])
    check("S01 lookup V2.1.1 -> L1/L2/L3 and page 23", "ASVS p.23" in o and "R/R/R" in o and "12 characters" in o, o)
    c, o = run([L, "5.3.4", "--json"])
    d = json.loads(o)
    check("S02 lookup 5.3.4 json -> page 39 and CWE 89", d[0]["asvs_page"] == 39 and d[0]["cwe"] == "89", o)
    c, o = run([L, "senha", "--level", "L1", "--limit", "20"])
    check("S03 Portuguese topic 'senha' L1 includes V2.1.1 and does not include V2.4.1 (2.4 is not L1)", "V2.1.1 " in o and "V2.4.1 " not in o, o)
    c, o = run([L, "password", "--level", "L1", "--limit", "20"])
    check("S03b English topic 'password' L1 includes V2.1.1 and does not include V2.4.1 (2.4 is not L1)", "V2.1.1 " in o and "V2.4.1 " not in o, o)
    c, o = run([L, "sql injection"])
    check("S04 'sql injection' -> V5.3.4 and OCRG topic p.45", "V5.3.4" in o and "OCRG p.45" in o, o)
    c, o = run([L, "jwt"])
    check("S05 jwt -> V3.5.3 and NOT COVERED in the OCRG", "V3.5.3" in o and "NOT COVERED in the OCRG" in o, o)
    c, o = run([L, "bcrypt"])
    check("S06 bcrypt -> V2.4.4 and NOT COVERED in the OCRG", "V2.4.4" in o and "NOT COVERED in the OCRG" in o, o)
    c, o = run([L, "kubernetes"])
    check("S07 kubernetes -> NOT COVERED in OCRG and ASVS", "NOT COVERED" in o and "OCRG" in o and "ASVS" in o, o)
    c, o = run([L, "--chapters"])
    check("S08 --chapters lists V14 p.61 and Appendix C", "V14 " in o and "p.61" in o and "-C" in o, o)
    c, o = run([L, "--validate"])
    check("S09 --validate OK (286 rows, 278 active, 8 removed, 34 IoT)", c == 0 and "286 rows, 278 active, 8 removed" in o, o)
    c, o = run([L, "--cwe", "89"])
    check("S10 --cwe 89 -> V5.3.4 and V5.3.5", "V5.3.4" in o and "V5.3.5" in o, o)
    c, o = run([L, "--ocrg", "csrf"])
    check("S11 --ocrg csrf -> OCRG p.141-146", "OCRG p.141-146" in o and "printed 140-145" in o, o)
    c, o = run([L, "--page-ocrg", "152"])
    check("S12 --page-ocrg 152 -> printed 151", "printed 151" in o, o)
    c, o = run([L, "9.9.9"])
    check("S13 nonexistent ID is flagged", "does not exist" in o, o)
    c, o = run([L, "--gaps"])
    check("S14 --gaps lists absent terms", "scrypt" in o and "OCRG:" in o, o)
    c, o = run([L, "--section", "3.4"])
    check("S15 --section 3.4 -> 5 cookie requirements (V3.4.1..V3.4.5)", "5 requirement(s)" in o and "V3.4.5" in o, o)
    c, o = run([L, "V2.10.1"])
    check("S16 V2.10.1 carries level notes (OS assisted / HSM)", "OS assisted" in o and "HSM" in o, o)
    c, o = run([L, "1.4.2"])
    check("S17 removed requirement appears as REMOVED", "REMOVED" in o or "DELETED" in o, o)

    # ---------------- checklist
    c, o = run([C, "generate", "--level", "L1"])
    check("C01 generate L1 -> 128 items, validation OK", c == 0 and "128 items vs 128" in o and "**OK**" in o, o)
    c, o = run([C, "generate", "--level", "L2"])
    check("C02 generate L2 -> 258 items", c == 0 and "258 items vs 258" in o, o)
    c, o = run([C, "generate", "--level", "L3"])
    check("C03 generate L3 -> 278 items", c == 0 and "278 items vs 278" in o, o)
    c, o = run([C, "generate", "--level", "L1", "--chapters", "3,4", "--format", "json"])
    d = json.loads(o)
    ids = [i["id"] for i in d["items"]]
    check("C04 L1 chapters 3,4 -> 20 items (12 + 8), all V3.x/V4.x", len(ids) == 20 and all(i.startswith(("V3.", "V4.")) for i in ids) and d["header"]["count_validation"] == "OK", o[:400])
    c, o = run([C, "generate", "--level", "L2", "--only-delta", "--format", "json"])
    d = json.loads(o)
    check("C05 L2 delta = 258 - 128 = 130 items", d["header"]["items"] == 130 and d["header"]["independent_count"] == 130, o[:300])
    c, o = run([C, "generate", "--level", "L3", "--only-delta", "--format", "json"])
    d = json.loads(o)
    check("C06 L3 delta = 278 - 258 = 20 items (L3 only)", d["header"]["items"] == 20, o[:300])
    c, o = run([C, "generate", "--level", "L1", "--sections", "5.3", "--format", "csv"])
    check("C07 csv L1 section 5.3 -> 10 data rows", len([l for l in o.splitlines() if l.startswith("V5.3.")]) == 10, o[:300])
    c, o = run([C, "generate", "--level", "L2", "--chapters", "2", "--include-recommended"])
    check("C08 L2 ch.2 with recommended includes V2.8.7", "V2.8.7" in o, o[:200])
    c, o = run([C, "generate", "--level", "L1", "--chapters", "1"])
    check("C09 L1 ch.1 -> 0 items (V1 has no L1)", "0 items vs 0" in o, o[:300])
    c, o = run([C, "ocrg"])
    check("C10 ocrg -> 78 rows", "78 rows" in o, o[:200])
    c, o = run([C, "stats"])
    check("C11 stats confirms nesting L1 ⊂ L2 ⊂ L3", "L1 without L2 = 0; L2 without L3 = 0" in o and "128" in o, o)
    # evaluation: everything pass at L1
    d = json.loads(run([C, "generate", "--level", "L1", "--format", "json"])[1])
    allpass = {i["id"].lstrip("V"): "pass" for i in d["items"]}
    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "all.json")
        json.dump(allpass, open(fp, "w", encoding="utf-8"))
        c, o = run([C, "evaluate", fp, "--level", "L1"])
        check("C12 evaluate all pass L1 -> verdict reached (self-assessed)", "ALL required requirements of L1" in o, o[-400:])
        c, o = run([C, "evaluate", fp, "--level", "L2"])
        check("C13 evaluate L1 pass does not reach L2", "NOT reached" in o, o[-400:])
        part = dict(allpass)
        part["2.1.1"] = "fail"
        part["3.1.1"] = {"status": "na"}
        fp2 = os.path.join(td, "part.json")
        json.dump(part, open(fp2, "w", encoding="utf-8"))
        c, o = run([C, "evaluate", fp2, "--level", "L1"])
        check("C14 fail and N/A without justification prevent the verdict", "V2.1.1" in o and "N/A without justification" in o and "NOT reached" in o, o[-600:])
        part["3.1.1"] = {"status": "na", "reason": "API without web client; no tokens in URL"}
        json.dump(part, open(fp2, "w", encoding="utf-8"))
        c, o = run([C, "evaluate", fp2, "--level", "L1"])
        check("C15 justified N/A is accepted (only the V2.1.1 failure remains)", "N/A without justification" not in o and "failures=1" in o, o[-400:])

    # ---------------- linter
    c, o = run([X, os.path.join(FX, "vuln_samples.java"), "--format", "json"])
    d = json.loads(o)
    rules = {f["rule"] for f in d["findings"]}
    need = {"SQL-CONCAT", "REDIRECT-JAVA-PARAM", "ERR-PRINTSTACK-OUT", "ERR-CATCH-ALL", "ERR-SWALLOW", "CRYPTO-DES", "CRYPTO-MD5-SHA1", "LOG-PASSWORD", "SECRET-IN-CODE", "JNI-PUBLIC-NATIVE", "THREAD-STATIC-STATE"}
    check("L01 vulnerable java triggers the 11 expected rules", need <= rules, str(need - rules))
    c, o = run([X, os.path.join(FX, "safe_samples.java"), "--include-info"])
    check("L02 safe java (parameterized, SHA-256, specific catch) -> 0 findings", "0 finding(s)" in o, o)
    c, o = run([X, os.path.join(FX, "vuln_samples.js"), "--format", "json"])
    rules = {f["rule"] for f in json.loads(o)["findings"]}
    check("L03 js triggers eval, HTML sink, string timer, postMessage, indexOf, CORS, ws://, new Function",
          {"JS-EVAL", "JS-HTML-SINK", "JS-TIMER-STRING", "JS-POSTMESSAGE-STAR", "JS-ORIGIN-INDEXOF", "CORS-WILDCARD", "WEBSOCKET-WS", "JS-NEW-FUNCTION"} <= rules, str(rules))
    c, o = run([X, os.path.join(FX, "vuln_samples.php"), "--format", "json"])
    rules = {f["rule"] for f in json.loads(o)["findings"]}
    check("L04 php triggers SQL concat, addslashes, redirect", {"SQL-CONCAT", "SQL-PHP-CONCAT", "PHP-ESCAPE-FUNCS", "REDIRECT-PHP-LOCATION"} <= rules, str(rules))
    c, o = run([X, os.path.join(FX, "vuln_samples.c"), "--format", "json"])
    rules = {f["rule"] for f in json.loads(o)["findings"]}
    check("L05 c triggers unsafe functions, scanf and format string", {"C-UNSAFE-STR", "C-SCANF", "C-FORMAT-STRING"} <= rules, str(rules))
    c, o = run([X, os.path.join(FX, "vuln_web.config"), "--format", "json"])
    rules = {f["rule"] for f in json.loads(o)["findings"]}
    check("L06 web.config triggers debug/trace, customErrors, validateRequest, cookies, session, credentials",
          {"CFG-DEBUG-TRACE", "CFG-CUSTOMERRORS-OFF", "CFG-VALIDATE-REQUEST-OFF", "CFG-COOKIE-FLAGS", "CFG-SESSION-URL", "CFG-FORMS-CREDENTIALS"} <= rules, str(rules))
    c, o = run([X, os.path.join(FX, "vuln_samples.java"), "--fail-on", "red_flag"])
    check("L07 --fail-on red_flag returns 1 with red flags", c == 1, o[-200:])
    c, o = run([X, os.path.join(FX, "safe_samples.java"), "--fail-on", "red_flag"])
    check("L08 --fail-on red_flag returns 0 without red flags", c == 0, o[-200:])
    c, o = run([X, "-", "--lang", "python"], stdin="import pickle\nx = pickle.loads(data)\nsubprocess.run(cmd, shell=True)\n")
    check("L09 [extrapolation] rules are off by default", "0 finding(s)" in o, o)
    c, o = run([X, "-", "--lang", "python", "--include-extrapolation"], stdin="import pickle\nx = pickle.loads(data)\nsubprocess.run(cmd, shell=True)\n")
    check("L10 --include-extrapolation turns on X-PY-UNSAFE-DESERIALIZE and X-SHELL-TRUE", "X-PY-UNSAFE-DESERIALIZE" in o and "X-SHELL-TRUE" in o and "[extrapolation]" in o, o)
    c, o = run([X, "--rules"])
    check("L11 --rules: 54 rules (49 + 5 extrapolation)", "Total: 54 rules (49 from source/inference, 5 extrapolation)" in o, o[-200:])
    c, o = run([X, "--explain", "sql-concat"])
    check("L12 --explain SQL-CONCAT cites OCRG p.51 and ASVS V5.3.4", "OCRG p.45,49,50,51" in o and "V5.3.4" in o, o)
    c, o = run([X, "-"], stdin="// String q = \"SELECT * FROM t WHERE a='\" + x + \"'\";\n")
    check("L13 comment line is ignored by default", "0 finding(s)" in o, o)
    c, o = run([X, "-", "--include-comments"], stdin="// String q = \"SELECT * FROM t WHERE a='\" + x + \"'\";\n")
    check("L14 --include-comments analyzes comments", "SQL-CONCAT" in o, o)
    c, o = run([X, "-"], stdin="String q = \"SELECT id FROM t WHERE a = ?\";\nps.setString(1, v);\n")
    check("L15 parameterized query does not trigger SQL-CONCAT", "0 finding(s)" in o, o)
    c, o = run([X, os.path.join(FX, "safe_samples.java"), "--fail-on", "verificar"])
    check("L16 legacy Portuguese alias --fail-on verificar is still accepted", c == 0, o[-200:])
    c, o = run([X, os.path.join(FX, "vuln_samples.java"), "--fail-on", "verify"])
    check("L17 --fail-on verify returns 1 with findings", c == 1, o[-200:])

    # ---------------- re-extraction (optional)
    if a.src:
        src = os.path.abspath(a.src)
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "r.json")
            c, o = run([os.path.join("scripts", "asvs_extract_text.py"), os.path.join(src, "OWASP-ASVS-4.0.3.txt"), "--out", out, "--check"])
            new = json.load(open(out, "r", encoding="utf-8"))
            old = json.load(open(os.path.join(PKG, "scripts", "asvs_requirements.json"), "r", encoding="utf-8"))
            check("E01 re-extraction of the ASVS from the text == package JSON", new["requirements"] == old["requirements"], o[-300:])
            check("E02 counts: 286 V1-V14 rows, 8 removed, L1=128 L2=258 L3=278",
                  "rows V1-V14: 286" in o and "deleted: 8" in o and "L1 required: 128" in o and "L2 required: 258" in o and "L3 required: 278" in o, o)
        c, o = run([os.path.join("tests", "verify_citations.py"), "--src", src])
        check("V01 verify_citations.py (range, IDs, positives, negatives, data, gaps, rules, tokens) without failures", c == 0 and "Total failures: 0" in o, o[-500:])
    if a.pdf:
        try:
            import fitz  # noqa: F401
            have = True
        except ImportError:
            have = False
        if have:
            pdf = os.path.abspath(a.pdf)
            with tempfile.TemporaryDirectory() as td:
                out = os.path.join(td, "raw.json")
                c, o = run([os.path.join("scripts", "build_asvs_from_pdf.py"), os.path.join(pdf, "OWASP-ASVS-4.0.3.pdf"), "--out", out])
                raw = {r["id"]: r for r in json.load(open(out, "r", encoding="utf-8"))["requirements"]}
                old = {r["id"]: r for r in json.load(open(os.path.join(PKG, "scripts", "asvs_requirements.json"), "r", encoding="utf-8"))["requirements"]}
                diffs = [(k, f) for k in old for f in ("page", "chapter", "section", "text", "L1", "L2", "L3", "cwe", "nist", "since", "deleted", "level_notes")
                         if raw.get(k, {}).get(f) != old[k][f]]
                check("E03 extraction by PDF COORDINATES == package JSON (0 divergences, 320 rows)", not diffs and len(raw) == len(old) == 320, str(diffs[:5]))
                out2 = os.path.join(td, "chk.json")
                c, o = run([os.path.join("scripts", "build_ocrg_checklist_from_pdf.py"), os.path.join(pdf, "OWASP-Code-Review-Guide-v2.pdf"), "--out", out2])
                new = json.load(open(out2, "r", encoding="utf-8"))["items"]
                old = json.load(open(os.path.join(PKG, "scripts", "ocrg_checklist.json"), "r", encoding="utf-8"))["items"]
                check("E04 OCRG checklist re-extracted from the PDF == package JSON (78 rows)", new == old and len(new) == 78, str(len(new)))
        else:
            print("SKIP E03/E04 (PyMuPDF not installed)")
    print("\n%d passed, %d failed" % (len(OK), len(FAIL)))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
