# SB3G-01. Spring Boot advantages and 3.0 novelties (SB3G p.22-39)

[from source] Ch.1 is **motivational/introductory**; it contains few technical specifications. Everything below is the author's statement about version 3.0, [DATED] (2024 book).

## Eight advantages listed (SB3G p.23-30)
1. **Rapid development:** auto-configuration and starters; Spring Initializr generates the project (SB3G p.23-24).
2. **Microservices-ready:** scales per component (SB3G p.24).
3. **Simplified configuration:** "convention over configuration"; contrast XML vs `@Service` + `application.properties` with `spring.datasource.*` (SB3G p.25-26).
4. **Ecosystem:** SQL/NoSQL, messaging (Kafka, RabbitMQ), Spring Cloud, AWS/Azure/GCP integration, security (OAuth 2.0/JWT), Actuator, third-party integrations (SB3G p.26-28).
5. **Cloud-native:** scalability/elasticity and binding to cloud services; cites Cloud Foundry as an example (SB3G p.28-29).
6. **Easier testing:** does not impose a framework (JUnit, TestNG etc.) (SB3G p.29).
7. **Active development** and 8. **community plugins** (SB3G p.29-30).

## Spring Boot 3.0 novelties according to the book (SB3G p.30-33)
- **Java 17 baseline** (sealed classes example) (SB3G p.30-31). The book also says Java 19 is supported and mentions "AppStartup" and a new dependency resolution algorithm (SB3G p.22); [inference] treat as the author's statements, not verified against the official documentation.
- **GraalVM:** less memory and faster startup for serverless (SB3G p.31).
- **Observability with Micrometer** and Micrometer Tracing (SB3G p.31).
- **Jakarta EE 10** (SB3G p.31).
- **MVC and RFC 7807:** error handling with `ProblemDetail` and `@RestControllerAdvice` (example with `new ProblemDetail()` and setters) (SB3G p.32).
- **Kotlin:** "improved" support cited, without details (SB3G p.33).

## Divergence
- p.22/p.30 (Java 17 baseline) vs p.80 ("minimum Java 11"): see `00-fontes-e-lacunas.md` §3.

## Boundary
Official details on 2.x -> 3.0 migration, the full list of changes and properties: **spring-boot-reference-expert**. The agent does not claim what changed between versions beyond the text above.
