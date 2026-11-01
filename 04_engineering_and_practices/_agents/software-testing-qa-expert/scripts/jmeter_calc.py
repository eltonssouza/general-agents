# -*- coding: utf-8 -*-
"""
jmeter_calc.py - supporting arithmetic for planning a JMeter Thread Group.

ORIGIN OF THE RULES AND CALCULATIONS (read before using the result):
  [from source] JMETER (JMeter Tutorial 2.11, PDF p.15): the Thread Group has a number of threads, ramp-up period
             (time to start all threads), loop count and error behavior.
  [from source] JMETER p.29-30: the Duration Assertion fails the sample above a limit in ms (examples 100 ms and 2000 ms);
             the limit here comes from YOUR --sla value, not from the book.
  [from source] JMETER p.50: non-GUI execution `jmeter -n -t plano.jmx -l resultado.jtl`; few listeners.
  [inference] threads/ramp-up = start rate; threads x loops = total requests; it is only arithmetic on p.15.
  [extrapolation] Little's Law (N = X x R; in a closed system with think time Z: X = N / (R + Z), N = X x (R + Z)).
                 It is NOT in JMETER. The latency (--latency) is a value that YOU supply; the script does not predict
                 percentiles (p90/p95/p99) or behavior under load.
  [extrapolation][DATED] `-e -o` (HTML dashboard) exists in versions later than the PDF's 2.11; check the current documentation.
Read-only, no network.

Usage:
  python -I jmeter_calc.py --threads 100 --ramp-up 20 --loops 10 --latency 80 --think-time 500 --sla 200
  python -I jmeter_calc.py --target-tps 250 --latency 800 --think-time 1200     (sizes threads, Little)
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


def plan_from_threads(threads, ramp_up_s, loops, latency_ms, think_ms, sla_ms):
    cycle_ms = latency_ms + think_ms
    res = {
        "inputs": {"threads": threads, "ramp_up_s": ramp_up_s, "loops": loops,
                   "latency_ms": latency_ms, "think_time_ms": think_ms, "sla_ms": sla_ms},
        "from_book": {
            "thread_group_fields": "threads, ramp-up, loop count, error (JMETER p.15)",
            "duration_assertion": "limit in ms per sample, mechanics on p.29-30; limit = your --sla",
            "non_gui_command": "jmeter -n -t plano.jmx -l resultado.jtl (JMETER p.50)",
        },
        "inference": {
            "start_rate_threads_per_s": round(threads / ramp_up_s, 3) if ramp_up_s > 0 else None,
            "total_requests": threads * loops if loops > 0 else "infinite (endless loop)",
        },
        "extrapolation": {},
        "notes": [],
    }
    if cycle_ms > 0:
        x = threads / (cycle_ms / 1000.0)
        res["extrapolation"]["steady_state_throughput_rps"] = round(x, 2)
        res["extrapolation"]["formula"] = "X = N / (R + Z) (Little, closed system) [extrapolation]; holds in steady state, after the ramp-up"
        if loops > 0 and threads > 0:
            res["extrapolation"]["min_duration_s_estimate"] = round(ramp_up_s + loops * cycle_ms / 1000.0, 2)
    else:
        res["notes"].append("latency + think time = 0: throughput depends only on the server and generator capacity; the formula does not apply.")
    if sla_ms is not None:
        res["sla_check"] = {"declared_latency_ms": latency_ms, "sla_ms": sla_ms,
                            "within_sla": latency_ms <= sla_ms,
                            "note": "compares two numbers you supplied; it is neither a measurement nor a prediction"}
    res["notes"].append("Percentiles are not estimated here: without measurement there is no basis in the book or in the theory used.")
    res["notes"].append("The load generator also has CPU/memory limits; validate the machine before trusting the generated load [extrapolation].")
    return res


def plan_from_tps(target_tps, latency_ms, think_ms, ramp_up_s):
    cycle_s = (latency_ms + think_ms) / 1000.0
    n = target_tps * cycle_s
    threads = max(1, math.ceil(n))
    return {
        "inputs": {"target_tps": target_tps, "latency_ms": latency_ms, "think_time_ms": think_ms, "ramp_up_s": ramp_up_s},
        "extrapolation": {
            "formula": "N = X x (R + Z) (Little, closed system) [extrapolation]; NOT in JMETER",
            "threads_exact": round(n, 3),
            "threads_rounded_up": threads,
        },
        "inference": {"start_rate_threads_per_s": round(threads / ramp_up_s, 3) if ramp_up_s > 0 else None},
        "notes": ["Use the measured latency (R) of the real system; with a higher R under load, more threads are needed for the same X.",
                  "In an open model (arrivals by rate), the Constant Throughput Timer/Throughput Shaping is another approach [extrapolation]."],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threads", type=int)
    ap.add_argument("--ramp-up", type=float, default=20.0, help="seconds")
    ap.add_argument("--loops", type=int, default=10, help="0 = infinite")
    ap.add_argument("--latency", type=float, default=80.0, help="average response time you supply, in ms (R)")
    ap.add_argument("--think-time", type=float, default=500.0, help="pause between requests, in ms (Z)")
    ap.add_argument("--sla", type=float, help="limit for the Duration Assertion, in ms")
    ap.add_argument("--target-tps", type=float, help="target throughput; computes the number of threads (Little)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    for name in ("latency", "think_time", "ramp_up"):
        if getattr(a, name) < 0:
            ap.error("--%s cannot be negative" % name.replace("_", "-"))
    if a.target_tps is not None:
        if a.target_tps <= 0:
            ap.error("--target-tps must be positive")
        res = plan_from_tps(a.target_tps, a.latency, a.think_time, a.ramp_up)
    else:
        threads = a.threads if a.threads is not None else 100
        if threads <= 0:
            ap.error("--threads must be positive")
        res = plan_from_threads(threads, a.ramp_up, a.loops, a.latency, a.think_time, a.sla)
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
    print("=== Thread Group planning support (JMeter) ===")
    for sec in ("from_book", "inference", "extrapolation"):
        if res.get(sec):
            rot = {"from_book": "[from source]", "inference": "[inference]", "extrapolation": "[extrapolation]"}[sec]
            print("\n%s" % rot)
            for k, v in res[sec].items():
                print("  %s: %s" % (k, v))
    if "sla_check" in res:
        c = res["sla_check"]
        print("\nSLA (supplied values): R=%s ms, limit=%s ms -> %s" % (c["declared_latency_ms"], c["sla_ms"], "within" if c["within_sla"] else "above"))
        print("  Suggested Duration Assertion: %s ms per sample (mechanics: JMETER p.29-30)" % c["sla_ms"])
    for n in res["notes"]:
        print("Note: %s" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
