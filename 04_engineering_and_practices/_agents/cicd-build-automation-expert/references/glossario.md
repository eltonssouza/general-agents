# Glossary of CI/CD, Gradle and build automation

Convention: `(SIGLA p.N)` = **PDF** page (see `INDEX.md`). Each entry says where the term is covered; no page = the term is not defined in the sources (`[extrapolation]`). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

### A
- **Action (GitHub Actions)**: a pre-packaged set of procedures executed inside a step. `[from source]` (GHA p.4)
- **Artifact-based build system**: a system in which the engineer declares what to build and the system decides how; examples Blaze and Bazel (and Pants, Buck). `[from source]` (SWE-G p.266)

### B
- **Big Bang Integration**: late integration of parts tested in isolation; takes days or weeks. `[from source]` (GHA p.3)
- **Blaze / Bazel**: Blaze is Google's build system; Bazel is the open version (2015). `[from source]` (SWE-G p.260)
- **Blue-green deployment**: two production environments; traffic switches between them; rollback by returning the traffic. `[from source]` (CICD p.22)
- **Build Cop**: the team member responsible for keeping the tests passing; prefers rollback to fixing forward. `[from source]` (SWE-G p.340)

### C
- **Canarying**: deploying first to a small percentage of production. `[from source]` (SWE-G p.331)
- **Continuous Build (CB)**: integrates the changes at the head and runs build and tests. `[from source]` (SWE-G p.332)
- **Continuous Delivery**: in CICD, automating the release up to production-ready code, which goes to production after manual testing or approval; in SWE-G, continuous assembly of release candidates and promotion through environments. `[from source]` (CICD p.22; SWE-G p.333)
- **Continuous Deployment**: if the code passes through all the stages, it is deployed automatically, without manual intervention. `[from source]` (CICD p.22)
- **Continuous Integration (CI)**: integrating work frequently, with automated build and tests that detect integration errors early. `[from source]` (SWE-G p.330; GHA p.3)
- **Culprit finding**: finding which change broke a test. `[from source]` (SWE-G p.340)

### D
- **DAG**: the directed acyclic graph with which Gradle decides the order of tasks. `[from source]` (GRADLE p.7)
- **DAST / SAST**: dynamic and static security testing. `[from source]` (CICD p.44-45)
- **DevSecOps**: integration of security into the development and operations stages; linked to shift left. `[from source]` (CICD p.43)
- **DORA (metrics)**: not defined in the sources. `[extrapolation]` (see `metricas-dora-e-engenharia-de-entrega.md`)

### E
- **Event**: the stimulus that triggers a workflow. `[from source]` (GHA p.4)

### F
- **Feature flag**: turns a feature on/off in production without changing the code. `[from source]` (CICD p.23; SWE-G p.349)
- **Flaky test**: the book deals with unstable tests that erode trust. `[from source]` (SWE-G p.337)

### G
- **GitOps**: an operating model driven by declarative configuration and IaC, with Git as the single source of truth. `[from source]` (CICD p.25)
- **Gradle Wrapper**: a script that downloads and configures Gradle; version it in the repository. `[from source]` (GRADLE p.62-64)
- **Green head / true head**: the latest change verified by the continuous build / the latest committed change. `[from source]` (SWE-G p.332)

### H
- **Hermetic test**: a test against a self-contained environment, with no external dependencies; more determinism and isolation. `[from source]` (SWE-G p.337-338)

### I
- **Incremental build**: redoing only what is out of date; in Gradle, `UP-TO-DATE` tasks. `[from source]` (GRADLE p.7)
- **Infrastructure as Code (IaC)**: managing infrastructure through machine-readable files. `[from source]` (CICD p.44)

### J
- **Job (GitHub Actions)**: a set of steps on the same runner; parallel to each other by default. `[from source]` (GHA p.3)

### M
- **Mid-air collision**: two changes to different files that, together, break a test. `[from source]` (SWE-G p.334)

### P
- **Pipeline**: an ordered set of stages in series and in parallel. `[from source]` (GHA p.3)
- **Pinning of actions by SHA**: current GitHub practice; not in the sources. `[extrapolation]`
- **Presubmit / Post-submit**: tests before / after the change is submitted. `[from source]` (SWE-G p.334)
- **Project / Task (Gradle)**: the two top-level concepts; a task is the minimum unit of work. `[from source]` (GRADLE p.13)

### R
- **Release candidate (RC)**: a cohesive, deployable unit assembled automatically from code, configuration and dependencies that passed the continuous build. `[from source]` (SWE-G p.333)
- **Runner**: a server that executes jobs, hosted by GitHub or your own. `[from source]` (GHA p.4)

### S
- **Sandbox (Bazel)**: isolates each action from the file system and the network. `[from source]` (SWE-G p.269)
- **Shift left**: handling quality and security earlier in the lifecycle. `[from source]` (CICD p.22-23, 43)
- **SourceSet (Gradle)**: a collection of source files and resources compiled together. `[from source]` (GRADLE p.26, 39)
- **Step**: a task of one or more shell commands or actions. `[from source]` (GHA p.3)

### T
- **Task-based build system**: a system in which the unit of work is the script task; Ant, Maven, Gradle, Grunt, Rake. `[from source]` (SWE-G p.263)
- **Trunk-based development**: integrating at the head/trunk; the book notes that "head" is also called master, mainline or trunk. `[from source]` (SWE-G p.346)

### U
- **UP-TO-DATE**: the mark Gradle prints next to tasks that did not need to run. `[from source]` (GRADLE p.44-47)

### V
- **Version skew**: a state in which a distributed system has several incompatible versions of code, data or configuration. `[from source]` (SWE-G p.331)

### W
- **Workflow**: a series of automated GitHub Actions procedures, defined in YAML in `.github/workflows/`. `[from source]` (GHA p.3-4; CICD p.36)
