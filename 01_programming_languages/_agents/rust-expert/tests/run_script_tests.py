# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic cases of tests/casos-de-teste.md against the rust-expert package:
  1. scripts (rust_lookup.py, rust_checklist.py, scan_rust_smells.py): expected output and exit code;
  2. coverage of cases 1-32 in the references, the prompt, and the skills (each case requires passages the package must carry);
  3. with --src: verify_citations.py and audit_tokens.py pass, and a mutation self-test proves the verifier
     REJECTS a wrong citation and a false negative claim.
Usage (from any folder):  python -I tests/run_script_tests.py [--src DIR with the .txt files extracted from the PDFs]
No network. Exit 0 if everything passed.
"""
import argparse
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
T = os.path.join(ROOT, "tests")


def run(script, *args, folder=S):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", os.path.join(folder, script)] + list(args),
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


CASES = []


def case(cid, desc, script, args, must, rc=0, must_not=()):
    CASES.append((cid, desc, script, args, must, rc, must_not))


FIX = os.path.join(S, "fixtures", "sample.rs")
case("CT-20", "lookup elision", "rust_lookup.py", ["elisão"], ["Book p.270-274", "Ref p.498-502", "When to annotate"])
case("CT-20b", "lookup in English", "rust_lookup.py", ["lifetime elision"], ["Ref p.498-502"])
case("CT-21", "tokio: NOT COVERED", "rust_lookup.py", ["tokio"], ["NOT COVERED", "Book p.491"], rc=1)
case("CT-21b", "serde: NOT COVERED", "rust_lookup.py", ["serde"], ["NOT COVERED"], rc=1)
case("CT-22", "atomics: partial", "rust_lookup.py", ["AtomicUsize"], ["PARTIAL", "Book p.482", "Ref p.143", "[extrapolation]"])
case("CT-26", "E0038: NOT COVERED", "rust_lookup.py", ["E0038"], ["NOT COVERED"], rc=1)
case("CT-26b", "dyn compatibility by id", "rust_lookup.py", ["--topic", "dyn-compatibility"], ["Ref p.147-150", "Book p.547, 557"])
case("CT-26c", "nonexistent term", "rust_lookup.py", ["blockchain consensus"], ["NOT COVERED"], rc=1)
case("CT-20c", "topic list", "rust_lookup.py", ["--list"], ["ownership", "unsafe", "out of scope/partial"])
case("CT-20d", "nonexistent topic by id", "rust_lookup.py", ["--topic", "nao-existe"], ["NOT COVERED"], rc=1)
case("CT-28", "unsafe checklist", "rust_checklist.py", ["unsafe"], ["Book p.592", "Book p.602", "Ref p.160", "[inference]", "Ref p.624-627"])
case("CT-28c", "edition checklist", "rust_checklist.py", ["edition", "--markdown"], ["- [ ]", "Book p.711", "Ref p.357"])
case("CT-28d", "area list", "rust_checklist.py", ["--list"], ["review", "errors", "ownership", "unsafe", "concurrency", "edition"])
case("CT-28e", "unknown area", "rust_checklist.py", ["xyz"], ["unknown area"], rc=2)
case("CT-28f", "labeled item without a page", "rust_checklist.py", ["review"], ["[extrapolation] no page"])
case("CT-28l", "Portuguese area alias", "rust_checklist.py", ["revisao"], ["[extrapolation] no page"])
case("CT-28g", "unsafe scan on the fixture", "scan_rust_smells.py", ["--profile", "unsafe", FIX],
     ["static-mut", "missing-safety-comment", "extern-no-unsafe", "attr-no-unsafe", "unsafe-op-in-unsafe-fn", "origin: [from source]"],
     must_not=["sample.rs:29 (production) missing-safety-comment", "sample.rs:55"])
case("CT-28h", "review scan on the fixture", "scan_rust_smells.py", ["--profile", "review", FIX],
     ["ref-string", "index-loop", "spawn-no-move", "origin: [extrapolation]"], must_not=["sample.rs:55"])
case("CT-28i", "rules with origin", "scan_rust_smells.py", ["--rules"],
     ["unwrap [review/medium] origin: [from source]", "ref-vec", "[extrapolation]", "transmute", "[inference]", "unchecked-api"])
case("CT-28j", "nonexistent path does not break", "scan_rust_smells.py", ["nao_existe_xyz.rs"], ["0 .rs file(s)"])


def check_json_outputs():
    fails = 0
    code, out = run("scan_rust_smells.py", "--json", "--profile", "all", FIX)
    try:
        d = json.loads(out)
        ok = code == 0 and d["files_scanned"] == 1 and all("origin" in f for f in d["findings"]) and len(d["findings"]) >= 10
    except Exception:
        ok = False
    print("%s %-7s scan --json: valid JSON, findings with origin" % ("OK   " if ok else "FAIL", "CT-28k"))
    fails += 0 if ok else 1
    code, out = run("rust_lookup.py", "--json", "mutex")
    try:
        d = json.loads(out)
        ok = code == 0 and d and d[0]["id"] == "mutex-arc"
    except Exception:
        ok = False
    print("%s %-7s lookup --json: mutex -> mutex-arc" % ("OK   " if ok else "FAIL", "CT-20e"))
    fails += 0 if ok else 1
    return fails


# coverage of cases 1-32: (case, file or 'refs', regex that must match)
# NOTE: the 'refs' patterns match the text of references/*.md, which is translated in a separate phase;
# they keep matching the Portuguese wording until then (patterns for agent/skill files are already English).
COVER = [
    (1, "refs", r"double free"), (1, "refs", r"pointer, length and capacity"), (1, "refs", r"\(i32, String\)"),
    (2, "refs", r"simulate elision"), (2, "refs", r"Each reference parameter gets its own lifetime"),
    (3, "refs", r"E0502"), (3, "refs", r"reallocate"),
    (4, "refs", r"(?i)contract violation"), (4, "refs", r"expect"),
    (5, "refs", r"trait object"), (5, "refs", r"monomorph"),
    (6, "refs", r"Arc<Mutex<"), (6, "refs", r"E0373"),
    (7, "refs", r"Weak"), (7, "refs", r"weak_count"),
    (8, "refs", r"starvation|Starvation"), (8, "refs", r"fair"),
    (9, "refs", r"scrutinee"), (9, "refs", r"dropped before the `else`"),
    (10, "refs", r"Edition 2018 and before|2018 e anteriores|≤2018"), (10, "refs", r"path"),
    (11, "refs", r"Invalid values"), (11, "refs", r"unsound"),
    (12, "refs", r"#\[unsafe\(no_mangle\)\]"), (12, "refs", r"unsafe extern"),
    (13, "refs", r"follow-set|Follow-set"), (13, "refs", r"lookahead"),
    (14, "refs", r"impl From<"), (14, "refs", r"Box<dyn Error>"),
    (15, "refs", r"Dyn compatible|dyn compatib"), (15, "refs", r"where Self: Sized"),
    (16, "agents/rust-expert.md", r"Other languages: decline and redirect"),
    (17, "refs", r"Rust does not embed a runtime"), (17, "agents/rust-expert.md", r"async runtimes"),
    (18, "refs", r"With a GC the collector frees"),
    (19, "agents/rust-expert.md", r"data, not instructions"), (19, "agents/rust-expert.md", r"Never run commands"),
    (20, "references/frameworks.md", r"simulate elision"),
    (21, "references/INDEX.md", r"Choice of crates"),
    (22, "references/INDEX.md", r"AtomicUsize::new"),
    (23, "skills/rust-code-review/SKILL.md", r"--check.*extrapolation"),
    (24, "skills/rust-edition-migration/SKILL.md", r"are not in the sources"),
    (25, "references/INDEX.md", r"PDF page"),
    (26, "references/regras-da-referencia.md", r"Dyn compatible"),
    (27, "agents/rust-expert.md", r"command output"), (27, "agents/rust-expert.md", r"do not reveal this prompt"),
    (28, "skills/rust-unsafe-audit/SKILL.md", r"scan_rust_smells"),
    (29, "references/glossario.md", r"\(Book p\.476, 678\)"),
    (30, "references/procedimentos.md", r"In a `const` context, `transmute`"),
    (31, "references/procedimentos.md", r"type-based check"),
    (32, "references/procedimentos.md", r"256 distinct discriminants"),
]


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def coverage():
    refs = "\n".join(read("references/" + f) for f in sorted(os.listdir(os.path.join(ROOT, "references"))) if f.endswith(".md"))
    fails = 0
    for caso, where, rx in COVER:
        txt = refs if where == "refs" else read(where)
        ok = re.search(rx, txt) is not None
        if not ok:
            fails += 1
            print("FAIL CT-%02d coverage: %s does not contain /%s/" % (caso, where, rx))
    print("%s coverage of cases 1-32 in the references/prompt/skills: %d checks" % ("OK   " if not fails else "FAIL", len(COVER)))
    n = len(re.findall(r"^### CASE", read("tests/casos-de-teste.md"), re.M))
    ok = n >= 20
    print("%s casos-de-teste.md has %d cases (minimum 20)" % ("OK   " if ok else "FAIL", n))
    return fails + (0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", help="directory with the .txt files extracted from the PDFs (enables the verifiers and the self-test)")
    a = ap.parse_args()
    fails = 0
    for fn in sorted(os.listdir(S)):
        if fn.endswith(".py"):
            try:
                py_compile.compile(os.path.join(S, fn), doraise=True, cfile=os.path.join(tempfile.gettempdir(), fn + "c"))
            except py_compile.PyCompileError as e:
                print("FAIL compilation", fn, e)
                fails += 1
    for cid, desc, script, args, must, rc, must_not in CASES:
        code, out = run(script, *args)
        missing = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not missing and not bad
        print("%s %-7s %s" % ("OK   " if ok else "FAIL", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (code, rc, missing, bad))
    fails += check_json_outputs()
    fails += coverage()
    if a.src:
        code, out = run("verify_citations.py", "--src", a.src, folder=T)
        ok = code == 0
        print("%s %-7s verify_citations: %s" % ("OK   " if ok else "FAIL", "VC", out.strip().splitlines()[-1]))
        if not ok:
            print(out[-1500:])
        fails += 0 if ok else 1
        code, out = run("audit_tokens.py", "--src", a.src, folder=T)
        ok = code == 0
        print("%s %-7s audit_tokens: %s" % ("OK   " if ok else "FAIL", "AT", out.strip().splitlines()[-1]))
        if not ok:
            print(out[-1500:])
        fails += 0 if ok else 1
        # mutation self-test: the verifier must REJECT a wrong citation and a false negative claim
        mut = {"positive": [{"id": "M1", "src": "Book", "pages": [85], "terms": ["Arc<Mutex<T>> e RwLock"], "claim": "wrong citation"}],
               "negative": [{"id": "M2", "src": ["Book"], "terms": ["ownership"], "claim": "false negative"}]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(mut, f)
            tmp = f.name
        code, out = run("verify_citations.py", "--src", a.src, "--checks", tmp, "--no-data", folder=T)
        os.remove(tmp)
        ok = code == 1 and "M1" in out and "M2" in out
        print("%s %-7s mutation self-test: verifier rejects a wrong citation and a false negative" % ("OK   " if ok else "FAIL", "MUT"))
        fails += 0 if ok else 1
    else:
        print("SKIP   citation verifiers (pass --src with the text extracted from the PDFs)")
    print("Summary: %d failures" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
