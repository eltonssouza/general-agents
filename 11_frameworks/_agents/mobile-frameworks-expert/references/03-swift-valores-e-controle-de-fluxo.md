# 03 - Swift: values, collections, control flow, optionals and switch (SWT p.1-6)

Source: "A Swift Tour" (SWT), 2026 capture; **Swift version not stated**. Prose read from the text; code read by **rendering** (it is in an image) and marked "code". Paraphrase; code snippets here are minimal and illustrative.

## First program and general syntax (SWT p.1)
- The "Hello, world!" tradition is solved in **one line**; that line is a complete program (SWT p.1, code: `print("Hello, world!")`) [from source].
- No library import is needed to print text or handle strings; code at **global scope** is the entry point, so **no `main()` is needed**; and **semicolons are not required** at the end of each statement (SWT p.1) [from source].
- The tour aims to give enough to start writing Swift; the rest is explained in the book (SWT p.1) [from source].

## let and var, inference and explicit type (SWT p.1-2)
- `let` = constant, `var` = variable. A constant's value **does not need to be known at compile time**, but must be assigned **exactly once** (SWT p.1) [from source].
- The value's type must match that of the constant/variable, but **you do not always need to write the type**: the compiler infers it from the initial value (SWT p.1) [from source].
- Without an initial value or without enough information: write the type after the name, separated by a colon (SWT p.1, code: `let explicitDouble: Double = 70`) [from source].
- Tour experiment: create an explicit `Float` constant with value 4 (SWT p.2) [from source].
- **No implicit conversion** between types: to convert, explicitly create an instance of the desired type (SWT p.2, code: `String(width)`) [from source]. Experiment: remove the conversion and see the error (the text does not transcribe the message).

## Strings (SWT p.2)
- Interpolation: value in parentheses preceded by a backslash: `\( )` (SWT p.2, code) [from source].
- Multiline strings with **three double quotes**; the leading indentation of each line is removed as long as it matches the indentation of the closing quotes (SWT p.2); single double quotes can appear unescaped in the block (code) [from source].

## Arrays and dictionaries (SWT p.2-3)
- Created with brackets `[]`; accessed by index or key inside brackets; a comma after the last element is allowed (SWT p.2) [from source].
- Arrays **grow automatically** when elements are added (SWT p.3, code: `append`) [from source].
- Empty ones: `[]` for an array and `[:]` for a dictionary (SWT p.3). When assigning empty to a **new** variable (or where there is no type information) you must **specify the type** (SWT p.3, code: `[String]`, `[String: Float]`) [from source].

## Control flow (SWT p.3-6)
- Conditionals: `if` and `switch`. Loops: `for-in`, `while`, `repeat-while`. **Parentheses** around the condition/variable are **optional**; **braces** around the body are **required** (SWT p.3) [from source].
- In `if`, the condition must be a **Boolean expression**: code like `if score { ... }` is an error, not an implicit comparison with zero (SWT p.3) [from source].
- `if` and `switch` can be written **after the `=`** of an assignment or after `return`, to choose a value (SWT p.3; code: `let scoreDecoration = if teamScore > 10 { ... } else { ... }`) [from source]. The text does not say in which version this was introduced (do not assert it).
- **while** repeats until the condition changes; **repeat-while** tests at the end, guaranteeing at least one execution (SWT p.5; code: both end at 128) [from source]. Experiment: change `m < 100` to `m < 0` to see the difference (SWT p.6).
- **Ranges:** `..<` omits the upper bound, `...` includes both (SWT p.6; code: `for i in 0..<4` sums 6) [from source].
- `for-in` over a dictionary uses a **pair of names** (key, value); dictionaries are an **unordered** collection, so iteration is in **arbitrary order** (SWT p.5; code: `for (_, numbers) in ...` with `_` to ignore the key) [from source].

## Optionals (SWT p.4)
- Values that may be missing are **optionals**: they contain a value **or `nil`**; `?` after the type marks the optional (SWT p.4; code: `String?`) [from source].
- `if let name = optional { ... }`: if it is `nil`, the condition is false and the block is skipped; otherwise the value is unwrapped and available inside the block (SWT p.4) [from source]. Experiment: set it to `nil` and add `else` (SWT p.4).
- The `??` operator provides a default value if the optional is empty (SWT p.4; code) [from source].
- **Short form:** `if let nickname { ... }` unwraps with the same name (SWT p.4; code; nothing is printed if it is `nil`) [from source].

## switch (SWT p.4-5)
- `switch` supports **any kind of data** and many comparisons; it is not limited to integers and equality (SWT p.4) [from source]. Code: string cases, several values in the same `case` separated by commas, and `case let x where x.hasSuffix("pepper")`; the `let` in the pattern assigns the matched value to a constant (SWT p.4-5) [from source].
- Experiment: remove the `default` and see which error appears (SWT p.5). The text **does not explain** the rule; that the error stems from exhaustiveness is [inference]/[extrapolation].
- After running the matching `case`, the program **exits the switch**: it does not continue to the next `case`, **with no explicit `break`** (SWT p.5) [from source].

## Limits
The tour does not cover `guard`, `fallthrough`, `inout`, custom operators, `Set`, `Character`, forced unwrapping `!`, `if case`, partial ranges etc. (NOT COVERED). Check with `python -I scripts/mob_lookup.py --gaps`.
