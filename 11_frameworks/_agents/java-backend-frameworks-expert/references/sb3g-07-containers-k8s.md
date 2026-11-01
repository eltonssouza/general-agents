# SB3G-07. Containers, Kubernetes and observability (SB3G p.184-206)

## Docker (SB3G p.187-191)
- Initializr project with **Spring Boot 3.2.1**, Spring Web, Gradle; `HelloController` ("Hello, Spring Boot 3!") (SB3G p.188).
- **Layered jar:** the text asks to "enable layering" without showing the configuration; it shows `BOOT-INF/layers.idx` with the layers `dependencies`, `spring-boot-loader`, `snapshot-dependencies`, `application` (SB3G p.188-189).
- **Cloud Native Buildpacks:** `./gradlew bootBuildImage --imageName=demoapp`; run `docker run -p 8080:8080 demoapp:latest` (SB3G p.190).
- **Graceful shutdown:** `server.shutdown=graceful`, `spring.lifecycle.timeout-per-shutdown-phase=20s`; `docker stop`; shutdown log messages (SB3G p.191).

## Kubernetes (SB3G p.191-199)
- Probes: *liveness* (restarts the container) and *readiness* (takes it out of traffic) (SB3G p.192). Actuator: `spring-boot-starter-actuator`; groups `management.endpoint.health.group.liveness.include=livenessState` and `...readiness.include=readinessState` (SB3G p.192).
- `Deployment` YAML (`/actuator/health/liveness` and `/readiness`, `initialDelaySeconds`, `periodSeconds`) and `Service` of type `LoadBalancer` (SB3G p.193-195). The book suggests replacing the `latest` tag with a specific version (SB3G p.194).
- Running: Docker Desktop Kubernetes; `kubectl apply -f` (SB3G p.195).
- **ConfigMap** (`app.message`) and **Secret** (`kubectl create secret generic app-secret --from-literal=api.key=...`) injected as environment variables `APP_MESSAGE` and `API_KEY` (SB3G p.196-198). The example returns the key via the `/apikey` endpoint for demonstration only (SB3G p.196); [extrapolation] it is not a safe practice.
- **Profiles:** `application-test.properties`/`application-prod.properties` and `SPRING_PROFILES_ACTIVE` (SB3G p.198-199).

## Prometheus and Grafana (SB3G p.200-206)
- `io.micrometer:micrometer-registry-prometheus`; `management.endpoints.web.exposure.include=health,info,prometheus` (SB3G p.201).
- Prometheus ConfigMap (`scrape_interval: 15s`, `metrics_path: '/actuator/prometheus'`), image `prom/prometheus:v2.20.1`, port 9090 (SB3G p.201-202). Grafana `grafana/grafana:7.2.0`, port 3000, default login admin/admin, Prometheus data source, dashboard imported by ID 12900 (SB3G p.203-204). [DATED] image versions and IDs.

## Limits
- Does not cover Helm, Kustomize, Ingress, HPA, resources/limits, GraalVM native image in practice (only cited in SB3G p.31), Spring Boot Docker Compose support, `spring-boot:build-image` via Maven: NOT COVERED.
