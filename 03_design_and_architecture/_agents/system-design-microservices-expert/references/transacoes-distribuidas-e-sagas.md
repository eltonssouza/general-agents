# Distributed transactions, Sagas, Outbox, and the Starbucks lesson

Sources: SBC (Hohpe; blog page of 11/19/2004, 4 printed pages from the site — it is NOT Helland's article "Life Beyond Distributed Transactions", which is not in the corpus), SOA, SAP, MS-MIC, MS-CLD, EDS, JMG. Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Starbucks Does Not Use Two-Phase Commit (SBC)

- Context: Hohpe returns from two weeks in Japan, sees the number of Starbucks in Shinjuku and Roppongi, and starts observing how they process orders. Starbucks maximizes order throughput, so it uses asynchronous processing. [from source] (SBC p.1)
- The queue is, literally, a line of cups on top of the espresso machine; it decouples cashier and barista and allows several baristas in a Competing Consumer scenario. [from source] (SBC p.1)
- Correlation: orders do not come out in order (different equipment, blended drinks take longer, baristas make several drinks in a batch); Starbucks solves this with a Correlation Identifier: in the US, the name written on the cup; in other countries, correlation by drink type. [from source] (SBC p.1) (SBC p.2) The times "10 seconds" and "2 minutes" from the previous package are not in the text and were removed.
- Exceptions, three strategies (Hohpe pairs them with real situations: not paying -> discard the drink/remove the cup from the queue; wrong drink -> remake; machine breaks -> refund): [from source] (SBC p.2)
  - Write-off: the simplest, do nothing or discard; acceptable if the loss is smaller than the cost of building a correction. The author's example: ISPs with errors in the billing/provisioning cycle, which ran reconciliation reports to find "free" accounts. [from source] (SBC p.2)
  - Retry: makes sense if there is a realistic chance of success (external unavailability yes, business rule violation no); with an Idempotent Receiver all operations can be resent, since the receivers that succeeded ignore duplicates. [from source] (SBC p.2)
  - Compensating Action: undo completed operations; works well in monetary systems, where the amount can be re-credited. [from source] (SBC p.3)
- 2PC at Starbucks would mean waiting at the cashier with the receipt and money on the counter until the drink was ready, to then exchange everything at once; no one could leave until the "transaction" finished, which would "kill the business". Lesson: 2PC can simplify life, but hurts the free flow of messages (and scalability) by keeping transactional resources stateful across asynchronous actions. [from source] (SBC p.3)
- Conversation: short synchronous interaction (order and pay) + long asynchronous one (prepare and receive); as at Amazon: order number synchronous, the rest (billing, packing, shipping) asynchronous, with compensation (refund) or retry. [from source] (SBC p.3)
- The article does not mention Saga, Outbox, Kafka, or microservices; those links are a reasonable [inference] (compensation ≈ Saga).

## 2. Transactions in service-based architectures

- SOA: propagating ACID transactional context across remote services is "extremely difficult"; BASE is used (basic availability, soft state, eventual consistency); example of an ATM deposit taking minutes/hours. If transactional consistency is indispensable, make the service coarser to use local ACID; or use events to notify consumers when the state has become consistent (with a lot of complexity). [from source] (SOA p.18) (SOA p.19)
- In microservices the transaction problems are smaller than in SOA, since generally a business request uses one service. [from source] (SOA p.18)
- SAP: EDA has no atomic transaction for a business process; if a unit of work must be split among processors, the pattern probably does not fit. In microservices, keeping a transactional unit across services would require a "transaction compensation framework". [from source] (SAP p.25) (SAP p.40)
- MS-MIC: private data per service prevents a single ACID transaction; eventual consistency is needed; referential integrity and distributed transactions across separate databases do not exist; the book states that ACID/2PC-style transactions run against the principles of microservices and that most NoSQL databases (Cosmos DB, MongoDB) do not support two-phase commit. [from source] (MS-MIC p.44) (MS-MIC p.49)
- MS-MIC on distributed transaction between database and broker (e.g., DTC with MSMQ): not recommended, because of CAP; in MS-MIC transactional MSMQ is a "legacy approach". [from source] (MS-MIC p.73) (MS-MIC p.158)
- JMG: the monolithic approach is the all-or-nothing transaction; the options are a distributed transaction with 2PC ("with all the complexity and scalability problems") or sagas. [from source] (JMG p.63)
- EDS: Kafka's transactions (exactly once) only cover what passes through Kafka and are not a rollback across services; "if you need multi-service transactions, consider implementing sagas". [from source] (EDS p.134)

## 3. Saga

- Definition (MS-CLD): a group of local transactions invoked sequentially; if one fails, the Saga aborts and invokes compensating transactions that undo the changes of the previous ones, restoring consistency. Example from the book: failure in Update Inventory triggers compensations that adjust the stock and cancel payment and order. [from source] (MS-CLD p.102) (MS-CLD p.103)
- Choreographed as a series of related events, or orchestrated as a set of related commands; MS-CLD's service aggregator would be the basis of an orchestrated Saga, and the topics (Service Bus/Event Grid) the basis of a choreographed one. [from source] (MS-CLD p.103)
- JMG (citing microservices.io): each local transaction updates the database and publishes a message/event that triggers the next one; if one fails due to a business rule, compensations are executed. Frameworks: Axon and Eventuate Tram Saga; "the chances of ending up DIY are high". Example: car reservation with Inventory, Reservation, and Payment. [from source] (JMG p.63)
- Orchestration vs. choreography: SOA defines orchestration (central mediator) and choreography (chained calls without a mediator); EDS discusses the trade-offs: orchestration writes the whole workflow in one place (easy to reason about, but coupled to the controller); choreography is pluggable and suits larger implementations. [from source] (SOA p.34) (SOA p.35) (EDS p.55)
- MS-MIC cites Sagas only as a feature of service buses (NServiceBus, MassTransit, Brighter) for long-running processes. [from source] (MS-MIC p.149)
- "Pivot transaction", "compensable/retriable", and "guideline: choreography for 2-4 steps, orchestration above 4" from the previous package are NOT in any source. [extrapolation] The compensable/pivot/retriable classification is from Chris Richardson's repertoire (book *Microservices Patterns*), outside the corpus; the "4 steps" threshold is a heuristic with no backing and was removed. Permitted use, labeled: see `scripts/audit_saga.py`.
- [inference] Combining SBC and MS-CLD: before the point at which the business considers the work irreversible, each step needs a compensation; after it, the sources suggest retry with an idempotent receiver (SBC p.2) instead of compensation.

## 4. Atomicity between database and event publication (Outbox)

- Problem: updating the state in the originating service and publishing the integration event atomically; if the service crashes after `SaveChanges` and before publishing, the system is left inconsistent. [from source] (MS-MIC p.158) EDS describes the same risk: duplicates if the notification goes out and the database does not persist, or absence of notification. [from source] (EDS p.75)
- MS-MIC options: transactional queue (DTC/MSMQ, legacy), transaction log mining, full Event Sourcing, and Outbox (transactional table as a queue). [from source] (MS-MIC p.73) (MS-MIC p.158)
- Log mining: couples the service to the DBMS log and low-level records may not correspond to the integration events. [from source] (MS-MIC p.159)
- Outbox as MS-MIC describes it: `IntegrationEvent` table in the same database as the entities; (1) start a local transaction, (2) change the entities and insert the event, (3) commit; then publish in one of two ways: publish right after the commit and mark the event as published in another local transaction, or use the table as a queue, with a worker that reads, publishes, and marks it as published; a checker worker can republish events "ready to publish". Example states: "ready to publish" -> "published". [from source] (MS-MIC p.159) (MS-MIC p.160)
- Sample implementation in .NET: `ResilientTransaction` with `CreateExecutionStrategy` to make the catalog's `SaveChanges` and the integration event log atomic across two DbContexts. [from source] (MS-MIC p.311) (MS-MIC p.312) (MS-MIC p.313)
- Full Event Sourcing is "one of the best approaches, if not the best", but requires restructuring the system. [from source] (MS-MIC p.158) (MS-MIC p.159)
- CDC: Change Data Capture connectors translate the database's write-ahead log into events; they are more efficient and more accurate than polling through the database API (which can miss operations within the query period). Databases with CDC in Kafka Connect: MySQL, Postgres, MongoDB, Cassandra; proprietary ones for Oracle, IBM, SQL Server. [from source] (EDS p.82)
- Debezium and "Message Relay" are tool/pattern names outside the corpus. [extrapolation] The consumer must be idempotent because publication may repeat (see `mensageria-e-event-driven-architecture.md`, section 5).

## 5. Out of scope

TCC, 3PC, isolation between sagas and anomalies, SagaLog/persistent orchestrator state, XA in detail (EDS p.117 and p.133 only cite XA as slow and avoided), Helland "Life Beyond Distributed Transactions" (Entities/Activities/Messages): NOT in the corpus.
