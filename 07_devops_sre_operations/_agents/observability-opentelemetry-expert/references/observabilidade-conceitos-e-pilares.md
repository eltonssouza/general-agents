# Observability: concepts, pillars, graphs and alerts [DOW]

## Distributed system and its costs
- [from source] Five architectural characteristics for agility: availability (fault tolerance), scalability, deployability, testability, maintainability (DOW p.1). Distributed system = many components on several servers that coordinate to appear as a coherent system to the end user (DOW p.1). Examples cited: Kubernetes, Apache Spark, Kafka (DOW p.1).
- [from source] Four business goals: competitiveness, agility, velocity, time-to-market; competitiveness is measured by product availability (DOW p.1, 3). See Figure 1 in `diagramas-e-figuras.md`.
- [from source] Disadvantages: management complexity at several levels (automation, installation, upgrade); components with different lifecycles and tools; **diagnosis** is usually the most complicated phase; cost of people and time; computing resources can grow exponentially with usage (DOW p.3). Hence the need for a reliable observability platform (DOW p.3).

## Monitoring vs observability
- [from source] Monitoring: obtains the system state from **predefined measurements** to detect a **known set of problems** (DOW p.3).
- [from source] Observability: measures the **understanding of the system state from several outputs**; it is a capability, like reliability, scalability and security, which must be **designed and implemented from the initial build, coding and testing** (DOW p.3). It is everyone's responsibility, like DevSecOps (DOW p.3).
- [from source] Monitoring indicates **when** something is wrong; observability indicates **why**; monitoring is a subset and a key action to make observability proactive instead of reactive (DOW p.3).
- [from source] Legacy systems that only aggregate measurements do not give the visibility to find and fix anomalies quickly (DOW p.3).

## The three data types (DOW p.4)
- **Metrics** [from source]: numeric measurements of system state; with tags they are groupable, searchable and plottable; good for storing, compressing and querying historical trends. Entry point of monitoring (CPU, memory, disk, network). Anyone can create one (e.g. treatments processed, time, status). They serve developers, operators and executives (DOW p.4).
- **Logs** [from source]: immutable timestamped records of events. Three formats: plain text (the most common, unstructured), structured (more recent, e.g. JSON) and binary (e.g. MySQL binlog, system journal, Avro) (DOW p.4). They give a more granular view and help with debugging and optimization; careful management is essential in interconnected failures (DOW p.4).
- **Traces** [from source]: graphical representation of event logs; distributed tracing follows a service request from service to service, representing the request's lifecycle (DOW p.4). Uses cited: developers optimize the least performant calls; SREs identify possible security breaches; DBAs detect long queries (DOW p.4). They make it possible to measure overall health, find bottlenecks and prioritize optimizations (DOW p.4).
- [from source] The three have their own purposes and work together to understand performance and behavior (DOW p.4).

## Graphs and alerts
- [from source] The goal is adoption by the whole organization; collecting without representing/interpreting makes the solution lose value (DOW p.4). **Graphs**: a global view over time of performance, state and reliability, from operators to usage by users (DOW p.4). **Alerts**: representation over time allows identifying deviant behavior and configuring alerts that notify operators and developers, enabling proactive action (DOW p.4).
- [from source] Building the platform requires a certain level of team maturity in collection and interpretation (DOW p.5).

## Internal tension (label it when answering)
- [from source] The text speaks of **three pillars**: logs, metrics and traces (DOW p.3), and then of **five pillars**: three for collection + two for interpretation (DOW p.5). Figure 2 names the three collection ones as Monitoring, Logging and Tracing (not "metrics") and the two interpretation ones as Alerting and Graphing (DOW p.5, figure). [inference] When answering, say which framing you are using; "monitoring" in the figure takes the place of the text's "metrics".
- [inference] The text says monitoring is a "subset" of observability (p.3) and Figure 2 places it as one of the collection pillars under "Profiling"; there is no strong contradiction, but the terminology is loose.
