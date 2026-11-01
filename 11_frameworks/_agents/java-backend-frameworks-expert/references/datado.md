# [DATED]: what ages in each source

## SB3G (July 2024; Spring Boot 3.2.x)
- Versions: Spring Boot 3.2.5 (SB3G p.81) and 3.2.1 (SB3G p.188); Spring Cloud 2023.0.1 (SB3G p.234); JDK 17 and Gradle 8.7 (SB3G p.15).
- Images: `bitnami/keycloak:latest` and variables `KEYCLOAK_USER`/`DB_*` (SB3G p.136-138); path `/auth/realms/` (SB3G p.142); `postgres:latest`, `mongo:4.4.6` (SB3G p.174); `prom/prometheus:v2.20.1` (SB3G p.202); `grafana/grafana:7.2.0` and dashboard 12900 (SB3G p.204); `confluentinc/cp-kafka` with ZooKeeper (SB3G p.213); `hlebalbau/kafka-manager:latest` (SB3G p.223).
- Statements about 3.0: Java 17 baseline, GraalVM, Micrometer, Jakarta EE 10, ProblemDetail (SB3G p.30-32).
- The Keycloak UI changes (SB3G p.141).

## QRK (2021; Quarkus 2.x)
- Plugin `2.2.3.Final` and logs `2.1.4.Final` (QRK p.3, 5); `quarkus.package.type=native` (QRK p.5); Mandrel/OpenJDK 11 (QRK p.5); measurements 5.984 s vs 0.013 s (QRK p.5) and figure 7 (QRK p.6); "about 450 extensions" (QRK p.1); `quarkus-maven-plugin:create` (QRK p.3).

## MPS (2024-11-09; MapStruct 1.6.3)
- Version 1.6.3 in all examples (MPS p.4); `maven-compiler-plugin` 3.8.1/3.5.1 and source/target 1.8 (MPS p.4, 6); Lombok 1.18.16 and binding 0.2.0 (MPS p.95); `MappingControl` experimental since 1.4 (MPS p.36); nested reverse experimental (MPS p.77).

## General rule
The agent does not know what changed after each date. If the user cites a later version, agree and mark [DATED]; do not claim version differences that the text does not provide.
