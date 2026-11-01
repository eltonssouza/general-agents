# Microservices vs. SOA vs. monoliths

Sources: SOA (Mark Richards, O'Reilly 2016, sponsored by NGINX; the previous package attributed it to "NGINX"), MS-MIC, MS-CLD, MS-WEB, SAP, JMG, EDS. Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Monolith

- A monolith is self-contained in behavior; generally deployed as a single unit; to scale horizontally the entire application is duplicated. [from source] (MS-WEB p.26)
- MS-WEB is a guide on monolithic applications and says that, in the vast majority of situations, a single application is much easier to build, deploy, and debug than one composed of several services, while still meeting the business requirements. [from source] (MS-WEB p.3)
- Advantages cited by MS-CLD: easy to build, test, deploy, debug, and scale vertically; many successful apps started this way. The "cycle of fear" describes the degradation: nobody understands the whole, changes have side effects, large releases, one unstable component brings everything down. [from source] (MS-CLD p.11) (MS-CLD p.12)
- Scaling a monolith scales all the code to the same degree; changing one component requires retesting and redeploying everything, although initial development is easier. [from source] (MS-MIC p.35)
- In SAP the monolith is a natural tendency of the layered style. [from source] (SAP p.15)
- JMG: "nothing wrong with monoliths", but there are limits to how far they can be pushed. [from source] (JMG p.16)

## 2. SOA vs. microservices (Richards)

- Both are "service-based" and distributed; the price is complexity and cost (contracts, protocol, unavailable services, security, distributed transactions). [from source] (SOA p.11) (SOA p.12)
- Sharing: SOA is "share-as-much-as-possible" (shared enterprise services; the shared Order service accesses several databases); microservices are "share-as-little-as-possible", based on DDD's bounded context. The cost of SOA is tight coupling and change risk; for microservices the book even admits violating DRY. [from source] (SOA p.32) (SOA p.33) (SOA p.34)
- Taxonomy: microservices have only functional and infrastructure services; SOA defines four types (business, enterprise, application, infrastructure). [from source] (SOA p.22) (SOA p.23) (SOA p.24)
- Ownership: in microservices, application teams are the owners; in SOA there are different owners per type (business, shared-services teams, integration), and coordination takes much more time. [from source] (SOA p.25) (SOA p.26)
- Granularity: SOA can range from small application services to entire subsystems; services that are too fine cause remote chatter and loss of ACID. Numeric example: 4 services x 100 ms = 600 ms of transport alone; consolidating into 1 service = 200 ms. Recommendation: start with coarser services and break them up later (citing Sam Newman). [from source] (SOA p.27) (SOA p.28) (SOA p.29)
- Orchestration vs. choreography: orchestration = coordination by a central mediator; choreography = chained calls without a mediator. Microservices favor choreography (but minimized, to avoid efferent coupling); SOA uses both, with orchestration in the messaging middleware. Too much choreography worsens performance and robustness; one solution is to consolidate fine services into a coarser one. [from source] (SOA p.34) (SOA p.35) (SOA p.36) (SOA p.37) (SOA p.38)
- Middleware vs. API layer: microservices have no messaging middleware/ESB; at most a "non-intelligent" API layer that abstracts the location and granularity of services. SOA has middleware with mediation/routing, message enrichment and transformation, and protocol transformation. [from source] (SOA p.40) (SOA p.41) (SOA p.42) (SOA p.43)
- When each fits: SOA suits large, heterogeneous systems with many shared components (e.g., insurance companies), and is poor for small web systems or well-defined workflows with few shared components. Microservices suit smaller, well-partitioned systems; they can be a good initial choice and the business may later require SOA, or the reverse path (SOA to microservices, to simplify). [from source] (SOA p.46)
- Interoperability: microservices support "protocol-aware" interoperability; only SOA supports "protocol-agnostic" (via middleware). In a heterogeneous environment with distinct protocols, SOA is favored; if everything speaks the same protocol (e.g., REST), microservices will do. [from source] (SOA p.47) (SOA p.48) (SOA p.49)
- Contract decoupling (transforming message and protocol without changing consumers) is an SOA capability that microservices do not have. [from source] (SOA p.49) (SOA p.50) (SOA p.53)
- The table matrix ("Goal: integration vs agility", "Two-Pizza Teams", "daily deploys") from the previous package is NOT in SOA and was removed; "Two-Pizza" does not appear in any source in the corpus.

## 3. MS-MIC's and SAP's view of SOA

- SOA decomposes the application into services (generally HTTP) classified into types; microservices derive from SOA but differ; large central brokers, organizational orchestrators, and ESB are typical of SOA and, "in most cases", anti-patterns in the microservices community; quoted phrase: "microservices are SOA done right". [from source] (MS-MIC p.40)
- "Smart endpoints and dumb pipes": a slogan that encourages decoupling between services and cohesion within each one; end-to-end services are choreographed via REST and events, instead of WS-* and centralized orchestrators. [from source] (MS-MIC p.64)
- Messaging infrastructure: lightweight broker (RabbitMQ, Service Bus), with the "intelligence" in the endpoints, unlike the large brokers of SOA. [from source] (MS-MIC p.69) (MS-MIC p.70)
- SAP says that microservices evolved from layered monoliths and from SOA, the latter "complex, expensive, and generally overkill". [from source] (SAP p.36)

## 4. Data: split or shared?

- MS-MIC rule: each microservice owns its model and data; private data is only accessed via API (REST, gRPC, SOAP) or asynchronously via messaging; if several services used the same data, schema changes would require coordinated updates and would break autonomy. [from source] (MS-MIC p.42) (MS-MIC p.43) (MS-MIC p.44)
- No microservice should include another's tables in its transactions, nor in direct queries. [from source] (MS-MIC p.48)
- Benefits of a database per microservice (MS-CLD): encapsulated data, schema evolves without affecting others, independent scaling, failure of one store does not affect others; enables polyglot. [from source] (MS-CLD p.99)
- JMG: each microservice is the single source of truth for its data; avoid sharing; duplicating data requires keeping it in sync. [from source] (JMG p.18)
- EDS (Newman in the foreword): a database shared between services creates a huge coupling point and makes schema evolution harder. [from source] (EDS p.8)
- Divergence to note: SAP suggests a shared database and code duplication as pragmatic solutions (SAP p.40). When answering, state that the sources diverge and attribute each position.
- Duplicating data across several services is not a design error when translated into the context of each bounded context; one service must be the sole owner/authority of each dataset. [from source] (MS-MIC p.66) (MS-CLD p.101)
- SDH summarizes: each service with its own database for low coupling. [from source] (SDH p.46)

## 5. When to keep the monolith and when to decompose

- For microservices MS-MIC lists benefits (small services, independent deployment and scaling, division among teams, fault isolation) and drawbacks (distributed application, deployment complexity, atomic transactions infeasible, more global resources, problems in direct client-to-microservice communication). [from source] (MS-MIC p.112) (MS-MIC p.113)
- Service size is not the point: what matters is low coupling, internal cohesion, and independence. [from source] (MS-MIC p.41)
- MS-CLD on cloud-native candidates: strategic systems that constantly evolve, high release velocity, features released without a full redeploy, teams with different stacks, components that scale independently. Smaller, lower-impact apps may do fine with a monolith on PaaS; it is often worth "optimizing" the monolith for the cloud. [from source] (MS-CLD p.29) (MS-CLD p.31)
- Signs of a "distributed monolith" (JMG): every function as a potential remote call, "chattiness", dependency cycles, excessive code sharing. [from source] (JMG p.18) (JMG p.19)
- The rules of thumb "3 to 8 developers", "Kubernetes cost outweighs the gain", and "distributed systems tax" from the previous package are NOT in any source and were removed. [extrapolation] Team/organization criteria should be treated as the architect's judgment, anchored in the benefits/drawbacks above.
- Gradual modernization: MS-MIC mentions that an API Gateway between clients and the monolithic API allows new APIs to be added as microservices without changing URIs for the clients. [from source] (MS-MIC p.59) The name "Strangler Fig" does NOT appear in the corpus. [extrapolation] (Fowler's pattern, general knowledge)

## 6. Out of scope

Conway's Law beyond quotations (SAP p.16; JMG p.17), Team Topologies, real cost/TCO, legacy data migration, platform governance.
