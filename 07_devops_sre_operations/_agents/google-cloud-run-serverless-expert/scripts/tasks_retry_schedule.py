# -*- coding: utf-8 -*-
"""
Skill: tasks-retry-schedule
Computes the sequence of retry intervals of a Cloud Tasks queue according to the MODEL
DESCRIBED IN THE RUN BOOK (Venema, Dec/2020, RUN p.133-134, Figure 7-2):
  1) first interval = minBackoff;
  2) doubling phase: the interval doubles on each attempt, maxDoublings times;
  3) linear phase: the interval grows on each attempt by (2^maxDoublings + minBackoff)
     [formula as described in the book text, with the example 2^2 + 1 = 5];
  4) the interval never exceeds maxBackoff (it stays constant);
  5) attempts stop at maxAttempts (0 or "unlimited" = unlimited: shows only the first N).
[DATED] The real API formula may differ from the book text: check the current documentation.
The book example (minBackoff 1 s, maxDoublings 2, maxBackoff 15 s) yields 1, 2, 4, 9, 14, 15, 15...,
consistent with Figure 7-2 (labels 2, 4, 9, 14, 15 seen on PDF page 134).
Usage: python -I tasks_retry_schedule.py --min 1 --max 15 --doublings 2 --attempts 8 [--show 20]
Queue defaults shown in the book (RUN p.135): minBackoff 0.1 s, maxBackoff 3600 s, maxDoublings 16, maxAttempts 100.
Arithmetic only, no network.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def intervals(min_b, max_b, doublings, attempts, show):
    """Returns the list of intervals between attempts (the n-th interval precedes the (n+1)-th retry)."""
    n = show if attempts in (0, None) else min(show, max(attempts - 1, 0))
    out = []
    cur = float(min_b)
    inc = (2 ** doublings) + float(min_b)
    for i in range(n):
        if i == 0:
            cur = float(min_b)
        elif i <= doublings:
            cur = cur * 2
        else:
            cur = cur + inc
        out.append(min(cur, float(max_b)))
    return out


def fmt(x):
    return f"{x:g}"


def main():
    ap = argparse.ArgumentParser(description="Cloud Tasks retry sequence (RUN book model)")
    ap.add_argument("--min", type=float, default=0.1, help="minBackoff in s (demo default: 0.1)")
    ap.add_argument("--max", type=float, default=3600, help="maxBackoff in s (demo default: 3600)")
    ap.add_argument("--doublings", type=int, default=16, help="maxDoublings (demo default: 16)")
    ap.add_argument("--attempts", type=int, default=100, help="maxAttempts (0 = unlimited)")
    ap.add_argument("--show", type=int, default=20, help="maximum number of intervals shown")
    a = ap.parse_args()
    if a.min <= 0 or a.max < a.min or a.doublings < 0 or a.attempts < 0 or a.show < 1:
        print("INVALID PARAMETERS: require min > 0, max >= min, doublings >= 0, attempts >= 0, show >= 1", file=sys.stderr)
        return 2
    seq = intervals(a.min, a.max, a.doublings, a.attempts, a.show)
    total = 0.0
    print(f"minBackoff={fmt(a.min)}s maxBackoff={fmt(a.max)}s maxDoublings={a.doublings} maxAttempts={'unlimited' if a.attempts == 0 else a.attempts}")
    print(f"linear-phase increment (book model): 2^{a.doublings} + {fmt(a.min)} = {fmt((2 ** a.doublings) + a.min)}s")
    print("n | interval(s) | cumulative wait(s)")
    for i, v in enumerate(seq, 1):
        total += v
        print(f"{i} | {fmt(round(v, 6))} | {fmt(round(total, 6))}")
    if a.attempts and a.attempts - 1 > len(seq):
        print(f"... (showing {len(seq)} of {a.attempts - 1} possible intervals)")
    print("After maxAttempts is exhausted Cloud Tasks forgets the task (RUN p.134): record the state in a database or use unlimited with care.")
    print("[DATED] model per the book text; check the formula in the current Cloud Tasks documentation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
