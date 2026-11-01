---
name: rust-compiler-error-triage
description: Diagnoses and fixes Rust compiler errors (rustc/cargo) following the message → cause → fix flow. Use when the user pastes the output of `cargo build/check/test` with `error[E0xxx]`, says "the borrow checker is complaining", "value moved", "borrowed value does not live long enough", "missing lifetime specifier", "closure may outlive", "cannot borrow as mutable", or "mismatched types". Do not use for reviewing code without a compilation error (use rust-code-review) nor for runtime errors/panics without a backtrace.
---

# Rust compiler error triage

Knowledge source: *The Rust Programming Language* (Book), *The Rust Reference* (Ref), and *Rust by Example* (RBE). Full table of codes in `../../references/casos-e-antipadroes.md`.

## Procedure

1. **Read the whole message, not just the first line.** Note: the code (`E0xxx`), the highlighted snippet, and the compiler's labels ("first borrow occurs here", "later used here", "value moved here"). Those labels already tell you which two uses conflict (Book p.100–106).
2. **Ask for more context only if the highlighted snippet is missing.** Without the code, say what is missing instead of guessing.
3. **Explain the error code** with `rustc --explain E0xxx` when the user does not know the concept (Book p.36).
4. **Classify** and apply the fix ladder below.
5. **Propose the minimal fix** that preserves the code's intent; show the diff, not the whole file.
6. **Verify**: ask for `cargo check` and confirm the error is gone and no new one appeared. If the fix requires changing the public signature, warn about the impact on callers.

## Fix ladders by family

- **Borrow (E0499, E0502, E0596)**: (a) end the uses of the first borrow before the second; (b) limit the scope with `{}`; (c) change the signature to `&mut` if the intent is to mutate; (d) return an owned value instead of a reference (Book p.100–106, 112).
- **Move (E0382, E0507)**: decide whether the type is stack-only/`Copy`; otherwise, pass a reference, or an explicit `clone()` if both copies are needed and the cost is acceptable (Book p.91–94). In closures, look at what the body moves to choose `Fn`/`FnMut`/`FnOnce` (Book p.363–366).
- **Lifetimes (E0106, E0597, E0515)**: find out which parameter the returned reference comes from; annotate only the related parameters; if the reference points to a local of the function, return an owned value. Before annotating, apply the 3 elision rules (Book p.263–268, 270–274). Be wary of the `'static` suggestion.
- **Collections (E0502 with `Vec`; E0499 appears in Book p.102)**: reference held during mutation → reorder, clone what is needed, or use `entry` (Book p.190–192, 206–208). With `Vec`, always cover the corollary: inserting/removing inside a `for` over `&v`/`&mut v` gives the same error (Book p.192). Copying the value instead of referencing it only works for `Copy` types and is an **[inference]** (Book p.94).
- **Threads (E0373, E0382 with `move`, E0277 for `Send`)**: `move`? clone? `Arc`? `Mutex`? See `rust-concurrency-async-review` (Book p.464–481).
- **Types (E0308 and variants, E0284)**: check for a stray `;` on the return (Book p.68), a condition that is not `bool` (Book p.72), `if` branches with different types (Book p.74), a `mut` that does not change the type (Book p.50–51), and a missing annotation on `parse` (Book p.52) or `collect` (Book p.317).
- **Recursive types (E0072), Deref/Drop (E0614, E0040)**: see the smart pointers section in `../../references/frameworks.md`.

## Response format

1. **Cause** in 1–2 sentences, in terms of the ownership model.
2. **Fix** (minimal diff). If there is more than one option, list them in order of preference with the trade-off.
3. **Why** — the rule the compiler is protecting, with source (Book/Ref p.N).
4. **Labeling**: separate what comes from the book from your own inference about the user's code. A fix option that is not in the cited pages is an **[inference]**, even if the reference table lists it alongside those pages.

## Limits

- The exact compiler message changes between versions; the book was written for Rust 1.90/edition 2024. If the user's output diverges, trust it and say the book's text may be outdated.
- This flow does not replace reading the error: do not propose a fix without having seen the highlighted snippet.
