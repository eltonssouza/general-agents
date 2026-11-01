# Modern C# features (C# 8 to C# 13) according to CSHist, CS12 and CS13

Convention: `(CSHist p.N)`, `(CS12 p.N)`, `(CS13 p.N)` = PDF page. The sources **name** most of the features (CSHist) and **explain** only those of C# 12 and 13 (CS12, CS13). In each section, "Sources" gives the grounding and "Supplement `[extrapolation]`" gives general C# knowledge, which is not in the PDFs. Code examples are illustrative (those from CS12/CS13 come from those pages, adapted).

## 1. Nullable reference types (C# 8)

- **Sources**: *nullable reference types* is a C# 8.0 feature `[from source] (CSHist p.8)`; it is "implemented in the compiler", but "much more useful when libraries are annotated" with the nullability state of arguments and returns `[from source] (CSHist p.8)`. C# 10 improves the accuracy of definite-assignment and nullability warnings `[from source] (CSHist p.4)`. C# 6 brought the null propagator (`?.`) `[from source] (CSHist p.11)`; C# 8 brought `??=` `[from source] (CSHist p.8)`; C# 9 suggests `if (e is not null)` as the new null test `[from source] (CSHist p.6)`.
- Supplement `[extrapolation]`: enabled with `#nullable enable` or `<Nullable>enable</Nullable>`; `string` = "must not be null", `string?` = "may be null"; the compiler emits **warnings** (not errors); `!` suppresses the warning but does not change execution (`NullReferenceException` is still possible).

## 2. Records, `init` and `with` (C# 9/10)

- **Sources**: records (C# 9) are "concise syntax for reference types that follow value semantics for equality" for data containers `[from source] (CSHist p.6)`; init-only setters provide non-destructive mutation (`with`) `[from source] (CSHist p.6)`; derived records can override virtual methods with a covariant return `[from source] (CSHist p.6)`. C# 10: record structs "synthesize many of the same methods as record classes"; structs and anonymous types support `with`; `sealed` on a record's `ToString` `[from source] (CSHist p.4)`. For primary constructors, the compiler generates public properties **only** on `record class`/`record struct` `[from source] (CS12 p.2)`.
- Supplement `[extrapolation]`: `record Pessoa(string Nome, int Idade);` generates a constructor, `init` properties, `Equals`/`GetHashCode`/`==`/`!=`, `ToString` and `Deconstruct`; `p with { Idade = 31 }` creates a modified copy; class records are reference types (not "value types in C# 9").

## 3. Pattern matching

- **Sources**: C# 7.0 introduced pattern matching `[from source] (CSHist p.11)`; C# 8: switch expressions, property, tuple and positional patterns `[from source] (CSHist p.8)`; C# 9: type patterns, parenthesized patterns, `and`, `or`, `not` and relational (`<`, `>`, `<=`, `>=`), in `is`, `switch` (expression and statement) and nested patterns `[from source] (CSHist p.6)`; C# 10: extended property patterns `[from source] (CSHist p.4)`; C# 11: list patterns `[from source] (CSHist p.3)` and matching a `Span<char>` against a constant `[from source] (CSHist p.3)`.
- Supplement `[extrapolation]`: illustrative example `n switch { < 0 => "neg", 0 => "zero", _ => "pos" }`; `_` is the discard; `{ Cliente.Cidade: "Curitiba" }` (extended property pattern); `[1, 2, ..var resto]` (list pattern).

## 4. Primary constructors (C# 12)

- **Sources**: they can be created on **any** `class` or `struct` (not only records); their parameters are in scope throughout the type's body; every explicit constructor must call the primary one with `this(...)`; adding a primary one prevents the implicit parameterless constructor; in a `struct`, the implicit constructor zeroes all fields including the primary parameters; **public properties only for records** `[from source] (CS12 p.1-2)`.
- Illustrative example: `public class Servico(ILogger logger) { public void Rodar() => logger.Log("ok"); }` (the parameter is used as state; it does not become a property).

## 5. Collection expressions (C# 12)

- **Sources**: concise `[...]` syntax for collection values; the *spread* element `..e` inserts the elements of another collection; works for arrays, `Span<T>`/`ReadOnlySpan<T>` and types with a collection initializer, such as `List<T>`; usable wherever a collection is needed, including as an argument `[from source] (CS12 p.2-3)`.
- Example (from the source): `int[] a = [1, 2, 3];`, `List<string> b = ["one", "two", "three"];`, `int[] single = [.. row0, .. row1, .. row2];` `[from source] (CS12 p.2-3)`.

## 6. `ref readonly` parameters, lambdas with defaults, alias, inline arrays, `Experimental`, interceptors (C# 12)

- `ref readonly`: more clarity for APIs that use `ref` or `in`; updating an API from `ref` to `ref readonly` does not break callers (changing to `in` would); examples: `Marshal.QueryInterface`, `ReadOnlySpan<T>(T)`, `Unsafe.IsNullRef` `[from source] (CS12 p.3-4)`.
- Default values in lambda parameters: same syntax and rules as methods `[from source] (CS12 p.4)`.
- Alias for any type with the `using` directive (tuples, arrays, pointers) `[from source] (CS12 p.4)`.
- Inline arrays: fixed-size array in a `struct` (`InlineArray(10)`), performance similar to an unsafe `fixed` buffer; "you probably won't declare your own", and you use them via `Span<T>` `[from source] (CS12 p.4-5)`.
- `Experimental`: marks types/methods/assemblies; the compiler warns when they are accessed `[from source] (CS12 p.5)`.
- **Interceptors**: **experimental/preview** C# 12 feature, "not recommended for production"; replaces calls at compile time, typical in source generators; requires `<InterceptorsPreviewNamespaces>` `[from source] (CS12 p.5-6)` `[VERSION-DEPENDENT]`.

## 7. `params` collections (C# 13)

- **Sources**: `params` is no longer limited to arrays; it accepts `Span<T>`, `ReadOnlySpan<T>`, types that implement `IEnumerable<T>` with an `Add` method and the interfaces `IEnumerable<T>`, `IReadOnlyCollection<T>`, `IReadOnlyList<T>`, `ICollection<T>`, `IList<T>`; with an interface, the compiler synthesizes the storage for the arguments `[from source] (CS13 p.2)`. Example: `public void Concat<T>(params ReadOnlySpan<T> items)` `[from source] (CS13 p.2)`.
- Supplement `[extrapolation]`: `params ReadOnlySpan<T>` usually avoids an array allocation on the caller side (the sources do not state this; the benefit is performance, to be measured).

## 8. New `Lock` type (C# 13/.NET 9)

- **Sources**: the .NET 9 runtime brings `System.Threading.Lock` for synchronization; `Lock.EnterScope()` enters an exclusive scope and returns a `ref struct` with the `Dispose()` pattern to exit; the `lock` statement recognizes a target of type `Lock` and uses the new API instead of `System.Threading.Monitor`; if the `Lock` is converted to another type (e.g. `object`), `Monitor`-based code is generated; to get the benefits it is enough to change the type of the locked object and "no other code needs to change" `[from source] (CS13 p.2)` `[VERSION-DEPENDENT]`.
- Supplement `[extrapolation]`: `private readonly Lock _gate = new();` + `lock (_gate) { ... }`; `lock(this)`, `lock(typeof(T))` and strings are discouraged targets because they are externally visible; the sources discuss neither this nor performance.

## 9. Other C# 13 novelties

- Escape `\e` for the ESCAPE character (U+001B); previously `\u001b` or `\x1b` was used, and `\x1b` was discouraged because following hex digits become part of the sequence `[from source] (CS13 p.3)`.
- Method group natural type: the compiler prunes candidates at each scope, removing the non-applicable ones `[from source] (CS13 p.3)`.
- Implicit "from the end" access (`^`) in object initializers for one-dimensional collections `[from source] (CS13 p.3-4)`.
- `ref` locals and `unsafe` in iterators and `async` methods, with no access across `await`/`yield return` `[from source] (CS13 p.4)`.
- `allows ref struct` (generic anti-constraint) and `ref struct` implementing interfaces (no conversion to the interface type, as it would be boxing; it must implement all the methods, including those with a default implementation) `[from source] (CS13 p.4-5)`.
- `partial` properties and indexers: one declaration and one implementation with equal signatures; the implementation cannot be an auto-property `[from source] (CS13 p.5-6)`.
- `OverloadResolutionPriorityAttribute`: library authors indicate the preferred overload; use with care `[from source] (CS13 p.6)`.
- `field` (contextual keyword) is **preview** in C# 13 (from VS 17.12); it accesses the synthesized backing field; possible breaking change if a field named `field` exists (use `@field` or `this.field`) `[from source] (CS13 p.1, 7)`; CSHist lists "field backed properties" in C# 14 `[from source] (CSHist p.1)` `[VERSION-DEPENDENT]`.

## 10. Items only named (no explanation in the sources)

Raw string literals, generic math, `required`, file-local types, UTF-8 literals, `global using`, file-scoped namespace, `with` on structs, `static abstract` in interfaces, top-level statements (explained only as "without ceremony", CSHist p.6), extension members, null-conditional assignment, unbound `nameof`, user-defined compound operators: ask for the version with `cs_version_lookup.py`; technical descriptions = `[extrapolation]`.
