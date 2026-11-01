# Glossary (terms as in the sources; own explanation)

| Term | Meaning in the sources | Page |
| --- | --- | --- |
| Distributed system | components on several servers that coordinate and appear as a single system | DOW p.1 |
| Monitoring | obtains state through predefined measurements for known problems; says "when" | DOW p.3 |
| Observability | understanding system state through several outputs; capability designed from the start; says "why" | DOW p.3 |
| Pillars | 3 (logs, metrics, traces; p.3) or 5 (3 for collection + alerting and graphing; p.5) | DOW p.3, 5 |
| Metrics | numeric measurements of state, groupable by tags | DOW p.4; OTW p.4 |
| Log | immutable timestamped record; text, structured or binary | DOW p.4; OTW p.4 |
| Trace | lifecycle of a request across services | DOW p.4; OTW p.4 |
| Span | segment of a trace for one operation: duration, errors, reference to the parent | OTW p.4-5 |
| Trace ID / Span ID | identifiers that connect the spans of a trace | OTW p.5 |
| Root span | span that covers the whole operation, top of the tree | OTW p.5 |
| SpanKind | relationship between spans (e.g. synchronous call between services) | OTW p.5 |
| SpanContext | context of nested spans; vague description in the text | OTW p.5 |
| Tracer Provider | SDK method that creates trace objects and configures processors, sampling, IDs and limits | OTW p.4 |
| Span processor | turns telemetry into an exportable format; runs in an ordered pipeline | OTW p.5 |
| BatchSpanProcessor | processor that groups spans before exporting | OTW p.5 |
| ConsoleSpanExporter | exports to the terminal; useful in testing | OTW p.5 |
| Sampling | exporting only part of the traces for performance or cost | OTW p.4 |
| Context API / context propagation | injecting context into headers and extracting it in the receiving service | OTW p.5 |
| Instrumentation | adding the SDK to the application so it emits signals; automatic or manual | OTW p.4 |
| API / SDK (OTel) | the API generates telemetry; the SDK exports, filters, samples | OTW p.1, 3 |
| Collector | vendor- and language-agnostic service: receivers, processors, exporters | OTW p.3 |
| Pipeline (Collector) | chaining of receivers-processors-exporters in YAML, per signal | OTW p.3 |
| Agent / Gateway | Collector on the application host (recommended) / independent service | OTW p.3 |
| OTLP | protocol to encode, transport and deliver telemetry (gRPC/HTTP + Protobuf) | OTW p.3 |
| Collection agent (DOW) | process on each system that collects data; must be monitored | DOW p.6 |
| Auto discovery | automatic discovery of endpoints (e.g. Kubernetes, Consul) | DOW p.5 |
| APM | application performance monitoring tool; end-to-end traces | DOW p.6 |
| Service mesh | proxies between endpoints that track requests and collect traces | DOW p.6; OTW p.3 |
| TSDB | time-series database to centralize and visualize metrics | DOW p.6; OTW p.7 |
| Lock-in | vendor dependency due to switching cost; OTel aims to eliminate it | OTW p.1 |
