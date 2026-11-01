# MPS-01. Setup, processor options and IDE (MapStruct 1.6.3, MPS p.3-14)

[from source] Version: **MapStruct 1.6.3**, guide dated 2024-11-09 (MPS p.1, 96).

## What it is (MPS p.3)
Annotation processor (JSR 269) that generates **type-safe** mapping classes, using plain method calls (**no reflection**), with build errors when the mapping is incomplete or incorrect. Two artifacts: `org.mapstruct:mapstruct` (annotations such as `@Mapping`) and `org.mapstruct:mapstruct-processor` (generator) (MPS p.3).

## Build
- **Maven:** property `org.mapstruct.version` 1.6.3, dependency `mapstruct`, and `annotationProcessorPaths` of the `maven-compiler-plugin` with `mapstruct-processor`; example with `source/target` 1.8 (MPS p.4). Eclipse: M2E, `m2e.apt.activation` `jdt_apt`; Java 1.8 or higher is required (MPS p.5).
- **Gradle:** `implementation mapstruct`, `annotationProcessor mapstruct-processor`, `testAnnotationProcessor` when used in tests (MPS p.5). **Ant:** `javac` with `-processorpath` (MPS p.5-6).
- **Java Modules:** supports Java 9+ (MPS p.13).

## `-Akey=value` options (MPS p.6-13)
| Option | Values / default | Page |
|---|---|---|
| `mapstruct.suppressGeneratorTimestamp` | false | 7 |
| `mapstruct.suppressGeneratorVersionInfoComment` | false | 7 |
| `mapstruct.verbose` | false (with Maven also `showWarnings`) | 7 |
| `mapstruct.defaultComponentModel` | `default` (default), `cdi`, `spring`, `jsr330`, `jakarta`, `jakarta-cdi`; `@Mapper#componentModel` prevails | 8 |
| `mapstruct.defaultInjectionStrategy` | `field` (default) or `constructor`; only for annotation-based models | 9 |
| `mapstruct.unmappedTargetPolicy` | `ERROR`/`WARN` (default)/`IGNORE` | 10 |
| `mapstruct.unmappedSourcePolicy` | `ERROR`/`WARN`/`IGNORE` (default) | 11 |
| `mapstruct.disableBuilders` | false | 11 |
| `mapstruct.nullValueIterableMappingStrategy` | `RETURN_NULL` (default)/`RETURN_DEFAULT` | 12 |
| `mapstruct.nullValueMapMappingStrategy` | same for maps | 13 |

Precedence of `unmappedTargetPolicy`: `@BeanMapping` > `@Mapper` > processor option (MPS p.10).

## IDE (MPS p.13-14)
Optional plugins for IntelliJ and Eclipse (completion in `target`/`source`/`expression`, go to declaration, quick fixes).

## Limits
Gradle Kotlin DSL, `kapt`/KSP, Spring Boot starter for MapStruct: NOT COVERED (the MPS mentions neither Kotlin nor Spring Boot).
