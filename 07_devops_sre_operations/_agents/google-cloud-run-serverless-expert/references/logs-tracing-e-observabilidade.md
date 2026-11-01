# Structured logs, tracing and metrics (RUN ch. 9, p.157-173)

For general observability and OpenTelemetry, refer to `observability-opentelemetry-expert`. The book here uses OpenCensus (2020) `[DATED]`.

## What Cloud Run captures
- **[from source]** Container stdout/stderr streams, files in `/var/log` (and subdirectories), syslog; in addition it forwards a **request log** (path, status, latency) (RUN p.157-158). The author recommends the **output streams** because they are portable (RUN p.158).
- **[from source]** View: Logs tab in the console; full Cloud Logging; in the terminal, `gcloud logging read "resource.type=cloud_run_revision" --limit 1` (the output carries `labels` such as `service_name` and `revision_name`) (RUN p.158-159). In Sept/2020 the Cloud Run CLI had no log *tail* (RUN p.158) **[DATED]**.
- **[from source]** "Invisible logs": PHP app writing to application files; several processes in the container without aggregation of the streams (in that case write to `/var/log`); there is no need to resend NGINX access logs, since a request log already exists (RUN p.159).
- **[from source]** Operations Suite: Cloud Logging, Cloud Monitoring (metrics and alerts), Error Reporting (tracks stack traces), Cloud Trace (latency) (RUN p.159).

## Structured logs
- **[from source]** Plain text arrives line by line with default severity; Cloud Run only collapses common types of multi-line logs (stack traces) into one event (RUN p.160). Logging in **JSON** with a `severity` field adds level and searchable attributes (example with `zerolog`, Go) (RUN p.160-162).
- **[from source]** Cloud Logging client libraries send directly to the API (bypassing the output streams) and hurt portability; prefer JSON on stdout (RUN p.162). The product used to be called Stackdriver (useful when searching for plugins) (RUN p.162).
- **[from source]** Levels (Table 9-1): DEBUG (local only), INFO, WARNING, ERROR (goal: zero errors in the logs; do not log an error in the normal flow), CRITICAL (`Fatal()` terminates the container and the user sees 503), ALERT (`Panic()` when someone must act now) (RUN p.162-163).
- **[from source]** Panics: the text stack trace becomes an event with default severity and Error Reporting detects it without configuration (other languages too) (RUN p.163). Do not record personal or sensitive data (RUN p.163, 173).
- **[from source]** In development use `zerolog.ConsoleWriter` for readable logs (RUN p.165).

## Request and trace context
- **[from source]** The GFE adds the **`X-Cloud-Trace-Context`** header; putting the trace ID in the logs (attribute `logging.googleapis.com/trace`) groups all the logs of a request, essential with many concurrent requests (example: 1,000 simultaneous requests, logs of three requests in the same millisecond) (RUN p.165-166). The `crzerolog` package (Yuki Furuyama) also adds the code location (RUN p.165-166).
- **[from source]** Propagate across services: capture the trace ID, and forward it in outgoing calls; the GFE preserves the ID if the header already exists (RUN p.167-168). Three steps in Go: logger with trace ID; trace ID in the incoming request context (OpenCensus `ochttp.Handler` with Stackdriver propagation); pass the context (`WithContext`) to the `idtoken` client in the outgoing call (RUN p.168-169). In the console: "Show all logs for this trace" (RUN p.171). Full distributed tracing (own spans, sampling, Cloud Trace) is only scratched (RUN p.171).
- **[from source]** Cloud Run system metrics in Cloud Monitoring: CPU and memory (utilization and allocation), latency and request count; **log-based metrics** created in the "Logs-based metrics" tab of Cloud Logging allow charts and alerts on log attributes (RUN p.171-172).
- **[from source]** Summary of the gain: level, business metadata (no personal data), code location, request context, trace context (RUN p.173).

## Rules
1. **[from source]** JSON on stdout with `severity`; no secrets or PII (RUN p.160-163, 173).
2. **[from source]** Propagate the trace ID across services to correlate logs (RUN p.167-169).
3. **[inference]** "My logs don't show up": check whether they go to stdout/stderr or `/var/log` (RUN p.157-159).
4. **[extrapolation] [DATED]** SLOs, burn-rate alerts, modern Cloud Trace/OpenTelemetry, `Cloud Monitoring` uptime checks: **NOT COVERED**.
