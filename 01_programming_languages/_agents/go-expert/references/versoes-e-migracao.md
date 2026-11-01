# Go 1.20 to 1.24: versions, changes and migration

Reference base for the Go specialist agent. Derived from the official Go 1.20 to 1.24 release notes (summarized in English in this file), the version marks of the Spec (go1.26) and the period warnings of Effective Go (2009) and the Little Go Book (go1.3.3).

## Contents

0. [Conventions, sources and scope](#0-conventions-sources-and-scope)
1. [Master table: feature → version](#1-master-table-feature--version)
2. [Detail by version](#2-detail-by-version)
   - [Go 1.20](#go-120) · [Go 1.21](#go-121) · [Go 1.22](#go-122) · [Go 1.23](#go-123) · [Go 1.24](#go-124)
3. [Attention items: breaks and silent changes](#3-attention-items-breaks-and-silent-changes)
4. [Migration checklist 1.19 → 1.24](#4-migration-checklist-119--124)
5. [GODEBUG (and GOEXPERIMENT) table](#5-godebug-and-goexperiment-table)
6. [What changed relative to Effective Go and the Little Go Book](#6-what-changed-relative-to-effective-go-and-the-little-go-book)
7. [Gaps and limits of the sources](#7-gaps-and-limits-of-the-sources)

---

## 0. Conventions, sources and scope

**Citation abbreviations.** (RN1.20 p.N) to (RN1.24 p.N) are the release notes of each version; (Spec p.N) is the language specification (go1.26 edition); (Eff p.N) is Effective Go; (Little p.N) is the Little Go Book (go1.3.3, GOPATH; the version appears in Little p.11-12). This file barely cites it, because the book predates all the versions covered; the links made here with it start only from its declared period and are [inference].

**Mark [inference].** Indicates a link, ordering or classification made here, without the source stating it. In particular, the labels "breaks the build" and "silent" in section 3 and the order of the checklist in section 4 are my own judgment, except where the source is cited.

**Nature of this file.** Summarizes the release notes (PDF) in English, always with the PDF page. Each version covers language, tools, runtime/compiler/linker, standard library and platforms. Where the intermediate note only announces something without detailing it, section 7 records the gap.

**Coverage.** Go 1.25 and Go 1.26 have no release notes here. Only isolated marks exist: the Spec is go1.26 and Effective Go cites `new` with an expression "from Go 1.26". Mentions of 1.25 inside the 1.24 notes are advance warnings (macOS 12, removal of `aliastypeparams`).

**Master rule of versioned behavior.** Since Go 1.21, the `go` line of `go.mod` (or `go.work`) chooses the default behavior of changes that could break programs; upgrading the toolchain without raising that line keeps the previous behavior (RN1.21 p.3). This rule appears explicitly for `panicnil` (RN1.21 p.3), timers (RN1.23 p.4) and vet's printf (RN1.24 p.3). For the loop variable, RN1.22 p.1 describes the change and p.3 only says that vet depends on go.mod; tying the semantics to the `go` line is **[inference]** (cross-reading of RN1.21 p.3, RN1.22 p.3 and RN1.23 p.2): no passage literally says that a `go.mod` with `go 1.21` keeps the old semantics on a new toolchain. For the other GODEBUGs the note does not say individually whether the default follows the `go` line; see section 5.

---

## 1. Master table: feature → version

Sub-tables by area. "Preview" means available only via flag or experiment in the indicated version.

### 1.1 Language

| Feature | Version | Source |
|---|---|---|
| Type alias `type A = T` | 1.9 | (Spec p.34, p.115) |
| `0b`/`0o` prefixes, `_` in literals, hexadecimal float, shift with signed count | 1.13 | (Spec p.6-8, p.64, p.115) |
| Embedded interfaces with repeated methods stop being an error | 1.14 | (Spec p.21, p.115) |
| Slice → array pointer; `unsafe.Add`, `unsafe.Slice` | 1.17 | (Spec p.72, p.113, p.115; RN1.20 p.1) |
| Generics, `~T`, `any`, `comparable` | 1.18 | (Spec p.6, p.20-21, p.36-38, p.115) |
| Slice → array conversion `[N]T(s)` | 1.20 | (RN1.20 p.1; Spec p.72, p.116) |
| `unsafe.SliceData`, `unsafe.String`, `unsafe.StringData` | 1.20 | (RN1.20 p.1; Spec p.114) |
| Non-strictly comparable types (interfaces) satisfy `comparable` | 1.20 | (RN1.20 p.2; Spec p.38, p.116) |
| Declaring types inside generic functions | 1.20 | (RN1.20 p.5) |
| Anonymous interface cycles rejected | 1.20 | (RN1.20 p.5) |
| Built-ins `min`, `max`, `clear` | 1.21 | (RN1.21 p.1; Spec p.99, p.116) |
| Package initialization order specified | 1.21 | (RN1.21 p.1-2) |
| Broader type inference (generic functions as arguments, interface methods) | 1.21 | (RN1.21 p.2; Spec p.103, p.116) |
| `panic(nil)` produces `*runtime.PanicNilError`; `recover` never returns nil during a panic | 1.21 | (RN1.21 p.3) |
| Per-iteration loop variable | 1.22 (preview in 1.21) | (RN1.22 p.1, p.3; RN1.21 p.3; Spec p.88-89, p.116) |
| `for i := range N` | 1.22 | (RN1.22 p.1-2; Spec p.116) |
| Range over iterator function | 1.23 (preview in 1.22) | (RN1.23 p.1; RN1.22 p.2; Spec p.88, p.116) |
| Generic type alias | 1.24 (preview in 1.23) | (RN1.24 p.1; RN1.23 p.1; Spec p.34, p.116) |
| `new(expr)` | 1.26 according to Effective Go; the Spec does not state it | (Eff p.15; Spec p.104) |

### 1.2 go command, modules and tools

| Feature | Version | Source |
|---|---|---|
| `go -C dir` in all subcommands | 1.20 (must be the first flag since 1.21) | (RN1.20 p.3; RN1.21 p.4) |
| `go test -skip`, `go generate -skip` | 1.20 | (RN1.20 p.3) |
| `-i` removed from build/test | 1.20 | (RN1.20 p.3) |
| `go build -cover` + `GOCOVERDIR` | 1.20 | (RN1.20 p.3-4) |
| `-pgo` (preview) | 1.20 | (RN1.20 p.3, p.5) |
| General PGO, `-pgo=auto` default, no single-main limit | 1.21 | (RN1.21 p.4-5) |
| CPU feature build tags (`amd64.v2`) | 1.20 | (RN1.20 p.2) |
| Stdlib without precompiled `.a` in `$GOROOT/pkg` | 1.20 | (RN1.20 p.2) |
| Cgo turned off if there is no C compiler | 1.20 | (RN1.20 p.3) |
| New `start` event in test JSON; `test2json` requires `-v=test2json` | 1.20 | (RN1.20 p.2) |
| GODEBUG formalized and tied to the `go` line | 1.21 | (RN1.21 p.3) |
| `go` line as strict minimum; `toolchain` directive; toolchain download | 1.21 | (RN1.21 p.3) |
| `go test -fullpath`, multi-package `-c`, `-o` directory | 1.21 | (RN1.21 p.4) |
| `go work vendor` | 1.22 | (RN1.22 p.2) |
| `go get` in legacy GOPATH mode stops working | 1.22 | (RN1.22 p.2) |
| `go test -cover` shows 0% for a package without tests | 1.22 | (RN1.22 p.2) |
| Vet: `append` with no values, `defer` with `time.Since`, `slog` keys | 1.22 | (RN1.22 p.3) |
| Opt-in telemetry, `go env -changed`, `go mod tidy -diff` | 1.23 | (RN1.23 p.2) |
| `godebug` directive in `go.mod`/`go.work` | 1.23 | (RN1.23 p.2) |
| Vet `stdversion` | 1.23 | (RN1.23 p.2) |
| `tool` directive in `go.mod`, `go tool`, `go get -tool` | 1.24 | (RN1.24 p.2) |
| `go build/install -json`; `go test -json` with build output | 1.24 | (RN1.24 p.2) |
| `GOAUTH`; VCS version embedded in the binary | 1.24 | (RN1.24 p.2) |
| `GOCACHEPROG` without experiment | 1.24 | (RN1.24 p.3) |
| Vet: `tests`, non-constant `printf`, `buildtag`, `copylock` in three-clause loop | 1.24 | (RN1.24 p.3) |
| Cgo `#cgo noescape` / `#cgo nocallback` | 1.24 | (RN1.24 p.2) |

### 1.3 Runtime, compiler, linker

| Feature | Version | Source |
|---|---|---|
| `runtime/coverage` | 1.20 | (RN1.20 p.5) |
| `runtime.Pinner`; `cgocheck=2` becomes `GOEXPERIMENT=cgocheck2` | 1.21 | (RN1.21 p.13) |
| Devirtualization by PGO | 1.21 (expanded in 1.22) | (RN1.21 p.5; RN1.22 p.4) |
| New execution tracer | 1.22 | (RN1.22 p.12) |
| Linker: consistent `-s`/`-w`; `-B gobuildid` | 1.22 | (RN1.22 p.4-5) |
| Collectable Timer/Ticker with unbuffered channel | 1.23 (requires `go 1.23.0+`) | (RN1.23 p.4) |
| `//go:linkname` restricted to marked symbols | 1.23 | (RN1.23 p.3-4) |
| Swiss Tables maps; new internal mutex | 1.24 | (RN1.24 p.3-4) |
| `runtime.AddCleanup`; `weak` package | 1.24 | (RN1.24 p.5) |
| GNU build ID / `LC_UUID` by default | 1.24 | (RN1.24 p.4) |

### 1.4 Standard library

| Feature | Version | Source |
|---|---|---|
| `crypto/ecdh` | 1.20 | (RN1.20 p.6) |
| `errors.Join`, multiple `%w`, `Unwrap() []error` | 1.20 | (RN1.20 p.6, p.10) |
| `http.ResponseController`; `ReverseProxy.Rewrite` | 1.20 | (RN1.20 p.6-8) |
| `context.WithCancelCause`, `Cause` | 1.20 | (RN1.20 p.8) |
| `bytes`/`strings` `CutPrefix`, `CutSuffix`; `bytes.Clone` | 1.20 | (RN1.20 p.8, p.15) |
| `sync.Map` `Swap`/`CompareAndSwap`/`CompareAndDelete` | 1.20 | (RN1.20 p.15) |
| `time.DateTime`/`DateOnly`/`TimeOnly`, `Time.Compare` | 1.20 | (RN1.20 p.15) |
| `os/exec` `Cmd.Cancel`/`WaitDelay` | 1.20 | (RN1.20 p.13) |
| `filepath.IsLocal`; `SkipAll` in `Walk`/`WalkDir` | 1.20 | (RN1.20 p.11, p.13) |
| `math/rand` with automatic seed; `rand.Seed` and `rand.Read` deprecated | 1.20 | (RN1.20 p.11-12) |
| `log/slog`, `testing/slogtest`, `slices`, `maps`, `cmp` | 1.21 | (RN1.21 p.6) |
| `context.WithoutCancel`, `AfterFunc`, `WithDeadlineCause`, `WithTimeoutCause` | 1.21 | (RN1.21 p.7) |
| `sync.OnceFunc`, `OnceValue`, `OnceValues` | 1.21 | (RN1.21 p.14) |
| `errors.ErrUnsupported` | 1.21 | (RN1.21 p.10) |
| `flag.BoolFunc`; panic when defining a flag after `Set` | 1.21 | (RN1.21 p.10) |
| `testing.Testing()` | 1.21 | (RN1.21 p.14) |
| `math/rand/v2`; `go/version` | 1.22 | (RN1.22 p.5-6) |
| `ServeMux` with method and wildcards; `Request.PathValue` | 1.22 | (RN1.22 p.6) |
| `cmp.Or`; `slices.Concat`; `database/sql.Null[T]`; `reflect.TypeFor` | 1.22 | (RN1.22 p.7, p.8, p.11, p.12) |
| `iter`, `unique`, `structs` | 1.23 | (RN1.23 p.4-5) |
| Iterators in `slices` and `maps` (`All`, `Keys`, `Collect`, `Sorted`…) | 1.23 | (RN1.23 p.4-5) |
| `Request.Pattern`; `ParseCookie`; `Cookie.Partitioned` | 1.23 | (RN1.23 p.7-8) |
| `encoding/binary` `Encode`/`Decode`/`Append`; `os.CopyFS`; `filepath.Localize` | 1.23 | (RN1.23 p.6-7, p.9) |
| `sync/atomic` `And`/`Or`; `sync.Map.Clear`; `slices.Repeat` | 1.23 | (RN1.23 p.10) |
| `runtime/debug.SetCrashOutput`; `text/template` `else with` | 1.23 | (RN1.23 p.9-10) |
| `os.Root`/`os.OpenRoot` | 1.24 | (RN1.24 p.4) |
| `testing.B.Loop`; `T.Context`; `T.Chdir` | 1.24 | (RN1.24 p.4-5, p.14) |
| `testing/synctest` (experimental) | 1.24 | (RN1.24 p.6) |
| `crypto/mlkem`, `hkdf`, `pbkdf2`, `sha3`; FIPS 140-3 | 1.24 | (RN1.24 p.5-6) |
| `encoding.TextAppender`/`BinaryAppender` | 1.24 | (RN1.24 p.10) |
| `encoding/json` tag `omitzero` | 1.24 | (RN1.24 p.10) |
| `strings`/`bytes` `Lines`, `SplitSeq`, `FieldsSeq`… | 1.24 | (RN1.24 p.6-7, p.13-14) |
| HTTP/2 without TLS; `Protocols` and `HTTP2` fields | 1.24 | (RN1.24 p.12) |

### 1.5 Platforms

| Feature | Version | Source |
|---|---|---|
| Windows 10/Server 2016 and macOS 10.15 as minimums | 1.21 (warning in 1.20) | (RN1.20 p.2; RN1.21 p.15) |
| `GOOS=wasip1`, `go:wasmimport` | 1.21 | (RN1.21 p.15) |
| `GOARM` with `,softfloat`/`,hardfloat` | 1.22 | (RN1.22 p.13) |
| `GOARM64`, `GORISCV64`; macOS 11 minimum | 1.23 | (RN1.23 p.11) |
| Linux kernel 3.2 minimum; `go:wasmexport` | 1.24 | (RN1.24 p.14) |

---

## 2. Detail by version

For each version: language, tools and go.mod, runtime/compiler/linker, standard library by package (only what changes usage) and platforms.

### Go 1.20

**Language** (RN1.20 p.1-2)
- Direct slice-to-array conversion: `[4]byte(x)` replaces `*(*[4]byte)(x)`. 1.17 had only introduced slice to array pointer. The note does not detail the behavior with a slice shorter than the array; the analogous pointer form panics at run time, but that is a reading of the intermediate note itself, not official text.
- `unsafe` gains `SliceData`, `String` and `StringData`, which together with `unsafe.Slice` (1.17) complete the set for building and taking apart slices and strings.
- Comparison of structs (field by field in declaration order, stopping at the first difference) and arrays (by increasing index) was only clarified in the Spec; no program changes.
- More permissive `comparable`: comparable but not strictly comparable types (interfaces) satisfy the constraint, so a generic with `K comparable` accepts `any` or composite types with an interface as key (Spec p.38 confirms the 1.20 mark).

**Tools and go.mod** (RN1.20 p.2-5)
- End of the precompiled `.a` of the stdlib in `$GOROOT/pkg`: the stdlib is compiled on demand and stored in the build cache.
- `-C <dir>` in all subcommands; `-i` removed; `go test -skip` and `go generate -skip`.
- Whole-program coverage: `go build -cover`, run with `GOCOVERDIR` pointing to the profile directory.
- PGO in preview with `-pgo=<file>`, `-pgo=auto` (looks for `default.pgo` in the main directory; in 1.20 it requires a single main) and `-pgo=off`.
- More robust `go test -json`; anyone calling `go tool test2json` directly passes `-v=test2json`; new `start` event.
- Cgo: with no findable `CC` and no `CGO_ENABLED` set, it becomes 0. Stdlib packages with cgo are `net`, `os/user` and `plugin`. On macOS, `net` and `os/user` were rewritten without cgo; `c-archive` with `net` needs `-lresolv` in the C link. The macOS race detector runs without Xcode.
- A main module inside `GOPATH/src` no longer installs libraries in `GOPATH/pkg`.
- `go version -m` reads Windows `c-shared` DLLs and Linux binaries without execute permission.
- Vet: loop variable captured after `T.Parallel()` in subtests; time layout `2006-02-01` in `Time.Format`/`Parse` (RN1.20 p.4-5).

**Runtime, compiler, linker** (RN1.20 p.5-6)
- GC with reorganized structures (up to about 2% of CPU); new `runtime/coverage` package to write coverage in programs that do not end via `os.Exit()`.
- Compiler: PGO in preview (measured gain of 3 to 4%); types declared inside generic functions; anonymous interface cycles become an error; build up to 10% faster.
- Linker: generated symbols now use the `go:` and `type:` prefixes; `debug/gosym` understands the new convention.
- Bootstrap requires Go 1.17.13.

**Standard library** (RN1.20 p.6-15)
- `errors`/`fmt`: error with multiple wraps via `Unwrap() []error`; `errors.Join`; `fmt.Errorf` accepts several `%w`; `errors.Is/As` traverse the list.
- `net/http`: `NewResponseController(w)` with per-request `SetReadDeadline`/`SetWriteDeadline`; `WriteHeader` accepts 1xx; `Server.DisableGeneralOptionsHandler`; `Transport.OnProxyConnectResponse`.
- `httputil.ReverseProxy.Rewrite` replaces `Director`; `SetURL` adjusts `Host`; `SetXForwarded` must be called, because with `Rewrite` the `X-Forwarded-*` headers are not sent on their own; `User-Agent` is no longer added when the incoming request has none.
- `math/rand`: global generator randomly seeded; `Seed` and `Read` deprecated; reproducible source via `rand.New(rand.NewSource(seed))`.
- `context`: `WithCancelCause` and `Cause`.
- `bytes`/`strings`: `CutPrefix`, `CutSuffix`; `bytes.Clone`.
- `sync.Map`: `Swap`, `CompareAndSwap`, `CompareAndDelete`.
- `time`: `DateTime`, `DateOnly`, `TimeOnly`, `Time.Compare`; `Parse` ignores precision below a nanosecond; `MarshalJSON` stricter about RFC 3339.
- `os/exec`: `Cmd.Cancel` and `Cmd.WaitDelay`. `path/filepath`: `IsLocal`, `SkipAll`. `io/fs`: `SkipAll`.
- `reflect`: `Value.Comparable`, `Equal`, `Grow`, `SetZero`; `SetIterKey/SetIterValue` now check unexported fields.
- `testing`: `B.Elapsed`; `T.Run` inside `T.Cleanup` now panics.
- `crypto`: new `crypto/ecdh`; constant-time `ecdsa` (+5% to +30% CPU); `rsa` with constant-time backend (decryption +15% to +45%, encryption about 20 times slower), `OAEPOptions.MGFHash`; `ed25519` with Ed25519ph/ctx; `subtle.XORBytes`; `tls.CertificateVerificationError`; `x509.SetFallbackRoots`.
- File and parser security: `GODEBUG=tarinsecurepath=0` and `zipinsecurepath=0` make the readers return `ErrInsecurePath`; `mime/multipart` with limits of 10000 headers and 1000 parts; `regexp` returns `syntax.ErrLarge` for an expression that is too large; `html/template` forbids actions in JS template literals from 1.20.3.
- `encoding/binary`: varint with partial read returns `io.ErrUnexpectedEOF`. `encoding/xml`: stricter decoder (multiple colons, empty namespace, different prefixes at open and close); new `Encoder.Close`.
- `net`: `LookupCNAME` returns the CNAME whenever one exists; `FlagRunning`; `Dialer.ControlContext`; Go resolver with `trust-ad` and `nsswitch.conf` reload.
- `net/http` (others): server accepts HEAD with a body; leading and trailing spaces in cookie names are removed; `Cookie` with empty `Expires` is valid.
- `runtime/metrics` and `runtime/pprof`: new metrics (`/sched/gomaxprocs:threads`, `/sync/mutex/wait/total:seconds`), pre-scaled mutex profiles.
- `os` on Windows: `NUL` is no longer a special case in `Mkdir`/`Stat`; `File.Stat` on a directory uses the handle.

**Platforms and requirements** (RN1.20 p.2, p.6, p.15)
- Last version for Windows 7, 8, Server 2008 and 2012; 1.21 will require Windows 10/Server 2016.
- Last for macOS 10.13 and 10.14; 1.21 will require 10.15.
- FreeBSD/RISC-V experimental; shims for FreeBSD 11 and earlier leave `syscall`.

### Go 1.21

**Language** (RN1.21 p.1-3)
- `1.N.0` numbering: the first release in the series is `go1.21.0`.
- Built-ins `min`, `max` (fixed number of arguments) and `clear` (zeroes a slice or empties a map).
- Package initialization order defined: sort by import path and repeat "take the first one whose imports have already been initialized". Programs that relied on an order not expressed by imports may change behavior. The Spec describes the rule without a version mark (Spec p.111).
- Stronger type inference: generic function (including partial) as an argument to another generic; generic function assigned to a variable or returned without explicit instantiation; interface methods take part in inference; untyped constants of different kinds for the same type parameter stop being an error; in assignment, component types must be identical.
- `recover` never returns nil during a panic: `panic(nil)` becomes `*runtime.PanicNilError`. Reversion `GODEBUG=panicnil=1`, turned on automatically when the main module declares `go 1.20` or lower.
- Preview of the per-iteration loop variable via the `LoopvarExperiment` wiki; the note describes only a preview (RN1.21 p.3). "Nothing changes by default" is a reading **[inference]**.

**Tools and go.mod** (RN1.21 p.3-4)
- GODEBUG formalized: the go command chooses old or new behavior by the `go` line of `go.work` (if any) or of the main `go.mod`.
- The `go` line becomes a strict minimum: `go 1.21.0` does not compile with Go 1.20. New `toolchain` directive suggests a minimum toolchain; the go command may download or invoke other toolchains.
- `-pgo=auto` is the default and the single-main restriction was removed; any `default.pgo` in the main directory is now used.
- `-C` must be the first flag; `go test -fullpath`; `go test -c` with several packages (error if two test packages have the same name); `go test -o` accepts a directory.
- Cgo: a Go method declared on a C type is now correctly reported as an error; with the external linker, `runtime/cgo` enters as a link dependency.

**Runtime, compiler, linker** (RN1.21 p.4-5)
- Deep stack trace shows the 50 innermost and the 50 outermost frames.
- Linux with huge pages: the runtime stops working around problematic OS configuration; the recommended fix is to adjust the OS per the GC guide (`max_ptes_none` section).
- GC tuning: up to 40% lower tail latency, with a possible small throughput loss; slightly higher `GOGC`/`GOMEMLIMIT` recover the tradeoff.
- Call from C to Go on a thread created in C: from about 1-3 µs to 100-200 ns.
- PGO ready for general use (2 to 7% gain); devirtualizes interface calls.
- amd64 assembler: `nosplit` without a frame does not get automatic `NOFRAME`. Linker: SEH by default on windows/amd64; removes unreferenced global maps.

**Standard library** (RN1.21 p.6-15)
- New packages: `log/slog`, `testing/slogtest`, `slices`, `maps` (the notes only announce them; section 7) and `cmp`, which defines the `Ordered` constraint and the generic functions `Less` and `Compare` (RN1.21 p.6).
- `context`: `WithoutCancel`, `AfterFunc`, `WithDeadlineCause`, `WithTimeoutCause`. `Background` and `TODO` converted to a shared type may be equal; comparing contexts by equality was never well defined.
- `sync`: `OnceFunc`, `OnceValue`, `OnceValues`.
- `errors.ErrUnsupported`; several `syscall` errors and `http.ErrNotSupported` match it via `errors.Is`.
- `flag`: `BoolFunc`; defining a flag after `Set` with the same name panics. The fix is usually to make the dependency between packages explicit so the definition is ordered before any `Set`.
- `testing`: `Testing()`, `-test.fullpath`.
- `bytes.Buffer`: `Available`, `AvailableBuffer`. `regexp.Regexp`: `MarshalText`/`UnmarshalText`. `encoding/binary.NativeEndian`.
- `reflect`: `ValueOf` no longer forces the argument to the heap; `Value.Clear`; `SliceHeader` and `StringHeader` deprecated in favor of the `unsafe` functions.
- `runtime`: `Pinner`; stack traces carry the creator goroutine's ID; `GODEBUG=cgocheck=2` removed (now `GOEXPERIMENT=cgocheck2`); `GOTRACEBACK=wer` on Windows.
- `crypto/tls`: server does not revalidate the client certificate on a resumed session (nor run `VerifyPeerCertificate`); session ticket API (`SessionState`, `WrapSession`, `UnwrapSession`); Extended Master Secret; `QUICConn`; more specific authentication-failure alerts.
- `crypto/x509`: name constraints applied to non-leaf certificates; `RevocationList.RevokedCertificates` deprecated. `crypto/elliptic`: `Curve` methods deprecated (use `crypto/ecdh`). `crypto/rsa`: call `PrivateKey.Precompute` even when deserializing an already precomputed key; `GenerateMultiPrimeKey` and `CRTValues` deprecated.
- `net`: Multipath TCP on Linux, off by default (`Dialer.SetMultipathTCP`, `ListenConfig.SetMultipathTCP`). `net/http`: `ResponseController.EnableFullDuplex`; `ErrSchemeMismatch`.
- `os`: `Chtimes` accepts zero `time.Time`; on Windows `Truncate` on a nonexistent file now errors and `File.Chdir` starts working; on Unix, `File.Fd` keeps the descriptor non-blocking.
- `go/ast`: `IsGenerated`, `File.GoVersion`. `go/build`: header directives. `unicode`: Unicode 15.0.0.

**Platforms and requirements** (RN1.21 p.15-16)
- Minimums: macOS 10.15 and Windows 10/Server 2016.
- `GOARCH=arm` in cross-compiler: `GOARM` default 7.
- WebAssembly: `go:wasmimport`; WASI Preview 1 experimental (`GOOS=wasip1`); existing `*_wasip1.go` files must be renamed, since the suffix now acts as a GOOS constraint.
- ppc64/ppc64le with `GOPPC64=power10`; linux/loong64 with `c-archive`, `c-shared` and `pie`.

### Go 1.22

**Language** (RN1.22 p.1-2)
- Variables in the `for` header become new on each iteration. Closures, goroutines and `defer` capture the value of their own iteration. The dependence on the file's language version (`go.mod` or build constraint) is a reading **[inference]**: RN1.22 p.3 only says that vet requires Go 1.22 because of go.mod or a build constraint; the cross-reading with RN1.21 p.3 and RN1.23 p.2 supports the reading that a module with an earlier `go` keeps the old semantics. The note does not mention the `i := i` idiom; that it stops being necessary in 1.22+ code is a direct consequence of the rule [inference].
- The three-clause loop copies the value of the previous iteration into the new variable; this is unsafe for values that contain locks (explained in RN1.24 p.3).
- `for i := range 10` iterates from 0 to 9.
- Range over function only as a preview, with `GOEXPERIMENT=rangefunc`.

**Tools and go.mod** (RN1.22 p.2-3)
- `go work vendor`; with `vendor` present, builds use `-mod=vendor` by default. If the workspace root is also one of the modules, the `vendor` there contains dependencies of the workspace or of the module, never both.
- `go get` with `GO111MODULE=off` is no longer supported; `go build` and `go test` keep working on legacy GOPATH programs.
- `go mod init` no longer imports requirements from `Gopkg.lock` and similar.
- `go test -cover` shows 0% coverage for a package without tests (before, "no test files"). CI scripts that interpret this output or enforce minimum coverage may react [inference].
- External linker without cgo enabled now fails the build.
- Vet: reference to a loop variable in a function literal is no longer flagged in 1.22+ files; new warnings for `append` with no values, `defer log.Println(time.Since(t))` and malformed keys/values in `slog`.

**Runtime, compiler, linker** (RN1.22 p.4-5)
- GC metadata closer to objects: 1 to 3% less CPU and about 1% less memory.
- Objects previously always aligned to 16 bytes may now guarantee only 8. Assembly that presumes greater alignment may break; temporary workaround `GOEXPERIMENT=noallocheaders` (will be removed).
- PGO: 2 to 14% gain; `GOEXPERIMENT=newinliner` is a preview of a new inliner.
- Linker: `-w` suppresses DWARF, `-s` suppresses the symbol table and implies `-w` (negatable with `-w=0`); `-B gobuildid` generates a GNU build ID; with `-linkmode=internal` on Windows, SEH information from C objects is preserved, which may change program behavior.
- Bootstrap: last point release of Go 1.20 or later. Web trace with a new per-thread view (only for traces generated by 1.22+).

**Standard library** (RN1.22 p.5-13)
- `math/rand/v2`: no `Read`; `Source` only with `Uint64`; renames `IntN`, `Int32`, `Int32N`, `Int64`, `Int64N`; new `Uint32`, `Uint32N`, `Uint64`, `Uint64N`, `UintN`; generic function `N`; ChaCha8 (used by the top-level functions) and PCG sources. Since 1.22, the top-level functions of `math/rand` without explicit seeding and the runtime itself also use ChaCha8.
- `go/version`: validates and compares version strings.
- `net/http`: `ServeMux` patterns with method (`"POST /items/create"`) and wildcards (`/items/{id}`, `/files/{path...}`, `{$}` to match exactly the trailing slash), read with `Request.PathValue`/`SetPathValue`. In a conflict the most specific pattern wins; with no winner there is a registration conflict; registration order remains irrelevant. New `ServeFileFS`, `FileServerFS`, `NewFileTransportFS`.
- `bufio`: `ErrFinalToken` with a `nil` token stops the `Scanner` without emitting an empty token; for the old behavior, return `[]byte{}`.
- `cmp.Or`; `slices.Concat`; `database/sql.Null[T]`; `reflect.TypeFor[T]()`, `PointerTo` (and `PtrTo` deprecated).
- `slices`: `Delete`, `DeleteFunc`, `Compact`, `CompactFunc`, `Replace` zero the elements between the new and old length; `Insert` always panics with an out-of-range index.
- `encoding/json`: `\b` and `\f` escaped as `\b`/`\f`. `encoding/base32|64|hex`: `AppendEncode`, `AppendDecode`.
- `archive/tar|zip`: `Writer.AddFS`. `log/slog`: `SetLogLoggerLevel`. `math/big`: `Rat.FloatPrec`. `net/netip`: `AddrPort.Compare`.
- `go/ast`: `Ident.Obj`, `Object`, `Scope` and related deprecated, new `Unparen`. `go/types`: `Alias` type with `Unalias`, controlled by `gotypesalias` (default 0 in 1.22); function-body `Scope` starts at the `func` token.
- `html/template`: actions in JS template literals are allowed again; `ErrJSTemplate` is no longer returned and `jstmpllitinterp` loses effect.
- `reflect.Value.IsZero` becomes true for -0.0 and for a struct with a non-zero `_` field.
- `runtime/trace`: rewritten tracer (reversion `GOEXPERIMENT=noexectracer2`, to be removed); `runtime/pprof`: mutex profiles scale by the number of blocked goroutines; `runtime/metrics`: new pause histograms (`/gc/pauses:seconds` deprecated).
- `syscall` is no longer marked deprecated (frozen; for new code, `golang.org/x/sys`).
- `crypto/tls`: stricter `ExportKeyingMaterial`; server with minimum TLS 1.2; no non-ECDHE ciphers before TLS 1.3. `crypto/x509`: `OID` type, `Certificate.Policies`.
- `os` and `os/exec` on Windows: `Stat` follows reparse points; effective `O_SYNC`; `LookPath` returns `ErrNotFound` when no executable extension is found. On Linux, `io.Copy` between `TCPConn`/`UnixConn`/`File` uses `splice`/`sendfile`.
- `http.Server`/`Client` reject invalid empty `Content-Length`.

**Platforms and requirements** (RN1.22 p.13-14)
- Last version for macOS 10.15; darwin/amd64 generates PIE by default.
- `GOARM` with suffix `,softfloat`/`,hardfloat`; loong64 with register arguments; openbsd/ppc64 experimental.

### Go 1.23

**Language** (RN1.23 p.1)
- Range over functions: accepts `func(func() bool)`, `func(func(K) bool)` and `func(func(K, V) bool)`; the calls to yield produce the values. Details in the `iter` package.
- Generic type alias in preview (`GOEXPERIMENT=aliastypeparams`), only within a package.

**Tools and go.mod** (RN1.23 p.2-3)
- Opt-in telemetry: local counters by default (`go telemetry local`); `go telemetry on` sends anonymous weekly reports.
- `GOROOT_FINAL` has no effect; to install outside `$GOROOT/bin/go`, use a symlink.
- `go env -changed`; `go mod tidy -diff` (unified diff, non-zero exit if there is a change, useful in CI); `go list -m -json` with `Sum` and `GoModSum`.
- `godebug` directive in `go.mod` and `go.work`.
- Vet `stdversion` flags a symbol too new for the version in effect in the file, for example `reflect.TypeFor` in a `go 1.21` module.
- Cgo: `-ldflags` for the C linker avoids "argument list too long". Trace tolerates partially corrupted traces.

**Runtime, compiler, linker** (RN1.23 p.3-4)
- Traceback after a panic indents with a tab from the second line of the message onward.
- PGO: build overhead drops from over 100% to a single digit; stack slot overlap; hot block alignment on 386/amd64 (`-gcflags=-d=alignhot=0` turns it off).
- Linker: `//go:linkname` can no longer reference internal stdlib symbols not marked at the definition (legacy uses in a large corpus keep working); `-checklinkname=0` for debugging; `-bindnow` on ELF.

**Standard library** (RN1.23 p.4-11)
- Timer and Ticker (conditioned on `go 1.23.0+`): collectable without `Stop`; unbuffered channel; `len` and `cap` return 0; after `Reset`/`Stop` no stale value arrives. Reversion `asynctimerchan=1`.
- New packages: `unique` (`Make` returns a pointer-comparable `Handle[T]`), `iter`, `structs` (`HostLayout`).
- Iterators: `slices.All`, `Values`, `Backward`, `Collect`, `AppendSeq`, `Sorted`, `SortedFunc`, `SortedStableFunc`, `Chunk`, `Repeat`; `maps.All`, `Keys`, `Values`, `Insert`, `Collect`; `go/ast.Preorder`; `reflect.Value.Seq/Seq2`, `Type.CanSeq/CanSeq2`.
- `net/http`: `ServeContent`, `ServeFile` and `ServeFileFS` remove `Cache-Control`, `Content-Encoding`, `Etag` and `Last-Modified` when serving an error (reversion `httpservecontentkeepheaders=1`); `Request.Pattern` (empty with `httpmuxgo121=1`); `Cookie.Quoted`, `Partitioned`, `Request.CookiesNamed`, `ParseCookie`, `ParseSetCookie`; mux patterns accept spaces/tabs after the method.
- `crypto/tls`: 3DES out of the default (`tls3des=1`); experimental key exchange `X25519Kyber768Draft00` on by default (`tlskyber=0`); Encrypted Client Hello on the client; `X509KeyPair`/`LoadX509KeyPair` fill `Leaf` (`x509keypairleaf`).
- `crypto/x509`: `CreateCertificateRequest` with RSA-PSS; verification of the generated signature; `ParseOID`; advance warning that `x509sha1` would be removed in 1.24.
- `go/types`: `gotypesalias` goes to 1, so `go/types` returns `*types.Alias` by default.
- `net`: `KeepAliveConfig`, `SetKeepAliveConfig`; `DNSError` wraps timeout and cancellation (`errors.Is(err, context.DeadlineExceeded)` works); `netedns0=0` turns off EDNS0.
- `database/sql`: `driver.Valuer` errors wrapped. `net/netip`: `reflect.DeepEqual` stops equating an IPv4 `Addr` and its IPv4-mapped IPv6.
- `os`: `CopyFS`; on Windows, changes in mode bits of reparse points (`winsymlink`) and in `Readlink`/`EvalSymlinks` (`winreadlinkvolume`); on Linux, `Process` uses pidfd. `path/filepath.Localize`.
- `encoding/binary`: `Encode`, `Decode`, `Append`. `sync.Map.Clear`; `sync/atomic` `And`/`Or`; `text/template` `else with`; `unicode/utf16.RuneLen`; `math/rand/v2` `Uint`, `ChaCha8.Read`.
- `runtime/debug.SetCrashOutput`; `runtime/pprof` with stacks of up to 128 frames (was 32); `time.Parse` rejects out-of-range timezone offsets; on Windows, Timer/Ticker/`Sleep` go from 15.6 ms to 0.5 ms resolution.

**Platforms and requirements** (RN1.23 p.11)
- macOS 11 minimum; last release with Linux kernel 2.6.32+ (1.24 requires 3.2+).
- openbsd/riscv64 experimental; `GOARM64` and `GORISCV64`; `go_wasip1_wasm_exec` without wasmtime earlier than 14.0.0.

### Go 1.24

**Language** (RN1.24 p.1)
- Generic type alias fully supported. `GOEXPERIMENT=noaliastypeparams` disables it for now; the `aliastypeparams` option will be removed in 1.25. The Spec records the same (Spec p.34, p.116).

**Tools and go.mod** (RN1.24 p.2-3)
- `tool` directive in `go.mod`, in place of the `tools.go` workaround with blank imports. `go get -tool` adds the directive; the `tool` meta-pattern allows `go get tool` and `go install tool`; `go tool` runs these tools.
- Executables from `go run` and `go tool` stay in the build cache (repeated runs faster, larger cache).
- `-json` in `go build` and `go install`; `go test -json` includes build output and failures (reversion `gotestjsonbuildtext=1`).
- `GOAUTH` for private modules; `GODEBUG=toolchaintrace=1`; `GOCACHEPROG` without experiment.
- `go build` records the main module's version derived from the VCS (tag/commit, `+dirty`); omit with `-buildvcs=false`.
- Cgo: `#cgo noescape` and `#cgo nocallback`; refuses incompatible C declarations of the same function across files. Objdump on loong64, riscv64 and s390x.
- Vet: `tests` (test, fuzzer, benchmark and example signatures and names); `printf` flags `fmt.Printf(s)` with a non-constant format, only in 1.24+ files; `buildtag` flags `go1.23.1` in `//go:build`; `copylock` flags a three-clause loop with `sync.Locker`.

**Runtime, compiler, linker** (RN1.24 p.3-4)
- Average gain of 2 to 3% CPU: native `map` based on Swiss Tables, small-object allocation and new internal mutex. Disable at build with `GOEXPERIMENT=noswissmap` and `GOEXPERIMENT=nospinbitmutex`.
- Compiler: error whenever the method receiver is a cgo-generated type, including via alias.
- Linker: GNU build ID (ELF) and `LC_UUID` (Mach-O) by default; `-B none` turns it off, `-B 0xNNNN` overrides.
- Bootstrap: Go 1.22.6 or higher; 1.26 should require a 1.24 point release.

**Standard library** (RN1.24 p.4-14)
- `os.Root`/`os.OpenRoot`: operations confined to the directory, including against symlinks that leave it.
- `testing.B.Loop`: `for b.Loop() { ... }` runs the function once per `-count` and prevents the compiler from eliminating the body. `T.Context`/`B.Context` (canceled before cleanup) and `T.Chdir`/`B.Chdir`. Experimental `testing/synctest` (`GOEXPERIMENT=synctest`).
- `runtime.AddCleanup` (several cleanups per object, interior pointers, no leak in cycles) preferable to `SetFinalizer`; `weak` package; `maphash.Comparable`/`WriteComparable`. `runtime.GOROOT` deprecated. `sync.Map` reimplemented (reversion `GOEXPERIMENT=nosynchashtriemap`).
- New crypto packages: `crypto/mlkem`, `crypto/hkdf`, `crypto/pbkdf2`, `crypto/sha3`. Transparent FIPS 140-3: `GOFIPS140` at build and GODEBUG `fips140` at run time.
- `encoding/json`: `omitzero` (uses `IsZero() bool` if it exists; omits zero `time.Time`); `UnmarshalTypeError.Field` includes embedded structs.
- `encoding`: `TextAppender` and `BinaryAppender`, implemented by many stdlib types (`time.Time`, `net/url.URL`, `netip.Addr`, `regexp.Regexp` etc.).
- `bytes`/`strings`: `Lines`, `SplitSeq`, `SplitAfterSeq`, `FieldsSeq`, `FieldsFuncSeq`. `text/template`: range over function and over integer. `go/types`: iterators (`Struct.Fields`, `Tuple.Variables`, `Scope.Children` and others).
- `math/rand.Seed` becomes a no-op (reversion `randseednop=0`). `crypto/rand.Read` never fails (the program crashes if there is a read error); new `rand.Text`.
- `crypto/cipher`: `NewGCMWithRandomNonce`; `NewOFB`, `NewCFBEncrypter`, `NewCFBDecrypter` deprecated. `crypto/aes.NewCipher` no longer exposes `NewCTR`, `NewGCM`, `NewCBCEncrypter`, `NewCBCDecrypter`: pass the `Block` to the `crypto/cipher` functions.
- `crypto/rsa`: keys smaller than 1024 bits fail (`rsa1024min=0`); `crypto/ecdsa`: deterministic signature (RFC 6979) when the random source is nil; `crypto/subtle`: `WithDataIndependentTiming`, and `XORBytes` panics on partial overlap.
- `crypto/tls`: `X25519MLKEM768` by default (`tlsmlkem=0`), Kyber draft removed, `CurvePreferences` no longer sets the order, ECH on the server. `crypto/x509`: SHA-1 removed from verification; `Policies` on creation (`x509usepolicies=0`); stricter RSA parsing (`x509rsacrt=0`).
- `net`: `ListenConfig` uses MPTCP by default where supported (currently Linux). `net/http`: `Protocols` and `HTTP2` fields, HTTP/2 without TLS (`UnencryptedHTTP2`); new criterion for 1xx responses (error if the total exceeds `Transport.MaxResponseHeaderBytes`).
- `log/slog.DiscardHandler`; `archive/zip|tar` `AddFS` writes an empty-directory header; `os/user` on Windows with service accounts.

**Platforms and requirements** (RN1.24 p.14-15)
- Linux: kernel 3.2+. macOS: last version with support for macOS 11; 1.25 will require macOS 12.
- WebAssembly: `go:wasmexport`; WASI Preview 1 can become a reactor/library with `-buildmode=c-shared`; more types accepted in `go:wasmimport`/`go:wasmexport`.
- windows/arm (32-bit) marked as broken.

---

## 3. Attention items: breaks and silent changes

Each item gives version, effect, reversion (GODEBUG, when the source cites one) and source. The labels **[build]** (visible failure) and **[silent]** (compiles and changes behavior) are my classification [inference]; the practical consequences described (e.g. "may affect log parsers", "anyone reading the tail sees zeros") are also deductions [inference], except where the note states them expressly (for example, `len(t.C)` and the non-blocking receive, RN1.23 p.4).

### 3.1 Change behavior without a compile error

- **Per-iteration loop variable (1.22) [silent].** Code that relied on sharing across iterations changes when `go` is raised to 1.22+. The notes cite no GODEBUG for the loop (absence in the source, **[inference]** that none exists); keeping the old `go` line as a reversion is **[inference]** from RN1.21 p.3 and RN1.22 p.3. No passage literally says that `go 1.21` with a new toolchain keeps the old semantics.
- **Timers (1.23) [silent].** Unbuffered channel, `len`/`cap` equal to 0; code that used `len(t.C)` to test readiness must use a non-blocking receive. Only applies with `go 1.23.0+`; `asynctimerchan=1` reverts even in that case (RN1.23 p.4).
- **`rand.Seed` (1.20 and 1.24) [silent].** In 1.20, the global is randomly seeded (`randautoseed=0` reverts); in 1.24, `Seed` no longer has any effect (`randseednop=0` reverts). Anyone who needs a reproducible sequence must create their own source with `rand.New(rand.NewSource(seed))` (RN1.20 p.11). That an explicit `Seed` stays valid in versions 1.20 to 1.23 is a deduction from the 1.24 note **[inference]**; the notes do not say how `randautoseed` and `randseednop` interact. Whether the default of these two GODEBUGs follows the `go` line is not stated case by case for them; the general rule is from RN1.21 p.3, so treat "follows the `go` line" as **[inference]** and state the gap to the user (the notes only affirm the link explicitly for `panicnil`, timers and vet's `printf`).
- **`panic(nil)` (1.21) [silent].** `recover()` stops being nil. `panicnil=1`; already on for modules with `go 1.20` or lower (RN1.21 p.3).
- **Package initialization order (1.21) [silent].** Ordering by import path; anyone who relied on an order not expressed by imports may change (RN1.21 p.1-2). No GODEBUG cited.
- **`ServeMux` (1.22) [silent].** Patterns with `{` and `}` and escaped paths have new meaning; `httpmuxgo121=1` reverts (RN1.22 p.6).
- **`ServeContent`/`ServeFile`/`ServeFileFS` (1.23).** Remove `Cache-Control`, `Content-Encoding`, `Etag` and `Last-Modified` on error responses, breaking compression middlewares by `Content-Encoding`; `httpservecontentkeepheaders=1` reverts (RN1.23 p.7-8).
- **Slices (1.22) [silent].** `Delete`/`Compact`/`Replace` zero the tail; anyone reading the tail of the underlying array sees zeros (RN1.22 p.12).
- **`bufio.Scanner` (1.22).** `ErrFinalToken` with a `nil` token no longer emits an empty token (RN1.22 p.7).
- **`encoding/json` (1.22).** `\b` and `\f` with short escape; tests that compare JSON as text change (RN1.22 p.8).
- **`reflect.Value.IsZero` (1.22).** Changes for -0.0 and for a struct with a `_` field (RN1.22 p.11).
- **Coverage (1.22).** A package without tests appears with 0% (RN1.22 p.2).
- **`netip` and `DeepEqual` (1.23).** An IPv4 `Addr` and its IPv4-mapped IPv6 are no longer equal (RN1.23 p.8).
- **`database/sql` (1.23).** `driver.Valuer` errors come wrapped (RN1.23 p.6). That `==` comparisons should become `errors.Is/As` is [inference]: the note gives no such guidance.
- **`time.Parse` (1.20 and 1.23).** Accepts digits below a nanosecond (1.20); rejects out-of-range timezone offsets (1.23) (RN1.20 p.15; RN1.23 p.10).
- **`encoding/binary` (1.20).** Varint with partial read returns `io.ErrUnexpectedEOF`, not `io.EOF` (RN1.20 p.10).
- **`go test -json` (1.24).** Includes build output; `gotestjsonbuildtext=1` reverts (RN1.24 p.2).
- **Binary with VCS version (1.24).** `+dirty` and version derived from tag/commit; `-buildvcs=false` omits it (RN1.24 p.2).
- **`crypto/rand.Read` (1.24).** Never returns an error; only affects anyone who replaces `rand.Reader` (RN1.24 p.7-8).
- **`sync.Map`, `map` and runtime mutex (1.24).** Reimplementations; there are diagnostic GOEXPERIMENTs (RN1.24 p.4, p.14).
- **Panic traceback (1.23).** Tab indentation may affect crash log parsers (RN1.23 p.3).
- **Mutex profiles and tracer (1.22).** New semantics and format; numbers not comparable with earlier ones (RN1.22 p.11-12).

### 3.2 Security and TLS/cryptography

- **TLS 1.22:** server with minimum TLS 1.2 (`tls10server=1`); no non-ECDHE ciphers before TLS 1.3 (`tlsrsakex=1`); stricter `ExportKeyingMaterial` (`tlsunsafeekm=1`) (RN1.22 p.7).
- **TLS 1.23:** 3DES out (`tls3des=1`); experimental Kyber on (`tlskyber=0`, useful with a server that times out on large records); `Leaf` filled (`x509keypairleaf`) (RN1.23 p.5-6).
- **TLS 1.24:** `X25519MLKEM768` by default (`tlsmlkem=0`); Kyber draft removed; `CurvePreferences` no longer orders (RN1.24 p.9).
- **TLS 1.21:** server does not revalidate the client certificate on a resumed session; more specific alerts may break tests that expect "bad certificate"; x509 applies name constraints to non-leaf certificates (RN1.21 p.8-9).
- **x509 1.24:** SHA-1 is no longer verified, with no reversion GODEBUG; `Policies` on creation (`x509usepolicies=0`); RSA with invalid CRT may be rejected (`x509rsacrt=0`) (RN1.24 p.9-10).
- **RSA:** 1.20 slower (decryption +15% to +45%, encryption about 20 times) (RN1.20 p.9); 1.21 asks for `Precompute` after deserializing (RN1.21 p.7); 1.24 rejects keys under 1024 bits (`rsa1024min=0`, only in tests) (RN1.24 p.8).
- **Files:** `tarinsecurepath=0`/`zipinsecurepath=0` enable rejection of insecure paths (the default may change in the future) (RN1.20 p.8); `mime/multipart` limits (`multipartmaxheaders`, `multipartmaxparts`) may affect large uploads (RN1.20 p.12).
- **HTTP:** invalid empty `Content-Length` is rejected since 1.22 (`httplaxcontentlength=1`) (RN1.22 p.10).
- **`ReverseProxy` (1.20):** migrate from `Director` to `Rewrite`; `X-Forwarded-*` stop being automatic (RN1.20 p.7-8).
- **`crypto/subtle.XORBytes` (1.24):** panic on partial overlap (RN1.24 p.8-9). **`crypto/aes.NewCipher` (1.24):** no `NewCTR/GCM/CBC*` on the returned value (RN1.24 p.7).
- **`html/template`:** 1.20.3 forbids actions in JS template literals (`jstmpllitinterp=1` reverts); in 1.22 they are allowed again and the GODEBUG loses effect (RN1.20 p.11; RN1.22 p.9).

### 3.3 Break build, CI or execution visibly [build]

- **`-i` removed (1.20)** from `go build` and `go test` (RN1.20 p.3). **`-C` first (1.21)** (RN1.21 p.4).
- **No C compiler (1.20):** `CGO_ENABLED` implicitly becomes 0, which may change the DNS resolver and `os/user`; set `CGO_ENABLED=1` or install a toolchain (RN1.20 p.3-4). **External linker without cgo (1.22):** fails (RN1.22 p.2).
- **Anonymous interface cycles (1.20):** compile error (RN1.20 p.5).
- **`go` line (1.21):** `go 1.21.0` does not compile on Go 1.20; toolchains may be downloaded (RN1.21 p.3).
- **`flag` (1.21):** defining a flag after `Set` with the same name panics (RN1.21 p.10).
- **`testing` (1.20):** `T.Run` in `T.Cleanup` panics (RN1.20 p.15).
- **`GODEBUG=cgocheck=2` (1.21):** removed; use `GOEXPERIMENT=cgocheck2` at build (RN1.21 p.13).
- **`*_wasip1.go` files (1.21):** suffix becomes a GOOS constraint (RN1.21 p.15).
- **Legacy GOPATH `go get` (1.22)** (RN1.22 p.2). **Assembly with 16-byte alignment (1.22)** (RN1.22 p.4).
- **`//go:linkname` (1.23):** reference to unmarked internal symbols is blocked by the linker; `-checklinkname=0` only for debugging (RN1.23 p.3-4). **`GOROOT_FINAL` (1.23):** ignored (RN1.23 p.2).
- **Cgo (1.24):** method receiver with a cgo-generated type (including via alias) and conflicting C declarations become an error (RN1.24 p.2-4).
- **Vet (1.20 to 1.24):** new findings in `go vet` and, in the case of the `tests` analyzer, also in the subset run by `go test` (RN1.24 p.3). For 1.20, the text does not state that the new analyzers enter the `go test` vet; treat them as `go vet` findings (RN1.20 p.4-5). Non-constant `printf` only applies with `go 1.24+` in go.mod (RN1.24 p.3).
- **Tools that read Go (1.20, 1.22, 1.23):** `go:`/`type:` symbols require `debug/gosym` 1.20 (RN1.20 p.6, p.10); `go/types` produces `*types.Alias` (1.22 opt-in, 1.23 default) and the function `Scope` starts at `func` (RN1.22 p.8-9; RN1.23 p.7); `go/ast` deprecated identifier resolution (RN1.22 p.8).
- **Environment:** Windows 10/macOS 10.15 (1.21), macOS 11 (1.23), Linux 3.2 (1.24), windows/arm broken (1.24) (RN1.21 p.15; RN1.23 p.11; RN1.24 p.14-15).

---

## 4. Migration checklist 1.19 → 1.24

Baseline: the first note is 1.20's, so what changed in 1.19.x only appears when the notes mention it (`multipart` limits since 1.19.8, `regexp` since 1.19.2/1.18.7). The order below is my suggestion [inference], except where the source cites the dependency.

**Phase A: prepare the environment (without touching semantics)**
1. Check OS and bootstrap prerequisites: Windows 10/Server 2016 and macOS 10.15 (1.21), macOS 11 (1.23), Linux 3.2 (1.24); bootstrap 1.17.13 (1.20), 1.20.x (1.22), 1.22.6 (1.24) (RN1.21 p.15; RN1.23 p.11; RN1.24 p.4, p.14) [order: inference].
2. Freeze the current `go` line. Updating only the toolchain keeps the old behavior of the items controlled by that line (RN1.21 p.3). Moving `go.mod` to the toolchain version should be a separate step [inference: separation into steps].
3. In CI and scripts: remove `-i` (RN1.20 p.3); put `-C` as the first flag (RN1.21 p.4); switch direct `go tool test2json` to `-v=test2json` and tolerate the `start` event (RN1.20 p.2); review parsers of `go test -cover` output (RN1.22 p.2) and `go test -json` (RN1.24 p.2).
4. Set `CGO_ENABLED` explicitly where cgo matters; ensure a C compiler in the build environment (RN1.20 p.3); without cgo, avoid external linking (RN1.22 p.2).
5. Decide about automatic toolchains (`toolchain` directive, download): in offline CI there may be surprises (RN1.21 p.3) [practical consequence: inference].

**Phase B: raise the toolchain and run vet/tests**
6. Run `go vet` and the test suite with the new toolchain and the old `go` line; handle findings for loop variable after `T.Parallel`, layout `2006-02-01`, `append` with no values, `time.Since` in `defer`, `slog` keys, `tests`, `buildtag`, `copylock` (RN1.20 p.4-5; RN1.22 p.3; RN1.24 p.3).
7. Look for uses of APIs that changed without warning: `rand.Seed`/fixed sequences (RN1.20 p.11; RN1.24 p.12), `panic(nil)` (RN1.21 p.3), `flag` redefined after `Set` (RN1.21 p.10), `T.Run` in `Cleanup` (RN1.20 p.15), `slices.Delete/Compact/Replace` (RN1.22 p.12), `bufio.Scanner` with `ErrFinalToken` (RN1.22 p.7), varint and `io.EOF` (RN1.20 p.10).
8. Review network and HTTP: `ReverseProxy.Director` to `Rewrite` (RN1.20 p.7-8); `ServeMux` patterns with braces (RN1.22 p.6); empty `Content-Length` (RN1.22 p.10); compression middleware over `ServeContent` (RN1.23 p.8); `net.LookupCNAME` and cookies (RN1.20 p.12-13).
9. Review TLS and cryptography: tests that expect "bad certificate" (RN1.21 p.9); minimum versions and ciphers (RN1.22 p.7; RN1.23 p.6); SHA-1, small RSA keys and x509 policies in test fixtures (RN1.24 p.8-10); `Precompute` after deserializing RSA (RN1.21 p.7); `crypto/elliptic` to `crypto/ecdh` (RN1.21 p.7). Plan capacity for costlier RSA/ECDSA (RN1.20 p.8-9) [planning: inference].
10. For a failure that only appears after the update, apply the cited reversion GODEBUG (section 5) as a transitional measure and record it in `go.mod` with the `godebug` directive from 1.23 on (RN1.23 p.2) [use as a transitional measure: inference].

**Phase C: turn on the new semantics by raising the `go` line**
11. Raise `go` in steps (for example 1.21, 1.22, 1.23, 1.24) instead of going straight there [inference], noting that: 1.21 turns on the GODEBUG defaults of that version and requires `go 1.21.0` as a strict minimum (RN1.21 p.3); 1.22 turns on the per-iteration loop variable (RN1.22 p.1; link to the `go` line is [inference], see §3.1); the `go` line is a strict minimum, so the toolchain must be at least the line's version (RN1.21 p.3); 1.23 turns on unbuffered timers (RN1.23 p.4); 1.24 turns on vet's non-constant `printf` (RN1.24 p.3).
12. After raising to 1.22: removing the unnecessary `i := i` is optional [inference]; audit three-clause `for` loops that capture state in closures (RN1.22 p.1) and locks in loop variables (RN1.24 p.3).
13. After raising to 1.23: replace `len(t.C)` with a non-blocking receive; use `go mod tidy -diff` in CI; enable `stdversion` in vet (RN1.23 p.2, p.4).
14. Tools: if the project uses `tools.go`, migrate to the `tool` directive (1.24) (RN1.24 p.2) [the migration itself is optional: inference].

**Phase D: optional adoption of new features**
15. PGO: put `default.pgo` in the main directory; from 1.21 it will be used automatically (RN1.21 p.4-5).
16. Replace old packages and idioms when it makes sense: `math/rand/v2` (RN1.22 p.5-6), iterators in `slices`/`maps` (RN1.23 p.4-5), `os.Root` (RN1.24 p.4), `testing.B.Loop` (RN1.24 p.4-5), `runtime.AddCleanup` instead of `SetFinalizer` (RN1.24 p.5), `omitzero` (RN1.24 p.10) [prioritization: inference].
17. Watch deprecations: `runtime.GOROOT`, `NewOFB/CFB*`, `reflect.SliceHeader/StringHeader`, `go/ast` identifier resolution, `crypto/elliptic` Curve, `rsa.GenerateMultiPrimeKey` (RN1.24 p.7, p.13; RN1.21 p.7, p.13; RN1.22 p.8).
18. Future warnings cited by the notes: macOS 12 in 1.25; removal of `aliastypeparams` in 1.25; 1.26 bootstrap requires 1.24.x (RN1.24 p.1, p.4, p.14). What 1.25 and 1.26 bring is not in the entries (section 7).

---

## 5. GODEBUG (and GOEXPERIMENT) table

### 5.1 GODEBUG

"Reverts" indicates the value that restores the previous behavior, according to the source. When the note does not give the value, it says "not stated".

| Setting | Version | Effect | Reversion / value | Source |
|---|---|---|---|---|
| `tarinsecurepath` | 1.20 | `Reader.Next` returns `ErrInsecurePath` | `=0` enables rejection; current default allows | (RN1.20 p.8) |
| `zipinsecurepath` | 1.20 | `NewReader` returns `ErrInsecurePath` | `=0` enables rejection | (RN1.20 p.8) |
| `randautoseed` | 1.20 | global generator seeded | `=0` restores determinism | (RN1.20 p.11-12) |
| `multipartmaxheaders` | 1.19.8/1.20 | limit of 10000 headers | adjustable; value not stated | (RN1.20 p.12) |
| `multipartmaxparts` | 1.19.8/1.20 | limit of 1000 parts | adjustable; value not stated | (RN1.20 p.12) |
| `jstmpllitinterp` | 1.20.3 | forbids actions in JS template literals | `=1` reverts; no effect since 1.22 | (RN1.20 p.11; RN1.22 p.9) |
| `panicnil` | 1.21 | `panic(nil)` produces `PanicNilError` | `=1` reverts; automatic with `go 1.20` or lower | (RN1.21 p.3) |
| `cgocheck=2` | removed in 1.21 | | use `GOEXPERIMENT=cgocheck2` | (RN1.21 p.13) |
| `httpmuxgo121` | 1.22 | new ServeMux | `=1` reverts (also leaves `Request.Pattern` empty, 1.23) | (RN1.22 p.6; RN1.23 p.8) |
| `httplaxcontentlength` | 1.22 | rejects empty `Content-Length` | `=1` reverts | (RN1.22 p.10) |
| `tlsunsafeekm` | 1.22 | strict `ExportKeyingMaterial` | `=1` reverts | (RN1.22 p.7) |
| `tls10server` | 1.22 | minimum TLS 1.2 on the server | `=1` reverts | (RN1.22 p.7) |
| `tlsrsakex` | 1.22 | no non-ECDHE ciphers before TLS 1.3 | `=1` reverts | (RN1.22 p.7) |
| `x509usepolicies` | 1.22 and 1.24 | `Policies` vs. `PolicyIdentifiers` on creation | 1.22: `=1` inverts; 1.24: `=0` reverts | (RN1.22 p.7-8; RN1.24 p.9) |
| `gotypesalias` | 1.22 | `go/types` produces `Alias` | default 0 in 1.22, 1 in 1.23; reversion value: `=0` [inference from the defaults] | (RN1.22 p.8-9; RN1.23 p.7) |
| `asynctimerchan` | 1.23 | Timer/Ticker channel with buffer | `=1` reverts | (RN1.23 p.4) |
| `httpservecontentkeepheaders` | 1.23 | keeps headers on error | `=1` reverts | (RN1.23 p.8) |
| `tls3des` | 1.23 | 3DES in the default list | `=1` reverts | (RN1.23 p.5) |
| `tlskyber` | 1.23 | Kyber draft enabled | `=0` turns off | (RN1.23 p.5) |
| `x509keypairleaf` | 1.23 | `Leaf` filled | controls it; value not stated | (RN1.23 p.6) |
| `netedns0` | 1.23 | EDNS0 headers | `=0` turns off | (RN1.23 p.7) |
| `winsymlink` | 1.23 | reparse point mode bits | default 1; reversion value not stated | (RN1.23 p.8-9) |
| `winreadlinkvolume` | 1.23 | `Readlink`/`EvalSymlinks` without normalizing volumes | default 1; reversion value not stated | (RN1.23 p.8-9) |
| `gotestjsonbuildtext` | 1.24 | `go test -json` with build text | `=1` reverts | (RN1.24 p.2) |
| `rsa1024min` | 1.24 | RSA < 1024 bits fails | `=0` reverts (tests only, `//go:debug`) | (RN1.24 p.8) |
| `tlsmlkem` | 1.24 | `X25519MLKEM768` by default | `=0` reverts | (RN1.24 p.9) |
| `x509rsacrt` | 1.24 | strict CRT parsing in RSA | `=0` reverts | (RN1.24 p.9-10) |
| `randseednop` | 1.24 | `rand.Seed` has no effect | `=0` reverts | (RN1.24 p.12) |
| `dataindependenttiming` | 1.24 | turns on DIT mode in the program | `=1` turns on (opt-in, not a reversion) | (RN1.24 p.8-9) |
| `fips140` | 1.24 | FIPS mode at run time | opt-in | (RN1.24 p.5-6) |
| `toolchaintrace` | 1.24 | traces toolchain selection | `=1` turns on (diagnostic) | (RN1.24 p.2) |
| `x509sha1` | removed in 1.24 | SHA-1 in `Verify` | no reversion | (RN1.23 p.6; RN1.24 p.9) |

**How to set.** The `go` line of `go.mod`/`go.work` chooses the default (RN1.21 p.3); the `godebug` directive in `go.mod`/`go.work` declares explicit values (RN1.23 p.2); `//go:debug` appears as a way to set `rsa1024min=0` (RN1.24 p.8). That `//go:debug` acts on the main package is outside knowledge and is not stated here.

**Scope conditioned on the `go` line.** According to the notes, this is explicit for `panicnil` (RN1.21 p.3) and for the timers' behavior (RN1.23 p.4). For the other GODEBUGs the note treats the rule as general (RN1.21 p.3) without repeating it case by case.

### 5.2 GOEXPERIMENT and build flags

| Item | Version | Effect | Source |
|---|---|---|---|
| `GOEXPERIMENT=cgocheck2` | 1.21 | replaces `GODEBUG=cgocheck=2` | (RN1.21 p.13) |
| `GOEXPERIMENT=rangefunc` | 1.22 | preview of range over function (official in 1.23) | (RN1.22 p.2) |
| `GOEXPERIMENT=noallocheaders` | 1.22 | alignment workaround; will be removed | (RN1.22 p.4) |
| `GOEXPERIMENT=newinliner` | 1.22 | preview of a new inliner | (RN1.22 p.4) |
| `GOEXPERIMENT=noexectracer2` | 1.22 | back to the old tracer; will be removed | (RN1.22 p.12) |
| `GOEXPERIMENT=aliastypeparams` | 1.23 | generic alias preview; removed in 1.25 | (RN1.23 p.1; RN1.24 p.1) |
| `GOEXPERIMENT=noaliastypeparams` | 1.24 | disables generic alias | (RN1.24 p.1) |
| `GOEXPERIMENT=noswissmap`, `nospinbitmutex` | 1.24 | turn off Swiss maps and the new mutex | (RN1.24 p.3-4) |
| `GOEXPERIMENT=nosynchashtriemap` | 1.24 | back to the old `sync.Map` | (RN1.24 p.14) |
| `GOEXPERIMENT=synctest` | 1.24 | enables `testing/synctest` | (RN1.24 p.6) |
| `-checklinkname=0` | 1.23 | allows forbidden `linkname` (debugging) | (RN1.23 p.3-4) |
| `-gcflags=-d=alignhot=0` | 1.23 | turns off PGO hot block alignment | (RN1.23 p.3) |
| `-B none` / `-B 0xNNNN` | 1.24 | linker build ID | (RN1.24 p.4) |
| `-buildvcs=false` | 1.24 | omits VCS version | (RN1.24 p.2) |

---

## 6. What changed relative to Effective Go and the Little Go Book

**Premise.** Effective Go was written for the 2009 release, is "not actively updated", and does not cover generics, modules and new libraries (Eff p.1). The Little Go Book is from the go1.3.3 era (Little p.11-12); no release note mentions it, so the links with it are [inference] based only on the date. Effective Go has recent touch-ups: the note on the loop variable before Go 1.22 (Eff p.44) and `new` with an expression from Go 1.26 (Eff p.15).

| Topic | What the notes say | Link with the books |
|---|---|---|
| **Loop variable** | Since 1.22 each iteration has a new variable, according to the version in `go.mod` (RN1.22 p.1, p.3). | The `Serve` example with one goroutine per request (Eff p.44) carries its own caveat: before 1.22 there is the shared-variable bug. The `i := i` trick typical of old guides becomes unnecessary in 1.22+ code [inference]. |
| **`rand.Seed`** | Automatic seed in 1.20, `Seed` deprecated; no-op in 1.24 (RN1.20 p.11-12; RN1.24 p.12); `math/rand/v2` in 1.22 (RN1.22 p.5-6). | Period guides usually seed with `Seed(time.Now().UnixNano())` [inference: my link]. No book citation. |
| **GOPATH and modules** | In 1.20, main module in `GOPATH/src` does not install in `GOPATH/pkg` (RN1.20 p.3); in 1.22, `go get` in legacy GOPATH mode (`GO111MODULE=off`) stopped working, although `go build`/`go test` keep working (RN1.22 p.2). The `go` line and `toolchain` in 1.21 (RN1.21 p.3), `go work vendor` in 1.22, `tool` in 1.24. | Effective Go does not cover modules (Eff p.1). For the go1.3.3 book, a GOPATH workspace was the model of the time [inference]. |
| **`interface{}` vs `any`** | The notes do not mention `any`. The Spec records `any`, `comparable` and generics as Go 1.18 (Spec p.115). | Effective Go uses `interface{}` (Eff p.11, p.25) without marking it as old. Do not assume it is obsolete merely from the general warning (Eff p.1). Equivalence as a type alias is outside knowledge: not stated here. |
| **Generics** | Mark 1.18 in the Spec; 1.20 relaxes `comparable`; 1.21 broadens inference; 1.24 releases generic alias (RN1.20 p.2; RN1.21 p.2; RN1.24 p.1). | Absent from both books [inference for Little; Eff p.1 for Effective Go]. |
| **Errors** | `errors.Join`, multiple `%w`, `Unwrap() []error` (1.20); `ErrUnsupported` (1.21) (RN1.20 p.6; RN1.21 p.10). | Effective Go does not cover modern error handling (wrapping, `errors.Is/As`); absence does not imply discouraging it. |
| **Concurrency** | Unbuffered Timer/Ticker (1.23), `sync.OnceFunc` (1.21), `context.AfterFunc`/`WithoutCancel` (1.21), `unique` (1.23). | Effective Go signals termination via channels and does not cover `context` or `sync.WaitGroup`; the examples are schematic (Eff p.34, 46, 50-51). |
| **Built-ins `min`, `max`, `clear`** | Arrive in 1.21 (RN1.21 p.1; Spec p.116). | Do not exist in the period books [inference]. |
| **`for i := range N` loop** | 1.22 (RN1.22 p.1-2). | Replaces `for i := 0; i < n; i++` when only repeating N times. |
| **Tests** | `-skip`, `B.Elapsed` (1.20); `Testing()`, `-fullpath` (1.21); `B.Loop`, `T.Context`, `T.Chdir` (1.24). | Effective Go does not cover tests. |
| **`new(expr)`** | Outside the notes. | See the cross-reading below. |

**`new(expr)` cross-reading.** Effective Go says that `new` accepts an expression "from Go 1.26" (Eff p.15). The Spec describes `new(expr)` in Spec p.104 without stating the version and the versions appendix ends at Go 1.24 (Spec p.116). Therefore: the 1.26 date comes only from Effective Go; the go1.26 Spec neither corroborates nor contradicts it. Since the Spec is go1.26, it is reasonable that the description holds for that version, but that reading is [inference]. The practical recommendation is to treat `new(expr)` as a Go 1.26 feature and not presume it exists in 1.24 or earlier, since the 1.20 to 1.24 notes do not mention it.

**Other cross-readings between Spec and notes.**
- `panic(nil)` causes a run-time panic without a version in the Spec (Spec p.105); the notes give 1.21 (RN1.21 p.3).
- Initialization order by import path without a version in the Spec (Spec p.111); notes: 1.21 (RN1.21 p.1-2).
- "Strictly comparable" defined in the Spec (Spec p.69-70) without a version; the appendix only records the 1.20 consequence (Spec p.116; RN1.20 p.2).
- The USES of `clear` (Spec p.24) and of `min`/`max` with constant arguments (Spec p.11) carry no version mark in the body; the DEFINITIONS carry the [Go 1.21] mark (`clear` on p.99, `min`/`max` on p.103) and the appendix dates the set to 1.21 (Spec p.116).
- Spec p.31 ties the [Go 1.18] and [Go 1.21] marks to the list of predeclared identifiers without saying which identifier belongs to which (Spec p.31); the fine attribution comes from the appendix and the notes (`any`/`comparable` in 1.18; `min`/`max`/`clear` in 1.21).
- The appendix describes the 1.14 mark as the end of the error for a repeated method via embedded interfaces (Spec p.115), while the body marks interface embedding at p.21; the two descriptions deal with the same subject, with different emphasis.

---

## 7. Gaps and limits of the sources

**Go 1.25 and Go 1.26.** There are no release notes here. Only these exist: the Spec edition is go1.26 (appendix with no entry beyond 1.24, Spec p.115-116); `new(expr)` marked 1.26 in Effective Go (Eff p.15); and period warnings in the 1.24 notes (macOS 12 in 1.25; removal of `aliastypeparams` in 1.25; bootstrap 1.24 in 1.26) (RN1.24 p.1, p.4, p.14). Any novelty in the Spec body beyond 1.24 must be treated as a version not stated (Spec note p.115-116).

**Announced without detail in the notes.**
- Go 1.21: `log/slog`, `testing/slogtest`, `slices` and `maps` are only announced; the notes do not describe the API (RN1.21 p.6). For `cmp` the notes say only that it defines `Ordered`, `Less` and `Compare` (RN1.21 p.6). Not covered here: levels, handlers, `Attr` and the 1.21 functions of `slices`/`maps`.
- Go 1.21: the per-iteration loop stayed only as a preview pointed to the `LoopvarExperiment` wiki (RN1.21 p.3); 1.22 says the supporting tooling stays as in 1.21 without saying which (RN1.22 p.1).
- Go 1.22: `math/rand/v2` has a list of renames, but not the complete contract; the "API migration tool" is only planned.
- Go 1.20: the exact behavior of slice → array conversion when the slice is shorter than the array is not detailed (RN1.20 p.1).
- Go 1.20: PGO is described as a preview without a usage recipe; the note refers to the PGO guide.
- Go 1.21: values and syntax of `go` and `toolchain` are mentioned, but the toolchain selection rules are in "Go Toolchains", outside the entries.
- Go 1.22: the handling of escaped paths in `ServeMux` is not described (RN1.22 p.6).
- Go 1.23: iterators and `unique` refer to the package documentation; signatures do not appear. `x509keypairleaf`, `winsymlink` and `winreadlinkvolume` appear without the reversion value.
- Go 1.24: `weak`, `testing/synctest` and FIPS are presented without a detailed API; on FIPS, the note says only that module version v1.0.0 was under testing at a CMVP-accredited laboratory, with no final certification status.
- Go 1.20 to 1.24: reversion values of `multipartmaxheaders`, `multipartmaxparts`, `x509keypairleaf`, `winsymlink` and `winreadlinkvolume` are not given.

**Completeness limits of this summary.** Each version gives a per-package summary, not the full list of all changes. For 1.22, `x509usepolicies` had its default change postponed: RN1.22 p.8 said the default might change in 1.23 and RN1.24 p.9 records the change in 1.24. Packages or changes smaller than what this file mentions may exist in the official release notes; absence here does not prove absence in the version.

**Scope of the books.** No release note mentions the Little Go Book; the links with it are [inference] based on the period (go1.3.3, Little p.11-12). Effective Go only enters through period warnings and a few marks (Eff p.1, p.11, p.15, p.25, p.44). The text does not mark `interface{}`, `runtime.NumCPU/GOMAXPROCS` (Eff p.46-47) or the graphics service cited (Eff p.53) as old; the general warning of Eff p.1 applies.

**Marking inconsistencies already resolved.** Spec marks in different parts of the document do not always say the same thing (Spec p.24/45/55 without version vs appendix with 1.21; p.31 with two marks together). The appendix (Spec p.114-116) is the most reliable reference within the Spec, and the notes complement it with 1.21 (`panic(nil)`, initialization order).

**What the agent should do when answering.** Cite the version and source of the feature; for anything after Go 1.24, say that the notes do not cover it; for `new(expr)`, say that only Effective Go gives the version (1.26); and, when there is doubt about behavior in an old module, ask what the module's `go` line is before stating the behavior (RN1.21 p.3) [recommendation: inference].
