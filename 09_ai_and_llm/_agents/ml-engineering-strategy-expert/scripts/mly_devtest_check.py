# -*- coding: utf-8 -*-
"""
mly_devtest_check.py - train/dev/test and metric coherence checker, applying the rules (qualitative and
the few numbers) given by the MLY (Machine Learning Yearning, Ng, 2018 DRAFT). Stdlib, no network.
Run with: python -I scripts/mly_devtest_check.py check CONFIG.json [--json]      or      ... example

The book gives explicit rules only in part: the script applies what is written (with page) and says when a
rule is an [inference] or when the book gives NO number. There is no "correct" size threshold: dev must be large
enough to detect differences between algorithms (p.19).

CONFIG keys (all optional; whatever is missing becomes "not verified"):
  n_train, n_dev, n_test                    sizes
  train_dist, dev_dist, test_dist, target_dist   label (string) OR dict {segment: fraction}; target = future data that matters
  tol_dist                                  YOUR tolerance (total variation distance) for dicts; default 0 (any difference is flagged)
  min_detectable_diff_pp                    smallest improvement you want to detect, in percentage points (e.g., 0.1)
  dev_error_pct                             current dev error (%)
  eyeball_fraction                          fraction of dev you inspect by hand (e.g., 0.1)
  metrics, satisficing                      lists of names; with >1 metric there must be 1 optimizing and N-1 satisficing (p.22)
  combined_single_number                    true if you combined the metrics into one (p.20-21)
  test_used_for_decisions                   true if you decide anything (including reverting a version) with the test set (p.26)
  labels_fixed_dev_only                     true if you fixed labels only in dev or only in test (p.35)
  train_has_target_distribution_data        true if part of the training data comes from the dev/test distribution (p.72)
  has_training_dev                          true if a training-dev set exists (p.77-78)
  project_stage                             "new" or "mature"; days_to_first_devtest = days to the 1st dev/test+metric (p.25)
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

EXAMPLE = {
    "n_train": 205000, "n_dev": 2500, "n_test": 2500,
    "train_dist": "internet+mobile", "dev_dist": "mobile", "test_dist": "mobile", "target_dist": "mobile",
    "min_detectable_diff_pp": 0.1, "dev_error_pct": 5, "eyeball_fraction": 0.1,
    "metrics": ["accuracy", "runtime_ms"], "satisficing": ["runtime_ms"],
    "test_used_for_decisions": False, "labels_fixed_dev_only": False,
    "train_has_target_distribution_data": True, "has_training_dev": False,
    "project_stage": "new", "days_to_first_devtest": 5,
}


def same(a, b, tol):
    if isinstance(a, dict) and isinstance(b, dict):
        ks = set(a) | set(b)
        tv = 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in ks)
        return tv <= tol, f"total variation distance = {tv:.3f}"
    return a == b, f"'{a}' vs '{b}'"


def check(c):
    F = []  # (severity, text, source)

    def add(sev, txt, src):
        F.append({"severity": sev, "finding": txt, "source": src})

    tol = float(c.get("tol_dist", 0.0))
    dd, td, tg, tr = c.get("dev_dist"), c.get("test_dist"), c.get("target_dist"), c.get("train_dist")
    if dd is not None and td is not None:
        ok, d = same(dd, td, tol)
        if ok:
            add("ok", f"dev and test seem to come from the same distribution ({d}).", "[from source p.17-18, 27]")
        else:
            add("high", f"dev and test come from different distributions ({d}). The book advises against it: it makes it hard to tell whether dev is overfit, "
                        "whether test is harder or merely different (p.17-18).", "[from source p.17-18]")
    else:
        add("n/v", "not verified: provide dev_dist and test_dist.", "-")
    if dd is not None and tg is not None:
        ok, d = same(dd, tg, tol)
        if ok:
            add("ok", f"dev reflects the target distribution ({d}).", "[from source p.15, 27]")
        else:
            add("high", f"dev does NOT reflect the target distribution ({d}); choose dev/test that reflect the future data that matters, "
                        "not the data you happen to have for training (p.15-16).", "[from source p.15-16]")
    if tr is not None and dd is not None:
        ok, d = same(tr, dd, tol)
        if not ok:
            add("info", f"training differs from dev ({d}); this is allowed and common with lots of data, but needs attention (p.71-72).", "[from source p.71-72]")
            if c.get("train_has_target_distribution_data") is False:
                add("medium", "no training data comes from the dev/test distribution; the book suggests putting part of the target-distribution examples "
                              "in training (e.g., 5,000 of 10,000 user images) and it helps diagnose mismatch (p.72, 81).", "[from source p.72, 81]")
            if c.get("has_training_dev") is False:
                add("medium", "training and dev differ and there is no training-dev set: variance cannot be separated from data mismatch (p.77-78).",
                    "[from source p.77-78]")
    nd, nt, ntr = c.get("n_dev"), c.get("n_test"), c.get("n_train")
    if nd is not None:
        if nd < 1000:
            add("medium", f"dev with {nd} examples: the book calls 100 small and cites 1,000 to 10,000 as common (p.19); "
                          "it may not detect small differences.", "[from source p.19]")
        elif nd <= 10000:
            add("ok", f"dev with {nd} examples is in the common range of 1,000 to 10,000 (p.19).", "[from source p.19]")
        else:
            add("info", f"dev with {nd} examples, above the common range; useful to detect very small improvements, but do not overdo it (p.19).",
                "[from source p.19]")
        md = c.get("min_detectable_diff_pp")
        if md is not None:
            if md <= 0.01 and nd <= 10000:
                add("medium", f"to detect ~{md} p.p. (mature applications chasing 0.01%) the book says dev may need to be "
                              "much larger than 10,000 (p.19).", "[from source p.19]")
            elif md <= 0.1 and nd < 10000:
                add("medium", f"to detect ~{md} p.p. the book gives 10,000 examples as a good chance of detection (p.19); 100 does not detect 0.1%.",
                    "[from source p.19]")
            elif md <= 0.1:
                add("ok", f"{nd} examples have a good chance of detecting ~{md} p.p. by the book's rule (10,000 -> 0.1%) (p.19).", "[from source p.19]")
            else:
                add("info", "the book gives no statistical power formula; it notes that significance tests are rarely used in practice (p.19 note 2).",
                    "[from source p.19 note 2]")
    if nt is not None:
        if nd is not None and ntr is not None and (nd + nt) / max(1.0, ntr + nd + nt) > 0.3:
            add("info", "dev+test take >30% of the data; the 30% heuristic is for 100-10,000 examples; with big data the fraction shrinks (p.19).",
                "[from source p.19]")
        add("info", "test should be large enough to give high confidence in the overall performance, without overdoing it (p.19, 27).", "[from source p.19, 27]")
    er, ef = c.get("dev_error_pct"), c.get("eyeball_fraction")
    if nd is not None and er is not None and ef is not None:
        k = nd * ef * er / 100.0
        txt = f"Expected Eyeball: ~{k:.0f} errors (n_dev*fraction*error)."
        if k < 10:
            txt += " Fewer than ~10 errors is considered far too few (p.38)."
            sev = "medium"
        elif k < 50:
            txt += " ~20 errors give a rough feel, ~50 a good one (p.38)."
            sev = "info"
        else:
            txt += " ~50 gives a good feel and ~100 a very good one (p.38)."
            sev = "ok"
        add(sev, txt, "[from source p.36-38]")
    ms, sa = c.get("metrics"), c.get("satisficing", [])
    if ms and len(ms) > 1:
        if c.get("combined_single_number"):
            add("ok", "multiple metrics combined into a single number (p.20-21).", "[from source p.20-21]")
        else:
            opt = [m for m in ms if m not in sa]
            if len(opt) == 1:
                add("ok", f"1 optimizing metric ('{opt[0]}') and {len(sa)} satisficing (p.22).", "[from source p.22]")
            else:
                add("high", f"{len(opt)} optimizing metrics: the book recommends a single number, or N-1 satisficing and 1 optimizing (p.20, 22).",
                    "[from source p.20, 22]")
    if c.get("test_used_for_decisions"):
        add("high", "the test set is being used for decisions (including reverting a version): this overfits it and removes the unbiased estimate (p.26).",
            "[from source p.26]")
    if c.get("labels_fixed_dev_only"):
        add("high", "labels fixed only in dev or only in test: apply the same process to both so they keep the same distribution (p.35).",
            "[from source p.35]")
    if c.get("project_stage") == "new" and c.get("days_to_first_devtest") is not None:
        d = c["days_to_first_devtest"]
        if d > 7:
            add("info", f"{d} days to the 1st dev/test+metric; the book asks for <1 week in a new project (mature ones may take months) (p.25).",
                "[from source p.25]")
        else:
            add("ok", f"{d} days to the 1st dev/test+metric (book goal: <1 week in a new project; p.25).", "[from source p.25]")
    return F


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    k = sp.add_parser("check")
    k.add_argument("config")
    k.add_argument("--json", action="store_true")
    sp.add_parser("example")
    a = ap.parse_args()
    if a.cmd == "example":
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=1))
        return
    c = json.load(open(a.config, "r", encoding="utf-8"))
    F = check(c)
    if a.json:
        print(json.dumps(F, ensure_ascii=False, indent=1))
        return
    order = {"high": 0, "medium": 1, "info": 2, "n/v": 3, "ok": 4}
    for f in sorted(F, key=lambda x: order.get(x["severity"], 9)):
        print(f"[{f['severity'].upper():<6}] {f['finding']}  {f['source']}")
    print("Warning: MLY is a 2018 draft [DATED]; the book gives no numeric thresholds beyond those cited (p.19, 38).")


if __name__ == "__main__":
    main()
