# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests (no model, no network) of the scripts and the package structure.

Usage:
  python -I tests/run_script_tests.py [--src PATH/src]   # --src enables verify_citations.py and audit_tokens.py
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
Expected values: arithmetic checked by hand and book pages cited in each test.
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

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL, OK = [], []


def run(args):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG, env=env)
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
    L = os.path.join("scripts", "sysdesign_lookup.py")
    T = os.path.join("scripts", "analyze_tradeoffs.py")
    S = os.path.join("scripts", "audit_saga.py")
    R = os.path.join("scripts", "calc_rate_limit.py")
    FX = os.path.join("tests", "fixtures")

    # ---- lookup
    rc, o = run([L, "--list"])
    check("lookup --list: 69 concepts and NOT COVERED marker", rc == 0 and has(o, "69 concepts", "NOT COVERED"), o)
    rc, o = run([L, "--concept", "circuit-breaker"])
    check("lookup circuit-breaker -> MS-MIC p.322 and MS-CLD p.127", rc == 0 and has(o, "MS-MIC p.322", "MS-CLD p.127", "Half-Open"), o)
    rc, o = run([L, "--concept", "little-law"])
    check("lookup little-law -> NOT COVERED", rc == 0 and has(o, "NOT COVERED"), o)
    rc, o = run([L, "--concept", "half-open"])
    check("lookup half-open -> NOT COVERED (term does not appear)", rc == 0 and has(o, "NOT COVERED", "does not appear"), o)
    rc, o = run([L, "--concept", "pacelc"])
    check("lookup pacelc -> partial, MS-CLD p.107", rc == 0 and has(o, "partial", "MS-CLD p.107"), o)
    rc, o = run([L, "--concept", "helland"])
    check("lookup helland -> NOT COVERED", rc == 0 and has(o, "NOT COVERED", "Life Beyond Distributed Transactions"), o)
    rc, o = run([L, "--query", "backoff"])
    check("lookup query backoff -> MS-CLD p.125", rc == 0 and has(o, "MS-CLD p.125"), o)
    rc, o = run([L, "--query", "consistent hashing"])
    check("lookup query consistent hashing -> SDH p.18", rc == 0 and has(o, "SDH p.18"), o)
    rc, o = run([L, "--query", "xyzzyplugh"])
    check("lookup nonexistent query -> rc 1 and NOT COVERED", rc == 1 and has(o, "NOT COVERED"), o)
    rc, o = run([L, "--concept", "saga", "--json"])
    try:
        d = json.loads(o)
        okj = d["key"] == "saga" and any(e["cite"] == "MS-CLD p.102" for e in d["entries"])
    except Exception:
        okj = False
    check("lookup saga --json valid with MS-CLD p.102", rc == 0 and okj, o)

    # ---- analyze_tradeoffs
    rc, o = run([T, "--tiers"])
    check("tradeoffs --tiers: 31.5 s matches the formula (SDH p.7)", rc == 0 and has(o, "31.5 seconds", "0d 0h 0m 31.5s", "8.76 hours", "8.76 h"), o)
    rc, o = run([T, "--availability", "0.999", "0.999", "0.999"])
    check("tradeoffs series 3x99.9% = 99.70030% (26.25 h/year)", rc == 0 and has(o, "99.70030%", "26.25 h"), o)
    rc, o = run([T, "--availability", "99.9", "99.9", "99.9"])
    check("tradeoffs accepts percentages (99.9 = 0.999)", rc == 0 and has(o, "99.70030%"), o)
    rc, o = run([T, "--availability", "1", "--redundancy", "0.99", "0.99"])
    check("tradeoffs parallel 2x99% = 99.990000%", rc == 0 and has(o, "99.990000%"), o)
    rc, o = run([T, "--compound", "50", "0.9999"])
    check("tradeoffs 50x99.99% = 99.5012% and 3.59 h/month (MS-MIC p.308: several hours)", rc == 0 and has(o, "99.5012%", "3.59 h", "MS-MIC p.308"), o)
    rc, o = run([T, "--throughput", "5000", "--latency-ms", "200"])
    check("tradeoffs Little 5000 req/s x 200 ms = 1000 in flight", rc == 0 and has(o, "L = 1000.00", "extrapolation"), o)
    rc, o = run([T, "--concurrency", "500", "--throughput", "5000"])
    check("tradeoffs Little: L=500, lambda=5000 -> W=100 ms", rc == 0 and has(o, "100.00 ms"), o)
    outs = [run([T, "--tail-services", str(n)])[1] for n in (10, 50, 100)]
    check("tradeoffs tail: 9.56% / 39.50% / 63.40%", has(outs[0], "9.56%") and has(outs[1], "39.50%") and has(outs[2], "63.40%"), "\n".join(outs))
    rc, o = run([T, "--pacelc", "PA/EL"])
    check("tradeoffs PACELC PA/EL without classifying products", rc == 0 and has(o, "NOT COVERED", "MS-CLD p.107") and "Cassandra" not in o, o)
    rc, o = run([T, "--pacelc", "XX/YY"])
    check("tradeoffs invalid PACELC -> rc 1", rc == 1, o)
    rc, o = run([T, "--availability", "0"])
    check("tradeoffs availability 0 -> rc 1", rc == 1, o)
    rc, o = run([T])
    check("tradeoffs no arguments -> rc 2", rc == 2, o)

    # ---- audit_saga
    rc, o = run([S, "--demo"])
    check("saga --demo: rc 0 and no errors/alerts", rc == 0 and has(o, "No errors/alerts"), o)
    rc, o = run([S, "--file", os.path.join(FX, "saga_ok.json")])
    check("saga_ok: rc 0", rc == 0 and has(o, "No errors/alerts"), o)
    rc, o = run([S, "--file", os.path.join(FX, "saga_bad.json")])
    check("saga_bad: rc 1 with S1,S2,S3,S5,S6,S7 and origins", rc == 1 and has(o, "[S1]", "[S2]", "[S3]", "[S5]", "[S6]", "[S7]", "SBC p.3", "MS-CLD p.102-103", "MS-MIC p.158-160"), o)
    rc, o = run([S, "--file", os.path.join(FX, "saga_bad.json"), "--format", "json"])
    try:
        d = json.loads(o)
        rules = {f["rule"] for f in d["findings"]}
        okj = {"S1", "S2", "S3", "S5", "S6", "S7"} <= rules
    except Exception:
        okj = False
    check("saga_bad --format json valid", rc == 1 and okj, o)
    rc, o = run([S, "--file", os.path.join(FX, "saga_ok.json"), "--strict"])
    check("saga_ok --strict: rc 0", rc == 0, o)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "s.json")
        json.dump({"name": "x", "steps": [{"name": "A", "service": "SA", "idempotent": True, "publishes_event": False},
                                          {"name": "B", "service": "SB", "idempotent": True, "publishes_event": False}]},
                  open(p, "w", encoding="utf-8"))
        rc, o = run([S, "--file", p])
        check("saga without pivot: non-final step without compensation -> ERROR S2", rc == 1 and has(o, "[S2]", "is not the last step"), o)
        p2 = os.path.join(td, "bad.json")
        open(p2, "w", encoding="utf-8").write("{not json")
        rc, o = run([S, "--file", p2])
        check("saga invalid JSON -> rc 2", rc == 2, o)
    rc, o = run([S, "--file", os.path.join(td, "naoexiste.json")])
    check("saga nonexistent file -> rc 2", rc == 2, o)

    # ---- calc_rate_limit
    rc, o = run([R, "--token-bucket", "100", "20", "150"])
    check("token bucket 100/20/150: 100 accepted, 50 rejected, 2.50 s", rc == 0 and has(o, "accepted: 100", "rejected", ": 50", "2.50 s", "extrapolation"), o)
    rc, o = run([R, "--backoff", "2000", "0", "4"])
    check("backoff without jitter 2000 ms x4: 2/4/8/16 s (MS-CLD p.125-126), total 30 s", rc == 0 and has(o, "2000.0", "4000.0", "8000.0", "16000.0", "30000.0"), o)
    rc1, o1 = run([R, "--backoff", "100", "2000", "6", "--jitter", "full", "--seed", "7"])
    rc2, o2 = run([R, "--backoff", "100", "2000", "6", "--jitter", "full", "--seed", "7"])
    rows = re.findall(r"^\s+\d+ \|\s+([\d.]+) \|\s+([\d.]+) \|", o1, re.M)
    okrows = len(rows) == 6 and all(float(w) <= float(c) + 1e-9 for c, w in rows) and float(rows[-1][0]) == 2000.0
    check("backoff full jitter: deterministic per seed and wait <= cap", rc1 == 0 and o1 == o2 and okrows, o1)
    rc, o = run([R, "--circuit-breaker", "S F F F F F S S", "--threshold", "5", "--open-seconds", "30", "--interval", "10"])
    check("CB: opens on the 5th consecutive failure and fails fast in the window", rc == 0 and has(o, "5 consecutive failures: opens", "fail fast"), o)
    rc, o = run([R, "--circuit-breaker", "S F F F F F S S", "--threshold", "5", "--open-seconds", "30", "--interval", "15"])
    check("CB: after the window lets a trial through and closes on success", rc == 0 and has(o, "trial call", "trial succeeded: closes"), o)
    rc, o = run([R, "--circuit-breaker", "F F F F F", "--threshold", "3", "--open-seconds", "0", "--interval", "1"])
    check("CB: a failing trial call reopens the circuit", rc == 0 and has(o, "3 consecutive failures: opens", "trial failed: reopens"), o)
    rc, o = run([R, "--circuit-breaker", "S X"])
    check("CB: invalid sequence -> rc 1", rc == 1, o)
    rc, o = run([R])
    check("rate: no arguments -> rc 2", rc == 2, o)

    # ---- package structure
    need = ["README.md", "AGENTS.md", os.path.join(".github", "agents", "system-design-microservices-expert.agent.md"),
            os.path.join("agents", "system-design-microservices-expert.md"), os.path.join(".claude-plugin", "plugin.json"),
            os.path.join("references", "INDEX.md"), os.path.join("tests", "casos-de-teste.md"),
            os.path.join("tests", "relatorio-de-fidelidade.md"), os.path.join("tests", "citation-checks.json")]
    check("required files exist", all(os.path.exists(os.path.join(PKG, f)) for f in need), str([f for f in need if not os.path.exists(os.path.join(PKG, f))]))
    ag = open(os.path.join(PKG, "agents", "system-design-microservices-expert.md"), encoding="utf-8").read()
    secs = ["prompt-injection", "[DATED]", "NOT COVERED", "Epistemic honesty", "Response format", "NOT in the corpus", "sysdesign_lookup.py", "calc_rate_limit.py"]
    check("agent .md has the required final sections", all(s in ag for s in secs), str([s for s in secs if s not in ag]))
    check("agent .md is not truncated (>= 90 lines)", ag.count("\n") >= 90, str(ag.count("\n")))
    refs = [f for f in os.listdir(os.path.join(PKG, "references")) if f.endswith(".md")]
    mentioned = set(re.findall(r"`([a-z0-9\-]+\.md)`", ag))
    miss = [m for m in mentioned if m not in refs]
    check("reference files cited in the agent exist", not miss, str(miss))
    scr = set(re.findall(r"`([a-z_]+\.py)", ag))
    miss = [s for s in scr if not os.path.exists(os.path.join(PKG, "scripts", s)) and not os.path.exists(os.path.join(PKG, "tests", s))]
    check("scripts cited in the agent exist", not miss, str(miss))
    bad = []
    for root, _, fs in os.walk(PKG):
        for fn in fs:
            if not fn.endswith((".md", ".py", ".json")):
                continue
            raw = open(os.path.join(root, fn), "rb").read()
            if raw.startswith(b"\xef\xbb\xbf"):
                bad.append(fn + ":BOM")
            t = raw.decode("utf-8", errors="replace")
            if re.search(r"C:\\Users|/Users/|/home/[a-z]+/", t) and fn != "run_script_tests.py":
                bad.append(fn + ":user path")
            if re.search("\u00c3[\u0080-\u00bf]|\u00e2\u20ac", t):
                bad.append(fn + ":mojibake")
    check("UTF-8 without BOM, no mojibake, and no user paths", not bad, str(bad))
    rd = open(os.path.join(PKG, "README.md"), encoding="utf-8").read()
    check("README covers Claude Code, Codex, and GitHub Copilot and the current-documentation notice",
          has(rd, "Claude Code", "Codex", "GitHub Copilot", "current documentation"), "")

    # ---- verifiers (require the extracted text)
    if a.src:
        rc, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        m = re.search(r"(\d+) positive, (\d+) negative", o)
        okc = rc == 0 and m and int(m.group(1)) >= 60 and int(m.group(2)) >= 15 and "Total failures: 0" in o
        check("verify_citations: >=60 positive, >=15 negative, 0 failures", bool(okc), o)
        rc, o = run([os.path.join("tests", "audit_tokens.py"), "--src", a.src])
        check("audit_tokens: 0 failures", rc == 0, o)
    else:
        print("INFO: use --src to run verify_citations.py and audit_tokens.py")

    print(f"\nSummary: {len(OK)} passed, {len(FAIL)} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
