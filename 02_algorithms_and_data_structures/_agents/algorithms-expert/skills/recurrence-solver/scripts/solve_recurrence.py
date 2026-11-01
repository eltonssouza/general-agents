# -*- coding: utf-8 -*-
"""
solve_recurrence.py - classifies divide-and-conquer recurrences using the RECURSION TREE METHOD.

Based on the book (Erickson, "Algorithms", 2019): T(n) = r T(n/c) + f(n); level i has r^i nodes of value f(n/c^i);
three cases (decreasing, equal, increasing) [from source] (JE p.49-52). Pages = PDF (printed = PDF - 18).
The book does NOT present the "Master Theorem" (index: "see recursion trees", JE p.454): this script does not call it that.

Modes:
  --a R --b C --k K [--p P]    T(n) = R*T(n/C) + Theta(n^K log^P n)      (a=r, b=c in the book's notation)
  --terms "al,co;al,co" --k K  T(n) = sum co*T(al*n) + Theta(n^K)        (subproblems of different sizes)
  --examples                   the book's recurrences with the page
Labels: the book uses O and f(n) without a logarithmic factor. The result with a log factor in f(n), the case p<=-1 and the case ρ>1
of --terms are [extrapolation] (usual generalizations, not from the book). No network; read-only.
"""
import argparse
import math
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

EPS = 1e-9


def fmt_pow(k):
    if abs(k - round(k)) < 1e-9:
        k = int(round(k))
        return "n" if k == 1 else ("1" if k == 0 else "n^%d" % k)
    return "n^%.5g" % k


def theta(k, logpow):
    base = fmt_pow(k)
    if abs(logpow) < EPS:
        return "Theta(%s)" % base
    lp = ("log n" if abs(logpow - 1) < EPS else "log^%.5g n" % logpow)
    return "Theta(%s)" % (lp if base == "1" else "%s %s" % (base, lp))


def solve_dc(r, c, k, p=0.0):
    if r < 1:
        raise ValueError("r (=a) must be >= 1")
    if c <= 1:
        raise ValueError("c (=b) must be > 1")
    if k < 0:
        raise ValueError("k must be >= 0")
    L = math.log(r, c)
    ratio = r / (c ** k)
    out = {"equation": "T(n) = %g T(n/%g) + Theta(%s%s)" % (r, c, fmt_pow(k), ("" if abs(p) < EPS else " log^%g n" % p)),
           "log_c_r": L, "ratio_per_level": ratio, "leaves": "n^%.5g" % L}
    if abs(k - L) < 1e-9:
        out["regime"] = "equal (all levels have the same value)"
        if p > -1 + EPS:
            out["result"] = theta(k, p + 1)
        elif abs(p + 1) < EPS:
            out["result"] = "Theta(%s log log n)" % fmt_pow(k)
        else:
            out["result"] = theta(k, 0)
        out["label"] = "[from source] (JE p.51): T(n)=O(f(n) log n)" + (
            "; with a log in f(n): [extrapolation]" if abs(p) > EPS else "")
        out["explanation"] = ("Each level sums to ~ n^%.5g; the result is (value of one level) x (number of levels = log_c n)." % k)
    elif k > L:
        out["regime"] = "decreasing (dominated by the root)"
        out["result"] = theta(k, p)
        out["label"] = "[from source] (JE p.51): T(n)=O(f(n))" + ("" if abs(p) < EPS else "; with a log in f(n): [extrapolation]")
        out["explanation"] = ("Ratio per level r/c^k = %.5g < 1: the series decays geometrically; this holds even for an infinite tree." % ratio)
    else:
        out["regime"] = "increasing (dominated by the leaves)"
        out["result"] = theta(L, 0)
        out["label"] = "[from source] (JE p.51): T(n)=O(n^(log_c r))"
        out["explanation"] = ("Ratio per level r/c^k = %.5g > 1: the series grows; the number of leaves n^(log_c r) dominates." % ratio)
    out["note"] = ("The book proves O(...) bounds; the Theta result holds when f(n) is Theta of the given value and the level constants"
                   " do not cancel [inference].")
    return out


def solve_terms(terms, k):
    """T(n) = sum co_i T(al_i n) + n^k. rho(x) = sum co_i al_i^x."""
    def rho(x):
        return sum(co * (al ** x) for al, co in terms)
    rk = rho(k)
    out = {"equation": "T(n) = " + " + ".join("%gT(%g n)" % (co, al) for al, co in terms) + " + Theta(%s)" % fmt_pow(k),
           "rho_k": rk}
    if rk < 1 - 1e-9:
        out["regime"] = "decreasing (dominated by the root): the total of each level is <= rho^i * f(n)"
        out["result"] = theta(k, 0)
        out["label"] = "[from source] (JE p.56, MomSelect: 1/5 + 7/10 = 9/10 < 1); (JE p.51)"
    elif abs(rk - 1) <= 1e-9:
        out["regime"] = "balanced: each level sums to ~ f(n), depth O(log n)"
        out["result"] = theta(k, 1)
        out["label"] = "[from source] (JE p.51-52, 57: T(n/3)+T(2n/3)+n = O(n log n), tight)"
    else:
        lo, hi = 0.0, max(k, 1.0)
        while rho(hi) > 1:
            hi *= 2
        lo = 0.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if rho(mid) > 1:
                lo = mid
            else:
                hi = mid
        out["regime"] = "increasing (dominated by the leaves)"
        out["result"] = theta((lo + hi) / 2, 0)
        out["label"] = "[extrapolation] (Akra-Bazzi type; the book does not solve this case)"
    return out


EXEMPLOS = [
    ("MergeSort  T(n)=2T(n/2)+n", dict(r=2, c=2, k=1), "JE p.46, 51"),
    ("Karatsuba  T(n)=3T(n/2)+n", dict(r=3, c=2, k=1), "JE p.59"),
    ("Naive multiplication  T(n)=4T(n/2)+n", dict(r=4, c=2, k=1), "JE p.58"),
    ("Pingala/exponentiation  T(n)=T(n/2)+O(1)", dict(r=1, c=2, k=0), "JE p.61"),
]
EXEMPLOS_TERMS = [
    ("MomSelect  T(n)=T(n/5)+T(7n/10)+n", [(0.2, 1), (0.7, 1)], 1, "JE p.56"),
    ("Blocks of 3  T(n)=T(n/3)+T(2n/3)+n", [(1 / 3, 1), (2 / 3, 1)], 1, "JE p.51, 57"),
]


def parse_terms(s):
    terms = []
    for part in s.split(";"):
        al, _, co = part.partition(",")
        def num(x):
            x = x.strip()
            if "/" in x:
                a, b = x.split("/")
                return float(a) / float(b)
            return float(x)
        terms.append((num(al), num(co) if co else 1.0))
    return terms


def show(out):
    print("Equation:          %s" % out["equation"])
    for key, lab in (("log_c_r", "log_c(r)"), ("ratio_per_level", "ratio per level"), ("rho_k", "rho(k)=sum co*al^k")):
        if key in out:
            print("%-18s %.6g" % (lab + ":", out[key]))
    print("Regime:            %s" % out["regime"])
    print("Solution:          %s" % out["result"])
    if "explanation" in out:
        print("Explanation:       %s" % out["explanation"])
    print("Origin/label:      %s" % out["label"])
    if "note" in out:
        print("Note:              %s" % out["note"])


def main():
    ap = argparse.ArgumentParser(description="Classifies divide-and-conquer recurrences (recursion tree).")
    ap.add_argument("--a", "--r", dest="a", type=float, help="r (=a): number of subproblems")
    ap.add_argument("--b", "--c", dest="b", type=float, help="c (=b): reduction factor")
    ap.add_argument("--k", type=float, default=1.0, help="polynomial exponent of f(n) (default 1)")
    ap.add_argument("--p", type=float, default=0.0, help="logarithmic exponent of f(n) (default 0) [extrapolation if != 0]")
    ap.add_argument("--terms", help='"alpha,coef;alpha,coef" for T(n)=sum coef*T(alpha n)+n^k (e.g. "1/5,1;7/10,1")')
    ap.add_argument("--examples", action="store_true")
    a = ap.parse_args()
    print("=== RECURRENCES BY RECURSION TREE (JE p.49-52; pages = PDF) ===")
    if a.examples:
        for nome, kw, pg in EXEMPLOS:
            print("\n# %s  (%s)" % (nome, pg))
            show(solve_dc(kw["r"], kw["c"], kw["k"]))
        for nome, terms, k, pg in EXEMPLOS_TERMS:
            print("\n# %s  (%s)" % (nome, pg))
            show(solve_terms(terms, k))
        return 0
    try:
        if a.terms:
            show(solve_terms(parse_terms(a.terms), a.k))
        elif a.a is not None and a.b is not None:
            show(solve_dc(a.a, a.b, a.k, a.p))
        else:
            ap.print_help()
            return 2
    except ValueError as e:
        print("Error: %s" % e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
