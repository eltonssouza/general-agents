# Practical cases, common failures and anti-patterns of CI/CD and build

Convention: `(SIGLA p.N)` = **PDF** page. Each item says what the sources support and what is extrapolation. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Big Bang Integration
- **Problem**: working on isolated parts and integrating everything at once; the integration "never worked as expected" and took days or weeks. `[from source]` (GHA p.3)
- **Remedy**: automate tests and integrate at least once a day, preferably on every check-in. `[from source]` (GHA p.3)

## 2. Long-lived branches and isolated sub-teams
- **Problem**: a sub-team creates a branch so as not to disturb the others and later suffers with integration and with hunting for the culprit. `[from source]` (SWE-G p.348)
- **Remedy at Google**: keep developing at the shared head, with CI, automatic rollbacks and culprit finding. `[from source]` (SWE-G p.348). The report also points to feature flags as an alternative to several long-lived branches (CICD p.23) and to small, short-lived branches (CICD p.24, 50). `[from source]`

## 3. Expensive, rare releases
- **Problem**: if each release requires a lot of work (the YouTube example has a manual regression cycle of 50 hours per release), the release is postponed to test more, one more feature gets in and the cycle gets worse; the experts burn out. `[from source]` (SWE-G p.348)
- **Remedy**: reduce cost, increase discipline and make the risk incremental; the book says the obvious operational fixes (more governance, more risk reviews) have a lower return than long-term architectural changes, such as migrating to microservices. `[from source]` (SWE-G p.348)

## 4. Task-based build with non-deterministic effects
- **Problem**: tasks that download files from the internet or write timestamps produce different results on each run and make it impossible to reproduce failures and to use a cache. `[from source]` (SWE-G p.266, 265)
- **Remedy**: artifact-based system (Bazel) with sandbox and dependencies by hash. `[from source]` (SWE-G p.269-270). In an ordinary Gradle build, the equivalent practice is to keep inputs and outputs declared and to avoid timestamps in generated content `[extrapolation]`.

## 5. Uncontrolled external dependencies
- **Problem**: depending on files outside the workspace can cause irreproducible builds ("works today, breaks tomorrow") and a security risk; floating versions such as Gradle's `1.+` violate determinism. `[from source]` (SWE-G p.269-270, 275)
- **Remedy**: record the hash and version in the repository and mirror the dependencies on trusted servers. `[from source]` (SWE-G p.270)

## 6. Trying to run everything in presubmit
- **Problem**: it is expensive, it blocks people because of other people's instability, and the repository may change during the test. `[from source]` (SWE-G p.334)
- **Remedy**: presubmit with only fast, reliable tests; the rest in post-submit, with failure management and rollbacks. `[from source]` (SWE-G p.334, 340)

## 7. Living with flaky tests
- **Problem**: unstable tests erode trust as much as broken tests do and make it harder to find the commit to revert. `[from source]` (SWE-G p.337)
- **Remedy**: some teams temporarily remove the flaky test from presubmit while they investigate and fix it; retries are also allowed; known failures are marked with a bug and tracked (the Takeout case uses bug tags to keep the suite green in a responsible way). `[from source]` (SWE-G p.337, 344)
- Note: "immediate quarantine" and "open a high-priority ticket" from v1 are **not** statements from the book `[extrapolation]`.

## 8. Credentials in code or in YAML
- **Problem**: secrets in CI/CD configuration files are exposed to abuse; misuse of credentials is one of the most exploited points. `[from source]` (CICD p.43-44)
- **Remedy**: keep secrets in a controlled place, group them by access level, prefer short-lived secrets; in GitHub Actions, reference them via `${{ secrets.NOME }}` as in the refcard examples. `[from source]` (CICD p.43-44; GHA p.6-7)

## 9. Third-party action pointing to a mutable ref
- **Problem**: using `@main`/`@master` lets a compromise of the action's repository change what your pipeline runs. `[extrapolation]` (the GHA/CICD sources do not cover this; SWE-G p.270 covers build dependencies by hash `[inference]`).
- **Remedy**: pin to the full commit SHA. `[extrapolation]`

## 10. Mixing Delivery with Deployment, automating the wrong process
- **Problem**: lack of experience leads to automating the wrong process, misconfiguring CI and confusing the two concepts. `[from source]` (CICD p.56)
- **Remedy**: roles per pipeline stage; training and coaching. `[from source]` (CICD p.56)

## 11. Poorly configured shared test environment
- **Problem**: test failures and faulty deploys caused by bad configuration of a shared environment. `[from source]` (CICD p.57)
- **Remedy**: on-demand test environments in the cloud (and, in the report, *preview environments* per pull request). `[from source]` (CICD p.57, 23)

## 12. Automating everything without criteria
- **Problem**: automation can cost more than it is worth; tasks done once, or that call for human creativity (accessibility, code review, a second authentication factor), should not always be automated. `[from source]` (CICD p.53, 63)
- **Remedy**: prioritize what repeats weekly or daily; follow steps (manual, document, test the document, automate, orchestrate, test and adjust). `[from source]` (CICD p.52-53; DevOps checklist in CICD p.61-62)

## 13. Continuous Delivery without feedback loops
- **Problem**: focusing only on release frequency or feature velocity can increase technical debt. `[from source]` (CICD p.13)
- **Remedy**: complement with feedback, code review that requires tests (PRs rejected for lack of tests correlate with lower perceived technical debt: 62.9% versus 54.5%) and coverage goals. `[from source]` (CICD p.13-14, 16) (correlation, not causation `[inference]`)

## 14. Rebuilding the artifact for each environment
- **Problem**: recompiling when promoting the RC through environments reduces the fidelity of the tests. `[from source]` (SWE-G p.333)
- **Remedy**: promote the same artifact (containers help keep consistency). `[from source]` (SWE-G p.333)

## 15. Executable code loose in the body of a Gradle task
- **Problem**: side effects run in the configuration phase on every build. `[extrapolation]` (see `ciclo-de-vida-e-fases-do-gradle.md`).
- **Remedy**: move it to `doLast`. `[extrapolation]`; the book puts executable code inside `<<`/`doLast` (GRADLE p.13, 16). `[from source]`

## 16. False negatives from security tools
- **Problem**: tools suffer from false positives and false negatives; the negatives give a false sense of security. `[from source]` (CICD p.57)
- **Remedy**: prepare the tool's integration, justify false positives and take every alert seriously. `[from source]` (CICD p.57)
