# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic cases of tests/casos-de-teste.md against the scripts
and checks that the output contains what the sources say (and the origin labels). Usage (from the package root):
  python -I tests/run_script_tests.py [--src <folder with JUNIT.txt, MOCK.txt, TDM.txt, JMETER.txt, SWEG.txt>]
With --src, it also runs verify_citations.py and audit_tokens.py. No network. Exit code 0 if everything passes.
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")
T = os.path.join(ROOT, "tests")


def run(path, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, "-I", path] + list(args),
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


CASES = []


def case(cid, desc, script, args, must, rc=0, must_not=()):
    CASES.append((cid, desc, os.path.join(S, script), args, must, rc, must_not))


# doubles_selector.py (SWE-G cap. 13)
case("CT-06", "slow stateful database -> fake", "doubles_selector.py",
     ["--slow-or-unhermetic", "--stateful-collaborator"],
     ["Fake", "SWE-G p.192-195", "[from source]"])
case("CT-06b", "existing fake", "doubles_selector.py", ["--slow-or-unhermetic", "--fake-available"],
     ["Existing fake", "SWE-G p.192-194"])
case("CT-06c", "fast dependency -> real", "doubles_selector.py", [],
     ["Real implementation", "SWE-G p.189, p.191"])
case("CT-07", "side effect -> minimal interaction testing", "doubles_selector.py", ["--verify-interactions"],
     ["Interaction testing", "SWE-G p.197-200", "change-detector"])
case("CT-07b", "error/value the real one does not produce -> stub", "doubles_selector.py", ["--fault-injection"],
     ["Stub", "SWE-G p.195-197"])
case("CT-08", "dummy is an extrapolation", "doubles_selector.py", ["--uninvoked-dummy"],
     ["[extrapolation]", "Meszaros"])
# tdm_audit.py (TDM p.3-8)
case("CT-15", "real data without masking and manual inspection", "tdm_audit.py", ["--raw-prod", "--manual-inspect"],
     ["CRITICAL FINDINGS", "TDM p.6, p.8", "TDM p.6-7", "Not legal advice", "does not cite LGPD"])
case("CT-15b", "positive practices", "tdm_audit.py", ["--masked", "--synthetic", "--auto-validation"],
     ["NO FINDINGS IN THE REPORTED ITEMS", "PASS", "TDM p.6"])
case("CT-15c", "exemption as routine", "tdm_audit.py", ["--exemption-routine"], ["TDM p.8", "WITH FINDINGS"])
# jmeter_calc.py (JMETER p.15; Little = extrapolation)
case("CT-18", "Thread Group arithmetic", "jmeter_calc.py",
     ["--threads", "50", "--ramp-up", "10", "--loops", "1", "--sla", "200"],
     ["start_rate_threads_per_s: 5.0", "total_requests: 50", "JMETER p.15", "JMETER p.29-30", "JMETER p.50"],
     must_not=["p99=", "p95="])
case("CT-19", "Little sizing and extrapolation label", "jmeter_calc.py",
     ["--target-tps", "250", "--latency", "800", "--think-time", "1200"],
     ["threads_rounded_up: 500", "[extrapolation]", "NOT in JMETER"])
case("CT-20", "invalid input", "jmeter_calc.py", ["--threads", "0"], ["--threads must be positive"], rc=2)
# testing_lookup.py
case("CT-01", "lookup pyramid (Portuguese keyword)", "testing_lookup.py", ["pirâmide"],
     ["80/15/5", "SWE-G p.156", "70/20/10 is NOT"])
case("CT-03", "lookup flaky", "testing_lookup.py", ["flaky"], ["SWE-G p.155", "0.1%"])
case("CT-15d", "lookup masking", "testing_lookup.py", ["data", "masking"], ["TDM p.6", "LGPD is NOT cited"])
case("CT-20b", "lookup non-gui", "testing_lookup.py", ["non-gui"], ["JMETER p.50", "-e -o"])
case("CT-09", "lookup JUnit 5 -> NOT COVERED", "testing_lookup.py", ["jupiter"],
     ["NOT COVERED", "JUnit 5/Jupiter is NOT in the sources"], rc=1)
case("CT-08b", "lookup Meszaros", "testing_lookup.py", ["meszaros"],
     ["Meszaros", "[extrapolation]"])
case("CT-19b", "lookup Little's Law (Portuguese keyword)", "testing_lookup.py", ["lei", "de", "little"],
     ["NOT COVERED", "Little's Law"], rc=1)
case("CT-23", "out of scope", "testing_lookup.py", ["kubernetes", "hpa"], ["NOT COVERED"], rc=1)
case("CT-23b", "filter by source", "testing_lookup.py", ["--list", "--book", "TDM"],
     ["tdm-visao", "tdm-masking-encryption"], must_not=["jmeter-thread-group", "fakes"])
case("CT-01b", "lookup pyramid (English keyword)", "testing_lookup.py", ["test", "pyramid"],
     ["80/15/5", "SWE-G p.156"])
case("CT-19c", "lookup Little's Law (English keyword)", "testing_lookup.py", ["little's", "law"],
     ["NOT COVERED", "Little's Law"], rc=1)


RANGES = {"JUNIT": (1, 8), "MOCK": (1, 12), "TDM": (1, 9), "JMETER": (1, 53), "SWE-G": (149, 221)}


def check_page_ranges():
    """Every citation (SIGLA p.N[-M][; p.K]) in references/, the agent, AGENTS.md, README and the index must be
    within the valid range of the source. Lines that mention 'v1' or 'sem lastro'/'no basis' (they cite v1 to refute it) are ignored."""
    import re
    files = [os.path.join(ROOT, "AGENTS.md"), os.path.join(ROOT, "README.md"),
             os.path.join(ROOT, "agents", "software-testing-qa-expert.md"),
             os.path.join(ROOT, ".github", "agents", "software-testing-qa-expert.agent.md"),
             os.path.join(S, "testing_index.json")]
    refs = os.path.join(ROOT, "references")
    files += [os.path.join(refs, f) for f in sorted(os.listdir(refs)) if f.endswith(".md")]
    pat = re.compile(r"(?<![A-Za-z-])(JUNIT|MOCK|TDM|JMETER|SWE-G) p\.(\d+)(?:\s*-\s*(\d+))?((?:\s*[;,]\s*p\.\d+(?:\s*-\s*\d+)?)*)")
    bad = 0
    n = 0
    for fp in files:
        for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
            if "v1" in line or "sem lastro" in line.lower() or "no basis" in line.lower():
                continue
            for m in pat.finditer(line):
                src = m.group(1)
                nums = [int(m.group(2))]
                if m.group(3):
                    nums.append(int(m.group(3)))
                nums += [int(x) for x in re.findall(r"\d+", m.group(4) or "")]
                lo, hi = RANGES[src]
                n += 1
                if any(x < lo or x > hi for x in nums):
                    bad += 1
                    print("   out of range: %s:%d %s p.%s" % (os.path.basename(fp), ln, src, nums))
    return n, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    fails = 0
    for cid, desc, script, args, must, rc, must_not in CASES:
        code, out = run(script, *args)
        missing = [m for m in must if m not in out]
        bad = [m for m in must_not if m in out]
        ok = code == rc and not missing and not bad
        print("%s %-7s %s" % ("OK   " if ok else "FAIL ", cid, desc))
        if not ok:
            fails += 1
            print("   rc=%s (expected %s) missing=%s unexpected=%s" % (code, rc, missing, bad))
    # the index must be valid JSON and have 'uncovered'
    import json
    try:
        d = json.load(open(os.path.join(S, "testing_index.json"), encoding="utf-8"))
        ok = len(d["topics"]) >= 25 and len(d["uncovered"]) >= 4
    except Exception as e:  # noqa
        ok = False
    print("%s %-7s testing_index.json valid (>=25 topics, negative coverage)" % ("OK   " if ok else "FAIL ", "IDX"))
    fails += 0 if ok else 1
    n, bad = check_page_ranges()
    ok = bad == 0
    print("%s %-7s valid page ranges (%d citations checked, %d out of range)" % ("OK   " if ok else "FAIL ", "RNG", n, bad))
    fails += 0 if ok else 1
    if a.src:
        for name, script in (("VC", "verify_citations.py"), ("AT", "audit_tokens.py")):
            code, out = run(os.path.join(T, script), "--src", a.src)
            last = out.strip().splitlines()[-1] if out.strip() else ""
            ok = code == 0
            print("%s %-7s %s: %s" % ("OK   " if ok else "FAIL ", name, script, last))
            fails += 0 if ok else 1
    print("Summary: %d failures" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
