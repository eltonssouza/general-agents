# Glossary (terms as used in the sources)

| Term | Source | Meaning according to the text |
|---|---|---|
| Annotation processor | MPS p.3 | Generates the mapper implementations at compile time (JSR 269) |
| `@Mapper` / `@Mapping` | MPS p.14 | Marks the mapping interface / configures a property (`target`, `source`, ...) |
| `componentModel` | MPS p.8, 31 | How the generated mapper is obtained: `default`, `cdi`, `spring`, `jsr330`, `jakarta`, `jakarta-cdi` |
| `InjectionStrategy` | MPS p.31-32 | `CONSTRUCTOR`, `FIELD`, `SETTER` |
| `@MappingTarget` | MPS p.20 | Parameter that is updated instead of creating an instance |
| `@ObjectFactory` | MPS p.60-63 | Method that creates the target (may receive the sources) |
| `@Context` | MPS p.42 | Parameter passed on to custom methods, factories and before/after |
| `@TargetType` | MPS p.40 | `Class` parameter with the target type |
| `@Qualifier` / `@Named` | MPS p.44-46 | Selection among methods with the same signature |
| `@ValueMapping` / `@EnumMapping` | MPS p.53, 58 | Mapping of enum constants / name transformation |
| `@InheritConfiguration` / `@InheritInverseConfiguration` | MPS p.76-77 | Direct / inverse configuration reuse |
| `@MapperConfig` | MPS p.78 | Shared configuration for several mappers |
| SPI | MPS p.84 | Processor extension points via `META-INF/services` |
| Builder / `BuilderProvider` | MPS p.22 | Mapping to immutable builder-based types |
| Funqy / `@Funq` | QRK p.6 | Quarkus portable serverless function API |
| DEV UI / dev mode | QRK p.3 | Local interface and development mode with live coding |
| Knative / CloudEvents | QRK p.4, 8 | Serverless deployment target / common event format |
| Mandrel | QRK p.5 | GraalVM distribution used for native binaries in Quarkus |
| Starter | SB3G p.24 | Dependency that brings auto-configuration (concept cited) |
| Auto-configuration | SB3G p.236 | Boot configures the application from the classpath, beans and properties |
| `ProblemDetail` / RFC 7807 | SB3G p.32 | Standardized error body in APIs |
| WebFlux / Reactor / `Mono` / `Flux` | SB3G p.79 | Reactive web / reactive library / stream of 0-1 / 0-N elements |
| Backpressure | SB3G p.75, 92 | Consumer controls how much it receives; in Reactor, `request(n)` |
| R2DBC | SB3G p.81 | Reactive relational access |
| CQRS / Event Sourcing / Saga / DDD | SB3G p.47-70 | Architectural patterns of ch.2 |
| Keycloak / realm / client | SB3G p.135-141 | Open-source IAM used in the OAuth2 examples |
| Resource server | SB3G p.143 | Application that validates JWTs |
| `SecurityFilterChain` / `SecurityWebFilterChain` | SB3G p.133, 155 | Servlet / reactive security configuration |
| RBAC | SB3G p.148 | Role-based access control |
| Testcontainers / WireMock | SB3G p.155, 176 | Disposable containers for testing / simulation of HTTP services |
| Layered jar / Buildpacks | SB3G p.189-190 | Layered jar / image generated without a Dockerfile |
| Liveness / readiness | SB3G p.192 | Kubernetes probes |
| Liquibase / changelog | SB3G p.125 | Versioned schema migration |
| Spring Batch (job/step/chunk) | SB3G p.121 | Batch processing with reader/processor/writer |
| AOP (aspect, advice, pointcut) | SB3G p.211 | Separation of cross-cutting concerns |
| Feign | SB3G p.233 | Declarative HTTP client (Spring Cloud OpenFeign) |
| CMAK | SB3G p.222 | Cluster Manager for Apache Kafka (formerly Kafka Manager) |
