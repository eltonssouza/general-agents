# Procedures and checklists for the Rust specialist agent

Operational reference derived from "The Rust Programming Language" (Book, Rust 1.90, 2024 edition) and "The Rust Reference" (Ref). All pages are from the source PDF and always carry a prefix: (Book p.N) or (Ref p.N). The only part that comes from "Rust by Example" (RBE) is the summary on handling multiple error types in section 12, cited as (RBE p.N). Passages marked **[inference]** are the consolidator's own links and do not appear as a direct instruction in the sources.

Format of each procedure: when to use, prerequisites, steps, verification, pitfalls, source.

## Contents

1. Install and verify the toolchain
2. Development cycle with Cargo (new, check, run, build --release, fmt, clippy, fix, doc)
3. Add dependencies and handle versions (SemVer)
4. Write and run tests (unit, integration, doc-tests, filters, TDD)
5. Refactor a CLI into "thin binary + library"
6. Set up a workspace
7. Write publishable doc comments
8. Publish to crates.io (and yank)
9. Write a procedural derive macro
10. Web server and thread pool with channels
11. Concurrency: threads, channels, shared state and async
12. Everyday language procedures (input, strings, modules, collections, errors)
13. Smart pointers, patterns, unsafe/FFI and traits
14. Code review by area ("if X, check Y" heuristics from the Reference)
15. Edition migration

---

## 1. Install and verify the toolchain

**When to use:** new machine, link error, `rustc` not found.

**Prerequisites:** Linux/macOS with `curl`; Windows with the official installer.

**Steps**
1. Linux/macOS: run the rustup script obtained with `curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh` (Book p.9). Windows: download the installer from the website; it asks for Visual Studio for the linker and native libraries (Book p.10).
2. Check with `rustc --version` (format: version, hash and date) and `cargo --version` (Book p.10, p.17).
3. Update with `rustup update`; remove everything with `rustup self uninstall` (Book p.11).
4. Offline documentation: `rustup doc`; the book itself: `rustup doc --book` (Book p.1, p.11).

**Verification:** both version commands respond.

**Pitfalls**
- A link error means there is no C compiler: macOS `xcode-select --install`; Linux gcc/clang (for example `build-essential` on Ubuntu). Some crates also depend on C code (Book p.10).
- `rustc` not found: check the PATH (Book p.10-11).
- Working offline with dependencies: create a temporary project, run `cargo add rand@0.8.5 trpl@0.2.0` once with network access and then use `--offline` in the cargo commands (Book p.12).

**Source:** Book p.9-12.

---

## 2. Development cycle with Cargo

**When to use:** in every project, from the first commit to delivery.

**Prerequisites:** toolchain installed (section 1).

**Steps**
1. Create: `cargo new <name>` generates a directory, `Cargo.toml`, `src/main.rs`, a Git repository and `.gitignore` (Book p.17-18). Inside an existing Git repository it does not initialize another; `--vcs=git` forces it and `--vcs` switches/removes the VCS (Book p.18). Library: `--lib` (Book p.165). Existing project: move the code to `src/` and run `cargo init` (Book p.19).
2. Iterate with `cargo check`: verifies that it compiles without producing an executable and is much faster than `build` (Book p.20). In compiler-driven development, repeat `cargo check` and handle the next error (Book p.664-667).
3. Run with `cargo run`: compiles if there was a change and runs (Book p.20). Program arguments go after `--` (Book p.316).
4. `cargo build` produces `target/debug/<name>` and creates `Cargo.lock` on the first build (Book p.19).
5. Delivery or benchmark: `cargo build --release` (output in `target/release`, with optimizations and slower compilation); always measure performance with the release binary (Book p.21).
6. `cargo fmt` formats the entire crate (`rustfmt` ships with the distribution) (Book p.15, p.707).
7. `cargo clippy` beyond the build: for example, flags an approximation of pi and suggests `std::f64::consts::PI` (lint `clippy::approx_constant`, deny by default) (Book p.708-709).
8. `cargo fix` applies the compiler's automatic fixes, such as removing an unnecessary `mut` (Book p.708).
9. `cargo doc --open` generates and opens the documentation, including that of the dependencies (Book p.33, p.387).
10. Obscure error: `rustc --explain E0308` (or the code shown) (Book p.36, p.664). Panic: `RUST_BACKTRACE=1 cargo run` (the `RUST_BACKTRACE=1` hint appears in Book p.40, 61; its use with `cargo run`, in Book p.214).
11. Third-party project: `git clone ...`, `cd`, `cargo build` (Book p.21).

**Verification:** `cargo check` with no errors and warnings; with no change to code or `Cargo.toml`, the build recompiles nothing; when only `src/main.rs` changes, only the project's crate is recompiled (Book p.20, p.31).

**Pitfalls**
- A loose `rustc main.rs` leaves the binary next to the source; with Cargo the output goes to `target/` (Book p.16, p.19, p.21).
- Benchmarking a debug build is misleading (Book p.21); backtraces require debug symbols, enabled by default without `--release` (Book p.214).
- The binary (ahead-of-time compilation) runs on machines without Rust installed (Book p.16).

**Suggested order before committing [inference]:** `cargo fmt`, `cargo clippy`, `cargo test`, and `cargo build --release` only at delivery.

**Source:** Book p.15-21, p.33, p.707-709.

---

## 3. Add dependencies and handle versions (SemVer)

**When to use:** when including an external crate or updating versions.

**Prerequisites:** Cargo project; network (or the offline procedure from section 1).

**Steps**
1. In `[dependencies]` of `Cargo.toml`, write `name = "x.y.z"` (for example `rand = "0.8.5"`) (Book p.29-30, p.181).
2. Run `cargo build`: Cargo updates the index, downloads the crate and the transitive dependencies and compiles everything (Book p.30-31).
3. Bring into scope what is needed with `use`, starting from the crate name (for example `use rand::Rng;`). The right trait cannot be guessed: consult `cargo doc --open` (Book p.33, p.181). The standard library (`std`) is not listed in `Cargo.toml`, but requires `use` (Book p.181).
4. Update within the compatible range: `cargo update` ignores `Cargo.lock` and picks the newest versions that `Cargo.toml` allows (Book p.32).
5. Change range (for example 0.8 to 0.999): edit `Cargo.toml` (Book p.32).
6. Commit `Cargo.lock` for reproducible builds (Book p.32).
7. When releasing a new version of your own crate, change the `version` field following SemVer (Book p.397).

**Verification:** `cargo build` finishes; `Cargo.lock` records the chosen versions; a second build does not recompile the dependencies.

**Pitfalls**
- In a workspace, the external dependency must be declared in the `Cargo.toml` of each crate that uses it; there is a single `Cargo.lock` and a single compatible version (Book p.402-403).
- The notes do not detail the SemVer range rules beyond the behavior of `cargo update` and manual editing; for 0.x versions, treat the range with care **[inference]**.

**Source:** Book p.29-33, p.181, p.397, p.402-403.

---

## 4. Write and run tests

### 4.1 Unit test

**When to use:** verify an isolated unit, in the same file as the code.

**Prerequisites:** library crate (`cargo new adder --lib` already creates the `tests` module and a sample test) (Book p.276-277).

**Steps**
1. Create `#[cfg(test)] mod tests { use super::*; ... }` in the file (Book p.306-307).
2. Annotate each test with `#[test]`; helper functions do not take the annotation (Book p.277).
3. Verify with `assert!`, `assert_eq!`, `assert_ne!`; when the default diagnostic is poor, add a formatted message with the obtained value (Book p.289-290).
4. Expected error: `#[should_panic(expected = "...")]` with a unique substring of the message, or `Result` with `is_err()` (Book p.293-296).
5. Expensive tests: `#[ignore]` (Book p.304-305).

### 4.2 Integration test

**When to use:** exercise the public API as an external consumer.

**Steps**
1. Create `tests/` next to `src/`; each file becomes a separate crate (Book p.308).
2. Import the library (`use adder::add_two;`); no `#[cfg(test)]` (Book p.309).
3. Shared helpers in `tests/common/mod.rs` with `mod common;` in the test; avoid `tests/common.rs`, which would show up as an empty test section (Book p.311-313).
4. Binary-only project: extract the logic into `src/lib.rs` so it can be tested (Book p.313).

### 4.3 Doc-tests

Code blocks in `///` are executed by `cargo test`, detecting outdated examples (Book p.388). Execution order: unit, integration, doc-tests (Book p.297, p.310).

### 4.4 `cargo test` commands and filters

- `cargo test`: runs everything (Book p.297).
- `cargo test <text>`: filters by substring of the name; the module is part of the name, so filtering by the module runs the whole module. Accepts only one value (Book p.302-303).
- `cargo test -- --test-threads=1`: sequential (Book p.297-298).
- `cargo test -- --show-output`: shows stdout of passing tests (Book p.299).
- `cargo test -- --ignored` / `--include-ignored`: only the ignored / all (Book p.304-305).
- `cargo test --test integration_test`: one file from `tests/` (Book p.310-311).
- Before `--` the arguments go to cargo; after, to the test binary; help with `cargo test --help` and `cargo test -- --help` (Book p.297).

### 4.5 TDD (the `search` example, Book p.336-346)
1. Write the failing test (`one_result`, search for "duct").
2. Skeleton `pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str>` returning `vec![]`, to fail for the right reason.
3. Implement: iterate `contents.lines()`, test `line.contains(query)`, accumulate into a mutable `Vec` and return it.
4. `cargo test`; refactor keeping the tests green.
5. New feature (case-insensitive search): extend the old test so the case-sensitive version does not break, add the new one, implement and wire it through `Config` and `run`.

### 4.6 Mock with `RefCell`
When the trait has `&self` and the mock needs to record calls: `RefCell<Vec<String>>`, `self.sent_messages.borrow_mut().push(...)` in `send(&self, ...)` and `.borrow().len()` in the assertions. Do not change the trait just because of the tests (Book p.441-442).

**Verification:** `cargo test` with no failures; an expected test that does not show up suggests a missing `#[test]` or a wrong filter **[inference]**.

**Pitfalls:** the `println!` output of passing tests stays hidden without `--show-output` (Book p.299); `#[should_panic]` without `expected` accepts any panic (Book p.293-296).

---

## 5. Refactor a CLI into "thin binary + library"

**When to use:** `main.rs` grew (parsing, I/O and logic mixed) and the logic needs to be testable.

**Prerequisites:** working binary project (the book uses `minigrep`, Book ch. 12).

**Steps**
1. Keep trivial parsing in `main` while it is small; split `main.rs` and `lib.rs` (Book p.323).
2. Extract `parse_config`, group the values in a `struct Config` with named fields and turn it into `Config::new` (Book p.323-327).
3. Replace `panic!` with `Result` and rename to `Config::build` (Book p.329).
4. In `main`: `Config::build(&args).unwrap_or_else(|err| { eprintln!(...); process::exit(1); })` (Book p.330, p.350). Error messages go to stderr with `eprintln!`; stdout can be redirected with `cargo run > output.txt` (Book p.349–350).
5. Extract `run(config) -> Result<(), Box<dyn Error>>`, using `?` in place of `expect`; in `main`, handle it with `if let Err(e) = run(config)` (Book p.331-334).
6. Move the logic (for example `search`) to `src/lib.rs` and import it in `main.rs` with `use minigrep::search;` (Book p.334-335).
7. Cover the lib with unit and integration tests (section 4).
8. Optional: receive an iterator in `Config::build` (`impl Iterator<Item = String>`, with `mut` to call `next`), discard the program name with a first `next()`, use `match args.next()` with `Some(v) => v` and `None => return Err(...)`, and pass `env::args()` directly at the call site without `collect`. This eliminates `clone`, since the Strings are moved into the struct (Book p.376-378).

**Flag via environment variable (Book p.345-347):** add `ignore_case: bool` to `Config`; in `build`, `env::var("IGNORE_CASE").is_ok()`; in `run`, choose the search function with `if config.ignore_case`. Usage: `IGNORE_CASE=1 cargo run -- to poem.txt` (Unix); in PowerShell, `$Env:IGNORE_CASE=1; cargo run -- to poem.txt`, and `Remove-Item Env:IGNORE_CASE` to remove it (Book p.347).

**Verification:** `main` only configures, calls `run` and handles the error; `cargo test` covers the lib; the binary's behavior stays the same.

**Pitfalls:** forgetting the `--` when passing arguments to the program (Book p.316); keeping logic in `main`, which prevents integration testing (Book p.313).

**Source:** Book p.316, p.323-350, p.376-378.

---

## 6. Set up a workspace

**When to use:** several crates that evolve together and share `Cargo.lock` and `target/`.

**Steps**
1. `mkdir add && cd add`; create `Cargo.toml` with `[workspace]` and `resolver = "3"` (Book p.399).
2. Inside the workspace, `cargo new adder` and `cargo new add_one --lib`: Cargo adds each member to `members` automatically (Book p.399-400).
3. Dependency between members: in `adder/Cargo.toml`, `add_one = { path = "../add_one" }` (Book p.401).
4. Build from the root with `cargo build`; run a member with `cargo run -p adder` (Book p.401-402).
5. External dependency: declare it in the `Cargo.toml` of each crate that uses it (Book p.402-403).
6. `cargo test` at the root runs the tests of all crates; `cargo test -p add_one` runs only one (Book p.404-405).
7. Publishing: each crate is published separately, choosing with `-p` (Book p.405).

**Verification:** `cargo build` at the root compiles all members; there is a single `Cargo.lock` at the root.

**Pitfalls:** expecting that declaring the dependency in one member makes it available to the others (Book p.402-403); forgetting the `path` dependency between members (Book p.401).

**Source:** Book p.399-405.

---

## 7. Write publishable doc comments

**When to use:** every public API, especially before publishing.

**Steps**
1. Put `///` immediately before the public item, in Markdown, with a `# Examples` section containing a code block (Book p.386-387).
2. Consider `# Panics` sections (panic scenarios), `# Errors` (for functions that return `Result`) and `# Safety` (for `unsafe fn`, describing invariants) (Book p.388). Document the panic of validated constructors (Book p.231-233).
3. Document the crate or module with `//!` at the top of `src/lib.rs` (Book p.389).
4. Generate with `cargo doc` (HTML in `target/doc`) or `cargo doc --open`, which includes the dependencies (Book p.387).
5. Run `cargo test`: the examples are executed as doc-tests (Book p.388).

**Verification:** the rendered page shows the sections; the doc-tests pass; the `# Panics` section appears in the generated doc (Book p.668).

**Pitfalls:** examples that do not compile break `cargo test`; this is an advantage, since it exposes outdated documentation (Book p.388). For `unsafe fn` without documented conditions, see section 14.6, `unsafe fn` bullet (Ref p.621-622).

**Source:** Book p.386-389.

---

## 8. Publish to crates.io

**When to use:** make a crate available to the public. Publishing is permanent.

**Prerequisites:** doc comments (section 7), green tests, crates.io account.

**Steps**
1. Create an account (login via GitHub), get the token at `https://crates.io/me/` and run `cargo login`, which saves it to `~/.cargo/credentials.toml` (Book p.394).
2. Choose a unique name (first come, first served); search before (Book p.395).
3. In `[package]` fill in `name`, `version`, `edition`, `description` (one or two sentences) and `license` (SPDX identifier). Without `description` and `license`, publish fails with a 400 error (Book p.395-396).
4. License outside SPDX: put the text in a file and use `license-file`. Multiple licenses with `OR`, for example `MIT OR Apache-2.0`, common practice (Book p.396).
5. `cargo publish` (Book p.396).
6. New version: change `version` according to SemVer and publish again (Book p.397).
7. Problematic version: `cargo yank --vers X.Y.Z`; undo with `--undo` (Book p.397-398).

**Verification:** the crate appears on crates.io with the version and documentation.

**Pitfalls:** published content cannot be deleted, only "yanked" (Book p.396-398); name taken; missing metadata (400 error).

**Source:** Book p.394-398.

---

## 9. Write a procedural derive macro

**When to use:** generate a trait `impl` automatically with `#[derive(Trait)]`.

**Prerequisites:** workspace or two crates; know the target trait (the book uses `HelloMacro`).

**Steps**
1. Create the trait crate: `cargo new hello_macro --lib`, with the trait and the associated function (Book p.638).
2. Inside it, create the macro crate: `cargo new hello_macro_derive --lib` (Book p.639).
3. In the macro crate's `Cargo.toml`: a `[lib]` section with `proc-macro = true`; dependencies `syn = "2.0"` and `quote = "1.0"` (Book p.639).
4. In the macro crate's `src/lib.rs`: `#[proc_macro_derive(HelloMacro)] pub fn ...(input: TokenStream) -> TokenStream`, which does `syn::parse(input).unwrap()` and delegates to an inner function `impl_...(&ast)` (Book p.639).
5. In the inner function, get `let name = &ast.ident;`, generate the code with `quote!{ impl Trait for #name { ... } }`, use `stringify!(#name)` for the name text and end with `.into()` (Book p.642).
6. In the consuming crate, declare both as a dependency (crates.io version or `path = ...`) and use `#[derive(HelloMacro)]` (Book p.643).

**Verification:** the consumer compiles and the generated method prints the type name.

**Structural choice:** separate crates allow using the trait without the derive; the alternative is for the trait crate to depend on the derive crate and re-export the macro (Book p.639).

**Pitfalls**
- In proc macros, use absolute paths and unlikely internal names, remove inert attributes from the output; the macro has full access to the build environment (Ref p.67-68, p.120).
- `proc-macro` compiles for the host (Ref p.570).
- Rules for declarative macros (`macro_rules!`) are in section 14.1.

**Source:** Book p.637-643; Ref p.67-68, p.120, p.570.

---

## 10. Web server and thread pool with channels

**When to use:** TCP server that serves connections in parallel without creating a thread per request.

**Prerequisites:** binary project; notions of threads and channels (section 11).

### 10.1 Single-thread base
1. `TcpListener::bind("127.0.0.1:7878").unwrap()` and `for stream in listener.incoming()` (Book p.648).
2. In `handle_connection(mut stream: TcpStream)`: `BufReader::new(&stream)`, `.lines()`, `.map(unwrap)`, `.take_while(|l| !l.is_empty())`, `collect::<Vec<_>>()`; the request ends at an empty line (Book p.650-651).
3. Respond with `stream.write_all(response.as_bytes())` (requires `std::io::prelude::*`), including `Content-Length` (Book p.653, p.655).
4. Route by reading only the first line (`buf_reader.lines().next().unwrap().unwrap()`) and comparing with `"GET / HTTP/1.1"` (Book p.656). Refactor by extracting only what differs (status and file) into a destructured tuple (Book p.658). With 3+ cases, `match &request_line[..]`: slicing is needed because `match` does not auto-deref like `==` does (Book p.661).

### 10.2 Compiler-driven ThreadPool
1. Write `main` with `ThreadPool::new(4)` and `pool.execute(|| handle_connection(stream))` (Book p.663-664).
2. `cargo check` reports E0433: convert into lib+bin (`pub struct ThreadPool;` in `src/lib.rs`, `use hello::ThreadPool;`) (Book p.664-665).
3. Next E0599 errors: add `new(size: usize)` and `execute<F>(&self, f: F) where F: FnOnce() + Send + 'static` (Book p.665-667).
4. Validate `size > 0`; store `Vec::with_capacity(size)` (Book p.667-669).
5. Replace `JoinHandle` with `Worker { id, thread }` with a private `Worker::new` (Book p.670-671).
6. Create the channel in `new`; the `Sender` stays in the pool and the `Receiver` is shared by `Arc::new(Mutex::new(receiver))` with `Arc::clone` per worker (Book p.672-676).
7. `type Job = Box<dyn FnOnce() + Send + 'static>`; `execute` does `Box::new(f)` and `send(job).unwrap()` (acceptable: the receiver only closes when the pool is destroyed) (Book p.677).
8. Worker: `thread::spawn(move || loop { let job = receiver.lock().unwrap().recv().unwrap(); job(); })`; `recv` blocks until there is work (Book p.678).

### 10.3 Graceful shutdown
1. `Drop for ThreadPool` with `join` per worker; E0507 is solved by iterating with `self.workers.drain(..)` (Book p.682-683).
2. `sender: Option<mpsc::Sender<Job>>`; `new` uses `Some(sender)`; `execute` uses `self.sender.as_ref().unwrap().send(job)` (Book p.684).
3. In `drop`, `drop(self.sender.take())` before the `join`s (Book p.684).
4. In the worker, `match` on `recv()`: `Ok(job)` executes; `Err(_)` prints and does `break` (Book p.685).
5. To demonstrate: `listener.incoming().take(2)` and the pool goes out of scope at the end of `main` (Book p.685-686).

**Verification:** slow requests do not block the others; on shutdown, each worker reports that it shut down and the program ends.

**Pitfalls:** without `Content-Length` the response is invalid (Book p.655); without dropping the `Sender` before the `join`s, the workers stay blocked in `recv` **[inference from step 3 of 10.3]**.

**Source:** Book p.647-686.

---

## 11. Concurrency: threads, channels, shared state and async

**Thread with guaranteed completion (Book p.461-465):** `let handle = thread::spawn(move || { ... });` (`move` if the closure uses data from the environment) and `handle.join().unwrap()` after `main`'s concurrent work.

**Channel between threads (Book p.467-473):**
1. `let (tx, rx) = mpsc::channel();` the type is inferred from the first `send`; if unused, it does not compile.
2. Move `tx` into the thread with `move`; `tx.send(val)` consumes `val` and returns a `Result` to handle.
3. Receive with `rx.recv()` (blocks), `try_recv()` (does not block) or `for received in rx` (until the channel closes).
4. Several producers: `let tx1 = tx.clone();` moving each clone into a thread.

**Shared counter (Book p.477-482):** `Arc::new(Mutex::new(0))`; on each iteration `let counter = Arc::clone(&counter);` and `spawn(move || { let mut num = counter.lock().unwrap(); *num += 1; })`; keep the handles in a `Vec` and `join` them all; read with `*counter.lock().unwrap()`. For simple numbers, consider `std::sync::atomic` instead of `Mutex`.

**First async program with `trpl` (Book p.491-495):** `cargo new hello-async`, `cargo add trpl`; `async fn` with `.await` on each future; in a synchronous `fn main()`, `trpl::block_on(async { ... })`; run with `cargo run -- "https://www.rust-lang.org"`.

**Async recipes**
- *First of two futures:* `trpl::select(f1, f2).await` and `match` on `Either::Left/Right`; also return the context (the URL) to report the winner (Book p.497-498).
- *Concurrent loops without tasks:* each loop in an `async` block and `trpl::join(fut1, fut2).await`; await the `join` future, not the individual ones (Book p.501-505).
- *Async channel with correct shutdown:* `let (tx, mut rx) = trpl::channel();`; sender `async move { ... tx.send(v).unwrap(); sleep.await }` (the `move` drops `tx` at the end); receiver `while let Some(v) = rx.recv().await`; `trpl::join` or `trpl::join!` with several producers (clone `tx`, all `async move`) (Book p.503-509).
- *timeout:* `async fn timeout<F: Future>(future_to_try: F, max_time: Duration) -> Result<F::Output, Duration>` with `trpl::select(future_to_try, trpl::sleep(max_time)).await` (`Left(output) => Ok(output)`, `Right(_) => Err(max_time)`); pass `future_to_try` first, since `select` is not fair and polls in argument order (Book p.514-516).

**Verification:** `join` returns; final counter equals the number of threads; the receiver leaves the loop when all `tx` are dropped.

**Pitfalls:** using the value after `send`; an undropped `tx` hangs `for received in rx`/`while let`; an async sender without `move` keeps `tx` alive and the receiver never finishes (Book p.469, p.472, p.503-509). For `async fn` and `?` in async blocks, see section 14.

**Source:** Book p.461-535.

---

## 12. Everyday language procedures

**When to use:** short recipes for recurring tasks; each gives the essentials.

**User input to number (Book p.26-42):** mutable `String::new()`; `read_line(&mut s)` appends (does not overwrite) and returns a `Result` that must be handled; `trim()` removes `\n`/`\r\n`; `.parse()` with an annotated type (`let guess: u32`); handle the `Result` with `expect` or `match { Ok(n) => n, Err(_) => continue }`. Before delivering: remove debug prints, ensure a `break` in the `loop`, do not ignore `Result` (warning `unused_must_use`).


**Strings (Book p.111-114, p.196-202):** `&str` parameters instead of `&String` (accepts `&String`, slices and literals). Concatenate: `push_str`/`push` to append, `s1 + &s2` for two (moves `s1`), `format!` for three or more. Iterate with `.chars()` (Unicode) or `.bytes()`; slice `&s[a..b]` only at char boundaries, otherwise panic.


**Modules (Book p.161-186):** declare `mod name;` in the crate root; the compiler looks inline, `src/name.rs` or `src/name/mod.rs`; a submodule of a non-root file lives in a directory named after the ancestor (putting `hosting.rs` in `src/` instead of `src/front_of_house/` makes the lookup fail); one file style per module; make public only what is needed. More binaries in `src/bin/`; `src/lib.rs` next to `src/main.rs` forms lib and bin.

**Collections (Book p.190-208):** `&v[i]` if an index failure is a bug that should bring the program down; `v.get(i)` if it is a normal situation. HashMap: `insert` overwrites; `entry(k).or_insert(v)` inserts if absent; to update from the old value, `let c = map.entry(k).or_insert(0); *c += 1;`; `get(&k)` returns `Option<&V>`.

**Errors (Book p.213-233):** panic: `RUST_BACKTRACE=1` and read from the top down to the first line in your own file (`full` for verbose). Propagation: return `Result<T, E>` with `?` on each fallible call, `fs::read_to_string` for files, and `main` with `-> Result<(), Box<dyn Error>>` ending in `Ok(())`. Validated type: private field, `new` with a documented `panic!` and public getter.

**Multiple error types (RBE p.255-269):**
- Problem: `Option` needs to interact with `Result`, or `Result<T, E1>` with `Result<T, E2>`; the goal is to make errors composable (RBE p.257). `?` is equivalent to an `unwrap` that does `return` instead of panicking on `Err`, and actually returns `Err(From::from(err))`, converting automatically if the error is convertible to the return type (RBE p.255, p.263). The `try!` macro is old; today `?` applies (RBE p.255-256).
- Criteria for a good error type, according to RBE (p.259): (1) represents different errors with the same type; (2) presents clear messages to the user; (3) is easy to compare (prefer `Err(EmptyVec)` to a `String` with the sentence); (4) can carry information about the error (`Err(BadChar(c, position))` instead of loose text); (5) composes well with other errors.
- Strategies, in order of presentation: (a) nest `Option<Result<..>>` and use `transpose` to swap it for `Result<Option<..>>` when you want to stop at the error but proceed if it is `None` (RBE p.258); (b) own error type that masks all errors into one, with `Display` and `ok_or`/`map_err` to convert; it loses the original error information (RBE p.259-260); (c) `Box<dyn Error>`: simple code preserving the original error, at the cost of the concrete type being known only at runtime; std converts any `Error` into `Box` via `From` (RBE p.261-262); (d) `?` instead of chained `ok_or`/`map_err`/`and_then`; the result is still a `Result` and must be handled at the top (RBE p.263-264); (e) own enum that wraps the errors (e.g. `EmptyVec` and `Parse(ParseIntError)`), with `Display`, `Error::source` returning the wrapped error and `impl From<ParseIntError>` for `?` to convert; more boilerplate and may not be necessary, and there are crates that generate it (RBE p.265-267).
- Iterating over `Result`s (RBE p.268-269): ignore failures with `filter_map(.. .ok())`; keep the failures aside with `map_err` inside the `filter_map`; fail the whole operation with `collect::<Result<Vec<_>, _>>()` (stops at the first failure; also works for `Option`); separate valid ones and failures with `partition(Result::is_ok)` and then `unwrap`/`unwrap_err` on each side.



---

## 13. Smart pointers, patterns, unsafe/FFI and traits

**Parent/child cycle without leaking (Book p.451-456):** children in `RefCell<Vec<Rc<Node>>>`; parent in `RefCell<Weak<Node>>`, initialized with `Weak::new()` and linked by `*leaf.parent.borrow_mut() = Rc::downgrade(&branch)`; when reading the parent, `upgrade()` returns `Option<Rc<Node>>` and `None` must be handled; validate with `Rc::strong_count` and `Rc::weak_count`. Mock with `RefCell`: section 4.6.

**OO state pattern (Book p.550-556):** `Post` holds `state: Option<Box<dyn State>>` initialized to `Draft`; transitions with receiver `self: Box<Self>`; in `Post`, `if let Some(s) = self.state.take() { self.state = Some(s.method()) }`; states without change return `self`; `content` delegates with `self.state.as_ref().unwrap().content(self)` (`as_ref` avoids moving out of `&self`); `content` has a default implementation `""` and only `Published` overrides it.


**Refutable patterns (Book p.565-573):** E0005 in `let`: use `let ... else { diverge }`, `if let` or `match`. Warning `irrefutable_let_patterns`: remove the `else`. E0308 in `let (x, y) = (1, 2, 3);`: match the elements or use `_`/`..`.

**Unsafe safely (Book p.592-606):**
1. Confirm that one of the five superpowers is really needed.
2. Minimal `unsafe` block, wrapped in a safe function when the invariant can be guaranteed locally (for example `assert!(mid <= len)`).
3. Comment `SAFETY`.
4. Run Miri: `rustup +nightly component add miri`, then `cargo +nightly miri run` or `miri test`. These commands are in (Book p.604–605); nightly only in the project, with `rustup override set nightly` (Book p.717).
5. Complement with tests: Miri only sees executed paths.

**FFI (Book p.599-601):** call C with `unsafe extern "C" { fn abs(input: i32) -> i32; }` and `unsafe {}` at the call; `safe fn` in the block dispenses with the `unsafe` at the call, but the promise is yours. Expose Rust: `#[unsafe(no_mangle)] pub extern "C" fn name() {...}`, with a name without collision risk.
- Default ABI (Ref p.115-116, p.162): a function without `extern` uses `"Rust"`; `extern fn` or an `extern` block without an ABI string uses `"C"`, but the Reference says this form is being phased out, so always write the ABI (`"C"`, `"system"`, `"C-unwind"`). The Book uses an explicit `"C"` (Book p.600).
- Symbols (Ref p.639-641): `no_mangle` also exports the item publicly and turns off mangling; `no_mangle`, `export_name` and `link_section` require `#[unsafe(...)]` in 2024 (previously optional). Choose names without collision risk.


---

## 14. Code review by area ("if X, check Y" heuristics)

Use as a sweep list in review; each item points to the Reference page.

### 14.1 Macros, attributes and expressions
- `$x:expr` forwarded to another macro: the second cannot match it by literal tokens; use `tt` or `ident` (Ref p.50-51).
- Matcher ending a fragment with `[`, `(`, `{` or using `as`/`where` after `expr`: check the follow-set (Ref p.65-66). `expr` only before `=>`, `,`, `;`; `ty` before `{ [ , => : = > >> ; | as where`; `pat` before `=> , = | if in`; avoid `$($e:expr)*` without a separator (Ref p.690, p.694-695).
  - Why (Ref p.65): `$i:expr [ , ]` is rejected even though it is unambiguous today, because `[` can start an expression suffix and a future syntax would break the matcher. Repetitions (Ref p.66): the separator must be able to follow the content; in `*`/`+` the content must be able to follow itself; the content must be able to follow what comes before and what comes after must be able to follow the content; if it can repeat zero times (`*`/`?`), what comes after must be able to follow what comes before. Formal appendix: Ref p.687-695.
  - Way out: reorder the matcher, with an ident or single element before the repetition (avoids the local ambiguity error, Ref p.50) and a separator or terminal (`,`, `;`, `=>`) right after `expr` **[inference]**.
- Macro across crates: `$crate::helper!` and `$crate::path::item`; `$crate` does not bypass privacy (Ref p.62-64). Hygiene: a `let x` inside the expansion is not visible to the caller (Ref p.63).
- Use by path (`crate::m!`) or by other crates: `#[macro_export]`; internal use by path: `pub(crate) use m;` after the definition (Ref p.56-57, p.60-61). Macro that generates `macro_rules!`/`mod`/`use` with an already existing name: ambiguity (Ref p.549-551).
- Proc macros: absolute paths, unlikely internal names, no inert attributes in the output (Ref p.67-68, p.120).
- `cfg!(...)` becomes a literal `true`/`false`; `#[cfg]` removes the item and `cfg_select!` chooses code by predicates (Ref p.89-90). **[inference]**: since `cfg!` only produces a boolean, the code of both branches must compile; the Reference does not state this.
- `#[expect]` in a large scope may go unfulfilled; `forbid` prohibits an inner `allow` (Ref p.207-210). `#[must_use]`: the function-based check does not fire when the call comes wrapped in a tuple, `Some(..)`, `if` or `match`, but the type-based check still applies if the expression's type is `#[must_use]`; intentional discard with `let _ =` or `_ =` (Ref p.216-217).
- `#[target_feature]` on a safe fn: check the caller's features or `unsafe` after runtime detection; prohibited on `main`, safe trait methods and with `inline(always)` (Ref p.227-228).
- Evolving public type: `#[non_exhaustive]`; the consumer needs `..` and a `_` arm; `as` fails (Ref p.248-250).
- Symbol attributes (`no_mangle`, `export_name`, `link_section`): `unsafe(...)` in 2024 and check for collisions; `global_allocator` unique in the graph; Windows GUI: `#![windows_subsystem = "windows"]` at the bin root (Ref p.639-643).
- `as` between integers, float to int or pointers: silent loss (Ref p.303-307); if the value may not fit, `TryFrom` is the fallible conversion (RBE p.56; the recommendation to replace `as` with `TryFrom` is **[inference]**).
- `?` in `async {}` or a closure affects the future/closure, not the outer function; the error needs `From` (Ref p.287, p.297).

### 14.2 Items, functions, traits and types
- `extern "C"` that may panic: `"C"` aborts; `"C-unwind"` propagates; native unwind crossing a non-unwind ABI is UB (Ref p.116-117, p.163).
- `async fn` with a reference: the future captures everything and the parameters are only dropped when the `await` completes (Ref p.117-118); in `async unsafe fn`, the caller is responsible for validity while the future lives (Ref p.118-119).
- Enum with `as`: only unit variants; with data, only via `repr(primitive)` and unsafe reading (Ref p.130-132); `= value` with fields requires `#[repr(u8)]` etc. (Ref p.128-129).
- Union read: `unsafe`, validate the bit pattern, remember the joint borrow of the fields (Ref p.135-137). `static mut`: prefer atomic or `Sync`, use `&raw mut` (Ref p.144).
- Trait used as `dyn`: no associated consts, `Self: Sized`, generic methods, `Self` in return/argument, `async fn` or `impl Trait` in the return; or `where Self: Sized` on the methods (Ref p.147-149).
- "parameter not constrained": `T`/`N` must appear in the implemented trait, in the implementing type or as a constrained associated type (Ref p.158-159). Orphan impl: newtype or local trait; `Box<Local>` counts as local (Ref p.157).
- In 2024, `unsafe extern` is mandatory; `safe fn` only if the signature is always safe (Ref p.160-161, p.166). GAT with a `where Self: 'a` error: required-clauses rule (Ref p.186-187). `Foo<N>` ambiguous with an alias: `Foo<{ N }>` (Ref p.176).
- Same-named method in inherent and trait: the `T`, `&T`, `&mut T` lookup may pick the trait; in a trait object, do not define a same-named inherent one (Ref p.334-335).
- `impl Trait` in return requires a single concrete type (otherwise `Box<dyn T>` or enum); replacing `<T: Tr>` with `impl Tr` breaks turbofish (Ref p.442). `match`/`if` with distinct function items: annotate a `fn` pointer (Ref p.412, p.478-480).

### 14.3 Patterns and closures
- Simple identifier in a `match` arm where a constant/variant was expected: if not imported, it becomes a binding that matches everything (Ref p.372-373).
- Guard with a side effect next to `|`: may run more than once (Ref p.361). `if let ... && ...` only in 2024; `let` with `||` needs parentheses (Ref p.357, p.363).
- `match x` to `match &x`/`*x` changes place versus value expression and temporaries (Ref p.359). Const in a pattern requires `#[derive(PartialEq)]`; NaN and `static mut` are rejected (Ref p.389-390).
- A `move` closure returned or sent to a thread may be `Fn`/`FnMut` (Ref p.428); a `&mut` captured by move moves the reference (Ref p.423).
- `let _ = x` or destructuring without reading does not capture; range, slice and multi-variant enum borrow and block a later `&mut` (Ref p.418-423). `Rc`/`Arc` captures the whole pointer; only `Box` has precise capture via deref (Ref p.425). `async` closure where `Fn`/`FnMut` is expected: check whether it is lending (Ref p.428-429).

### 14.4 Layout, memory, lifetimes and variance
- `repr(packed)`: never `&field` (includes `println!("{}", s.f)`); use a copy, `{s.f}` or `&raw const` with `read_unaligned` (example on p.463; the same pattern appears on p.294; theory of the misaligned place in regras-da-referencia.md, section 5); do not mix `align` and `packed` (Ref p.293-294, p.462-463, p.627).
- Rust enum modeling a C enum with arbitrary values is UB; primitive `repr` on an enum without variants is an error (Ref p.459). **[inference]**: `repr(C, u8)` only holds 256 distinct discriminants; the number 256 is not on those pages.
- Raw pointers: `==` compares the address; do not transmute pointers into bytes (Ref p.434-435, p.463). `unsafe` that depends on a destructor: `forget`/`ManuallyDrop`/abort bypass it (Ref p.497).
- `let x = f(&temp());` with an ordinary function, method on the temporary, `async {}`, closure or `break` does not extend the temporary (Ref p.495-496). `const`/`static` with `&mut` or `&Atomic*`/`Cell` in tail position: lifetime extension error (Ref p.633-637).
- Variance: `*mut T`, `&mut T`, `UnsafeCell<T>`, `fn(T)` make the parameter invariant/contravariant; `PhantomData<T>` is covariant and counts for drop check and auto traits (Ref p.466, p.504).
- Only lifetimes are implied bounds; bounds required by the struct are repeated in the functions (Ref p.472). `Box<dyn T>` is `+ 'static`, `&'a dyn T` is `+ 'a` (Ref p.500-501). Elision: two inputs without `self` with a borrowed output is an error; with `&self`, the output binds to `self` (Ref p.498-499).

### 14.5 Modules, paths and visibility
- `use Alias::Variant` or `use Type::ASSOC_CONST` failing: import the enum/type (Ref p.542). `use x::*` next to a same-named external module/macro: ambiguity error; explicit import (Ref p.545-547).
- Public API across crates: the whole chain from the root to the item is `pub`; check for a `pub use` that leaks internal types (Ref p.555, p.560). Prefer `pub(crate)`/`pub(super)`; `pub(self)` is private; `pub(in path)` requires an ancestor, no alias, starting with `crate`/`self`/`super` (Ref p.558).
- `::x` changes between 2015 and 2018; a nested module does not see the parent's names (Ref p.514, p.533). `no_std` does not guarantee the absence of `std` at link time; `alloc` requires `extern crate alloc;` (Ref p.523-524).

### 14.6 Unsafe, UB, FFI and linking
- **`unsafe` block:** go through the UB list: alignment (by the pointer's type), dangling and bounds, aliasing, writing to immutable bytes, invalid values (`bool`, `char`, enum, null reference, `NonZero`), uninitialized integers/pointers (Ref p.624-629); the validity list is in regras-da-referencia.md, section 5, item Invalid values (Ref p.627-628). Field through a possibly misaligned pointer: `&raw const`/`&raw mut` (Ref p.627), reading and writing with `read_unaligned`/`write_unaligned` instead of dereferencing directly (Ref p.463; example with `repr(packed)` on p.294); details in regras-da-referencia.md, section 5, item Alignment.
- **`unsafe fn`:** the review script has three questions. (1) Is there documentation of the extra safety conditions the caller must meet and the compiler does not check, for example index within bounds in `get_unchecked`? The Reference asks for the function to come with this documentation (Ref p.621; in the Book, the `# Safety` section, Book p.388). (2) The body counts as an `unsafe` block by default; it stops counting only with the `unsafe_op_in_unsafe_fn` lint on (Ref p.622), so each dangerous operation inside it must be justified by the function's conditions. (3) Does the code produce any invalid value? Check, in regras-da-referencia.md, section 5, item Invalid values: `bool` and `char` (Ref p.627); enum, reference and `Box`, and uninitialized integers, floats and raw pointers (Ref p.628); uninitialized memory in general (Ref p.629). The Reference's list is non-exhaustive, and it itself says to read the Rustonomicon before writing unsafe code (Ref p.624); the Rustonomicon is not in the PDF read. In a `const` context, `transmute` of a pointer with provenance to an integer is UB (Ref p.628-629); reading uninitialized bytes outside `union`/padding is UB (Ref p.629).
- FFI with panic or exception: `-unwind` ABI on both sides; `"C"` with unwinding is UB; `-fno-exceptions` in C (Ref p.567). Mixing `panic=abort` and `unwind`: `link.unwinding`, `ffi_unwind_calls`, care with `dlopen` (Ref p.574-575). `catch_unwind`/`join` do not handle errors from C/C++ code reliably (Ref p.567).
- `staticlib` includes std and exports symbols: version script and `--gc-sections`; avoid two Rust `staticlib`s in the same link (Ref p.570, p.574). `proc-macro` compiles for the host (Ref p.570). With musl/`crt-static`, check the binary (Ref p.572-573).
- **`asm!`:** (a) every modified register is an output or clobber (`out(..) _`/`clobber_abi`); (b) modifier on operands smaller than the register; (c) without `nostack` if it uses the stack; (d) `pure`/`nomem`/`readonly` only if true; (e) preserve DF and the x87 stack; (f) no unwinding out; (g) `noreturn` does not fall off the end; (h) `lateout` only writes after reading the inputs (registers and operands: Ref p.583, 601; options `pure`/`nomem`/`readonly`/`nostack`/`noreturn`: Ref p.603-608; rules: Ref p.608-611). **`naked_asm!`:** restore callee-saved, end in `ret` or diverge, `.cfi_*` if there is unwinding (Ref p.612-614).

---

## 15. Edition migration

**When to use:** upgrade a crate to the 2021 or 2024 edition (the Book uses 2024; `edition` is a field of `[package]`, Book p.395).

**Prerequisites:** green tests and committed code before migrating **[inference]**.

**Steps**
1. Apply the automatic fixes with `cargo fix`, which also migrates between editions (Book p.708).
2. Review by hand what the tool does not solve, using the lists below.
3. Run `cargo check`, `cargo test` and `cargo clippy` after changing the `edition` field **[inference: verification order]**.

**2018 to 2021 checklist (Ref p.430-432):** closures capture disjoint fields; review drop order, the closure's `Send`/`Sync` and old local-borrow workarounds.

**2024 checklist**
- Patterns with `mut`/`ref`/`&` under `ref` mode (for example `Some(mut x)` against `&Option<T>`) (Ref p.374).
- Return `impl Trait` now captures lifetimes (Ref p.444).
- Fallback of the `!` type with `Default::default()`/`return` (Ref p.482).
- Drop order of temporaries in `if let` and in tail expressions, relevant for locks and `RefCell` (Ref p.490).
- `unsafe extern` mandatory and symbol attributes (`no_mangle` etc.) with `unsafe(...)` (Ref p.160-161, p.166, p.639-641).
- Chained `if let` with `&&` only compiles in 2024 (Ref p.357, p.363); `resolver = "3"` in the workspace (Book p.399).

**Verification:** the suite passes with no change in behavior; pay attention to locks and `RefCell`, where the new drop order may change deadlocks or panics **[inference]**.

**Pitfalls:** `::x` changes meaning between 2015 and 2018 (Ref p.533); relying only on `cargo fix` without reviewing drop order and closure capture **[inference]** (the Reference describes the capture change on p.430-432 and the drop change on p.490, but does not mention `cargo fix`).

**Source:** Book p.395, p.399, p.708; Ref p.357-363, p.374, p.430-432, p.444, p.482, p.490, p.533, p.639-641.
