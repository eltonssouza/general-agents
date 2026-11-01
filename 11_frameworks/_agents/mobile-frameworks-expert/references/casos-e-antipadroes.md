# Cases and antipatterns supported by the texts

Only pitfalls that the tour/page itself points to (or direct deductions, labeled) appear here. Each row corresponds to a linter rule when one exists.

## Swift (SWT)
| # | Antipattern / pitfall | Why (source) | Fix according to the text | Rule |
|---|---|---|---|---|
| 1 | Reassigning a `let` constant | a constant receives a value exactly once (SWT p.1) | use `var` | SWF-01 |
| 2 | `if score { ... }` with a number/identifier | the condition must be Boolean; there is no implicit comparison with zero (SWT p.3) | `if score != 0 {` or a Boolean condition | SWF-02 |
| 3 | Body of `if`/`for`/`while` without braces | braces are required (SWT p.3) | add `{ }` | SWF-03 |
| 4 | `switch` without `default` | the tour proposes removing the `default` to see the error (SWT p.5); the exhaustiveness rule is [inference] | include `default` (or cover all cases of an enum) | SWF-04 |
| 5 | `break` at the end of each `case` | execution does not fall into the next case (SWT p.5) | omit it | SWF-05 |
| 6 | `var lista = []` | an empty array/dictionary without a type requires a type (SWT p.3) | `var lista: [String] = []` | SWF-06 |
| 7 | `"texto" + numero` or `Int + Double` | no implicit conversion (SWT p.2) | `String(numero)`, `\(numero)` or `Double(inteiro)` | SWF-07 |
| 8 | Overriding without `override` / `override` without a method | compiler error in both cases (SWT p.9) | add/remove `override` | SWF-08/09 |
| 9 | Class with a property without a value and without `init` | every property needs a value (SWT p.9) | value at declaration or `init` | SWF-10 |
| 10 | Struct method that changes the struct itself without `mutating` | `mutating` marks a method that modifies the structure (SWT p.16) | add `mutating` | SWF-11 |
| 11 | Calling a `throws` function without `try` | code that can throw is marked with `try` (SWT p.17) | `try`, `try?` or do-catch | SWF-12 |
| 12 | Calling an `async` function without `await` | the call is marked with `await` (SWT p.14) | `await` (or `async let`) | SWF-13 |
| 13 | Type says it follows a protocol but does not implement a requirement | tour experiment about adding a requirement (SWT p.16); the error is [inference] | implement the requirement | SWF-14 |
| 14 | Accessing an actor without `await` | access to an actor's method/property takes `await` (SWT p.15) | `await` | SWF-17 |
| 15 | Accessing an optional's member directly | the tour uses `if let`, `??`, `?.` (SWT p.4, 11); [inference] | unwrap | SWF-19 |
| 16 | Assuming dictionary iteration order | iteration in arbitrary order (SWT p.5) | do not depend on the order | (no rule) |
| 17 | Expecting the protocol value to expose the class's extra members | a "boxed" value only exposes the protocol (SWT p.16-17) | use the concrete type | (no rule) |
| 18 | Expecting a struct to share state like a class | a struct is copied; a class is by reference (SWT p.13) | choose according to the need | (no rule) |
| 19 | Using `!`, `try!`, `++`, C-style for | **outside the tour** [extrapolation] | use the tour's constructs | SWF-X1..X3 |
| 20 | Stating the Swift version in which `any`/`if` expression/actors appeared | the tour gives no version; [extrapolation] | state "version not stated" | - |

## React Native / Flutter (RN, FLT)
| # | Pitfall | Why | Fix |
|---|---|---|---|
| 21 | Giving installation steps/commands as if they were in the source | RN says getting started is in another section (RN p.1); FLT only links "Install Flutter" (FLT p.1) | NOT COVERED |
| 22 | Stating that Flutter uses Dart "because the page says so" | only "Dart and Flutter" appears in the videos (FLT p.2) | say the text does not assert it; [extrapolation] if requested |
| 23 | Explaining Flutter's constraints model beyond the summary sentence | the page only carries the sentence (FLT p.2) | cite the sentence and say NOT COVERED for the rest |
| 24 | Saying "RN 0.87 changed X" | the collection has only one version | NOT COVERED (change map does not exist) |
| 25 | Recommending RN, Flutter or Swift | the sources neither compare nor recommend | NOT COVERED; only criteria (`mob_compare.py`) |
| 26 | Treating Swift as a "mobile framework" equivalent to RN/Flutter | SWT is a language tour with no UI or platforms | explain the difference in nature |
