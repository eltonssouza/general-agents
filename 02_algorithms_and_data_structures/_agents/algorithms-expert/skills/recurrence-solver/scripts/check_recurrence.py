# -*- coding: utf-8 -*-
"""
check_recurrence.py - NUMERICAL VERIFIER of recurrences: evaluates T(n) exactly (integers, memoization) and compares it with the
closed form or with the growth order stated in the book (Erickson, "Algorithms", 2019; pages = PDF).

Use it to check an answer before stating it: if the ratio T(n)/g(n) does not stabilize or the exact equality fails,
the proposed closed form is wrong. It is NOT a proof (it only tests the requested n) [inference].

Usage:
  python -I check_recurrence.py --list
  python -I check_recurrence.py --preset hanoi --max 30
  python -I check_recurrence.py --all                      # runs all the book's recurrences (exit 1 if anything fails)
  python -I check_recurrence.py --div --r 3 --c 2 --k 1 --max 20 --claim "n^1.58496"
  python -I check_recurrence.py --lin --coef 1,1 --f 1 --base 1,1 --max 40   # T(n)=T(n-1)+T(n-2)+1, T(0)=T(1)=1
"""
import argparse
import math
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def cdiv(a, b):
    return -(-a // b)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# each preset: (description, page, T(n) function with memo, kind of check, parameters)
def make_presets():
    P = {}

    def hanoi():
        @lru_cache(None)
        def T(n):
            return 0 if n == 0 else 2 * T(n - 1) + 1
        return T
    P["hanoi"] = ("T(n)=2T(n-1)+1, T(0)=0 (Tower of Hanoi)", "JE p.44", hanoi, ("exato", lambda n: 2 ** n - 1), "n")

    def recfibo():
        @lru_cache(None)
        def T(n):
            return 1 if n <= 1 else T(n - 1) + T(n - 2) + 1
        return T
    P["recfibo-calls"] = ("T(n)=T(n-1)+T(n-2)+1, T(0)=T(1)=1 (RecFibo calls)", "JE p.117", recfibo,
                          ("exato", lambda n: 2 * fib(n + 1) - 1), "n")

    def mergesort():
        @lru_cache(None)
        def T(n):
            return 1 if n <= 1 else T(cdiv(n, 2)) + T(n // 2) + n
        return T
    P["mergesort"] = ("T(n)=T(ceil(n/2))+T(floor(n/2))+n (MergeSort)", "JE p.46, 51", mergesort,
                      ("razao", lambda n: n * math.log2(n) if n > 1 else 1, 0.5, 3.0), "pot2")

    def qs_worst():
        @lru_cache(None)
        def T(n):
            return 0 if n <= 1 else T(n - 1) + n
        return T
    P["quicksort-pior"] = ("T(n)=T(n-1)+n (QuickSort, pivot always extreme)", "JE p.48, 52", qs_worst,
                           ("exato", lambda n: n * (n + 1) // 2 - 1 if n >= 1 else 0), "n")

    def karatsuba():
        @lru_cache(None)
        def T(n):
            return 1 if n <= 1 else 3 * T(cdiv(n, 2)) + n
        return T
    P["karatsuba"] = ("T(n)=3T(ceil(n/2))+n (Karatsuba)", "JE p.59", karatsuba,
                      ("razao", lambda n: n ** math.log2(3), 0.5, 8.0), "pot2")

    def naive_mult():
        @lru_cache(None)
        def T(n):
            return 1 if n <= 1 else 4 * T(cdiv(n, 2)) + n
        return T
    P["multiplicacao-ingenua"] = ("T(n)=4T(ceil(n/2))+n (naive multiplication)", "JE p.58", naive_mult,
                                  ("razao", lambda n: float(n * n), 0.5, 4.0), "pot2")

    def mom():
        @lru_cache(None)
        def T(n):
            if n <= 25:
                return n * 8 // 5 + 1  # arbitrary base case (book: "or whatever", JE p.55)
            return T(cdiv(n, 5)) + T(7 * n // 10) + (8 * n) // 5
        return T
    P["momselect"] = ("T(n)=T(n/5)+T(7n/10)+8n/5 (MomSelect comparisons; book bound: 16n)", "JE p.56-57", mom,
                      ("teto", lambda n: 16 * n), "n")

    def mom3():
        @lru_cache(None)
        def T(n):
            return 1 if n <= 1 else T(cdiv(n, 3)) + T(2 * n // 3) + n
        return T
    P["blocos-de-3"] = ("T(n)=T(n/3)+T(2n/3)+n (selection with blocks of 3)", "JE p.57", mom3,
                        ("razao", lambda n: n * math.log2(n) if n > 1 else 1, 0.3, 4.0), "geom")

    def subset():
        @lru_cache(None)
        def T(n):
            return 1 if n == 0 else 2 * T(n - 1) + 1
        return T
    P["subset-sum-backtracking"] = ("T(n)=2T(n-1)+1 (Subset Sum by backtracking)", "JE p.96", subset,
                                    ("razao", lambda n: float(2 ** n), 0.99, 2.01), "n")

    def split_full():
        @lru_cache(None)
        def T(n):
            return 1 if n == 0 else sum(T(i) for i in range(n)) + n
        return T
    P["splittable-historia-completa"] = ("T(n)=sum_{i<n} T(i)+n (Splittable, full history)", "JE p.102-103", split_full,
                                         ("razao", lambda n: float(2 ** n), 0.5, 3.0), "n")

    def optbst():
        @lru_cache(None)
        def T(n):
            return 1 if n == 0 else sum(T(k - 1) + T(n - k) for k in range(1, n + 1)) + n
        return T
    P["bst-otima-backtracking"] = ("T(n)=sum_k (T(k-1)+T(n-k)) + n (optimal BST by backtracking)", "JE p.110-111", optbst,
                                   ("razao", lambda n: float(3 ** n), 0.3, 3.0), "n")

    def pingala():
        @lru_cache(None)
        def T(n):
            return 0 if n <= 1 else T(n // 2) + 2
        return T
    P["pingala-potencia"] = ("T(n)=T(floor(n/2))+2 (multiplications of PingalaPower)", "JE p.61", pingala,
                             ("teto", lambda n: 2 * math.log2(n) if n > 1 else 0), "n")
    return P


PRESETS = make_presets()


def sample_points(kind, mx):
    if kind == "pot2":
        return [2 ** j for j in range(2, mx + 1)]
    if kind == "geom":
        return [int(round(1.5 ** j)) for j in range(6, mx + 1) if int(round(1.5 ** j)) > 1]
    return list(range(max(2, mx // 8), mx + 1, max(1, mx // 8)))


def run_preset(name, mx, verbose=True):
    desc, pag, mk, chk, kind = PRESETS[name]
    T = mk()
    pts = sample_points(kind, mx)
    ok = True
    if verbose:
        print("\n[%s] %s  (%s)" % (name, desc, pag))
    for n in pts:
        v = T(n)
        if chk[0] == "exato":
            expected = chk[1](n)
            good = (v == expected)
            if verbose:
                print("  n=%-6d T(n)=%-22d expected=%-22d %s" % (n, v, expected, "OK" if good else "FAIL"))
        elif chk[0] == "teto":
            bound = chk[1](n)
            good = v <= bound + 1e-9
            if verbose:
                print("  n=%-6d T(n)=%-10d ceiling=%-12.6g %s" % (n, v, bound, "OK" if good else "FAIL"))
        else:
            g = chk[1](n)
            ratio = v / g
            good = chk[2] <= ratio <= chk[3]
            if verbose:
                print("  n=%-6d T(n)=%-14d g(n)=%-14.6g T/g=%-9.5f %s" % (n, v, g, ratio, "OK" if good else "FAIL"))
        ok = ok and good
    return ok


def run_div(r, c, k, mx, claim_exp):
    @lru_cache(None)
    def T(n):
        return 1 if n <= 1 else r * T(cdiv(n, c)) + int(round(n ** k))
    L = math.log(r, c)
    exp = claim_exp if claim_exp is not None else (k if k > L + 1e-9 else L)
    logk = 1 if abs(k - L) < 1e-9 else 0
    print("\n[custom division] T(n)=%d*T(ceil(n/%d))+n^%g, T(1)=1; claim: Theta(n^%.5g%s)" %
          (r, c, k, exp, " log n" if (claim_exp is None and logk) else ""))
    prev = None
    ok = True
    for j in range(3, mx + 1):
        n = c ** j
        g = (n ** exp) * (math.log(n, c) if (claim_exp is None and logk) else 1.0)
        ratio = T(n) / g
        drift = "" if prev is None else "  (change %+.2f%%)" % (100 * (ratio - prev) / prev)
        print("  n=%-12d T(n)=%-22d T/g=%.5f%s" % (n, T(n), ratio, drift))
        prev = ratio
    if prev is not None and (prev <= 0 or prev > 1e6):
        ok = False
    print("  Reading: if T/g stabilizes (change -> 0) the stated order is plausible; if it keeps growing/decaying, it is wrong.")
    return ok


def run_lin(coef, f_exp, base, mx):
    m = len(coef)
    T = list(base) + [0] * (mx + 1)

    def ff(n):
        return int(round(n ** f_exp)) if f_exp else 1
    for n in range(m, mx + 1):
        T[n] = sum(coef[i] * T[n - 1 - i] for i in range(m)) + ff(n)
    print("\n[custom linear] T(n)=%s + n^%g; base=%s" %
          (" + ".join("%dT(n-%d)" % (coef[i], i + 1) for i in range(m)), f_exp, list(base)))
    for n in range(max(m, mx - 5), mx + 1):
        print("  n=%-4d T(n)=%d  T(n)/T(n-1)=%.6f" % (n, T[n], T[n] / T[n - 1]))
    print("  Reading: the ratio T(n)/T(n-1) converges to the largest root of the characteristic equation "
          "(e.g. 2 for T=2T(n-1)+1; 1.618... for Fibonacci) [inference].")
    return True


def main():
    ap = argparse.ArgumentParser(description="Numerical verifier of recurrences from the book (or your own).")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--preset")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--max", type=int, default=20, help="largest n (or 2^max / exponent depending on the preset)")
    ap.add_argument("--div", action="store_true", help="T(n)=r T(ceil(n/c)) + n^k")
    ap.add_argument("--r", type=int, default=2)
    ap.add_argument("--c", type=int, default=2)
    ap.add_argument("--k", type=float, default=1.0)
    ap.add_argument("--claim", help='claimed exponent, e.g. "1.58496" (omitted: uses the recursion tree method\'s)')
    ap.add_argument("--lin", action="store_true", help="T(n)=sum coef_i T(n-i)+n^f")
    ap.add_argument("--coef", default="2")
    ap.add_argument("--f", type=float, default=0.0)
    ap.add_argument("--base", default="0")
    a = ap.parse_args()
    if a.list:
        for k, v in PRESETS.items():
            print("%-30s %s  (%s)" % (k, v[0], v[1]))
        return 0
    if a.all:
        fails = []
        for name, v in PRESETS.items():
            mx = {"pot2": 14, "geom": 24, "n": 24}[v[4]]
            if v[4] == "n" and name in ("momselect", "pingala-potencia", "quicksort-pior"):
                mx = 2000
            if not run_preset(name, mx, verbose=False):
                fails.append(name)
        print("Summary: %d recurrences, %d failures%s" % (len(PRESETS), len(fails), (": " + ", ".join(fails)) if fails else ""))
        return 1 if fails else 0
    if a.preset:
        if a.preset not in PRESETS:
            print("Unknown preset. Use --list.")
            return 2
        ok = run_preset(a.preset, a.max)
        return 0 if ok else 1
    if a.div:
        claim = float(a.claim) if a.claim else None
        return 0 if run_div(a.r, a.c, a.k, a.max, claim) else 1
    if a.lin:
        coef = [int(x) for x in a.coef.split(",")]
        base = [int(x) for x in a.base.split(",")]
        if len(base) < len(coef):
            base = base + [base[-1]] * (len(coef) - len(base))
        return 0 if run_lin(coef, a.f, base, a.max) else 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
