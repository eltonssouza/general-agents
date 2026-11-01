# SB3G-02. Microservices architectural patterns (SB3G p.42-71)

[from source] Ch.2 is **conceptual** (almost no Spring code); it uses analogies. There is no Spring implementation of the patterns, except the banking diagram example.

## Microservices
- Definition, benefits and cost (more upfront communication work) (SB3G p.44).
- Six principles: autonomy, loose coupling, reuse, fault tolerance, composability, discoverability (SB3G p.45).
- Design patterns: **Aggregator** (SB3G p.46), **API Gateway** (single entry point, authentication, routing) (SB3G p.46), **Saga** (SB3G p.47, 69-70).

## DDD (SB3G p.47-51)
- Domain and **bounded contexts**; ubiquitous language; **Anti-Corruption Layer** (SB3G p.48).
- Layers: UI, application (no business logic), domain, infrastructure (SB3G p.49).
- E-commerce example: User, Product, Order, Payment, Review, Notification services (SB3G p.50).
- The book says DDD is aimed at large projects (about six months or more) and probably overkill for small projects (SB3G p.47-48).

## CQRS (SB3G p.51-53)
- Separation of commands (write) and queries (read) (SB3G p.51-52).
- Best practices: start simple, clear communication, database design, testing; pitfalls: overcomplication, getting the scale wrong, mixing responsibilities, learning curve (SB3G p.52-53).
- Benefits: independent scaling, optimized schemas, security, separation of concerns (SB3G p.53).
- The book warns that CQRS is not suited to everything and increases complexity if there is no real imbalance (SB3G p.52).

## Event Sourcing and EDA (SB3G p.54-65)
- EDA: producer, broker, consumer; immutable events (SB3G p.54-55). Event Sourcing: an event log rebuilds the state (inventory example: 10 items and 2 purchases = 8) (SB3G p.55-56); parallel reading (SB3G p.56-57); EDA vs ES difference (SB3G p.57-58); JSON example of user events (SB3G p.58-60).
- ES + CQRS: UI, command, event store, publication, event handler/bus, read database, materialized view (SB3G p.60-63). Banking example with Kafka (SB3G p.64-65).

## Other patterns (SB3G p.65-70)
SOA with ESB (SB3G p.66), **Circuit Breaker** (SB3G p.66-67), Layered (SB3G p.67-68), MVC (SB3G p.68-69), Saga with compensating transactions (SB3G p.69-70).

## Limits
- The book does **not** tie Circuit Breaker, Saga, API Gateway to specific Spring libraries (Resilience4j, Spring Cloud Gateway etc.). Do not state this as from the book: NOT COVERED.
