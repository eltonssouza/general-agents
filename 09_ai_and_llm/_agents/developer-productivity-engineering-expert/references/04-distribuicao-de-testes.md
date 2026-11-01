# 04. Test distribution (ch. 8, DPE p.43-50)

> Boundary: test strategy, the pyramid, flaky tests in general and frameworks belong to the `software-testing-qa-expert` agent; general CI belongs to `cicd-build-automation-expert` (folder 04). Here only the book's DPE angle.

## 4.1 Why tests (p.43)
- `[from source]` Many large customers report that test execution accounts for 60% to 90% of build time; causes: more integration/functional tests, sequential execution, dependence on expensive external services (p.43). `[vendor claim]` no sample.
- `[from source]` When tests are slow, developers do not run them locally and wait for CI, which brings the effects of ch. 6 (p.43).

## 4.2 Traditional options and limits (p.43-45)
- `[from source]` **No parallelism:** implicit dependencies between tests and shared resources (e.g. the test database) make it hard; the book suggests refactoring or separating tests with and without dependencies (p.43).
- `[from source]` **Parallelism on one machine:** limited by CPU and memory; makes the developer's machine unavailable; organizations overspend on powerful workstations (example: US$ 8 million for 1,000 developers with US$ 8,000 workstations) or on CI agents costing over US$ 150 thousand, underutilized; fragility from sharing the file system and ports across JVMs (p.43-44).
- `[from source]` **CI fanout** (several CI jobs, each with a subset): fragmented reports, painful debugging with dozens or hundreds of logs, manual balancing, administrative overhead, the full build repeated per agent, and it works only in CI (requires a PR to get fast feedback) (p.44-45).

## 4.3 Capabilities of fine-grained, transparent distribution (p.45-46)
- `[from source]` Available on any invocation (local command line, CI, IDE if it delegates to the build); no change to the developer's workflow, with a single job and an aggregated report; test prerequisites run once; sequential execution per agent for more reliability; balancing by history and dynamic scheduling, with elastic agents; fallback to local execution if there are no agents (p.45-46).

## 4.4 Complementarity with cache (p.46)
- `[from source]` Cache and distribution should be used together: when almost everything comes from the cache, the impact of distribution is small; with many misses, almost all the acceleration comes from distribution; without modularization the cache helps little and distribution is very resource-intensive, hence the case for investing in modularization; together they form a virtuous cycle of frequent builds with small changes (p.46).

## 4.5 Eclipse Jetty case study (p.46-50)
- `[from source]` Project with 145 modules and ~450,000 uncommented Java lines; baseline (0): 51m35s, with 92% (47m35s) in tests (p.46-47).
- `[from source]` With 10 remote agents (DT1): 22m35s (18m37s in tests). Splitting 6 slow test classes (DT2): 20m12s (16m14s in tests). The execution unit is the test class, so a goal is never faster than its slowest class (p.47). Tests: 47m35s → 16m14s, about 3× (p.48).
- `[from source]` Small change in a private method of `jetty-client`: without distribution (C1) 39m37s (36m33s in tests); with cache + distribution (C2) 14m50s (11m50s in tests), 2.7× over C1 and 3.5× over the baseline (p.48). All tests re-run because the runtime classpath changes (p.48).
- `[from source]` With multithreaded Maven (`-T 1C`): without cache or distribution (OP) 35m27s; with both (C2P) 10m49s, 3.3× (p.49).
- `[inference]` This is the vendor's own case with the vendor's tool, on an open source project; it does not prove the same gain on other projects. The book says the degree depends on the project (p.48).

## 4.6 Conclusion (p.50)
- `[from source]` Test execution tends to dominate build time even with cache; distribution extends parallelism from one machine to many, works locally and produces a single report (p.50).
