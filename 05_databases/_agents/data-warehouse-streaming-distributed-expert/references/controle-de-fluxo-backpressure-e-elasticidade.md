# Load Management: Load Shedding, Backpressure and Elasticity

> Convention: `(STREAM p.N)` = PDF page = printed page. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Overview
[from source] Stream processors do not control the input rate (push). When the input exceeds capacity: *load shedding* temporarily drops tuples, trading accuracy for sustainable performance, suitable for strict-latency applications that tolerate approximate results; when correctness matters more, dropping is not an option: the excess can be buffered and processed later (back-pressure); elasticity adjusts the configuration and resources, ensuring correctness under varying load, and avoids idle resources when the load falls (STREAM p.21-22).

## 2. Load shedding
[from source] A component (the load shedder) monitors rates and metrics and decides when, where, how many and which tuples to drop; many systems limit shedding to operators that do not modify tuples (filter, union, join) or to windows/SUM/COUNT; an alternative is to treat it as a feedback control problem; *drop operators* are usually placed near the sources; there is a precomputed *load shedding road map* (LSRM); strategies for which tuples to drop: random (sampling), by whole window, semantic (concept drift) (STREAM p.22).

## 3. Scheduling and flow control
[from source] When bursts are transient and more latency is preferred over lost results, back-pressure and flow control do not sacrifice accuracy: buffering, load-aware scheduling (prioritizes operators to minimize backlog), rate regulation and *throttling* of the producer. They require buffer space and an accumulated load within capacity. Load-aware scheduling uses the selectivity and cost of operators (STREAM p.22).
- [from source] The 1st generation **also** had scheduling and flow control, so load shedding was not "the only alternative" (v1 claimed this); Section 6.4 says shedding was popular and that modern systems no longer favor degrading the quality of the result (STREAM p.25-26).

## 4. Back-pressure
- [from source] In a network of producers and consumers, all operators slow down to the speed of the slowest consumer; the pressure propagates upstream to the sources; to avoid losing data, a persistent input queue (e.g. Apache Kafka) and adequate storage are required (STREAM p.23).
- [from source] *Buffer-based*: implicit control through buffer availability (shared local pool; TCP between machines, with a limit on data in flight) (STREAM p.23-24, Fig. 7).
- [from source] *Credit-based flow control* (CFC, Kung et al.; an ATM switch technique), implemented in Apache Flink: each task tells the senders its buffer availability through credit messages; when the credit reaches zero (or a threshold), back-pressure appears on the virtual channel; advantage: it affects only pairs of tasks, not other channels on the same TCP connection (important with skew); disadvantage: credit messages can increase end-to-end latency (STREAM p.23, Fig. 8).
- [extrapolation] "Reactive Streams" and the idea that Kafka "retains without losing a single byte" are the agent's extensions; the survey only says that a persistent queue is necessary.

## 5. Elasticity
- [from source] An elastic system needs a **policy** (an algorithm that decides when/how much to scale from metrics) and a **mechanism** (allocates resources, reassigns work, migrates state, ensuring correctness) (STREAM p.23). Heuristic policy (rules and thresholds on CPU, throughput, queues, memory; CPU/memory can mislead in multi-tenant environments; Dhalion and IBM Streams use congestion/back-pressure signals to find bottlenecks but do not detect overprovisioning) and predictive policy (analytical models: queueing theory, control, linear models such as DS2) (STREAM p.23-24). Commercial auto-scaling: Google Cloud Dataflow, Heron, IBM System S (STREAM p.23).
- [from source] State redistribution preserves the semantics of hash-based keys. Uniform hashing is simple but can have a high migration cost; consistent hashing is preferred; Flink uses a variation with **key groups** mapped to tasks in ranges; the number of key groups limits the maximum parallelism of keyed state; hashing does poorly with skew; *hybrid partitioning* combines consistent hashing and explicit mapping (STREAM p.24).
- [from source] Reconfiguration strategies: **stop-and-restart** (stop, take a snapshot, restart; simple and always correct, but stalls the whole pipeline; the survey says it is **very common in modern systems**), **partial pause and restart** (FLUX; blocks only the affected subgraph), **pro-active replication** (state copies for near-"live" reconfiguration, ChronoStream). State transfer: all-at-once or progressive (Megaphone), the latter smooths latency spikes but lengthens the migration (STREAM p.25).
- [inference] v1 said that elasticity migrates RocksDB state "without restarting the pipeline, in a few seconds". This contradicts p.25 (stop-and-restart is common) and has no number in the survey; it was removed.

## 6. First vs second generation
[from source] Load shedding was popular in the 1st generation; queries formed a shared plan, so load management affected several queries; today queries are independent jobs, and back-pressure in one does not affect the others in the cluster; "scale down" is a recent requirement; the dependence on persistent queues is a recent characteristic; modern techniques are general, applicable even with variable or unknown cost and selectivity (STREAM p.25-26). Open problems: adaptive scheduling on arbitrary plans, UDFs, general windows; general reconfiguration (STREAM p.26).

## Terms from the original (checked by tests/audit_tokens.py)
- `shedding`, `throttling`, `LSRM` (STREAM p.22)
- `credit`, `ATM`, `Flink`, `Kafka` (STREAM p.23)
- `key`, `groups`, `consistent`, `Dhalion` (STREAM p.24)
- `stop-and-restart`, `FLUX`, `ChronoStream`, `Megaphone` (STREAM p.25)
