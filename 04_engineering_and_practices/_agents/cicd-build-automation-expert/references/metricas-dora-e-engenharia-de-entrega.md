# Delivery metrics (DORA) and what the sources actually bring

Convention: `(SIGLA p.N)` = **PDF** page. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Audit verdict
**None of the four sources in this package defines the DORA metrics or brings Elite/High/Medium/Low bands.** The CICD pages that v1 cited for this (p.5-15) are in fact a **survey on TDD, BDD, SOLID and microservices** (CICD p.5-18), and the SWE-G pages it cited (p.465-475) do not exist in the 408-page PDF. V1 brought definitions, a "maturity matrix" (for example, Elite with lead time under 1 hour and failure rate of 0% to 15%) and a list of "five enablers", all marked `[from source]`. Those numbers and definitions were **removed as `[from source]`**. Where they still appear, they are `[extrapolation]` with the origin declared.

## 2. What the sources say about delivery metrics
- The DZone report mentions, in passing, "another recent survey" that measured continuous delivery maturity by objective metrics (deploy frequency, lead time, MTTR, change failure rate etc.); **in this survey**, instead, respondents rated their own "delivery continuity" on a slider. There is no definition or band. `[from source]` (CICD p.16)
- Result of this self-assessment (correlation, n=584): among those who gave 75-100% continuity, 65.7% said deploys "rarely" cause incidents/rollbacks, versus 52.2% (50-75%) and 44.7% (25-50%). `[from source]` (CICD p.17)
- Report caution: without complementary feedback loops, a high release frequency does not improve the software; organizations that release "too fast" and "too slow" both report a lot of technical debt; the optimal perceived speed correlates with the optimal technical debt. `[from source]` (CICD p.13)
- Data cited by a sponsor (Armory) from the "2021 State of Continuous Delivery" report, with 19 thousand developers: almost two thirds reported that code takes **a week or more** from commit to production; 69.1% ship to production **at least once a week**; more than half take **a day or more** to fix an unplanned outage; almost 20% of companies take **more than a month** to restore services. `[from source]` (CICD p.34-35) Sponsor content; not DZone research.
- Another sponsor (CloudBees): Capital One automated 90% of the pipeline and deploy frequency rose 1,300%; Autodesk reportedly saw 10x in productivity. `[from source]` (CICD p.27) Promotional content; no method described.
- SWE-G: "faster is safer" (small changes and frequent releases improve quality and cost) `[from source]` (SWE-G p.347, 353). The CI chapter cites *Accelerate* (Forsgren et al., 2018) as proof of the benefits of CI, in a footnote `[from source]` (SWE-G p.346), and uses the expression "MTTCU" (*mean time to clean up*) for the time to close bugs after the fix, "in DevOps terms" `[from source]` (SWE-G p.344). The book does **not** define the four metrics.

## 3. DORA itself `[extrapolation]`
The DORA (DevOps Research and Assessment) program and its four metrics (deploy frequency, change lead time, recovery time and change failure rate) are general knowledge outside these sources. The bands per level change with each edition of the report and **are not fixed thresholds**.

Audited reference available in the user's collection: the `dora-devops-delivery-expert` package (DORA 2024 report, p.13) brings these 2024 clusters `[extrapolation]`, **not coming from the sources of this package**:

| 2024 level | Change lead time | Deploy frequency | Failure rate | Failed deployment recovery |
|---|---|---|---|---|
| Elite | less than 1 day | on demand (several per day) | 5% | less than 1 hour |
| High | 1 day to 1 week | 1/day to 1/week | 20% | less than 1 day |
| Medium | 1 week to 1 month | 1/week to 1/month | 10% | less than 1 day |
| Low | 1 month to 6 months | 1/month to 1/6 months | 40% | 1 week to 1 month |

Correct readings `[extrapolation]`: the failure rate is a value per cluster, not a band (Medium, 10%, is more stable than High, 20%); the clusters emerge from the year's data and are **not** a maturity model; the report uses the name "failed deployment recovery time" and not "MTTR". Consult the DORA package for statistical limits.

### v1 numbers with NO basis
- "Elite: Lead Time < 1 hour" (DORA 2024: less than 1 day).
- "Elite: CFR 0-15% (typically < 5%)", "High: 15-20%", "Medium: 21-30%", "Low: > 30%" (DORA 2024: 5%, 20%, 10%, 40%, per cluster).
- "Elite MTTR < 1 hour; High < 1 day; Medium 1 day to 1 week; Low > 1 week" (DORA 2024: High and Medium < 1 day; Low 1 week to 1 month).
- Frequency "Low < 1 time per month", "Medium 1/month to 1/week" (DORA 2024 defines Low as 1/month to 1/6 months).
- Overall classification by average points ("DORA score"): nonexistent in the sources and discouraged by the DORA 2024 report, which says not to use it as a maturity model `[extrapolation]`.
- "Five mandatory pillars" to reach Elite: no source brings this list.

## 4. How to measure (package procedure, `[extrapolation]`)
Simple operational definitions, per application/service: frequency = successful deploys to production in the period; lead time = time from commit to deploy in production; recovery = time from failure to restoration; failure rate = deploys that required a fix or rollback divided by the total. Record the time window. `scripts/dora_evaluator.py` does the calculations and compares them with the table above (labeled) and with the CICD survey numbers (p.34-35).
