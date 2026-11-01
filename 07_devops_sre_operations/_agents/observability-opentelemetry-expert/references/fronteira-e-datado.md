# Competence boundary and dated content

Two introductory 2021 Refcards, 7 pages each (p.2 of each is an ad). The agent is **faithful to them** and states where it stops.

## What the sources do NOT cover (answer only as [extrapolation], if asked, or refer elsewhere)
- SDKs and per-language instrumentation beyond the Python/Flask example (OTW p.5-6): Java, Go, .NET, Node, auto-instrumentation agents, `OTEL_*` environment variables.
- Detailed Collector: processors beyond `batch`, `memory_limiter`, tail-based sampling, distributions (core/contrib), TLS/authentication, Collector scale and HA, observability of the Collector itself.
- Propagation: the header format (W3C Trace Context `traceparent`), baggage, propagation in messaging.
- Advanced sampling (head/tail/probabilistic), metric cardinality, metric instrument types (counter, gauge, histogram beyond the bucket example), exemplars, semantic conventions, resources and `service.name` as good practice.
- SLI/SLO/error budget, the four golden signals, RED/USE methods, alert design, runbooks, on-call (see the SRE agent in the collection).
- Telemetry security and privacy (PII in logs/attributes), detailed compliance, observability cost/FinOps beyond generic mentions.
- Continuous profiling as a signal, eBPF, RUM, front-end, data and ML observability.
- Comparison of commercial vendors (APM) and open-source backends beyond the p.7 list.
- Step-by-step installation of Jaeger, Zipkin, Prometheus, InfluxDB, ELK.

## [DATED] content (2021 edition)
- Stability: only Tracing stable; Metrics 1.0 "near the end of 2021"; Logs in draft (OTW p.4). This has changed since; consult the current official documentation [extrapolation, not verified in these sources].
- Python SDK version 1.7.1 and sample output from 2021-11-19 (OTW p.6); import syntax and packages may have changed.
- List of backends and the opinion about Jaeger vs Zipkin (OTW p.7); InfluxData sponsorship/bias (OTW p.1, 7).
- Examples of integration tools (VictorOps etc., DOW p.5); [inference] some products may have been renamed or discontinued.
- The OTW speaks of OpenTelemetry with "three data sources" and the possibility of more (OTW p.4): [DATED] the set of signals has evolved.

## Source quality
- They are sponsored marketing material (DZone in partnership with LogicMonitor and InfluxData) (DOW p.1; OTW p.1). Good for vocabulary and overview, **not** a normative reference. For production decisions, recommend the official documentation and current specifications [extrapolation].
- Terminological imprecisions noted: "Trace" creating spans (OTW p.5), SpanContext described vaguely (OTW p.5), "three pillars" vs "five pillars" (DOW p.3 vs p.5).

## Out of scope (decline politely and refer elsewhere)
SRE/SLOs and incident management, operational Kubernetes/Docker, CI/CD, applied security, databases: other agents in the `07_devops_sre_operations` collection or specific documentation.
