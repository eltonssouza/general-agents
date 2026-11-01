# Concurrency and parallelism: Ractor, Fiber Scheduler, M:N threads

Page convention: `(R30 p.N)` etc. = PDF page of the respective note (see `INDEX.md`). Labels: `[from source]` = it is on the cited page; `[inference]`, `[extrapolation]`, `[DATED]`, `[VERSION-DEPENDENT]`.

## 1. Ractor (Ruby 3.0, experimental)
- `[from source]` Ractor is an "actor-like" concurrent abstraction, designed for parallel execution without thread-safety concerns (R30 p.2).
- `[from source]` Several ractors can be created and run in parallel; safety comes from ractors not being able to share "normal" objects; communication is by message passing (R30 p.2).
- `[from source]` To limit sharing, Ractor imposes restrictions on syntax; without multiple Ractors there is no restriction (R30 p.2).
- `[from source]` The specification and implementation were immature, so the feature is marked experimental and emits an "experimental feature" warning on the first `Ractor.new` (R30 p.2).
- `[from source]` Official example: the function `tarai(14, 7, 0)` run 4 times in sequence versus 4 `Ractor.new` in parallel, collected with `take` (R30 p.3). Measured result: real time of 64.56 s (sequential) against 16.69 s (parallel), "3.87 times faster", on an Ubuntu 20.04 machine with an Intel i7-6700 (4 cores, 8 hardware threads) (R30 p.3).
- `[from source]` The notes refer to `doc/ractor.md` for details (R30 p.3). Rules on shareable objects (`shareable`), copying and ownership transfer (`move`) are **not** in the notes: see section 5.
- `[from source]` Ruby 3.3: M:N threads are always enabled in Ractors other than the main one (R33 p.4).
- `[from source]` Ruby 3.4: `require` inside a Ractor is now allowed (the loading process runs in the main Ractor); `Ractor._require(feature)`, `Ractor.main?`, `Ractor.[]` and `Ractor.[]=` (Ractor-local storage) and `Ractor.store_if_absent(key){ init }` were added (R34 p.6). YJIT 3.4 also supports shareable constants in multi-ractor mode (R34 p.4).
- `[inference]` Ractor is the notes' option for CPU parallelism in pure Ruby code, but the feature was born experimental in 3.0 and the 3.3 and 3.4 notes only bring specific adjustments; confirm the current state in the documentation of the version in use.

## 2. Fiber Scheduler (Ruby 3.0)
- `[from source]` `Fiber#scheduler` was introduced to intercept blocking operations, which allows lightweight concurrency without changing existing code (R30 p.3).
- `[from source]` Classes and methods supported at the time: `Mutex#lock`, `Mutex#unlock`, `Mutex#sleep`, `ConditionVariable#wait`, `Queue#pop`, `SizedQueue#push`, `Thread#join`, `Kernel#sleep`, `Process.wait`, and `IO#wait`, `IO#read`, `IO#write` and related methods (`#gets`, `#puts`...) (R30 p.3). `IO#select` was not supported (R30 p.3).
- `[from source]` The example uses the `async` gem, which provides the event loop; this loop uses the `Fiber#scheduler` hooks to make `Net::HTTP` non-blocking. Other gems can use the same interface, and other implementations (JRuby, TruffleRuby) can offer the same hooks (R30 p.4).
- `[extrapolation]` The scheduler registration API (`Fiber.set_scheduler`) and the choice between `async` and other schedulers are not in the notes.
- `[extrapolation]` Scale claims ("tens of thousands of connections") are not in the notes.

## 3. M:N threads (Ruby 3.3)
- `[from source]` The M:N thread scheduler (Feature #19842): M Ruby threads are managed by N native threads, reducing creation and management cost (R33 p.4).
- `[from source]` It may break compatibility with C extensions, so it is disabled in the main Ractor by default; `RUBY_MN_THREADS=1` enables it there; always enabled in the other Ractors (R33 p.4).
- `[from source]` `RUBY_MAX_CPU=n` sets the maximum N (default 8). Since only one Ruby thread per Ractor runs at a time, the number of native threads is the smaller of `RUBY_MAX_CPU` and the running Ractors, so single-Ractor applications use 1 native thread (R33 p.4). Blocking operations may use more than N native threads (R33 p.5).
- `[VERSION-DEPENDENT]` Only from Ruby 3.3.

## 4. Other concurrency/system items
- `[from source]` 3.3: `Socket.getaddrinfo` and similar name resolutions can now be interrupted where pthreads exist (R33 p.5).
- `[from source]` 3.4: `TCPSocket.new` (`TCPSocket.open`) and `Socket.tcp` implement Happy Eyeballs v2 (RFC 8305): concurrent IPv6/IPv4 resolution, attempts with IPv6 priority staggered every 250 ms, first successful connection wins; enabled by default; disabled with `RUBY_TCP_NO_FAST_FALLBACK=1`, `Socket.tcp_fast_fallback=false` or `fast_fallback: false` (R34 p.2).
- `[from source]` 3.4: `Timeout.timeout` rejects negative values (R34 p.10).

## 5. What the notes do NOT say (do not attribute to the source)
- GVL/GIL: the acronym does not appear in the five notes; "without the GVL" is `[extrapolation]` (what the notes say is "parallel without thread-safety concerns", R30 p.2).
- Rules of `shareable`/`unshareable`, `Ractor.yield`, `Ractor.receive`, `send`, `move: true`, deep copy and `Ractor::IsolationError`: `[extrapolation]` (the notes only mention `Ractor.new` and `take`, and point to `doc/ractor.md`, R30 p.3).
- Pools, Sidekiq, Puma, Rails: outside the notes.
