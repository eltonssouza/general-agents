# Procedural abstraction and compound data

Source: SICP chs. 1-2 (PDF pages; see `INDEX.md`).

## 1. Higher-order and first-class procedures
- `[from source]` (SICP p.67): procedures are abstractions that describe compound operations independently of the particular numbers; but if parameters can only be numbers, the ability to abstract is limited, which motivates procedures that take procedures.
- `[from source]` (SICP p.69): the generic `sum` takes `term`, bounds `a` and `b`, and `next`; with it the book defines `sum-cubes`, `sum-integers` and `pi-sum` (approximation of π). The summation pattern is captured once.
- `[from source]` (SICP p.83-84): the book shows that the square root can be seen as a fixed point of a transformation (`fixed-point-of-transform`, `average-damp`, `newton-transform`); the importance of higher-order procedures is that they let abstractions be represented as explicit elements of the language (SICP p.84).
- `[from source]` (SICP p.84): elements with fewer restrictions have *first-class status*, with "rights and privileges": they can be named by variables, passed as arguments, returned as results, and included in data structures. The book says Lisp grants this full status to procedures and that this brings implementation challenges (SICP p.84).
- `[from source]` (SICP p.82): `deriv` takes a procedure `g` and returns another procedure (approximate derivative, with `dx` = 0.00001), like `average-damp`; it is the book's example of "procedure as returned value". Newton's method uses `newton-transform` (SICP p.82-83).

## 2. Data abstraction: constructors and selectors
- `[from source]` (SICP p.91): data abstraction is the methodology that isolates how a compound object is used from the details of how it is constructed; the interface between the parts is a set of **selectors** and **constructors**; the example is rational-number arithmetic (`make-rat`, `numer`, `denom`).
- `[from source]` (SICP p.94): changing only `make-rat` (for example, reducing the fraction with `gcd`) changes the behavior without touching `add-rat`, `mul-rat`, etc.
- `[from source]` (SICP p.94-95): the central idea is to identify, for each data type, a basic set of operations in terms of which all manipulation is expressed. The **abstraction barriers** (figure 2.1) separate "levels" of the system: programs above use `add-rat` etc.; these use `make-rat`/`numer`/`denom`; these use pairs (`cons`/`car`/`cdr`).
- `[from source]` (SICP p.95-96): stated advantage: programs become easier to maintain and modify, since the dependence on the representation is confined to a few modules; the book compares computing the `gcd` at construction vs. at selection, without changing `add-rat` and the others, and says the methodology allows postponing that decision (SICP p.96).
- `[extrapolation]`: the v1 barrier diagram with "line segments / Cartesian points / pairs" corresponds to exercise 2.2 (segments and points, SICP p.96), but the book does not use the example of swapping Cartesian coordinates for polar in this section; polar vs rectangular appears in 2.4 (SICP p.168-171).

## 3. What is "data"? (SICP 2.1.3)
- `[from source]` (SICP p.97): data is defined by a collection of selectors and constructors plus conditions they must satisfy; for pairs, the condition is that if `z` is `(cons x y)` then `(car z)` is `x` and `(cdr z)` is `y`.
- `[from source]` (SICP p.97-98): `cons`, `car`, `cdr` can be implemented with procedures alone (`cons` returns a `dispatch` procedure that responds to 0 or 1). The book stresses that the goal is not to show that Scheme works this way (Lisp implements pairs directly, for efficiency), but that it *could*; that the ability to manipulate procedures as objects automatically gives the ability to represent compound data; and that this style is called **message passing** (SICP p.98).
- `[inference]` (from SICP p.97-98): "data" and "code" are not disjoint categories; it is a contract between constructors and selectors. The phrase "the distinction is purely artificial" from v1 is interpretation, not book text.

## 4. Closure property
- `[from source]` (SICP p.104): the ability to create pairs whose elements are pairs is the essence of the importance of lists; it is called the *closure property of cons*. A combining operation satisfies closure if the results of combining things with it can be combined with the same operation. Closure is the key to the power of a means of combination because it allows hierarchical structures.
- `[from source]` (SICP p.141, note 6): the term comes from abstract algebra (a set closed under an operation); the book warns that the Lisp community also uses "closure" for an implementation technique for procedures with free variables, a sense that SICP does **not** use. Therefore, the entry "Closure (function) (SICP p.230)" in version 1 was a misattribution.
- `[from source]` (SICP p.105): lists are sequences formed by nested `cons` (`(cons 1 (cons 2 ...))` and `list`). Trees and hierarchies: SICP p.112; convention "sequences as conventional interfaces" (`enumerate`, `filter`, `map`, `accumulate`, "signal flow"): SICP p.117-118.
- `[from source]` (SICP p.141, note 7): Fortran/Basic combine data in arrays that cannot contain arrays; Pascal/C admit structures of structures, but require the programmer to manipulate pointers; the book says these languages lack a general "glue" like Lisp's pairs.

## 5. Limits of this reference
- The book does **not** call the set of rules the "closure property of algebra" anything beyond what appears on p.104 and p.141.
- There is no table "procedural abstraction = data = code" in SICP, nor the term "abstraction barrier" outside figure 2.1 and the cited text.
