# Cases and antipatterns

Cases reported by the book are **vendor anecdotes** (no verifiable data); use them as illustration, not as evidence. Pages = PDF.

## Cases from the book
| Case | Lesson `[from source]` | Page |
|---|---|---|
| Team of 6 devs with a 1 min build vs team of 11 with 4 min | faster builds, more builds | 28-29 |
| Jetty (145 modules): 51m35s → 14m50s with cache + distribution | combine cache and distribution | 46-49 |
| CI took 40 min to generate jars; local 1-2 min | measure; the cause was the disk | 53 |
| Insurance company: local build 20 min vs CI < 1 min | dev machine data reveals differences (network share) | 54 |
| Cache "5× slower": 128 threads vs 1 | compare builds with data, not assumptions | 55 |
| Gradle 2016: < 3% of changes passed without flaky | visibility + fix-it days | 67 |
| Local Tomcat with no version in the name | cache reveals non-reproducibility | 69 |
| 30 devs suffering in silence | telemetry instead of complaints | 70 |
| 1 in 40 local builds failed (IntelliJ) | failure dashboard finds what nobody reported | 72 |
| Antivirus: 39 s per build x 1.3 mi builds ≈ 8 eng-years | quantify to decide | 80 |

## Antipatterns
| Antipattern | Why (book) | Page |
|---|---|---|
| Shifting feedback to the right (fewer local tests) | compounding effects closer to production | 32-33 |
| Long builds "to save" | accumulate changes, failures and investigations | 82 |
| Turning on the cache and forgetting it | low ABP; negative savings | 58 |
| Volatile inputs (timestamp in jar) | cache never hits | 41-42 |
| Marking the test as passing if it passed on retry | flakiness grows and blocks again | 74 |
| Just deleting flaky tests | drops coverage (objection) | 75 |
| Prioritizing only those who complain | many stay silent; talent leaves | 55, 70, 84 |
| CI fanout as the definitive solution | fragmented reports, no local feedback | 44-45 |
| CI teams optimizing auditability without looking at productivity | adverse effect on devs | 17 |
| Buying huge workstations/agents for tests | underutilization and cost | 44 |
| Using individual activity metrics as evaluation (DPM) | can be counterproductive | 22-23 |

## Antipatterns in using the book itself `[inference]`
- Quoting "50%-90% savings" or "hard ROI" as a promise for the user's case.
- Applying the example's numbers (US$ 1/min, 80% waiting) without own data.
- Applying the book to non-JVM stacks without checking tooling support (p.25).
