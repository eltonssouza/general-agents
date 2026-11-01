# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic (script) cases of tests/casos-de-teste.md and, with --text, the verifiers
against the text extracted from the PDF. Usage (from the package root):
  python -I tests/run_script_tests.py [--text <Open-Data-Structures.txt>]
No network. Exit code 0 if all pass.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
SK = os.path.join(ROOT, "skills")
T = os.path.join(ROOT, "tests")


def run(path, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args), capture_output=True, text=True,
                       encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


CASES = []


def case(cid, desc, path, args, must, rc=0, must_not=()):
    CASES.append((cid, desc, path, args, must, rc, must_not))


# --- cost lookup (ods_cost_lookup.py)
LK = os.path.join(S, "ods_cost_lookup.py")
case("CT-08", "add cost in the ArrayStack", LK, ["arraystack", "--op", "add"],
     ["amortized", "ODS p.36; ODS p.49", "Theorem 2.1"])
case("CT-08b", "RedBlackTree: worst case and height", LK, ["redblacktree"],
     ["O(log n) [worst case]", "ODS p.208", "<= 2 log n", "ODS p.196"])
case("CT-08d", "Portuguese --op alias still works (altura -> height)", LK, ["redblacktree", "--op", "altura"],
     ["<= 2 log n", "ODS p.196"])
case("CT-08c", "LinearHashTable: invariant and analysis", LK, ["linear probing"],
     ["analysis assumes independent, uniform hash values", "ODS p.127"])
case("CT-21", "out of scope: flow/NP", LK, ["Ford-Fulkerson"], ["NOT COVERED"], rc=1)
case("CT-04b", "term outside the book: tombstone", LK, ["tombstone"], ["NOT COVERED", "del", "ODS p.121"], rc=1)
case("CT-04b2", "Portuguese term outside the book: lapide", LK, ["lapide"], ["NOT COVERED", "del", "ODS p.121"], rc=1)
case("CT-06b", "Treap, Scapegoat and RBT by guarantee type", LK, ["--kind", "expected"],
     ["Treap", "SkiplistSSet", "MeldableHeap"])
case("CT-22", "quicksort stability is not in the book", LK, ["quicksort", "--op", "stability"],
     ["NOT COVERED"], rc=1)

# --- simulators
SIM = os.path.join(S, "structure_simulator.py")
case("CT-09", "ArrayStack: Lemma 2.1", SIM, ["arraystack", "--m", "100000", "--pattern", "growshrink", "--check"],
     ["resizes_r                            41", "lemma_2.1_violations                 0", "book's bounds: OK"])
case("CT-09b", "DualArrayDeque: Lemma 2.2", SIM, ["dualarraydeque", "--m", "20000", "--pattern", "random", "--check"],
     ["lemma_2.2_violations                 0", "book's bounds: OK"])
case("CT-13", "SEList: invariant and potential", SIM, ["selist", "--m", "20000", "--b", "8", "--pattern", "random", "--check"],
     ["invariant_b-1..b+1                   True", "book's bounds: OK"])
case("CT-14", "ScapegoatTree sorted: height and rebuild", SIM, ["scapegoat", "--m", "20000", "--pattern", "sorted", "--check"],
     ["height_invariant_violations          0", "book's bounds: OK"])

# --- calculators and demos
CALC = os.path.join(SK, "amortized-cost-calculator", "scripts", "calculate_amortized.py")
case("CT-10", "Rootish n=100000, index 5000", CALC, ["--mode", "rootish", "--n", "100000", "--index", "5000"],
     ["r <= (3 + sqrt(1 + 4n))/2 = 317", "<= 2r - 1 = 633", "block 99, position 50"])
case("CT-17", "additive resize is [extrapolation]", CALC, ["--mode", "resize", "--n", "1000", "--growth", "additive"],
     ["[extrapolation]", "quadratic growth"])
case("CT-17b", "geometric resize and Lemma 2.1", CALC, ["--mode", "resize", "--n", "1000"],
     ["sum n_i = 1023 <= 2m + 2r = 2020", "ODS p.47-48"])
HASH = os.path.join(SK, "hash-probe-analyzer", "scripts", "analyze_hash_probes.py")
case("CT-11", "del: find continues", HASH, ["--demo", "tombstones"],
     ["found: True", "CORRECT", "ODS p.121-122"])
case("CT-16", "nil instead of del: false negative", HASH, ["--demo", "naive_failure"],
     ["found: False", "FALSE NEGATIVE", "[inference]"])
case("CT-11b", "invariant length(t) >= 2q", HASH, ["--demo", "invariant"],
     ["maintained in all operations: True"])
ROT = os.path.join(SK, "tree-rotation-simulator", "scripts", "simulate_rotation.py")
case("CT-12", "left rotation at 20", ROT, ["--dir", "left", "--node", "20"],
     ["In-order sequence preserved:          True", "w moves up 1 and u moves down 1:     True"])
case("CT-12b", "invalid rotation", ROT, ["--dir", "left", "--node", "25"], ["has no right child"], rc=1)
LKP = os.path.join(SK, "morin-topic-lookup", "scripts", "morin_lookup.py")
case("CT-04c", "lookup: del", LKP, ["del"], ["ODS p.121-123", "does not use the word tombstone"])
case("CT-04d", "lookup: tombstone outside the book", LKP, ["tombstone"], ["NOT COVERED"], rc=1)
case("CT-01b", "lookup: potential method (Portuguese query)", LKP, ["metodo", "do", "potencial"],
     ["ODS p.61; ODS p.88-89; ODS p.209", "there is no general statement in Ch. 1"])
case("CT-01c", "lookup: potential method (English query)", LKP, ["potential", "method"],
     ["ODS p.61; ODS p.88-89; ODS p.209", "there is no general statement in Ch. 1"])
case("CT-25", "lookup: subject index uses printed pages (Portuguese query)", LKP, ["indice", "remissivo"], ["add 12"])
case("CT-25b", "lookup: subject index uses printed pages (English query)", LKP, ["subject", "index"], ["add 12"])


def norm_sq(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[\s_]+", "", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    a = ap.parse_args()
    fails = 0
    for cid, desc, path, args, must, rc, must_not in CASES:
        code, out = run(path, *args)
        missing = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not missing and not bad
        print("%s %-7s %s" % ("OK   " if ok else "FAIL ", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (code, rc, missing, bad))

    # CT-15: maximum height of a B-tree (book formula h <= log_B(l/2) + 1, ODS p.290), B = 256, l = 10^9 leaves
    B, leaves = 256, 10 ** 9
    h = math.floor(math.log(leaves / 2, B) + 1)
    ok = h == 4
    print("%s %-7s B-tree B=256, 10^9 leaves: h <= %d (expected 4)" % ("OK   " if ok else "FAIL ", "CT-15", h))
    fails += 0 if ok else 1

    # morin-topic-lookup index: check each table-of-contents entry against the text
    if a.text:
        raw = open(a.text, encoding="utf-8").read()
        parts = re.split(r"=== PAGE (\d+) ===", raw)
        pages = {int(parts[i]): norm_sq(parts[i + 1]) for i in range(1, len(parts), 2)}
        idx = json.load(open(os.path.join(SK, "morin-topic-lookup", "scripts", "morin_index.json"), encoding="utf-8"))
        bad = [it["topico"] for it in idx["toc"] if norm_sq(it["topico"].split(":")[0]) not in pages.get(it["pagina_pdf"], "")]
        ok = not bad
        print("%s %-7s morin_index.json: %d table-of-contents entries checked against the text%s"
              % ("OK   " if ok else "FAIL ", "IDX", len(idx["toc"]), "" if ok else " | failures: %s" % bad))
        fails += 0 if ok else 1
        bad_pages = [t["topico"] for t in idx["topics"] if any(p < 1 or p > 326 for p in t["paginas"])]
        ok = not bad_pages
        print("%s %-7s morin_index.json: %d curated topics with pages between 1 and 326" % ("OK   " if ok else "FAIL ", "IDX2", len(idx["topics"])))
        fails += 0 if ok else 1

        # verifiers
        code, out = run(os.path.join(T, "verify_citations.py"), "--text", a.text)
        ok = code == 0
        print("%s %-7s verify_citations: %s" % ("OK   " if ok else "FAIL ", "VC", out.strip().splitlines()[-1]))
        fails += 0 if ok else 1
        code, out = run(os.path.join(T, "audit_tokens.py"), "--text", a.text)
        ok = code == 0
        print("%s %-7s audit_tokens: %s" % ("OK   " if ok else "FAIL ", "AT", out.strip().splitlines()[-1]))
        fails += 0 if ok else 1

        # verifier self-test: a wrong page and a present negative term must FAIL
        bogus = {"positive": [{"id": "X1", "pages": [47], "terms": ["B = 256"], "claim": "deliberately wrong page"}],
                 "negative": [{"id": "X2", "terms": ["Treap"], "claim": "deliberately present term"}]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(bogus, f)
            tmp = f.name
        code, out = run(os.path.join(T, "verify_citations.py"), "--text", a.text, "--checks", tmp)
        os.remove(tmp)
        ok = code == 1 and "X1" in out and "X2" in out
        print("%s %-7s verifier self-test (must detect X1 and X2)" % ("OK   " if ok else "FAIL ", "VC-self"))
        fails += 0 if ok else 1
    print("Total failures: %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
