# -*- coding: utf-8 -*-
"""
quorum_calc.py - computes R + W against N (Dynamo/Voldemort-style replication).

Declared origin:
  [from source] STRAUCH p.45-46: N = replicas, R = machines read, W = machines that block on write;
             the read-your-own-writes model requires R + W > N. A failed write (fewer than W)
             leaves an unspecified state and must be reissued; W may be 0 (non-blocking write).
  [from source] STRAUCH p.61-62 (Dynamo): "quorum-like" requires R + W > N; many choose R + W < N for latency;
             R = 1 and W = N for an 'authoritative cache'; typical configuration N = 3, R = 2, W = 2.
  [inference] fault tolerance: a read tolerates N-R replicas down; a write tolerates N-W (arithmetic).
  [extrapolation] the level names ONE/TWO/THREE/QUORUM/ALL and QUORUM = floor(N/2)+1 (modern Cassandra) are NOT in the
             sources; they are only accepted as a shortcut and marked [extrapolation].
The script does NOT claim linearizable consistency: only the condition cited by the book.

Usage: python -I quorum_calc.py -N 3 -R 2 -W 2
       python -I quorum_calc.py -N 3 -R QUORUM -W ONE      (shortcuts [extrapolation])
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

NAMED = {"ONE": lambda n: 1, "TWO": lambda n: 2, "THREE": lambda n: 3,
         "QUORUM": lambda n: n // 2 + 1, "ALL": lambda n: n}


def parse_level(s, n):
    """Returns (value, used_shortcut)."""
    u = str(s).strip().upper()
    if u in NAMED:
        return NAMED[u](n), True
    if u.lstrip("-").isdigit():
        return int(u), False
    raise ValueError("invalid level: %r (use an integer or ONE/TWO/THREE/QUORUM/ALL)" % s)


def analyze(n, r, w):
    if n < 1:
        raise ValueError("N must be >= 1")
    if not (0 <= w <= n):
        raise ValueError("W must be between 0 and N (W=0 = non-blocking write, STRAUCH p.46 note 5)")
    if not (1 <= r <= n):
        raise ValueError("R must be between 1 and N")
    total = r + w
    return {
        "n": n, "r": r, "w": w, "sum": total,
        "overlap": total > n,
        "read_tolerates": n - r,
        "write_tolerates": n - w,
    }


def main():
    ap = argparse.ArgumentParser(description="R + W > N (STRAUCH p.45-46, 61-62)")
    ap.add_argument("-N", "--replication-factor", type=int, default=3)
    ap.add_argument("-R", "--read", default="2")
    ap.add_argument("-W", "--write", default="2")
    a = ap.parse_args()
    try:
        r, r_alias = parse_level(a.read, a.replication_factor)
        w, w_alias = parse_level(a.write, a.replication_factor)
        res = analyze(a.replication_factor, r, w)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    print("=" * 66)
    print("R + W against N [STRAUCH p.45-46, 61-62; p.N = PDF page]")
    print("=" * 66)
    print("N = %d | R = %d | W = %d" % (res["n"], res["r"], res["w"]))
    print("R + W = %d + %d = %d (N = %d)" % (res["r"], res["w"], res["sum"], res["n"]))
    if r_alias or w_alias:
        print("[extrapolation] shortcuts ONE/TWO/THREE/QUORUM/ALL and QUORUM = floor(N/2)+1 are not in the sources.")
    if res["overlap"]:
        print("R + W > N: condition the book cites for read-your-own-writes and for a 'quorum-like' system (STRAUCH p.46, 61).")
        print("  [inference] the read and write sets overlap by arithmetic; this does not imply linearizability.")
    else:
        print("R + W <= N: no guaranteed overlap; a read may hit replicas without the latest write (eventual consistency).")
        print("  Dynamo allows choosing R + W < N for latency (STRAUCH p.61).")
    if res["w"] == 0:
        print("W = 0: non-blocking write, no guarantee of success (STRAUCH p.46, note 5).")
    print("[inference] tolerates %d replica(s) down on read and %d on write (N-R, N-W)." % (res["read_tolerates"], res["write_tolerates"]))
    print("Examples from the book: N=3, R=2, W=2 (typical, STRAUCH p.62); R=1, W=N for 'authoritative cache' (p.62).")
    print("If a write fails (fewer than W acknowledgements), the state is unspecified: reissue (STRAUCH p.46).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
