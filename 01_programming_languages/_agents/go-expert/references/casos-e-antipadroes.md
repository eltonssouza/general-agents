# Go cases and anti-patterns

Reference base derived from three sources: **Eff** (Effective Go, 2009), **Little** (The Little Go Book, go1.3.3, GOPATH era) and **Spec** (Spec go1.26). Citations use the format (Eff p.N) or (Little p.N). A few lines cite the Spec (§2.3, §2.4, §2.6); all were checked against the Spec text. For the formal rules of the language, the reference is `regras-da-spec.md`.

## Contents

1. [How to read this document](#1-how-to-read-this-document)
2. [Tables of anti-patterns and pitfalls by topic](#2-tables-of-anti-patterns-and-pitfalls-by-topic)
   - 2.1 Slices, append and aliasing
   - 2.2 Maps
   - 2.3 Pointers, copies and receivers
   - 2.4 Interfaces and type assertions
   - 2.5 Errors, defer, panic
   - 2.6 Concurrency and data races
   - 2.7 Strings and runes
   - 2.8 Scope and shadowing
   - 2.9 Conventions, names and package organization
   - 2.10 Compilation and tooling
3. [Illustrative cases](#3-illustrative-cases)
   - 3.1 Effective Go
   - 3.2 The Little Go Book
4. [Gaps and warnings](#4-gaps-and-warnings)

## 1. How to read this document

- **Source** says where the claim comes from; **era** says the age of the source: Eff = 2009, Little = go1.3.3 (GOPATH).
- **[DATED]** marks what depends on old Go. When the entry itself says a newer version changes the conclusion (the case of the loop variable before Go 1.22), that is stated. Anywhere else I propose a modern caveat, it comes as **[inference]** and must be checked against the Spec before being treated as fact.
- Compiler error messages appear only when the sources carry them: "no new variables on left side of :=", "import cycle not allowed" and "Item undefined".
- The code snippets are minimal and rewritten; they are not copies of the sources.

## 2. Tables of anti-patterns and pitfalls by topic

### 2.1 Slices, append and aliasing

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| The caller's slice does not grow after calling a function that does `append` | The slice descriptor is passed by value; the result of `append` must be assigned | Always use `s = append(s, x)`; `Append`-style functions return the slice | Eff p.19, 26; Little p.43 | Eff 2009 / Little go1.3.3 (structural rule, not dated) |
| `make([]int, 5)` followed by `append(..., 9332)` gives five zeros and then the value | `make` with `n` creates `n` already-existing elements; `append` puts after them | Use `make([]int, 0, 5)` if the intent is capacity, not length | Little p.43 | go1.3.3 |
| Panic when indexing a slice created with `make([]int, 0, 10)` and `scores[7] = x` | The indexing bound is `len`, not `cap` | Reslice (`scores[0:8]`) or `append` | Little p.42 | go1.3.3 |
| Changing `sub[0]` changes the original array/slice | A subslice is a window onto the same array, not a copy | Use `copy` for an independent destination | Little p.44–46 | go1.3.3 |
| In a 2D matrix, a row that grows overwrites its neighbor | Rows allocated in a single shared block | Allocate row by row if the rows can grow (trade-off of two allocations) | Eff p.20 | 2009 |
| A function that receives an array does not change the caller's array | Arrays are values; the function receives a copy | Pass a slice (or a pointer to an array) | Eff p.17–18 | 2009 |
| Passing a slice to a variadic function becomes a single argument; `append(a, b)` with `b` a slice does not compile | Missing `...` | Write `f(s...)` / `append(a, b...)` | Eff p.25–26 | 2009 |
| Negative index on a slice does not work | Go offers no negative indices | Use `len(s)-1` | Little p.45 | go1.3.3 |
| Belief that `[]*T` is cheaper to pass than `[]T` | Passing the slice costs the same in both cases | Choose the type by element semantics, not by that cost | Little p.49 | go1.3.3 |
| Whoever reads the growth rule "doubles at each overflow" treats it as a contract | The book describes 10, 20, 40 from an initial cap of 5 | **[DATED]** treat the factor as an implementation detail; do not program counting on it. **[inference]**: confirm in the current Spec/runtime | Little p.43 | go1.3.3, **[DATED]** |

### 2.2 Maps

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| Different result on each run when iterating a map | Iteration order is random | Do not depend on order; sort the keys if needed | Little p.48 | go1.3.3 |
| A slice cannot be used as a map key | Slices have no equality | Use a comparable type (string, array, comparable struct) | Eff p.20 | 2009 |
| Map field in a struct not used correctly | The map needs `make` before use; the book shows the literal with `make(map[string]*Saiyan)` | Initialize in the constructor/literal. The consequence of not initializing is not described in the book | Little p.47 | go1.3.3 |
| Cannot tell whether the key exists: `lookup["x"]` returns zero | The zero value is ambiguous | Comma-ok form: `v, ok := m[k]` (returns `0, false` in the example) | Little p.47; Eff p.21–22 | both |
| Need for a set | Go has no set type | Use `map[string]bool` and `delete` | Eff p.21–22 | 2009 |

### 2.3 Pointers, copies and receivers

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| `Super(goku)` prints 9000 instead of 19000 | The function changes the copy of the struct | Receive `*Saiyan` and pass `&goku` | Little p.29–30 | go1.3.3 |
| Reassigning the pointer inside the function does not change the caller's | The address is also passed by copy | Change what is pointed to (`*p = ...`) or return the new pointer | Little p.30 | go1.3.3 |
| A `T` value does not satisfy an interface whose methods have a `*T` receiver | The method set of `T` does not include those of `*T` | Pass `&b`; declare a pointer receiver consciously | Eff p.28–29 | 2009 |
| Calling a pointer method on a non-addressable value is forbidden | There is no address to take; Eff says the language forbids the error because the method would receive a copy and the modifications would be lost | Assign to a variable first or use a pointer | Eff p.29 | 2009 |
| `makeT().Mp` (method value of a pointer method on a function result) does not compile | The result of `makeT()` is not addressable; the Spec marks that line as invalid | Store the result in a variable (`t := makeT()`) and use `t.Mp`, equivalent to `(&t).Mp` | Spec p.52 | Spec go1.26 |
| For a **call** (`x.m()`), the shortcut only holds with `x` addressable | The Spec defines `x.m()` as shorthand for `(&x).m()` if `x` is addressable and the method set of `&x` contains `m`; the non-addressable case is not described with an error message in that passage, and the conclusion that the call is invalid comes from Eff p.29 and is [inference] as far as the Spec is concerned | Same fix: intermediate variable or pointer | Spec p.57–58; Eff p.29 | Spec go1.26 / 2009 |
| Struct with a lock/buffer field unusable without initialization | The zero value was not designed | Design the zero value to be useful (`SyncedBuffer`) | Eff p.15 | 2009 |

### 2.4 Interfaces and type assertions

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| Runtime crash on `x.(T)` | The dynamic value is not `T` | Use comma-ok: `t, ok := x.(T)` | Eff p.32; Little p.68 | both |
| `a.(int)` fails at run time | The underlying type is not int | Check the type or avoid the empty interface | Little p.68 | go1.3.3 |
| Code with `interface{}` "ugly and dangerous" (author's opinion) | Loss of static typing | Prefer interfaces with behavior; use the empty one only when it is the only option | Little p.68 | go1.3.3 (**[DATED]** as to the absence of generics; **[inference]** that modern generics change part of the conclusion) |
| `json.Marshal` ignores the custom `Marshaler` implementation | The type does not satisfy the interface by mistake (signature/receiver); the check only happens at run time | Compile-time assertion: `var _ json.Marshaler = (*RawMessage)(nil)` | Eff p.39 | 2009 |
| Many `var _ Iface = ...` declarations | Excess of redundant checks | Use only when no equivalent static conversion exists | Eff p.39 | 2009 |
| Concrete type exposed unnecessarily | API coupled to the implementation | Return the interface (`hash.Hash32`, `cipher.Stream`) and hide the type | Eff p.33 | 2009 |
| Looking for function overloading | There is no overloading | Distinct names | Little p.36 | go1.3.3 |

Note: the classic pitfall "an interface holding a nil pointer is not nil" is **not** in the sources as a pitfall (Effective Go does not cover it). What the Spec offers is the example of dynamic type `*T` with a nil value (Spec p.12) and the interface equality rule (Spec p.69); the pitfall is a deduction [inference] from those two passages. See `procedimentos.md` P6.1 and `regras-da-spec.md` §3.6.

### 2.5 Errors, defer, panic

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| Crash when using `fi` after `fi, _ := os.Stat(path)` with a nonexistent path | Error discarded with `_`; the text calls the practice "terrible practice" | Always check `err` | Eff p.36 | 2009 |
| Missing `err != nil` check | Forgetting the standard model | Check right after the call that can fail | Little p.63 | go1.3.3 |
| `defer file.Close()` before checking the open error | Defer registered on an invalid resource | Check `err` and return before the `defer` | Little p.65 | go1.3.3 |
| Resource does not close on some path | Scattered manual closing | `defer f.Close()` next to the open | Eff p.13 | 2009 |
| Defer prints/uses the "wrong" value | Defer arguments are evaluated at defer time | Understand the `trace`/`un` pattern | Eff p.14 | 2009 |
| Panic crosses the library boundary to the client | Panic used as internal error control without translation | `recover` at the package boundary and convert to `error` | Eff p.52 | 2009 |
| Library panics on a recoverable error | Overuse of panic | Prefer continuing/returning an error | Eff p.50 | 2009 |
| Hard to inspect the cause of the error | Opaque error | Structured error (`os.PathError`) and type assertion; sentinel `io.EOF` with `==` | Eff p.48–49; Little p.64 | both |
| Variable from the `if` init does not exist afterwards | Scope limited to `if/else if/else` | Declare before if you need it outside | Little p.67 | go1.3.3 |

### 2.6 Concurrency and data races

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| Loop goroutines use the same value of the loop variable | Shared loop variable; the text warns that the example has a bug in Go before 1.22 | Pass the variable as a closure argument or copy it locally (classic fix, **[inference]**); the note restricts the bug to versions before 1.22, that is, in new versions the conclusion changes | Eff p.44 | **[DATED]** (Go < 1.22; the note itself cites the change) |
| `counter++` in several goroutines gives repeated, missing, out-of-order values, and possibly worse | `++` becomes several machine instructions; data race | Mutex (`Lock` + `defer Unlock`) or `atomic` | Little p.74–75; Eff p.34 | both |
| The handler's `Counter` example is not concurrency-safe | Shared state without protection | `sync`/`atomic` | Eff p.34 | 2009 |
| Program ends before the goroutines | The Spec defines that the program exits when `main` returns and that this does not wait for the other goroutines; Little shows the effect (the process exits before the goroutine runs) | Synchronize via a channel or a wait tool | Spec p.111 (primary source); Little p.73 | Spec go1.26 / go1.3.3 |
| `time.Sleep` to wait for goroutines | Too little time (not finished) or too much (waste); the Little example carries a comment that this is bad and should not be done | Explicit synchronization; the example exists only to show that `main` exits without waiting (Spec p.111) | Little p.73 (example with `time.Sleep`), p.76 (argument); Spec p.111 | go1.3.3 / Spec go1.26 |
| Deadlock from forgetting `Unlock` | Lock never released, even with a single lock | `defer lock.Unlock()` right after `Lock` | Little p.75–76 | go1.3.3 |
| Coarse locks or two locks in opposite order | Parallelism is lost; opposite order causes hard-to-see deadlock | Fine-grained locks and consistent order | Little p.75 | go1.3.3 |
| Sender blocks with an unbuffered channel and slow workers | No receiver ready | A buffer only postpones; if input exceeds capacity, it blocks again. Alternative: drop with `select/default` | Little p.79–80 | go1.3.3 |
| `select` with `default` + `time.After`: the timeout never applies | `default` fires immediately if no channel is ready | Remove the `default` when you want to wait | Little p.81 | go1.3.3 |
| Goroutine per request without a limit consumes resources without a ceiling | Unbounded creation under load | Semaphore with a channel or a fixed worker pool | Eff p.44–45 | 2009 |
| Overdoing "share by communicating" | Reference counting is simpler with a mutex | Use a mutex where it is clearer | Eff p.42 | 2009 |
| Thinking concurrency is parallelism | Distinct concepts | Separate structure (concurrency) from simultaneous execution | Eff p.47 | 2009 |
| `go func(){...}` without `()` | The function literal must be called | Write `go func(){...}()` | Eff p.43 | 2009 |

### 2.7 Strings and runes

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| `len` of a string with one Unicode character returns 3 | `len` counts bytes | Count runes when you need characters | Little p.69 | go1.3.3 |
| Indexing/iterating expects characters and gets bytes | `range` yields runes; conversion to `[]byte` exposes bytes | Consciously choose `range` (runes) or `[]byte` (bytes) | Little p.69 | go1.3.3 |
| Copy cost when converting | `[]byte(x)` and `string(x)` copy, because strings are immutable | Avoid conversions in hot loops | Little p.69 | go1.3.3 |
| Looking for "indexOf with a start" | No equivalent API | `strings.Index(haystack[5:], " ")` | Little p.45 | go1.3.3 |
| Recursive `String()` when formatting the type itself | `Sprintf("%s", m)` calls `String` again | Convert to the base type (`string(m)`) or use a verb that does not ask for a string | Eff p.24, 27 | 2009 |

### 2.8 Scope and shadowing

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| Error "no new variables on left side of :=" | `:=` redeclares in the same scope without a new variable | Use `=` the second time; beware the muscle memory of alternating | Little p.23–24 | go1.3.3 |
| Outer variable does not change; there is a shadowed copy | `:=` in an inner scope creates a new variable | Use `=` or declare outside; remember that parameters and results share the body's scope | Eff p.7–8 | 2009 |
| Multiple `:=` does not change the type | `power` inferred as int only accepts integers afterwards | Declare with the right type from the start | Little p.24 | go1.3.3 |
| `err` reused in an `os.Open` + `f.Stat` flow | Redeclaration via `:=` with at least one new variable | Guard clauses without `else` | Eff p.7 | 2009 |

### 2.9 Conventions, names and package organization

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| "Unsatisfactory" code from literal translation of C++/Java | Different idioms | Rethink the problem in terms of Go | Eff p.2 | 2009 |
| Fighting gofmt | Manual rearranging against the tool | Reorganize the code | Eff p.2 | 2009 |
| Long name to compensate for missing docs (`DoOrWaitUntilDone`) | Name doing the job of a comment | Short name and doc | Eff p.4 | 2009 |
| Widespread `import .` | Pollutes the namespace | Use only in tests external to the package | Eff p.4 | 2009 |
| Lowercase name inaccessible from another package (`newItem`, field `price`) | Visibility by capitalization | Export with an uppercase initial | Little p.56 | go1.3.3 |
| Error "import cycle not allowed" | A imports B and B imports A, directly or indirectly | Reorganize or extract a third package | Little p.54–55 | go1.3.3; GOPATH structure **[DATED]** |
| "Item undefined" errors in `db.go` | Type moved to another package (`shopping`) without adjusting references | Qualify with the package and adjust imports | Little p.55 | go1.3.3; **[DATED]** as to the layout |
| Inconsistency in the example with `new(Saiyan)` and lowercase `goku.name` | Didactic defect of the book (the struct has `Name`/`Power`) | Not a language rule; ignore | Little p.33 | go1.3.3 |

### 2.10 Compilation and tooling

| Symptom | Cause | Fix | Source | Era |
|---|---|---|---|---|
| `;` inserted before `{` breaks the code | Opening brace on the next line of `if/for/switch/select` | Open the brace on the same line | Eff p.5–6 | 2009 |
| Unused imports or variables prevent compiling | Compiler rule: an unused import bloats the program and slows compilation; an initialized and unused variable is wasted computation and perhaps a sign of a bigger bug | During development, silence with blank: `var _ = fmt.Printf` right after the imports and `_ = fd` in the body, with a reminder comment; then remove (Little only reports the error and does not teach this workaround) | Eff p.37–38; Little p.21–22 (imports), p.24 (variables) | both |
| Return value that does not matter gets in the way (e.g., only the `bool` matters) | An unused variable does not compile | `_, exists := power("goku")`: the blank receives no assignment and can repeat with any type | Little p.25 | go1.3.3 |
| `error` return discarded with `_` to "ignore" the failure | Practice that Eff calls terrible; the example with `fi, _ := os.Stat(path)` breaks if the path does not exist | Use `_` only for the irrelevant value (`if _, err := os.Stat(path); ...`) and always check the `error` (see §2.5) | Eff p.36 | 2009 |
| `go run` fails for lack of `package main`/`main` | No entry point | Declare `package main` and `func main`; with `go build` there is simply no entry point | Little p.19–20 | go1.3.3 |
| Wrong command-line argument | `os.Args[0]` is the path of the executable | Real arguments start at index 1 | Little p.21 | go1.3.3 |

## 3. Illustrative cases

### 3.1 Effective Go

- **`os.Open` + `f.Stat` with reused `err`** (Eff p.7): guard clauses without `else` and redeclaration via `:=`. Lesson: returning early keeps the happy path aligned to the left.
- **`unhex`, `shouldEscape`, `Compare`** (Eff p.9–11): `switch` without an expression and case lists. Lesson: `switch` replaces if-else chains and avoids implicit fallthrough.
- **Labeled loop with `break Loop`** (Eff p.10): exits the loop from inside the `switch`. Lesson: a plain `break` only ends the `switch`.
- **`nextInt` / `io.ReadFull`** (Eff p.12–13): multiple returns instead of an output pointer; named results. Lesson: return the value and the error together.
- **`Contents` with `defer f.Close()`** (Eff p.13): closes on any path. Lesson: pair acquisition and release.
- **`trace`/`un`** (Eff p.14): defer arguments evaluated when the defer is registered. Lesson: you can mark a function's entry and exit with one line.
- **`SyncedBuffer`** (Eff p.15): useful zero value, transitively. Lesson: design types that work without a constructor.
- **`NewFile` with a composite literal** (Eff p.16): returns the address of a local variable safely. Lesson: lean constructors.
- **2D `picture` with two allocations** (Eff p.20): row by row versus a single block. Lesson: the trade-off decides between flexibility and cost.
- **`timeZone` and `offset`** (Eff p.21–22): map with comma-ok, set via `map[string]bool`, `delete`. Lesson: distinguish absence from zero.
- **Recursive `MyString.String`** (Eff p.24): classic infinite-recursion trap via `Sprintf`. Lesson: convert to the base type.
- **`ByteSize` with `iota` and `String`** (Eff p.26–27): enumeration and formatting on a scalar type; the `%f` verb avoids the recursion. Lesson: `String` on simple types requires care with the verb.
- **`ByteSlice.Write`** (Eff p.28–29): pointer receiver to satisfy `io.Writer`; use with `fmt.Fprintf(&b, ...)`. Lesson: pass `&b`.
- **`Sequence` + `sort.IntSlice`** (Eff p.30–31): type conversion to reuse methods. Lesson: converting is cheaper than reimplementing.
- **`crc32.NewIEEE`, `adler32.New`, `cipher.NewCTR`** (Eff p.33): return an interface and hide the concrete type. Lesson: swapping the algorithm does not change client code.
- **`Counter`, `Chan`, `HandlerFunc`/`ArgServer`** (Eff p.34–36): any type can have methods; `Counter` is not concurrency-safe. Lesson: methods on non-struct types become HTTP handlers.
- **`var _ json.Marshaler = (*RawMessage)(nil)`** (Eff p.39): compile-time check. Lesson: use when the error would be silent at run time.
- **`bufio.ReadWriter` and `Job` with embedded `*log.Logger`** (Eff p.40–41): embedding versus manual forwarding; refine via `job.Logger`. Lesson: embedding promotes methods without writing them.
- **Channel semaphore, fixed pool, `Request` with `resultChan`, `Vector.DoAll`, free list with `select/default`** (Eff p.44–48): bounded-concurrency patterns. Lesson: the channel is both data and synchronization. The loop variable in the semaphore example is **[DATED]** (Go < 1.22).
- **`os.PathError` and retry with `syscall.ENOSPC`** (Eff p.48–49): structured error inspected by type assertion. Lesson: errors carry context.
- **`CubeRoot` with panic, `safelyDo` with recover, regexp `Compile` with a local `Error`** (Eff p.50–52): internal panic, external `error`. Lesson: recover at the boundary.
- **QR code web server** (Eff p.52–54): `flag`, `html/template` (escapes automatically), `http.HandlerFunc`, `template.Must`, blocking `ListenAndServe`. The external chart service cited is only the example's. **[DATED]** as to that service and 2009 APIs; **[inference]**.

### 3.2 The Little Go Book

- **Copy vs pointer** (Little p.29–30): `Super(s Saiyan)` changes the copy; `Super(s *Saiyan)` with `&Saiyan{...}` changes the original. Lesson: reference for explaining pass by value.
- **Growing capacity with append** (Little p.43): initial capacity 5 and 25 insertions; the author describes 10, 20, 40. Lesson: growth is amortized. **[DATED]** as to the "2x" factor.
- **Window over an array** (Little p.44–45): `scores[2:4]` and `slice[0] = 999` changes `scores`. Lesson: a subslice is a view, not a copy.
- **`strings.Index(haystack[5:], " ")`** (Little p.45): idiomatic substitute for indexOf with a start position.
- **Removal by swapping with the last** (Little p.45): swaps with the last element and returns `source[:lastIndex]`. Lesson: O(1) removal when order does not matter.
- **`copy(worst, scores[:5])`** (Little p.46): copies the five lowest after `sort.Ints`. Lesson: `copy` isolates from the original; the author suggests experimenting with different sizes.
- **Map with existence check** (Little p.47): `power, exists := lookup["vegeta"]` returns `0, false`.
- **shopping/db/models/main structure** (Little p.53–55): organization and breaking a cycle. **[DATED]** as to the GOPATH layout.
- **Embedding** (Little p.35–36): `Saiyan` embeds `*Person`; `goku.Name` and `goku.Person.Name` are equivalent; its own `Introduce` "overrides", and the original stays at `s.Person.Introduce()`. Lesson: composition instead of inheritance.
- **`Logger` interface** (Little p.58): `Log(message string)` with `SqlLogger`, `ConsoleLogger`, `FileLogger`; implicit satisfaction. Lesson: interfaces are satisfied without declaration.
- **`io.EOF` as a sentinel** (Little p.64): `if err == io.EOF`.
- **`defer file.Close()`** (Little p.65): comes after the check of the `os.Open` error.
- **`if err := process(); err != nil`** (Little p.67): the variable exists in `else if`/`else`, not outside.
- **Mutex on a counter** (Little p.74–75): `lock.Lock(); defer lock.Unlock(); counter++`. Lesson: the same counter without a lock has a data race.
- **Worker pool** (Little p.77–79): five goroutines `go worker.process(c)` on the same channel; each value goes to exactly one worker.
- **Dropping with select/default** (Little p.80): 20 msg/s input against 10 msg/s capacity drops half.
- **Timeout with `time.After`** (Little p.80–81): `case c <- v:` and `case <-time.After(100ms):`.
- **Conceptual implementation of `after`** (Little p.81): a goroutine that sleeps and sends on a channel. Lesson: there is no magic.
- **`select` in `for` in the worker** (Little p.81): `case data := <-c` and `case <-time.After(10ms)` as a "pause".

## 4. Gaps and warnings

- This file cites the **Spec go1.26** only at isolated points (p.12, p.52, p.57–58, p.69, p.111); the formal rules (method sets, comparability, `range` semantics) are in `regras-da-spec.md`.
- The nil-pointer-in-interface pitfall: no source describes it; it is a deduction [inference] from Spec p.12 and p.69 (see `procedimentos.md` P6.1 and `regras-da-spec.md` §3.6). `range` over integer/function, `min`/`max`, generics and modules are not covered by this file (see `versoes-e-migracao.md` and `regras-da-spec.md`); the content of Eff and Little predates them.
- The only case in which the source text itself says a newer version changes the conclusion is the loop variable before Go 1.22 (Eff p.44). Other modern points, here, are **[inference]**.
- Little items are from go1.3.3 and the GOPATH layout; treat package structure and the slice growth factor as **[DATED]**.
- The Little book does not describe the consequence of using an uninitialized map (Little p.47); I do not assert it.
