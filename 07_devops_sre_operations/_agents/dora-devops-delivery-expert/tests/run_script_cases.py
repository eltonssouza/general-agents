# -*- coding: utf-8 -*-
"""
run_script_cases.py - runs the test cases that depend on the scripts (deterministic) and checks the output.

Usage: python -I tests/run_script_cases.py
Read-only, no network. Exit 0 if all pass.
"""
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(PKG, "scripts")


def run(script, *args):
    p = subprocess.run([sys.executable, "-I", os.path.join(S, script), *args], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, (p.stdout + p.stderr)


# (id, script, args, expected_rc, must_contain[], must_not_contain[])
CASES = [
    ("T04", "dora_classify.py", ["classify", "--lead-time", "3d", "--deploy-freq", "2/week", "--cfr", "12", "--recovery", "5h", "--rework", "8"], 0,
     ["Change lead time [3d]: High", "Deploy frequency [2/week]: High", "Medium (10%)", "High/Medium", "NOT COVERED: the report does not publish a per-level range", "overall level"], ["Elite |"]),
    ("T05", "dora_classify.py", ["classify", "--lead-time", "8mo"], 0, ["outside the report's ranges"], []),
    ("T06", "dora_classify.py", ["classify", "--recovery", "3d"], 0, ["NOT covered by the table"], []),
    ("T07", "dora_classify.py", ["classify", "--cfr", "15"], 0, ["AMBIGUOUS"], []),
    ("T08", "dora_classify.py", ["classify", "--rework", "20"], 0, ["NOT COVERED"], []),
    ("T08b", "dora_classify.py", ["classify", "--lead-time", "12h", "--deploy-freq", "on-demand", "--cfr", "4", "--recovery", "30m"], 0,
     ["[12h]: Elite", "[on-demand]: Elite", "[30m]: Elite"], []),
    ("T08c", "dora_classify.py", ["classify", "--lead-time", "abc"], 1, ["ERRO"], []),
    ("T09", "dora_effects.py", ["estimate", "--capability", "ai", "--outcome", "estabilidade"], 0, ["-7.2%", "p.40", "does NOT cross zero"], []),
    ("T10a", "dora_effects.py", ["estimate", "--capability", "ai", "--outcome", "estabilidade", "--increase", "50"], 2, ["NOT COVERED"], ["-14.4"]),
    ("T10b", "dora_effects.py", ["estimate", "--capability", "ai", "--outcome", "estabilidade", "--increase", "50", "--linear"], 0, ["[extrapolation]", "-14.40%", "NOT in the report"], []),
    ("T12", "dora_effects.py", ["show", "--capability", "plataforma"], 0, ["+8%", "+10%", "+6%", "-8%", "-14%"], []),
    ("T15", "dora_effects.py", ["estimate", "--capability", "ai", "--outcome", "produtividade"], 0, ["+2.1% per +25%", "p.32"], []),
    ("T15b", "dora_effects.py", ["estimate", "--capability", "ai", "--outcome", "produto"], 0, ["CROSSES zero"], []),
    ("T15c", "dora_effects.py", ["estimate", "--capability", "xyz", "--outcome", "burnout"], 2, ["NOT COVERED"], []),
    ("T18", "dora_lookup.py", ["MTTR"], 0, ["failed deployment recovery time", "GAP"], []),
    ("T19", "dora_lookup.py", ["trunk-based"], 2, ["NOT COVERED"], []),
    ("T19b", "dora_lookup.py", ["kubernetes"], 2, ["NOT COVERED"], []),
    ("T29", "dora_lookup.py", ["elite vs low"], 0, ["p.15"], []),
    ("T14", "dora_lookup.py", ["causalidade"], 0, ["p.105-106", "110-111"], []),
    ("T23", "dora_lookup.py", ["2025"], 2, ["NOT COVERED"], []),
    ("T20", "dora_lookup.py", ["carrot cake recipe"], 2, ["NOT COVERED"], []),
    ("T16", "dora_lookup.py", ["ranking de desenvolvedores"], 2, ["p.74"], []),
]


def main():
    bad = 0
    for cid, script, args, rc_exp, must, mustnot in CASES:
        rc, out = run(script, *args)
        miss = [m for m in must if m not in out]
        extra = [m for m in mustnot if m in out]
        ok = rc == rc_exp and not miss and not extra
        print(f"{cid}: {'OK' if ok else 'FAIL'}  ({script} {' '.join(args)})")
        if not ok:
            bad += 1
            print(f"   rc={rc} (expected {rc_exp}); missing={miss}; unexpected={extra}")
            print("   output:", out[:600].replace("\n", " | "))
    print(f"RESULT: {len(CASES) - bad}/{len(CASES)} OK")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
