# Capítulo 13 — Concorrência (Concurrency; by Brett L. Schuchert)

Source: CL ch. 13, PDF p.174-187 (opening and epigraph on p.174; text from p.175).

Author: Brett L. Schuchert (CL p.174). The chapter is an overview; the deeper treatment is in Appendix A,
"Concorrência II" (Concurrency II) (CL p.175; appendix at PDF p.310). The text refers to printed "page 317", which is not the PDF page.

## Why concurrency?
- Concurrency is a decoupling strategy: it separates **what** is done from **when** it is done (CL p.175).
- In a single-threaded application, what and when are so coupled that the call stack shows the whole state (CL p.175).
- Structural benefit: the system becomes many small computers collaborating, which can make it easier to understand and to separate concerns (e.g. the Servlets model) (CL p.175).
- Performance benefit: response-time and throughput requirements (a site aggregator that takes over 24 h; a user waiting behind 150; processing data sets in parallel) (CL p.175-176).
- The decoupling provided by Web containers is far from perfect; the programmer must still ensure correctness (CL p.175).

## Myths and misconceptions
- Myth: concurrency always improves performance. It only does when there is a lot of waiting time that can be shared among threads or processors (CL p.176).
- Myth: the design does not change when writing concurrent programs. The decoupling of what/when changes the structure a lot (CL p.176).
- Myth: with a Web or EJB container you do not need to understand concurrency. You need to know what the container does and how to guard against concurrent update and deadlock (CL p.176).
- Balanced statements according to the book (CL p.176):
  - concurrency incurs some overhead, in performance and in additional code;
  - correct concurrency is complex, even for simple problems;
  - concurrency bugs are usually not repeatable and so are often ignored as one-offs;
  - concurrency often requires a fundamental change in design strategy.

## Challenges
- A shared `++lastIdUsed` between two threads can produce three results, one of them incorrect (both get the same value) (CL p.177).
- There are 12,870 possible execution paths for two threads in that method with `int`; with `long`, 2,704,156 (CL p.177).
- Most paths give a valid result; the problem is that some do not (CL p.177).

## Concurrency defense principles
### SRP
- The concurrency model is complex enough to be a reason to change of its own and should be separated from the rest of the code (CL p.177).
- Concurrency code has its own life cycle of development, change and tuning, and its own, harder challenges (CL p.177).
- Recommendation: keep concurrency-related code separate from other code (CL p.178).

### Limit the scope of data
- Use `synchronized` to protect critical sections that use the shared object, and restrict the number of such sections (CL p.178).
- More places that change shared data increase the chance of forgetting to protect one, of duplicating effort (violating DRY) and of making it hard to find the source of failures (CL p.178).
- Recommendation: take data encapsulation seriously and severely limit access to any data that may be shared (CL p.178).

### Use copies of data
- Copy objects and treat the copies as read-only, or let each thread produce a result in a copy and merge them in a single thread (CL p.178).
- The extra cost of creating objects and garbage collection is probably worth it if it avoids synchronization; measure before worrying (CL p.178).

### Threads should be as independent as possible
- Each thread in its own world, sharing no data, with everything in local variables (example: servlets that receive everything as parameters in `doGet`/`doPost`) (CL p.178-179).
- Recommendation: partition the data into independent subsystems that can be handled by independent threads, possibly on different processors (CL p.179).

## Know your library
- Items to consider in Java 5: use the thread-safe collections; use the Executor framework for unrelated tasks; use non-blocking solutions whenever possible; know the library classes that are not thread safe (CL p.179).
- The `java.util.concurrent` collections (originating in Doug Lea's work) are safe and efficient; `ConcurrentHashMap` outperforms `HashMap` in nearly all cases and has safe compound operations; start with it (CL p.179).
- Other classes cited: `ReentrantLock` (a lock acquired in one method and released in another), `Semaphore` (a counting semaphore) and `CountDownLatch` (waits for N events before releasing the threads) (CL p.179).
- Recommendation: review the available classes; in Java, `java.util.concurrent`, `.atomic` and `.locks` (CL p.179).

## Know your execution models
- Basic definitions: bound resources, mutual exclusion, starvation, deadlock and livelock (CL p.180).
- Producer-consumer: producers put tasks into a bounded queue, consumers take them out; both wait and signal (queue not empty / not full) (CL p.180).
- Readers-writers: balance readers and writers without starvation and with reasonable throughput; writers waiting on readers can starve, priority writers lower throughput (CL p.181).
- Dining philosophers: threads competing for resources (forks); without care, there is deadlock, livelock and loss of throughput (CL p.181).
- Most concurrency problems will be a variation of these three; recommendation: learn these basic algorithms and their solutions (CL p.181).

## Beware dependencies between synchronized methods
- Dependencies between synchronized methods cause subtle bugs; `synchronized` protects one method, but the client may use several in sequence (CL p.181).
- Recommendation: avoid using more than one method on a shared object (CL p.182).
- When it is necessary, three ways out (CL p.182):
  - client-based locking: the client locks the server before the first method and holds the lock until the last;
  - server-based locking: create a method on the server that locks, calls everything and unlocks;
  - adapted server: an intermediary server does the locking when the original server cannot be changed.

## Keep synchronized sections small
- Locks cause delays and overhead; do not scatter `synchronized` around, but do protect the critical sections (CL p.182).
- Have as few critical sections as possible, but do not enlarge them to achieve that: extending synchronization beyond the minimum increases contention and worsens performance (CL p.182).
- Recommendation: keep synchronized sections as small as possible (CL p.182).

## Writing correct shut-down code is hard
- Shutting down properly is hard: deadlock with threads waiting for a signal that never arrives (a parent waiting for a stuck child; a producer/consumer pair in which the consumer stays blocked without receiving the signal) (CL p.182).
- If you need proper shutdown, expect to spend a good part of your time on it (CL p.182).
- Recommendation: think about shutdown early, get it working and review existing algorithms (CL p.183).

## Testing threaded code
- Tests do not prove correctness, but they reduce risk; with threads and shared data everything gets more complex (CL p.183).
- General recommendation: write tests able to expose problems and run them frequently, varying programmatic, system and load configurations; if a test fails, track it down, even if it passes on the next run (CL p.183).
- The seven detailed recommendations (CL p.183):
  1. Treat spurious failures as candidate threading issues: do not dismiss failures as cosmic rays or one-offs (CL p.183).
  2. Get your nonthreaded code working first: use POJOs called by the threads and do not mix hunting common bugs with hunting thread bugs (CL p.183-184).
  3. Make your threaded code pluggable (configurable to run in several configurations): run with one or several threads, with fast, slow and varying test doubles, and with a configurable number of iterations (CL p.184).
  4. Make your threaded code tunable: allow the number of threads to be adjusted, even at run time, and consider self-tuning by throughput and usage (CL p.184).
  5. Run with more threads than processors, to force task switching and reveal missing critical sections or deadlock (CL p.184).
  6. Run on different platforms, early and often, on all target platforms; each OS has a different threading policy (CL p.184-185).
  7. Instrument your code to try to force failures: inserting calls such as wait, sleep, yield and priority changes the execution order and increases the chance of exposing errors (CL p.185).
- Manual instrumentation: inserting `yield()` etc. by hand; if it fails, the error was already there. Problems: finding the places, knowing what to insert, leaving junk in production and being a shot in the dark (CL p.185-186).
- Automated instrumentation: with aspects, CGLIB or ASM; for example a `ThreadJigglePoint` class with an empty implementation in production and a random implementation (sleep, yield or proceed) in test, running the tests many times (CL p.186-187).
- IBM has the ConTest tool, which does something similar with more sophistication (CL p.187).

## Chapter conclusion
- First of all, follow the SRP: separate the code that knows about threads from the code that does not, into POJOs (CL p.187).
- Know the sources of problems: multiple threads on shared data or common resources; boundary cases such as shutting down or ending a loop (CL p.187).
- Lock only what is necessary; avoid calling one locked section from inside another; keep few shared objects and a short scope (CL p.187).
- Run the threaded code many times, in many configurations and platforms; the testability of the Three Laws of TDD helps with this (CL p.187).

## Examples from the book
- Class `X` with `getNextId()` and the three possible results (CL p.176-177).
- Table of execution model definitions (CL p.180).
- `nextUrlOrNull` instrumented with `Thread.yield()` by hand (CL p.185) and with `ThreadJigglePoint.jiggle()` (CL p.186).

## What the chapter does NOT say / common confusions
- It does not say that concurrency always speeds things up; it says the opposite (CL p.176).
- It does not forbid `synchronized`; it asks for minimal and few sections (CL p.182).
- Translation/printing errors: the three results list "thread um" (thread one) twice (the second is the other thread) (CL p.177); the instrumentation section speaks of `Object.sleep`, `Object.yield` and `Object.priority` (CL p.185). [extrapolation] In Java, `sleep` and `yield` are `Thread` methods, and priority is set through `Thread.setPriority`.
- The fourth item of "Know your library" appears truncated in the translation; the meaning is to know the classes that are not thread safe [inference] (CL p.179).

## [DATED]
- Java 5 is presented as the new reference platform (CL p.179).
- ConTest (IBM) is a 2008 tool; check whether it still exists before recommending it [extrapolation] (CL p.187).
- Experiment on OS X and Windows XP in a VM, from 2007 (CL p.184).
