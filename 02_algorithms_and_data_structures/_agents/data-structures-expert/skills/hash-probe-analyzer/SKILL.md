---
name: hash-probe-analyzer
description: Simulates the LinearHashTable of the book Open Data Structures (entries data, nil and del; invariant length(t) >= 2q; resize by the book's rules) and demonstrates why deleting by writing nil instead of del produces a false negative.
allowed-tools: Bash, Read
---

# hash-probe-analyzer

Deterministic, read-only tool with no network access. Source: ODS Sec. 5.2 (pages = PDF; printed = N − 12).

```bash
python -I skills/hash-probe-analyzer/scripts/analyze_hash_probes.py --demo tombstones
python -I skills/hash-probe-analyzer/scripts/analyze_hash_probes.py --demo naive_failure
python -I skills/hash-probe-analyzer/scripts/analyze_hash_probes.py --demo invariant
```

## Encoded rules and their origin
- Three kinds of entry (data, `nil`, `del`) and counters `n` and `q` (data plus `del`) `[from source] (ODS p.121)`.
- Invariant `length(t) ≥ 2q`; `add` resizes if `2(q+1) > length(t)`; `remove` resizes if `8n < length(t)`; `resize` uses the smallest `d` with `2^d ≥ 3n` and sets `q = n` `[from source] (ODS p.121-123)`.
- The simulator's hash function is `x mod length(t)` (didactic) `[extrapolation]`; the book uses multiplicative hashing (ODS p.116).
- The false negative of naive removal is an `[inference]` from the argument of ODS p.123 (no operation in the book writes `nil` over a previously occupied cell). The term "tombstone" is an external label.
