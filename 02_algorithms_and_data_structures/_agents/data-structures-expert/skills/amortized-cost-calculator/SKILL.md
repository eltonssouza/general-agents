---
name: amortized-cost-calculator
description: Calculates and simulates the resize cost of the ArrayStack (the book's rule, the Lemma 2.1 bound), the space of the RootishArrayStack (block/position of an index, waste bounds) and the space of the SEList, following Open Data Structures (Morin). Additive growth is only a demonstration [extrapolation].
tools: Bash, Read
---

# amortized-cost-calculator

Deterministic, read-only tool with no network access. Source: ODS Chs. 2 and 3 (pages = PDF; printed = N − 12).

```bash
python -I skills/amortized-cost-calculator/scripts/calculate_amortized.py --mode resize --n 1000 --growth geometric
python -I skills/amortized-cost-calculator/scripts/calculate_amortized.py --mode resize --n 1000 --growth additive --chunk 10
python -I skills/amortized-cost-calculator/scripts/calculate_amortized.py --mode rootish --n 100000 --index 5000
python -I skills/amortized-cost-calculator/scripts/calculate_amortized.py --mode selist --n 10000 --b 100
```

## What comes from the book and what does not
- Geometric `resize`: doubles to `max(1, 2n)` when full; the bound `sum n_i ≤ 2m + 2r` is Lemma 2.1 `[from source] (ODS p.45, 47-48)`.
- Additive `resize`: the book does not analyze it; the quadratic result is `[extrapolation]`.
- Rootish mode: block `b = ⌈(−3 + √(9+8i))/2⌉`, position `j = i − b(b+1)/2` `[from source] (ODS p.64)`; blocks `r ≤ (3+√(1+4n))/2` and waste ≤ 2r−1 `[from source] (ODS p.67)`.
- `selist`: up to `n/(b−1) + 1` blocks, wasted space O(b + n/b) `[from source] (ODS p.81, 89)`.
To simulate sequences with removals and check the lemmas, use `scripts/structure_simulator.py`.
