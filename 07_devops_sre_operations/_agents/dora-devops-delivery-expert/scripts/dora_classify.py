# -*- coding: utf-8 -*-
"""
dora_classify.py - compares the delivery metrics of ONE application/service with the clusters
published in DORA24 (p.13-14). Read-only, no network, deterministic.

WARNINGS (from the report): the levels are NOT thresholds set in advance; they emerge from the
cluster analysis of the year's responses (p.13). They serve as a benchmark reference, not as
certification or a maturity model (p.15, p.74). Use per application/service and compare yourself
with yourself over time (p.16, p.74).

Usage:
  python -I scripts/dora_classify.py ranges
  python -I scripts/dora_classify.py classify --lead-time 3d --deploy-freq 2/week \
        --cfr 12 --recovery 5h [--rework 8] [--json]

Formats:
  duration: 30m, 6h, 3d, 2w, 1mo, 6mo   (m=min, h=hours, d=days, w=weeks, mo=30-day months [inference])
  frequency: on-demand | N/day | N/week | N/month | N/year  (Portuguese alias accepted: sob-demanda)
  cfr, rework: percentage (0-100)

Exit: 0 ok; 1 invalid input.
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

H = 1.0
DAY = 24 * H
WEEK = 7 * DAY
MONTH = 30 * DAY  # script convention (the report does not define the month)
SIX_MONTHS = 6 * MONTH

LEVELS = ["Elite", "High", "Medium", "Low"]
RANK = {"Elite": 0, "High": 1, "Medium": 2, "Low": 3}

# DORA24 p.13 (table) - cluster values
CFR_VALUES = {"Elite": 5.0, "High": 20.0, "Medium": 10.0, "Low": 40.0}
PCT_RESP = {"Elite": "19% (18-20%)", "High": "22% (21-23%)", "Medium": "35% (33-36%)", "Low": "25% (23-26%)"}

RANGES_TXT = """DORA24 p.13 - 2024 clusters (percentage of respondents, 89% uncertainty interval)
Level   | Lead time         | Deploy frequency                  | Failure rate  | Failed deployment recovery  | % respondents
Elite   | < 1 day           | on demand (several per day)       | 5%            | < 1 hour                    | 19% (18-20%)
High    | 1 day to 1 week   | 1/day to 1/week                   | 20%           | < 1 day                     | 22% (21-23%)
Medium  | 1 week to 1 month | 1/week to 1/month                 | 10%           | < 1 day                     | 35% (33-36%)
Low     | 1 to 6 months     | 1/month to 1/6 months             | 40%           | 1 week to 1 month           | 25% (23-26%)
Notes: (1) failure rate is the cluster value, not an interval; medium (10%) is better than high (20%) - p.14 explains:
medium is slower but more stable. (2) high and medium have the same recovery range (< 1 day).
(3) rework rate has no per-level range in the report (NOT COVERED for benchmark). (4) 'month' = 30 days here and is an
inference of the script. (5) clusters emerge from the data; they are not prescribed thresholds (p.13)."""


def parse_duration(s):
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(mo|m|h|d|w)\s*", s.lower())
    if not m:
        raise ValueError(f"invalid duration: {s!r} (use 30m, 6h, 3d, 2w, 1mo)")
    v, u = float(m.group(1)), m.group(2)
    return v * {"m": 1 / 60, "h": 1, "d": DAY, "w": WEEK, "mo": MONTH}[u]


def parse_freq(s):
    """returns deploys per day"""
    t = s.strip().lower()
    if t in ("on-demand", "ondemand", "sob-demanda", "on_demand"):
        return None  # marker: on demand
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*/\s*(day|week|month|year)", t)
    if not m:
        raise ValueError(f"invalid frequency: {s!r} (use on-demand, 3/day, 2/week, 1/month, 4/year)")
    v, u = float(m.group(1)), m.group(2)
    return v / {"day": 1, "week": 7, "month": 30, "year": 365}[u]


def level_lead_time(h):
    if h < DAY:
        return "Elite", "< 1 day"
    if h <= WEEK:
        return "High", "1 day to 1 week"
    if h <= MONTH:
        return "Medium", "1 week to 1 month"
    if h <= SIX_MONTHS:
        return "Low", "1 month to 6 months"
    return None, "above 6 months: outside the report's ranges (worse than Low)"


def level_deploy(per_day):
    if per_day is None or per_day > 1:
        return "Elite", "on demand / several times per day"
    if per_day >= 1 / 7:
        return "High", "between 1/day and 1/week"
    if per_day >= 1 / 30:
        return "Medium", "between 1/week and 1/month"
    if per_day >= 1 / 180:
        return "Low", "between 1/month and 1/6 months"
    return None, "fewer than 1 deploy every 6 months: outside the report's ranges (worse than Low)"


def level_recovery(h):
    if h < 1:
        return "Elite", "< 1 hour"
    if h < DAY:
        return "High/Medium", "< 1 day (the report gives the same range for High and Medium)"
    if h < WEEK:
        return None, "between 1 day and 1 week: range NOT covered by the table (NOT COVERED); falls between Medium/High and Low"
    if h <= MONTH:
        return "Low", "1 week to 1 month"
    return None, "above 1 month: outside the report's ranges (worse than Low)"


def level_cfr(p):
    dist = sorted((abs(p - v), lvl) for lvl, v in CFR_VALUES.items())
    best, second = dist[0], dist[1]
    amb = (second[0] - best[0]) < 1e-9 or (second[0] - best[0]) <= 2.0
    note = (f"closest cluster value: {best[1]} ({CFR_VALUES[best[1]]:.0f}%)"
            + ("; AMBIGUOUS with " + second[1] + f" ({CFR_VALUES[second[1]]:.0f}%)" if amb else ""))
    return best[1], note, amb


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("ranges")
    c = sub.add_parser("classify")
    c.add_argument("--lead-time")
    c.add_argument("--deploy-freq")
    c.add_argument("--cfr", type=float)
    c.add_argument("--recovery")
    c.add_argument("--rework", type=float)
    c.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "ranges" or a.cmd is None:
        print(RANGES_TXT)
        return 0
    res = {"metrics": {}, "warnings": []}
    try:
        if a.lead_time is not None:
            lvl, why = level_lead_time(parse_duration(a.lead_time))
            res["metrics"]["change_lead_time"] = {"input": a.lead_time, "level": lvl, "range": why}
        if a.deploy_freq is not None:
            lvl, why = level_deploy(parse_freq(a.deploy_freq))
            res["metrics"]["deployment_frequency"] = {"input": a.deploy_freq, "level": lvl, "range": why}
        if a.cfr is not None:
            if not 0 <= a.cfr <= 100:
                raise ValueError("cfr must be between 0 and 100")
            lvl, why, amb = level_cfr(a.cfr)
            res["metrics"]["change_failure_rate"] = {"input": f"{a.cfr:g}%", "level": lvl, "range": why, "ambiguous": amb}
        if a.recovery is not None:
            lvl, why = level_recovery(parse_duration(a.recovery))
            res["metrics"]["failed_deployment_recovery_time"] = {"input": a.recovery, "level": lvl, "range": why}
        if a.rework is not None:
            if not 0 <= a.rework <= 100:
                raise ValueError("rework must be between 0 and 100")
            res["metrics"]["rework_rate"] = {"input": f"{a.rework:g}%", "level": None,
                                             "range": "NOT COVERED: the report does not publish a per-level range for rework rate (p.11-13)"}
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    if not res["metrics"]:
        print("ERROR: provide at least one metric", file=sys.stderr)
        return 1

    m = res["metrics"]
    thr = [m[k]["level"] for k in ("change_lead_time", "deployment_frequency", "failed_deployment_recovery_time") if k in m]
    stab = [m["change_failure_rate"]["level"]] if "change_failure_rate" in m else []
    res["throughput_levels"] = thr
    res["stability_levels"] = stab
    ranks = [RANK[x] for x in thr if x in RANK]
    if len(ranks) >= 2 and max(ranks) - min(ranks) >= 2:
        res["warnings"].append("Throughput metrics at very different levels: unusual profile (the report says the metrics tend to move together, p.10). Check the measurement or the specific bottleneck.")
    res["warnings"] += [
        "Levels are benchmarks from the 2024 clusters (p.13), not official thresholds or a maturity model (p.15, p.74).",
        "There is no single 'overall level' here: the clusters arise from the joint combination of the four metrics; use the per-metric profile.",
        "Focus on improving against your own baseline, per application/service (p.14-16, p.74).",
    ]
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    names = {"change_lead_time": "Change lead time", "deployment_frequency": "Deploy frequency",
             "change_failure_rate": "Change failure rate", "failed_deployment_recovery_time": "Failed deployment recovery",
             "rework_rate": "Rework rate"}
    print("Comparison with the DORA24 p.13 clusters (per-metric profile):")
    for k, v in m.items():
        lvl = v["level"] if v["level"] else "-"
        print(f"- {names[k]} [{v['input']}]: {lvl} | {v['range']}")
    print("Throughput (lead time, frequency, recovery):", ", ".join(str(x) if x else "outside the ranges/not covered" for x in thr) or "n/d")
    print("Stability (failure rate; rework has no range):", ", ".join(str(x) if x else "n/c" for x in stab) or "n/d")
    for w in res["warnings"]:
        print("WARNING:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
