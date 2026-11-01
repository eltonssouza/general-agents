# OpenTelemetry: signals, tracing, context and instrumentation [OTW p.4-6]

## Observability and instrumentation (OTW p.4)
- [from source] Goal of observability: to understand what happens inside the application at any moment through telemetry about performance, behavior and health; it makes finding bugs and bottlenecks easier (OTW p.4).
- [from source] **Instrumentation** = adding the OpenTelemetry SDK to the application so that it emits signals (typically logs, metrics and trace spans); there are **automatic and manual** options (OTW p.4).
- [from source] Three supported data sources: traces, metrics and logs, with the possibility of more in the future (OTW p.4).

## The three signals (OTW p.4)
- **Traces** [from source]: follow a single transaction (e.g. API request, periodic job) through an application or network of applications. For each operation touched a **span** is created that records duration, errors and a **reference to the parent span**; following the transaction shows which service/operation causes slowness or failure (OTW p.4). Backends cited: Zipkin or Jaeger (OTW p.4). The text also cites uses outside software (manufacturing, logistics) as illustration (OTW p.4).
- **Metrics** [from source]: measurements of a service at a moment; typically **aggregated in the emitting application** and collected at fixed intervals (from every second to once a day); they serve as a reference for alerts and automatic actions when thresholds are exceeded. Examples: success/error rate (42 req/s), latency (count per histogram bucket), bandwidth usage (12%) (OTW p.4).
- **Logs** [from source]: timestamped records with metadata, structured or not; in OpenTelemetry they can be **independent or attached to spans** and serve root-cause analysis (OTW p.4).

## State of the specifications in 2021 [DATED] (OTW p.4)
[from source] In 2021 only the Tracing specification was stable (inherited from OpenTracing); Metrics had v1.0 expected for the end of 2021; Logs was in draft, with v1.0 perhaps in 2022; because of the risk of breaking changes the Refcard **does not detail** Metrics and Logs (OTW p.4). [DATED] Check the current state in the project documentation.

## Tracing SDK (OTW p.4-5)
- [from source] **Tracer Provider**: SDK method that creates trace objects and configures span processors, sampling, unique ID generation and span limits (OTW p.4).
- [from source] **Sampling**: the SDK can sample the number of traces exported, for performance or cost (OTW p.4). [extrapolation] Strategies (head, tail, probabilistic) are not in the text.
- [from source] **Span processors**: turn telemetry into an exportable format; the SDK must provide a pipeline of several processors in the order they were registered on the provider (OTW p.5).

## Tracing API (OTW p.5)
- [from source] **Trace**: creates spans; it does not exist without an SDK Tracer Provider. **Span**: one operation within a trace; spans nest in a **tree** with a **root span** covering the whole operation; they must have a recognizable name, a unique ID and a trace ID to connect the spans of the trace. **SpanKind**: describes relationships between spans (e.g. synchronous calls to other services), helping to see where there is latency. **SpanContext**: for nested spans with a context different from the overall trace (OTW p.5).
- [extrapolation] In code the API uses the **Tracer** object to create spans (the text calls the creating object "Trace"); the text describes SpanContext vaguely (see glossary). SpanKind values (CLIENT, SERVER, PRODUCER...) are not listed; only `SpanKind.SERVER` appears in the manual Flask example (OTW p.6) and `SpanKind.INTERNAL` in the output (OTW p.6).

## Context API and propagation (OTW p.5)
- [from source] Needed to follow requests across services: trace ID, span ID and current span state. OpenTelemetry **injects** the context into the **request headers** and **extracts** it in the receiving service: "context propagation". You normally do not think about it, but it is possible to attach user-defined properties (e.g. user ID, server name, datacenter region) for later analysis (OTW p.5).
- [inference] The text does not name the header format; [extrapolation] the standard is W3C Trace Context (listed only as further reading in DOW p.7).

## Python example (OTW p.5-6) [DATED in versions]
- [from source] `opentelemetry-api` and `opentelemetry-sdk` are installed via pip; the `TracerProvider` is created, a `BatchSpanProcessor` with `ConsoleSpanExporter` is added (the batch groups spans before sending; the console is for testing), the tracer is obtained and a span is opened with `start_as_current_span` (OTW p.5).
- [from source] The JSON output shown has name, context (trace_id, span_id, trace_state), kind INTERNAL, null parent_id, start/end time, status UNSET, attributes, events, links and resource with `telemetry.sdk.*` (version 1.7.1) and `service.name` equal to `unknown_service` (OTW p.6). [inference] `unknown_service` indicates the service was not named; [extrapolation] naming the service via resource is common practice, not stated in the text.
- [DATED] Imports, SDK version and `pip install` are from 2021; check the current documentation.

## Automatic vs manual (Flask, OTW p.6)
- [from source] Manual: the developer imports API and SDK, configures provider and processor, extracts context from the headers (`extract(request.headers)`), sets `kind=SERVER` and request attributes, inside `start_as_current_span`. Automatic: `FlaskInstrumentor().instrument_app(app)` replaces all of this (OTW p.6). There are packages for Django and databases such as MongoDB and PostgreSQL (OTW p.6).
- [from source] In large applications automatic saves a lot of repetitive code, but **you lose control**; in some cases it is worth customizing (OTW p.6). The trend is more frameworks with native support (OTW p.6).

## Legacy migration (OTW p.6)
- [from source] Greenfield: using OpenTelemetry is easy; legacy: refactoring may not be worth the time and brings risk; the alternative is to keep it and use a tool such as **Telegraf** to convert the current telemetry and emit it to OpenTelemetry (OTW p.6).
