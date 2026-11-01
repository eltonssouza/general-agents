# Cases and anti-patterns (backed by the sources)

Each item lists the signal, the problem according to the source, and the alternative the book itself offers. Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Items from the previous package that lacked backing (e.g., "Distributed monolith with 2PC in microservices as its own category", "retry storm without jitter" as a rule) were rewritten or removed.

| # | Anti-pattern | Problem according to the sources | Alternative in the sources |
| :-: | :--- | :--- | :--- |
| 1 | Chains of synchronous HTTP between microservices | blocking, coupling, and cascading failure; "an HTTP-based monolith" [from source] (MS-MIC p.50) (MS-MIC p.51); latency is the sum of the steps [from source] (MS-CLD p.79) | messaging/events, materialized view, aggregator, request-reply [from source] (MS-CLD p.79) (MS-CLD p.80) (MS-CLD p.81) |
| 2 | Distributed monolith | remote call in every function, "chattiness", dependency cycles, excessive code sharing [from source] (JMG p.18) (JMG p.19) | reduce what is shared to a minimum, rethink the split; consolidate thin services [from source] (SOA p.37) |
| 3 | Database shared between services | schema change requires coordinated update and breaks autonomy [from source] (MS-MIC p.44); major coupling point [from source] (EDS p.8) | private data + API/messaging; caveat: SAP admits a shared database as a practical solution (SAP p.40) |
| 4 | "Monolithic" gateway or "new ESB" | becomes an aggregator/orchestrator of all services, single point of failure, team bottleneck [from source] (MS-MIC p.58) (MS-MIC p.62) (MS-MIC p.63); business rules in the middleware [from source] (JMG p.120) | several gateways per client/boundary (BFF); thin gateway [from source] (MS-CLD p.71) |
| 5 | ESB and central orchestrators | typical of SOA and, in most cases, anti-patterns among microservices [from source] (MS-MIC p.40); the middleware centralizes coordination [from source] (SOA p.38) | smart endpoints and simple channels [from source] (MS-MIC p.64) |
| 6 | Architecture sinkhole | requests cross layers without logic; 80-20 rule [from source] (SAP p.14) | open some layers, aware of the loss of isolation [from source] (SAP p.15) |
| 7 | Too-fine granularity | requires orchestration and becomes "heavy SOA" [from source] (SAP p.39); 4 calls of 100 ms = 600 ms [from source] (SOA p.28) | start with larger services and split later [from source] (SOA p.29) |
| 8 | Naive retry without CB or backoff | aggravates cascading effects and can cause DoS [from source] (MS-MIC p.309) (MS-MIC p.321); retry storms [from source] (JMG p.60) | backoff, jitter, circuit breaker, idempotency [from source] (MS-MIC p.320) (MS-MIC p.322) |
| 9 | Remote calls without timeout | threads blocked until the pool is exhausted [from source] (MS-MIC p.307); a single global timeout is problematic [from source] (SOA p.17) | timeouts per context, derived from the SLA [from source] (JMG p.59) (SOA p.17) |
| 10 | Updating the database and publishing an event without atomicity | lost event or inconsistency if it crashes between the two steps [from source] (MS-MIC p.158) (EDS p.75) | Outbox, log mining/CDC, Event Sourcing [from source] (MS-MIC p.158) (MS-MIC p.159) (MS-MIC p.160) (EDS p.82) |
| 11 | Distributed 2PC transaction between services | hurts scalability; killed the business in the Starbucks example [from source] (SBC p.3); complexity and scale [from source] (JMG p.63); NoSQL without 2PC [from source] (MS-MIC p.49) | Saga, compensation, retry with idempotency [from source] (MS-CLD p.102) (SBC p.2) (SBC p.3) |
| 12 | Non-idempotent consumer | duplicates from retry (e.g., double payment) [from source] (EDS p.127); events must be idempotent or detectable [from source] (MS-MIC p.164) (MS-MIC p.165) | deduplicate at the transport and in the application [from source] (MS-MIC p.165) |
| 13 | CQRS/Event Sourcing by reflex | "do not use CQRS and DDD everywhere"; many services are better off with CRUD [from source] (MS-MIC p.202) (MS-MIC p.203); ES brings complexity [from source] (MS-CLD p.105) | apply where the difference in demand justifies it |
| 14 | Wrongly sized mediator | open-source hub for very complex orchestration, or BPM for simple routing, is a recipe for failure [from source] (SAP p.21) | choose the mediator implementation according to the need |
| 15 | Central broker treated as "SOA-lite" | the lightweight broker does not orchestrate, transform, or route in complex ways [from source] (SAP p.38) | keep the broker as transport; cluster/federate to avoid SPOF [from source] (SAP p.38) |
| 16 | Mixing messaging and synchronous HTTP in the same interactions | MS-MIC recommends avoiding the mix when adopting commands/events via messages [from source] (MS-MIC p.70) | synchronous only from client to front end |
| 17 | Direct query of another service's tables | no microservice should include another's tables in its transactions, nor direct queries [from source] (MS-MIC p.48) | API of the data owner or local copy via event [from source] (MS-MIC p.66) |
| 18 | Undocumented open/closed layer | coupled, fragile architectures that are hard to test and deploy [from source] (SAP p.12) | document open/closed layers and why [from source] (SAP p.12) |
| 19 | Event contracts without governance | event contracts and versioning are a central challenge of EDA [from source] (SAP p.25) | standard format and versioning policy from the start [from source] (SAP p.25) |
| 20 | Depending on a single gateway/service without redundancy | SPOF [from source] (SDH p.28) (MS-MIC p.62) | multiple instances, load balancer, multi-region [from source] (MS-CLD p.129) |

## Reference cases

- Starbucks (SBC p.1-3): asynchrony, Competing Consumer, Correlation Identifier, write-off/retry/compensation, short synchronous + long asynchronous conversation.
- eShopOnContainers (MS-MIC, MS-CLD): reference application with .NET microservices, BFF/gateways, and event bus (MS-MIC p.46; MS-CLD p.93-94).
- JCG Car Rentals (JMG p.58-63; p.108-121): Java reference application for resilience and gateway.
- Table of "classic cases" (Netflix, Amazon, etc.) from the previous package: removed, with no backing in the cited pages. [extrapolation]

## Out of scope

Case studies of specific companies beyond the examples above; real post-mortems (see the SRE package).
