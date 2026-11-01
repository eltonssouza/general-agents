# SB3G-03. Reactive REST, WebFlux and backpressure (SB3G p.72-97)

## Concepts (SB3G p.73-79)
- Reactive = non-blocking, data streams, change propagation; vocabulary: Observable, Observer, Subscription, Subject, backpressure, asynchronous operations (SB3G p.74-76). The text uses analogies (supermarket checkout, water fountain) and makes a reference to "Android" that does not apply to Spring (SB3G p.76).
- When to consider: real-time UIs, complex network applications, microservices, IoT/streaming; criteria: performance, volume/velocity, complexity, resource constraints (SB3G p.76-77). The book says the decision is not "use the newest" (SB3G p.77).
- Company examples: Booking.com (Spring WebFlux), The Guardian (Akka/Play), Patreon (RxJava) (SB3G p.78).
- **WebFlux** and **Project Reactor** (`Flux` 0..N, `Mono` 0..1) are the reactive libraries cited (SB3G p.79).

## Sample project (SB3G p.80-90)
- Initializr with **Spring Boot 3.2.5**, Java 17, dependencies **Spring Reactive Web**, **Spring Data R2DBC**, **H2**, Gradle build (SB3G p.80-81).
- Model: `@Table("users") public record User(@Id Long id, String name, String email) {}` (SB3G p.82); explains records (immutability, less boilerplate) (SB3G p.82-83).
- H2/R2DBC properties: `spring.h2.console.enabled=true`, `spring.r2dbc.url=r2dbc:h2:mem:///testdb`, `spring.r2dbc.username=sa`, `spring.sql.init.mode=always`, `spring.sql.init.platform=h2`; `schema.sql` in `resources` (SB3G p.83-84).
- Repository: `R2dbcRepository` (or `ReactiveCrudRepository`) returns `Mono`/`Flux` (SB3G p.84). The example declares `R2dbcRepository<User, String>` with `Long id` (inconsistency) (SB3G p.82, 84).
- Controller: `@RestController`, `@RequestMapping("/users")`; CRUD returning `Mono<User>`, `Flux<User>`, `Mono<Void>` (SB3G p.85-86).
- `createUser` with email uniqueness: `flatMap`, `then`, `map`, `doOnNext`, `onErrorResume` (409 on conflict) (SB3G p.87-88).
- Running: `./gradlew bootRun`, port 8080 by default; manual tests via `curl` (POST/GET/DELETE; 409 and 204) (SB3G p.88-90).

## Backpressure (SB3G p.91-97)
- Problem: a consumer slower than the producer leads to memory overflow, performance degradation and system crashes (SB3G p.92).
- In Reactor, the subscriber requests data with `request(n)` (SB3G p.92).
- Strategies: buffering, dropping, batching, rate limiting (SB3G p.93).
- Experiment: `/stream` endpoint with `onBackpressureBuffer()` vs `getAllUsers`; bash script with 300 concurrent `curl` requests (SB3G p.94-95). The book concludes that time grows more slowly on `/stream` and warns that the local test does not replace monitoring (SB3G p.95-96). [inference] treat as an **illustration**, not a benchmark.

## Limits
- Does not cover WebClient in detail (only mentions it in the comparison with Feign, SB3G p.233), nor R2DBC with PostgreSQL, nor reactive transactions: NOT COVERED.
- The book's code was **not run** by the agent.
