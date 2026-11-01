# Distributed systems fundamentals and metrics

Convention: `(SIGLA p.N)` = PDF page (see `INDEX.md`, page map). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.
This reference is deliberately short in the "from source" passages: the corpus provides definitions and lists, not mathematical derivations.

## 1. Scalability

- Definition: scalability is the property of a system to handle growing load by adding resources. [from source] (SDH p.6)
- Vertical (more CPU/RAM/disk on one machine): simpler, but with a physical limit and a single point of failure. Horizontal (more servers/nodes): allows "nearly unlimited" scale, at the cost of the complexity of managing a distributed system. [from source] (SDH p.28)
- In the cloud context, MS-CLD recommends prioritizing scale-out over scale-up and designing stateless services so that any instance serves any request. [from source] (MS-CLD p.130-131)
- Sticky sessions/node affinity should be avoided; if there is state, keep it in a distributed cache. [from source] (MS-CLD p.131)
- MS-CLD gives operational autoscaling guidance: scale out aggressively and scale in conservatively, with a cool-down example of 5 min (adding) and up to 15 min (removing). [from source] (MS-CLD p.131) This is an example from the book for Azure, not a universal constant.
- Stateful vs. stateless: SDH defines state kept between requests vs. each request self-contained. [from source] (SDH p.30)

## 2. Availability

- Definition: Availability = Uptime / (Uptime + Downtime). [from source] (SDH p.7)
- "Nines" table (it is in an image on the page): 99% = 3.65 days/year; 99.9% = 8.76 h; 99.99% = 52.56 min; 99.999% = 5.26 min; 99.9999% = 31.5 s. [from source] (SDH p.7)
- Composition of dependencies: MS-MIC states that 50 dependencies with 99.99% availability each result in several hours of unavailability per month, through a domino effect (amplified partial failure). [from source] (MS-MIC p.308)
- Formulas: in series, A = A1 x A2 x ... x An; in independent parallel, A = 1 - (1-A1)...(1-An). [extrapolation] (reliability math; the book only gives the qualitative example above). Example: 3 services of 99.9% in series = 99.7003% (about 26.2 h/year, versus 8.76 h from SDH p.7); 2 independent instances of 99% in parallel = 99.99%. The independence assumption rarely holds (correlated failures). [extrapolation]
- Redundancy requires deciding on cost and complexity: MS-CLD discusses multiple instances, load balancer, multi-region, and geo-replication, and says that the level of redundancy depends on business requirements. [from source] (MS-CLD p.128-129)
- MTBF/MTTR do not appear in the corpus. [extrapolation] A = MTBF/(MTBF+MTTR) is the classic form of the same SDH formula.

## 3. Latency and throughput

- Latency: time for an operation to complete; throughput: work done per period, typically RPS or TPS. [from source] (SDH p.8)
- Cost of summed remote calls: in the SOA example, 4 services with 100 ms of transport per call generate 600 ms of transport alone; consolidating into 1 service would reduce it to 200 ms. [from source] (SOA p.28)
- In chains of synchronous calls the latency is the sum of the steps. [from source] (MS-CLD p.79)
- Timeouts: there is no "magic number"; the service SLA is the source for choosing. [from source] (JMG p.59) SOA shows the benchmark + margin reasoning (example: 2,000 ms doubled to 4,000 ms) and its problems, and recommends per-context, externally configurable timeouts, not global ones. [from source] (SOA p.16-17)
- Little's Law (L = λ·W): NOT in the corpus. [extrapolation] (queueing theory, steady state). Example: 5,000 req/s x 0.2 s = 1,000 in-flight requests on average; useful for sizing thread/connection pools.
- Tail latency amplification: NOT in the corpus. [extrapolation] If each call has a 1% chance of being slow and the request depends on N independent calls, P(at least one slow) = 1 - 0.99^N: N=10 gives 9.56%; N=50 gives 39.50%; N=100 gives 63.40%. The book only states, qualitatively, that more synchronous dependencies between microservices worsen response time. [from source] (MS-MIC p.65)

## 4. CAP and consistency

- CAP: it is impossible for a distributed data store to simultaneously guarantee Consistency (every read sees the most recent write or an error), Availability (every request receives a non-error response, with no guarantee that it is the most recent), and Partition Tolerance. [from source] (SDH p.9)
- MS-CLD describes the same three terms, says that a database only guarantees two of the three and that, without a partition, there are also trade-offs between consistency and performance; it mentions that CAP is usually extended to PACELC, without detailing the four classes. [from source] (MS-CLD p.107)
- The four classes PC/EC, PA/EL, PC/EL, PA/EC and the classification of specific databases (Spanner, Cassandra, MongoDB...) are NOT in the corpus. [extrapolation] The classification depends on configuration (consistency levels, quorum) and must be checked in the product documentation.
- "P is mandatory in real networks" is the usual reading of the theorem, not a sentence from the corpus. [extrapolation]
- Strong vs. eventual consistency: strong = every read after a confirmed write reflects the write; eventual = convergence with no guarantee of when. [from source] (SDH p.29)
- In microservices: private data per service implies there is no single ACID transaction across services; the book opts for availability and eventual consistency in most scenarios. [from source] (MS-MIC p.44) (MS-MIC p.49)
- The term "consistency" is overloaded (CAP vs. ACID vs. consistency models). [from source] (EDS p.116)
- In event-driven systems, eventual consistency brings two consequences: lack of timeliness (one consumer lags behind another) and collisions (concurrent changes to the same entity). [from source] (EDS p.118-120)

## 5. Out of the corpus scope

The FLP theorem and consensus in depth (SDH only lists Paxos and Raft, SDH p.20), logical clocks, quorums, SLO/SLI/error budget (see the SRE package), capacity calculation beyond the question playbook of SDH p.52.
