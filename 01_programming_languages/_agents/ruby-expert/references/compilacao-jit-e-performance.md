# JIT compilation, performance and garbage collector (Ruby 3.0 to 3.4)

Convention: `(R3x p.N)` = PDF page of the note (see `INDEX.md`).

## 1. Ruby 3x3 goal (Ruby 3.0)
- `[from source]` Since 2015 development has aimed at performance, concurrency and typing; Matz declared that Ruby 3 would be 3 times faster than Ruby 2 ("Ruby 3x3") (R30 p.1).
- `[from source]` With the Optcarrot benchmark (NES emulation, measures single-thread performance), Ruby 3.0 reached 3 times the performance of Ruby 2.0 (R30 p.1). Matz qualifies it: "in some benchmarks" (R30 p.2).
- `[from source]` The 3.1 note confirms that Ruby 3x3 was achieved, but says that the JIT, despite the gains on Optcarrot, did not benefit real business applications (R31 p.1).

## 2. MJIT
- `[from source]` MJIT entered Ruby 2.6 (2018) (R31 p.1). It is a method-based JIT and uses an external C compiler (R31 p.2).
- `[from source]` In 3.0, the JIT was supposed to give a gain in limited workloads (games such as Optcarrot, AI such as Rubykon, applications that spend most of their time calling a few methods many times); it was not yet ready for workloads such as Rails, which spend time in many methods and suffer from instruction cache (i-cache) misses aggravated by the JIT (R30 p.2). The JIT code had shrunk considerably in size (R30 p.2).
- `[from source]` 3.1: `--jit-max-cache` default went from 100 to 10000; methods with more than 1000 instructions are no longer skipped; JIT code is not canceled when a TracePoint for class events is enabled (support for Rails' Zeitwerk) (R31 p.8).
- `[from source]` 3.2: MJIT reimplemented in Ruby (`ruby_vm/mjit/compiler`), compilation in a child process (fork) instead of the "MJIT worker" native thread; MSWIN and MinGW are no longer supported; `--mjit-min-calls` renamed to `--mjit-call-threshold`; `--mjit-max-cache` goes back from 10000 to 100 (R32 p.11).
- `[from source]` 3.3: RJIT (JIT in pure Ruby) was introduced and **replaced MJIT** (R33 p.4).
- `[DATED]` MJIT: do not use it as a production recommendation; 3.0 itself describes it as limited to certain workloads (R30 p.2).

## 3. YJIT
- `[from source]` 3.1: YJIT is a new "in-process" JIT (no external compiler), developed by Shopify, aimed at speeding up Rails applications (R31 p.1-2). It uses Basic Block Versioning; with Lazy Basic Block Versioning (LBBV) it first compiles the start of the method and the rest incrementally once the types of arguments and variables are determined (R31 p.2).
- `[from source]` Gains in 3.1: up to 22% on railsbench and 39% on liquid-render (R31 p.2). Experimental, disabled by default; enabled with `--yjit`; limited to Unix-like x86-64 platforms (R31 p.2).
- `[from source]` 3.2: YJIT is no longer experimental ("tested in production for more than a year and quite stable"); supports x86-64 and arm64/aarch64 on Linux, macOS, BSD and other Unix (includes Apple M1/M2, AWS Graviton, Raspberry Pi 4); compiling requires Rust 1.58.0 or higher (`rustc`) before `./configure` (R32 p.4).
- `[from source]` 3.2: faster than 3.1, with about 1/3 of the memory overhead; 41% faster (geometric mean) than the interpreter on yjit-bench; physical memory for JIT code allocated on demand; Code GC frees the pages when consumption reaches `--yjit-exec-mem-size`; `RubyVM::YJIT.runtime_stats` gains Code GC metrics; `--yjit-stats` collects statistics (at some cost) (R32 p.4). Defaults: `--yjit-exec-mem-size` 64 MiB and `--yjit-call-threshold` 30 (R32 p.5).
- `[from source]` 3.3: large gains over 3.2 (better support for splat/rest, registers, more calls compiled, inlining of methods such as Rails' `#blank?` and `#present?`) (R33 p.2); more than 3x faster than the interpreter on Optcarrot (R33 p.3).
- `[from source]` 3.3, memory: `--yjit-call-threshold` rises from 30 to 120 automatically with more than 40,000 ISEQs; `--yjit-cold-threshold` added; Code GC disabled by default, and `--yjit-exec-mem-size` becomes a hard limit (re-enabled with `--yjit-code-gc`) (R33 p.3).
- `[from source]` 3.3: `RubyVM::YJIT.enable` enables YJIT at run time (for example, after the application boots); the note says Rails 7.2 would enable it by default through that method; `--yjit-disable` allows using other YJIT options without enabling it at startup (R33 p.3). Also `--yjit-perf` (Linux perf) and `--yjit-trace-exits` with sampling (R33 p.3).
- `[from source]` 3.4: `--yjit-mem-size` (unified limit, default 128 MiB) as an alternative to `--yjit-exec-mem-size`; `--yjit-log` and `RubyVM::YJIT.log`; `RubyVM::YJIT.runtime_stats` with invalidation, inlining and metadata encoding statistics; compressed context; registers for local variables and arguments; `Array#each`, `Array#select` and `Array#map` rewritten in Ruby with YJIT on (Feature #20182); inlining of trivial methods (R34 p.3-4).
- `[extrapolation]` The environment variable `RUBY_YJIT_ENABLE=1`, Puma/Docker integration and the `compiled_iseq_count` key are **not** in the notes. Use `--yjit` (R31 p.2) or `RubyVM::YJIT.enable` (R33 p.3).
- `[extrapolation]` "Rewritten in Rust": the notes say only that compiling YJIT requires Rust (R32 p.4).

## 4. RJIT (Ruby 3.3)
- `[from source]` Pure Ruby JIT that replaced MJIT; supports only x86-64 on Unix; does not require a C compiler at run time; exists "for experimental purposes only" and the note recommends **continuing to use YJIT in production** (R33 p.4).

## 5. Garbage collector and allocation
- `[from source]` 3.3: young objects referenced by old objects are no longer promoted immediately, reducing the frequency of major GC (Feature #19678); new variable `REMEMBERED_WB_UNPROTECTED_OBJECTS_LIMIT_RATIO` (default 0.01) (R33 p.5). Write barriers on several types (Time, Enumerator, MatchData, Method, File::Stat, BigDecimal and others); Variable Width Allocation for Hash, Time, Thread::Backtrace and other classes; weak references in the GC (R33 p.5). `defined?(@ivar)` optimized with Object Shapes (R33 p.5).
- `[from source]` 3.3: the variable `RUBY_GC_HEAP_INIT_SLOTS` was deprecated and is a no-op; use `RUBY_GC_HEAP_{0,1,2,3,4}_INIT_SLOTS` (R33 p.6).
- `[from source]` 3.4: modular GC: `--with-modular-gc` at build time and `RUBY_GC_LIBRARY` at run time; default GC separated into `gc/default/default.c`; experimental library based on MMTk (requires a Rust toolchain) (R34 p.4). `GC.config` and the `rgengc_allow_full_mark` parameter (R34 p.5-6).
- `[from source]` 3.1: Variable Width Allocation for Strings, experimental (R31 p.8).
- `[from source]` 3.4: redefining optimized core methods (`String.freeze`, `Integer#+`) emits a "performance" category warning with `-W:performance` or `Warning[:performance] = true` (R34 p.10).
- `[extrapolation]` "Heap compaction" and "pause reduction" of the GC are not in the notes read.

## 6. Other performance items in the notes
- `[from source]` 3.0: pasting long code into IRB became 53 times faster (11.7 s to 0.22 s) (R30 p.6). 3.4: `JSON.parse` about 1.5 times faster than json-2.7.x (R34 p.7). 3.2: `ERB::Util.html_escape` faster than `CGI.escapeHTML` (R32 p.18).
