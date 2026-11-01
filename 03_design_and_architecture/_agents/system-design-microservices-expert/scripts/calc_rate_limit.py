#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calc_rate_limit.py - deterministic simulators: token bucket, exponential backoff (with optional jitter), and circuit breaker.

ORIGIN AND LABELS (the numbers below are EXAMPLE parameters; none is a universal limit):
  Token bucket .... [extrapolation] The corpus only LISTS the algorithm (SDH p.14: "allows bursts within the average limit").
                    The simulation (bucket with capacity and constant refill) is general knowledge. Code 429 for
                    excess: NGINX example in APIGW p.23 (limit_req_status 429; the NGINX default is 503).
                    X-RateLimit-* and Retry-After headers are NOT in the corpus and are not emitted.
  Backoff ......... [from source] retry with exponential wait: example of 6 attempts with 2^n seconds (MS-MIC p.317, p.320) and
                    of 4 attempts starting at 2 s and doubling (MS-CLD p.125-126). --jitter none reproduces that format.
                    Jitter is recommended (MS-MIC p.320-321, which uses Polly's DecorrelatedJitterBackoffV2).
                    [extrapolation] --jitter full = uniform(0, ceiling) and --jitter decorrelated (approximation) are not corpus formulas.
  Circuit breaker . [from source] opens after N failures, fails fast during a window, and then lets a trial call through:
                    MS-MIC p.322 (5 consecutive failures, 30 s) and MS-CLD p.126-127 (100 failures, 30 s CheckCircuit).
                    [extrapolation] the names CLOSED/OPEN/TRIAL (Closed/Open/Half-Open) are terminology external to the corpus.

Usage (Python 3, stdlib only):
  python -I scripts/calc_rate_limit.py --token-bucket 100 20 150
  python -I scripts/calc_rate_limit.py --backoff 2000 0 4                 # base_ms cap_ms(0=no cap) attempts
  python -I scripts/calc_rate_limit.py --backoff 100 2000 6 --jitter full --seed 7
  python -I scripts/calc_rate_limit.py --circuit-breaker "S S F F F F F S S" --threshold 5 --open-seconds 30 --interval 10
Exit: 0 success; 1 invalid parameter; 2 nothing requested.
"""
import argparse
import random
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def token_bucket(capacity, refill_per_s, burst):
    if capacity <= 0 or refill_per_s <= 0 or burst < 0:
        print("Error: capacity and refill must be > 0 and the burst >= 0.")
        return 1
    print("=== Token bucket [extrapolation; SDH p.14 only lists the algorithm] ===")
    print(f" capacity={capacity} tokens, refill={refill_per_s} tokens/s, burst at t=0: {burst} requests")
    accepted = min(capacity, burst)
    rejected = burst - accepted
    print(f" accepted: {accepted} | rejected (HTTP 429 in the NGINX example, APIGW p.23): {rejected} | tokens left: {capacity - accepted}")
    if rejected:
        print(f" refilling {rejected} tokens takes {rejected / refill_per_s:.2f} s at the refill rate")
    print(f" sustained mean throughput: {refill_per_s} req/s; maximum instantaneous burst: {capacity} requests")
    return 0


def backoff(base_ms, cap_ms, retries, jitter, seed):
    if base_ms <= 0 or retries <= 0 or cap_ms < 0:
        print("Error: base_ms > 0, attempts > 0, and cap >= 0 (0 = no cap).")
        return 1
    rng = random.Random(seed)
    print(f"=== Exponential backoff, jitter={jitter} ===")
    print(" [from source] without jitter: wait = base * 2^(n-1) (MS-MIC p.317/p.320; MS-CLD p.125-126). "
          "[extrapolation] full/decorrelated here are general approximations.")
    print(f" base={base_ms} ms, cap={'no cap' if cap_ms == 0 else str(cap_ms) + ' ms'}, attempts={retries}, seed={seed}")
    print(f" {'attempt':>9} | {'cap_n (ms)':>12} | {'wait (ms)':>12} | {'cumulative (ms)':>14}")
    total = 0.0
    prev = float(base_ms)
    for n in range(1, retries + 1):
        ceiling = base_ms * (2 ** (n - 1))
        if cap_ms:
            ceiling = min(cap_ms, ceiling)
        if jitter == "none":
            wait = float(ceiling)
        elif jitter == "full":
            wait = rng.uniform(0, ceiling)
        else:  # decorrelated (approximation): uniform(base, prev*3) limited to the cap
            hi = prev * 3
            wait = rng.uniform(base_ms, hi)
            if cap_ms:
                wait = min(cap_ms, wait)
            prev = wait
        total += wait
        print(f" {n:>9} | {ceiling:>12.1f} | {wait:>12.1f} | {total:>14.1f}")
    print(f" total cumulative wait: {total:.1f} ms ({total / 1000.0:.2f} s)")
    return 0


def circuit_breaker(seq, threshold, open_seconds, interval):
    calls = [x.upper() for x in seq.split() if x]
    if not calls or any(c not in ("S", "F") for c in calls):
        print("Error: use a sequence of 'S' (success) and 'F' (failure) separated by spaces.")
        return 1
    if threshold < 1 or open_seconds < 0 or interval <= 0:
        print("Error: --threshold >= 1, --open-seconds >= 0, --interval > 0.")
        return 1
    print("=== Circuit breaker [from source: behavior, MS-MIC p.322; MS-CLD p.126-127] ===")
    print(f" opens after {threshold} consecutive failures; stays open {open_seconds} s; one call every {interval} s")
    print(" States: CLOSED (normal), OPEN (fail fast), TRIAL (one trial call) [extrapolation: names Closed/Open/Half-Open]")
    state = "CLOSED"
    fails = 0
    opened_at = None
    t = 0.0
    print(f" {'#':>3} {'t(s)':>6} {'result':>9} {'state before':>13} -> {'after':<8} action")
    for i, c in enumerate(calls, 1):
        before = state
        action = "execute"
        if state == "OPEN":
            if t - opened_at >= open_seconds:
                state = "TRIAL"
                action = "window expired: lets a trial call through"
            else:
                action = "fail fast (call is not sent)"
                print(f" {i:>3} {t:>6.1f} {'--':>9} {before:>13} -> {state:<8} {action}")
                t += interval
                continue
        if c == "F":
            if state == "TRIAL":
                state = "OPEN"
                opened_at = t
                action = "trial failed: reopens"
            else:
                fails += 1
                if fails >= threshold:
                    state = "OPEN"
                    opened_at = t
                    action = f"{fails} consecutive failures: opens"
        else:
            fails = 0
            if state == "TRIAL":
                state = "CLOSED"
                action = "trial succeeded: closes"
        print(f" {i:>3} {t:>6.1f} {c:>9} {before:>13} -> {state:<8} {action}")
        t += interval
    return 0


def main():
    ap = argparse.ArgumentParser(description="Simulators with a declared origin (see docstring).")
    ap.add_argument("--token-bucket", nargs=3, type=float, metavar=("CAPACITY", "REFILL_PER_S", "BURST"))
    ap.add_argument("--backoff", nargs=3, type=int, metavar=("BASE_MS", "CAP_MS", "ATTEMPTS"))
    ap.add_argument("--jitter", choices=["none", "full", "decorrelated"], default="none")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--circuit-breaker", help="sequence 'S S F F ...'")
    ap.add_argument("--threshold", type=int, default=5, help="consecutive failures to open (MS-MIC p.322 example: 5)")
    ap.add_argument("--open-seconds", type=float, default=30.0, help="open window (MS-MIC p.322 and MS-CLD p.127 example: 30 s)")
    ap.add_argument("--interval", type=float, default=1.0, help="simulated seconds between calls")
    a = ap.parse_args()
    done = False
    rc = 0
    if a.token_bucket:
        cap, refill, burst = a.token_bucket
        rc |= token_bucket(int(cap), refill, int(burst))
        done = True
    if a.backoff:
        rc |= backoff(a.backoff[0], a.backoff[1], a.backoff[2], a.jitter, a.seed)
        done = True
    if a.circuit_breaker:
        rc |= circuit_breaker(a.circuit_breaker, a.threshold, a.open_seconds, a.interval)
        done = True
    if not done:
        ap.print_help()
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())
