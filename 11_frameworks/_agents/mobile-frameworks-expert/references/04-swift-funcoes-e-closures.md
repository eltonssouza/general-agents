# 04 - Swift: functions and closures (SWT p.6-8)

Source SWT (Swift version not stated; 2026 capture). Code read by rendering.

## Functions (SWT p.6)
- `func` declares a function; you call it with its name and an argument list in parentheses; `->` separates the parameters from the return type (SWT p.6; code: `greet(person:day:)` returns String) [from source]. Experiment: remove the `day` parameter and add another (SWT p.6).
- **Argument labels:** by default the parameter name is the label; you can write a custom label before the name, or `_` for **no label** (SWT p.6; code: `greet(_ person: String, on day: String)` called as `greet("John", on: "Wednesday")`) [from source].
- **Tuples** form compound values, for example to return several values; elements can be referred to **by name or by number** (SWT p.6-7; code: `calculateStatistics` returns `(min:, max:, sum:)`; `statistics.sum` and `statistics.2`) [from source]. The function body is cut off between p.6 and p.7 in the capture; the tour uses a loop that updates min/max/sum.

## Nested functions and functions as values (SWT p.7)
- Functions can be **nested** and have access to variables declared in the outer function; useful to organize long or complex functions (SWT p.7; code: `returnFifteen` with an inner `add()` that changes `y`) [from source].
- Functions are **first-class**: a function can **return another function** (SWT p.7; code: `makeIncrementer() -> ((Int) -> Int)`) and **take another function as an argument** (SWT p.7-8; code: `hasAnyMatches(list:condition:)` with `lessThanTen`) [from source].

## Closures (SWT p.8)
- Functions are a special case of **closures**: blocks of code that can be called later; they have access to variables and functions of the scope where they were created, **even when executing in a different scope** (SWT p.8) [from source].
- Unnamed closure: code between braces `{}`; `in` separates the arguments/return type from the body (SWT p.8; code: `numbers.map({ (number: Int) -> Int in ... })`) [from source]. Experiment: rewrite it to return zero for odd numbers.
- **Shorter forms** (SWT p.8): when the closure's type is already known (e.g., a delegate callback) you can omit the parameter types, the return, or both; **single-statement** closures implicitly return its value (code: `numbers.map({ number in 3 * number })`) [from source].
- Parameters can be referred to **by number** (`$0`, `$1`) in very short closures; a closure passed as the **last argument** can come right after the parentheses; if it is the **only argument**, the parentheses can be omitted (SWT p.8; code: `numbers.sorted { $0 > $1 }`) [from source].

## Limits (NOT COVERED in the tour)
`inout`, default parameter values, variadic parameters, `@escaping`, capture/reference cycles, `guard`, throwing functions (see 09), `reduce`/`filter` (only `map` and `sorted` appear in the code).
