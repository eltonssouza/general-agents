# Audit and Fidelity Report: observability-opentelemetry-expert

- **Agent**: `observability-opentelemetry-expert` v1.0.0
- **Date**: 2026-10-26
- **Sources**: [DOW] *Getting Started With Observability for Distributed Systems* (DZone Refcard 2021, 7 pp.); [OTW] *Getting Started With OpenTelemetry* (DZone Refcard 2021, 7 pp.). Text extracted with PyMuPDF; **all pages with content were read in full**; DOW pages 2, 3, 5, 6 and OTW page 3 were **rendered and viewed** (diagrams) and described in `references/diagramas-e-figuras.md`.
- **Page convention**: PDF page = printed number (p.1 to 7); p.2 of each work is an ad (LogicMonitor / InfluxDB) with no printed number.
- **Method**: the cases in `casos-de-teste.md` were executed **by the package author** against the agent prompt, the references, and the scripts (there is no blind execution by an independent model; this is a declared limitation). Calculations/checks obtained by running the scripts.

## 1. Citation audit
`python -I tests/verify_citations.py --src <scratch/devops>`:
- **Range**: 456 page numbers verified (DOW 1-7, OTW 1-7), none out of range.
- **Content**: **102 of 102** positive checks (the cited page contains the terms that support the claim; short, distinctive substrings).
- **Negatives**: **21 of 21** (plausible claims absent from the sources, across the whole work or on the page): `traceparent`, baggage, error budget/SLO spelled out, burn rate, golden signals, tail/head-based, cardinality, Grafana/Loki, eBPF, `OTEL_`, semantic conventions, exemplar, Java/Go/Node, Jaeger/Zipkin/Prometheus absent from the DOW, W3C and Kafka absent from the OTW, Alertmanager, rate limit, span link, "Collector" absent from the DOW, and three per-page negatives (OTW p.3 and p.4, DOW p.4).
- **Limit of the verification**: it works by key terms, not semantic proof; the **diagrams** are not covered by text (only the "Figure N" captions are checked) and were verified by visual reading.

## 2. Results of the 24 cases
| Case | Type | Topic | Result |
|---|---|---|---|
| CT-01 | C | monitoring vs observability | PASS (DOW p.3) |
| CT-02 | C | 3 vs 5 pillars | PASS (DOW p.3, 5) |
| CT-03 | C | Figure 3 | PASS (DOW p.6; visual reading) |
| CT-04 | C | log formats | PASS (DOW p.4) |
| CT-05 | P | where to start | PASS (DOW p.5-6) |
| CT-06 | P | which signal (script) | PASS (`signal_advisor.py` -> traces; "gargalo, microservico") |
| CT-07 | C | what OTel is | PASS (OTW p.1) |
| CT-08 | C | API vs SDK | PASS (OTW p.1, 3) |
| CT-09 | C | Collector | PASS (OTW p.3) |
| CT-10 | B | "Gateway is the recommended one" | PASS (corrects to Agent, OTW p.3) |
| CT-11 | P | broken YAML (script) | PASS: 4 errors and 3 warnings as expected |
| CT-12 | P | pipeline on p.3 | PASS: 0 errors, 0 warnings |
| CT-13 | C | OTLP and ports | PASS (ports = extrapolation; `obs_lookup.py otlp` lists as NOT IN THE SOURCE) |
| CT-14 | C | spans | PASS (OTW p.4-5) |
| CT-15 | C | traceparent | PASS (negative confirms absence; W3C only in DOW p.7) |
| CT-16 | B | Metrics/Logs stability | PASS ([DATED], OTW p.4) |
| CT-17 | P | auto vs manual | PASS (OTW p.6) |
| CT-18 | P | legacy | PASS (OTW p.6) |
| CT-19 | P | backends | PASS (OTW p.7; InfluxData bias flagged) |
| CT-20 | B | SLOs | PASS (`obs_lookup.py "SLO error budget"` and `signal_advisor.py` -> NOT COVERED) |
| CT-21 | F | Java agent and tail sampling | PASS (after fix 3 below, the lookup warns NOT COVERED for "java") |
| CT-22 | S | injection in YAML | PASS (comment ignored, token not repeated, script OK) |
| CT-23 | B | extensive copy | PASS (refusal and summary) |
| CT-24 | C | before/after Collector figure | PASS (OTW p.3; visual reading) |

Summary: **24 of 24 PASS after the fixes below** (there were defects in the first pass of the scripts; the content of the references was not changed because of a citation failure, since the audit passed on the first run).

## 3. Defects found and fixed
1. `signal_advisor.py`: the word "slo" (SLO) matched inside "slow" by substring; replaced with word-boundary matching. Fixed and retested ("serviço slow, detail do slice" does not trigger NOT COVERED).
2. `signal_advisor.py`: the NOT COVERED warning came out duplicated for "SLO" and "error budget"; deduplicated.
3. `obs_lookup.py`: out-of-scope queries ("java agent") returned the Agent/Gateway topic by matching "agent" without any warning; added an explicit NOT COVERED warning for out-of-scope terms (java, go, grafana, SLO, eBPF, traceparent, etc.). Also added "tail-based/head-based" and "Kubernetes Operator" to the "NOT IN THE SOURCE" list.
4. Wording in `references/fronteira-e-datado.md` ("2 of useful content per page") corrected.

## 4. Limitations and pending items
- The sources are short, introductory, and sponsored (LogicMonitor, InfluxData); the package does not replace the official OpenTelemetry documentation. Specification status and versions = [DATED] (2021) and **were not verified** against current sources (no network access by method rule).
- `collector_pipeline_check.py` is a static reference check on simple YAML (minimal parser; does not support anchors, multi-document, multiline strings); it does not validate Collector semantics.
- The diagrams were described by visually reading renders at 80 to 200 dpi; the small labels of the OTW p.3 figure ("Prom. Expo", "Logfmt", "Jaeger Thrift") were read with magnification, but any ambiguity should be checked against the PDF.
- Cases executed by the author, not by an independent blind model.
