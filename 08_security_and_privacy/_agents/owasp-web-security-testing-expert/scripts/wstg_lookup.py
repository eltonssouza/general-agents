# -*- coding: utf-8 -*-
"""
wstg_lookup.py - locates OWASP WSTG 4.2 tests by ID or topic (read-only, no network, deterministic).

Usage:
  python -I scripts/wstg_lookup.py WSTG-SESS-03
  python -I scripts/wstg_lookup.py WSTG-v42-INFO-02          (accepts the versioned format)
  python -I scripts/wstg_lookup.py "session fixation" --top 3   (Portuguese terms also work: fixacao de sessao)
  python -I scripts/wstg_lookup.py --category ATHN           (lists the tests of the category)
  python -I scripts/wstg_lookup.py --page 202                (which tests cover the PDF page)
  python -I scripts/wstg_lookup.py --printed 200             (printed page -> PDF page)
  python -I scripts/wstg_lookup.py --list | --gaps | --datado

Page convention: PDF page (WSTG p.N); printed page = N - 2.
Output: [from source] = id/title/pages according to the guide's index; the index keywords (mostly Portuguese, so Portuguese
queries keep working) belong to the package [inference].
"""
import argparse
import json
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
OFFSET = 2

# Topics verified as ABSENT (no occurrence as a whole term) in the extracted text of WSTG 4.2.
# Each term may list alternatives separated by " / "; Portuguese alternates are kept so Portuguese queries still match.
GAPS = [
    ("jwt / json web token", "no occurrence; the guide has no test dedicated to JWT tokens"),
    ("saml / openid connect", "no occurrence; federation and SSO only appear generically in SESS-06 and ATHN-10"),
    ("oauth", "a single incidental occurrence (list of secret-search keywords, p.352); no OAuth test"),
    ("webauthn / passkeys / fido", "no occurrence"),
    ("sbom / slsa / software supply chain / cadeia de suprimentos de software", "no occurrence (SCA is cited only as a CI/CD tool, p.18)"),
    ("mass assignment", "no occurrence"),
    ("prototype pollution", "no occurrence"),
    ("content security policy / csp", "no occurrence; clickjacking covers X-Frame-Options and frame busting (p.402-411)"),
    ("nis2 / lgpd", "no occurrence; the guide only cites GDPR, GLBA, SB-1386, PCI DSS, FFIEC as examples (p.18, 26)"),
    ("dread", "no occurrence; threat modeling cites STRIDE and NIST 800-30 (p.20, 27)"),
    ("kubernetes / serverless / azure / gcp / terraform", "no occurrence; cloud only in CONF-11 (S3) and CONF-10"),
    ("http/2 e http/3", "no occurrence"),
    ("epss", "no occurrence; severity cites CVSS (p.35, 441-442)"),
    ("race condition as a dedicated test / race condition como teste dedicado / condicao de corrida", "there is no race condition test; 'race' appears as a coverage approach in INFO-07 (p.76)"),
    ("nuclei", "no occurrence"),
]

DATADO = [
    "Flash/Silverlight/applets/ActionScript (CONF-08, CLNT-08) are obsolete.",
    "Web SQL (INPV-05.8) is a discontinued technology.",
    "CMS and framework cookie/keyword tables (INFO-08, p.83-84) and HPP-by-technology tables (INPV-04, p.233) date from 2009-2020.",
    "Numeric cryptography and TLS values (CRYP-01, CRYP-04; e.g., 398-day certificate, 2048 bits, 10,000 PBKDF2 iterations) reflect 2020.",
    "Note on XST/TRACE (CONF-06): the guide itself says it only works today with Flash.",
    "Tool lists (Appendix A, p.444-447) and search engine lists (INFO-01) are from 2020.",
    "The guide cites Top 10 2013/2017 and ASVS 4.0.x; check the current edition.",
    "Session timeout values (15 min banks; 60 min forums) are the 2020 guide's recommendations.",
]


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with open(os.path.join(HERE, "wstg_index.json"), "r", encoding="utf-8") as f:
        return json.load(f)["entries"]


def fmt(e):
    a, b = e["pages"]
    pg = f"p.{a}" if a == b else f"p.{a}-{b}"
    pr = f"printed {a - OFFSET}" if a == b else f"printed {a - OFFSET}-{b - OFFSET}"
    lines = [f"{e['id']} | {e['title']}", f"  category: {e['category']}", f"  [from source] WSTG {pg} ({pr})", f"  reference: references/{e['reference']}"]
    if e.get("status"):
        lines.append(f"  status: {e['status']}")
    if e.get("note"):
        lines.append(f"  note: {e['note']}")
    return "\n".join(lines)


def canon_id(q):
    q = q.strip().upper().replace("_", "-")
    q = re.sub(r"^WSTG-V\d+-", "WSTG-", q)
    if re.fullmatch(r"[A-Z]{4}-\d{1,2}(\.\d)?", q):
        q = "WSTG-" + q
    m = re.fullmatch(r"(WSTG-[A-Z]{4})-(\d{1,2})(\.\d)?", q)
    if m:
        q = f"{m.group(1)}-{int(m.group(2)):02d}{m.group(3) or ''}"
    return q


def search(entries, query, top):
    qn = norm(query)
    toks = [t for t in re.split(r"[^a-z0-9._-]+", qn) if len(t) > 1]
    scored = []
    for e in entries:
        hay = norm(e["title"] + " " + e["keywords"] + " " + e["category"])
        sc = 0
        if qn and qn in hay:
            sc += 5
        for t in toks:
            if re.search(r"(?<![a-z0-9])" + re.escape(t), hay):
                sc += 1
        if sc:
            scored.append((sc, e))
    scored.sort(key=lambda x: (-x[0], x[1]["pages"][0]))
    return [e for _, e in scored[:top]]


def main():
    ap = argparse.ArgumentParser(description="Lookup WSTG 4.2")
    ap.add_argument("query", nargs="*")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--category")
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--datado", action="store_true")
    a = ap.parse_args()
    E = load()

    if a.gaps:
        print("NOT COVERED in WSTG 4.2 (verified by searching the extracted text; answer 'NOT COVERED' and, if useful, [extrapolation]):")
        for t, why in GAPS:
            print(f"- {t}: {why}")
        return 0
    if a.datado:
        print("[DATED] WSTG 4.2 (2020) items that need current verification:")
        for d in DATADO:
            print("- " + d)
        return 0
    if a.list:
        for e in E:
            print(f"{e['id']:<14} p.{e['pages'][0]}-{e['pages'][1]:<4} {e['title']}")
        return 0
    if a.printed is not None:
        print(f"printed page {a.printed} = PDF page {a.printed + OFFSET}")
        return 0
    if a.page is not None:
        hits = [e for e in E if e["pages"][0] <= a.page <= e["pages"][1]]
        print(f"PDF page {a.page} (printed {a.page - OFFSET}):")
        if not hits:
            print("  no test mapped (index page, opening page or outside the map).")
        for e in hits:
            print("  " + fmt(e).replace("\n", "\n  "))
        return 0
    if a.category:
        c = a.category.upper()
        sel = [e for e in E if e["id"].startswith("WSTG-" + c)]
        if not sel:
            print(f"NOT COVERED: unknown category {c}. Categories: INFO CONF IDNT ATHN ATHZ SESS INPV ERRH CRYP BUSL CLNT APIT")
            return 0
        for e in sel:
            print(fmt(e))
        return 0
    if not a.query:
        ap.print_help()
        return 0

    q = " ".join(a.query)
    cid = canon_id(q)
    exact = [e for e in E if e["id"] == cid]
    if exact:
        print(fmt(exact[0]))
        return 0
    qn = norm(q)
    for term, why in GAPS:
        for alt in re.split(r"\s*/\s*", term):
            if norm(alt) == qn:
                print(f"NOT COVERED: '{q}' is not in WSTG 4.2. {why}")
                print("Answer as [extrapolation] and recommend checking current sources; consider referring to ASVS/Code Review.")
                return 0
    hits = search(E, q, a.top)
    if not hits:
        print(f"NOT COVERED: no test or topic in the index matches '{q}'. Do not cite a page; reason as [extrapolation] or refer onward.")
        return 0
    for e in hits:
        print(fmt(e))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
