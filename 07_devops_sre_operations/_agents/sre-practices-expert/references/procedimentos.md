# Procedures and checklists derived from the book

Each procedure marks its origin. Pages = PDF (printed = N−12). Steps the book enumerates are `[from source]`; adaptations to the user's case are `[inference]`.

## P1. Define SLIs/SLOs for a service
1. Start from what users value and work backwards to the indicators. [from source] (SRE p.48)
2. Choose a few SLIs per system type (serving, storage, pipeline, correctness). [from source] (SRE p.46)
3. Express the SLO with the measurement method and conditions (percentile, window, scope). [from source] (SRE p.48)
4. Do not use current performance as the target; avoid absolutes; start loose and tighten. [from source] (SRE p.48-49)
5. Define an internal SLO tighter than the published one; avoid overachieving the SLO by too much. [from source] (SRE p.49)
6. Compute the error budget (1 − target) and agree with the product what happens when it is exhausted (freeze releases, invest in testing/resilience); ensure SRE authority. [from source] (SRE p.25, 43, 330)
7. Track the SLI against the SLO (4-step control loop). [from source] (SRE p.49)

## P2. Decide whether a rule should page (5 questions + philosophy)
Questions: does it detect an urgent, actionable, user-visible condition (active or imminent)? will I ever be able to ignore it? is there certainty that users are affected? can I act (urgent, automatable)? have others already been paged? [from source] (SRE p.59-60). Page only if: it requires an urgent reaction, is actionable, requires intelligence and concerns a new problem (SRE p.60). Otherwise: ticket or logging. [from source] (SRE p.25-26)

## P3. Production triage (troubleshooting)
1. Record the problem (expected, actual, how to reproduce) in a bug tracker. [from source] (SRE p.106)
2. Triage: measure the impact; if severe, stop the bleeding before hunting for the root cause, preserving evidence. [from source] (SRE p.106-107)
3. Examine: metrics, logs, current state. [from source] (SRE p.107)
4. Diagnose: simplify, divide and conquer, "what touched it last". [from source] (SRE p.108-109)
5. Test and Treat: testable hypotheses; obvious first; record everything. [from source] (SRE p.110)
6. Cure and postmortem. [from source] (SRE p.111)

## P4. Manage an incident
1. Declare early (second team? customer-visible? an hour without a solution?). [from source] (SRE p.125)
2. Designate an Incident Commander; separate Ops, Communication and Planning; only Ops touches the system. [from source] (SRE p.123)
3. Open a command post and the live incident state document (App. C template). [from source] (SRE p.123-124, 332)
4. Do an explicit handoff with confirmation. [from source] (SRE p.124)
5. Close with exit criteria and start the postmortem. [from source] (SRE p.332-333, 126)

## P5. Write and review a postmortem
1. Check the triggers (downtime above the threshold, data loss, on-call intervention, resolution time, monitoring failure). [from source] (SRE p.126)
2. Use the App. D template (13 fields) — see `scripts/postmortem_tool.py`. [from source] (SRE p.334-336)
3. Write without blame; identify multiple root causes and actions. [from source] (SRE p.126-127)
4. Review with the 5 criteria; share; do not leave it unreviewed. [from source] (SRE p.127-128)

## P6. Deal with overload and cascading failure in production
Order suggested by the book in the immediate steps section (no declared ranking): increase resources, stop health check failures, restart servers with caution, drop traffic carefully and increase gradually, degraded modes, eliminate batch, eliminate bad traffic; use incident management. [from source] (SRE p.198-199)

## P7. Size a service (Ch. 2 method)
Peak load ÷ capacity per task measured in a load test = minimum tasks; add redundancy (N+1 or N+2); small regions may accept N+1 as a conscious cost decision. Example: 3,470 QPS, 100 QPS/task → 35; N+2 → 37. [from source] (SRE p.35). Use `scripts/sre_math.py provision`.

## P8. Build a sustainable on-call
Limits from the book: ≤25% of time on-call, ≥50% on engineering, 8 people at one site or 6 per site at two, ≤2 incidents per 12 h shift, response time of 5 or 30 min depending on the service. [from source] (SRE p.99-101). Measure daily tickets and paging events per shift. [from source] (SRE p.102)

## P9. Audit toil
Apply the 6 criteria to each task; separate from overhead; measure the percentage of time (quarterly survey); compare with the rotation floor (2/6, 2/8). [from source] (SRE p.51-52) Prioritization of which toil to attack: `[extrapolation]` (the book gives no method).

## P10. Backup/recovery strategy
Start from the recovery scenarios, not from the backup: how much recent data can be lost, how fast to recover, how far back in the past; retention layers; soft deletion; out-of-band validation; test recovery end to end continuously. [from source] (SRE p.248-254)

## P11. Launch safely
Checklist per topic (Ch. 27), gradual rollout with canary, feature flags, clients with backoff and jitter, load test. [from source] (SRE p.265-270)

## P12. Introduce a service to SRE
Simple PRR (6 phases) or Early Engagement; assess the importance of the service and the availability of the team. [from source] (SRE p.308-311) Objectives, limitations of Simple PRR and Early Engagement candidates: see the section "Engagement model (Ch. 32)" of `gestao-treinamento-interrupts-e-engajamento.md` (SRE p.308, 310).

## P13. Contain a cascade with a sacrificial cluster (incident #465 model)
Steps of what the book **did** (App. C-D), not a guaranteed recipe: (1) declare an incident and name an IC; (2) find the cause in the logs and prepare the fix (new index) in parallel; (3) concentrate **all** traffic on a sacrificial cluster so the others recover while instances come up; (4) increase capacity **checking the math** (the board's 2x was off by an order of magnitude; 10x was needed); (5) reintroduce traffic in steps of 1%, 10%, 30%, 50% and 100% observing errors and task failures; (6) close the incident only after 30 minutes of nominal performance. [from source] (SRE p.332-335). Adapting to other systems is [inference].

## P14. Estimate the RAM of a Borgmon-style time-series monitor
RAM ≈ series × (horizon ÷ collection interval) × 24 B per point [derived from the book's example: 1 million series × 12 h at 1 min < 17 GB]; choose the horizon to fit the investigation of an incident (the book justifies 12 h as a "magic number"); anything older goes to external storage (TSDB). The 24 B is a 2016 number and the book does not detail the label overhead. [from source] (SRE p.90-91, 98)

## P15. Decide whether automating a failover is worthwhile (Decider reasoning)
(1) Estimate the human time per failover and how many per week; (2) convert to availability (30-90 min per failover is infeasible for a demanding SLO); (3) compute how much downtime per failover the error budget accepts (in the case, <30 s); (4) if the human procedure cannot get there, automate; (5) count the cost: applications now need more fault-tolerance logic (custom JDBC). [from source] (SRE p.66-67); the generalization is [inference].

## P16. Push a global configuration safely (lessons from the Change-Induced case)
Full canary **regardless of perceived risk** (SRE p.118); exercise rare keyword combinations with the new functionality; fast, already-tested rollback (p.117, 118); alerts that do not flood the channels; alternative access tools and out-of-band communication; do not count on the luck of someone watching channels in real time (p.118). Steps as a checklist are [inference].

## P17. Answer "does the book cover this?" (three-level lookup)
`python -I scripts/sre_lookup.py "<term>"`: **COVERED** (the term is, as a whole word, in the body of a package summary that cites a page), **POINTER ONLY** (the book has the term on pages X, but the package does not summarize it: say so and do not invent content), **NOT COVERED** (curated list of things outside the book or no occurrence in the book's index). Only assert "the book does not carry it" at the third level; at the first two cite the pages.
