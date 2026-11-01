---
name: go-code-review
description: Reviews Go code for idioms, names, errors, pointers and receivers, slices and maps, interfaces, defer and pitfalls, with an automatic scan (rand.Seed, `Get` getters, Lock without defer Unlock, defer in a loop, panic(nil), goroutine in a loop according to the `go` line of go.mod). Use when the user asks "review this Go code", "is this idiomatic?", "code review of my package", "what should I improve in this function" or pastes Go code for evaluation. Do not use for version migration (use go-version-migration), nor to review only concurrency (use go-concurrency-review) or generics (use go-generics-review).
---

# Go code review

Sources: Effective Go (Eff, **2009, not updated**), Spec (go1.26), Little Go Book (Little, **go1.3.3, dated**) and release notes 1.20–1.24 (RN). Details in `../../references/procedimentos.md`, `frameworks.md` and `casos-e-antipadroes.md`.

## Procedure

1. **Find out the version**: the `go` line of `go.mod` (it decides, for example, the loop variable semantics) and the toolchain in use. Without a go.mod, say that version-sensitive rules go unevaluated.
2. **Run the scan** (read-only, no network) and use the result as a map, not as a verdict:
   ```bash
   python -I scripts/scan_go_smells.py PATH
   ```
   The script reads the nearest `go.mod`. It is regex: confirm each item by reading the code.
   Attention: 0 findings from the scan is NOT an approval; it does not cover a discarded error (`x, _ :=`), `defer` before checking the error, nil inside an interface, `select` with `default` in a loop, a nil channel or a double `close` — read the code.
3. **Walk through the checklist** below; for each deviation cite the rule and the source.
4. **Mark the era of the source**: advice that exists only in Little or Effective Go and that newer material changes must be stated as **[DATED]** (e.g. loop variable before Go 1.22, Eff p.44 and RN1.22).
5. **Deliver** prioritized findings (format below).

## Checklist (each item points to the source)

**Names and form**
- Getter without prefix: `Owner()`, not `GetOwner()`; setter `SetOwner()` (Eff p.4). MixedCaps; visibility by uppercase; avoid repeating the package name in the symbol (Eff p.3–5).
- Code formatted with the standard formatter; no parentheses in `if`/`for`/`switch` (Eff p.2–3).

**Errors and `defer`**
- An error is a return value; handle it before using the result; `defer resource.Close()` right after the error check (Little p.63–65).
- `panic` only for impossible situations/initialization; `recover` only in a deferred function and converting to `error` at the package boundary (Eff p.49–52).
- `defer` inside a loop only runs at the end of the function and accumulates (Spec p.97).
- Anyone testing `recover() == nil` or using `panic(nil)`: the semantics changed in Go 1.21 (RN1.21 p.3).

**Pointers, receivers and data**
- Pointer receiver to mutate, share or avoid a large copy; value for small structs (Little p.29–30, 37, 49; Eff p.28–42).
- Slices and maps: `len` vs `cap`, reassign the result of `append`, a subslice shares memory, a map needs `make`, map iteration order is not stable (Little p.42–48).
- `new` vs `make` vs composite literal; useful zero value (Eff p.15–26).
- Accept narrow interfaces (e.g. `io.Reader`/`io.Closer`) when you only call one method (Little p.58–59). "Accept interfaces, return structs" is **not in the sources**: if you recommend it, mark it [inference].
- A `String()` that calls `Sprintf` with its own type recurses; convert to the base type (Eff p.24).

**Concurrency** (summary; go deeper with `go-concurrency-review`)
- `time.Sleep` is not synchronization: Little uses `Sleep` to wait for goroutines and calls that bad (Little p.73, PDF), because `main` exits without waiting for them (Little p.73; Spec p.111: when `main` returns, the program ends and does not wait for other goroutines). `Lock()` always with `defer Unlock()` (Little p.75–76).

**Debugging built-ins**
- `println`/`print` in production code: the Spec treats them as bootstrapping functions, with no guarantee of staying in the language and with implementation-dependent formatting (Spec p.105; see `../../references/regras-da-spec.md`, section 3.19). Recommending logging instead is an [inference].

## Response format

- **Summary** (2–3 lines) and the Go version considered.
- **Findings** by severity: `file:line` — problem — why it matters — fix — source (Eff/Spec/Little/RN p.N), with **[DATED]** or **[inference]** when applicable.
- **Not verified**: what could not be confirmed (I did not compile; no `go vet`).
- Reply in the language the user writes in (default: English).

## Limits

- The scan is regex; it does not understand types or build macros. It does not prove the absence of problems.
- Effective Go (2009) and the Little Go Book (go1.3.3) do not cover modules, generics, `context`, `errors.Is/As`, wrapping with `%w` or `sync.WaitGroup` in depth; say so instead of assuming they are discouraged.
