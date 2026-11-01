# -*- coding: utf-8 -*-
"""
slr_guide.py - method-selection guide with the recommendations of ISLR and ESL (each rule with its PDF page).

Read-only, stdlib, no network, deterministic. The base is scripts/slr_guide.json (52 rules).
The script only FILTERS the rules by the facts given; the rules are [from source]; the filter is [inference].
No rule replaces validating by CV on your own dataset.

Usage:
  python -I scripts/slr_guide.py list [--area AREA]
  python -I scripts/slr_guide.py show G06
  python -I scripts/slr_guide.py recommend [--goal prediction|inference|exploration] [--response quant|binary|multiclass|none]
        [--n N] [--p P] [--linear yes|no] [--nonlinear moderate|strong] [--interpretable yes|no] [--few-relevant yes|no]
        [--correlated yes] [--gaussian yes|no] [--separated yes] [--imbalanced yes] [--need-probs yes] [--noisy-labels yes]
        [--messy yes] [--model rf|boosting|svm|tree] [--selection yes] [--data-rich yes] [--many-tests yes]
        [--time-series yes] [--heterosc yes] [--outliers yes] [--only-distances yes] [--interaction yes] [--small-n yes]
        [--json]
Areas: objective, principle, regression, high-dimension, non-linear, classification, trees, svm, assessment, diagnostics,
unsupervised (the former Portuguese names, e.g. arvores, avaliacao, are still accepted).
Page convention: PDF (printed ISLR = PDF - 15; printed ESL = PDF - 19).
"""
import argparse
import io
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))

# Portuguese area names (previous CLI input) -> current English names
AREA_ALIASES = {
    "objetivo": "objective", "principio": "principle", "regressao": "regression", "alta-dimensao": "high-dimension",
    "nao-linear": "non-linear", "classificacao": "classification", "arvores": "trees", "avaliacao": "assessment",
    "diagnostico": "diagnostics", "nao-supervisionado": "unsupervised",
}


def load():
    with io.open(os.path.join(HERE, "slr_guide.json"), encoding="utf-8") as f:
        return json.load(f)["rules"]


def derive(a):
    f = {}
    for k in ("goal", "response", "linear", "nonlinear", "interpretable", "few_relevant", "correlated", "gaussian",
              "separated", "imbalanced", "need_probs", "noisy_labels", "messy", "model", "selection", "data_rich",
              "many_tests", "time_series", "heterosc", "outliers", "only_distances", "interaction", "small_n", "p_large"):
        v = getattr(a, k, None)
        if v is not None:
            f[k] = v
    notes = []
    if a.n and a.p:
        if a.p > a.n:
            f["np"] = "p_gt_n"
        elif a.n >= 10 * a.p:
            f["np"] = "n_gg_p"
        else:
            f["np"] = "comparable"
        notes.append("n >> p was defined as n >= 10p ([inference]: the book gives no number; ISLR p.218 says only 'n much larger than p').")
        if "p_large" not in f and a.p >= 40:
            f["p_large"] = "yes"
            notes.append("large p = p >= 40 (ISLR p.222: best subset is infeasible above about 40).")
    if a.n and "small_n" not in f and a.n < 100:
        f["small_n"] = "yes"
        notes.append("small n = n < 100 ([inference]; the ESL uses N = 50 as an example of small N, p.262).")
    return f, notes


def matches(rule, facts):
    q = rule["when"]
    if not q:
        return "always"
    for k, v in q.items():
        if facts.get(k) != v:
            return None
    return "matched"


def show(r):
    print(f"[{r['id']}] ({r['area']}) {r['situation']}")
    print(f"    -> {r['recommendation']}")
    print(f"    Pages: {'; '.join(r['pages'])} | source: {r['source']}")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    sub = ap.add_subparsers(dest="cmd")
    l = sub.add_parser("list")
    l.add_argument("--area")
    s = sub.add_parser("show")
    s.add_argument("id")
    r = sub.add_parser("recommend")
    r.add_argument("--goal", choices=["prediction", "inference", "exploration"])
    r.add_argument("--response", choices=["quant", "binary", "multiclass", "none"])
    r.add_argument("--n", type=int)
    r.add_argument("--p", type=int)
    for k, ch in [("linear", ["yes", "no"]), ("nonlinear", ["moderate", "strong"]), ("interpretable", ["yes", "no"]),
                  ("few-relevant", ["yes", "no"]), ("correlated", ["yes"]), ("gaussian", ["yes", "no"]),
                  ("separated", ["yes"]), ("imbalanced", ["yes"]), ("need-probs", ["yes"]), ("noisy-labels", ["yes"]),
                  ("messy", ["yes"]), ("model", ["rf", "boosting", "svm", "tree"]), ("selection", ["yes"]),
                  ("data-rich", ["yes"]), ("many-tests", ["yes"]), ("time-series", ["yes"]), ("heterosc", ["yes"]),
                  ("outliers", ["yes"]), ("only-distances", ["yes"]), ("interaction", ["yes"]), ("small-n", ["yes"]),
                  ("p-large", ["yes"])]:
        r.add_argument("--" + k, choices=ch)
    r.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rules = load()
    if a.cmd == "list":
        area = AREA_ALIASES.get(a.area, a.area) if a.area else None
        for x in rules:
            if area and x["area"] != area:
                continue
            print(f"{x['id']} ({x['area']}): {x['situation']}")
        return 0
    if a.cmd == "show":
        x = next((y for y in rules if y["id"].lower() == a.id.lower()), None)
        if not x:
            print("rule not found; use list")
            return 2
        show(x)
        return 0
    if a.cmd == "recommend":
        facts, notes = derive(a)
        res = [(m, x) for x in rules for m in [matches(x, facts)] if m]
        if a.json:
            print(json.dumps({"facts": facts, "rules": [dict(type=m, **x) for m, x in res], "notes": notes}, ensure_ascii=False, indent=1))
            return 0
        print("Facts used:", json.dumps(facts, ensure_ascii=False))
        for n in notes:
            print("Note:", n)
        matched = [x for m, x in res if m == "matched"]
        always = [x for m, x in res if m == "always"]
        print(f"\n== Rules matching the situation ({len(matched)}) ==")
        for x in matched:
            show(x)
        if not matched:
            print("(no specific rule matched: provide more facts or see the general rules)")
        print(f"\n== General rules that always apply ({len(always)}) ==")
        for x in always:
            show(x)
        print("\nWarning: [from source] rules with PDF pages; the filter is [inference]. Validate the method by CV (ISLR p.198-199; ESL p.261-262); no rule is a theorem.")
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
