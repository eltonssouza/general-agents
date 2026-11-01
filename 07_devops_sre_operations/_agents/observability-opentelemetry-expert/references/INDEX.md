# Reference index: observability-opentelemetry-expert

Sources (two DZone Refcards, both from 2021, 7 pages each):

- **[DOW]** *Getting Started With Observability for Distributed Systems* (DZone Refcard; Nicolas Giron and Hicham Bouissoumer, KumoMind; (c) 2021 Devada). File: `Distributed-Observability-Whitepaper.pdf`.
- **[OTW]** *Getting Started With OpenTelemetry: Observability and Monitoring for Modern Applications* (DZone Refcard; Charles Mahler, InfluxData; (c) 2021 Devada). File: `OpenTelemetry-Whitepaper.pdf`.

## Page convention
Cited page = **PDF page** (1 to 7 in each work). It matches the number printed in the footer: p.1 is the cover (printed number "1"), **p.2 of each PDF is a sponsor ad with no technical content** (no printed number) and p.3 to 7 have the printed number equal to the PDF's. No conversion map is needed. Citation format: `[from source] (DOW p.N)` or `(OTW p.N)`; range `(DOW p.5-6)`.

## Labels
- `[from source]`: read on the cited page. `[inference]`: direct deduction from the text. `[extrapolation]`: external knowledge (not in the Refcards). `[DATED]`: 2021 state that has since changed. No label = do not use.
- Both Refcards are **introductory and short**: most of the practical observability knowledge (SLOs, cardinality, advanced sampling, semantic conventions, the W3C propagation header) is **not** in them.

## Thematic map

| File | When to open | Pages |
| --- | --- | --- |
| `observabilidade-conceitos-e-pilares.md` | monitoring vs observability, metrics/logs/traces, graphs and alerts, 3 vs 5 pillars tension | DOW 3-5 |
| `plataforma-e-coleta-em-sistemas-distribuidos.md` | platform checklist, how to monitor/log/trace, agents, collectors | DOW 5-6 |
| `opentelemetry-arquitetura-e-collector.md` | APIs, SDKs, Collector, YAML pipelines, Agent vs Gateway, OTLP | OTW 1, 3 |
| `opentelemetry-sinais-tracing-e-contexto.md` | traces/spans/metrics/logs in OTel, Tracer Provider, sampling, Context API, Python, auto vs manual, legacy | OTW 4-6 |
| `backends-e-escolhas-de-armazenamento.md` | where to send data (Jaeger, Zipkin, Prometheus, InfluxDB, ELK...) | OTW 7, DOW 6 |
| `diagramas-e-figuras.md` | what each diagram shows (DOW Fig 1-3, OTW before/after the Collector) | DOW 3,5,6; OTW 3 |
| `fronteira-e-datado.md` | what the sources do NOT cover and what is dated | all |
| `procedimentos.md` | playbooks P1-P5 | DOW 5-6; OTW 3-6 |
| `casos-e-antipadroes.md` | supported and unsupported anti-patterns | all |
| `glossario.md` | terms | all |

Scripts: `scripts/obs_lookup.py` (+ `obs_index.json`), `scripts/collector_pipeline_check.py`, `scripts/signal_advisor.py`. Audit: `tests/verify_citations.py` + `tests/citation-checks.json`.
