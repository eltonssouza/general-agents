# Fidelity report: java-backend-frameworks-expert

Verification date: 2026-10-26 (local environment, Windows, Python 3). **No blind validation by an independent model was done**: the tests were written and executed by the package author.

## 1. Sources and reading
| Abbreviation | Source | Pages | Read |
|---|---|---|---|
| SB3G | *Mastering Spring Boot 3.0*, Ahmet Meric, Packt, Jul/2024 (a book, not a compilation) | 256 | p.2-243 in full (prose and code) in sequential blocks, with notes on disk; p.244-251 (back-of-book index) **only sampled**; p.252-256 Packt ads; p.1, 7, 19, 21, 41, 99, 159, 183, 207, 227, 243 blank |
| QRK | DZone Refcard *Quarkus Serverless Functions*, Daniel Oh, Red Hat, 2021 | 9 | in full; p.2 ad; **figure 7 (p.6) rendered and checked visually** (RSS 12/73/136 MB; boot 0.016/0.943/4.3 s) |
| MPS | *MapStruct 1.6.3 Reference Guide*, 2024-11-09 | 96 | in full (code text and tables; the PDF is native text; line numbers from the extraction are noise) |

SB3G figures (pattern diagrams, Keycloak/Grafana/CMAK/Kafka Manager screenshots) and the other QRK figures were **not** inspected; statements about them come only from the surrounding prose.

## 2. Page convention
PDF page. SB3G: printed = PDF - 19 in the chapters (checked in all chapters); QRK: printed = PDF; MPS: PDF only.

## 3. Citation verification (`tests/verify_citations.py`)
Command: `python -I tests/verify_citations.py --src ../../../scratch/frameworks`.
- **Range:** about 1,900 page references `ABBR p.N` in the package's .md/.py/.json files within 1..max of each source and **none** pointing to a blank SB3G page.
- **Positive:** 177 checks (SB3G 96, QRK 9, MPS 72) confirm key terms on the cited page (4 normalization variants to tolerate line breaks in the middle of tokens).
- **Negative:** 28 checks of plausible claims that the sources do **not** contain: the MPS does not cover Spring Boot, Kotlin/kapt/ksp, `java.util.Optional`, Java records, Jackson/Hibernate, `componentModel = "spring"` in an example, MapStruct 2.x, the name of the collection strategy attribute; the QRK does not cover Panache, Hibernate, Quarkus 3, Funqy-Azure, benchmark, detailed DevServices; the SB3G does not mention Quarkus or MapStruct, does not use Resilience4j, Flyway, `@PreAuthorize`, `@Transactional`, Caffeine/Redis, Helm/Kustomize, `@SpringBootTest`, `@DataJpaTest`, Spring Boot 3.3, Spring Authorization Server, does not implement a starter (no `AutoConfiguration.imports`/`spring.factories`) and does not show the layered jar configuration.
- **Final result:** 0 failures.

### Additional audit (token by token)
A standalone script (not included) extracted the backtick-delimited snippets from the references and checked whether they appear on the pages cited on the same line. Of the ~100 alerts, most were pseudo-code/shortcuts/file names of the package itself (e.g. `scan DIR`, `GET /message/{message}`); **5 real corrections** were applied: the `numberFormat` page (MPS p.32-33), the pages of `keyTargetType`/`valueTargetType` and `nullValueMappingStrategy` of `@MapMapping` (MPS p.13, 67, 68), the page of `Long id` (SB3G p.82, 84), the page of the `/auth/realms/` URLs (SB3G p.142) and the WireMock page (SB3G p.174, 176).

## 4. Script tests (`tests/run_script_tests.py`)
62 automated checks, all passing: lookup (search, NOT COVERED for Kotlin/custom starter/Panache/nonexistent term, `--page` with blank/promotional/out-of-range pages, `--json`), checklist (PRESENT/ABSENT/ALERT on a fixture project, empty directory, nonexistent, invalid section), `mapstruct_tool.py` (generates `@Mapper` with documented attributes; aborts a bad spec with ERRORS citing pages; validates `MapperOk.java` with no findings and `MapperRuim.java` with ERRORS/WARNINGS; injection text in comments is ignored), `compare_approaches.py` (separates the vendor claim, states "what the text does not say"), index/data consistency and `verify_citations.py`.

## 5. Conceptual cases (`tests/casos-de-teste.md`)
30 cases (C/P/B/F/I) checked manually against agent + references + scripts; those with a supporting script are listed in the Verification column. Injection cases (27-30): the agent treats code/JSON/PDF as data; the scripts only read files and execute nothing.

## 6. Findings about the sources themselves (reported in the package)
1. SB3G p.22/30 (Java 17 baseline) vs p.80 (minimum 11).
2. SB3G p.82 vs 84: `Long id` with `R2dbcRepository<User, String>`.
3. SB3G p.188: layered jar without the plugin configuration.
4. SB3G p.15 and 237 promise custom starters; ch.9 does not implement them; p.129 mentions multiple data sources that are not shown.
5. SB3G p.216 vs 220: Kafka producer/consumer ports.
6. SB3G p.145: `grant_type=password` flow and example credentials/`:latest` images [extrapolation: do not recommend for production].
7. MPS p.54: prose `IllegalStateException` vs code `IllegalArgumentException`.
8. QRK: vendor material; performance claims without methodology; p.8 has `-H "Ce-1.0"` (probable typo).

## 7. Limitations and pending items
- Sources from 2021-2024 [DATED]; the agent does not know what changed afterwards.
- `mapstruct_tool.py validate` is a **heuristic textual linter** (regex + annotation mini-parser): it can be wrong on unusual Java; it only reports ERROR for explicit MPS rules; it **compiles** nothing.
- `sb3_checklist.py` detects by textual markers; absence does not mean an error; the Java 17/Boot 3 markers are [extrapolation].
- The SB3G back-of-book index (p.244-251) was not used.
- Spring Boot/Quarkus/MapStruct were not run; the books' code was not tested.
- No blind test by an independent model.
