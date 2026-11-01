# -*- coding: utf-8 -*-
"""
dora_effects.py - queries the EFFECT ESTIMATES published in DORA24 (with page, source type and
whether the 89% uncertainty interval crosses zero, when legible in the figure). It computes
nothing beyond what the report publishes.

Usage:
  python -I scripts/dora_effects.py list
  python -I scripts/dora_effects.py show --capability ai [--outcome productivity]
  python -I scripts/dora_effects.py estimate --capability ai --outcome stability --increase 25
  python -I scripts/dora_effects.py estimate --capability ai --outcome stability --increase 50 --linear

Capabilities: ai | leadership | platform | ai-in-product (Portuguese aliases accepted: ia, lideranca,
plataforma, ia-no-produto). Outcomes can be typed in English or Portuguese (e.g. stability/estabilidade).

Honesty rules:
 - 'per +25%' effects only hold for +25% (the report does not publish the curve); any other value = NOT COVERED,
   unless --linear is used, which prints a LINEAR EXTRAPOLATION labeled [extrapolation] (not from the report).
 - all are estimated associations from an observational survey (not an experiment; p.110); 89% intervals (p.108).
 - 'crosses_zero' comes from visual reading of the figures (p.32, 37, 39, 42, 72), flagged when there is uncertainty.
Exit: 0 ok; 1 invalid input; 2 not covered.
"""
import argparse
import json
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# kind: per25 = estimated % change for +25% of the predictor; contrast = % difference using vs not using (text)
# crosses_zero: False / True / None (not legible or not applicable) ; "edge" = touches zero (visual reading)
E = [
    # --- AI, individual (Fig 7, p.32)
    ("ai", "flow", 2.6, "per25", False, 32, "figure 7"),
    ("ai", "job satisfaction", 2.2, "per25", False, 32, "figure 7"),
    ("ai", "productivity", 2.1, "per25", False, 32, "figure 7 + text"),
    ("ai", "time spent on toilsome work", 0.4, "per25", True, 32, "figure 7"),
    ("ai", "burnout", -0.6, "per25", True, 32, "figure 7"),
    ("ai", "time spent on valuable work", -2.6, "per25", False, 32, "figure 7"),
    # --- AI, development workflow (Fig 9, p.37)
    ("ai", "documentation quality", 7.5, "per25", False, 37, "figure 9 + text"),
    ("ai", "code quality", 3.4, "per25", False, 37, "figure 9 + text"),
    ("ai", "code review speed", 3.1, "per25", False, 37, "figure 9 + text"),
    ("ai", "approval speed", 1.3, "per25", "edge", 37, "figure 9 + text"),
    ("ai", "cross-functional coordination (xfn)", 0.1, "per25", True, 37, "figure 9"),
    ("ai", "technical debt", -0.8, "per25", True, 37, "figure 9"),
    ("ai", "code complexity", -1.8, "per25", False, 37, "figure 9 + text"),
    # --- AI, delivery (Fig 10, p.39-40)
    ("ai", "delivery throughput", -1.5, "per25", False, 40, "figure 10 + text"),
    ("ai", "delivery stability", -7.2, "per25", False, 40, "figure 10 + text"),
    # --- AI, performance (Fig 11, p.42-43)
    ("ai", "organizational performance", 2.3, "per25", False, 43, "figure 11 + text"),
    ("ai", "team performance", 1.4, "per25", False, 43, "figure 11 + text"),
    ("ai", "product performance", 0.2, "per25", True, 42, "figure 11"),
    # --- Transformational leadership (Fig 18, p.72)
    ("leadership", "job satisfaction", 9.1, "per25", False, 72, "figure 18"),
    ("leadership", "burnout", -9.9, "per25", False, 72, "figure 18"),
    ("leadership", "productivity", 8.7, "per25", False, 72, "figure 18 (text p.71 says ~9%)"),
    ("leadership", "team performance", 8.7, "per25", False, 72, "figure 18"),
    ("leadership", "product performance", 4.5, "per25", False, 72, "figure 18"),
    ("leadership", "organizational performance", 10.3, "per25", False, 72, "figure 18"),
    # --- Internal platform (text p.49-54): contrast using vs not using
    ("platform", "individual productivity", 8.0, "contrast", None, 49, "text"),
    ("platform", "team performance", 10.0, "contrast", None, 49, "text"),
    ("platform", "delivery and operations performance (organization)", 6.0, "contrast", None, 49, "text"),
    ("platform", "delivery throughput", -8.0, "contrast", None, 53, "text"),
    ("platform", "change stability", -14.0, "contrast", None, 54, "text"),
    ("platform", "throughput when use is exclusive across the whole cycle", -6.0, "contrast", None, 53, "text (hypothesis, not a definitive connection)"),
    ("platform", "productivity with developer independence (individual and team)", 5.0, "contrast", None, 51, "text"),
    ("platform", "team productivity with a dedicated platform team", 6.0, "contrast", None, 52, "text (individual: negligible)"),
    # --- Priorities / AI in product (text)
    ("ai-in-product", "delivery stability (teams that added AI experiences)", -10.0, "contrast", None, 67, "text + figure 17"),
]

SYN = {
    "ai": ["ai", "ia", "inteligencia artificial", "artificial intelligence", "adocao de ia", "ai adoption"],
    "leadership": ["leadership", "lideranca", "transformational leadership", "lideranca transformacional"],
    "platform": ["platform", "plataforma", "idp", "platform engineering"],
    "ai-in-product": ["ai-in-product", "ia-no-produto", "ia no produto", "ai-powered experiences", "ai in product"],
}

# Portuguese outcome words -> English fragments (user input stays accepted in Portuguese)
PT_OUTCOME = {
    "produtividade": "productivity", "estabilidade": "stability", "vazao": "throughput", "satisfacao": "satisfaction",
    "fluxo": "flow", "qualidade": "quality", "documentacao": "documentation", "organizacional": "organizational",
    "organizacao": "organization", "time": "team", "produto": "product", "desempenho": "performance",
    "divida tecnica": "technical debt", "complexidade": "complexity", "revisao": "review", "aprovacao": "approval",
    "entrega": "delivery", "independencia": "independence", "coordenacao": "coordination",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def cap_key(q):
    q = norm(q)
    for k, vs in SYN.items():
        if q == k or q in [norm(v) for v in vs]:
            return k
    return None


def rows(cap=None, outcome=None):
    pool = [r for r in E if not cap or r[0] == cap]
    if not outcome:
        return pool
    q = norm(outcome)
    cands = [q]
    if q in PT_OUTCOME:  # Portuguese input -> English fragment
        cands.append(PT_OUTCOME[q])
    for strict in (True, False):  # whole word first, then substring
        out = []
        for r in pool:
            name = norm(r[1])
            for c in cands:
                pat = rf"(?<![a-z]){re.escape(c)}(?![a-z])" if strict else re.escape(c)
                if re.search(pat, name):
                    out.append(r)
                    break
        if out:
            return out
    return []


def fmt(r):
    cap, name, val, kind, cz, page, src = r
    if kind == "per25":
        base = f"{val:+.1f}% per +25% of the predictor"
    else:
        base = f"{val:+.0f}% (contrast/use, text)"
    z = {False: "89% interval does NOT cross zero (visual reading)", True: "89% interval CROSSES zero (visual reading): uncertain effect",
         "edge": "interval touches zero (visual reading)", None: "interval not legible/not published in the text"}[cz]
    return f"- [{cap}] {name}: {base} | DORA24 p.{page} ({src}) | {z}"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list")
    s = sub.add_parser("show")
    s.add_argument("--capability")
    s.add_argument("--outcome")
    e = sub.add_parser("estimate")
    e.add_argument("--capability", required=True)
    e.add_argument("--outcome", required=True)
    e.add_argument("--increase", type=float, default=25.0)
    e.add_argument("--linear", action="store_true")
    j = [sub.choices["show"], sub.choices["estimate"]]
    for p in j:
        p.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd in (None, "list"):
        for k in SYN:
            print(f"{k}: {sum(1 for r in E if r[0] == k)} estimates")
        print("All are estimated associations from an observational survey (DORA24 p.110), 89% intervals (p.108).")
        return 0
    cap = None
    if a.capability:
        cap = cap_key(a.capability)
        if cap is None:
            print(f"NOT COVERED: capability {a.capability!r} has no effect estimate in the collection. "
                  f"Available: {', '.join(SYN)}", file=sys.stderr)
            return 2
    rs = rows(cap, a.outcome)
    if not rs:
        print("NOT COVERED: no published estimate for this capability/outcome combination.")
        return 2
    if a.cmd == "show":
        if a.json:
            print(json.dumps([dict(zip(["cap", "outcome", "value", "kind", "crosses_zero", "page", "source"], r)) for r in rs],
                             ensure_ascii=False, indent=2))
        else:
            for r in rs:
                print(fmt(r))
            print("WARNING: association, not causal proof; the unit is the relative % change in the outcome score/indicator, as the report presents it.")
        return 0
    # estimate
    if len(rs) > 1:
        print("Ambiguous combination; refine --outcome. Candidates:")
        for r in rs:
            print(fmt(r))
        return 1
    r = rs[0]
    if r[3] == "per25":
        if abs(a.increase - 25.0) < 1e-9:
            print(fmt(r))
        elif a.linear:
            print(fmt(r))
            print(f"[extrapolation] linear for +{a.increase:g}%: {r[2] * a.increase / 25.0:+.2f}%  "
                  "(NOT in the report; the report only publishes +25% and does not say the effect is linear)")
        else:
            print(f"NOT COVERED: the report only publishes the effect for +25% ({r[2]:+.1f}%, p.{r[5]}). "
                  "For another value use --linear (labeled extrapolation) or say there is no data.")
            return 2
    else:
        print(fmt(r))
        print("Note: this effect is a contrast (e.g. with vs without a platform), not a rate per +25%.")
    print("WARNING: association from an observational survey; confirm with a local experiment (p.7, p.83).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
