# -*- coding: utf-8 -*-
"""
asvs_lookup.py - DETERMINISTIC lookup of the ASVS 4.0.3 requirements (and of the OCRG topic index).
Standard library only; no network; read-only (reads asvs_requirements.json, ocrg_index.json, gaps.json
next to the script). Run with `python -I`.

Usage:
  python -I scripts/asvs_lookup.py V2.1.1                  # by ID (V optional; accepts v4.0.3-2.1.1)
  python -I scripts/asvs_lookup.py 5.3.4 3.4.2 --json
  python -I scripts/asvs_lookup.py password --level L1     # by topic (en, or Portuguese keywords such as "senha"), filtered by level
  python -I scripts/asvs_lookup.py "sql injection" --limit 8
  python -I scripts/asvs_lookup.py --chapter 5 --level L1  # all L1 requirements of chapter V5
  python -I scripts/asvs_lookup.py --section 3.4
  python -I scripts/asvs_lookup.py --cwe 89
  python -I scripts/asvs_lookup.py --chapters              # chapters, pages, and counts
  python -I scripts/asvs_lookup.py --ocrg csrf             # OCRG topics only (PDF and printed pages)
  python -I scripts/asvs_lookup.py --gaps                  # terms verified absent from each source
  python -I scripts/asvs_lookup.py --validate              # checks the integrity/counts of the JSON
  python -I scripts/asvs_lookup.py --page-ocrg 152         # converts an OCRG PDF page to its printed page

Page convention: ASVS = footer number (PDF page = printed). OCRG = PDF page; printed = PDF - 1.
Level marks (as in the book): R = required (checkmark); O = recommended, not required; '-' = not required.
Labels: [from source] = text/page verified in the extracted data; [inference] = package mapping (ASVS<->OCRG).
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

# Expected counts (extracted by two independent methods: PDF coordinates and text; see tests/).
EXPECTED = {"rows_v1_v14": 286, "deleted": 8, "active": 278, "appendix_c": 34,
            "L1_required": 128, "L2_required": 258, "L2_recommended": 1, "L3_required": 278,
            "sections": 71, "chapters": 14}

# Theme map (Portuguese keywords, kept so Portuguese input still works) -> English terms that appear in the requirement text [inference: package vocabulary].
# English themes need no mapping: they match the requirement text directly.
THEMES = {
    "senha": ["password"], "senhas": ["password"], "autenticacao": ["authentication", "authenticator"],
    "sessao": ["session"], "sessoes": ["session"], "cookie": ["cookie"], "cookies": ["cookie"],
    "token": ["token"], "jwt": ["jwt", "stateless session token"], "oauth": ["oauth"],
    "controle de acesso": ["access control"], "autorizacao": ["authorization", "access control"],
    "idor": ["idor", "insecure direct object"], "csrf": ["csrf", "cross-site request forgery"],
    "xss": ["xss", "output encoding", "cross-site scripting"], "injecao": ["injection"],
    "sql": ["sql", "database quer"], "sqli": ["sql", "database injection", "parameterized"],
    "comando": ["command injection", "os command"], "xxe": ["xxe", "xml external"],
    "deserializacao": ["deserialization", "serialization"], "serializacao": ["serializ"],
    "validacao": ["validation", "validated"], "sanitizacao": ["sanitiz"], "encoding": ["encoding", "encode"],
    "criptografia": ["cryptograph", "encrypt"], "cripto": ["cryptograph"], "chave": ["key"], "chaves": ["key"],
    "segredo": ["secret"], "segredos": ["secret"], "aleatorio": ["random"], "aleatorios": ["random"],
    "hash": ["hash"], "salt": ["salt"], "tls": ["tls"], "https": ["tls", "https"], "certificado": ["certificate"],
    "log": ["log"], "logs": ["log"], "logging": ["log"], "auditoria": ["audit", "log"], "erro": ["error", "exception"],
    "erros": ["error", "exception"], "excecao": ["exception"], "upload": ["upload", "uploaded"], "arquivo": ["file"],
    "arquivos": ["file"], "ssrf": ["ssrf"], "redirecionamento": ["redirect"], "redirect": ["redirect"],
    "cors": ["cors", "cross-origin"], "csp": ["content security policy", "csp"], "cabecalhos": ["header"],
    "headers": ["header"], "api": ["api", "web service", "restful"], "rest": ["restful", "rest "], "graphql": ["graphql"],
    "soap": ["soap"], "dependencia": ["dependenc", "component", "librar"], "dependencias": ["dependenc", "component", "librar"],
    "sbom": ["software bill of materials", "sbom"], "build": ["build"], "pipeline": ["pipeline", "build"],
    "configuracao": ["configuration", "configur"], "debug": ["debug"], "privacidade": ["privacy", "personal"],
    "dados sensiveis": ["sensitive data", "sensitive"], "retencao": ["retention"], "backup": ["backup"],
    "mfa": ["multi-factor", "mfa", "otp"], "otp": ["otp", "one-time"], "sms": ["sms"], "biometria": ["biometric"],
    "phishing": ["phishing", "impersonation"], "forca bruta": ["brute force", "anti-automation"], "lockout": ["lockout"],
    "rate limit": ["rate limiting", "anti-automation"], "logica de negocio": ["business logic"], "race": ["race condition", "time of check"],
    "toctou": ["time of check", "toctou"], "memoria": ["memory", "buffer", "overflow"], "overflow": ["overflow"],
    "threat modeling": ["threat model"], "modelagem de ameacas": ["threat model"], "arquitetura": ["architecture"],
    "sdlc": ["software development lifecycle", "secure software development"], "codigo malicioso": ["malicious code", "back door", "time bomb"],
    "backdoor": ["back door"], "iot": ["iot", "embedded", "firmware"], "firmware": ["firmware"], "cdn": ["cdn", "content distribution"],
    "sri": ["subresource integrity"], "subdominio": ["subdomain"], "dns": ["dns"], "sandbox": ["sandbox"], "mass assignment": ["mass parameter assignment", "unsafe parameter assignment"],
    "redos": [], "navegador": ["browser"], "storage": ["storage"], "localstorage": ["localstorage", "browser storage"],
}

LEVELS = ("L1", "L2", "L3")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm(s):
    return re.sub(r"\s+", " ", strip_accents(s).lower()).strip()


def load_json(name):
    with open(os.path.join(HERE, name), "r", encoding="utf-8") as f:
        return json.load(f)


def marks(r):
    out = []
    for c in LEVELS:
        v = r[c]
        out.append("R" if v == "R" else ("O" if v == "O" else "-"))
    return "/".join(out)


def level_ok(r, level):
    return r.get(level) == "R"


def show_req(r, d, as_json=False):
    sec = d["sections"].get(r["section"], {})
    if as_json:
        return {"id": "V" + r["id"], "chapter": r["chapter"], "section": r["section"], "section_title": sec.get("title"),
                "asvs_page": r["page"], "levels(L1/L2/L3)": marks(r), "cwe": r.get("cwe"), "nist": r.get("nist"),
                "since": r.get("since"), "deleted": r["deleted"], "level_notes": r.get("level_notes"), "text": r["text"],
                "source": "[from source] ASVS p.%d" % r["page"]}
    lines = ["V%s  [ASVS p.%d]  levels L1/L2/L3: %s" % (r["id"], r["page"], marks(r))]
    lines.append("  section %s - %s" % (r["section"], sec.get("title", "?")))
    lines.append("  " + r["text"])
    extra = []
    if r.get("cwe"):
        extra.append("CWE " + r["cwe"])
    if r.get("nist"):
        extra.append("NIST 800-63b §" + r["nist"])
    if r.get("since"):
        extra.append("since " + r["since"])
    if r.get("level_notes"):
        extra.append("level notes: " + json.dumps(r["level_notes"], ensure_ascii=False))
    if r["deleted"]:
        extra.append("REMOVED in 4.0.3 (the numbering was not reused)")
    if extra:
        lines.append("  " + " | ".join(extra))
    lines.append("  source: [from source]")
    return "\n".join(lines)


def parse_id(tok):
    t = tok.strip()
    t = re.sub(r"^v?4\.0\.3-", "", t, flags=re.I)
    t = re.sub(r"^v", "", t, flags=re.I)
    if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{1,2}", t) or re.fullmatch(r"C\.\d{1,2}", t, flags=re.I):
        return t.upper() if t[0] in "cC" else t
    return None


def expand_terms(query):
    q = norm(query)
    terms = {q}
    toks = q.split()
    for t in toks:
        terms.add(t)
        for k, vs in THEMES.items():
            if t == k or q == k:
                terms.update(vs)
    if q in THEMES:
        terms.update(THEMES[q])
    # thematic phrases inside the query
    for k, vs in THEMES.items():
        if " " in k and k in q:
            terms.update(vs)
    return [t for t in terms if t]


def search_reqs(d, query, level=None, chapter=None, include_deleted=False, limit=10):
    terms = expand_terms(query)
    qtoks = [t for t in norm(query).split() if len(t) > 2]
    res = []
    for r in d["requirements"]:
        if r["deleted"] and not include_deleted:
            continue
        if chapter is not None and str(r["chapter"]) != str(chapter):
            continue
        if level and not level_ok(r, level):
            continue
        hay = norm(r["text"])
        sec = norm(d["sections"].get(r["section"], {}).get("title", ""))
        score = 0
        for t in terms:
            if re.search(r"(?<![a-z0-9])" + re.escape(t), hay):
                score += 2 if t in qtoks or t == norm(query) else 1
            if re.search(r"(?<![a-z0-9])" + re.escape(t), sec):
                score += 1
        if score:
            res.append((score, r))
    res.sort(key=lambda x: (-x[0], [int(p) if p.isdigit() else 0 for p in re.split(r"[.]", x[1]["id"])]))
    return [r for _, r in res[:limit]], len(res)


def ocrg_topics(idx, query):
    terms = set(expand_terms(query)) | {norm(query)}
    qtoks = [t for t in norm(query).split() if len(t) > 2]
    res = []
    for t in idx["topics"]:
        score = 0
        kws = [norm(k) for k in t["keywords"]] + [norm(t["title"]), norm(t["id"])]
        for q in set(qtoks) | {norm(query)}:
            for k in kws:
                if q == k:
                    score += 4
                elif q in k or (len(k) > 3 and k in q):
                    score += 2
        if score:
            res.append((score, t))
    res.sort(key=lambda x: -x[0])
    return [t for _, t in res]


def fmt_pages(pages):
    pages = sorted(set(pages))
    out, i = [], 0
    while i < len(pages):
        j = i
        while j + 1 < len(pages) and pages[j + 1] == pages[j] + 1:
            j += 1
        out.append(str(pages[i]) if i == j else "%d-%d" % (pages[i], pages[j]))
        i = j + 1
    return ",".join(out)


def show_topic(t, as_json=False):
    pdf = t["pages"]
    if as_json:
        return {"id": t["id"], "title": t["title"], "pdf_pages": fmt_pages(pdf), "printed_pages": fmt_pages([p - 1 for p in pdf]),
                "file": "references/" + t["ref"], "related_asvs[inference]": t["asvs"], "source": "[from source] OCRG p." + fmt_pages(pdf)}
    s = "OCRG p.%s (printed %s)  %s  -> references/%s" % (fmt_pages(pdf), fmt_pages([p - 1 for p in pdf]), t["title"], t["ref"])
    if t["asvs"]:
        s += "\n    Related ASVS [inference]: " + ", ".join("V" + a for a in t["asvs"])
    return s


def validate(d, idx):
    errs = []
    main = [r for r in d["requirements"] if r["chapter"] != "C"]
    appc = [r for r in d["requirements"] if r["chapter"] == "C"]
    active = [r for r in main if not r["deleted"]]
    c = {"rows_v1_v14": len(main), "deleted": len(main) - len(active), "active": len(active), "appendix_c": len(appc),
         "L1_required": sum(1 for r in active if r["L1"] == "R"), "L2_required": sum(1 for r in active if r["L2"] == "R"),
         "L2_recommended": sum(1 for r in active if r["L2"] == "O"), "L3_required": sum(1 for r in active if r["L3"] == "R"),
         "sections": len([k for k in d["sections"] if k != "C"]), "chapters": len([k for k in d["chapters"] if k != "C"])}
    for k, v in EXPECTED.items():
        if c.get(k) != v:
            errs.append("count %s: expected %s, got %s" % (k, v, c.get(k)))
    # sequence per section
    seq = {}
    for r in d["requirements"]:
        seq.setdefault(r["section"], []).append(r["id"])
    for sec, ids in seq.items():
        nums = [int(i.split(".")[-1]) for i in ids]
        if nums != list(range(1, len(nums) + 1)):
            errs.append("non-contiguous sequence in %s" % sec)
    for t in idx["topics"]:
        for a in t["asvs"]:
            if not any(r["id"] == a for r in d["requirements"]):
                errs.append("ocrg_index: ASVS %s does not exist (topic %s)" % (a, t["id"]))
    return c, errs


def main():
    ap = argparse.ArgumentParser(description="Lookup of ASVS 4.0.3 and the OCRG v2.0 index")
    ap.add_argument("query", nargs="*", help="IDs (V2.1.1) or topic (password, sql injection...)")
    ap.add_argument("--level", choices=LEVELS)
    ap.add_argument("--chapter")
    ap.add_argument("--section")
    ap.add_argument("--cwe")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--include-deleted", action="store_true")
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--ocrg", metavar="TOPIC")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--page-ocrg", type=int, metavar="N", help="converts an OCRG PDF page to its printed page")
    a = ap.parse_args()

    d = load_json("asvs_requirements.json")
    idx = load_json("ocrg_index.json")
    gaps = load_json("gaps.json")

    if a.page_ocrg is not None:
        n = a.page_ocrg
        if 1 <= n <= 220:
            printed = ("printed %d" % (n - 1)) if n >= 4 else "no printed number (cover/index/blank page)"
            print("OCRG: PDF p.%d = %s (convention: printed = PDF - 1)" % (n, printed))
        else:
            print("OCRG has 220 PDF pages; page out of range.")
        return

    if a.validate:
        c, errs = validate(d, idx)
        print(json.dumps(c, ensure_ascii=False))
        if errs:
            print("FAILURES:\n  " + "\n  ".join(errs))
            sys.exit(1)
        print("OK: counts and sequences match (V1-V14: %d rows, %d active, %d removed; Appendix C: %d)." %
              (c["rows_v1_v14"], c["active"], c["deleted"], c["appendix_c"]))
        return

    if a.gaps:
        print("Terms VERIFIED ABSENT (whole-word search in the extracted text; see tests/verify_citations.py).")
        for src in ("ocrg", "asvs", "ambos"):
            print("- %s: %s" % ("BOTH" if src == "ambos" else src.upper(), ", ".join(gaps[src])))
        print("For these topics answer NOT COVERED in the indicated source; outside knowledge becomes [extrapolation]/[DATED].")
        return

    if a.chapters:
        print("ASVS 4.0.3 chapters (page = footer = PDF)")
        for k in sorted(d["chapters"], key=lambda x: (x == "C", int(x) if x.isdigit() else 99)):
            rs = [r for r in d["requirements"] if str(r["chapter"]) == k]
            act = [r for r in rs if not r["deleted"]]
            print("V%s %-48s p.%-3d rows=%-3d active=%-3d L1=%-3d L2=%-3d L3=%-3d" % (
                k if k != "C" else "-C", d["chapters"][k]["title"][:48], d["chapters"][k]["page"], len(rs), len(act),
                sum(1 for r in act if r["L1"] == "R"), sum(1 for r in act if r["L2"] == "R"), sum(1 for r in act if r["L3"] == "R")))
        return

    if a.ocrg:
        ts = ocrg_topics(idx, a.ocrg)
        if not ts:
            hit = [src for src in ("ocrg", "ambos") if norm(a.ocrg) in [norm(x) for x in gaps[src]]]
            print("NOT COVERED in the OCRG for '%s'%s" % (a.ocrg, " (term verified absent from the text)" if hit else " (no index topic; term not verified as absent)"))
            return
        out = [show_topic(t, a.json) for t in ts[:a.limit]]
        print(json.dumps(out, ensure_ascii=False, indent=1) if a.json else "\n".join(out))
        return

    results = []
    tot = None
    if a.cwe or a.section or (a.chapter and not a.query):
        for r in d["requirements"]:
            if r["deleted"] and not a.include_deleted:
                continue
            if a.cwe and a.cwe not in (r.get("cwe") or "").split():
                continue
            if a.section and r["section"] != a.section.lstrip("Vv"):
                continue
            if a.chapter and str(r["chapter"]) != a.chapter.lstrip("Vv"):
                continue
            if a.level and not level_ok(r, a.level):
                continue
            results.append(r)
        tot = len(results)
        results = results[:a.limit * 100]
    elif a.query:
        ids = [parse_id(q) for q in a.query]
        if all(ids):
            for i in ids:
                m = [r for r in d["requirements"] if r["id"].lower() == i.lower()]
                if m:
                    results.append(m[0])
                else:
                    print("ID %s does not exist in ASVS 4.0.3 (V1-V14, C.1-C.34)." % i)
        else:
            qs = " ".join(a.query)
            results, tot = search_reqs(d, qs, a.level, a.chapter, a.include_deleted, a.limit)
            ts = ocrg_topics(idx, qs)[:5]
            if not results and not ts:
                srcs = []
                for src in ("ocrg", "asvs"):
                    if norm(qs) in [norm(x) for x in gaps[src] + gaps["ambos"]]:
                        srcs.append(src.upper())
                if srcs:
                    print("NOT COVERED: '%s' was verified as ABSENT from: %s." % (qs, ", ".join(srcs)))
                else:
                    print("Nothing found for '%s' (term not verified as absent; try synonyms)." % qs)
                return
            if not results and norm(qs) in [norm(x) for x in gaps["asvs"] + gaps["ambos"]]:
                print("NOT COVERED in the ASVS for '%s' (term verified absent from the text)." % qs)
            if a.json:
                print(json.dumps({"asvs": [show_req(r, d, True) for r in results], "ocrg": [show_topic(t, True) for t in ts]}, ensure_ascii=False, indent=1))
                return
            if results:
                print("== ASVS 4.0.3: %d result(s) (showing %d) ==" % (tot, len(results)))
                for r in results:
                    print(show_req(r, d))
                    print()
            if ts:
                print("== OCRG v2.0 (topics) ==")
                for t in ts:
                    print(show_topic(t))
            if not ts and norm(qs) in [norm(x) for x in gaps["ocrg"] + gaps["ambos"]]:
                print("NOT COVERED in the OCRG for '%s' (term verified absent from the text)." % qs)
            return
    else:
        ap.print_help()
        return

    if a.json:
        print(json.dumps([show_req(r, d, True) for r in results], ensure_ascii=False, indent=1))
        return
    print("== %d requirement(s) ==" % (tot if tot is not None else len(results)))
    for r in results:
        print(show_req(r, d))
        print()


if __name__ == "__main__":
    main()
