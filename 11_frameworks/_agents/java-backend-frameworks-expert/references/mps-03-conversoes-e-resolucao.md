# MPS-03. Type conversions, references and method resolution (MPS p.32-48)

## Implicit conversions (MPS p.32-35)
- Primitives <-> wrappers (with `null` check), numeric types among themselves, primitives/wrappers <-> `String` (with `numberFormat` in `DecimalFormat` style) (MPS p.32-33).
- Conversion from a larger to a smaller type can lose value/precision; the `typeConversionPolicy` attribute in `@Mapper`/`@MapperConfig` controls warning/error; **default `IGNORE`** for compatibility (MPS p.32).
- `enum` <-> `String`; `enum` <-> `Integer` (by `ordinal()`; an out-of-range value raises an exception cited in the text); `BigInteger`/`BigDecimal` (with `numberFormat`) (MPS p.33).
- Dates: `Date`/`XMLGregorianCalendar` <-> `String` with `dateFormat` (`SimpleDateFormat` pattern); Joda; `java.time` (`ZonedDateTime`, `LocalDateTime`, `LocalDate`, `LocalTime` <-> `String`; `Instant`/`Duration`/`Period` via `parse`/`toString`); `LocalDateTime`/`LocalDate` <-> `Date` use UTC; `ZonedDateTime` <-> `Date` uses the system default time zone; `java.sql` types (MPS p.33-34).
- `Currency`, `UUID`, `StringBuilder`, `URL`, `Locale` <-> `String` with exceptions for invalid values (MPS p.34-35).
- Examples: `numberFormat = "$#.00"`, `numberFormat = "#.##E0"`, `dateFormat = "dd.MM.yyyy"`; also in `@IterableMapping` (MPS p.33).

## Object references (MPS p.35-36)
Routine per attribute pair: 1) same type = copy (collection = copy of the collection); 2) existing method with the types; 3) built-in conversion; 4) complex conversions (method(method), method(conversion), conversion(method)); 5) automatic submethod; 6) build error with the attribute path (MPS p.35-36).
- **`MappingControl`** (experimental since 1.4) in `@MapperConfig`, `@Mapper`, `@BeanMapping`, `@Mapping`; enum `Use` with `DIRECT`, `MAPPING_METHOD`, `BUILT_IN_CONVERSION`, `COMPLEX_MAPPING`; `@DeepClone`; example `NoComplexMapping.class` (MPS p.36).
- `@Mapper(disableSubMappingMethodsGeneration = true)` turns off automatic submethods; shared configurations still do not apply in those submethods (issue #1086) (MPS p.36).
- Guide tip: cut references between entities by mapping to the id with a manual method (MPS p.35).

## Nested mappings (MPS p.36-38)
- `.` notation: `@Mapping(target = "fish.kind", source = "fish.type")`; `ignore = true` at nested level; "cherry-pick" across different levels; `constant`/`expression` on a nested target (MPS p.36-38). There is a `null` check on each nested source property (MPS p.38).
- The guide **recommends writing dedicated nested methods** instead of configuring everything in the parent method (MPS p.38); the reporting policy of the generated nested method may be `IGNORE` (MPS p.38).

## Custom methods and other mappers (MPS p.38-41)
- Pass the whole source object to a manual method with `source = "source"` (parameter name) (MPS p.38-39).
- `@Mapper(uses = X.class)`; hand-written mappers in the `default` model need a **public no-arg constructor**; in the CDI model they must be beans (MPS p.40).
- `@TargetType` (`Class` parameter) for generic methods (e.g. resolving `Reference` -> JPA entity) (MPS p.40-41). `@Context` passes state to custom methods, `@ObjectFactory` and before/after; there is no null-check on calls in context and `@Context` parameters must appear in the generated method (MPS p.42-43).

## Resolution and qualifiers (MPS p.43-48)
- Selects the **most specific** method (similar to Java method resolution); a tie = error (MPS p.43).
- `@Qualifier` (retention `CLASS`) + `@Mapping(qualifiedBy = {...})`; a method/class with a qualifier is **no longer** used for mappings without `qualifiedBy`; `@BeanMapping#qualifiedBy` selects a *factory* (MPS p.44-45).
- `@Named` with `qualifiedByName` is lighter, but more fragile under refactoring (MPS p.46).
- `defaultValue` is a `String` converted to the target type; with `qualifiedBy(Name)` it forces the method; alternative: `defaultExpression` (MPS p.46-48).

## Limits
There is no rule for `Optional`, nor a list of conversions for types from libraries not cited (e.g. Money): NOT COVERED.
