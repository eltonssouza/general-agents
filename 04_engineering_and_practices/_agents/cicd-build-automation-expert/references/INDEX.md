# Index and page map: CI/CD & Build Automation Expert

Convention of this package: **every citation `(SIGLA p.N)` uses the PDF page number** (the PDF reader's count). Printed pages differ in some cases; the map below shows how to convert. Paraphrase; nothing here is the text of the works.

## 1. Sources, nature and dates

| Abbreviation | PDF (in `04_engineering_and_practices/`) | Nature | Date / version | PDF pages | Printed vs PDF |
|---|---|---|---|---|---|
| **CICD** | `CI-CD-DZone-Trend-Report-2021.pdf` | **Trend report** (collection of articles, DZone survey of May 2021 with 695 responses, sponsor announcements and case studies). **Not a book.** | Jun/2021 | 67 (p.19, 54, 64 have no useful text; p.26, 33, 41, 46, 49, 59, 67 are advertisements) | same (footer "PAGE N") |
| **GRADLE** | `Gradle-Cookbook-JavaCodeGeeks.pdf` (internal title: *Gradle Build Automation Handbook*) | **Collection of tutorials** (8 chapters, JavaCodeGeeks/Exelixis Media). Describes **Gradle 2.3** (2015), Eclipse Luna, JDK 1.7. | 2016 | 78 | body: **printed = PDF − 8** (e.g., "1 / 70" is on PDF p.9); cover and table of contents in Roman numerals |
| **GHA** | `GitHub-Actions-Guide.pdf` | 7-page **refcard** (DZone Refcard no. 373, Justin Albano). Uses `actions/checkout@v2`, `openjdk:11`, deploy to Azure. | Feb/2022 | 7 (p.2 is an advertisement) | same |
| **SWE-G** | `Software-Engineering-at-Google-completo.pdf` | **Complete book** (O'Reilly, 2020; online version CC BY-NC-ND), exported as **408 pages with no printed number**. Chapters used: 18 (Build Systems), 22 (Large-Scale Changes), 23 (Continuous Integration), 24 (Continuous Delivery). | 2020 | 408 | **there is no printed page in the PDF**; the pages of the paper book do not correspond |

Not used: `Software-Engineering-at-Google.pdf` (20 pages) is a different text (article by Fergus Henderson, 2017); it is not a source of this package.

### SWE-G page map (PDF)
| Chapter | PDF pages |
|---|---|
| 18 Build Systems and Build Philosophy | p.260-277 |
| 22 Large-Scale Changes | p.316-329 |
| 23 Continuous Integration | p.330-346 (TL;DR p.345; footnotes p.345-346) |
| 24 Continuous Delivery | p.347-353 |

> **Correction from v1**: v1 cited SWE-G p.215 and p.369-495 (pages that do not exist or are about other subjects in this 408-page PDF) and called chapter 22 "Chapter 20". All those pages were redone.

### GRADLE page map (PDF)
| Topic | PDF pages |
|---|---|
| Preface (DAG, incremental build) | p.7 |
| Ch. 1 "Hello World": what it is, installation, tasks, `dependsOn`, `<<`, commands | p.9-16 |
| Ch. 2 Properties (daemon, `-D`, `-P`, `gradle.properties`) | p.17-24 |
| Ch. 3 GWT (plugins, dependencies, source sets, `buildscript`) | p.25-38 |
| Ch. 4 SourceSets | p.39-49 |
| Ch. 5 OSGi/BNDTools | p.50-61 |
| Ch. 6 Wrapper | p.62-64 |
| Ch. 7 NetBeans | p.65-71 |
| Ch. 8 War plugin and Tomcat | p.72-78 |

### CICD page map (PDF)
| Topic | Pages |
|---|---|
| DZone 2021 survey (TDD/BDD/SOLID, microservices, technical debt, delivery "continuity") | p.5-18 |
| Cloud-native CI/CD (CI, CD vs deployment, blue-green, feature flags, GitOps) | p.21-25 |
| Sponsor advertisements/opinions (CloudBees, Armory, Cloudsmith, Sauce Labs) | p.26-27, 33-35, 40-41, 49-50 |
| Observability and AIOps | p.28-32 |
| Repository-based pipelines (GitHub Actions vs GitLab CI) | p.36-39 |
| Security in CI/CD | p.42-45, 56-58 |
| Infrastructure as code | p.51-53 |
| To automate or not | p.61-63 |
| Vendor case studies | p.20, 47, 55, 60, 65 |

## 2. Thematic map (read only the relevant file)

| Trigger (user question) | File | Main sources |
|---|---|---|
| CI, CD, Big Bang, pipeline stages | [fundamentos-de-ci-cd-e-pipeline.md](fundamentos-de-ci-cd-e-pipeline.md) | GHA p.1-3; CICD p.22-25; SWE-G p.330-334 |
| What Gradle is, tasks, DAG, `dependsOn` | [arquitetura-e-conceitos-do-gradle.md](arquitetura-e-conceitos-do-gradle.md) | GRADLE p.7-16 |
| Build phases, `doLast`, config vs execution | [ciclo-de-vida-e-fases-do-gradle.md](ciclo-de-vida-e-fases-do-gradle.md) | GRADLE p.13, 16 (+ `[extrapolation]`) |
| Plugins, dependencies, SourceSets, incremental, wrapper | [plugins-dependencias-e-build-incremental-gradle.md](plugins-dependencias-e-build-incremental-gradle.md) | GRADLE p.18-45, 62-64, 72 |
| Workflow, job, step, runner, YAML | [github-actions-workflows-jobs-e-steps.md](github-actions-workflows-jobs-e-steps.md) | GHA p.3-5; CICD p.36-38 |
| Deploy to Azure, secrets | [deploy-continuo-e-gestao-de-segredos-gha.md](deploy-continuo-e-gestao-de-segredos-gha.md) | GHA p.6-7; CICD p.43-44, 57 |
| Delivery metrics, DORA | [metricas-dora-e-engenharia-de-entrega.md](metricas-dora-e-engenharia-de-entrega.md) | CICD p.16-17, 34-35; SWE-G p.347, 353 (DORA itself is `[extrapolation]`) |
| Pipeline security, supply chain | [devsecops-e-seguranca-na-cadeia-de-suprimentos.md](devsecops-e-seguranca-na-cadeia-de-suprimentos.md) | CICD p.40, 42-45, 56-58; SWE-G p.269-270 |
| Bazel, hermeticity, presubmit, flaky, canary | [sistemas-de-build-hermeticos-e-ci-no-google.md](sistemas-de-build-hermeticos-e-ci-no-google.md) | SWE-G p.260-277, 330-353 |
| Common mistakes | [casos-e-antipadroes.md](casos-e-antipadroes.md) | several |
| Step-by-step how-to | [procedimentos.md](procedimentos.md) | several |
| Terms | [glossario.md](glossario.md) | several |
| What the sources do NOT say; dated content | [lacunas-e-conteudo-datado.md](lacunas-e-conteudo-datado.md) | audit |

## 3. Scripts (in `scripts/`, Python 3 stdlib, no network, run with `python -I`)
- `cicd_lookup.py` (+ `cicd_index.json`): topic -> source and pages (PDF); returns `NOT COVERED` when the collection does not deal with the subject.
- `gradle_trace.py`: order of the DAG of the `java` plugin tasks and an alert for loose code in the task body (`[extrapolation]` rule, labeled).
- `dora_evaluator.py`: computes the four measures from raw data and compares them with the cluster table of the DORA report 2024 p.13 (**`[extrapolation]`, does not come from this package's sources**) and with the CICD survey numbers (CICD p.34-35).
- `gha_linter.py`: workflow checks; each rule declares its origin (`[from source]`, `[inference]` or `[extrapolation]`).
- Tests: `tests/verify_citations.py` (+ `citation-checks.json`), `tests/audit_tokens.py`, `tests/run_script_tests.py`.
