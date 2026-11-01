# Pitfalls and antipatterns in C# (12 cases)

Convention: `(CSYB p.N)`, `(CSHist p.N)`, `(CS12 p.N)`, `(CS13 p.N)` = PDF page. Each case carries its **level of grounding**:

- **Book**: the advice is in the cited text.
- **Partial**: the book covers the problem, but the modern recommendation is extrapolation.
- **Extrapolation**: a known C#/.NET antipattern, absent from the sources (use `[extrapolation]` when answering).

The code snippets are illustrative, written for this package.

---

## 1. Struct changed by value (the silent copy) — grounding: partial

- **Source**: assigning or passing a struct copies the values; changing the copy does not change the original `[from source] (CSYB p.89-90)`; glossary "copied on assignment; passed by value" `[from source] (CSYB p.211)`.
- **Defect**: `void Deslocar(Ponto p) { p.X += 10; }` changes only the copy; the caller still has `X = 5`.
- **Fix**: return the changed struct (`Ponto Deslocar(Ponto p)`), pass it with `ref` `[from source] (CSYB p.60-61)` or use `class` if shared identity matters `[from source] (CSYB p.92-95)`.
- `[extrapolation]` Prefer immutable structs (`readonly struct`, cited as a C# 7.2 feature in CSHist p.9); "mutable struct is an antipattern" is a general recommendation, not the book's.

## 2. Null reference — grounding: partial

- **Source**: `Account a;` creates only the label; without `new` there is no object (compile error for an unassigned local variable) `[from source] (CSYB p.93-94)`; arrays of objects start with `null` `[from source] (CSYB p.145)`; `FindAccount` returns `null` and the caller tests it `[from source] (CSYB p.146, 157)`; forgetting the test makes the program "follow a null reference" and fail `[from source] (CSYB p.157)`.
- **Fix**: test before using (`if (conta != null)`); document when a method returns `null` `[from source] (CSYB p.157)`.
- **Modern features**: the `?.` propagator (C# 6) `[from source] (CSHist p.11)`; nullable reference types (C# 8) `[from source] (CSHist p.8)`; the `is not null` test (C# 9) `[from source] (CSHist p.6)`.
- `[extrapolation]` The runtime exception is called `NullReferenceException` (name absent from the book); `?.` returns `null` along the chain and can be combined with `??`.

## 3. `ArrayList`/`Hashtable` instead of generic collections — grounding: book

- **Source**: `ArrayList` stores `object`, requires a cast and is not type safe (accepts anything) `[from source] (CSYB p.150-151)`; `List<T>` and `Dictionary<TKey,TValue>` check types at compile time and need no cast `[from source] (CSYB p.151-153)`; recommendation: use them "in preference to hashtables and arraylists" `[from source] (CSYB p.153)`; the history compares generics with `ArrayList` `[from source] (CSHist p.14)`.
- **Fix**: `List<Conta>`, `Dictionary<string, Conta>`; test `ContainsKey` before indexing `[from source] (CSYB p.153)`.
- `[extrapolation]` Boxing/unboxing: storing an `int` in an `ArrayList` wraps the value in an `object` (cost); the book does not mention it.

## 4. Swallowed or misused exceptions — grounding: partial

- **Source**: "don't catch everything": if there is no way to really handle it, let the exception propagate instead of returning an empty object, since that only postpones the failure `[from source] (CSYB p.74)`; exceptions for what really prevents the program from continuing (an out-of-range value calls for a message, not an exception) `[from source] (CSYB p.75)`; test the handlers `[from source] (CSYB p.183)`; create your own exception types derived from `System.Exception` `[from source] (CSYB p.181-182)`.
- **Caution**: the book itself uses `catch { return false; }` and `return null` in `Save`/`Load` as a documented convention, and says that nowadays it prefers to throw `[from source] (CSYB p.156-157)`. Nuance: an empty `catch` with no signal to the caller is different from one that returns an indicator.
- `[extrapolation]` When rethrowing, use `throw;` (preserves the stack trace); `throw ex;` resets it. The book only shows `throw new ...` `[from source] (CSYB p.75, 182)`.

## 5. Data shared between threads without mutual exclusion — grounding: book (mechanism) / extrapolation (lock target)

- **Source**: two threads incrementing `overDraftCount` lose updates; the book describes the sequence `[from source] (CSYB p.177)`; solution with a token object and `Monitor.Enter`/`Monitor.Exit` `[from source] (CSYB p.178)`; protect all shared variables, avoid the "deadly embrace" `[from source] (CSYB p.178, 180)`.
- **C# 13**: `System.Threading.Lock`; `lock` uses `Lock.EnterScope()`; to get the benefit it is enough to change the type of the locked object `[from source] (CS13 p.2)` `[VERSION-DEPENDENT]`.
- `[extrapolation]` The `lock` statement is the usual form (sugar over `Monitor`); avoid `lock(this)`, `lock(typeof(T))`, `lock("text")`; use a private, `readonly` field. The book mentions neither `lock` nor these targets.

## 6. Stream not closed — grounding: book

- **Source**: forgetting `Close()` may lose data, prevents other programs from using/moving/renaming the file and consumes a system resource `[from source] (CSYB p.80)`; pattern with `try/catch/finally` and `Close()` in the `finally` `[from source] (CSYB p.156, 158)`.
- **Fix**: close in the `finally`.
- `[extrapolation]` `using`/`using var` (which calls `Dispose`) is the modern form and is equivalent to `try/finally`; CSHist only mentions "using declarations" in C# 8 (p.8).

## 7. Comparing `float`/`double` with `==` — grounding: book

- **Source**: "it is not meaningful to compare floating-point values" for equality: `3.0 * (1.0/3.0)` may give 0.99999999 and `x == 1.0` fails; subtract and check whether the difference is very small `[from source] (CSYB p.41)`; `!=` likewise `[from source] (CSYB p.41)`.
- **Monetary values**: `decimal` (28-29 digits) for finance `[from source] (CSYB p.29)`; the author also suggests integers in cents `[from source] (CSYB p.32)`.
- `[extrapolation]` `Math.Abs(a - b) < tolerance` and the `m` suffix (`10.5m`).

## 8. `new` instead of `override` — grounding: partial

- **Source**: without `virtual`/`override` the child's method is a replacement and the compiler asks for `new` `[from source] (CSYB p.125)`; the author is "very much against" replacing methods and prefers `override` `[from source] (CSYB p.126)`; `virtual` + `override` form the pair `[from source] (CSYB p.122-123)`.
- `[extrapolation]` Effect on dispatch: `Conta c = new Poupanca(); c.Imprimir();` runs the **base** method if the child used `new`, and the child's if it used `override`.

## 9. Array bounds error (*off-by-one*) — grounding: book

- **Source**: indexes start at 0; there is no `scores[11]` in an array of 11; going past the array crashes the program `[from source] (CSYB p.68)`; use `i < TAMANHO` with a constant `[from source] (CSYB p.68-69)`.
- `[extrapolation]` The exception is called `IndexOutOfRangeException`; `foreach` avoids manual indexes.

## 10. Modern feature on an old language/SDK — grounding: book

- **Source**: new features may require new libraries/types; each version page documents the dependencies `[from source] (CSHist p.1)`; C# 12 is supported on .NET 8 `[from source] (CS12 p.1)`; C# 13 on .NET 9 `[from source] (CS13 p.1)`; C# 8 depends on the CLR/libraries of .NET Core 3.0 `[from source] (CSHist p.8)`.
- **Fix**: look up the feature's version (`cs_version_lookup.py`), check the project's language and SDK version; *preview* features (Interceptors, `field` in C# 13) require opt-in `[from source] (CS12 p.5-6; CS13 p.7)`.
- `[extrapolation]` How to pin `LangVersion` in the project.

## 11. `Parse` without handling — grounding: book

- **Source**: `Parse` (e.g. `int.Parse`) throws an exception for invalid text; without a `catch`, the program terminates `[from source] (CSYB p.72)`; wrap it in `try/catch` and show a message `[from source] (CSYB p.72-73, 199)`.
- `[extrapolation]` `TryParse` avoids the exception and returns `bool`.

## 12. Exposed static or public state — grounding: book

- **Source**: private data, public methods `[from source] (CSYB p.100-101)`; `static` = member of the class, not a "constant" `[from source] (CSYB p.104)`; a changed static value affects the whole system, so it must be private and changed through methods `[from source] (CSYB p.105)`; admitted exception: public data when performance matters more `[from source] (CSYB p.101)`.
- **Fix**: encapsulate with properties or accessor methods `[from source] (CSYB p.139-141)`.
