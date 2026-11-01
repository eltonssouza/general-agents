# Resilience and fault tolerance

Sources: MS-MIC (ch. 7, "Implement resilient applications"), MS-CLD (ch. 6), JMG (ch. 6), SOA, SDH. Pages = PDF (MS-MIC: printed = PDF - 15). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. The numbers below (attempts, windows, thresholds) are EXAMPLES from the books' code/figures, not universal recommendations.

## 1. Partial failure

- Resilience is the ability to recover from failures and keep working; it is not about avoiding failures, it is about accepting them and responding without downtime or data loss. [from source] (MS-MIC p.306) (MS-CLD p.123)
- Partial failure is a constant risk: a slow or unreachable service blocks the caller's threads (e.g., synchronous RPC without a timeout), until the threads are exhausted and the entire application becomes unresponsive. [from source] (MS-MIC p.307)
- Failure is amplified by chains of synchronous HTTP; even excellent dependencies fail: 50 dependencies at 99.99% generate several hours of unavailability per month. [from source] (MS-MIC p.307) (MS-MIC p.308)
- SOA's availability vs. responsiveness: availability = accepting the request in a timely manner (connecting); responsiveness = receiving a response in a timely manner; the first is handled with retry/queue, the second (timeouts) is harder. [from source] (SOA p.15) (SOA p.16)
- JMG: the network is not reliable and latency is not zero ("fallacies of distributed computing"); each service should have a defined SLA, which guides timeouts and allows deriving the consumers' SLAs. [from source] (JMG p.58)

## 2. Strategies for partial failure (MS-MIC)

MS-MIC list: (1) asynchronous communication between internal services; (2) retries with exponential backoff (poorly designed, together with the lack of a circuit breaker, they can aggravate things and cause a DoS); (3) timeouts: never block indefinitely; (4) Circuit Breaker; (5) fallbacks (cached data or default value; simpler for queries than for commands); (6) limit the queue of pending requests (bulkhead). [from source] (MS-MIC p.309)

## 3. Retry and backoff

- Retry with exponential backoff repeats the operation with increasing waits up to a maximum number of attempts; suitable for transient failures (e.g., container moved to another node). [from source] (MS-MIC p.310)
- MS-MIC code example (Polly, eShopOnContainers): 6 attempts, wait of `2^attempt` seconds, starting at 2 s. Note: the example also treats `404` as a failure to retry, because of container initialization; this is peculiar to the case and not a rule. [from source] (MS-MIC p.317) (MS-MIC p.320)
- MS-CLD example: up to 4 retries, initial wait of 2 s doubling on each attempt; after exhaustion, it triggers a fallback. [from source] (MS-CLD p.125) (MS-CLD p.126)
- Which failures to retry: MS-CLD lists short-lived statuses (404, 408, 429, 502, 503, 504) and asks whether 403 would be retried: no; only what is a failure is retried, not a correct response denying authorization. [from source] (MS-CLD p.124) (MS-CLD p.125)
- Jitter: regular retries under high concurrency generate retry spikes; MS-MIC recommends adding jitter (example: `DecorrelatedJitterBackoffV2` with a median first retry of 1 s and 5 attempts) and points to Marc Brooker's article. [from source] (MS-MIC p.320) (MS-MIC p.321)
- The "full jitter" formula `wait = uniform(0, min(cap, base·2^n))` from the previous package is NOT in the corpus (the book uses Polly's decorrelated jitter). [extrapolation] (formula from the AWS architecture blog, widespread in practice).
- JMG: use libraries (Spring Retry, failsafe, resilience4j); example with 5 attempts, initial interval 1000 ms and maximum 20000 ms; backoff instead of a fixed interval, since "retry storms" (thundering herd) cause unavailability; idempotency on both sides is indispensable. [from source] (JMG p.59) (JMG p.60)
- Built-in retries of Azure services: Service Bus example with a default policy of 9 attempts and 30 s wait. [from source] (MS-CLD p.132) [DATED] (value from one edition of the book)
- SDH: "implement retry with exponential backoff for temporary failures and so as not to overload the system during recovery". [from source] (SDH p.59)

## 4. Circuit Breaker

- Purpose (MS-MIC): if the error rate exceeds a threshold, the circuit "trips" and the next attempts fail immediately; after a waiting period, the client tries again and, if successful, closes the circuit. [from source] (MS-MIC p.309)
- Retry and CB have different purposes: retry expects success; CB avoids executing an operation that is probably doomed to fail; they can be combined, with the retry sensitive to the CB's exceptions and giving up attempts when the CB indicates a non-transient failure. Careless retries "can create a DoS on your own software". [from source] (MS-MIC p.321) (MS-MIC p.322)
- MS-MIC example (Polly): opens after 5 consecutive failures and stays open for 30 s; during that period calls fail immediately. There are `Isolate`/`Reset` to open/close manually (e.g., isolating a downstream during an upgrade). [from source] (MS-MIC p.322) (MS-MIC p.325)
- MS-CLD example: after a pre-defined number of failed calls it blocks traffic and periodically lets a test call through; in the figure, the circuit opens after 100 failed requests and a 30 s `CheckCircuit` defines the frequency of the test call; if it succeeds, the circuit closes. [from source] (MS-CLD p.126) (MS-CLD p.127)
- The three states with the names Closed/Open/Half-Open do NOT appear in the corpus; the behavior (closed -> open -> test call -> closed) is described. [extrapolation] (Nygard/Fowler terminology). Thresholds such as "50% errors in 10 s" from the previous package were invented.
- SOA: circuit breaker avoids waiting for timeouts; unlike a physical circuit breaker, it can reset itself (Netflix's Ribbon; Nygard's book *Release It!*). [from source] (SOA p.16) (SOA p.17)
- JMG: CB + fallback; Hystrix "probably the best known and most tested". [from source] (JMG p.61) [DATED] Hystrix is in maintenance mode (outside knowledge, not from the book); JMG itself cites resilience4j and failsafe (JMG p.59); use a maintained library and check the current state.

## 5. Timeout, bulkhead, fallback, and budgets

- Timeout: "without a timeout, the caller can block indefinitely"; clients should always use timeouts. [from source] (MS-MIC p.307) (MS-MIC p.309) Values: derive from the SLA (JMG p.59); avoid global timeouts and prefer per-context, configurable ones (SOA p.17). "500-1,500 ms" from the previous package was invented. [extrapolation]
- Bulkhead: Polly Bulkhead Isolation limits parallel calls (semaphore) and allows a queue outside the bulkhead; it allows rejecting the excess before executing; it exposes occupancy and overflow events, useful for autoscaling. [from source] (MS-MIC p.309) (MS-MIC p.310)
- Naval analogy of the bulkhead, isolation with dedicated thread pools/queues, and isolated tenants: [from source] (JMG p.60) (JMG p.61) MS-CLD only lists the Bulkhead policy in the Polly table. [from source] (MS-CLD p.124)
- Fallback: structured behavior after failure. [from source] (MS-CLD p.124)
- Time budget: retries, CB, and timeouts "eat" the SLA budget; calculate the remaining time to cut off disposable work. [from source] (JMG p.62)
- Persistent queues: if the architecture is message-based, queues should be persistent and replicated; in-memory-only events are lost if the process crashes. [from source] (JMG p.62)
- Rate limiters: control the rate of requests from a source and drop the excess; it is better to delegate to gateways and orchestration layers. [from source] (JMG p.62)
- Testing resilience: inject failures (chaos); in SDH, "implement chaos engineering". [from source] (MS-CLD p.127) (JMG p.63) (SDH p.64)

## 6. Health checks

- Health ≠ diagnostics: health is the microservice reporting its state for actions such as updating/deploying. [from source] (MS-MIC p.79)
- Liveness: whether the microservice is alive, that is, able to accept requests and respond. Readiness: whether the dependencies (database, queues) are ready for it to do its job. (Presented as the two types of checks in the AspNetCore.Diagnostics.HealthChecks library.) [from source] (MS-MIC p.79)
- The guide defines "healthy" for the example as an API reachable over HTTP and an available SQL database; it requires a front end (an orchestrator, for example) that queries the health reports. [from source] (MS-MIC p.326)
- Heartbeats/health checks allow early failure detection and avoid cascading failures. [from source] (MS-MIC p.325) (SDH p.22)
- Orchestrators: automatic health monitoring and failover (reprovisioning a failed instance). [from source] (MS-CLD p.24)
- The "critical anti-pattern" (checking the database in liveness causes a crash loop in Kubernetes) and the "kill the container/remove from the Service" actions from the previous package are NOT in the corpus. [extrapolation] Common good practice: keep liveness lightweight and put dependencies in readiness; check the current Kubernetes documentation.

## 7. Resilience in the platform and the mesh

- Redundancy: multiple instances, a load balancer that removes unhealthy instances, multi-region, geo-replication, DNS traffic manager; justify cost/complexity. [from source] (MS-CLD p.128) (MS-CLD p.129) (MS-CLD p.130)
- Service mesh: sidecar proxies take over service discovery, load balancing (choosing instances by observed latency), retry on another instance, eviction of instances with errors, metrics, and tracing; Istio/Envoy list circuit breaker and health checks. [from source] (MS-CLD p.133) (MS-CLD p.134) (MS-CLD p.135)
- MS-MIC note: from version 3.0.0 of eShopOnContainers, HTTP resilience came to be provided by the Linkerd mesh; Polly remains on the database connections. [from source] (MS-MIC p.306) [DATED] The Polly APIs in the code excerpts belong to the versions of the book's time.

## 8. Out of scope

Numeric tuning of thresholds, adaptive concurrency/advanced load shedding, SLO/error budget (SRE package), DR/RTO/RPO (only cited as terms in MS-CLD).
