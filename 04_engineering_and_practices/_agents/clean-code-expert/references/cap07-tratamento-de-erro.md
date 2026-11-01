# Cap. 7 — Tratamento de Erro (Error Handling; by Michael Feathers)

Source: CL ch. 7, PDF p.107-116 (opening on p.107; conclusion and bibliography on p.116).

## Premise
- The chapter is signed by Michael Feathers (CL p.107).
- Error handling is necessary, but it dominates a lot of code to the point of hiding what the code does. If it obscures the logic, it is wrong (CL p.107).
- Goal: clean **and** robust code. The two do not conflict if error handling is a separate concern, visible independently of the main logic (CL p.116).

## Use exceptions rather than return codes
- Flags and error codes clutter the caller, who must check for the error right after the call, and it is easy to forget. It is better to throw an exception (CL p.108).
- With exceptions, the calling code is cleaner and the logic is not obscured by error handling (CL p.108).
- The gain is not aesthetic: two intertwined concerns, the shutdown algorithm and error handling, are separated and can be studied independently (CL p.109).

## Write your try-catch-finally statement first
- Exceptions define a scope. What runs in the `try` can be aborted at any point and resume in the `catch` (CL p.109).
- `try` blocks are like transactions. The `catch` must leave the program in a consistent state, no matter what happens in the `try` (CL p.109).
- Good practice: when writing code that may throw exceptions, start with `try-catch-finally`. This defines what the user of the code should expect (CL p.109).
- TDD flow of the example: (1) a test that expects `StorageException` for an invalid file; (2) a stub that returns an empty list, and the test fails; (3) an implementation with `try`, which tries to open the file and converts the exception, and the test passes; (4) a refactoring that narrows the `catch` from `Exception` to `FileNotFoundException`; (5) TDD for the rest of the logic inside the scope (CL p.109-110).
- Write tests that force exceptions and then add behavior to the handler. This leads you to create the transactional scope of the `try` first (CL p.110).

## Use unchecked exceptions
- Section opened with "A discussão acabou" (The debate is over) (CL p.110).
- Checked exceptions seemed like a great idea in early Java and had advantages, but they are not necessary for robust software. C#, C++, Python and Ruby do not check them and still allow robust software (CL p.110).
- The price of checked exceptions is a **violation of the Open/Closed Principle** (OCP), with a cross-reference to [Martin] (CL p.110).
- If the `catch` is three levels above, the exception must be declared in the signature of every method on the path. A change at a low level forces signature changes at many high levels, with recompilation and redeployment of modules that did not change themselves (CL p.111).
- Result: a cascade of changes and **broken encapsulation**, because all the functions on the path need to know details of the low-level exception (CL p.111).
- Exception to the rule: checked exceptions can be useful in a critical library, where you must catch them. In general application development, the dependency costs outweigh the advantages (CL p.111).

## Provide context with exceptions
- Each exception must carry enough context to determine the source and location of the error. The stack trace does not say what the purpose of the failed operation was (CL p.111).
- Create informative messages: mention the operation that failed and the type of failure. If logging is in place, pass enough information to record the error in the `catch` (CL p.111).

## Define exception classes in terms of a caller's needs
- Errors can be classified by source or by type, but the main concern should be **how they will be caught** (CL p.111).
- Bad example: a call to `ACMEPort.open()` with three nearly identical `catch` blocks (`DeviceResponseException`, `ATM1212UnlockedException`, `GMXError`), all with log and report. There is duplication (CL p.111-112).
- Solution: a `LocalPort` wrapper that catches and translates the three exceptions into a common type, `PortDeviceFailure` (CL p.112).
- Wrapping third-party APIs is called "a melhor prática que existe" (the best practice there is): it minimizes the dependency on them, lets you switch libraries, makes it easy to mock the calls in tests and frees you from the vendor's design choices (CL p.112-113).
- In general, a single exception class is enough for an area of the code, and the data sent with the exception distinguishes the errors. Use different classes only when you want to catch one and let the other pass (CL p.113).

## Define the normal flow (Special Case)
- Following the previous sections, you wrap APIs, throw your own exceptions and put a handler above the code to deal with any aborted computation. Most of the time this is great, but there are situations in which you do not want to abort (CL p.113).
- Example: `MealExpensesNotFound` used to fall back to the per diem muddles the expenses total logic (CL p.113).
- Solution: the DAO always returns a `MealExpenses`. With no expenses, it returns `PerDiemMealExpenses`, whose total is the per diem. This is Fowler's **Special Case** pattern: a class or object that handles the special case and encapsulates it, and the client does not need to deal with the different behavior (CL p.113-114).

## Don't return null
- Returning `null` is the first item on the list of things we do that **cause** errors. It creates work and throws problems onto callers. All it takes is one missed check to lose control of the application (CL p.114).
- In the `registerItem` example, the problem is not a missing `null` check (there is no check for `persistentStore`), but having too many checks (CL p.114).
- Instead of returning `null`, throw an exception or return a SPECIAL CASE object. If a third-party API returns `null`, wrap it in a method that throws an exception or returns a special case (CL p.114).
- Collections: return an empty list, for example `Collections.emptyList()`, which is immutable and predefined, instead of `null`. This eliminates the `if` and reduces `NullPointerException` (CL p.114-115).

## Don't pass null
- Returning `null` is bad, passing it is worse. Avoid it, unless the API expects `null` (CL p.115).
- Example `MetricsCalculator.xProjection(p1, p2)`: passing `null` causes `NullPointerException`. Throwing `InvalidArgumentException` requires a handler, and what would good handling be? `assert` documents well, but does not solve it, and the error remains at run time (CL p.115-116).
- In most languages there is no good way to deal with a `null` passed by accident, so the logical approach is to **forbid passing `null` by default**. That way, a `null` in the parameter list is a sign of a problem (CL p.116).

## Examples from the book
- Listing 7-1: `DeviceController.sendShutDown` with an invalid handle and nested status checks (CL p.108).
- Listing 7-2: the same logic with `tryToShutDown` and `DeviceShutDownError` (CL p.108-109).
- `SectionStore.retrieveSection`: TDD of the `try` scope with `StorageException` (CL p.109-110).
- `ACMEPort` versus `LocalPort` (wrapper that translates exceptions) (CL p.111-112).
- `MealExpenses` / `PerDiemMealExpenses` (Special Case) (CL p.113-114).
- `registerItem` with a cascade of `null` checks; `getEmployees` with an empty list (CL p.114-115).
- `MetricsCalculator.xProjection` with `null`, exception and `assert` (CL p.115-116).

## What the chapter does NOT say / common confusions
- It does not condemn checked exceptions in every case: it admits their usefulness in critical libraries (CL p.111).
- The principle violated by checked exceptions is **Open/Closed**, not Single Responsibility (CL p.110).
- It does not talk about "Null Object". The name used is Special Case, from Fowler (CL p.114). The Null Object pattern is a close relative [extrapolation].
- It does not mention `Optional`, `Result`/`Either` types or nullability annotations. For "don't return null", the book's alternatives are exception, Special Case and empty collection (CL p.114-115).
- It does not say to use `assert` against `null`: it says `assert` does not solve the problem (CL p.116).
- It does not say "one exception class per error". It says the opposite: in general one class per area is enough (CL p.113).
- The rule that error handling is "one thing" and should live in its own function is in Ch. 3 (CL p.54), not here.

## [DATED]
- The exception test uses `@Test(expected = StorageException.class)`, from JUnit 4 (CL p.109). JUnit 5 uses `assertThrows` [DATED][extrapolation].
- The discussion of checked exceptions is centered on Java. Later languages, such as Kotlin, abolished checked exceptions. The book's list of languages (C#, C++, Python, Ruby) is from 2008 (CL p.110) [DATED][extrapolation].
- `Collections.emptyList()` is still valid. Today there is also `List.of()` (Java 9+) [extrapolation].
