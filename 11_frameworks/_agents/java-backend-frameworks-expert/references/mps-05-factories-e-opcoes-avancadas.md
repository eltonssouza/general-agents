# MPS-05. Factories and advanced options (MPS p.60-75)

## Object factories (MPS p.60-63)
By default the target's default constructor is used; alternative: a no-arg method, a method with `@ObjectFactory`, or a method with only a `@TargetType` parameter that returns the type; registered via `@Mapper#uses` or in the mapper itself (MPS p.60-61). `@ObjectFactory` can receive the sources as parameters and serves to indicate "factory only" (MPS p.63). Factories also apply in update methods for nested beans (MPS p.62-63).

## Default values, constants, expressions (MPS p.64-66)
- `defaultValue` (when the source is `null`) and `constant` (always; **cannot** have `source`); both are `String` (literal for primitives/wrappers; others converted) (MPS p.64).
- `expression = "java(...)"`: Java only; the expression is **not validated** at generation (the error appears when compiling the generated code); use a qualified name or `@Mapper(imports = ...)` (MPS p.65). `defaultExpression` only when the source is `null`; same restrictions (MPS p.65-66).

## Subclasses and result type (MPS p.66-67)
- `@SubclassMapping(source, target)`; without a mapping for a subclass (e.g. `GrapeDto`), it becomes the parent type; abstract/interface parent type = compile error, unless `subclassExhaustiveStrategy = RUNTIME_EXCEPTION` (throws `IllegalArgumentException` at runtime) (MPS p.66). `@SubclassMapping` does **not** combine with update methods, `@Context` or `@TargetType` (MPS p.67).
- `@BeanMapping(resultType = ...)`, `@Mapping#resultType`, `@IterableMapping#elementTargetType`, `@MapMapping#keyTargetType`/`valueTargetType` (MPS p.67).

## `null` handling (MPS p.68-70)
- **`null` argument:** default returns `null`; `nullValueMappingStrategy = NullValueMappingStrategy.RETURN_DEFAULT` returns an "empty" bean (constants and expressions still populated), an empty iterable or an empty map; hierarchy `@BeanMapping`/`@IterableMapping`/`@MapMapping` > `@Mapper` > `@MapperConfig` (MPS p.68). Dedicated variants for collections/maps (MPS p.68).
- **Properties in update methods:** `nullValuePropertyMappingStrategy` = `SET_TO_DEFAULT` or `IGNORE` (default: assign `null`); `SET_TO_DEFAULT` creates `ArrayList`, `LinkedHashMap`, an empty array, `""`, `false`/`0` or a new instance (requires a default constructor) (MPS p.68-69). Collections/maps with getter/adder always have a `null` check (MPS p.69).
- **`nullValueCheckStrategy`:** `ON_IMPLICIT_CONVERSION` (default) or `ALWAYS`; hierarchy `@Mapping` > `@BeanMapping` > `@Mapper` > `@MapperConfig` (MPS p.69-70). Manual methods must handle `null` (MPS p.69).
- **Presence checker:** a `hasXYZ` method replaces the null-check; configurable/disableable via SPI (MPS p.70).

## Conditional mapping (MPS p.70-73)
- `@Condition` (returns `boolean`) for properties; condition on a source parameter via `@SourceParameterCondition` or `@Condition(appliesTo = ConditionStrategy.SOURCE_PARAMETERS)` (MPS p.70).
- In update methods it replaces the null-check (and assigns `null` when the condition fails, in the example) (MPS p.71-72). `@TargetPropertyName`/`@SourcePropertyName` (String) only in `@Condition` (MPS p.72-73). `@Condition` takes precedence over the bean's presence checker; qualifiers via `conditionQualifiedBy`/`conditionQualifiedByName` (MPS p.73).

## Exceptions (MPS p.74-75)
`throws` on the mapping method propagates checked exceptions from manual methods; undeclared ones become `RuntimeException` in a generated `try/catch` (MPS p.74-75). MapStruct only generates a null-check when converting types or building via constructor; manual methods must return non-null values and handle `null` (MPS p.75).

## Limits
Does not cover validation (Bean Validation), `@AfterMapping` with advanced `@Context` beyond what is cited, nor asynchronous mapping: NOT COVERED.
