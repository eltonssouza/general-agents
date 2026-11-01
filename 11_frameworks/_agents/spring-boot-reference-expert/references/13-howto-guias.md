# 13 — "How-to" Guides (ch. 17): task-based index

Pages = PDF (SBR p.N; printed = N−20). Version 2.7.18 [DATED]. The how-tos were folded into the thematic references; this table shows where the book answers each question and the page.

| Question | Where (SBR p.) | Reference |
|---|---|---|
| How do I create my `FailureAnalyzer`? | 556 | 01 |
| How do I see why auto-config switched on/off? | 556-557 (`--debug`, `-Ddebug`, `conditions` endpoint) | 00, 10 |
| How do I customize the `Environment` before startup? | 557-559 (`EnvironmentPostProcessor`, `spring.factories`) | 02 |
| How do I expand properties from the build? | 560-562 (Maven `@..@`, Gradle `expand`) | 02 |
| How do I externalize `SpringApplication`? | 562-565 (`spring.main.*`) | 01, 02 |
| How do I change where properties are located? | 565 (`spring.config.name/location`) | 02 |
| Short arguments (`--port`)? | 565 (`server.port=${port:8080}`) | 02 |
| Active/default profile; per-environment config | 566-568 | 03 |
| Switch the web server; disable the server | 569-571 | 05 |
| HTTP port, random port, discover the port | 571-572 | 05 |
| Compression, SSL, HTTP/2 | 572-575 | 05 |
| Servlet/Filter/Listener; access log; proxy | 577-582 | 05 |
| REST JSON/XML, `ObjectMapper`, multipart | 587-591 | 04, 05 |
| ViewResolvers | 592-593 | 05 |
| Jersey with Spring Security / another framework | 594-595 | 05 |
| Proxy in `RestTemplate`; Netty `WebClient` | 596-598 | 08 |
| Logback/Log4j2 | 598-603 | 03 |
| Custom DataSource and two DataSources | 603-615 | 07 |
| Repositories, `@EntityScan`, JPA, naming, L2 cache | 616-628 | 07 |
| Several `EntityManagerFactory`; `persistence.xml` | 622-626 | 07 |
| Database initialization (JPA, Hibernate, scripts, Batch, Flyway, Liquibase) | 628-635 | 07 |
| Jedis instead of Lettuce; non-transacted JMS | 635-636 | 07, 08 |
| Batch: DataSource, jobs at startup, args | 637-638 | 07 |
| Actuator: port, whitelabel, sanitization, health→metric | 638-641 | 10, 11 |
| Security: turn off default config, `UserDetailsService`, HTTPS behind a proxy | 642-644 | 06 |
| Hot swapping and templates | 644-645 | 00 |
| Tests: Spring Security, Testcontainers, slices | 646-652 | 04 |
| Build: build-info, git, versions, executable jar, classifier, requiresUnpack | 652-658 | 12 |
| War, convert an existing app, WebLogic | 659-667 | 09 |

## Sanitization of sensitive values (highlight)
- **[from source]** In the `env` and `configprops` endpoints, keys ending in `password`, `secret`, `key`, `token`, `vcap_services`, `sun.java.command` and keys containing `credentials` have the value masked (`******`); for keys ending in `address`, `addresses`, `uri`, `uris`, `url`, `urls` only the URI password is masked (SBR p.639).
- **[from source]** Customize: `management.endpoint.env.keys-to-sanitize` / `configprops.keys-to-sanitize` **replace** the defaults; `additional-keys-to-sanitize` **add to them**; or a `SanitizingFunction` bean (SBR p.639-640).
- **[from source]** Chain rule of the `SanitizingFunction` bean: `SanitizableData` gives access to the key, the value and the originating `PropertySource` (so everything from one source can be sanitized); each `SanitizingFunction` is called **in order, until one changes the value**; if none changes it, the built-in key-based sanitization runs. With two functions, the second only runs if the first does not change the value (SBR p.640).
- **[from source]** URI sanitization: for keys ending in `address`, `addresses`, `uri`, `uris`, `url`, `urls`, only the sensitive part `<scheme>://<user>:<password>@<host>:<port>/` is masked: `myclient.uri=http://user1:password1@localhost:8081` becomes `http://user1:******@localhost:8081` (SBR p.639). `keys-to-sanitize`/`additional-keys-to-sanitize` exist only for `env` and `configprops` (SBR p.639-640, Appendix A p.770); the `beans` endpoint has in Appendix A only `enabled` and `cache.time-to-live` (p.769), with no sanitization property [inference: absence verified on those pages].

## Spring Batch job arguments
- **[from source]** Command-line arguments starting with `--` become `Environment` properties and are **not** passed to the job; use the format without `--` (`someParameter=someValue`) (SBR p.638).

## Where the detail of each how-to went (round 4)
The page details of the how-tos were folded into the thematic references ("round 4" sections): 17.1-17.2 (FailureAnalyzer, auto-config diagnosis, `EnvironmentPostProcessor`, property expansion, `spring.main.*`, profiles) in `02` (SBR p.556-568); 17.3 and 17.4 (embedded server, SSL/PEM, HTTP/2, proxy, access log, cookies, JSON/XML, multipart, view resolvers) in `05` (SBR p.569-598); 17.7 (logging) in `03` (SBR p.598-603); 17.8-17.12 (data, database initialization, Flyway/Liquibase, Redis/Jedis, JMS, Batch) in `07` (SBR p.603-638); 17.13 (Actuator) in `10` and `11` (SBR p.638-641); 17.15-17.16 (hot swap, tests) in `00`, `04` and `07` (SBR p.644-652); 17.17 (build-info, git, versions, jar) in `12` (SBR p.652-658); 17.18 (war) in `09` (SBR p.659-667).
