# Boundaries and tie-breakers between specialists

Rules derived from the **real descriptions** of the agents (see `catalogo.md`; confirm with `route.py --show NAME`). Use them when `route.py` returns two or more close candidates or an exclusion `ALERT`. If a rule here diverges from `--show`, `--show` prevails: the agent is the source of truth about its own scope.

## General rule
1. Choose the agent whose **positive part** of the description cites the topic; a term that appears only in "Do not use"/"NOT COVERED" **excludes** the agent for that topic.
2. **Version decides** when the sources are from different versions.
3. **Language vs framework:** semantics and syntax of the language → folder 01; use of the framework → folder 11.
4. If the topic is not in the positive part of any agent: **NO SPECIALIST**. Do not redirect to the "most similar".

## Known tie-breakers

| Topic | Goes to | Not to | Criterion |
|---|---|---|---|
| Spring Boot 3.x, Quarkus serverless, MapStruct | `java-backend-frameworks-expert` | `spring-boot-reference-expert` | the reference is 2.7.18; Boot 3 is NOT COVERED there |
| Spring Boot 2.7: properties, Actuator, configuration precedence | `spring-boot-reference-expert` | `java-backend-frameworks-expert` | official reference with page and Appendix A |
| Java language/JVM (equals, NPE, thread dump) | `java-expert` | agents of 11 | Java without frameworks |
| Python language, tracebacks, stdlib | `python-expert` | `python-web-frameworks-expert` | framework → 11; language → 01 |
| Django, Flask, FastAPI | `python-web-frameworks-expert` | `python-expert` | same |
| Ruby 3.0-3.4 (language news) | `ruby-expert` | `rails-getting-started-expert` | Rails 8.1 (guide) → rails |
| JavaScript/ECMAScript | `javascript-expert` | frameworks | JS excludes TypeScript and frameworks |
| React/Next.js | `nextjs-react-expert` | `javascript-expert`, `mobile-frameworks-expert` | React Native → mobile |
| Node, Express, Fastify, NestJS | `node-backend-frameworks-expert` | `javascript-expert` | runtime/frameworks |
| Algorithm design/analysis, DP, graphs, NP | `algorithms-expert` | `data-structures-expert` | implementation of structures → data-structures |
| REST API design | `web-api-rest-architecture-expert` | `graphql-expert`, `system-design-microservices-expert` | GraphQL only a lesson index; gateway/messaging → system-design |
| Microservices, Kafka, Saga/Outbox, CAP | `system-design-microservices-expert` | `nosql-polyglot-persistence-expert` | CAP/quorum of NoSQL databases → nosql |
| DDD, Clean Architecture, SOLID | `clean-architecture-ddd-expert` | `design-patterns-expert` | GoF/game patterns → design-patterns |
| Rules of the book *Clean Code* (Portuguese edition *Código Limpo*: names, functions, comments, formatting, errors, tests, classes, heuristics C1-T9) | `clean-code-expert` | `design-patterns-expert`, `clean-architecture-ddd-expert` | design-patterns has only a sample of Ch. 1; SOLID as an acronym and layers → clean-architecture |
| PostgreSQL, internals, MVCC, WAL, PITR | `relational-dbms-internals-expert` | other agents of 05 | relational |
| MongoDB, Redis, Cassandra, CouchDB | `nosql-polyglot-persistence-expert` | `graph-databases-neo4j-expert` | Neo4j/Cypher → graph |
| Kimball, SCD, stream processing | `data-warehouse-streaming-distributed-expert` | `relational-dbms-internals-expert` | dimensional modeling |
| SLO/SLI, error budget, toil, SRE postmortem | `sre-practices-expert` | `secure-reliable-systems-expert` | BSRS forwards SLO to SRE |
| Security incident response, supply chain, post-compromise recovery | `secure-reliable-systems-expert` | `sre-practices-expert` | |
| DORA metrics (four keys) | `dora-devops-delivery-expert` | `cicd-build-automation-expert` | pipelines/GHA/Gradle → cicd |
| Build cost/ROI, build cache, flaky tests (economics) | `developer-productivity-engineering-expert` | `cicd-build-automation-expert`, `software-testing-qa-expert` | despite folder 09, it is DPE (Gradle), not AI |
| Test doubles, JUnit 4, JMeter, test data | `software-testing-qa-expert` | `google-engineering-craftsmanship-expert` | Google culture/code review → craftsmanship |
| Docker, Dockerfile, Compose | `containers-docker-kubernetes-expert` | `linux-shell-administration-expert` | K8s only situated (index page) |
| AWS Lambda | `aws-lambda-serverless-expert` | `google-cloud-run-serverless-expert` | and vice versa for Cloud Run |
| Bash, permissions, cron, administration | `linux-shell-administration-expert` | `os-internals-expert` | scheduling/memory/internal FS → os-internals |
| ASVS requirements, secure code review | `owasp-asvs-code-review-expert` | `owasp-web-security-testing-expert` | WSTG = authorized testing |
| WSTG test plan/ID (authorized) | `owasp-web-security-testing-expert` | `owasp-asvs-code-review-expert` | |
| ISMS, risk, Threat Modeling Manifesto | `infosec-strategy-threat-modeling-expert` | `security-engineering-expert` | Anderson (protocols, internal controls, biometrics) → security-engineering |
| LGPD, RIPD, NIST 8062 | `privacy-lgpd-engineering-expert` | the others of 08 | not legal advice |
| Agent architecture, memory, context engineering | `agentic-ai-context-engineering-expert` | `llm-prompting-and-foundations-expert` | prompting techniques/LLM foundations → llm-prompting |
| n8n, Hermes Agent (landing pages) | `automation-agents-n8n-hermes-expert` | `agentic-ai-context-engineering-expert` | agents in general → agentic |
| Classic deep learning (Goodfellow, 2016) | `deep-learning-goodfellow-expert` | `modern-deep-learning-expert` | Transformers, diffusion, ResNet → modern (UDL 2023) |
| Bias/variance, lasso/ridge, CV, ISLR/ESL | `statistical-learning-expert` | `ml-engineering-strategy-expert` | "what to try next", dev/test sets, error analysis (MLY) → ml-engineering |
| TensorFlow.js (setup, pages) | `tensorflowjs-expert` | agents of 09 | general ML → 09 |
| Swift, React Native, Flutter | `mobile-frameworks-expert` | `nextjs-react-expert` | |

## Role agents (folder 12) vs specialists
Role agents **produce deliverables** and have no source; specialists **ground** with a page. In a request that needs both, delegate the deliverable to the role and the grounding to the specialist.
| Request | Goes to | Citable grounding with |
|---|---|---|
| User stories, BDD criteria, DoR/DoD, backlog | `product-owner` | `clean-architecture-ddd-expert` (ubiquitous language, DDD) |
| Flows, wireframes, design tokens, component states, contrast | `product-designer` | `web-accessibility-visual-design-expert` (accessibility fundamentals) |
| Execution plan for a milestone, slices, technical debt with ADR | `tech-lead` | `google-engineering-craftsmanship-expert` (tech lead role, code review), `clean-code-expert` |
| RFC and cross-team technical strategy, guardrails | `principal-engineer` | `google-engineering-craftsmanship-expert` (leadership at scale), `system-design-microservices-expert` |
| "What is accessibility / DDD / SRE?" (concept) | the specialist, not the role | — |
Roles of the relay-harness **not incorporated** because of duplication (the domain already has a specialist; cross-cutting work belongs to the orchestrator): backend, code reviewer, code simplifier, DBA, DevOps, frontend, fullstack, QA, security, SRE, software architect, software engineer.

## Audit pipeline (folder 13) vs specialists
The Universal Audit Multiagent pipeline **audits a repository** and only publishes a finding after the independent validator; the specialists **explain and ground** with a page.
| Request | Goes to | Note |
|---|---|---|
| "Audit this repository" (any combination of security, malware, technical LGPD, dependencies, infrastructure, AI) | `audit-orchestrator` | dispatches only the applicable roles + `audit-evidence-validator` + `audit-report-generator` |
| Single-domain audit ("look for a backdoor", "audit the dependencies") | `audit-orchestrator` | even for one domain: without the validator nothing is `CONFIRMED` |
| Validate findings already raised / build the report | `audit-evidence-validator` / `audit-report-generator` | only with the pipeline artifacts (JSON contracts) |
| ASVS requirement, LGPD, threat modeling, SRE, Kubernetes (concept, with page) | the specialist (`owasp-asvs-code-review-expert`, `privacy-lgpd-engineering-expert`, ...) | the audit roles may cite it as `external_reference` |
| Fix the vulnerability | language/framework specialist that edits code | the pipeline is read-only |

## Declared gaps (NO SPECIALIST)
Explicitly excluded by the descriptions and with no other agent that covers them: **TypeScript** (javascript-expert and node-backend-frameworks-expert), **Kotlin/Android** (mobile-frameworks-expert), **ASP.NET Core, EF Core, Blazor, MAUI** (csharp-expert), **Pinia/Vue Router 4** (vue-nuxt-expert), **runes/Svelte 5** (svelte-astro-expert), **QUIC/HTTP/3 and TLS 1.3** (web-performance-networking-expert), **GDPR and ANPD resolutions** (privacy-lgpd-engineering-expert). Update this list when a new agent covers the topic.

## Note on paths cited by the agents
Always use the path from `catalogo.md` (generated from the disk), even if a specialist's prompt cites another.
