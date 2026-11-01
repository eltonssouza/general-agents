# 07. Condition variables, semaphores, concurrency bugs, events and monitors (ch. 30-34, appendices C-D)

PDF: ch.30 = p.410-428; ch.31 = p.494-513; ch.32 = p.557-572; ch.33 = p.611-622; ch.34 (dialogue) = p.651-652; appendix C = p.722; appendix D (monitors, marked "Deprecated") = p.744-756.

## 1. Condition variables (ch.30)

- **[from source]** Waiting for a condition by spinning (`while (done == 0);`) wastes CPU; a **condition variable** is an explicit queue with `wait()` and `signal()` (idea from Dijkstra/Hoare) (OSTEP p.410-411). `wait` requires the mutex to be locked, releases it and sleeps atomically, and reacquires it on return (p.412).
- **[from source]** Correct join: state variable `done` + mutex + cond (`thr_exit`: lock, done=1, signal, unlock; `thr_join`: lock, `while (done==0) wait`, unlock). Without a state variable, the signal may be lost; without the lock there is a race between checking and sleeping (OSTEP p.412-414). Hold the lock when signaling and when waiting (p.414).
- **[from source]** **Producer/consumer (bounded buffer)** (Dijkstra): with one cv and `if`, two consumers make the assertion fail; cause: signal is only a hint (**Mesa semantics**; almost every system) as opposed to **Hoare semantics** (OSTEP p.415-419). Switching to `while` is not enough: with a single cv a consumer may wake another consumer and all sleep (p.419-421). Solution: **two cvs** (`empty` and `fill`) and a buffer of MAX entries (p.421-423). A shell pipe is the everyday example (p.415).
- **[from source]** **Covering condition** (Lampson & Redell): `pthread_cond_broadcast` when you do not know whom to wake (memory allocator); if it only works with broadcast where it should not need it, there is a bug (OSTEP p.423-425).

## 2. Semaphores (ch.31)

- **[from source]** Semaphore = integer with `sem_wait` (decrements; waits if negative) and `sem_post` (increments; wakes one thread); negative = number of waiters; `sem_init(&s, 0, value)` (OSTEP p.494-495).
- **[from source]** Lock = binary semaphore initialized to 1; ordering (parent waits for child) = initialized to 0; rule: initial value = number of resources you are willing to hand out right after initialization (OSTEP p.496-500).
- **[from source]** Producer/consumer with `empty` (MAX) and `full` (0); with MAX>1 there is a race in `put`; putting the mutex around everything causes **deadlock**; fix: mutex only around the critical section (OSTEP p.500-504).
- **[from source]** **Reader-writer lock** (readers can starve writers; rwlocks may not pay off) (OSTEP p.504-506). **Philosophers**: always picking left→right causes deadlock; break the dependency with philosopher 4 (OSTEP p.506-508). **Thread throttling** with a semaphore (admission control) (p.509). "Zemaphore" with lock+cv; building a CV from a semaphore is hard (p.509-510).

## 3. Concurrency bugs (ch.32)

- **[from source]** Study by Lu et al.: MySQL, Apache, Mozilla, OpenOffice; **105 bugs**: 74 non-deadlock and 31 deadlock (OSTEP p.557-558). **97%** of the non-deadlock bugs are **atomicity violation** or **order violation** (OSTEP p.561). Fixes: lock around (atomicity) and cv + state (order) (OSTEP p.558-561).
- **[from source]** **Deadlock**: four conditions (**mutual exclusion, hold-and-wait, no preemption, circular wait**) (OSTEP p.563). Prevention: **order locks** (total/partial; by lock address), acquire everything at once, `trylock` with backoff (beware of **livelock**), **lock-free/wait-free** structures with compare-and-swap (OSTEP p.563-568). **Avoidance by scheduling** (Banker's) only in restricted environments (p.568-569); **detect and recover** (databases) (p.569-570).
- **[from source]** Best practice: care and acquisition order; MapReduce as a lock-free model (OSTEP p.570).

## 4. Event-based concurrency (ch.33)

- **[from source]** **Event loop** (`getEvents` + handler); `select()`/`poll()`; no locks on a single CPU; **never block**; **asynchronous I/O** (`aio_read`, `aio_error`) and signals; **manual stack management**/**continuation**; multi-CPU reintroduces locks, page faults block implicitly, disk and network AIO do not integrate well (OSTEP p.611-620).
- **[DATED/extrapolation]** `epoll`, `kqueue`, `io_uring` do not appear in the book (text search: absent).

## 5. Monitors (appendix D, "Deprecated")

- **[from source]** Monitor = implicit lock in the methods (Brinch Hansen, Hoare); Java uses `synchronized`; Hoare semantics (signal transfers the monitor) × Mesa (hint); original Java only had one implicit cv (broadcast → **thundering herd**) and later gained the `Condition` class (OSTEP p.744-755). Read as a sample (p.749-756).

## 6. Decision rules

1. Only needs mutual exclusion → lock. Needs to wait for a condition → CV with state variable and `while`.
2. More than one kind of wait (producers × consumers) → one cv per condition.
3. Cyclic lock dependency → global order (address) or `trylock`.
4. Before optimizing: one big lock, then measure (Knuth, p.328).
