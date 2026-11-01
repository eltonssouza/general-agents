# -*- coding: utf-8 -*-
"""
error_budget_calc.py - availability, allowed downtime and error budget calculator.

Only formulas the book provides (Google SRE Book, 2016; pages = PDF, printed = N-12):
  * time-based availability = uptime / (uptime + downtime)               [from source] (SRE p.38)
  * aggregate availability  = successful requests / total                [from source] (SRE p.38)
  * error budget = 1 - SLO (e.g. 99.99% -> 0.01%)                        [from source] (SRE p.25; p.330)
  * downtime table by nines (Appendix A)                                 [from source] (SRE p.326-327)
  * budget consumption: failure / budget (example 0.0002% of 0.001% = 20%)     [from source] (SRE p.43)
  * value of the extra nine: revenue x availability delta (example $900)       [from source] (SRE p.40)
  * allowed corrupted bytes (99.99% of 2 GB = 200 KB)                    [from source] (SRE p.242)
Period convention (calibrated to reproduce Appendix A): year=365 days, quarter=90, month=30,
week=7, day=1, hour=1/24 [inference: checked against the 48 table cells with --table].

Offline, no external files. Python 3 stdlib.
"""
import argparse
import math
import re
import sys

PERIODS = [("year", 365 * 86400), ("quarter", 90 * 86400), ("month", 30 * 86400),
           ("week", 7 * 86400), ("day", 86400), ("hour", 3600)]

# Values printed in Appendix A (SRE p.326-327), in the order of the columns above.
BOOK_TABLE = {
    90.0: ["36.5 days", "9 days", "3 days", "16.8 hours", "2.4 hours", "6 minutes"],
    95.0: ["18.25 days", "4.5 days", "1.5 days", "8.4 hours", "1.2 hours", "3 minutes"],
    99.0: ["3.65 days", "21.6 hours", "7.2 hours", "1.68 hours", "14.4 minutes", "36 seconds"],
    99.5: ["1.83 days", "10.8 hours", "3.6 hours", "50.4 minutes", "7.20 minutes", "18 seconds"],
    99.9: ["8.76 hours", "2.16 hours", "43.2 minutes", "10.1 minutes", "1.44 minutes", "3.6 seconds"],
    99.95: ["4.38 hours", "1.08 hours", "21.6 minutes", "5.04 minutes", "43.2 seconds", "1.8 seconds"],
    99.99: ["52.6 minutes", "12.96 minutes", "4.32 minutes", "60.5 seconds", "8.64 seconds", "0.36 seconds"],
    99.999: ["5.26 minutes", "1.30 minutes", "25.9 seconds", "6.05 seconds", "0.87 seconds", "0.04 seconds"],
}
UNIT = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}


def parse_book(cell):
    """Returns (value in seconds, tolerance in seconds = one unit of the last printed digit; the 99.999%/day cell prints 0.87 for an exact 0.864, a rounding in the book)."""
    m = re.match(r"([\d.]+)\s+(days|hours|minutes|seconds)$", cell)
    txt = m.group(1)
    dp = len(txt.split(".")[1]) if "." in txt else 0
    unit = UNIT[m.group(2)]
    return float(txt) * unit, (10 ** -dp) * unit


def human(sec):
    if sec >= 86400:
        return "%.4g days" % (sec / 86400)
    if sec >= 3600:
        return "%.4g hours" % (sec / 3600)
    if sec >= 60:
        return "%.4g min" % (sec / 60)
    return "%.4g s" % sec


def pct(s):
    v = float(str(s).replace("%", "").replace(",", "."))
    if not 0 < v <= 100:
        raise SystemExit("SLO/availability must be in (0, 100]")
    return v


def cmd_downtime(a):
    slo = pct(a.slo)
    frac = 1 - slo / 100
    print("SLO %s%% -> error budget = 1 - SLO = %.6g%% [from source] (SRE p.25; p.330)" % (a.slo, frac * 100))
    print("Allowed downtime per period (no planned downtime; [from source] formula SRE p.38):")
    for name, sec in PERIODS:
        print("  %-10s %s" % (name, human(frac * sec)))
    print("Note: the book warns that, for global services, time is usually less useful than the success rate (SRE p.38).")


def cmd_requests(a):
    slo = pct(a.slo)
    total = a.total
    allowed = total * (1 - slo / 100)
    print("Aggregate availability = successes/total [from source] (SRE p.38)")
    print("With %d requests in the window and SLO %s%%: up to %.6g failures (%.6g%% of the total)." % (total, a.slo, allowed, 100 * allowed / total))
    if a.failed is not None:
        used = a.failed / allowed * 100 if allowed else float("inf")
        avail = 100 * (total - a.failed) / total
        print("Observed failures: %d -> availability %.6g%%; budget consumed: %.4g%%" % (a.failed, avail, used))
        print("EXCEEDED" if a.failed > allowed else "within budget")


def cmd_consume(a):
    slo = pct(a.slo)
    budget = 1 - slo / 100
    fail = a.failure_rate / 100
    used = fail / budget * 100
    print("Budget = %.6g%%; failure rate = %.6g%% -> consumes %.4g%% of the budget. [from source] (SRE p.43 gives 0.0002%% over 0.001%% = 20%%)" % (budget * 100, a.failure_rate, used))
    if used >= 100:
        print("Budget exhausted: the book describes freezing releases and investing in testing/resilience (SRE p.43; freeze changes except security and bugs for the cause, SRE p.330).")
    print("Note: the book does NOT cover burn rate or multi-window alerts [extrapolation if the user asks for them].")


def cmd_value(a):
    d = (pct(a.to) - pct(a.frm)) / 100
    v = a.revenue * d
    print("Availability increase %.6g%% x revenue %.2f = value %.2f [from source] (SRE p.40: example $1M, 99.9%%->99.99%% = $900)" % (d * 100, a.revenue, v))
    print("If the cost of the additional nine is lower than this value, it pays off; if higher, it does not (SRE p.40).")


def cmd_integrity(a):
    slo = pct(a.slo)
    allowed = a.size_bytes * (1 - slo / 100)
    print("SLO %s%% of good bytes in %d bytes allows up to %.6g corrupted bytes [from source] (SRE p.242: 2 GB -> 200 KB)" % (a.slo, a.size_bytes, allowed))


def cmd_table(a):
    bad = 0
    print("Appendix A (SRE p.326-327): computed x printed comparison (tolerance = one unit of the last printed digit; the 99.999%/day cell prints 0.87 for an exact 0.864, a rounding in the book).")
    names = [p[0] for p in PERIODS]
    for lvl, cells in BOOK_TABLE.items():
        frac = 1 - lvl / 100
        row = []
        for (name, sec), cell in zip(PERIODS, cells):
            calc = frac * sec
            book, tol = parse_book(cell)
            ok = abs(calc - book) <= tol * 1.0001 + 1e-9
            if not ok:
                bad += 1
            row.append("%s%s" % (human(calc), "" if ok else " (!= %s)" % cell))
        print("%-8s%% | %s" % (lvl, " | ".join(row)))
    print("Columns:", ", ".join(names))
    print("Result:", "table reproduced (48 cells)" if not bad else "%d cells diverge" % bad)
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("downtime", help="allowed downtime per period for an SLO")
    s.add_argument("slo", help="e.g. 99.99")
    s.set_defaults(f=cmd_downtime)
    s = sub.add_parser("requests", help="allowed failures in a window given a request count")
    s.add_argument("--slo", required=True)
    s.add_argument("--total", type=int, required=True)
    s.add_argument("--failed", type=int)
    s.set_defaults(f=cmd_requests)
    s = sub.add_parser("consume", help="fraction of the budget consumed by a failure rate")
    s.add_argument("--slo", required=True)
    s.add_argument("--failure-rate", type=float, required=True, help="in percent, e.g. 0.0002")
    s.set_defaults(f=cmd_consume)
    s = sub.add_parser("value", help="value of moving up in nines, given revenue")
    s.add_argument("--revenue", type=float, required=True)
    s.add_argument("--from", dest="frm", required=True)
    s.add_argument("--to", required=True)
    s.set_defaults(f=cmd_value)
    s = sub.add_parser("integrity", help="corrupted bytes allowed by an integrity SLO")
    s.add_argument("--slo", required=True)
    s.add_argument("--size-bytes", type=int, required=True)
    s.set_defaults(f=cmd_integrity)
    s = sub.add_parser("table", help="reproduce and check Appendix A")
    s.set_defaults(f=cmd_table)
    a = ap.parse_args(argv)
    r = a.f(a)
    return r or 0


if __name__ == "__main__":
    sys.exit(main())
