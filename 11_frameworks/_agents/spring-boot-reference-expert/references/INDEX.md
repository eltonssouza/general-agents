# INDEX — Spring Boot Reference Documentation 2.7.18 (SBR)

## 1. What the source is (identification)
- **Title:** *Spring Boot Reference Documentation*, **Version 2.7.18**, authors listed on the cover (Phillip Webb, Dave Syer, Josh Long, Stéphane Nicoll and others; SBR p.1). Copyright **2012-2023** (SBR p.22). Official reference document as an 882-page PDF (~1.47 million characters), native text (not OCR).
- **Exact version:** Spring Boot **2.7.18**. The text states: requires **Java 8** and is compatible up to and including **Java 21**; requires Spring Framework **5.3.31+** (SBR p.27). Maven 3.5+ and Gradle 6.8.x/6.9.x/7.x/8.x (SBR p.27); Tomcat 9.0, Jetty 9.4/10.0, Undertow 2.0 (SBR p.27-28).
- **Dates:** the copyright header runs to 2023 and the example logs carry November 2023 dates (e.g. SBR p.69, 72). All content is **[DATED] relative to this version/edition**; later Spring Boot versions are not covered.
- **Acronym:** SBR. **Language of the sources:** English; the references in this package are in English (paraphrase).

## 2. Page convention (used in the WHOLE package)
- **"SBR p.N" = PDF page number** (the `=== PAGE N ===` marker of the extracted text).
- **Printed number = N − 20** for N ≥ 21 (e.g. "Getting Started" is printed page 7 = PDF p.27; Appendix B starts on printed 779 = PDF p.799). Pages 1-20 are the cover and table of contents (no useful printed number).
- The scripts always show the PDF page and, when useful, the printed one.

## 3. Reading coverage (honest statement)
- **Read in full (text):** PDF p.1-667 (cover, table of contents, chs. 1 to 17: Getting Started through How-to), in sequential blocks, with notes saved to disk (`scratch/frameworks/spring-boot-reference-expert/notes/`). For reading, the duplicated Kotlin blocks and `import` lines were filtered (the Java equivalent was read); pages with only Kotlin code appear empty in the filtered version. Some PDF pages have partial text in the extraction itself (truncated code listings); the claims use only what the text carries.
- **Read in full:** Appendix B (metadata, p.799-820) and Appendix E (executable jar, p.837-843).
- **Processed by script (not read line by line):** Appendix A (common properties, p.668-799; Name/Description/Default table read by column position with PyMuPDF), Appendix C (auto-configuration classes, p.820-827), Appendix D (test slices, p.828-837) and Appendix F (managed versions, p.843-876). This produced `scripts/sbr_index.json` (1,679 Appendix A keys; ~1,156 dependency coordinates).
- **Not visually verified:** no page was rendered as an image for inspection; the column structure of the appendix tables was checked by word coordinates. The PDF contains no raster image (count per page = 0; only decoration/table vectors), so there is no figure whose content escapes the text.
- **Limits of the source:** the PDF cuts at least one Appendix A cell at the page break (key `spring.datasource.dbcp2.max-wait-...` on p.688: the suffix is not in the text) and has small internal inconsistencies (see `datado.md`).
- **Blind test:** there were three independent rounds (rounds 1, 2 and 3); the coverage defects pointed out in each were fixed and are in the trail of `tests/relatorio-de-fidelidade.md` (§6, §7 and §8). Round 2 produced the **term index** (`scripts/sbr_terms.json`, §7 below); round 3 (cases drawn by page) showed omissions of **details on a page** and produced round 4's systematic sweep (SSL/TLS/PEM and HTTP/2, proxy, embedded server, Actuator in detail, logging, data and build how-tos, deploy, Appendix A.1-A.4/A.11/A.14, Appendix B).
- **Detail reading (round 4):** besides the reading of chs. 1-17, the pages with the highest density of details (how-to 556-667, Actuator 440-477, logging 137-146, deploy 524-540, Appendix B 799-820 and tables A.1, A.11 and A.14) were reread against the `references/`; each omitted detail became a paraphrase with a page ("round 4" sections at the end of each topical file).

## 4. Map of chapters → pages → reference file
| Ch. | Title (from the book) | SBR p. (PDF) | Reference |
|---|---|---|---|
| 1-3 | Legal, Getting Help, Documentation Overview | 22-26 | 00-visao-geral-e-versao.md |
| 4 | Getting Started (intro, requirements, installation, 1st app, jar) | 27-39 | 00-visao-geral-e-versao.md |
| 5 | Upgrading Spring Boot | 40-41 | 00-visao-geral-e-versao.md |
| 6 | Developing with Spring Boot (build, starters, structure, auto-config, devtools) | 42-70 | 00-visao-geral-e-versao.md |
| 7.1 | SpringApplication (banner, lazy, events, runners, exit) | 71-87 | 01-springapplication-e-ciclo-de-vida.md |
| 7.2 | Externalized Configuration | 87-133 | 02-configuracao-externalizada.md |
| 7.3-7.6 | Profiles, Logging, i18n, AOP | 133-147 | 03-profiles-e-logging.md |
| 7.7-7.12 | JSON, tasks, Testing, custom auto-config/starter, Kotlin | 147-248 | 04-json-tarefas-testes-autoconfig.md |
| 8.1-8.3 | Web servlet, WebFlux, graceful shutdown | 249-301 | 05-web-servlet-e-reativo.md |
| 8.4-8.7 | Security, Session, GraphQL, HATEOAS | 301-322 | 06-seguranca-session-graphql.md |
| 9 | Data (SQL and NoSQL) | 323-371 | 07-dados-sql-e-nosql.md |
| 10-11 | Messaging and IO (cache, Quartz, mail, REST clients, JTA) | 372-435 | 08-mensageria-e-io.md |
| 12, 14 | Container Images; Deploying | 436-439, 524-540 | 09-imagens-de-conteiner-e-deploy.md |
| 13.1-13.5 | Actuator: endpoints, health, info, HTTP/JMX, loggers | 440-477 | 10-actuator-endpoints-saude-info.md |
| 13.6-13.11 | Metrics, auditing, tracing, cloud foundry | 477-523 | 11-metricas-e-observabilidade.md |
| 15-16 | Spring Boot CLI; Build Tool Plugins | 541-555 | 12-cli-e-build-plugins.md |
| 17 | How-to Guides | 556-667 | 13-howto-guias.md |
| Appendices | A properties, B metadata, C/D auto-config/slices, E executable jar, F versions | 668-876 | 14-apendices-propriedades-e-versoes.md (+ E in 12) |

Full navigable listing: `python -I scripts/sbr_lookup.py --chapters` and `--toc 7.2`.

## 5. Cross-cutting files
- `glossario.md` terms and acronyms; `procedimentos.md` steps P1-P10 (what to do in each typical task); `casos-e-antipadroes.md` symptom-cause-source pairs; `datado.md` dated items and PDF inconsistencies.

## 6. Scripts (all stdlib, no network, `python -I`)
| Script | Function |
|---|---|
| `scripts/sbr_lookup.py` | search by topic, property (`--prop`: Appendix A page, **default with the appendix page**, body page and paraphrased description when curated), managed dependency (`--dep`), page (`--page`: separates the title at the TOP of the page from the titles that START on it), table of contents, gaps (`--gaps`); answer on three levels (COVERED / POINTER ONLY / NOT COVERED) using `sbr_terms.json` and `sbr_curated.json` |
| `scripts/build_cover_index.py` | generates `scripts/sbr_cover.json` (tokens per line of the `references/` summaries, except this INDEX); it is the only index that decides COVERED; `--check` verifies it is up to date |
| `scripts/build_term_index.py` | generates `scripts/sbr_terms.json` (index of words/pairs and pages of the Reference text; no prose) — maintenance, requires only the extracted text (`--src`) |
| `scripts/sbr_propcheck.py` | static validator of application.properties/yml against the documented keys; rules backed by the text; missing key = "unknown", not an error |
| `scripts/sbr_checklist.py` | production/configuration checklist with page citation; manual items |
| `scripts/sbr_actuator.py` | Actuator endpoint map, web/JMX exposure, paths, health HTTP status |
| `scripts/sbr_precedence.py` | precedence of configuration sources, file order, conversion to environment variable |
| `scripts/build_index.py` | rebuilds `sbr_index.json` from the text/PDF (maintenance only; requires PyMuPDF and the PDF) |
| `tests/verify_citations.py`, `tests/audit_tokens.py`, `tests/run_script_tests.py` | verify the citations (range, positive/negative content, terms between backticks) and the scripts |

## 7. Coverage map (three levels; round 2)
Levels used by `scripts/sbr_lookup.py` and by this map: **COVERED** (round 5 rule) = a summary with a page in `references/` treats the term, as a whole term or contiguous phrase in the body of the summary (index `scripts/sbr_cover.json`; a structured entry from the table of contents/Appendix A/F alone gives POINTER ONLY and `--prop`/`--dep` give key, default and page); **POINTER ONLY** = the Reference has the subject (or mentions it), but the package only indicates the page, without summarizing; **NOT COVERED** = the Reference does not carry it (0 occurrences in the term index `scripts/sbr_terms.json`, generated by `scripts/build_term_index.py` from the text, or a subject from the curated outside list `scripts/sbr_curated.json`). "The Reference does not carry X" is only allowed at this third level.

| Subject (Reference 2.7.18) | Level | Where / pages |
|---|---|---|
| Externalized configuration, profiles, logging, SpringApplication | COVERED | 01, 02, 03 (p.71-146) |
| Boot tests: `@SpringBootTest`, MockMvc, `@MockBean`, utilities | COVERED | 04 (p.154-171, 223-228) |
| Slices: `@DataJpaTest`, `@JdbcTest`, `@DataJdbcTest`, `@DataR2dbcTest`, `@JooqTest`, `@DataMongoTest`, `@DataNeo4jTest`, `@DataRedisTest`, `@DataLdapTest`, `@JsonTest`, `@WebMvcTest`, `@WebFluxTest`, `@GraphQlTest`, `@RestClientTest`, `@WebService*Test` | COVERED (round 2) | 04 §"Test slices: details per annotation" (p.172-223) |
| Spring REST Docs (`@AutoConfigureRestDocs`), Spock | POINTER ONLY (one line) | 04 (p.203-214, 223) |
| Web MVC, Jersey, embedded containers, WebFlux, graceful shutdown | COVERED | 05 (p.249-301, 569-598) |
| Declarative SSL/TLS, PEM (PKCS#8 vs PKCS#1, `openssl pkcs8`), HTTP/2 (h2/h2c per server: Tomcat/libtcnative, Jetty `http2-server` + ALPN, Netty, Undertow), multiple connectors | COVERED (round 4) | 05 §"HTTP/2, TLS and PEM" (p.573-575, 582, 585) |
| Behind a proxy: NATIVE vs FRAMEWORK vs NONE, `redirect-context-root`, `remoteip.*` (either turns on the valve), default of `internal-proxies` | COVERED (round 4) | 05 §"Behind a proxy: step by step" and A.11 (p.580-582, 643-644, 763-764) |
| Embedded server: customizers, servlet/filter registration, SameSite, access log, legacy cookies, JSP, Jersey, JSON/XML, view resolvers, Jackson, multipart | COVERED (round 4) | 05 (p.272-282, 576-598) |
| Appendix A.11 (server.*) and A.1-A.4 (core, cache, mail) with defaults and meaning | COVERED (round 4) | 05 and 14 (p.668-679, 754-767) |
| Security (defaults, OAuth2, SAML), Session, GraphQL, HATEOAS | COVERED; fine-grained authorization/hardening POINTER ONLY | 06 (p.301-322) |
| DataSource/pools (Hikari, Tomcat, DBCP2, UCP), JPA, JDBC, jOOQ, R2DBC | COVERED (round 2) | 07 (p.323-344, 617-634) |
| NoSQL: Redis, MongoDB, Neo4j, Elasticsearch, Cassandra, Couchbase, LDAP, InfluxDB | COVERED; Geode, Solr in depth: POINTER ONLY | 07 (p.344-371) |
| Embedded LDAP (embedded in-memory LDAP, UnboundID: tests only, random port, no `spring.ldap.urls`, `schema.ldif`, validation) | COVERED (round 4; previously listed as POINTER ONLY in the lookup) | 07 §"LDAP and in-memory LDAP server" (p.368-370) |
| Data how-tos in detail: custom DataSource (`jdbc-url` vs Hikari), two DataSources, several `EntityManagerFactory`, naming, L2 cache, `import.sql`, per-platform scripts, Flyway/Liquibase (callbacks, test data), initialization detectors | COVERED (round 4) | 07 §"Round 4 additions" (p.603-638) |
| Messaging: JMS, RabbitMQ (incl. `spring.rabbitmq.listener.*`, retries, redelivery), Kafka (incl. `spring.kafka.listener.*`, embedded), RSocket, Integration, WebSocket | COVERED (round 2) | 08 (p.372-401, 713-737) |
| Rabbit DLX/DLQ (declaration), Kafka listener retry/DLT, offset semantics | POINTER ONLY (p.388, 724) | `sbr_lookup.py dead letter` |
| Cache (per provider), Hazelcast, Quartz, email, validation, REST clients, Web Services, JTA | COVERED (round 2) | 08 §"IO additions" (p.402-435) |
| Images (Dockerfile, layertools, buildpacks), deploy (cloud, systemd, init.d, war) | COVERED; build-image plugin command: NOT COVERED (0 occurrences) | 09 (p.436-439, 524-540, 659-667); platform details and launch script in round 4 |
| Actuator: endpoints, health, probes, info, HTTP/JMX, loggers | COVERED | 10 (p.440-477) |
| Actuator in detail: security with `EndpointRequest`, custom endpoints (entry, predicates, status), reactive health/groups/`additional-path`, probes table, info/git, JMX/Jolokia | COVERED (round 4) | 10 §"Round 4 additions" (p.441-477) |
| Micrometer metrics: Prometheus (scrape_config, exemplars, Pushgateway), exporters, meters | COVERED (round 2) | 11 (p.477-523) |
| `metrics` endpoint (sum of the matching meters; `area:nonheap`; `id:Metaspace`) and Appendix A.14 properties (step, batch-size, StatsD, Stackdriver, Prometheus, health, CORS) | COVERED (round 4) | 11 §"Round 4" (p.517, 769-798) |
| Grafana, PromQL, Prometheus service discovery | NOT COVERED | 0 occurrences of Grafana |
| Devtools (packaging, restart, LiveReload, remote, defaults) | COVERED (round 2) | 00 §5 (p.58-70) |
| CLI, Maven/Gradle/Ant plugins, executable jar | COVERED; detailed plugin usage: POINTER ONLY (the text refers to another document, p.550) | 12 |
| `build-info`, `git.properties` (starter-parent already preconfigures the Git plugin), overriding managed versions, Ant `findmainclass`, `Repackager` | COVERED (round 4) | 12 (p.468, 551-554, 652-655) |
| Appendices A, C, D, F | COVERED by script-generated index (name, page, default, section); description paraphrased for ~95 keys and A.1-A.4/A.11/A.14 in prose | `sbr_lookup.py --prop/--dep`; 14 |
| Appendix B (metadata: groups, properties, deprecation, hints, providers, annotation processor) | COVERED (round 4) | 14 §"Round 4 additions" (p.799-820) |
| Logging in detail (`%clr` colors, file table, Logback rotation, groups, Logback extensions, includes, Log4j2) | COVERED (round 4) | 03 (p.137-146, 598-603) |
| `circuit breaker`, Sleuth, Zipkin, ZooKeeper | POINTER ONLY (passing mention) | `sbr_lookup.py circuit breaker` (p.464) |
| GraalVM/native image/AOT, Boot 3.x/Jakarta/Java 17, Observation/OpenTelemetry, Resilience4j, virtual threads, Docker Compose/`@ServiceConnection`, SSL bundles, OpenAPI, gRPC, KRaft | NOT COVERED | curated list (`sbr_lookup.py --gaps`) |

## 8. Scope: the JavaCodeGeeks guide (Spring Boot 3) is OUTSIDE this collection
- This package covers **only** the *Spring Boot Reference Documentation 2.7.18*. The practical **"Spring Boot 3" guide from JavaCodeGeeks** (Docker Compose, Kafka with KRaft, Prometheus/Grafana, `bootBuildImage`, Java 17/Jakarta EE 10, Resilience4j/conceptual circuit breaker etc.), **Quarkus** and **MapStruct** belong to the agent **java-backend-frameworks-expert**. A question whose answer depends only on that guide: NOT COVERED here and redirected to that agent; what the Reference 2.7.18 states about the same subject remains in scope (e.g. Prometheus `scrape_config`, p.494; `NewTopic`, p.389).
