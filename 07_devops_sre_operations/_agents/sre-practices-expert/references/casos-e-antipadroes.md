# Cases and anti-patterns from the book

Pages = PDF (printed = N−12). Cases are from Google and [DATED] in tooling; the lessons are what matters.

## Cases
| Case | What it illustrates | Page |
|---|---|---|
| Margaret Hamilton / P01 (Apollo 8) | Anticipate human error and document it | SRE p.16 |
| Chubby planned outage | Overshooting the SLO too much creates dependency | SRE p.45 |
| Bigtable over-alerting | SLO set by the average and noisy alerts | SRE p.60 |
| Gmail/Workqueue paging | A robotic response to a page is a red flag | SRE p.60-61 |
| Ads MySQL on Borg / Decider | Manual failover of 30-90 min gave 99% at best; a target of <30 s per failover only with automation (95% of cases <30 s); cost: failure logic in every app (JDBC); -95% toil, ~60% of the hardware freed | SRE p.66-67 |
| Diskerase (Ch. 7 and Ch. 13) | Empty set = "all"; missing sanity check | SRE p.74, 119-120 |
| Test-Induced / Change-Induced / Process-Induced | Test: tested rollback (1 of 100 databases, restored in 1 h); Change: full canary and the luck of an engineer watching channels (reverted in 5 min, incident in 10 min, up to 1 h for some services); Process: sanity check for an empty filter (Diskerase, 3 h to rebuild the 1st installation, 3 days for most of it) | SRE p.116-120 |
| App Engine latency | Mitigate before finding the cause; spurious correlation | SRE p.112-114 |
| Incident "The Firm" (Mary and Malcolm) | Narrow technical focus, poor communication, freelancing | SRE p.122-124 |
| Shakespeare Sonnet++ (incident #465) | Cascading failure: 88x traffic, sacrificial cluster USA-2, 2x failed due to an order-of-magnitude error (15:33-15:34), 10x, ramp-up at 1/10/30/50/100%, 66-min outage and 89-min incident, exit after 30 nominal min; ~1.21 billion queries lost | SRE p.332-336 |
| Gmail 2011 | Tape restore (GTape); estimate given and met, 99%+ ahead of schedule; defense in depth | SRE p.254-255 |
| Google Music 2012 | Race in a deletion pipeline (~600 thousand tracks, 21 thousand users); 436,223 on tape, ~161 thousand without backup; 1.5 PB in 5,475 restore jobs; ~7 days | SRE p.255-258 |
| Keyhole / NORAD Tracks Santa | Launch with a 25x peak (>1 million req/s), "make-children-cry switches" | SRE p.261 |
| Auxon | Intent-based capacity planning; "Stupid Solver"; 2 years of development | SRE p.152-158 |
| Viceroy | Cross-site collaboration | SRE p.298-301 |
| Bigtable without the log disk / Diskerase | Automation that trusts an implicit signal (first unused disk = empty machine) wiped a Bigtable cluster; empty set = "everything" wiped the CDN disks (~2 days to reinstall) | SRE p.68, 74 |
| Prodtest / cluster turnup | Chained tests + idempotent fixes every 15 min; 6+ weeks from network-ready to live; "One Week Turnup" | SRE p.67-72 |
| Moiré load pattern / Google Workflow | Pipelines that overlap on a shared resource; Workflow (2003) with Task Master, leases, server token | SRE p.236-240 |
| Google Cron | Prefer skipping over duplicating; state in cron itself (Paxos, 3 replicas); precomputed job names | SRE p.226-231 |
| Viceroy and DFP→F1 | Dashboard convergence (2012-2014); live migration of 100 TB/day indexed | SRE p.298-303 |
| Knight Capital | Dead code behind a flag (p.83); automation too fast: US$ 440 million loss in a few hours, 2012 (p.321; note 160 on p.322); duration in minutes is not stated | SRE p.83, 321-322 |

## Anti-patterns by theme
Label: this list is a **package synthesis**; the book uses the word *anti-pattern* only on p.111 and 113 (Ch. 12), in Table 28-1 (p.274) and in the opening of Ch. 33 (p.316), and "trench warfare" (p.23) is described as a bad pattern. The remaining items are the package's readings of what the book advises against, and must not be cited as "the book calls this an anti-pattern" nor extended to whole page ranges (for example, for config without review p.80 only says that all schemes require strict code review).
- **Risk/SLO**: chasing 100%; choosing the SLO from current performance; too many SLOs; using averages; letting the balance be decided by politics or fear. (SRE p.37, 42, 46-49)
- **Toil/automation**: accepting toil as normal; automation outside the owning team; non-idempotent fixes; ambiguous special values; no rate limit/sanity checks. (SRE p.53, 70-74)
- **Monitoring**: alerting on "something odd"; email alerts as the main channel; complex dependency hierarchies; page with robotic response; alerts never used. (SRE p.56, 59-61, 330)
- **Release**: machine-dependent builds; releasing straight from mainline; config without review [package reading: p.80 only requires strict code review in all configuration models; the book does not use the term anti-pattern there]; leaving release engineering for later (p.81). (SRE p.76-81)
- **Testing**: testing only the hermetic; rollback not tested before a big test; loose canary because of "low risk"; disabling tests in break-glass. (SRE p.117-118, 137-138, 144)
- **Incidents**: narrow technical focus, poor communication, freelancing, implicit handoff, declaring late. (SRE p.122-125)
- **Postmortem**: punishment, venting, no review, ignoring follow-up. (SRE p.127-128)
- **Overload**: a backend shutting itself down when overloaded; retries at several layers (4^3 = 64); deadline without propagation; trusting cache as capacity. (SRE p.182-183, 189-193)
- **Consensus**: leader election by heartbeat/STONITH; human-dependent failover. (SRE p.203-204)
- **Pipelines**: periodic for a continuous problem; adding workers when the job does not finish. (SRE p.235, 240)
- **Data**: "replication is backup" (p.247); backup without a restore test (p.254); validation too strict (p.253). (SRE p.247, 253-254)
- **Management**: trial by fire; assigning tickets randomly; on-call and project work at the same time; embedding two SREs. (SRE p.276, 287-288, 290)

## Internal tensions in the book (declare to the user)
- Error budget period: quarter in Ch. 3 (SRE p.42-43) vs "often a month" in App. B (SRE p.330).
- 50% is the ops ceiling in Ch. 1 and Ch. 11 (SRE p.23, 99), and is "toil < 50%" in Ch. 5 (SRE p.52), with 25% as the on-call ceiling (SRE p.100).
- The list of cascading failure steps is not a declared ranking (SRE p.198-199), whereas the prevention list is "in rough priority order" (SRE p.188).
