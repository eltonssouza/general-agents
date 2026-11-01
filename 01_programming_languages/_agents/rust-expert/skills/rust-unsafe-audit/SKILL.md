---
name: rust-unsafe-audit
description: Audits or writes `unsafe` Rust code — unsafe blocks, `unsafe fn/trait/impl`, raw pointers, `static mut`, FFI (`extern`, `no_mangle`), unions, and transmute — checking SAFETY comments, encapsulation, and undefined behavior (UB) risks, and running an automatic scan. Use when the user says "review this unsafe", "is this safe?", "can I use unsafe here?", "audit the FFI", "static mut", or "how do I run Miri". Do not use for 100% safe code (use rust-code-review).
---

# `unsafe` audit in Rust

Sources: Book ch. 20 (p.592–606), Ref (unsafe obligations and the UB list, Ref p.620–629). Details in `../../references/regras-da-referencia.md` and `../../references/frameworks.md`.

## Procedure

1. **Is `unsafe` necessary?** Confirm the code uses one of the 5 superpowers (dereference a raw pointer, call an unsafe function, access/modify a `static mut`, implement an unsafe trait, access a union field); if it does not, the block does not need to exist (Book p.592–593).
2. **Run the scan**:
   ```bash
   python -I <PKG>/scripts/scan_rust_smells.py --profile unsafe PATH
   ```
   (`<PKG>` = package root; from this skill, `../../`. Checklist with pages: `python -I <PKG>/scripts/rust_checklist.py unsafe`.)
   It flags `unsafe` without `// SAFETY:`, an unsafe operation inside `unsafe fn` without an explicit `unsafe {}` block, `static mut`, `transmute`, `from_raw_parts`, and `*_unchecked` APIs (the latter, an **[extrapolation]** convention), casts to raw pointers, `extern` without `unsafe`, and `no_mangle`/`export_name`/`link_section` without `unsafe(...)` (mandatory in edition 2024 — Ref p.620, 623, 639–641). It is regex: confirm each item.
3. **For each unsafe block/fn**, check:
   - a **minimal** block (only the operation that requires unsafe);
   - a `// SAFETY:` comment explaining why the obligations hold; `unsafe fn` documents the caller's obligations in `# Safety` (Book p.592–606);
   - the `unsafe` is **encapsulated** in a safe API whose guarantees the module actually enforces;
   - the Reference's UB list was walked through (invalid data, aliasing, invalid dereference, etc. — Ref p.624–629).
   - **Conceptual questions about UB** ("what is UB?", "what should I check in this function?"): state the points listed in `../../references/regras-da-referencia.md` (UB section, Ref p.624–629): the Reference's list is non-exhaustive and is not a formal model; `unsafe` does not relax the language rules; definition of *sound*/*unsound* code; *dangling* pointer; alignment; reading/writing through a pointer vs `&raw`; validity of values (`bool`, `char`, uninitialized integers).
   - **`unsafe_op_in_unsafe_fn`**: Ref p.621–622 describes the body of an `unsafe fn` as an unsafe block by default, adjustable by the lint; Book p.596 shows an explicit `unsafe {}` inside `unsafe fn`, with the compiler warning. The default per edition is **not in the PDFs** (**[NOT VERIFIED IN THE PDF]**). Practical recommendation: always write an explicit `unsafe {}` and warn that the original code may compile without a warning in one edition and warn in another.
4. **`static mut`**: direct accesses create a data race risk; use `&raw` instead of references and consider alternatives: the Book prefers concurrency techniques and thread-safe smart pointers (Book p.603); citing atomics or `Mutex` as substitutes is an **[inference]** (the Book only names atomics as an alternative to `Mutex`, Book p.482).
5. **FFI**: `unsafe extern` asserts that the signatures are correct — a wrong signature is UB (Ref p.623); a symbol exported with `#[unsafe(no_mangle)]` needs a name without collision risk (Book p.600–601; Ref p.639).
6. **Run Miri** when possible:
   ```bash
   rustup +nightly component add miri
   cargo +nightly miri test
   ```
   Miri requires nightly and only sees executed paths: finding a problem indicates a bug; finding none does **not** prove absence (Book p.604–606). Complement with tests.

## Response format

List per `unsafe` item: location — superpower used — obligations (invariants) — evidence that they hold — possible risk/UB — fix. End with a verdict: *acceptable*, *acceptable with adjustments*, or *redo without unsafe*.

## Limits

- An audit by reading does not demonstrate the correctness of `unsafe`. State explicitly what could not be verified.
- Inline assembly, `repr` layout, and unwinding across ABIs have their own rules in the Reference (Ref p.564–619); consult `regras-da-referencia.md` before giving an opinion.
