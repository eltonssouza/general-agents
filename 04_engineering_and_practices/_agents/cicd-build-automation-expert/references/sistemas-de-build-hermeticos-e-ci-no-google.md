# Build systems and CI/CD at scale (Software Engineering at Google)

Convention: `(SWE-G p.N)` = page of the **408-page PDF** (no printed number; see `INDEX.md`). Chapters: 18 Build Systems (p.260-277), 22 Large-Scale Changes (p.316-329), 23 Continuous Integration (p.330-346), 24 Continuous Delivery (p.347-353). The book is from 2020 and describes Google (Blaze/Bazel, TAP, Forge); internal tools are `[DATED]` or Google-specific. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. What a build system is for
- A good build system optimizes two properties: being **fast** (one command and the binary in seconds) and **correct** (anyone, on any machine, gets the same result if the inputs are the same). `[from source]` (SWE-G p.260)
- Most builds at Google are triggered by automation, not by people; code is built, tested and sent to production without human intervention, at different paces per team. `[from source]` (SWE-G p.260)
- Without a build system, the problem scales: an isolated compiler does not manage dependencies across several languages; shell scripts become slow, tedious and dependent on each person's environment. `[from source]` (SWE-G p.261-262)
- "It's all about dependencies": managing dependencies is perhaps the most fundamental task of a build system. `[from source]` (SWE-G p.263)

## 2. Task-based systems
- Ant, Maven, Gradle, Grunt and Rake are cited as task-based: the unit of work is the task, a script that the engineer defines. `[from source]` (SWE-G p.263)
- Ant, cited as an example, was released in 2000. `[from source]` (SWE-G p.264) `[DATED]`
- "Dark side": the system does not know what the scripts do; so it is conservative in scheduling (hard to parallelize), cannot guarantee correct incremental builds (any task may download a file or write a timestamp) and the scripts become hard-to-maintain code. `[from source]` (SWE-G p.265)
- Typical bugs: a change of output location that breaks another task; a removed dependency; assumptions about the machine; a non-deterministic component (downloading a file, timestamp); race conditions. `[from source]` (SWE-G p.266)
- When incremental builds are fragile, people start running `clean` before every build, which defeats the purpose. `[from source]` (SWE-G p.265)

## 3. Artifact-based systems (Blaze/Bazel)
- Instead of the engineer defining tasks, they declare **what** to build (targets, dependencies, few options) and the system decides **how**; BUILD files are declarative manifests. `[from source]` (SWE-G p.266)
- Analogy with functional programming: the build is a function from source files and tools to binaries. `[from source]` (SWE-G p.266-267)
- In a Bazel example, `java_binary` and `java_library` are target types; on a second `bazel build` with no changes, the system exits immediately; with a change to one file, it rebuilds only what is needed and reuses the rest. `[from source]` (SWE-G p.267-268)
- Tools are treated as dependencies (the Java compiler is an implicit dependency of each `java_library`); toolchains give platform independence. `[from source]` (SWE-G p.268-269)
- **Sandboxing**: each action sees only the declared inputs and the outputs produced; the sandbox also restricts network communication; undeclared files written are discarded. `[from source]` (SWE-G p.269)
- External dependencies: a manifest with a cryptographic hash (see `devsecops-e-seguranca-na-cadeia-de-suprimentos.md`). `[from source]` (SWE-G p.269-270)
- **Distributed builds**: *remote caching* (artifacts indexed by the target and the hash of the inputs) and *remote execution*; for the cache to work the build must be **completely reproducible**, that is, the same inputs produce exactly the same output on any machine. `[from source]` (SWE-G p.270-272)
- Chapter conclusion: task-based systems have fundamental problems when scaling; Google believes almost every new project benefits from an artifact-based system from the start; the cost is the loss of flexibility (generic tasks are not written in a real language); migrating from an existing task system can be hard. `[from source]` (SWE-G p.272-273)
- The chapter also observes that Gradle lets you declare a dependency version as "1.+", which makes builds non-deterministic, and that Bazel requires manually declared versions. `[from source]` (SWE-G p.275)
- **Build hermeticity**: the term "hermetic" is defined in the book for **tests** (self-contained test environment, without external dependencies, with more determinism and isolation; SWE-G p.337-338). Applied to builds, the idea is equivalent to declared inputs and tools, no network and reproducible output (SWE-G p.269-271) `[inference]`. "Bit-for-bit identical" and "absence of timestamp" are the package's formulations `[extrapolation]`; the book says "exactly the same output" (p.271) and cites the timestamp as a source of non-determinism (p.265-266).

## 4. CI at scale (chapter 23)
- **Presubmit vs post-submit**: Google's practical rule is to run **only fast, reliable tests** in presubmit; some loss of coverage in presubmit may be accepted, as long as the rest is caught in post-submit and a few rollbacks are accepted; in post-submit, longer times and some instability are accepted. `[from source]` (SWE-G p.334)
- Why not run everything in presubmit: it is expensive, it blocks because of others' flakiness and the repository may change during the test (**mid-air collision**, rare but daily at Google's scale). `[from source]` (SWE-G p.334)
- Most teams run the small (unit) tests in presubmit; larger tests vary by team; hermetic tests reduce instability. `[from source]` (SWE-G p.334)
- In TAP, each team is asked for a fast subset of tests (generally the unit tests) for presubmit; empirically, a change that passes it has a probability of **95% or more** of passing the rest; the average wait time to submit is about **11 minutes**, often in the background. `[from source]` (SWE-G p.340) `[DATED]` (Google numbers from 2020)
- TAP handles more than 50 thousand unique changes per day and runs more than 4 billion test cases per day. `[from source]` (SWE-G p.339)
- **Build Cop**: each team has someone responsible for keeping the tests passing; the most effective tool is **rollback**, preferred to fixing forward; TAP has even done automatic rollback when it has high confidence in the culprit. `[from source]` (SWE-G p.340-341)
- **Culprit finding**: batches of changes; TAP splits the failing batch and runs it in isolation; there are binary search tools. `[from source]` (SWE-G p.340)
- **Continuous build (CB)**: runs build and tests at the head; concepts of *true head* and *green head*; RCs are normally cut at the green head. `[from source]` (SWE-G p.332-333)
- **Release candidate tests and probers**: broader tests run on the RC promoted through environments; the same tests run against production (*probers*). `[from source]` (SWE-G p.334-335)
- **Flaky tests**: they erode trust; some teams use a tool to temporarily remove flaky tests from presubmit while they investigate; another technique is to allow multiple attempts of the test; Google has statistical classification of flakes. `[from source]` (SWE-G p.337; classification p.332). The book does **not** mention "quarantine" as a mandatory policy nor a deadline.
- "CI is alerting": 100% green is expensive; not every test failure indicates a production problem; a policy of "nobody commits if the last CI is not green" can be mistaken when the cause is well understood. `[from source]` (SWE-G p.335-336)
- Takeout case study: sandboxed tests in presubmit prevented 95% of servers broken by bad configuration and reduced nightly deploy failures by 50%; E2E tests moved to post-submit every two hours cut the set of culprits by 12 times. `[from source]` (SWE-G p.342)
- Nothing in the book sets "under 10 minutes" for presubmit; v1 attributed this to SWE-G p.469-472. What exists is "11 minutes of average wait" in TAP (p.340).

## 5. Continuous Delivery (chapter 24)
- Principle: smaller batches result in more quality ("faster is safer"); Google's CD idioms: agility, automation, isolation, reliability, data-driven decisions and **phased rollout**. `[from source]` (SWE-G p.347-348)
- **Flag guarding**: every new feature guarded by a flag; the value can be changed without a new binary; turning a flag on for 100% of users at once is not a good idea. `[from source]` (SWE-G p.349)
- Search's **release train**: from rare weekly releases to a binary in production every two days; "if you miss the train, wait for the next one". `[from source]` (SWE-G p.349-350)
- **Staged rollouts** and representative tests when testing everything is infeasible; A/B of deploys in large apps; "change-neutral releases" when the base is small. `[from source]` (SWE-G p.351-352)
- "Always Be Deploying" as a remedy for release latency at scale. `[from source]` (SWE-G p.352)
- Canarying (deploying to a small percentage of production) is cited as a problem minimizer, with the risk of *version skew* (SWE-G p.331) and as a source of information about crashes or stability, but little about whether the version is better (p.352) `[from source]`. **The book does not describe** automatic SLO-driven canary with instant rollback, nor "1%", nor p95/p99 (v1 attributed this to SWE-G p.483-487); that is `[extrapolation]`.

## 6. Large-Scale Changes (chapter 22, only the introduction was read)
Definition: a set of logically related changes that cannot in practice be submitted as an atomic unit; at Google, almost always generated by tools; categories: cleaning up anti-patterns, replacing deprecated features, infrastructure improvements (such as a compiler upgrade) and migrating users to a new system. `[from source]` (SWE-G p.316-317). The rest of the chapter (process, tools, testing) was **not audited**.
