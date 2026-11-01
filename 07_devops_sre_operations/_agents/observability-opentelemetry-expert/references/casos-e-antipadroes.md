# Cases and anti-patterns

## Supported by the sources
| Anti-pattern | Why | Source |
| --- | --- | --- |
| Treating monitoring as a synonym for observability | monitoring = predefined measurements for known problems; observability = understanding the state from several outputs, designed from the start | DOW p.3 |
| Leaving observability for "after deploy" | it is a capability to design and implement from the build onward | DOW p.3 |
| Collecting data without graphs/alerts/interpretation | the solution loses value for most of the organization | DOW p.4 |
| Collection agent without monitoring and without a consumption limit | can affect the main workload | DOW p.6 |
| Logs without a policy (format, verbosity, tags) | hinders metric-event correlation | DOW p.6 |
| Platform designed by a single team | everyone has requirements (compliance, integration, usability) | DOW p.5 |
| Instrumenting everything manually when an automatic package exists | a lot of repetitive code; but you lose control, so choose consciously | OTW p.6 |
| Changing the order of processors without thinking | processors run in the configured sequence | OTW p.3 |
| Coupling the application to a vendor's exporters | lock-in and switching cost; standardize via OTLP/Collector | OTW p.1, 3, 7 |
| Refactoring the whole legacy codebase just to adopt OTel | may not be worth it and brings risk; use a converter | OTW p.6 |
| Exporting 100% of traces without thinking about cost | the SDK allows sampling for performance or cost | OTW p.4 |

## Common claims the sources do NOT support (correct before answering)
| Claim | Status |
| --- | --- |
| "The sources define SLOs/error budgets/golden signals" | they do not appear; [extrapolation] |
| "The OTW explains the traceparent / baggage header" | no; it only describes context injection/extraction in headers (OTW p.5) |
| "The OTW recommends tail-based sampling" | no; it only says the SDK can sample (OTW p.4) |
| "The Collector Gateway is the recommended option" | false: the **Agent** is the recommended one (OTW p.3) |
| "OTel logs were stable in 2021" | false: draft; only Tracing was stable (OTW p.4) |
| "The three pillars are metrics, logs and traces and nothing else" | the DOW also describes five pillars (DOW p.5) |
| "The DOW recommends Prometheus/Jaeger" | it names neither Prometheus nor Jaeger; the backends are listed by the OTW (p.7) |
| "The OTW covers instrumentation in Java/Go/Node" | only Python/Flask (OTW p.5-6) |
| "The DOW explains the W3C Trace Context format" | it only lists it as further reading (DOW p.7) |
| "Observability is only SRE work" | the text says it is everyone's responsibility (DOW p.3) |

## Worked practical cases
1. **Team has Prometheus and wants traces**: traces with spans/parent (OTW p.4), Jaeger or Zipkin as backends (OTW p.7), Collector to route by signal (OTW p.3); Prometheus remains for metrics (OTW p.7). Integration details = [extrapolation].
2. **Flask application without instrumentation**: `FlaskInstrumentor` (OTW p.6); context propagated through headers (OTW p.5).
3. **Many services with different agents per backend** ("before" figure, OTW p.3): consolidate into a Collector with OTLP (OTW p.3).
4. **"How do I know where the request got slow?"**: trace, spans with duration and parent (OTW p.4), SpanKind helps to see latency (OTW p.5).
