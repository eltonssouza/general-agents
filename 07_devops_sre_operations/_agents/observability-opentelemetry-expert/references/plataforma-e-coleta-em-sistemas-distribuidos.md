# Platform and collection in distributed systems [DOW p.5-6]

## Platform considerations checklist (table, DOW p.5)
[from source] Ten questions: high availability (24/7?); scalability without losing data (cloud? on-premise?); auto discovery (discover endpoints via Kubernetes or Consul); security (policies, encryption, access to sensitive data, auditability); distributed storage (availability and retention); cost management; compliance; documentation; usability (API for automation, e.g. scripts, Ansible); integration (Slack, VictorOps, OpsGenie, PagerDuty, email); compatibility (flexible and modular for the next three years). The text's conclusion: no single team designs the platform; everyone looks after compliance and integration and ease of use for operations, development, SRE and security (DOW p.5).

## How to monitor (DOW p.5-6)
- [from source] Start by automating the collection of **metrics**; they show the first areas to address, from resource allocation to cloud cost (DOW p.5). First physical data (CPU, memory, disk, network); then system data (processes, states, versions, consumption); measuring resource usage per component helps profile the system's behavior (DOW p.5).
- [from source] Simple method: (1) an **agent on each system**; the agent itself must be monitored and must not consume so much that it affects the main workload; (2) **centralize** the data in a remote platform (e.g. a time-series database) with graphical visualization and alert generation (DOW p.6).

## How to log (DOW p.6)
- [from source] Define a **global log management policy**: format and flow, verbosity according to the environment, transformations to identify events quickly (DOW p.6).
- [from source] **Tag** management is crucial to correlate metric and event; the system writes in a defined format and location; a **collector** (possibly different from the metrics one) reads, transforms and centralizes on an external platform, where there may be compression and archiving (DOW p.6). Some new-generation collectors extract metrics from events; doing so before identifying the need reduces iterations and resources (DOW p.6).

## How to trace (DOW p.6)
- [from source] It starts with **instrumenting** the environment to collect and correlate data; then dependencies between services, performance and abnormal events (errors, latency) become visible (DOW p.6). Two levels of instrumentation: adding code to the application (via an APM tool, end to end from the front end to the database) or adopting a **service mesh** (proxies between endpoints track requests and collect traces) (DOW p.6).
- [from source] To make the trace identifiable, a **unique identifier is assigned to each step** of the query, allowing the steps to be correlated in the right order (DOW p.6).
- [inference] The text speaks of an identifier per step and does not name trace id/span id or the propagation header; the trace id/span id vocabulary appears only in the OTW p.5. [extrapolation] The standardized header format is W3C Trace Context, which the DOW only lists as further reading (DOW p.7).
