# Glossary (SBR 2.7.18 terms; pages = PDF, printed = N−20)

| Term | Meaning according to the text | SBR p. |
|---|---|---|
| Starter | Set of `spring-boot-starter-*` dependency descriptors; third parties do not use the `spring-boot` prefix | 44-45 |
| Auto-configuration | Automatic configuration based on the dependencies; opt-in with `@EnableAutoConfiguration`; backs off if you define the bean | 50-51 |
| `@SpringBootApplication` | Meta-annotation: `@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan` | 36, 54 |
| Fat/uber/executable jar | Executable jar with nested jars (`BOOT-INF/lib`); differs from "shaded" | 37, 837 |
| Relaxed binding | Rules that match `kebab-case`, `camelCase`, `underscore` and `UPPERCASE` to the same property | 115-117 |
| `@ConfigurationProperties` | Binds external properties to a typed object (JavaBean or constructor binding) | 103-112 |
| `PropertySource` | Source of `Environment` properties; 15-level order | 87-88 |
| Config data | `application.properties/yaml` files and imports (`spring.config.import`) | 88, 90-98 |
| Profile | Named configuration segment activated by `spring.profiles.active` | 133-137 |
| Multi-document file | File split into logical documents (`---` or `#---`) | 99-100 |
| Configuration tree | Directory in which file name = key and content = value (`configtree:`) | 96-98 |
| Devtools | Development module: restart, LiveReload, dev defaults; turned off in a packaged app | 58-70 |
| Liveness / Readiness | Availability states: "can I recover?" / "can I receive traffic?" | 77 |
| Actuator | Module of production-ready features (endpoints, metrics, health) | 440 |
| Endpoint | Management point; available when enabled and exposed | 440, 442-443 |
| Health group | Subset of indicators served at `/actuator/health/<group>` | 460-462 |
| Micrometer / `MeterRegistry` | Metrics facade; registries per monitoring system | 477-480 |
| `FailureAnalyzer` | Converts a startup exception into a readable message with an action | 72, 556 |
| `CommandLineRunner` / `ApplicationRunner` | Code run after startup, before accepting traffic | 83-84 |
| Slice test | Test that loads only part of the context (`@WebMvcTest`, `@DataJpaTest`...) | 172 |
| `@MockBean` / `@SpyBean` | Replace/spy on a bean with Mockito in the test context | 168-171 |
| Layered jar | Jar with `layers.idx` for Docker/OCI image layers | 436-437 |
| Buildpacks | Image build directly from the Maven/Gradle plugins (Cloud Native Buildpacks) | 438-439 |
| `PropertiesLauncher` | Launcher configurable via `loader.*`; `loader.home` default `${user.dir}`, `loader.system` default `false`, `loader.path` empty = `BOOT-INF/lib`; lookup: environment, system properties, `loader.properties`, exploded manifest, manifest | 841-843 |
| Configuration metadata | Property metadata JSON for IDEs | 799-820 |
| SBR | Abbreviation of this collection: *Spring Boot Reference Documentation 2.7.18* | 1 |
| h2 / h2c | HTTP/2 over TLS / HTTP/2 over plain TCP (useful behind a proxy that terminates TLS) | 574 |
| PKCS#8 / PKCS#1 / SEC 1 | PEM private-key formats: PKCS#8 is the preferred one; the others convert with `openssl pkcs8 -topk8 -nocrypt` | 574 |
| ALPN | Application-layer protocol negotiation required by h2 over TLS (JDK 9+, or libtcnative/ALPN dependencies on JDK 8) | 574-575 |
| Meter (Micrometer) / tag | The `metrics` endpoint sums the meters that match the name and the tags (`tag=key:value`) | 517 |
| `step` (Micrometer) | Step size (reporting frequency) of an exporter; in StatsD it sets the statistics window as `max` | 793 |
| Embedded LDAP | In-memory LDAP server (UnboundID) auto-configured for tests | 369-370 |
| Fully executable jar | Jar with an embedded launch script (init.d); cannot be zip64 | 534-535 |
