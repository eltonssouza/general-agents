---
name: dpe-cost-roi-calculator
description: Calculates the cost and ROI of build waiting and debugging with the DPE Handbook formulas (cost per engineer-year, local and CI waiting, debugging, faulty build logic, the 200-engineer example, P_pass of flaky tests, annual savings, days saved). Use when the user asks "how much does our build wait cost?", "how much do I save by cutting 2 minutes?" or "what is the chance a build passes with flaky tests?". Do not use to promise payback.
---

# Build cost and ROI

Source: DPE p.19, 24, 29-30, 67, 74 and 78-84 (PDF page; printed = N − 5). The default numbers come from the book's EXAMPLE (a team of 200); the book says to use your own data (p.78-79). Never assume the example's numbers are the user's.

## Procedure

1. Ask for the parameters (builds per year, wait fraction, cost per minute, failure rate, times) and run (read-only, no network):
   ```bash
   python -I <PKG>/scripts/dpe_cost.py engineer-year [--days 230 --cm 1.0]
   python -I <PKG>/scripts/dpe_cost.py wait --builds-year 100000 --wait-frac 0.5 --cm 1.0 [--kind local|ci --minutes 1]
   python -I <PKG>/scripts/dpe_cost.py debug --builds-year 100000 --fail 0.2 --invest 0.5 --minutes 30 --cm 1.0
   python -I <PKG>/scripts/dpe_cost.py faulty --builds-year 100000 --fail 0.2 --invest 0.5 --minutes 30 --cm 1.0
   python -I <PKG>/scripts/dpe_cost.py example [--faulty-ci-min 120]
   python -I <PKG>/scripts/dpe_cost.py feedback --build-min 5 --fail-rate 0.2 --debug-min 15
   python -I <PKG>/scripts/dpe_cost.py flaky --tests 1000 --builds-day 100 [--target 0.01 --rate R --retries N]
   python -I <PKG>/scripts/dpe_cost.py savings --cost-per-min 1 --builds-year 100000 [--minutes-saved M | --build-min B --reduction-pct P]
   python -I <PKG>/scripts/dpe_cost.py team-time --builds-week 1010 --before 1 --after 0.6
   ```
   (`<PKG>` = package root; from this skill, `../../`.) The global `--json` option (before the subcommand) prints JSON. Exit 0; an argument error exits with 2. The values above are only illustrative; use the user's.
2. Interpret: each line carries the formula, the value and a label: `[from source]` (formula or example number), `[user data]`, `[inference]`, `[extrapolation]`. Keep the labels in the answer.
3. The book's promotional numbers (50-90% savings, "hard" ROI) are `[vendor claim]`. The book gives neither payback nor the online calculator's formulas.
4. Inconsistencies to flag: TCI 90 (table p.82) versus 120 (calculation p.83); 180 builds/dev for Team 2 (p.28); "exponential" (p.29) with linear numbers.

## Response format

Parameters used and their origin — formula `[from source] (DPE p.N)` — result — sensitivity to the assumptions — vendor caveats.

## Limits

A counting model, not a measurement. Without representative user data, the result is only an illustration.
