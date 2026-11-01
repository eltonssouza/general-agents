# Timeline of C# versions (CSHist, CS12, CS13)

Convention: `(CSHist p.N)`, `(CS12 p.N)`, `(CS13 p.N)` = PDF page (articles without printed numbering). `CSHist` = *The history of C#* (the PDFs `CSharp-9/10/11-WhatsNew.pdf` have the same 16-page text, updated on 18/11/2025, p.16).

**What the sources do:** they list the features per version, sometimes with a paragraph of context. They do **not** give Visual Studio versions per release (except where indicated below), nor the .NET version of every release. What is not in the table is "version not stated in the sources".

Library dependency note (applies to any feature): the language uses types and methods from a "standard library" delivered in packages; to use new features in old environments it may be necessary to install specific libraries (each version page documents the dependencies) `[from source] (CSHist p.1)`.

## 1. Table by version

| Version | Release | Platform/IDE cited in the source | Features listed | Pages |
| :-- | :-- | :-- | :-- | :-: |
| **C# 1.0** | January/2002 | Visual Studio .NET 2002 | classes, structs, interfaces, events, properties, delegates, operators and expressions, statements, attributes; "looked a lot like Java" and was born with the ECMA goal "simple, modern, general-purpose object-oriented"; no generics, no LINQ | 15-16 |
| **C# 1.2** | April/2003 | Visual Studio .NET 2003 | the `foreach` code started calling `Dispose` on the `IEnumerator` when it implements `IDisposable` | 15 |
| **C# 2.0** | November/2005 | Visual Studio 2005 | generics, partial types, anonymous methods, nullable value types, iterators, covariance and contravariance; also: separate accessibility for `get`/`set`, method group conversions, static classes, delegate inference | 14-15 |
| **C# 3.0** | November/2007 | Visual Studio 2008 (full features with .NET Framework 3.5) | auto-implemented properties, anonymous types, query expressions (LINQ), lambdas, expression trees, extension methods, implicitly typed local variables, partial methods, object and collection initializers | 13-14 |
| **C# 4.0** | April/2010 | Visual Studio 2010 | `dynamic`, named/optional arguments, generic covariance/contravariance, embedded interop types | 12-13 |
| **C# 5.0** | August/2012 | Visual Studio 2012 | asynchronous members (`async`/`await`), caller info attributes | 12 |
| **C# 6.0** | July/2015 | Visual Studio 2015 | static imports, exception filters, auto-implemented property initializers, expression-bodied members, null propagator (`?.`), string interpolation, `nameof`, index initializers, `await` in `catch`/`finally`, default values for get-only properties; launch of Roslyn (compiler written in C#) | 11-12 |
| **C# 7.0** | March/2017 | Visual Studio 2017 | out variables, tuples and deconstruction, pattern matching, local functions, expanded expression-bodied members, ref locals and ref returns, discards, binary literals and digit separators, throw expressions | 10-11 |
| **C# 7.1** | August/2017 | (language version selection option) | `async Main`, `default` literal, inferred tuple element names, pattern matching on a generic type parameter | 10 |
| **C# 7.2** | November/2017 | – | `readonly struct`, `in` modifier, `ref readonly` return, `ref struct`, non-trailing named arguments, leading `_` in literals, `private protected`, `?:` with ref | 9-10 |
| **C# 7.3** | May/2018 | – | access to fixed fields without pinning, reassigning ref locals, initializers on `stackalloc`, `fixed` with any type that follows the pattern, more generic constraints, `==`/`!=` on tuples, attributes on the backing field, overload resolution improvements; options `-publicsign`, `-pathmap` | 8-9 |
| **C# 8.0** | September/2019 | first release aimed at .NET Core (features depend on the CLR/libraries of .NET Core 3.0) | `readonly` members, default interface members, switch expressions, property/tuple/positional patterns, `using` declarations, static local functions, shadowing in lambdas, disposable `ref struct`, **nullable reference types**, asynchronous streams, indices and ranges, `??=`, unmanaged constructed types, nested `stackalloc`, interpolated verbatim string | 7-8 |
| **C# 9** | November/2020 | .NET 5 (default language for those targeting .NET 5) | **records**, init-only setters, top-level statements, relational and logical patterns (`and`/`or`/`not`); `nint`/`nuint`, function pointers, `localsinit`, module initializers, extended partial methods; target-typed `new`, static anonymous functions, target-typed conditional, covariant returns, extension `GetEnumerator` in `foreach`, discards in lambdas, attributes on local functions | 5-7 |
| **C# 10** | November/2021 | .NET 6 (runtime performance improvements cited) | record structs, struct improvements, interpolated string handlers, `global using`, file-scoped namespace, extended property patterns, natural type and return type for lambdas, attributes on lambdas, interpolated `const`, `sealed` on a record's `ToString`, more precise assignment/nullability analysis, `CallerArgumentExpression`, new `#line`; preview: generic attributes and static abstract in interfaces; the annual cadence begins | 4-5 |
| **C# 11** | November/2022 | – (.NET version not stated) | raw string literals, generic math, generic attributes, UTF-8 literals, newlines in interpolation, list patterns, file-local types, `required`, auto-default structs, matching `Span<char>` against a constant, extended `nameof`, `nint` and `uint` as aliases of `IntPtr`/`UIntPtr` (source's wording), ref fields and `scoped ref`, improved method group conversion, warning wave 7 | 3-4 |
| **C# 12** | November/2023 | .NET 8 (CS12 p.1) | primary constructors, collection expressions (with `..e`), inline arrays, optional parameters in lambdas, `ref readonly` parameters, alias for any type, `Experimental` attribute, Interceptors (preview) | 2-3; CS12 p.1-6 |
| **C# 13** | November/2024 | .NET 9 (CS13 p.1) | `params` collections, new `lock` type/semantics, `\e` escape, overload resolution optimizations on method groups, `^` access in object initializers, `ref` locals and `unsafe` in iterators/async, `ref struct` implements interfaces, `allows ref struct`, partial properties and indexers, overload resolution priority; `field` as preview (VS 17.12) | 2; CS13 p.1-7 |
| **C# 14** | November/2025 | – (.NET version not stated) | extension members, null-conditional assignment, `nameof` with unbound generic types, more implicit conversions to `Span<T>`/`ReadOnlySpan<T>`, modifiers on simple lambda parameters, properties with `field`, partial events and constructors, user-defined compound operators | 1 |

All rows: `[from source]` on the pages in the last column. The English terms above translate the names of the features that the source lists.

## 2. Context the sources give (by version)

- **C# 2.0, generics**: with `List<T>` there can be `List<string>` and `List<int>` with type-safe operations; "better than a `ListInt` type derived from `ArrayList` or casting `Object`" `[from source] (CSHist p.14)`. Iterators let you examine a list with `foreach`, gaining readability `[from source] (CSHist p.15)`.
- **C# 3.0**: the main feature is the query expression (LINQ); lambdas, expression trees and anonymous types are the foundation; "instead of a `for` for the average of a list, `list.Average()`"; the beginning of hybrid OO/functional C# `[from source] (CSHist p.13-14)`.
- **C# 4.0**: `dynamic` lets you ignore compile-time typing, as in dynamic languages; "potential for errors, but also great power" `[from source] (CSHist p.13)`.
- **C# 6.0**: small features to eliminate "boilerplate"; Roslyn: the compiler is now written in C# and can be used as a service `[from source] (CSHist p.12)`.
- **C# 7.2**: `readonly struct` indicates an immutable struct that should be passed as `in` to its methods; `ref struct` indicates a struct that accesses managed memory and must always stay on the stack `[from source] (CSHist p.9)`.
- **C# 8**: "first major release specifically for .NET Core"; default interface members require CLR improvements (.NET Core 3.0); indices/ranges and asynchronous streams require new library types; NRT is more useful when libraries are annotated `[from source] (CSHist p.7-8)`.
- **C# 9**: records = concise syntax for reference types with value semantics for equality; init-only setters provide non-destructive mutation (`with`); return covariance is available to derived records; `top-level statements` do away with the namespace, the `Program` class and `static void Main()` `[from source] (CSHist p.6)`; an `e is not null` pattern is the new null test `[from source] (CSHist p.6)`.
- **C# 10**: structs and anonymous types support `with`; record structs synthesize methods similar to those of record classes `[from source] (CSHist p.4)`; annual .NET cadence; generic attributes and static abstract members in interfaces remained as preview `[from source] (CSHist p.5)`.
- **C# 11**: "C# 11 introduces generic math"; writing numeric algorithms only once for all numeric types; required members and auto-default structs help structs; file-local types simplify source generators `[from source] (CSHist p.3-4)`.
- **C# 12/13**: see `recursos-modernos.md`. C# 12 is supported on .NET 8 `[from source] (CS12 p.1)`; C# 13 on .NET 9 `[from source] (CS13 p.1)`.
- **C# 14**: lists only the names `[from source] (CSHist p.1)`.

## 3. Version not stated in the sources `[extrapolation]`

Questions of the type "in which version did X arrive?" for features that are **not** in the lists above: answer "version not stated in the sources" and, if supplementing, label it `[extrapolation]`. Examples: Visual Studio/SDK per version (the sources only give VS 2022 17.5-17.8 for the C# 12 feature *previews*, CS12 p.1, and VS 17.12 for `field`, CS13 p.1), .NET 7 for C# 11, .NET 10 for C# 14, third-party libraries.

## 4. Languages and frameworks

C# 1.0 "was a viable alternative to Java on the Windows platform" `[from source] (CSHist p.15)`. The CSYB examples are from .NET Framework, WPF and Windows 8 `[DATED]` `[from source] (CSYB p.16, 189)`.
