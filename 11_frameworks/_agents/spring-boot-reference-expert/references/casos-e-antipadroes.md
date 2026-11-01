# Cases and antipatterns (symptom → what the text says → page)

Pages = PDF (SBR p.N; printed = N−20). Version 2.7.18 [DATED]. Each row is a statement from the book; probable causes marked [inference] are deductions.

| # | Symptom / antipattern | What the text says | SBR p. |
|---|---|---|---|
| 1 | `spring.config.location` in `application.properties` has no effect | `spring.config.name/location/additional-location` are read early and must be environment properties (OS variable, system property, argument) | 91 |
| 2 | `spring.profiles.active` inside `application-prod.yml` | only valid in non-profile-specific documents | 135 |
| 3 | Actuator `include: *` in YAML gives a parse error | `*` has special meaning in YAML; use quotes | 445 |
| 4 | `shutdown`/`loggers` endpoint returns 403 on POST | CSRF is on; with the default security config POST/PUT/DELETE give 403 | 448 |
| 5 | I defined a `SecurityFilterChain` for the Actuator and the rest of the app was left without default rules | a `SecurityFilterChain` bean makes Boot's default security back off completely; configure the rest as well | 448 |
| 6 | Database down restarts all pods | liveness must not depend on external checks (restart cascade) | 77, 464 |
| 7 | Pod receives requests while terminating | window between the start of shutdown and removal from the load balancer; use `preStop` with sleep + graceful shutdown; adjust the grace period | 527-528 |
| 8 | Immediate 503 error on Undertow during shutdown | Undertow accepts requests but answers 503 during graceful shutdown; the others stop accepting at the network level | 300 |
| 9 | RabbitMQ messaging reprocesses the same message endlessly | without retry and with an exception in the listener there is indefinite redelivery; `defaultRequeueRejected=false` or `AmqpRejectAndDontRequeueException` | 388 |
| 10 | Quartz tables disappear on every restart | Quartz default scripts drop tables when the schema is initialized (`initialize-schema=always`) | 416 |
| 11 | Schema created twice (Hibernate + scripts/Flyway) | use a single mechanism; do not mix `schema.sql/data.sql` with Flyway/Liquibase | 628, 630 |
| 12 | `data.sql` runs before Hibernate creates the tables | scripts run before the `EntityManagerFactory` beans; use `spring.jpa.defer-datasource-initialization=true` | 630 |
| 13 | Hikari ignores `app.datasource.url` | Hikari uses `jdbc-url`; use your own `DataSourceProperties` or the explicit type | 606 |
| 14 | `ddl-auto` created/dropped the schema in another environment | default `create-drop` only with an embedded database and no schema manager; otherwise `none`; when leaving the embedded database do not assume tables exist | 617, 629 |
| 15 | `spring.jpa.properties.hibernate.jdbc.batch-size` has no effect | `spring.jpa.properties.*` has no relaxed binding; use the exact Hibernate name | 618 |
| 16 | `@MockBean` does not change behavior during startup | not suitable for beans exercised during the refresh; create the mock with `@Bean` | 171 |
| 17 | Test context starts several times | `@MockBean`/`@SpyBean` change the context cache key | 171 |
| 18 | Test slice "sees" too many components | a custom `@ComponentScan` on the app class disables the slice filters | 158, 222-223 |
| 19 | `@Transactional` in the test does not roll back data written by the server | with RANDOM_PORT/DEFINED_PORT client and server run in different threads/transactions | 156 |
| 20 | Key has no effect because camelCase was used in a placeholder | placeholders must use the canonical kebab-case form | 99 |
| 21 | Property list "does not merge" across profiles | lists are replaced as a whole (only the highest-priority one counts, items are not merged); maps merge by key; the rule holds for properties from all sources, not just files (NOTE on p.121) | 117-121 |
| 22 | `.json` suffix in the URL does not match the controller | suffix matching is disabled (and deprecated); use a parameter or content negotiation | 260-261 |
| 23 | `NoHandlerFoundException` is never thrown | static content mapped to `/**` serves everything; restrict `static-path-pattern` or `add-mappings=false` | 262 |
| 24 | MVC app + `starter-webflux` did not become reactive | with both, Boot configures MVC; force it via `setWebApplicationType(REACTIVE)` | 289 |
| 25 | Servlet filter does not run on the error page | the filter needs the `ERROR` dispatcher; the default `FilterRegistrationBean` does not include it | 270-271 |
| 26 | `Filter` order ignored when annotating the `@Bean` method | order with `@Order`/`Ordered` on the filter class or `FilterRegistrationBean#setOrder` | 276 |
| 27 | Devtools "works in production" | devtools turns itself off in a packaged app; enabling with `-Dspring.devtools.restart.enabled=true` is a security risk; remote devtools never in production | 59, 68 |
| 28 | H2 console exposed | development only; behind Security it requires CSRF off and SAMEORIGIN for the console | 334-336 |
| 29 | Executable jar becomes "corrupted"/does not extract | fully executable jars have a script at the start (`jar -xf` may fail); zip64 cannot be executable | 534-535 |
| 30 | `layertools` does not work in the image | does not work with a fully executable jar with a launch script | 437 |
| 31 | Using JUL in an executable jar gives a class error | JUL uses the system classloader and there are known problems with executable jars; prefer another implementation | 143, 843 |
| 32 | E-mail hangs threads | some SMTP timeouts are infinite; set `mail.smtp.*timeout` | 418 |
| 33 | Spring Boot app used as a dependency | does not work (classes in `BOOT-INF/classes`); use a classifier or a separate module | 655 |
| 34 | `application.properties` with `@..@` does not expand | only with `starter-parent` (or manual filtering); production only, not `src/test/resources` | 560-561 |
| 35 | Batch job arguments vanish | `--x=y` arguments become Environment properties and do not go to the job | 638 |
| 36 | `@DataJpaTest` data vanishes at the end of the test | the slice is transactional and rolls back; turn it off with `@Transactional(propagation = Propagation.NOT_SUPPORTED)` on the test or class (`@Rollback`/`@Commit` are not in the Reference) | 190-191 |
| 37 | `@DataJpaTest` uses H2 and not the application's Postgres | the slice configures an embedded database if one is on the classpath; `@AutoConfigureTestDatabase(replace = Replace.NONE)` uses the real database | 190, 193 |
| 38 | `@Service`/`@Component` does not exist in `@DataJpaTest`/`@WebMvcTest` | plain `@Component` and `@ConfigurationProperties` are not scanned in slices; `@EnableConfigurationProperties` or `@Import` | 175, 190, 221 |
| 39 | `@WebFluxTest` does not find a functional route or `SecurityWebFilterChain` | the slice does not detect `RouterFunction` or that bean: `@Import` or `@SpringBootTest` | 182 |
| 40 | Rabbit message redelivered forever after a listener exception | with retries off (default) delivery is repeated indefinitely; `defaultRequeueRejected=false` or `AmqpRejectAndDontRequeueException`; with retries, `RejectAndDontRequeueRecoverer` and a DLX if the broker is configured | 388 |
| 41 | `/actuator/prometheus` does not respond (404) | the endpoint is not exposed by default: expose it and use `metrics_path: "/actuator/prometheus"` in the scrape_config | 494 |
| 42 | WAR on Tomcat uses the wrong pool | `spring.datasource.type` bypasses the algorithm and matters if the Tomcat container provides `tomcat-jdbc`; jdbc/data-jpa starters bring HikariCP | 326 |
| 43 | Devtools in the production jar | a repackaged jar does not carry devtools by default (`excludeDevtools=false` includes it, for remote only); enabling with `-Dspring.devtools.restart.enabled=true` in production is a risk | 59, 68 |
| 44 | Redis cache with TTL for only one cache | `spring.cache.redis.time-to-live` applies to the provider; per-cache TTL via `RedisCacheManagerBuilderCustomizer` | 409-410 |
| 45 | `spring.data.mongodb.*` ignored with your own `MongoClientSettings` | your own `MongoClientSettings` is used unchanged and `spring.data.mongodb.*` is ignored | 348 |
| 46 | Redirects behind a TLS proxy come out with the wrong scheme/port (Tomcat) | `server.forward-headers-strategy` NATIVE is enough with `X-Forwarded-For`/`X-Forwarded-Proto`; with SSL terminated at the proxy set `server.tomcat.redirect-context-root=false` so `X-Forwarded-Proto` applies before redirects; either of the two `remoteip.*` properties turns on the valve | 580-582, 643 |
| 47 | PEM key `BEGIN RSA PRIVATE KEY` does not work in `server.ssl.certificate-private-key` | prefer PKCS#8; PKCS#1/SEC 1 convert with `openssl pkcs8 -topk8 -nocrypt -in <input> -out <output>` | 574 |
| 48 | HTTP/2 with TLS on Tomcat in JDK 8 logs an ALPN error | requires `libtcnative` and `-Djava.library.path`; without it the error is not fatal and HTTP/1.1 + SSL comes up; Jetty needs `http2-server` + one of the three ALPN | 574-575 |
| 49 | `/actuator/metrics/jvm.memory.max?tag=area:nonheap` returns a "strange" number | the value is the SUM of the matching meters: Code Cache + Compressed Class Space + Metaspace; for Metaspace only, add `&tag=id:Metaspace` | 517 |
| 50 | StatsD `max` statistics do not match the collector | `management.metrics.export.statsd.step` (default 1m) is the window for windowed statistics: align it with the scrape interval | 793 |
| 51 | I cited p.362 as the origin of the `contact-points` default | the body (p.362) only has an example and port 9042; the default `[127.0.0.1:9042]` is from Appendix A (p.682) | 362, 682 |
| 52 | `spring.ldap.urls` mandatory with embedded LDAP? | no: the embedded LDAP (UnboundID, "for testing purposes") starts on a random port and triggers the normal LDAP support | 369-370 |
| 53 | Custom Hikari datasource ignores `app.datasource.url` | with Hikari on the classpath the property is `jdbc-url`; or redefine `DataSourceProperties` under your prefix | 606-609 |
| 54 | `spring.jpa.properties.hibernate.jdbc.batchSize` has no effect | `spring.jpa.properties.*` has no relaxed binding: use the provider's exact name (`hibernate.jdbc.batch_size`) | 618 |
| 55 | Servlet filter registered via `@Bean` is not ordered | `@Order`/`Ordered` on the filter class (not on the `@Bean` method) or `FilterRegistrationBean#setOrder`; `logging.level.web=debug` shows the order | 276 |
| 56 | Spring Security + Actuator: own `SecurityFilterChain` and the rest of the app was left open | with any `SecurityFilterChain` Boot backs off completely: create a second bean for the rest | 448 |
| 57 | Build-info/git do not show up in `/info` | `build-info` needs the goal in `spring-boot-maven-plugin`; `git.properties` comes from `git-commit-id-plugin` (already pre-configured in starter-parent); `git.commit.time` in the format `yyyy-MM-dd'T'HH:mm:ssZ` | 467-468, 653-654 |
| 58 | `application.properties` filtered by Maven breaks Spring's `${...}` | without starter-parent set `@` as the delimiter and `useDefaultDelimiters=false`; the parent already switches the token | 561, 565 |
