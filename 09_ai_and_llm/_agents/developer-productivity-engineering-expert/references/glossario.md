# DPE glossary (terms from the book; PDF pages)

| Term | Meaning according to the book | Page |
|---|---|---|
| DPE (*Developer Productivity Engineering*) | Engineering practice (automation, data, acceleration) to maximize developer productivity and happiness | 14 |
| DPM (*Developer Productivity Management*) | Approach centered on people and activity metrics | 14, 21 |
| Toolchain | The set of tools that assembles, verifies and delivers the software (IDE, build, tests, CI, caches, repositories) | 17, 52 |
| Feedback cycle | Time between changing the code and knowing the build/test result | 28 |
| Creative flow | State of concentration that depends on a fast and correct response from the toolchain | 15, 29 |
| Build cache | Cache of build actions (tasks/goals) indexed by a hash of the inputs | 34, 36 |
| Dependency cache / binary repository | Cache of dependency binaries between repositories; different from the build cache | 34 |
| Local / remote cache | Local directory vs output shared by the organization | 40 |
| Cache key | Hash of an action's inputs | 36 |
| Compile avoidance / ABI | The compile key considers only the public API (visible binary interface) | 38, 48 |
| Volatile input | Input that changes on every run (timestamp) and prevents a cache hit | 41-42 |
| Leaf module | Module that no other module depends on | 41 |
| Test Distribution | Fine-grained, transparent distribution of tests across remote agents | 43, 45 |
| CI fanout | Several CI jobs, each with a subset of tests | 44 |
| MABP | Maximum build performance achievable by the stack | 51 |
| ABP | Actual build performance | 51 |
| Build Scan | Vendor's per-build report with inputs, timings, cache and failures | 57, 64 |
| Verification failure | The build detects a real problem in the code | 60 |
| Non-verification failure | Failure of the build software/environment/services (build logic, repositories, environment, external services) | 60 |
| MTTR | Mean time to repair/resolve | 14, 61 |
| Reproducible build | Same output whenever the declared input does not change | 68 |
| Reliable build | Low rate of non-verification failures (a concept distinct from reproducible) | 66, 68 |
| Flaky test | Passes and fails for the same code | 73 |
| Flaky quarantine | Secondary process that runs flaky tests without blocking integration | 75 |
| Flaky Fix-It Day | Day dedicated by the whole team to fixing flakiness | 67, 75 |
| Complaint-driven development | Prioritizing only what generates complaints | 70 |
| Shift right of feedback | Postponing feedback to later stages | 32 |
| CM, DE, CE, BL, BCI, DW, BYL, BYCI | Cost model parameters (cost per minute, working days, cost per engineer-year, local/CI builds per day, office days, builds per year) | 78 |
| WL, WCI | Fraction of unproductive waiting in local/CI builds | 79 |
| FL, FCI, IL, ICI, TL, TCI | Failure rate, investigation rate and investigation time (local/CI) | 81, 82 |
| P_pass | Probability of a run with no flaky failure = Π(1 − P_flaky) | 74 |
