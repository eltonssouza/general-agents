---
name: rust-edition-migration
description: Plans and verifies Rust edition migration (2015→2018→2021→2024) and explains behavior differences between editions (closures, binding modes, temporaries, `impl Trait`, prelude, paths, `unsafe extern`, `#[unsafe(no_mangle)]`). Use when the user says "migrate to edition 2024", "cargo fix --edition", "what changes in 2021", "why does this code behave differently", or asks which edition a feature requires. Do not use to update the compiler version without changing the edition, nor to update dependencies.
---

# Rust edition migration

Sources: Book appendix E (p.711–712), Ref (differences by edition; consolidated table in `../../references/regras-da-referencia.md`).

## Procedure

1. **Find the current edition**: the `edition` field in `Cargo.toml`; without the field, 2015 applies (Book p.711).
2. **Ensure a clean starting point**: `cargo check` without errors and a versioned tree.
3. **Apply the automatic migration**: the book says `cargo fix` migrates between editions and points to the Rust Edition Guide for the procedure (Book p.708, 712). The flag details (for example `cargo fix --edition`) **are not in the sources**: confirm in the Edition Guide or in `cargo fix --help`. Then change `edition` in `Cargo.toml` and run `cargo check` and the tests.
4. **Manually review what the tool does not resolve** using the differences table (Ref):
   - **Closures**: capture by disjoint path instead of the whole variable ("edition 2018 and before" captures the whole variable); changes borrows, drop, and auto traits (Ref p.430–432). That this is edition 2021 is not in the excerpt read from the Reference: **[inference]**.
   - **Binding modes** (2024): `ref`/`ref mut`/`mut` and `&pat` under a non-move mode are no longer accepted (Ref p.374).
   - **`impl Trait` in return position** (2024): captures all lifetimes in scope (Ref p.444).
   - **Divergence fallback** (2024): becomes `!`; before it was `()` (Ref p.482).
   - **Temporaries** (2024): the Reference records that 2024 added the rule "temporaries of the `if let` scrutinee are dropped before the `else`" and that temporaries of the block tail die after the tail (Ref p.490–491). The previous behavior is not described in the Reference: present it as an **[inference]**.
   - **Let chains** in `if`: only 2024 (Ref p.357).
   - **`dyn`** mandatory in 2021 (Ref p.438–439); own **prelude** in 2021 and 2024 (Ref p.522); leading **`::`** in paths: 2015 = crate root, 2018+ = extern prelude (Ref p.533).
   - **Symbols and FFI** (2024): `extern` requires `unsafe extern`; `no_mangle`, `export_name`, `link_section` require `#[unsafe(...)]` (Ref p.620, 623, 639–641). The `rust-unsafe-audit` script detects these cases.
   - **New keywords**: use `r#` for identifiers that collide (Book p.694).
5. **Verify**: `cargo check`, tests, `cargo clippy`; compare behavior where the change is semantic (temporaries, drop, capture).

## Response format

Source edition → target, list of items that apply to the user's code (with source), commands to run, risks of silent behavior change, and how to test them.

## Labeling rule

The Reference describes the current rule and says what an edition *added*; the old behavior is only a source when the page states it. Label as **[inference]** any "it used to be like this" that is not on the cited page.

## Limits

- The table covers the differences the Reference records; it is not the full Edition Guide (the book points to it, Book p.712). If an item is not in the table, say it was not found in the sources.
- If an item appears marked **[NOT VERIFIED IN THE PDF]** in `regras-da-referencia.md`, do not treat it as a fact.
