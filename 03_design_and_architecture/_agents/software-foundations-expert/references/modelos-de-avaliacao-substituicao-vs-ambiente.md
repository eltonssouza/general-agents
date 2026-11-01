# Evaluation models: substitution vs environment

Main source: SICP, chs. 1, 3 and 4 (page convention: PDF; see `INDEX.md`). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. The substitution model (SICP 1.1.5)
- `[from source]` (SICP p.29): to apply a compound procedure to arguments, evaluate the body with each formal parameter replaced by the corresponding argument. The book illustrates with `(f 5)`, where `f` calls `sum-of-squares`, which calls `square`; the reduction ends at `136` (SICP p.28-29).
- `[from source]` (SICP p.30): the purpose of substitution is to help us think about procedure application, not to describe how the interpreter really works; in practice the "substitution" is done with a local environment for the formal parameters. The model is only the first in a sequence of increasingly elaborate models and "breaks down" when mutable data enters (ch. 3).
- `[from source]` (SICP p.30-31): **applicative order** = evaluate operator and operands and only then apply; **normal order** = expand fully (substitute operand expressions for the parameters) and only then reduce. In normal order, `(+ 5 1)` and `(* 5 2)` are each evaluated twice (SICP p.31).
- `[from source]` (SICP p.31): for procedures modelable by substitution that produce legitimate values, the two orders give the same value; Lisp uses applicative order partly for efficiency (avoiding repeated evaluations) and, more importantly, because normal order becomes much more complicated outside the domain of substitution.
- `[from source]` (SICP p.367-368): with lazy evaluation, `(try 0 (/ 1 0))` returns `1`, whereas in Scheme (applicative order) it gives an error. A procedure is *strict* in an argument if the argument is evaluated before entering the body; *non-strict* otherwise (SICP p.368).
- Example trace (from the book, p.29-30): `(f 5)` → `(sum-of-squares (+ 5 1) (* 5 2))` → `(+ (square 6) (square 10))` → `(+ 36 100)` → `136` (applicative order); in normal order the expansion `(+ (* (+ 5 1) (+ 5 1)) (* (* 5 2) (* 5 2)))` precedes the reductions (SICP p.30).

## 2. Why assignment (`set!`) breaks substitution (SICP 3.1.3)
- `[from source]` (SICP p.217): as long as there is no assignment, two evaluations of the same procedure with the same arguments give the same result and procedures behave like mathematical functions; programming this way (chs. 1-2) is called functional programming. With `set!` the language "can no longer be interpreted" by the substitution model.
- `[from source]` (SICP p.217-219): `make-simplified-withdraw` accumulates effect between calls (`(W 20)` gives 5, `(W 10)` gives -5), unlike `make-decrementer`, which can be explained by substitution. When trying to substitute in `make-simplified-withdraw`, the first occurrence of `balance` (before the `set!`) and the second (after) would have to be distinguished, and substitution cannot do that.
- `[from source]` (SICP p.219): the root of the problem is that substitution treats symbols as names of values; with `set!` a variable comes to designate a "place" where a value can be stored and changed. Footnote 9 (SICP p.223) observes that substituting the name in `(set! <name> ...)` would give `(set! 25 ...)`, which is meaningless.
- `[from source]` (SICP p.219-220): objects created by `make-decrementer` (D1, D2) are interchangeable; those from `make-simplified-withdraw` (W1, W2) are not, since their calls have distinct effects.
- `[from source]` (SICP p.220): a language in which "equals can be substituted for equals" is **referentially transparent**; referential transparency is violated when `set!` is included, which makes reasoning about programs much harder.
- `[from source]` (SICP p.221): the imperative style (heavy use of assignment) introduces pitfalls, for example the order of assignments in an iterative `factorial` with `set!`.
- `[from source]` (SICP p.279): by admitting assignment we are forced to admit *time* in the model; expressions no longer always have the same value.
- `[inference]` (from SICP p.217-221): `(f x) + (f x)` can differ from `2 * (f x)` when `f` changes internal state; the book shows the phenomenon with `W`, not this literal expression.

## 3. The environment model (SICP 3.2)
- `[from source]` (SICP p.224): an **environment** is a sequence of **frames**; each frame is a (possibly empty) table of bindings, and has a pointer to the enclosing environment (except the global one). The value of a variable is that of the first frame that binds it; if none binds it, the variable is *unbound*. An inner binding can hide (*shadow*) another in an outer frame (SICP p.224-225).
- `[from source]` (SICP p.225): expressions only have meaning relative to some environment; there is a global environment with a single frame (which binds, for example, `+` to the primitive addition procedure).
- `[from source]` (SICP p.225-226): a procedure is always a pair made of code and a pointer to an environment; it is only created by evaluating a `lambda` expression, and its environment is the one in which the `lambda` was evaluated. A procedure `define` is syntactic sugar for `lambda`.
- `[from source]` (SICP p.226-227): applying a procedure = creating a frame that binds the parameters to the argument values, whose enclosing environment is the environment stored in the procedure, and evaluating the body in this new environment. `define` creates a binding in the current frame; `set!` locates the binding in the first frame that contains it and changes it (error if *unbound*).
- `[from source]` (SICP p.227): the rules are more complex than substitution, but they correctly describe how the interpreter evaluates expressions; they serve as the model for the interpreter of ch. 4 (SICP p.335).
- `[from source]` (SICP p.230-234): in `(define W1 (make-withdraw 100))` the call creates the environment E1 with `balance`; the returned procedure has E1 as its environment. When calling `(W1 50)`, the new frame (with `amount`) has E1 as its enclosing environment (not the global one) and the `set!` changes `balance` in E1 (SICP p.232-233). E1 is the "place" that holds W1's local state; `W2` gets another environment E2 and, therefore, independent state (SICP p.233-234).
- `[from source]` (SICP p.141, note 6): SICP does **not** use the word "closure" in the sense of an implementation technique for procedures with free variables (the sense used by the Lisp community); in the book, "closure" is the algebraic property of data (see `abstracao-procedural-e-dados-compostos.md`). What SICP calls a "code + environment pair" corresponds to what CI calls a closure (CI p.166: the function object captures the environment in which it was declared).

## 4. Lexical scope vs dynamic scope
- `[from source]` (SICP p.42): in procedures with internal definitions, the free variable `x` gets its value from the argument with which the enclosing procedure was called; this discipline is called **lexical scoping**, associated with the block structure of Algol 60.
- `[from source]` (CI p.131): with dynamic scope one does not know what a name refers to until the code runs; Lox has no dynamically scoped variables, but methods and fields of objects are resolved dynamically.
- `[from source]` (CI p.164): Lox's lexical-scope rule: a used variable refers to the preceding declaration with the same name in the innermost scope that encloses the expression; this is part of the static semantics (CI p.163).
- `[extrapolation]`: the list of languages with lexical scope (Python, JavaScript, Rust) and dynamic scope (Emacs Lisp, Bash) is **not** in any of the three books. Version 1 of the package attributed "dynamic scope" to `TAUP p.364`; the extracted text of TAUP does not contain that expression.

## 5. Diagnostic procedure `[inference]`
1. Is there assignment/mutation (`set!`, mutable fields)? If not, substitution suffices (SICP p.217, 227).
2. If so, trace frames: global frame; for each `lambda`, a procedure object (code + creation environment); for each call, a new frame whose enclosing environment is the procedure's environment, not the caller's (SICP p.226-227, p.232).
3. With lazy evaluation, remember that mutability and delayed evaluation "do not mix well" (SICP p.325).

## 6. What the book does not say
- It does not define "dynamic scope" as a SICP concept; it does not claim that "most modern languages" use applicative order (it says Lisp does, p.31).
- It does not present (set! 100 ...) as the only reason for the failure; the reason is the distinction between name and place (p.219).
