# OpenTelemetry: architecture, Collector and OTLP [OTW p.1, 3]

## What it is and why it exists (OTW p.1)
- [from source] Open-source collection of tools, APIs, SDKs and specifications to **standardize how telemetry is modeled and collected**; born from the merger of OpenCensus (Google) and OpenTracing (CNCF); contributors cited: Microsoft, Red Hat, Google, Amazon, Shopify, Datadog, Facebook (OTW p.1).
- [from source] Long-term goal: a standardized, **vendor-independent** solution to instrument applications and send telemetry to **any backend without changing the code**; it reduces the effort of maintaining instrumentation and eliminates the risk of lock-in due to switching cost (OTW p.1).
- [from source] Telemetry is time-series data, with properties that are hard for traditional databases, which gave rise to an ecosystem of optimized tools (OTW p.1). [DATED] The characterization "only tracing stable" is from 2021 (see `fronteira-e-datado.md`).

## APIs and SDKs (OTW p.1, 3)
- [from source] APIs and SDKs are the **language-specific** part. The **APIs** instrument the code and **generate** the telemetry (OTW p.1). The **SDKs** are the bridge between the API and export; they can **filter or sample** before exporting and export to multiple destinations according to configuration (OTW p.3).

## Collector (OTW p.3)
- [from source] Alternative to in-process exporters dedicated to each backend; it is vendor **and** language independent: it receives from any SDK and exports to any supported backend without touching the application (OTW p.3).
- [from source] Three components: **Receivers** (typically listen on network ports, but can pull), **Processors** (enrich/transform between reception and export; run in the **configured sequence, so order matters**), **Exporters** (forward to backends; there can be several, to route specific types or replicate to multiple destinations) (OTW p.3).
- [from source] Components are assembled into **pipelines defined in YAML**. The p.3 example: receiver `otlp` (grpc and http protocols), processor `batch`, exporter `otlp` with endpoint `otelcol:4317`, extensions `health_check`, `pprof`, `zpages`, and three pipelines (`traces`, `metrics`, `logs`) linking receiver, processor and exporter (OTW p.3). [inference] The text does not explain the extensions or `batch`; use only what the page says.
- [from source] Two deployment modes: **Agent** (Collector alongside the application on the same host: binary, sidecar via service mesh or DaemonSet in Kubernetes) is the **recommended option**, since it allows collection by push or pull and enriching data with custom tags and hardware information; **Gateway** (Collector as an independent service, several instances, usually per application cluster or datacenter) is more complicated, but offers API token management and scale flexibility (OTW p.3).

## OTLP (OTW p.3)
- [from source] Specification of how to **encode, transport and deliver** telemetry between sources, intermediate nodes (collectors) and backends; it uses gRPC or HTTP and a specific Protocol Buffer schema (OTW p.3). [extrapolation] Default ports (4317/4318) and protocol version details are not in the pages; 4317 appears only in the example YAML.

## What the text does NOT detail (boundary)
Advanced Collector configuration (processors beyond `batch`, `memory_limiter`, `tail_sampling`, contrib distributions, authentication, TLS), performance tuning and Collector high availability. All of that is [extrapolation].
