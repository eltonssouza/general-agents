# Procedures (playbooks) derived from the sources

Each step comes from the cited pages; order and grouping are the agent's [inference], unless stated otherwise.

## P1. Start observing a distributed system (DOW p.5-6)
1. Go through the ten-item considerations checklist with the teams (DOW p.5) and record the answers; nobody decides alone (DOW p.5).
2. Start with **metrics**: physical (CPU, memory, disk, network), then system (processes, states, versions) (DOW p.5).
3. Deploy one agent per system; monitor the agent and limit its consumption (DOW p.6). Centralize in a time-series database with graphs and alerts (DOW p.6).
4. Define the log policy (format, verbosity per environment, transformations) and tag management (DOW p.6).
5. Instrument for traces (code/APM or service mesh) with a unique identifier per step (DOW p.6).
6. Build graphs and alerts for broad adoption (DOW p.4).

## P2. Choose the signal for a question (inference supported by DOW p.4 and OTW p.4)
- "Is something wrong now? What is the trend?": metrics (DOW p.4; OTW p.4).
- "What happened at that instant, in detail?": logs (DOW p.4).
- "Where in the service chain did the request get slow/fail?": traces (DOW p.4; OTW p.4).
- When you need the "why": combine them; the text states the three act together (DOW p.4). Script: `signal_advisor.py`.

## P3. Assemble a minimal pipeline in the Collector (OTW p.3)
1. Define `receivers` (e.g. `otlp` with grpc/http), `processors` (e.g. `batch`), `exporters` (e.g. `otlp`) (OTW p.3).
2. In `service.pipelines`, create one pipeline per signal (`traces`, `metrics`, `logs`) linking receivers, processors and exporters; remember that the **order of processors matters** (OTW p.3).
3. Decide Agent (recommended, on the host) or Gateway (independent service) (OTW p.3).
4. Validate references with `collector_pipeline_check.py` (checks names defined vs used; does not validate the real Collector semantics).

## P4. Instrument an application with OpenTelemetry (OTW p.4-6)
1. Choose automatic (framework package) or manual; automatic saves code, manual gives control (OTW p.6).
2. Configure the Tracer Provider, span processor and exporter (console for testing) (OTW p.5).
3. In calls between services, ensure context propagation (injection/extraction in headers) (OTW p.5); in manual Flask, extract from the headers and use `kind=SERVER` (OTW p.6).
4. For legacy, consider a converter (Telegraf) instead of refactoring (OTW p.6).
5. Choose the backend per signal and switch by exporter configuration (OTW p.7).
[extrapolation] Current versions and APIs: check the current documentation.

## P5. Answer "should I migrate to OpenTelemetry?" (inference)
Arguments from the text: standardization and less instrumentation effort, no lock-in (OTW p.1, 7); legacy can stay as it is with a converter (OTW p.6). Caveats: the stability of Metrics/Logs was uncertain in 2021 [DATED] (OTW p.4); sponsored source (OTW p.1). Any real cost/benefit analysis is [extrapolation].
