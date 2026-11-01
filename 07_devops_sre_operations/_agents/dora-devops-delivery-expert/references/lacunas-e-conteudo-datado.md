# Collection gaps and [DATED] content

## 1. What the report does NOT cover (use "NOT COVERED" or [extrapolation])
- A list and detailed description of the DORA capabilities (CI/CD, trunk-based, test automation, etc.): there are only pointers to dora.dev/capabilities (DORA24 p.16, p.74; links in the notes on p.56). The report states there are more than 30 capabilities (p.74), without listing them.
- MTTR/"time to restore"/"lead time for changes" terminology: does not appear (0 occurrences); the report uses "failed deployment recovery time" and "change lead time".
- Benchmark ranges for rework rate (only the 4 original metrics entered the clusters, p.13).
- Recovery interval between 1 day and 1 week in the levels table (p.13).
- Numeric effects of leadership/user-centricity on delivery metrics, except what is in the figures; numeric effect of stable priorities (direction only).
- Technologies, tools, architectures (Kubernetes, microservices, Backstage, observability, SBOM, canary, chaos): not covered.
- Reliability/SLO metrics in detail: mentions only (p.55, p.74, p.80).
- ROI formulas (2020 whitepaper cited p.72, p.78).
- Ideal batch size, PR limits, specific AI policies: the report recommends small batches and policies, without numbers.
- Raw data, sample weights, N per analysis, response rate, full effect size and numeric intervals: not published in the PDF (only figures and point %).

## 2. [DATED]
- The entire report is from 2024 (v. 2024.3; check for a newer version at dora.dev/vc/?v=2024.3, p.117). AI adoption, trust, interface and task numbers reflect early 2024 (p.22) and may be outdated. [DATED]
- Levels (clusters) change every year (p.13): the 2024 values do not hold as a permanent standard. [DATED]
- The inclusion of rework rate (p.11) and the throughput/stability split are the 2024 position; later editions may have revised them. [DATED]
- "DevOps" tends to leave the spotlight in DORA's terminology (p.82). [DATED]
- Tools/links (dora.dev/quickcheck etc.) may have changed.

## 3. Small internal inconsistencies observed (so they are not propagated)
1. Productivity with leadership: text p.71 says 9%; figure 18 (p.72) shows 8.7%.
2. Platform and age: text p.51 speaks of "productivity", the axis of figure 14 (p.50) is organizational performance.
3. AI factor: p.30 says "seven items" but lists six tasks (probably counting the overall item).
4. Order of the Elite vs Low comparison labels in the text extraction (p.15) differs from the image; the image is the reference.
5. The failure rate term appears as "change fail rate" (p.10) and "change failure rate" (p.11).
