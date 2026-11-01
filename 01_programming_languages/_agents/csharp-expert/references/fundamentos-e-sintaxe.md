# C# fundamentals and syntax (CSYB, ch. 1-3 and 4.2/4.11)

Convention: `(CSYB p.N)` = PDF page (printed = N − 5). Everything without `[from source]` is `[inference]`, `[extrapolation]` or `[DATED]`, as indicated. Code examples are illustrative (not literal excerpts from the book).

## 1. Origin and execution model

- C# was created by Microsoft and resembles C++ and Java `[from source] (CSYB p.15)`.
- The book describes **managed** code (watched over by the system, slower) and **unmanaged** code (faster, can crash the computer) `[from source] (CSYB p.15-16)`.
- C# is compiled: a compiler converts the C# text into low-level instructions, which are then turned into hardware commands `[from source] (CSYB p.16)`.
- The tools cited are Visual Studio (free Express edition) and the .NET Framework command-line tools `[from source] (CSYB p.16)` `[DATED]`.
- Example program: `using System;`, a `class` with `static void Main()` (and only one `Main`), `Console.ReadLine()`, `double.Parse(...)` `[from source] (CSYB p.19-23)`. There is no namespace declaration in this program `[from source] (CSYB p.19)`.
- `Main` is the starting point; without it the system "does not know where to start" `[from source] (CSYB p.20)`.
- A semicolon ends each statement `[from source] (CSYB p.22)`; layout does not matter to the compiler, only to the reader `[from source] (CSYB p.26)`.
- Top-level statements (C# 9) do away with the namespace, the `Program` class and `static void Main()` `[from source] (CSHist p.6)`.
- [extrapolation] CIL, CLR, JIT, Roslyn, `dotnet new/build/run`, `.csproj`, SDK: outside the sources. See `procedimentos.md` §1.

## 2. Numeric types, text and `bool`

### Integers
- The book's table (bits and range): `sbyte` 8 (−128..127), `byte` 8 (0..255), `short` 16, `ushort` 16, `int` 32 (−2,147,483,648..2,147,483,647), `uint` 32, `long` 64, `ulong` 64, `char` 16 (0..65,535) `[from source] (CSYB p.28)`.
- The book warns that exceeding the limit may go undetected: `byte` 255 + 1 "may wrap around" to 0 `[from source] (CSYB p.28)`.
- A literal outside the range of the short type (`sbyte tinyVal = 128;`) gives a compile error `[from source] (CSYB p.29)`.
- [extrapolation] `checked`/`unchecked`/`OverflowException` are not in the book.

### Reals: `float`, `double`, `decimal`
- `float`: precision of **7 digits**; `double`: **15 digits**; `decimal`: uses twice the space of `double`, **28-29 digits**, for financial calculation `[from source] (CSYB p.29)`.
- A literal without a suffix is `double`; with `f` it is `float` `[from source] (CSYB p.29, 36)`. `float x = 3.4;` does not compile; use `3.4f` or a cast `[from source] (CSYB p.36)`.
- The author uses `decimal` for account balances `[from source] (CSYB p.99, 102)` and suggests storing prices in cents (150 pence) instead of floating point `[from source] (CSYB p.32)`.
- [extrapolation] the `m` suffix (`99.95m`) for `decimal` literals: it does not appear in the book. Without it the literal is `double` and does not convert implicitly to `decimal`.
- [inference] 128 bits for `decimal` = "twice the `double`" (64 bits, which the book does not state). Treat 128 bits as [extrapolation].

### Text
- `char`: a single character, single quotes; Unicode with "more than 65,000" glyphs `[from source] (CSYB p.30)`. Escapes `\' \" \\ \0 \a \b \f \n \r \t \v` and `\x0041` `[from source] (CSYB p.30-31)`.
- `string`: double quotes; `@"..."` (verbatim) ignores escapes and allows multiple lines, useful for paths `[from source] (CSYB p.31, 82-83)`. Concatenation with `+` converts the other operand to text `[from source] (CSYB p.24-25)`.
- Strings are **immutable**: "changing" one creates another string `[from source] (CSYB p.136, 208)`. `s1 == s2` compares the text `[from source] (CSYB p.137)`.
- The book's string methods: `Substring`, `Length`, `ToUpper`/`ToLower`, `Trim`/`TrimStart`/`TrimEnd`, indexing `name[0]` (read-only) `[from source] (CSYB p.137-138)`; `char.IsDigit`, `IsLetter`, `IsLetterOrDigit`, `IsLower`, `IsUpper`, `IsPunctuation`, `IsWhiteSpace` `[from source] (CSYB p.138)`; heavy editing with `StringBuilder` (`System.Text`) `[from source] (CSYB p.138)`.
- [extrapolation] UTF-16, heap allocation and `string.Intern` are not covered.

### `bool`
- Only `true` or `false`; the book keeps state in `bool` `[from source] (CSYB p.32)`.
- [extrapolation] C# does not convert `int` to `bool` (`if (n)` does not compile; use `n != 0`): a language fact, not stated in the book.

### Identifiers
- Start with a letter; then letters, digits or `_`; upper and lower case differ `[from source] (CSYB p.32)`. Camel-case convention for variables `[from source] (CSYB p.33)`; constants in UPPER CASE, `const` `[from source] (CSYB p.43)`.

## 3. Expressions, operators and conversions

- Precedence: unary minus, `*`, `/`, `+`, `-`; `2 + 3 * 4` gives 14; parentheses force the order; the book says the list is not complete `[from source] (CSYB p.34)`.
- **Widening** (everything fits) is implicit; **narrowing** requires an explicit cast: `float f = (float) d;` `[from source] (CSYB p.35)`. The cast "washes the compiler's hands": the programmer takes the risk `[from source] (CSYB p.35)`.
- A cast from real to integer **discards** the fractional part: `(int)1.999` gives 1 `[from source] (CSYB p.36)`.
- Integer division truncates: `1/2` is 0 and `1/2.0` is 0.5 `[from source] (CSYB p.36)`; use a cast to control the operator: `(float) i / (float) j` `[from source] (CSYB p.37)`. The book's trick for rounding up: `(n + 99) / 100` `[from source] (CSYB p.38)`.
- `double.Parse` converts text to a number `[from source] (CSYB p.19, 23-24)`; invalid input throws an exception (`FormatException`) `[from source] (CSYB p.72)`. Handling: `try`/`catch` around the `Parse` `[from source] (CSYB p.72-73)`.
- [extrapolation] `int.TryParse(text, out n)` avoids the exception; it is not in the book. The `%` operator is not in the book either.
- Comparing reals: `==` and `!=` with floating point "is not meaningful" because of limited precision (example `3.0 * (1.0/3.0)` may give 0.99999999); the book says to **subtract and check whether the difference is very small** `[from source] (CSYB p.41)`. [extrapolation] `Math.Abs(a - b) < tolerance` is the usual way to write this.
- Relational `== != < <= > >=` and `!` `[from source] (CSYB p.41)`; `&&` and `||` `[from source] (CSYB p.41-42)`. De Morgan's laws when inverting conditions `[from source] (CSYB p.42, 48)`. [extrapolation] short-circuiting of `&&`/`||`: a language fact, absent from the book.

## 4. Flow control

- `if (cond) ... else ...`; the `else` is optional; a `{ }` block groups statements `[from source] (CSYB p.40, 42)`.
- Loops: `do ... while (cond);` runs at least once `[from source] (CSYB p.45)`; `while (cond)` tests first `[from source] (CSYB p.45)`; `for (setup; test; update)` `[from source] (CSYB p.46-47)`. Changing the control variable inside the `for` "does stupid things" `[from source] (CSYB p.47)`.
- `break` leaves the loop; the author asks for caution (a relative of `goto`) `[from source] (CSYB p.47-48)`; `continue` goes back to the top of the loop `[from source] (CSYB p.48)`.
- Shortcuts: `++`, `--`, `+=`, `-=`, `*=`, `/=`; `i++` gives the value before, `++i` the value after; every assignment returns the assigned value `[from source] (CSYB p.49-50)`.
- `switch (value) { case 1: ...; break; default: ...; break; }`; accepts numbers and strings; several consecutive `case` labels share the same block; `default` covers the rest; the book suggests `ToUpper()`/`ToLower()` to compare commands and putting method calls (not much code) inside the `case` `[from source] (CSYB p.76-78)`. [extrapolation] the rule "without `break`/`return`/`goto case` there is no fall-through" is not stated in the book.
- `foreach` appears once, as a "new loop" over the `Values` of a hash table `[from source] (CSYB p.159)`; the glossary says collections support enumeration for the `foreach` `[from source] (CSYB p.205)`.
- Output formatting: `Console.WriteLine("i: {0} f: {1:0.00}", i, f)`; `{0,10:0}` width, `{0,-10:0}` left-aligned, `#,##0` `[from source] (CSYB p.51-52)`.

## 5. Methods

- Method = a named block; it helps with reuse and with breaking tasks down `[from source] (CSYB p.53-54)`. A parameter receives a copy of the value `[from source] (CSYB p.54)`; `return` returns a value; `void` returns nothing `[from source] (CSYB p.55)`.
- A **parameter** is the variable in the header; an **argument** is the value in the call `[from source] (CSYB p.55)`.
- Named arguments (`readValue(low: 25, high: 100, prompt: "")`) and optional ones (default value; optionals come after the required ones) `[from source] (CSYB p.58-59)`. The author "doesn't like" defaults that much, because they hide behavior `[from source] (CSYB p.59)`.
- Passing **by value**: changing the parameter does not change the caller's variable `[from source] (CSYB p.59-60)`.
- By **reference** (`ref`): the method operates on the variable itself; `ref` goes in the header **and** in the call `[from source] (CSYB p.60-61)`. Document side effects `[from source] (CSYB p.61)`.
- `out`: the method only delivers a result; the compiler guarantees that it assigns the parameter; allows returning more than one value; `out` goes in the call too `[from source] (CSYB p.61)`.
- Think about how the method fails (return code, exception) `[from source] (CSYB p.63)`.
- [extrapolation] that `ref` requires an initialized variable and `out` does not: C# rules, not stated that way in the book.

## 6. Scope

- The scope of a local variable is the block where it was declared; on leaving the block it is discarded `[from source] (CSYB p.64)`.
- An inner block **cannot** reuse a variable name from the outer block (unlike C++); successive blocks may repeat the name `[from source] (CSYB p.64-65)`.
- A `for (int i = ...)` variable lives only in the loop `[from source] (CSYB p.65)`. A class member is shared among methods (it must be `static` in a static `Main`); `static` ≠ `const` `[from source] (CSYB p.65-66)`.

## 7. Arrays

- `int [] scores = new int [11];` creates the "box" and `scores` is the label `[from source] (CSYB p.67-68)`. Elements start as 0 `[from source] (CSYB p.68)`.
- The index starts at 0; there is no `scores[11]` in an array of 11; going outside the array "makes the program fail" `[from source] (CSYB p.68)`. [extrapolation] the exception is `IndexOutOfRangeException` (name absent from the book).
- Use `const int` for the size `[from source] (CSYB p.68-69)`. 2D arrays `int [,] board = new int [3,3];` `[from source] (CSYB p.69)`; initializers `new string[] { ... }` `[from source] (CSYB p.70)`; the book recommends few dimensions and preferring arrays of `struct` `[from source] (CSYB p.71)`.
- An array of objects holds references, all `null` at the start `[from source] (CSYB p.145)`.

## 8. Enumerations

- `enum SeaState { EmptySea, Attacked, ... }` creates a type with named values; use `SeaState.EmptySea`; "use enumerated types often" `[from source] (CSYB p.85-86)`.

## 9. Outside the book (labeled summary)

| Topic | Status |
| :-- | :-- |
| `checked`/`unchecked`, `OverflowException` | [extrapolation] |
| `m` suffix; `decimal` = 128 bits | [extrapolation] |
| `int.TryParse`, `%`, short-circuiting, `int`→`bool` | [extrapolation] |
| `switch` fall-through rule | [extrapolation] |
| `var`, interpolation `$""`, tuples, `switch` expression | names only in CSHist (see `versoes-e-evolucao.md`) |
