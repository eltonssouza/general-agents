# Cloud-native, containers, and observability

Sources: MS-CLD (ch. 1, 3, 4, 6, 7), MS-MIC, JMG (ch. 12, 14-17), SDH. Pages = PDF (MS-CLD: printed = PDF - 10; JMG: printed = PDF - 15). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Azure products and Java tools in the books reflect ~2019-2023; check the current documentation.

## 1. The twelve factors (MS-CLD table)

MS-CLD presents the methodology as "widely accepted" and a reasonable foundation for cloud-native. [from source] (MS-CLD p.16)

| # | Factor | What MS-CLD says |
| :-: | :--- | :--- |
| 1 | Code Base | one code base per microservice, in its own repository, versioned, deployable to several environments [from source] (MS-CLD p.16) |
| 2 | Dependencies | each microservice isolates and packages its dependencies [from source] (MS-CLD p.16) |
| 3 | Configurations | configuration externalized by a tool outside the code; the same deployment propagates across environments [from source] (MS-CLD p.16) |
| 4 | Backing Services | data stores, caches, and brokers exposed by an addressable URL, interchangeable [from source] (MS-CLD p.16) |
| 5 | Build, Release, Run | strict separation, with a unique ID and rollback capability; CI/CD [from source] (MS-CLD p.17) |
| 6 | Processes | each microservice in its own process; state externalized in a backing service [from source] (MS-CLD p.17) |
| 7 | Port Binding | each service self-contained, with interfaces exposed on its own port [from source] (MS-CLD p.17) |
| 8 | Concurrency | scale out with identical copies instead of one giant instance [from source] (MS-CLD p.17) |
| 9 | Disposability | disposable instances, fast startup, and graceful shutdown [from source] (MS-CLD p.17) |
| 10 | Dev/Prod Parity | environments as similar as possible; containers help [from source] (MS-CLD p.17) |
| 11 | Logging | logs as event streams, processed by an aggregator [from source] (MS-CLD p.17) |
| 12 | Admin Processes | administrative tasks as one-off processes, separate from the application [from source] (MS-CLD p.17) |

- Configuration via environment variables is also advocated in JMG, which points out the limitation: they are static and a change may require a restart; dynamic configuration costs instrumentation. [from source] (JMG p.108) MS-CLD's wording mentions "externalize in a configuration management tool" and injecting via environment variable when promoting between environments. [from source] (MS-CLD p.26)
- Factors 9, 8, 6, and 5 are discussed together with containers/orchestrators and CI/CD. [from source] (MS-CLD p.25) (MS-CLD p.27) (MS-CLD p.28)

## 2. Containers, orchestration, and Kubernetes

- Containers give portability and consistency across environments and a smaller footprint than VMs. [from source] (MS-CLD p.23) (MS-CLD p.24)
- Tasks of an orchestrator: scheduling, affinity/anti-affinity, health monitoring, failover, scaling, networking, service discovery, rolling upgrades with rollback. Kubernetes is "the de facto standard" in the cloud-native world. [from source] (MS-CLD p.24) (MS-CLD p.25)
- Autoscaling in AKS: the Horizontal Pod Autoscaler watches resource demand and scales pod replicas out and in; KEDA exposes custom metrics to the HPA for event-driven workloads. [from source] (MS-CLD p.60) (MS-CLD p.64)
- Ingress: a Kubernetes resource with rules for exposing services (HTTP/L7); the Application Gateway Ingress Controller integrates it with Azure. [from source] (MS-CLD p.73)
- Not every application needs this: smaller, lower-impact apps may be fine as a monolith on PaaS. [from source] (MS-CLD p.29) (MS-CLD p.31)
- "Pods", "Services", and other Kubernetes concepts are described superficially; the corpus is not a Kubernetes manual. [extrapolation] What is not above ("Pods, Ingress, HPA" of the previous package as a full chapter) should be checked in the official documentation.
- Serverless: SDH defines it as a model in which the provider manages infrastructure and scaling, with event-triggered functions and billing by compute time. [from source] (SDH p.47)

## 3. Observability

- JMG: observability is measuring, collecting, and analyzing signals (metrics, traces, logs, events, profiles) to locate problems and their cause; three pillars covered: logs, metrics, and distributed tracing. [from source] (JMG p.129) (JMG p.144) (JMG p.145)
- MS-CLD: three patterns for reliable operation: logging, monitoring, and alerts. [from source] (MS-CLD p.136)
- Logs: local files lose usefulness in the cloud (ephemeral disk, requests spread across services); prefer centralized logs; generate a correlation ID at the start of a long interaction and record it in every related message; standardize the format across services; adjustable log levels (Serilog example). [from source] (MS-CLD p.137) (MS-CLD p.138) (MS-CLD p.139)
- MS-MIC: different teams should agree on a single logging format and a consistent way of viewing diagnostic events. [from source] (MS-MIC p.79)
- Monitoring: centralized systems collect metrics (query time, average response time, CPU/memory) and business counters; dashboards; alerts triggered by metric values, log queries, events, platform health, and availability tests. [from source] (MS-CLD p.140) (MS-CLD p.150)
- Cost of metrics: total number of metrics and of distinct time series, storage (memory is expensive, disk is cheap), raw vs. pre-aggregated metrics. [from source] (JMG p.144)
- Distributed tracing: a method to profile and monitor microservice applications; logs are "flat" and do not show causality; three ingredients: instrumentation, infrastructure, and visualization; propagating context is harder in Kafka/gRPC than in HTTP; Zipkin and Brave are examples; the concept comes from the Dapper paper (Google, 2010). [from source] (JMG p.145) (JMG p.146) (JMG p.147)
- Service mesh integrates logs, metrics, and tracing (Istio with Jaeger/Zipkin). [from source] (JMG p.152) (MS-CLD p.134)
- [DATED] OpenTelemetry and W3C Trace Context appear in JMG as recent initiatives: OpenTelemetry "available only as a draft specification" and Trace Context as a "draft" (JMG p.141, p.152). Today they are consolidated standards (outside knowledge, not from the book); check the documentation. The previous package attributed OpenTelemetry/TraceContext to MS-CLD, which does not mention them.
- Heartbeats and health checks: see `resiliencia-e-tolerancia-a-falhas.md` (section 6). SDH's system logging and monitoring: [from source] (SDH p.64) (SDH p.75)

## 4. Out of scope

Cloud-native security (MS-CLD ch. 8-9 and MS-MIC ch. 9, not audited in this package), IaC/GitOps (MS-CLD p.27 merely mentions Terraform/ARM), cloud costs, SRE (see the SRE package).
