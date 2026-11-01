# -*- coding: utf-8 -*-
"""
run_script_tests.py - deterministic tests of the 3 scripts (nx_changes, nx_lint, nx_lookup) against the fixtures.
Usage: python -I tests/run_script_tests.py   (exit 0 if everything passes). No network; does not execute the framework.
Each test: (id, args, expected exit, snippets that MUST appear, snippets that MUST NOT appear).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, ".."))
S = os.path.join(PKG, "scripts")
FX = os.path.join(HERE, "fixtures")
CH, LI, LK = (os.path.join(S, n) for n in ("nx_changes.py", "nx_lint.py", "nx_lookup.py"))

T = [
    ("T01 changes 14->16 breaking/removal", [CH, "changes", "--from", "14", "--to", "16", "--kind", "breaking,removal"], 0,
     ["Async request APIs", "next lint command removed", "NX15 p.", "NX16 p.12"], ["NX14 BREAKING"]),
    ("T02 requirements 16", [CH, "requirements", "--version", "16"], 0, ["20.9", "5.1.0", "Safari 16.4+"], []),
    ("T03 requirements 14 (Node only)", [CH, "requirements", "--version", "14"], 0, ["18.17"], ["Minimum TypeScript"]),
    ("T04 topic caching goes through 13, 15 and 16", [CH, "topic", "caching"], 0, ["NX13", "force-cache", "NX15", "NX16", "Cache Components"], []),
    ("T05 topic middleware -> NX14 no mention", [CH, "topic", "middleware"], 0, ["NX14", "the text does not say", "proxy.ts"], []),
    ("T06 topic unstable_after -> NX16 no mention", [CH, "topic", "unstable_after"], 0, ["NX15", "NX16 (2025-10-21):\n  the text does not say"], []),
    ("T07 topic outside the collection", [CH, "topic", "graphql"], 0, ["NOT COVERED"], []),
    ("T08 upgrade 15->16", [CH, "upgrade", "--from", "15", "--to", "16"], 0,
     ["UPGRADE CHECKLIST Next.js 15 -> 16", "[ ] REMOVAL", "npx @next/codemod@canary upgrade latest", "Chained changes", "upgrade guide"], ["## Next.js 15"]),
    ("T09 upgrade 12->14 starts with React 18.2", [CH, "upgrade", "--from", "12", "--to", "14"], 0, ["Minimum React 18.2.0", "next export", "## Next.js 13"], []),
    ("T10 commands 15", [CH, "commands", "--version", "15"], 0, ["next-async-request-api", "react@rc"], ["next dev --webpack"]),
    ("T11 invalid version (17) = error", [CH, "changes", "--from", "14", "--to", "17"], 2, ["Invalid version"], []),
    ("T12 changes 16->16 empty", [CH, "changes", "--from", "16", "--to", "16"], 0, ["No entries"], []),
    ("T13 lint app-ruim target 16 fails", [LI, os.path.join(FX, "app-ruim"), "--target", "16"], 1,
     ["NXL001", "NXL004", "NXL005", "NXL007", "NXL009", "NXL010", "NXL011", "NXL012", "NXL018", "NXL019", "NXL020", "NXL032",
      "NXP002", "NXP003", "NXL090"], []),
    ("T14 lint app-bom target 16 clean", [LI, os.path.join(FX, "app-bom"), "--target", "16"], 0, ["0 error(s), 0 warning(s), 0 info"], []),
    ("T15 severity depends on the target: async APIs in 14 = nothing", [LI, os.path.join(FX, "app-ruim", "app", "blog", "page.tsx"), "--target", "14"], 1,
     ["NXL001", "NXL004"], ["NXL007", "NXL008", "NXL010"]),
    ("T16 async APIs in 15 = warning", [LI, os.path.join(FX, "app-ruim", "app", "blog", "page.tsx"), "--target", "15"], 1,
     ["[WARN] NXL007"], ["[ERROR] NXL007"]),
    ("T17 parallel routes only fail in 16", [LI, os.path.join(FX, "app-ruim"), "--target", "15"], 1, [], ["NXL032"]),
    ("T18 injection in comment/string does not change the result", [LI, os.path.join(FX, "injecao"), "--target", "16"], 1,
     ["NXL007"], ["IGNORE ALL", "perfect", "system prompt"]),
    ("T19 DATED rule is informational", [LI, os.path.join(FX, "app-ruim", "pages", "old.js"), "--target", "16"], 0,
     ["[INFO] NXL090", "DATED: NXHB p.58-60", "Do not claim deprecation"], ["ERROR"]),
    ("T20 list-rules", [LI, "--list-rules"], 0, ["NXL001", "NXL032", "NXP001"], []),
    ("T21 lookup getInitialProps -> NXHB", [LK, "getInitialProps"], 0, ["NXHB", "DATED", "56"], []),
    ("T22 lookup --conflicts", [LK, "--conflicts"], 0, ["C01", "NXHB p.41,42", "NX13 p.11,14", "C06", "silence"], []),
    ("T23 lookup --page NXHB 42", [LK, "--page", "NXHB", "42"], 0, ["Link"], []),
    ("T24 lookup React Native = NOT COVERED", [LK, "react", "native"], 0, ["NOT COVERED", "mobile-frameworks-expert"], []),
    ("T25 lookup --gaps", [LK, "--gaps"], 0, ["NOT COVERED", "Next.js 17"], []),
    ("T26 lookup --sources", [LK, "--sources"], 0, ["NX16", "21/10/2025", "NXHB", "19/11/2019"], []),
]


def run(args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-I"] + args, capture_output=True, text=True, encoding="utf-8", env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    bad = 0
    for tid, args, code, must, mustnot in T:
        rc, out = run(args)
        errs = []
        if rc != code:
            errs.append(f"exit {rc} != {code}")
        for m in must:
            if m not in out:
                errs.append(f"missing: {m!r}")
        for m in mustnot:
            if m in out:
                errs.append(f"should not contain: {m!r}")
        print(("OK   " if not errs else "FAIL "), tid, "" if not errs else "; ".join(errs))
        bad += bool(errs)
    print(f"{len(T) - bad}/{len(T)} tests passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
