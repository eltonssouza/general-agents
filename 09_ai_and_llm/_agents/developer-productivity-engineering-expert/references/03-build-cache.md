# 03. Build cache (ch. 7, DPE p.34-42)

## 3.1 What it is (p.34)
- `[from source]` Build cache stores **build actions** (Gradle tasks, Maven goals) and is different from, and complementary to, the dependency cache/binary repository, which stores dependencies between source code repositories; the build cache speeds up building a single repository (p.34).
- `[from source]` The concept is "relatively new in the Java world", introduced by Gradle in 2017; Google and Facebook have used it internally for years (p.34). `[DATED]` the state of Maven/Gradle/other tools has changed since 2022.
- `[from source]` It is most effective in multi-module builds; modules separate responsibilities, avoid cyclic dependencies and ease a future migration to microservices; more modularization increases "cacheability" (p.34).
- `[from source]` With Maven, a reliable build requires always cleaning the previous output (full rebuild); Gradle is incremental, but branch switching, pulling changes and clean CI builds still rebuild everything (p.34-35). `[DATED]` there have been cache extensions for Maven and distinct tools since then `[extrapolation]`.

## 3.2 How it works (p.36)
- `[from source]` Each action has inputs and outputs; the cache computes a hash of the inputs (sources, classpath, compiler version etc.) to form a key; if an entry exists, the output is copied and the action does not run; otherwise it runs and stores (p.36).
- `[from source]` Examples of a project with 4 modules and 20 actions (p.35-39): changing a public method in module `export-api` (no dependents) runs 20% of the actions; changing a public method in `service` (with dependent `webapp`) runs 40%; changing only a method body in `service` runs 20%, because the compile classpath key considers only the public API (compile avoidance); an implementation change in `core` (which everything depends on) runs 30%; worst case, changing a public method in `core`, runs 65% (p.35-39). The numbers belong to the illustrative example, not to measurements.
- `[from source]` In an implementation-only change, the tests of dependent modules still re-run, because the runtime classpath changes (p.38).

## 3.3 Local vs remote (p.40-41)
- `[from source]` Local cache: a directory on the machine running the build; speeds up local flow and branch switching and strengthens the local *quality gate* (many organizations weaken it because of long builds) (p.40).
- `[from source]` Remote cache shares outputs between the organization's builds; the pattern described: only CI builds write to the remote, while CI and local builds read (p.40). Reduces CI compute and queues caused by a lack of agents; a customer chart shows improved agent availability (p.40-41; figure cannot be extracted).

## 3.4 Effectiveness and sustainment (p.41-42)
- `[from source]` In a single module there is little benefit, except in CI with several jobs over the same changeset; benefits "grow exponentially" with the number and size of modules (p.41). If n is the number of modules and the module is a leaf, rebuilding it costs ~1/n of the full build; typically half of the modules are leaves (p.41).
- `[from source]` To keep the gain: monitor continuously, including infrastructure (download speed of the remote nodes and storage capacity) (p.41).
- `[from source]` **Volatile inputs are the enemy of the cache**: example of a `build.properties` with a timestamp in the jar, which prevents hits in the downstream test (p.41-42). See also reproducibility (07).
- `[from source]` Summary: the author cites average savings of 90% in the company's own projects and a minimum of 50% in organizations that adopted cache (p.42). `[vendor claim]` numbers without methodology or interval; treat as an optimistic order of magnitude.

## 3.5 Supplements from ch. 9 on cache
- `[from source]` Cache is not "fire and forget": teams that turned on the cache without monitoring were disappointed within a few months; without management there can be "negative savings" (p.58). See `05-profiling-e-analytics.md`.
- `[from source]` Causes of low effectiveness: modules that change a lot and have many dependents, actions with non-reproducible output (code generator with timestamp), JVMs from different vendors (p.52, p.57).
