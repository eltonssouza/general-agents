# -*- coding: utf-8 -*-
"""
dpe_cost.py - cost/ROI calculator for build time and waiting (DPE, Gradle Inc., 2022).
Stdlib, no network, deterministic. Pages = PDF (printed = N - 5).

Subcommands:
  engineer-year   CE = DE*CM*8*60                              (DPE p.78)
  wait            annual waiting cost = B_year*W*CM*minutes     (DPE p.79-80)
  debug           debugging cost = B_year*F*I*T*CM            (DPE p.81)
  faulty          same for faulty build logic                (DPE p.82-83)
  example         reproduces the 200-engineer example         (DPE p.78-84)
  feedback        average successful build time and context switches (DPE p.30, 67)
  flaky           P_pass, flaky failures/day, maximum rate per test  (DPE p.74)
  savings         annual savings = cost/min * minutes saved * builds/year (DPE p.19, 24)
  team-time       days saved per year (reproduces Team 2 and Team 3) (DPE p.29)

Labels: [from source] = formula/number from the book's example; [user data] = supplied parameter;
[inference] = package step; [extrapolation] = parameter or model outside the book.
The default numbers are from the book's EXAMPLE (team of 200); the book says to use your own data (DPE p.78-79).
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

L = "[from source]"
U = "[user data]"
I = "[inference]"
X = "[extrapolation]"


def usd(v):
    return "US$ {:,.0f}".format(v).replace(",", ".")


def engineer_year(de=230.0, cm=1.0):
    return de * cm * 8 * 60


def wait_cost(builds_year, wait_frac, cm, minutes=1.0):
    return builds_year * wait_frac * cm * minutes


def debug_cost(builds_year, fail, invest, minutes, cm):
    return builds_year * fail * invest * minutes * cm


def feedback(build_min, fail_rate, debug_min, n_builds, switches=2.0):
    avg = build_min + fail_rate * build_min + debug_min
    ctx = fail_rate * n_builds * switches
    return avg, ctx


def flaky_pass(n_tests, p):
    return (1.0 - p) ** n_tests


def flaky_max_rate(n_tests, target, retries):
    """Maximum rate per test such that 1-P_pass <= target.
    retries=0: (1-p)^n = 1-target. retries=1: each test only fails if it fails twice: effective probability p^2 (inference)."""
    q = (1.0 - target) ** (1.0 / n_tests)
    eff = 1.0 - q  # maximum effective rate per test (after retries)
    if retries == 0:
        return eff
    return eff ** (1.0 / (retries + 1))


def team_days_saved(builds_week, before_min, after_min, weeks=52.0, hours_day=8.0):
    return builds_week * weeks * (before_min - after_min) / 60.0 / hours_day


def cmd_engineer_year(a):
    ce = engineer_year(a.days, a.cm)
    lines = [f"CE = DE*CM*8*60 = {a.days:g}*{a.cm:g}*480 = {usd(ce)} per engineer-year {L} (DPE p.78); parameters {U}"]
    lines.append("Book example: 230 days, US$ 1/min => US$ 110.400 (DPE p.78)")
    return {"CE": ce}, lines


def cmd_wait(a):
    c = wait_cost(a.builds_year, a.wait_frac, a.cm, a.minutes)
    page = "p.79" if a.kind == "local" else "p.80"
    lines = [f"Annual waiting cost ({a.kind}) = B_year*W*CM*min = {a.builds_year:g}*{a.wait_frac:g}*{a.cm:g}*{a.minutes:g} = {usd(c)} {L} (DPE {page}); parameters {U}"]
    if a.minutes:
        lines.append(f"Each minute saved is worth {usd(wait_cost(a.builds_year, a.wait_frac, a.cm, 1))} per year; each second {usd(wait_cost(a.builds_year, a.wait_frac, a.cm, 1)/60)} {I} (the book gives US$ 6.667/s in the example, p.79)")
    if a.engineer_year_cost:
        lines.append(f"Equivalent to {c / a.engineer_year_cost:.1f} engineer-years at {usd(a.engineer_year_cost)} {I}")
    return {"cost": c}, lines


def cmd_debug(a, faulty=False):
    c = debug_cost(a.builds_year, a.fail, a.invest, a.minutes, a.cm)
    page = "p.82-83" if faulty else "p.81"
    lines = [f"Annual cost = B_year*F*I*T*CM = {a.builds_year:g}*{a.fail:g}*{a.invest:g}*{a.minutes:g}*{a.cm:g} = {usd(c)} {L} (DPE {page}); parameters {U}"]
    return {"cost": c}, lines


def cmd_example(a):
    cm, de, bl, bci, dw = 1.0, 230.0, 2000.0, 2000.0, 250.0
    ce = engineer_year(de, cm)
    byl, byci = bl * dw, bci * dw
    wl, wci = 0.8, 0.2
    al, aci = 3.0, 8.0
    wait_l = wait_cost(byl, wl, cm, al)
    wait_ci = wait_cost(byci, wci, cm, aci)
    dbg_l = debug_cost(byl, 0.2, 0.05, 20, cm)
    dbg_ci = debug_cost(byci, 0.1, 0.2, 60, cm)
    f_l = debug_cost(byl, 0.002, 1.0, 240, cm)
    f_ci = debug_cost(byci, 0.001, 1.0, a.faulty_ci_min, cm)
    hw = 200000.0
    total = wait_l + wait_ci + dbg_l + dbg_ci + f_l + f_ci + hw
    lines = [
        f"CE = {usd(ce)} (DPE p.78); BYL = BYCI = {byl:,.0f} (DPE p.78) {L}".replace(",", "."),
        f"Local build waiting ({al:g} min): {usd(wait_l)} (DPE p.79, p.84) {L}",
        f"CI build waiting ({aci:g} min): {usd(wait_ci)} (DPE p.80, p.84) {L}",
        f"Debugging of code failures: {usd(dbg_l)} local + {usd(dbg_ci)} CI = {usd(dbg_l + dbg_ci)} (DPE p.81) {L}",
        f"Faulty build logic: {usd(f_l)} local + {usd(f_ci)} CI (TCI={a.faulty_ci_min:g} min) = {usd(f_l + f_ci)} (DPE p.83) {L}",
        f"CI hardware: {usd(hw)} (DPE p.83) {L}",
        f"TOTAL = {usd(total)} per year; half = {total / 2 / ce:.1f} engineer-years (DPE p.84: about 15) {L}",
    ]
    if a.faulty_ci_min != 120:
        lines.append(f"WARNING: the book uses TCI=120 min in the calculation (p.83) but 90 min in the table (p.82); with {a.faulty_ci_min:g} the total differs from US$ 3.200.000. Inconsistency in the book.")
    else:
        lines.append("WARNING: the table on p.82 says TCI=90 min; the calculation on p.83 (reproduced here) uses 120. Use --faulty-ci-min 90 to see the total with 90 (US$ 3.185.000).")
    lines.append("Example assumptions [vendor claim]: no verifiable source; use your own data (DPE p.78-79).")
    return {"total": total, "wait_local": wait_l, "wait_ci": wait_ci, "debug": dbg_l + dbg_ci, "faulty": f_l + f_ci, "hardware": hw, "CE": ce}, lines


def cmd_feedback(a):
    avg, ctx = feedback(a.build_min, a.fail_rate, a.debug_min, a.builds, a.switches)
    lines = [
        f"Average successful build time = tb + f*tb + tdebug = {a.build_min:g} + {a.fail_rate:g}*{a.build_min:g} + {a.debug_min:g} = {avg:.2f} min {L} (DPE p.30, p.67); parameters {U}",
        f"Context switches = f * n_builds * {a.switches:g} = {ctx:.1f} {L} (factor 2 on p.30; 'number of switches' on p.67)",
        f"{I} the book's formula is an approximation (it does not model several failures per build).",
    ]
    return {"avg_success_minutes": avg, "context_switches": ctx}, lines


def cmd_flaky(a):
    lines = []
    res = {}
    if a.rate is not None:
        eff = a.rate ** (a.retries + 1) if a.retries else a.rate
        pp = flaky_pass(a.tests, eff)
        fail = 1 - pp
        per_day = fail * a.builds_day
        lines.append(f"P_pass = (1-p)^n = (1-{eff:.3g})^{a.tests} = {pp:.6f} {L} (DPE p.74)")
        lines.append(f"P(flaky failure) = 1-P_pass = {fail:.4%}; failures per day = {per_day:.2f} of {a.builds_day:g} builds {L} (DPE p.74)")
        if a.retries:
            lines.append(f"With {a.retries} retry(ies) the effective probability per test is p^{a.retries + 1} {I} (assumes independent retries)")
        lines.append(f"Book target: < 1% of developer pipeline runs (DPE p.74): {'OK' if fail < 0.01 else 'ABOVE'}")
        res.update(p_pass=pp, fail_prob=fail, per_day=per_day)
    else:
        mx = flaky_max_rate(a.tests, a.target, a.retries)
        lines.append(f"Maximum average rate per test for {a.target:.2%} of builds affected, {a.tests} flaky tests, {a.retries} retry(ies): {mx:.4%} {L} (DPE p.74: example 0.005% without retry and 0.7% with one)")
        lines.append(f"Builds tolerated per day: {a.target * a.builds_day:.1f} of {a.builds_day:g} {L} (DPE p.74: 5 in the example)")
        if a.retries:
            lines.append(f"{I} retry treated as independent: the test only fails if it fails {a.retries + 1} times (p^{a.retries + 1}).")
        res.update(max_rate=mx)
    return res, lines


def cmd_savings(a):
    minutes = a.minutes_saved
    note = ""
    if a.reduction_pct is not None:
        minutes = a.build_min * a.reduction_pct / 100.0
        note = f" (minutes saved = {a.build_min:g} * {a.reduction_pct:g}% = {minutes:g}; the percentage is {X})"
    save = a.cost_per_min * minutes * a.builds_year
    lines = [f"Annual savings = cost/min * minutes saved * builds/year = {a.cost_per_min:g} * {minutes:g} * {a.builds_year:g} = {usd(save)} {L} (DPE p.19){note}; parameters {U}"]
    if a.engineer_year_cost:
        lines.append(f"= {save / a.engineer_year_cost:.2f} engineer-years at {usd(a.engineer_year_cost)} {L} (DPE p.24: time saved x builds -> engineer-years x loaded cost)")
    if a.wait_frac is not None:
        lines.append(f"Adjusted by the unproductive waiting fraction W={a.wait_frac:g}: {usd(save * a.wait_frac)} {I} (the book applies W in ch. 15, p.79)")
    lines.append("Does not include the cost of the solution, licenses or dedicated team: the book does not calculate payback.")
    return {"savings": save}, lines


def cmd_team_time(a):
    d = team_days_saved(a.builds_week, a.before, a.after, a.weeks, a.hours)
    lines = [f"Days saved/year = builds/week*{a.weeks:g}*(before-after)/60/{a.hours:g} = {d:.1f} {L} (DPE p.29; weeks/year and hours/day are {I}, they match the examples)",
             "Book examples: Team 2 (1010 builds/week, 1 min -> 36 s) = 44 days; Team 3 (12000/week, 9 -> 5 min) = 5200 days (DPE p.29)"]
    if a.devs:
        lines.append(f"Fraction of engineering time = {d / (a.devs * a.days_dev):.1%} with {a.devs} devs and {a.days_dev:g} days/year (book: ~25% for Team 3 with 220 days, p.29)")
    return {"days_saved": d}, lines


def build_parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("engineer-year")
    p.add_argument("--days", type=float, default=230)
    p.add_argument("--cm", type=float, default=1.0)
    p = sp.add_parser("wait")
    p.add_argument("--kind", choices=["local", "ci"], default="local")
    p.add_argument("--builds-year", type=float, required=True)
    p.add_argument("--wait-frac", type=float, required=True)
    p.add_argument("--cm", type=float, required=True)
    p.add_argument("--minutes", type=float, default=1.0)
    p.add_argument("--engineer-year-cost", type=float)
    for name in ("debug", "faulty"):
        p = sp.add_parser(name)
        p.add_argument("--builds-year", type=float, required=True)
        p.add_argument("--fail", type=float, required=True)
        p.add_argument("--invest", type=float, required=True)
        p.add_argument("--minutes", type=float, required=True)
        p.add_argument("--cm", type=float, required=True)
    p = sp.add_parser("example")
    p.add_argument("--faulty-ci-min", type=float, default=120.0)
    p = sp.add_parser("feedback")
    p.add_argument("--build-min", type=float, required=True)
    p.add_argument("--fail-rate", type=float, required=True)
    p.add_argument("--debug-min", type=float, required=True)
    p.add_argument("--builds", type=float, default=1.0)
    p.add_argument("--switches", type=float, default=2.0)
    p = sp.add_parser("flaky")
    p.add_argument("--tests", type=int, required=True)
    p.add_argument("--builds-day", type=float, required=True)
    p.add_argument("--target", type=float, default=0.01)
    p.add_argument("--rate", type=float, help="flake rate per test (0-1); if omitted, computes the maximum rate")
    p.add_argument("--retries", type=int, default=0)
    p = sp.add_parser("savings")
    p.add_argument("--cost-per-min", type=float, required=True)
    p.add_argument("--builds-year", type=float, required=True)
    p.add_argument("--minutes-saved", type=float, default=0.0)
    p.add_argument("--build-min", type=float, default=0.0)
    p.add_argument("--reduction-pct", type=float)
    p.add_argument("--engineer-year-cost", type=float)
    p.add_argument("--wait-frac", type=float)
    p = sp.add_parser("team-time")
    p.add_argument("--builds-week", type=float, required=True)
    p.add_argument("--before", type=float, required=True)
    p.add_argument("--after", type=float, required=True)
    p.add_argument("--weeks", type=float, default=52.0)
    p.add_argument("--hours", type=float, default=8.0)
    p.add_argument("--devs", type=float)
    p.add_argument("--days-dev", type=float, default=220.0)
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    table = {
        "engineer-year": cmd_engineer_year, "wait": cmd_wait, "debug": cmd_debug,
        "faulty": lambda x: cmd_debug(x, True), "example": cmd_example, "feedback": cmd_feedback,
        "flaky": cmd_flaky, "savings": cmd_savings, "team-time": cmd_team_time,
    }
    res, lines = table[a.cmd](a)
    if a.json:
        print(json.dumps({"result": res, "lines": lines}, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
