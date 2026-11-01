---
name: context-budget-estimator
description: Estimates a context budget with numbers the user provides (tokens per component, window, number of tools, prices) and applies the CE2 p.12 short- and long-term memory rules, the BAAS p.88-89 utility function, and the BAAS p.109-110 feedback weight adjustment. Use when the user asks "how much of the 128k window does my prompt use?", "what is the cost per 1,000 calls with caching?", "split these items into short- and long-term memory". Do not use to tokenize text or to cite prices as a fact from the texts.
---

# Context budget estimator and calculators

Sources: BAAS p.88-89 (utility; `--demo` reproduces 95.00 and 127.50) and p.109-110 (weights: x1.1 if +1; x0.9 if −1); CE2 p.12 (eqs. 5-6, memory), p.16 (about 50% occupancy) and p.18 (30 and 100 tools), the last two `[DATED]`. Page convention: PDF (BAAS: printed = PDF − 25; CE2: PDF = printed).

## Procedure

1. Collect the numbers from the user (nothing is tokenized; tokens, window, and prices are theirs). Invalid values (negative, NaN) give exit 2.
2. Run (read-only, no network):
   ```bash
   python -I <PKG>/scripts/ctx_calc.py budget --window 128000 --component sistema=2000 --component historico=30000 --tools 20 --reserve-output 4000 --prefix sistema --price-in 3 --price-cached 0.3 --price-out 15 --cache-hit 0.8 --out-tokens 500 --calls 1000 [--chars NAME=CHARACTERS --chars-per-token N --warn-fill 0.5 --config cfg.json]
   python -I <PKG>/scripts/ctx_calc.py memory-split --theta-s 0.3 --theta-l 0.7 --item NAME=W_TEMPORAL,W_IMPORTANCE
   python -I <PKG>/scripts/ctx_calc.py utility --demo
   python -I <PKG>/scripts/ctx_calc.py utility --option NAME=PRICE,COMFORT,CONVENIENCE [--base 1000 --w-price 0.05 --w-comfort 10 --w-conv 15]
   python -I <PKG>/scripts/ctx_calc.py weights --weight NAME=VALUE --key NAME --feedback 1 [--up 1.1 --down 0.9 --normalize]
   ```
   (`<PKG>` = package root; from this skill, `../../`.) In `budget`, `--component`, `--chars`, and `--prefix` can repeat; `--config` accepts a JSON with the same keys; prices are per 1M tokens and YOURS. Component names (such as `sistema`/`historico` above) are free labels chosen by the user. The example values above are the user's, not from the texts.
3. Interpret the output (formula, page, and label in each subcommand):
   - `utility --demo` and `weights`: reproduce examples printed in BAAS (`[from source]`); weights and factors are arbitrary according to the book itself.
   - `memory-split`: implements the CE2 p.12 definition (`[from source]`); the paper does NOT give weight values or thresholds.
   - `budget`: package construction (`[inference]`/`[extrapolation]`); the alerts cite CE2 p.16 and p.18 (`[DATED]`, context-specific); the texts provide neither a budgeting method nor prices.

## Response format

Parameters provided, command, result with units, alerts with label and page, and a caveat that the numbers are the user's.

## Limits

It does not tokenize, does not measure real cost, and does not replace measurement with the model and provider in use. Prices change `[DATED]`.
