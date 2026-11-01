# Go Spec rules (go1.26): map, pitfalls, generics, run-time errors and versions

Reference base for the Go specialist agent, derived mainly from the "Go Programming Language Specification" (go1.26), cited as "Spec". Every claim carries a page in the format (Spec p.N). Items that the source notes present as a derivation (logical consequence of rules, not a Spec sentence) carry the mark [inference]. What does not come from the Spec (or goes beyond its text) carries [inference]; knowledge external to the sources, when it appears, carries [extrapolation].

## Contents

1. How to read
2. "Where to look" map
3. Subtle rules and pitfalls, by topic (3.1 to 3.21)
4. Generics: type sets, constraints, comparable, instantiation, inference
5. Undefined and unspecified behavior and run-time errors
6. Versioned items
7. Source limitations and dated content

## 1. How to read

- The Spec does not use the term "undefined behavior" in the passages covered; it speaks of compile errors, implementation restrictions, run-time panics and implementation-dependent behavior (Spec p.4, p.12, p.111).
- Page numbers are those of the PDF used in the notes; with other pagination, use the topic as the key.
- [inference] entries are heuristics grounded in the Spec, not its text.

## 2. "Where to look" map

| Topic | Pages |
|---|---|
| Index, introduction, notation | p.1–3 |
| Source code, comments, tokens, automatic `;` | p.3–5 |
| Identifiers and keywords | p.5 |
| Operators and punctuation (lexical) | p.6 |
| Literals: integer, float, imaginary | p.6–8 |
| Literals: rune, string, escapes | p.8–11 |
| Constants (overview, default types, precision) | p.11–12 |
| Variables, static and dynamic type | p.12–13 |
| Boolean, numeric, string types | p.13–14 |
| Array and slice | p.14–16 |
| Struct, embedded, tags | p.16–18 |
| Pointer and function (types) | p.18–19 |
| Interfaces: basic, embedded, general, type sets, implementation | p.19–24 |
| Map and channel (types) | p.24–25 |
| Representation, underlying type | p.25–26 |
| Identity, assignability, representability | p.27–29 |
| Method sets | p.29–30 |
| Blocks, declarations, scope, labels, predeclared, exporting | p.30–32 |
| Constants and iota | p.32–34 |
| Type declarations (alias, definition) | p.34–36 |
| Type parameters, constraints, `comparable`, satisfaction | p.36–39 |
| `var`, `:=` | p.39–40 |
| Function and method | p.40–42 |
| Operands, qualified, composite literals, function literals | p.42–47 |
| Selectors, method expressions and values | p.47–52 |
| Index, slice expressions, type assertion | p.52–56 |
| Calls and variadics | p.56–58 |
| Instantiation and inference | p.58–63 |
| Precedence, arithmetic, overflow, float, string | p.63–68 |
| Comparison, logical, address, receive | p.68–71 |
| Conversions | p.71–76 |
| Constant expressions | p.76–77 |
| Order of evaluation | p.77–78 |
| Terminating statements, empty, labeled, expression, send, IncDec | p.78–81 |
| Assignment | p.81–83 |
| `if`, `switch` | p.83–87 |
| `for` and `range` (integer, function) | p.87–92 |
| `go`, `select` | p.92–94 |
| `return`, `break`, `continue`, `goto`, `fallthrough` | p.94–97 |
| `defer` | p.97–98 |
| Built-ins | p.98–105 |
| Packages, imports, sieve example | p.105–108 |
| Zero value | p.108–109 |
| Initialization, execution, errors, run-time panics | p.109–112 |
| `unsafe`, sizes and alignment | p.112–114 |
| Appendix: language versions | p.114–116 |
| Appendix: unification (can be ignored when writing code, Spec p.116) | p.116–117 |

Not summarized (consult directly): the EBNF of each production next to its section (p.3–47); examples of valid and invalid numeric literals (p.6–10); rune and string escapes (p.9–10); keyword list (p.5).

## 3. Subtle rules and pitfalls, by topic

### 3.1 Lexical and literals

- Automatic semicolon: inserted at the end of a line whose last token is an identifier, literal, `break`/`continue`/`fallthrough`/`return`, or one of `++ -- ) ] }`; it can be omitted before `)` or `}` (Spec p.5). Hence [inference]: breaking a line after a binary operator is safe, before it is not.
- `_` counts as a lowercase letter; `_42` is an identifier, not a literal (Spec p.4, p.6).
- Integers: `0` followed by digits is octal (`0600`); `0o` and `0b` and the `_` between digits are Go 1.13. The `_` cannot be doubled or placed at the end (Spec p.6–7).
- Hexadecimal float requires the `p` exponent; `0x15e-2` is a subtraction, not a float (Spec p.7–8).
- Decimal imaginary ignores leading zeros (`0123i == 123i`); `0o123i == 83i` (Spec p.8).
- Rune: `'\400'` illegal; `\u`/`\U` reject surrogates and values above 0x10FFFF; `'\''` valid, `"\'"` and `'\"'` (in a rune) illegal (Spec p.9–10).
- String: `\xNN` and `\nnn` are isolated bytes; `\u` gives UTF-8. `"\xff"` has 1 byte, `"ÿ"` has 2 (Spec p.10).
- Permitted restrictions: reject NUL, ignore a leading BOM and reject a BOM in the middle (Spec p.4).

### 3.2 Constants, representability and iota

- Numeric constants are exact, without overflow; hence there are no constants for -0, infinity or NaN (Spec p.11).
- Untyped: literals, `true`, `false`, `iota` and expressions with only untyped operands. Typed: by declaration with a type or conversion (Spec p.11).
- When acquiring a type by use, it is an error if the value is not representable. If the destination is a type parameter, the result is a non-constant value (Spec p.11).
- Default types: `bool`, `rune`, `int`, `float64`, `complex128`, `string`. An integer literal becomes `int`, a rune literal becomes `rune` (int32), `2.0` becomes `float64` (Spec p.12).
- Minimums of any implementation: 256-bit integers, 256-bit float mantissa, 16-bit exponent; error if the integer is not exact or if the float overflows; rounds if precision is lacking (Spec p.12).
- Representability (Spec p.28–29): a float is representable if it rounds without overflow (negative zero becomes zero). Spec examples: `1e10` fits in `uint64`; `1.1` does not fit in `int`; `-1` not in `uint16`; `1024` not in `byte`; `'a'` not in `string`; `1e1000` not in `float64`; `42i` not in `float32`; `(42 + 0i)` fits in `float32`. For type parameter T, it holds for each type of the type set.
- `const`: the number of identifiers equals the number of expressions. With an explicit type, the expressions must be assignable to it and the type cannot be a type parameter; without a type, the constant keeps the expression's type. `const zero = 0.0` is an untyped float (Spec p.32).
- In a parenthesized block, omitting the list repeats the previous list and type (Spec p.33).
- `iota` is the index of the ConstSpec in the block, from 0, untyped; several uses in the same ConstSpec have the same value; outside a block it is 0; a fixed-value line consumes an index. To type the sequence, declare the type on the first line (Spec p.33–34).

### 3.3 Types: underlying, identity, assignability

- Underlying type: for a predeclared type or type literal, itself; for a defined type, that of the declaration; for a type parameter, that of the constraint (interface). An alias does not create a type (Spec p.26).
- Identity (Spec p.27): a named type is always different from any other. The rest is structural: array (element and length), slice, pointer, map, channel (element and direction), function (arity, types and variadicity; parameter names do not count), interface (same type set), instantiated type (same generic and identical type args). Struct: same sequence of fields, names, types, tags and embedded condition; non-exported fields from different packages always differ. An empty tag equals absence (Spec p.17).
- Assigning x (type V) to T is permitted if (Spec p.28): (1) V and T identical; (2) same underlying type, no type parameter, and at least one unnamed; (3) channels of the same element, V bidirectional, and one of the two unnamed; (4) T an interface (not a type parameter) implemented by x; (5) x is `nil` and T is a pointer, function, slice, map, channel or interface; (6) x is an untyped constant representable in T.
- Type parameters: `nil` is assignable to T if it is to each type of the type set; an unnamed V is assignable to each type of T's type set; V a type parameter is assignable to an unnamed T if all of V's type set is (Spec p.28).
- Consequence [inference of rule 2]: `type A int` and `type B int` are not assignable to each other, since both are named.
- Alias (Go 1.9): same type, no new methods. The alias cannot be a type parameter declared in the declaration itself (`type A[P any] = P` illegal), but can be a type parameter of the enclosing function (Spec p.34).
- A type definition creates a distinct type; the given type cannot be a type parameter (`type T[P any] P` illegal) (Spec p.35–36).
- The definition does not inherit methods: `type NewMutex Mutex` and `type PtrMutex *Mutex` have an empty method set; but interface methods and methods of elements of a composite type remain (`type MyBlock Block` with Block an interface keeps the methods) (Spec p.35–36).

### 3.4 Numerics, string, array and slice

- Numeric types are all distinct, except `byte` (alias of `uint8`) and `rune` (alias of `int32`). `int` and `int32` differ even with the same size; mixing requires conversion. `int` has the size of `uint` (32 or 64 bits); arithmetic is two's complement (Spec p.14).
- A string is an immutable sequence of bytes. `len(s)` counts bytes (constant if `s` is constant); `&s[i]` is invalid; `s[i]` is a non-constant `byte` and not assignable (Spec p.14, p.53).
- The array length is part of the type and is a non-negative constant representable as `int` (Spec p.14).
- Direct recursion through an array or struct is illegal (`type T [10]T`); going through a pointer, function or slice is valid (Spec p.15, p.18).
- An uninitialized slice is `nil`; slices of the same array share storage; capacity is the size plus the rest of the array (Spec p.15). `make([]T, n, c)` is equivalent to slicing a new `[c]T`; slices of slices require initializing the inner ones, which may have different sizes (Spec p.16).
- Predeclared types, arrays and structs are self-contained (full copy; zero is never nil). Pointer, function, slice, map and channel have shared references: changing a slice element affects all slices of the array (Spec p.26).

### 3.5 Struct, pointer and function

- An embedded field is `T` or `*T` (T a non-pointer type name and not a type parameter; `*T` only for non-interface); the field name is the unqualified name (Spec p.16–17). Embedding `T` and `*T` together is illegal (Spec p.17).
- Promoted fields and methods act like ordinary ones, except that they do not name a field in a composite literal of the outer struct (Spec p.17).
- Method sets with embedding (Spec p.17): S with embedded `T` has in S and `*S` the promoted methods with receiver `T`, and `*S` also those of `*T`; S with embedded `*T` has both in S and `*S`. Implication [inference]: a struct by value with embedded `T` does not satisfy an interface that requires a method with receiver `*T`.
- The zero of function and pointer is `nil`. In parameter and result lists, either all names exist or none; only the last parameter is variadic (Spec p.18–19).

### 3.6 Basic interfaces, map and channel

- An uninitialized interface is `nil`; `any` is an alias of `interface{}` (Go 1.18). Explicit method names are unique and not blank. When embedding interfaces, same-named methods need identical signatures (Spec p.19–21).
- Static versus dynamic type, in two layers. [from source] An interface variable has a dynamic type: the non-interface type of the assigned value, unless the value is the predeclared `nil`, which has no type; the Spec's example assigns `x = v` with `var v *T` and says `x` now has the value `(*T)(nil)` and dynamic type `*T` (Spec p.12). [from source] Two interfaces are equal if they have identical dynamic types and equal dynamic values, or if both are nil (Spec p.69). [inference] The conclusion that `x != nil` in that case, and hence the "classic pitfall" of an interface with a nil pointer, is a deduction from p.12 + p.69. No source describes the pitfall and Effective Go (2009) does not cover it.
- `new` and the address of a composite literal allocate anonymous variables (Spec p.12).
- A map is unordered. The key requires full `==` and `!=`: it cannot be a function, map or slice; an interface key with a non-comparable dynamic value causes a panic (Spec p.24). A nil map reads as empty, but does not accept insertion. The `make(map, n)` hint does not limit the size. Removal by `delete` and `clear` (Spec p.24).
- Channel: zero is `nil` and is never ready to communicate. Unbuffered, the send only completes with a ready receiver. The direction can only be restricted, never widened. The `<-` associates with the leftmost `chan`: `chan<- <-chan int` is `chan<- (<-chan int)`. Several goroutines can use the same channel (send, receive, `cap`, `len`) without extra synchronization; it is FIFO (Spec p.25).

### 3.7 Method sets and method declaration

- Method set of defined type T: receiver `T`. Of `*T`: receiver `*T` or `T` (T neither pointer nor interface). Of an interface: the intersection of the type set. Other type: empty (Spec p.29–30).
- Names unique and not blank; if the base type is a struct, method names and non-blank field names must differ (Spec p.30, p.41).
- Method: one non-variadic receiver, of type `T` or `*T`, with T defined (neither pointer nor interface) in the same package; the identifier can be omitted (Spec p.41).
- Generic receiver: `func (p Pair[A, B]) ...`; names free and unique, constraints implicit from the definition; MethodDecl has no parameter list of type parameters of its own (Spec p.41–42).
- Receiver via alias: the alias cannot be generic nor denote an instantiated generic type, directly or indirectly (Spec p.42).
- There are no method literals nor a distinct "method" type (Spec p.58).

### 3.8 Declarations, scope and shadowing

- No identifier is declared twice in the same block, nor in the file block and package block at the same time. `_` and `init` do not create a binding; `init` in the package block can only be a function (Spec p.30).
- Implicit blocks: universe, package, file, each `if`/`for`/`switch`, each clause of `switch`/`select` (Spec p.30).
- Scopes (Spec p.30–31): top level in the package block; imported package in the file block; receiver, parameters and results in the body; function type parameter from the function name to the end of the body; type's, from the type name to the end of the TypeSpec; local const/var, from the end of the Spec to the end of the innermost block; local type, from the identifier on (can be recursive).
- Shadowing: an inner block can redeclare; the inner entity prevails while visible (Spec p.31). Since the local scope begins after the declaration, `x := x` reads the outer `x` [inference, Spec p.31]. Predeclared identifiers can be shadowed [inference from the universe scope].
- Labels: scope is the function body (no nested functions), they do not collide with other identifiers; an unused label is an error. The `package` clause is not a declaration (Spec p.31).
- Predeclared (Spec p.31–32): types `any bool byte comparable complex64 complex128 error float32 float64 int int8..int64 rune string uint uint8..uint64 uintptr`; constants `true false iota`; `nil`; functions `append cap clear close complex copy delete imag len make max min new panic print println real recover`.
- Exported: first character a Unicode uppercase letter (category Lu), declared in the package block or a field/method (Spec p.32). Alphabets without uppercase (CJK) do not export [inference]. Non-exported names from different packages are different (Spec p.32).

### 3.9 Variables, `:=` and functions

- `var` without a type: the type comes from the value; an untyped constant uses the default; `nil` does not initialize a variable without an explicit type (Spec p.39).
- The compiler may reject a local variable never used; the Spec only permits it, does not require it (Spec p.39).
- `:=` only in functions. It can redeclare variables from the same block (or from the parameter list, in the body) with the same type, if at least one non-blank is new; redeclaring only assigns. Non-blank names on the left are unique (Spec p.40).
- Pitfall [inference from the "same block" rule]: inside an `if`, `err := ...` with everything new in that block creates a shadowed `err`, without assigning to the outer one (Spec p.40).
- A function with results ends in a terminating statement, otherwise "missing return" (Spec p.40–41; list in 3.18). Without type parameters, the body may be missing (external implementation). A generic function must be instantiated before being called or used as a value (Spec p.41).

### 3.10 Operands, composite literals and closures

- Blank only as an operand on the left of an assignment. Qualified requires an imported package and an exported identifier from the package block (Spec p.43).
- A composite literal creates a new value on each evaluation; elements and keys must be assignable, without extra conversion; a duplicate key is an error (Spec p.43–44).
- Parsing: a literal with a TypeName between the keyword and the `{` of `if`/`for`/`switch` needs parentheses (Spec p.44).
- Struct without keys: all fields, in order. With keys: omitted ones become zero; naming a non-exported field of another package is an error (Spec p.44). Hence [inference], a keyless literal of a foreign struct is infeasible when there are non-exported fields.
- Array and slice: key a non-negative constant representable as `int`; without a key, uses the previous index + 1. `[...]T` fixes the length at max index + 1; fewer elements fills with zero; an index outside the array is an error. A slice literal has len and cap equal to max index + 1 (Spec p.45).
- Empty versus nil: `&[]int{}` points to an empty non-nil slice; `new([]int)` points to a nil slice (Spec p.45).
- Map literal: every element has a key; order of non-constant keys in 3.17 (Spec p.45).
- Elision of the element and key type when identical to the literal's; `&T` omittable if the element is `*T`; with a named pointer (`type PPoint *Point`) it makes an implicit conversion (Spec p.46).
- Literal whose type is a type parameter: all types of the type set with the same underlying type, valid for a literal (Spec p.44).
- A function literal does not declare type parameters. It is a closure: captured variables are shared and live while accessible (Spec p.46–47). Capture is by variable, not by value [inference]; see 3.18 for the per-iteration `for`.

### 3.11 Selectors, method expressions and method values

- `x.f`: depth is the number of embedded fields traversed; the smallest prevails; without exactly one `f` at that depth, it is ambiguous and illegal (Spec p.48).
- `x.f` with a defined pointer is shorthand for `(*x).f` only for fields; `q.M0()` with `type Q *T2` is invalid (Spec p.48–49).
- `x.m()` is shorthand for `(&x).m()` if x is addressable and m is in the method set of `&x` (Spec p.57); a call result is not addressable, so `makeT().Mp()` is invalid (Spec p.52).
- Method expression `T.M` takes the receiver as the first argument. `(*T).Mv` is allowed; `T.Mp` (pointer receiver via value type) is illegal. It is also derived from an interface method (Spec p.50).
- Method value `x.M`: x is evaluated and copied at creation; later changes to `*t` do not affect the saved receiver. Value receiver with x a pointer copies the pointed-to value at that instant; pointer receiver with an addressable value stores `&x` (Spec p.50–52). Pitfall [inference]: `defer`/goroutine/callback with `obj.Method` and a value receiver uses the copy from the moment of creation.

### 3.12 Index, slice expressions, type assertion and calls

- Index (Spec p.52–53): non-negative constant representable as `int` (untyped becomes `int`); a variable must be an integer. A constant outside the array (or of a constant string) is a compile error; at run time, panic. On a pointer to an array, `a[x]` is `(*a)[x]`; on a pointer to a slice it does not hold. A missing or nil map reads the zero value (`v, ok = m[k]` reports); assigning to a nil map panics. Map elements are not in the addressable list (p.70), so `&m[k]` is not allowed [inference].
- Index by type parameter: identical elements across the whole type set (string gives byte); if there is a map, all maps with identical keys; not assignable if there is a string (Spec p.53).
- Simple slice `a[low:high]`: array and string go up to `len`; slice goes up to `cap(a)`, so `s[:cap(s)]` is valid. Non-negative constants with `low <= high`. A sliced array must be addressable. Slicing nil gives nil. The result shares the array (Spec p.54–55).
- Full slice `a[low:high:max]`: cap = `max - low`; does not hold for string; only the first index is omittable; `0 <= low <= high <= max <= cap(a)`. Limits capacity and forces reallocation on `append` [inference from usage]. Slicing a string gives a non-constant result of the same type (Spec p.55).
- `x.(T)` requires x to be an interface (not a type parameter). Concrete T must implement x's type, otherwise a compile error; interface T checks the dynamic type. Single form: panic on failure; `v, ok` form: zero value, no panic; nil x always fails (Spec p.56).
- Call: the function and arguments are evaluated, then parameters and results are created; nil function panics. `f(g(...))` holds if g returns several assignable values, without other arguments. A variadic with no arguments receives `nil`; with arguments, a new slice; `s...` passes the slice without copying, and changes show up in the caller (Spec p.57–58).

### 3.13 Operators, arithmetic and floating point

- Binary operators require identical types, except shifts and untyped constants (converted to the other operand) (Spec p.64). Shift count: signed integer (Go 1.13) or an untyped constant representable in `uint`.
- Non-constant shift with an untyped constant left operand: the constant takes the type it would have if only the left side were there. `var f float32 = 1<<s` and `1.0<<s` in a float context are illegal; `make([]byte, 1.0<<s)` and `a[1.0<<s]` use `int`; with a 32-bit `int`, shifting by 33 zeroes without error (`a[1.0<<s]` becomes `a[0]`), with 64 bits it panics (Spec p.64).
- Precedence: 5 `* / % << >> & &^`; 4 `+ - | ^`; 3 comparisons; 2 `&&`; 1 `||`. Left-associative. Since `&` is multiplicative and `|` additive, `a & b == c` is `(a & b) == c` (Spec p.65).
- `++` and `--` are statements; `*p++` is `(*p)++` (Spec p.65). Type parameter operands: operator valid for the whole type set; precision of the concrete argument (Spec p.66).
- Integers (Spec p.66–67): division truncates toward zero and the remainder has the sign of the dividend (`-5/3 = -1`, `-5%3 = -2`); the type's minimum divided by -1 gives itself, remainder 0, no panic. A constant zero divisor is a compile error; at run time, panic. Dividing by a power of 2 equals shifting only for a non-negative dividend (`-11/4 == -2`, `-11>>2 == -3`). A negative shift count panics; no upper limit; right shift is arithmetic on signed and logical on unsigned. Unsigned wraps modulo 2^n; signed has deterministic overflow without panic, and the compiler cannot assume `x < x+1`. `^x` uses a mask of 1 bits (unsigned) or -1 (signed).
- Float (Spec p.67–68, p.78): division by zero beyond IEEE 754 depends on the implementation; FMA fusion may occur, even across statements; `float64(x*y) + z` forces rounding and forbids fusion; exact equality may diverge between architectures [inference]. Parentheses control the order: in `x + (y + z)`, `y+z` comes first.

### 3.14 Comparison, address and receive

- Slice, map and function compare only with `nil`. Struct compares field by field, ignoring `_`, stopping at the first difference; array by index (Spec p.69).
- [from source] Two interfaces are equal if they have identical dynamic types and equal dynamic values, or if both are nil (Spec p.69). Comparing interfaces with the same non-comparable dynamic type causes a panic; it holds for arrays of interfaces and structs with an interface field (Spec p.69). Beware `==` on `any`/`error` and `any` as a key [inference]. About an interface holding a nil pointer and `x != nil`: deduction from Spec p.12 + p.69 [inference], see 3.6.
- Pointers to distinct zero-size variables may or may not be equal. Channels are equal if from the same `make` or both nil. A non-interface X compares with interface T if X is comparable and implements T. The result is an untyped boolean (Spec p.69).
- Strictly comparable: comparable with no interface at any level; a type parameter is comparable if strictly so (Spec p.69–70). Since Go 1.20, interfaces satisfy `comparable` without being strict, with the risk of panic (Spec p.116).
- `&&` and `||` evaluate the right side only if needed (Spec p.70).
- `&x` requires addressable (variable, indirection, slice index, field of an addressable struct, index of an addressable array) or a composite literal; `&*x` with x nil panics (Spec p.70).
- Receiving from a nil channel blocks forever; from a closed channel returns zero after the values already sent; in `v, ok := <-ch`, `ok` is true only for an actual send. Type parameter: all channels with receive and the same element (Spec p.70–71).

### 3.15 Conversions (Spec p.71–76)

- Constant to an ordinary type yields a typed constant; to a type parameter yields a NON-constant value, with the argument's precision (Spec p.71–72). Integer constant to string follows the code point.
- Permitted (non-constant): assignable; same underlying type (ignoring tags); unnamed pointers whose bases have identical underlying types; integer and float between each other; complex between each other; integer, `[]byte`, `[]rune` to string; string to `[]byte`/`[]rune`; slice to array (Go 1.20); slice to array pointer (Go 1.17). Pointer and integer only via `unsafe` (Spec p.72–73).
- Integer to integer: sign extension or zeros, truncation, no overflow signal: `uint32(int8(uint16(0x10F0))) == 0xFFFFFFF0`. Float to integer truncates toward zero. `float32(x)` forces rounding (Spec p.73).
- Float/complex out of range: no failure, implementation-dependent result (Spec p.74).
- String to `[]byte`/`[]rune` gives a non-nil slice, implementation-dependent capacity; a nil or empty `[]byte` becomes `""` (Spec p.74).
- Integer to string gives the UTF-8 of the code point (invalid becomes U+FFFD). The text warns that the form may go away, that `go vet` flags uses and that `utf8.AppendRune`/`utf8.EncodeRune` are preferred. `string(65)` is `"A"` (Spec p.75).
- Slice to array/pointer: panic if `len(slice) < len(array)`. Nil becomes `[0]T` without error and a nil pointer; empty non-nil gives a non-nil pointer, pointing to the underlying array (Spec p.75–76).

### 3.16 Constant expressions (Spec p.76–77)

- Exact precision: `Huge = 1<<100` and `Huge >> 98` in `int8` is valid. The compiler may round untyped float constants, affecting validity in an integer context.
- Mixing untyped constants: the "constant kind" further along in integer, rune, float, complex wins. `const x float64 = 3/2` is 1.0; `3/2.` is 1.5.
- A typed constant must be representable: `uint(-1)`, `int(3.14)` and `Four * 100` with `Four int8` do not compile. Constant division or remainder by zero is an error.
- Untyped `^1` is -2; `uint8(^1)` is illegal; `^uint8(1)` is 0xFE.
- Constant shift: untyped left gives an integer constant; otherwise the left's type, which must be an integer (`float64(2) >> 1` illegal).
- `len`/`cap` are constants, without evaluating the argument, for a constant string or array (or pointer to array) with no receive or non-constant call in the expression (Spec p.102). Thus, `range` with only an index over a nil `*[7]int` does not dereference (Spec p.89–90).

### 3.17 Order of evaluation (Spec p.77–78)

- In an expression, assignment or `return`, calls, receives and binary logical operators proceed left to right.
- The order between that and reading variables or indexing is NOT specified: `[]int{a, f()}` may give `[1,2]` or `[2,2]` if `f` changes `a`. Repeated or dependent keys in a map literal are ambiguous. Review rule [inference]: flag as a defect an expression that reads a variable and calls something that changes it.
- At package level, initialization dependencies take precedence over left-to-right order between expressions, but not within each one.

### 3.18 Statements

Terminating (Spec p.78–79): `return`, `goto`, call to the built-in `panic`; terminating block; `if` with `else` and both terminating; `for` without a condition, without range and without a `break` referring to it; `switch` with `default`, without `break` and with terminating cases (or `fallthrough`); `select` without `break` with terminating cases; a label on a terminating statement. Only the built-in `panic` counts (p.78); the Spec lists the cases and says other statements do not terminate (p.79). That `log.Fatal` and `os.Exit` do not count is [inference] from that list (the Spec does not mention them). A `for {}` with a `break` referring to it stops being terminating.

Expression as a statement: `append cap complex imag len make new real` and the `unsafe` functions (Add, Alignof, Offsetof, Sizeof, Slice, SliceData, String, StringData) cannot be; a discarded `append(s, x)` does not compile (Spec p.80).

Assignment (Spec p.81–83):
- Two phases: the index and indirection operands on the left and the expressions on the right are evaluated; then assignment goes from left to right. So `i, x[i] = 1, 2` uses the old `i`; `x[0], x[0] = 1, 2` leaves 2; `x[1], x[3] = 4, 5` assigns `x[1]` and then panics on `x[3]`.
- `x op= y` is `x = x op (y)` with `x` evaluated once; blank is not valid on the left of `op=`. Target: addressable, map index or `_`. Assigning copies the reference, not the referent. An untyped constant to an interface or blank takes the default type.

`switch` (Spec p.83–87):
- Expression evaluated once; cases from left to right and top to bottom until the first that matches; they need not be constants, and `case f():` only has effect if reached. `default` in any position, only if nothing matches; without an expression it is `true`; `nil` does not work; the type must be comparable.
- `fallthrough` only as the last non-empty statement of a clause that is not the last, and never in a type switch. The compiler may reject duplicate constants (current ones reject integers, floats and strings, Spec p.85).
- Type switch: x an interface (not a type parameter); distinct types that implement x's type; at most one `case nil`. In `v := x.(type)`, `v` has the case's type if there is only one; with several types, `default` or `nil`, it has x's type. A type parameter that, when instantiated, duplicates a previous case: the first prevails (Spec p.85–86).

`for` and `range` (Spec p.87–92):
- Clause: init once; post after each execution of the block; post is not a short declaration.
- Per iteration (Go 1.22): each iteration has its own variables; the next is born before the post, with the previous one's value at that moment. Closures with `i++` in the body print 1, 3, 5 (before 1.22: 6, 6, 6) (Spec p.88). Also holds for `range` variables (p.90).
- Range accepts array, pointer to array, slice, string, map, channel with receive, integer (Go 1.22) and iterator function (Go 1.23). Channel and integer have at most one variable; the others, two (Spec p.88).
- The expression is evaluated once before the loop, except with at most one variable and `x` or `len(x)` constant. The notes say the text does not detail whether an array by value is copied (Spec p.89).
- Array/slice in ascending order (nil slice does not iterate). String by code points, index of the first byte; invalid UTF-8 gives U+FFFD and advances one byte. Map: order unspecified and variable; an entry removed beforehand is not produced; one created during may or may not be; nil does not iterate. Channel: until closed; nil blocks forever; `for range ch {}` drains (Spec p.89–90).
- Integer: from 0 to n-1, nothing if n <= 0. An integer type of n is valid; an untyped constant uses the type of the pre-existing integer variable or the default (`int`). Invalid: `for u = range 256` with `u uint8` and `range 1e3` (Spec p.89–91).
- Iterator function: `func(func() bool)`, `func(func(V) bool)` or `func(func(K, V) bool)`. The range passes a synthesized yield; each call runs the body once and returns true; if the body ends (e.g., `break`), it returns false and must not be called again (Spec p.89–90). Iterators must test the return and stop (Spec p.91). The Spec does not say here the consequence of calling yield after false, nor does it deal with `defer`/`recover` in the iterator.
- Type parameter: same underlying type across the whole type set; with channels, only channels of the same element and with receive (Spec p.92). Variables not declared by the range pre-exist and receive as in an assignment (Spec p.90).

`return`, jumps, `go`, `select`, `defer`:
- Results start at zero: the Spec says that, however declared, "result values are initialized to the zero values" on function entry (Spec p.95). `return` with values assigns the results before the defers (Spec p.95). `return f()` multivalued is accepted; a bare return requires named results; shadowing a result (`if _, err := ...` and bare `return`) may be rejected (Spec p.94–95).
- `break` exits the innermost `for`/`switch`/`select`; use a label to exit the loop from inside a switch/select. A labeled `continue` requires an enclosing `for`. `goto` does not jump over a declaration that would enter scope nor into a block (Spec p.95–97).
- `defer` with a nil function panics at invocation, not at declaration (Spec p.97). With `defer obj.Method` the method value copy in 3.11 applies [inference].
- The notes are sparse on `go` (p.92), `select` (p.92–94) and `defer` (p.97–98). It is known that a nil channel is never ready (p.25), that `select` enters the terminating-statement rule (p.79) and that `break` only ends the `select` (p.95). Other details: consult the Spec.

### 3.19 Built-ins (Spec p.98–105)

The notes keep only these rules:
- `append` and `copy`: the result is independent of memory overlap (Spec p.98).
- `min`, `max`, `clear`: Go 1.21 (Spec p.99, p.103, p.116).
- `close`/send on a closed channel or `close` of nil: panic (Spec p.80, p.99–100).
- `len` and `cap` always fit in `int` (Spec p.101); constness in 3.16.
- `make` of a slice/channel with a negative size or `n > m` at run time: panic. The map hint is only a hint (Spec p.102–103).
- `new(expr)` appears in the body (Spec p.104) with no version in the appendix (section 6).
- `panic(nil)` is a run-time panic (Spec p.105), no version given.
- `print` and `println` (Spec p.105): the Spec treats them as bootstrapping functions, documented for completeness, with no guarantee of remaining in the language; they return no result; the formatting of arguments depends on the implementation; `println` puts spaces between the arguments and a line break at the end. An implementation need not accept arbitrary types, but must accept boolean, numeric and string. [inference] In review, `println`/`print` in production code is a sign of forgotten debugging; use a logging package; the Spec gives no such guidance.

### 3.20 Packages, zero value and initialization

- A package name is not `_`. Import with `.` brings exported names into the file block; `_` only initializes. Importing itself (directly or indirectly) is illegal, as is importing without using an exported name (except `_`). The meaning of the path depends on the implementation (Spec p.106–107).
- The zero value is recursive: `false`, `0`, `""` and `nil` for pointer, function, interface, slice, channel, map (Spec p.108).
- Initialization: order between files depends on presentation to the compiler; the Spec encourages lexical order by name (p.109); hidden dependencies make the order unspecified (p.110); packages by import path order, no version given (p.111); initialization dependency beats left-to-right order (p.78). The notes do not detail the dependency rules for variables or `init`; read p.109–111.

### 3.21 unsafe, sizes and alignment (Spec p.112–114)

- Pointer and integer only convert via `unsafe` (Spec p.73); the effect of `unsafe.Pointer` to `uintptr` and back depends on the implementation (p.112).
- `unsafe.Add` and `unsafe.Slice`: Go 1.17. `SliceData`, `String`, `StringData`: Go 1.20 (Spec p.113–114, p.116).
- `unsafe.Slice` and `unsafe.String` panic with negative len, or nil ptr with non-zero len (Spec p.113–114). The return of `StringData` on an empty string and the address of `SliceData` with zero cap on a non-nil slice are unspecified (p.114).
- Size of `int`, `uint`, `uintptr`: 32 or 64 bits (Spec p.14). Size and alignment tables (p.113–114) are not in the notes.

## 4. Generics: type sets, constraints, comparable, instantiation and inference

### 4.1 Type parameters

- Go 1.18. Each parameter is a new named type, a placeholder. Non-blank names are unique and all names are mandatory; `[_ any]` is valid (Spec p.36–37).
- A constraint is an interface. If it is `interface{E}` with E a type element, the `interface{}` can be omitted in the list: `[T ~int]`, `[T int|string]`, `[T []P]`. Outside a list it is illegal (`type Constraint ~int`) (Spec p.37–38).
- Parse: in `type T[P *C] ...` an array is read. Resolve with `interface{*C}` or a trailing comma `[P *C,]` (Spec p.37).
- In a definition or alias, the given type is not a type parameter (Spec p.34, p.36). A function literal does not declare type parameters (p.46). Methods use only the receiver's (p.41–42).
- Scope: a function's begins after the function name (the constraint cites other parameters); a type's, after the type name, allowing `List[T]` with `next *List[T]` (Spec p.31, p.36).
- Generic alias: Go 1.24, must be instantiated on use (Spec p.34). A generic type requires explicit type args in every instantiation (p.36, p.60).

### 4.2 Type sets

- Every interface defines a type set. Basic: only methods, usable as a variable type. General: has type elements (`T`, `~T`, unions) or `comparable`; only valid as a constraint or element of another constraint interface, never as the type of a variable, field or non-interface component (Spec p.19–23).
- Computation (Spec p.21–22): empty interface = all non-interface types; non-empty = intersection of the elements; method = non-interface types whose method set includes it; `T` = only T; `~T` = types whose underlying type is T; union = union of the type sets. The type set never contains interfaces; "all types" includes those of all possible programs.
- `interface{ int; string }` has an empty type set (Spec p.22). The declaration compiles, but cannot be instantiated (p.43); the compiler need not report a type parameter operand with an empty type set before instantiation (p.43). In review, be suspicious [inference].
- `~T`: the underlying type of T is T itself and T is not an interface; `~MyInt` and `~error` are illegal (Spec p.22).
- T in `T` or `~T` is not a type parameter. Non-interface terms of a union have disjoint type sets: `~int | MyInt` illegal; `float32 | Float` is valid, since Float is an interface (Spec p.23). `MyInt` (from `type MyInt int`, Spec p.22) appears in the Spec without a tilde: `~int | MyInt` is the illegal example (Spec p.23). [inference] `int | MyInt` (both without a tilde) is legal, since `{int}` and `{MyInt}` are disjoint; the text does not give that example literally, only the disjointness rule (p.23) and the type set of `T` without a tilde as "only T" (p.21–22).
- Implementation restriction: a union with more than one term cannot contain `comparable` nor interfaces with methods, nor embed such interfaces (Spec p.23). An interface does not embed itself by a type element, nor via a union or array (Spec p.23–24).
- Implementation: a non-interface T implements I if it is in I's type set; an interface T, if its type set is a subset of I's (Spec p.24).

### 4.3 `comparable` and satisfaction (Spec p.38–39)

- `comparable` (Go 1.18) is the set of strictly comparable non-interface types. Interfaces are comparable but not strictly: they do not implement `comparable`, although they satisfy it since Go 1.20, which allows `any` in `[K comparable]` (Spec p.38).
- Examples (p.38): `int` implements; `[]byte` does not; `interface{}` does not implement but satisfies; `struct{f any}` satisfies without implementing.
- Formal rule: T satisfies C if T implements C, or if C is written as `interface{ comparable; E }` with E a basic interface, and T is comparable and implements E.
- [from source] Spec table: `any` does NOT satisfy `interface{ comparable; int }` (p.38) nor `interface{ comparable; m() }` (p.39), although `any` satisfies `comparable` alone (p.38). [inference] The reason, by the formal rule above, is that `any` does not implement the element E (`int` or `m()`); the justification column of the table is truncated in the PDF extraction.
- Consequence: comparing type parameter operands may panic, since `any` as an argument may have a non-comparable dynamic value (Spec p.39). `comparable` and interfaces that embed it only serve as constraints (p.38).

### 4.4 Instantiation (Spec p.58–59)

- Two steps: substitute each type arg throughout the declaration (including in the parameter list) and check whether each satisfies the substituted constraint. If it fails, the instantiation fails. An instantiated type becomes a named non-generic type; an instantiated function becomes a non-generic function.
- Type args may be omitted if inferable: a call with ordinary arguments, assignment to a variable of known type, passing as an argument or return. In other cases (`x := sum`) the list is mandatory. A partial list is a prefix (omit from the right) and is not empty: `apply[]` is illegal (p.59). In generic types, always explicit (p.60).
- [from source] Spec example (p.59), with `func apply[S ~[]E, E any](s S, f func(E) E) S`: `f1 := apply[[]int]` explicitly supplies only the type argument of S (the Spec comment is cut off in the PDF extraction after "type argument for", and the rest is E's inferred argument); `f2 := apply[[]string, string]` supplies both explicitly. That E is inferred from `S ~[]E` in `f1` is [inference] with the mechanism of p.60–61 (equation `S ≡C ~[]E`).
- Gap: the text of the compiler error message when inference fails (for example "cannot infer T") is in no source; the Spec only says that, if inference fails, the program is invalid (p.60).

### 4.5 Inference (Spec p.59–63; appendix p.116–117)

- A system of equations is solved for the bound type parameters (parameters without an explicit argument, including those of generic functions passed as arguments); those of outer functions enter the equations without being solved (Spec p.61).
- Equations: per pair (untyped non-constant argument, parameter), `typeof(p) ≡A typeof(a)` (undirected assignability); per parameter, `Pk ≡C Ck` (constraint); also for assignment and return of a generic function to a variable of function type (Spec p.60–61).
- Two phases: unification with typed operands; then untyped constants (p.61). For a parameter still without an argument, the default type of the "constant kind" applies; a conflict between kinds of untyped constants for the same parameter makes inference fail ("conflicting constant kinds", p.62); lack of an argument after the two phases or a cycle in the arguments also make it fail (p.62).
- In assignment, passing or `return`, the top-level structure may match loosely, the elements exactly (p.63). Constraints: if the whole set has the same underlying type U and P already has an argument, they unify loosely; a single-term constraint that is not `~T` fixes that term in P; repeats while there are new arguments (p.63).
- Example (p.60): `dedup[S ~[]E, E comparable](S) S` with `Slice` (named over `[]int`) gives S=Slice and E=int via `~[]E` (implicit core type).
- Go 1.21: uses interface methods and infers arguments of an assigned or passed generic function (Spec p.116). The appendix's unification rules are only mapped; the Spec says they can be ignored when writing code (p.116).

Operations with type parameters require compatibility across the whole type set: index, range, receive, literal and operators (p.44, p.53, p.66, p.71, p.92); type assertion and type switch require x to be an interface, not a type parameter (p.56, p.85).

## 5. Undefined and unspecified behavior and run-time errors

### 5.1 Run-time panics

Run-time errors are a `panic` with a `runtime.Error` value (satisfies `error`); the exact values per condition are not specified (Spec p.111–112). Causes:

- array, slice or string index out of bounds (p.52–53, p.111); slice expression out of range (p.54–55);
- integer division by zero (p.66); shift with a negative count (p.67);
- field via nil pointer; `&*x` with x nil (p.48, p.70, p.82); method via nil interface (p.48);
- assignment to a nil map (p.53); non-comparable interface key in a map (p.24);
- comparison of interfaces with a non-comparable dynamic type (p.69); comparison of a type parameter instantiated by `any` and similar (p.39). Concrete example: with `type Set[K comparable] map[K]struct{}` and `s := Set[any]{}`, `s[[]int{1}] = struct{}{}` panics; this is a deduction [inference] from Spec p.24 (an interface key with a non-comparable dynamic value causes a panic) + p.38–39 (`any` satisfies `comparable`, and the comparison may panic); the sources do not bring this example;
- a single-form type assertion that fails (p.56); call of a nil function (p.57);
- slice to array/pointer with a smaller slice (p.75);
- send on a closed channel; `close` of a closed or nil channel (p.80, p.99–100);
- `make` with a negative size or `n > m` (p.102);
- `unsafe.Slice`/`unsafe.String` with negative len, or nil ptr and non-zero len (p.113–114);
- `panic(nil)` (p.105); `defer` of a nil function, at invocation (p.97).

### 5.2 Unspecified or implementation-dependent

- Map iteration order and visibility of entries created in the loop (Spec p.24, p.89).
- Order between reading a variable/indexing and calls in the same expression; order of non-constant keys in a map literal (p.45, p.77–78).
- Panic on float division by zero; FMA fusion (p.67–68).
- Float/complex conversion out of range; rounding of untyped float constants (p.74, p.77).
- Capacity of string to `[]byte`/`[]rune` (p.74).
- Equality of pointers to zero-size variables (p.69, p.114).
- Initialization order with hidden dependencies and between files (p.109–110).
- Effect of `unsafe.Pointer` to `uintptr` and back; `StringData` of an empty string; `SliceData` with zero cap on a non-nil slice (p.112, p.114).
- Calling yield after false (p.90).

### 5.3 Restrictions permitted to the tool and guarantees

- May be rejected or limited: NUL and BOM outside the start (p.4); limited internal precision of constants, respecting the minimums (p.12); unused local variable (p.39); empty type set only at instantiation (p.43); union with `comparable` or an interface with methods (p.23); duplicate constant cases (p.85).
- Guarantees against unfounded fear: signed overflow is deterministic and without panic (p.67); conversion between integers never signals overflow (p.73); `len`/`cap` fit in `int` (p.101); `append` and `copy` are independent of overlap (p.98).

## 6. Versioned items

### 6.1 Marked in the Spec

General rule (Spec p.115): the appendix explains that source code using a feature is rejected if the language version implied or required by the compiler is earlier than the version in which the feature was introduced; the Spec's example is `0b1011`, rejected below Go 1.13. The following table lists the minimum language version per feature (Spec p.115–116). The link between this rule and the `go` line of `go.mod` comes from the release notes (RN1.21 p.3), not from the Spec [inference].

| Version | Feature | Where |
|---|---|---|
| Go 1.9 | Type alias | p.34, p.115 |
| Go 1.13 | `0b`/`0o`; `_` in literals; hexadecimal float; `i` suffix on any literal; signed shift count | p.6–8, p.64, p.115 |
| Go 1.14 | Embedding an interface in an interface; overlapping identical methods stops being an error | p.21, p.115 |
| Go 1.17 | Slice to array pointer; `unsafe.Add`, `unsafe.Slice` | p.72, p.113, p.115 |
| Go 1.18 | Generics: type parameters, `~`, unions, `any`, `comparable`, instantiation | p.6, p.20–21, p.36–38, p.58, p.115 |
| Go 1.20 | Slice to array; `unsafe.SliceData`/`String`/`StringData`; interfaces satisfy `comparable` | p.38, p.72, p.114, p.116 |
| Go 1.21 | `min`, `max`, `clear`; inference with interface methods and an assigned or passed generic function | p.99, p.103, p.116 |
| Go 1.22 | Per-iteration variables; range over integer | p.88–89, p.116 |
| Go 1.23 | Range over iterator function | p.88, p.116 |
| Go 1.24 | Alias with type parameters | p.34, p.116 |

Reconciliations between the notes:
- Predeclared identifiers (p.31) carry [Go 1.18] and [Go 1.21] together in the title; the appendix resolves it: `any` and `comparable` are 1.18; `min`, `max`, `clear` are 1.21.
- The [Go 1.21] mark is on the built-ins' DEFINITIONS: `clear` on p.99 and `min`/`max` on p.103 (confirmed in the text; the appendix repeats it on p.116). The USES in the body carry no mark: `clear` is cited in the map section without a version (p.24), and `min`/`max` appear without a version when speaking of constants (p.11). I did not confirm `min`/`max`/`clear` as built-ins on p.45 and p.55: on p.55 the `max` is the third index of the full slice `a[low:high:max]`, not the built-in.
- Go 1.14: the body marks the embedding of interfaces (p.21); the appendix describes the effect (p.115).

### 6.2 NOT stated by the Spec

- `[...]T` in a composite literal (Spec p.45) and full slice `a[low:high:max]` (p.55).
- `new(expr)` with an expression (p.104): absent from the appendix, which ends at Go 1.24 (p.116). A hint from another source in the set (Effective Go p.15): `new` with an expression "as of Go 1.26". This does not come from the Spec; it is a hint, not a rule.
- `panic(nil)` as a run-time panic (p.105); package initialization by import order (p.111).
- Definition of "strictly comparable" (p.69–70); only the 1.20 consequence is in the appendix (p.116).
- Inference with a generic function passed, assigned or returned: the body (p.59) marks no version; the appendix attributes part to 1.21 (p.116).
- Any novelty in the body later than Go 1.24: the appendix stops at 1.24 although the Spec is go1.26 (p.115–116). Treat as version not stated.

## 7. Source limitations and dated content

- Version: the Spec is go1.26; the supporting release notes go from 1.20 to 1.24, and the version appendix also only reaches 1.24. For 1.25 and 1.26 features, the body may describe without recording a version; do not assume the version.
- Uneven coverage of the notes: parts that the map treated as "detailed" (`go`, `select`, `defer`, most built-ins, `recover`, initialization dependency rules, size and alignment tables) have little or no content in the notes and were not reconstructed here. `if` (p.83) and unification (p.116–117) were only mapped. The pages in section 2 say where to read the Spec.
- PDF extraction: the text came without indentation and the pagination is that of the extracted file; code examples and Unicode characters may have been lost (a case in another source: Little p.69). Check critical passages in the original Spec.
- Review heuristics (for example "flag as a defect") are guidance from the notes, not a Spec requirement.
- The Spec defines the language, not style: it does not teach safe concurrency, the standard library (`fmt`, `errors`, `sync`, `context`), modules, tests or best practices. `utf8.AppendRune`, `utf8.EncodeRune` and `go vet` (p.75) are isolated mentions.
- Other sources in the set: Effective Go declares itself written for the 2009 release and not actively updated, without generics, modules and new libraries (Eff p.1); the Little book shows `go1.3.3` and the GOPATH model, predating modules (Little p.10–12, p.53–57). They must not override the Spec on modern language rules.
