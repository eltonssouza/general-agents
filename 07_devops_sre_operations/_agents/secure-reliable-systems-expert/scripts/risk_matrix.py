# -*- coding: utf-8 -*-
"""
risk_matrix.py - computes the ranking of the BSRS disaster risk assessment matrix (Appendix A, BSRS p.535-536).

Rule from the book: ranking = probability (within one year) x impact; sort from highest to lowest (BSRS p.535).
Scales (BSRS p.536):
  probability: almost never 0.0 | unlikely 0.2 | somewhat unlikely 0.4 | likely 0.6 | highly likely 0.8 | inevitable 1.0
  impact:        negligible 0.0 | minimal 0.2 | moderate 0.5 | severe 0.8 | critical 1.0
The book also recommends reviewing outliers (an unlikely event can be critical because of its impact; BSRS p.402): the script flags
probability <= 0.2 with impact >= 0.8 for review [inference on the numeric criterion; the recommendation is from the book].
Numeric values 0.0-1.0 or labels (en/pt) are accepted.

Usage (Python 3, stdlib, no network; run with `python -I`):
  python -I scripts/risk_matrix.py scales
  python -I scripts/risk_matrix.py sample                 # sample CSV with the risks of Table A-1 (blank values)
  python -I scripts/risk_matrix.py rank riscos.csv [--json] [--top N]
      CSV (UTF-8, header): theme,risk,probability,impact,systems
  python -I scripts/risk_matrix.py rank riscos.json       # list of objects with the same keys
"""
import argparse
import csv
import io
import json
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROB = {"almost never": 0.0, "quase nunca": 0.0, "unlikely": 0.2, "improvavel": 0.2, "somewhat unlikely": 0.4, "um tanto improvavel": 0.4,
        "pouco provavel": 0.4, "likely": 0.6, "provavel": 0.6, "highly likely": 0.8, "altamente provavel": 0.8, "inevitable": 1.0, "inevitavel": 1.0}
IMP = {"negligible": 0.0, "desprezivel": 0.0, "minimal": 0.2, "minimo": 0.2, "moderate": 0.5, "moderado": 0.5, "severe": 0.8, "severo": 0.8,
       "critical": 1.0, "critico": 1.0}

SAMPLE = [("Environmental", "Earthquake"), ("Environmental", "Flood"), ("Environmental", "Fire"), ("Environmental", "Hurricane"),
          ("Infrastructure reliability", "Power outage"), ("Infrastructure reliability", "Loss of internet connectivity"),
          ("Infrastructure reliability", "Authentication system down"), ("Infrastructure reliability", "High system latency/infrastructure slowdown"),
          ("Security", "System compromise"), ("Security", "Insider theft of intellectual property"), ("Security", "DDoS/DoS attack"),
          ("Security", "Misuse of system resources (e.g., cryptocurrency mining)"), ("Security", "Vandalism/website defacement"),
          ("Security", "Phishing attack"), ("Security", "Software security bug"), ("Security", "Hardware security bug"),
          ("Security", "Emerging serious vulnerability (e.g., Meltdown/Spectre, Heartbleed)")]


def norm(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().strip().split())


def parse(v, table, what):
    if isinstance(v, (int, float)):
        x = float(v)
    else:
        t = norm(v).replace(",", ".")
        if t in table:
            return table[t]
        try:
            x = float(t)
        except ValueError:
            raise ValueError("invalid %s: %r (use 0.0-1.0 or a label from the scale)" % (what, v))
    if not 0.0 <= x <= 1.0:
        raise ValueError("%s out of range 0.0-1.0: %r" % (what, v))
    return x


def load_rows(path):
    if path.lower().endswith(".json"):
        with io.open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser(description="Disaster risk matrix (BSRS Appendix A)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("scales")
    sub.add_parser("sample")
    p = sub.add_parser("rank")
    p.add_argument("file")
    p.add_argument("--json", action="store_true")
    p.add_argument("--top", type=int, default=0)
    a = ap.parse_args()
    if a.cmd in (None, "scales"):
        print("Probability within one year (BSRS p.536): almost never 0.0 | unlikely 0.2 | somewhat unlikely 0.4 | likely 0.6 | highly likely 0.8 | inevitable 1.0")
        print("Impact on the organization (BSRS p.536): negligible 0.0 | minimal 0.2 | moderate 0.5 | severe 0.8 | critical 1.0")
        print("Ranking = probability x impact (BSRS p.535). E.g., 0.8 requires more immediate attention than 0.5 or 0.3.")
        return
    if a.cmd == "sample":
        print("theme,risk,probability,impact,systems")
        for th, r in SAMPLE:
            print('%s,"%s",,,' % (th, r))
        return
    rows = load_rows(a.file)
    out = []
    errs = []
    for i, r in enumerate(rows, 1):
        try:
            pr = r.get("probability", "")
            im = r.get("impact", "")
            if pr in ("", None) or im in ("", None):
                errs.append("line %d (%s): probability or impact blank; ignored" % (i, r.get("risk", "?")))
                continue
            p_ = parse(pr, PROB, "probability")
            i_ = parse(im, IMP, "impact")
        except ValueError as e:
            errs.append("line %d (%s): %s" % (i, r.get("risk", "?"), e))
            continue
        rank = round(p_ * i_, 4)
        out.append({"theme": r.get("theme", ""), "risk": r.get("risk", ""), "probability": p_, "impact": i_, "rank": rank,
                    "systems": r.get("systems", ""), "review_outlier": bool(p_ <= 0.2 and i_ >= 0.8)})
    out.sort(key=lambda x: (-x["rank"], -x["impact"], x["risk"]))
    if a.top:
        out = out[: a.top]
    if a.json:
        print(json.dumps({"ranking": out, "warnings": errs}, ensure_ascii=False, indent=1))
        return
    print("| # | Theme | Risk | Prob. | Impact | Ranking | Systems | Notes |")
    print("|---|-------|------|-------|--------|---------|---------|-------|")
    for n, x in enumerate(out, 1):
        obs = "review outlier: unlikely but high impact (BSRS p.402)" if x["review_outlier"] else ""
        print("| %d | %s | %s | %.1f | %.1f | %.2f | %s | %s |" % (n, x["theme"], x["risk"], x["probability"], x["impact"], x["rank"], x["systems"], obs))
    for e in errs:
        print("WARNING: " + e)
    print("\nDevelop response plans for the most critical risks (BSRS p.535). Assess per location if there are several sites (BSRS p.535).")


if __name__ == "__main__":
    main()
