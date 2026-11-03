---
name: tree-rotation-simulator
description: Simulates rotate_left and rotate_right from Open Data Structures (Morin) on a sample BST and checks the in-order sequence, the parent/child pointers and the depth change (w moves up 1, u moves down 1).
allowed-tools: Bash, Read
---

# tree-rotation-simulator

Deterministic, read-only tool with no network access. Source: ODS Sec. 7.2, p.165-166 (pages = PDF; printed = N − 12).

```bash
python -I skills/tree-rotation-simulator/scripts/simulate_rotation.py --dir left --node 20
python -I skills/tree-rotation-simulator/scripts/simulate_rotation.py --dir right --node 30
```

## What is checked
- The rotation preserves the BST property (same in-order sequence) and `depth(w)` drops by 1 while `depth(u)` rises by 1 `[from source] (ODS p.165-166)`.
- Root without a parent and consistency of `parent` `[from source] (ODS p.165-166)` (the book's code handles `u` being the root).
- The number of changed fields is an experimental count `[extrapolation]`; the book does not count pointers and does not state the O(1) cost in words: `[inference]` (only a constant number of pointers change).
