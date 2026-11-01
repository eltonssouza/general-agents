# Event Sourcing and CQRS

Sources: EDS (ch. 7), MS-CLD (ch. 5), MS-MIC (ch. 6 and the integration events section). Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Event Sourcing

- Idea (EDS): events (state changes) are a central element; if stored immutably and in the order of creation, the log provides a complete audit and allows the current state to be re-derived by rewinding and replaying the log. [from source] (EDS p.70)
- Command Sourcing is the variant applied to events entering the service (it stores the input before any processing); Event Sourcing records the state changes produced. Both allow recovery from corruption/bugs by fixing the code and reprocessing. [from source] (EDS p.71) (EDS p.72) (EDS p.73) (EDS p.74)
- "Version control for your data": in a database with update in place the previous state is lost; "ledgers do not use erasers". It also helps answer "why was this order rejected?". [from source] (EDS p.72) (EDS p.74)
- The event, and not the database record, becomes the source of truth; this avoids divergence between what the service saves and what it communicates, and the atomicity problem between database and notification. [from source] (EDS p.74) (EDS p.75)
- Whole fact or delta? The author's rule: record exactly what was received, immutably; combining can be done at read time. [from source] (EDS p.79) (EDS p.80)
- Event-sourced view = projection in Event Sourcing language; it can be fully recreated from the log. [from source] (EDS p.86)
- MemoryImage: cache an entire dataset in memory; to reduce load time a "snapshot" of the log is kept via a compacted topic. [from source] (EDS p.85)
- MS-CLD: each operation that affects data is persisted in an event store, which becomes the system of record; the current state is projected by replaying the events (e.g., shopping cart); there are no updates/deletes, which minimizes contention and locks; history is kept (how the state was reached). Storage candidates mentioned: Cosmos DB, MongoDB, Cassandra, CouchDB, RavenDB. Cost: complexity and learning curve. [from source] (MS-CLD p.104) (MS-CLD p.105)
- MS-MIC: ES stores only domain events in place of the current state; it gives the history and the state at any instant in the past; it requires restructuring a good part of the system and a suitable database (Event Store, Cosmos DB, etc.); "it is not the easiest solution unless you already know event sourcing". [from source] (MS-MIC p.158) (MS-MIC p.159)
- Periodic snapshots (e.g., "every 100 events") and O(1) load time: NOT in the corpus. [extrapolation] (common technique to bound the cost of replay).
- "Temporal queries/time travel" appear in MS-MIC as "determine the state of the system at any moment in the past". [from source] (MS-MIC p.159)

## 2. CQRS

- CQS (Bertrand Meyer): methods either return state (queries, with no side effects) or change state (commands), not both; CQRS (Greg Young, popularized by Udi Dahan) is more elaborate and is based on commands, events, and optionally asynchronous messages; it often involves different physical databases for reads and writes; a more evolved version uses Event Sourcing in the write database. [from source] (MS-MIC p.199) (MS-MIC p.200)
- Simplified version used in eShopOnContainers: separate queries and commands with two logical models and ONE database; DDD (aggregates, etc.) only on the transactional side; simple queries with a micro ORM (Dapper) and tailored ViewModels, without the restrictions of DDD. [from source] (MS-MIC p.200) (MS-MIC p.201) (MS-MIC p.202) (MS-MIC p.203)
- CQRS and most DDD patterns are NOT top-level architectural styles (microservices, SOA, and EDA are); they describe something inside a component; different bounded contexts adopt different patterns; "do not use CQRS and DDD everywhere"; many microservices are better off as simple CRUD. [from source] (MS-MIC p.202) (MS-MIC p.203)
- MS-CLD: separating read and write operations can maximize performance, scalability, and security; read in a denormalized representation, write in a normalized model; synchronization by event when the write side is modified; read and write scale independently and stricter security can be imposed on writes; it results in a more complex design and should be applied strategically. [from source] (MS-CLD p.103) (MS-CLD p.104)
- Eventual consistency: the read model synchronizes "eventually"; there may be lag. [from source] (MS-CLD p.104) EDS: the read side runs slightly behind; the user may not "read their own writes"; there are strategies (e.g., blocking read). [from source] (EDS p.77) The "milliseconds of lag" and "optimistic updates or WebSockets" from the previous package are speculation; MS-MIC recommends making eventual consistency explicit to the user. [from source] (MS-MIC p.71)
- EDS: CQRS separates the write path from the read path with an asynchronous channel; analogy with the databases' write-ahead log; benefits: writing to Kafka is faster than to a database, batch maintenance of update-in-place structures, and independently optimized reads/writes. [from source] (EDS p.76)
- Materialized views and polyglot views: many read models, each on the appropriate technology (e.g., key-value for the site and Elasticsearch/Solr for text search), rebuildable from the log. [from source] (EDS p.77) (EDS p.78)
- For queries that cross services, MS-MIC lists an aggregating API Gateway, GraphQL Federation, CQRS with read tables/Materialized View, and "cold data" in a central reporting database; if you constantly aggregate information from several services, it may be a sign of bad design (perhaps merge services). [from source] (MS-MIC p.47) (MS-MIC p.48)
- Implementation with Kafka: Kafka Streams (tables and state stores) and Kafka Connect (CDC, sinks to read databases). [from source] (EDS p.80) (EDS p.81) (EDS p.82) (EDS p.84)

## 3. When to adopt (synthesis)

[inference] According to the sources: simple CRUD does not need CQRS (MS-MIC p.202-203); CQRS comes in when reads and writes have very distinct demands or need to scale separately (MS-CLD p.103-104; MS-MIC p.203: "query and transaction demands are drastically different"); Event Sourcing comes in when history/audit/replay are worth the cost of complexity (MS-CLD p.105; MS-MIC p.159). The "Yes/No by domain" table (financial, logistics, etc.) and the "10,000 reads to 1 write" rationale from the previous package are not in the corpus. [extrapolation]

## 4. Out of scope

Aggregates/tactical DDD (see the Clean Architecture/DDD package), event versioning (EDS ch. 13 only on schemas), Command Bus/MediatR in detail (MS-MIC p.286 onward), saga consistency with ES.
