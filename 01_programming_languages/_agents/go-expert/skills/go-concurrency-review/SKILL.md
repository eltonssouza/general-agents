---
name: go-concurrency-review
description: Reviews and designs concurrency in Go — goroutines, channels (buffered and unbuffered, nil, close), select, Mutex/RWMutex, defer/panic/recover, worker pools, stopping goroutines, loop variable in goroutines depending on the version. Use when the user says "I have a race", "deadlock", "leaking goroutine", "how do I stop this goroutine", "channel or mutex?", "worker pool", "select with default in a loop" or pastes code with `go func`, `chan` or `sync.`. Do not use for general style review (use go-code-review) nor for version migration (use go-version-migration).
---

# Concurrency in Go

Sources: Effective Go (Eff p.42–48, **2009**), Little Go Book (Little p.72–82, **go1.3.3, dated**), Spec (semantics of channels, `select`, `go`, `defer`) and release notes. Decision trees in `../../references/frameworks.md` (concurrency section) and rules in `../../references/regras-da-spec.md`.

## Procedure

1. **Find out the version** (go.mod): the loop variable is per-iteration only since Go 1.22 (RN1.22 p.1, p.3). In earlier versions, a goroutine created in a loop that uses the loop variable is a bug (Eff p.44).
2. **Run the scan** `python -I ../go-code-review/scripts/scan_go_smells.py PATH` (rules `loopvar-goroutine`, `lock-no-defer`, `sleep-sync`, `defer-in-loop`) and confirm by reading the code.
3. **Choose the primitive**: a channel to transfer data/signal and as a semaphore; a mutex to protect simple shared state (Eff p.42–48; Little p.76–77). A rule like "channel whenever possible" is **not in** the sources: mark it [inference] if you use it.
4. **Review checklist**:
   - `time.Sleep` to wait for goroutines is bad: too short or wasteful (Little p.73, 76).
   - `Lock()` followed by `defer Unlock()`; forgetting the `Unlock` causes deadlock (Little p.75–76).
   - Channels: blocking on `send`/`receive`, buffer, backpressure policies (block, buffer, drop, timeout), double close and `send` on a closed channel, `nil` channel (Little p.77–81; Spec p.70–71, 80, 88, 92–93, 99–100).
   - `select`: `default` in a loop becomes a busy wait; `select` rules (Little p.80–81; Spec p.92–93).
   - A `main` that returns without waiting for the goroutines ends the program: when the `main` invocation returns, the program exits and does not wait for the other goroutines (Spec p.111; example in Little p.73).
   - Goroutines created without a limit: use a pool/semaphore (Eff p.42–48).
   - `recover` only inside a deferred function and called directly; `panic(nil)` changed in 1.21 (Spec p.105; RN1.21 p.3).
   - Timers and tickers in Go 1.23+ (with `go 1.23.0` or higher): unbuffered channel; `len(t.C)` is not a readiness test (RN1.23 p.4).
   - Attention: 0 findings from the scan is not an approval (it does not cover `select` with `default` in a loop, a nil channel or a double `close`).
5. **Propose the minimal fix**; if the fix requires `sync.WaitGroup`, `context` or the race detector, know that `sync.WaitGroup` and `errgroup` do not appear in any of the four sources, and `context` only appears in the release notes as isolated news (e.g. `WithCancelCause`, RN1.20 p.8; `WithoutCancel`, `AfterFunc`, RN1.21 p.7): Little does not cover them (Little p.72–82). Use the available sources and mark the rest as [extrapolation].

## Response format

Diagnosis (which concurrency rule is violated), corrected snippet, why (source), and what to verify. The race detector only appears in the sources as an implementation change on macOS (RN1.20 p.4), with no usage guidance; recommending `go test -race` is [extrapolation] and must be marked as such. Reply in the language the user writes in (default: English).

## Limits

- Old sources (2009 and go1.3.3) do not cover `context`, `errgroup` or `sync.WaitGroup`; the release notes only cite isolated news about `context` and `sync`; the Spec defines the semantics of channels, not usage patterns.
- The Spec items on `go`, `select` and `defer` are thinly distilled: for a fine rule, read the Spec at the pages indicated in `regras-da-spec.md`.
