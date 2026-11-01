# SB3G-09. AOP, Feign and auto-configuration (SB3G p.228-242)

## AOP (SB3G p.229-232)
- Concepts: join point, pointcut, advice (before/after/around), aspect, weaving (SB3G p.229-230).
- Example: `spring-boot-starter-aop`; `@Aspect @Component LoggingAspect` with `@Around`, `@Before`, `@After` and pointcut `execution(* com.packt.ahmeric..*.*(..))` (SB3G p.231-232). Sample log output (SB3G p.232).

## Feign (SB3G p.233-236)
- Declarative HTTP client; compared to `RestTemplate` (synchronous, more code) and `WebClient` (reactive, steeper curve) (SB3G p.233).
- Dependency `spring-cloud-starter-openfeign` with BOM `spring-cloud-dependencies` version **2023.0.1** (SB3G p.234) [DATED]; `@EnableFeignClients`; `@FeignClient(name, url)` with `@GetMapping`/`@PathVariable`; `record Post` (SB3G p.234-235). The example consumes a public test API (SB3G p.234-236).

## Conditional auto-configuration (SB3G p.236-238)
- Boot examines the classpath, beans and properties (SB3G p.236). `@ConditionalOnProperty`, `@ConditionalOnClass`, `@ConditionalOnExpression` cited; example: `@ConditionalOnExpression("${logging.aspect.enabled:false}")` on the `LoggingAspect` (SB3G p.237).

## Best practices and pitfalls (SB3G p.238-241)
- AOP: use sparingly, precise pointcuts, simple advice (SB3G p.238-239). Feign: centralized configuration, custom *error decoder*, tests with mocks (SB3G p.239). Auto-config: `@Conditional`, avoid conflicts, `@AutoConfigureOrder` (SB3G p.239).
- Pitfalls: excessive AOP; poorly configured Feign (timeouts, error handling); ignoring auto-config conditions and `@ConditionalOnMissingBean` (SB3G p.240-241).
- "Real example" of poorly scoped proxies (SB3G p.241): the explanation (a singleton service "locked" by an aspect on a method) is **technically imprecise** [extrapolation]; the agent reports it as a claim of the book without endorsing it. Mentions JDK proxy vs CGLIB (SB3G p.241).

## Important gap
- The book announces **custom starters** (SB3G p.15, 237), but **does not implement them**: NOT COVERED for creating a starter/`AutoConfiguration.imports`.
- The `@ConditionalOnExpression` example with default value `false` leaves the aspect **off** if the property does not exist (SB3G p.237) [inference from the `:false` expression].
