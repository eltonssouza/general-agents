# MPS-02. Defining and obtaining mappers (MPS p.14-32)

## Basic mapping (MPS p.14-17)
- Interface annotated with `org.mapstruct.Mapper`; the implementation is generated at build time (MPS p.14).
- Properties with the same name are mapped implicitly; different names via `@Mapping(target = ..., source = ...)`; uses the **JavaBeans property name** (MPS p.14).
- `@BeanMapping(ignoreByDefault = true)`: explicit mode (only what is in `@Mapping`; no unmapped-target warnings) (MPS p.15). *Fluent setters* are supported (MPS p.15).
- The generated code is "as if hand-written" (getters/setters) (MPS p.16). A new mapping method is only created for bean properties, not for `Collection`/`Map` (MPS p.16). Collections with the same element type are copied into a new collection (MPS p.17).
- **Composition** (meta-annotation): `@Mapping` with `@Target(ANNOTATION_TYPE)`; "duck typing"; less clear error messages; safer alternative: `@InheritConfiguration` (MPS p.17).

## Custom methods (MPS p.18-19)
- `default` method in the interface (Java 8+) or **abstract** class (allows fields); the generated code invokes the manual method when the types match (MPS p.18-19).
- **Multiple source parameters:** an ambiguous property requires `source = "param.prop"`; returns `null` if **all** parameters are `null`; a non-bean parameter can be mapped directly (MPS p.19).
- **Target `"."`** maps all properties of a nested bean; conflicts are resolved explicitly (MPS p.20).

## Update and public fields (MPS p.20-22)
- `@MappingTarget` updates an existing instance; **only one** parameter can be the target; the return may be the target type (MPS p.20). Collections: `ACCESSOR_ONLY` clears and populates; `ADDER_PREFERRED`/`TARGET_IMMUTABLE` do not clear (MPS p.20).
- Public fields without getter/setter: read if `public`/`public final` (not `static`); write only if `public` (not `final`/`static`) (MPS p.21).

## Builders and constructors (MPS p.22-26)
- Builders via the `BuilderProvider` SPI: public static no-arg method that returns the builder and a no-arg *build* method; with several, it looks for `build`, otherwise error; `@Builder` in `@BeanMapping`/`@Mapper`/`@MapperConfig`; `@Builder#disableBuilder` and the option `mapstruct.disableBuilders` (MPS p.22-24). Supports Lombok (separate module), AutoValue, Immutables, FreeBuilder (MPS p.24).
- Constructors (without builder): `@Default` (any package) > single public constructor > no-arg constructor; ambiguous = error; parameters match by name (or `@ConstructorProperties`); **factory/`@ObjectFactory` takes precedence** over constructor (MPS p.24-25).

## Map to bean and annotations (MPS p.26-29)
- `Map<String, ...>` -> bean: target properties read keys from the map; a raw `Map` or one without a `String` key produces a warning (MPS p.26-27).
- `@AnnotateWith` generates annotations on the mapper (e.g. Camel `@Converter`) and `@Javadoc` generates Javadoc (MPS p.27-29).

## Obtaining the mapper (MPS p.30-32)
- **Without DI:** `Mappers.getMapper(Class)`; `INSTANCE` field convention; generated mappers are **stateless and thread-safe** (MPS p.30).
- **With DI:** injection (CDI, Spring or JSR 330) is recommended, via `@Mapper#componentModel` or processor option; constants in `MappingConstants.ComponentModel`; CDI generates `@ApplicationScoped`; mappers in `uses` must also be beans (MPS p.31).
- **Injection strategy:** `InjectionStrategy.CONSTRUCTOR`/`FIELD`/`SETTER`; default **field**; the guide recommends **constructor** to ease testing; with circular dependencies in Spring compilation may fail and then use `SETTER`; for abstract classes or decorators use setter (MPS p.31-32).

## Limits
The MPS does **not** show a complete example with `componentModel = "spring"` in a Spring Boot project; for that: NOT COVERED and a labeled [extrapolation], routing to the Spring Boot reference agent.
