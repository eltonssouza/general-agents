#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_tradeoffs.py - availability math, Little's Law, latency tail, and PACELC labels.

ORIGIN OF EACH RULE (this script encodes nothing without declaring its origin):
  [from source]   Availability = Uptime/(Uptime+Downtime) and the table of "nines" (99% = 3.65 days/year ... 99.9999% = 31.5 s)
                  come from SDH p.7 (the table is an image on the page). Qualitative example "50 dependencies at 99.99% yield
                  several hours of downtime per month": MS-MIC p.308.
  [extrapolation] Series composition (product) and parallel composition (1 - prod(1-Ai)), MTBF/MTTR, Little's Law (L = lambda*W) and
                  tail amplification 1 - p^N are general math; they are NOT in the corpus. The assumption that failures are
                  independent rarely holds in practice.
  [extrapolation] PACELC: the corpus only mentions the name (MS-CLD p.107). Only the general definition of each class is printed here;
                  products are NOT classified (it varies with configuration; consult the product documentation).

Usage (Python 3, stdlib only):
  python -I scripts/analyze_tradeoffs.py --tiers
  python -I scripts/analyze_tradeoffs.py --availability 0.999 0.999 0.995 --redundancy 0.99 0.99
  python -I scripts/analyze_tradeoffs.py --compound 50 0.9999
  python -I scripts/analyze_tradeoffs.py --throughput 5000 --latency-ms 200
  python -I scripts/analyze_tradeoffs.py --tail-services 10 --percentile 0.99
  python -I scripts/analyze_tradeoffs.py --pacelc PC/EC
Availability values can be fractions (0.999) or percentages (99.9); numbers > 1 are read as percentages.
Exit 0 success; 1 usage/value error; 2 nothing requested.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SECONDS_PER_YEAR = 365 * 86400
SECONDS_PER_MONTH_30D = 30 * 86400

# SDH p.7 (image): downtime per year per tier
SDH_TIERS = [(0.99, "3.65 days", "two nines"), (0.999, "8.76 hours", "three nines"), (0.9999, "52.56 minutes", "four nines"),
             (0.99999, "5.26 minutes", "five nines"), (0.999999, "31.5 seconds", "six nines")]

PACELC = {
    "PC/EC": "during a partition, favors Consistency; without a partition, favors Consistency (accepts more latency)",
    "PA/EL": "during a partition, favors Availability; without a partition, favors Latency (accepts weaker consistency)",
    "PC/EL": "during a partition, favors Consistency; without a partition, favors Latency",
    "PA/EC": "during a partition, favors Availability; without a partition, favors Consistency",
}


def to_frac(x):
    v = float(x)
    if v > 1.0:
        v = v / 100.0
    if not (0.0 < v <= 1.0):
        raise ValueError(f"invalid availability: {x}")
    return v


def downtime_str(avail, seconds_base=SECONDS_PER_YEAR, unit="year"):
    if avail >= 1.0:
        return f"0 seconds per {unit}"
    secs = (1.0 - avail) * seconds_base
    d = int(secs // 86400)
    h = int((secs % 86400) // 3600)
    m = int((secs % 3600) // 60)
    s = secs % 60
    return f"{d}d {h}h {m}m {s:.1f}s per {unit} ({secs / 3600:.2f} h)"


def cmd_tiers():
    print("=== Table of 'nines' [from source] SDH p.7 (image) checked against the formula ===")
    for a, book, name in SDH_TIERS:
        print(f" {a * 100:9.4f}%  book: {book:14}  computed: {downtime_str(a)}  ({name})")


def cmd_series_parallel(avail, redundancy):
    svc = [to_frac(a) for a in avail] if avail else [0.999]
    print("=== Composite availability [extrapolation] (independence assumed) ===")
    ser = 1.0
    for i, a in enumerate(svc, 1):
        print(f" - service {i}: {a * 100:.4f}%")
        ser *= a
    print(f" Series (product): {ser * 100:.5f}%  -> {downtime_str(ser)}")
    if redundancy:
        un = 1.0
        for r in redundancy:
            un *= (1.0 - to_frac(r))
        par = 1.0 - un
        print(f" Redundant parallel group ({len(redundancy)} instances): {par * 100:.6f}%")
        total = ser * par
        print(f" Series x redundant group: {total * 100:.6f}%  -> {downtime_str(total)}")
    print(" Warning: correlated failures (same datacenter, same version, same dependency) make this optimistic.")


def cmd_compound(n, each):
    a = to_frac(each)
    tot = a ** n
    print(f"=== {n} dependencies in series at {a * 100:.4f}% each [extrapolation] ===")
    print(f" Total availability: {tot * 100:.4f}%")
    print(f" Downtime: {downtime_str(tot, SECONDS_PER_MONTH_30D, '30-day month')}")
    print(" [from source] MS-MIC p.308: 50 dependencies at 99.99% yield several hours of downtime per month (the calculation above agrees).")


def cmd_little(thr, lat_ms, conc):
    print("=== Little's Law L = lambda * W [extrapolation; not in the corpus] ===")
    if thr is not None and lat_ms is not None:
        print(f" lambda={thr} req/s, W={lat_ms} ms -> L = {thr * lat_ms / 1000.0:.2f} requests in flight (on average)")
    elif conc is not None and lat_ms is not None:
        print(f" L={conc}, W={lat_ms} ms -> max lambda = {conc / (lat_ms / 1000.0):.2f} req/s")
    elif conc is not None and thr is not None:
        print(f" L={conc}, lambda={thr} req/s -> max mean W = {conc / thr * 1000.0:.2f} ms")
    else:
        print("Error: provide two of --throughput, --latency-ms, and --concurrency.")
        return 1
    print(" Steady state and averages; peaks and queues need headroom.")
    return 0


def cmd_tail(n, p):
    if not (0.0 < p < 1.0) or n < 1:
        print("Error: --percentile in (0,1) and --tail-services >= 1.")
        return 1
    all_fast = p ** n
    print("=== Tail latency amplification [extrapolation; not in the corpus] ===")
    print(f" Each call is fast with prob. {p * 100:.2f}%; N={n} independent calls")
    print(f" P(all fast) = {all_fast * 100:.2f}%  |  P(at least one slow) = {(1 - all_fast) * 100:.2f}%")
    print(" [from source] only the qualitative effect: more synchronous dependencies worsen response time (MS-MIC p.65).")
    return 0


def cmd_pacelc(code):
    c = code.upper().strip()
    print("=== PACELC [extrapolation] (the corpus only mentions the name: MS-CLD p.107) ===")
    if c not in PACELC:
        print(f"Unknown code '{code}'. Valid: {', '.join(PACELC)}")
        return 1
    print(f" {c}: {PACELC[c]}")
    print(" Classification of specific products: NOT COVERED in the corpus and configuration-dependent; consult the documentation.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Quantitative analyses labeled by origin.")
    ap.add_argument("--tiers", action="store_true", help="table of nines (SDH p.7) vs. computation")
    ap.add_argument("--availability", nargs="+", help="availabilities of services in series")
    ap.add_argument("--redundancy", nargs="+", help="redundant instances in parallel (single group)")
    ap.add_argument("--compound", nargs=2, metavar=("N", "AVAILABILITY"), help="N identical dependencies in series")
    ap.add_argument("--throughput", type=float)
    ap.add_argument("--latency-ms", type=float)
    ap.add_argument("--concurrency", type=float)
    ap.add_argument("--tail-services", type=int)
    ap.add_argument("--percentile", type=float, default=0.99)
    ap.add_argument("--pacelc")
    a = ap.parse_args()
    done = False
    rc = 0
    try:
        if a.tiers:
            cmd_tiers()
            done = True
        if a.availability or a.redundancy:
            cmd_series_parallel(a.availability, a.redundancy)
            done = True
        if a.compound:
            cmd_compound(int(a.compound[0]), a.compound[1])
            done = True
        if a.throughput is not None or a.latency_ms is not None or a.concurrency is not None:
            rc |= cmd_little(a.throughput, a.latency_ms, a.concurrency)
            done = True
        if a.tail_services:
            rc |= cmd_tail(a.tail_services, a.percentile)
            done = True
        if a.pacelc:
            rc |= cmd_pacelc(a.pacelc)
            done = True
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    if not done:
        ap.print_help()
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())
