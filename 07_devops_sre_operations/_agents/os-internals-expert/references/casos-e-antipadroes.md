# Solved cases and anti-patterns

Format: situation → answer → where the book supports it. Labels: [from source], [inference], [extrapolation].

## Scheduling
1. **"My short job waits 100 s behind a long one."** → FIFO convoy effect; SJF/STCF solve it if the duration is known (A=100, B=C=10: 110 → 50) [from source] (OSTEP p.292-293).
2. **"RR with quantum 1 is fair, so is it the best?"** → improves response (average 1 versus 5), but worsens turnaround (13, 14, 15; average 14) [from source] (OSTEP p.297).
3. **"MLFQ: a job that always issues I/O before the allotment runs out dominates the CPU."** → this is the gaming of rules 4a/4b; the final rule 4 counts the total allotment [from source] (OSTEP p.384-387).
4. **"CFS: how much CPU for nice −5 versus 0?"** → weights 3121 and 1024: ~3/4 and ~1/4 of sched_latency (36 ms and 12 ms); A's vruntime advances at 1/3 the rate of B's [from source] (OSTEP p.473-474).
5. **"Fairness and turnaround together?"** → inherent trade-off [from source] (OSTEP p.297-298).

## Memory
6. **"Why does my program print the same address in two processes?"** → program addresses are virtual; each process has its own address space [from source] (OSTEP p.49, 276). (The book's example disables ASLR, p.276.)
7. **"Does the translation of 4400 with a 4 KB bounds fail?"** → yes: VA ≥ bounds raises an exception [from source] (OSTEP p.204-205).
8. **"Heap segment at VA 4200: PA = 34 KB + 4200?"** → no; subtract the segment start (4096): offset 104 → 34920 [from source] (OSTEP p.306).
9. **"Paging made the system slow."** → one extra reference per memory access; the TLB solves the common case (hit); misses cost [from source] (OSTEP p.487, 541-543).
10. **"70% hit rate in a loop over an array of 10 ints?"** → miss, hit, hit, miss, hit, hit, hit, miss, hit, hit with 16 B pages [from source] (OSTEP p.543-545).
11. **"A 4 MB linear table per process is unviable."** → multi-level reduces space at the cost of 2 extra accesses on a miss [from source] (OSTEP p.600-602).
12. **"I increased memory and FIFO got worse."** → Belady's Anomaly (sequence 1,2,3,4,1,2,5,1,2,3,4,5) [from source] (OSTEP p.694).
13. **"Loop over 50 pages with a cache of 49."** → LRU and FIFO 0% hit; Random has a non-zero hit rate [from source] (OSTEP p.699).
14. **"The system only does paging and gets slow (thrashing)."** → admission control or OOM killer [from source] (OSTEP p.703).

## Concurrency
15. **"A counter with two threads gives 19345221."** → race condition in load/add/store [from source] (OSTEP p.58-61).
16. **"I used `if (count==0) wait`."** → with Mesa semantics, use `while`; with one cv and several consumers it still fails; use two cvs [from source] (OSTEP p.417-423).
17. **"A mutex around everything in producer/consumer with semaphores hung."** → deadlock; reduce the scope of the lock [from source] (OSTEP p.502-504).
18. **"Two locks in opposite order."** → deadlock; order them (lock address) or use trylock with care for livelock [from source] (OSTEP p.561-566).
19. **"I used a spinning flag to synchronize threads."** → don't; use a CV [from source] (OSTEP p.140-141).
20. **"Need more concurrency in the list: hand-over-hand?"** → rarely beats the single lock; measure [from source] (OSTEP p.323-324).

## Persistence and distributed
21. **"A random 4 KB disk access takes ~6 ms: how much bandwidth?"** → ~0.66 MB/s (Cheetah) [from source, DATED] (OSTEP p.151-152).
22. **"RAID-5 for a database with many small writes?"** → each write = 4 I/Os; throughput N/4 · R; mirroring is better for random I/O [from source] (OSTEP p.248-250).
23. **"Does opening a file read bitmaps?"** → no; only an allocating write consults bitmaps [from source] (OSTEP p.440).
24. **"Power failed after writing only the bitmap."** → space leak; ordered journaling writes the data before the metadata commit [from source] (OSTEP p.576, 586).
25. **"Does fsync solve everything?"** → sometimes the directory also needs `fsync` [from source] (OSTEP p.342).
26. **"NFS: I restarted the server and the clients carried on."** → stateless protocol + idempotent operations + retry [from source] (OSTEP p.797-804).
27. **"Two clients edit the same file in AFS."** → the last to close wins; in NFS blocks could get mixed [from source] (OSTEP p.822-823).
28. **"SSD: overwriting a page."** → requires erasing the block; log-structured FTL, GC and write amplification [from source] (OSTEP p.655-663).

## Answer anti-patterns (of the agent itself)
- Attributing "Docker/cgroups/epoll/Raft/CAP" to the book (absent): mark [extrapolation] or say "the collection does not cover it".
- Giving a number without the page or without running the script when there is a calculation.
- Citing the chapter's printed page as if it were the PDF's: always use the PDF page and the INDEX map.
- Claiming the book "recommends" MLFQ/CFS values beyond those cited (p.386-388, 472-473): they are examples and defaults of the time.
