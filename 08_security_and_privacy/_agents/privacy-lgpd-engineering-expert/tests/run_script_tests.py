# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the cases of tests/casos.json that have a command (package scripts) and checks the
expected outputs (substrings), forbidden outputs and exit code. It also checks data integrity
(no duplicate ids, valid JSON) and that all scripts run with `python -I` without a network.

Usage (Python 3, stdlib):
  python -I tests/run_script_tests.py            # from the package root or any folder
Exit codes: 0 all good; 1 there are failures.
"""
import io
import json
import os
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)


def run(cmd):
    p = subprocess.run([sys.executable, "-I"] + cmd, cwd=PKG, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def main():
    with io.open(os.path.join(HERE, "casos.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    casos = data["casos"]
    fails = []
    ids = [c["id"] for c in casos]
    if len(ids) != len(set(ids)):
        fails.append("duplicate ids in casos.json")
    n = 0
    for c in casos:
        if not c.get("cmd"):
            continue
        n += 1
        rc, out = run(c["cmd"])
        if rc != c.get("exit_code", 0):
            fails.append("%s: exit %s != %s" % (c["id"], rc, c.get("exit_code", 0)))
        for s in c.get("contains", []):
            if s not in out:
                fails.append("%s: output does not contain %r" % (c["id"], s))
        for s in c.get("not_contains", []):
            if s in out:
                fails.append("%s: output contains the forbidden %r" % (c["id"], s))
    # data integrity
    for fn in ("privacy_index.json", "checklist_items.json", "lgpd_nist_mapping.json"):
        try:
            with io.open(os.path.join(PKG, "scripts", fn), "r", encoding="utf-8") as f:
                json.load(f)
        except Exception as e:
            fails.append("Invalid JSON %s: %s" % (fn, e))
    # checklist: unique ids and valid pages
    with io.open(os.path.join(PKG, "scripts", "checklist_items.json"), "r", encoding="utf-8") as f:
        ck = json.load(f)
    cid = [i["id"] for i in ck["items"]]
    if len(cid) != len(set(cid)):
        fails.append("duplicate ids in the checklist")
    for i in ck["items"]:
        for p in i["pages"]:
            lim = 49 if i["origem"] == "nist" else 25
            if not (1 <= p <= lim):
                fails.append("checklist %s: page out of range %s" % (i["id"], p))
    # map: valid levels
    with io.open(os.path.join(PKG, "scripts", "lgpd_nist_mapping.json"), "r", encoding="utf-8") as f:
        mp = json.load(f)
    for r in mp["rows"]:
        if r["nivel"] not in ("TEXTUAL", "INFERENCE", "NO_SUPPORT"):
            fails.append("map %s: invalid level" % r["id"])
        if r["nivel"] == "TEXTUAL" and (not r["lgpd_termos"] or not r["nist_termos"]):
            fails.append("map %s: TEXTUAL requires terms on both sides" % r["id"])
    # help commands of the scripts
    for s in ("privacy_lookup.py", "compliance_checklist.py", "map_lgpd_nist.py", "ripd_templates.py"):
        rc, out = run([os.path.join("scripts", s), "-h"])
        if rc != 0:
            fails.append("%s -h failed (rc=%s)" % (s, rc))
    print("Cases with a command executed: %d of %d" % (n, len(casos)))
    if fails:
        print("FAILURES (%d):" % len(fails))
        for x in fails:
            print(" - " + x)
        return 1
    print("OK: all cases with a command passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
