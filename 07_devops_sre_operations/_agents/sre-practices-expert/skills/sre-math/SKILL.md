---
name: sre-math
description: "Does the operational arithmetic the Google SRE book provides: N+2 provisioning, toil floor from the on-call rotation, retry amplification, on-call limits, bimodal latency, consensus quorum, scan time, Borgmon RAM and incident duration. Use when the user asks \"how many tasks do I need for 3470 QPS?\", \"how much do 4x3 retries amplify?\" or \"how many people on the on-call rotation?\". Do not use for real capacity planning."
---

# SRE arithmetic from the book

Source: SRE p.35, 52, 90-91, 98, 100-101, 179, 192-194, 216-218, 251, 331 and 335 (PDF page; printed = N − 12). Each subcommand cites the page of the book's example and marks what is `[inference]`.

## Procedure

1. Choose the subcommand and run it (read-only, offline):
   ```bash
   python -I <PKG>/scripts/sre_math.py provision --peak 3470 --per-task 100 [--redundancy 2]
   python -I <PKG>/scripts/sre_math.py toil-floor --rotation 8 [--oncall-weeks 2]
   python -I <PKG>/scripts/sre_math.py retry-amp [--tries 4 --layers 3 --rate N]
   python -I <PKG>/scripts/sre_math.py oncall [--sites 1|2 --shift-hours 12 --hours-per-incident 6 --slo X]
   python -I <PKG>/scripts/sre_math.py bimodal [--threads 1000 --qps 1000 --latency 0.1 --stuck-fraction 0.05 --deadline 100]
   python -I <PKG>/scripts/sre_math.py quorum [--failures 1 | --replicas N]
   python -I <PKG>/scripts/sre_math.py scan-time --petabytes 1 --mb-per-s 100 [--tasks 1 --binary]
   python -I <PKG>/scripts/sre_math.py borgmon-ram --series 2500000 [--interval 60 --hours 12 --bytes-per-point 24]
   python -I <PKG>/scripts/sre_math.py duration --start 14:54 --end 16:00
   ```
   (`<PKG>` = package root; from this skill, `../../`.) The defaults in brackets are the script's; only `provision`, `toil-floor`, `scan-time`, `borgmon-ram` and `duration` have required arguments.
2. Interpret: the output shows the calculation, the book's example with page, and warnings. Label printed examples and formulas as `[from source] (SRE p.N)`; extending them to the user's numbers is `[inference]`. Borgmon (24 B per point) is `[DATED]` (2016).
3. Per-task capacity must come from load testing (p.331), not from tradition.

## Response format

Inputs used — result — equivalent example from the book with page — labels — what to measure to validate.

## Limits

Does not replace capacity planning with real data. The adaptive throttling formula is in an illegible figure in the PDF (p.177) and is not computed here; circuit breaker and jitter are not in the book.
