# Glossary (terms from the SRE book; pages = PDF, printed = N−12)

| Term | Meaning (paraphrased) | Page |
|---|---|---|
| Site Reliability Engineering (SRE) | Discipline of operating services with software engineering, covering the whole lifecycle | SRE p.15, 23 |
| SLI | Quantitative measure of an aspect of the level of service (latency, error rate, throughput) | SRE p.44 |
| SLO | Target value or range for an SLI | SRE p.45 |
| SLA | Contract with consequences for not meeting SLOs; SRE normally does not build it (business/legal choose the consequences); "SLA" in everyday use often means SLO (note 16); note 17: if you never win a conversation by citing SLOs, an SRE team may not be worth it; note 18: fault injection has another purpose, but helps set expectations | SRE p.45, 49, 50 |
| Error budget | 1 − availability target; failure budget spent at feature velocity | SRE p.25, 43 |
| Yield | Fraction of well-formed requests that succeed | SRE p.44 |
| Durability | Probability that data is retained in the long term | SRE p.44 |
| Unplanned downtime | Focus of the book's risk metric | SRE p.38 |
| Toil | Manual, repetitive, automatable, tactical work with no enduring value, that scales with the service | SRE p.51 |
| Overhead | Administrative work not tied to the service (not toil) | SRE p.51, 53 |
| Four golden signals | Latency, traffic, errors, saturation | SRE p.57 |
| White-box / black-box | Monitoring by internal metrics / by external behavior | SRE p.55 |
| Page / ticket / logging | Three valid monitoring outputs (p.26: alerts/tickets/logging; p.330: pages/tickets/logging; p.95: tickets as the destination of subcritical alerts) | SRE p.26, 95, 330 |
| Borgmon, varz | Google's monitoring system and export format [DATED] | SRE p.88-89 |
| Playbook | Document of best practices for response; ~3x better MTTR | SRE p.26 |
| Wheel of Misfortune | Disaster role-play for training (mention on p.26 and p.103, together with DiRT; postmortem reenactment p.128; description in Ch. 28, p.280) | SRE p.26, 103, 128, 280 |
| DiRT | Google's annual Disaster Recovery Testing | SRE p.103, 317 |
| Hermetic build | Build identical regardless of the machine | SRE p.77 |
| Cherry picking | Taking only the fix from mainline to the release branch | SRE p.77-78 |
| Canary | Updating a subset to observe before expanding | SRE p.138, 268 |
| Break-glass | Mechanism to push config before tests finish | SRE p.144 |
| Zero MTTR | Bug detected by a test before reaching production | SRE p.135 |
| Incident Command System | Basis of incident management (4 roles in the book) | SRE p.123 |
| Freelancing | Changing the system without coordination during an incident | SRE p.123 |
| Blameless postmortem | Postmortem focused on systemic causes, not on culprits | SRE p.126-127 |
| Lame duck | Backend still serving but asking clients to stop sending | SRE p.166 |
| Subsetting | Limiting the pool of backends of each client | SRE p.166 |
| Weighted Round Robin | Round robin weighted by capacity reported by the backend | SRE p.173 |
| Adaptive throttling | Local rejection by the client according to requests vs accepts (2-min window) | SRE p.176-177 |
| Criticality | 4-level value of the importance of the request | SRE p.177 |
| Cascading failure | Failure that grows through positive feedback | SRE p.184 |
| Load shedding | Dropping part of the load near overload | SRE p.189 |
| Graceful degradation | Reducing quality to reduce work | SRE p.190 |
| Query of Death | Request that brings down the process | SRE p.195 |
| Split-brain | Two parts acting as leader simultaneously | SRE p.203 |
| CAP, ACID, BASE | Consistency/availability concepts | SRE p.201-203 |
| Paxos / Multi-Paxos | Family of consensus algorithms | SRE p.204-205, 211 |
| Replicated state machine | Same operations, in the same order, on several replicas | SRE p.205 |
| Idempotent | Safe to repeat; essential for partial failures | SRE p.230 |
| Thundering herd | Synchronized burst of load | SRE p.231, 235 |
| Soft deletion / lazy deletion | Data marked as deleted but recoverable for a limited time | SRE p.248-249 |
| Out-of-band validation | Independent verification of the data | SRE p.252-253 |
| LCE | Launch Coordination Engineer | SRE p.262 |
| PRR | Production Readiness Review | SRE p.305, 308 |
| N+2 | Peak served with two units less | SRE p.35, 330 |
| Kindling | Emergencies waiting to happen on an overloaded team | SRE p.291 |
| Time-series arena / horizon | Fixed-size memory block of Borgmon with a collector that expires the oldest; horizon = interval between the newest and the oldest (~12 h; ~24 B per point) [DATED] | SRE p.90-91 |
| TSDB | External time-series database where Borgmon archives state; slower, but cheaper and larger than RAM | SRE p.91 |
| Labelset / varz / rate() | Name of a series as a set of labels; page of exported metrics; total delta ÷ total time of the window | SRE p.89-91, 93 |
| Prober / Alertmanager | Black-box protocol check that exports series / router that inhibits, deduplicates and does fan-in/out of alerts | SRE p.95-96 |
| Consistent hashing | Stable mapping when backends join or leave (alternative to `id mod N`, which remaps almost everything) | SRE p.162 |
| GRE (encapsulation) | Google's current solution for VIP: packet inside another IP+GRE (24 B overhead; may require larger MTU) [DATED] | SRE p.162 |
| DSR / NAT on VIP | Direct Server Response (backend replies directly; requires same broadcast domain) / NAT (entry per connection, no stateless fallback) | SRE p.162 |
| Least-Loaded Round Robin / sinkholing | Round Robin among the backends with the fewest active requests / sick backend that returns errors quickly and attracts traffic | SRE p.172-173 |
| GCU | Google Compute Unit: virtual CPU unit for equivalence across machine architectures | SRE p.172 |
| Decider / MoB | Automatic failover daemon of Ads MySQL (2009; <30 s in 95% of cases) / MySQL on Borg | SRE p.67 |
| Prodtest | Unit tests (Python) of real services per cluster, paired with idempotent fixes | SRE p.68-70 |
| Diskerase | Disk wiping at decommissioning; incident of the empty set = "everything" | SRE p.74, 119-120 |
| Sacrificial cluster | Cluster that concentrates traffic so the others can recover from a cascade (Shakespeare, USA-2) | SRE p.332, 335 |
| Make-children-cry switches | Kill switches of the NORAD Tracks Santa launch | SRE p.261 |
| Moiré load pattern | Problem related to thundering herd: two or more pipelines whose runs sometimes overlap on a shared resource; can occur even in continuous pipelines, less common with more uniform load; the example's peak is "1.2 M" of aggregate load, **with no unit given in the book** (Fig. 25-3) | SRE p.236-237 |
| Task Master / Workflow | In-memory state server with journal (system prevalence) of Google Workflow, with leases and server token | SRE p.238-240 |
| Bazel / Blaze | Google's build tool, open-sourced as Bazel (note 37); dependency graphs | SRE p.78, 81, 140, 147 |
| Push on Green | Deploy of every build that passes all tests | SRE p.77, 158 |
| Zookeeper / Consul / etcd | Consensus services used as clients (only named in the book) | SRE p.205 |
| Bad Apple Theory | (Refuted) idea that removing the "bad" ones is enough for the system to be fine | SRE p.292 |
| Postvitam | After-action report that explains the critical decisions that led to success | SRE p.294 |
| HiPPO | Highest-Paid Person's Opinion | SRE p.321 |
| Swing capacity | Mobile reserve capacity (telecom: "switch on wheels") | SRE p.318 |
| Knight Capital | 2012 "software glitch": loss of US$ 440 million in a few hours; dead code under a flag | SRE p.83, 321-322 |
| Viceroy | Unified monitoring dashboard framework in 2012-2014 | SRE p.298-300 |
| Root cause | Defect in a software or human system that, if repaired, gives confidence that the event will not recur in the same way; an incident can have several, each can be a root cause on its own and must be repaired | SRE p.55 |
| Push | Any change to the running software of a service or to its configuration | SRE p.55 |
| Alert (ticket, email alert, page) | Notification to a human, sent to a ticket queue, an e-mail alias or a pager; classified as tickets, email alerts and pages | SRE p.55 |
| Node / machine | Interchangeable terms for a running kernel instance (physical server, VM or container) | SRE p.55 |
| Paging events (production meeting) | Pages from monitoring reviewed tactically; two questions: should it have paged like this? should it have paged? If not, remove the non-actionable pages | SRE p.296 |
| Nonpaging events (production meeting) | Three items: should have paged and did not (fix the monitoring so it pages); not pageable but requires attention (follow up, including reactive operational work); not pageable and requires no attention (remove the alert, it is noise) | SRE p.297 |
| Outgoing deadline | Outgoing deadline of an RPC: reduce it by a few hundred ms; consider a ceiling for noncritical or fast backends, without making certain kinds of request always fail | SRE p.193 |
| Queueless server | Server without a queue, relying on failover to other tasks when threads are exhausted (Gmail); for bursty traffic, the queue can be sized by threads in use, time per request and size and frequency of bursts | SRE p.189 |
| Hedged request | Send the RPC to a primary and, after a time, to other instances; on receiving the first response, cancel the others | SRE p.193 |
| Feature flag framework | Gradual rollout mechanism with 6 requirements (many parallel changes, 1 to 10% of users, routing by user/session/object/location, failure handled without affecting users, independent and immediate rollback, measurement of the effect) | SRE p.268 |
| CAPA | Corrective and preventative action: systematic investigation of root causes to prevent recurrence; corresponds to blameless postmortems | SRE p.319 |
| Near miss | Event that could have caused serious harm but did not; treated as a "preventive postmortem" (CHIRP in the UK) | SRE p.320 |
| Quorum lease | Read lease over part of the state granted to a quorum of replicas, for a short time; allows strongly consistent local reads at the cost of write performance | SRE p.212 |
| Dueling proposers | Multi-Paxos livelock in which proposals repeatedly interrupt each other; avoided by electing a proposer or rotating slots, with random backoff | SRE p.211 |
| Watchdog | Thread that wakes periodically and, if no work has occurred since the last check, assumes the server hung and kills it | SRE p.200 (note 108) |
