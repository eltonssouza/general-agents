# Evaluators: metacircular, lazy, and nondeterministic (`amb`)

Source: SICP ch. 4 and 5.4 (PDF pages; see `INDEX.md`).

## 1. The metacircular evaluator (SICP 4.1)
- `[from source]` (SICP p.335): an evaluator written in the same language it evaluates is called *metacircular*; it is essentially a Scheme formulation of the environment model of ch. 3, with two parts: evaluating a combination (subexpressions, then apply) and applying a compound procedure (evaluate the body in a new environment that extends the procedure's). The book describes the `eval`/`apply` cycle (figure 4.1, SICP p.336).
- `[from source]` (SICP p.336-337): `eval` takes an expression and an environment and does case analysis on the syntactic type: self-evaluating, variables (lookup in the environment), `quote`, assignment/definition (call `eval` recursively for the value), `if`, `lambda` (packages parameters, body and environment), `begin`, `cond` (transformed into nested `if`s) and applications (evaluates operator and operands and passes to `apply`).
- `[from source]` (SICP p.337-338): `apply` distinguishes primitive procedures (`apply-primitive-procedure`) from compound ones (evaluates the body in an environment extended with a frame binding parameters and arguments).
- `[from source]` (SICP p.335): the evaluator uses data abstraction (predicates and selectors such as `assignment?`, `assignment-variable`) to be independent of the representation of the syntax; environment and procedure operations are in 4.1.3 (SICP p.346).
- `[from source]` (SICP p.352-353): an evaluator can be seen as a machine that takes as input the description of another machine; the book says the evaluator is a **universal machine**, since it imitates other machines described as Lisp programs (SICP p.353). Program-as-data is discussed in 4.1.5 (SICP p.352-354) and the halting problem at SICP p.354 and p.365.
- `[extrapolation]`: **"homoiconicity"** does not appear in SICP (the term is from later literature); v1 attributed it to SICP p.334. Based on the book, one can say the evaluator makes "data as programs" (SICP p.353).

## 2. Separating syntactic analysis from execution (SICP 4.1.7)
- `[from source]` (SICP p.359): the simple evaluator is inefficient because syntactic analysis and execution are interleaved; if a program runs many times, its syntax is analyzed many times (example: `factorial`).
- `[from source]` (SICP p.360): `eval` is split into `analyze` (the expression only; returns an *execution procedure*) and the execution, which takes the environment; `eval` becomes `((analyze exp) env)`; thus the analysis is done once and the execution can occur many times. The book says this makes the evaluator "significantly more efficient".
- `[extrapolation]`: "several orders of magnitude" (v1) is **not** in the book; use "significantly more efficient" (SICP p.360).

## 3. Lazy evaluation (SICP 4.2)
- `[from source]` (SICP p.367-368): in normal-order languages the evaluation of arguments is delayed until the value is needed, which is called *lazy evaluation*; in Scheme, `(try 0 (/ 1 0))` gives an error, with lazy evaluation it returns 1. A procedure can be strict or non-strict in an argument (SICP p.368); `cons` is an example of a constructor that can be non-strict, which allows implementing streams as lists (SICP p.368).
- `[from source]` (SICP p.369): on application, the evaluator decides which arguments to evaluate and which to delay; the delayed ones become **thunks**, which contain the argument expression and the environment of the application; *forcing* is evaluating the thunk's expression. A thunk is forced when it is passed to a primitive that uses its value, when it is the value of the predicate of a conditional, or when it is the operator to be applied. The book's interpreter **memoizes** thunks (there are "subtle considerations", SICP p.369).
- `[from source]` (SICP p.369-372): `actual-value` = `(force-it (eval exp env))`; `force-it` evaluates the expression in the thunk's environment (p.371). In the memoized version, the forced thunk becomes an `evaluated-thunk`: it stores the value and forgets the unneeded environment (`(set-cdr! (cdr obj) '())`, SICP p.372).
- `[from source]` (SICP p.375-379): 4.2.3 presents streams as lazy lists.
- `[from source]` (SICP p.329-330): 3.5.4 shows *call-by-name* (thunks without memoization) vs *call-by-need* (with memoization); the book warns that mutability and delayed evaluation "do not mix well" (SICP p.325).
- `[inference]`: the term "Normal Order with Call by Need" from v1 conflates two ideas; the book uses "normal order" for the evaluation order and "call-by-need" for the memoized variant (SICP p.329-330).

## 4. Nondeterministic computing and `amb` (SICP 4.3)
- `[from source]` (SICP p.379): nondeterministic computing is a paradigm in which an automatic search is built into the evaluator; it is useful in "generate and test" applications (like streams); the key idea is that expressions can have more than one possible value and the evaluator chooses one and keeps the choice, trying others if a requirement fails later (SICP p.379-380).
- `[from source]` (SICP p.380): `(amb e1 ... en)` ambiguously returns the value of one of the `ei`; `(amb)` with no alternatives *fails* (aborts the computation with no value). `(require p)` is `(if (not p) (amb))`. The book calls `amb` a choice point and says time "branches" (SICP p.381).
- `[from source]` (SICP p.381): `an-element-of` and `an-integer-starting-from` are examples; they differ from streams because `amb` returns *one* integer, not the object representing the sequence.
- `[from source]` (SICP p.381): the `amb` evaluator does systematic search; on finding a dead end, it goes back to an earlier choice point (*backtracking*, SICP p.380, p.389).
- `[from source]` (SICP p.383-389): examples: "multiple-dwelling" floors puzzle (Baker, Cooper, Fletcher, Miller, Smith, SICP p.383), the liars puzzle (p.384), eight queens as an exercise (ex. 4.44, SICP p.385) and natural-language parsing (SICP p.385-389).
- `[from source]` (SICP p.389-391): in the `amb` evaluator, execution procedures take three arguments: environment, **success continuation** (a two-argument procedure: the value obtained and a failure continuation to use if this value leads to a new dead end) and **failure continuation** (no arguments, tries another branch). `ambeval` is `((analyze exp) env succeed fail)` (SICP p.391). Failures propagate from the most recent choice point to earlier ones; side effects (assignments) are undone on backtracking by a failure continuation that restores the old value (SICP p.390, p.394).
- `[from source]` (SICP p.397-398): `permanent-set!` and `if-fail` allow assignments that are not undone and failure handling.
- `[extrapolation]`: "Einstein problem" (v1) does not appear in SICP; the book's examples are those at p.383-389.

## 5. Tail recursion in the explicit-control evaluator (SICP 5.4)
- `[from source]` (SICP p.502): an evaluator able to run `sqrt-iter` without growing storage is *tail-recursive*; the metacircular evaluator of ch. 4 does not specify whether it is, since it inherits the mechanism of the underlying Scheme; in the explicit-control evaluator the property is obtained in `ev-sequence` by restoring `continue` before evaluating the last expression (SICP p.501-503). Without it, iterative processes such as `sqrt-iter` would require space proportional to the number of iterations (SICP p.503).

## 6. What the book does not say
- It does not use the term "homoiconicity", nor "orders of magnitude" for `analyze`, nor "Einstein problem".
- It does not claim that memoized thunks "free memory for the collector" as a motivation; it only shows that the environment is forgotten (`'()`, p.372).
