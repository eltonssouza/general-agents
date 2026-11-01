# Glossary (EN/PT) with sources

Short definitions, written in English, with the page where the corpus defines or uses the term. Pages = PDF. A term without a page = general vocabulary (labeled). Labels: `[from source]`, `[extrapolation]`.

| Term (EN) | Term (PT) | Short definition | Source |
| :--- | :--- | :--- | :--- |
| 2PC / two-phase commit | commit em duas fases | protocol with separate prepare and execute steps, which holds transactional resources stateful and hurts the asynchronous flow | [from source] (SBC p.3) |
| ACID / BASE | ACID / BASE | atomic, consistent transactions vs. basic availability, "soft" state, and eventual consistency | [from source] (SOA p.18) |
| API Gateway | gateway de API | single entry point for groups of microservices; reverse proxy with cross-cutting functions | [from source] (MS-MIC p.57) (MS-MIC p.59) |
| Application service / Enterprise service / Business service | serviço de aplicação / corporativo / de negócio | SOA service types, from abstract to application-specific | [from source] (SOA p.23) (SOA p.24) |
| Architecture sinkhole | sumidouro de arquitetura | requests pass through the layers without logic; 80-20 rule | [from source] (SAP p.14) |
| At-least-once / exactly-once | pelo menos uma vez / exatamente uma vez | the corpus treats "exactly once" as idempotency + atomic commit; the terms as a named taxonomy are [extrapolation] | [from source] (EDS p.130) |
| Availability | disponibilidade | proportion of operational time; Uptime/(Uptime+Downtime) | [from source] (SDH p.7) |
| Backing service | serviço de apoio | auxiliary resource (data, cache, broker) attachable by URL | [from source] (MS-CLD p.16) (MS-CLD p.26) |
| Bloom filter | filtro de Bloom | probabilistic structure: "definitely absent" or "possibly present" | [from source] (SDH p.25) |
| Bounded Context | contexto delimitado | DDD model and data boundary; correlates with a microservice | [from source] (MS-MIC p.43) (MS-MIC p.44) (SOA p.33) |
| BFF (Backend for Frontend) | backend para frontend | one gateway per client type | [from source] (MS-MIC p.58) (MS-CLD p.71) |
| Broker topology / Mediator topology | topologia broker / mediador | EDA without a central mediator vs. with a mediator that orchestrates | [from source] (SAP p.18) (SAP p.21) |
| Bulkhead | anteparo/isolamento | limiting resources per dependency so that one does not overload everything | [from source] (MS-MIC p.309) (JMG p.60) |
| CAP | CAP | consistency, availability, and partition tolerance: all three cannot be guaranteed | [from source] (SDH p.9) |
| CDC | captura de mudanças | translating the database write log into events | [from source] (EDS p.82) |
| Chattiness | tagarelice | excessive calls between services | [from source] (JMG p.19) |
| Choreography / Orchestration | coreografia / orquestração | coordination without a mediator vs. by a central mediator | [from source] (SOA p.34) (SOA p.35) (EDS p.55) |
| Circuit breaker | disjuntor | fail fast after repeated failures; periodic test call | [from source] (MS-MIC p.309) (MS-CLD p.126) |
| Command / Event / Query | comando / evento / consulta | request for action / fact that occurred / read without side effects | [from source] (EDS p.45) (EDS p.46) |
| Compacted topic | tópico compactado | keeps only the latest event per key | [from source] (EDS p.39) |
| Compensating action/transaction | ação/transação compensatória | undoes the effect of an operation already completed | [from source] (SBC p.3) (MS-CLD p.102) |
| Competing consumers | consumidores concorrentes | several consumers reading the same queue | [from source] (SBC p.1) |
| Consistent hashing | hash consistente | hash ring; only a small part of the data is reassigned when nodes change | [from source] (SDH p.18) |
| Consumer group | grupo de consumidores | consumers that divide the partitions of a topic | [from source] (EDS p.35) |
| Contract decoupling | desacoplamento de contrato | transforming message/protocol without changing consumers; an SOA capability | [from source] (SOA p.49) (SOA p.50) |
| Correlation identifier | identificador de correlação | links the response/product to the request | [from source] (SBC p.1) (MS-CLD p.81) (MS-CLD p.139) |
| CQRS / CQS | CQRS / CQS | separating read from write (model) / methods that either read or change state | [from source] (MS-MIC p.199) (MS-MIC p.200) |
| Dead letter queue | fila de mensagens mortas | destination for unprocessable messages | [from source] (EDS p.142) |
| Distributed monolith | monólito distribuído | remote services with monolith-like coupling | [from source] (JMG p.18) (JMG p.19) |
| Event-carried state transfer | transferência de estado por evento | event replicates data to the consumer | [from source] (EDS p.52) (EDS p.53) |
| Event Sourcing | event sourcing | state derived from an immutable log of events | [from source] (EDS p.70) (MS-CLD p.104) |
| Event-sourced view / projection | visão derivada / projeção | read model regenerable from the log | [from source] (EDS p.86) |
| Eventual consistency | consistência eventual | convergence with no guarantee of when | [from source] (SDH p.29) |
| Idempotent receiver | receptor idempotente | ignores duplicates, allowing safe retry | [from source] (SBC p.2) (MS-MIC p.165) |
| Idempotent / safe (HTTP) | idempotente / seguro | same effect if repeated / does not modify the resource | [from source] (JMG p.22) |
| Integration event | evento de integração | event between bounded contexts/services | [from source] (MS-MIC p.71) |
| Layers of isolation / closed layer | camadas de isolamento / camada fechada | change isolated within one layer | [from source] (SAP p.10) |
| Liveness / readiness | liveness / readiness | alive and able to respond / dependencies ready | [from source] (MS-MIC p.79) |
| Materialized view | visão materializada | denormalized local copy of data owned by others | [from source] (MS-CLD p.79) (MS-CLD p.101) |
| Microkernel | microkernel | core + plug-ins | [from source] (SAP p.28) |
| Optimistic concurrency control | controle otimista de concorrência | version check before writing | [from source] (EDS p.124) |
| Outbox | outbox | events table in the same local transaction, published afterwards | [from source] (MS-MIC p.73) (MS-MIC p.159) |
| Partition (Kafka) | partição | unit of ordering and parallelism; order only within the partition | [from source] (EDS p.34) (EDS p.36) |
| Polyglot persistence | persistência poliglota | different stores per service | [from source] (MS-MIC p.44) (MS-CLD p.99) |
| Processing unit / virtualized middleware | unidade de processamento / middleware virtualizado | components of the space-based architecture | [from source] (SAP p.45) (SAP p.46) |
| Rate limiting | limitação de taxa | protecting a service from excess requests; token bucket, leaky bucket, and window algorithms | [from source] (SDH p.14) (APIGW p.22) |
| Request-reply (queues) | requisição-resposta por filas | two queues and a correlation ID | [from source] (MS-CLD p.80) (MS-CLD p.81) |
| Retry / backoff / jitter | nova tentativa / recuo / ruído | repeating with increasing, randomized waiting | [from source] (MS-MIC p.310) (MS-MIC p.321) |
| Saga | saga | sequence of local transactions with compensations | [from source] (MS-CLD p.102) (JMG p.63) |
| Service discovery / registry | descoberta de serviços | registry as the single source of truth | [from source] (SDH p.24) |
| Service mesh / sidecar | malha de serviços / sidecar | infrastructure layer with a proxy next to each service | [from source] (MS-CLD p.95) (MS-CLD p.133) |
| Share-as-little-as-possible | compartilhar o mínimo | microservices philosophy (SOA: share as much as possible) | [from source] (SOA p.32) |
| Single writer principle | princípio do escritor único | one service owns the evolution of a data type | [from source] (EDS p.120) (EDS p.121) |
| SLA | acordo de nível de serviço | each service should have one defined | [from source] (JMG p.58) |
| Space-based | baseada em espaço | replicated in-memory data grids without a central database | [from source] (SAP p.45) |
| Tail latency | latência de cauda | high latency percentiles; amplification by N dependencies is [extrapolation] | [extrapolation] |
| Timeout | tempo limite | never wait indefinitely | [from source] (MS-MIC p.309) |
| Tombstone / delete marker | marcador de exclusão | message with a null value that removes the key on compaction | [from source] (EDS p.142) (EDS p.143) |
| Twelve-factor | doze fatores | cloud-native methodology | [from source] (MS-CLD p.16) (MS-CLD p.17) |
| Write-off | baixa/descarte | tolerating the failure when fixing it costs more | [from source] (SBC p.2) |

General-use terms cited in this package that have no origin in the corpus: Little's law, PACELC (only the name in MS-CLD p.107), full jitter, half-open, pivot transaction, Strangler Fig. [extrapolation]
