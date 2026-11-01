# Fidelity report — spring-boot-reference-expert

Source: *Spring Boot Reference Documentation*, Version 2.7.18 (SBR), 882 PDF pages. Convention: **"SBR p.N" = PDF page; printed = N−20**.

## 1. What was read (precise statement)
- **In full (text):** PDF p.1-667 (cover, table of contents and chapters 1-17), in sequential blocks, with notes recorded in `scratch/frameworks/spring-boot-reference-expert/notes/` (n01...n13). During reading, duplicated Kotlin blocks and `import` lines were filtered out (the equivalent Java code was read); pages with only Kotlin were left blank in the filtered version.
- **In full:** Appendix B (p.799-820) and E (p.837-843).
- **By script (not read line by line):** Appendix A (p.668-799), C (p.820-827), D (p.828-837) and F (p.843-876), via PyMuPDF by column position.
- **Not done:** no page was rendered as an image for visual inspection (the PDF has no raster images; count = 0). The column layout of the appendices was checked by coordinates.
- **Independent test:** there were **three blind rounds** with an evaluator independent of the solver (rounds 1, 2 and 3; see §6, §7 and §8). The 60 cases in `casos-de-teste.md` were written/evaluated by the package author (that alone is not independent validation).
- **Round 4 note:** "read in full" did not mean "every page converted into content": round 3 (cases drawn by page) found page details that the `references/` omitted. Round 4 re-read, against the references, the pages with the highest density of details (how-to 556-667, Actuator 440-477, logging 137-146, deploy 524-540, Appendix B and the tables A.1, A.11, A.14) and converted the omissions into paraphrase with a page (§8).

## 2. Automatic checks (run: `python -I tests/run_script_tests.py --src <folder>`)
| Check | Result |
|---|---|
| `verify_citations.py`: page range (1-882) of the `SBR p.N` citations (~1,930) and loose `p.N` in the references (~1,725) | 0 failures |
| `verify_citations.py`: **288 positive checks** (114 original + 20 from round 1 + 52 from round 2 + 102 from round 4) (key terms present on the cited page) and **49 negative** (22 original + 7 from round 1 + 9 from round 2 + 11 from round 4) (plausible claims that the book does NOT carry: GraalVM, native image, Spring Boot 3, OpenTelemetry, Micrometer Tracing/Observation, Docker Compose, `@ServiceConnection`, virtual threads, OpenAPI/Swagger, gRPC, KRaft, Resilience4j, Grafana, `@Rollback`/`@Commit`, build-image...) | 0 failures |
| `audit_tokens.py`: 3,526 backticked terms (2,041 up to round 2) in the references checked against the cited page(s), with `--strict` (accepts 0 neighboring pages) | 0 failures, 0 "near" |
| `run_script_tests.py`: 125 checks (67 up to round 1; +26 from round 2: three-level lookup, reproducible term index, Prometheus in `sbr_actuator.py`, M08; +32 from round 4: `--page`, `--prop` with description, lookup levels, Appendix A sections; with `--src`) | 125/125 |

## 3. Errors found and fixed during the work (quality trail)
1. **Printed pages used as PDF pages** in `08-mensageria-e-io.md` (cache, Hazelcast, Quartz, mail, validation, REST clients, JTA had citations with the printed number from the table of contents). Detected by `audit_tokens.py`; fixed to PDF (e.g. Quartz p.415-417, not 395-397). Citations of TestRestTemplate (p.226-229), `customizerBuilder` (p.663-664) and Appendix C components (p.820-825/825-827) were also fixed.
2. **Reading filter that discarded prose** (Kotlin blocks): the first version of the filter erased paragraphs; it was rewritten and the affected pages of the p.160-231 stretch were re-read with the fixed filter.
3. **Appendix A index:** extraction by lines broke keys in the middle; replaced by column reading (PyMuPDF) and checked by sampling. One cell of the PDF itself is truncated (`spring.datasource.dbcp2.max-wait-`, p.688): the key is dropped from the index instead of being completed.
4. **Prefix keys mentioned in the body** (e.g. `spring.datasource.*`) made any key look "known"; now only Appendix A wildcards and curated dynamic prefixes count, and templates such as `management.endpoint.<id>.enabled` match by segment.

## 4. Evaluation of the cases in `casos-de-teste.md` (40 cases)
- **Verified by script/deterministic check:** 2-6, 8, 10, 12, 14-16, 18, 26, 28, 29 (partially), 38-40.
- **Evaluated against references + agent (reading):** 1, 7, 9, 11, 13, 17, 19-25, 27, 30-37. In all of them the expected behavior is in the agent prompt (§2 boundaries, §7 labels, §9 injection) and in the cited references.
- **Result:** 40/40 conform to what the author himself expected. This is **not** independent validation.

## 5. Known limitations and risks
- Defaults only exist for keys whose Appendix A row carried a value (840 of 1,679 keys have no default in the table or it is not extractable); the agent must say "not shown in the table".
- The rules of `sbr_propcheck.py`/`sbr_checklist.py` cover what the text supports; several production recommendations are labeled **[inference]**. They do not replace a security/operations review.
- The script's YAML reader is a subset (maps, lists, `---`, simple flow lists); anchors and complex multi-line blocks may not be interpreted (INFO warning `P00`).
- Pages with code only in Kotlin were not read in Kotlin (the Java equivalent was); Kotlin-specific claims only come from SBR p.245-248.
- The PDF text has internal inconsistencies (e.g. Maven 3.5/3.3/3.2; `generate-unique-name`), documented in `references/datado.md`.
- Everything is **[DATED]** to 2.7.18 (2023): Spring Boot 3.x, Jakarta, native image and modern observability are NOT COVERED.

## 6. Post-blind-test fixes (round 1)
Origin: blind test of 14 cases with an evaluator independent of the solver (provisional grade reached: F 2.93; L 2.71; R 2.93; S 3.00; 74/77 citations OK, 3 overstatements). The 8 defects attributed to the package were **checked page by page in the source** (SBR 2.7.18) and fixed (8/8). Backup of the previous state in `scratch/blind/backups_round1/spring-boot-reference-expert/`.

| # | Defect confirmed in the source | Fix |
|---|---|---|
| 1 | `webEnvironment` listed without semantics (p.156) | `references/04`: definitions of MOCK/RANDOM_PORT/DEFINED_PORT/NONE (p.156), management on a random port and reactive type (p.157) |
| 2 | M12 "p.76-78" (they were **printed** pages; PDF = p.96-98) and C51 "p.76-77"; configtree/Docker secrets = p.96-98, p.101 only carries "no native encryption" + Vault | `sbr_checklist.py` M12 -> "p.96-98, 101"; C51 -> "p.96-98, 101, 639" and the message cites p.97-98 for configtree; `references/02` and agent §4 also cite them |
| 3 | C51 labeled as [inference] the masking of `env`/`configprops`, stated on p.639 | label [from source] (SBR p.639) in the C51 message; `references/02` |
| 4 | M13 (proxy) "p.560-561" (property expansion at build); proxy = 17.3.12, p.580-582 | M13 -> "p.580-582" |
| 5 | No probes manifest (p.463) nor `preStop` (p.528); `sbr_lookup.py preStop` empty | excerpts in `references/10` (probes) and `references/09` (preStop/terminationGracePeriodSeconds); index: `preStop`, `terminationGracePeriodSeconds`, `livenessProbe`, `readinessProbe`, `startupProbe`, `httpGet`, `configtree`, `/run/secrets`, `org.springframework.boot.context.config` (also in `build_index.py` -> `EXTRA_IDS`, to survive a rebuild) |
| 6 | No trace of `org.springframework.boot.context.config` (p.565) | `references/02` §1 and `procedimentos.md` P6 |
| 7 | `sbr_precedence.py` rejected `cmdline`, `jar-config-data` etc. | new aliases for sources and for the 4 config data types; `winner` indicates the winner among files when several appear |
| 8 | P01 of `sbr_propcheck.py` depends on the file name (`application-<profile>.*`) or on `on-profile` | `--as-profile NAME`; the output carries a NOTE when `spring.profiles.active/default/include` appears in a file treated as non-profile; docstring updated |
| D12 | [inference] "JSON/ECS via Log4j2" without backing (YAML/JSON on p.602-603 is a **configuration file** format; the text has no "Elastic Common Schema"/Logstash) | `references/03`: explicit note + NOT COVERED for structured output logging; negative check |

**Extras of the same kind (page errors found and fixed in `sbr_checklist.py`)**: C61 "p.562" (printed) -> p.581-582; C65 "p.571" (printed) -> p.591; C64 "p.418" -> p.418-419 (the example timeouts are on p.419); C33 "p.60, 243" -> p.60 (p.243 does not deal with `include-*`); C04 "p.451, 463" -> p.463, 471 (p.451 does not deal with the management port); C11 without the 30s default -> added appendix A p.672.

**Counts after round 1**: `verify_citations.py` 134 positive / 29 negative / 0 failures; `audit_tokens.py` 1,246 terms, 0 failures, 0 near; `run_script_tests.py` 67/67.

**Not fixed / outside the package**: points of C08/C09 that depend on the JavaCodeGeeks guide (p.22, p.191-193) belong to the java-backend-frameworks-expert agent; "3.2+ requires Java 21" (C11) and the hedge in C05 were solver defects (C05 follows from item 1, already fixed).

**Status**: these fixes were made and checked by the package author. The **independent validation is round 2** (a new blind test with new cases, including the fixed topics); until then, the notes above do not count as a new approval.

## 7. Post-blind-test fixes (round 2)
Origin: `scratch/blind/runs2/spring-boot-reference-expert/avaliacao.md` (evaluator C; 14 new cases; raw F 2.43 / in-scope F 2.93; L 2.79; R 2.93; S 3.00; 68/72 citations OK = 94.4%, 0 wrong page, 4 overstatements). Provisional approval reached; the 7 defects attributed to the package (omissions of the same kind: facts that the Reference states and the `references/` did not carry) were **checked page by page in the source** (SBR 2.7.18) and fixed (7/7). Backup of the previous state (package and `_agents_tests`) in `scratch/blind/backups_round2/spring-boot-reference-expert/`. This round fixes the **package's coverage**, not the performance on the 14 cases (the cases' answer key was not used).

| # | Defect confirmed in the source | Fix |
|---|---|---|
| D1 | `references/04` only said `@DataJpaTest`/`@JdbcTest` are transactional (SBR p.173-195) | section "Test slices: details per annotation": embedded database and SQL logs (p.190); `@Component`/`@ConfigurationProperties` not scanned and `@EnableConfigurationProperties` (p.190); `Propagation.NOT_SUPPORTED` (p.190-191); `TestEntityManager`, `JdbcTemplate` and `@AutoConfigureTestEntityManager` (p.191); `Replace.NONE` (p.193); note: Spring Test Rollback/Commit = 0 occurrences ([extrapolation]); the Reference's Testcontainers is Neo4j, not Postgres (p.647-649) |
| D2 | `references/08` omitted the text of p.388 (retries off; default recoverer; DLX "if the broker is configured"; `RabbitRetryTemplateCustomizer`) | bullets "Listener retries and redelivery" and Appendix A of `spring.rabbitmq.listener.simple.*`/`direct.*`/`template.retry.*` (p.733-737) and Kafka (`spring.kafka.listener.*`, consumer, embedded) |
| D3 | `references/11` and `sbr_actuator.py` without the Prometheus passage of p.494 | `scrape_configs`/`job_name`/`metrics_path`/`targets`; "by default the endpoint is not available"; exemplars (`SpanContextSupplier`, OpenMetrics); Pushgateway (`simpleclient_pushgateway`, `management.metrics.export.prometheus.pushgateway.enabled`); `sbr_actuator.py show prometheus` updated; exporters and meters in detail (p.477-523) |
| D4 | `references/07` omitted from p.326: Hikari via the jdbc/data-jpa starters; `spring.datasource.type` in a Tomcat container (`tomcat-jdbc`); the `DataSourceBuilder` list | bullet "Pool choice" (p.325-326), Tomcat pool example, loadable driver, JNDI, `NamedParameterJdbcTemplate`; [inference] labeled for a WAR on an external Tomcat |
| D5 | "Reactor Netty (default)" anchored on p.297-300 | p.297 lists the servers and port 8080; the "default" is on p.428, 569, 575 and 659 (positive checks) |
| D6 | `sbr_lookup.py "circuit breaker"` answered NOT COVERED | term index + curated list: **POINTER ONLY**, passing mention on p.464, without Resilience4j or configuration; `references/10` |
| D7 | `references/00` omitted p.59 (repackaged jar without devtools; `excludeDevtools=false`/`developmentOnly`) and M08 only cited p.50, 59 | `references/00` §5 (packaging and devtools details p.59-70); M08: "p.59, 68" |

**WRONG ANSWER KEY / scope (recorded, no content change):** (a) the `spring.rabbitmq.listener.simple.*` keys exist (p.733-735): they are now in the references; (b) internal Security x Actuator divergence (p.302 x p.446-448) now recorded in `references/06`; (c) "Resilience" appears as a generic word in the text; only "Resilience4j" is NOT COVERED (the lookup tells them apart). **Declared scope:** the JavaCodeGeeks guide (Spring Boot 3) is **outside** this collection and belongs to *java-backend-frameworks-expert*; declared in the README, INDEX §8, prompt, `AGENTS.md` and the Copilot adapter.

**Sweep for omissions of the same class (topics added with pages):**

| Topic | Where | Pages |
|---|---|---|
| Test slices (JPA, JDBC, Data JDBC/R2DBC, jOOQ, Mongo, Neo4j, Redis, LDAP, Cassandra, Couchbase, Elasticsearch, JSON, WebMvc, WebFlux, GraphQL, RestClient, WebService, REST Docs, `@ImportAutoConfiguration`, user configuration and slices, Spock) | `references/04` | 172-223 |
| DataSource/pools, JNDI, JPA (Envers, `ddl-auto`, bootstrap), Spring Data JDBC, jOOQ, R2DBC, Redis, Mongo (embedded), Neo4j, Elasticsearch, Cassandra, Couchbase, LDAP, InfluxDB | `references/07` | 323-371 |
| RabbitMQ (retries, redelivery, `listener.*`, streams, configurers), Kafka (container, Streams, extra properties, embedded), JMS (ActiveMQ, Artemis, JNDI, `@JmsListener`) | `references/08` | 372-396, 713-737 |
| Cache per provider, Hazelcast, Quartz, mail, validation, `RestTemplate`/`WebClient`, Web Services, RSocket, Integration, JTA | `references/08` | 396-435 |
| Prometheus, exporters (Dynatrace, New Relic, Datadog, ...), meters (HTTP, cache, GraphQL, DataSource, Hibernate, Mongo, Jetty...), tags, filters | `references/11` | 477-523 |
| Devtools (packaging, restart, LiveReload, global, remote, defaults) | `references/00` | 58-70 |
| WebFlux (formats, codecs, static, errors, filters, server), default Netty | `references/05` | 283-300, 428, 569, 575, 659 |
| Security (defaults, turning pieces off, WebFlux), Session, GraphQL (RouterFunction, WebInterceptor, CORS, RSocket) | `references/06` | 301-321 |
| Images: `ENTRYPOINT`, layertools, what the Reference does NOT carry about buildpacks (no build-image) | `references/09` | 436-439, 524, 550 |
| 10 new cases/anti-patterns (#36-#45) | `references/casos-e-antipadroes.md` | 59, 68, 175, 182, 190-193, 326, 348, 388, 409-410, 494 |

**`sbr_lookup.py` on three levels:** it only says "the Reference does not cover it" for terms in the curated out-of-scope list (`scripts/sbr_curated.json`) or with no occurrence in the term index generated from the text (`scripts/sbr_terms.json`, by `scripts/build_term_index.py`: 15,328 words and 64,642 pairs with pages, no prose; reproducible byte for byte, verified in `run_script_tests.py`). Output: **COVERED** (rc 0), **POINTER ONLY** (rc 3), **NOT COVERED** (rc 2). A term with a summary in the references but no occurrence in the text (e.g. a note saying "0 occurrences") is not COVERED.

**Counts after round 2**: `verify_citations.py` 186 positive / 38 negative / 0 failures; `audit_tokens.py` 2,041 terms, 0 failures, 0 near; `run_script_tests.py` 93/93.

**Still pointer only (the Reference has it, the package does not summarize it):** Spring REST Docs in detail (p.203-214), Spock (p.223), Apache Geode/GemFire (p.314, 344-345, 404), DLX/DLQ declaration in Rabbit and Kafka listener retry/DLT (p.388, 390), `auto-offset-reset` semantics (p.724), passing mentions of circuit breaker, Sleuth, Zipkin and ZooKeeper (p.464, 494, 518, 96), detailed use of the Maven/Gradle plugins (the text refers to another document, p.550) and the per-driver properties of Appendix A (reachable only via `sbr_lookup.py --prop`: name, page and default when the table carries it). Not covered: Grafana/PromQL, build-image/`bootBuildImage`, Docker Compose, KRaft, Resilience4j, Observation/OpenTelemetry, GraalVM/native image, Boot 3.

**Status**: fixes made and checked by the package author; independent validation of the new coverage requires a **round 3** with new cases (the 14 cases of round 2 are "burned").

## 8. Post-blind-test fixes (round 3)
Origin: `scratch/blind/runs3/spring-boot-reference-expert/avaliacao.md` (evaluator C; 14 new cases on drawn pages; F 2.50; L 2.93; R 2.93; S 3.00; 75/76 citations OK = 98.7%, 0 wrong page, 1 overstatement; 7 package defects, 3 serious, all about depth: the Reference states it and the package only pointed to it or omitted it). **No factually wrong answer came from the package.** The defects were checked page by page in the text (`Spring-Boot-Reference.txt`, 2.7.18) before fixing.

| # | Defect confirmed in the source | Fix |
|---|---|---|
| D1 (serious, C05) | p.517: the value of the `metrics` endpoint is the SUM of the matching meters; `area:nonheap` = Code Cache + Compressed Class Space + Metaspace; `&tag=id:Metaspace`; the package only said "use the name in the code" and `--page 517` labeled the page as "13.7 Auditing" | `references/11` (endpoint + "Round 4" section), `sbr_actuator.py show metrics`, 5 positive checks p.517. **Page→title map:** the table of contents only records the START page of each title and `--page` inherited the last title started up to the page (13.7 starts in the middle of p.517, after 13.6.6); now `--page` separates "in progress at the TOP" from "titles that START on this page" (checked on 30 random pages, seed 7: 0 divergences). **Second place with the same error:** the Appendix A section (`secao` in `sbr_index.json`) was assigned by the whole page; 87 keys were in the wrong section (e.g. `spring.rsocket.*` in A.14 instead of A.13, `spring.mail.*` in A.4 instead of A.3, `spring.thymeleaf.*` in A.11 instead of A.10); recomputed by the key's position on the page (and `build_index.py` fixed to the same rule); the key `spring.devtools.restart.trigger-file` (p.799) was missing from the index's Appendix A and was fixed |
| D2 (serious, C13) | p.573-575: PKCS#8 x PKCS#1 and `openssl pkcs8 -topk8 -nocrypt`; Tomcat on JDK 8 with `libtcnative`; Jetty `http2-server` + one of the three ALPN; Reactor Netty and Undertow | `references/05` section "HTTP/2, TLS and PEM" (+ HTTP and HTTPS together, several connectors); lookup becomes COVERED for PKCS#1, openssl, libtcnative, ALPN, `http2-server`; 10 positive checks p.573-575, 582, 585 |
| D3 (serious, C08d) | p.792-793: `batch-size` (measurements per request) and `statsd.step` (align to the scrape); the index only kept key+default | `references/11` (A.14 in prose with appendix and body page), `references/05` (A.11), `references/14` (A.1-A.4, A.15-A.16); `sbr_curated.json` gained `descricoes` (94 keys, paraphrase + appendix page + body page) and `sbr_lookup.py --prop` prints the default with the **appendix** page, the body page and the description (or warns that the package keeps only key+default and says to read the appendix) |
| D4 (medium, C03) | p.580-582, 643: NATIVE x FRAMEWORK, `server.tomcat.redirect-context-root=false`, either of the two `remoteip.*` turns the valve on, default of `internal-proxies` (p.764) | `references/05` section "Behind a proxy: step by step" and A.11; the old lines point to it; anti-pattern #46; checks p.580-582, 643-644, 763-764 |
| D5 (medium, C04) | `sbr_lookup.py "embedded ldap"` gave POINTER ONLY although `references/07` summarized LDAP in Portuguese ("LDAP embutido") | level becomes COVERED: section "LDAP and in-memory LDAP server (embedded LDAP)" with "for testing purposes" (p.369), without `spring.ldap.urls` (p.370), YAML list/index, `schema.ldif`/`ldif`, `validation.schema` (p.370); the lookup matching rule accepts non-alphanumeric separators (`PKCS#1`, `tag=id:Metaspace`) |
| D6 (medium, C14) | p.652-655: `<execution>` of `build-info`, starter-parent already pre-configures the Git plugin, `git.commit.*` in `/info`, versions warning | `references/12` (build info, git info, versions, jar, dependency); lookup `git.commit.time`/`git-commit-id` COVERED. **Bug found along the way:** the curated list matched by part of a word, and `git.commit.time` fell into the term `@Commit`; now it matches by whole token |
| D7 (minor, C02) | p.569-570: Jetty 10 = `jetty.version` 10.0.8 + exclusion of the Jetty 9 dependencies; the Reference does not state the Java of Jetty 10 | `references/05` (server line + Gradle/Undertow in WebFlux) and `datado.md` ("Reference gaps"); negative p.569-570 |
| Page overstatement (C10) | "contact-points (body p.362)": the default `[127.0.0.1:9042]` is from Appendix A (p.682); p.362 only has an example | `--prop` prints the default as "default in Appendix A (SBR p.682)" and warns not to cite the body; anti-pattern #51; positive check p.682 and negative p.362 |
| `@DynamicPropertySource` (C06) | it is on p.649-650 (Testcontainers with `@Container` on p.647-648) | `references/04`, `sbr_lookup.py --gaps`: 647-650; checks p.647-650 |

**Systematic sweep (omissions of the same class), by chapter.** Method: (1) triage by page (properties/identifiers on the page absent from the references; 53 pages never cited); (2) extraction of all NOTE/TIP/WARNING/IMPORTANT/CAUTION blocks from chapters 1-17 with terms absent from the references (131 blocks); (3) full re-read of the pages with the highest density. Topics added:

| Chapter (Reference) | Topic added | Where | Pages |
|---|---|---|---|
| Using / devtools | trigger file, ResourceLoader/AspectJ, profiles in global files, `FileSystemWatcher`, Relaunch in the IDE, optional `@SpringBootApplication` | `references/00` | 44, 56-57, 61, 64-67, 70 |
| Features / SpringApplication, config | banner (`application.title`, `formatted-version`, `setBanner`), `addListeners`, JSON `null`, import with profile, configtree (dots, `byte[]`, `/*/`, alphabetical order, Docker secrets), canonical placeholder, YAML, Optional/Period/Duration/DataSize, profiles, i18n | `references/01`, `02` | 75, 81-82, 90, 96-99, 102, 107-125, 133, 136-137, 147 |
| Features / logging | `%clr` colors, file table, Logback rotation and patterns, levels via variable, predefined groups, shutdown hook, `LoggingSystem`, forwarded properties, MDC, `springProfile`/`springProperty`, Logback includes, Groovy, file-only logging, Log4j2 (starter, JUL, YAML/JSON, composite) | `references/03` | 137-146, 598-603 |
| Features / testing | vintage, `@RunWith`, RANDOM_PORT x management, `TypeExcludeFilter`, imported `@TestConfiguration`, `AopTestUtils`, `initFields`/`satisfies`, `@WebFluxTest` and security, `@ImportAutoConfiguration`, `WebTestClient`, custom auto-config (imports, order, Javadoc), Kotlin | `references/04` | 155-159, 172-191, 219-227, 231-247 |
| Web / embedded servers, HTTP/2, CORS | SSL/PEM, HTTP/2 per server, proxy, customizers, servlet/filter registration and order, `ServletContextInitializer`, SameSite, encoding, access logs, legacy cookies, MBean registry, JSP, Jersey, JSON/XML, Jackson, multipart, view resolvers, RestTemplate/WebClient, cache busting, `BasicErrorController`, whitelabel, `@LocalServerPort`, JWT resource server, A.11 | `references/05` | 259, 263, 272-282, 310, 569-598, 639, 643-644, 754-767 |
| Data / how-to and LDAP | custom and dual DataSource, JPA (properties, naming, L2 cache, DI, several EMFs, `persistence.xml`), Spring Data web/REST, initialization (Hibernate, `import.sql`, per-platform scripts, Batch, Flyway/Liquibase, test data, detectors), Jedis, JMS, Batch, embedded LDAP | `references/07` | 368-370, 603-638 |
| Actuator / endpoints and properties | web-only endpoints, security with `EndpointRequest`, CORS, custom endpoints (entry, conversion, predicates, status, Range, Principal), health (registry, tree, custom status, reactive, groups, `additional-path`), probes and lifecycle, info/git, paths, management SSL, JMX/Jolokia, loggers; A.14 (health, endpoints, CORS, metrics, StatsD, Stackdriver, Prometheus) | `references/10`, `11` | 441-477, 517, 519-522, 769-798 |
| Deploying | Cloud Foundry, Kubernetes, Heroku, AWS Elastic Beanstalk, Boxfuse, Google Cloud, systemd, init.d (zip64, conf, variables), launch script | `references/09` | 524-540 |
| How-to build / plugins | build-info, git, versions, executable jar, Ant `findmainclass`, `Repackager` | `references/12` | 551-554, 652-655 |
| Appendices | A.1-A.4 (logging, main, banner, config, Quartz, tasks, cache, mail), A.15-A.16, B (format, deprecation, hints, providers, annotation processor) | `references/14` | 668-679, 797-820 |
| Lookup | `--page` (top x start), `--prop` (appendix x body, descriptions), curated matching by token, separators in reference matching, Appendix A section, `trigger-file`; `sbr_terms.json` regenerated (identical: 15,328 words, 64,642 pairs) | `scripts/` | |

**Counts after round 4**: `verify_citations.py` 288 positive (186 + 102 new) / 49 negative (38 + 11 new) / 0 failures; `audit_tokens.py` 3,526 terms, 0 failures, 0 near (`--strict`); `run_script_tests.py` 125/125 (93 + 32 new); `casos-de-teste.md` with 60 cases (12 new: #49-#60).

**Still pointer only (the Reference has it, the package does not summarize it):** Spring REST Docs in detail (p.203-214), Spock (p.223), Apache Geode/GemFire (p.314, 344-345, 404), DLX/DLQ declaration in Rabbit and Kafka listener retry/DLT (p.388, 390), `auto-offset-reset` semantics (p.724), passing mentions of circuit breaker, Sleuth, Zipkin and ZooKeeper (p.464, 494, 518, 96), detailed use of the Maven/Gradle plugins (the text refers to other documents, p.550, 654), Appendix A descriptions outside the curated keys (A.5-A.9, A.12-A.13: `--prop` says to read the page), Appendices C and D (class lists: page index only) and the Actuator API documentation (referred to by the text, p.441). Much of Data/Messaging/IO (chapters 9-11) remains as in round 2: the triage of the note blocks found no relevant gaps beyond those recorded above.

**Status**: fixes made and checked by the package author against the text; independent validation requires a **round 4** blind test with new cases (the 14 of round 3 are "burned").

## 9. Post-blind-test fixes (round 4)
Origin: `scratch/blind/runs4/spring-boot-reference-expert/avaliacao.md` (F 2.64; L 2.86; R 2.71; S 3.00; 73/75 citations OK; two wrong answers, C02 and C07b, both after a package gap).
- **D1 (serious, C07):** `references/11` gained the Atlas/Datadog section (SBR p.780-782): `lwc-*` keys, `meter-time-to-live` 15m, `batch-size`, and the rule `lwc-step` <= `step` with `step` an even multiple of `lwc-step` (7s with a step of 1m or 10s violates it; the computation is labeled [inference]); curated descriptions in `sbr_curated.json`.
- **D2 (serious, C02):** `references/02` gained the constructor binding section (SBR p.107-110): `record` does not need `@ConstructorBinding` unless there are several constructors; nested null x empty `@DefaultValue`; without `@Component`/`@Bean`/`@Import`; `Optional` becomes `null`.
- **D3:** `#---` separator (comment prefix, top-to-bottom order, AND x OR of p.100-101). **D4:** `--prop` tells "no published default (p.766)" apart from "default in the description" and curates Undertow/multipart. **D5:** JBoss note (`webjars-locator-jboss-vfs`, p.258). **D6:** stem search (`autoscal`) and autoscaling note (p.464-465). Redis citation: Appendix A (p.702-704), not p.635.
- **Lookup redone:** COVERED only by the content of the summaries (`sbr_cover.json`, generated by `build_cover_index.py`), whole term/phrase, no substring; the table of contents/Appendix alone give POINTER ONLY. `record` and `ConstructorBinding` became truly COVERED; `HPA` is NOT COVERED; `jboss` is COVERED only because the p.258 summary exists now.
- **Known limit:** a plain one-word common term written without emphasis (no backticks, bold, italics, quotes) in the summaries does not cover; identifiers and phrases of 2+ words cover anywhere. Portuguese queries that do not exist in the English text give NOT COVERED (the curated synonyms keep some Portuguese input aliases).
