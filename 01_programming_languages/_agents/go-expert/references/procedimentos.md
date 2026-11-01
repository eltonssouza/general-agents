# Go review procedures and checklists

Reference base for the Go specialist agent. Sources: Effective Go (Eff), Spec go1.26 (Spec), The Little Go Book (Little, go1.3.3/GOPATH) and release notes 1.20–1.24 (RN). Each procedure gives: when to use, steps, how to verify, pitfalls and source. Steps marked **[DATED]** depend on GOPATH or on old tools/versions and do not represent current practice. Links marked [inference] are mine, not from the source text.

## Contents

1. Formatting and comments
2. Names and exports
3. Declarations and scope
4. Functions and receivers
5. Slices and maps
6. Interfaces and embedding
7. Errors, defer and panic
8. Concurrency
9. Strings, bytes and runes
10. Packages, build and tools
11. Consolidated review checklist
12. Known gaps

---

## 1. Formatting and comments

### P1.1 Format the code
**When to use:** before any review or commit.
1. Run the project's formatter (`go fmt ./...`); it indents, aligns fields and sorts imports alphabetically (Little p.66).
2. Do not align anything by hand and use tabs for indentation (Eff p.2–3).
3. Check that the opening brace stays on the same line as the statement (Eff p.5–6).

**Verify:** a second run of the formatter changes nothing [inference].
**Pitfalls:** treating formatting as a style debate; Little describes it as authoritative to avoid arguments (Little p.66). Breaking the opening brace onto a new line changes the meaning of the code in control statements (Eff p.5–6).
**Source:** Eff p.2–3, p.5–6; Little p.66.

### P1.2 Documentation comments
Effective Go says little about comments, and this was checked against the source text: Go accepts line comments (`//`, the norm) and block comments (`/* */`, used mainly as package comments, inside expressions or to disable large chunks); a comment immediately before a top-level declaration, with no blank line in between, documents that declaration and is the primary documentation of the package or command (Eff p.3). For the writing conventions of doc comments the document refers to "Go Doc Comments", which is **not in the sources**: do not invent style rules (start of the sentence, lists, links); say that the detailed convention is outside the material. Offline reading of documentation: see P10.4 (**[DATED]**). See section 12.

---

## 2. Names and exports

### P2.1 Review package, symbol and method names
**When to use:** when creating a package or exported API, or when reviewing names.
1. Package: lowercase, short, no `_` or mixedCaps (Eff p.4).
2. Exported symbols do not repeat the package name, since the caller already writes it as a prefix (Eff p.4).
3. Getter without a `Get` prefix; a one-method interface takes the suffix `-er` (Eff p.4–5).
4. If the method has a canonical name (for example `String`), the signature must be the canonical one (Eff p.4–5).
5. Multi-word names in MixedCaps or mixedCaps, without underscores (Eff p.5).

**Verify:** read the calls as the package user would write them and look for stutter in the name [inference].
**Pitfalls:** a name with a signature different from the canonical one misleads anyone who expects the standard interface (Eff p.4–5).
**Source:** Eff p.4–5.

---

## 3. Declarations and scope

### P3.1 Detect shadowing with `:=`
**When to use:** `:=` inside `if`, `for`, `switch` or a clause, reusing a name that already exists outside.
1. List the variables on the left side; in an inner block, every new name becomes a new variable (Spec p.30–31, p.40).
2. If the intent was to assign to the outer variable, switch to `=` or declare it beforehand.
3. In a function with a named result and a bare return, check whether a shadowed `err` prevents compilation (Spec p.95).

**Verify:** compile and run the project's shadowing analyzer, if one exists [inference].
**Pitfalls:** the error "disappearing" in the inner block while the outer variable stays nil.
**Source:** Spec p.30–31, p.40, p.95.

### P3.2 Numeric types, constants and `iota`
1. Numeric types are distinct: mixing `int`, `int64`, `uint` requires explicit conversion (Spec p.14).
2. Untyped constants get around this when representable (Spec p.28).
3. With `iota`, skips, `_` and implicit lines: confirm that the implicit repetition of the last list is intentional (Spec p.33–34).
4. The width of `int` changes shifts; do not assume 32 or 64 bits (Spec p.64). Guaranteed sizes only hold for fixed-width types (Spec p.114).

**Source:** Spec p.14, p.28, p.33–34, p.64, p.114.

### P3.3 Type definition versus alias
1. `type X Y` creates a new type and does not inherit methods from Y (Spec p.35).
2. If the intent is merely another name for the same type, use an alias (Spec p.34).
3. Structs with different tags are distinct types for identity (Spec p.17, p.27); the conversion rule is in Spec (block 2 of the source).

**Source:** Spec p.17, p.27, p.34–35.

### P3.4 Package initialization order
**When to use:** package variables that depend on one another, or several `init`.
1. Package variables: at each step the first one, in declaration order, that does not depend on an uninitialized variable is initialized. The dependency is transitive and lexical within the package; a cycle makes the program invalid (Spec p.109).
2. Example from the text: with `a = c + b`, `b = f()`, `c = f()`, `d = 3` and `f` incrementing `d`, the order is d, b, c, a (Spec p.110).
3. `init` may appear several times, with no parameters or results; it runs after the package variables, in source order (Spec p.110–111).
4. Imports are initialized before the importer, only once (Spec p.111).
5. Everything runs in one goroutine; an `init` may launch goroutines, but the next one only starts when the previous returns (Spec p.111).

**Pitfalls:** a dependency hidden behind an interface has unspecified order (Spec p.110). Ordering criterion among packages: version not stated in the text (Spec p.111).
**Source:** Spec p.109–111.

### P3.5 Captured loop variable
1. With per-iteration semantics [Go 1.22], each iteration has its own variable (Spec p.88).
2. The text ties the behavior to the language version (Spec p.115). Before removing `i := i` copies, check the `go` directive in the project's `go.mod` (the file is not in this text).
3. If the body changes the control variable, the next copy inherits the value at the moment of the post statement (Spec p.88).

**Source:** Spec p.88, p.115.

---

## 4. Functions and receivers

### P4.1 Choose the receiver
1. Pointer receiver where there is mutation (Eff p.29).
2. If the type will be used as an interface, compare the method set: T does not include the methods of *T (Eff p.29; Spec p.29, p.50).
3. If a struct embeds `T` and the interface requires a method of `*T`, only `*S` satisfies it; `S` by value does not (Spec p.17).

**Verify:** try assigning the value to the target interface; the compiler reports the missing method [inference].
**Source:** Eff p.29; Spec p.17, p.29, p.50.

### P4.2 Design a type with a useful zero value
1. Compose fields whose zero value already works (`sync.Mutex`, `bytes.Buffer`) (Eff p.15–16).
2. Avoid a mandatory `Init` method; if necessary, offer a constructor (Eff p.15–16).
3. Allocation: `make` for slice, map and channel; `new` or `&T{}` for the rest; do not use `new([]int)` (Eff p.17).

**Source:** Eff p.15–17.

### P4.3 Method values, variadics and literals
1. `obj.Method` stored in a callback, `defer` or goroutine: the receiver was evaluated and copied at creation (Spec p.50–51).
2. `f(s...)` passes the slice without copying; the variadic function can change the caller's array (Spec p.58).
3. A struct literal without keys is fragile to field changes; from another package with unexported fields it does not even compile (Spec p.44).
4. Function without a final `return`: the last statement must be terminating (Spec p.78–79).
5. Expression that reads a variable and calls a function that modifies it: order unspecified (Spec p.78).

**Source:** Spec p.44, p.50–51, p.58, p.78–79.

### P4.4 Generics
1. `==` on T requires the `comparable` constraint or comparable terms; if T can be an interface, the comparison may panic (Spec p.38–39, p.69, p.116).
2. An interface with type elements or `comparable` does not work as the type of a variable, field or parameter; only as a constraint (Spec p.23, p.38).
3. A method does not accept type parameters; use a generic function (Spec p.41–42).
4. Numeric literal in generic code: `P(1.1)` is not a constant and is computed at the argument's precision (Spec p.72).

**Source:** Spec p.23, p.38–42, p.69, p.72, p.116.

---

## 5. Slices and maps

### P5.1 Create and grow slices
1. `make([]T, n)` gives len = cap = n; if `append` follows, the result has `n` zeros before the appended values and, in general, the intent was `make([]T, 0, n)` [inference: Spec p.102 only gives len and cap of `make`; the effect with `append` appears in Little p.43]. Constant sizes: non-negative, representable as int, `n <= m`; `make([]int, 1e3)` is valid (Spec p.102–103).
2. Assign the result of `append` back; as a standalone statement it does not compile (Eff p.26; Spec p.80). If there is capacity, it reuses the array, otherwise it allocates a new one (Spec p.98).
3. `append([]byte, string...)` and `copy([]byte, string)` accept a string; `copy` copies the minimum of the sizes and returns that number (Spec p.98–99).

**Verify:** check the return value of `copy` when the destination may be smaller.
**Source:** Eff p.26; Spec p.80, p.98–99, p.102–103.

### P5.2 Avoid sub-slice aliasing
1. In `b := a[i:j]`, `append` or a write to `b` may overwrite `a` (Spec p.55).
2. To limit capacity, use `a[i:j:j]` (Spec p.55).
3. `s[:n]` with n > len(s) is valid up to cap(s); review whether it exposes old data (Spec p.54).
4. `[N]T(s)` and `(*[N]T)(s)` panic if `len(s) < N` (Spec p.75).

**Pitfalls:** `append(s[:i], ...)` overwrites elements of `s` after `i` when there is capacity (Spec p.98).
**Source:** Spec p.54–55, p.75, p.98.

### P5.3 Use maps safely
1. Nil map: reading and `len` are safe; writing panics (Spec p.24, p.53). Initialize with `make`.
2. When "absent" differs from "zero", use comma-ok (Eff p.21).
3. `any` key or struct with an interface field: the dynamic values must be comparable (Spec p.24).
4. `delete` is a no-op for a nil map or absent key (Spec p.101).
5. Range over a map: do not depend on order or on visibility of insertions; removing an entry not yet reached is safe (Spec p.89).
6. Concurrency: the Spec block only states safe use without synchronization for channels (Spec p.25); nothing was said about maps. Do not claim safety based on it.

**Source:** Eff p.21; Spec p.24–25, p.53, p.89, p.101.

### P5.4 Recent built-ins
- `clear` [Go 1.21]: empties a map; zeroes a slice up to `len`; nil is a no-op (Spec p.99).
- `min`/`max` [Go 1.21]: at least one argument; `min(s...)` is invalid; NaN contaminates the result; `-0.0 < 0.0`; strings compare bytewise (Spec p.103–104).
- `new(expr)`: accepts an expression, but the **version is not stated** and the appendix (up to 1.24) does not list it (Spec p.104, p.115–116). Do not use in code that must compile on versions 1.20–1.24 without checking.
- Built-ins are not function values; `complex`, `real` and `imag` do not accept a type parameter (Spec p.98, p.101).

**Source:** Spec p.98–104, p.115–116.

---

## 6. Interfaces and embedding

### P6.1 Avoid a non-nil interface holding a nil value
**When to use:** a function returns `error` (or another interface) and there is a nil concrete pointer nearby.
Two layers, so as not to mix what the text says with what is deduced from it:

**(a) [from source]**
1. An interface variable has a static type and a dynamic type; the dynamic one is that of the value assigned at run time, except if the value is the predeclared `nil`, which has no type (Spec p.12).
2. The Spec example: after `x = v`, with `v` of type `*T` and value nil, `x` has value `(*T)(nil)` and dynamic type `*T` (Spec p.12).
3. Two interfaces are equal if they have identical dynamic types and equal dynamic values, or if both have the value nil (Spec p.69).

**(b) [inference]** (no source describes the trap, and Effective Go does not cover it)
4. Combining (a): an interface holding `(*T)(nil)` has dynamic type `*T`, so it is not the nil interface and `x != nil` is true. This conclusion and its practical danger (a function returning `error` with a nil pointer inside) are my deduction.
5. Return a literal `nil` when there is no error, instead of a concrete pointer variable.

**Verify:** compare the function's result with `nil` in a test [inference].
**Source:** Spec p.12, p.69 (a); the rest is [inference]. See also `regras-da-spec.md` §3.6.

### P6.2 Embedding
1. Two embedded types that promote the same name at the same depth produce an ambiguous selector, an error if used (Spec p.48).
2. See P4.1 step 3 for the effect of a pointer receiver on an embedded type.

**Source:** Spec p.17, p.48.

### P6.3 Assertions, switches and comparison
1. Single-form `x.(T)` only when a crash is acceptable; otherwise `v, ok :=` (Eff p.32; Spec p.56).
2. Type switch with several types in one `case`: the variable keeps the interface's type (Spec p.85).
3. `==` on `any` or `error` with a slice, map or function dynamic value panics (Spec p.69).
4. Do not use a `struct{}` pointer as identity; zero-size variables may share an address (Spec p.69, p.114).
5. A `String` method must not format its own receiver with `%s` or `%v` of the same type, to avoid infinite recursion (Eff p.24).

**Source:** Eff p.24, p.32; Spec p.56, p.69, p.85, p.114.

---

## 7. Errors, defer and panic

### P7.1 Handle errors
1. `error` is the interface with `Error() string`; nil indicates absence (Spec p.111).
2. Check every error return; discarding with `_` requires a reason (Eff p.36).
3. The error path returns early, without an unnecessary `else` (Eff p.6–7).
4. End of reading is signaled by `io.EOF`, a package variable created with `errors.New("EOF")`; compare with `err == io.EOF` (Little p.64; use in a read loop in Eff p.13). Any other error is returned to the caller (Eff p.13).

**Source:** Eff p.6–7, p.13, p.36; Little p.64; Spec p.111.

### P7.2 Use `defer` with resources
**When to use:** any resource that must be closed or released.
1. Open the resource and check `err` first (Little p.65).
2. Call `defer resource.Close()` immediately after the check; multiple `return`s are covered (Little p.65; Eff p.13).
3. In a loop, `defer` runs only at the end of the function (Spec p.97: deferred calls run before the function returns) and accumulates; extracting the body into its own function is [inference].
4. `defer f(x)` evaluates `x` at the moment of the `defer`; use a closure to see the final value (Spec p.97).
5. Changing the returned error in a defer requires a named result (Spec p.97–98).

**Reading example (Eff p.13, `Contents`):** open with `os.Open`, return the error if any, `defer f.Close()`, and read in a loop with `n, err := f.Read(buf[0:])`. On each pass, append what was read with `append(result, buf[0:n]...)` (only the `n` bytes read) before looking at `err`; if `err == io.EOF`, `break`; any other error, `return "", err`, and the file is closed on that return. `Read` returns the count and the error; the slice's size limits how much is read, and `f.Read(buf[0:32])` reads into the first 32 bytes (Eff p.18).

**Advantages of `defer Close()` that the sources cite:**
- It stays close to the opening: the release is written next to where the resource is born, which is clearer than leaving it at the end of the function (Eff p.13; Little p.65).
- It covers every `return`: the deferred function runs immediately before the enclosing one returns, by `return`, end of body or panic (Spec p.97); Little mentions the multiple return points and "violent" termination (Little p.65).
- It is not forgotten when editing: Effective Go says it guarantees you never forget to close, an easy mistake when adding a new return path (Eff p.13); Little points out how easy it is to forget the `Close` of something declared ten lines above (Little p.65).

**Source:** Eff p.13, p.18; Little p.65; Spec p.97–98.

### P7.3 Convert an internal panic into `error`
**General rule before the recipe:**
- Returning `error` as an extra return value is the usual way to report failure to the caller; the canonical `Read` returns a count and an error (Eff p.49).
- `panic` is for the unrecoverable and the "impossible" (the example is a loop that does not converge); library functions should avoid it, because if the problem can be worked around, it is better to let the program continue (Eff p.49–50). Acceptable counterexample: initialization failure, where the library cannot configure itself (Eff p.50).
- Little says that `panic` and `recover` exist, are equivalent to throwing and catching an exception, and are rarely used (Little p.64).

**When to use the recipe:** parser or deep recursive code where propagating the error manually pollutes the code; the public API must keep returning `error`.
1. Define an error type local to the package (Eff p.51–52).
2. Create a helper that does `panic(Error(msg))` (Eff p.51–52).
3. In the public function, `defer` with `recover` that converts the value to `error` and re-panics if it is not the local type (Eff p.51–52).
4. `recover` only works if called directly by the deferred function (Spec p.105).

**Verify:** no panic escapes the public API (Eff p.52).
**Pitfalls:** swallowing panics of other types hides real bugs [inference].
**Source:** Eff p.49–52; Little p.64; Spec p.105.

---

## 8. Concurrency

### P8.1 Review checklist
1. Is any variable written by more than one goroutine? If so, protect it with a mutex or switch to passing via a channel (Little p.74, p.77).
2. Reader/writer pattern: consider `RWMutex` (Little p.76).
3. `defer lock.Unlock()` right after `Lock()` (Little p.75).
4. Is there a way to know that each goroutine has finished? Is their number bounded? (Eff p.43–45).
5. Do not use `time.Sleep` to wait for goroutines; Little marks it as bad and uses it only in examples (Little p.73, p.76).
6. Define the overload policy: block, buffer, drop or timeout (Little p.79–81).

**Source:** Eff p.43–45; Little p.73–81.

### P8.2 Limit concurrency (two variants)
**When to use:** requests arrive faster than the supported processing.
- Variant (a): buffered channel of size `MaxOutstanding` as a semaphore; acquire BEFORE launching the goroutine (Eff p.44–45).
- Variant (b): fixed pool of goroutines consuming a single channel (Eff p.44–45).

**Verify:** there are never more than the limit running simultaneously [inference].
**Pitfalls:** acquiring the semaphore inside the already launched goroutine does not limit the number of goroutines created [inference from "BEFORE"].
**Source:** Eff p.44–45.

### P8.3 Parallelize an operation over a vector
1. Split into independent parts.
2. One goroutine per part, signaling on a buffered channel when done.
3. Drain N signals; only then consider the work complete (Eff p.46).

**Source:** Eff p.46.

### P8.4 Channels and control
1. Only the use of channels (send, receive, cap, len) is stated to be safe without synchronization (Spec p.25).
2. Direction `<-chan T` or `chan<- T` can only be restricted, never widened (Spec p.25, p.28).
3. `break` inside a `switch` or `select` in a loop exits only them; to exit the loop use a label (Spec p.95).
4. Iterator [Go 1.23]: test the return value of `yield` and stop when false (Spec p.89–90).

**Source:** Spec p.25, p.28, p.89–90, p.95.

---

## 9. Strings, bytes and runes

### P9.1 Handle text correctly
1. `len(s)` and `s[i]` on a string count bytes, not characters (Spec p.14, p.53, p.101).
2. To iterate over characters, `range` over a string: index in bytes, value is a rune, an invalid sequence becomes U+FFFD (Spec p.89).
3. Hex and octal escapes in literals are bytes; code point escapes are UTF-8 (Spec p.10).
4. `string(i)` with an integer is suspect; use `strconv.Itoa` or equivalent (Spec p.75).
5. `unsafe.String` and `unsafe.StringData` [Go 1.20]: do not modify the bytes afterwards, since strings are immutable (Spec p.114).

**Verify:** test with multibyte input and with invalid UTF-8 [inference].
**Source:** Spec p.10, p.14, p.53, p.75, p.89, p.101, p.114.

---

## 10. Packages, build and tools

### P10.1 Run and compile
1. Development: `go run main.go` compiles in a temporary directory, runs and cleans up; `go run --work` shows the directory (Little p.19).
2. Deployment: `go build` and distribute the binary (Little p.19).
3. Without `package main` and a `main` function, `go build` compiles (useful for libraries) but `go run` fails for lack of an entry point (Little p.19–20).
4. `main` has no parameters or results; the program exits when it returns (Spec p.111).

**Pitfalls:** Little is go1.3.3; flags and behavior may have changed, check against the version in use [inference].
**Source:** Little p.19–20; Spec p.111.

### P10.2 Break a cyclic import
1. Identify the shared type that causes the cycle.
2. Move it to a new package (example from the text: `shopping/models`).
3. The two original packages import the new one; it imports neither of them (Little p.55–56).

**Verify:** the compiler stops reporting a cycle [inference].
**Source:** Little p.55–56.

### P10.3 **[DATED]** Dependencies in the GOPATH model
Do not present as current practice.
1. `go get <path>` downloads into `$GOPATH/src` (Little p.56).
2. `go get` inside a project scans imports and downloads what is missing; `go get -u` updates (Little p.57).

**Pitfalls:** Little does not cover modules or `go.mod`; do not use this flow as the basis for current projects.
**Source:** Little p.56–57.

### P10.4 **[DATED]** Offline documentation with `godoc`
1. `godoc -http=:6060` and open `localhost:6060` (Little p.22).
2. Tool cited by a go1.3.3 book; confirm it exists in the current installation before recommending it.

**Source:** Little p.22.

### P10.5 Review use of `unsafe`
1. Every package using `unsafe` needs manual type checking and may not be portable (Spec p.112).
2. `unsafe.Pointer` cannot be dereferenced; Pointer/`uintptr` conversions have implementation-defined effect (Spec p.112).
3. `unsafe.Add` and `unsafe.Slice` [Go 1.17]; `unsafe.SliceData` [Go 1.20]. `Slice(ptr, len)` is equivalent to conversion to an array and slicing, except that a nil ptr with len 0 returns nil (Spec p.113–114).
4. `Sizeof`, `Alignof` and `Offsetof` are `uintptr` constants for constant-size types; type parameters have variable size. `Offsetof` requires a selector `s.f` (Spec p.113).
5. Layout and padding beyond the alignment relations (minimum 1; struct = largest of the fields; array = element) are not guaranteed in the text (Spec p.113–114).
6. The rules for valid use of `Pointer` are not in this text; do not claim anything beyond them.

**Source:** Spec p.112–114.

---

## 11. Consolidated review checklist

Merged from the Eff and Spec lists; each item points to the procedure that details it.

1. Formatted by gofmt, tabs, brace on the same line (P1.1).
2. Package and symbol names without repetition, without `Get`, with `-er` (P2.1).
3. No accidental shadowing with `:=` (P3.1).
4. Explicit numeric conversions; `iota` intentional (P3.2).
5. Defined type versus alias chosen on purpose (P3.3).
6. Initialization order without hidden dependency (P3.4).
7. Loop variable capture checked against the module version (P3.5).
8. Receiver and method set consistent with the interfaces (P4.1).
9. Useful zero value; `make` and `new` used correctly (P4.2).
10. Generics: adequate constraint, no generic method (P4.4).
11. `append` assigned back; sub-slice aliasing handled (P5.1, P5.2).
12. Maps: nil, comma-ok, range order and concurrency (P5.3).
13. No non-nil interface holding a nil value (P6.1).
14. Type assertions with comma-ok; `String` without recursion (P6.3).
15. Errors checked; early return (P7.1).
16. Resources closed with `defer` close to acquisition (P7.2).
17. Public package does not expose panic (P7.3).
18. Goroutines with known termination and bounded number; shared data protected (P8.1, P8.2).
19. Text handled as bytes and runes consciously (P9.1).
20. No cyclic import; GOPATH and `godoc` steps treated as **[DATED]** (P10.2–P10.4).

---

## 12. Known gaps

- Documentation comments: Effective Go only describes the basics and refers to "Go Doc Comments", which is not in the sources (Eff p.3; P1.2).
- Modules and `go.mod`: not covered by Little (GOPATH); the module version affects loop semantics (P3.5).
- `new(expr)` and the package initialization ordering criterion: version not stated in the text (P5.4, P3.4).
- Map safety under concurrency: not stated by the Spec block used (P5.3).
- Rules for valid use of `unsafe.Pointer`: absent from the text (P10.5).
