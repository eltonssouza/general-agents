# Plugins, dependencies, SourceSets, incremental build and Wrapper in Gradle

Convention: `(GRADLE p.N)` = **PDF** page (printed = PDF − 8). Everything is from **Gradle 2.3 (2015)**: the `compile`, `testCompile` and `apiCompile` configurations that the book uses are `[DATED]` (later versions replaced them; check the current documentation). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Plugins
- Gradle offers a set of basic tasks (generate WAR, copy files, create directories); in more complex projects plugins are added with `apply plugin:'NAME'` at the top of the script. `[from source]` (GRADLE p.25)
- GWT example: plugins `war`, `java`, `eclipse` and tasks `compileJava` (javac), `classes`, `jar`, `war`, `eclipse`. `[from source]` (GRADLE p.25)
- In the chapter 3 script: `apply plugin: 'war'`, `'java'`, `'gwt'`, `'eclipse'`, `'jetty'`; `war` adds WAR assembly, `java` is the base for the others and gives the ability to compile and test, `eclipse` generates configuration for the Eclipse project, `jetty` deploys the WAR directly. `[from source]` (GRADLE p.33-34)
- The `gwt` plugin comes from a third-party dependency (Steffen Schaefer's plugin) declared in `buildscript`; the Tomcat plugin is by Benjamin Muschko. `[from source]` (GRADLE p.26, 34, 37, 74-75). That is, there are plugins that ship with Gradle and third-party plugins downloaded from a repository `[inference]`; the "core vs community" division into formal categories is not made in the book.
- `war` plugin: adds the `war` task, which copies files keeping the project structure; adds the `providedCompile` and `providedRuntime` configurations (dependencies not packaged in `WEB-INF/lib`); default directory `src/main/webapp`, changeable with `webAppDirName`. `[from source]` (GRADLE p.72)
- The embedded Tomcat plugin serves for testing WARs; to deploy to a remote server the book cites the `cargo` plugin. `[from source]` (GRADLE p.78)

## 2. Dependencies and repositories
- Dependency management is described as a critical feature: centralizing and automating the management of libraries, including automatic search and detection of transitive dependency conflicts. `[from source]` (GRADLE p.25)
- Example `[DATED]`: `dependencies { compile 'com.google.gwt:gwt-user:2.7.0' }` (GRADLE p.25). In SourceSets: `apiCompile`, `implCompile`, `testCompile` (GRADLE p.41). `[from source]`
- The `repositories { mavenCentral() }` block indicates where Gradle looks for dependencies; in the example, the GWT libraries come from the Maven central repository, and the outputs show `Download https://repo1.maven.org/...`. `[from source]` (GRADLE p.33-34)
- The block `buildscript { repositories { jcenter() } dependencies { classpath '...' } }` declares dependencies of the build itself; it accepts only `classpath`. `[from source]` (GRADLE p.33-34) (`jcenter()` was deprecated later `[extrapolation]`.)
- Downloaded libraries are kept in the `caches/modules-2/files-2.1` directory inside the Gradle home (GRADLE p.38). `[from source]`
- **`implementation` vs `api`**: **not in the book**. The `implementation`/`api` configurations appeared in versions later than Gradle 2.3 and replaced `compile`; the idea is that `implementation` does not expose the dependency on the module's consumer classpath, reducing cascading recompilation. `[extrapolation]` (v1 attributed this to GRADLE p.17-18; an error).

## 3. SourceSets
- A source set is a collection of source files compiled together; for the Java plugin, the default directories are `src/main/java`, `src/main/resources`, `src/test/java` and `src/test/resources`. `[from source]` (GRADLE p.26)
- Chapter 4 definition: a collection of Java files and resources compiled and assembled together; the idea is to group files of the same meaning without having to separate them into another project. `[from source]` (GRADLE p.39)
- A new source set (`api`, `impl`) automatically generates tasks such as `compileApiJava`, `processApiResources` and `apiClasses`; `Jar` tasks per source set assemble separate JARs. `[from source]` (GRADLE p.44-45)
- Inspectable properties: `java.srcDirs`, `resources.srcDirs`, `allJava.files`, `output.classesDir`, `output.resourcesDir`. The default output directory seen in the output is `build/classes/main` (Gradle 2.3). `[from source]` (GRADLE p.43) `[DATED]` (later versions use `build/classes/java/main` `[extrapolation]`).
- `javadoc` uses the `main` source set by default and generates into `build/docs/javadoc`. `[from source]` (GRADLE p.47)
- Each source set can have its own compiler and classpath `[inference]`; the book states the grouping, it does not detail the classpath.

## 4. Incremental build and `UP-TO-DATE`
- The Preface states that Gradle supports incremental builds by determining which parts of the build tree are up to date so as not to re-run what depends on them. `[from source]` (GRADLE p.7)
- In the GWT chapter, `compileJava { options.incremental = true }` enables incremental Java compilation: the book explains that, in large projects, this tells Gradle exactly which input files are out of date relative to the previous run and compiles only those. `[from source]` (GRADLE p.33-34)
- The outputs show `UP-TO-DATE` next to tasks that did not need to run (`:compileJava`, `:processResources`, `:classes`, `:war` etc.). `[from source]` (GRADLE p.44-47, 75)
- **Not in the book**: input/output hash calculation, `@Input`/`@Output` annotations, local/remote build cache and the `--profile` flag. Descriptions of these are `[extrapolation]`. V1 attributed them to GRADLE p.26-30 (which are SourceSets pages).
- From SWE-G (concept, not Gradle): in task-based systems, the system does not know what the task reads and writes, so it cannot guarantee correct incremental builds without additional information; artifact-based systems know inputs and outputs. `[from source]` (SWE-G p.265, 268)

## 5. Properties, daemon and options
- Two kinds of properties: **system** (configure the JVM that runs the build, via `GRADLE_OPTS` or `JAVA_OPTS`) and **project** (parameterize the project). `[from source]` (GRADLE p.17)
- The daemon (`-Dorg.gradle.daemon=true`) keeps essential libraries and classes loaded and reduces build time (the book shows a comparison with and without the daemon). `[from source]` (GRADLE p.17-20) `[DATED]` (the daemon's default behavior changed in later versions `[extrapolation]`)
- Other properties: `org.gradle.java.home`, `org.gradle.jvmargs`, `org.gradle.configureondemand` and `org.gradle.parallel` ("incubating" modes). `[from source]` (GRADLE p.20)
- `-P` on the command line passes a project property; the book says the best way is a `gradle.properties` file and that the file in the user directory (`$USER_HOME/.gradle`) takes precedence over the project's. `[from source]` (GRADLE p.23-24)
- Custom properties in the script use the `ext { }` block; the book considers it bad to define them in the script. `[from source]` (GRADLE p.22-23)

## 6. Gradle Wrapper
- The Wrapper is a batch/shell script that downloads and configures Gradle to run the tasks, allowing you to build without having Gradle installed; it is described as good practice for unifying the Gradle version across the team. `[from source]` (GRADLE p.62)
- Generated by a task of type `Wrapper` with `gradleVersion`, `distributionUrl` etc.; the generated files (in the example `gradlej`/`gradlej.bat`; by default `gradlew`) must go into version control. `[from source]` (GRADLE p.63-64)
- Points: `distributionUrl` can point to an internal URL; when using the wrapper, any Gradle installed on the machine is ignored. `[from source]` (GRADLE p.64)
