# Rust: principles, mental models and decision trees

Reference base of the Rust specialist agent, consolidated from The Rust Programming Language (Book, Rust 1.90, 2024 edition) and Rust by Example (RBE). Organized by problem, not by chapter.

**Conventions**
- Citations: `(Book p.N)` and `(RBE p.N)` indicate the page of the source PDF. This file is almost entirely Book and RBE; the only `(Ref p.N)` citation is the edition caveat on temporaries (section 9). Fine-grained language rules: `regras-da-referencia.md`.
- **[inference]** marks links made during consolidation between notes that no note states explicitly. They are working hypotheses, not a rule from the book.
- Rule format: "if X → Y".

## Contents

1. Ownership and borrowing
2. Choosing the data type
3. Strings and collections
4. Error handling
5. Traits and generics
6. Lifetimes
7. Closures and iterators
8. Smart pointers
9. Concurrency
10. State and OOP
11. Pattern matching and control flow
12. Macros
13. Unsafe
14. Modules, crates, Cargo, workspaces and tests
15. Known gaps

---

## 1. Ownership and borrowing

### Principle
Ownership exists mainly to manage heap data: knowing who uses what, minimizing duplication and cleaning up what is no longer used (Book p.84). With a GC the collector frees memory; without one the programmer pairs allocation/deallocation (forgetting leaks, freeing early invalidates, freeing twice is a bug). Rust automates the pairing with scope plus `drop` (Book p.87). A compiler error means "this does not yet do what you want safely"; the errors shown in the book are intentional and lead to the correct version (Book p.6, 47).

### The three rules
1. Every value has an owner. 2. Only one owner at a time. 3. When the owner goes out of scope, the value is dropped (Book p.85).

Assignment, passing to a function and returning move (or copy, if `Copy`) (Book p.95–96). Assigning to an existing variable runs `drop` immediately on the old value (Book p.92). Variables are destroyed in reverse order of creation (Book p.425).

Layout of `String`: pointer, length and capacity on the stack, contents on the heap. `s2 = s1` copies only the three fields and invalidates `s1`; `clone` also copies the heap (Book p.88–93).

### Tree: move, copy, clone or borrow?
- Stack-only, fixed-size, scalar type → `Copy`, trivial copy (Book p.94, RBE p.169–170).
- Type that allocates or manages a resource → moves by default (Book p.94).
- Function only reads or modifies and the caller remains the owner → borrow (`&`/`&mut`) instead of taking ownership; this is idiomatic (Book p.99–100, 107).
- Two independent copies really needed → `clone`, accepting the cost (Book p.91, 94).
- `clone` only to silence the borrow checker in a first draft, small data, single copy → acceptable; optimize later (Book p.326).

Why: Rust never makes an automatic deep copy, so every implicit copy is presumably cheap; `clone` is the visual signal of possibly expensive code (Book p.92, 94).

### Golden rule of borrowing
Either one mutable reference, or any number of immutable ones; and every reference must be valid (Book p.106). Model: many readers OR one writer (Book p.103).
- Two simultaneous `&mut` → E0499; `&mut` with live `&` → E0502, because a reader does not expect changes underneath it (Book p.101–103).
- The borrow lasts from creation to the **last use**, not to the end of the block; `&` followed by `&mut` compiles if the `&` are no longer used (Book p.103–104, RBE p.177–178).
- Several `&mut` in sequence → extra `{}` scope (Book p.102). `&mut` requires a `mut` owner (RBE p.175–176).
- Fields of a borrowed struct are not moved on access (Book p.127). Partial move (`let Person { name, ref age } = p;`) prevents using `p` as a whole; types with `Drop` do not allow it (RBE p.172).

### Slices
A loose index (the `usize` from `first_word`) has no link to the `String` and becomes stale after `clear()` without warning. Returning `&str` ties the result to the data, and the compiler forbids mutating the `String` while the slice lives (Book p.108–113). Slice indices must fall on UTF-8 boundaries (Book p.111).

### Drop and RAII
`drop(x)` from `std::mem` brings the release forward (releasing a lock); manual `.drop()` is forbidden because of double free (Book p.426–428). Implement `Drop` only for your own destruction logic (RBE p.167–168); errors in `drop` do not propagate with `?` (RBE p.204–206).

### Trade-offs
- Static analysis is conservative: it may reject a correct program, since accepting an incorrect one would be worse (Book p.436, 592). Ways out: `RefCell`/`Rc` (section 8) or `unsafe` (section 13).
- Rust does not prevent logic errors: `Rc` cycles and deadlocks remain possible (Book p.447, 482).

---

## 2. Choosing the data type

### Principle
What the compiler can check should go into the type; what it cannot becomes a documented contract with `panic!` (Book p.230). Types that encode invariants (`u32` for non-negative, non-`Option` for required) move checks from runtime to the compiler (Book p.230).

### Tree
- Value is "one among several" exclusive possibilities → **enum**; data goes directly in the variants, with different types and amounts, and each variant becomes a constructor (Book p.140–144, RBE p.32).
- Parts coexist and have meaning → named **struct**; tuples force you to remember `.0`/`.1` (Book p.126–127).
- Naming fields would be verbose, but the type must be distinct → **tuple struct** (Book p.121).
- Implementing a trait without data → **unit-like struct** (Book p.121–122).
- Type safety (units, IDs) at no cost → **newtype** `struct Miles(f64)` (RBE p.154, Book p.621); it also works around the orphan rule (Book p.619).
- Just abbreviating a long type → **type alias**: it is not a new type and does not protect (adding `NanoSecond + Inch` compiles) (RBE p.51, Book p.622–623). Useful example: `io::Result<T>` (RBE p.51, 253).
- Marking unit/state in the type without storage → **PhantomData** with empty enums: `Length<Inch> + Length<Mm>` does not compile (RBE p.161–164).
- Invalid transitions must be impossible → **typestate** (section 10).
- "One or nothing" → `Option<T>`, which replaces `null`: `Option<T>` and `T` are distinct types, so the compiler forces handling absence; non-`Option` types are non-null (Book p.145–147).

### Visibility and encapsulation
- Everything is private by default: hiding details becomes the default and it is clear what can change without breaking clients (Book p.169–170).
- `pub` on a struct does not expose fields (each field decides); `pub` on an enum exposes all variants (Book p.174–175).
- Invariant across fields → private fields and public methods that maintain it; it allows swapping `Vec` for `HashSet` without breaking callers (Book p.537–538). A private field requires a public constructor (Book p.175, RBE p.117); a validating constructor prevents invalid instances (Book p.232).
- Fine-grained reach: `pub(crate)`, `pub(super)`, `pub(in path)` (RBE p.113–116).

### Methods and constructors
- Function that only makes sense for one type → method in `impl` (Book p.131, 133).
- `&self` to read (default); `&mut self` to modify; `self` by value is rare, when it transforms the value and prevents reusing the original (Book p.133).
- `new` is not a special word. Fallible construction → `build` returning `Result`, since many expect `new` never to fail (Book p.329; p.137 says only that `new` is not a special name).
- A struct that **owns** its data uses `String`, not `&str`; storing references requires lifetimes (Book p.122, 124).

### Conversions and derives
- `impl From<A> for B` gives `Into` for free, not the reverse; prefer `From` (RBE p.53–55). Fallible conversion → `TryFrom` (RBE p.56). Text to your own type → `FromStr` + `parse` (RBE p.57–58).
- `as`: integers truncate bits; float to integer saturates since 1.45; `to_int_unchecked` is `unsafe` (RBE p.46–48).
- `Debug` is derived; `Display` is manual, since the compiler does not know what the end user should see (Book p.703, RBE p.9). `Display` generates `ToString` (RBE p.8, 57).
- `Eq`+`Hash` for `HashMap` keys; `Ord` for `BTreeSet` (Book p.704–706). `Copy` is rarely required; what `Copy` does, `Clone` does with an explicit `clone` (Book p.706). It can be `Copy` only if all components are and the type does not manage a resource (RBE p.214–215). Tests with `assert_eq!` require `PartialEq` and `Debug` (Book p.288).

### Numbers and bindings
- Integer: when in doubt `i32`; `usize` for indexing and non-negative counts (Book p.54, 665). Float: `f64`; floats do not implement `Hash` (Book p.55, RBE p.289–293).
- Overflow: do not rely on release wrapping; choose `wrapping_*`, `checked_*`, `overflowing_*` or `saturating_*` (Book p.54–55).
- `let` is immutable by default; `mut` only when it changes, for clarity (Book p.46–48). Transforming a value or type while keeping the name → shadowing; `mut` does not change the type (Book p.49–50). Domain value used in several places → `const` (Book p.48–49). `static mut` requires `unsafe` (RBE p.39).

---

## 3. Strings and collections

### Strings
There is no integer indexing of `String`: the byte index is not always a valid Unicode scalar, and O(1) would not be met (Book p.199–201). Philosophy: correct UTF-8 as the default, with more up-front thought and fewer errors later (Book p.202). Think in terms of "bytes vs char vs grapheme" and choose explicitly (Book p.200–202).
- Parameter that only reads text → `&str`. `trim_matches` returns a slice without allocating; `replace` allocates (RBE p.276–277).
- `push_str` takes `&str` so as not to take ownership; `+` takes ownership of the left side and reuses its buffer (Book p.196–198). `String::from` and `.to_string()` are a matter of style (Book p.195).
- Paths are not UTF-8: `Path`/`PathBuf` use `OsString`; `to_str` returns `Option` (RBE p.307). `env::args` panics on invalid Unicode; use `args_os` if you need to accept it (Book p.317).

### Choosing a collection
- Contiguous ordered list → `Vec<T>`; lookup by key → `HashMap<K,V>` (Book p.188, 204).
- Array `[T; N]` only if the size is fixed and known or you want the stack; when in doubt, vector (Book p.59, RBE p.25–26).
- No duplicates → `HashSet` (wrapper of `HashMap<T, ()>`); ordered → `BTreeSet` (RBE p.294–295).
- Different types in a `Vec`: closed set → enum + exhaustive `match`; open → trait object (Book p.193).
- List of items: normally `Vec<T>` beats a cons list (Book p.412); a recursive type needs `Box` (RBE p.37).

### Vec
- `push` may reallocate the buffer; therefore a reference to an existing element is forbidden during `push` (E0502), and so is inserting/removing inside a `for` over the vector (Book p.191–192). **"Vec + reference" checklist (cover it whenever the error is E0502 with `Vec`)**: (1) is the reference used after the `push`? (2) the `for` over `&v`/`&mut v` holds the whole vector, so do not insert or remove inside the loop (Book p.192).
- `[i]` out of bounds panics instead of reading someone else's memory (Book p.61, 212–213). Index that may overflow → `.get(i)` returns `Option` (RBE p.26).

### HashMap
- `Copy` values are copied; owned values are moved into the map; references require the data to live as long as the map (Book p.206).
- One key, one value: decide between overwriting, keeping or combining; `entry` is cleaner and fits the borrow checker better (Book p.206–208).
- Iteration order is arbitrary (Book p.205, 208). Slow in profiling → swap the hasher; do not optimize before measuring (Book p.209).

---

## 4. Error handling

### Principle
Rust requires acknowledging the possibility of error before compiling (Book p.210). Central question: "who decides?". `panic!` takes the decision away from the caller; `Result` hands it back (Book p.228). That is why `Result` is the good default for a function that can fail (Book p.228).

### Main tree
1. Absence is a normal result, not an error → `Option` (RBE p.232).
2. The caller can and should react → `Result` (Book p.228, RBE p.232).
3. Contract violation (caller's bug) or bad state from which it is not possible to continue → `panic!`, with the contract documented in the API (Book p.229–230).
4. Example, prototype or test → `unwrap`/`expect`/`panic!` are appropriate; in a test, panic is how the test fails (Book p.228). In a prototype, `unimplemented!` is more descriptive (RBE p.232).
5. You know more than the compiler (literal `"127.0.0.1".parse()`) → `expect` documenting the reason; if the source becomes user input, handle it properly (Book p.229).

Refinements:
- Expected failure (parser with malformed data, HTTP rate limit) → `Result`. Unexpected input from the caller → return an error; panic only if continuing is unsafe (Book p.230).
- Programming bug → `panic!`; usage/environment error that the user fixes → `Result` (Book p.328).
- In production, `expect` with context beats `unwrap` (Book p.221, RBE p.232).
- Validation in a constructor: `assert!` with a `# Panics` section when the invalid value is an unrecoverable programming error; `build` → `Result` when the caller needs to handle it (Book p.667–668).

### The `?` operator
- Unwraps the success or returns the error, converting via `From::from` (RBE p.255–256, 263).
- Requires a compatible return: a function returning `()` gives E0277; change the return or use `match` (Book p.225–226).
- Does not convert `Option` to `Result`: use `ok()` or `ok_or()` (Book p.226). On `Option`, `?` returns `None` and allows chaining (`a.job?.phone_number?`) (RBE p.238–239). `Option<Result<..>>` → `.transpose()` (RBE p.257–258).
- `main` may return `Result<(), E>`; the error is printed with `Debug` (RBE p.250).

### Which error type?
- Prototype, or the caller only displays the message → `Box<dyn Error>`: preserves errors of distinct types; cost: type known only at runtime; requires `impl Error` (an empty one suffices, with `Debug` and `Display`) (Book p.332, RBE p.261–262).
- The caller needs to distinguish causes → own **enum** with `Display`, `impl Error` (optional `source()`) and `impl From<...>` per wrapped error; `?` converts on its own. More boilerplate; there are crates to reduce it (RBE p.265–267, Book p.223).
- A good error type: one type for several failures, friendly message, easy to compare, carries data, composes with others (RBE p.259–260).
- Changing the error type → `map_err`; `Option` → `Result` → `ok_or` (RBE p.259–260). A domain alias (`type MathResult = ...`) avoids a pyramid of `match` (RBE p.282–286).

### Error funnel in applications
Internal functions return `Result`; only `main` converts into a message on stderr (`eprintln!`) and a non-zero exit code (`process::exit(1)`) (Book p.330, 332, 349–351). Want the unwrapped value → `unwrap_or_else`; success is `()` and only the error matters → `if let Err(e)` (Book p.334).

### Iterating over Results (RBE p.268–269)
Keep everything → `map(parse).collect::<Vec<_>>()`; ignore failures → `filter_map(... .ok())`; collect errors separately → `map_err(|e| errors.push(e)).ok()`; fail on the first `Err` → `collect::<Result<Vec<_>, _>>()` (also works for `Option`); two groups → `partition(Result::is_ok)`.

### `Option` fallbacks (RBE p.246–248)
Two axes: eager/lazy and preserve/modify. `or(x)` eager, preserves; `or_else(closure)` lazy, preserves; `get_or_insert(x)` eager, modifies; `get_or_insert_with(closure)` lazy, modifies. Pitfall: the eager argument is moved even if unused. Function that already returns `Option` → `and_then` (with `map` it would become `Option<Option<T>>`) (RBE p.243–245).

### Panic
`panic!` normally unwinds the stack running destructors (RBE p.233–235). Smaller binary: `panic = 'abort'` in the release profile; trade-off: no cleanup by the application (Book p.211). `unwrap` in `Drop` can cause a double panic and abort (Book p.683). A test that returns `Result` does not use `#[should_panic]`; to assert `Err`, use `assert!(v.is_err())` (Book p.296).

---

## 5. Traits and generics

### Principle
Generics eliminate duplication by the same process as extracting a function (Book p.237) and cost nothing at runtime thanks to monomorphization (Book p.247). Traits move the "method does not exist" error to compile time (Book p.259, 546).

### Tree: enum, generic or trait object?
- Closed, known set of types → **enum** (Book p.541).
- Homogeneous collection (one concrete type per instantiation) → **generic + bound**, monomorphized (Book p.543).
- Heterogeneous, extensible by third parties or type known only at runtime → **`Box<dyn Trait>`** (Book p.541–543, 546).
- Return with distinct types per branch → `Box<dyn Trait>`; a single concrete type → `impl Trait` (Book p.257, RBE p.200–201, 211–213).

Cost of the trait object: dynamic dispatch and loss of inlining; gain: flexibility (Book p.547). A type that does not implement the trait is rejected at compile time (Book p.546). A bare trait in the return has indefinite size, hence `Box` and explicit `dyn` (RBE p.200–201).

### `impl Trait` vs `T`
- Parameters: `impl Trait` when the arguments may have different types; `T` with a bound when they must be the same (Book p.254–255). Downside: no turbofish (RBE p.210–211).
- Return: essential for closures and iterators with closures (unnamed types) (Book p.256–257, RBE p.211–213); if it returns an iterator that borrows an argument, add `+ 'a`.
- Several bounds → `+`; cluttered signature → `where`, which also accepts bounds on arbitrary types (`Option<T>: Debug`) (Book p.255, RBE p.153).

### Associated type vs trait parameter
- **Associated type**: one impl per type; callers do not annotate the type; avoids repeating parameters in consumers (Book p.608, RBE p.157–160).
- **Generic trait**: several impls per type, with annotation (Book p.608).
- Adding a parameter to an existing trait without breaking impls → default (Book p.611).

### Impl structure
- Method only for a concrete type → `impl Point<f32>`; method conditional on bounds → block `impl<T: Display + PartialOrd> Pair<T>` (Book p.245, 257–258). Struct parameters after `impl`; method ones after `fn` (Book p.246). Without `<T>` after `impl` the impl is concrete (RBE p.147).
- Many generic parameters → split the code (Book p.243). Every generic is `Sized`; for `str`/`dyn Trait` use `T: ?Sized` and `&T` (Book p.627).

### Orphan rule and newtype
A trait can be implemented on a type only if one of the two is local (Book p.251, 619). `Display for Vec<T>` → newtype; all methods of the inner type → `Deref`; to restrict → delegate only what you want (Book p.619–620).

### Reuse without inheritance
- Default methods with override (Book p.539). Supertraits (`trait Student: Person`) require both impls; `&dyn Student` calls both (RBE p.216–218).
- Same-named methods in distinct traits → qualified syntax `<Form as UsernameWidget>::get(&form)` (RBE p.219–220). An inherent method takes priority over a trait one (Book p.612); an associated function without `self` requires the qualified form (Book p.613, 615).
- `a + b` is `a.add(b)` of `Add`; each `impl Add<Rhs> for Lhs` defines `type Output`; swapping the types is another impl (RBE p.202–203). `Iterator` requires only `type Item` and `next` (RBE p.207–209).
- `Clone` is explicit; `Copy` is an implicit bitwise copy and a subtrait of `Clone` (RBE p.214–215).

---

## 6. Lifetimes

### Principle
Annotations **do not change how long a reference lives**; they describe relationships between lifetimes for the borrow checker (Book p.264–265). They go in the signature, part of the contract, not in the body; this way the error points to the right place (Book p.265). The concrete `'a` is the intersection of the scopes, that is, the smallest (Book p.266). Lifetimes are generics (`'a` and `T` in the same `<>` list) and cost zero at runtime (Book p.273–274).

### When to annotate: simulate elision (Book p.271)
1. Each reference parameter gets its own lifetime.
2. If there is exactly one input lifetime, it goes to all outputs.
3. If there are several and one is `&self`/`&mut self`, the one from `self` goes to the outputs.

A reference left without a lifetime → error; the compiler does not guess. Applies to `fn` and `impl`.
- One input reference → do not annotate (RBE p.194). Method with `&self` returning a reference → normally no annotation (Book p.273).
- Free function with two or more input references that returns a reference (`longest`) → annotate, deciding which parameter the return is borrowed from and linking only that one. The compiler's suggestion to use the same lifetime everywhere may be wrong (in `search`, only `contents` links to the return) (Book p.272, 337–338).
- Parameter that does not influence the return → no shared lifetime (Book p.267–268). The return must match some parameter, otherwise it would be a reference to a local value (Book p.268, RBE p.184–185).
- Struct or enum with a reference → `struct Borrowed<'a>(&'a i32)`, annotating all reference fields; the `impl<'a>` redeclares it and uses it after the type name (Book p.269, 272, RBE p.187–188).
- Compiler "does not see" that the result comes from the longer argument → the fix is not in the body; the signature already states the smaller lifetime (Book p.267).

Origin: before 1.0 everything was explicit; repetitive patterns were moved into the compiler and more may appear (Book p.270).

### `'static`
- As a reference lifetime: lives for the whole program (literals, `static`); can be coerced to a shorter one (RBE p.191–192). `Box::leak` creates `&'static` at runtime without ever freeing (RBE p.192).
- As a bound `T: 'static`: the type contains no non-static references; owned data always satisfies it, a reference to it generally does not (RBE p.193). That is why `thread::spawn` and `execute` require `'static` (Book p.464–466, 666).
- Compiler suggests `'static` → check whether the reference really lives for the whole program; in general it is a dangling reference or incompatible lifetimes, and the fix is at the cause (Book p.273).

### Bounds and coercion
`T: 'a` says the references inside `T` live at least `'a` (RBE p.189). `<'a: 'b, 'b>` reads "`'a` lasts at least as long as `'b`"; pitfall: reading it backwards (RBE p.190). A short lifetime does not become a long one (RBE p.183). A variable's lifetime is not a scope: it goes from creation to destruction (RBE p.181).

---

## 7. Closures and iterators

### Principle
Closures do not need type annotations: they are not an exposed interface, they are short, and the compiler infers one concrete type per parameter, fixed at first use (Book p.355–358, RBE p.93). Annotating is optional (Book p.356).

### Which Fn trait?
Determined by what the **body** does with what it captures (Book p.361, 363–365):
- moves a value out → only `FnOnce`;
- mutates without moving out → `FnMut`;
- only reads or captures nothing → `Fn`.
Every closure implements at least `FnOnce`. The capture is the least restrictive possible: `&T`, `&mut T` or `T` (RBE p.94–96). A closure that mutates requires `let mut` (RBE p.95).

### Which bound to require in your own API?
- Accepting a function or closure → generic with an `Fn*` bound, not `fn`; `fn` only to interoperate with C (Book p.629).
- Calls once → `FnOnce` (accepts all, like `unwrap_or_else`); several times with mutation → `FnMut` (like `sort_by_key`) (Book p.362).
- Several times without mutating, e.g. in concurrency → `Fn`. **[inference]** extrapolated from the Book examples (p.361–362); the note itself marks it as inferred.
- Choose the most permissive one the function really requires (Book p.366). From most restrictive: `Fn`, `FnMut`, `FnOnce` (RBE p.97–98).
- A closure has an anonymous type, hence the mandatory generic (RBE p.100). Ordinary functions satisfy `Fn()` (RBE p.101). No capture → pass the function (`unwrap_or_else(Vec::new)`, `map(ToString::to_string)`), same generated code; choose for clarity (Book p.362, 629–630).

### Returning and storing closures
- One → `impl Fn...`, with `move` if it captures (RBE p.102, Book p.630).
- Several with the same signature in the same container → `Box<dyn Fn...>`, since each `impl Trait` is a distinct opaque type (Book p.631–632).
- Closure for another thread → `move`; without it main could drop the value and the reference would become invalid (Book p.360–361, 464–466).

### Iterator vs loop
- Prefer iterators: less boilerplate and fewer index errors, works for non-indexable sequences, minimizes mutable state (Book p.368, 379–380). Equivalent performance: the book's benchmark ~19.6 ms (for) vs ~19.2 ms (iter) (Book p.381).
- `for x in collection` beats `while` with an index (bounds check per iteration, risk of panic); repeat N times → `(1..4).rev()` (Book p.79–80).
- Pipeline: source → lazy adapters → consumer (`collect`, `sum`, `for`) (Book p.367, 369–371).
- Result consumed incrementally → return `impl Iterator<Item = &'a str>` instead of `Vec` (Book p.379). Function that must own the items → receive `impl Iterator<Item = String>` instead of a slice, avoiding `clone` (Book p.376–377). Only reads → `&[T]` (RBE p.25–26).
- `for` applies `into_iter`: `iter()` borrows, `into_iter()` consumes, `iter_mut()` modifies in place (RBE p.67–68). Pitfall: `find` over `iter()` receives `&&i32` (RBE p.105–107).
- Loops: `for` > `while` > `loop`; `loop` with `break value` suits retry (Book p.76, 78–80). `break`/`continue` act on the innermost loop, unless labeled (Book p.76–77). Many `else if` → `match` (Book p.73).

---

## 8. Smart pointers

### Decision table
| I need... | Use | Notes |
|---|---|---|
| Heap, single owner | `Box<T>` | No extra overhead (Book p.416) |
| Several owners, read-only, 1 thread | `Rc<T>` | `Rc::clone(&a)` only increments a counter (Book p.432) |
| Interior mutation, runtime checking | `RefCell<T>` | Error only at runtime, small overhead (Book p.444) |
| Several owners and mutation, 1 thread | `Rc<RefCell<T>>` | Speed traded for flexibility (Book p.444–446) |
| Several owners across threads | `Arc<T>` | Atomic, costs performance (Book p.481, RBE p.298) |
| Shared mutation across threads | `Arc<Mutex<T>>` | `Mutex` is the thread-safe `RefCell` (Book p.446, 475) |
| Non-owning reference (child → parent) | `Weak<T>` | Breaks cycles (Book p.450, 452) |

### When `Box<T>` (Book p.410)
1. Type of unknown size where an exact size is required (recursive). 2. Lots of data with ownership transferred without copying. 3. Owning a value that matters only because it implements a trait (trait object). A lone `i32` on the heap is rarely worth it; prefer the stack (Book p.411).

### Comparison (Book p.436)
Owners: `Rc` multiple; `Box` and `RefCell` one. Checking: `Box` mutable and immutable at compile time; `Rc` only immutable at compile time; `RefCell` both at runtime. `RefCell` mutates the interior even when immutable.

### Tree
- You know who finishes last → that one is the owner, normal rules suffice; you do not know → `Rc` (Book p.429).
- Compiler rejects code that you know respects the borrows → `RefCell`; useful for mocks (Book p.436, 441). Compile-time checking remains the best in most cases (early errors, no cost) (Book p.435).
- Graphs and trees: only ownership edges are strong (parent → child `Rc`), the others `Weak`; dropping the child must not drop the parent, but the reverse should (Book p.450, 452). If all edges must be ownership, there is no reorganization: care and tests (Book p.450).

### Deref
`deref` returns a reference so as not to move out of `self` (Book p.421). Deref coercion is resolved at compile time, at no cost. `&mut T` → `&U` holds; `&T` → `&mut U` never (it would require an exclusivity that does not exist) (Book p.423).

### Pitfalls
- A leak is memory safe; `Rc`+`RefCell` cycles are not detected and are a logic bug (Book p.447, 450).
- `Rc` is not `Send`; the error "`Rc<...>` cannot be sent between threads safely" → swap to `Arc`, same API (Book p.481, 483).
- Prefer `Rc::clone(&a)` over `a.clone()` to distinguish a cheap clone from a deep copy when hunting performance problems (Book p.432).

---

## 9. Concurrency

### Principle
Threads bring performance and complexity: unguaranteed ordering, race conditions, deadlocks, bugs that are hard to reproduce (Book p.459). Rust mitigates with ownership and with `Send`/`Sync`, the only concurrency concepts built in; the rest is library (Book p.483–484). Many solutions are crates that evolve faster than std (Book p.484).

### Tree: threads, channels, Arc<Mutex> or async?
1. CPU-bound and parallelizable (data in independent parts) → **threads** (Book p.533).
2. I/O-bound and highly concurrent (messages from several sources at different rates) → **async**; a thread per download scales poorly with blocking I/O (Book p.486, 533).
3. Both → combine (video on a dedicated thread, UI notified through an async channel) (Book p.533–534).
4. Between threads, transferring data → **channel** (single ownership); sharing state → **`Arc<Mutex<T>>`** (multiple ownership, more complex) (Book p.475).
5. Counter or simple number → atomics, not `Mutex` (Book p.482).

### Threads
- The end of main terminates all spawned threads (Book p.460); keep the `JoinHandle` and `join` it if it needs to complete (Book p.461, RBE p.300). `join` before main's loop serializes (Book p.462–463).
- `spawn` closures need `move`; `move` swaps the default of borrowing for moving and does not violate ownership (Book p.464–466).
- Map-reduce: one thread per chunk returning a value, reduction at `join` (RBE p.301–304). Number of threads dependent on the input → cap with a constant. In production `thread::Builder::spawn` returns `Result` instead of panicking (Book p.671–672).

### Channels and Mutex
- `send` takes ownership of the value, and the `Result` indicates a dropped receiver; handle it in a real app (Book p.469–471). `recv` blocks; `try_recv` in a loop when there is other work to interleave (Book p.469).
- Several producers: clone the `Sender` (RBE p.305–306). `Receiver` does not clone; several workers on one queue → `Arc<Mutex<Receiver>>` (Book p.675).
- `Mutex<T>` prevents access without `lock`; the guard releases on `Drop`, so lock/unlock is not forgotten. Remaining risk: **deadlock** (Book p.475–477, 482). `lock` fails if the holder panicked (Book p.476).
- Temporaries: in `let x = expr;` they die at the end of the `let`; in `while let`, `if let` and `match` they live until the end of the block, possibly holding a lock (Book p.680). Edition caveat: in 2024 the `if let` scrutinee is dropped before the `else` (Ref p.490–491); the Book's generalization holds for `while let`/`match`, not for the `else` of `if let` in 2024.

### Thread pool (Book p.662–684)
- Limit threads (one per request allows DoS); design the usage API first (Book p.662–663).
- `execute<F: FnOnce() + Send + 'static>`: `FnOnce` (job runs once), `Send` (crosses threads), `'static` (unknown duration) (Book p.666).
- Graceful shutdown: dropping the `sender` closes the channel and every `recv` fails; workers leave the loop and the pool's `Drop` does `join` (Book p.683–684). Independent of how the work is executed (Book p.681).
- Taking a field out of `&mut self`: `Option::take`, or `Vec::drain(..)` on collections; `Option` only if the need is real (Book p.682–683).
- "If it compiles, it works" is not universal: an empty pool compiled and did nothing; write tests (Book p.667).

### Async
- Futures are lazy; `await` starts it and only there does the runtime switch tasks; between awaits it is synchronous (Book p.492, 510). In an async block execution is linear; concurrency requires separate futures and `join` (Book p.505).
- `main` cannot be `async` (it needs a runtime); runtime macros rewrite it (Book p.494–496).
- Each async block becomes an anonymous type (state machine); mixing them in a `Vec` requires trait objects (Book p.493, 522–523). `Pin` prevents moving the possibly self-referential state machine; `Unpin` is the normal case, `!Unpin` the special one (Book p.523–528). Pin matters to those who build runtimes; day to day, just fix the errors (Book p.529).
- No need for an independent task → async blocks + `join`, no task or thread (Book p.501). An un-awaited `spawn_task` runs until the end of the async main (Book p.500).
- `join!` with a number of futures known at compile time; `join_all` (with `Pin`/trait objects) when only known at runtime (Book p.509, 522).
- `join` is fair; `select` from `trpl` is not and favors argument order: put the priority one first (Book p.502, 515).
- `async move` when the block must own something to drop it (`tx`) or uses borrowed parameters (Book p.493, 507–508). Program that does not terminate: `rx_fut` completes only when all `tx` are dropped, and `tx` is only dropped at the end of the block that awaits the `join` (Book p.506–507).
- `yield_now` only yields; `sleep` waits for time. Slicing CPU-bound work with awaits gives fairness but costs overhead; measure (Book p.513–514). Streams: Iterator + Future = `Poll<Option<Item>>`; import `StreamExt` for `next` (Book p.518, 530).
- Hierarchy: thread = boundary of synchronous operations; task = of asynchronous ones; future = granular unit (Book p.532). Async is complementary to threads and usually combines with them; threads cost memory and may not exist on embedded systems without an OS (Book p.486, 532).

---

## 10. State and OOP

### Principle
The Book treats OO as tools: encapsulation through private fields (section 2), reuse through default methods and polymorphism through generics or trait objects (section 5). OO patterns are "not always the best solution" in Rust, because of ownership (Book p.561).

### Tree: modeling states
- Few, fixed states → **enum** with `match`; viable, but each consumer repeats the `match` (Book p.556).
- Requirements change and you want to touch only one place → **state pattern** with `Option<Box<dyn State>>` and `take()`: each state owns its rules and transitions (Book p.548, 553, 557).
- Misuse must be impossible (reading a draft as published) → **typestate** (`DraftPost` → `PendingReviewPost` → `Post`): methods consume `self` and return the next type; a method that does not exist in the wrong state does not compile (Book p.558–561).

### Trade-offs
| Approach | Gain | Cost |
|---|---|---|
| Enum | Simple, closed | Repeated `match` (Book p.556) |
| State pattern (`dyn`) | Local rules per state (Book p.548, 557) | Coupled states (inserting `Scheduled` forces changing `PendingReview`), duplicated logic, invalid transitions become runtime no-ops, requires `take()` (Book p.553, 557) |
| Typestate | Invalid transition does not compile | Caller reassigns (`let post =`); transitions are no longer encapsulated (Book p.559–561) |

- Growing duplication in the transitions → consider a macro (Book p.557–558).
- **[inference]** `PhantomData` with empty enums (RBE p.161–164) and the Book's typestate (p.558–561) exploit the same idea (state in the type); RBE does not present it as typestate.
- No implementation inheritance: reuse through default traits; hierarchy of contracts through supertraits (RBE p.216–218).

---

## 11. Pattern matching and control flow

### Principle
A pattern "matches the shape" of the data and only then uses parts of it (Book p.563). Each place of use (`let`, parameter, `for`, `match`, `if let`, `while let`) is a pattern slot (Book p.564–569). `match` descends the value through the arms in order until the first one that matches (Book p.148–149).

### Tree
- Exhaustiveness checked → `match` (prevents forgetting `None`) (Book p.153).
- Only one pattern matters → `if let` (less code, no checking) (Book p.156–157); `if let ... else if let` for independent conditions (Book p.566–567).
- The unmatched case should exit early → `let...else`; the `else` must diverge (Book p.158–159, RBE p.85).
- Repeat while it matches → `while let` (RBE p.86–87).
- `let`, parameters and `for` accept only **irrefutable** patterns; `if let`/`while let`/`let...else` accept refutable ones and the compiler warns if they are irrefutable (Book p.571–573).

### Wildcards and bindings
- Catch-all: a name if you use the value, `_` if not; it must be the last arm (Book p.154–155). `_x` still binds/moves; `_` does not (Book p.583–584).
- `|` for a few values, `..=` for contiguous ranges, only numeric and `char` (Book p.575–576).
- A guard `if` does not count toward exhaustiveness (Book p.567, RBE p.78). To compare with an outer variable, use a new name and a guard; the same name would shadow (Book p.587–588).
- `id @ 3..=7` binds and tests a range, preserving exhaustiveness (Book p.589, RBE p.79–80).
- `..` once per tuple (Book p.585–586); a struct without all fields requires `..` (RBE p.77); slices `[first, middle @ .., last]` (RBE p.72). Dereferencing uses `*`; destructuring uses `&`, `ref`, `ref mut` (RBE p.74–75).

### Expressions
Without `;` the block evaluates to the last value; with `;` it evaluates to `()` (Book p.66, 68). Pitfall: `;` on the last line of an `if` branch changes the type to `()` and breaks the equality between branches (RBE p.61). `if` requires `bool` (Book p.72). `!` converts to any type (RBE p.110–111).

---

## 12. Macros

### Principle
Macros accept a variable number of parameters and expand before the compiler interprets the code, and can implement a trait for a type (a function runs at runtime; the trait must exist at compile time) (Book p.633). They expand to AST, not text, without precedence bugs (RBE p.221). With no reflection to obtain the type name at runtime, generating an `impl` with the name requires a macro (Book p.638).

### Tree
- No variadics and no code generation → **function** (Book p.633).
- DRY, small DSL, variadic interface by syntax matching → **`macro_rules!`** (Book p.634, RBE p.221).
- Complex token analysis (validating SQL), new attribute or derive → **procedural** (Book p.634, 643–644): `derive` only on structs/enums and receives 1 `TokenStream`; attribute-like works for other items and receives 2 (attribute and item); function-like receives 1 (Book p.637, 643–644).

### Trade-offs
- Harder to read and maintain (Book p.633–634). They must be in scope before use; functions need not (Book p.634).
- Procedural ones require their own crate (`proc-macro = true`); the restriction may be lifted in the future (Book p.636, 638–639). Convention: `foo` → `foo_derive`; the name in `proc_macro_derive(Name)` is usually the trait's (Book p.638, 640).

### Practice
- `macro_rules!`: designators (`ident`, `expr`, `ty`, `pat`, `block`, `item`, `literal`, `tt`...), several arms like `match`, repetition `$(...),+`/`*`, recursion with base case and head/tail (RBE p.222–226, 231). Real cases: generating nearly identical functions and tests (RBE p.227–229); `lazy_static` and `clap` (RBE p.230).
- Procedural derive: `TokenStream` → `syn::parse` → `DeriveInput` → `quote!` → `.into()` (Book p.640–642). The outer function only parses; the inner one transforms (Book p.640). The return is `TokenStream`, not `Result`; the example uses `unwrap`, and in production better messages are worthwhile (Book p.641).

---

## 13. Unsafe

### Principle
The compiler's analysis is conservative; `unsafe` is the escape hatch when you know something it does not (Book p.592). **`unsafe` does not turn off the borrow checker**; it only unlocks five actions (Book p.592–593), which serve as a checklist of where UB may lurk. RBE summarizes four uses: dereferencing raw pointers, calling `unsafe` functions (including FFI), accessing `static mut` and implementing `unsafe` traits (RBE p.343–344).

### Contract in three roles (Book p.595–599, 602)
- Whoever writes `unsafe fn` documents the contract in a `SAFETY` comment.
- Whoever calls it in `unsafe {}` asserts having read and fulfilled the contract.
- Whoever wraps it in a safe function guarantees the contract internally. Inside `unsafe fn`, unsafe operations still require an `unsafe` block (Book p.596); comment each one (Book p.602).

### Tree
- Needs unsafe → small block, isolated in a safe abstraction, so it does not "leak" (Book p.593, 596, RBE p.343–344).
- Interface with C → `extern` block with `#[link]`, safe wrapper, `#[repr(C)]` on the exchanged structs (RBE p.327–329). Raw pointers serve FFI and safe abstractions that the borrow checker does not understand (Book p.595).
- Raw pointer to a local → `&raw const`/`&raw mut`; avoid `address as *const T` (Book p.594).
- Global mutable state → prefer concurrency primitives over `static mut` (Book p.603); if unavoidable, documented `unsafe` functions, access through raw pointer (Book p.602–603).
- Validate with Miri: finding a problem is a bug; not finding one does not prove absence, since it only sees executed code (Book p.606).
- `slice::from_raw_parts` requires a valid pointer and the correct type (RBE p.343–344). `asm!` is always `unsafe`, with pitfalls of registers and labels (RBE p.345–356).

---

## 14. Modules, crates, Cargo, workspaces and tests

### Mental model
- Module tree ≈ file system: `crate` = `/`, `super` = `..` (Book p.166, 168, 173).
- Privacy: children see ancestors, ancestors do not see the child's internals (Book p.169). `pub` on a module only lets you refer to the module; the contents remain private (Book p.171).
- `use` is a symbolic link in the scope where it appears and does not affect which files compile (Book p.176, 186). `mod` is not include: declare once (Book p.185, RBE p.123–125).
- Internal structure ≠ exposed structure: `pub use` reorganizes the API without touching the code (Book p.180, 390, 394).

### Imports
- Absolute vs relative: the Book prefers absolute (definition and call tend to change independently); `super::` when item and caller move together (Book p.168, 173–174).
- Function → import the **parent module**; struct, enum and others → full path; name conflict → parent or `as`. It is a convention, with no strong reason (Book p.178–180).
- Nested paths reduce lines (Book p.182). Glob: avoid (hides origin, can break with a new dependency); acceptable in a test module and prelude (Book p.183).
- Files: `name.rs` + `name/`; `mod.rs` is the old style (Book p.185–186).

### Package and workspace
- **Thin binary, thick lib**: `main.rs` orchestrates (args, config, `run`, error); `lib.rs` holds the testable logic (Book p.172–173, 323). `main` is not directly testable, and a binary-only crate cannot be imported by `tests/` (Book p.313, 323).
- Workspace: root with `[workspace]`, no `[package]`; members with their own `Cargo.toml` (Book p.399–400). A single `Cargo.lock` keeps compatible versions; a single `target` avoids recompiling (Book p.400, 402–403). Dependencies between members are declared explicitly (Book p.401).
- The public API is a contract; see the Rust API Guidelines (Book p.172). Publishing is permanent; `yank` does not delete code; leaked secrets must be revoked; the crates.io token is a secret (Book p.394, 396, 398). Common license: `MIT OR Apache-2.0` (Book p.396).
- Workflow: `check` while writing, `build`/`run` when you need the binary, `--release` for delivery/benchmark (Book p.20–21). `dev` with low `opt-level`, `release` high (Book p.384–385). `[dev-dependencies]` do not propagate (RBE p.342). `cargo install` only for binaries from crates.io (Book p.406).

### Tests
- Anatomy: arrange, act, assert (Book p.276). Failure = panic in the test thread (Book p.279).
- Two levels: unit in `mod tests` with `#[cfg(test)]` (sees private items via `use super::*`; testing private functions is debated) and integration in `tests/` (public API; each file is a crate; helpers in `tests/common/mod.rs`) (Book p.306–308, RBE p.340–341).
- `assert_eq!`/`assert_ne!` instead of `assert!(a == b)`, for the message with both values; order does not matter (Book p.285, 287). Unstable text → assert a property (`contains`) (Book p.288–289).
- `#[should_panic(expected = "...")]` for the right panic (Book p.293–294).
- Tests run in parallel; do not share state/files; own resources or `--test-threads=1` (Book p.297–298, RBE p.133–135). Slow → `#[ignore]` (Book p.303–305). Doc tests in `///` are executed (RBE p.337–339).
- TDD: make the test compile with a skeleton (`unimplemented!()`) so it fails for the right reason (Book p.336–337). Refactor in small steps; a returned tuple that is promptly taken apart suggests a struct (Book p.321, 324).

### Process
`rustfmt` ends style discussions (Book p.707). Editions change only the initial parse; crates of different editions link together (Book p.711–712). Only the latest stable is supported; do not fear updating (Book p.714–716). Nightly only per project (`rustup override set nightly`); beta in CI detects regressions (Book p.715, 717). Names: snake_case for functions, variables and files; SCREAMING_SNAKE for constants (Book p.14, 48–49, 62).

---

## 15. Known gaps

- This file practically does not use the Reference (Ref): formal rules (layout, undefined behavior, grammar, exact semantics of lifetimes and coercion) are in `regras-da-referencia.md`.
- Orphan rule: only the newtype workaround was covered (Book p.251, 619).
- Choice of crates (arguments, errors, async runtimes) is out of scope; the sources only cite `clap` and the like (Book p.316, RBE p.323–326).
- RBE items such as `Path`, processes, `fs`, pipes and asm appear summarized (RBE p.307–356).
- Everything marked **[inference]** must be validated against the primary source before becoming a hard rule.
