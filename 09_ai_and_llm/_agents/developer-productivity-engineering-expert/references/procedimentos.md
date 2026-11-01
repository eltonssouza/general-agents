# DPE procedures

Each step indicates its origin: `[from source] (DPE p.N)` or `[inference]` (organization of the steps by the package, from the cited pages). They are not an official process of the book.

## P1. Build the business case (p.19, 24, 78-84)
1. Gather own data: local builds/day, CI builds/day, average times, failure rates, cost per minute or per engineer-year (p.78-79, 90).
2. Apply the cost model (`dpe_cost.py example|total`) and label the book's assumptions as an example (p.78).
3. Estimate savings = cost per minute × minutes saved × builds per year (p.19) and compare with tool and team cost `[inference]`: the book provides no payback.
4. Declare the vendor bias and test sensitivity (±) `[inference]`.

## P2. Diagnose slowness (p.51-53, 56-57)
1. Instrument local and CI builds (p.53-54).
2. Measure the median and percentiles (P5, P25, P75, P95) of build time per week (p.56).
3. Look for causes of the ABP–MABP gap: parallelism turned off, large module on the critical path, cache with misses, non-reproducible output, memory, I/O, latency, large test classes (p.52).
4. Compare builds with a hit and a miss to find inputs that differ (p.57).

## P3. Introduce build cache (p.34-42, 58)
1. Check modularization (leaf modules, unstable modules) (p.41, 52).
2. Eliminate volatile inputs and sources of non-reproducibility (p.41-42, 68-69).
3. Local + remote cache: CI writes, everyone reads (p.40).
4. Monitor node bandwidth and storage (p.41) and hit rate per action (p.53-54); standardize toolchains (p.57).
5. Do not treat it as "fire and forget" (p.58).

## P4. Speed up tests (p.43-50)
1. Measure the fraction of time spent in tests (p.43, 47).
2. Remove implicit dependencies and shared resources; separate tests with and without dependencies (p.43).
3. Prefer transparent distribution over CI fanout when available; consider splitting slow classes (p.45, 47).
4. Combine with cache and modularization (p.46).

## P5. Triage a build failure (p.60-65, 71)
1. Classify: verification vs non-verification (p.60).
2. Compare with the last successful build (inputs and environment) (p.65).
3. Check history: is it the first occurrence? is it flaky? does it affect others? (p.64).
4. Prioritize the failure list in the book's order (p.71).

## P6. Flaky test program (p.73-76)
1. Collect all failures and rank tests and causes (p.67, 75).
2. Measure the rate of developer builds impacted; target < 1% (p.74); use P_pass (p.74).
3. Retry in another order, in isolation and in another environment to classify (p.73-74).
4. Quarantine so as not to block; Fix-It Days (p.75).
5. Confirm with history that there has been no flakiness since the fix (p.76).

## P7. Culture and operation of the DPE team (p.17, 19-20, 55-56, 70)
1. Dedicated team with its own goals and metrics (p.19).
2. Be proactive, not complaint-driven (p.55, 70).
3. Make the team's impact visible with data (p.56).
4. Explicit culture of continuous improvement (p.17).
