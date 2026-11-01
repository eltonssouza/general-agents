# -*- coding: utf-8 -*-
"""
test_plan_generator.py - generates a COVERAGE plan/checklist of OWASP WSTG 4.2 cases from the declared scope.

Executes nothing against the target, uses no network, generates no payloads. It only selects guide IDs and lists pages and cautions
documented by the guide itself. The "feature -> tests" relation belongs to the package [inference]; the IDs and pages are [from source].

Usage:
  python -I scripts/test_plan_generator.py features                 # lists the known features
  python -I scripts/test_plan_generator.py plan --scope scope.json [--format md|json]
  python -I scripts/test_plan_generator.py plan --features auth,session,upload --authorized [--approach black|gray|white]
  python -I scripts/test_plan_generator.py sample                   # prints an example scope

Authorization gate: without declared authorization (scope.authorization.written=true or --authorized) the plan is NOT generated
(exit 3), unless --draft is passed (draft marked DO NOT EXECUTE). This does not replace a real contract/rules of engagement.
"""
import argparse
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))

BASE = ["INFO-01", "INFO-02", "INFO-03", "INFO-04", "INFO-05", "INFO-06", "INFO-07", "INFO-08", "INFO-10",
        "CONF-01", "CONF-02", "CONF-04", "CONF-05", "CONF-06", "CONF-07", "ERRH-01", "CRYP-01", "CRYP-03"]

FEATURES = {
    "auth": ("login/authentication", ["ATHN-01", "ATHN-02", "ATHN-03", "ATHN-04", "ATHN-05", "ATHN-06", "ATHN-07", "ATHN-08", "ATHN-09", "IDNT-04", "IDNT-05"]),
    "registration": ("registration and provisioning", ["IDNT-02", "IDNT-03", "IDNT-04", "IDNT-05"]),
    "roles": ("roles and access control", ["IDNT-01", "ATHZ-02", "ATHZ-03", "ATHZ-04"]),
    "session": ("sessions and cookies", ["SESS-01", "SESS-02", "SESS-03", "SESS-04", "SESS-05", "SESS-06", "SESS-07", "SESS-08", "SESS-09"]),
    "multichannel": ("alternative channels (mobile, call center, SSO, environments)", ["ATHN-10"]),
    "forms": ("forms and reflected/stored parameters", ["INPV-01", "INPV-02", "INPV-04", "INPV-17"]),
    "sql": ("relational database access", ["INPV-05", "INPV-05.1", "INPV-05.2", "INPV-05.3", "INPV-05.4", "INPV-05.5", "INPV-05.7"]),
    "nosql": ("NoSQL database", ["INPV-05.6"]),
    "ldap": ("LDAP directory", ["INPV-06"]),
    "xml": ("XML, XPath, SOAP", ["INPV-07", "INPV-09"]),
    "ssi": ("server-side includes", ["INPV-08"]),
    "mail": ("IMAP/SMTP webmail", ["INPV-10"]),
    "templates": ("server-side templates", ["INPV-18"]),
    "fetch-url": ("server fetches user-supplied URLs", ["INPV-19"]),
    "file-include": ("file inclusion by parameter", ["ATHZ-01", "INPV-11", "INPV-11.1", "INPV-11.2"]),
    "commands": ("OS command calls", ["INPV-12", "INPV-13"]),
    "proxies": ("proxy/cache chain", ["INPV-15", "INPV-16"]),
    "upload": ("file upload", ["BUSL-08", "BUSL-09", "CONF-03"]),
    "business-logic": ("business rules (cart, coupons, flows, limits)", ["BUSL-01", "BUSL-02", "BUSL-03", "BUSL-04", "BUSL-05", "BUSL-06", "BUSL-07"]),
    "spa": ("JavaScript-heavy front end / browser", ["CLNT-01", "CLNT-02", "CLNT-03", "CLNT-04", "CLNT-05", "CLNT-06", "CLNT-07", "CLNT-09", "CLNT-12", "CLNT-13", "INPV-14"]),
    "websockets": ("WebSockets", ["CLNT-10"]),
    "postmessage": ("postMessage / web messaging", ["CLNT-11"]),
    "graphql": ("GraphQL API", ["APIT-01"]),
    "cloud-storage": ("cloud storage", ["CONF-11"]),
    "dns": ("subdomains and DNS", ["CONF-10"]),
    "crypto": ("custom cryptography or client-side encrypted data", ["CRYP-02", "CRYP-04"]),
    "legacy-ria": ("legacy Flash/Silverlight", ["CONF-08", "CLNT-08"]),
    "filesystem": ("file permissions on the host", ["CONF-09"]),
}

# Cautions that the guide itself documents (id -> (text, page))
CAUTIONS = {
    "INFO-04": ("Unless the rules of engagement say otherwise, the guide wants to discover all reachable applications; confirm the scope before testing what is discovered.", 62),
    "CONF-01": ("DoS tests may not be feasible because of the unavailability they cause; tests may have unpredictable effects on the server.", 91),
    "CONF-02": ("Log-filling testing is 'dangerous in production environments'.", 96),
    "CONF-06": ("PUT: if a web shell is uploaded, overwrite it or warn the target's security team for immediate removal.", 112),
    "CONF-10": ("The guide's proof of concept claims the subdomain; only with express authorization.", 122),
    "CONF-11": ("The guide lists uploading and deleting objects; use an identifiable test file and only with express authorization.", 126),
    "IDNT-04": ("Enumerating accounts can lock them and lead to IP bans by WAF/IPS.", 137),
    "ATHN-02": ("A lockout policy can lock the administrative account.", 145),
    "ATHN-03": ("Use an account that can be locked; if there is only one account, run it at the end of the plan.", 148),
    "ATHN-04": ("Requires understanding the flow; bypass attempts by parameter/forced browsing only within scope.", 151),
    "SESS-03": ("Test with two accounts (victim and attacker), preferably on separate machines or browsers.", 198),
    "SESS-09": ("Test with two accounts (victim and attacker), preferably on separate machines or browsers.", 216),
    "BUSL-09": ("Web shell: protect it and remove it when done (p.376); decompression bomb only with written approval (p.377).", 376),
    "BUSL-07": ("The result comes from the observations of the other tests; keep notes throughout the execution.", 371),
    "INPV-05": ("Test one field at a time, keeping the others constant; automation requires a high volume of queries.", 238),
    "INPV-02": ("Browser exploitation frameworks (e.g., BeEF) only with specific authorization.", 227),
}

SAMPLE = {
    "target": "app.example.test (staging environment)",
    "authorization": {"written": True, "reference": "contract/SOW and rules of engagement (fill in)", "window": "YYYY-MM-DD to YYYY-MM-DD", "contact": "target technical owner"},
    "approach": "gray",
    "features": ["auth", "session", "roles", "forms", "sql", "upload", "business-logic", "spa"],
    "accounts": ["regular_user", "admin_user", "second_regular_user"],
    "destructive_allowed": False,
    "dos_allowed": False,
    "out_of_scope": ["third-party systems", "social engineering attacks"],
}


def load_index():
    with open(os.path.join(HERE, "wstg_index.json"), "r", encoding="utf-8") as f:
        return {e["id"]: e for e in json.load(f)["entries"]}


def build(scope, idx):
    feats = scope.get("features", [])
    unknown = [f for f in feats if f not in FEATURES]
    chosen = {}
    for i in BASE:
        chosen.setdefault(i, ["base"])
    for f in feats:
        if f in FEATURES:
            for i in FEATURES[f][1]:
                chosen.setdefault(i, []).append(f)
    def order(i):
        e = idx["WSTG-" + i]
        return e["pages"][0]
    ids = sorted(chosen, key=order)
    rows = []
    for i in ids:
        e = idx["WSTG-" + i]
        c = CAUTIONS.get(i)
        rows.append({"id": e["id"], "title": e["title"], "pages": e["pages"], "reference": e["reference"],
                     "why": chosen[i], "caution": ({"text": c[0], "page": c[1]} if c else None)})
    return rows, unknown


def render_md(scope, rows, unknown, draft):
    L = []
    L.append("# WSTG 4.2 coverage plan")
    if draft:
        L.append("\n> **DRAFT - DO NOT EXECUTE**: authorization not declared. Obtain authorization and rules of engagement before any test.")
    L.append(f"\n- Target: {scope.get('target', '(not provided)')}")
    au = scope.get("authorization", {})
    L.append(f"- Authorization: {au.get('reference', '(not provided)')} | window: {au.get('window', '(not provided)')} | contact: {au.get('contact', '(not provided)')}")
    L.append(f"- Approach: {scope.get('approach', 'black')} (the guide defines the ch.4 method as black box and cites gray/white-box per test; WSTG p.47)")
    L.append(f"- Test accounts: {', '.join(scope.get('accounts', [])) or '(none provided)'}")
    L.append(f"- Destructive actions allowed: {scope.get('destructive_allowed', False)} | DoS allowed: {scope.get('dos_allowed', False)}")
    L.append(f"- Out of scope: {', '.join(scope.get('out_of_scope', [])) or '(none provided)'}")
    L.append("\n## Notices")
    L.append("- [from source] The guide should not be used as a mere checklist: new vulnerabilities appear and time/resources must be reprioritized by business risk (WSTG p.8).")
    L.append("- [from source] Isolated security testing does not measure the application's security; combine it with code review and threat modeling (WSTG p.7, 22-23).")
    L.append("- [inference] This list only covers cases from the guide; business logic flaws require their own abuse cases (WSTG p.354).")
    if unknown:
        L.append(f"- Unknown features ignored: {', '.join(unknown)} (use 'features').")
    L.append("\n## Checklist")
    cur = None
    for r in rows:
        cat = r["id"].split("-")[1]
        if cat != cur:
            cur = cat
            L.append(f"\n### {cat}")
        a, b = r["pages"]
        pg = f"WSTG p.{a}" if a == b else f"WSTG p.{a}-{b}"
        L.append(f"- [ ] {r['id']} - {r['title']} ({pg}; references/{r['reference']}; reason: {', '.join(r['why'])})")
        if r["caution"]:
            L.append(f"  - Caution [from source] (WSTG p.{r['caution']['page']}): {r['caution']['text']}")
    L.append("\n## Log (fill in during execution)")
    L.append("For each test: date, who ran it, technique used, evidence (masking sensitive data), result, finding ID (see `finding_template.py`). The guide asks for a formal record of what was done, by whom and when (WSTG p.19).")
    L.append("\n## Boundaries")
    L.append("- Verification requirements and code review: `owasp-asvs-code-review-expert`. Threat modeling: `infosec-strategy-threat-modeling-expert`.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("features")
    sub.add_parser("sample")
    p = sub.add_parser("plan")
    p.add_argument("--scope")
    p.add_argument("--features")
    p.add_argument("--approach", default=None, choices=["black", "gray", "white"])
    p.add_argument("--authorized", action="store_true")
    p.add_argument("--draft", action="store_true")
    p.add_argument("--format", default="md", choices=["md", "json"])
    a = ap.parse_args()

    if a.cmd == "features":
        for k, (d, ids) in FEATURES.items():
            print(f"{k:<16} {d}  -> {', '.join('WSTG-' + i for i in ids)}")
        print("(base, always included): " + ", ".join("WSTG-" + i for i in BASE))
        return 0
    if a.cmd == "sample":
        print(json.dumps(SAMPLE, ensure_ascii=False, indent=2))
        return 0
    if a.cmd != "plan":
        ap.print_help()
        return 0

    scope = {}
    if a.scope:
        with open(a.scope, "r", encoding="utf-8") as f:
            scope = json.load(f)
    if a.features:
        scope["features"] = [x.strip() for x in a.features.split(",") if x.strip()]
    if a.approach:
        scope["approach"] = a.approach
    authorized = a.authorized or bool(scope.get("authorization", {}).get("written"))
    if not authorized and not a.draft:
        print("REFUSED: authorization not declared. Set scope.authorization.written=true (or --authorized) after obtaining authorization and rules of engagement; or use --draft for a draft marked DO NOT EXECUTE.", file=sys.stderr)
        return 3
    idx = load_index()
    rows, unknown = build(scope, idx)
    if a.format == "json":
        print(json.dumps({"draft": not authorized, "scope": scope, "tests": rows, "unknown_features": unknown}, ensure_ascii=False, indent=2))
    else:
        print(render_md(scope, rows, unknown, draft=not authorized), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
