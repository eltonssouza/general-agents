# MPS-04. Collections, maps, streams and enums (MPS p.48-60)

## Collections (MPS p.48-50)
- Method with source/target collection types; the generated code iterates and converts each element by method or implicit conversion (MPS p.48). Collection properties use the corresponding collection method (MPS p.49).
- Without a collection *setter* (JAXB pattern): uses the getter and `addAll` (MPS p.49).
- A method with an iterable source (`java` package) and a non-iterable target is **not** allowed, nor the reverse (MPS p.50).

## Maps (MPS p.50)
`@MapMapping` (example with `valueDateFormat = "dd.MM.yyyy"`); converts key and value, by implicit conversion or another mapping method (MPS p.50). Other `@MapMapping` attributes besides `valueDateFormat`, `nullValueMappingStrategy`, `keyTargetType` and `valueTargetType` are not detailed in the guide (NOT COVERED). (`nullValueMappingStrategy` of `@MapMapping`: MPS p.13, 68; `keyTargetType`/`valueTargetType`: MPS p.67.)

## Collection strategies (MPS p.50-51)
`CollectionMappingStrategy`: `ACCESSOR_ONLY`, `SETTER_PREFERRED`, `ADDER_PREFERRED`, `TARGET_IMMUTABLE` (`DEFAULT` is equivalent to `ACCESSOR_ONLY` and should not be used explicitly) (MPS p.50-51). Adders are typical of generated JPA entities; MapStruct assumes the target's collections are initialized, and the guide suggests *factories* when needed (MPS p.51). Do not confirm the name of the `@Mapper` attribute for this strategy: the text only names the type (NOT COVERED for the attribute name).

## Implementations used (MPS p.51-52)
`Iterable`/`Collection`/`List` -> `ArrayList`; `Set` -> `LinkedHashSet`; `SortedSet`/`NavigableSet` -> `TreeSet`; `Map` -> `LinkedHashMap`; `SortedMap`/`NavigableMap` -> `TreeMap`; `ConcurrentMap` -> `ConcurrentHashMap`; `ConcurrentNavigableMap` -> `ConcurrentSkipListMap`.

## Streams (MPS p.52-53)
`java.util.Stream` mapped with `Stream#map` + `collect`; mapping a `Stream` to `Iterable`/array **consumes** the stream (MPS p.52-53).

## Enums (MPS p.53-60)
- **Enum -> enum:** by name; `@ValueMapping(source, target)` (grouped in `@ValueMappings`); a constant without a match = **build error**; several values may go to the same target (MPS p.53-54).
- `MappingConstants` constants: `ANY_REMAINING` (maps by name whatever is left and the rest goes to the indicated target), `ANY_UNMAPPED` (does not try to map by name), `NULL`, `THROW_EXCEPTION` (only in `target`); `ANY_REMAINING` and `ANY_UNMAPPED` not together and once per set; with `@InheritInverseConfiguration`/`@InheritConfiguration` the `ANY_*` are ignored (MPS p.54-56).
- **Enum <-> String:** `enum -> String`: `ANY_REMAINING` produces an error; `String -> enum`: needs a default value (`ANY_REMAINING`/`ANY_UNMAPPED`) otherwise a warning (MPS p.57).
- **`@EnumMapping`:** `nameTransformationStrategy` (`suffix`, `stripSuffix`, `prefix`, `stripPrefix`, `case` with `upper`/`lower`/`capital`) and `configuration` (MPS p.58-60). Custom strategies via SPI (MPS p.60, 91).
- Composition of `@ValueMapping` as a meta-annotation (MPS p.60).
- Guide divergence: the text cites `IllegalStateException` for an unknown value, but the generated code uses `IllegalArgumentException` (MPS p.54, 59).

## Limits
There is no handling of enums with associated fields/values nor *mapping* to `EnumSet`: NOT COVERED.
