# Advanced features and execution (CSYB, ch. 3.4, 3.6, 4.12-4.13 and 5)

Convention: `(CSYB p.N)` = PDF page (printed = N − 5). Code examples are illustrative. What does **not** come from the book is labeled and collected in section 9.

## 1. Exceptions

- `Parse` (e.g. `int.Parse`) throws an exception when the text is invalid; without a `catch`, the system shows the exception and terminates the program; the book's example shows `System.FormatException` `[from source] (CSYB p.71-72)`.
- `try { ... } catch { ... }`: when something is thrown, flow goes to the `catch` and **does not return** to the `try` `[from source] (CSYB p.72)`.
- `catch (Exception e)` gives access to `e.Message` `[from source] (CSYB p.73)`. `try` blocks can be nested; the `catch` at the matching level applies `[from source] (CSYB p.73-74)`.
- "Don't catch everything": do not try to handle every exception; if a `Load` does not find the file, the best thing is to throw "file not found" instead of returning an empty object, since the placeholder only postpones the error `[from source] (CSYB p.74)`.
- `finally`: runs **with or without** an exception; it is used to close files and release resources, even if the `catch` returns or throws `[from source] (CSYB p.74-75, 207)`.
- `throw new Exception("Boom");` creates and throws; reserve exceptions for situations in which the program really cannot continue (an invalid height value is handled with a message, not an exception) `[from source] (CSYB p.75)`.
- Custom exception: `public class BankException : System.Exception` with a constructor `: base(message)`; the thrown object must derive from `System.Exception`; the book recommends custom types (even with an error number) `[from source] (CSYB p.181-182)`.
- Several `catch` blocks in sequence match by type; the one for `System.Exception` comes last `[from source] (CSYB p.182-183)`.
- Error-handling code is rarely exercised, so "programs fail in the handlers"; test them `[from source] (CSYB p.183)`.
- Constructors can only fail by throwing an exception `[from source] (CSYB p.112-113)`; `Dictionary` throws `KeyNotFoundException` for a missing key `[from source] (CSYB p.153)`; `FileNotFoundException` appears in the removed-DLL example `[from source] (CSYB p.186)`.
- The book's own practical handling: `Save` uses `catch { return false; }` and `Load` returns `null`, closing the file in `finally`; the author admits that nowadays he prefers to throw an exception in such cases `[from source] (CSYB p.156-157)`.
- `as` returns `null` if the type does not match; a cast `(IAccount)` fails with an exception `[from source] (CSYB p.148)`.

## 2. Collections and generics

- An array has a fixed size; going past the size crashes the program `[from source] (CSYB p.149)`.
- **`ArrayList`** (`System.Collections`): "an array that grows"; `Add`, `Remove`, `Count`, `Contains`; it stores references to `object`, so a **cast** is needed when reading (`(Account) store[0]`) `[from source] (CSYB p.149-151)`. It is **not type safe**: it accepts a `KitchenSink` in the middle of accounts and the problem (an exception) only shows up on use `[from source] (CSYB p.150-151)`.
- **`List<T>`** (`System.Collections.Generic`): everything `ArrayList` does, with type checking **at compile time** and no cast `[from source] (CSYB p.151-152)`. Generics = abstraction: the list behavior holds for any type `[from source] (CSYB p.151-152)`.
- **`Dictionary<TKey,TValue>`**: the typed version of `Hashtable`; `Add`, indexer, `ContainsKey`; duplicate keys are not allowed; missing key → `KeyNotFoundException` `[from source] (CSYB p.152-153)`.
- The author's recommendation: "whenever you need to store a bunch of things, make a `List`; to find by key, `Dictionary`; use them in preference to hashtables and arraylists" `[from source] (CSYB p.153)`.
- Generics arrived in C# 2.0; the history compares `List<T>` with deriving from `ArrayList` or casting `Object` `[from source] (CSHist p.14)`.
- `[DATED]` `ArrayList` and `Hashtable` (the book itself ranks them as inferior, p.153). Writing custom generic types is "out of scope" of the text `[from source] (CSYB p.153)`.

## 3. Files and streams

- *Stream* = connection between the program and a resource (file, network, console); `Console` is a stream `[from source] (CSYB p.78-79, 211)`.
- `StreamWriter w = new StreamWriter("test.txt")` opens/creates the file and **destroys** the previous content if it already exists; failures raise an exception `[from source] (CSYB p.79)`. `WriteLine` writes one line `[from source] (CSYB p.79)`.
- **`Close()` is mandatory**: it flushes pending text, releases the file for other programs and returns the system resource `[from source] (CSYB p.80)`.
- Namespace `System.IO` (`using System.IO;`) `[from source] (CSYB p.80-81)`.
- `StreamReader`: `ReadLine()` and `EndOfStream` to read until the end `[from source] (CSYB p.81-82)`. Paths: no folder = the program's folder; `@"c:\data\..."` with a verbatim string `[from source] (CSYB p.82-83)` `[HOST]` (the path separator depends on the OS).
- The book shows the pattern **`try { ... } catch { ... } finally { if (textOut != null) textOut.Close(); }`** to guarantee closing `[from source] (CSYB p.156, 158)`.
- Using `TextWriter`/`TextReader` as a parameter allows saving to a file, network, etc. ("streams are wonderful") `[from source] (CSYB p.158-159)`.
- Object persistence: each object saves and loads itself; the type is written with `GetType().Name` and recreated by a *factory* `[from source] (CSYB p.155-164)`.

## 4. Threads, synchronization and `Monitor`

- *Thread* = flow of execution; simple programs have one, which starts at `Main` `[from source] (CSYB p.172)`. A computer supports several threads by **rapid switching** or with several processors `[from source] (CSYB p.172)`.
- "Threads can be dangerous": bugs only appear in certain sequences and are hard to reproduce `[from source] (CSYB p.173, 179-180)`.
- The `Thread` class is in `System.Threading`; the starting point is a `ThreadStart` delegate; `new Thread(ts)` and `t1.Start()` `[from source] (CSYB p.174-175)`.
- Example of a **lost update**: two threads incrementing `overDraftCount = overDraftCount + 1` without protection undercount; the sequence (read, get interrupted, another writes, overwrite) is described step by step `[from source] (CSYB p.177)`.
- The book's solution: **mutual exclusion** with a "token" object (`static object sync = new object();`) and `Monitor.Enter(sync); ... Monitor.Exit(sync);`; waiting threads queue up `[from source] (CSYB p.178)`.
- Others: `Thread.Sleep`, `Join()`, `Abort()`, `Suspend()`/`Resume()`, `ThreadState` `[from source] (CSYB p.178-179)`; `[DATED]` `Abort`/`Suspend`/`Resume` (see §9).
- Risks: not releasing the synchronization object blocks the other threads; "deadly embrace" (A waits for B and B waits for A) `[from source] (CSYB p.178)`. Tips: protect shared variables with `Monitor`; avoid the deadly embrace by separating producers and consumers; plan logging/debugging; threads must be part of the design `[from source] (CSYB p.180)`.
- Processes have isolated memory; `Process.Start("Notepad.exe")` (`System.Diagnostics`) `[from source] (CSYB p.180)`.
- The text warns that the described behavior belongs to Microsoft's .NET, not to the language `[from source] (CSYB p.174)` `[HOST]`.
- C# 13/.NET 9 introduces `System.Threading.Lock`: `lock` recognizes the type and uses `Lock.EnterScope()` instead of `Monitor`; "no other code needs to change" `[from source] (CS13 p.2)` `[VERSION-DEPENDENT]`.

## 5. Program organization

- Several source files; library (`.dll`, no `Main`) with `csc /target:library` and `/reference` `[from source] (CSYB p.184-186, 208)` `[DATED]` (command line of the time).
- Removing the DLL causes `FileNotFoundException`; the author speaks of "DLL hell" and of version control `[from source] (CSYB p.186)`.
- Namespaces avoid name collisions (`namespace CustomerBanking { ... }`), `using` imports, fully qualified name; the author prefers qualified names `[from source] (CSYB p.186-189, 209)`.

## 6. Events and graphical interface (WPF/XAML) `[DATED]`

- The chapter teaches WPF with XAML (Windows Vista/7/8) `[from source] (CSYB p.189-198)`. Useful, independent ideas: the business object separated from the UI `[from source] (CSYB p.172, 195)`; `+=` on `Click` registers a delegate `[from source] (CSYB p.198)`; an event handler runs on a thread created by the system `[from source] (CSYB p.173, 198)`.

## 7. Debugging and quality

- Debug methodically: a failure report with reproducible steps; intermittent faults are the worst `[from source] (CSYB p.200-201)`.
- "Crash" failures: unforeseen state (every selection statement with a `default` handler), infinite loops, infinite recursion (*stack overflow*), uncaught exception; "wrong answer" failures: uninitialized members, typos, logic errors `[from source] (CSYB p.201)`.
- Tips: do not assume; prove it with code; explain the problem to someone (rubber duck); step away; go back to a state without the defect and reintroduce the changes; "bug fixes cause bugs", so run automated tests after the fix `[from source] (CSYB p.201-202)`.
- No useful program is perfect; assess impact and priority `[from source] (CSYB p.202-203)`.
- Use of tests: `[from source] (CSYB p.102-103)`.

## 8. Outside the book and `[DATED]`

The book (2019) uses `Thread`, `Monitor`, `ArrayList`/`Hashtable`, `Close()`. The modern supplements below are **[extrapolation]**, never attributed to the book.

## 9. Labeled supplement `[extrapolation]`

| Topic | Supplement (not in the book) |
| :-- | :-- |
| Resource disposal | CSHist mentions "using declarations" in C# 8 `[from source] (CSHist p.8)` and `Dispose` in the C# 1.2 `foreach` `[from source] (CSHist p.15)`. `[extrapolation]` `using (var w = new StreamWriter(...))`/`using var` calls `Dispose()` at the end and is equivalent to `try/finally`. |
| Rethrowing an exception | The book only shows `throw new` `[from source] (CSYB p.75, 182)`. `[extrapolation]` `throw;` preserves the stack trace; `throw ex;` resets it. |
| Boxing/unboxing | The book only talks about casting and typing `[from source] (CSYB p.150-152)`. `[extrapolation]` Putting a value (`int`) in an `ArrayList` wraps it in an `object` (memory cost); `List<int>` avoids this. |
| Locks | The book uses `Monitor.Enter/Exit` `[from source] (CSYB p.178)`. `[extrapolation]` `lock (object)` is syntactic sugar over `Monitor`; avoid `lock(this)`, `lock(typeof(T))` and strings (externally visible target). |
| async/await, Task, ThreadPool, ConcurrentDictionary | Outside the book; CSHist only lists async/await in C# 5.0 `[from source] (CSHist p.12)`. |
| .NET exceptions | NullReferenceException, IndexOutOfRangeException, InvalidCastException, ArgumentException, DivideByZeroException: names absent from the book. |
| `Thread.Abort`/`Suspend` | Obsolete/removed in modern .NET. |
