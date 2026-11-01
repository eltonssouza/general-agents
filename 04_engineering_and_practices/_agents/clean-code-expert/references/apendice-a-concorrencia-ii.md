# Appendix A — Concurrency II (by Brett L. Schuchert)

Source: CL Appendix A, PDF p.310-340 (opening and first heading on p.310; tutorial with full code p.336-340; Appendix B starts on p.341).

Extension of ch. 13, in independent topics that can be read in any order (CL p.310).
Internal page references ("página 177", "página 343", "p. 321") are printed pages, not PDF pages.

## Client/server example
- A single-threaded server accepts a connection, processes it, and goes back to waiting; a test with a 10,000 ms timeout validates the throughput of a series of requests (CL p.310-311).
- Before adding threads, find out where the time is spent: I/O (sockets, database, virtual memory) or processor (computation, regex, garbage collection) (CL p.311).
- Adding threads to a processor-bound problem does not make it faster; in an I/O-bound problem, concurrency can increase efficiency, since one part uses the CPU while another waits (CL p.311-312).
- Creating one thread per request passes the test but is naive: there is no limit on threads (risk with many users) (CL p.312).
- The server accumulates responsibilities: managing connections, processing the client, thread policy, and shutdown policy (CL p.312).
- This violates the SRP; thread management should live in a few well-controlled places, and code that manages threads should do only that (CL p.313).
- Solution: one class per responsibility; all thread policy behind a `ClientScheduler` interface, so concurrency problems have a single place to look (CL p.313).
- Changing the policy (e.g., to the Java 5 Executor framework with a fixed pool) becomes a matter of creating a new class and plugging it in (CL p.314).
- Centralizing concurrency code in a few classes is an application of the SRP (CL p.314).

## Possible execution paths
- With one thread, `return ++lastIdUsed;` has a single path and a guaranteed result (CL p.314).
- With two threads there are three possible results, including both receiving the same value (CL p.315).
- The Java line becomes eight bytecode instructions; two threads can interleave them like shuffled cards (CL p.315).
- Uncle Bob's email formula: with N steps and T threads, paths = (T*N)! / (N!^T); examples: N=2,T=2 → 6; N=2,T=3 → 90; N=3,T=3 → 1680 (CL p.315-316; formula checked against the image on p.316).
- For the real case (8 bytecodes, 2 threads): 12,870 paths; with `long`, 2,704,156 (CL p.316).
- With `synchronized`, the paths drop to two with two threads and N! in the general case (CL p.316).

### Going deeper: atomicity and the memory model
- Assigning a 32-bit value is atomic under the Java memory model (CL p.316).
- Per the JVM specification, assigning a 64-bit value (`long`) requires two 32-bit assignments; another thread can slip in between them (CL p.317).
- The pre-increment `++` can be interrupted, so it is not atomic (CL p.317).
- Definitions used: frame, local variable, operand stack (LIFO) (CL p.317).
- Assigning a constant (`resetId`) is safe even with ten threads: there is only one possible result (CL p.318).
- In `getNextId`, one thread reads 42 with GETFIELD and is interrupted, the other runs everything and writes 43; the first resumes and also writes 43: one increment is lost. Synchronizing the method solves it (CL p.318-319).
- Lesson: understand the memory model well enough to know what is safe; `++` (pre or post) is not atomic. Know where shared values are, which code can cause concurrent reads/updates, and how to avoid them (CL p.319).

## Know your library
### Executor framework and futures
- If you create threads by hand or without a pool, consider the Executor (Java 5, `java.util.concurrent`): cleaner, shorter code that is easy to follow (CL p.319).
- The Executor manages the pool, resizes and recreates threads, and supports futures (CL p.319).
- It works with `Runnable` and with `Callable`, which returns a result (CL p.319).
- A future is useful for launching independent operations and waiting for both; `get()` blocks until the future finishes (CL p.319-320).

### Nonblocking solutions
- Classes such as `AtomicBoolean`, `AtomicInteger`, and `AtomicReference` allow safe updates without locking (CL p.320).
- The atomic version almost always beats the synchronized one; cases where it is slower practically do not exist (CL p.320).
- Basis: the processor's CAS (compare-and-swap) operation, analogous to optimistic database locking; `synchronized` is analogous to pessimistic locking and always acquires a lock (CL p.320-321).
- CAS checks whether the variable still has the last known value; if another thread changed it, it tries again. Detecting is usually cheaper than locking, even under moderate to high contention (CL p.321).

### Nonthread-safe classes
- Examples: `SimpleDateFormat`, database connections, `java.util` containers, servlets (CL p.321).
- Individually safe methods do not make an operation that calls two of them safe (e.g., `containsKey` + `put` on a `Hashtable`) (CL p.321-322).
- Solutions: client-based locking (`synchronized(map)` with all users doing the same); server-based locking with an ADAPTER that offers `putIfAbsent`; or thread-safe collections such as `ConcurrentHashMap.putIfAbsent` (CL p.322).

## Dependencies between methods
- An `IntegerIterator` with synchronized `hasNext()` and `next()` still fails with two threads: both see `hasNext()` true on the last element and one runs past the end. The problem is that the client uses two methods (CL p.322-323).
- This bug appears only in the final iteration, late and in production (CL p.323).
- Three options: tolerate the failure; client-based locking; server-based locking (CL p.323).
- Tolerating the failure (catching and ignoring the exception) is sloppy, comparable to rebooting at midnight to free memory (CL p.324).
- Client-based locking duplicates code in every client (violates DRY) and is risky: one programmer forgetting is enough. The story of the Local 705 union system (1971) shows a circular-buffer bug lasting weeks caused by a single unprotected use (CL p.324-325).
- Server-based locking: change the API to a synchronized `getNextOrNull()`; the client checks for `null` (CL p.325-326).
- Prefer server-based locking because (CL p.326): it reduces repeated code; it allows switching to a non-thread-safe version in single-threaded use, gaining performance; it reduces the chance of error; it enforces a single policy in one place; it reduces the scope of shared variables.
- If the server is not yours: use an ADAPTER that changes the API and adds the locking, or, better, thread-safe collections with extended interfaces (CL p.326).

## Increasing throughput
- Example: read and parse pages from a list of URLs; the shared `PageIterator` synchronizes only the critical section; it is always better to synchronize the minimum (CL p.326-327).
- Assumptions: I/O 1 s per page, parsing 0.5 s, I/O uses 0% of the CPU and parsing 100% (CL p.327-328).
- One thread: 1.5 s × N; 13 pages ≈ 19.5 s (CL p.328).
- With several threads, parsing (CPU) overlaps with reading (I/O): two pages per second, three times the throughput of one thread (CL p.328).

## Deadlock
- Example: an application with a pool of 10 database connections and 10 MQ connections; the create and update operations acquire the resources in opposite orders and the system hangs (CL p.328-329).
- Inserting debugging statements changes the timing and makes the deadlock vanish or move (CL p.329).
- The four necessary conditions (CL p.329-330):
  1. Mutual exclusion: resources that cannot be used by several threads at the same time and are limited (database connection, file open for writing, record lock, semaphore);
  2. Lock and wait: a thread holds a resource until it obtains all the others it needs;
  3. No preemption: one thread does not take a resource from another;
  4. Circular wait ("deadly embrace"): T1 holds R1 and wants R2; T2 holds R2 and wants R1.
- All four must be present; breaking just one makes deadlock impossible (CL p.330).

### How to break each condition
- Mutual exclusion: use resources that allow simultaneous use (e.g., `AtomicInteger`), have as many resources as threads, or check that all are free before taking any. Limitation: most resources are limited and exclusive (CL p.330-331).
- Lock and wait: do not wait; check each resource and, if one is busy, release all and start over. Risks: starvation (low CPU) and livelock (high, useless CPU). Inefficient, but almost always implementable as a last resort (CL p.331).
- Preemption: allow asking the holder of the resource to release it; a holder that is also waiting releases everything and starts over. Fewer restarts, but managing the requests is tricky (CL p.331).
- Circular wait: the most common method; all threads acquire resources in an agreed global order (CL p.331).
- Problems with ordering: the acquisition order may not match the order of use, holding resources longer; and sometimes ordering is impossible, when the second resource depends on the result of the first (CL p.332).
- Isolating the threading part of the solution allows experimenting and choosing the strategy (CL p.332).

## Testing multithreaded code
- Test shown: two threads calling `takeNextId()` and checking that the value advanced by two units, repeating until it fails (CL p.332-334).
- This test rarely catches the error: it needs more than a million iterations and still fails rarely; much larger values and per-machine, per-OS, per-JVM readjustments would be needed (CL p.334).
- Ideas (CL p.334):
  - Monte Carlo testing: tunable tests run repeatedly with randomly varied parameters, preferably on an integration server; record the failure conditions;
  - run on every target platform, repeatedly and constantly;
  - run on a machine with varied loads, simulating production.
- Even so the odds are low; the worst bugs occur once in a billion (CL p.335).

## Tools
- IBM's ConTest alters (instruments) classes to change the execution order; see the translation confusion about its effect below (CL p.335).
- Use: create tests and code that simulate several users under varied loads; instrument test and production with ConTest; run (CL p.335).
- Reported result: from one failure in ten million iterations to one in about thirty (CL p.335).
- Recommended reading: Doug Lea, Concurrent Programming in Java (CL p.335).

## Examples from the book
- Server and client without threads, throughput test with timeout (CL p.310-311; full code p.336-339).
- Server with thread per request and refactoring with `ClientScheduler`/`ThreadPerRequestScheduler`; Listing A-1 `ExecutorClientScheduler` (CL p.312-314, p.340).
- Bytecode tables of `resetId` and `getNextId` (CL p.317-319).
- Synchronized `ObjectWithValue` versus `AtomicInteger`; logical simulation of CAS (CL p.320-321).
- `IntegerIterator`, `IntegerIteratorServerLocked`, `ThreadSafeIntegerIterator` (CL p.322-326).
- `PageReader`/`PageIterator` and Figures A.1/A.2 (CL p.326-328).
- Listing A-2: `ClassWithThreadingProblemTest` with an explanatory table of the lines (CL p.332-334).

## What the appendix does NOT say / common confusions
- Translation error: the text defines atomic operation as "qualquer operação que seja interrompível" (literally, "any operation that is interruptible") (CL p.316). [inference] The book's own reasoning (`++` is not atomic precisely because it can be interrupted, CL p.317) shows that the correct meaning is uninterruptible.
- Translation error: it says ConTest makes it "less likely" that unsafe code fails (CL p.335), but the numbers on the same page show far more frequent failures. Use the meaning: it makes failures more likely [inference].
- Contradictory footnote: it says the Iterator interface is "inherently thread-safe" and right after that it was never designed for multiple threads (CL p.326). [inference] The meaning is that it is not safe.
- The four conditions are not attributed to Coffman in the book (CL p.329).
- The book does not cover `ExecutorService` beyond the example, nor `CompletableFuture`, `ReadWriteLock`, `volatile` as a topic, or virtual threads.

## [DATED]
- Java 5 as a novelty (Executor, atomic classes, "Java 5" JVM) (CL p.314, p.319-320).
- `Hashtable`, Commons HttpClient (`GetMethod`) and JUnit 4 `@Test(timeout=...)` (CL p.311, p.321-322, p.327).
- IBM's ConTest: a 2008 tool; confirm availability before recommending [extrapolation] (CL p.335).
- [extrapolation] Later APIs (`CompletableFuture`, virtual threads) are not in the book; when mentioning them, label them as outside the book.
