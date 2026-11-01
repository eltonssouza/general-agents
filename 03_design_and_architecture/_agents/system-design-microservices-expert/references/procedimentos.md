# Procedures (actionable playbooks anchored in the sources)

Each step carries its origin. When a step is our own heuristic, it is labeled. Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## P1. System design playbook (SDH, interview template)

1. Clarify requirements: functional (features, users, interaction, data types, integrations) and non-functional (read vs. write, availability, latency, consistency...). [from source] (SDH p.51)
2. Estimate capacity: daily/monthly users and peak, read/write RPS, storage, cache memory, bandwidth; check whether the estimate is necessary. [from source] (SDH p.52)
3. High-level design: clients, application servers, load balancers, services, databases, storage, cache, queues, external services. [from source] (SDH p.53)
4. Data model and database choice (entities, relations, keys, normalization; relational vs. NoSQL). [from source] (SDH p.54) (SDH p.55)
5. API design: protocols (HTTPS, WebSockets, gRPC, AMQP/MQTT) and style according to the requirements. [from source] (SDH p.56)
6. Deep-dive into components (sharding/replication, servers behind the load balancer, cache and invalidation). [from source] (SDH p.57)
7. Address key concerns: scalability/performance and reliability (SPOFs, redundancy, replication, circuit breaker, retry with backoff, monitoring). [from source] (SDH p.58) (SDH p.59)
- Use `scripts/analyze_tradeoffs.py` for availability numbers (the formulas are [extrapolation]; the table of nines is from SDH p.7).

## P2. Choosing the architectural style

1. Gather the critical attributes (agility, deployment, testability, performance, scalability, ease of development). [from source] (SAP p.15) (SAP p.53)
2. Compare with the ratings per pattern (`padroes-arquiteturais-fundamentais.md`, section 6) and take into account infrastructure, skills, budget, deadline, and size. [from source] (SAP p.53)
3. SOA vs. microservices: heterogeneity of protocols/systems and many shared components point to SOA; smaller, well-partitioned systems point to microservices. [from source] (SOA p.46) (SOA p.49)
4. If the application is a simple monolith and it is sufficient, MS-WEB argues that it is easier to build, deploy, and debug. [from source] (MS-WEB p.3)

## P3. Identifying microservice boundaries

1. Start from the domain model and the data: decoupled data islands and contexts with their own language (e.g., User/Customer/Buyer). [from source] (MS-MIC p.46) (MS-MIC p.47)
2. The goal is not the most granular separation, but the most meaningful one for the domain; strong cohesion points to a single service. [from source] (MS-MIC p.51)
3. A bounded context may have several physical services; the logical architecture does not need to coincide with the physical one. [from source] (MS-MIC p.45) (MS-MIC p.46)
4. Warning sign: constant aggregation of data from several services may indicate a need to merge services. [from source] (MS-MIC p.48)
5. If you must orchestrate/call other services on every request, review the granularity. [from source] (SAP p.39) (SOA p.37)

## P4. Removing synchronous queries between services

1. Identify the internal HTTP calls made to assemble a response. [from source] (MS-MIC p.50)
2. Replicate only the needed attributes into the consuming service's database via events (Materialized View). [from source] (MS-MIC p.66) (MS-CLD p.79) (MS-CLD p.101)
3. If that is not possible, use Aggregator or Request/Reply with a correlation ID. [from source] (MS-CLD p.79) (MS-CLD p.80) (MS-CLD p.81)
4. Make eventual consistency explicit to users/the business. [from source] (MS-MIC p.71)

## P5. Publishing an event atomically (Outbox)

1. Create the integration events table in the same database as the entities. [from source] (MS-MIC p.159)
2. In a single local transaction: change the entities, insert the event ("ready to publish"), and commit. [from source] (MS-MIC p.159) (MS-MIC p.160)
3. Publish right after the commit and mark it as published in a new local transaction, or use the table as a queue with a worker. [from source] (MS-MIC p.160)
4. Have a checker that republishes pending events. [from source] (MS-MIC p.160)
5. Make the consumer idempotent (P6). [from source] (MS-MIC p.164) (MS-MIC p.165)
6. Alternatives: CDC (EDS p.82), full Event Sourcing (MS-MIC p.158-159). [from source]

## P6. Idempotent consumer

1. Give each event/command a unique identity. [from source] (MS-MIC p.165) (EDS p.127)
2. Prefer idempotent operations ("set price = 25") over deltas ("add 5"). [from source] (MS-MIC p.165)
3. Deduplicate at the transport (if available) and in the handler; with RabbitMQ consider the `redelivered` flag. [from source] (MS-MIC p.165) (MS-MIC p.166)
4. If on Kafka with read-process-write, evaluate the transactions API (exactly once) and its limits. [from source] (EDS p.130) (EDS p.134)

## P7. Resilient remote call

1. Define timeouts from the service SLA, per context and configurable. [from source] (JMG p.59) (SOA p.17)
2. Retry only for transient failures (e.g., 408/429/502/503/504; not 403), with exponential backoff and jitter, and with idempotency. [from source] (MS-CLD p.124) (MS-CLD p.125) (MS-MIC p.320) (MS-MIC p.321) (JMG p.60)
3. Circuit breaker for prolonged failures, combined with retry. [from source] (MS-MIC p.321) (MS-MIC p.322)
4. Fallback (cache/default value) for queries; limit on pending requests (bulkhead). [from source] (MS-MIC p.309) (MS-MIC p.310)
5. Test with injected failures. [from source] (MS-CLD p.127)
6. Numeric values: start from the books' examples (MS-MIC p.317 and p.322; MS-CLD p.126 and p.127) as a starting point, and adjust by measurement. [inference]
- Simulate with `scripts/calc_rate_limit.py --backoff ...` and `--circuit-breaker ...` (explicitly [extrapolation]).

## P8. Designing a Saga

1. List the local transactions of the flow and, for each one, the compensation. [from source] (MS-CLD p.102) (MS-CLD p.103)
2. Choose choreography (events) or orchestration (commands/aggregator); orchestration concentrates the flow in one place (easier to understand, more coupled) and choreography is pluggable. [from source] (MS-CLD p.103) (EDS p.55)
3. For retry of final steps use an idempotent receiver. [from source] (SBC p.2)
4. Use `scripts/audit_saga.py` to check compensation/idempotency/Outbox rules (rules labeled with their origin; the notion of "pivot" is [extrapolation]).
5. Consider a framework: JMG mentions Axon and Eventuate Tram. [from source] (JMG p.63)

## P9. Designing a gateway/BFF

1. Decide whether you need a gateway: many services and remote/mobile clients. [from source] (MS-MIC p.55) (MS-MIC p.56)
2. Choose functions: L7 routing, aggregation, cross-cutting offloading. [from source] (MS-MIC p.59) (MS-MIC p.60)
3. Split by client and by business boundary; keep it thin and free of business rules. [from source] (MS-MIC p.58) (MS-CLD p.71)
4. Scale out and handle SPOF/bottleneck. [from source] (MS-MIC p.62)
5. In NGINX: rate limit by zones, body size, authentication (APIGW p.22-30). [from source]

## P10. Choosing REST vs. gRPC vs. messaging

1. External client/browser and public API: REST/JSON. [from source] (MS-CLD p.95)
2. Unavoidable internal synchrony: gRPC. [from source] (MS-CLD p.92) (MS-CLD p.94)
3. Propagating changes between services: events. [from source] (MS-MIC p.65) (MS-MIC p.71)
4. Migration from REST to gRPC as a "procedure" of the previous package has NO playbook in the sources. [extrapolation]

## Out of scope

Strangler Fig as a named procedure (only the idea of a gateway mediating a monolith, MS-MIC p.59); operations runbooks (SRE package).
