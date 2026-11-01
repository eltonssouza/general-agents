# Messaging and event-driven architecture

Sources: EDS (Stopford, Confluent/O'Reilly 2018), MS-MIC, MS-CLD, SDH, SAP, SBC, JMG. Pages = PDF (EDS: printed = PDF - 15). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. The SAP mediator/broker topologies are in `padroes-arquiteturais-fundamentais.md`.

## 1. Queues, topics, and event bus

- Message queue: an asynchronous communication mechanism; producers send and move on, several consumers can pull from the queue to distribute load. [from source] (SDH p.13)
- Queue = point to point: the queue guarantees that the message is processed by exactly one of the consumer instances; producer or consumer scale without affecting the other; technologies may differ at the ends. [from source] (MS-CLD p.82) MS-MIC: single-receiver, ideal for asynchronous commands; since clouds recover from failures, the same message may arrive more than once, so the receiver must be idempotent. [from source] (MS-MIC p.70)
- Topic = one-to-many: one service publishes, several subscribe; publisher and subscribers do not know each other. [from source] (MS-CLD p.85) (MS-CLD p.86) MS-MIC: publish/subscribe allows adding subscribers without changing the sender (open/closed principle). [from source] (MS-MIC p.71)
- Event bus: an abstraction/interface with publish, subscribe, and unsubscribe, with an implementation on top of a broker; for a prototype, RabbitMQ in a container is enough; for high-scale production MS-MIC suggests evaluating Azure Service Bus and service buses such as NServiceBus, MassTransit, and Brighter (which offer, for example, Sagas). [from source] (MS-MIC p.71) (MS-MIC p.72) (MS-MIC p.73) (MS-MIC p.149)
- Microservices community preference: a lightweight ("dumb") broker, with the intelligence in the endpoints; unlike the large brokers of SOA. [from source] (MS-MIC p.69) (MS-MIC p.70)
- If event-driven eventual consistency is adopted, it must be explicit to users and the business. [from source] (MS-MIC p.71)
- A message has a header (metadata such as identification/security) and a body. [from source] (MS-MIC p.69)

## 2. Azure service numbers and limits in MS-CLD [DATED]

The values below are from the analyzed edition of MS-CLD and change often; check the service's current documentation before using them.
- Storage Queues: up to 500 TB, message up to 64 KB, no ordering guarantee, 7-day retention, no duplicate detection/transactions. [from source] (MS-CLD p.82) (MS-CLD p.83)
- Service Bus Queues: FIFO, message up to 256 KB, queue size up to 80 GB, duplicate detection, partitioning, sessions, transactions. [from source] (MS-CLD p.83) (MS-CLD p.84)
- Service Bus Topics: up to 2,000 subscribers. [from source] (MS-CLD p.86)
- Event Grid: push model, guaranteed delivery within 24 h with retry and dead-letter; no ordering/transactions/sessions. [from source] (MS-CLD p.88)
- Event Hubs: partitioned streaming, default retention of 1 day (configurable), keeps events after they are read. [from source] (MS-CLD p.89)

## 3. Kafka as a distributed log (EDS)

- A Kafka cluster is a collection of files full of messages; the abstraction is the partitioned log (append-only files), which favors sequential access. [from source] (EDS p.32)
- The consumer reads from the position of the last message read and periodically records its new position; reading and writing are sequential; O(1) read/write on a partition; it works as an event store for Event Sourcing. [from source] (EDS p.33) (EDS p.34)
- Partition: a "bucket" of data; each log is a replica of a partition; the producer's partitioner uses round-robin or, if there is a key, a hash of the key, so the same key always goes to the same partition and is strongly ordered. [from source] (EDS p.34)
- Ordering: Kafka only guarantees ordering within a partition; for relative order, the same key (e.g., CustomerId); global ordering requires a single-partition topic, with throughput limited to one machine; producer retries must send batches one at a time per destination so as not to reorder. [from source] (EDS p.36) (EDS p.37)
- Consumer group: messages of a topic are spread among the consumers of a group; a partition is assigned to only one consumer instance (invariant), which preserves order even with failures and restarts; services inherit load balancing and high availability. [from source] (EDS p.35) (EDS p.38) (EDS p.39) [inference] Hence the useful parallelism of a group is limited by the number of partitions (extra instances sit idle).
- Durability by replication: with factor 3, two machines can be lost without losing data; for sensitive data, 3 replicas per partition and the producer waiting for replication, with retries; synchronous disk flush should be used sparingly. [from source] (EDS p.37) (EDS p.38)
- Compacted topics: keep only the latest event per key (asynchronous process, superseded versions may linger for a while); they retain data with a primary key; useful for tables in stream processing. [from source] (EDS p.39) (EDS p.40)
- Retention: time-based by default; Kafka keeps data for two weeks by default (configurable) — the previous package said "7 days". Removing a record with a null value (delete marker/tombstone); in a compacted topic the message with a key and null value is removed on compaction. [from source] (EDS p.142) (EDS p.143)
- Long-term storage: topics above 100 TB are not uncommon, but Kafka is not a database (no broad queries); the "latest-versioned" pattern combines a regular and a compacted topic. [from source] (EDS p.40)
- Quotas: limit bandwidth per service for a shared cluster. [from source] (EDS p.36)
- Scale examples cited (2018): a cluster of ~100 nodes at 30 GB/s (New Relic) and clusters of ~200 nodes (Netflix); clusters of 5-10 nodes serving a company. [from source] (EDS p.35) [DATED] These are examples of the time, not limits.
- Dead letter queue: a concept from traditional brokers; in Kafka, implementers create their own error topic. [from source] (EDS p.142)

## 4. Event semantics

- Events are fact and notification, with no expectation of future action or response; they can be used for notification (the consumer can still query the data owner) and for state transfer (event-carried state transfer, the event replicates the data into the consumer, which queries locally). [from source] (EDS p.46) (EDS p.50) (EDS p.52) (EDS p.53)
- Advantages of state transfer: isolation/autonomy, faster local access, and offline use; advantages of REST/RPC: simplicity, singleton state, and centralized control. [from source] (EDS p.53)
- Receiver-driven routing: the routing logic stays in the receiver, which reduces coupling and makes the system "pluggable" (e.g., a repricing service that plugs into the events). [from source] (EDS p.49) (EDS p.51)
- Event Collaboration: no service owns the whole process; each handles a subset of transitions and reacts to events (choreography); contrasted with orchestration by a process manager, easier to understand and more coupled. Choreography suits larger implementations that change independently. [from source] (EDS p.54) (EDS p.55)
- Mixing protocols: within a bounded context, request/response protocols and events; between contexts, events only. [from source] (EDS p.57) (EDS p.58)
- On coupling: loose coupling allows independent change; tight coupling extracts more value; sharing always increases coupling; essential data coupling is unavoidable. [from source] (EDS p.47) (EDS p.48) (EDS p.49)
- The sentence "a notification event with only the id forces a synchronous HTTP callback" from the previous package is an exaggeration: EDS shows that the consumer can query via REST/RPC or receive the state in the event, depending on the trade-off. [from source] (EDS p.50) (EDS p.52)

## 5. Duplicates, idempotency, and "exactly once"

- Retries cause duplicate processing (e.g., payment charged twice). Natural deduplication requires an identity key per call and a database with the history of keys; event-driven systems end up deduplicating on every message received. [from source] (EDS p.127) (EDS p.128)
- Two opportunities for duplication in the broker: sending (lost ack -> resend) and reading (unconfirmed offset -> re-read). "Exactly once" = idempotency + atomic commit: the broker uses producer identifier + sequence number per batch; the atomic commit of output and offsets (consumer offsets topic) uses markers, a transaction coordinator, and a transaction log (which the book describes as implementing two-phase commit). [from source] (EDS p.129) (EDS p.130) (EDS p.131) (EDS p.132)
- Number from the book: with commits every 100 ms and 1 KB messages, the transaction overhead is about 3% compared to in-order at-least-once delivery. It is an example measured by the author in 2018, not a guarantee. [from source] (EDS p.132)
- Limitations: only valid when input and output pass through Kafka; calls to external services, databases, stdout are not covered; a commit cannot be undone; for multi-service transactions "consider sagas". [from source] (EDS p.133) (EDS p.134)
- MS-MIC: update events must be idempotent or carry information to detect duplicates; example "set the price to 25" instead of "add 5"; deduplicate at the transport and in the application ("your best bet"); in RabbitMQ the `redelivered` flag indicates possible reprocessing. [from source] (MS-MIC p.164) (MS-MIC p.165) (MS-MIC p.166)
- SBC and SDH reinforce: retry combined with Idempotent Receiver; making operations idempotent simplifies retry. [from source] (SBC p.2) (SDH p.64)
- The taxonomy "at-most-once / at-least-once / exactly-once" as a named list does not exist in the corpus. [extrapolation] (general delivery concept). MS-CLD's Service Bus is described with "at most once delivery" in the sense of discarding duplicate messages. [from source] (MS-CLD p.84)

## 6. Out of scope

Consumer group rebalancing in detail, KSQL/Kafka Streams (EDS ch. 14-15, only mentioned), RabbitMQ/AMQP internals, MQTT (SDH only lists AMQP/MQTT, SDH p.56), Avro schemas/Schema Registry (EDS ch. 13).
