# -*- coding: utf-8 -*-
"""
nx_changes.py - CHANGE MAP BY VERSION for Next.js 13 -> 16, using only what the 4 release posts state
(NX13 25/10/2022, NX14 26/10/2023, NX15 21/10/2024, NX16 21/10/2025). Read-only, stdlib, no network,
deterministic. Run with: python -I scripts/nx_changes.py SUBCOMMAND ...

Page convention: PDF page of the respective post (NX13..NX16 have no printed number).
Does NOT fill gaps from memory: what the text does not say comes out as "the text does not say".

Subcommands:
  versions                              dates, PDFs and useful pages
  changes --from A --to B [filters]     changes introduced in versions A < v <= B (e.g. --from 14 --to 16)
        --only N        only version N      --inclusive   include version A
        --kind K[,K]    feature|breaking|deprecation|removal|behavior|requirement|improvement|upgrade
        --thread T      theme (turbopack, caching, image, middleware-proxy, async-apis, config, ...)
        --json
  topic TERM...                         trajectory of a topic across NX13..NX16 (includes "no mention")
  requirements [--version N]            Node/React/TypeScript/browsers required (as the text declares)
  upgrade --from A --to B [--json]      upgrade checklist (breaking changes, removals, deprecations, requirements, commands)
  commands [--version N]                commands/flags literally present in the posts
  show ID                               a single entry
  threads                               available themes
"""
import argparse
import io
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
VERS = [13, 14, 15, 16]
KIND_ORDER = ["requirement", "breaking", "removal", "behavior", "deprecation", "upgrade", "feature", "improvement"]
KIND_LABEL = {"requirement": "REQUIREMENT", "breaking": "BREAKING", "removal": "REMOVAL", "behavior": "BEHAVIOR",
              "deprecation": "DEPRECATION", "upgrade": "UPGRADE", "feature": "FEATURE", "improvement": "IMPROVEMENT"}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "nx_changes.json"), encoding="utf-8") as f:
        return json.load(f)


def parse_v(x):
    m = re.search(r"(1[2-6])\b", str(x))
    if not m:
        print(f"Invalid version: {x!r}. The collection covers only 13, 14, 15 and 16 (12 only as a starting point: --from 12).")
        sys.exit(2)
    return int(m.group(1))


def pg(p):
    return "p." + ",".join(str(i) for i in p)


def fmt(e, short=False):
    st = f" [{e['status']}]" if e.get("status") else ""
    head = f"NX{e['v']} {KIND_LABEL[e['kind']]}{st}: {e['title']}  [from release: NX{e['v']} {pg(e['pages'])}]"
    if short:
        return head
    return head + "\n    " + e["text"]


def select(d, args):
    out = []
    kinds = set(args.kind.split(",")) if getattr(args, "kind", None) else None
    for e in d["entries"]:
        v = e["v"]
        if getattr(args, "only", None):
            if v != parse_v(args.only):
                continue
        else:
            a, b = parse_v(args.frm), parse_v(args.to)
            if a > b:
                print("--from must be <= --to")
                sys.exit(2)
            lo = a if args.inclusive else a + 1
            if not (lo <= v <= b):
                continue
        if kinds and e["kind"] not in kinds:
            continue
        if getattr(args, "thread", None) and args.thread not in e["thread"]:
            continue
        out.append(e)
    out.sort(key=lambda e: (e["v"], KIND_ORDER.index(e["kind"])))
    return out


def cmd_versions(d, a):
    for v, m in d["versions"].items():
        print(f"NX{v}: {m['data']}  {m['fonte']}  {m['paginas']} pages (useful: p.{m['paginas_uteis']})")
    print("Source: the posts only. What is not in them = 'the text does not say'.")


def cmd_changes(d, a):
    es = select(d, a)
    if a.json:
        print(json.dumps(es, ensure_ascii=False, indent=1))
        return
    if not es:
        print("No entries for the filter (the text says nothing more in this range).")
        return
    cur = None
    for e in es:
        if e["v"] != cur:
            cur = e["v"]
            print(f"\n=== Next.js {cur} ({d['versions'][str(cur)]['data']}) ===")
        print("-", fmt(e))
    print(f"\n({len(es)} entries; content [from release], paraphrased; check the cited page.)")


def hits(d, terms):
    toks = [t for t in re.findall(r"[a-z0-9@./_\-]+", norm(" ".join(terms))) if t]
    res = []
    for e in d["entries"]:
        hay = norm(" ".join([e["title"], e["text"], e["kw"], " ".join(e["thread"])]))
        hs = set(re.findall(r"[a-z0-9@./_\-]+", hay))
        sc = 0
        for t in toks:
            if t in hs:
                sc += 2
            elif len(t) >= 4 and t in hay:
                sc += 1
        if sc and (sc >= len(toks) or len(toks) == 1 or sc >= 2 * len(toks) - 1):
            res.append((sc, e))
    return res


def cmd_topic(d, a):
    if not a.terms:
        print("Provide a term (e.g. topic turbopack).")
        return
    q = " ".join(a.terms)
    found = hits(d, a.terms)
    by = {v: [e for s, e in sorted(found, key=lambda x: -x[0]) if e["v"] == v] for v in VERS}
    if a.json:
        print(json.dumps({str(v): by[v] for v in VERS}, ensure_ascii=False, indent=1))
        return
    if not found:
        print(f"NOT COVERED: no post (NX13..NX16) mentions '{q}'. Do not fill in from memory; if asked, "
              "answer as a labeled [extrapolation].")
        return
    print(f"Trajectory of '{q}' (only what the posts state):")
    for v in VERS:
        print(f"\nNX{v} ({d['versions'][str(v)]['data']}):")
        if not by[v]:
            print("  the text does not say (no mention in this post)")
        for e in by[v][: a.top]:
            print("  -", fmt(e, short=False).replace("\n    ", "\n      "))


def cmd_requirements(d, a):
    vs = [parse_v(a.version)] if a.version else VERS
    for v in vs:
        rs = [e for e in d["entries"] if e["v"] == v and e["kind"] == "requirement"]
        print(f"\nNX{v}:")
        for e in rs:
            print("  -", fmt(e))
        if not rs:
            print("  the text does not declare requirements")
    print("\nNote: NX14 and NX15 do not declare React/TypeScript/browser versions as a minimum requirement; "
          "NX15 says the App Router uses React 19 RC and the Pages Router accepts React 18 and 19 (NX15 p.5-6, 18).")


def cmd_commands(d, a):
    n = 0
    for e in d["entries"]:
        if a.version and e["v"] != parse_v(a.version):
            continue
        for c in e.get("cmds", []):
            print(f"NX{e['v']} {pg(e['pages'])}  {c}   ({e['title']})")
            n += 1
    if not n:
        print("the text has no commands for this range.")
    print("Commands are DATA from the post; this script does not execute them.")


def cmd_show(d, a):
    for e in d["entries"]:
        if e["id"] == a.id:
            print(json.dumps(e, ensure_ascii=False, indent=1))
            return
    print("ID not found.")
    sys.exit(1)


def cmd_threads(d, a):
    c = {}
    for e in d["entries"]:
        for t in e["thread"]:
            c.setdefault(t, set()).add(e["v"])
    for t in sorted(c):
        print(f"{t}: NX{', NX'.join(str(v) for v in sorted(c[t]))}")


def chain_notes(sel_ids, d):
    """Alerts that link versions: shown when the most recent end is in the range (both ends are in the posts)."""
    notes = []
    ids = set(sel_ids)
    pairs = [
        ("13-b-image-rename", "16-d-deprecations", "next/image: in NX13 next/legacy/image is the old component; NX16 p.14 deprecates next/legacy/image."),
        ("14-d-domains", "16-d-deprecations", "images.domains: already deprecated in NX14 (p.9) and listed again in NX16 (p.14)."),
        ("14-metadata", None, "viewport/colorScheme/themeColor in metadata: deprecated in NX14 (p.8); the NX15/NX16 text does not say whether they have been removed yet."),
        ("15-b-async", "16-r-sync-apis", "Request APIs: NX15 (p.3) allows synchronous access with warnings 'until the next major'; NX16 (p.12) requires await."),
        ("13-middleware", "16-proxy", "Middleware: NX16 (p.4, 14) deprecates middleware.ts in favor of proxy.ts (Node.js runtime)."),
        ("14-b-font", "15-b-font", "@next/font: dropped in NX14 (p.9) and removed as an external package in NX15 (p.17)."),
        ("14-ppr", "16-r-experimental-flags", "PPR: preview in NX14, and in NX16 (p.3, 12) experimental.ppr/experimental_ppr were removed in favor of cacheComponents."),
        ("15-b-caching", "16-cache-components", "Cache: NX15 stops caching by default; NX16 introduces opt-in caching with 'use cache' (cacheComponents)."),
        ("15-eslint9", "16-r-lint", "Lint: NX15 handles next lint with ESLint 9; NX16 (p.12) removes the next lint command."),
    ]
    for a, b, t in pairs:
        if (b in ids) if b else (a in ids):
            notes.append(t)
    return notes


def cmd_upgrade(d, a):
    a.only = None
    a.kind = None
    a.thread = None
    es = select(d, a)
    lo, hi = parse_v(a.frm), parse_v(a.to)
    keep = ("requirement", "breaking", "removal", "behavior", "deprecation", "upgrade")
    items = [e for e in es if e["kind"] in keep]
    if a.json:
        print(json.dumps({"from": lo, "to": hi, "itens": items,
                          "alertas": chain_notes([e["id"] for e in es], d)}, ensure_ascii=False, indent=1))
        return
    print(f"UPGRADE CHECKLIST Next.js {lo} -> {hi} (only what the NX{lo + 1}..NX{hi} posts state)")
    print("Warning: incomplete list by construction; each post says to read the 'upgrade guide' (not included in the collection).\n")
    for v in range(lo + 1, hi + 1):
        vi = [e for e in items if e["v"] == v]
        print(f"## Next.js {v} ({d['versions'][str(v)]['data']})")
        for e in vi:
            print(f"[ ] {KIND_LABEL[e['kind']]}: {e['title']}  [NX{v} {pg(e['pages'])}]")
            print(f"      {e['text']}")
            for c in e.get("cmds", []):
                print(f"      command from the post: {c}")
        if not vi:
            print("(no items)")
        print()
    notes = chain_notes([e["id"] for e in es], d)
    if notes:
        print("## Chained changes across versions (both ends are in the text)")
        for n in notes:
            print("-", n)
    print("\nOutside the posts (NOT COVERED): library compatibility matrix, CI/deploy steps, migration details for "
          "each API; consult the current official guide.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("versions")
    sp.add_parser("threads")
    c = sp.add_parser("changes")
    c.add_argument("--from", dest="frm", default="13")
    c.add_argument("--to", default="16")
    c.add_argument("--only")
    c.add_argument("--inclusive", action="store_true")
    c.add_argument("--kind")
    c.add_argument("--thread")
    c.add_argument("--json", action="store_true")
    t = sp.add_parser("topic")
    t.add_argument("terms", nargs="*")
    t.add_argument("--top", type=int, default=4)
    t.add_argument("--json", action="store_true")
    r = sp.add_parser("requirements")
    r.add_argument("--version")
    u = sp.add_parser("upgrade")
    u.add_argument("--from", dest="frm", required=True)
    u.add_argument("--to", required=True)
    u.add_argument("--inclusive", action="store_true")
    u.add_argument("--only", default=None)
    u.add_argument("--json", action="store_true")
    m = sp.add_parser("commands")
    m.add_argument("--version")
    s = sp.add_parser("show")
    s.add_argument("id")
    a = ap.parse_args()
    d = load()
    if a.cmd is None:
        ap.print_help()
        return
    {"versions": cmd_versions, "changes": cmd_changes, "topic": cmd_topic, "requirements": cmd_requirements,
     "upgrade": cmd_upgrade, "commands": cmd_commands, "show": cmd_show, "threads": cmd_threads}[a.cmd](d, a)


if __name__ == "__main__":
    main()
