# 06. Failure types and troubleshooting (ch. 10-11, DPE p.60-65)

## 6.1 Verification vs non-verification (p.60-61)
- `[from source]` Build failures block developers and are highly sensitive to repair time, unlike performance problems, which do not block (p.60).
- `[from source]` **Verification failure:** the build detects a real problem in the code. **Non-verification failure:** a problem in the build's own software: faulty build logic, unavailable artifact repositories, faulty build environments, defective external services (p.60).
- `[from source]` Ambiguous language: "broken build" and "the build failed" serve two distinct problems, with undefined responsibilities (p.60).
- `[from source]` Classifying is hard: there are non-failures that look like verification (different versions of the same dependency on the classpath) and verifications that look like non-verification (a snapshot dependency that CI resolves differently from the local build) (p.60-61). Normally whoever started the build bears the failure, even without knowing the type or the responsible party (p.61).
- `[from source]` DPE goals for failures: improve MTTR and engage the right resources; minimize non-verification failures (p.61).

## 6.2 Efficient troubleshooting (p.62-63)
- `[from source]` Thesis: most disruptions are easy for whoever has context; what is missing is a comprehensive, organized record of what happened in the build (participating tools, dependencies, repository, timings). This record helps distinguish whether the cause is infrastructure (build/CI team) or code (developer) (p.62).
- `[from source]` Critical aspects to record: build environment (hardware, OS), toolchain (services that run binaries), inputs (tools, projects and libraries, source code state, configuration) and outputs (problems detected, debugging information, timings per component, best practices followed); the record must be navigable and have deep links (p.62-63).
- `[from source]` "Staggering waste" anecdote: without tooling, the common approach is to run the build again hoping for flakiness, then clear caches, and only then ask for help; build engineers also lack data (p.63).

## 6.3 Build Scan as an example (p.64-65)
- `[from source]` The book describes the Build Scan as an "X-ray" of the build, with per-task data and graphical views for root-cause analysis, also useful with failure analytics (ch. 13) and with the cache (ch. 7) (p.64). `[vendor claim]` "de facto standard" is self-praise.
- `[from source]` Data from large open source projects: typically 2%-5% of builds fail for reasons unrelated to the developer (p.64); 3%-10% of test builds fail because of test infrastructure problems, varying with reliance on integration tests (p.64). The primary source of these data is not detailed.
- `[from source]` Test history answers "was it me? do I need to fix it now? is it flaky?" by showing whether that failure is recent and isolated; many CIs show only the isolated failure; capturing local failures too allows comparing a failed local build against a passing CI build (p.64-65).
- `[from source]` Comparing the Build Scan of a failed build and a successful one eliminates root-cause dimensions (dependency conflicts, inputs, environment) and reduces MTTR (p.65).
- `[from source]` Summary: comprehensive toolchain, input and output data, combined across multiple builds, give the historical picture (p.65).

## 6.4 Use by the agent
To classify a failure, ask: (1) what changed since the last success? (2) did it fail the same way in another environment/CI? (3) is it the first occurrence or is there history? `[inference]` from p.64-65. For prioritization use `07-confiabilidade-e-flaky.md` §7.3.
