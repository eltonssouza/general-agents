# -*- coding: utf-8 -*-
"""
slr_calc.py - calculators for metrics and concepts of ISLR (1st ed.) and ESL (2nd ed.), standard library only.

Deterministic, no network, read-only. Run with:  python -I scripts/slr_calc.py SUBCOMMAND [options] [--json]
Page convention: PDF (printed ISLR = PDF - 15; printed ESL = PDF - 19). Each output carries formula, page and source label:
  [from source] = formula/value checked on the cited page; [inference] = direct deduction; [extrapolation] = outside the collection.

Subcommands:  python -I scripts/slr_calc.py --help   (list) ;   python -I scripts/slr_calc.py SUB --help
"""
import argparse
import json
import math
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ----------------------------------------------------------------- numeric utilities
def flist(s):
    return [float(x) for x in str(s).replace(";", ",").split(",") if x.strip() != ""]


def mean(v):
    return sum(v) / len(v)


def var_pop(v):
    m = mean(v)
    return sum((x - m) ** 2 for x in v) / len(v)


def sd_samp(v):
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def betacf(a, b, x):
    MAXIT, EPS, FPMIN = 400, 3e-16, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = FPMIN if abs(d) < FPMIN else d
        c = 1.0 + aa / c
        c = FPMIN if abs(c) < FPMIN else c
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = FPMIN if abs(d) < FPMIN else d
        c = 1.0 + aa / c
        c = FPMIN if abs(c) < FPMIN else c
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def betai(a, b, x):
    """Regularized incomplete beta I_x(a,b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * betacf(a, b, x) / a
    return 1.0 - front * betacf(b, a, 1.0 - x) / b


def t_pvalue_two_sided(t, df):
    return betai(df / 2.0, 0.5, df / (df + t * t))


def f_pvalue_upper(F, d1, d2):
    if F <= 0:
        return 1.0
    return betai(d2 / 2.0, d1 / 2.0, d2 / (d2 + d1 * F))


def t_quantile_two_sided(alpha, df):
    """t quantile such that P(|T|>q)=alpha (bisection)."""
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_pvalue_two_sided(mid, df) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def impurities(counts):
    n = float(sum(counts))
    p = [c / n for c in counts]
    mis = 1.0 - max(p)
    gini = sum(x * (1 - x) for x in p)
    ent = -sum(x * math.log(x) for x in p if x > 0)
    return n, p, mis, gini, ent


# ----------------------------------------------------------------- standardized output
class Out:
    def __init__(self, args, title):
        self.args = args
        self.d = {"calculation": title, "formulas": [], "result": {}, "notes": []}

    def f(self, text, cite, source="[from source]"):
        self.d["formulas"].append({"formula": text, "page": cite, "source": source})

    def r(self, **kw):
        self.d["result"].update(kw)

    def n(self, note):
        self.d["notes"].append(note)

    def emit(self):
        if getattr(self.args, "json", False):
            print(json.dumps(self.d, ensure_ascii=False, indent=1))
            return 0
        print(f"== {self.d['calculation']} ==")
        for f in self.d["formulas"]:
            print(f"Formula: {f['formula']}  ({f['page']}) {f['source']}")
        for k, v in self.d["result"].items():
            if isinstance(v, float):
                v = float(f"{v:.3e}") if (v != 0 and abs(v) < 1e-4) else round(v, 6)
            print(f"  {k} = {v}")
        for n in self.d["notes"]:
            print("Note:", n)
        return 0


# ----------------------------------------------------------------- subcommands
def c_mse_decomp(a):
    o = Out(a, "Decomposition of the expected test error at x0 (bias-variance)")
    preds = flist(a.preds)
    m = mean(preds)
    var = var_pop(preds)
    bias = m - a.truth
    o.f("E(y0 - f^(x0))^2 = Var(f^(x0)) + [Bias(f^(x0))]^2 + Var(eps)  (eq. 2.7)", "ISLR p.49")
    o.f("Err(x0) = sigma_eps^2 + Bias^2 + Var  (eq. 7.9)", "ESL p.242")
    o.r(mean_of_predictions=m, bias=bias, squared_bias=bias ** 2, variance=var, noise_variance=a.noise_var,
        expected_error=bias ** 2 + var + a.noise_var)
    o.n("The variance uses divisor n (population of the replicates); the predictions are f^(x0) obtained on distinct training sets. Valid for squared loss: for 0-1 loss bias and variance do NOT add up (ESL p.245-247).")
    return o.emit()


def c_regression(a):
    o = Out(a, "Linear regression fit measures")
    n, p = a.n, a.p
    rse = math.sqrt(a.rss / (n - p - 1))
    r2 = 1 - a.rss / a.tss
    adj = 1 - (a.rss / (n - p - 1)) / (a.tss / (n - 1))
    F = ((a.tss - a.rss) / p) / (a.rss / (n - p - 1))
    o.f("RSE = sqrt(RSS/(n-p-1))  (3.25; p=1: 3.15)", "ISLR p.95; ISLR p.84")
    o.f("R^2 = 1 - RSS/TSS  (3.17)", "ISLR p.85")
    o.f("adjusted R^2 = 1 - [RSS/(n-d-1)]/[TSS/(n-1)]  (6.4)", "ISLR p.227")
    o.f("F = [(TSS-RSS)/p] / [RSS/(n-p-1)]  (3.23)", "ISLR p.90")
    o.r(RSE=rse, R2=r2, adjusted_R2=adj, F=F, df1=p, df2=n - p - 1, F_p_value=f_pvalue_upper(F, p, n - p - 1))
    return o.emit()


def c_confusion(a):
    o = Out(a, "Confusion matrix: rates")
    tp, fp, fn, tn = a.tp, a.fp, a.fn, a.tn
    N = tn + fp
    P = tp + fn
    Pp = tp + fp
    Nn = tn + fn
    tot = N + P
    div = lambda x, y: (x / y) if y else float("nan")
    o.f("Error rate = (FP+FN)/total; FPR = FP/N; TPR = TP/P (sensitivity, recall, power); PPV = TP/P* (precision); NPV = TN/N*; specificity = 1 - FPR", "ISLR p.163-164; ISLR p.160")
    o.r(total=tot, error=div(fp + fn, tot), sensitivity_TPR=div(tp, P), specificity=div(tn, N), FPR=div(fp, N),
        PPV_precision=div(tp, Pp), NPV=div(tn, Nn), null_classifier_error=div(min(P, N), tot))
    f1 = div(2 * tp, 2 * tp + fp + fn)
    o.r(F1_extrapolation=f1)
    o.n("F1 is NOT on the pages read: [extrapolation]. Null classifier = always predict the majority class (ISLR p.159-160).")
    return o.emit()


def c_roc(a):
    o = Out(a, "ROC curve and AUC (points per threshold)")
    sc = flist(a.scores)
    lab = [int(x) for x in a.labels.replace(";", ",").split(",") if x.strip() != ""]
    if len(sc) != len(lab):
        print("scores and labels have different lengths")
        return 2
    P = sum(lab)
    N = len(lab) - P
    pts = [(0.0, 0.0)]
    for t in sorted(set(sc), reverse=True):
        tp = sum(1 for s, y in zip(sc, lab) if s >= t and y == 1)
        fp = sum(1 for s, y in zip(sc, lab) if s >= t and y == 0)
        pts.append((fp / N, tp / P))
    if pts[-1] != (1.0, 1.0):
        pts.append((1.0, 1.0))
    auc = sum((x1 - x0) * (y0 + y1) / 2 for (x0, y0), (x1, y1) in zip(pts, pts[1:]))
    o.f("ROC: true positive rate (sensitivity) against false positive rate (1 - specificity) over all thresholds; AUC = area under the curve (0.5 = chance)", "ISLR p.162-163")
    o.r(points_FPR_TPR=[(round(x, 4), round(y, 4)) for x, y in pts], AUC=auc)
    o.n("The trapezoidal AUC computation is [inference] (the book defines the AUC as the area, without giving the algorithm).")
    return o.emit()


def c_cv(a):
    o = Out(a, "Cross-validation")
    if a.op == "folds":
        n, k = a.n, a.k
        base, extra = divmod(n, k)
        sizes = [base + 1 if i < extra else base for i in range(k)]
        o.f("k-fold: k groups of size ~ n/k; training on (k-1)n/k observations; LOOCV = k = n; in practice k = 5 or 10", "ISLR p.196; ISLR p.198")
        o.r(fold_sizes=sizes, approx_training_size=(k - 1) * n / k)
    elif a.op == "est":
        e = flist(a.errors)
        o.f("CV(k) = (1/k) sum MSE_i  (5.3)", "ISLR p.196")
        o.f("CV(f) = (1/N) sum L(y_i, f^{-kappa(i)}(x_i))  (7.48)", "ESL p.261")
        o.r(CV=mean(e), standard_error=sd_samp(e) / math.sqrt(len(e)) if len(e) > 1 else float("nan"))
        o.n("The standard error (sample standard deviation / square root of k) is [inference]: the book shows standard error bars without giving the formula (ESL p.263).")
    elif a.op == "one-se":
        rows = []
        for tok in a.table.split(","):
            s, m, se = tok.split(":")
            rows.append((float(s), float(m), float(se)))
        best = min(rows, key=lambda r: r[1])
        lim = best[1] + best[2]
        cand = [r for r in rows if r[1] <= lim]
        pick = min(cand, key=lambda r: r[0])
        o.f("One-standard-error rule: smallest model whose error is within 1 SE of the minimum", "ISLR p.229; ESL p.263")
        o.r(minimum_at=best[0], limit=lim, chosen=pick[0])
    elif a.op == "loocv-ols":
        res = flist(a.resid)
        h = flist(a.leverage)
        cv = mean([(r / (1 - hi)) ** 2 for r, hi in zip(res, h)])
        o.f("CV(n) = (1/n) sum ((y_i - yhat_i)/(1 - h_i))^2  (5.2) [only linear/polynomial least squares]", "ISLR p.195-196")
        o.f("Version for linear smoothers: replace h_i by S_ii (7.51); GCV uses trace(S)/N (7.52)", "ESL p.263-264")
        o.r(CV_n=cv)
    return o.emit()


def c_criteria(a):
    o = Out(a, "Cp, AIC, BIC and adjusted R² (least squares model, d predictors)")
    n, d, s2, rss = a.n, a.d, a.sigma2, a.rss
    err = rss / n
    cp_islr = (rss + 2 * d * s2) / n
    aic_islr = (rss + 2 * d * s2) / (n * s2)
    bic_islr = (rss + math.log(n) * d * s2) / (n * s2)
    cp_esl = err + 2 * (d / n) * s2
    bic_esl = (n / s2) * (err + math.log(n) * (d / n) * s2)
    o.f("ISLR: Cp = (1/n)(RSS + 2 d sigma^2)  (6.2)", "ISLR p.226")
    o.f("ISLR: AIC = (1/(n sigma^2))(RSS + 2 d sigma^2) (constant omitted)", "ISLR p.227")
    o.f("ISLR: BIC = (1/(n sigma^2))(RSS + log(n) d sigma^2)  (6.3) [checked visually on the rendered page]", "ISLR p.227")
    o.f("ESL: Cp = err + 2 (d/N) sigma^2 (7.26) = AIC(alpha) (7.30); err = RSS/N", "ESL p.249; ESL p.250")
    o.f("ESL: BIC = (N/sigma^2)[err + (log N)(d/N) sigma^2]  (7.36) = -2 loglik + (log N) d in the Gaussian case  (7.35)", "ESL p.252")
    r = dict(ISLR_Cp=cp_islr, ISLR_AIC=aic_islr, ISLR_BIC=bic_islr, ESL_Cp_AIC=cp_esl, ESL_BIC=bic_esl)
    if a.tss:
        r["adjusted_R2"] = 1 - (rss / (n - d - 1)) / (a.tss / (n - 1))
    o.r(**r)
    o.r(relation_ISLR_Cp_equals_ESL_Cp=abs(cp_islr - cp_esl) < 1e-9 * max(1, abs(cp_esl)),
        relation_ISLR_BIC_equals_ESL_BIC_over_N=abs(bic_islr - bic_esl / n) < 1e-9 * max(1, abs(bic_islr)),
        relation_ISLR_AIC_equals_Cp_over_sigma2=abs(aic_islr - cp_islr / s2) < 1e-9 * max(1, abs(aic_islr)))
    o.n("The scales differ, but they rank the models the same way for fixed n and sigma^2 [inference]. Do not compare numbers from one convention with those of the other. Minimum is better (adjusted R²: maximum). With p > n these criteria do not apply (ISLR p.256).")
    o.n("log(n) > 2 for n > 7: BIC penalizes more than Cp (ISLR p.227; ESL p.252).")
    return o.emit()


def c_node(a):
    o = Out(a, "Tree node impurity")
    o.f("Classification error E = 1 - max p_mk (8.5); Gini = sum p(1-p) (8.6); Entropy = -sum p log p (8.7)", "ISLR p.326-327")
    o.f("Impurities (9.17); weight by the sizes N_mL and N_mR of the child nodes", "ESL p.328")
    if a.op == "node":
        n, p, mis, g, e = impurities([float(x) for x in a.counts.split(",")])
        o.r(n=n, proportions=[round(x, 4) for x in p], misclassification_error=mis, gini=g, entropy_nats=e)
    else:
        L = [float(x) for x in a.left.split(",")]
        R = [float(x) for x in a.right.split(",")]
        nl, _, ml, gl, el = impurities(L)
        nr, _, mr, gr, er = impurities(R)
        t = nl + nr
        o.r(weighted_error=(nl * ml + nr * mr) / t, weighted_gini=(nl * gl + nr * gr) / t, weighted_entropy=(nl * el + nr * er) / t)
        o.n("ESL example (p.328-329): (300,100)+(100,300) and (200,400)+(200,0) have the same error 0.25, but the second has lower Gini and entropy (pure node): grow the tree with Gini or entropy.")
    return o.emit()


def c_ttest(a):
    o = Out(a, "t statistic and CI of a coefficient")
    t = a.coef / a.se
    p = t_pvalue_two_sided(t, a.df)
    q = t_quantile_two_sided(0.05, a.df)
    o.f("t = (beta^ - 0)/SE(beta^)  (3.14); 95% CI ~ beta^ +- 2 SE (3.9), exactly the 97.5% quantile of the t with n-2 df", "ISLR p.82; ISLR p.81")
    o.f("Z-score z_j = beta^_j/(sigma^ sqrt(v_j))  (3.12)", "ESL p.67")
    o.r(t=t, two_sided_p_value=p, t_quantile_97_5=q, CI95_approx_2SE=(a.coef - 2 * a.se, a.coef + 2 * a.se), CI95_exact=(a.coef - q * a.se, a.coef + q * a.se))
    return o.emit()


def c_ftest(a):
    o = Out(a, "F test for a subset of coefficients (nested models)")
    d1 = a.p1 - a.p0
    d2 = a.n - a.p1 - 1
    F = ((a.rss0 - a.rss1) / d1) / (a.rss1 / d2)
    o.f("F = [(RSS0 - RSS1)/(p1 - p0)] / [RSS1/(N - p1 - 1)]  (3.13); ISLR (3.24) com q = p1 - p0", "ESL p.67; ISLR p.92")
    o.r(F=F, df1=d1, df2=d2, p_value=f_pvalue_upper(F, d1, d2))
    o.n("Book test (ESL p.70): RSS0 = 32.81, RSS1 = 29.43, N = 67, larger model with 9 parameters (p1 = 8 predictors + intercept) and smaller with 5 (p0 = 4): F = 1.67 with (4, 58) df and p = 0.17.")
    return o.emit()


def c_t2(a):
    o = Out(a, "Two-sample t statistic (pooled), one per variable/gene")
    s2 = ((a.n1 - 1) * a.sd1 ** 2 + (a.n2 - 1) * a.sd2 ** 2) / (a.n1 + a.n2 - 2)
    se = math.sqrt(s2) * math.sqrt(1 / a.n1 + 1 / a.n2)
    t = (a.mean2 - a.mean1) / se
    o.f("t_j = (x2bar_j - x1bar_j)/se_j; se_j = sigma^_j sqrt(1/N1 + 1/N2); sigma^2 = [sum_C1 + sum_C2 (x - xbar)^2]/(N1+N2-2)  (18.38)(18.39)", "ESL p.703-704")
    o.r(pooled_sigma2=s2, se=se, t=t, two_sided_p_value=t_pvalue_two_sided(t, a.n1 + a.n2 - 2))
    return o.emit()


def c_multtest(a):
    o = Out(a, "Multiple testing")
    m, al = a.m, a.alpha
    if a.op == "bonferroni":
        o.f("Bonferroni: reject H0j if p_j < alpha/M; FWER <= alpha", "ESL p.705")
        o.r(threshold=al / m)
    elif a.op == "fwer":
        o.f("FWER (independent tests) = 1 - (1 - alpha)^M", "ESL p.705")
        o.r(FWER_independent=1 - (1 - al) ** m)
    elif a.op == "expected-false":
        o.f("False positives under the global null (independent): binomial(M, alpha), mean M*alpha, sd sqrt(M alpha (1-alpha))", "ESL p.704")
        o.r(mean=m * al, std_dev=math.sqrt(m * al * (1 - al)))
    elif a.op == "bh":
        p = flist(a.pvalues)
        M = len(p)
        order = sorted(range(M), key=lambda i: p[i])
        L = 0
        for j, i in enumerate(order, start=1):
            if p[i] < al * j / M:
                L = j
        thr = p[order[L - 1]] if L else None
        rej = sorted(i + 1 for i in order[:L])
        o.f("Benjamini-Hochberg: L = max{ j : p_(j) < alpha*j/M }; reject all with p_j <= p_(L); FDR <= (M0/M) alpha (independence)", "ESL p.706-707")
        o.r(M=M, L=L, BH_threshold=thr, rejected_indices_1based=rej)
    elif a.op == "fdr-plugin":
        o.f("FDR^ = E^(V)/R_obs, with E^(V) = (1/K) sum_j sum_k I(|t^k_j| > C)  (18.46)", "ESL p.708")
        o.r(estimated_FDR=a.ev / a.robs)
        o.n("Book example (ESL p.708): 1518/1000 = 1.518 average permutations above C = 4.101 and R_obs = 11: FDR^ ~ 14%.")
    return o.emit()


def c_boot(a):
    o = Out(a, "Bootstrap and error estimators")
    if a.op == "prob-in":
        v = 1 - (1 - 1 / a.n) ** a.n
        o.f("Pr(obs i is in the bootstrap sample) = 1 - (1 - 1/N)^N ~ 0.632  (7.55)", "ESL p.270")
        o.r(probability=v, limit_1_minus_exp_minus_1=1 - math.exp(-1))
    elif a.op == "err632":
        o.f(".632: 0.368*err + 0.632*Err(1)  (7.57); gamma = p1(1-q1)+(1-p1)q1 (7.59); R = (Err(1)-err)/(gamma-err) (7.60); w = 0.632/(1-0.368R); .632+ = (1-w) err + w Err(1)  (7.61)", "ESL p.270-271")
        e632 = 0.368 * a.err + 0.632 * a.err1
        o.r(err632=e632)
        if a.p1 is not None and a.q1 is not None:
            g = a.p1 * (1 - a.q1) + (1 - a.p1) * a.q1
            R = (a.err1 - a.err) / (g - a.err) if g != a.err else float("nan")
            R = max(0.0, min(1.0, R))
            w = 0.632 / (1 - 0.368 * R)
            o.r(gamma=g, R=R, w=w, err632_plus=(1 - w) * a.err + w * a.err1)
        o.n("Book example (1-NN, independent labels, p1 = q1 = 0.5): err = 0, Err(1) = 0.5 gives .632 = 0.316 and .632+ = 0.5 (ESL p.270-271).")
    elif a.op == "alpha":
        al = (a.vary - a.cov) / (a.varx + a.vary - 2 * a.cov)
        o.f("alpha = (sigma_Y^2 - sigma_XY)/(sigma_X^2 + sigma_Y^2 - 2 sigma_XY)  (5.6)", "ISLR p.202")
        o.r(alpha=al)
    elif a.op == "se":
        v = flist(a.values)
        o.f("SE_B(alpha^) = sqrt( (1/(B-1)) sum_r (alpha*_r - mean)^2 )  (5.8); bootstrap variance (7.53)", "ISLR p.204; ESL p.268-269")
        o.r(B=len(v), mean=mean(v), SE_B=sd_samp(v))
    return o.emit()


def c_knn(a):
    o = Out(a, "kNN and the curse of dimensionality")
    if a.op == "edge":
        o.f("Expected edge of the neighborhood cube that captures the fraction r in p dimensions: e_p(r) = r^(1/p)", "ESL p.41")
        o.r(edge=a.r ** (1 / a.p))
    elif a.op == "median-dist":
        d = (1 - 0.5 ** (1.0 / a.n)) ** (1.0 / a.p)
        o.f("Median distance from the origin to the nearest neighbor: d(p,N) = (1 - (1/2)^(1/N))^(1/p)  (2.24)", "ESL p.42")
        o.r(d=d)
    elif a.op == "epe":
        nb = flist(a.neighbors)
        k = len(nb)
        bias = a.fx0 - mean(nb)
        o.f("EPE_k(x0) = sigma^2 + [f(x0) - (1/k) sum f(x_(l))]^2 + sigma^2/k  (2.47)", "ESL p.56; ESL p.242")
        o.r(k=k, squared_bias=bias ** 2, variance=a.sigma2 / k, EPE=a.sigma2 + bias ** 2 + a.sigma2 / k)
    return o.emit()


def c_logistic(a):
    o = Out(a, "Logistic regression: probability, odds and logit")
    if a.op == "prob":
        xs = flist(a.x)
        bs = flist(a.coefs)
        z = a.b0 + sum(b * x for b, x in zip(bs, xs))
        p = 1 / (1 + math.exp(-z))
        o.f("p(X) = e^{b0+b1X1+...}/(1+e^{...})  (4.2, 4.7); odds = p/(1-p) = e^{...} (4.3); logit = b0 + b1X1 + ... (4.4, 4.6)", "ISLR p.147; ISLR p.150")
        o.r(logit=z, odds=math.exp(z), probability=p)
        o.n("Book test (ISLR p.149): b0 = -10.6513, b1 = 0.0055: X = 1000 -> p ~ 0.0057; X = 2000 -> p = 0.586 (the book prints 0.00576 because it uses unrounded coefficients).")
    elif a.op == "odds":
        o.f("odds = p/(1-p): p = 0.2 -> 1/4; p = 0.9 -> 9", "ISLR p.147")
        o.r(odds=a.p / (1 - a.p))
    else:
        o.f("p = odds/(1+odds)", "ISLR p.147")
        o.r(p=a.odds / (1 + a.odds))
    return o.emit()


def c_lda1(a):
    o = Out(a, "LDA with p = 1")
    mu = flist(a.mu)
    pi = flist(a.pi) if a.pi else [1.0 / len(mu)] * len(mu)
    s2 = a.sigma2
    d = [a.x * m / s2 - m * m / (2 * s2) + math.log(p) for m, p in zip(mu, pi)]
    mx = max(d)
    post = [math.exp(v - mx) for v in d]
    sm = sum(post)
    post = [v / sm for v in post]
    o.f("delta_k(x) = x mu_k/sigma^2 - mu_k^2/(2 sigma^2) + log pi_k  (4.13); class with the largest delta; boundary (mu1+mu2)/2 if pi1 = pi2 (4.14)", "ISLR p.155")
    o.r(deltas=d, predicted_class=1 + d.index(mx), posteriors=post)
    if len(mu) == 2 and abs(pi[0] - pi[1]) < 1e-12:
        o.r(Bayes_boundary=(mu[0] + mu[1]) / 2)
    return o.emit()


def c_shrink(a):
    o = Out(a, "Shrinkage in the orthonormal case and ridge df")
    if a.op == "ridge-ortho":
        o.f("Ridge: beta^R = beta^ /(1 + lambda)  (ISLR 6.14 com X = I; ESL Tabela 3.4)", "ISLR p.240; ESL p.90")
        o.r(beta_ridge=a.beta / (1 + a.lam))
    elif a.op == "lasso-ortho":
        b, l = a.beta, a.lam
        if a.convention == "islr":
            thr = l / 2
            o.f("Lasso (ISLR 6.15, objective 6.13): y_j - lambda/2 if y_j > lambda/2; y_j + lambda/2 if y_j < -lambda/2; 0 otherwise (soft-thresholding)", "ISLR p.240")
        else:
            thr = l
            o.f("Lasso (ESL Table 3.4, objective 3.52 with 1/2 RSS): sign(beta)(|beta| - lambda)_+", "ESL p.90; ESL p.87")
        v = math.copysign(max(abs(b) - thr, 0.0), b)
        o.r(threshold=thr, beta_lasso=v)
        o.n("The lambda scales differ between ISLR (threshold lambda/2) and ESL (threshold lambda): do not mix them.")
    else:
        d = flist(a.d)
        dfv = sum(x * x / (x * x + a.lam) for x in d)
        o.f("df(lambda) = sum_j d_j^2/(d_j^2 + lambda)  (3.50)", "ESL p.87")
        o.f("Shrinkage factor of coordinate j: d_j^2/(d_j^2 + lambda)  (3.47)", "ESL p.85")
        o.r(df=dfv, factors=[x * x / (x * x + a.lam) for x in d])
    return o.emit()


def c_kernel(a):
    o = Out(a, "SVM kernels and hinge loss")
    if a.op == "hinge":
        o.f("Hinge: max[0, 1 - y f(x)]  (9.25)", "ISLR p.371-372; ESL p.445")
        o.r(hinge=max(0.0, 1 - a.y * a.f))
        return o.emit()
    x = flist(a.x)
    y = flist(a.y)
    dot = sum(u * v for u, v in zip(x, y))
    if a.op == "linear":
        o.f("K = sum x_ij x_i'j  (9.21)", "ISLR p.367")
        o.r(K=dot)
    elif a.op == "poly":
        o.f("K = (1 + sum x_ij x_i'j)^d  (9.22; ESL 12.22)", "ISLR p.367; ESL p.443")
        o.r(K=(1 + dot) ** a.d)
    elif a.op == "radial":
        o.f("K = exp(-gamma sum (x_ij - x_i'j)^2)  (9.24; ESL 12.22)", "ISLR p.367; ESL p.443")
        o.r(K=math.exp(-a.gamma * sum((u - v) ** 2 for u, v in zip(x, y))))
    elif a.op == "poly2-features":
        def h(v):
            x1, x2 = v
            r2 = math.sqrt(2)
            return [1, r2 * x1, r2 * x2, x1 * x1, x2 * x2, r2 * x1 * x2]
        hx, hy = h(x), h(y)
        o.f("Degree-2 polynomial kernel in 2 inputs = <h(x), h(x')> with h = (1, sqrt2 x1, sqrt2 x2, x1^2, x2^2, sqrt2 x1 x2), M = 6  (12.23)", "ESL p.443")
        o.r(K_kernel=(1 + dot) ** 2, K_via_h=sum(u * v for u, v in zip(hx, hy)), h_x=hx, h_y=hy)
    return o.emit()


def c_pca(a):
    o = Out(a, "PCA: proportion of variance explained")
    v = flist(a.variances)
    tot = sum(v)
    pve = [x / tot for x in v]
    cum = []
    s = 0
    for x in pve:
        s += x
        cum.append(s)
    o.f("PVE_m = (variance of component m)/(total variance); the PVEs sum to 1; at most min(n-1, p) components", "ISLR p.397-398; ISLR p.392")
    o.r(PVE=pve, cumulative=cum)
    return o.emit()


def c_kmeans(a):
    o = Out(a, "K-means: objective and number of partitions")
    if a.op == "objective":
        pts = [flist(r) for r in a.points.split(";")]
        asg = [int(x) for x in a.assign.split(",")]
        ks = sorted(set(asg))
        pair = 0.0
        cent = 0.0
        for k in ks:
            idx = [i for i, g in enumerate(asg) if g == k]
            for i in idx:
                for j in idx:
                    pair += sum((u - v) ** 2 for u, v in zip(pts[i], pts[j])) / len(idx)
            m = [mean([pts[i][d] for i in idx]) for d in range(len(pts[0]))]
            for i in idx:
                cent += sum((u - v) ** 2 for u, v in zip(pts[i], m))
        o.f("W = sum_k (1/|C_k|) sum_{i,i' in C_k} sum_j (x_ij - x_i'j)^2  (10.11) = 2 sum_k sum_{i in C_k} ||x_i - xbar_k||^2  (10.12)", "ISLR p.402; ISLR p.403")
        o.r(objective_pairs_10_11=pair, twice_sum_to_centroids_10_12=2 * cent, identity_holds=abs(pair - 2 * cent) < 1e-9 * max(1, pair))
        o.n("The ESL (14.31) writes W(C) = sum N_k sum ||x_i - xbar_k||^2 with 1/2 in the definition (14.28): ESL p.527-528.")
    else:
        N, K = a.n, a.k
        S = sum((-1) ** (K - k) * math.comb(K, k) * k ** N for k in range(1, K + 1)) // math.factorial(K)
        o.f("S(N,K) = (1/K!) sum_{k=1}^{K} (-1)^{K-k} C(K,k) k^N  (14.30)", "ESL p.527")
        o.r(S=S)
        o.n("Book test: S(10,4) = 34,105 and S(19,4) ~ 1e10 (ESL p.527-528). ISLR p.403: about K^n partitions.")
    return o.emit()


def c_counts(a):
    o = Out(a, "Counts of models and parameters")
    if a.op == "subsets":
        p = a.p
        o.f("Best subset: 2^p modelos; forward/backward stepwise: 1 + p(p+1)/2", "ISLR p.221; ISLR p.223-224")
        o.r(best_subset=2 ** p, stepwise=1 + p * (p + 1) // 2)
        o.n("p = 20: 1,048,576 versus 211 (ISLR p.223). p = 30: 2^30 = 1,073,741,824 (ISLR p.93).")
    elif a.op == "cov-params":
        p, K = a.p, a.k
        o.f("Each covariance: p(p+1)/2; QDA: K p(p+1)/2; LDA has K p linear coefficients", "ISLR p.164-165")
        o.f("Boundary parameters: LDA (K-1)(p+1); QDA (K-1){p(p+3)/2 + 1}", "ESL p.129-130")
        o.r(cov_one=p * (p + 1) // 2, QDA_covariances=K * p * (p + 1) // 2, LDA_linear_coefs=K * p, LDA_boundaries=(K - 1) * (p + 1), QDA_boundaries=(K - 1) * (p * (p + 3) // 2 + 1))
        o.n("p = 50: 1,275 per matrix (ISLR p.164-165).")
    else:
        o.f("Cubic spline with K knots uses 4 + K degrees of freedom", "ISLR p.288")
        o.r(df=4 + a.knots)
    return o.emit()


def c_ensemble(a):
    o = Out(a, "Bagging, random forests and boosting")
    if a.op == "rf-variance":
        o.f("Var(average of B identically distributed trees with correlation rho) = rho sigma^2 + (1-rho)/B sigma^2  (15.1)", "ESL p.607")
        o.r(variance=a.rho * a.sigma2 + (1 - a.rho) / a.B * a.sigma2, limit_B_infinity=a.rho * a.sigma2)
        o.n("For B independent variables (rho = 0): sigma^2/B (ISLR p.331; ESL p.607).")
    elif a.op == "oob":
        pr = 1 - (1 - 1 / a.n) ** a.n
        o.f("Each tree uses ~2/3 of the observations; ~1/3 of the trees (B/3) have each observation as OOB", "ISLR p.333; ESL p.270")
        o.r(fraction_in_sample=pr, oob_trees_per_observation=a.B * (1 - pr))
    elif a.op == "adaboost":
        e = a.err
        al = math.log((1 - e) / e)
        o.f("AdaBoost.M1: alpha_m = log((1-err_m)/err_m); w_i <- w_i exp[alpha_m I(y_i != G_m(x_i))]; beta_m = alpha_m/2  (10.12)", "ESL p.358; ESL p.363")
        o.r(alpha=al, beta=al / 2, error_weight_factor=math.exp(al), correct_factor=1.0)
        o.n("The factors matter only in relative terms: multiplying all weights by e^{-beta} changes nothing (ESL p.363).")
    elif a.op == "boost-update":
        o.f("Regression boosting (Alg. 8.2): f <- f + lambda f^b (8.10); r_i <- r_i - lambda f^b(x_i) (8.11)", "ISLR p.338")
        fb = flist(a.fb)
        r = flist(a.resid)
        o.r(new_residuals=[ri - a.lam * fi for ri, fi in zip(r, fb)])
    return o.emit()


def c_diag(a):
    o = Out(a, "Regression diagnostics: VIF and leverage")
    if a.op == "vif":
        if a.r2 is not None:
            o.f("VIF(beta_j) = 1/(1 - R^2_{Xj|X-j}); minimum 1; rule of thumb: above 5 or 10 is problematic", "ISLR p.116-117")
            o.r(VIF=1 / (1 - a.r2))
        else:
            o.f("R^2_{Xj|X-j} = 1 - 1/VIF", "ISLR p.116-117")
            o.r(R2=1 - 1 / a.vif)
    else:
        xs = flist(a.xs)
        n = len(xs)
        xb = mean(xs)
        sxx = sum((x - xb) ** 2 for x in xs)
        h = [1 / n + (x - xb) ** 2 / sxx for x in xs]
        o.f("h_i = 1/n + (x_i - xbar)^2 / sum (x_i' - xbar)^2  (3.37); h_i in [1/n, 1]; mean (p+1)/n", "ISLR p.113")
        o.r(leverage=h, mean=mean(h), expected_mean_p_plus_1_over_n=2 / n)
    return o.emit()


def c_slr(a):
    o = Out(a, "Simple linear regression")
    x, y = flist(a.x), flist(a.y)
    n = len(x)
    xb, yb = mean(x), mean(y)
    sxx = sum((u - xb) ** 2 for u in x)
    b1 = sum((u - xb) * (v - yb) for u, v in zip(x, y)) / sxx
    b0 = yb - b1 * xb
    rss = sum((v - b0 - b1 * u) ** 2 for u, v in zip(x, y))
    tss = sum((v - yb) ** 2 for v in y)
    rse = math.sqrt(rss / (n - 2)) if n > 2 else float("nan")
    se1 = rse / math.sqrt(sxx) if n > 2 else float("nan")
    se0 = rse * math.sqrt(1 / n + xb * xb / sxx) if n > 2 else float("nan")
    o.f("beta1 = sum (x-xbar)(y-ybar)/sum (x-xbar)^2; beta0 = ybar - beta1 xbar  (3.4)", "ISLR p.77")
    o.f("SE(beta1)^2 = sigma^2/sum (x-xbar)^2; SE(beta0)^2 = sigma^2 [1/n + xbar^2/sum (x-xbar)^2]; RSE = sqrt(RSS/(n-2))  (3.8)", "ISLR p.81")
    o.r(beta0=b0, beta1=b1, RSS=rss, TSS=tss, R2=1 - rss / tss, RSE=rse, SE_beta0=se0, SE_beta1=se1)
    return o.emit()


# ----------------------------------------------------------------- CLI
def build():
    ap = argparse.ArgumentParser(description="ISLR/ESL calculators (stdlib). Each output carries formula, page and label.")
    sub = ap.add_subparsers(dest="cmd")

    def add(name, fn, help_):
        p = sub.add_parser(name, help=help_)
        p.add_argument("--json", action="store_true")
        p.set_defaults(_run=fn)
        return p

    p = add("mse-decomp", c_mse_decomp, "squared bias, variance and expected error (ISLR 2.7, ESL 7.9)")
    p.add_argument("--truth", type=float, required=True, help="true f(x0)")
    p.add_argument("--preds", required=True, help="predictions f^(x0) over several training sets: a,b,c")
    p.add_argument("--noise-var", type=float, default=0.0)

    p = add("regression", c_regression, "RSE, R², adjusted R², F")
    p.add_argument("--rss", type=float, required=True)
    p.add_argument("--tss", type=float, required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--p", type=int, required=True)

    p = add("confusion", c_confusion, "rates from TP FP FN TN")
    for k in ("tp", "fp", "fn", "tn"):
        p.add_argument("--" + k, type=float, required=True)

    p = add("roc", c_roc, "ROC points and AUC")
    p.add_argument("--scores", required=True)
    p.add_argument("--labels", required=True, help="0/1")

    p = add("cv", c_cv, "cross-validation (folds | est | one-se | loocv-ols)")
    p.add_argument("op", choices=["folds", "est", "one-se", "loocv-ols"])
    p.add_argument("--n", type=int)
    p.add_argument("--k", type=int)
    p.add_argument("--errors")
    p.add_argument("--table", help="size:mean:se,size:mean:se,...")
    p.add_argument("--resid")
    p.add_argument("--leverage")

    p = add("criteria", c_criteria, "Cp, AIC, BIC (ISLR and ESL) and adjusted R²")
    p.add_argument("--rss", type=float, required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--d", type=int, required=True)
    p.add_argument("--sigma2", type=float, required=True)
    p.add_argument("--tss", type=float)

    p = add("node", c_node, "node or split impurity")
    p.set_defaults(op="node")
    p.add_argument("--counts")
    p.add_argument("--left")
    p.add_argument("--right")

    p = add("ttest", c_ttest, "t, p-value and CI of a coefficient")
    p.add_argument("--coef", type=float, required=True)
    p.add_argument("--se", type=float, required=True)
    p.add_argument("--df", type=float, required=True)

    p = add("ftest", c_ftest, "F for nested models")
    p.add_argument("--rss0", type=float, required=True)
    p.add_argument("--rss1", type=float, required=True)
    p.add_argument("--p0", type=int, required=True)
    p.add_argument("--p1", type=int, required=True)
    p.add_argument("--n", type=int, required=True)

    p = add("t2", c_t2, "two-sample t (ESL 18.38)")
    for k in ("mean1", "mean2", "sd1", "sd2"):
        p.add_argument("--" + k, type=float, required=True)
    p.add_argument("--n1", type=int, required=True)
    p.add_argument("--n2", type=int, required=True)

    p = add("multtest", c_multtest, "Bonferroni, FWER, BH, expected false positives, plug-in FDR")
    p.add_argument("op", choices=["bonferroni", "fwer", "expected-false", "bh", "fdr-plugin"])
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--m", type=int, default=1)
    p.add_argument("--pvalues")
    p.add_argument("--ev", type=float)
    p.add_argument("--robs", type=float)

    p = add("boot", c_boot, "bootstrap: prob-in | err632 | alpha | se")
    p.add_argument("op", choices=["prob-in", "err632", "alpha", "se"])
    p.add_argument("--n", type=int, default=100)
    p.add_argument("--err", type=float)
    p.add_argument("--err1", type=float)
    p.add_argument("--p1", type=float)
    p.add_argument("--q1", type=float)
    p.add_argument("--varx", type=float)
    p.add_argument("--vary", type=float)
    p.add_argument("--cov", type=float)
    p.add_argument("--values")

    p = add("knn", c_knn, "kNN: edge | median-dist | epe")
    p.add_argument("op", choices=["edge", "median-dist", "epe"])
    p.add_argument("--p", type=int)
    p.add_argument("--r", type=float)
    p.add_argument("--n", type=int)
    p.add_argument("--sigma2", type=float, default=1.0)
    p.add_argument("--fx0", type=float)
    p.add_argument("--neighbors")

    p = add("logistic", c_logistic, "prob | odds | from-odds")
    p.add_argument("op", choices=["prob", "odds", "from-odds"])
    p.add_argument("--b0", type=float, default=0.0)
    p.add_argument("--coefs", default="")
    p.add_argument("--x", default="")
    p.add_argument("--p", type=float)
    p.add_argument("--odds", type=float)

    p = add("lda1", c_lda1, "LDA with one predictor")
    p.add_argument("--mu", required=True)
    p.add_argument("--sigma2", type=float, required=True)
    p.add_argument("--pi")
    p.add_argument("--x", type=float, required=True)

    p = add("shrink", c_shrink, "ridge-ortho | lasso-ortho | ridge-df")
    p.add_argument("op", choices=["ridge-ortho", "lasso-ortho", "ridge-df"])
    p.add_argument("--beta", type=float, default=0.0)
    p.add_argument("--lam", type=float, required=True)
    p.add_argument("--convention", choices=["islr", "esl"], default="islr")
    p.add_argument("--d", default="")

    p = add("kernel", c_kernel, "linear | poly | radial | poly2-features | hinge")
    p.add_argument("op", choices=["linear", "poly", "radial", "poly2-features", "hinge"])
    p.add_argument("--x", default="")
    p.add_argument("--y", default="")
    p.add_argument("--d", type=int, default=2)
    p.add_argument("--gamma", type=float, default=1.0)
    p.add_argument("--f", type=float)

    p = add("pca", c_pca, "PVE from the component variances")
    p.add_argument("--variances", required=True)

    p = add("kmeans", c_kmeans, "objective | partitions")
    p.add_argument("op", choices=["objective", "partitions"])
    p.add_argument("--points", help='"x,y;x,y;..."')
    p.add_argument("--assign")
    p.add_argument("--n", type=int)
    p.add_argument("--k", type=int)

    p = add("counts", c_counts, "subsets | cov-params | spline-df")
    p.add_argument("op", choices=["subsets", "cov-params", "spline-df"])
    p.add_argument("--p", type=int, default=0)
    p.add_argument("--k", type=int, default=2)
    p.add_argument("--knots", type=int, default=0)

    p = add("ensemble", c_ensemble, "rf-variance | oob | adaboost | boost-update")
    p.add_argument("op", choices=["rf-variance", "oob", "adaboost", "boost-update"])
    p.add_argument("--rho", type=float, default=0.0)
    p.add_argument("--sigma2", type=float, default=1.0)
    p.add_argument("--B", type=int, default=100)
    p.add_argument("--n", type=int, default=100)
    p.add_argument("--err", type=float)
    p.add_argument("--lam", type=float, default=0.01)
    p.add_argument("--fb")
    p.add_argument("--resid")

    p = add("diag", c_diag, "vif | leverage")
    p.add_argument("op", choices=["vif", "leverage"])
    p.add_argument("--r2", type=float)
    p.add_argument("--vif", type=float)
    p.add_argument("--xs")

    p = add("slr", c_slr, "simple linear regression")
    p.add_argument("--x", required=True)
    p.add_argument("--y", required=True)
    return ap


def main():
    ap = build()
    a = ap.parse_args()
    if not getattr(a, "_run", None):
        ap.print_help()
        return 1
    if a.cmd == "node":
        a.op = "node" if a.counts else "split"
        if a.op == "split" and not (a.left and a.right):
            print("use --counts \"a,b\" or --left \"a,b\" --right \"c,d\"")
            return 2
    try:
        return a._run(a)
    except (ValueError, ZeroDivisionError, TypeError) as e:
        print("INPUT ERROR:", e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
