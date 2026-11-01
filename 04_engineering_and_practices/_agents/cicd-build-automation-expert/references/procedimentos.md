# Operating procedures

Convention: `(SIGLA p.N)` = **PDF** page. Each step carries the label of its origin. Where a step comes from the package (and not from the sources), it is marked `[extrapolation]` and must be checked against the current documentation. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## Procedure 1: CI workflow in GitHub Actions
**Goal**: a workflow that builds and tests on every push.
1. Create `.github/workflows/<name>.yml` in the repository. `[from source]` (GHA p.4; CICD p.36)
2. Declare `name` (optional), `on` (trigger, for example `[push]`) and `jobs`. `[from source]` (GHA p.4)
3. In each job, define `runs-on` and `steps`; start with the checkout, because the state of the runner is unknown. `[from source]` (GHA p.4-5)
4. Use `run:` for shell commands and `uses:` for actions; with more than one command, use `|`. `[from source]` (GHA p.5)
5. Separate build and test into jobs and use `needs:` to order them; keep the artifact with `upload-artifact` and download it in later jobs. `[from source]` (GHA p.4-7)
6. Harden (`[extrapolation]`, does not come from the sources; check the current GitHub documentation):
   - `permissions: contents: read` at the top, widening only where necessary;
   - pin third-party actions to the full commit SHA (or, at the very least, to a version tag);
   - `timeout-minutes` per job;
   - `concurrency` with `cancel-in-progress: true` to cancel redundant runs;
   - dependency caching (for example, `cache: gradle` in the Java setup action).
   Example (labeled, illustrative versions):
```yaml
# [extrapolation] package example; confirm versions and syntax in the current documentation
name: ci
on: [push, pull_request]
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '17', cache: gradle }
      - run: ./gradlew build
```

## Procedure 2: diagnose a slow Gradle build or one without `UP-TO-DATE`
1. Understand what the book shows: the Preface says Gradle skips what is up-to-date (GRADLE p.7); the outputs display `UP-TO-DATE` per task (GRADLE p.44-47, 75). `[from source]`
2. View tasks and properties: `gradle tasks`, `gradle properties` and the `dependencies` task (GRADLE p.15, 21). `[from source]` Increase verbosity with `--info` or `--debug`, `-q` to silence (GRADLE p.13-14). `[from source]`
3. Enable the daemon and compare times (the book shows the effect, GRADLE p.17-20), and consider `org.gradle.parallel` (GRADLE p.20). `[from source]` `[DATED]` (the default changed in modern versions `[extrapolation]`)
4. For large builds, enable `options.incremental = true` in the Java compilation (GRADLE p.33-34). `[from source]`
5. Steps with no basis in the sources, `[extrapolation]`: `./gradlew build --profile` (timing report), `--scan`, inspecting the declared inputs/outputs of tasks and avoiding timestamps in generated content (reduces cache invalidation).
6. Standardize the Gradle version with the **Wrapper** and version its files (GRADLE p.62-64). `[from source]`

## Procedure 3: assess delivery (metrics) honestly
1. Choose **one application or service** and a period. `[extrapolation]`
2. Collect: deploys to production; commit→production time; restoration time; failed deploys. `[extrapolation]` (the sources do not define the metrics; see `metricas-dora-e-engenharia-de-entrega.md`)
3. Run `python -I scripts/dora_evaluator.py ...` (compares with the table of the DORA report 2024 p.13, `[extrapolation]`, and with the CICD survey numbers (CICD p.34-35), `[from source]`).
4. Interpret with caution: the clusters emerge from the year's data, they are neither thresholds nor a maturity model. `[extrapolation]`
5. Actions supported by the sources: smaller batches and frequent release (SWE-G p.347, 353); fast, reliable presubmit (SWE-G p.334); feature flags (CICD p.23; SWE-G p.349); fast rollback (SWE-G p.340-341). `[from source]`

## Procedure 4: automate a process (CICD checklist)
1. Execute by hand and learn. 2. Document. 3. Code/script. 4. Create tests. 5. Review by another person. 6. Publish. 7. Monitor. 8. Retrospective. `[from source]` (CICD p.61-62)
For infrastructure: try it manually; document; **test the document**; automate; orchestrate in a pipeline; test and adjust. `[from source]` (CICD p.52-53)

## Procedure 5: review a pipeline's security
1. Secrets: nothing in configuration files; access by level; short-lived. `[from source]` (CICD p.43-44)
2. Who can change the pipeline configuration and when it was last reviewed. `[from source]` (CICD p.57)
3. SAST before deploy and DAST on the running application; continuous monitoring. `[from source]` (CICD p.44-45)
4. False positives justified; false negatives as a risk. `[from source]` (CICD p.57)
5. Dependencies by hash and own mirror (build). `[from source]` (SWE-G p.270)
6. Pin actions by SHA and declare minimal `permissions`. `[extrapolation]`
7. Run `python -I scripts/gha_linter.py --file <workflow.yml>` (each rule declares its origin).
