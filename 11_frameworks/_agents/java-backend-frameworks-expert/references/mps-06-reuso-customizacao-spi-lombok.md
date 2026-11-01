# MPS-06. Configuration reuse, customization, SPI and Lombok (MPS p.76-96)

## Reuse (MPS p.76-79)
- **`@InheritConfiguration`:** method A inherits from B if A's types are assignable to B's; candidates in the current mapper, supertypes or a shared config interface; `name = "..."` if there are several; does **not** refer to methods of used mappers (`uses`) (MPS p.76).
- **`@InheritInverseConfiguration`:** inverse (A's result type = B's source type); `name =`; `@InheritConfiguration` prevails in a conflict; transitive inheritance; `expression`, `defaultExpression`, `defaultValue` and `constant` are silently ignored in the inverse; `ignore` only applies when there is a `source`; reverse of nested properties is experimental since 1.1.0.Beta2 (MPS p.77).
- **`@MapperConfig` + `@Mapper#config`:** same attributes as `@Mapper`; what is in `@Mapper` prevails; lists (`uses`) are combined; "prototype" methods serve as a template (MPS p.78).
- `mappingInheritanceStrategy`: `EXPLICIT` (default), `AUTO_INHERIT_FROM_CONFIG`, `AUTO_INHERIT_REVERSE_FROM_CONFIG`, `AUTO_INHERIT_ALL_FROM_CONFIG` (MPS p.79).

## Customization (MPS p.79-84)
- **Decorators:** `@DecoratedWith(Class.class)`; the decorator is a subtype of the mapper (may be abstract); unimplemented methods delegate to the original; with CDI use CDI decorators instead (MPS p.79-80).
  - `default` model: constructor with 1 parameter of the mapper type (MPS p.80).
  - **Spring:** the original implementation gets `@Qualifier("delegate")`; the decorator does `@Autowired @Qualifier("delegate")`; the class that extends the decorator is `@Primary` (MPS p.80-81).
  - **JSR 330:** the original gets `@Named("<fqn of the implementation>")` (the name ends with `_` when there is a decorator); at the point of use a `@Named` without a value is needed to choose the decorator (MPS p.81-82).
- **`@BeforeMapping`/`@AfterMapping`:** in the abstract mapper, in a `uses` type or in a `@Context` parameter; only called if return and parameters are assignable; a non-null return becomes the mapping result; order: *before* without target before null-checks and construction, *before* with `@MappingTarget` after construction, *after* at the end; within the group: `@Context`, mapper, `uses`, supertype; the order within the same type is **not guaranteed** (MPS p.82-84). With builders: *before* with a real `@MappingTarget` is not invoked; *after* must receive the builder as `@MappingTarget` (MPS p.84).

## SPI (MPS p.84-93)
- Implementation in a separate JAR, with a `META-INF/services/<SPI name>` file containing the class name, added to the annotation processor's classpath (alongside `mapstruct-processor`); it may need to be added to the IDE's *factory path* (MPS p.84).
- Documented SPIs: `AccessorNamingStrategy` (e.g. fluent API `withX`) (MPS p.84-86), `MappingExclusionProvider` (default excludes `java.*`/`javax.*`) (MPS p.87), `BuilderProvider` (e.g. disabling builders) (MPS p.88), `EnumMappingStrategy` (MPS p.88-90), `EnumTransformationStrategy` (MPS p.91), `AdditionalSupportedOptionsProvider` (custom `-A` options via `getOptions()`) (MPS p.92-93).

## Third-party integration (MPS p.93-96)
- **"Non-distributed" annotations** recognized by **name** in any package: `@ConstructorProperties` and `@Default`; the guide advises against adding a third-party annotation just for mapping and suggests creating your own (`@Default` with `@Target(CONSTRUCTOR)`, retention `CLASS`) (MPS p.93-94).
- **Lombok:** works since MapStruct 1.2.0.Beta1 and Lombok 1.16.14; from Lombok **1.18.16** the additional processor `lombok-mapstruct-binding` (version 0.2.0 in the example) is required in `annotationProcessorPaths` (Maven) or `annotationProcessor` (Gradle); Lombok with scope `provided`/`compileOnly`; adjust via `lombok.config` if there is an incompatibility (MPS p.94-96). [DATED] example versions.

## Limits
Does not show Spring Boot, Kotlin (KAPT/KSP), or Records; for those topics: NOT COVERED.
