---
name: rust-concurrency-async-review
description: Chooses and reviews the concurrency model in Rust — threads, channels (mpsc), `Arc<Mutex<T>>`, async/await, futures, `join`/`select`, streams, `Send`/`Sync` — and diagnoses errors such as E0373, unsatisfied `Send`, and deadlock. Use when the user asks "threads or async?", "how do I share state between threads", "my future doesn't run", "async blocking", "implement a worker pool", or pastes code with `thread::spawn`, `tokio`/`async fn`. Do not use for general compilation errors (use rust-compiler-error-triage).
---

# Concurrency and async in Rust

Sources: Book ch. 16–17 and 21 (Book p.458–534, 664–686), RBE p.298–306. Decision trees in `../../references/frameworks.md` (Concurrency section).

## Procedure

1. **Classify the workload**: CPU-bound or I/O-bound? How many tasks? Is an async runtime already adopted? Embedded without an OS? (Book p.532–534).
2. **Decide the model**:
   - A few CPU-heavy tasks → **threads**.
   - Many I/O waits → **async** with a runtime (Rust does not bundle a runtime — Book p.494, 496).
   - The two can be combined, e.g., an async channel between a thread and a runtime (Book p.532–534).
3. **If threads**, choose the primitive: **channel (mpsc)** to transfer ownership/messages; **`Arc<Mutex<T>>`** for shared state; **atomics** for simple counters (Book p.469, 476, 481).
   - Error "closure may outlive" (E0373) → missing `move`. Use after `move` (E0382) → clone before (e.g., `Arc::clone`) or redesign ownership. Unsatisfied `Send` (E0277) → the type (e.g., `Rc`) cannot cross threads; swap it for `Arc` (Book p.464–481, 483).
   - `Send` = ownership transferable between threads; `Sync` = `&T` is `Send` (Book p.483).
   - Review lock acquisition order (deadlock) and what to do on `lock().unwrap()` / `send().unwrap()` (poisoned mutex: `lock` fails if another thread that held the lock panicked, Book p.476; closed receiver; deadlock, Book p.482).
4. **If async**, go through the checklist:
   - Missing `.await` → futures are lazy and do not run (Book p.492).
   - **Blocking** call inside async → starvation of the other tasks (Book p.510–513).
   - `async move` when the block must be the owner (e.g., dropping `tx` so the channel closes) (Book p.507–508).
   - `join` waits for all and is fair; `select` takes the first and the poll order matters (Book p.501–502, 515).
   - `StreamExt` in scope; `Pin`/`Unpin` when storing futures in collections (Book p.518, 529).
   - Timeout/retry/race between sources with `select` + `sleep` (Book p.514–516).
5. **Worker pool with channels** (recipe): `Arc<Mutex<Receiver<Job>>>`, `Job = Box<dyn FnOnce() + Send + 'static>`, shutdown by dropping the `Sender` and calling `join`; pitfalls: a lock guard held across a `while let`, `unwrap` in `Drop` (Book p.664–686).

## Response format

The model recommendation (with the decision rule), the checklist points that apply to the user's code, and the corrected snippet. Mark **[inference]** wherever you are extrapolating.

## Limits

- The book's `trpl::*` APIs belong to the book's support crate, not to std nor to a production runtime (Book ch. 17). When recommending a concrete runtime, say the choice belongs to the project and is outside the book's scope.
- Figures in ch. 17 were not legible in the extraction; the conclusions come from the text.
