# Glossary (only terms that appear in the sources)

Convention: `RN p.N`, `FLT p.N`, `SWT p.N` = PDF page. Definitions in our own words; terms in English as they appear in the sources. What the source does not define is stated.

## React Native (RN)
| Term | Meaning according to the text |
|---|---|
| Snack Player | Tool created by Expo to embed and run React Native projects in the browser and see how they render on platforms such as Android and iOS (RN p.2). |
| Native Components | Presented as the "foundation" of React Native and as the next step (RN p.3); **the text does not define it**. |
| Developer Notes | Blocks of platform-specific explanation (Android, iOS, Web) (RN p.3). |
| Getting started | Starting instructions that "moved to their own section" (RN p.1); they are not on this page. |

## Flutter (FLT)
| Term | Meaning according to the text |
|---|---|
| Widget | In Flutter "everything is a widget" (FLT p.1); the widget catalog is a navigation card (FLT p.1). No formal definition. |
| Stateful widget | Topic of the "Adding interactivity" link: learn to add it to the app (FLT p.2). No definition. |
| Constraints | The summary sentence: constraints go down, sizes go up, parents set positions (FLT p.2). |
| Learning pathway | Recommended path after setting up the environment (FLT p.1). |
| Single codebase | Promise of building multiplatform apps from a single codebase (FLT p.1). |

## Swift (SWT)
| Term | Meaning according to the text |
|---|---|
| Global scope as entry point | Code at global scope is the entry point: there is no `main()` (SWT p.1). |
| `let` / `var` | Constant (assigned exactly once) / variable (SWT p.1). |
| Type inference | The compiler deduces the type from the initial value (SWT p.1). |
| Interpolation | `\( )` inside a string (SWT p.2). |
| Optional | Value that contains a value or `nil`; marked with `?` after the type (SWT p.4). |
| `if let` | Unwraps an optional in a block; skipped if `nil` (SWT p.4). |
| `??` | Default value for an empty optional (SWT p.4). |
| Optional chaining (`?.`) | If the value before `?` is `nil`, the whole expression is `nil` (SWT p.11). |
| Range `..<` / `...` | Excludes / includes the upper bound (SWT p.6). |
| Argument label | By default, the parameter name; customizable or `_` for none (SWT p.6). |
| Tuple | Compound value; elements by name or number (SWT p.6-7). |
| Closure | Block of code callable later, with access to the creation scope; functions are a special case (SWT p.8). |
| `override` | Marks a method that overrides the superclass; absence or excess is a compiler error (SWT p.9). |
| `init` / `deinit` | Initializer / cleanup before deallocation (SWT p.9). |
| `willSet` / `didSet` | Code before/after assigning a new value, outside initializers (SWT p.11). |
| Raw value | Fixed value of an enum case, set at declaration (SWT p.12-13). |
| Associated value | Value of a case set when the instance is created (SWT p.13). |
| `struct` | Type that is copied when passed around; classes are by reference (SWT p.13). |
| `async` / `await` | Marks an asynchronous function / marks the call (SWT p.14). |
| `async let` | Calls an asynchronous function in parallel (SWT p.14). |
| `Task` | Calls an asynchronous function from synchronous code (SWT p.14). |
| Task group | Structure for concurrent code (SWT p.14-15). |
| Actor | Like a class, but safe for simultaneous asynchronous interaction (SWT p.15). |
| Protocol | Declaration of requirements adoptable by classes, enums and structs (SWT p.15). |
| `mutating` | Marks a struct method that modifies it (SWT p.16). |
| Extension | Adds methods, computed properties and conformance to an existing type (SWT p.16). |
| Boxed protocol type | Value treated only as the protocol; extra members are inaccessible (SWT p.16-17). |
| `Error` / `throws` / `try` | Error protocol / function that can throw / mark on a call that can throw (SWT p.17). |
| `try?` | Converts to an optional and discards the error (SWT p.18). |
| `defer` | Block executed right before the function returns, even with an error (SWT p.18). |
| Generic / `where` | `<Name>`; list of requirements before the body (SWT p.18-19). |
