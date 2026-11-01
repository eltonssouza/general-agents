# -*- coding: utf-8 -*-
"""
ng_lookup.py - topic lookup across the 5 Angular Overview captures (NG18..NG22).

Usage:
  python -I scripts/ng_lookup.py TERM [TERM...] [--json]   # concept(s) + pages per version, or NOT COVERED
  python -I scripts/ng_lookup.py --page 21 3                 # what the index detects on page N of the PDF of version V
  python -I scripts/ng_lookup.py --gaps                      # terms that NO Overview cites (verified)
  python -I scripts/ng_lookup.py --versions                  # summary of the 5 captures (pages, footer, useless pages)

Source: scripts/ng_index.json. Pages = PDF pages. Doc-capture based overview agent:
when the term is not in the Overviews the answer is "NOT COVERED" (not "does not exist").
Terms are accepted in Portuguese and English.
"""
import argparse
import json
import os
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
VERSIONS = [18, 19, 20, 21, 22]
# pt/en synonyms -> concept ids (curated; only points to concepts that exist in the index)
SYN = {
    "sinal": "signals", "signal": "signals", "reatividade": "fine-grained-reactivity", "reactivity": "fine-grained-reactivity",
    "defer": "defer-block", "adiado": "deferred-loading", "deferred": "deferred-loading", "lazy": "lazy-loadable-templates",
    "injecao": "dependency-injection", "di": "dependency-injection", "injection": "dependency-injection",
    "rota": "router", "roteamento": "router", "routing": "router", "route": "router", "guard": "router",
    "formulario": "forms", "form": "forms", "componente": "components", "component": "components",
    "servidor": "ssr", "server": "ssr", "hidratacao": "hydration", "estatico": "ssg", "static": "ssg",
    "seguranca": "security", "sanitizacao": "security", "sanitization": "security", "xss": "xss-csrf", "csrf": "xss-csrf",
    "internacionalizacao": "i18n", "internationalization": "i18n",
    "traducao": "i18n", "translation": "i18n", "update": "ng-update", "atualizacao": "ng-update", "upgrade": "ng-update",
    "migracao": "migration-schematics", "migration": "migration-schematics",
    "ide": "language-service", "vite": "vite-esbuild", "esbuild": "vite-esbuild", "build": "vite-esbuild",
    "lts": "release-lts", "release": "release-lts", "imagem": "ngoptimizedimage", "image": "ngoptimizedimage",
}
GAP_SYN = {
    "standalone": "standalone", "zoneless": "zoneless", "zone": "zoneless", "zone.js": "zoneless", "ngmodule": "ngmodule",
    "modulos": "ngmodule", "modules": "ngmodule", "@if": "control-flow", "@for": "control-flow", "@switch": "control-flow", "ngif": "control-flow",
    "ngfor": "control-flow", "computed": "computed-effect", "effect": "computed-effect", "linkedsignal": "computed-effect",
    "resource": "resource-api", "httpresource": "resource-api", "material": "angular-material", "cdk": "angular-material",
    "animacao": "animations", "animations": "animations", "animation": "animations", "teste": "testing", "testes": "testing",
    "test": "testing", "tests": "testing",
    "testing": "testing", "jasmine": "testing", "karma": "testing", "jest": "testing", "vitest": "testing",
    "typescript": "typescript", "rxjs": "rxjs", "observable": "rxjs", "inject": "inject-fn", "mcp": "ai-mcp", "ia": "ai-mcp",
    "ai": "ai-mcp", "llm": "ai-mcp", "webpack": "webpack", "pwa": "pwa-sw", "elements": "angular-elements", "aot": "aot-ivy",
    "ivy": "aot-ivy", "incremental": "incremental-hydration", "signal-forms": "signal-forms",
}


def strip(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def load():
    return json.load(open(os.path.join(HERE, "ng_index.json"), encoding="utf-8"))


def fmt_concept(c):
    cites = []
    for v in VERSIONS:
        pg = c["pages"].get(str(v))
        cites.append(f"NG{v}: " + (f"p.{','.join(map(str, pg))}" if pg else "not detected"))
    return f"{c['id']} [{c['group']}] {c['label']}\n    " + " | ".join(cites) + f"\n    note: {c['note']}"


def find(idx, terms):
    hits, gaps = [], []
    seen = set()
    for t in terms:
        k = strip(t)
        g = GAP_SYN.get(k) or GAP_SYN.get(k.strip("@"))
        if g:
            gaps.append((t, g))
            continue
        k2 = k.lstrip("@")
        cid = SYN.get(k2)
        found = []
        if cid:
            found = [c for c in idx["concepts"] if c["id"] == cid]
        if not found:  # 1) same id; 2) id contains; 3) label/note contains (only if nothing before)
            found = [c for c in idx["concepts"] if k2 and strip(c["id"]) == k2]
        if not found:
            found = [c for c in idx["concepts"] if k2 and k2 in strip(c["id"])]
        if not found:
            found = [c for c in idx["concepts"] if k2 and (k2 in strip(c["label"]) or k2 in strip(c["note"]))]
        if not found:
            gaps.append((t, None))
        for c in found:
            if c["id"] not in seen:
                seen.add(c["id"])
                hits.append(c)
    return hits, gaps


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--page", nargs=2, type=int, metavar=("VERSION", "PAGE"))
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--versions", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    idx = load()
    if a.versions:
        for v in VERSIONS:
            m = idx["meta"][str(v)]
            pc = ", ".join(f"p.{p}:{k}" for p, k in m["page_class"].items())
            print(f"NG{v}: {m['pages']} pages; label {m['nav_version_label']}; footer {m['footer_years']}; stamp {m['build_stamp'] or '-'}\n   {pc}")
        return
    if a.gaps:
        print("Terms that NONE of the 5 Overviews cites (verified by text pattern; NOT COVERED, does not mean nonexistent):")
        for g in idx["gaps"]:
            print(f"  - {g['label']}" + (f": FOUND in {g['found']}" if g["found"] else ""))
        return
    if a.page:
        v, p = a.page
        if str(v) not in idx["meta"] or not (1 <= p <= idx["meta"][str(v)]["pages"]):
            print(f"NOT COVERED: NG{v} p.{p} is outside the collection.")
            return
        cls = idx["meta"][str(v)]["page_class"][str(p)]
        print(f"NG{v} p.{p}: class '{cls}' (heuristic; cookie banner on every page)")
        for c in idx["concepts"]:
            if p in c["pages"].get(str(v), []):
                print(f"  - {c['label']}")
        return
    if not a.terms:
        ap.print_help()
        return
    hits, gaps = find(idx, a.terms)
    if a.json:
        print(json.dumps({"concepts": hits, "not_covered": [t for t, _ in gaps]}, ensure_ascii=False, indent=1))
        return
    for c in hits:
        print(fmt_concept(c))
    for t, g in gaps:
        extra = " (verified term: no Overview cites it)" if g else ""
        print(f"NOT COVERED: '{t}' does not appear in the NG18-NG22 Overviews{extra}. Any answer will be [extrapolation].")
    if hits:
        print("\nReminder: 'not detected' in a capture does NOT prove removal (see ng_diff.py).")


if __name__ == "__main__":
    main()
