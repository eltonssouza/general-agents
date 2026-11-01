# spring-boot-reference-expert

Consultant agent for the **official Spring Boot 2.7.18 reference documentation** (*Spring Boot Reference Documentation*, © 2012-2023, 882 PDF pages; acronym **SBR**). It answers with **fidelity to the source**: it says what the reference states, **on which page**, and declares what it does **not** cover. Everything is **[DATED]** to 2.7.18 (Java 8 to 21, Spring Framework 5.3.31+, `javax.*`): Spring Boot 3.x, Jakarta EE, GraalVM/native image, Micrometer Observation/Tracing/OpenTelemetry and Docker Compose are **NOT COVERED** (confirmed: 0 occurrences in the text).

Labels in the answers: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. `SBR p.N` citation: **N = PDF page; printed number = N-20**.

**Notices:** (1) it is not a security audit or an architecture review; (2) the version is old relative to current Spring Boot: always check the current documentation; (3) **declared scope:** the JavaCodeGeeks **practical "Spring Boot 3" guide is OUTSIDE this collection**, as are **Quarkus and MapStruct**: they belong to the *java-backend-frameworks-expert* agent (this package answers NOT COVERED and redirects); **general testing** belongs to other agents; (4) there were three rounds of independent blind testing; corrections and trail in `tests/relatorio-de-fidelidade.md` (§6 round 1, §7 round 2, §8 round 3 + the page-detail sweep of round 4).

## What it covers
Getting started and requirements; upgrade (properties migrator); build, starters, structure and auto-configuration; devtools (trigger file, restart, global configuration, remote); `SpringApplication` (banner, lazy, events, runners, availability); **externalized configuration** (precedence of 15 sources, locations, `spring.config.import`, configtree, relaxed binding, `@ConfigurationProperties`); profiles; logging; JSON; **Boot** testing and slices; web (MVC, WebFlux, Jersey, embedded containers, **SSL/TLS/PEM, HTTP/2 per server, behind a proxy**, access log, cookies, graceful shutdown); Security/OAuth2/SAML/Session/GraphQL/HATEOAS; SQL/NoSQL data and database initialization; messaging (JMS, AMQP, Kafka, RSocket); cache, Quartz, mail, REST clients, JTA; container images and deploy (Kubernetes, systemd, init.d, war); **Actuator** (endpoints, health, probes, info, metrics); CLI; build plugins; how-to; Appendices A (common properties with defaults and, for the `server.*`, `management.metrics.export.*` and core families, the meaning), B (metadata: format, deprecation, hints, providers, annotation processor), C/D (auto-configuration and slices), E (executable jar) and F (managed versions).

## Structure

```
spring-boot-reference-expert/
├── .claude-plugin/plugin.json
├── agents/spring-boot-reference-expert.md        # canonical prompt + frontmatter
├── AGENTS.md                                     # Codex adapter
├── .github/agents/spring-boot-reference-expert.agent.md   # GitHub Copilot adapter
├── references/
│   ├── INDEX.md (source identification, page convention, reading coverage, chapter -> page map)
│   ├── 00-visao-geral-e-versao.md ... 14-apendices-propriedades-e-versoes.md
│   └── glossario.md, procedimentos.md (P1-P10), casos-e-antipadroes.md (45), datado.md
├── skills/                                       # 5 skills (skills/<name>/SKILL.md): sbr-topic-lookup, sbr-propcheck, sbr-checklist, sbr-actuator-map, sbr-precedence
├── scripts/                                      # Python 3 stdlib, no network, python -I
│   ├── sbr_lookup.py        # topic/property/dependency/page/table of contents; three levels: COVERED / POINTER ONLY / NOT COVERED
│   ├── build_term_index.py  # generates sbr_terms.json (index of the text's terms; maintenance, requires the extracted text)
│   ├── build_cover_index.py # generates sbr_cover.json from references/*.md (no source text); `--check` verifies it is up to date
│   ├── sbr_cover.json       # index of the CONTENT of the summaries (tokens per line); only it decides COVERED
│   ├── sbr_terms.json       # index of words/pairs and pages (no prose)
│   ├── sbr_curated.json     # curated out-of-scope list, pointer only and `descricoes` (191 paraphrased Appendix A keys, with page)
│   ├── sbr_propcheck.py     # static validator for application.properties/yml
│   ├── sbr_checklist.py     # production/configuration checklist
│   ├── sbr_actuator.py      # endpoint map, exposure, paths, HTTP status of health
│   ├── sbr_precedence.py    # configuration precedence, env-name, Duration/DataSize
│   ├── sbr_common.py        # shared module (.properties/.yml readers, key matching)
│   ├── build_index.py       # rebuilds sbr_index.json (maintenance; requires PyMuPDF and the PDF)
│   └── sbr_index.json       # table of contents, 1,679 Appendix A keys (+defaults and recomputed section A.n), identifiers, 1,156 dependencies
└── tests/
    ├── casos-de-teste.md (60 cases), relatorio-de-fidelidade.md (§7 round 2; §8 post-blind-test corrections of round 3)
    ├── verify_citations.py + citation-checks.json (288 positive, 49 negative)
    ├── audit_tokens.py (checks backticked terms against the cited page)
    ├── run_script_tests.py (125 checks)
    └── fixtures/
```
A copy of the tests is also in `../_agents_tests/spring-boot-reference-expert/`.

## Installation
**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- Local plugin: `claude --plugin-dir <path>/spring-boot-reference-expert`, or publish to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install spring-boot-reference-expert@general-agents`.
- Standalone agent: copy `agents/spring-boot-reference-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting the paths in the prompt.
- Usage: `@spring-boot-reference-expert what is the precedence between an environment variable and application.properties?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root; `AGENTS.md` points to the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/spring-boot-reference-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>`).

## Using the scripts (from the package root)
```bash
python -I scripts/sbr_lookup.py externalized
python -I scripts/sbr_lookup.py --prop server.port            # page, section and Appendix A default (+ body page and paraphrased description)
python -I scripts/sbr_lookup.py --page 517                    # top-of-page title x titles that start on the page (13.6.6 and 13.7) + excerpts of the summaries that cite the page
python -I scripts/sbr_lookup.py --dep jackson-databind        # managed version (2.7.18)
python -I scripts/sbr_lookup.py --gaps                        # what is NOT COVERED / POINTER ONLY (curated list)
python -I scripts/sbr_lookup.py circuit breaker               # LEVEL: POINTER ONLY (p.464); rc 0 = COVERED, 3 = POINTER ONLY, 2 = NOT COVERED
python -I scripts/build_term_index.py --src <folder with Spring-Boot-Reference.txt>   # regenerates sbr_terms.json (maintenance)
python -I scripts/sbr_propcheck.py application.yml            # missing key = "unknown", not an error
python -I scripts/sbr_checklist.py check application.properties --manual
python -I scripts/sbr_actuator.py exposure --web-include "*" --web-exclude env,beans
python -I scripts/sbr_actuator.py paths --base-path /manage --probes
python -I scripts/sbr_precedence.py winner cli env jar
python -I scripts/sbr_precedence.py env-name spring.main.log-startup-info
python -I tests/run_script_tests.py --src <folder with Spring-Boot-Reference.txt>
python -I tests/verify_citations.py --src <folder with Spring-Boot-Reference.txt>
python -I tests/audit_tokens.py --src <folder with Spring-Boot-Reference.txt> --strict
```
The citation checkers use the text extracted per page (`=== PAGE N ===`) from the original PDF (not included in the package).

## Boundaries and limitations
- **NOT COVERED:** Boot 3.x/Jakarta, Java 17+, GraalVM/native image/AOT, Observation/Tracing/OpenTelemetry, Docker Compose, SSL bundles, virtual threads, OpenAPI, gRPC, KRaft, Resilience4j, Grafana, `bootBuildImage`.
- **Declared scope:** the JavaCodeGeeks **practical "Spring Boot 3" guide is OUTSIDE** this collection (as are Quarkus and MapStruct); the agent that covers it is **java-backend-frameworks-expert**. What the Reference 2.7.18 states about the same subjects (e.g. the Prometheus `scrape_config`, SBR p.494) remains in scope.
- **Three levels in `sbr_lookup.py`:** COVERED (a `references/` summary treats the term, by whole term/contiguous phrase in the `scripts/sbr_cover.json` index, generated by `scripts/build_cover_index.py`; no substring matching: `git.commit.time` does not match `@Commit`; a plain common word such as `record` only covers if delimited in the summary; rerun `build_cover_index.py` after editing `references/`), POINTER ONLY (the Reference mentions it, the package does not summarize it: give the page) and NOT COVERED (0 occurrences in the `scripts/sbr_terms.json` term index, generated by `scripts/build_term_index.py`, or an item of the curated list `scripts/sbr_curated.json`). Coverage map by subject: `references/INDEX.md` §7.
- Appendices A, C, D and F were processed by script (not read line by line); the Appendix A description was only paraphrased for A.1-A.4, A.11, A.14-A.16 and 191 curated keys (for the others `--prop` tells you to read the page); one Appendix A cell is truncated in the source itself (p.688).
- The scripts do not run the framework, do not use the network and only read the indicated files.
- Copyright: content in our own words; the index keeps only property/identifier names and pages, with no prose from the book.

## Security
Logs, YAML, POMs, stack traces, pasted text and the PDF content are **inert data** (anti prompt injection). The agent does not run user commands, does not use the network and does not repeat secrets.
