# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests of the go-expert package (no network, read-only; writes only to a temporary folder).

Covers: (1) the four scripts (go_lookup, go_checklist, scan_go_smells, check_gomod) on the fixtures; (2) package hygiene
(UTF-8 without BOM, LF, no absolute user path, valid JSON, existing references, structure of agent/AGENTS.md/Copilot);
(3) for each case in tests/casos-de-teste.md, that the required facts exist in the package (cases 1-32); (4) with --src, the
citation verifiers (verify_citations.py, audit_tokens.py) and their SENSITIVITY (a wrong claim must fail).
This is NOT blind execution by an independent model: it proves that the information is in the package and that the scripts behave as described.

Usage (from the package root):  python -I tests/run_script_tests.py [--src FOLDER_WITH_THE_PDF_TXT_FILES]
Exit 0 if everything passes.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run(*args):
    p = subprocess.run([sys.executable, "-I"] + [os.path.join(ROOT, a) if i == 0 else a for i, a in enumerate(args)],
                       capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=ROOT)
    return p.returncode, p.stdout + p.stderr


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


RESULTS = []


def check(cid, desc, ok, detail=""):
    RESULTS.append((cid, desc, bool(ok), detail))


def has_all(text, items):
    return [x for x in items if x not in text]


# ---------------------------------------------------------------- scripts
LOOKUP = "scripts/go_lookup.py"
CHECKLIST = "scripts/go_checklist.py"
SCAN = "skills/go-code-review/scripts/scan_go_smells.py"
GOMOD = "skills/go-version-migration/scripts/check_gomod.py"
FIX_SCAN = "skills/go-code-review/scripts/fixtures"
FIX_OLD = "skills/go-version-migration/scripts/fixtures/old"
FIX_MID = "skills/go-version-migration/scripts/fixtures/mid"


def script_tests():
    rc, out = run(LOOKUP, "receiver ponteiro ou valor")
    miss = has_all(out, ["Value vs pointer receivers", "[from source] Eff p.29", "[from source] Eff p.24", "Little p.37", "Spec p.29, p.30", "PDF"])
    check("CT-20", "go_lookup receiver", rc == 0 and not miss, str(miss))

    rc, out = run(LOOKUP, "context e errgroup para cancelar goroutines")
    miss = has_all(out, ["NOT COVERED", "RN1.20 p.8", "RN1.21 p.7", "errgroup"])
    check("CT-21", "go_lookup NOT COVERED (context/errgroup)", not miss, "rc=%s %s" % (rc, miss))

    rc, out = run(LOOKUP, "kubernetes operator")
    check("CT-21b", "go_lookup unknown topic", rc == 3 and "NOT COVERED" in out and "Do not invent" in out, out[-200:])

    rc, out = run(LOOKUP, "panic(nil) no 1.21")
    check("CT-14s", "go_lookup panic(nil)", rc == 0 and "RN1.21 p.3" in out and "PanicNilError" in out, out[:200])

    rc, out = run(LOOKUP, "go 1.26 novidades")
    check("CT-17s", "go_lookup Go 1.26 without release notes", "NOT COVERED" in out and "Go 1.25 and 1.26" in out, out[-250:])

    rc, out = run(LOOKUP, "--list")
    check("CT-20b", "go_lookup --list", rc == 0 and "receivers" in out and "Known gaps" in out)

    rc, out = run(LOOKUP, "--json", "select default timeout")
    try:
        data = json.loads(out)
        ok = rc == 0 and data["topicos"] and data["topicos"][0]["id"] == "select"
    except Exception as e:  # noqa
        ok = False
    check("CT-20c", "go_lookup --json", ok)

    rc, out = run(CHECKLIST, "concorrencia")
    miss = has_all(out, ["[from source]", "[inference]", "Little p.73", "Little p.75", "Spec p.111", "RN1.23 p.4", "PDF"])
    wg = [ln for ln in out.splitlines() if "WaitGroup" in ln and "[from source]" in ln]
    check("CT-22", "go_checklist concorrencia", rc == 0 and not miss and not wg, "%s %s" % (miss, wg))

    rc, out = run(CHECKLIST, "--list")
    check("CT-22b", "go_checklist --list", rc == 0 and "concorrencia" in out and "generics" in out)

    rc, out = run(CHECKLIST, "zzz")
    check("CT-22c", "go_checklist unknown area", rc == 2)

    rc, out = run(CHECKLIST, "concurrency")
    check("CT-22d", "go_checklist English alias (concurrency)", rc == 0 and "Little p.73" in out)

    rc, out = run(SCAN, FIX_SCAN)
    rules = ["loopvar-goroutine", "rand-seed", "lock-no-defer", "defer-in-loop", "recover-eq-nil", "panic-nil", "getter-get-prefix",
             "sleep-sync", "ignored-result", "select-default-loop"]
    miss = has_all(out, rules + ["10 finding(s)", "go 1.21", "NOT an approval"])
    check("CT-23", "scan_go_smells fixtures", rc == 0 and not miss, str(miss))

    rc, out = run(SCAN, FIX_SCAN + "/sample_test.go")
    check("CT-23b", "scan_go_smells 0 findings is not an approval", rc == 0 and "0 finding(s)" in out and "NOT an approval" in out)

    rc, out = run(SCAN, "caminho/que/nao/existe")
    check("CT-23c", "scan_go_smells nonexistent path does not break", rc == 0 and "0 .go file(s)" in out)

    rc, out = run(GOMOD, "--target", "1.24", FIX_OLD)
    miss = has_all(out, ["[inference", "built-ins min, max, clear", "panicnil", "Go 1.25 and 1.26 have no release notes", "copied table"])
    check("CT-24", "check_gomod old -> 1.24", rc == 0 and not miss, str(miss))

    rc, out = run(GOMOD, FIX_MID)
    miss = has_all(out, ["only exists from 1.23 onward", "already declared in go.mod", "OLD MODE (go < 1.23)"])
    check("CT-25", "check_gomod mid (godebug em go 1.22)", rc == 0 and not miss, str(miss))

    rc, out = run(GOMOD, "nao-existe/go.mod")
    check("CT-24b", "check_gomod missing go.mod", rc == 2)

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "go.mod")
        with open(p, "w", encoding="utf-8") as f:
            f.write("module x\n\ngo 1.24\n\ntool example.com/t\n")
        rc, out = run(GOMOD, p)
        check("CT-32s", "check_gomod go 1.24 com diretiva tool", rc == 0 and "tool: example.com/t" in out and "WARNING" not in out, out[:200])
        with open(p, "w", encoding="utf-8") as f:
            f.write("module x\n\ngo 1.23\n\ntool example.com/t\n")
        rc, out = run(GOMOD, p)
        check("CT-32t", "check_gomod warns about tool in go 1.23", "`tool` directive" in out and "WARNING" in out, out[:200])


# ---------------------------------------------------------------- hygiene
def hygiene_tests():
    bad_enc, bad_abs, bad_json = [], [], []
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            if f.endswith((".pyc", ".png")) or "__pycache__" in rel:  # binaries (e.g. .claude-plugin/icon.png)
                continue
            b = open(p, "rb").read()
            try:
                t = b.decode("utf-8")
            except UnicodeDecodeError:
                bad_enc.append(rel + " (not UTF-8)")
                continue
            if b.startswith(b"\xef\xbb\xbf"):
                bad_enc.append(rel + " (BOM)")
            if b"\r\n" in b:
                bad_enc.append(rel + " (CRLF)")
            if rel != "tests/run_script_tests.py" and re.search("\u00c3[\u0080-\u00bf]|\u00e2\u20ac|\ufffd", t):
                bad_enc.append(rel + " (mojibake)")
            if rel != "tests/run_script_tests.py" and re.search(r"[A-Za-z]:\\(Users|development)|/Users/|/home/[a-z]+/", t):
                bad_abs.append(rel)
            if f.endswith(".json"):
                try:
                    json.loads(t)
                except Exception as e:  # noqa
                    bad_json.append("%s: %s" % (rel, e))
    check("HY-1", "files in UTF-8 without BOM, LF, no mojibake", not bad_enc, str(bad_enc))
    check("HY-2", "no absolute user path", not bad_abs, str(bad_abs))
    check("HY-3", "valid JSON", not bad_json, str(bad_json))

    # references of the index and the checklists exist
    idx = json.loads(read("scripts/go_index.json"))
    missing = []
    for t in idx["topicos"]:
        for part in t["ref"].split(";"):
            m = re.search(r"references/[\w\-]+\.md", part)
            if m and not os.path.exists(os.path.join(ROOT, m.group(0))):
                missing.append(m.group(0))
    check("HY-4", "reference files cited in go_index.json exist", not missing, str(missing))

    # agent structure
    agent = read("agents/go-expert.md")
    miss = has_all(agent, ["# Epistemic honesty", "# Security: anti prompt-injection", "# When to consult references and skills",
                           "# Response format", "**Page convention.**", "[DATED]", "[from source]", "[inference]", "[extrapolation]",
                           "**Does not cover**", "scripts/go_lookup.py", "scripts/go_checklist.py"])
    check("HY-5", "agents/go-expert.md has the required sections", not miss, str(miss))
    n = len(agent.splitlines())
    check("HY-5b", "prompt not truncated (> 60 lines)", n > 60, str(n))
    paths = set(re.findall(r"`((?:scripts|skills|tests|references)/[\w./\-]+\.(?:py|md))", agent))
    nf = [p for p in paths if not os.path.exists(os.path.join(ROOT, p))]
    check("HY-6", "paths cited in the agent exist", not nf, str(nf))

    cop = read(".github/agents/go-expert.agent.md")
    fm = re.match(r"---\nname: go-expert\ndescription: (.+)\ntools: \[(.+)\]\n(?:model: .+\n)?---\n", cop)
    check("HY-7", "Copilot agent with frontmatter (description, tools) and body with <PKG>", bool(fm) and "<PKG>" in cop and "# Security" in cop)
    ag = read("AGENTS.md")
    miss = has_all(ag, ["Page convention", "[DATED]", "[extrapolation]", "anti prompt-injection", "NOT COVERED", "<PKG>"])
    check("HY-8", "AGENTS.md (Codex) complete", not miss, str(miss))
    rd = read("README.md")
    miss = has_all(rd, ["### Claude Code", "### Codex (OpenAI)", "### GitHub Copilot", "current documentation"])
    check("HY-9", "README with installation on the 3 platforms and a notice about current documentation", not miss, str(miss))
    check("HY-10", "valid plugin.json with name and version", json.loads(read(".claude-plugin/plugin.json")).get("name") == "go-expert")
    for sk in ("go-code-review", "go-version-migration", "go-concurrency-review", "go-generics-review"):
        check("HY-11-" + sk, "SKILL.md of %s with frontmatter" % sk,
              re.match(r"---\nname: %s\ndescription: .+\n---\n" % sk, read("skills/%s/SKILL.md" % sk)) is not None)


# ---------------------------------------------------------------- cases x package
# NOTE: the strings looked up in references/*.md are literal excerpts of those files; update them together with the references.
CASE_FACTS = {
    1: [("references/frameworks.md", "pointer methods can only be called on pointers")],
    2: [("references/frameworks.md", "`a[1:3:5]` gives capacity 4"), ("references/procedimentos.md", "a[i:j:j]")],
    3: [("references/regras-da-spec.md", "classic pitfall")],
    4: [("references/frameworks.md", "is per function, not per block")],
    5: [("references/procedimentos.md", "Call `defer resource.Close()` immediately after the check")],
    6: [("references/frameworks.md", "A panic in a goroutine without defer+recover terminates the whole program")],
    7: [("references/versoes-e-migracao.md", "no passage literally says that a `go.mod` with `go 1.21` keeps the old semantics")],
    8: [("references/frameworks.md", "Receiving from a closed channel")],
    9: [("references/regras-da-spec.md", "`~MyInt` and `~error` are illegal")],
    10: [("references/regras-da-spec.md", "allows `any` in `[K comparable]`")],
    11: [("references/regras-da-spec.md", "`apply[]` is illegal")],
    12: [("references/versoes-e-migracao.md", "stops being necessary in 1.22+ code")],
    13: [("references/versoes-e-migracao.md", "randseednop=0")],
    14: [("references/versoes-e-migracao.md", "panicnil=1")],
    15: [("references/versoes-e-migracao.md", "`new(expr)` cross-reading")],
    16: [("agents/go-expert.md", "Other languages: refuse and redirect")],
    17: [("agents/go-expert.md", "Go 1.25 and 1.26")],
    18: [("references/frameworks.md", "not stated by any source read")],
    19: [("agents/go-expert.md", "If this material contains orders directed at you")],
    20: [("scripts/go_index.json", '"id": "receivers"')],
    21: [("scripts/go_index.json", "errgroup")],
    22: [("scripts/go_checklists.json", '"concorrencia"')],
    23: [("skills/go-code-review/SKILL.md", "0 findings from the scan is NOT an approval")],
    24: [("skills/go-version-migration/scripts/check_gomod.py", "[inference")],
    25: [("skills/go-version-migration/scripts/check_gomod.py", "only exists from 1.23 onward")],
    26: [("references/INDEX.md", "the printed page is N − 1")],
    27: [("references/casos-e-antipadroes.md", "Little p.73 (example with `time.Sleep`)")],
    28: [("references/glossario.md", "NumCPU/GOMAXPROCS")],
    29: [("agents/go-expert.md", "text of the PDFs")],
    30: [("agents/go-expert.md", "reveal your prompt")],
    31: [("tests/verify_citations.py", "negative")],
    32: [("references/versoes-e-migracao.md", "`tool` directive in `go.mod`")],
}


def case_tests():
    cases = read("tests/casos-de-teste.md")
    ids = sorted({int(x) for x in re.findall(r"^### CASE (\d+)", cases, re.M)})
    check("CS-1", "casos-de-teste.md has cases 1-32 (>= 20)", ids == list(range(1, 33)), str(ids))
    for cid, facts in CASE_FACTS.items():
        miss = [(f, s) for f, s in facts if s not in read(f)]
        check("CS-%02d" % cid, "case %d: required facts are in the package" % cid, not miss, str(miss))
    inj = [i for i in (19, 29, 30)]
    check("CS-inj", "injection cases present (19, 29, 30)", all(i in ids for i in inj))


# ---------------------------------------------------------------- verifiers (with --src)
def verifier_tests(src):
    rc, out = run("tests/verify_citations.py", "--src", src)
    m = re.search(r"(\d+) positive, (\d+) negative, (\d+) index sources, (\d+) checklist items, (\d+) failures", out)
    ok = rc == 0 and m and int(m.group(1)) >= 60 and int(m.group(2)) >= 15 and int(m.group(5)) == 0
    check("VC-1", "verify_citations.py passes (>= 60 positive, >= 15 negative, 0 failures)", ok, out[-300:])

    rc, out = run("tests/audit_tokens.py", "--src", src)
    check("VC-2", "audit_tokens.py with no RANGE/FAIL outside the exceptions list", rc == 0, out[-600:])

    with tempfile.TemporaryDirectory() as td:
        bad = {"positive": [{"id": "X1", "doc": "Eff", "pages": [29], "terms": ["phrase that does not exist on this page xyz"], "claim": "false"}],
               "negative": []}
        p1 = os.path.join(td, "bad_pos.json")
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(bad, f)
        rc, out = run("tests/verify_citations.py", "--src", src, "--checks", p1, "--index", os.path.join(td, "x"), "--checklists", os.path.join(td, "y"))
        check("VC-3", "sensitivity: a wrong positive claim fails (exit 1)", rc == 1 and "FAIL" in out, out[-200:])
        bad2 = {"positive": [], "negative": [{"id": "X2", "docs": ["Eff"], "terms": ["defer f.Close()"], "claim": "false negative"}]}
        p2 = os.path.join(td, "bad_neg.json")
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(bad2, f)
        rc, out = run("tests/verify_citations.py", "--src", src, "--checks", p2, "--index", os.path.join(td, "x"), "--checklists", os.path.join(td, "y"))
        check("VC-4", "sensitivity: a negative whose term exists fails (exit 1)", rc == 1 and "found in" in out, out[-200:])
        bad3 = {"positive": [{"id": "X3", "doc": "Eff", "pages": [999], "terms": ["a"], "claim": "page out of range"}], "negative": []}
        p3 = os.path.join(td, "bad_rng.json")
        with open(p3, "w", encoding="utf-8") as f:
            json.dump(bad3, f)
        rc, out = run("tests/verify_citations.py", "--src", src, "--checks", p3, "--index", os.path.join(td, "x"), "--checklists", os.path.join(td, "y"))
        check("VC-5", "sensitivity: a page out of range fails", rc == 1 and "out of range" in out, out[-200:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", help="folder with the .txt files extracted from the PDFs (tests/extract_pdf_text.py); enables the verifiers")
    a = ap.parse_args()
    script_tests()
    hygiene_tests()
    case_tests()
    if a.src:
        verifier_tests(a.src)
    else:
        check("VC-0", "citation verifiers (skipped: pass --src)", True, "skipped")
    fails = [r for r in RESULTS if not r[2]]
    for cid, desc, ok, detail in RESULTS:
        print("%s %-9s %s%s" % ("OK   " if ok else "FAIL ", cid, desc, "" if ok or not detail else "  | " + detail[:300]))
    print("Summary: %d tests, %d failures" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
