# Security and resilience: ReDoS, Regexp.timeout, API removals and backtraces

Convention: `(R3x p.N)` = PDF page of the note (see `INDEX.md`).

## 1. ReDoS: improved matching algorithm (Ruby 3.2)
- `[from source]` Regexp matching can take unexpectedly long; if the code matches a possibly inefficient regex against untrusted input, an attacker can exploit this for denial of service (ReDoS) (R32 p.5).
- `[from source]` Ruby 3.2 brought two improvements: an improved matching algorithm (memoization technique) and a Regexp timeout (R32 p.5).
- `[from source]` Example from the note: `/^a*b?a*$/ =~ "a" * 50000 + "x"` takes 10 s in 3.1 and 0.003 s in 3.2 (R32 p.5).
- `[from source]` About 90% of matches (in the authors' experiments) now finish in linear time (R32 p.6). The optimization may consume memory proportional to the input size per match; allocation is usually deferred, and a normal match should use at most about 10 times the input size; the note asks to report memory overruns in real applications (R32 p.6-7).
- `[extrapolation]` Complexity classes ($O(2^n)$, polynomial) and the engine name (Onigmo) are not in the notes.

## 2. `Regexp.timeout` (Ruby 3.2)
- `[from source]` The optimization does not apply to certain regexes: those that use advanced features (back-references, look-around) or huge fixed repetitions. As a workaround, the Regexp timeout was created (R32 p.7).
- `[from source]` `Regexp.timeout = 1.0` and an expensive match raise `Regexp::TimeoutError` after one second (R32 p.7).
- `[from source]` `Regexp.timeout` is a **global** setting; for specific regexes use the `timeout:` keyword of `Regexp.new`; `Float::INFINITY` turns the limit off for that regex (R32 p.7).
- `[inference]` For code that matches regexes with back-references or look-around against third-party input, setting a global timeout is consistent with what the note presents as a fallback defense. The note does not say the timeout is mandatory, nor that the value 1.0 is adequate: the value is the project's choice.
- `[extrapolation]` Where to configure it (Rails initializer), which value to use, and how to respond to the user (HTTP 4xx) are not in the notes.
- `[VERSION-DEPENDENT]` Only from Ruby 3.2.
- `[from source]` 3.3: `Regexp::new` now accepts at most 2 arguments (the third was deprecated in 3.2) (R33 p.6).

## 3. Other changes with security/robustness effects
- `[from source]` 3.0: `$SAFE` was removed completely; it became an ordinary global variable (R30 p.7).
- `[from source]` 3.1: Psych 4.0 makes `Psych.load` use `safe_load` by default; the note suggests Psych 3.3.2 for migrating (R31 p.8).
- `[from source]` 3.2: removed `Kernel#taint`, `untaint`, `tainted?`, `trust`, `untrust`, `untrusted?` and C functions for "taintedness"/"trustedness" (R32 p.16-17).
- `[from source]` 3.2: removed `Fixnum`, `Bignum`, `Random::DEFAULT`, `Struct::Group`, `Struct::Passwd`, `Dir.exists?`, `File.exists?`, `Kernel#=~` (R32 p.16).
- `[from source]` 3.2: `libyaml` and `libffi` are no longer bundled with psych and fiddle; you may need to install `libyaml-dev` (R32 p.16).
- `[from source]` 3.4: `RubyGems` gains `--attestation` in `gem push` (signing at sigstore.dev) (R34 p.6); Bundler gains `lockfile_checksums` and `bundle lock --add-checksums` (R34 p.6); `URI` now uses the RFC 3986 parser by default (R34 p.10).
- `[extrapolation]` Any CVE analysis or web application security practices: outside the notes.

## 4. Backtraces and error messages
- `[from source]` The reversed backtrace order introduced in Ruby 2.5 was **reverted** in 3.0: the 2.4 behavior applies again, with the message and the error line first and the callers afterwards (R30 p.8). (The previous version of this package stated the opposite.)
- `[from source]` 3.4: the format changes: single quotes instead of backtick and the class name before the method name (when the class has a permanent name), for example `'Object#foo'`; `Kernel#caller` and `Thread::Backtrace::Location` methods change accordingly (R34 p.8). `Exception#set_backtrace` accepts an array of `Thread::Backtrace::Location` (R34 p.5).
- `[from source]` `error_highlight` and `SyntaxSuggest`: see `tipagem-estatica-e-ferramentas.md`.
