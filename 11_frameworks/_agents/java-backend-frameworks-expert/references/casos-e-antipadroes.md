# Cases and anti-patterns supported by the sources

## MapStruct (MPS)
1. **Constant with `source`:** a constant cannot reference a source property (MPS p.64).
2. **Ambiguous property with several parameters:** error until qualified with `param.prop` (MPS p.19).
3. **Two `@MappingTarget`:** only one parameter can be the target (MPS p.20).
4. **Invalid Java expression:** not validated at generation, the generated code fails to compile (MPS p.65).
5. **Forgetting an import in `expression`:** use a qualified name or `imports` (MPS p.65).
6. **Enum without a match:** build error, unless `@ValueMapping` is used (MPS p.54).
7. **`ANY_REMAINING` in enum -> String:** error (MPS p.57).
8. **`ANY_REMAINING` and `ANY_UNMAPPED` together:** not allowed (MPS p.54).
9. **Circular dependency between Spring mappers with constructor injection:** compilation may fail; use `SETTER` (MPS p.32).
10. **Lombok 1.18.16+ without `lombok-mapstruct-binding`:** MapStruct stops working (MPS p.94).
11. **Qualifier with retention other than `CLASS`:** the guide requires `CLASS` (MPS p.45).
12. **Inverse config inheritance with `expression`/`constant`:** silently ignored (MPS p.77).
13. **`SET_TO_DEFAULT` without a default constructor:** requires a default constructor or `defaultValue` (MPS p.69).
14. **`@SubclassMapping` with an update method:** not supported (MPS p.67).
15. **Consuming a `Stream` twice after mapping to `Iterable`/array:** the stream is consumed (MPS p.53).
16. **Relying on the order of `@BeforeMapping` methods within the same type:** not guaranteed (MPS p.84).

## Spring Boot (SB3G)
17. **CSRF disabled by default in the example:** the book only justifies it for APIs used by other applications (SB3G p.134).
18. **`/login` with own password:** the example uses `grant_type=password` and sample secrets (SB3G p.145) [extrapolation: do not replicate in production].
19. **`:latest` images and trivial credentials in the examples:** didactic (SB3G p.136-138, 173-174).
20. **`ddl-auto=update`:** present in the example (SB3G p.106); the book's alternative for schema evolution is Liquibase (SB3G p.125-127).
21. **CQRS where there is no imbalance:** the book warns against overcomplication (SB3G p.52-53).
22. **Excessive AOP / broad pointcut:** the example itself applies to all methods of the package; the book recommends precise pointcuts (SB3G p.231, 239).
23. **Feign without timeout/error configuration:** pitfall cited (SB3G p.240).
24. **Backpressure without monitoring:** the book admits the local test is limited (SB3G p.96).
25. **Mixing blocking code in a reactive flow:** the reactive login example uses `RestTemplate` inside a `Mono` (SB3G p.157); the book does not comment on it [inference].

## Quarkus (QRK)
26. **Forgetting to remove extensions when switching platform (HTTP -> Lambda -> Knative events):** the text says to remove `funqy-http`/`openshift` when moving to Lambda and to return with `openshift` for Knative (QRK p.6, 8).
27. **Reading startup times as a guarantee:** the text says they vary by environment (QRK p.5).
