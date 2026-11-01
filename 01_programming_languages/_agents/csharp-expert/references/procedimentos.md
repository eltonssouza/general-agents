# Step-by-step procedures

Convention: `(CSYB p.N)`, `(CSHist p.N)`, `(CS12 p.N)`, `(CS13 p.N)` = PDF page. Each step says where it comes from: `[from source]` (on the cited pages), `[inference]` or `[extrapolation]` (general C#/.NET knowledge, absent from the sources). Illustrative code.

## 1. Write, compile and run

1. **Specify before programming**: the book insists on a specification and on test triggers before the code `[from source] (CSYB p.9-13, 103)`.
2. **Write the source** in a file (`.cs`); the convention is to name the file after the class (`GlazerCalc.cs`) `[from source] (CSYB p.20)`. The program needs **a single** `static void Main()` `[from source] (CSYB p.20)`; `using System;` opens the `Console` namespace `[from source] (CSYB p.20, 80)`.
3. **Compile**: the compiler points out errors (it only produces output when there are none) and warnings `[from source] (CSYB p.16)`; read the message (e.g. `CS0165`, `CS0120`, `CS0535`) `[from source] (CSYB p.93, 106, 117)`.
4. **Library**: without `Main`, compile as a library: `csc /target:library AccountManagement.cs` and reference it with `/reference:` `[from source] (CSYB p.185)` `[DATED]` (command line of the time).
5. **Run** and check the result with tests `[from source] (CSYB p.102-103)`.
6. `[extrapolation]` In modern .NET: `dotnet new console -n App`, `dotnet build`, `dotnet run`; the `.csproj` defines the language version (`LangVersion`) and the *target framework*; the compiler (Roslyn) generates CIL, which the runtime compiles (JIT). None of this is in the sources. For C# 12/13 the .NET 8/9 SDK is needed `[from source] (CS12 p.1; CS13 p.1)`.

## 2. Choose the right type

Decision order (rules 1-4 have grounding; 5-6 are `[extrapolation]`):

1. **A fixed set of named states/values?** → `enum` `[from source] (CSYB p.85-86)`.
2. **Only the contract (what to do, not how)?** → `interface`; naming convention `I...`; reference objects through the interface; tests attach to it `[from source] (CSYB p.116-120, 130)`.
3. **A family of types with common code and mandatory parts to implement?** → `abstract` class (a single parent) combined with an interface `[from source] (CSYB p.128-130)`.
4. **Group related data into a block that is copied (value)?** → `struct`; **identity, shared references, behavior and inheritance?** → `class` `[from source] (CSYB p.87-92, 211)`. [inference] the book gives no size limit or mutability rule for structs.
5. **Data with value equality and copy-with-change (`with`)?** → `record`/`record struct` `[from source] (CSHist p.4, 6)` `[VERSION-DEPENDENT]` (C# 9/10). Details of what the compiler generates = `[extrapolation]`.
6. `[extrapolation]` Common guidelines: small struct (on the order of 16 bytes), immutable and short-lived; avoid mutable structs.

## 3. Triage a runtime error (stack trace)

1. **Read the type and message** of the exception (`FormatException: Input string was not in a correct format.`) `[from source] (CSYB p.72-73)`.
2. **Find the first frame of your code**: the trace lists `at ...Main(String[] args)`; ignore library frames (those starting with System) `[from source] (CSYB p.72)` (the example shows `System.Number` frames followed by the user's method) `[inference]`.
3. **Reproduce**: failures that "always happen" are easy; intermittent ones require finding the sequence; changing the code/data layout and seeing the failure change indicates memory corruption `[from source] (CSYB p.200-201)`.
4. **Classify**: crash (unforeseen state, loop, recursion, unhandled exception) or wrong answer (uninitialized, typo, logic) `[from source] (CSYB p.201)`.
5. **Fix and test**: run the automated tests after the fix ("fixes cause bugs") `[from source] (CSYB p.202)`.
6. `[extrapolation]` Mapping exception → cause (`NullReferenceException`, `IndexOutOfRangeException`, `InvalidCastException`, `DivideByZeroException`, `ArgumentException`, `OverflowException`) and *inner exceptions*: names absent from the book. The script `parse_cs_stack.py` labels each item as book or extrapolation.

## 4. Protect data shared between threads

1. **Decide by design**: threads must be in the design from the start `[from source] (CSYB p.180)`.
2. **Identify the shared variable** (e.g. a counter) and the read-modify-write section `[from source] (CSYB p.177)`.
3. **Create the token object**: `static object sync = new object();` and wrap the section in `Monitor.Enter(sync); ...; Monitor.Exit(sync);` `[from source] (CSYB p.178)`.
4. **Avoid the deadly embrace** (A waits for B, B waits for A): separate producers and consumers `[from source] (CSYB p.178, 180)`.
5. `[extrapolation]` In modern code, use `lock (_gate) { ... }` (guarantees `Exit` even with an exception), with `_gate` a private `readonly` field; never `lock(this)`/`lock(typeof(T))`/string. With C# 13/.NET 9, declare `_gate` as `System.Threading.Lock`: `lock` then uses `Lock.EnterScope()` and nothing else changes `[from source] (CS13 p.2)` `[VERSION-DEPENDENT]`.

## 5. Read and write text files

1. `using System.IO;` `[from source] (CSYB p.80-81)`.
2. **Write**: `StreamWriter w = new StreamWriter("dados.txt"); w.WriteLine("..."); w.Close();`; note: an existing file is replaced `[from source] (CSYB p.79-80)`.
3. **Read**: `StreamReader r = new StreamReader("dados.txt"); while (!r.EndOfStream) { string l = r.ReadLine(); ... } r.Close();` `[from source] (CSYB p.81-82)`.
4. **Guarantee closing** with `try/catch/finally` and `Close()` in the `finally` `[from source] (CSYB p.156, 158)`.
5. **Paths**: no folder = the program's folder; use `@` before the literal (e.g. `c:\data\2009\November\sales.txt`) `[from source] (CSYB p.82-83)` `[HOST]`.
6. `[extrapolation]` Modern form: `using var w = new StreamWriter(...)` (disposal on leaving the scope); CSHist mentions "using declarations" in C# 8 (p.8).

## 6. Debug without guessing

1. Gather the report with reproducible steps; "no steps, discard it" is an argument of the author `[from source] (CSYB p.200)`.
2. Do not assume: add code that **proves** what you believe `[from source] (CSYB p.201)`.
3. Explain the problem to someone else; step away for a while; go back to the last good state and reintroduce changes with version control `[from source] (CSYB p.201-202)`.
4. Only debug what **should** work: know how the program should behave before changing it `[from source] (CSYB p.202)`.
5. Consider "starting over" when it is cheaper `[from source] (CSYB p.202)`.

## 7. Test business objects

1. Write tests that call the methods and check the effect; count the errors and make a negative result impossible to ignore `[from source] (CSYB p.102-103)`.
2. Prefer TDD: tests first `[from source] (CSYB p.103)`.
3. Attach tests to the **interface** to test all the components that implement it `[from source] (CSYB p.120)`.
4. Also test the error handlers `[from source] (CSYB p.183)`.
5. `[extrapolation]` xUnit/NUnit/MSTest are external tools; the book mentions *unit test* only in the glossary `[from source] (CSYB p.212)`.
