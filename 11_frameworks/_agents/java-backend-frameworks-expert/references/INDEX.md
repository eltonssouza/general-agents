# INDEX: java-backend-frameworks-expert

Package proportional to **three sources of different natures**. Read §1 before citing anything.

## 1. Sources (identification verified in the text)

| Acronym | File | What it really is | Pages | Date/version in the text | Usefulness |
|---|---|---|---|---|---|
| **SB3G** | `Spring-Boot-3-Guide-JavaCodeGeeks.pdf` | Book **"Mastering Spring Boot 3.0"**, by **Ahmet Meric**, Packt Publishing, © 2024 (1st ed. July 2024; ISBN 978-1-80323-078-8). **It is not a compilation of articles**; "JavaCodeGeeks" is only where the file came from (SB3G p.2-3, 5). | 256 | Code uses Spring Boot 3.2.x (SB3G p.81, 188), JDK 17, Gradle 8.7 (SB3G p.15) | High, but **didactic/advanced**: neither a basic guide nor a reference manual. Abundant prose, real code excerpts. |
| **QRK** | `Quarkus-Guide.pdf` | **DZone Refcard** "Getting Started With Quarkus Serverless Functions", by **Daniel Oh** (Red Hat), © 2021 Devada, Red Hat partnership (QRK p.1, 9). | 9 | Quarkus **2.x** (plugin 2.2.3.Final; logs "Quarkus 2.1.4.Final") (QRK p.3, 5) | Medium-low: **overview of serverless with Quarkus**, not a general Quarkus guide. p.2 is an advertisement (useless). |
| **MPS** | `MapStruct-Reference.pdf` | **MapStruct 1.6.3 Reference Guide** (Morling, Gudian, Derksen, Hrisafov and community), **2024-11-09**, license CC BY-SA 4.0 (MPS p.1, 3, 96). | 96 | **1.6.3** | High: complete official reference of MapStruct 1.6.3. |

Out of scope: the **extensive official Spring Boot reference** belongs to the agent **spring-boot-reference-expert**: route to it.

## 2. Page convention
- **SB3G:** cite the **PDF page** (`SB3G p.N`). Printed book number = N - 19 on chapter pages (e.g. PDF 23 = printed 4). Map: Ch.1 PDF 22 (printed 3); Ch.2 PDF 42 (printed 23); Ch.3 PDF 72 (53); Ch.4 PDF 100 (81); Ch.5 PDF 130 (111); Ch.6 PDF 160 (141); Ch.7 PDF 184 (165); Ch.8 PDF 208 (189); Ch.9 PDF 228 (209); Index PDF 244 (225). Front matter uses Roman numerals (xiii...).
- **QRK:** PDF page = printed number (1-9).
- **MPS:** only the PDF page exists (1-96); the guide has no printed numbering; the table of contents (p.1-2) uses section numbers (e.g. 5.9), not page numbers.
- All citations in the package follow `SIGLA p.N` (PDF).

## 3. What was read
- **SB3G:** p.2-243 read in full (prose and code); p.244-251 (back-of-book index) only sampled (p.244-245 and p.252-256 are Packt advertisements); figures (diagrams, Keycloak/Grafana/CMAK screenshots) have **no** extractable text; statements about them come from the surrounding prose.
- **QRK:** 9 pages in full; figures 1-10 (DEV UI, OpenShift, Lambda) have no text; **figure 7 (QRK p.6) was rendered and checked visually** (numbers in `qrk-quarkus-serverless.md`); the other figures were not inspected.
- **MPS:** 96 pages in full (table text and code). The code line numbers in the PDF are extraction noise.
- Intermediate notes: `scratch/frameworks/java-backend-frameworks-expert/notes/`.

## 4. References by topic

| File | Content | Source/pages |
|---|---|---|
| `00-fontes-e-lacunas.md` | Nature of the sources, gaps and internal divergences | all |
| `sb3g-01-visao-e-novidades.md` | Spring Boot advantages and 3.0 novelties according to the book | SB3G p.22-33 |
| `sb3g-02-padroes-arquiteturais.md` | Microservices, DDD, CQRS, Event Sourcing, Saga, Circuit Breaker | SB3G p.42-71 |
| `sb3g-03-rest-reativo.md` | WebFlux, Reactor, reactive REST API, backpressure | SB3G p.72-97 |
| `sb3g-04-dados-cache-batch.md` | Spring Data JPA/Mongo, cache, Spring Batch, Liquibase | SB3G p.100-129 |
| `sb3g-05-seguranca.md` | Spring Security, OAuth2/JWT, Keycloak, RBAC, reactive | SB3G p.130-158 |
| `sb3g-06-testes.md` | TDD, Mockito, @WebMvcTest, Testcontainers, WireMock, WebTestClient | SB3G p.160-181 |
| `sb3g-07-containers-k8s.md` | Layered jar, buildpacks, graceful shutdown, probes, ConfigMap/Secret, Prometheus/Grafana | SB3G p.184-206 |
| `sb3g-08-kafka.md` | Kafka + Spring Boot, producer/consumer, CMAK | SB3G p.208-226 |
| `sb3g-09-aop-feign-autoconfig.md` | AOP, Feign, @Conditional, pitfalls | SB3G p.228-242 |
| `qrk-quarkus-serverless.md` | Quarkus serverless (Refcard) | QRK p.1-9 |
| `mps-01-setup-e-opcoes.md` | Dependencies, processor, `-A` options, IDE | MPS p.3-14 |
| `mps-02-definindo-mappers.md` | @Mapper, @Mapping, builders, constructors, obtaining the mapper, DI | MPS p.14-32 |
| `mps-03-conversoes-e-resolucao.md` | Implicit conversions, references, resolution, qualifiers | MPS p.32-48 |
| `mps-04-colecoes-streams-enums.md` | Collections, maps, streams, @ValueMapping, @EnumMapping | MPS p.48-60 |
| `mps-05-factories-e-opcoes-avancadas.md` | Factories, defaults, expressions, subclasses, null, @Condition, exceptions | MPS p.60-75 |
| `mps-06-reuso-customizacao-spi-lombok.md` | Config inheritance, @MapperConfig, decorators, before/after, SPI, Lombok | MPS p.76-96 |
| `glossario.md` | Terms | |
| `procedimentos.md` | Procedures P1-P8 | |
| `casos-e-antipadroes.md` | Cases and anti-patterns supported by the text | |
| `datado.md` | What is dated in each source | |

## 5. Scripts (Python 3 stdlib, `python -I`, no network, do not run the framework)
- `scripts/fw_lookup.py` (+ `fw_index.json`): topic search across the 3 sources; `--gaps` lists NOT COVERED.
- `scripts/sb3_checklist.py`: Spring Boot 3 project checklist from the SB3G items (`list`, `scan DIR`).
- `scripts/mapstruct_tool.py`: `generate SPEC.json` (generates a @Mapper interface with only the attributes documented in MPS 1.6.3) and `validate FILE.java` (validates against documented rules).
- `scripts/compare_approaches.py` (+ `compare_data.json`): compares approaches with what the text says and where it is silent.
