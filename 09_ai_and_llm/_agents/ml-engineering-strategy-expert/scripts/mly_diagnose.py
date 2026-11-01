# -*- coding: utf-8 -*-
"""
mly_diagnose.py - bias/variance/data-mismatch diagnosis decider and numeric utilities from the MLY
(Machine Learning Yearning, Andrew Ng, 2018 DRAFT). Stdlib, no network, deterministic.
Run with: python -I scripts/mly_diagnose.py SUBCOMMAND ...
Pages = PDF page (= printed number). Errors in PERCENT (e.g., 15 means 15%).

Subcommands
  bv          --train T --dev D [--optimal O | --human H] [--traindev TD] [--desired X] [--tol Y] [--json]
              Decomposition (MLY p.42, 46-47, 77-80):
                bias (informal)          = training error                            (p.42)
                avoidable bias           = training error - optimal error rate       (p.47)
                variance (no train-dev)  = dev error - training error                 (p.42, 47)
                with training-dev:  variance = train-dev error - training error;
                                    data mismatch = dev error - train-dev error       (p.77-80)
              The book does NOT fix a numeric threshold for "high"; the script ranks the components and only
              flags "high" if you pass --tol (YOUR threshold, [inference]).
  optverify   --pairs "s*:sout;s*:sout;..."   or   --file file.json   (list of [s_star, s_out])
              Optimization Verification Test (p.85-87, 89): Score(y*) > Score(y_out) => problem in the
              search/optimization algorithm; otherwise => problem in the scoring function/objective.
  f1          --precision P --recall R      F1 = 2/((1/P)+(1/R)) (harmonic mean; p.21 note 4) and the simple average (p.20)
  weights     --n-target N --n-extra M      beta for equal weights = N/M (p.76: 5,000 vs 200,000 => 1/40)
  eyeball     --error-rate E --errors K     Eyeball dev size = K / E (p.38: 100 errors at 5% => 2,000)
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ACTIONS = {
    "avoidable_bias": [
        ("increase model size (layers/neurons); if variance rises, use regularization", "p.49, 51"),
        ("modify features based on error analysis", "p.51"),
        ("reduce or remove regularization (L2, L1, dropout): reduces avoidable bias, increases variance", "p.51"),
        ("modify the model architecture", "p.51"),
        ("error analysis on the training set", "p.52"),
        ("does NOT help: more training data (helps variance, generally not bias)", "p.51"),
    ],
    "variance": [
        ("add training data (the simplest and most reliable, if data and compute are available)", "p.49, 53"),
        ("add regularization (L2, L1, dropout): reduces variance and increases bias", "p.53"),
        ("early stopping (based on dev error): reduces variance and increases bias", "p.53"),
        ("feature selection (mainly useful with a small training set)", "p.53"),
        ("shrink the model: use with caution; regularizing is usually better", "p.53"),
        ("modify features/architecture (may affect both bias and variance)", "p.53-54"),
    ],
    "data_mismatch": [
        ("understand how the properties differ between training and dev (error analysis on dev)", "p.81"),
        ("collect more training data similar to dev", "p.81"),
        ("artificial data synthesis, carefully, to avoid overfitting to the synthesized subset", "p.82-83"),
    ],
}


def f(x):
    return f"{x:.4g}"


def cmd_bv(a):
    train, dev = a.train, a.dev
    notes = []
    if a.optimal is not None and a.human is not None:
        print("Pass --optimal OR --human, not both.")
        return 2
    opt = a.optimal if a.optimal is not None else a.human
    opt_kind = None
    if a.optimal is not None:
        opt_kind = "optimal error rate as given (p.46-47)"
    elif a.human is not None:
        opt_kind = ("human error as a proxy for the optimal rate (p.66, 68: the optimum is at most the human error; "
                    "avoidable bias is at least training - human)")
    comp = {}
    if opt is None:
        notes.append("[inference] without an optimal/human error, I used optimal = 0, which overestimates avoidable bias if the "
                     "problem has irreducible noise (p.46: e.g., 14% of unintelligible audio).")
        opt = 0.0
        opt_kind = "optimal assumed 0 [inference]"
    comp["optimal_error_unavoidable_bias"] = opt
    comp["avoidable_bias"] = train - opt
    comp["total_bias_(optimal+avoidable)"] = train
    if a.traindev is not None:
        comp["variance"] = a.traindev - train
        comp["data_mismatch"] = dev - a.traindev
        defs = "variance = train-dev - training; mismatch = dev - train-dev (MLY p.77-80)"
    else:
        comp["variance"] = dev - train
        defs = "variance = dev - training (MLY p.42, 47)"
    if comp["avoidable_bias"] < 0:
        notes.append("[from source] negative avoidable bias: the algorithm beats the optimal rate on the training set, a sign of "
                     "overfitting/memorization; focus on reducing variance, not bias (p.47, note 8).")
    if comp["variance"] < 0:
        notes.append("[inference] negative variance: the dev (or train-dev) error is below the training error; "
                     "check the numbers, the sets and the error computation.")
    if "data_mismatch" in comp and comp["data_mismatch"] < 0:
        notes.append("[inference] negative mismatch: dev better than train-dev; check the relative difficulty "
                     "of the distributions.")
    ranked = [(k, comp[k]) for k in ("avoidable_bias", "variance", "data_mismatch") if k in comp]
    ranked.sort(key=lambda kv: -kv[1])
    dominant = ranked[0][0] if ranked[0][1] > 0 else None
    res = {"input": {"train": train, "dev": dev, "traindev": a.traindev, "reference": opt_kind},
           "definitions": defs, "components": comp, "order_by_magnitude": [k for k, _ in ranked],
           "dominant": dominant, "notes": notes}
    if a.desired is not None:
        res["dev_gap_vs_desired"] = dev - a.desired
        res["train_gap_vs_desired"] = train - a.desired
    flags = []
    if a.tol is not None:
        for k, v in ranked:
            if v > a.tol:
                flags.append(k)
        res["above_user_threshold"] = {"threshold": a.tol, "components": flags}
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print(f"Input: train={f(train)}%  dev={f(dev)}%" + (f"  train-dev={f(a.traindev)}%" if a.traindev is not None else ""))
    print(f"Reference: {opt_kind}")
    print(f"Definitions: {defs}")
    print(f"  optimal error (unavoidable bias): {f(opt)}%")
    print(f"  avoidable bias                  : {f(comp['avoidable_bias'])}%  [from source p.47]" + ("  (at least; human proxy)" if a.human is not None else ""))
    print(f"  total bias (optimal+avoidable)  : {f(train)}%  [from source p.47]")
    print(f"  variance                        : {f(comp['variance'])}%  [from source p.42, 47" + (", 77-80]" if a.traindev is not None else "]"))
    if "data_mismatch" in comp:
        print(f"  data mismatch                   : {f(comp['data_mismatch'])}%  [from source p.77-80]")
    if a.desired is not None:
        print(f"  dev gap vs desired              : {f(dev - a.desired)} points (learning curve p.56-57, 61)")
    print("Order by magnitude:", " > ".join(f"{k} ({f(v)})" for k, v in ranked))
    if dominant:
        print(f"Dominant component: {dominant}  [inference: the book compares magnitudes, it does not fix a threshold]")
    else:
        print("No positive component: nothing to attack with this decomposition [inference].")
    if a.tol is not None:
        print(f"Above the user threshold ({f(a.tol)}): {', '.join(flags) if flags else 'none'}  [inference: threshold chosen by you]")
    else:
        print("The book defines no numeric threshold for 'high' bias/variance; compare each component with the gain that matters to the product (p.47: with 1% avoidable bias and 1% variance the algorithm is 'doing quite well'; p.45: 0.5%/1% is low bias and low variance).")
    for n in notes:
        print("NOTE:", n)
    focus = [k for k in (flags or ([dominant] if dominant else [])) if k in ("avoidable_bias", "variance", "data_mismatch")]
    for k in focus:
        print(f"Actions from the book for {k}:")
        for txt, pg in ACTIONS[k]:
            print(f"  - {txt}  [from source {pg}]")
    print("Warning: 2018 draft [DATED]; the recipes assume well-defined train/dev/test sets (p.15) and a single-number metric (p.20).")
    return 0


def cmd_opt(a):
    pairs = []
    if a.file:
        data = json.load(open(a.file, "r", encoding="utf-8"))
        pairs = [(float(x[0]), float(x[1])) for x in data]
    elif a.pairs:
        for tok in a.pairs.split(";"):
            tok = tok.strip()
            if tok:
                s1, s2 = tok.split(":")
                pairs.append((float(s1), float(s2)))
    if not pairs:
        print("Provide --pairs or --file.")
        return 2
    search = sum(1 for s, o in pairs if s > o)
    obj = len(pairs) - search
    ps, po = 100.0 * search / len(pairs), 100.0 * obj / len(pairs)
    res = {"n_errors": len(pairs), "search_optimization_problem": search, "scoring_function_problem": obj,
           "pct_search": ps, "pct_scoring": po}
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    print(f"{len(pairs)} dev errors examined (MLY p.86).")
    print(f"  Score(y*) > Score(y_out): {search} ({ps:.1f}%) -> search/optimization algorithm failure  [from source p.86, 87]")
    print(f"  Score(y*) <= Score(y_out): {obj} ({po:.1f}%) -> scoring function/objective failure       [from source p.86, 87]")
    bigger = "scoring function" if obj >= search else "search algorithm"
    print(f"Where to focus: {bigger}. Improving the other part removes, at most, the corresponding fraction of errors (ceiling; p.86: 95%/5%).")
    return 0


def cmd_f1(a):
    p, r = a.precision, a.recall
    if p <= 0 or r <= 0:
        print("Precision and recall must be > 0.")
        return 2
    f1 = 2.0 / ((1.0 / p) + (1.0 / r))
    print(f"F1 = 2/((1/P)+(1/R)) = {f1:.1f}  [from source p.21 note 4]; simple average = {(p + r) / 2:.1f}  [from source p.20]")
    return 0


def cmd_w(a):
    if a.n_extra <= 0 or a.n_target <= 0:
        print("Sizes must be > 0.")
        return 2
    beta = a.n_target / a.n_extra
    print(f"beta (equal weights between the two sets) = {a.n_target}/{a.n_extra} = {beta:.6g} = 1/{a.n_extra / a.n_target:.6g}  [from source p.76: 5,000 and 200,000 => 1/40]")
    print("The book suggests tuning beta on the dev set and only using reweighting when the extra data is very different or much larger (p.76). Example objective: squared error (the book warns it is not a good choice for classification).")
    return 0


def cmd_eye(a):
    if not 0 < a.error_rate <= 100:
        print("--error-rate must be in (0,100].")
        return 2
    n = a.errors / (a.error_rate / 100.0)
    print(f"Eyeball dev ~ {n:.0f} examples for ~{a.errors:g} errors at {a.error_rate:g}% error  [from source p.38: 5% and ~100 errors => ~2,000]")
    print("Book guide for the number of errors in the Eyeball set: 10 is too few, ~20 gives a rough feel, ~50 is good, ~100 is very good (p.38).")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("bv")
    b.add_argument("--train", type=float, required=True)
    b.add_argument("--dev", type=float, required=True)
    b.add_argument("--optimal", type=float)
    b.add_argument("--human", type=float)
    b.add_argument("--traindev", type=float)
    b.add_argument("--desired", type=float)
    b.add_argument("--tol", type=float)
    b.add_argument("--json", action="store_true")
    o = sp.add_parser("optverify")
    o.add_argument("--pairs")
    o.add_argument("--file")
    o.add_argument("--json", action="store_true")
    g = sp.add_parser("f1")
    g.add_argument("--precision", type=float, required=True)
    g.add_argument("--recall", type=float, required=True)
    w = sp.add_parser("weights")
    w.add_argument("--n-target", type=float, required=True)
    w.add_argument("--n-extra", type=float, required=True)
    e = sp.add_parser("eyeball")
    e.add_argument("--error-rate", type=float, required=True)
    e.add_argument("--errors", type=float, default=100)
    a = ap.parse_args()
    fn = {"bv": cmd_bv, "optverify": cmd_opt, "f1": cmd_f1, "weights": cmd_w, "eyeball": cmd_eye}[a.cmd]
    sys.exit(fn(a))


if __name__ == "__main__":
    main()
