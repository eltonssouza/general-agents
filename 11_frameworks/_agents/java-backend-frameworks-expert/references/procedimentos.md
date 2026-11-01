# Procedures (P1-P8)

Each step cites the source. Steps without a source are `[extrapolation]`.

## P1. Choose the right source
1. Question about **MapStruct**? Use MPS (official reference 1.6.3). 2. About **Spring Boot in practice** (reactive, JPA, security, testing, K8s, Kafka, AOP/Feign)? Use SB3G. 3. About **Quarkus**? Only QRK (serverless, 2021); the rest is NOT COVERED. 4. About Spring Boot properties/attributes/load order in detail? Route to **spring-boot-reference-expert**.

## P2. Set up a Spring Boot 3 project according to SB3G
Use `python -I scripts/sb3_checklist.py list` and `scan DIR`. Book's didactic order: Initializr with Java 17 and Gradle (SB3G p.80-81, 188) -> model and repository (SB3G p.82-86, 104-105) -> database via Docker Compose (SB3G p.105-106, 112-113) -> security (SB3G p.133-153) -> tests (SB3G p.161-178) -> image and K8s (SB3G p.188-199) -> observability (SB3G p.201-204).

## P3. Data and migration
JPA + Postgres (SB3G p.103-106), Mongo (SB3G p.112-114), cache (SB3G p.117-118), batch (SB3G p.120-123), Liquibase with `includeAll` and numbered files (SB3G p.125-127). For each item, state what is **not** covered (see `sb3g-04`).

## P4. OAuth2/JWT security
Security starter (SB3G p.133) -> Keycloak (SB3G p.136-141) -> dependencies and properties (SB3G p.141-143) -> resource server with JWT (SB3G p.143) -> RBAC with role converter (SB3G p.151-153). Warn: the example's credentials and `password` flow (SB3G p.145) are didactic [extrapolation].

## P5. Write a MapStruct mapper
1. `@Mapper` interface (MPS p.14). 2. Choose `componentModel` (MPS p.8, 31). 3. Map divergences with `@Mapping` (MPS p.14). 4. Define a policy for unmapped properties (MPS p.10). 5. Conversions/formats (MPS p.32-34). 6. Collections (MPS p.48-49). 7. Enums (MPS p.53-60). 8. Verify the build (mapping errors appear at compile time, MPS p.3). Use `scripts/mapstruct_tool.py generate|validate`.

## P6. Update / inverse mapper
`@MappingTarget` (MPS p.20), `@InheritConfiguration`/`@InheritInverseConfiguration` (MPS p.76-77), `nullValuePropertyMappingStrategy` (MPS p.68-69), `@Condition` (MPS p.70-72).

## P7. Choose between approaches
Use `scripts/compare_approaches.py list|compare`. Where the text does not compare (e.g. Quarkus vs Spring Boot in real performance), say so and label `[extrapolation]` if the user insists.

## P8. Answer outside coverage
Say "NOT COVERED", cite the closest source and route (spring-boot-reference-expert for official Spring Boot). Do not fill in from memory.
