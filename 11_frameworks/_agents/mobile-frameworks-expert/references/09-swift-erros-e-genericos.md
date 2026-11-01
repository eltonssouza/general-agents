# 09 - Swift: error handling and generics (SWT p.17-19)

Source SWT (Swift version not stated). Code read by rendering.

## Representing and throwing errors (SWT p.17)
- Errors are represented by **any type that adopts the `Error` protocol** (SWT p.17; code: `enum PrinterError: Error { case outOfPaper, noToner, onFire }`) [from source].
- `throw` throws an error; `throws` marks the function that can throw. If an error is thrown, the function **returns immediately** and the calling code handles the error (SWT p.17; code: `send(job:toPrinter:) throws -> String`) [from source].

## Handling errors (SWT p.17-18)
- **do-catch:** inside `do`, code that can throw is marked with **`try`**; in the `catch`, the error is automatically named `error`, unless you give it another name (SWT p.17) [from source]. Experiment: change the printer name to "Never Has Toner" so the function throws (SWT p.17).
- **Multiple `catch` clauses** handle specific errors; you write a **pattern** after `catch`, as after `case` in a switch (SWT p.17; code: `catch PrinterError.onFire`, `catch let printerError as PrinterError`, and a generic `catch`) [from source]. Experiment: throw an error inside the `do` to land in the 1st, 2nd and 3rd `catch` (SWT p.18).
- **`try?`** converts the result to an optional: if the function throws, the specific error is **discarded** and the result is `nil`; otherwise it is an optional with the returned value (SWT p.18; code) [from source].
- **`defer`** writes a block executed **after all the rest of the function's code, right before it returns**, **regardless** of whether the function throws an error; it lets you write setup and cleanup side by side (SWT p.18; code: `fridgeIsOpen` goes back to `false`) [from source].

## Generics (SWT p.18-19)
- A name inside **angle brackets** creates a generic function or type (SWT p.18; code: `func makeArray<Item>(repeating item: Item, numberOfTimes: Int) -> [Item]`) [from source].
- You can create generic forms of functions, methods, **classes, enumerations and structures** (SWT p.19; code: reimplementation of `Optional` as `enum OptionalValue<Wrapped>` with `.none` and `.some`) [from source].
- **`where`** right before the body specifies a list of requirements: require the type to implement a protocol, require two types to be the same, or require a class to have a given superclass (SWT p.19; code: `anyCommonElements<T: Sequence, U: Sequence>` with `where T.Element: Equatable, T.Element == U.Element`) [from source].
- `<T: Equatable>` is the same as `<T> ... where T: Equatable` (SWT p.19) [from source]. Experiment: turn `anyCommonElements` into a function that returns the array of common elements.

## Limits (NOT COVERED)
`rethrows`, `Result`, typed `throws`, `try!`, `guard` with errors, `async throws`, `defer` in nested scopes (only one example), generics with `associatedtype`, opaque types (`some`), parameter packs.
