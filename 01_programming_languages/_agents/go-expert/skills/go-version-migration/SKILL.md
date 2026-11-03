---
name: go-version-migration
description: "Plans and verifies migration between Go versions (1.19→1.20, 1.21, 1.22, 1.23, 1.24): the `go` line of go.mod, toolchain, GODEBUG, loop variable semantics, `rand.Seed`, `panic(nil)`, timers, ServeMux, range over integer and function, PGO, `tool`/`godebug` directives. Includes a go.mod checker. Use when the user says \"upgrade Go\", \"bump go.mod to 1.22\", \"what changes in 1.24\", \"my test broke after upgrading\", \"which version brought X\" or asks whether a feature exists in a version. Do not use for style review (use go-code-review). Go 1.25 and 1.26 have NO release notes in the sources."
---

# Migration between Go versions (1.20–1.24)

Main source: official Go 1.20–1.24 release notes (RN1.20…RN1.24) and the Spec's version marks. Everything is in `../../references/versoes-e-migracao.md` (master table, attention items, checklist, GODEBUG).

## Procedure

1. **Read the user's go.mod** with the checker (read-only). If the user did not state the version nor send the go.mod, **do not fabricate a go.mod** to "confirm" anything: answer conditionally ("if your `go` is X…"); the checker only consults a table of the release notes:
   ```bash
   python -I scripts/check_gomod.py --target 1.24 PATH_TO_go.mod_OR_DIRECTORY
   ```
   It shows the `go` line, the `toolchain`, the `godebug`, the available features, the behaviors in old mode and what raising to `--target` would bring.
2. **Ensure a clean starting point**: green build and tests on the current version, versioned tree.
3. **Raise one version at a time** (the order 1.20 → 1.21 → 1.22 → 1.23 → 1.24 is an **[inference]**: the notes do not dictate the order; it is the safest for isolating causes). The `go` line of go.mod is a strict minimum since 1.21 and selects the GODEBUG defaults (RN1.21 p.3).
4. **For each version**, open the corresponding section in `versoes-e-migracao.md` (section 2) and the list of items that change behavior without an error (section 3). The most frequent:
   - **Per-iteration loop variable** (go ≥ 1.22): whoever depended on sharing changes (RN1.22 p.1; Eff p.44). That the semantics depend on the `go` line, that there is no GODEBUG for it and that the rollback is to keep the old line is an **[inference]** (crossing RN1.21 p.3, RN1.22 p.3 and RN1.23 p.2); no passage says this literally. Require a toolchain ≥ the version of the `go` line (RN1.21 p.3).
   - **`panic(nil)`** (1.21): raises `*runtime.PanicNilError`; `recover()` is no longer nil; `panicnil=1` reverts and is on for `go 1.20` or lower (RN1.21 p.3).
   - **`rand.Seed`** (1.20 and 1.24): global generator randomly seeded in 1.20 (`randautoseed=0`); `Seed` has no effect in 1.24 (`randseednop=0`) (RN1.20 p.11–12; RN1.24 p.12).
   - **Timers** (1.23, requires `go 1.23.0`+): unbuffered channel; the readiness test by `len(t.C)` no longer works; `asynctimerchan=1` reverts (RN1.23 p.4).
   - **`ServeMux`** (1.22): new patterns with method and wildcards; `httpmuxgo121=1` reverts (RN1.22 p.6).
   - **`slices.Delete/Compact/Replace`** (1.22) zero the tail (RN1.22 p.12).
5. **Apply the reverting GODEBUG settings only as a bridge**, recording the reason; the `godebug` directive in go.mod exists from 1.23 (RN1.23 p.2).
6. **Optional news** (not required to migrate): `min`/`max`/`clear` (1.21), `for i := range N` (1.22), range over function (1.23), generic alias and `tool` directive (1.24). The 1.21 book/notes only **announce** `log/slog`, `slices`, `maps` and `cmp` without listing the API: do not detail the API from these sources (RN1.21 p.6).
7. **Verify**: `go build ./...`, `go vet ./...` and the tests (the notes cite new `vet` findings per version, see section 1.2 of the reference), and compare behavior where the change is silent. Tool recommendations beyond those cited in the notes (e.g. `-race`) are [extrapolation].

## Response format

Source version → target, items that apply to the user's code/project (with source), reverting GODEBUG when it exists, verification commands and risks of silent change. State explicitly what could **not** be confirmed. Reply in the language the user writes in (default: English).

## Limits

- **No Go 1.25 and 1.26**: there are only isolated marks (e.g. `new(expr)` appears as 1.26 in Effective Go p.15; Spec p.104 does not state the version). For those versions, say the sources do not cover them.
- The Spec's version table ends at 1.24; features with no marked version must be treated as "version not stated".
- Some GODEBUG revert values are not in the notes (`multipartmaxheaders`, `multipartmaxparts`, `x509keypairleaf`, `winsymlink`, `winreadlinkvolume`): say "not stated".
