# Delivery metrics and performance levels (DORA24)

Convention: `(DORA24 p.N)` = PDF page (= printed number). Paraphrase; not the report's text.

## 1. The four keys (p.9-10)

- The report presents four software delivery metrics, "the four keys", repeatedly validated by DORA, to measure the outcomes of the delivery process (DORA24 p.9). [from source]
- They measure throughput and stability of changes, and apply to any kind of change, including configuration and not just code (DORA24 p.10). [from source]
- Definitions (DORA24 p.10) [from source]:
  - **Change lead time**: time between a commit/code change and its successful deploy to production.
  - **Deployment frequency**: how often application changes are deployed to production.
  - **Change fail rate**: percentage of deploys that cause failures in production and require a hotfix or rollback.
  - **Failed deployment recovery time**: time to recover from a deploy that failed.
- The metrics typically move together: the best do well on all four, the worst do poorly on all four (DORA24 p.10). [from source]
- Note 1 (p.16): only a deploy that causes a problem after reaching production, where users can feel it, counts as a change failure; a change blocked along the way is seen as a demonstration that the deploy process detects errors (DORA24 p.16). [from source]
- Terminology: the report writes "change lead time" and "failed deployment recovery time". It does not use the acronym MTTR, nor "time to restore", nor "lead time for changes" (0 occurrences in the text). If the user uses names from earlier editions or from tools, treat the equivalence as [inference] and [DATED]. [inference]

## 2. The fifth metric: rework rate and the two factors (p.11-12)

- Historically, the failure rate was the "outlier" metric: strongly correlated with the other three, but statistical tests did not allow merging the four into a single factor; changing the wording of the question helped, but did not solve it (DORA24 p.11). [from source]
- Old hypothesis: the failure rate works as a proxy for the volume of rework the team has to do. To test it, the 2024 survey added a question about unplanned deploys made to fix a user-visible bug in the last six months (DORA24 p.11). [from source]
- Result: rework rate and failure rate are related, and together they form a reliable factor of **delivery stability** (DORA24 p.11). [from source]
- More than half of the teams in the study show differences between throughput and stability, which led to treating delivery performance through two factors (DORA24 p.11). [from source]
- Map (DORA24 p.11-12) [from source]:
  - **Software delivery throughput**: change lead time, deployment frequency, failed deployment recovery time. Measures the speed of making updates of any kind, normal or in response to failure.
  - **Software delivery stability**: change failure rate and rework rate. Measures the likelihood that deploys generate additional, immediate, unintended work.
  - The **software delivery performance** concept uses the five metrics; the report uses the concept and the two factors depending on the analysis (DORA24 p.12).
- Note: the cluster analysis (levels) was done on the four original metrics, for consistency with prior years (DORA24 p.13). Therefore **there is no per-level range for rework rate**: benchmark NOT COVERED. [from source] + [inference]

## 3. 2024 levels (clusters) (p.13-15)

Method (DORA24 p.13): questions about the respondent's main application/service; cluster analysis identifies responses similar to each other and distinct from the rest; the levels **are not defined in advance, they emerge from the responses**; it gives an annual snapshot. Four clusters emerged in 2024. [from source]

| Level | Change lead time | Deployment frequency | Change fail rate | Failed deployment recovery time | % of respondents (UI 89%) |
|---|---|---|---|---|---|
| Elite | < 1 day | on demand (multiple deploys per day) | 5% | < 1 hour | 19% (18-20%) |
| High | 1 day to 1 week | 1/day to 1/week | 20% | < 1 day | 22% (21-23%) |
| Medium | 1 week to 1 month | 1/week to 1/month | 10% | < 1 day | 35% (33-36%) |
| Low | 1 month to 6 months | 1/month to 1/6 months | 40% | 1 week to 1 month | 25% (23-26%) |

Source: DORA24 p.13 [from source]. Correct readings of the table:
- Failure rate is one value per cluster, not a range; the **Medium (10%) cluster is more stable than High (20%)** and slower (DORA24 p.13-14). [from source]
- High and Medium have the same recovery range (< 1 day). Between 1 day and 1 week of recovery the table says nothing: a gap. [inference]
- Figure 1 (p.14) illustrates the clusters on axes per metric; the failure rate scale goes from ~10% to 50%. [from source]

### Throughput or stability? (p.14)
- In all clusters, throughput and stability are correlated, including in Medium, where throughput is lower and stability higher than in High; this suggests other factors influencing the cluster (DORA24 p.14). [from source]
- "Which is better: more frequent deploys or fewer failures?" There may be no universal answer: it depends on the application, the team's goals and, above all, the users' expectations (DORA24 p.14). [from source]
- Labeling the fast ones as "high" and the slower but stable ones as "medium" is a decision that exposes a trap of the levels: **improving matters more than reaching a level; the best teams are those of elite *improvement*, not necessarily elite *performance*** (DORA24 p.14; repeated p.15). [from source]

### Elite vs Low (p.15)
Compared with Low, the Elite cluster has: 127x faster lead time, 182x more deploys per year, 8x lower failure rate, 2293x faster recovery (labels checked on the image; the order in the extracted text is different) (DORA24 p.15). [from source] The report does not explain how the ratio was calculated; 8x is consistent with 40%/5% from the table. [inference]

### Industry (p.15)
The research rarely finds that industry predicts delivery performance; there are high-performing teams in all verticals. Note 3: the 2019 report found significantly better performance in retail (DORA24 p.15-16). [from source]

### How to use the clusters (p.15)
They are benchmark data from the year's survey, to inspire the idea that the elite level is achievable; more important than reaching a level is improving overall performance (DORA24 p.15). [from source]

## 4. How to use the metrics day to day (p.7, 16, 74)

The report's recipe (DORA24 p.16): [from source]
1. Choose the main application/service to measure and improve.
2. Bring together the responsible cross-functional team, measure and agree on current performance (the DORA Quick Check, dora.dev/quickcheck, helps drive the conversation and the baseline).
3. Understand what prevents improvement, e.g., with a value stream mapping exercise.
4. Agree on a plan; it may target one of the capabilities researched by DORA or something specific to the application/organization.
5. Execute, reserving dedicated capacity, and record learnings.
6. After the change settles, reassess the four keys; repeat.
- Change does not happen overnight; it requires a learning climate, fast flow and fast feedback (DORA24 p.16). [from source]
- The 7-step experimental cycle from the summary (p.7): choose area/outcome, measure baseline, formulate hypotheses, agree on a plan, do, measure progress, repeat (DORA24 p.7). [from source]
- Ways of measuring cited (p.79): conversations and reflection in team meetings, DORA Quick Check, commercial and open-source tools in the Software Engineering Intelligence category, custom integrations (DORA24 p.79). [from source]

### Discouraged uses (p.74) [from source]
- Apply the four keys at the **application/service** level, not the organization or business line.
- Use them to visualize continuous improvement effort, **not to compare teams, and certainly not individuals**.
- **Do not use them as a maturity model**; being low/medium/high/elite is interesting, but these labels have little value in the transformation journey (DORA24 p.74).
- Think beyond the four keys: user feedback metrics are as important as they are, because most teams have already found reasonable speed/stability solutions and gains diminish when high performance becomes common (DORA24 p.74). Dashboards combining technical metrics (four keys, reliability) and business metrics are recommended (DORA24 p.74).

## 5. Relationship with operational and organizational performance (p.80, p.59)
- Operational performance (studied since 2018) measures the ability to make and keep promises about the product/service; the best results come when delivery and operations join forces to drive organizational performance and well-being; the diagram uses the four keys, reliability and SLOs (DORA24 p.80). [from source]
- 2024 caveat: with high user focus, product quality does not require high throughput/stability; with low focus, fast and stable delivery is the only path to product quality (DORA24 p.59-60). [from source]

## 6. Outside the collection
Target MTTR/SLO values, instrumenting the metrics in pipelines, operational definitions of "deploy" per technology, detailed technical capabilities (CI/CD, trunk-based etc.): the report only points to dora.dev (p.16, p.74); all of this is [extrapolation] or NOT COVERED.
