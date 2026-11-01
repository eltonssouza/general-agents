# 00. Sources, gaps and internal divergences

This is a **mixed-coverage** agent: one large, didactic source (SB3G), one complete and specific official reference (MPS), and one tiny promotional source (QRK). Answers must make clear which source they come from.

## 1. Nature of each source
- **SB3G** is an **intermediate/advanced-level** book built around a sample project (an online bookstore) used across several chapters; lots of motivational text, little normative specification. It is not the official Spring Boot documentation [from source] (SB3G p.2-3, 14). Code run with JDK 17 and Gradle 8.7 (SB3G p.15).
- **QRK** is a **sponsored Refcard** (Red Hat/DZone, 2021) focused on **serverless functions** with Quarkus (SB3G does not apply) (QRK p.1, 3, 9).
- **MPS** is the **official reference** of MapStruct 1.6.3 dated 2024-11-09 (MPS p.1, 96).

## 2. Gaps (answer "NOT COVERED")
- **"Official" Spring Boot**: exhaustive properties, full actuator, profiles in depth, externalized config, etc. -> route to **spring-boot-reference-expert**.
- **Spring Boot 3.x versions later than 3.2.x**: the book uses 3.2.5 (SB3G p.81), 3.2.1 (SB3G p.188); nothing about 3.3+ [DATED].
- **Custom starters / own auto-configuration**: the preface (SB3G p.15) and ch.9 (SB3G p.237) promise it, but the book only covers `@Conditional*`, `@AutoConfigureOrder` and `@ConditionalOnMissingBean` conceptually (SB3G p.237-241); it **does not implement a starter**.
- **Multiple data sources**: the ch.4 summary mentions it (SB3G p.129), but the chapter does not show it.
- **Quarkus**: only serverless/Funqy/Knative/AWS Lambda/CloudEvents on Quarkus 2.x; nothing about classic REST, Panache, data extensions, security, testing beyond continuous testing, configuration, Quarkus 3.x (QRK p.1-9).
- **MapStruct**: the MPS does **not** mention Spring Boot (the word does not appear), Kotlin, `Optional`, or Java records as a topic; only `componentModel = "spring"` and a decorators section with Spring (MPS p.8, 31, 81). For these questions: NOT COVERED.
- **Quarkus vs Spring Boot comparison** beyond the Refcard sentence (QRK p.1): there is no technical comparison in the sources.

## 3. Internal divergences and inaccuracies of the sources (report, do not "fix")
1. **Minimum Java version in SB3G:** p.22 and p.30 say the Spring Boot 3.0 baseline is Java 17; p.80 says it "requires at least Java 11, but we will use 17". The agent treats the divergence as a **book inconsistency** (SB3G p.22, 30, 80).
2. **R2dbcRepository<User, String>** with `@Id Long id` (SB3G p.82 vs p.84): type inconsistency in the example.
3. **Ch.7 "Enable layering"** (SB3G p.188): the text asks to "configure the plugin" but **does not show the configuration**; it only shows the resulting `layers.idx` (SB3G p.189).
4. **Ch.8:** the text mentions a "MessageProducer service", but the code is `EventProducerController` (SB3G p.217-218); ports cited: p.216 shows `server.port:8181` and p.220 uses 8282 (producer) and 8181 (consumer).
5. **Ch.5 reactive login:** the controller returns `Mono`, but uses a blocking `RestTemplate` (SB3G p.157): the book does not discuss this.
6. **Ch.5 password flow:** `/login` uses `grant_type=password` (SB3G p.145). [extrapolation] this flow is considered legacy/discouraged in current OAuth2; the book does not discuss it.
7. **MPS p.54:** the text says `IllegalStateException` for an unknown constant, but the generated code of the same example throws `IllegalArgumentException` (MPS p.54, 59).
8. **MPS p.8:** description of the `jakarta`/`jsr330` componentModel with `{@code @Named}` syntax (leftover Javadoc formatting in the documentation).
9. **QRK p.8:** the `curl` example lists `-H "Ce-1.0"` (probably a typo in the original for the CloudEvent version header); the agent does not correct it as fact.

## 4. Safe usage
The SB3G examples use trivial development credentials (`admin/admin` in Keycloak, `yourpassword`, `secret-client`) and `:latest` images (SB3G p.106, 136-138, 173-174). They are **local learning material**; do not recommend them as a production configuration [extrapolation].
