---
name: ifa-cost-calc
description: Compares the count of traversal operations with index-free adjacency (IFA, O(1) per relationship) and with index lookup (O(log n)), and shows Table 2-1 of the book Graph Databases. Use when the user asks "why does Neo4j traverse relationships in constant time?", "how much does a d-level traversal cost?" or wants IFA vs index numbers. Do not use it to predict real query time.
---

# Traversal cost: IFA against index

Sources: NEO4J p.168–170 (O(m) against O(m log n)) and Table 2-1 (p.38–39), PDF pages (printed = N − 18).

## Procedure

1. Run the calculation (read-only, no network):
   ```bash
   python -I <PKG>/scripts/ifa_cost_calc.py -N 1000000 -d 3 -k 50 [--fanout 100]
   python -I <PKG>/scripts/ifa_cost_calc.py --steps 1000 -N 1000000
   python -I <PKG>/scripts/ifa_cost_calc.py --table21
   ```
   (`<PKG>` = package root; from this skill, `../../`.)
2. Label what comes out:
   - O(1) per step with IFA, O(log n) with an index, O(m) against O(m log n): `[from source]` (p.168).
   - the k^d variant (visited nodes = sum of k^i) is `[inference]`; the index fan-out (log base) is an `[extrapolation]` parameter, since the book does not mention B+ trees.
   - the computed ratio is a counting model, not measured time. The measured times are in Table 2-1 (`--table21`) and are old data `[DATED]`.

## Response format

Parameters used — IFA count — index count — ratio — labeled caveats — pages.

## Limits

Does not replace measurement with representative data (NEO4J p.109–113). Costs of Neo4j's current storage are not in the book.
