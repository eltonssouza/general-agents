# 05. Performance profiling and analytics (ch. 9, DPE p.51-58)

## 5.1 MABP vs ABP (p.51-52)
- `[from source]` Almost no organization has an actionable view of toolchain performance and reliability (p.51).
- `[from source]` **MABP** (*Maximum Achievable Build Performance*) is the maximum build performance as a function of the technology stack (e.g. Scala has a lower MABP than Java because of the compiler; Gradle has a higher MABP than Maven). **ABP** (*Actual Build Performance*) is the real performance; most of the DPE benefit comes from reducing the ABP–MABP gap, but DPE also seeks to raise the MABP, since ABP never exceeds MABP (p.51).
- `[from source]` Cache and test distribution would raise the MABP "by an order of magnitude" for any supported build system and mitigate differences between technologies (p.51-52). `[vendor claim]`.
- `[inference]` MABP and ABP are concepts from the book, not standardized metrics; the book defines neither a unit nor a procedure for computing the MABP.

## 5.2 Where ABP falls below MABP (p.52-53)
- `[from source]` Scenarios: Maven/Gradle parallelism not used; parallelism with low utilization because of a large module on the critical path; ineffective cache because of modules that change a lot; non-reproducible output; under- or over-allocated memory; slow I/O (antivirus, disks); slow annotation processors; large test classes limiting distribution; high latency to caches (new office) (p.52).
- `[from source]` The toolchain has complex, ever-changing inputs (IDE, build, tests, CI, disks, cache nodes, binary manager); dependency download time in CI is often a bottleneck and almost nobody measures it (p.52). No one in the author's account knew how much of the compile time came from an annotation processor (p.53).
- `[from source]` Anecdote: at one customer, generating the jars took 40 minutes in CI and 1-2 minutes locally; the difference was the disk (local SSD); replacing the CI disks gave a large speedup (p.53).
- `[from source]` The data serve two purposes: seeing trends and pathologies; finding the root cause (chemical plant analogy) (p.53).

## 5.3 Instrumentation (p.53-54)
- `[from source]` Collect data from every toolchain run with four goals: monitor ABP metrics and trends; drill into any past run; compare profiles with different inputs to find the cause of a regression or improvement; monitor low-level pathologies (e.g. cache hit rate per action) (p.53-54).
- `[from source]` Without data it is almost impossible to find irregular performance problems ("flaky performance") (p.54).
- `[from source]` Insurance company anecdote: local builds of over 20 minutes versus under 1 minute in CI, by developers working from home using a network share as the output directory; it was only seen after collecting data from the developers' machines too (p.54).
- `[from source]` "Even the experts get it wrong" anecdote: in a cache test, the "after" build seemed 5× slower; the comparison via Build Scan showed 128 threads before and 1 after, caused by a `.mvn` directory in the parent with `maven.config` (p.55). Stated lesson: we trust too much in what we think we configured (p.55).

## 5.4 Dev vs infrastructure collaboration and a proactive stance (p.54-56)
- `[from source]` Performance regressions go unnoticed (small increases) or are not reported because reporting takes effort; reports without complete data do not lead to a fix; only severe regressions escalate (p.54).
- `[from source]` Toolchain teams tend to be incident-driven; they should be proactive (analogy: online store and load time) (p.55). Workshop exercise: the codebase grows 30% and the build gets 10% faster; "nobody" notices; for 100 developers it would be savings of millions per year (p.56). `[vendor claim]` value not derived in the text.

## 5.5 Analytics and percentiles (p.56-57)
- `[from source]` Pick one aspect at a time (e.g. reduce the fraction of very slow builds). To close the ABP–MABP gap, the example proposes bringing the build time **median** close to the 5th percentile; the median is used because the mean is distorted by outliers; collect data for weeks to normalize hourly and daily variations (p.56).
- `[from source]` A chart from a streaming service's team shows the median and P25-P75 and P5-P95 bands (p.56-57; image cannot be extracted).

## 5.6 Build Scan as profiling (p.57-58)
- `[from source]` The Build Scan shows build inputs, the impact of each execution unit, and where the cache hit or missed and why; one starts with the longest unit and walks the input graph. Example: comparing scans with a hit and a miss, one discovers that the toolchain binaries differ (JVMs from different vendors), motivating standardizing the toolchain (p.57).
- `[from source]` "Not fire and forget": infrastructure that turns on the cache and does not invest in tools to tune it sees the ABP stay low for months; accelerating without management can produce negative savings; a working cache is "one of the cheapest and tastiest lunches", but it is not free (p.58).
- `[vendor claim]` Build Scan is described as the "de facto standard" elsewhere (p.64); it is a Gradle product.
