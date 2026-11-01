# [DATED] — what is version/edition-specific and inconsistencies in the PDF

Date reference: **Spring Boot 2.7.18**, copyright 2012-2023; log examples from 11/23/2023 (SBR p.22, 69, 72). Pages = PDF (printed = N−20). Nothing below says what changed afterwards; it only marks what the text **declares** as limited, deprecated or old.

## Markings in the text itself (version 2.7.18)
- Requires **Java 8**; compatible up to **Java 21**; Spring Framework 5.3.31+ (SBR p.27). Servlet 3.1/4.0; Tomcat 9.0, Jetty 9.4/10.0, Undertow 2.0 (SBR p.27-28).
- Code with `javax.*` (validation, servlet, JMS, WebSocket etc.); no `jakarta` outside Appendix F coordinates.
- URL suffix (for example .json) and `spring.mvc.pathmatch.use-suffix-pattern`/`favor-path-extension`: **deprecated** and future removal is announced (SBR p.261).
- Elasticsearch `RestHighLevelClient`: auto-configuration **deprecated** (SBR p.358). Hazelcast 3: deprecated (SBR p.414). `FlywayCallback`: deprecated (SBR p.632).
- **OAuth 2 Authorization Server:** the text says Spring Security did not yet implement it and mentions the Spring Security OAuth project (SBR p.311).
- `schema.sql`/`data.sql` together with Flyway/Liquibase: "support will be removed in a future release" (SBR p.630).
- `spring-boot-properties-migrator` serves migrations between feature releases (SBR p.40).
- Platform and log examples are old (JDK 8, Maven 3.3.1, 2014 dates, CloudCaptain/Boxfuse) (SBR p.525-533).
- Metrics: properties under `management.metrics.export.*`; `httptrace` as an endpoint; no Observation API (SBR p.440-442, 477-498).
- Tests: `@MockBean`/`@SpyBean`, `TestRestTemplate`, `WebTestClient` as described; no Docker Compose or automatic service connection annotation (SBR p.168-171, 226-229).

## Internal inconsistencies in the PDF (cite the pages)
1. **Maven version:** "3.5+" in the requirements table (SBR p.27), "3.3 or later" in the installation text (SBR p.28) and "3.2 (or later)" for the plugin (SBR p.550).
2. **`spring.datasource.generate-unique-name`:** the body recommends setting it to `true` to isolate test databases (SBR p.323), but the Appendix A table shows default `true` (SBR p.689).
3. **Spelling `reponse-url`** in a SAML example (SBR p.312-313) [possible typo in the source].
4. **Truncated cell** in Appendix A: `spring.datasource.dbcp2.max-wait-` without the suffix (page break, SBR p.688); the package index discards that key instead of completing it.

## How to answer
- Question about "today"/"current version": say the collection is 2.7.18 [DATED] and that later changes are NOT COVERED: decline and redirect (Boot 3.x: java-backend-frameworks-expert; the rest: current documentation). The only allowed warning is that this book is 2.7.18; do not offer Boot 3 facts from memory (Java 17+, Jakarta etc.), not even labeled [extrapolation].

## Reference gaps recorded in round 4
- **Jetty 10:** the Reference only says Jetty 10 supports Servlet 4.0 and shows the `jetty.version` 10.0.8 override with the exclusions of the Jetty 9 dependencies (SBR p.569-570); it **does not state Jetty 10's minimum Java**. Any claim about that is an [extrapolation] with no page.
- **Appendix A.5-A.9:** the package keeps key, page, section and default; the description was only paraphrased for some of the keys (A.1-A.4, A.11 and A.14 in prose in the references; ~95 keys in `sbr_curated.json`). For the rest, `--prop` tells the user to read the description on the Appendix A page.
- **Appendix A.12 and A.13:** the `spring.rsocket.server.ssl.*` keys (A.13) share p.769 with the start of A.14, and `spring.security.user.*` (A.12) share p.768 with A.13; the index now assigns the section by the key's position on the page.
