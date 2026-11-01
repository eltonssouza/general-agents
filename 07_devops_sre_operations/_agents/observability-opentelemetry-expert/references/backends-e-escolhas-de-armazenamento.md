# Backends and storage choices [OTW p.7; DOW p.5-6]

## What the OTW lists (OTW p.7)
- **Traces** [from source]: Zipkin (older, released by Twitter) and Jaeger (newer, graduated in the CNCF, like Kubernetes and Prometheus; a sign that in the long run it may be the stronger choice). Similar visualization features, both with an OpenTelemetry exporter and several storage backends (OTW p.7). [DATED] 2021 judgment about "stronger in the long run"; reassess.
- **Metrics** [from source]: two leaders, InfluxDB and Prometheus, both open-source time-series tools, with a query language, visualization, alerting and integrations (OTW p.7). [DATED] The OTW is sponsored by InfluxData and written by one of its employees (OTW p.1, 7); consider vendor bias.
- **Logs** [from source]: depends on how you want to work: convert them into structured metrics and use a time-series database; Telegraf, Logstash or FluentD process raw logs before storage; for semi-structured/unstructured logs, ElasticSearch is a common choice (OTW p.7).
- [from source] Central message: OpenTelemetry gives **options**; choosing tools is a trade-off between convenience, features, cost and usability (OTW p.7). Switching backend is, according to the text, changing a little exporter configuration of the standardized exporters, without refactoring code (OTW p.7).

## What the DOW adds (DOW p.5-6)
- [from source] The central platform can be a time-series database with visualization and alerting (DOW p.6); figure 3 shows the observability platform with Archive, Compression, Retention and Encryption (DOW p.6). Distributed storage is a checklist criterion (DOW p.5).

## Outside the text
[extrapolation] Comparing cost, scale, query language and retention across backends, or citing Grafana, Loki, Tempo, Elastic APM etc.: none of that is in the Refcards. If you cite it, label it [extrapolation] and [DATED].
