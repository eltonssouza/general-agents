# -*- coding: utf-8 -*-
"""
ng_build_index.py - (re)generates scripts/ng_index.json from the text extracted from the 5 "Angular-NN-Overview" PDFs.

Usage:  python -I scripts/ng_build_index.py --src PATH/scratch/frameworks [--out scripts/ng_index.json] [--show]
Read-only on the .txt files; no network; executes nothing from the target.

Page convention: N = PDF page (marker "=== PAGE N ===" in the extracted text).
Each PDF is a CAPTURE of the "What is Angular?" page (Overview) of the documentation, not a book.
The index stores, per concept and per version, the pages where a text pattern appears; the source
text is NOT copied into the index (only pages and notes in our own words).
The absence of a concept in a capture NEVER means removal/nonexistence in the framework.
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

VERSIONS = [18, 19, 20, 21, 22]
NPAGES = {18: 6, 19: 7, 20: 7, 21: 9, 22: 9}
FILE = "Angular-{v}-Overview.txt"

# (id, group, English label, regex over normalized lowercase text, note in our own words)
CONCEPTS = [
    # --- framing
    ("web-framework", "framing", "Angular presented as a web framework (fast and reliable)", r"web framework that empowers", "Opening sentence of the Overview."),
    ("users-love", "framing", "Tagline with 'users love'", r"users love", "Variation of the opening sentence."),
    ("angular-dev-home", "framing", "Angular.dev as the official home of the documentation", r"official home for angular documentation", "Sentence that appears only in the newer captures."),
    ("essentials-tutorials", "framing", "Invitation to Essentials and Tutorials", r"essentials", "Links to a quick overview and a step-by-step guide."),
    ("google-maintained", "framing", "Maintained by a dedicated team at Google", r"maintained by a dedicated team at google", "Origin/maintenance."),
    ("scale", "framing", "Scales with team size and codebase size", r"scale with both the size of your team", "Scalability promise."),
    # --- development features
    ("components", "feature", "Components (code encapsulated in parts)", r"well-?\s*encapsulated parts", "Description of components."),
    ("opinionated-component-model", "feature", "Headline 'opinionated component model + flexible DI'", r"opinionated component model", "Only in captures 18-20."),
    ("dependency-injection", "feature", "Dependency injection (any mention)", r"dependency injection", "Includes the mention in the DevTools DI tree."),
    ("di-modular-testable", "feature", "DI for modular, decoupled, testable code", r"modular, loosely", "DI text in captures 18-20."),
    ("di-share-code", "feature", "DI as code sharing across components", r"share code across", "DI wording in captures 21-22."),
    ("never-miss-version", "tool", "Headline 'never miss a version with ng update'", r"never miss a version", "Only in captures 18-20."),
    ("perf-targets-headline", "feature", "Headline 'meet your performance targets with SSR, SSG, hydration...'", r"meet your performance targets", "Only in captures 18-20."),
    ("guarantee-works-headline", "feature", "Headline 'guarantee everything works together' (first-party modules)", r"guarantee everything works", "Only in captures 18-20."),
    ("explore-links", "framing", "'Explore Dependency Injection/Routing/Forms' links", r"explore forms|explore angular routing|explore dependency injection", "Per-feature cards in captures 21-22."),
    ("keep-large-teams", "scale", "Headline 'keep large teams productive with Vite and esbuild'", r"keep large teams productive", "Build section."),
    ("signals", "feature", "Signals (fine-grained reactivity)", r"signals", "Cited as the basis of reactivity."),
    ("fine-grained-reactivity", "feature", "Fine-grained reactivity", r"fine-?\s*grained reactivity", "Description of the reactivity model."),
    ("compile-time-optimizations", "feature", "Compile-time optimizations", r"compile-?\s*time", "Tied to reactivity."),
    ("ssr", "feature", "Server-side rendering (SSR)", r"server-?\s*side\s+rendering", "SSR is cited."),
    ("ssg", "feature", "Static site generation (SSG)", r"static site\s+generation", "SSG is cited."),
    ("hydration", "feature", "Full DOM hydration", r"hydration", "Hydration is cited."),
    ("deferred-loading", "feature", "Deferred loading", r"deferred loading", "Phrase from the performance card headline."),
    ("defer-block", "feature", "@defer block in templates", r"@defer", "'@defer' text/link; in NG18-NG20 there is also an inline code snippet that the extraction leaves blank (checked by rendering only in NG18 p.2)."),
    ("lazy-loadable-templates", "feature", "Templates split into on-demand loadable parts", r"lazy-?\s*loadable", "Description of the @defer block."),
    ("router", "feature", "Router (guards, data resolution, lazy-loading)", r"route\s+guards", "Description of routing."),
    ("forms", "feature", "Forms (standardized participation and validation)", r"form participation", "Description of forms."),
    ("first-party-modules", "feature", "First-party forms and routing modules as a single card", r"first-?\s*party modules for", "'Guarantee everything works together' headline in captures 18-20."),
    # --- tools
    ("cli", "tool", "Angular CLI (project running in under a minute)", r"under a minute", "Description of the CLI."),
    ("devtools", "tool", "Angular DevTools (component tree inspector, DI tree)", r"component tree\s+inspector", "Component tree inspector, DI tree and flame chart."),
    ("devtools-flamechart", "tool", "Custom performance flame chart in DevTools", r"flame chart", "Part of the DevTools description."),
    ("ng-update", "tool", "ng update (automatic code transformations)", r"ng update", "Updating to major versions."),
    ("language-service", "tool", "Language service for IDEs", r"language service", "Code completion, navigation, refactoring, diagnostics."),
    ("vite-esbuild", "tool", "Build pipeline with Vite and esbuild", r"vite", "Cited in the CLI section."),
    # --- trust, stability
    ("monorepo", "stability", "Commit-by-commit verification against Google's monorepo", r"colossal\s+monorepo", "Google internal tests."),
    ("backwards-compat", "stability", "Stability, backward compatibility and migration tools", r"include migration\s+tools", "Stability commitment (sentence '...compatible and includes migration tools'; in NG20 the sentence is split between pp. 3 and 4)."),
    ("release-lts", "stability", "Predictable release schedule and LTS windows", r"long term\s+support", "Support policy."),
    ("migration-schematics", "stability", "Automatic migration schematics", r"migration\s+schematics", "Official update tooling."),
    # --- scale
    ("i18n", "scale", "Internationalization (translation and formatting, ICU syntax)", r"icu syntax", "i18n support."),
    ("security", "scale", "Secure by default (HTML sanitization, trusted types)", r"trusted type", "Cited together with XSS and CSRF."),
    ("xss-csrf", "scale", "XSS and CSRF cited as common vulnerabilities", r"cross-?\s*site\s+scripting", "Part of the security text."),
    ("google-apps", "scale", "Used in large Google apps (Google Fonts, Google Cloud)", r"google fonts", "Examples of scale."),
    ("build-speed-claim", "scale", "Report of builds of hundreds of thousands of lines in under a minute", r"hundreds of thousands of lines", "Claim by developers."),
    # --- open source, community
    ("github-open", "community", "Open development on GitHub", r"made in the open on github", "Transparency."),
    ("roadmap-rfcs", "community", "Public roadmap and RFCs", r"request for\s+comments", "Transparency."),
    ("devlibrary", "community", "Google DevLibrary", r"devlibrary", "Resource library."),
    ("gdes", "community", "Google Developer Experts (GDEs)", r"developer experts", "Community partnerships."),
    ("aurora", "community", "Partnership with Chrome's Aurora", r"aurora", "Performance optimizations/Core Web Vitals."),
    ("ngoptimizedimage", "community", "NgOptimizedImage cited as a built-in optimization", r"ngoptimizedimage", "Cited in the Aurora partnership."),
    ("core-web-vitals", "community", "Core Web Vitals", r"core web\s+vitals", "Cited improvements."),
    ("firebase", "community", "Integrations: Firebase", r"firebase", "List of Google partners."),
    ("tensorflow", "community", "Integrations: TensorFlow (spelling varies across versions)", r"tensorflow", "List of Google partners."),
    ("flutter", "community", "Integrations: Flutter", r"flutter", "List of Google partners."),
    ("material-design", "community", "Integrations: Material Design", r"material design", "List of Google partners."),
    ("google-cloud", "community", "Integrations: Google Cloud", r"google cloud", "Also cited as a product at scale."),
    # --- footer / meta
    ("bluesky", "meta", "Social network link: Bluesky", r"bluesky", "Footer."),
    ("discord", "meta", "Link: Discord", r"discord", "Footer."),
    ("community-translations", "meta", "Footer 'Community translations'", r"community translations", "Footer of the newer captures."),
    ("languages-footer", "meta", "Footer 'Languages'", r"\blanguages\b", "Footer of the older captures."),
    ("build-stamp", "meta", "Stamp 'Built by Angular at vX.Y.Z+sha'", r"built by angular at v", "Only in captures 21-22."),
    ("press-kit", "meta", "Press Kit / Code of Conduct", r"press kit", "Footer."),
]

# Terms that NO overview cites (verified by the script; "NOT COVERED" in the lookup).
# (id, label, regex)
GAP_TERMS = [
    ("standalone", "standalone components", r"standalone"),
    ("zoneless", "zoneless / zone.js", r"zoneless|zone\.js|\bzone\b"),
    ("control-flow", "control flow (@if/@for/@switch)", r"@if\b|@for\b|@switch\b|control flow|\*ngif|\*ngfor"),
    ("ngmodule", "NgModule", r"ngmodule"),
    ("computed-effect", "computed / effect / linkedSignal", r"computed|\beffect\b|linkedsignal"),
    ("resource-api", "resource / httpResource", r"httpresource|\bresource\(|\bresource api"),
    ("signal-forms", "Signal Forms", r"signal forms"),
    ("incremental-hydration", "incremental hydration / event replay", r"incremental hydration|event replay"),
    ("angular-material", "Angular Material / CDK (as a library)", r"angular material|\bcdk\b"),
    ("animations", "animations", r"animation"),
    ("testing", "testing (Jasmine/Karma/Jest/Vitest)", r"jasmine|karma|\bjest\b|vitest|unit test|testing"),
    ("typescript", "TypeScript", r"typescript"),
    ("rxjs", "RxJS / Observables", r"rxjs|observable"),
    ("inject-fn", "inject() function", r"\binject\("),
    ("ng-commands", "ng new/serve/build/generate commands", r"ng (new|serve|build|generate|test)\b"),
    ("ai-mcp", "AI / MCP / assistants", r"\bmcp\b|\bai\b|artificial intelligence|llm"),
    ("webpack", "webpack", r"webpack"),
    ("pwa-sw", "PWA / service workers", r"service worker|\bpwa\b"),
    ("angular-elements", "Angular Elements / web components", r"angular elements|web components"),
    ("aot-ivy", "AOT / Ivy", r"\baot\b|ahead-of-time|\bivy\b"),
    ("version-numbers", "framework version numbers/release dates", r"release date|released on"),
]

BOILER = [
    r"this site uses cookies.*", r"deliver its services.*", r"google to deliver.*", r"and to analyze traffic.*",
    r"learn more", r"ok, got it", r"on this page", r"edit", r"menu docs", r"v\d\d", r"docs", r"tutorials",
    r"playground", r"reference", r"more_horiz", r"routine", r"check_circle", r"open_in_new",
    r"features that power your\s*(development)?", r"develop applications faster( than ever)?",
    r"ship with confidence", r"works at any scale", r"open-source first", r"a thriving community", r"than ever",
    r"development", r"google to", r"deliver its services", r"and to analyze traffic\.", r"this site uses cookies from",
]
BOILER_RE = [re.compile(b + r"$", re.I) for b in BOILER]


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"-\s*\n\s*", "-", s)
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def page_hits(pages, cre):
    """Pages where the pattern appears; phrases split across two pages count on the page where they start."""
    ns = {n: norm(raw) for n, raw in pages.items()}
    hits = []
    for n in sorted(ns):
        if cre.search(ns[n]):
            hits.append(n)
        elif n + 1 in ns:
            tail = ns[n][-120:]
            joint = tail + " " + ns[n + 1][:120]
            m = cre.search(joint)
            if m and m.start() < len(tail) and m.end() > len(tail) + 1:
                hits.append(n)
    return hits


def useful_chars(raw):
    seen = set()
    tot = 0
    for ln in raw.splitlines():
        t = ln.strip()
        if not t or t in seen:
            continue
        seen.add(t)
        if any(b.match(t) for b in BOILER_RE):
            continue
        tot += len(t)
    return tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "ng_index.json"))
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()

    data = {"_nota": "Index generated by ng_build_index.py. Pages = PDF pages. No source text copied.",
            "versions": VERSIONS, "meta": {}, "concepts": [], "gaps": []}
    pages_by_v = {}
    for v in VERSIONS:
        pg = load_pages(os.path.join(a.src, FILE.format(v=v)))
        if len(pg) != NPAGES[v]:
            print(f"WARNING: v{v} has {len(pg)} pages (expected {NPAGES[v]})")
        pages_by_v[v] = pg
        full = norm(" ".join(pg.values()))
        info = {"pages": len(pg), "useful_chars": {}, "page_class": {}}
        for n, raw in pg.items():
            u = useful_chars(raw)
            info["useful_chars"][str(n)] = u
            info["page_class"][str(n)] = "navigation-or-footer-only" if u < 200 else ("partial" if u < 400 else "content")
        m = re.search(r"©\s*(\d{4})-(\d{4})", full)
        info["footer_years"] = f"{m.group(1)}-{m.group(2)}" if m else None
        m = re.search(r"built by angular at (v\d+\.\d+\.\d+)", full)
        info["build_stamp"] = m.group(1) if m else None
        m = re.search(r"\bv(\d\d)\b", full)
        info["nav_version_label"] = "v" + m.group(1) if m else None
        info["cookie_banner_pages"] = [n for n, raw in pg.items() if "cookies" in raw.lower()]
        data["meta"][str(v)] = info

    for cid, grp, label, rx, note in CONCEPTS:
        rec = {"id": cid, "group": grp, "label": label, "note": note, "pattern": rx, "pages": {}}
        cre = re.compile(rx)
        for v in VERSIONS:
            hits = page_hits(pages_by_v[v], cre)
            if hits:
                rec["pages"][str(v)] = hits
        data["concepts"].append(rec)

    for gid, label, rx in GAP_TERMS:
        cre = re.compile(rx)
        found = {}
        for v in VERSIONS:
            hits = page_hits(pages_by_v[v], cre)
            if hits:
                found[str(v)] = hits
        data["gaps"].append({"id": gid, "label": label, "pattern": rx, "found": found})

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {a.out}: {len(data['concepts'])} concepts, {len(data['gaps'])} gap terms")
    if a.show:
        for c in data["concepts"]:
            row = " ".join(f"{v}:{','.join(map(str, c['pages'].get(str(v), []))) or '-'}" for v in VERSIONS)
            print(f"{c['id']:30s} {row}")
        for g in data["gaps"]:
            print("GAP", g["id"], g["found"])


if __name__ == "__main__":
    main()
