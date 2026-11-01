# Fundamental architectural patterns (Mark Richards, SAP)

Main source: SAP, *Software Architecture Patterns* (O'Reilly, 2015). Pages = PDF (printed = PDF - 7). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.
SAP rates each pattern with a Low/High "rating" (there are no 1-5 stars) and summarizes everything in an arrow figure on p.53 (image), consistent with the text.

## 1. Layered architecture (n-tier)

- The most common pattern, the "de facto" one for most Java EE applications; it matches the organizational structure of companies. [from source] (SAP p.8)
- Components organized in horizontal layers; the pattern does not fix the number/types, but most have four: presentation, business, persistence, and database (sometimes business and persistence merge). [from source] (SAP p.8)
- Closed layer: the request must pass through the layer immediately below. Rationale: layers of isolation (a change in one layer does not affect the others, as long as the contracts are maintained). [from source] (SAP p.10)
- Example from the book: swapping JSP for JSF without affecting the business layer, if the contract (model) between presentation and business does not change. [from source] (SAP p.11)
- An open layer is possible when it makes sense; document which layers are open/closed and why, or the architecture becomes coupled and fragile. [from source] (SAP p.11) (SAP p.12)
- Anti-pattern "architecture sinkhole": requests cross layers as a simple pass-through, without logic. The 80-20 rule: it is typical to have ~20% pass-through requests and ~80% with logic; if the proportion is inverted, the book suggests considering opening some layers, aware that this makes it harder to control change. [from source] (SAP p.14) (SAP p.15)
- It tends toward monolithic applications, even when separating presentation and business into distinct units. [from source] (SAP p.15)
- Ratings: agility Low; deployment Low; testability High; performance Low; scalability Low; ease of development High (Conway: the company's communication structure). [from source] (SAP p.15) (SAP p.16)

## 2. Event-driven (EDA)

- An asynchronous distributed pattern, highly scalable and adaptable; composed of decoupled, single-purpose event processors. Two topologies: mediator and broker. [from source] (SAP p.18)
- Mediator: for multi-step events that require central orchestration. Four component types: event queues, event mediator, event channels, and event processors. The mediator knows the steps but does NOT execute the business logic. There are an initial event and processing events. [from source] (SAP p.18) (SAP p.19) (SAP p.20)
- Mediator implementation: from open-source integration hubs (Spring Integration, Apache Camel, Mule ESB) to BPEL/engine and BPM (jBPM) depending on sophistication; using a simple hub for very complex orchestration, or BPM for simple routing, is a "recipe for failure". [from source] (SAP p.20) (SAP p.21)
- Broker: no central mediator; the flow is distributed in a chain through a lightweight broker; processors publish a new event when they finish. Relay race analogy. [from source] (SAP p.21) (SAP p.22) (SAP p.24)
- There may be published events that no one consumes (future evolution/extension). [from source] (SAP p.22)
- Considerations: complex because it is asynchronous and distributed; lack of atomic transaction for a business process (splitting a unit of work among processors is a sign that EDA may not fit); event contract governance and a versioning policy from the start. [from source] (SAP p.24) (SAP p.25)
- Ratings: agility High; deployment High (broker easier than mediator); testability Low; performance High; scalability High; development Low. [from source] (SAP p.25) (SAP p.26)
- Strengths/weaknesses "high performance, no global view of failures, bottleneck in the mediator" cited in earlier versions of this package are not stated as such in SAP. SAP only says that the mediator couples more to the processor (SAP p.26) and that there is difficulty with testing and contracts. [inference] Difficulty tracing the end-to-end flow is a plausible consequence of the absence of a coordinator in the broker. [extrapolation]

## 3. Microkernel (plug-in)

- Natural for product applications; consists of a core system and independent plug-in modules. [from source] (SAP p.28)
- The core needs to know which plug-ins exist and how to access them, typically via a registry (name, data contract, access protocol). Plug-ins must be independent of each other. [from source] (SAP p.29)
- Contracts can be standard or custom; for third-party plug-ins an adapter is created; version contracts from the start. [from source] (SAP p.30)
- Classic example: the Eclipse IDE; another example in the book is a claims processing system with per-state rules as plug-ins. [from source] (SAP p.30) (SAP p.31)
- It can be embedded in another pattern; for product applications it "should be your first choice". [from source] (SAP p.31) (SAP p.32)
- Ratings: agility High; deployment High; testability High; performance High (customizable, e.g., trimmed-down JBoss); scalability Low; development Low (contract governance, registry). [from source] (SAP p.32) (SAP p.33)

## 4. Microservices (SAP's view)

- Separately deployed units; think in terms of service components, whose grain ranges from a module to a large part of the application; defining the right granularity is one of the biggest challenges. [from source] (SAP p.34) (SAP p.35)
- It is a distributed architecture: remote access via JMS, AMQP, REST, SOAP, RMI, etc. It evolved from layered monoliths and from SOA. [from source] (SAP p.35) (SAP p.36)
- Three topologies: REST-based API, REST-based application, and centralized messaging (lightweight broker, which is NOT "SOA-lite": it does not orchestrate, transform, or route in complex ways). [from source] (SAP p.36) (SAP p.37) (SAP p.38)
- Granularity and orchestration: components that are too fine lead to orchestration and a heavy SOA; needing to orchestrate from the UI/API or communicate between services for a single request suggests wrong granularity. [from source] (SAP p.39)
- ATTENTION (divergence from the "database-per-service" discourse): SAP admits resolving cross-service data needs via a shared database and copying common functionality between services (violating DRY) to maintain independence. MS-MIC and MS-CLD, on the other hand, advocate private data per service (see `microsservicos-vs-soa-e-monolitos.md`). [from source] (SAP p.40)
- A distributed transaction across service components is very hard and would require a "transaction compensation framework" that adds complexity; if the need for orchestration persists, the book says the pattern is probably not suitable. [from source] (SAP p.40) (SAP does not discuss 2PC by name.)
- Deployment: only the components that change are deployed; hot deploy possible. It shares with EDA the problems of contract, remote availability, and authentication. [from source] (SAP p.40) (SAP p.41)
- Ratings: agility High; deployment High; testability High; performance Low; scalability High; development High. [from source] (SAP p.41) (SAP p.42)

## 5. Space-based

- Motivation: with growing load the bottleneck migrates from the web server to the app server and to the database; the database is the final limiting factor. [from source] (SAP p.44)
- Designed for scalability and concurrency and for variable/unpredictable loads; also called "cloud architecture pattern"; the name comes from tuple space (distributed shared memory); it removes the central database bottleneck by using replicated in-memory data grids. Example: auction site. [from source] (SAP p.45)
- Two components: processing unit (application modules + in-memory data grid + optional asynchronous persistence + replication engine) and virtualized middleware. [from source] (SAP p.45) (SAP p.46)
- Virtualized middleware: messaging grid (receives the request/session and chooses a processing unit; from round-robin to "next-available"), data grid (keeps the data identical across the units; replication is described as asynchronous and very fast, sometimes in microseconds), processing grid (optional; mediates requests that involve several types of units), and deployment manager (starts/stops units according to load). [from source] (SAP p.46) (SAP p.47) (SAP p.48) (SAP p.49)
- Considerations: complex and expensive; good for smaller web apps with variable load (social networks, auctions); poorly suited for traditional relational applications with a lot of operational data; there is generally a datastore for initial load and asynchronous persistence; it does not require the cloud. Products cited: GemFire, JavaSpaces, GigaSpaces, Oracle Coherence, etc. [from source] (SAP p.49) (SAP p.50)
- Ratings: agility High; deployment High; testability Low; performance High; scalability High; development Low. [from source] (SAP p.50) (SAP p.51)
- "Write-behind cache" is a term from the previous package, not from SAP; the equivalent content is the optional asynchronous persistence above. [inference]

## 6. Comparison table (SAP text, arrows of Figure A-1)

| Pattern | Agility | Deploy | Testability | Performance | Scalability | Development |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Layers | Low | Low | High | Low | Low | High |
| Event-driven | High | High | Low | High | High | Low |
| Microkernel | High | High | High | High | Low | Low |
| Microservices | High | High | High | Low | High | High |
| Space-based | High | High | Low | High | High | Low |

Source: individual ratings on the pages cited above; visual summary in (SAP p.53). The book warns that the chart is not enough: you must analyze infrastructure, skills, budget, deadline, and application size, and that changing the architecture later is difficult and expensive. [from source] (SAP p.52) (SAP p.53)

## 7. Other styles cited in lists (without depth)

Client-server, serverless, EDA, and P2P: one-sentence definitions in (SDH p.45) (SDH p.47) (SDH p.48) (SDH p.49). Microservices in SDH: loosely coupled, independently deployable services, each with its own database, communicating through lightweight protocols. [from source] (SDH p.46)

## 8. Out of scope

Pipeline/filter, CQRS as a top-level style, hexagonal/clean (see the Clean Architecture package), service-based architecture from Richards' later book.
