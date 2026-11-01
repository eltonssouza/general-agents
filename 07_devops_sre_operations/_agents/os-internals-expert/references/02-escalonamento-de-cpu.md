# 02. CPU scheduling (ch. 7, 8, 9, 10, 11)

PDF: ch.7 = p.290-302; ch.8 (MLFQ) = p.380-391; ch.9 (proportional share) = p.465-478; ch.10 (multiprocessor) = p.528-540; ch.11 (dialogue) = p.594-595.
Scripts: `python -I scripts/sched_sim.py run|mlfq|stride|cfs-slice|cfs-run ...` (see `scripts/` and `tests/`).

## 1. Workload assumptions and metrics (ch.7)

- **[from source]** Five initial assumptions about the workload: all jobs have the same duration; they arrive together; they run to completion; they only use the CPU; the duration is known. They are relaxed throughout the chapter (OSTEP p.291).
- **[from source]** **Turnaround** = T_completion − T_arrival (Eq.7.1) (OSTEP p.291). **Response time** = T_firstrun − T_arrival (Eq.7.2) (OSTEP p.295). **Fairness** (e.g., Jain's Fairness Index) often conflicts with performance (OSTEP p.291).
- **[inference]** "Waiting" (waiting time) = turnaround − duration only holds for jobs without I/O; the book formalizes only turnaround and response and mentions "total wait time" as a simulator output (p.302).

## 2. Policies (with the book's numbers)

| Policy | Rule | Example and book result |
|---|---|---|
| **FIFO/FCFS** | arrival order | A,B,C of 10 s: completion 10,20,30, average turnaround 20 (p.292); A=100, B=C=10: (100+110+120)/3 = 110 (**convoy effect**) (p.292-293) |
| **SJF** (non-preemptive) | shortest job first | same case: (10+20+120)/3 = 50 (p.293); optimal if all arrive together (p.294); with B,C arriving at t=10: (100+(110−10)+(120−10))/3 = 103.33 (p.294) |
| **STCF/PSJF** (preemptive) | on each arrival, run the one with the least remaining time | (120−0 + 20−10 + 30−10)/3 = 50 (p.295); provably optimal under the new assumptions (p.295) |
| **Round Robin** | time slice (quantum) and alternate; slice is a multiple of the timer period (p.296) | 3 jobs of 5 s, slice 1: average response (0+1+2)/3 = 1 versus SJF (0+5+10)/3 = 5 (p.297); turnaround: 13,14,15 (average 14) (p.297) |

- **[from source]** Response time of the STCF example (Fig.7.5): A=0, B=0, C=10, average 3.33 (OSTEP p.296).
- **[from source]** SJF/STCF optimize turnaround and are bad for response; RR optimizes response and is "nearly pessimal" in turnaround, worse than FIFO in many cases; any policy that is fair on a short scale suffers in turnaround (inherent trade-off) (OSTEP p.297-298).
- **[from source]** The cost of a context switch includes caches, TLBs and branch predictors; **amortization**: 10 ms slice with 1 ms switch = ~10% waste; 100 ms slice = <1% (OSTEP p.297).
- **[from source]** I/O: treat each CPU burst as a job; this allows **overlap** (OSTEP p.298-299). Without an oracle: the OS normally does not know the duration (p.299), which motivates MLFQ.

## 3. MLFQ (ch.8)

- **[from source]** Problem: without prior knowledge of duration, minimize response for interactive jobs and turnaround. MLFQ comes from Corbató et al. 1962 (CTSS) (OSTEP p.380).
- **[from source]** Final rules (OSTEP p.389): (1) higher priority runs; (2) equal priorities: RR with the queue's quantum; (3) a new job enters the highest queue; (4) when the level's **allotment** is used up (summing all the times it gave up the CPU), it moves down one queue; (5) every period S, move all jobs to the highest queue (**priority boost**).
- **[from source]** Intermediate versions (OSTEP p.382, 385-387): rules 4a/4b (if it uses up the allotment it moves down; if it gives up the CPU early, it stays and the allotment restarts) allow **gaming** (issuing I/O just before the end; using ~99% of the allotment) (p.384-385); **starvation** of long jobs (p.384); boost solves starvation and the CPU→interactive phase change (p.385); S is a "voo-doo constant" (Ousterhout) (p.386).
- **[from source]** Parameterization: high queues with short slices (≤10 ms), low ones with long slices (hundreds of ms); Solaris TS: tables, 60 queues, 20 ms to hundreds of ms, boost ~1 s [DATED]; FreeBSD 4.3: formula with usage decay; `nice` as advice (OSTEP p.387-389).
- **[from source]** Examples: a long job moves down Q2→Q1→Q0 with a 10 ms slice (p.383); short job B (20 ms) arrives at T=100 and finishes in two slices, approximating SJF (p.383).
- **[extrapolation]** As for a "good" value of S or number of queues: the book says there is no easy answer (p.387); any concrete value is an engineering decision.

## 4. Proportional share (ch.9)

- **[from source]** **Lottery**: tickets represent the share; A=75, B=25 tickets; draw at each slice; probabilistic (B runs 4 of 20 slices in one example); ticket currency, transfer, inflation; list with counter (A=100,B=50,C=250; winner 300 → C) (OSTEP p.465-469). Fairness study F = (1st completion)/(2nd completion): low for short jobs (p.469).
- **[from source]** **Stride**: stride = (large number)/tickets; 10,000 → A=100, B=200, C=40; runs the lowest "pass" and adds the stride; cycle A B C C C A C C (C 5×, A 2×, B 1×); drawback: global state (what pass to give a new job?) (OSTEP p.470-471).
- **[from source]** **CFS (Linux)**: vruntime; typical **sched_latency** 48 ms divided by n processes; typical **min_granularity** 6 ms (n=10 → 4.8 becomes 6 ms); nice from −20 to +19 mapped by a weight table (nice 0 = 1024; −5 = 3121); Eq.9.1: time_slice_k = weight_k/Σweight × sched_latency; Eq.9.2: vruntime_i += (1024/weight_i) × runtime_i; red-black tree (O(log n)); on wakeup, vruntime = minimum in the tree (OSTEP p.471-476).
- **[from source]** Fair-share limits: does not fit well with I/O; the problem of assigning tickets/nice; good in VMs/cloud (OSTEP p.476).

## 5. Multiprocessor (ch.10)

- **[from source]** Cache coherence and **bus snooping**; locks are still needed; **cache affinity** (OSTEP p.529-532).
- **[from source]** **SQMS** (single queue): simple, but does not scale (locks) and loses affinity; **MQMS** (queue per CPU): scales and preserves affinity, but suffers **load imbalance**; solution: continuous **migration** and **work stealing** (OSTEP p.533-537).
- **[from source]** Linux has had three schedulers (O(1), CFS, BFS); O(1) and CFS multi-queue, BFS single queue (OSTEP p.537). **[DATED]** The book does not describe the later evolution of the Linux scheduler.

## 6. Using the script

- `sched_sim.py run --policy STCF --jobs "A:0:100,B:10:10,C:10:10"` reproduces average turnaround 50 and response 3.33 (p.295-296).
- `sched_sim.py mlfq ... --old-rules` demonstrates the gaming of rules 4a/4b; without the flag, it uses the final rules. Conventions not specified by the book (tie-breaks, where the job returning from I/O enters) are declared in the script header [inference].
