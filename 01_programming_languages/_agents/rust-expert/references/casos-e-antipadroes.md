# Cases, compiler errors and antipatterns in Rust

Reference base derived from "The Rust Programming Language" (Book, Rust 1.90, edition 2024), "The Rust Reference" (Ref) and "Rust by Example" (RBE). Citations in the format (Book p.N), (Ref p.N), (RBE p.N), using the PDF page. No Ref material went into this file; only the Book and RBE had error cases. Passages marked **[inference]** are my own connections, not claims made by the sources.

## Contents

1. [Conventions and usage notes](#conventions-and-usage-notes)
2. [Part 1: Compiler error code table](#part-1-compiler-error-code-table)
   - 1.1 Move and ownership
   - 1.2 Borrows and mutability
   - 1.3 Lifetimes
   - 1.4 Types and inference
   - 1.5 Traits and generics
   - 1.6 Smart pointers and interior mutability
   - 1.7 Concurrency and async
   - 1.8 Unsafe
   - 1.9 Patterns and exhaustiveness
   - 1.10 Modules, visibility and imports
   - 1.11 Lints and warnings
   - 1.12 Runtime panics
3. [Part 2: Antipatterns and common mistakes](#part-2-antipatterns-and-common-mistakes)
4. [Part 3: Illustrative cases from the books](#part-3-illustrative-cases-from-the-books)

## Conventions and usage notes

- Compiler messages change between versions; what matters is the cause (Book p.9). The message texts below are approximations of the books' examples.
- Codes that only appear in a version-specific context: the text of E0433 ("use of unresolved module or unlinked crate") and the hint "use `cargo add`" come from the Book 1.90 compiler output (Book p.176–177). The `static_mut_refs` lint is deny-by-default in the context of Book 1.90/edition 2024 (Book p.602). The `try` keyword is reserved from the 2018 edition on, and `try!` only compiles in the 2015 edition (Book p.694–695; RBE p.256, 358).
- Where the notes give only the message, with no E0xxx code, the code column carries the name of the situation or of the lint, and I do not invent codes.
- Fixes are in order of preference: the first is the most idiomatic according to the source.

# Part 1: Compiler error code table

## 1.1 Move and ownership

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0382 (simple move) | "borrow of moved value: `s1`" after `let s2 = s1;` or after passing `s` to a function | `String` is not `Copy`; the assignment or the call moves ownership | Use only the new owner; pass `&s`; `s1.clone()` if you need both; return ownership in the return value | Book p.91, 95, 99 |
| E0382 (operators and collections) | Use of `s1` after `s1 + &s2`; variables invalid after `map.insert(a, b)`; collection used after `into_iter()`; argument of `or`/`get_or_insert` reused | `+`, `insert`, `into_iter` and by-value functions consume the operand | `format!` or clone beforehand; insert references (with valid lifetimes); iterate by `&`/`iter()` | Book p.197–198, 206; RBE p.68, 246–247, 297 |
| E0382 (closure/thread/channel) | "use of moved value" after `move ||`; `val` used after `tx.send(val)`; `Mutex` or `Receiver` moved "in previous iteration of loop" | `move` and `send` transfer ownership; single ownership cannot go to several threads | Do not use after moving; clone beforehand; `Arc` (and `Arc<Mutex<Receiver<_>>>`) with `Arc::clone` per thread. The compiler's hint to take the expression out of the loop does not solve the real problem | Book p.466, 470–471, 478, 675–676; RBE p.96 |
| E0382 (partial move) | "borrow of partially moved value: `person`" | Moving a field out of a struct and then using the whole struct | Avoid the partial move (clone the field) or use only the remaining fields **[inference]** | RBE p.172 |
| E0382 (shared list) | "use of moved value: `a`" when making two lists point to `a` with `Box` | `Box` moves ownership | `Rc<List>` with `Rc::clone(&a)` (references would require lifetimes) | Book p.431–432 |
| E0507 (FnMut closure) | "cannot move out of `value`, a captured variable in an `FnMut` closure" in `sort_by_key` | The closure moves a captured variable out, so it is only `FnOnce`, and `sort_by_key` requires `FnMut` | Do not move out of the environment (use a `+= 1` counter); clone if the cost is acceptable | Book p.364–366 |
| E0507 (JoinHandle) | "cannot move out of `worker.thread` which is behind a mutable reference" | `join` consumes the handle and only `&mut` is available | `self.workers.drain(..)`, or `Option<JoinHandle>` with `take()` | Book p.682–683 |
| Move out of `&mut self.state` (no code in the notes) | `self.state = self.state.request_review()` does not compile | You cannot move out of a borrowed field | `Option<Box<dyn State>>` with `take()` to get and put back; `as_ref().unwrap()` on `&self` | Book p.553, 555 |
| Move out of a type with `Drop` (no code in the notes) | "cannot move out of a type which implements the `Drop` trait" | Moving a field out of a type with a destructor would leave `Drop` inconsistent | Clone or use by reference | RBE p.172 |
| (no code) `Copy` denied | Error when deriving `Copy` on a type whose parts implement `Drop` | `Copy` and `Drop` are incompatible | Explicit `Clone` | Book p.94 |
| E0040 | "explicit use of destructor method" on `c.drop()` | A manual call would cause a double free | `drop(c)` (`std::mem::drop`) | Book p.426–427 |

## 1.2 Borrows and mutability

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0384 | "cannot assign twice to immutable variable" | Reassignment to an immutable binding | `let mut x` (the compiler already suggests it) | Book p.47 |
| E0596 (parameter) | "cannot borrow `*some_string` as mutable, as it is behind a `&` reference" | Mutating through `&T` | `&mut String` parameter, `mut` variable, `&mut s` at the call | Book p.100–101 |
| E0596 (variable) | "cannot borrow `x` as mutable, as it is not declared as mutable" | `&mut` of an immutable variable | `let mut x`; if outward immutability is a requirement, interior mutability. `new_edition(&mut immutabook)` is the same error | Book p.437; RBE p.176 |
| E0596 (`&self` trait) | "cannot borrow `self.sent_messages` as mutable, as it is behind a `&` reference" in the mock | The trait's `send(&self)` prevents `push` on a `Vec` | `RefCell<Vec<_>>`; do not change to `&mut self` just because of the test | Book p.441–442 |
| E0499 | "cannot borrow `s` as mutable more than once at a time" | Two `&mut` with overlapping uses | Finish using the first; `{}` scope | Book p.102 |
| E0499 (split_at_mut) | "cannot borrow `*values` as mutable more than once" when reimplementing `split_at_mut` in safe Rust | The borrow checker cannot prove that the slices do not overlap | Use the std `split_at_mut`; or `unsafe` with `from_raw_parts_mut` and `add`, after `assert!(mid <= len)` | Book p.597–598 |
| E0502 | "cannot borrow `s` as mutable because it is also borrowed as immutable" | `&` alive when `&mut` appears; `v.push` with `&v[0]` still in use; `s.clear()` with a slice in use | The last use of the `&` must occur before the `&mut`; use the reference before the `push`; do not mutate the string while the `&str` lives. Copying the value instead of referencing it (e.g. `let first = v[0]` when the type is `Copy`) is an **[inference]**, supported only by Book p.94 (`Copy`) and p.190: the adjacent pages do not propose this | Book p.103–104, 112–113, 190–191; RBE p.178 |
| Closure with captured `&mut` (no code) | `println!` between creating the closure and calling it gives an error | The closure's mutable borrow blocks any other use | Only use the variable after the closure's last call | Book p.360 |
| (no code) | Moving the `Box` while a live reference exists | The move would invalidate the reference | Finish using the reference before moving | RBE p.174 |
| (no code) | `usize` index becomes stale after `clear()`, with no compile error | The value is not tied to the string | Return `&str` (slice), which the compiler tracks | Book p.109–112 |

## 1.3 Lifetimes

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0106 (return) | "missing lifetime specifier" on `fn longest(x: &str, y: &str) -> &str` or `search(query, contents) -> Vec<&str>` | Elision cannot tell which input the return comes from | Annotate only what is related: `longest<'a>(x: &'a str, y: &'a str) -> &'a str`; in `search`, `'a` only on `contents`. Do not blindly accept the `'a` on everything that the compiler suggests | Book p.263, 272, 338 |
| E0106 (dangle) | "missing lifetime specifier" on `fn dangle() -> &String` | Returning a reference to a local that will be dropped | Return an owned `String`; `'static` is suggested but unusual | Book p.105–106 |
| E0106 (field) | Struct with `username: &str` | Reference field without a lifetime | `String` for now; lifetimes on the struct (`ImportantExcerpt<'a>`) when needed | Book p.123–124, 269 |
| E0597 | "`x` does not live long enough" (also `result` used after `string2` goes out of scope; `&i` passed to `impl Debug + 'static`) | Reference outlives the owner | Reorganize scopes so the owner lives longer; pass the owned value when the bound is `'static` | Book p.261, 267; RBE p.183, 185, 193 |
| E0515 | "cannot return value referencing local variable" with `result.as_str()` | The return points to data created in the function | Return an owned type (`String`). Annotating a lifetime unrelated to the parameters does not fix it | Book p.268 |
| E0373 | "closure may outlive the current function, but it borrows `v`" in `thread::spawn` | The thread requires `'static`; the closure captured by reference | `move ||` | Book p.464–465 |

## 1.4 Types and inference

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0308 (input) | "expected `&String`, found `&{integer}`" in `cmp` | Comparing read text with a number | `trim().parse()` to the numeric type; shadowing | Book p.36–37 |
| E0308 (mut does not change type) | `spaces = spaces.len();` ("expected `&str`, found `usize`") | `mut` allows a new value, not a new type | Shadowing with a new `let` | Book p.50–51 |
| E0308 (return) | `-> i32` function ending in `x + 1;` ("expected `i32`, found `()`") | The `;` turned the final expression into a statement | Remove the final `;`; the same error catches `if`/`match` branches with an extra `;` | Book p.68; RBE p.61 |
| E0308 (condition) | `if number {` with an integer ("expected `bool`") | Rust does not convert an integer to bool | `number != 0` | Book p.72 |
| E0308 (branches) | `if c { 5 } else { "six" }` ("incompatible types"); `match` with `5` and `"hello"` | All branches have a single type | Make the types equal; `continue`/`panic!` arms are fine because they are `!` | Book p.74, 624–625 |
| E0308 (closure) | Closure `\|x\| x` called with `String` and then with `5` | The first use fixes the type | Same type, or distinct closures; the compiler suggests `5.to_string()` | Book p.357–358 |
| E0308 (generic) | `Point { x: 5, y: 4.0 }` with `Point<T>` | Only one parameter `T` | `Point<T, U>` | Book p.242–243 |
| E0308 (opaque) | "expected opaque type, found a different opaque type" in `vec![f1(), f2()]` | Each function with `impl Fn` has its own opaque type | `Box<dyn Fn(i32) -> i32>` with `Box::new` | Book p.631–632 |
| E0308 (arity) | "expected a tuple with 3 elements, found one with 2" in `let (x, y) = (1,2,3)` | The pattern's arity differs | Make them equal, or `_`/`..` | Book p.565–566 |
| E0284 | "type annotations needed" in `"42".parse().expect(..)` | The compiler cannot infer the target | `let guess: u32`. Likewise untyped `None` (`Option<i32>`), `.into()` without a target, `let x: Sheep = Animal::new(..)` | Book p.52, 146; RBE p.54, 197, 280 |
| E0277 (Option) | "cannot add `Option<i8>` to `i8`" | `Option<T>` is a different type | Handle the variant with `match`, `if let` or methods | Book p.146–147 |
| E0277 (reference) | "can't compare `{integer}` with `&{integer}`" in `assert_eq!(5, y)` | Number against a reference | `*y` | Book p.418 |
| E0277 (str) | "the type `str` cannot be indexed by `{integer}`" in `s1[0]` | Strings are UTF-8; an integer index is ambiguous | `.chars().nth()`, `.bytes()` or a range slice | Book p.198–199 |
| E0277 (`?`) | "the `?` operator can only be used in a function that returns `Result` or `Option`" | `main` returns `()` | `fn main() -> Result<(), Box<dyn Error>>` and a final `Ok(())` (in a test: return `Result<(), E>`) | Book p.225–227; RBE p.332 |
| E0072 | "recursive type `List` has infinite size" (with E0391 for a cycle in drop) | Recursive variant without indirection | `Box<List>` (the compiler also lists `Rc`, `&`) | Book p.413–415 |
| E0614 | "type `MyBox<{integer}>` cannot be dereferenced" | `Deref` is missing | `impl Deref` with `type Target = T` and `deref` returning `&self.0` | Book p.420–421 |
| (no code) | `expected expression, found `let` statement` in `let x = (let y = 6);` | `let` is a statement; `x = y = 6` does not exist in Rust | Two separate `let`s | Book p.65–66 |
| (no code) | `let s1: str = "..."`; generic function refuses `str` | A DST cannot be a variable or an argument; implicit `Sized` | `&str`; `T: ?Sized` and `&T` | Book p.626–627 |

## 1.5 Traits and generics

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0277 (Display) | "`Rectangle` doesn't implement `std::fmt::Display`" with `{}` | The struct has no default `Display` | `{:?}`/`{:#?}` with `Debug`, or implement `Display` | Book p.128–129; RBE p.7, 12–13 |
| E0277 (Debug) | "`Rectangle` doesn't implement `Debug`" | Derive is missing | `#[derive(Debug)]` | Book p.129 |
| E0277 (trait object) | "the trait bound `String: Draw` is not satisfied" (cast `Box<String>` to `Box<dyn Draw>`) | Type in `Box<dyn Draw>` without the trait | Another type, or implement `Draw` | Book p.546–547 |
| E0277 (supertrait) | "`Point` doesn't implement `Display`" when implementing `OutlinePrint`; `to_string` not found on `&Self` | Supertrait not satisfied or not declared | Declare `trait OutlinePrint: fmt::Display` and implement `Display` | Book p.617–618 |
| E0277 (missing bound) | Generic function called with `Triangle` without `Debug`/`HasArea`; `{:?}` or `==` on a type without derive | The type does not meet the bound | Implement/derive the trait | RBE p.150, 199 |
| E0369 | "binary operation `>` cannot be applied to type `&T`" | Generic without a comparison bound | `T: std::cmp::PartialOrd` | Book p.240–241 |
| E0790 | "cannot call associated function on trait without specifying the corresponding impl type" on `Animal::baby_name()` | Function without `self` is ambiguous | `<Dog as Animal>::baby_name()` | Book p.615 |
| (no code) | "multiple `get` found" | Same-named methods in two traits | `<Type as Trait>::method(&x)` | RBE p.220 |
| (no code) | `impl Trait` in the return with `NewsArticle` on one path and `SocialPost` on another | `impl Trait` accepts a single concrete type | Trait object `Box<dyn Trait>` | Book p.256–257 |
| (no code) | `impl Display for Vec<T>` in your crate | Orphan rule: the type or the trait must be local | Newtype `Wrapper(Vec<String>)` | Book p.251, 619 |
| (no code) | Default method in `State` returning `self` does not compile for a trait object | The concrete `Self` is unknown (dyn compatibility) | Repeat impls per type, or another pattern | Book p.557 |
| E0599 (trait not in scope) | "no method named `next` found for struct `tokio_stream::iter::Iter`" | `StreamExt` not imported | `use trpl::StreamExt;` | Book p.518–519 |
| E0599 (missing) | "no function or associated item named `new`" / "no method named `execute`" | Not yet implemented | Implement in the `impl` | Book p.665–666 |

## 1.6 Smart pointers and interior mutability

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| (runtime) | Panic "already borrowed: BorrowMutError" | Two active `borrow_mut`; it compiles but violates the rules at run time | Make sure earlier `Ref`/`RefMut` go out of scope | Book p.443–444 |
| (runtime) | Stack overflow when printing a structure with a cycle; counts stuck | `Rc` to `Rc` cycle via `RefCell`, strong never reaches 0 | `Weak<T>` on the non-owning edge | Book p.449–454 |

## 1.7 Concurrency and async

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0277 (Send) | "`Rc<Mutex<i32>>` cannot be sent between threads safely ... `Send` is not implemented" | `Rc` is not thread-safe | `Arc<Mutex<T>>`. The error is long: focus on the `Send` line | Book p.480–481 |
| E0752 | "`main` function is not allowed to be `async`" | `main` cannot be async | `fn main()` with `trpl::block_on(async { ... })` | Book p.494–495 |
| E0277 (Unpin) | "`dyn Future<Output = ()>` cannot be unpinned" in `Vec<Box<dyn Future>>` for `join_all` | `Box<T>` is only a `Future` if `T: Unpin`; async blocks can be `!Unpin` | `pin!` on each future and `Vec<Pin<&mut dyn Future<Output = ()>>>`; `Box::pin` if the value must live beyond the scope | Book p.523, 528–529 |
| (no code) | Different async blocks in a `Vec` without a trait object | Each block is a distinct type | Pinned trait object (line above) | Book p.522–523 |

## 1.8 Unsafe

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0133 | "call to unsafe function is unsafe and requires unsafe block" | `unsafe fn` outside `unsafe` | Minimal `unsafe {}`, after reading the function's contract | Book p.595–596 |
| `static_mut_refs` (deny by default in the Book 1.90 context) | Error when referencing `static mut`, including the implicit reference in `println!` | References to `static mut` are a UB risk | `&raw const`/`&raw mut`; `#[allow(static_mut_refs)]` only as an exception | Book p.602 |
| UB detected by Miri | "pointer not dereferenceable ... dangling pointer" when using `from_raw_parts_mut` on an arbitrary address | Memory that is not yours | Never do it; use only pointers derived from valid data | Book p.599, 605 |

## 1.9 Patterns and exhaustiveness

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0004 | "non-exhaustive patterns: `None` not covered" (also `match` with guards only) | `match` without all cases; guards are ignored for exhaustiveness | Missing arm or catch-all `_` | Book p.152–153; RBE p.69, 78 |
| E0005 | "refutable pattern in local binding" in `let Some(x) = opt;` | `let` requires an irrefutable pattern | `let ... else { return; }`, `if let` or `match` | Book p.571–572 |
| (no code) | Struct in a pattern without all fields: "pattern does not mention field `x`" | Incomplete pattern | List the field, or `..` | RBE p.77 |
| (no code) | `if let Ok(age) = age && age > 30` does not work (according to the text) | The new `age` only exists after `{` | Nested `if age > 30` | Book p.567 |

## 1.10 Modules, visibility and imports

| Code | Typical symptom | Cause | Fixes (in order) | Source |
|---|---|---|---|---|
| E0603 (module) | "module `hosting` is private" | Module is private to the caller | `pub mod hosting` | Book p.169–170; RBE p.115–116 |
| E0603 (function) | "function `add_to_waitlist` is private" | `pub` on the module does not make its contents public | `pub fn` as well | Book p.171–172 |
| E0433 | "failed to resolve: use of unresolved module or unlinked crate `hosting`" plus an `unused import` warning | `use` only applies in the scope where it appears; moving the function to a child module loses the shortcut | `use` in the child module or `super::hosting`. The hint "use `cargo add hosting`" is a distraction: fix the path | Book p.176–177 |
| E0433 | "use of undeclared type `ThreadPool`" | Type does not exist yet/is not imported | Create the struct in the lib and `use hello::ThreadPool;` | Book p.664–665 |
| E0432 | "unresolved import `rand`" in a workspace crate | Dependency declared only in another member | Add it to the `Cargo.toml` of the crate that uses it | Book p.403 |
| (no code) | Instantiating a struct from another module fails; "`ClosedBox` has private fields" | Private field without a public constructor | Public associated function | Book p.175; RBE p.117 |
| (no code) | `mod.rs` and `name.rs` for the same module | Two styles for the same module | Pick one | Book p.186 |
| (no code) | "expected identifier, found keyword `match`" (or `try`) | Reserved word used as a name | `r#match`/`r#try` in the definition and in the call (2015 calling 2018+) | Book p.694–695; RBE p.358 |
| (no code) | `tests/common.rs` creates a "running 0 tests" section | Each file in `tests/` is a test crate | `tests/common/mod.rs` | Book p.311–313; RBE p.341 |

## 1.11 Lints and warnings

| Lint / warning | Symptom | Cause | Fixes | Source |
|---|---|---|---|---|
| `unused_must_use` | "unused `Result` that must be used" | Ignoring the return of `read_line` or `run(config)` | Handle with `expect`/`match`/`if let Err`; `let _ =` ignores explicitly, but the Book prefers handling | Book p.28, 333–334 |
| `unused_must_use` (iterators) | "unused `Map` that must be used" | Lazy adapter without a consumer | `collect` or another consumer; `let _ =` only silences | Book p.371 |
| `unused_mut` | "variable does not need to be mutable" | Unnecessary `mut` | `cargo fix` | Book p.708 |
| `irrefutable_let_patterns` | "irrefutable `let...else` pattern" | Pattern always matches | Remove `else` or use `let` | Book p.573 |
| `clippy::approx_constant` | Clippy error on the literal `3.1415` | Approximates π | `std::f64::consts::PI` | Book p.709 |
| `dead_code` | "field `workers` is never read" | Fields not yet used | Implement the `Drop` that uses the fields | Book p.679, 681 |
| unused import | "unused import: `rand`" | Import not used | Remove/use it; `cargo fix` | Book p.402–403 |
| manifest | "manifest has no description, license" and a 400 error on `cargo publish` | `description` and `license` missing | Fill them in under `[package]` | Book p.395–396 |
| Linker | Linker errors on the first compilation | C compiler/linker missing | Install a C toolchain | Book p.10 |

## 1.12 Runtime panics

| Panic | Cause | Fix | Source |
|---|---|---|---|
| `index out of bounds: the len is 5 but the index is 10` | Index coming from runtime; Rust aborts instead of reading invalid memory | `get`; prefer `for`; validate size | Book p.60–61, 79–80, 190, 213 |
| `byte index 1 is not a char boundary` | Slice in the middle of a multibyte character (the block 2 Book only says "exit with an error") | Limits on a character boundary | Book p.111, 201 |
| `ParseIntError { kind: InvalidDigit }` via `expect` | `expect` crashes on `Err` | `match` + `continue` | Book p.40–41 |
| Integer overflow | Debug: panic; release: silent wrap (u8 256 becomes 0) | Choose a type suited to the range **[inference]** | Book p.54 |
| `unwrap` on `None`/`Err` | Lack of context | `expect("reason")`; handle the error | Book p.220–221; RBE p.237, 249, 280 |
| `poll` after `Ready` | Many futures panic | Do not repeat `poll` | Book p.521 |
| Failing `#[should_panic]` | "test did not panic as expected" or "panic did not contain expected string" | Code did not panic, or the message differs | Book p.293, 295 |

# Part 2: Antipatterns and common mistakes

## Variables, types and control flow
- Leaving the secret's `println!` in the game's final code: remove debugging before shipping (Book p.34, 42).
- `while` with an index to traverse a collection: it can panic if the size and the condition diverge and it is slower; use `for` (Book p.79–80).
- Expecting `x = y = 6` to work or `let` to return a value, as in C/Ruby (Book p.65–66); expecting `mut` to change the type, when the way is shadowing (Book p.50–51).

## Ownership, borrows and strings
- Loose `usize` index (`first_word`): it becomes stale. Return a slice and use `&str` as the parameter to accept `String`, `&String`, slices and literals (Book p.107–114).
- Parameters separated by dimension (`area(width, height)`): group them in a struct (Book p.126–127).
- Indexing `String` by integer or slicing without looking at the UTF-8 boundary (Book p.198–201).
- Keeping a reference into a `Vec` and calling `push`: reallocation would invalidate the reference (Book p.190–191).
- Inserting into a `HashMap` and continuing to use the moved values (Book p.206); forgetting the `*` in `*count += 1` (Book p.208).
- Returning a reference to a local and "fixing" it by annotating a lifetime: no annotation solves it, return the owned value (Book p.268). Accepting the `'a` on all parameters suggested by the compiler without thinking about the real relationship (Book p.338).

## Errors, `Option` and `Result`
- `unwrap` with a generic message: prefer `expect("reason")` (Book p.220–221). In production, avoid `unwrap` for I/O, `lock`, `recv`, `send`, parsing and file reading; only in a teaching example (Book p.648, 651, 653, 677–678). Inside `Drop` it risks a double panic (Book p.683).
- `expect` with a single message for any read failure: it hides the cause; propagate with `?` (Book p.322, 332).
- `panic!("not enough arguments")` in `Config::new` and `args[1]` without validation: messages for the programmer; return `Result` (Book p.327–329).
- Deep `match` on `Result`: use `unwrap_or_else` with closures (Book p.219). Checking an environment variable with `unwrap`/`expect` when all that matters is that it is set: use `is_ok()` (Book p.347).
- Error messages on stdout go to the file when redirecting with `>`; use `eprintln!` (Book p.349–350).
- Guards and `if let` without `else` let cases pass silently; use `match` without a guard when exhaustiveness matters (Book p.567, 587). A catch-all before other arms makes them unreachable (Book p.154).

## Modules and organization
- `use` all the way to the function: it obscures the origin; bring in the parent module (Book p.178). Glob `use x::*`: opaque names and fragile to upgrades; reserve it for tests or a prelude (Book p.183).
- `main` with several responsibilities and many variables in scope (Book p.321–322).
- Mixing `mod.rs` and `name.rs` for the same module (Book p.186).
- Trusting that `cargo yank` removes leaked secrets (Book p.398).

## Smart pointers and traits
- `a.clone()` on `Rc` where the convention is `Rc::clone(&a)` (Book p.432).
- `RefCell` as a shortcut to escape the borrow checker when static checking would do (Book p.435–436).
- Cons list instead of `Vec<T>` in real code (Book p.412).
- Expecting Rust to prevent leaks: `Rc` cycles leak; use `Weak<T>` (Book p.447, 450).
- Expecting struct inheritance: it does not exist without a macro; use a trait with default methods plus generics or trait objects (Book p.539). Calling the default from inside the overriding method is not possible (Book p.253).
- Trait object when all elements have the same type: `Screen<T: Draw>` is enough (Book p.543).
- Using an iterator after `sum`, or forgetting `let mut` for `next` (Book p.369–370).

## Concurrency and async
- Forgetting `join` (threads die with `main`) or putting it too early (removes the concurrency) (Book p.460–462).
- Moving a single `Mutex`/`Receiver` to several threads; use `Arc` (Book p.478, 675–676). A `Mutex` deadlock passes the compiler (Book p.482).
- Holding a `MutexGuard` longer than necessary: in `while let`/`if let`/`match` the temporary guard lasts the whole block; use `let job = ...recv().unwrap();` (Book p.680, 685).
- Thread per connection without a limit (Book p.662–663). Thinking that "it compiled means it works" (Book p.667).
- Async: forgetting `.await` (Book p.492); a single block with sends, sleeps and then `recv` runs linearly, use separate blocks with `join` (Book p.505–506); a `recv` loop that does not end because `tx` was not dropped, use `async move` (Book p.506–508); a blocking function in async causes starvation, insert `yield_now` (Book p.513) or move the blocking work to its own thread with an async channel (Listing 17-25, Book p.533); the book only *names* `spawn_blocking` as part of the runtime (Book p.532) and does not explain it (Book p.510–511).

## Unsafe
- A large `unsafe` block makes the memory bug hard to find; use minimal blocks and a safe abstraction (Book p.593).
- `safe fn` without the guarantee actually existing is a false promise to the compiler (Book p.600).
- `from_raw_parts_mut` on an arbitrary address and integer-to-pointer casts (Book p.599, 605). Suppressing `static_mut_refs` for convenience instead of `&raw const/mut` (Book p.602).

## Tests
- `#[should_panic]` without `expected` can "pass" for the wrong reason (Book p.293). `assert!` without a custom message gives weak diagnostics (Book p.289–290).
- Parallel tests that write the same file fail because of interference, not a bug (Book p.297). A failing unit test prevents integration tests and doc-tests (Book p.310).
- `to_lowercase` covers basic Unicode but is not 100% exact (Book p.344). A server that always answers the same HTML without reading the request (Book p.655).

# Part 3: Illustrative cases from the books

## Book, chapters 1 to 3: getting started and common concepts
- **Guessing game** (Book p.24–43): built in layers (input, `rand`, `cmp` + `match`, shadowing + `parse`, `loop`, `break`, `match` on `Result` with `continue`). Lesson: handle invalid input without crashing. `gen_range(1..=100)` is an inclusive range and requires `use rand::Rng`; the Book pins `rand = "0.8.5"` and warns that >=0.9.0 does not guarantee the API (Book p.30, 33).
- **Control flow** (Book p.73–80): `if` as an expression (Listing 3-2); `loop` returning a value (`break counter * 2`); label `'counting_up`; `for` over an array and `(1..4).rev()` are safer than `while` with an index (Listings 3-3 to 3-5).

## Book, chapter 4: ownership
- **`String` move** (Figures 4-1 to 4-4, Book p.88–92): ptr/len/cap copied, heap not; double free never occurs because `s1` is invalidated. Reassignment drops the old value immediately (Book p.92–93).
- **`clone` vs `Copy`** (Book p.93–94) and **`takes_ownership`/`makes_copy`/`gives_ownership`** (Listings 4-3/4-4, Book p.95–96): who copies and who moves.
- **`calculate_length`** (Listing 4-5, Book p.97–99): the ceremony of returning ownership, eliminated by `&String`.
- **`change(&s)`** (Listing 4-6, Book p.100): E0596. **`r1`/`r2`/`r3`** (Book p.102–104): E0499 and E0502; the reference's scope ends at its last use.
- **`dangle()` vs `no_dangle()`** (Book p.104–106): dangling reference rejected; returning `String` solves it.
- **`first_word`** (Listings 4-7 to 4-9, Book p.107–114): from a loose `usize` to a slice and to `&str` as the parameter.

## Book, chapters 5 and 6: structs, enums and match
- **`User`** (Listings 5-1 to 5-7, Book p.117–120): mutability of the whole instance, shorthand, `..user1` with partial move. `Color`/`Point` and `AlwaysEqual` (Book p.121–122): tuple struct and unit-like struct.

## Book, chapter 7: modules
- **`restaurant`** (Listings 7-1 to 7-22, Book p.165–186): absolute/relative paths, privacy, `super`, `Breakfast`/`Appetizer`, `use`, `pub use`, extraction into files. `backyard` (Book p.164) shows the `src/garden/vegetables.rs` layout.

## Book, chapters 8 and 9: collections and errors
- **Listing 8-6** (Book p.190–191): `&v[0]` + `push` shows why the borrow checker protects against reallocation. **Listing 8-9** (Book p.192): `SpreadsheetCell` enum for heterogeneous types in a `Vec`.
- **Strings** (Listings 8-18/8-19, Book p.197–201): `+` uses deref coercion `&String` to `&str`; "Здравствуйте" has 12 letters and 24 bytes, `&hello[0..4]` gives "Зд" and `&hello[0..1]` panics; "नमस्ते" has 18 bytes, 6 chars and 4 grapheme clusters (the PDF extraction lost some of the combining marks).
- **Errors** (Listings 9-5 to 9-9, Book p.218–224): handle `NotFound` by creating the file; the same function at four levels (`match`, `?`, chained `?`, `fs::read_to_string`). `?` on `Option` (Listing 9-11) and `main` returning `Result<(), Box<dyn Error>>` (Listing 9-12) (Book p.226–227).

## Book, chapter 10: generics, traits and lifetimes
- **`largest`** (Listings 10-1 to 10-5, Book p.234–241): function extraction; `largest<T>` requires `PartialOrd`. **`mixup`** (Listing 10-11, Book p.245–246): generics of the `impl` vs of the method. **`Option_i32`/`Option_f64`** (Book p.247): monomorphization.
- **`Summary`** (Listings 10-12 to 10-14, Book p.248–253): impl for two types, a default method that calls a required method. **`Pair<T>`** (Listing 10-15, Book p.257–258): `cmp_display` conditional on `Display + PartialOrd`.
- **Lifetimes** (Listings 10-16 to 10-24, Book p.260–269): dangling reference with `'a`/`'b` scopes; `longest<'a>` compiles with nested scopes and fails if `result` is used after `string2` dies; `ImportantExcerpt<'a>` does not outlive `novel`.
- **Elision** (Book p.270–274): `first_word` with and without annotation; `longest` where elision is not enough; `level` (rule 1) and `announce_and_return_part` (rule 3); `longest_with_an_announcement<'a, T>` with `where T: Display`.

## Book, chapters 11 to 14: tests, minigrep, closures and Cargo
- **Tests** (Book p.276–313): `adder` and `Rectangle::can_hold` (a `<` in place of `>` is caught by the test); `greeting`/`Guess::new` with `should_panic` and `expected`; `--show-output`; filtering in `add_two`; `internal_adder` tests a private function; `tests/common/mod.rs`.
- **minigrep** (Book p.315–351): CLI with `env::args`, `fs::read_to_string`, `Config`, `Result`, `Box<dyn Error>`, `lib.rs` + `main.rs`, TDD, `env::var`, `eprintln!`.
- **Closures** (Book p.353–366): `giveaway` with `unwrap_or_else(|| self.most_stocked())`; `add_one_v1..v4`; `thread::spawn(move || ...)`; `sort_by_key` with `Fn`/`FnMut`/`FnOnce` (moving a captured `String` fails, a `+= 1` counter works).
- **Iterators** (Listings 13-12 to 13-22, Book p.369–381): manual `next`, `sum`, `map` without consumption, `collect`, `shoes_in_size`; minigrep rewritten with `impl Iterator<Item = String>`; the `for` vs iterator benchmark shows equivalent performance.
- **Cargo** (Listings 14-1 to 14-6, Book p.387–406): `///` and `//!`; `pub use` flattens `art::kinds::PrimaryColor` into `art::PrimaryColor`; `cargo publish` of `guessing_game`; `add` workspace (`-p`, single lock, E0432); `cargo install ripgrep`.

## Book, chapter 15: smart pointers
- **`Box` and cons list** (Listings 15-1 to 15-5, Book p.411–415): infinite size without `Box`. **`MyBox<T>` with `Deref`** (Listings 15-6 to 15-13, Book p.417–423): `hello(&m)` via deref coercion vs `hello(&(*m)[..])`.
- **`Drop`** (Listings 15-14 to 15-16, Book p.425–427): reverse order; `c.drop()` forbidden, `drop(c)`.
- **`Rc`** (Listings 15-17 to 15-19, Book p.430–433): `Box` fails at sharing; `strong_count` 3 becomes 2 when leaving the scope.
- **`RefCell`** (Listings 15-20 to 15-24, Book p.438–446): `MockMessenger` with `RefCell<Vec<String>>`; panic from two `borrow_mut`; `Rc<RefCell<i32>>` with 5 becoming 15 across three lists.
- **Cycles and `Weak`** (Listings 15-25 to 15-29, Book p.447–456): `a`<->`b` cycle overflows the stack when printing; `Node` tree with `Weak` to the parent, `upgrade` returns `None` after the drop.

## Book, chapters 16 and 17: concurrency and async
- **Threads** (Listings 16-1 to 16-5, Book p.460–465): spawn without `join` dies early; `join` before the loop serializes; capture by reference fails and `move` solves it (the compiler is conservative because `main` could drop `v`).
- **Channels** (Listings 16-6 to 16-11, Book p.467–474): `send`/`recv`, use after send rejected, multiple producers (non-deterministic order).
- **`Mutex` and `Arc`** (Listings 16-12 to 16-15, Book p.476–481): a 10-thread counter goes through a move error, then `Rc` not `Send`, then `Arc<Mutex<T>>`.
- **Basic async** (Listings 17-1 to 17-8, Book p.491–502): `page_title` and its desugared form with `impl Future`; async `main` forbidden, `block_on` solves it; `select`/`Either` races two URLs; `join` is fair and deterministic.
- **Async channels and starvation** (Listings 17-9 to 17-17, Book p.503–513): a single block is linear; `async move` and `join!` with several producers; `thread::sleep` blocks, `sleep`/`yield_now` yield.
- **Timeout, streams, pin** (Listings 17-18 to 17-25, Book p.514–533): `timeout` with `select` + `sleep`; `StreamExt`; `join_all` with `Box<dyn Future>` fails and `pin!` solves it; thread + async channel + `block_on`.

## Book, chapters 18 and 19: OOP and patterns
- **`Draw`/`Screen`** (Listings 18-3 to 18-10, Book p.542–547): heterogeneous `Vec<Box<dyn Draw>>` vs homogeneous `Screen<T: Draw>`; `SelectBox` + `Button` extend the library without changing it; error if the type does not implement the trait.
- **`blog::Post`** (Listings 18-11 to 18-21, Book p.549–561): state pattern with `Option<Box<dyn State>>`, `take()`, `self: Box<Self>`, `as_ref().unwrap()`; then states as types (`DraftPost`, `PendingReviewPost`).
- **Patterns** (Listings 19-3 to 19-10, Book p.566–573): `if let`/`else if` chain, `while let Ok(value) = rx.recv()`, patterns in `for`/parameters, refutability (E0005, `let...else`, inverse warning).
- **Shadowing in `match`** (Listing 19-11 vs 19-27, Book p.574–575, 587–588): `Some(y)` creates a new variable; a guard fixes it.
- **Destructuring** (Listings 19-14 to 19-22, Book p.578–584): struct, nested enum, `(Some(_), Some(_))` to avoid overwriting configuration; `_s` moves, `_` does not.

## Book, chapter 20: unsafe and advanced features
- **Unsafe** (Listings 20-1 to 20-12, Book p.594–605): raw pointers created in safe code and dereferenced in `unsafe`; `split_at_mut` fails in safe code (E0499) and passes with `from_raw_parts_mut`; Miri detects a dangling pointer; FFI in both directions; `static mut COUNTER` read via `&raw const`; `unsafe trait` tied to `Send`/`Sync`.
- **Advanced traits** (Listings 20-13 to 20-24, Book p.607–619): associated type vs generic; `Add` (`Rhs=Self` vs `Add<Meters> for Millimeters`); disambiguation `Pilot`/`Wizard`/`Human::fly` and `Animal::baby_name`; supertrait `OutlinePrint: Display`; newtype `Wrapper(Vec<String>)` against the orphan rule.
- **Types and functions** (Listings 20-25 to 20-34, Book p.622–632): aliases `Thunk` and `io::Result<T>`; `continue` typed as `!`; `do_twice(f: fn(i32) -> i32, ...)`; functions and enum initializers work as closures; `impl Fn` fails in a `Vec`, `Box<dyn Fn>` solves it.
- **Macros** (Listings 20-35 to 20-42, Book p.635–644): simplified `vec!` with `macro_rules!` (the text mistakenly cites "Listing 20-29", it is 20-35); `HelloMacro` derive; `#[route(GET, "/")]` and `sql!(...)`.

## Book, chapter 21: web server (final project)
- **Single-thread and `/sleep`** (Listings 21-1 to 21-10, Book p.648–661): from listening to the 404 in ~40 lines (Book p.658); `/sleep` shows the serial blocking. `thread::spawn` per connection is the unbounded starting point (Book p.663).
- **`ThreadPool`** (Listings 21-12 to 21-25, Book p.664–686): incremental construction; `while let` with a held lock (Listing 21-21); graceful shutdown with non-deterministic worker order.
- **PDF discrepancy** (Book p.683, 687–689): the final listing uses `Option<JoinHandle<()>>` with `take`, while the text presents `drain(..)` as better; the `main` header appears labeled "src/lib.rs" (wrong label).

## Rust by Example: error cases
- **Ownership and borrowing** (RBE p.96, 172–185): `move` and later use; partial move; `Drop` prevents moving fields; `&mut` with active readers; reference to a local returned.
- **Generics, traits, modules** (RBE p.115–117, 150, 164, 193, 199, 220): private items and fields, unsatisfied bounds, types with different units incompatible, `'static` with `&i`, missing derive, same-named methods.
- **Std and tests** (RBE p.206–341): `File::create` overwrites; `unwrap` on `None`/`Err`; `try!` only in the 2015 edition; floats do not work as `HashMap` keys; pipe only processes after `stdin` is dropped; `?` in a test requires `Result`, in a doc test requires a hidden `try_main`; `tests/common/mod.rs`.
