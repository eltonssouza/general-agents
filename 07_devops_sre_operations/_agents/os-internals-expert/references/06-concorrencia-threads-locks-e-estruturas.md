# 06. Concurrency: threads, pthread API, locks and concurrent structures (ch. 26, 27, 28, 29)

PDF: ch.26 = p.52-67; ch.27 = p.133-144; ch.28 = p.213-234; ch.29 = p.315-330; dialogue = p.10-11.

## 1. Threads and the origin of the problem (ch.26)

- **[from source]** **Thread** = another point of execution (another PC) in the same address space; each thread has its own registers and **stack** (thread-local storage); switching between threads uses the **TCB** and does not switch the page table (OSTEP p.52-53).
- **[from source]** Reasons for threads: **parallelism** and avoiding blocking on I/O; processes are better for separate tasks with little sharing (OSTEP p.53-54).
- **[from source]** Counter example: two threads adding 1e7 times; observed results 19345221 and 19221041 instead of 20,000,000 (OSTEP p.57-59). Cause: `counter++` becomes load/add/store; with interleaving (T1 and T2 read 50) the result is 51 instead of 52 (OSTEP p.60-61).
- **[from source]** Terms (Dijkstra): **critical section**, **race condition** (data race), **indeterminate** program, **mutual exclusion** (OSTEP p.61, p.64). **Atomicity** = "all or nothing" (transaction) (OSTEP p.62). There are two interactions: atomicity and **waiting for another** (sleep/wake) (p.62-63). The OS was the first concurrent program (p.64).

## 2. pthread API (ch.27)

- **[from source]** `pthread_create(thread, attr, start_routine, arg)`; `pthread_join(thread, value_ptr)`; never return a pointer to a variable on the thread's stack (OSTEP p.133-137).
- **[from source]** Locks: `pthread_mutex_lock/unlock`; typical errors: not initializing (`PTHREAD_MUTEX_INITIALIZER` or `pthread_mutex_init`) and not checking return codes; `trylock` and `timedlock` should generally be avoided (OSTEP p.137-139).
- **[from source]** Condition variables: `pthread_cond_wait(cond, mutex)` releases the lock when it sleeps and reacquires it on return; always `while` (spurious wakeup = only a "hint"); **never** synchronize with a spinning flag: about half of the ad hoc uses studied were buggy (OSTEP p.139-141). Compile with `-pthread` (p.141). Usage tips (p.142). The book's tool: helgrind (p.144).

## 3. Locks (ch.28)

- **[from source]** Criteria: **mutual exclusion**, **fairness** (starvation) and **performance** (no contention; contention on one CPU; multiple CPUs) (OSTEP p.215).
- **[from source]** Disabling interrupts: simple, but requires trusting the user, does not work on multiprocessors and may lose interrupts; only inside the OS (OSTEP p.216-217). A flag with load/store fails because of interleaving (OSTEP p.217-218).
- **[from source]** **Test-and-set** (atomic exchange; x86 xchg) → **spin lock**; correct, **no fairness**, bad on 1 CPU (preemptive) and acceptable on multiple CPUs with a short critical section (OSTEP p.218-222). **Compare-and-swap** (compare-and-exchange) (p.222-223). **Load-linked/store-conditional** (MIPS, Alpha, PowerPC, ARM) (p.223-224). **Fetch-and-add** and **ticket lock** (guaranteed progress) (OSTEP p.224-226). Dekker/Peterson with only loads/stores do not work on modern hardware (OSTEP p.219).
- **[from source]** Spinning too much: N−1 time slices wasted (OSTEP p.225-226); **yield** reduces it but costs a switch and does not solve starvation (OSTEP p.226-227); **queues with park/unpark** (Solaris) and the **wakeup/waiting race** problem (setpark) (OSTEP p.227-230); **priority inversion** (Mars) and **priority inheritance** (p.229).
- **[from source]** Linux **futex** (`futex_wait`, `futex_wake`); the nptl mutex uses an integer (bit 31 = held; other bits = waiters) with a fast path (OSTEP p.230-232). **Two-phase lock**: spins a little and then sleeps (OSTEP p.232).
- **[extrapolation]** MCS/CLH locks, RCU, seqlocks, adaptive mutexes are not in the book (searching for "seqlock" and "memory barrier" returns nothing).

## 4. Concurrent structures (ch.29)

- **[from source]** Basic recipe: one lock per structure (like a monitor); counter: 1 million updates take ~0.03 s with 1 thread but >5 s with 2 (OSTEP p.316). **Approximate counter**: per-CPU local counters + global with threshold S; global lags by up to (number of CPUs × S); S=1024 in the graph (OSTEP p.317-320).
- **[from source]** List: moving `malloc` outside the lock and using a single exit reduces bugs in error paths (about 40% of kernel bugs are in rare paths) (OSTEP p.321-323); **hand-over-hand locking** almost never beats the single lock (OSTEP p.323-324).
- **[from source]** **Michael & Scott** queue with two locks and a dummy node (OSTEP p.324-325). Hash table with **one lock per bucket** scales "magnificently" (OSTEP p.326-327).
- **[from source]** Lessons: more concurrency is not necessarily faster; avoid premature optimization (Knuth); the Linux **big kernel lock** example (OSTEP p.321, p.327-328).

## 5. Pitfalls

- Using `if` instead of `while` when waiting on a condition (p.140, p.423).
- Holding a lock during slow I/O unnecessarily [inference; the book only shows the cost of contention].
- Relying on `volatile` as synchronization: **the book uses `volatile` in the examples and does not claim it suffices**; the solution is a lock/atomic (p.58, p.215-224).
