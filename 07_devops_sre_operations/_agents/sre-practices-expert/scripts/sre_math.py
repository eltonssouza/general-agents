# -*- coding: utf-8 -*-
"""
sre_math.py - operational arithmetic that the Google SRE Book (2016) does explicitly.
Pages = PDF (printed = N-12). Nothing here is an "invented" formula: each subcommand cites the page
of the book's example and labels what is [inference].

Subcommands:
  provision   size tasks: ceil(peak / capacity per task) + redundancy              (SRE p.35)
  toil-floor  toil floor from the on-call rotation                                 (SRE p.52)
  retry-amp   retry amplification across layers and budgets                        (SRE p.179, p.192)
  oncall      on-call limits (25%, 8 or 6 people, 2 incidents per shift)           (SRE p.100-101; p.331)
  bimodal     busy threads when part of the requests never completes               (SRE p.193-194)
  quorum      consensus replicas: majority 2f+1, % of unavailability tolerated     (SRE p.216-218)
  scan-time   time to scan a dataset at a given rate (1T vs 1E)                    (SRE p.251)
  borgmon-ram RAM of a Borgmon-like monitor: series x points x 24 B                (SRE p.90-91; 12 h = note 50, p.98)
  duration    minutes between two times (outage 14:54-16:00; incident 15:01-16:30) (SRE p.335)
Offline; stdlib.
"""
import argparse
import math
import sys


def cmd_provision(a):
    base = math.ceil(a.peak / a.per_task)
    total = base + a.redundancy
    print("Peak %.6g / %.6g per task = %.4g -> minimum %d tasks [from source] (SRE p.35: 3,470 QPS, 100 QPS/task -> 35)" % (a.peak, a.per_task, a.peak / a.per_task, base))
    print("With redundancy N+%d: %d tasks [from source] (SRE p.35: N+2 -> 37; during updates 36 remain and with a machine failure 35)" % (a.redundancy, total))
    print("Book warning: the assumption that two simultaneous failures are negligible may not hold with SPOFs (SRE p.35, note 13).")
    print("Capacity per task must come from load testing, not from tradition (SRE p.331).")


def cmd_toil_floor(a):
    floor = a.oncall_weeks / a.rotation * 100
    print("Toil floor = %d on-call/interrupt weeks / %d rotation weeks = %.3g%% [from source] (SRE p.52: 2/6=33%%, 2/8=25%%)" % (a.oncall_weeks, a.rotation, floor))
    print("Book target: toil < 50%% of time (SRE p.52). Headroom for engineering = %.3g%%." % (50 - floor))


def cmd_retry_amp(a):
    attempts = a.tries ** a.layers
    print("Amplification across layers: %d attempts per layer in %d layers = %d attempts at the lowest level [from source] (SRE p.192: 4^3 = 64)" % (a.tries, a.layers, attempts))
    print("Worst case with a per-request limit of up to 3 attempts: ~3X the traffic; with a per-client retry budget of 10%: ~1.1X [from source] (SRE p.179)")
    if a.rate:
        print("With a rate of %.6g req/s: up to %.6g req/s in the worst case from attempts (per-request) and ~%.6g req/s with a 10%% budget" % (a.rate, a.rate * 3, a.rate * 1.1))
    print("Always randomized exponential backoff; per-request limit; per-server budget (e.g. 60 retries/min) [from source] (SRE p.191-192)")


def cmd_oncall(a):
    if a.sites == 1:
        n = 8
        print("One site: minimum of %d engineers (2 always on-call, one-week shifts, each one 1 week per month) [from source] (SRE p.100)" % n)
    else:
        n = 6 * a.sites
        print("Two sites: reasonable minimum of 6 per site (total %d) [from source] (SRE p.100; p.331)" % n)
    print("Limits: <=25% of time on-call; >=50% on engineering [from source] (SRE p.100)")
    per = a.hours_per_incident
    max_inc = int(a.shift_hours // per)
    print("With %.4g h per incident and a %.4g h shift: at most %d incidents per shift [from source] (SRE p.101: 6 h and 2 per 12 h shift)" % (per, a.shift_hours, max_inc))
    print("Typical response times: 5 min (user-facing/sensitive) and 30 min (less sensitive) [from source] (SRE p.99)")
    if a.slo:
        slo = float(a.slo) / 100
        q = 90 * 24 * 60 * (1 - slo)
        print("SLO %s%% per quarter (90 d, calendar [inference]) = %.4g min of downtime; the book cites ~13 min for 99.99%% (SRE p.99-100)" % (a.slo, q))


def cmd_bimodal(a):
    normal = a.qps * a.latency
    stuck = a.qps * a.stuck_fraction * a.deadline + a.qps * (1 - a.stuck_fraction) * a.latency
    served = min(1.0, a.threads / stuck)
    print("Available threads: %d" % a.threads)
    print("Normal operation: %.6g QPS x %.6g s = ~%.4g busy threads [from source] (SRE p.193)" % (a.qps, a.latency, normal))
    print("With %.3g%% of requests stuck until the %.6g s deadline: demand of ~%.5g threads [from source] (SRE p.193-194: 5,000+95)" % (a.stuck_fraction * 100, a.deadline, stuck))
    print("Fraction served ~%.1f%%; error ~%.1f%% [from source] (SRE p.194: 19.6%% and 80.4%%)" % (served * 100, (1 - served) * 100))
    print("Book lesson: deadlines several orders of magnitude above the average latency are bad; fail early (SRE p.194).")


def cmd_quorum(a):
    if a.replicas is None:
        n = 2 * a.failures + 1
        nb = 3 * a.failures + 1
        print("Tolerate %d failures: %d replicas (majority, 2f+1); with Byzantine failures: %d (3f+1) [from source] (SRE p.216)" % (a.failures, n, nb))
        print("Without Byzantine the minimum is 3 replicas; 5 tolerate two failures, useful because of planned maintenance [from source] (SRE p.216)")
    else:
        n = a.replicas
        q = n // 2 + 1
        tol = n - q
        print("%d replicas: majority quorum = %d, tolerates %d unavailable (%.0f%%) [from source] (SRE p.218: 5 -> 3, 40%%; 6 -> 4, 33%%)" % (n, q, tol, 100 * tol / n))
        if n % 2 == 0:
            print("Even number: adding a replica can reduce the percentage availability [from source] (SRE p.218)")


def cmd_scan(a):
    unit = 2 ** 50 if a.binary else 10 ** 15
    secs = a.petabytes * unit / (a.mb_per_s * (2 ** 20 if a.binary else 10 ** 6))
    years = secs / (365 * 86400)
    print("%.6g PB at %.6g MB/s by one task = %.1f years [%s]" % (a.petabytes, a.mb_per_s, years, "binary units" if a.binary else "decimal units"))
    print("The book says ~8 decades for 700 PB at 300 MB/s (SRE p.251); running with --binary reproduces the order of magnitude [inference about the units].")
    if a.tasks > 1:
        py = years / a.tasks
        if py >= 1:
            t = "%.2f years" % py
        elif py * 365 >= 1:
            t = "%.2f days" % (py * 365)
        elif py * 365 * 24 >= 1:
            t = "%.2f hours" % (py * 365 * 24)
        else:
            t = "%.2f minutes" % (py * 365 * 24 * 60)
        print("With %d tasks in parallel (independent shards): %s [inference, idea from the book in SRE p.251-252]" % (a.tasks, t))


def cmd_borgmon_ram(a):
    points = a.hours * 3600 / a.interval
    total = a.series * points * a.bytes_per_point
    print("Series: %.6g; horizon: %.6g h; interval: %.6g s => %.6g points per series" % (a.series, a.hours, a.interval, points))
    print("RAM = %.6g x %.6g x %.4g B = %.4g bytes = %.4g GB (decimal) = %.4g GiB [derived]" % (
        a.series, points, a.bytes_per_point, total, total / 1e9, total / 2 ** 30))
    print("From the book: ~24 bytes per point; 1 million series for 12 h at 1 min fit in under 17 GB of RAM [from source] (SRE p.90-91) [DATED];")
    print("          12 h is a 'magic number' (note 50, p.98); the state is archived in the TSDB (slower, cheaper and larger) [from source] (SRE p.91).")
    print("Caveat [inference]: the book does not say whether the 24 B include labels and indexes; treat the result as a floor. Book example => 1e6 x 720 x 24 = 17.28e9 B = 16.1 GiB.")


def _hm(x):
    h, m = x.split(":")
    return int(h) * 60 + int(m)


def cmd_duration(a):
    d = _hm(a.end) - _hm(a.start)
    if d < 0:
        d += 24 * 60
    print("%s -> %s = %d minutes (%dh%02d) [derived]" % (a.start, a.end, d, d // 60, d % 60))
    print("App. D (SRE p.335): OUTAGE 14:54-16:00 = 66 min; INCIDENT 15:01-16:30 = 89 min; exit criterion = 30 min of nominal performance.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("provision")
    s.add_argument("--peak", type=float, required=True)
    s.add_argument("--per-task", type=float, required=True)
    s.add_argument("--redundancy", type=int, default=2)
    s.set_defaults(f=cmd_provision)
    s = sub.add_parser("toil-floor")
    s.add_argument("--rotation", type=int, required=True, help="people in the rotation (weeks of the cycle)")
    s.add_argument("--oncall-weeks", type=int, default=2, help="primary+secondary per cycle (book: 2)")
    s.set_defaults(f=cmd_toil_floor)
    s = sub.add_parser("retry-amp")
    s.add_argument("--tries", type=int, default=4)
    s.add_argument("--layers", type=int, default=3)
    s.add_argument("--rate", type=float)
    s.set_defaults(f=cmd_retry_amp)
    s = sub.add_parser("oncall")
    s.add_argument("--sites", type=int, choices=[1, 2], default=1)
    s.add_argument("--shift-hours", type=float, default=12)
    s.add_argument("--hours-per-incident", type=float, default=6)
    s.add_argument("--slo")
    s.set_defaults(f=cmd_oncall)
    s = sub.add_parser("bimodal")
    s.add_argument("--threads", type=int, default=1000)
    s.add_argument("--qps", type=float, default=1000)
    s.add_argument("--latency", type=float, default=0.1)
    s.add_argument("--stuck-fraction", type=float, default=0.05)
    s.add_argument("--deadline", type=float, default=100)
    s.set_defaults(f=cmd_bimodal)
    s = sub.add_parser("quorum")
    s.add_argument("--failures", type=int, default=1)
    s.add_argument("--replicas", type=int)
    s.set_defaults(f=cmd_quorum)
    s = sub.add_parser("scan-time")
    s.add_argument("--petabytes", type=float, required=True)
    s.add_argument("--mb-per-s", type=float, required=True)
    s.add_argument("--tasks", type=int, default=1)
    s.add_argument("--binary", action="store_true")
    s.set_defaults(f=cmd_scan)
    s = sub.add_parser("borgmon-ram")
    s.add_argument("--series", type=float, required=True)
    s.add_argument("--interval", type=float, default=60, help="collection interval in seconds")
    s.add_argument("--hours", type=float, default=12)
    s.add_argument("--bytes-per-point", dest="bytes_per_point", type=float, default=24)
    s.set_defaults(f=cmd_borgmon_ram)
    s = sub.add_parser("duration")
    s.add_argument("--start", required=True)
    s.add_argument("--end", required=True)
    s.set_defaults(f=cmd_duration)
    a = ap.parse_args(argv)
    a.f(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
