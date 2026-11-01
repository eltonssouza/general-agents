# Gaps (what the sources do NOT say) and dated content

Convention: `(SIGLA p.N)` = **PDF** page. This list comes from the audit: these are claims that v1 attributed to the sources as `[from source]` without basis. Use it to answer "the book does not cover this" and to label. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Not in the sources (label `[extrapolation]` or say there is no coverage)
| Topic | Situation in the sources |
|---|---|
| DORA metrics (definitions, Elite/High/Medium/Low bands) | Only a passing mention of the four metrics (CICD p.16), with no definition or number |
| Three Gradle phases (Initialization, Configuration, Execution), `settings.gradle`, `doFirst` | Absent from the GRADLE PDF (Gradle 2.3) |
| Cycle detection in the DAG, automatic parallelism of independent branches | Absent (only "DAG" in the Preface, GRADLE p.7) |
| Hash of inputs/outputs, local/remote build cache, `--profile`, `--scan` | Absent; the book only shows `UP-TO-DATE` and the `options.incremental` option (GRADLE p.7, 33-34) |
| `implementation` vs `api`, Kotlin DSL, `plugins {}` block | Absent; the book uses `apply plugin:` and `compile` (GRADLE p.25, 33) `[DATED]` |
| Pinning of actions by SHA, `@main`/`@master`, `permissions:` | Absent from GHA and CICD |
| `pull_request`, `workflow_dispatch`, `schedule`, `concurrency`, `cancel-in-progress`, `timeout-minutes`, `environment`, `cache:` | Absent from GHA and CICD |
| Masking of secrets in logs, NaCl/Libsodium encryption, organization/repository/environment secrets, protection rules | Absent |
| Ephemeral runners "destroyed after each job" | GHA says only that the runner can be hosted by GitHub or your own (p.4) |
| "Launched in 2019" | GHA p.3 says **November 2019** (correct); the v1 package omitted the month |
| Presubmit "under 10 minutes" | Not stated; the book cites an average wait of ~11 min (SWE-G p.340) |
| Automatic SLO-based canary with instant rollback; 1%/5%; p95/p99; "error budget" to abort a release | Absent; SWE-G cites canarying, staged rollouts and A/B of deploys (p.331, 351-352); "error budget" only as an analogy with SRE (SWE-G p.336, 346, 353) |
| Quarantine of flaky tests with a high-priority ticket | Absent; there is "temporarily remove from presubmit" (SWE-G p.337) and bug tags (p.344) |
| Bit-for-bit identical, "absence of timestamp" as the definition of build hermeticity | The book says "exactly the same output" (SWE-G p.271); hermetic is defined for tests (p.337-338) |
| Tricorder (static analysis in presubmit) | Cited in other SWE-G chapters (for example p.289-296), not in chapters 18, 23 and 24 |
| Trivy, Clair, SBOM as a pipeline tool, SCA | SBOM appears only in the CICD p.40 advertisement; Trivy/Clair/SCA absent |
| GitHub Actions "organization secrets", Azure ACR/AWS ECR/ECS/Kubernetes as targets | Only Azure (container registry and App Service) in GHA p.6-7 |
| Maven, Ant and Gradle "compared in detail" | Only a summary in the Preface and in ch. 1 (GRADLE p.7, 9) and the "task-based" classification (SWE-G p.263) |

## 2. Dated content
- **GRADLE**: Gradle 2.3 and JDK 1.6 (GRADLE p.9); Eclipse Luna (GRADLE p.26); `task nome << { }`, an operator removed later (GRADLE p.13); `compile` (GRADLE p.25); `testCompile` (GRADLE p.41); `output.classesDir` (GRADLE p.43); daemon via `GRADLE_OPTS` (GRADLE p.17-18); `jetty` and `gwt` plugins (GRADLE p.33-34); `jcenter()` (GRADLE p.33); Tomcat plugin 2.0 (GRADLE p.74). `[DATED]`
- **GHA**: `actions/checkout@v2`, `upload-artifact@v2`, `azure/login@v1`, `openjdk:11`, Azure CLI's `--sdk-auth` and `Settings → Secrets` (GHA p.4-7). `[DATED]` Check the current documentation.
- **CICD**: May 2021 survey (695 responses); numbers from the "State of Continuous Delivery 2021" via a sponsor (p.34-35); Mabl 53%/38% (p.42); commercial tools (HCL Launch, Cloudsmith, Pantheon, Sauce Labs, Worksoft, GitLab, Opsera, Armory, CloudBees). `[DATED]`
- **SWE-G**: Google numbers from 2020 (TAP, 50 thousand changes/day, 11 minutes, 95%); internal names TAP, Forge, ObjFS, Critique, Borg, Rapid. `[DATED]`

## 3. Nature of the sources (weight of the claims)
- **SWE-G** is a book authored by Google engineers (reviewed, with an editor). It describes Google; generalizing is `[inference]`.
- **CICD** is a trend report: DZone survey (p.5-18, correlations from a sample of 695 responses) and articles by contributors and **sponsor content** (p.27, 34-35, 40-41, 50). Sponsor claims are promotional and without method.
- **GHA** is an introductory 7-page refcard (tutorial with Azure), not a complete GitHub Actions reference.
- **GRADLE** is a collection of tutorials based on Gradle 2.3 (2015/16), not the Gradle manual.
