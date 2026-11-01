# Go: principles, mental models and decision trees

Reference base for the Go specialist agent. Organized by problem. Each item gives the principle (the why), the "if X → Y" rule, the trade-offs and the source.

## Contents

0. How to read: sources, era labels and gaps
1. Values vs pointers and receivers
2. Slices, arrays, maps: new vs make vs literal
3. Interfaces
4. Embedding vs forwarding (composition)
5. Error handling, panic and recover
6. Defer
7. Concurrency: goroutines, channels, mutex, buffer, select, backpressure, stopping
8. Names and package organization
9. Formatting and fmt
10. Control flow and functions (general idioms)
11. Conflicts between sources and known gaps

---

## 0. How to read: sources, era labels and gaps

**Sources and abbreviations.** (Eff) Effective Go, from 2009: predates generics and modules. (Spec) Specification go1.26: normative and current. (Little) The Little Go Book, go1.3.3 with GOPATH: very dated. (RN) release notes Go 1.20 to 1.24. Citations such as (Eff p.N) point to the **PDF** page of the source (see `INDEX.md`, page convention).

**Labels.**
- **[DATED: Eff]** and **[DATED: Little]** mark content from an old source that may conflict with newer Spec or RN. When a newer source exists that corrects it, it is indicated.
- **[inference]** marks my links between sources or extrapolations that no source states literally.
- No label = the cited source states it and there is no sign of conflict with newer material.

**Coverage warning (important).** This file deals mainly with Eff, Little and (in concurrency, defer and panic/recover) the Spec. The release notes and the details of generics live in their own files: where this base says "see RN1.xx", open `versoes-e-migracao.md` (master table, attention items, GODEBUG) before stating anything about version changes; for generics, `regras-da-spec.md` §4. `errors.Is/As`, `context` and modern `sync` (WaitGroup, errgroup) are not in Eff, Little or the Spec, and the RN only cite isolated novelties (e.g., `errors.Join`, `context.WithoutCancel`, `sync.OnceFunc`); beyond that the subject is not covered by the sources.

---

## 1. Values vs pointers and receivers

### 1.1 Mental model: everything is a copy
- **Principle.** Passing a value copies the value; passing a `*T` copies the address, which keeps pointing to the same data. Reassigning the pointer inside the function does not change the caller's pointer; only changing the pointed-to data is visible (Little p.29–30). This is not exclusive to Go: the author compares with Ruby, Python, Java and C#; Go just makes the indirection visible (Little p.30).
- **What pointers are for.** Two purposes: avoiding an expensive copy and sharing/mutating the same value. The real gain is in sharing (Little p.30). Passing by value is a way to hand "immutable" data to the receiver (Little p.37).
- **The same question applies everywhere.** The pointer/value decision is the same for local variable, field, return, parameter and receiver (Little p.37).

### 1.2 Decision tree: pointer or value?
1. **Does the code need the function/method to change the caller's data?** If yes → pointer (Little p.37; Eff p.28–29).
2. **Is the struct large?** If yes → pointer, even with no intent to mutate, to avoid the copy cost (Little p.37).
3. **Is the struct tiny** (something like `Point{X, Y int}`)? If yes → a value may pay off through direct access, without indirection. The difference only shows with tens of thousands of items (Little p.37).
4. **Do you want the receiver to be unable to change the data?** If yes → value. The author notes that "more often" this is not what is wanted (Little p.37).
5. **In doubt** → pointer (Little p.37). **[DATED: Little]** It is a default from an introductory book; treat it as a heuristic, not a design rule. [inference] The final decision should weigh semantics (is the type a "value" or an "entity"?) and cost, and should be consistent per type.

**Little's example (step 1).** `Super(goku)` with `func Super(s Saiyan)` and `s.Power += 10000` prints 9000, because the function changes a copy (Little p.29–30). With `goku := &Saiyan{"Goku", 9000}` and `func Super(s *Saiyan)`, the caller sees the change (Little p.30). The same holds for a method: with `func (s *Saiyan) Super()`, `goku.Super()` changes the original and the printed `Power` goes from 9001 to 19001 (Little p.31). For an integer type, Eff shows `Counter int` with `func (ctr *Counter) ServeHTTP(...)` and `*ctr++`: the receiver must be a pointer for the increment to be visible to the caller (Eff p.34).

**Trade-off.** Pointer: less copying and shared mutability, but aliasing (who else sees this data?) and, [inference], more allocation pressure when the value "escapes". Value: isolation and simplicity, but copy cost growing with size.

### 1.3 `[]T` or `[]*T`; map of values or of pointers
- Passing or returning the slice itself costs the same in both cases (it is a copy of a reference to an array). The choice of `T` vs `*T` depends on **how you use each individual element**, applying the logic of section 1.2, and not on how you use the slice or the map (Little p.49).

### 1.4 Receivers: method rules
- **Methods on any named type** (except pointer or interface), not only structs (Eff p.28). Classic example: a `ByteSlice` type with `Write` on `*ByteSlice` to satisfy `io.Writer` (Eff p.28–29).
- **Set rule.** Value methods can be called on a value or a pointer; pointer methods can only be called on pointers (Eff p.29). Eff explains why: a pointer method can modify the receiver, and calling it on a value would make the method receive a copy, discarding the modifications; so the language forbids this error (Eff p.29). Exception cited in the same passage: if the value is addressable, the compiler inserts the address operator by itself; with `var b ByteSlice`, `b.Write` is rewritten as `(&b).Write` (Eff p.29). To assign to `io.Writer` you pass `&b`, since only `*ByteSlice` satisfies the interface (Eff p.29).
- **If the type needs a pointer receiver** (because it changes state) → it is `*T` that satisfies the interface; a plain `T` does not (Eff p.28–29). [inference] Practical consequence: when assigning to an interface, pass `&t`, not `t`.
- **Slice passed by value.** The function sees and changes the elements in the shared array, but to grow or reassign the slice it must return it or use a pointer receiver (Eff p.19).
- **`String()` and fmt.** If you need to print both `T` and `*T` with the same format, the `String` receiver must be a value; for structs the Eff text says a pointer is more efficient and idiomatic (Eff p.24). Assumed tension: choose according to who will be printed.
- **Mixing receivers on the same type.** None of the sources read deals with this. [inference] Avoid mixing without reason, because of the set rule above.

### 1.5 Returning the address of a local
- Returning `&File{...}` of a local variable is valid in Go: the storage survives the function (Eff p.16). Principle behind it: the programmer does not decide stack vs heap, the language guarantees the semantics. [inference] Do not "optimize" by avoiding pointers out of fear of dangling.

---

## 2. Slices, arrays, maps: new vs make vs literal

### 2.1 Mental model
- **A slice is a window onto a shared array.** Slicing or passing does not copy data. This changes the style: instead of passing a starting position, you pass `haystack[5:]` (Little p.44–45).
- **Capacity when reslicing.** The Spec defines capacity as the slice's length plus the part of the array beyond it, and says that from the original slice you can create a slice of length up to that capacity (Spec p.15). For slices, the upper bound of `a[low:high]` is `cap(a)`, not `len(a)` (Spec p.54). That `cap(a[:n])` is k when `a` has capacity k (with `n <= k`) is a deduction [inference] from those two passages: the Spec only exemplifies the computation with an array, where `a[1:4]` over `[5]int` gives length 3 and capacity 4 (Spec p.54), and `a[1:3:5]` gives capacity 4 (Spec p.55).
- **Slices, maps and channels need `make`**; `new(X)` and `&X{}` only allocate. The author treats this as a fundamental rule that explains much of the apparent complexity (Little p.84, p.42).
- **Maps are references.** Changes made inside a function show up in the caller (Eff p.20).

### 2.2 Tree: new, make, literal?
1. **Is the type a slice, map or channel?** → `make` (returns the value ready for use, not a pointer). For any other type → `new(T)` or `&T{}` (Eff p.17).
2. **Want `new([]int)`?** Almost never: it returns a pointer to a nil slice. The idiomatic way is `make([]int, 100)` (Eff p.17).
3. **Does the zero value already work?** → no constructor needed; design for that (section 1 of Eff p.15, and below). If not enough → constructor with a composite literal, returning `&File{...}` (Eff p.16).
4. **Are there fields to initialize?** → prefer `&X{field: value}` to `new(X)` followed by assignments, for readability (Little p.32–33). Use `field: value` also to omit fields and be independent of order; `new(File)` is equivalent to `&File{}` (Eff p.16).
5. **Want to hide allocation from the rest of the code?** → `NewX` function (Little p.32–33). In a package with one main type, the constructor is called just `New` (Eff p.4; see section 8).

**Useful zero value as a principle.** Design structs to work without initialization. The property is transitive: a struct with `sync.Mutex` and `bytes.Buffer` is already usable (Eff p.15).

### 2.3 Which way to create a slice?
According to Little p.43–44:
- Values known in advance → `[]T{a, b, c}`.
- Will write at specific indices → `make([]T, n)`. Careful: it is born with `n` zeroed elements.
- Unknown number of elements → `var s []T` (nil) + `append`.
- Have an idea of the size → `make([]T, 0, n)` + `append`. Even knowing the exact size, this form is valid, a "matter of preference".

Additions from Eff:
- `append` always with assignment of the result: `x = append(x, ...)`, because the underlying array may change. Appending a slice to a slice requires `y...` (Eff p.26). `append` is a builtin because the result type depends on the caller (Eff p.25).
- `len` and `cap` work on a nil slice and give 0 (Eff p.19).
- To read "the first 32 bytes" of a buffer use `buf[0:32]`; the function that reads into a buffer should receive `[]byte`, not a pointer + count, because the slice length already limits the read (Eff p.18).

**Capacity trade-off.** `make` with `cap` avoids successive reallocations. If the size is a guess that is too large, it wastes memory. [inference] The gain only matters in hot loops.

### 2.4 Arrays vs slices
- Arrays serve for fine memory layout, avoiding allocation or explicit dimensions (e.g., transformation matrix). Most code uses slices; even passing `*[3]float64` "is not idiomatic" (Eff p.17–18).

### 2.5 2D slices
- Rows that can grow or shrink → allocate each row separately (avoids overwriting the next one). Fixed-size rows → allocating a single block and slicing may be more efficient (Eff p.20).

### 2.6 Removing an element
- If order does not matter: swap with the last and shrink with `s[:len(s)-1]` (Little p.45). With order, the source read does not say; [inference] the following elements must be moved.

### 2.7 Maps
- Key of any type with defined equality; **slices cannot be keys** (Eff p.20).
- Set → `map[T]bool`; test by direct indexing (absent = false) (Eff p.21).
- A missing key returns the zero value. To distinguish "absent" from "zero" → `v, ok := m[k]`; presence only → `_, present := m[k]` (Eff p.21–22).
- `delete(m, k)` is safe even if the key does not exist (Eff p.22).
- Maps printed with `%v` come out sorted by key (Eff p.23). [DATED: Eff] Eff does not discuss the **iteration** order of `range` over a map; Little says it is random (Little p.48) and the Spec says it is unspecified and may vary (Spec p.89). Do not assume order.

### 2.8 Constants and enumerations
- Constants: only numbers, runes, strings, booleans; expression evaluable at compile time (`1<<3` yes, `math.Sin(...)` no) (Eff p.26).
- Enumerations with `iota`, using `_ = iota` to skip the first (Eff p.26).
- **[DATED: Eff]** Eff does not cover constants with generics or constraint types. For that, the Spec.

---

## 3. Interfaces

### 3.1 Principles
- **Interface = set of methods, for almost any type.** That is why integers, functions, channels and structs can serve as HTTP handlers (Eff p.36). Implicit implementation allows swapping and testing without touching the client (Little p.58).
- **Depend on the minimum.** If the function only calls `Close()`, accept `io.Closer`, not the concrete type (Little p.58–59).
- **Small interfaces.** With 1–2 methods they are common and named after the method (Eff p.30). One-method interface: method name + `-er` (`Reader`, `Writer`, `Formatter`) (Eff p.5).

### 3.2 "Accept interfaces, return structs": what the sources say
- **Accepting narrow interfaces** has direct support: Little p.58–59 (above).
- **"Return a struct (concrete type)" is not stated by any source read.** [inference] It is a community convention; here, treat it as a non-source.
- **There is one case where Eff recommends the opposite:** if the type exists only to implement an interface and has no extra exported methods, **do not export the type; export the interface and make the constructor return the interface** (examples: `crc32.NewIEEE` and `adler32.New` return `hash.Hash32`). Benefits: swapping the algorithm means changing only the constructor; the documentation is not repeated in each implementation (Eff p.32–33). **[DATED: Eff]** [inference] Prefer this pattern only in the strict case described; outside it, returning the concrete type lets the caller use extra methods without a type assertion.

### 3.3 Decision tree: when to create an interface?
1. **Does the function need only a small subset of behaviors?** → declare (or use) a minimal interface at the point of use (Little p.58–59).
2. **Is there more than one real implementation, or do I need to swap/test?** → interface (Little p.58).
3. **Is there an import cycle?** → interfaces help: they have few dependencies because they have no implementation. The other way out is to extract structures to a package with no dependencies on the project (Little p.54–56, p.59). See section 8.
4. **Only one implementation and nobody varies** → [inference] do not create an interface in anticipation.

### 3.4 Type assertion, type switch, checks
- Discover the dynamic type → type switch; reusing the name (`switch t := t.(type)`) is idiomatic (Eff p.11).
- Only one type matters → type assertion, **always with "comma ok"** if it can fail; without it, failure becomes a run-time crash (Eff p.32).
- Check at run time without using the value: `if _, ok := val.(json.Marshaler); ok` (Eff p.38).
- **Compile-time guarantee** that a type satisfies the interface: `var _ json.Marshaler = (*RawMessage)(nil)`. Use only in the rare cases where no static conversion already forces the check; do not do it for every type (Eff p.39).

### 3.5 Adapting functions to interfaces
- Function with the right signature → function type with a method, in the `http.HandlerFunc` pattern: `http.Handle("/args", http.HandlerFunc(ArgServer))` (Eff p.35–36).

### 3.6 Conversion to access another set of methods
- Converting between types with the same structure does not create a new value, and gives access to the other set of methods (`sort.IntSlice(s).Sort()`). It is an idiom, but more unusual than implementing several interfaces (Eff p.30–31). **[DATED: Eff]** [inference] For sorting, check the current `sort`/`slices` API before recommending; Eff does not cover packages after 2009.

---

## 4. Embedding vs forwarding (composition)

### 4.1 Principle
- **Struct + method + composition replaces class + inheritance.** The author of Little defends composition as more robust: it avoids coupling the class to the superclass and focuses on behavior rather than hierarchy (Little p.28, p.36).
- Embedding reuses implementation **without writing forwarding methods** (e.g., `bufio.ReadWriter` embeds `*Reader` and `*Writer`; a `Job` embeds `*log.Logger`) (Eff p.40–41).

### 4.2 Rules the agent must know
- **The receiver of a promoted method is the inner type, not the outer** (Eff p.40). [inference] There is no "super" nor virtual polymorphism: the inner method does not see the outer (deduction from Eff p.40; the text only says the receiver is the inner type). If the inner needs to call something from the outer, pass it as a parameter or interface.
- **Interfaces only embed interfaces**; they compose by union (Eff p.40).
- The embedded field has the type's name, without a package qualifier (`job.Logger`), useful to refine a method (Eff p.41).
- **Name conflicts.** The less nested name hides the more nested one. The same level is usually an error, but is accepted if the duplicated name is never used outside the type definition (Eff p.41–42).
- **An embedded field of pointer type must be initialized before use** (Eff p.40).

### 4.3 Tree: embedding or named field + forwarding methods?
1. **Want to expose the whole API of the inner type on the outer too?** → embedding.
2. **Want only to reuse behavior, without exposing it?** → [inference] named field and own methods; the sources read do not discuss the case explicitly, but embedding promotes the whole exported set.
3. **Want to refine a method of the inner one?** → embed and declare the method on the outer; the inner remains accessible via `outer.Inner.Method` (Eff p.41).
4. **Want subtyping/inheritance?** → does not exist; use an interface (section 3).

---

## 5. Error handling, panic and recover

### 5.1 Principles
- **Errors are values returned along with the result**, and it is good style to provide detailed information (Eff p.48). They are also part of the normal flow and produce code that is easier to follow, although the author admits many dislike it (Little p.71).
- **Return multiple values**, not in-band codes such as -1 for EOF (Eff p.11–12).
- **Libraries avoid panic**; if the problem can be worked around, the program should continue (Eff p.50).

### 5.2 Tree: error, panic or what?
1. **Predictable failure (I/O, invalid input, missing resource)?** → return `error`. Whoever needs the detail uses a type switch or assertion (e.g., `*os.PathError` and its `Err` field) (Eff p.49).
2. **Unrecoverable or "impossible" situation** (e.g., a loop that does not converge)? → `panic` (Eff p.50).
3. **Package initialization failure?** → an exception where panic is acceptable (Eff p.50).
4. **Writing a library?** → do not let panic escape to the client: convert to `error` (Eff p.52).
5. **Does a server need to survive a bug in a goroutine?** → `defer` with `recover` and a log, without bringing down the others (Eff p.51).

### 5.3 Error message quality
- The string should identify the origin, with a package or operation prefix (e.g., "image: unknown format") (Eff p.49).
- Rich types (like `PathError` with `Op`, `Path`, `Err`) give useful context even far from the call (Eff p.48–49).
- **[DATED: Eff]** Eff works with type switch/assertion on the error. Eff (2009) does not describe chaining (wrapping) or `errors.Is/As`. RN1.20 brings composite errors (`errors.Join`, multiple `%w`, `Unwrap() []error`; RN1.20 p.6, p.10; see `versoes-e-migracao.md` §2, Go 1.20).

### 5.4 Panic: the exact semantics (Spec)
- A `panic` (explicit or run-time) ends F; F's defers run, then the caller's, up to the top of the goroutine; then the program terminates and reports the value (Spec p.104).
- **`recover` only works**: inside a deferred function and called **directly** by it. It does not work in a helper function called by the deferred one. Outside a panic, or called indirectly, it returns nil (Spec p.104–105; Eff p.50–51).
- If the deferred function D (of G) calls `recover` successfully and returns normally, the panic stops; the intermediate state is discarded, G's defers registered before D run and G returns to its caller (Spec p.104–105).
- **A panic in a goroutine without defer+recover terminates the whole program** (Spec p.104). [inference] `recover` in one goroutine does not protect others: each goroutine needs its own.
- **`panic(nil)`**: Spec p.105 says that, to ensure `recover` returns non-nil on a panic, `panic` with a nil interface causes a run-time panic. The version in which this was introduced is not in the text read; check the RN.

### 5.5 Internal package pattern: panic/recover to unwind
- In a parser/deep recursion, the package does `panic` with a **local error type**; the public function (`Compile`) has a defer that recovers, zeroes the named return and converts to `error` via `e.(Error)`. If the panic is not of the local type, the assertion fails and the unwinding continues (re-panic) (Eff p.51–52).
- **Rule:** only inside a package; do not expose panics to the client (Eff p.52).
- **Trade-off.** Simplifies recursive code, but hides control flow. [inference] Use when nesting makes manual `error` propagation the dominant noise.

---

## 6. Defer

### 6.1 Principle
- Advantages the sources cite for `defer f.Close()`: (1) the release stays close to the open, clearer than at the end of the function (Eff p.13; Little p.65); (2) it covers all return points, since the call runs immediately before the function returns, through `return`, end of body or panic (Spec p.97), and Little adds that it runs even on a "violent" exit (Little p.65); (3) it guarantees the close is not forgotten when editing the function and adding a new return path (Eff p.13; Little p.65 speaks of forgetting the `Close` of something declared ten lines above). It is not only for resources: it can register a function's exit (Little p.71).
- Reading example (Eff p.13, `Contents`): `defer f.Close()` right after checking the `os.Open` error; loop with `n, err := f.Read(buf[0:])`, accumulating only `buf[0:n]`; `err == io.EOF` ends the loop and another error returns, with the file closed by the defer. `Read` accepts a slice instead of a pointer and count, and `buf[0:32]` limits the read to 32 bytes (Eff p.18).

### 6.2 Rules
- **Resource to release (close file, unlock mutex) → `defer` right after acquiring** (Eff p.13).
- **Each `defer` evaluates and stores the function and arguments at the moment it is executed**; the calls run in reverse order (LIFO). `for i := 0; i <= 3; i++ { defer fmt.Print(i) }` prints 3 2 1 0 (Spec p.97; Eff p.13–14).
- The deferred function runs before the enclosing one returns: through `return`, end of body or because the goroutine is panicking (Spec p.97).
- **Defers run after `return` assigns the results and before going back to the caller**. A closure can read and change named results (`return 6` with `result *= 7` returns 42). The deferred function's returns are discarded (Spec p.97–98).
- `nil` deferred function: the panic occurs at **invocation**, not at the `defer` (Spec p.97).
- Entry/exit trace: `defer un(trace("a"))`. `trace` is evaluated immediately, `un` on exit (Eff p.14).
- `defer` is per function, not per block: it differs from scope-based resource management (Eff p.15).

### 6.3 Pitfall and trade-offs
- **Defer in a loop** accumulates until the end of the *function* (Eff p.13–14; Spec p.97). [inference] In a loop that opens many resources, extract the body into a helper function, so the defer runs on each iteration.
- A defer has a cost (it stores function and arguments), but the sources read give no numbers; do not assert cost without measuring.
- **Tree:** need to release on exit by any path → `defer`. Need to release before the end of the function (e.g., long lock) → [inference] release explicitly or isolate in a function.

---

## 7. Concurrency

### 7.1 Principles
- **The problem is sharing data.** Without shared data, there is nothing to synchronize. Concurrent reads are safe; writes need synchronization (Little p.74, p.77).
- **Share memory by communicating.** Values pass through channels, only one goroutine accesses the value at a time; data races do not occur "by design" in this scheme (Eff p.42). Channels change the view from "dangerous regions of code" to message passing (Little p.82).
- **Not to excess.** Eff admits the motto can be taken too far: a reference counter may be better with a mutex around an integer (Eff p.42).
- **Concurrency is not parallelism.** Go is concurrent, not parallel; not every parallelization problem fits the model (Eff p.47).

### 7.2 Tree: goroutine, channel or mutex?
1. **Simple shared state, short lock** (counter, small cache)? → `sync.Mutex`/`sync.RWMutex` (Little p.75–76, p.82; Eff p.42).
2. **Coordination** (wait for completion, signal "there is new data"), **distributing work**, **passing ownership of a datum**? → channels (Little p.76–77, p.82; Eff p.42–43).
3. **Many reads and few writes?** → `RWMutex`, but note: it forces you to think not only about *when* but *how* the data is accessed (read vs write) (Little p.76).
4. **More than one lock?** → deadlock is easy and hard to detect. Prefer fine-grained locks (little code) to coarse ones, which cancel the gain from concurrency (Little p.75).
5. **Atomic counting?** → `sync/atomic`. Little recommends mastering `sync` and `sync/atomic` besides channels (Little p.82). **[DATED: Little]** For novelties in `sync` and `sync/atomic`, the RN cite only isolated points (`sync.OnceFunc` in 1.21, RN1.21 p.14; atomic `And`/`Or` and `sync.Map.Clear` in 1.23, RN1.23 p.10); see `versoes-e-migracao.md` §1.4.

**Trade-off.** Channels make flow and ownership explicit, but cost in complexity when the problem is just "protect an integer". A mutex is simple and local, but does not scale in reasoning when the state spreads.

### 7.3 Goroutines: launch semantics
- `go` requires a function/method call, without parentheses around the expression. **Function and arguments are evaluated in the calling goroutine**, at the `go` point; only the execution is independent. Returns are discarded (Spec p.92).
- A function literal in a goroutine requires the call: `go func() { ... }()` (Eff p.42–43). Closures keep the referenced variables alive (Eff p.43).
- **Loop variable captured by a closure.** Since Go 1.22 each iteration has its own variable (RN1.22 p.1; Spec p.88); Eff warns that the `Serve` example has the shared-variable bug in earlier versions (Eff p.44). **[DATED: Eff/Little]** Any goroutine-in-loop example from these sources must be reread in this light. That the behavior depends on the `go` line of `go.mod` is [inference] (see `versoes-e-migracao.md` §3.1): confirm the version before asserting.
- **When `main` returns, the program exits without waiting for the other goroutines** (Spec p.111).

### 7.4 Stopping and waiting for goroutines
1. **Wait for completion** → channel: the goroutine signals when done and the other side does `<-c` (Eff p.43).
2. **Wait for N tasks** → N signals on a channel, then drain N times (Eff p.46). If the signaling channel has a buffer, the goroutine does not get stuck trying to signal (Eff p.46).
3. **Tell a goroutine to "stop".** The sources read bring no dedicated mechanism (cancellation, `context`). [inference] The derivable pattern is a signaling channel read in a `select` inside the goroutine's loop (Little p.81 shows `select` in a loop). For `context`, consult a current source: it is not in these sources.
4. **Who closes the channel?** The Spec does not say (Spec p.99–100). Spec rules, separated by operation:
   - **Receiving from a closed channel:** the operation always proceeds immediately, returning the element's zero value after the values already sent have been received (Spec p.70); after `close` and exhaustion, the receive returns the zero value without blocking (Spec p.100). In the form `x, ok = <-ch`, `ok` is `false` when the value is a zero generated because the channel is closed and empty, and `true` when it came from a successful send (Spec p.71); the Spec also says the two-value receive form indicates whether the channel is closed (Spec p.100).
   - **Sending on a closed channel:** the send "proceeds" by causing a run-time panic (Spec p.80); sending to or closing an already-closed channel causes a panic (Spec p.99–100).
   - **Closing:** closing a nil channel also causes a panic; closing a receive-only channel is an error (Spec p.99–100).

   [inference] The closer should be the sender, never the receiver, because sending after closing is a panic.
5. **Goroutine leak.** [inference] A goroutine blocked forever on an unpaired send/receive never terminates (Spec p.80: blocking on a nil channel is forever; unbuffered, until there is a receiver). Always design the exit.

### 7.5 Buffer, blocking and channel semantics
- **The receiver always blocks until there is data.** On an unbuffered channel, the sender blocks until the receive. With a buffer, until the copy into the buffer (Eff p.43; Spec p.80).
- `len(ch)` = items in the queue, `cap(ch)` = buffer size; both 0 for nil (Spec p.101). `make(chan T)` unbuffered; `make(chan T, n)` with negative n causes a run-time panic (Spec p.102).
- Nil channel: send blocks forever (Spec p.80); `select` with only nil and no default blocks forever (Spec p.93). [inference] Assigning nil to a channel variable disables that `case` of the `select`.
- **When to buffer?** (a) Absorb spikes (Little p.79). (b) Semaphore (below). (c) Keep the sender from getting stuck on signaling (Eff p.46). Trade-off: a buffer hides consumer slowness and postpones the problem instead of solving it [inference].

### 7.6 Backpressure: four strategies (Little p.79–81)
Tree for "the consumer cannot keep up":
1. **High processing guarantee (cannot lose)?** → let the sender **block**.
2. **Short bursts?** → **buffer** to absorb the spike.
3. **Is loss acceptable?** → **drop** with `select` + `default`. An empty `default` drops silently.
4. **Wait up to a limit?** → `case <-time.After(d):` alongside the channel operation.

**Trade-offs.** Blocking propagates the slowness backwards (may stall the producer). A buffer only postpones. Dropping requires loss tolerance. A timeout requires deciding what to do when it expires.

### 7.7 Limiting concurrency
- **Buffered channel as a semaphore**: send before processing, receive when done (Eff p.44).
- **Also limit goroutine creation.** The one-goroutine-per-request design can consume resources without limit if requests arrive fast. Solutions: acquire the semaphore before `go`, or start a fixed number of workers reading from the same channel (Eff p.44–45).
- **Response via a channel inside the request** (channels are first-class values): the request carries its `resultChan`, which allows demultiplexing without a mutex (Eff p.45–46).
- **Parallelize**: split independent work into N pieces, launch one goroutine per piece and drain N signals (Eff p.46).
- **Free list** with a buffered channel + `select` with `default` (non-blocking): if the list is full, the buffer is dropped and the GC collects it (Eff p.47–48).
- **CPUs.** `runtime.NumCPU()`; `runtime.GOMAXPROCS(0)` only queries (default = NumCPU; overridable by environment or a positive call) (Eff p.46–47). **[DATED: Eff]** The behavior of `GOMAXPROCS` and the scheduler may have changed later; check the RN before asserting numbers.

### 7.8 Select: exact rules (Spec p.92–93)
1. On entry, the channels of the receives and the channels and values of the sends are evaluated exactly once, in code order, even if the case is not chosen. The left side of a receive with assignment is not yet evaluated.
2. If any communication can proceed, **one is chosen by uniform pseudo-random selection**. Otherwise, with `default`, it is chosen. Otherwise it blocks.
3. Executes the communication, evaluates the left side and assigns, runs the case's list.
- A nil channel never proceeds; `select {}` blocks forever. **There is no priority or fallthrough** between cases (Spec p.93). [inference] To prioritize, the code must be structured (for example, nested `select`).
- **Pitfall.** `select` with `default` in a loop, without other blocking, spins without waiting (the Spec only defines that the default is chosen when nothing is ready) (Spec p.93). [inference] It consumes CPU.
- Little p.81 summarizes: the first available channel is chosen; if several, random; without default it blocks. A common pattern is `select` inside `for`.

---

## 8. Names and package organization

### 8.1 Package and symbol names (Eff)
- **Package name**: short, concise, evocative; lowercase, one word, no underscore or mixedCaps. Prioritize brevity, since everyone types it. Do not worry about collisions a priori: the importer can rename locally. It is the base name of the directory (`encoding/base64` → `base64`) (Eff p.4).
- **Avoid repeating the package in the symbol.** Access is `package.Name`: `bufio.Reader`, not `BufReader`. Package `ring` with one main type: constructor `ring.New`, not `NewRing` (Eff p.4).
- **Long names do not make code more readable**; a good doc comment is worth more (Eff p.4).
- **Getters without `Get`**: field `owner` → `Owner()`; setter `SetOwner` (Eff p.4). Getters/setters are neither required nor forbidden.
- **One-method interfaces** → method + `-er` (Eff p.5). **Canonical names** (`Read`, `Write`, `Close`, `Flush`, `String`): use only with the same signature and meaning. If your type does the same as a well-known method, use the same name (`String`, not `ToString`) (Eff p.5).
- **Avoid `import .`**; tolerable only in tests that must run outside the package under test (Eff p.4).

### 8.2 Project organization
- Subpackage in a subdirectory; the package name equals the directory's; import by full path (Little p.53–54). Executable in `main/` with `package main`, running `go run main/main.go` (author's preference) (Little p.54).
- **Cyclic import is forbidden by the compiler.** Solution: extract shared structures to their own package (e.g., `models`) that does not import the root package or its subpackages (Little p.54–56), and/or use interfaces (Little p.59).
- **[DATED: Little]** Little assumes go1.3.3 and **GOPATH**: import paths and workspace structure described there do not represent the current modules model. Eff (2009) also predates modules. The sources read do not cover `go.mod`; consult the RN/current documentation before advising on module structure, version or layout. The principles of package naming and cycle breaking remain valid [inference].

### 8.3 Tree: where to put a shared type?
1. **Do two packages need the same type and one already imports the other?** → extract to its own package with no dependencies on the project (Little p.55–56).
2. **Do they only need behavior, not the type?** → interface in the consumer (Little p.59) [inference].

---

## 9. Formatting and fmt

### 9.1 Formatting
- **Let the machine format.** Formatting is "the most contentious but least consequential"; a single style saves time. If gofmt's result looks odd, reorganize the code (or report a bug), do not work around it (Eff p.2). The standard library goes through gofmt (Eff p.3). Layout doubt → run gofmt and accept (Eff p.2).
- Tabs for indentation; **no line limit** (if it gets long, break and indent with one extra tab); **no parentheses** in `if`/`for`/`switch`; shorter operator precedence (`x<<8 + y<<16`) (Eff p.3).
- Comments: `//` is the norm; `/* */` for package comments, inside an expression or to disable large blocks (Eff p.3).
- **Opening brace on the same line** as `if/for/switch/select`; on the next line, automatic `;` insertion breaks the code (Eff p.5–6).
- **[DATED: Eff]** The description of package comments and doc comments is from 2009. If the agent needs current documentation rules (doc comment formatting), check the RN; do not assume.

### 9.2 Printing with fmt (Eff p.22–25)
- Families: `Print/Println/Printf`; `Fprint*` (any `io.Writer`, e.g., `os.Stdout`, `os.Stderr`); `Sprint*` (returns a string) (Eff p.22).
- `Println` puts a space between arguments and a newline. `Print` only inserts a space when neither side is a string (Eff p.22).
- `%d` etc. do not ask for size/sign flags; the argument type decides (Eff p.22–23).
- **Default format for any value: `%v`.** (Eff p.23)
- **Control a type's format** → define `String() string`. To print both T and *T, the `String` receiver must be a value (Eff p.24). See also section 1.4.
- Variadic arguments: `fmt.Sprintln(v...)`; without `...` the slice goes as a single argument. A variadic can have a specific type (`...int`) (Eff p.25).
- **Numeric conversions are explicit** when the function requires a specific type (`int64(count)`) (Little p.69).

---

## 10. Control flow and functions (general idioms)

### 10.1 Control flow
- **The happy path goes down the page; errors exit early** (guard clauses), eliminating `else` (Eff p.6–7). Operational rule: the `if` body ends in `break/continue/goto/return` → omit the `else` (Eff p.6).
- Braces are mandatory, which favors simple multi-line `if` (Eff p.6).
- Initialization statement in `if`/`switch` limits scope: `if err := f(); err != nil` (Eff p.6).
- if-else-if-else chain → expressionless `switch` (≡ `switch true`) (Eff p.9). Multiple values in a case → comma-separated list; there is no automatic fall-through (Eff p.9–10).
- Exit a loop from inside a `switch` → label on the loop and `break Label`; a plain `break` only exits the switch. `continue` with a label only in loops (Eff p.10).
- `for`: three forms; `range` for array/slice/string/map/channel; `for k := range m` (key only); `for _, v := range` (value only) (Eff p.8). `range` over a string decodes UTF-8 by code point; invalid encoding consumes 1 byte and yields U+FFFD (Eff p.9).
- There is no comma operator and `++/--` are statements → multiple variables in the `for`, with parallel assignment (`i, j = i+1, j-1`) (Eff p.9).
- **[DATED: Eff]** `range` over integers and functions (iterators) and the change in loop variable semantics are not in Eff; see Spec p.88-91, RN1.22 p.1-2 and RN1.23 p.1 (details in `versoes-e-migracao.md` §2).

### 10.2 Functions
- Return multiple values instead of passing a pointer to simulate a return (Eff p.11–12).
- **Name results** when that documents which is which (`(value, nextPos int)`) or simplifies the code (bare `return`), as in `io.ReadFull` (Eff p.12–13). Interaction with defer: a closure can change a named result (section 6).
- **Discard values** with `_` whenever the return is not used (Little p.25), since an unused variable is a compile error (Little p.24). Example: `if _, err := os.Stat(path); ...` (Eff p.36).

### 10.3 Initialization
- Package variables can use expressions computed at run time (Eff p.27).
- `init()` → set up state impossible to express in declarations and verify/repair state before execution (Eff p.28).

### 10.4 Blank identifier in development
- Not-yet-used imports/variables: `var _ = fmt.Printf` / `_ = fd` right after the imports, with a comment reminding to clean up (Eff p.37–38).
- Import only for the side effect: `import _ "net/http/pprof"` (Eff p.38).

---

## 11. Conflicts between sources and known gaps

**Conflicts / tensions to resolve in the answer to the user**
| Topic | Source A | Source B | Suggested resolution |
|---|---|---|---|
| In doubt, pointer | Little p.37 | Eff p.24, p.29 (value vs pointer by context) | Treat Little as a beginner's heuristic; decide by semantics/size/consistency [inference] |
| Returning an interface | Eff p.32–33 (only in the "type exists only to implement an interface" case) | The "return struct" convention is in no source read | Follow Eff only in the strict case; otherwise [inference] return the concrete type |
| Project structure | Little p.53–56 (GOPATH, go1.3.3) | Current modules (outside the sources read) | Keep the principles, ignore the workspace layout **[DATED: Little]** |
| Goroutine in a loop with a closure | Eff p.42–43, p.44 | RN1.22 p.1; Spec p.88 (per-iteration variable) | Review old examples in light of RN1.22 |
| `panic(nil)` | Spec p.105 (causes a run-time panic) | Eff p.50–51 (describes recover without this case) | Follow the Spec; the version of introduction (1.21) comes from RN1.21 p.3 |
| Errors and type switch | Eff p.49 | RN1.20 p.6, p.10 (`errors.Join`, multiple `%w`, `Unwrap() []error`) | Cite RN1.20 for composite errors; the rest of wrapping is not in the sources |

**Gaps (nothing in the sources read)**
- `context`, cancellation, `sync.WaitGroup`/`errgroup`, `sync.Once`/`Pool`.
- Generics: the Spec covers syntax, type sets and inference (see `regras-da-spec.md` §4); no source gives a guide on when to use generics.
- Modules (`go.mod`), versioning, `internal/`, modern project layout.
- Tests, benchmarks, race detector, profiling (only `import _ "net/http/pprof"` is mentioned, Eff p.38).
- Tools and novelties of RN 1.20–1.24: handled in `versoes-e-migracao.md`, not in this file; version claims must cite the RN with a page.

**General rule for the agent.** If the question touches generics, modules, chained errors, `context`, loop variable or the scheduler, treat Eff and Little as **[DATED]** historical context and seek confirmation in the Spec and the RN (via `regras-da-spec.md` and `versoes-e-migracao.md`). Tell the user clearly what came from a source and what is [inference].
