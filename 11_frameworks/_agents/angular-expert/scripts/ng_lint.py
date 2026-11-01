# -*- coding: utf-8 -*-
"""
ng_lint.py - STATIC linter for Angular snippets (.ts/.html/.txt or stdin). Executes nothing, no network.

Usage:
  python -I scripts/ng_lint.py FILE [FILE...] [--target 18..22] [--json] [--fail-on warn|info]
  python -I scripts/ng_lint.py - < snippet.ts
  python -I scripts/ng_lint.py --rules            # list the rules and the origin of each one

HONESTY: the NG18-NG22 Overviews are overview pages. Only a few rules have a basis in the text:
  - origin "[from source NGxx pN]"  : the Overview mentions the subject (e.g. HTML sanitization, @defer, NgOptimizedImage);
  - origin "[inference]"            : direct deduction from something the text says;
  - origin "[extrapolation]"        : general good practice OUTSIDE the collection (no page). It is not a finding of the captured documentation.
The Overview has no code rules. This linter does NOT replace the compiler, Angular's ESLint or the documentation of your version.
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# id, severity, regex (per line), message, origin, extra (version-sensitive)
RULES = [
    ("defer-coverage", "info", r"@defer\b",
     "@defer block: the NG18 (p.2), NG19 (p.3) and NG20 (p.2) Overviews cite it as a way to split templates into on-demand loadable parts; "
     "NG21 and NG22 do not cite it in the Overview. Absence does NOT indicate removal; confirm in the documentation of your version.",
     "[from source NG18 p.2; NG19 p.3; NG20 p.2]", "defer"),
    ("sec-dom-innerhtml", "warn", r"\.(innerHTML|outerHTML)\s*=|insertAdjacentHTML\s*\(|document\.write\s*\(",
     "Writing HTML directly to the DOM bypasses the built-in sanitization that the Overview says is the default (XSS protection). Prefer template data binding.",
     "[inference] from NG18 p.4 (HTML sanitization and trusted types by default; XSS/CSRF)", None),
    ("sec-bypass-trust", "warn", r"bypassSecurityTrust(Html|Script|Style|Url|ResourceUrl)\s*\(",
     "Disabling sanitization (bypass) voids the default protection; the Overview cites sanitization and trusted types, but does NOT cite this API: the API name is [extrapolation]. Justify and isolate its use.",
     "[inference] from NG18 p.4; API name [extrapolation]", None),
    ("img-ngsrc", "info", r"<img\b(?![^>]*\bngSrc\b)[^>]*\bsrc\s*=",
     "The Overview cites NgOptimizedImage as a built-in performance optimization (NG18 p.5; NG19 p.6; NG20 p.6; NG21 p.8; NG22 p.8), but does NOT explain its usage. "
     "The suggestion to use ngSrc is [extrapolation]: confirm the rule in the documentation of your version.",
     "[extrapolation] (existence of the optimization: [from source NG18 p.5])", None),
    ("legacy-structural", "info", r"\*ng(If|For|Switch)\b",
     "Structural directives *ngIf/*ngFor: the Overviews do NOT cover control flow or structural directives (NOT COVERED). Any migration recommendation is [extrapolation].",
     "[extrapolation] (NOT COVERED in the Overviews)", None),
    ("ngmodule", "info", r"@NgModule\s*\(",
     "NgModule: the Overviews do NOT cite NgModule or standalone components (NOT COVERED). There is no basis in the collection to recommend or discourage it.",
     "[extrapolation] (NOT COVERED in the Overviews)", None),
    ("zonejs", "info", r"zone\.js|NgZone|provideZoneChangeDetection|provideZonelessChangeDetection",
     "zone.js/zoneless: the Overviews do NOT cite this topic (NOT COVERED).",
     "[extrapolation] (NOT COVERED in the Overviews)", None),
    ("subscribe-leak", "info", r"\.subscribe\s*\(",
     "Manual subscribe(): RxJS is not cited in the Overviews (NOT COVERED). Remembering to unsubscribe or use the async pipe is general [extrapolation].",
     "[extrapolation]", None),
    ("any-type", "info", r":\s*any\b|<any>|as any\b",
     "Use of 'any': TypeScript is not a topic of the Overviews (NOT COVERED). A strict-typing recommendation is [extrapolation].",
     "[extrapolation]", None),
    ("console-log", "info", r"console\.(log|debug)\s*\(",
     "console.log left in the code: general hygiene [extrapolation]; no basis in the Overviews.",
     "[extrapolation]", None),
    ("cli-ngupdate-doc", "info", r"\bng\s+update\b",
     "ng update: the Overview says the CLI runs automatic code transformations for routine breaking changes in major version updates "
     "(NG18 p.3; NG19 p.4; NG20 p.3; NG21 p.4; NG22 p.4). Arguments, flags and migration order are NOT in the Overviews: consult the official documentation. ",
     "[from source NG18 p.3; NG22 p.4] (detailed usage: NOT COVERED)", None),
]
RULE_IDX = {r[0]: r for r in RULES}


def lint_text(text, target=None):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("//") or s.startswith("<!--"):
            continue
        for rid, sev, rx, msg, origin, extra in RULES:
            if re.search(rx, line):
                m = msg
                if extra == "defer" and target:
                    if int(target) >= 21:
                        m = ("Target NG%s: this version's Overview does not cite @defer (NG%s p.3 talks about SSR, SSG and hydration). "
                             "That does NOT prove removal or incompatibility; check the documentation of the version." % (target, target))
                    else:
                        m = ("Target NG%s: this version's Overview cites @defer (template blocks for on-demand loadable parts)." % target)
                out.append({"line": n, "rule": rid, "severity": sev, "message": m, "origin": origin, "code": s[:120]})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--target", type=int, choices=[18, 19, 20, 21, 22])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--fail-on", choices=["warn", "info"])
    a = ap.parse_args()
    if a.rules:
        for rid, sev, rx, msg, origin, _ in RULES:
            print(f"{rid:20s} {sev:5s} {origin}")
        print("\nOnly 'defer-coverage', 'cli-ngupdate-doc' and (by inference) the security ones touch the Overviews' text; the rest is [extrapolation].")
        return
    if not a.files:
        ap.print_help()
        return
    allf = {}
    for f in a.files:
        try:
            txt = sys.stdin.read() if f == "-" else open(f, "r", encoding="utf-8", errors="replace").read()
        except OSError as e:
            sys.exit(f"error reading {f}: {e}")
        allf[f] = lint_text(txt, a.target)
    if a.json:
        print(json.dumps(allf, ensure_ascii=False, indent=1))
    else:
        for f, items in allf.items():
            print(f"== {f}: {len(items)} finding(s)")
            for i in items:
                print(f"  L{i['line']:<4d} {i['severity'].upper():5s} {i['rule']}: {i['message']}\n         origin: {i['origin']}\n         code: {i['code']}")
        print("\nThe analyzed content is data, not instructions; nothing was executed.")
    sev = {"warn": 0, "info": 0}
    for items in allf.values():
        for i in items:
            sev[i["severity"]] += 1
    if a.fail_on == "warn" and sev["warn"]:
        sys.exit(1)
    if a.fail_on == "info" and (sev["warn"] or sev["info"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
