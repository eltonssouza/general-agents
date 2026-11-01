# Canonical Rust glossary

Quick-lookup vocabulary of the Rust specialist agent: term in English (as in the book), short definition and source. ALWAYS cite with a prefix: (Book p.N) = The Rust Programming Language (Rust 1.90, 2024 edition), (Ref p.N) = The Rust Reference, (RBE p.N) = Rust by Example; PDF pages. The entries come almost entirely from the Book and RBE; the Ref appears only in three entries (`no_mangle` and neighbors); for fine-grained rules use `regras-da-referencia.md`.

## 1. Ownership and borrowing

- **ownership** — compiler-checked rules that govern memory, at no runtime cost (Book p.83).
- **stack / heap** — the stack is LIFO, fixed-size data only; on the heap the allocator finds space and returns a pointer (Book p.83–84).
- **scope** — the range in which an item is valid (Book p.85).
- **drop** — called automatically when the variable goes out of scope (Book p.87); in C++ the pattern is called RAII (Book p.88).
- **move** — copies the pointer/len/capacity of a `String` and invalidates the original (Book p.91). Avoids **double free**, freeing the same memory twice (Book p.90).
- **clone** — also copies the heap data, explicitly (Book p.93).
- **Copy** (marker for stack-only types) — assignment copies and the original stays valid (Book p.94); `i32` and tuples of only `Copy` are `Copy`, `(i32, String)` is not (Book p.95). As a derivable trait, see section 3.
- **ownership in calls/returns** — passing or returning a value moves or copies, as in assignment (Book p.95–96).
- **reference (`&T`)** — followable address to data of another variable, guaranteed valid for the lifetime of the reference (Book p.98); immutable by default (Book p.27).
- **borrowing** — creating a reference; the borrower is not the owner (Book p.100).
- **dereference (`*`)** — opposite of `&` (Book p.99).
- **mutable reference (`&mut T`)** — allows modifying the borrowed value; requires a `mut` variable (Book p.101).
- **data race** — simultaneous accesses to the same data, at least one a write, without synchronization; Rust prevents it at compile time (Book p.102).
- **dangling reference** — points to memory possibly handed to someone else (Book p.104); the main target of lifetimes (Book p.260).
- **slice** — reference to a contiguous sequence, without ownership; stores start and length (Book p.107, 109–110); `&[i32]` for arrays (Book p.114).
- **string slice (`&str`)** — `&s[start..end]`, end exclusive (Book p.109, 111). A **string literal** is `&str` pointing into the binary, hence immutable (Book p.113).
- **automatic referencing and dereferencing** — in `obj.method()` Rust inserts `&`, `&mut` or `*` (Book p.134–135).
- **shadowing** — a new `let` with an existing name hides the previous one (Book p.37, 49).

## 2. Types and data

- **scalar / compound types** — scalars: integers, float, `bool`, `char` (Book p.53); compound: tuples and arrays (Book p.57).
- **integers** — `i8`..`i128`, `u8`..`u128`, `isize`/`usize` (depend on the architecture); signed in two's complement (Book p.53). Literals `98_222`, `0xff`, `0o77`, `0b1111_0000`, `b'A'`, suffix `57u8` (Book p.54). Division truncates toward zero (Book p.55–56).
- **float** — `f32`/`f64`, default `f64`, IEEE-754 (Book p.55).
- **`bool` / `char`** — `bool` takes one byte (Book p.56); `char` is 4 bytes and a Unicode scalar value, not always a human "character" (Book p.57).
- **tuple / array** — tuple: fixed size, mixed types (Book p.57–58); array: homogeneous, on the stack, `[T; N]` and `[v; N]` (Book p.59).
- **unit (`()`)** — empty tuple, type and value; implicit return (Book p.58).
- **statement vs expression** — a statement returns no value; an expression evaluates to a value (Book p.64).
- **function** — snake_case; definition order irrelevant (Book p.62); parameter = definition, argument = value (Book p.63); return after `->` (Book p.66).
- **`const`** — always immutable, type required, constant expression only (Book p.48).
- **struct / field / instance** — type that groups named values; an instance has concrete values (Book p.116–117).
- **field init shorthand** — `email` instead of `email: email` (Book p.119). **Struct update syntax** `..other` goes last (Book p.120).
- **tuple struct** — fields without names; each one is a distinct type (Book p.121). **Unit-like struct** — no fields, useful for a trait without data (Book p.121–122).
- **method** — called with `.` (Book p.26–27); defined on a struct/enum/trait object, with `self` first (Book p.132). **Associated function** — any function in `impl`; without `self` it is not a method, called with `::` (Book p.26, 136).
- **`impl` block / `Self`** — associates content with the type; `Self` is an alias for it (Book p.133, 137). **Getter** — Rust does not generate it automatically (Book p.134).
- **enum / variant** — a value is exactly one variant, in the enum's namespace (Book p.27, 139–141). A tuple variant becomes a function, usable as a function pointer (Book p.630).
- **`Option<T>`** — `None`/`Some(T)`, in the prelude (Book p.145).
- **DST / unsized** — size known only at runtime (`str`, `dyn Trait`); always behind a pointer (Book p.626). **`Sized` / `?Sized`**: generics get an implicit `Sized`, `?Sized` relaxes it (Book p.626–627).
- **never type `!`** — empty type of diverging functions; coerces to any type (Book p.624–625).
- **type alias** — `type Name = Type;`, a synonym and not a new type (Book p.621–622).
- **newtype pattern** — single-field tuple struct wrapping another type, no runtime cost (Book p.619).
- **`PhantomData`** — "phantom" type parameter (RBE p.161–164).

## 3. Traits and generics

- **generics / type parameter** — abstract type placeholders (Book p.234); `T` by convention, short UpperCamelCase (Book p.239).
- **monomorphization** — concrete code per type used; zero runtime cost (Book p.246–247).
- **trait** — method signatures that define shared behavior, like interfaces (Book p.248).
- **trait bound** — `T: Trait` (Book p.248, 254); other forms (`T: 'a`, `T: ?Sized`, `A + B`) in Appendix B (Book p.700–701).
- **`impl Trait`** — sugar for a bound, in parameter or return position (Book p.254, 256). As a return it is a single opaque type; two uses are different types even with the same signature (Book p.630–632).
- **coherence / orphan rule** — a trait can be implemented for a type only if one of the two is local to the crate (Book p.251).
- **blanket implementation** — trait for every type that satisfies another (`ToString` for `Display`) (Book p.258).
- **associated type** — type placeholder in the trait, like `Item` in `Iterator` (Book p.607). **Default type parameter**: `Rhs=Self` in `Add` (Book p.609–610).
- **operator overloading** — only traits from `std::ops`, no new operators (Book p.609); `Add` has `type Output` (RBE p.163–164, 202–203). Table: `+ Add`, `== PartialEq`, `< PartialOrd`, `[] Index` (Book p.696–698, 702); `&&`, `||`, `?`, `=` cannot be overloaded.
- **fully qualified syntax** — `<Type as Trait>::function(...)` (Book p.616). **Supertrait** — trait that yours depends on (Book p.616).
- **trait object** — `dyn Trait` behind a pointer (`&dyn`, `Box<dyn>`, `Rc<dyn>`) with a method table; allows distinct types in a collection (Book p.542–543, 546; `Rc<dyn Trait>` in particular: Book p.626).
- **static / dynamic dispatch** — static: method known at compile time (monomorphization); dynamic: resolved at runtime via a trait object, with a cost and no inlining (Book p.547).
- **dyn compatibility** — rules for where dynamic dispatch fits; the Book refers to the Reference (Book p.547); default methods returning `self` by value do not work (Book p.557).
- **`self: Box<Self>`** — receiver that takes ownership of the box (Book p.553). **State pattern** — a state object decides behavior; in Rust, structs + traits (Book p.548).
- **OOP in Rust** — encapsulation via `pub` (private by default) (Book p.536–537, 539); inheritance does not exist (Book p.539); polymorphism is more general than inheritance (Book p.539); **bounded parametric polymorphism** = generics + bounds (Book p.540). By the Gang of Four definition, structs/enums with `impl` are objects (Book p.536).
- **`Clone`** — explicit copy, may run arbitrary code; derive requires all fields to be `Clone` (Book p.705).
- **`Copy`** (trait) — bit copy; no methods; requires `Clone` and `Copy` parts (Book p.705–706).
- **`Debug`** — `{:?}`; required by `assert_eq!` (Book p.704).
- **`PartialEq` / `Eq`** — `PartialEq` allows `==` (Book p.704; RBE p.84, 162, 164); `Eq` signals total equality, impossible for floats (NaN) and required by `HashMap` keys (Book p.704).
- **`PartialOrd` / `Ord`** — `partial_cmp` returns `Option<Ordering>`; structs compare field by field (Book p.704–705); `Ord` uses `cmp`, requires `PartialOrd` + `Eq`, used by `BTreeSet` (Book p.705).
- **`Hash` / `Default`** — `Hash` maps to a fixed size, all fields `Hash` (Book p.706); `Default` calls `default` per field, with `..Default::default()` (Book p.706; RBE p.188).
- **derive** — `#[derive(...)]`; `Display` is not derivable; libraries offer their own derive via procedural macro (Book p.703; RBE p.84, 162).
- **`Display` / `fmt`** — one trait per format: `{}`, `{:?}`/`{:#?}`, `{:b}`, `{:x}`/`{:X}`, `{:o}`; implemented with `write!(f, ...)` (RBE p.8, 10, 12, 16–17, 199, 260). `ToString` comes from `Display`, do not implement it directly (RBE p.57).
- **`From` / `Into`, `TryFrom` / `TryInto`** — conversions from `std::convert`; `try_into` returns `Result` (RBE p.53–56). **`FromStr`** — basis of `parse::<T>()`, with `type Err` (RBE p.57–58, 251).

## 4. Lifetimes

- **lifetime** — scope in which a reference is valid (Book p.260). The **borrow checker** compares lifetimes (Book p.261).
- **generic lifetime parameter** — `'a`, short and lowercase (Book p.264).
- **lifetime elision rules** — deterministic compiler cases, not full inference nor programmer rules (Book p.270). **Input/output lifetimes**: on parameters vs return (Book p.270).
- **`'static`** — may live for the whole program; every string literal is `'static` (Book p.273).
- **higher-ranked (`for<...>`)** — higher-ranked lifetimes (Book p.692–693, 700).

## 5. Error handling

- **recoverable vs unrecoverable** — recoverable: report/retry; unrecoverable: symptom of a bug (Book p.210). No exceptions: `Result<T, E>` and `panic!` (Book p.210).
- **unwinding / abort** — on panic, the default cleans up the stack; the alternative is to abort (Book p.211). **Backtrace** via `RUST_BACKTRACE` (Book p.213).
- **`Result<T, E>`** — `Ok(T)`/`Err(E)`, in the prelude (Book p.27, 216–217).
- **`io::Error` / `ErrorKind`** — `.kind()` returns the enum, e.g. `NotFound` (Book p.218–219).
- **propagating the error** — returning the error to the caller (Book p.221). **`?` operator**: returns the function's `Err` or unwraps the `Ok`, passing through `From::from` (Book p.223; RBE p.255–256, 263).
- **`Box<dyn Error>`** — trait object for "any error" (Book p.227, 332).
- **`Termination`** — trait that `main` may return; `report` returns `ExitCode` (Book p.227).
- **function contract** — violating the inputs is the caller's bug (Book p.230).
- **`error::Error`** — `impl Error for T {}` suffices with `Debug` + `Display` (RBE p.262–263).
- **`Option`/`Result` combinators** — `unwrap`, `expect`, `map`, `and_then`, `flatten`, `or_else`, `ok_or`, `map_err`, `ok()`, `transpose` (RBE p.236–253, 258–269).

## 6. Collections and strings

- **`Vec<T>`** — contiguous values of the same type (Book p.188); `Vec::new()` needs an annotation, `vec![]` infers (Book p.188). `push` requires `mut`, `pop` removes the last (Book p.189, 193).
- **`&v[i]` vs `v.get(i)`** — indexing panics out of range; `get` returns `Option<&T>` (Book p.189–190).
- **enum for heterogeneous types** — `Vec<Enum>` stores distinct data (Book p.192).
- **`str` / `String`** — `str` is the only string type in the core, a UTF-8 slice (Book p.194); `String` is from std, growable, owning, a wrapper of `Vec<u8>` (Book p.194–195, 199).
- **three views of a string** — bytes, `char`, grapheme clusters (Book p.200); clusters require crates (Book p.202).
- **`HashMap<K, V>`** — keys to values by hash, heap (Book p.204–205); `HashSet` in RBE (RBE p.294–295).
- **Entry API** — `entry` returns `Entry`; `or_insert` gives `&mut V` (Book p.207–208).
- **SipHash / `BuildHasher`** — default hasher resistant to DoS, not the fastest; alternatives implement `BuildHasher` (Book p.209).
- **text and `Vec` methods in RBE** — `push_str`, `replace`, `trim_matches`, `split_whitespace`, `lines`, `from_utf8_lossy`, `first`, `iter_mut` (RBE p.50, 96, 257, 275, 277–279, 290, 295, 297–298; `from_utf8_lossy` is at RBE p.315).

## 7. Closures, iterators and functions

- **closure** — anonymous function that captures values from the scope of definition (Book p.353, 355).
- **`Fn` / `FnMut` / `FnOnce`** — implemented automatically according to how the body treats the captured values (Book p.361). `FnMut`: mutates the environment, does not move out (Book p.363, 365). `FnOnce`: moves out, called once (Book p.364). `sort_by_key` requires `FnMut` (Book p.363). RBE: closure bounds (RBE p.97–102).
- **`move` (closure)** — forces taking ownership of what it uses (Book p.360, 692–693); in RBE, `mem::drop(x)` in the closure forces capture by value (RBE p.96–98).
- **function pointer `fn`** — a type, not a trait; implements `Fn`, `FnMut`, `FnOnce` (Book p.628–629).
- **`Box<dyn Fn(i32) -> i32>`** — unifies closures with the same signature (Book p.632).
- **iterator** — walks a sequence and knows when it ends (Book p.367); **lazy** until consumed (Book p.367).
- **`Iterator` trait** — type `Item` and `next(&mut self) -> Option<Self::Item>` (Book p.368).
- **consuming adapters** — exhaust the iterator (`sum`, `collect`) (Book p.369–370). **Iterator adapters** — produce another iterator (`map`, Book p.370; `filter`, Book p.372).
- **`iter` / `into_iter` / `iter_mut`** — `&T`; values by ownership; `&mut T` (Book p.369).
- **zero-cost abstraction** — no runtime overhead (Book p.381).
- **combinators in RBE** — `enumerate`, `rev`, `any`, `find`, `position`, `take_while`, `zip`, `chain`, `cycle`, `filter_map`, `partition`, `map_while`, `collect()` (RBE p.14, 66–68, 105–109, 208–209, 212, 228, 268–269, 303, 314).

## 8. Smart pointers

- **pointer / smart pointer** — a pointer holds an address; `&` only borrows, with no overhead (Book p.408). A smart pointer has extra capabilities, generally owns, and implements `Deref` and `Drop` (Book p.408).
- **`Box<T>`** — data on the heap, pointer on the stack (Book p.410); RBE: recursive types, `Box::new(x)` (RBE p.37, 171).
- **recursive type / cons list** — needs indirection to have a known size (Book p.411); cons list comes from Lisp, base `Nil` (Book p.411–412).
- **`Deref` / `DerefMut`** — customize `*` via `deref(&self) -> &Self::Target` (Book p.417, 420–421, 423).
- **deref coercion** — `&T` becomes `&U` if `T: Deref<Target=U>` (Book p.421–422).
- **`Drop` / destructor** — `drop(&mut self)` on leaving scope, in the prelude (Book p.424–425); destructor is the general term (Book p.426–427). RBE: `mem::drop` brings it forward (RBE p.167–168, 205, 215).
- **`Rc<T>`** — multiple owners, single-thread, outside the prelude (Book p.429, 432); `strong_count`/`weak_count` (Book p.433, 450).
- **interior mutability** — mutating through an immutable reference with encapsulated `unsafe` (Book p.435); `Mutex<T>` does this for threads (Book p.482).
- **`RefCell<T>`** — borrows checked at runtime, a violation causes `panic` (Book p.435); `Ref`/`RefMut` come from `borrow`/`borrow_mut` (Book p.443).
- **test double / mock** — substitute in tests; a mock records calls (Book p.437).
- **memory leak** — Rust is memory safe, but does not guarantee avoiding leaks (Book p.447).
- **`Weak<T>`** — from `Rc::downgrade`, gives no ownership; `upgrade()` returns `Option<Rc<T>>` (Book p.450–451).

## 9. Concurrency and async

- **fearless concurrency** — concurrency errors become compile errors (Book p.457).
- **thread** — part of the program that runs simultaneously (Book p.459); std is **1:1** (Book p.459). **Race conditions / deadlocks** (Book p.459).
- **`thread::spawn` / `JoinHandle<T>`** — closure of the new thread; `join()` blocks until it finishes (Book p.459, 461; RBE p.300, 306).
- **channel / `mpsc`** — `tx`/`rx`, closed if one half is dropped (Book p.467); multiple producer, single consumer (Book p.468). `recv` blocks, `try_recv` does not (Book p.469).
- **Mutex / `MutexGuard`** — mutual exclusion with a lock (Book p.475); the guard implements `Deref` and `Drop` (Book p.476–477); **poisoned** if another thread panicked while holding the lock (Book p.476, 678).
- **`Arc<T>`** — like `Rc`, safe across threads, with atomic cost (Book p.481); `Mutex`/`Arc` is to threads what `RefCell`/`Rc` is to a single thread (Book p.482).
- **`Send` / `Sync`** — markers: ownership transferable between threads; `T: Sync` iff `&T: Send` (Book p.483). Composites inherit; raw pointers are not `Send` (Book p.483).
- **parallelism vs concurrency** — alternating tasks vs progressing simultaneously (Book p.487–488). **CPU-bound vs I/O-bound** (Book p.485–486).
- **future / `Future`** — value that may not be ready (Book p.490); **lazy**, does nothing until `await` (Book p.492).
- **`async` / `await`** — `async` marks interruptible blocks; `await` is postfix (`expr.await`) and a pause point (Book p.490, 492).
- **polling / `Poll`** — `poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>`; `Ready` or `Pending` (Book p.490, 520–521).
- **runtime / executor** — Rust does not embed a runtime; the executor runs async code (Book p.494, 496). **`trpl`**: the book's crate over `futures` and `tokio` (Book p.491).
- **`trpl::block_on`** — blocks until the future completes; transition from sync to async (Book p.495, 504).
- **`trpl::select` / `Either`** — the first future to finish; `Either` does not imply success (Book p.497–498).
- **`trpl::spawn_task`** — analogous to `thread::spawn` (Book p.499–501). **`join` / `join!`** — complete when all complete, output as a tuple, fair alternation (Book p.501–502, 509). **`trpl::channel`** — `rx` mut, `recv()` produces a future (Book p.503).
- **starvation / `yield_now`** — a future without await monopolizes the thread; `yield_now` yields to the runtime (Book p.510, 513). **Cooperative multitasking**: each future yields at await points (Book p.513).
- **stream / `StreamExt`** — asynchronous iteration (Book p.517). Version-dependent: the `Stream` trait is not yet in std (Book p.518, 530); `StreamExt` must be in scope (Book p.518).
- **`Pin` / `Unpin`** — `Pin` guarantees the pointed-to value does not move (Book p.524, 526); `Unpin` is an automatic marker, special case `!Unpin` (Book p.527–528). A **self-referential type** breaks when moved (Book p.525).
- **task / work stealing** — a task is managed by the runtime, not by the OS (Book p.532); work stealing moves tasks between threads (Book p.533).
- **thread pool / `Worker` / `Job`** — threads created ahead of time (Book p.662); `Worker` holds `id` and `JoinHandle<()>` (Book p.670); `Job` = `Box<dyn FnOnce() + Send + 'static>` (Book p.677).
- **compiler-driven development** — write the caller first and follow the compiler's errors (Book p.662, 664).
- **TCP / HTTP** — TCP is the transport, HTTP defines the content; both request-response (Book p.647). `TcpListener::bind` returns `Result` (Book p.648); `incoming()` iterates connection attempts (Book p.648–649). CRLF is `\r\n` (Book p.652).

## 10. Modules, packages and Cargo

- **rustup / rustc / Cargo** — version installer (Book p.9), compiler (Book p.15–16), build system and package manager (Book p.17).
- **crate / crate root** — unit of compilation (Book p.18, 161); the root forms the root module (Book p.161). **Package**: Cargo feature, contains `Cargo.toml` (Book p.160–161).
- **binary vs library crate** — a binary has `main`; a library does not, and "crate" usually means library (Book p.29, 161). **Binary target**: only it allows `cargo install` (Book p.406).
- **Crates.io / registry** — the registry is a local copy of Crates.io data (Book p.31). **dependencies** (Book p.17).
- **Cargo.toml / TOML** — `[package]` and `[dependencies]` (Book p.18). **Cargo.lock** pins versions, is not edited (Book p.19, 31).
- **SemVer** — `0.8.5` is `^0.8.5`, >=0.8.5 and <0.9.0 (Book p.30).
- **debug vs release** — `target/debug` vs `--release` (Book p.19, 21). **Release profiles** `dev`/`release`; **`opt-level`** 0 in dev and 3 in release (Book p.384).
- **prelude** — std items in every program (Book p.25).
- **module tree** — under the implicit `crate` module; parent, child, siblings (Book p.166). **Paths**: absolute starts at `crate`/crate name; relative at `self`, `super` or local (Book p.167).
- **re-exporting (`pub use`)** — brings in and exposes the name, decoupling internal structure from the API (Book p.180, 390, 394). **Glob (`*`)** (Book p.183).
- **documentation comment** — `///` documents the following item via rustdoc (Book p.386); `//!` the containing item (Book p.389).
- **yank** — blocks new dependencies on the version without breaking existing `Cargo.lock` (Book p.397).
- **workspace** — packages with a shared `Cargo.lock` and `target` (Book p.399).
- **separation of concerns** — `main.rs` orchestrates, logic in `lib.rs` (Book p.323). **stdout vs stderr** (Book p.349); `eprintln!` goes to stderr (RBE p.6).
- **I/O in RBE** — `File`, `BufReader`, `fs`, `env::args`, `Command` (RBE p.310–326).

## 11. Patterns and control flow

- **`match` / arm** — tests patterns and executes the first arm that matches (Book p.35–36, 148–149). **Exhaustive** (Book p.153); **catch-all** and `_` (Book p.154).
- **`if let` / `let...else`** — `if let` is sugar for `match`; `let...else` requires an `else` that leaves the flow (Book p.157, 159); `while let` in RBE (RBE p.26, 80–87). An `if` condition must be `bool`; blocks are also called arms (Book p.70, 72).
- **loop label** — `'name:` with `break`/`continue` (Book p.77).
- **pattern** — syntax for matching the structure of values (Book p.563). **Refutable / irrefutable**: `let x = 5;` vs `Some(x)` in `if let` (Book p.571).
- **match guard** — extra `if`, only in `match` (Book p.586). **`@` binding** (Book p.589). **`..`** ignores the rest (Book p.585–586). **`_` vs `_name`**: only the second binds (Book p.583–584).

## 12. Macros

- **macro** — the `!` marks a call that generates code (Book p.15). Declarative (`macro_rules!`) and three procedural kinds: derive, attribute-like, function-like (Book p.633). **Metaprogramming** (Book p.633).
- **declarative macro** — like `match` over source code, substitutes at compile time (Book p.634); `#[macro_export]` exposes it (Book p.635). `$x:expr` captures an expression; `$(...),*` repeats (Book p.635–636).
- **procedural macro / `TokenStream`** — receives and produces code; `TokenStream` comes from the `proc_macro` crate (Book p.636–637, 640).
- **`syn` / `quote` / `DeriveInput`** — parsing and generation; `quote!` with `#name` and `.into()` (Book p.640–642).
- **`stringify!`** — expression to string at compile time, without evaluating (Book p.642).
- **attribute-like / function-like** — new attribute with two `TokenStream`s (Book p.643); function-like accepts variable arguments (Book p.644).

## 13. Unsafe and FFI

- **unsafe superpowers** — 5 actions: dereference a raw pointer, call an unsafe function, `static mut`, unsafe trait, `union` fields (Book p.592).
- **raw pointers** — `*const T`/`*mut T`, ignore borrowing, no cleanup (Book p.593); `&raw const`/`&raw mut` create them (Book p.594).
- **safe abstraction** — safe function over unsafe, like `split_at_mut` (Book p.593, 596–599).
- **FFI / `extern`** — `"C"` is the common ABI (Book p.599–600).
- **mangling / `#[unsafe(no_mangle)]`** — exporting to C requires turning off renaming; the attribute is unsafe (Book p.600–601). The Reference says that, before the 2024 edition, `no_mangle` could be used without the `unsafe` qualifier; in 2024 writing `#[unsafe(no_mangle)]` is mandatory, and the same applies to `link_section` and `export_name` (Ref p.639–641). The attribute also exports the symbol publicly (Ref p.639).
- **static variable** — global SCREAMING_SNAKE_CASE, fixed address, unlike `const` (Book p.601–602).
- **unsafe trait** — `unsafe trait` + `unsafe impl` (Book p.603).
- **Miri** — detects undefined behavior at runtime; requires nightly (Book p.604).

## 14. Tests

- **correctness** — the type system does not cover everything (Book p.275).
- **test function** — `#[test]`; `cargo test` builds the runner (Book p.276); RBE: `#[should_panic]`, `#[ignore]` (RBE p.331–336).
- **unit vs integration tests** — unit can test private interfaces; integration only the public API (Book p.306).
- **`#[cfg(test)]`** — compiled only under `cargo test` (Book p.306–307).
- **filtering** — a string passed to `cargo test` filters by name (Book p.278, 303). **Doc-tests** (Book p.278).
- **TDD** — test fails, minimum to pass, refactor (Book p.336).

## 15. Tools, editions and process

- **edition** — key `edition = "2024"` in Cargo.toml (Book p.1, 18); every roughly three years, active ones 2015, 2018, 2021, 2024 (Book p.711). Edition-dependent: features that require a new keyword only in the new ones; the compiler supports the previous ones and dependencies of different editions combine (Book p.711–712). Migration with `cargo fix` (Book p.712).
- **release channels** — Nightly, Beta, Stable (Book p.714); a release every six weeks (Book p.715–716); stable supported for six weeks (Book p.716).
- **feature flag/gate / RFC** — unstable only on nightly (Book p.716, 718); RFC is the proposal process (Book p.717).
- **keywords** — in use (Book p.692–693); `as` does casts, disambiguates a trait and renames in `use`. Reserved: `abstract, become, box, do, final, gen, macro, override, priv, try, typeof, unsized, virtual, yield` (Book p.693).
- **raw identifier `r#`** — keyword as identifier (Book p.694). **Turbofish** `parse::<i32>()` (Book p.700).
- **rustfmt / Clippy / rustfix / rust-analyzer** — ship with Rust (Book p.707–708); rust-analyzer uses LSP (Book p.709–710).
