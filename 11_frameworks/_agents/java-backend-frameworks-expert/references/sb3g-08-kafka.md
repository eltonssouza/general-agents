# SB3G-08. Event-driven with Kafka (SB3G p.208-226)

## Concepts (SB3G p.209-212)
- EDA and benefits (responsiveness, scalability, flexibility, efficiency, experience) (SB3G p.209). Kafka as broker; LinkedIn/Apache origin (SB3G p.210). ZooKeeper coordinates brokers (SB3G p.210).
- Brokers, topics, partitions, replication and offsets; consumer groups (SB3G p.211-212).

## Environment (SB3G p.212-214)
- `docker-compose.yml` with `zookeeper` (2181) and `confluentinc/cp-kafka` (9092), `KAFKA_ZOOKEEPER_CONNECT`, `KAFKA_ADVERTISED_LISTENERS`, `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1`; `docker-compose up -d` (SB3G p.213). [DATED] ZooKeeper architecture and unpinned image tags.

## Applications (SB3G p.214-221)
- Two Spring Boot projects (producer and consumer), dependency **Spring for Apache Kafka**; Spring Web in the producer; different ports (SB3G p.215-216). Divergence: p.216 shows `server.port:8181` and p.220 uses 8282 on the producer and 8181 on the consumer.
- **Producer:** `KafkaTemplate<String,String>`; `GET /message/{message}` sends to the topic `messageTopic`; properties `spring.kafka.bootstrap-servers`, `producer.key-serializer`, `producer.value-serializer` (SB3G p.217-218).
- **Consumer:** `@KafkaListener(topics = "messageTopic", groupId = "consumer_1_id")`; properties `consumer.group-id`, `consumer.auto-offset-reset=earliest`, String deserializers (SB3G p.219).
- End-to-end test: start the compose, producer (8282), consumer (8181), call `GET http://localhost:8282/message/hello-world` and watch the log (SB3G p.220-221).

## Monitoring (SB3G p.221-226)
- Suggested metrics: brokers, topics, consumer lag, producers (SB3G p.222). **CMAK** (Kafka Manager) in the compose (`hlebalbau/kafka-manager:latest`, port 9000, `ZK_HOSTS`) (SB3G p.223-225). [DATED]

## Limits
- Does not cover JSON/Avro serialization, error handling/retries/DLT, Kafka transactions, exactly-once delivery, Kafka in KRaft mode, Spring Cloud Stream, RabbitMQ (only mentioned in SB3G p.27): NOT COVERED.
