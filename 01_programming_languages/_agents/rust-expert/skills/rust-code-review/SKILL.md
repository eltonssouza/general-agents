---
name: rust-code-review
description: Reviews Rust code for idioms, error handling, ownership, API design, and pitfalls, with an automatic scan for attention points (unwrap, panics, `as` casts, `&String`/`&Vec`, index loops, clone, thread::spawn without move). Use when the user asks "review this Rust code", "is this idiomatic?", "code review my crate", "what should I improve in this module", or pastes Rust code for evaluation. Do not use to fix a specific compilation error (use rust-compiler-error-triage), nor to audit `unsafe` in depth (use rust-unsafe-audit).
---

# Rust code review

Sources: Book, Ref, and RBE (source table in the package README); cited pages = PDF pages. Checklist with origin and page: `python -I <PKG>/scripts/rust_checklist.py review`. Details in `../../references/procedimentos.md` and `../../references/frameworks.md`.

## Procedure

1. **Define the scope**: files/diff to review, Rust version, and the `edition` in `Cargo.toml` (a missing key means 2015 — Book p.711).
2. **Run the scan** (read-only, no network) and use the result as a map of where to look, not as a verdict:
   ```bash
   python -I <PKG>/scripts/scan_rust_smells.py --profile review PATH
   ```
   `<PKG>` = package root (from this skill, `../../`). Each finding carries its **origin** (label and page); `--rules` lists the rules. The script ignores `unwrap`/`expect`/`panic!` in `#[cfg(test)]` and in `tests/`. False positives are expected; confirm by reading the code.
3. **Read the code** following the checklist below and confirm or discard each script finding.
4. **If possible, ask for** `cargo check` (Book p.20), `cargo clippy`, and `cargo fmt` (Book p.707–709); the `--check` flag of `cargo fmt` is not in the sources: **[extrapolation]**. Interpret the warnings.
5. **Deliver** prioritized findings (format below).

## Checklist (each item points to its source)

**Errors**
- Every `unwrap`/`expect`/`panic!`/`[]` indexing in production code falls into one of four cases: (a) example/test/prototype; (b) known invariant — require an `expect` with a message that explains why; (c) expected failure — convert to `Result`; (d) contract violation — document a `# Panics` section and keep the panic (Book p.220–230).
- `main` returns `Result` when it uses `?`; library errors with their own type and `From`; `Box<dyn Error>` for binaries (Book p.220–230, RBE p.232–264).
- Types validated in the constructor (newtype with a private field) instead of scattered checks (Book p.230–233).

**Ownership and API**
- Parameters: `&str` instead of `&String` (Book p.107, 113); `&[T]` instead of `&Vec<T>` is an **[extrapolation]** (analogy with Book p.113–114); `self` only when it needs to consume (Book p.133).
- Return a slice instead of an index when it makes sense (Book p.107–114).
- `clone()` only when both copies are needed and the cost is acceptable (Book p.91–94).
- Minimal mutability; `const` for magic numbers; shadowing instead of `mut` when changing the type (Book p.48–50, 54–55).

**Flow and types**
- `match`/`if let`/`let…else`: exhaustiveness, catch-all position, `let…else` for early return (Book p.153–159).
- Overflow: a conscious choice among `checked_*`, `wrapping_*`, `saturating_*`, `overflowing_*`; `as` can truncate — prefer `From`/`TryFrom` (overflow: Book p.54–55; truncation and saturation of `as`: RBE p.46–48; `TryFrom`: RBE p.56 — the preference for `TryFrom` is an **[inference]**).
- Strings: do not index a `String` by integer; beware of slices outside a `char` boundary (Book p.196–202).
- Loops: `for` over an iterator instead of an index; iterator consumers present; type annotated on `collect` (Book p.367–379).

**Sharing**
- `Rc<RefCell<…>>` only with a real need for shared mutation; consider cycles and `Weak` (Rc: Book p.431–436; Rc<RefCell>: p.443–445; cycles and Weak: p.447, 450–453).
- `thread::spawn` needs `move` when it captures local data (Book p.464–481).

## Response format

- **Summary** (2–3 lines).
- **Findings** in order of severity: `file:line` — problem — why it matters — suggested fix — source (Book/Ref/RBE p.N) or **[inference]**.
- **What is good** (one line, if relevant).
- **Not verified**: what could not be confirmed (e.g., I did not compile the code).

## Limits

- The scan is regex-based; it understands neither macros nor types. It does not prove the absence of problems.
- The book covers Rust 1.90/edition 2024; crate recommendations (e.g., `rand` 0.8.5) are version-dependent (Book p.30).
