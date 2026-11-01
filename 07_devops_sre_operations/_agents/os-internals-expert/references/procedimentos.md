# Procedures (routines P1 to P10)

Each routine says what to do, which reference to open, which script to run and where the book supports it. Labels: [from source], [inference], [extrapolation].

## P1. Compute turnaround and response for a scheduling policy
1. List the jobs `NAME:ARRIVAL:LENGTH`. 2. Choose a policy (FIFO, SJF, STCF, RR with quantum). 3. Run `python -I scripts/sched_sim.py run --policy P --jobs "..."`. 4. Interpret: turnaround = completion − arrival (OSTEP p.291), response = firstrun − arrival (p.295). 5. Compare with the book's examples (p.292-297) and say that tie-breaks are [inference].
Reference: `02-escalonamento-de-cpu.md`.

## P2. Choose between FIFO/SJF/STCF/RR/MLFQ
- Only turnaround and known times → STCF (p.295). Interactivity → RR (p.296-297) or MLFQ without knowing the duration (p.380). Needs share → lottery/stride/CFS (p.465-476). Each answer cites the metric sacrificed (trade-off, p.297-298).

## P3. Simulate MLFQ and diagnose starvation/gaming
1. `sched_sim.py mlfq --jobs ... --queues N --quantum Q [--boost S] [--old-rules]`. 2. Without boost, a long job may starve (p.384-385); with `--old-rules` a job that gives up the CPU before the allotment keeps its priority (gaming, p.384-385). 3. Final rules: p.389. 4. Values for S/queues: no recipe in the book (p.386-387).

## P4. Translate a virtual address
1. Identify the scheme: base/bounds (p.202-205), segments (p.305-308), linear paging (p.481-487), 2 levels (p.602-607).
2. Run `vm_sim.py base-bounds|segments|linear|multilevel`. 3. Check faults: bounds, segmentation violation, invalid PTE (SEGMENTATION_FAULT, p.487), protection (PROTECTION_FAULT).
References: `03-...` and `04-...`.

## P5. Estimate TLB and table cost
1. `vm_sim.py sizes` for the linear table size (p.483-484) and the need for levels (p.606). 2. `vm_sim.py tlb` for the hit rate (p.544: 70%). 3. Remember: a miss in a 2-level table = two extra accesses (p.602, p.607); TLB coverage (p.553).

## P6. Choose and evaluate a page replacement policy
1. `vm_sim.py replace --policy ALL --frames N --refs ...`. 2. Compare with OPT (p.691-693). 3. Check anomalies: FIFO (Belady, p.694), looping-sequential (LRU/FIFO 0%, p.699). 4. AMAT with `vm_sim.py amat` (p.691). 5. CLOCK/use bit: p.701-702; the initial use bit is [inference].

## P7. Diagnose a concurrency bug
1. Classify: atomicity violation, order violation (97% of non-deadlock, p.561) or deadlock (4 conditions, p.563). 2. Atomicity → lock; order → CV + state variable; deadlock → lock order/address/trylock (p.563-566). 3. In a CV: `while`, lock when signaling, shared state (p.414, p.419). 4. Measure before optimizing (p.328).
References: `06-...` and `07-...`.

## P8. Estimate disk I/O time and compare RAID
1. `storage_calc.py disk --seek-ms --rpm --size-kb --mbps` (p.150-152). 2. `storage_calc.py raid --n --b --s --r` (p.249). 3. Conclude with the book's recommendations (p.250); disk values are [DATED].

## P9. Count I/Os of file operations and analyze crash consistency
1. `storage_calc.py io-count --op open|read|write-alloc|create` (p.439-442). 2. For a power failure: list the 3 writes (inode, bitmap, data) and the 6 scenarios (p.575-576). 3. Compare fsck (p.577-579), data journaling (p.580-585), ordered/metadata (p.585-587). 4. Block reuse → revoke (p.587-588).

## P10. Explain NFS/AFS or choose between them
1. Stateless + idempotency + retry (NFS, p.797-804). 2. Consistency: flush-on-close and attribute cache (p.805-806) vs callbacks and whole-file caching (p.819-823). 3. Workloads: re-reading a large file favors AFS; a small part of a large file favors NFS (p.824-826). 4. Gaps: Paxos/Raft/CAP are not in the book (mark [extrapolation]).

## P11 (cross-cutting). Boundary questions
- If the question is "how do I configure X on Linux" → refer to `linux-shell-administration-expert`. If it involves containers → containers agent. What the book does not cover: `references/12-seguranca-labs-e-lacunas-do-acervo.md`.
