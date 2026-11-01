# -*- coding: utf-8 -*-
"""
ctx_calc.py - small deterministic calculators tied to BAAS and CE2 (stdlib, no network, tokenizes nothing).

Subcommands (each output carries the formula, page, and origin label):
  budget        context budget estimator, parameterized BY YOU (tokens per component, window, tools, prices)
  memory-split  applies the short/long-term memory rules of CE2 p.12 (eqs. 5-6) to weights that YOU provide
  utility       utility function of the BAAS p.88-89 example (--demo reproduces 95.00 and 127.50)
  weights       feedback-based weight adjustment rule of BAAS p.109-110 (x1.1 if +1; x0.9 if -1)

Honesty of origin:
  - utility --demo and weights reproduce examples printed in BAAS (weights and factors are the book's, arbitrary according to the book itself).
  - memory-split implements the DEFINITION of CE2 p.12 (checked visually); the paper does NOT give weight values or thresholds.
  - budget is a PACKAGE CONSTRUCTION ([inference]/[extrapolation]): the alerts cite heuristics from CE2 p.16 (~50% occupancy, coding agents)
    and CE2 p.18 (30/100 tools, DeepSeek-v3), both [DATED] and context-specific; the paper provides neither a budgeting method nor prices.
Page convention: PDF (BAAS printed = PDF - 25; CE2 PDF = printed).
"""
import argparse
import io
import json
import math
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def die(msg, code=2):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


def pos_num(x, name, allow_zero=False):
    try:
        v = float(x)
    except (TypeError, ValueError):
        die(f"{name} must be a number (received {x!r})")
    if math.isnan(v) or math.isinf(v) or v < 0 or (v == 0 and not allow_zero):
        die(f"{name} must be {'>= 0' if allow_zero else '> 0'} and finite (received {x!r})")
    return v


def kv(items, what):
    out = []
    for it in items or []:
        if "=" not in it:
            die(f"{what} must have the form NAME=VALUE (received {it!r})")
        k, v = it.split("=", 1)
        k = k.strip()
        if not k:
            die(f"{what} with empty name")
        out.append((k, v.strip()))
    return out


# ----------------------------------------------------------------- budget
WARN_FILL_DEFAULT = 0.5     # CE2 p.16 (coding agents, Osmani 2025) [DATED]; the user can change it
TOOLS_WARN = 30             # CE2 p.18 (DeepSeek-v3, Dbreunig 2025) [DATED]
TOOLS_FAIL = 100            # same


def build_components(a, cfg):
    comps = {}
    for k, v in kv(a.component, "--component"):
        comps[k] = comps.get(k, 0) + pos_num(v, f"component {k}", allow_zero=True)
    chars = kv(a.chars, "--chars")
    if chars:
        if a.chars_per_token is None:
            die("--chars requires --chars-per-token (characters/token ratio of YOUR tokenizer; this package assumes no value)")
        r = pos_num(a.chars_per_token, "--chars-per-token")
        for k, v in chars:
            comps[k] = comps.get(k, 0) + math.ceil(pos_num(v, f"chars {k}", allow_zero=True) / r)
    for k, v in (cfg.get("components") or {}).items():
        comps[k] = comps.get(k, 0) + pos_num(v, f"component {k}", allow_zero=True)
    return comps


def cmd_budget(a):
    cfg = {}
    if a.config:
        try:
            with io.open(a.config, encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, ValueError) as e:
            die(f"could not read {a.config}: {e}")
    window = a.window if a.window is not None else cfg.get("window")
    if window is None:
        die("provide --window (window size in tokens of YOUR model) or 'window' in --config")
    window = pos_num(window, "window")
    comps = build_components(a, cfg)
    if not comps:
        die("provide at least one --component NAME=TOKENS (or --chars) or 'components' in --config")
    reserve = pos_num(a.reserve_output if a.reserve_output is not None else cfg.get("reserve_output", 0), "reserve_output", allow_zero=True)
    ntools = a.tools if a.tools is not None else cfg.get("tools")
    warn = pos_num(a.warn_fill if a.warn_fill is not None else cfg.get("warn_fill", WARN_FILL_DEFAULT), "warn_fill")
    prefix = list(a.prefix or []) + list(cfg.get("prefix") or [])
    for p in prefix:
        if p not in comps:
            die(f"--prefix {p!r} is not a provided component ({', '.join(comps)})")

    total = sum(comps.values())
    fill_in = total / window
    fill_all = (total + reserve) / window
    print("CONTEXT BUDGET [package construction; tokens provided by you, nothing is tokenized here]")
    print(f"window = {window:,.0f} tokens | reserved output = {reserve:,.0f}")
    width = max(max(len(k) for k in comps), len('input + reserved output'))
    for k, v in comps.items():
        print(f"  {k:<{width}}  {v:>10,.0f} tokens  {v / window:>7.1%} of the window" + ("  [stable prefix]" if k in prefix else ""))
    print(f"  {'TOTAL input':<{width}}  {total:>10,.0f} tokens  {fill_in:>7.1%} of the window")
    print(f"  {'input + reserved output':<{width}}  {total + reserve:>10,.0f} tokens  {fill_all:>7.1%} of the window")
    print("formulas: occupancy = sum(components) / window; occupancy with output = (sum + reserve) / window  [package arithmetic]")

    alerts = []
    if fill_all > 1:
        alerts.append(("ERROR", f"input + reserved output exceeds the window ({fill_all:.1%}); the excess is {total + reserve - window:,.0f} tokens [arithmetic]"))
    elif fill_in > warn:
        alerts.append(("ALERT", f"input occupancy {fill_in:.1%} above threshold {warn:.0%}. Origin of the default threshold: CE2 p.16 reports that the performance of CODING agents tends to drop above ~50% occupancy (cited source: Osmani 2025) [DATED]; it is a single-domain heuristic, adjust with --warn-fill"))
    if ntools is not None:
        nt = pos_num(ntools, "tools", allow_zero=True)
        if nt > TOOLS_FAIL:
            alerts.append(("ALERT", f"{nt:.0f} tools: CE2 p.18 reports, for DeepSeek-v3, near-certain failure above {TOOLS_FAIL} [DATED; model-specific, 2025]"))
        elif nt > TOOLS_WARN:
            alerts.append(("ALERT", f"{nt:.0f} tools: CE2 p.18 reports performance degradation above {TOOLS_WARN} for DeepSeek-v3 [DATED; model-specific, 2025]"))
    if comps:
        big = max(comps.items(), key=lambda kv_: kv_[1])
        if total and big[1] / total > 0.5 and len(comps) > 1:
            alerts.append(("NOTE", f"'{big[0]}' accounts for {big[1] / total:.0%} of the input; CE2 p.16-17 discusses selection, filtering, and reranking, and CE2 p.13 lightweight references for large content [inference]"))
    if not prefix:
        alerts.append(("NOTE", "no component marked as stable prefix (--prefix); CE2 p.18 recommends a stable prefix, append-only updates, and deterministic serialization to take advantage of the KV cache [DATED]"))
    for lvl, msg in alerts:
        print(f"[{lvl}] {msg}")
    if not alerts:
        print("[OK] no alerts with the given parameters (this does not guarantee quality; the thresholds are [DATED] heuristics)")

    pin = a.price_in if a.price_in is not None else cfg.get("price_in")
    if pin is not None:
        pin = pos_num(pin, "price_in", allow_zero=True)
        pcache = a.price_cached if a.price_cached is not None else cfg.get("price_cached")
        pcache = pin if pcache is None else pos_num(pcache, "price_cached", allow_zero=True)
        hit = pos_num(a.cache_hit if a.cache_hit is not None else cfg.get("cache_hit", 0), "cache_hit", allow_zero=True)
        if hit > 1:
            die("--cache-hit must be between 0 and 1")
        pout = a.price_out if a.price_out is not None else cfg.get("price_out", 0)
        pout = pos_num(pout, "price_out", allow_zero=True)
        out_tok = pos_num(a.out_tokens if a.out_tokens is not None else cfg.get("out_tokens", 0), "out_tokens", allow_zero=True)
        calls = pos_num(a.calls if a.calls is not None else cfg.get("calls", 1), "calls")
        ptok = sum(comps[p] for p in prefix)
        cached = ptok * hit
        fresh = total - cached
        cost = (fresh * pin + cached * pcache + out_tok * pout) / 1e6
        print("\nESTIMATED COST [arithmetic extrapolation: the texts provide neither prices nor a cost method; prices per 1 million tokens, provided by you]")
        print(f"  new input = {fresh:,.0f} tokens x {pin} ; cached input = {cached:,.0f} tokens x {pcache} ; output = {out_tok:,.0f} x {pout}")
        print(f"  cost per call = {cost:.6f} ; per {calls:,.0f} calls = {cost * calls:.4f}")
        print("  formula: (new x p_in + cached x p_cache + output x p_out) / 1e6; cached = (prefix tokens) x the hit rate provided")
    return 0


# ----------------------------------------------------------------- memory-split
def cmd_memory(a):
    ts = pos_num(a.theta_s, "theta-s", allow_zero=True)
    tl = pos_num(a.theta_l, "theta-l", allow_zero=True)
    items = []
    for k, v in kv(a.item, "--item"):
        parts = v.split(",")
        if len(parts) != 2:
            die(f"--item {k}=TEMPORAL,IMPORTANCE (received {v!r})")
        items.append((k, pos_num(parts[0], f"w_temporal de {k}", allow_zero=True), pos_num(parts[1], f"w_importance de {k}", allow_zero=True)))
    if not items:
        die("provide at least one --item NAME=w_temporal,w_importance")
    print("CE2 p.12 MEMORY RULES (definitions 5.1-5.3; formulas checked by rendering the page)")
    print("  Ms = f_short({c in C : w_temporal(c) > theta_s})")
    print("  Ml = f_long({c in C : w_importance(c) > theta_l  AND  w_temporal(c) <= theta_s})")
    print("  f_transfer: Ms -> Ml (consolidation; the paper cites repetition, emotional significance, and relevance to existing knowledge, with no formula)")
    print(f"  theta_s = {ts} ; theta_l = {tl}  (YOUR parameters: the paper gives neither values nor a method to estimate the weights)\n")
    for k, wt, wi in items:
        in_ms = wt > ts
        in_ml = (wi > tl) and (wt <= ts)
        dest = "short-term (Ms)" if in_ms else ("long-term (Ml)" if in_ml else "neither")
        extra = ""
        if in_ms and wi > tl:
            extra = "  [inference: in Ms with importance above theta_l; candidate for consolidation via f_transfer]"
        print(f"  {k:<20} w_temporal={wt:<8} w_importance={wi:<8} -> {dest}{extra}")
    print("\nNote: f_short, f_long, and f_transfer (filtering, abstraction, compression) are NOT implemented here; only the threshold selection.")
    return 0


# ----------------------------------------------------------------- utility
def cmd_utility(a):
    base = pos_num(a.base, "base")
    wp, wc, wv = (pos_num(x, n, allow_zero=True) for x, n in ((a.w_price, "w-price"), (a.w_comfort, "w-comfort"), (a.w_conv, "w-conv")))
    opts = []
    if a.demo:
        opts += [("Budget Airline", 300, 3, 2), ("Road Trip", 150, 4, 3)]
    for k, v in kv(a.option, "--option"):
        parts = v.split(",")
        if len(parts) != 3:
            die(f"--option {k}=PRICE,COMFORT,CONVENIENCE (received {v!r})")
        opts.append((k, *[pos_num(x, f"{n} of {k}", allow_zero=True) for x, n in zip(parts, ("price", "comfort", "convenience"))]))
    if not opts:
        die("provide --demo or --option NAME=PRICE,COMFORT,CONVENIENCE")
    print("UTILITY FUNCTION of BAAS p.88-89 (weighted-scoring example; the weights 0.05/10/15 and the base 1000 are arbitrary according to the book)")
    print(f"  U = ({base:g} - price) x {wp:g} + comfort x {wc:g} + convenience x {wv:g}")
    best = None
    for k, pr, co, cv in opts:
        u = (base - pr) * wp + co * wc + cv * wv
        print(f"  {k:<18} price={pr:g} comfort={co:g} convenience={cv:g} -> utility {u:.2f}")
        if best is None or u > best[1]:
            best = (k, u)
    print(f"  best option: {best[0]} ({best[1]:.2f})  [highest utility; the expected utility with probabilities (BAAS p.89) is not computed here]")
    if a.demo and base == 1000 and (wp, wc, wv) == (0.05, 10, 15):
        print("  check against the book (p.89): Budget Airline 95.00 and Road Trip 127.50")
    return 0


# ----------------------------------------------------------------- weights
def cmd_weights(a):
    ws = {}
    for k, v in kv(a.weight, "--weight"):
        ws[k] = pos_num(v, f"weight {k}", allow_zero=True)
    if not ws:
        die("provide at least one --weight NAME=VALUE")
    if a.key not in ws:
        die(f"--key {a.key!r} is not among the weights ({', '.join(ws)})")
    if a.feedback not in (-1, 1):
        die("--feedback must be 1 or -1")
    up = pos_num(a.up, "up")
    down = pos_num(a.down, "down")
    before = dict(ws)
    ws[a.key] *= up if a.feedback == 1 else down
    print("FEEDBACK-BASED WEIGHT ADJUSTMENT (BAAS p.109-110: feedback +1 multiplies the weight by 1.1; -1 by 0.9; the book hard-codes fixed factors and suggests that an LLM generate the factor, p.110)")
    for k in before:
        print(f"  {k:<14} {before[k]:.4f} -> {ws[k]:.4f}")
    if a.normalize:
        s = sum(ws.values())
        if s == 0:
            die("the sum of the weights is zero; cannot normalize")
        print("  normalized (package extrapolation; the book's code does not normalize): " + ", ".join(f"{k}={v / s:.4f}" for k, v in ws.items()))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("budget", help="context budget (tokens per component)")
    b.add_argument("--window", type=float)
    b.add_argument("--component", action="append", metavar="NAME=TOKENS")
    b.add_argument("--chars", action="append", metavar="NAME=CHARACTERS")
    b.add_argument("--chars-per-token", type=float)
    b.add_argument("--reserve-output", type=float)
    b.add_argument("--tools", type=float, help="number of tools in the context")
    b.add_argument("--warn-fill", type=float, help="occupancy threshold (default 0.5, from CE2 p.16 [DATED])")
    b.add_argument("--prefix", action="append", metavar="COMPONENT", help="component that forms the stable prefix (cache)")
    b.add_argument("--price-in", type=float, help="price per 1M input tokens (yours)")
    b.add_argument("--price-cached", type=float, help="price per 1M cached input tokens (yours)")
    b.add_argument("--price-out", type=float, help="price per 1M output tokens (yours)")
    b.add_argument("--cache-hit", type=float, help="fraction of the prefix that hits the cache (0 to 1)")
    b.add_argument("--out-tokens", type=float)
    b.add_argument("--calls", type=float)
    b.add_argument("--config", help="JSON with the same keys (window, components, reserve_output, tools, warn_fill, prefix, price_in, ...)")
    m = sp.add_parser("memory-split", help="CE2 p.12 rules")
    m.add_argument("--theta-s", type=float, required=True)
    m.add_argument("--theta-l", type=float, required=True)
    m.add_argument("--item", action="append", metavar="NAME=W_TEMPORAL,W_IMPORTANCE")
    u = sp.add_parser("utility", help="BAAS p.88-89")
    u.add_argument("--demo", action="store_true")
    u.add_argument("--option", action="append", metavar="NAME=PRICE,COMFORT,CONVENIENCE")
    u.add_argument("--base", type=float, default=1000)
    u.add_argument("--w-price", type=float, default=0.05)
    u.add_argument("--w-comfort", type=float, default=10)
    u.add_argument("--w-conv", type=float, default=15)
    w = sp.add_parser("weights", help="BAAS p.109-110")
    w.add_argument("--weight", action="append", metavar="NAME=VALUE")
    w.add_argument("--key", required=True)
    w.add_argument("--feedback", type=int, required=True)
    w.add_argument("--up", type=float, default=1.1)
    w.add_argument("--down", type=float, default=0.9)
    w.add_argument("--normalize", action="store_true")
    a = ap.parse_args()
    return {"budget": cmd_budget, "memory-split": cmd_memory, "utility": cmd_utility, "weights": cmd_weights}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
