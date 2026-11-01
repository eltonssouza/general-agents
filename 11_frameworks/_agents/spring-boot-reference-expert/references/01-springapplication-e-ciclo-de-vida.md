# 01 — SpringApplication and lifecycle (ch. 7.1)

Pages = PDF (SBR p.N; printed = N−20). Version 2.7.18 [DATED].

## Startup and failures
- **[from source]** `SpringApplication.run` starts the app (SBR p.71); the startup log shows details (user, PID, profiles). Turn it off with `spring.main.log-startup-info=false` (this also suppresses the active profiles log) (SBR p.72).
- **[from source]** If the app does not start, `FailureAnalyzer`s give a message and an action; with no analyzer, turn on the conditions report with `--debug`/the `debug` property or DEBUG on `ConditionEvaluationReportLoggingListener` (SBR p.72-73). To create your own: register it in `META-INF/spring.factories` (SBR p.556).
- **[from source]** Concrete `FailureAnalyzer` example: with the embedded server on 8080 and the port taken, the `APPLICATION FAILED TO START` block appears with the description "Embedded servlet container failed to start. Port 8080 was already in use" and the action to identify and stop the process listening on 8080 or configure another port for the application (SBR p.73). The phrase is in the Reference, p.73.

## Lazy initialization
- **[from source]** `spring.main.lazy-initialization=true` (or `setLazyInitialization`/`lazyInitialization`) creates beans on demand and reduces startup time, but **defers the discovery of errors** and requires memory for all beans; that is why it is not the default and tuning the heap first is recommended; `@Lazy(false)` opens an exception per bean (SBR p.73-74).

## Banner
- **[from source]** `banner.txt` on the classpath or `spring.banner.location`; image `banner.gif|jpg|png` or `spring.banner.image.location`; `spring.banner.charset`; variables `${application.version}`, `${spring-boot.version}`, `${Ansi.NAME}`...; mode `spring.main.banner-mode` = console | log | off; bean `springBootBanner`. The `application.*` variables only resolve with `java -jar`/launchers (SBR p.74-75). **Fix when the variables do not resolve:** run as a packaged jar with `java -jar` or, for an **unpacked** jar, with `java org.springframework.boot.loader.JarLauncher` (the launcher initializes the banner properties before assembling the classpath); `java -cp <classpath> <mainclass>` does not resolve them (SBR p.75). Turn the banner off in code: `new SpringApplication(Cls.class)` + `setBannerMode(Banner.Mode.OFF)` + `run(args)` (example from section 7.1.4, SBR p.75).

## Customization
- **[from source]** Local instance `new SpringApplication(...)` + setters, or `SpringApplicationBuilder` (fluent, parent/child hierarchy: web components in the child; same `Environment`) (SBR p.75-77). It can also be configured through `spring.main.*` properties (SBR p.76, 562).

## Availability (liveness/readiness)
- **[from source]** States: *Liveness* (`CORRECT`/`BROKEN`) and *Readiness* (`ACCEPTING_TRAFFIC`/`REFUSING_TRAFFIC`); exposed as health groups when Actuator is present; also through `ApplicationAvailability` (SBR p.77-78).
- **[from source]** **Liveness must not depend on external checks** (a database being down would cause cascading restarts); it is considered live after the context refresh; ready after the runners (SBR p.77).
- **[from source]** Startup tasks should go in `CommandLineRunner`/`ApplicationRunner`, not in callbacks such as `@PostConstruct` (SBR p.77). To change the state: `AvailabilityChangeEvent.publish(...)` (SBR p.78-80).

## Events (order)
- **[from source]** `ApplicationStartingEvent` → `ApplicationEnvironmentPreparedEvent` → `ApplicationContextInitializedEvent` → `ApplicationPreparedEvent` → `ApplicationStartedEvent` → `AvailabilityChangeEvent` with `LivenessState.CORRECT` → `ApplicationReadyEvent` → `AvailabilityChangeEvent` with `ReadinessState.ACCEPTING_TRAFFIC`; `ApplicationFailedEvent` on failure (SBR p.81). `WebServerInitializedEvent` and `ContextRefreshedEvent` fire between Prepared and Started (SBR p.81-82).
- **[from source]** Some events occur before the context: register listeners through `addListeners`/`listeners(...)` or `META-INF/spring.factories` (key `org.springframework.context.ApplicationListener`); listeners run on the same thread, so avoid long tasks; in a hierarchy the same event may arrive duplicated (SBR p.81-82).

## Web application type, arguments, runners, exit
- **[from source]** Context choice: Spring MVC present → servlet; otherwise WebFlux → reactive; otherwise non-web; override with `setWebApplicationType` (use `NONE` in JUnit tests) (SBR p.82).
- **[from source]** `ApplicationArguments`; `ApplicationRunner`/`CommandLineRunner` (order by `Ordered` or by the `Order` annotation) (SBR p.82-84).
- **[from source]** Shutdown hook by default; `ExitCodeGenerator`; the first non-zero exit code wins (SBR p.84-86).
- **[from source]** Admin: `spring.application.admin.enabled` exposes an MXBean; `local.server.port` reports the port (SBR p.86). Startup tracking: `BufferingApplicationStartup`/`FlightRecorderApplicationStartup`; the `startup` endpoint needs the `BufferingApplicationStartup` (SBR p.86-87, 441).

## Warning
- **[inference]** The text gives no startup time figures as a target; the times in the logs (e.g. 2.63 s, SBR p.72) are only examples.

## Round 4 additions: banner, events and runners warning (page details)
- **[from source]** Banner: the variables `${application.title}` (title declared in `MANIFEST.MF`, e.g. `Implementation-Title: MyApp` prints `MyApp`), `${application.version}` and `${application.formatted-version}` are only available with `java -jar` or `java -cp` with Boot's launchers; they are not resolved if you run an unpacked jar with `java -cp <classpath> <mainclass>` (SBR p.75). To generate the banner in code, use `SpringApplication.setBanner(…)` with an implementation of `org.springframework.boot.Banner` (method `printBanner()`); `spring.main.banner-mode` chooses between console (`System.out`), log or off; the printed banner is registered as the singleton bean `springBootBanner` (SBR p.75). Fix for the `java -cp` case: use `java -jar` (packaged jar) or `java org.springframework.boot.loader.JarLauncher` (unpacked jar), which initializes the banner's `application.*` properties before assembling the classpath (SBR p.75). The book's example for turning the banner off: `SpringApplication application = new SpringApplication(MyApplication.class); application.setBannerMode(Banner.Mode.OFF); application.run(args);` (SBR p.75, section 7.1.4).
- **[from source]** Events: some events fire before the `ApplicationContext` exists, so you cannot register a listener for them as a `@Bean`; register with `SpringApplication.addListeners(…)` or `SpringApplicationBuilder.listeners(…)` (SBR p.81). Listeners run on the same thread by default, so they must not run long tasks (use application/command-line runners) (SBR p.82).
