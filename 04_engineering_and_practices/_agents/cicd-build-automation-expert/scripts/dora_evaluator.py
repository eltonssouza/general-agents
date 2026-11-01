# -*- coding: utf-8 -*-
"""
dora_evaluator.py - computes the four delivery measures and compares them with labeled EXTERNAL references.

IMPORTANT (audit): the sources of this package (CICD, GRADLE, GHA, SWE-G) do NOT define the DORA metrics and do NOT carry
Elite/High/Medium/Low ranges (CICD p.16 only mentions them in passing). Therefore this script:
  1) computes the measures from raw data (simple arithmetic) [extrapolation];
  2) compares them with the cluster table of the DORA 2024 report, p.13 (copied from the audited package
     dora-devops-delivery-expert; it does NOT come from the sources of this package) [extrapolation];
  3) compares them with the survey numbers cited in CICD p.34-35 (sponsor content) [from source];
  4) does NOT assign an "overall level" or an average score: the DORA 2024 report (p.13-15, 74) says the clusters emerge from
     the year's data and are not a maturity model [extrapolation].
v1 used ranges (Elite with lead time <= 1 h, CFR 0-15%, MTTR etc.) with no backing in any source; they were removed.

Usage:
  python -I scripts/dora_evaluator.py ranges
  python -I scripts/dora_evaluator.py evaluate --deploy-frequency 20 --lead-time-hours 36 --recovery-hours 5 --cfr-percent 12
  (accepted aliases: --mttr-hours = --recovery-hours; frequency in DEPLOYS PER MONTH; month = 30 days [inference])
  python -I scripts/dora_evaluator.py compute --deploys 24 --days 30 --failed 3 --lead-hours 10 20 50 --recovery-hours 2 6
Exit: 0 ok; 2 invalid input.
"""
import argparse
import json
import statistics
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

H = 1.0
DAY = 24 * H
WEEK = 7 * DAY
MONTH = 30 * DAY  # script convention [inference]
SIX_MONTHS = 6 * MONTH

TABLE = """2024 clusters (DORA 2024, p.13) [extrapolation: not from the sources of this package]
Level   | Lead time          | Deploy frequency                  | Failure rate  | Failed-deploy recovery
Elite   | < 1 day            | on demand (several per day)       | 5%            | < 1 hour
High    | 1 day to 1 week    | 1/day to 1/week                   | 20%           | < 1 day
Medium  | 1 week to 1 month  | 1/week to 1/month                 | 10%           | < 1 day
Low     | 1 month to 6 months| 1/month to 1/6 months             | 40%           | 1 week to 1 month
Notes: (1) failure rate is a VALUE per cluster, not a range (Medium, 10%, is more stable than High, 20%); (2) High and Medium
have the same recovery range; between 1 day and 1 week the table says nothing; (3) the clusters emerge from the year's data,
they are not thresholds or a maturity model; (4) 'month' = 30 days is a convention of this script [inference]."""

SURVEY = """Survey numbers cited in CICD p.34-35 [from source; sponsor content (Armory), 19 thousand devs, State of CD 2021]
- almost 2/3 of respondents: code takes 1 week or more from commit to production;
- 69.1%: ship to production at least once a week;
- more than half: it takes 1 day or more to fix an unplanned outage;
- almost 20% of companies: more than 1 month to restore services."""

CFR_CLUSTER = {"Elite": 5.0, "High": 20.0, "Medium": 10.0, "Low": 40.0}


def level_deploy_freq(per_month):
    per_day = per_month / 30.0
    if per_day > 1:
        return "Elite", "more than 1 deploy per day (on demand, several per day) [script approximation: 'several per day' = more than 1/day]"
    per_week = per_month * 7 / 30.0
    if per_week >= 1:
        return "High", "between 1/day and 1/week"
    if per_month >= 1:
        return "Medium", "between 1/week and 1/month"
    if per_month * 6 >= 1:
        return "Low", "between 1/month and 1/6 months"
    return "below-Low", "fewer than 1 deploy every 6 months (outside the table ranges)"


def level_lead_time(h):
    if h < DAY:
        return "Elite", "less than 1 day"
    if h <= WEEK:
        return "High", "between 1 day and 1 week"
    if h <= MONTH:
        return "Medium", "between 1 week and 1 month"
    if h <= SIX_MONTHS:
        return "Low", "between 1 month and 6 months"
    return "above-Low", "more than 6 months (outside the table ranges)"


def level_recovery(h):
    if h < 1:
        return "Elite", "less than 1 hour"
    if h < DAY:
        return "High or Medium", "less than 1 day (the table gives the same range for High and Medium)"
    if h < WEEK:
        return "gap", "between 1 day and 1 week: the table has no range for this interval"
    if h <= MONTH:
        return "Low", "between 1 week and 1 month"
    return "above-Low", "more than 1 month (outside the table ranges)"


def cfr_reading(p):
    near = sorted(CFR_CLUSTER.items(), key=lambda kv: abs(kv[1] - p))
    best, second = near[0], near[1]
    txt = "values per cluster: Elite 5%%, Medium 10%%, High 20%%, Low 40%%; closest: %s (%g%%)" % (best[0], best[1])
    if abs(abs(best[1] - p) - abs(second[1] - p)) < 2.0 and best[0] != second[0]:
        txt += "; ambiguous between %s and %s" % (best[0], second[0])
    return best[0], txt


def survey_notes(per_month, lead_h, rec_h):
    notes = []
    if lead_h >= WEEK:
        notes.append("lead time >= 1 week: situation of the majority group (almost 2/3) in the CICD p.34 survey")
    else:
        notes.append("lead time < 1 week: better than the majority group (almost 2/3 take >= 1 week) cited in CICD p.34")
    if per_month * 7 / 30.0 >= 1:
        notes.append("deploy >= 1/week: in the 69.1% group of the CICD p.34 survey")
    else:
        notes.append("deploy < 1/week: outside the 69.1% group that ships >= 1/week (CICD p.34)")
    if rec_h >= DAY:
        notes.append("recovery >= 1 day: in the 'more than half' group of CICD p.34")
    else:
        notes.append("recovery < 1 day: better than 'more than half' (>= 1 day) in CICD p.34")
    return notes


def evaluate(per_month, lead_h, rec_h, cfr):
    r = {
        "reference": "DORA 2024 p.13 [extrapolation]; CICD survey p.34-35 [from source]; no overall level",
        "input": {"deploys_per_month": per_month, "lead_time_h": lead_h, "recovery_h": rec_h, "cfr_pct": cfr},
    }
    lv, d = level_deploy_freq(per_month)
    r["deploy_frequency"] = {"cluster": lv, "reading": d}
    lv, d = level_lead_time(lead_h)
    r["lead_time"] = {"cluster": lv, "reading": d}
    lv, d = level_recovery(rec_h)
    r["recovery"] = {"cluster": lv, "reading": d}
    lv, d = cfr_reading(cfr)
    r["failure_rate"] = {"closest_cluster": lv, "reading": d}
    r["cicd_survey"] = survey_notes(per_month, lead_h, rec_h)
    return r


def print_eval(r):
    print("=" * 70)
    print("COMPARISON WITH EXTERNAL REFERENCES (not a certification nor a maturity model)")
    print("DORA 2024 p.13 ranges: [extrapolation] (outside the package sources). CICD p.34-35 survey: [from source].")
    print("=" * 70)
    e = r["input"]
    print("Input: %.1f deploys/month | lead time %.1f h | recovery %.1f h | failure rate %.1f%%" % (
        e["deploys_per_month"], e["lead_time_h"], e["recovery_h"], e["cfr_pct"]))
    print("1. Deploy frequency -> %s: %s" % (r["deploy_frequency"]["cluster"], r["deploy_frequency"]["reading"]))
    print("2. Lead time        -> %s: %s" % (r["lead_time"]["cluster"], r["lead_time"]["reading"]))
    print("3. Recovery         -> %s: %s" % (r["recovery"]["cluster"], r["recovery"]["reading"]))
    print("4. Failure rate     -> %s: %s" % (r["failure_rate"]["closest_cluster"], r["failure_rate"]["reading"]))
    print("-" * 70)
    print("Survey cited in CICD p.34-35 [from source; sponsor content]:")
    for n in r["cicd_survey"]:
        print("  - " + n)
    print("-" * 70)
    print("NO overall level: the DORA 2024 report says the clusters emerge from the year's data, are not fixed thresholds and")
    print("must not be used as a maturity model or to compare teams (p.13-15, 74) [extrapolation].")
    print("Use it per application/service and compare against your own history. The sources of this package do not define the metrics.")
    print("=" * 70)


def cmd_compute(a):
    if a.days <= 0 or a.deploys < 0 or a.failed < 0 or a.failed > a.deploys:
        print("invalid input: --days > 0, 0 <= --failed <= --deploys", file=sys.stderr)
        return 2
    per_month = a.deploys * 30.0 / a.days
    cfr = (100.0 * a.failed / a.deploys) if a.deploys else 0.0
    print("COMPUTED MEASURES [extrapolation: operational definitions of the package; the sources do not define the metrics]")
    print("- frequency: %d deploys in %g days = %.2f deploys/month (month = 30 days)" % (a.deploys, a.days, per_month))
    print("- failure rate: %d/%d = %.1f%%" % (a.failed, a.deploys, cfr))
    lead = None
    if a.lead_hours:
        lead = statistics.median(a.lead_hours)
        print("- lead time: median of %d changes = %.1f h (mean %.1f h)" % (len(a.lead_hours), lead, statistics.mean(a.lead_hours)))
    rec = None
    if a.recovery_hours:
        rec = statistics.median(a.recovery_hours)
        print("- recovery: median of %d incidents = %.1f h (mean %.1f h)" % (len(a.recovery_hours), rec, statistics.mean(a.recovery_hours)))
    if lead is not None and rec is not None:
        print()
        print_eval(evaluate(per_month, lead, rec, cfr))
    else:
        print("(provide --lead-hours and --recovery-hours to compare with the references)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Delivery measures and comparison with labeled external references")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("ranges", help="show the reference tables and their origin")
    ev = sub.add_parser("evaluate", help="compare the given values with the references")
    ev.add_argument("--deploy-frequency", type=float, required=True, help="deploys per month")
    ev.add_argument("--lead-time-hours", type=float, required=True)
    ev.add_argument("--recovery-hours", "--mttr-hours", dest="recovery", type=float, required=True)
    ev.add_argument("--cfr-percent", type=float, required=True, help="0-100")
    ev.add_argument("--json", action="store_true")
    co = sub.add_parser("compute", help="compute the measures from raw data")
    co.add_argument("--deploys", type=int, required=True)
    co.add_argument("--days", type=float, required=True)
    co.add_argument("--failed", type=int, required=True)
    co.add_argument("--lead-hours", type=float, nargs="*")
    co.add_argument("--recovery-hours", type=float, nargs="*")
    # v1 compatibility (no subcommand)
    ap.add_argument("--deploy-frequency", type=float, dest="v1_df")
    ap.add_argument("--lead-time-hours", type=float, dest="v1_lt")
    ap.add_argument("--mttr-hours", type=float, dest="v1_mt")
    ap.add_argument("--cfr-percent", type=float, dest="v1_cfr")
    a = ap.parse_args()

    if a.cmd == "ranges":
        print(TABLE)
        print()
        print(SURVEY)
        print()
        print("The v1 ranges of this package (Elite with lead time <= 1 h, CFR <= 10%, MTTR with different ranges) had NO backing.")
        return 0
    if a.cmd == "evaluate":
        if a.deploy_frequency < 0 or a.lead_time_hours < 0 or a.recovery < 0 or not (0 <= a.cfr_percent <= 100):
            print("invalid input", file=sys.stderr)
            return 2
        r = evaluate(a.deploy_frequency, a.lead_time_hours, a.recovery, a.cfr_percent)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print_eval(r)
        return 0
    if a.cmd == "compute":
        return cmd_compute(a)
    if None not in (a.v1_df, a.v1_lt, a.v1_mt, a.v1_cfr):
        print_eval(evaluate(a.v1_df, a.v1_lt, a.v1_mt, a.v1_cfr))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
