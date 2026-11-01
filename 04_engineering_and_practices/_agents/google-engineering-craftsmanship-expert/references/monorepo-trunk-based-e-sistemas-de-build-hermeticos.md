# Monorepo, Trunk-Based Development, Dependencies and Build Systems (SWE-G Ch. 16, 17, 18 and 21)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`. Ch. 16 "Version Control and Branch Management" (PDF p.231-246, Titus Winters), Ch. 17 "Code Search" (p.247-259), Ch. 18 "Build Systems and Build Philosophy" (p.260-278, Erik Kuefler), Ch. 21 "Dependency Management" (p.297-315, Titus Winters).

## 1. Version control and source of truth (Ch. 16)
- [from source] (SWE-G p.231) The authors consider "trunk-based development" (one repository, no dev branches) a particularly scalable policy.
- [from source] (SWE-G p.232) A VCS extends the file system by mapping (file, time, branch) to content.
- [from source] (SWE-G p.234-235) Centralized vs distributed VCS (DVCS). The book says Google's main repository is a very large internal centralized VCS and that attempts to migrate to Git ran into size and Hyrum's Law effects (p.235).
- [from source] (SWE-G p.235-236) "Source of truth": even in a well-managed DVCS, one branch in one repository is declared the source of truth.
- [from source] (SWE-G p.237) Work in progress is equivalent to a branch.
- [from source] (SWE-G p.237-238) Dev branches: the authors believe that a policy that uses dev branches to obtain stability is "inherently misguided"; stability is better solved with tests, CI and code review. Alternative: trunk-based, rely on tests and CI, keep the build green and disable incomplete or untested functionality at runtime (p.238).
- [from source] (SWE-G p.238) Release branches are generally benign; fixes are cherry-picked from the trunk; in high-performing organizations identified by DORA, release branches are practically nonexistent.
- [from source] (SWE-G p.239) Google data: a monorepo shared by about 50,000 engineers, with the Piper VCS (more than 80 TB of content and metadata; 60,000 to 70,000 commits per working day). OWNERS files per directory. The book does NOT describe "CitC" in this chapter (the acronym does not appear in the PDF); workspaces are mentioned in Ch. 19 (p.283: FUSE-based file system).
- [from source] (SWE-G p.239-240) One-Version: "for every dependency in the repository there should be only one version to choose from"; example of the Abseil fork that breaks due to duplicated dependencies; shading works for functions but not for types.
- [from source] (SWE-G p.240) "One-Version Rule": developers should never have the choice of "which version of this component should I use?" (the rule is "not rigid" in practice, note 11 on p.246).
- [from source] (SWE-G p.241) Avoid long branches; only a few of the roughly 1,000 teams have a long dev branch, for unusual compatibility-over-time reasons; six-month "build horizon" (every job in production is rebuilt and redeployed within at most six months).
- [from source] (SWE-G p.242-243) The book does not claim the monorepo is "the only way": it discusses pros and cons and the alternative of the virtual monorepo (VMR). What matters is following One-Version.
- [from source] (SWE-G p.244-245) TL;DR: use a VCS; choices about which version to depend on do not scale; trunk-based development is a predictive factor in high-performing organizations (DORA); long dev branches are not a good default.
- Fidelity note: the v1 package attributed the chapter to Rachel Potvin and spoke of "5,000 consumers updated in one transactional operation" (p.235) and of "Live at Head" as a consequence of the monorepo (p.234, p.297). The chapter is by Titus Winters; the article by Potvin and Levenberg is only cited (note 15, p.246); "5,000 consumers" does not appear; "Live at Head" is one of the dependency models of Ch. 21 (p.303), not of Ch. 16.

## 2. Code Search (Ch. 17), the essentials only
- [from source] (SWE-G p.247) Code Search is the tool for browsing and searching code; the integration with Kythe/Grok brought cross-references. Principle: "answer the next question about the code in one click". TL;DR (p.258): helping developers understand code gives a large productivity gain.

## 3. Build: tasks vs artifacts (Ch. 18)
- [from source] (SWE-G p.260) Purpose of a build system: transform source code into binaries; it must be fast and correct (same result on any machine with the same inputs). Blaze is the internal system; Bazel is the open version (2015).
- [from source] (SWE-G p.263-266) Task-based systems (Ant, Maven, Gradle, Grunt, Rake) give "too much power to the engineer and too little to the system": difficulties with parallelization, incremental builds and script maintenance.
- [from source] (SWE-G p.266-267) Artifact-based systems (Blaze, Bazel, Pants, Buck): BUILD files are declarative manifests of artifacts, dependencies and options; the "how" is left to the system; analogy with functional programming.
- [from source] (SWE-G p.267-268) Example of a BUILD with `java_binary` and `java_library`; the build assembles a dependency graph between artifacts; since each target runs only one compiler, it is safe to parallelize and reuse outputs.
- [from source] (SWE-G p.268-269) Tools as dependencies (toolchains); rules and actions declare inputs and outputs; sandboxing prevents actions from reading undeclared files and restricts network access (p.269).
- [from source] (SWE-G p.269-270) Deterministic external dependencies: a manifest with the cryptographic hash of each external dependency; updating must be a conscious and centralized choice; mirroring dependencies on servers under control is recommended.
- [from source] (SWE-G p.270-271) Distributed builds: remote caching (artifacts indexed by the target and by a hash of the inputs; requires reproducible builds) and remote execution (p.271-272). At Google since 2008; ObjFS (cache) and Forge (execution) (p.272).
- [from source] (SWE-G p.273-274) Fine-grained modules and the "1:1:1 rule" (section title on p.273; the details were not audited here); target visibility (p.274).
- [from source] (SWE-G p.275-277) Internal vs external dependencies; automatic version management is a "recipe for disaster" in non-trivial projects (p.275); transitive dependencies and the One-Version rule (p.276); mirroring, hashing and vendoring (p.277); Google vendors into a `third_party` directory.
- Fidelity note: the word "hermetic" is NOT used in Ch. 18 (a text search of the PDF returns no occurrences on p.260-277). The term appears in the testing chapters (p.155, p.192, p.208) and the CI chapter (p.337-339). The v1 package spoke of "hard prohibitions: no network, no environment variables, no clock" and of "the cryptographic hash determines with 100% certainty the artifact's hash" (p.265-274). The book says: the sandbox restricts undeclared files and network (p.269); the remote cache requires that the same inputs produce the same output (p.271); "nothing prevents an action author from introducing a nondeterministic process" (p.269). "Millions of hours saved per day" is not in it.

## 4. Dependency management (Ch. 21), the essentials only
- [from source] (SWE-G p.297) Dependency management deals with libraries and packages that the organization does not control; it is one of the "least understood" problems in software engineering.
- [from source] (SWE-G p.303) Models listed with stability properties: Nothing Changes, SemVer, distribution bundle and "Live at Head".
- [from source] (SWE-G p.314) TL;DR: prefer version control problems to dependency management problems; SemVer is a "lossy" estimate of risk; tests and CI give real evidence.

## 5. What was NOT audited in depth
- Sections of Chs. 17, 18 and 21 outside the pages cited above (for example, Live at Head in detail, p.304-313) were not read in full in this audit.
