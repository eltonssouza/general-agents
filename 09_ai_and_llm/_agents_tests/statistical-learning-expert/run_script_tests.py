# -*- coding: utf-8 -*-
"""
run_script_tests.py - runs the deterministic test cases of the package scripts (no model, no network).

Usage:
  python -I tests/run_script_tests.py [--src PATH/scratch/ai]   # --src enables citation verification and the numbers audit
Exit 0 if all pass. The conceptual cases (which require the agent) are in tests/casos-de-teste.md.
The expected values come from the book pages (ISLR p.N / ESL p.N), indicated in each case.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I"]
FAIL, OK = [], []


def run(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding="utf-8", cwd=PKG)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, detail=""):
    (OK if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: " + detail[:500]))


def val(out, key):
    m = re.search(r"^\s*" + re.escape(key) + r" = (.+)$", out, re.M)
    return m.group(1).strip() if m else None


def fval(out, key):
    v = val(out, key)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def close(a, b, tol):
    return a is not None and abs(a - b) <= tol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    L = os.path.join("scripts", "slr_lookup.py")
    C = os.path.join("scripts", "slr_calc.py")
    G = os.path.join("scripts", "slr_guide.py")

    # ---------------- lookup
    c, o = run([L, "lasso"])
    check("L01 lasso -> ISLR p.234-243 and ESL p.87-94", "ISLR p.234-243" in o and "ESL p.87-94" in o, o)
    c, o = run([L, "benjamini"])
    check("L02 benjamini -> ESL p.702-711 and notice of absence in the ISLR", "ESL p.702-711" in o and "ISLR 0" in o, o)
    c, o = run([L, "deep learning"])
    check("L03 deep learning -> NOT COVERED", "NOT COVERED" in o, o)
    c, o = run([L, "xgboost"])
    check("L04 xgboost -> NOT COVERED", "NOT COVERED" in o, o)
    c, o = run([L, "--page", "ESL", "249"])
    check("L05 ESL p.249 read, ch.7", "page READ by this package" in o and "Ch.7" in o and "printed 230" in o, o)
    c, o = run([L, "--page", "ESL", "150"])
    check("L06 ESL p.150 NOT read", "NOT READ" in o, o)
    c, o = run([L, "--printed", "ISLR", "175"])
    check("L07 ISLR printed 175 -> PDF 190", "PDF p.190" in o, o)
    c, o = run([L, "--printed", "ESL", "219"])
    check("L08 ESL printed 219 -> PDF 238", "PDF p.238" in o, o)
    c, o = run([L, "--map", "boosting"])
    check("L09 boosting map: ISLR p.336-338 and ESL p.356-389", "ISLR p.336-338" in o and "ESL p.356-389" in o, o)
    c, o = run([L, "--chapters", "ISLR"])
    check("L10 ISLR chapters (ch.10 and 441 pages)", "Ch.10" in o and "441" in o, o)
    c, o = run([L, "--gaps"])
    check("L11 gaps lists unread ranges and R labs", "UNREAD RANGES" in o and "R labs" in o, o)
    c, o = run([L, "random", "forest"])
    check("L12 random forest -> ESL p.606-614", "ESL p.606-614" in o, o)
    c, o = run([L, "--page", "ISLR", "999"])
    check("L13 page out of range -> exit 2", c == 2, o)
    c, o = run([L, "bootstrap", "--json"])
    try:
        j = json.loads(o)
        check("L14 valid --json with results", len(j["results"]) >= 1, o)
    except Exception as e:
        check("L14 valid --json", False, str(e))
    c, o = run([L, "--coverage"])
    check("L15 coverage states that neither book was read in full", "Neither book was read in full" in o, o)
    c, o = run([L, "survival"])
    check("L16 survival -> partial coverage/NOT COVERED with count", "NOT COVERED" in o and "ESL" in o, o)
    c, o = run([L, "validacao", "cruzada"])
    check("L17 Portuguese query still works: validacao cruzada -> ISLR p.196-201", "ISLR p.196-201" in o, o)
    c, o = run([L, "aprendizado profundo"])
    check("L18 Portuguese gap key still works: aprendizado profundo -> NOT COVERED", "NOT COVERED" in o, o)

    # ---------------- calc (expected values come from the books)
    c, o = run([C, "ttest", "--coef", "0.0475", "--se", "0.0027", "--df", "198"])
    check("C01 2SE CI of Advertising ~ [0.042, 0.053] (ISLR p.82)", "(0.0421, 0.0529)" in o, o)
    c, o = run([C, "ftest", "--rss0", "32.81", "--rss1", "29.43", "--p0", "4", "--p1", "8", "--n", "67"])
    check("C02 F = 1.67 and p = 0.17 (ESL p.70)", close(fval(o, "F"), 1.67, 0.01) and close(fval(o, "p_value"), 0.17, 0.005), o)
    c, o = run([C, "confusion", "--tp", "81", "--fp", "23", "--fn", "252", "--tn", "9644"])
    check("C03 Default: sens 24.3%, spec 99.8%, error 2.75%, null 3.33% (ISLR p.159-160)",
          close(fval(o, "sensitivity_TPR"), 0.243, 0.001) and close(fval(o, "specificity"), 0.998, 0.001) and close(fval(o, "error"), 0.0275, 0.0001) and close(fval(o, "null_classifier_error"), 0.0333, 0.0001), o)
    c, o = run([C, "logistic", "prob", "--b0", "-10.6513", "--coefs", "0.0055", "--x", "2000"])
    check("C04 p(2000) = 0.586 (ISLR p.149)", close(fval(o, "probability"), 0.586, 0.001), o)
    c, o = run([C, "logistic", "prob", "--b0", "-10.6513", "--coefs", "0.0055", "--x", "1000"])
    check("C05 p(1000) ~ 0.0058 (ISLR p.149 prints 0.00576)", close(fval(o, "probability"), 0.00576, 0.0001), o)
    c, o = run([C, "logistic", "prob", "--b0", "-3.5041", "--coefs", "0.4049", "--x", "1"])
    check("C06 student: 0.0431 (ISLR p.150)", close(fval(o, "probability"), 0.0431, 0.0002), o)
    c, o = run([C, "logistic", "prob", "--b0", "-10.869", "--coefs", "0.00574,0.003,-0.6468", "--x", "1500,40,1"])
    check("C07 student with balance 1500 and income 40: 0.058 (ISLR p.152)", close(fval(o, "probability"), 0.058, 0.001), o)
    c, o = run([C, "logistic", "odds", "--p", "0.2"])
    check("C08 p = 0.2 -> odds 1/4 (ISLR p.147)", close(fval(o, "odds"), 0.25, 1e-9), o)
    c, o = run([C, "knn", "edge", "--p", "10", "--r", "0.01"])
    check("C09 e_10(0.01) = 0.63 (ESL p.41)", close(fval(o, "edge"), 0.63, 0.005), o)
    c, o = run([C, "knn", "edge", "--p", "10", "--r", "0.1"])
    check("C10 e_10(0.1) ~ 0.80 (ESL p.41)", close(fval(o, "edge"), 0.80, 0.01), o)
    c, o = run([C, "knn", "median-dist", "--p", "10", "--n", "500"])
    check("C11 d(10, 500) ~ 0.52 (ESL p.42)", close(fval(o, "d"), 0.52, 0.005), o)
    c, o = run([C, "kmeans", "partitions", "--n", "10", "--k", "4"])
    check("C12 S(10,4) = 34105 (ESL p.527)", val(o, "S") == "34105", o)
    c, o = run([C, "kmeans", "partitions", "--n", "19", "--k", "4"])
    check("C13 S(19,4) ~ 1e10 (ESL p.528)", 1e10 <= (fval(o, "S") or 0) <= 1.2e10, o)
    c, o = run([C, "boot", "err632", "--err", "0", "--err1", "0.5", "--p1", "0.5", "--q1", "0.5"])
    check("C14 1-NN: .632 = 0.316 and .632+ = 0.5 (ESL p.270-271)", close(fval(o, "err632"), 0.316, 1e-9) and close(fval(o, "err632_plus"), 0.5, 1e-9), o)
    c, o = run([C, "boot", "alpha", "--varx", "1", "--vary", "1.25", "--cov", "0.5"])
    check("C15 alpha = 0.6 (ISLR p.202-203)", close(fval(o, "alpha"), 0.6, 1e-9), o)
    c, o = run([C, "boot", "prob-in", "--n", "1000"])
    check("C16 probability of being in the bootstrap sample ~ 0.632 (ESL p.270)", close(fval(o, "probability"), 0.632, 0.001), o)
    c, o = run([C, "multtest", "expected-false", "--m", "12625", "--alpha", "0.05"])
    check("C17 expected false positives 631.3 and sd 24.5 (ESL p.704)", close(fval(o, "mean"), 631.25, 0.1) and close(fval(o, "std_dev"), 24.5, 0.1), o)
    c, o = run([C, "multtest", "bonferroni", "--m", "12625", "--alpha", "0.05"])
    check("C18 Bonferroni 0.05/12625 = 3.9e-6 (ESL p.705)", close(fval(o, "threshold") * 1e6 if fval(o, "threshold") else None, 3.96, 0.05), o)
    c, o = run([C, "multtest", "bh", "--pvalues", "0.001,0.008,0.039,0.041,0.042,0.06,0.074,0.205,0.212,0.216", "--alpha", "0.05"])
    check("C19 BH (ESL p.706-707): L = 2", val(o, "L") == "2" and "[1, 2]" in o, o)
    c, o = run([C, "node", "--left", "300,100", "--right", "100,300"])
    c2, o2 = run([C, "node", "--left", "200,400", "--right", "200,0"])
    check("C20 ESL p.328-329: same error 0.25; second split has lower Gini",
          close(fval(o, "weighted_error"), 0.25, 1e-9) and close(fval(o2, "weighted_error"), 0.25, 1e-9) and fval(o2, "weighted_gini") < fval(o, "weighted_gini"), o + o2)
    c, o = run([C, "criteria", "--rss", "100", "--n", "50", "--d", "3", "--sigma2", "2", "--tss", "400"])
    check("C21 Cp ISLR = Cp ESL; BIC ISLR = BIC ESL / n; AIC = Cp/sigma2",
          "relation_ISLR_Cp_equals_ESL_Cp = True" in o and "relation_ISLR_BIC_equals_ESL_BIC_over_N = True" in o and "relation_ISLR_AIC_equals_Cp_over_sigma2 = True" in o, o)
    c, o = run([C, "counts", "subsets", "--p", "20"])
    check("C22 p = 20: 1,048,576 versus 211 (ISLR p.223)", val(o, "best_subset") == "1048576" and val(o, "stepwise") == "211", o)
    c, o = run([C, "counts", "cov-params", "--p", "50", "--k", "2"])
    check("C23 p = 50: 1,275 covariance parameters (ISLR p.164-165)", val(o, "cov_one") == "1275", o)
    c, o = run([C, "kernel", "poly2-features", "--x", "0.3,-1.2", "--y", "2,0.5"])
    check("C24 degree-2 poly kernel = <h(x),h(x')> (ESL p.443)", "K_kernel = 1.0" in o and "K_via_h = 1.0" in o, o)
    c, o = run([C, "shrink", "lasso-ortho", "--beta", "1.0", "--lam", "0.5", "--convention", "islr"])
    c2, o2 = run([C, "shrink", "lasso-ortho", "--beta", "1.0", "--lam", "0.5", "--convention", "esl"])
    check("C25 orthonormal lasso: ISLR threshold lambda/2 -> 0.75; ESL threshold lambda -> 0.5", close(fval(o, "beta_lasso"), 0.75, 1e-9) and close(fval(o2, "beta_lasso"), 0.5, 1e-9), o + o2)
    c, o = run([C, "shrink", "ridge-ortho", "--beta", "2", "--lam", "1"])
    check("C26 orthonormal ridge beta/(1+lambda) = 1 (ISLR p.240)", close(fval(o, "beta_ridge"), 1.0, 1e-9), o)
    c, o = run([C, "ensemble", "adaboost", "--err", "0.25"])
    check("C27 AdaBoost alpha = ln 3 (ESL p.358)", close(fval(o, "alpha"), math.log(3), 1e-6), o)
    c, o = run([C, "ensemble", "rf-variance", "--rho", "0.05", "--sigma2", "1", "--B", "500"])
    check("C28 forest variance rho s2 + (1-rho)/B s2 = 0.0519 (ESL p.607)", close(fval(o, "variance"), 0.0519, 1e-6), o)
    c, o = run([C, "diag", "vif", "--r2", "0.99378"])
    check("C29 VIF ~ 160 for R2 = 0.9938 (ISLR p.117)", close(fval(o, "VIF"), 160.7, 0.2), o)
    c, o = run([C, "diag", "leverage", "--xs", "1,2,3,4,10"])
    check("C30 mean leverage = (p+1)/n (ISLR p.113)", close(fval(o, "mean"), 0.4, 1e-9), o)
    c, o = run([C, "lda1", "--mu=-1.25,1.25", "--sigma2", "1", "--x", "0.2"])
    check("C31 LDA p=1: boundary at 0 and x = 0.2 goes to class 2 (ISLR p.155)", "Bayes_boundary = 0.0" in o and "predicted_class = 2" in o, o)
    c, o = run([C, "cv", "one-se", "--table", "1:10:2,2:8:1.5,3:6.2:1.0,4:6.0:1.0,5:6.1:1.0"])
    check("C32 one-standard-error rule picks the smallest model within 1 SE (ISLR p.229)", close(fval(o, "chosen"), 3.0, 1e-9), o)
    c, o = run([C, "cv", "folds", "--n", "392", "--k", "10"])
    check("C33 k-fold: training size (k-1)n/k = 352.8 (ISLR p.198)", close(fval(o, "approx_training_size"), 352.8, 1e-9), o)
    c, o = run([C, "pca", "--variances", "2.48,0.99,0.357,0.173"])
    check("C34 PVE sums to 1", "1.0" in o or "0.99999" in o, o)
    c, o = run([C, "slr", "--x", "1,2,3,4,5", "--y", "5,8,11,14,17"])
    check("C35 simple regression: beta0 = 2, beta1 = 3 (ISLR p.77)", close(fval(o, "beta0"), 2.0, 1e-9) and close(fval(o, "beta1"), 3.0, 1e-9), o)
    c, o = run([C, "mse-decomp", "--truth", "1", "--preds", "0.8,1.2,1.1,0.9", "--noise-var", "0.5"])
    check("C36 bias-variance: expected error = bias2 + var + noise (ISLR p.49)", close(fval(o, "expected_error"), 0.525, 1e-9), o)
    c, o = run([C, "roc", "--scores", "0.9,0.8,0.7,0.6,0.55,0.4", "--labels", "1,1,0,1,0,0"])
    check("C37 AUC = 0.8889", close(fval(o, "AUC"), 0.888889, 1e-5), o)
    c, o = run([C, "regression", "--rss", "559.8", "--tss", "5435", "--n", "200", "--p", "3"])
    check("C38 Advertising (ISLR p.91): RSE 1.69, R2 0.897, F ~ 570", close(fval(o, "RSE"), 1.69, 0.01) and close(fval(o, "R2"), 0.897, 0.001) and close(fval(o, "F"), 570, 6), o)
    c, o = run([C, "t2", "--mean1", "1", "--mean2", "2", "--sd1", "1", "--sd2", "1", "--n1", "44", "--n2", "14"])
    check("C39 two-sample t (ESL p.703-704)", close(fval(o, "t"), 3.2589, 0.001), o)
    c, o = run([C, "node"])
    check("C40 incomplete input -> exit 2", c == 2, o)
    c, o = run([C, "logistic", "prob", "--b0", "0", "--coefs", "1", "--x", "0", "--json"])
    try:
        j = json.loads(o)
        check("C41 valid --json with formulas and pages", j["formulas"] and "page" in j["formulas"][0], o)
    except Exception as e:
        check("C41 valid --json", False, str(e))
    c, o = run([C, "ttest", "--coef", "1", "--se", "0.5", "--df", "58"])
    check("C42 t = 2 with 58 df: p ~ 0.05 (ESL p.69: quantile 2.002 with 58 df)", close(fval(o, "two_sided_p_value"), 0.0503, 0.001), o)
    c, o = run([C, "multtest", "fwer", "--alpha", "0.05", "--m", "100"])
    check("C43 independent FWER = 1-(1-0.05)^100", close(fval(o, "FWER_independent"), 1 - 0.95 ** 100, 1e-6), o)

    # ---------------- guide
    c, o = run([G, "recommend", "--n", "50", "--p", "5000"])
    check("G01 p > n -> rule G06 with ISLR p.256-259", "[G06]" in o and "ISLR p.256-259" in o, o)
    c, o = run([G, "show", "G28"])
    check("G02 G28 (boosting) with ISLR p.337-338 and ESL p.381-384", "ISLR p.337-338" in o and "ESL p.381-384" in o, o)
    c, o = run([G, "recommend", "--goal", "inference"])
    check("G03 inference -> G01", "[G01]" in o, o)
    c, o = run([G, "recommend", "--response", "multiclass"])
    check("G04 multiclass -> G19 (LDA and masking)", "[G19]" in o and "ESL p.124-125" in o, o)
    c, o = run([G, "recommend", "--imbalanced", "yes"])
    check("G05 imbalanced -> G22", "[G22]" in o, o)
    c, o = run([G, "recommend", "--many-tests", "yes"])
    check("G06 many tests -> G41 (FDR)", "[G41]" in o, o)
    c, o = run([G, "list", "--area", "trees"])
    check("G07 lists the tree rules", "G27" in o and "G28" in o, o)
    c, o = run([G, "list", "--area", "arvores"])
    check("G07b Portuguese area name still accepted (arvores)", "G27" in o and "G28" in o, o)
    c, o = run([G, "recommend", "--json", "--n", "1000", "--p", "10"])
    try:
        j = json.loads(o)
        check("G08 --json: n >> p derived", j["facts"].get("np") == "n_gg_p", o)
    except Exception as e:
        check("G08 valid --json", False, str(e))

    # ---------------- verifier (optional)
    if a.src:
        c, o = run([os.path.join("tests", "verify_citations.py"), "--src", a.src])
        check("V01 verify_citations passes (positive and negative)", c == 0, o[-600:])
        c, o = run([os.path.join("tests", "audit_numbers.py"), "--src", a.src])
        check("V02 audit_numbers runs", c == 0 and "Numbers checked" in o, o[-300:])

    print(f"\n{len(OK)} PASS, {len(FAIL)} FAIL")
    for n in FAIL:
        print("  FAILED:", n)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
