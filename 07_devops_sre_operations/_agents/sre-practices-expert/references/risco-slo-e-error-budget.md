# Risk, SLI/SLO/SLA, availability and error budget (Ch. 3, 4, App. A, App. B)

Pages = PDF (printed = N−12).

## Risk (Ch. 3)
- Past a certain point, more reliability makes the service worse: it limits feature velocity and raises cost; users do not notice the difference because their experience is dominated by less reliable components (e.g., the cellular network). [from source] (SRE p.37)
- Cost is not linear: one increment can cost 100x the previous one; two cost dimensions: redundant resources and opportunity cost. [from source] (SRE p.37)
- Principle: "reliable enough, but no more reliable than needed"; the goal is a minimum and a maximum at the same time. [from source] (SRE p.37)
- The book focuses on **unplanned downtime**, expressed in nines; each additional nine is an order of magnitude toward 100%. [from source] (SRE p.38)

## Formulas the book gives (p.38, formulas are images; checked visually)
- Time-based availability = uptime / (uptime + downtime). [from source] (SRE p.38)
- Aggregate availability (by requests, rolling window, e.g., one day) = successful requests / total requests. [from source] (SRE p.38)
- Examples from the text: 99.99% per year allows 52.56 min of downtime; 2.5M requests/day with a daily target of 99.99% allow up to 250 errors. [from source] (SRE p.38)
- At Google the time-based metric usually makes no sense (global services, almost always partially "up"); the success rate (yield) is used. Targets are quarterly, tracked weekly or daily. [from source] (SRE p.38)
- Error budget = 1 − availability target (99.99% → 0.01% budget). [from source] (SRE p.25; p.330)
- Example: SLO of 99.999% of queries per quarter → budget of 0.001%; a problem that fails 0.0002% of queries consumes 20% of the quarter's budget. [from source] (SRE p.43)
- Cost example: 99.9% → 99.99% = +0.09%; with $1M of revenue, that is worth $900; it only pays off if the extra nine costs less than that. [from source] (SRE p.40)
- Heuristic: use the background error rate of ISPs (measured between 0.01% and 1%) as a noise floor. [from source] (SRE p.40) [DATED]

## Risk tolerance
- Consumer: questions (expected level, link to revenue, paid/free, competitors, consumer/enterprise); the type of failure matters (constant low rate vs total outage); cost is a key factor; other metrics (latency) give degrees of freedom. [from source] (SRE p.39-40)
- Infrastructure: infrastructure has several customers with different needs; making it ultra-reliable for all of them is usually too expensive. Bigtable example: consumer services that serve data on the user's request want low latency and high reliability; offline analytics teams (MapReduce) want throughput. What each one wants from the **request queue**: the low-latency user wants the queue (almost) always **empty**, to process each request on arrival (an inefficient queue is a common cause of tail latency); the offline analytics user wants the queue **never empty**, so the system is never idle waiting for the next request. One's success is the other's failure. [from source] (SRE p.41)
- Solution in the example: partition the infrastructure into independent tiers, two kinds of cluster: **low latency** (with plenty of capacity slack, less contention, more redundancy and customer isolation) and **throughput** (run "hot", with less redundancy); the second meets the relaxed needs at a much lower cost, perhaps **only 10-50% of the cost of a low-latency cluster** (that is, the throughput cluster costs 10% to 50% of the other). Key strategy: offer explicitly delineated service tiers, which **externalizes** the cost difference to customers and motivates them to choose the cheapest tier that meets their needs; Google+ can put privacy-critical data in a globally consistent datastore (Spanner-like) and optional data in a cheaper NoSQL (Bigtable-like). Several tiers run on **identical hardware and software**, varying the amount of resources, the degree of redundancy, geographic constraints and, critically, the configuration of the infrastructure software. [from source] (SRE p.41)

## Motivation for the error budget (Mark Roth)
- Tension between dev (velocity) and SRE (reliability), amplified by information asymmetry; typical tensions: fault tolerance, testing, push frequency, canary duration/size. [from source] (SRE p.42)
- Procedure: product defines a per-quarter SLO; actual uptime is measured by a neutral third party (monitoring); the difference is the budget; while budget remains, releases continue. [from source] (SRE p.42-43)
- Budget exhausted: releases are temporarily suspended and resources go to testing/resilience; subtler alternatives to on/off exist (slow down, roll back). [from source] (SRE p.43)
- Network outages or datacenter failures that reduce the measured SLO also consume the budget; the number of pushes can be reduced for the rest of the quarter and the whole team supports it, since everyone shares responsibility for uptime. [from source] (SRE p.43)
- Requires SRE to have the authority to stop launches; the product team becomes self-policing. [from source] (SRE p.43)
- If the SLO gets in the way of launching features, it can be loosened. [from source] (SRE p.43)
- Appendix B: period "often a month"; once exhausted, freeze changes except urgent security fixes and bugs that address the cause; for an SLO > 99.99% a quarterly reset is appropriate **because the allowed downtime is small**; the budget is described as a common, data-driven mechanism to assess the risk of launches and gives SRE and development the shared goal of innovating faster without "blowing the budget". [from source] (SRE p.330). Note: Ch. 3 speaks of a quarter, App. B of "often a month"; the book does not reconcile them.

## SLI/SLO/SLA (Ch. 4)
- SLI: a quantitative measure of some aspect of the level of service (latency, error rate, throughput). [from source] (SRE p.44)
- Availability = fraction of time usable, often the fraction of successful requests (yield); durability = probability that data is retained over the long term. [from source] (SRE p.44)
- SLO: a target value or range for an SLI. [from source] (SRE p.45)
- **Not every SLI becomes an SLO (p.45)**: the book says the SLO value is not always chosen; for HTTP requests coming from outside, QPS is determined essentially by users' desire, so **no SLO is set for QPS**; average latency per request, however, can be the object of a target. The book's example of a "fast" SLO uses **average search latency below 100 ms** (the book itself uses the average in this example; the caveat about averages vs percentiles comes later, p.46-47; 100 ms is declared an arbitrary value). QPS and latency can be linked: more QPS tends to increase latency and there is a "performance cliff" above a certain load. [from source] (SRE p.45) [inference: that is why QPS enters as capacity-planning data and not as an SLO target; see p.175-176 and p.188-192]
- SLA: a contract (explicit or implicit) with consequences, most easily recognized when financial (rebate, penalty); test: "what happens if the SLO is not met?" — with no explicit consequence, it is an SLO. [from source] (SRE p.45)
- SRE's role in SLAs: SRE normally does NOT get involved in building SLAs (tied to business and product decisions); it gets involved in helping avoid triggering the consequences of missed SLOs and can help define the SLIs (there must be an objective way to measure the agreement's SLOs). [from source] (SRE p.45)
- In practice: business and legal choose the consequences and penalties of a violation; SRE's role is to help them understand the probability and difficulty of meeting the SLA's SLOs; be conservative in what you advertise, since the larger the audience, the harder it is to change or remove bad SLAs. [from source] (SRE p.49-50)
- Note 16: in everyday speech "SLA" almost always means SLO ("SLA violation" is usually a missed SLO); a real SLA violation can become a lawsuit for breach of contract. [from source] (SRE p.50, note 16; call-out on p.45)
- Note 17 (p.50, call-out in the sentence on p.49 about defending the chosen SLOs: if you never win a conversation about priorities by citing an SLO, it is probably not worth it): if you can never win a conversation about SLOs, it is probably not worth having an SRE team for that product. [from source] (SRE p.50, note 17; call-out on p.49)
- Note 18 (p.50, call-out in the p.49 passage "Don't overachieve", about taking the system down on purpose, like Chubby's planned outages, to avoid excessive dependence): failure injection (or fault injection; reference [Ben12]) serves a different purpose, but can also help set expectations. [from source] (SRE p.50, note 18; call-out on p.49)
- No public SLA does not mean no consequence: Google Search has no SLA with the world, but unavailability costs reputation and advertising revenue. [from source] (SRE p.45-46)
- Do not choose the SLO from current performance; keep it simple; avoid absolutes; have few SLOs; perfection can wait. [from source] (SRE p.48-49)
- Percentiles instead of averages; example 99% of Get RPCs < 100 ms; separate objectives per workload class. [from source] (SRE p.47-48)
- SLI categories by system type: serving (availability, latency, throughput), storage (latency, availability, durability), pipelines (throughput, end-to-end latency), correctness. **Caveat on p.46**: all systems should care about correctness (the right answer, the right data, the right analysis) and it should be tracked as a health indicator, but it is usually a property of the data in the system, not of the infrastructure itself, and therefore **normally it is not SRE's responsibility to meet**; do not claim that SRE "guarantees correct answers". Aggregation (p.46): aggregating measurements requires care; the per-minute average can hide bursts of a few seconds (a system with 200 req/s on even seconds and 0 on odd seconds has the same average as a constant 100 req/s, but instantaneous load twice the average), and the latency average hides the long tail. [from source] (SRE p.46)
- Standardize indicators: aggregation intervals and regions, frequency, requests included, acquisition method, access latency. [from source] (SRE p.47-48)
- 4-step control loop (measure, compare, decide, act). [from source] (SRE p.49)
- Safety margin (tighter internal SLO) and "don't overachieve" (Chubby case: planned outage to expose dependencies). [from source] (SRE p.45, p.49)
- Condition for the global Chubby synthetic outage: SRE makes global Chubby meet its SLO without significantly exceeding it; **in each quarter in which a real failure has not brought availability below the target**, a controlled outage is synthesized, taking the system down on purpose. Reason: real outages were so rare that service owners came to depend on Chubby as if it never went down (false sense of security); the outage exposes unreasonable dependencies early. [from source] (SRE p.45)
- Measure like the user: Gmail went from about 99.0% to more than 99.9% by measuring at the client. [from source] (SRE p.330) [DATED]

## Availability table (Appendix A, p.326-327)
Assumes no planned downtime. Columns: year, quarter, month, week, day, hour.
| Level | Year | Qtr. | Month | Week | Day | Hour |
|---|---|---|---|---|---|---|
| 90% | 36.5 d | 9 d | 3 d | 16.8 h | 2.4 h | 6 min |
| 95% | 18.25 d | 4.5 d | 1.5 d | 8.4 h | 1.2 h | 3 min |
| 99% | 3.65 d | 21.6 h | 7.2 h | 1.68 h | 14.4 min | 36 s |
| 99.5% | 1.83 d | 10.8 h | 3.6 h | 50.4 min | 7.20 min | 18 s |
| 99.9% | 8.76 h | 2.16 h | 43.2 min | 10.1 min | 1.44 min | 3.6 s |
| 99.95% | 4.38 h | 1.08 h | 21.6 min | 5.04 min | 43.2 s | 1.8 s |
| 99.99% | 52.6 min | 12.96 min | 4.32 min | 60.5 s | 8.64 s | 0.36 s |
| 99.999% | 5.26 min | 1.30 min | 25.9 s | 6.05 s | 0.87 s | 0.04 s |
[from source] (SRE p.326-327). The script `error_budget_calc.py --table` reproduces and checks it.

## Numerical examples of risk, SLI and SLO that were missing (Ch. 3-6) [from source]
- Targets by service type: a typical Google Apps for Work service would have an **external quarterly target of 99.9%**, backed by a stronger internal target and by a contract with penalties; **YouTube in 2006** got a lower target than the enterprise one, being a consumer product still changing and growing fast (SRE p.39). The published target of Google Compute Engine was "**three and a half nines**": 99.95% (SRE p.44).
- Latency: an SLO on a 100 ms average hides the tail; example from Fig. 4-1: the typical request takes ~50 ms, but **5% of requests are 20 times slower**; a system that serves 200 req/s on even seconds and 0 on odd seconds has the same average as a constant 100 req/s, but peaks of 200; example SLOs: 99% of Get RPCs in under 100 ms; 90% in under 1 ms and 99% in under 10 ms; 99.9% in under 100 ms; 95% of Set from throughput clients in under 1 s; 99% of Set from latency clients with payload < 1 kB in under 10 ms (SRE p.45-48). Standardized aggregation: "1-minute average", "measured every 10 seconds".
- Tail (Ch. 6): with average latency of 100 ms at 1,000 req/s, 1% of requests may take 5 s; if 1% of requests are 50x the average, the rest are about twice as fast as the average (note 23); a backend's p99 can become the frontend's median (SRE p.58, 62). For a 99.9% annual target (which allows ~9 hours of aggregate downtime per year; per the App. A table it is 8.76 h), probing for status 200 more than once or twice **per minute** is probably unnecessary, and checking disk occupancy more often than **every 1-2 minutes** also is (two distinct rules; only the disk one is "every 1-2 min"); a 1-min window for CPU hides long spikes that feed the tail (SRE p.59).
- Background error rate example: ISPs between 0.01% and 1% (SRE p.40); 99.9% → 99.99% is worth $900 on $1M of revenue (0.09% × $1M) (SRE p.40).

## Corrections after the blind test (round 6): aggregate metric × outage duration (Ch. 3, p.38, and the closing note of App. A, p.328) [from source]
- **The appendix's recommendation (p.328).** Using an **aggregate unavailability** metric ("X% of all operations failed") is **more useful than focusing on outage duration** in two cases: services that can be **partially available**, for example because they have several replicas and only some are unavailable, and services whose **load varies over the day or week** rather than staying constant. The appendix refers to the time-based and aggregate availability equations of Ch. 3. (SRE p.328)
- **The two equations (p.38).** Time-based availability is the proportion of time the system is up (uptime ÷ (uptime + downtime)), and the App. A table (p.326-327) converts nines into minutes of downtime. But, at Google, a time-based metric usually makes no sense for globally distributed services, because it is very likely that at least part of the traffic is being served somewhere in the world at any moment (the service is at least partially "up"); therefore availability is defined by the **request success rate** (yield): successful requests ÷ total, over a rolling window. (SRE p.38)
- **When to use each.** App. A opens by saying that availability is generally computed from the time the service was unavailable in a period and that the table (p.326-327) assumes **no planned downtime**; the closing note (p.328) adds that, for a partially available or variable-load service, the aggregate metric is more useful than duration. (SRE p.326-328)
- [inference] The same minutes of outage weigh differently if they fall at peak or in the small hours, which explains the preference for the aggregate metric when load varies; this is the package's reading, not a sentence from the book. (SRE p.328)

## What the book does NOT say
Burn rate, multi-window alerts, "error budget policy" as a document, SLO per critical user journey, comparison of rolling vs calendar window as a design choice (p.38 only mentions a one-day rolling window), a table beyond 5 nines; the "1 − SLO" formula appears only in words. All of this is `[extrapolation]` (later Workbook/practice).
