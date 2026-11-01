# 05. Swapping, replacement policies, VAX/VMS, Linux VM and VMM (ch. 21, 22, 23, 24, appendix B)

PDF: ch.21 = p.640-650; ch.22 = p.690-707; ch.23 = p.723-741; ch.24 (dialogue) = p.757-759; appendix B (VMM) = p.677-689 (dialogue A = p.639).
Script: `python -I scripts/vm_sim.py replace|amat ...`.

## 1. Swap mechanisms (ch.21)

- **[from source]** To support large spaces a bigger, slower level is added (disk/SSD); old alternative: manual **memory overlays** (OSTEP p.640). **Swap space** = reserved disk area; pages are moved in page-sized units; its size limits the pages in use (OSTEP p.641-642). Binaries also serve as a source of code pages (p.641-642).
- **[from source]** **Present bit** in the PTE; accessing a non-present page = **page fault**, handled in software by the OS (almost all systems, even with a hardware TLB) because disk is slow and the hardware does not understand swap (OSTEP p.642-644). The "fault" is misleading: the access is legal (p.643).
- **[from source]** Service: the disk address is kept in the PTE bits; the process blocks during the I/O; at the end the OS marks present, updates the PFN and retries the instruction (OSTEP p.643-644). If memory is full, the **page-replacement policy** chooses the victim; a wrong choice costs 10,000 to 100,000 times (p.644-645).
- **[from source]** Complete flow: Fig.21.2 (hardware: TLB hit; miss with invalid PTE → SEGMENTATION_FAULT; protection → PROTECTION_FAULT; present → TLB_Insert; !present → PAGE_FAULT) and Fig.21.3 (software: FindFreePhysicalPage, EvictPage, DiskRead, update PTE, retry) (OSTEP p.645-646).
- **[from source]** **High/low watermark** and **swap/page daemon** in the background free pages up to HW when fewer than LW remain; allows clustering writes to swap (OSTEP p.646-647).

## 2. Replacement policies (ch.22)

- **[from source]** **AMAT = T_M + P_miss × T_D** (Eq.22.1); with T_M = 100 ns, T_D = 10 ms and 90% hit: ≈ 1 ms (1.0001 ms); with 99.9%: 10.1 µs (OSTEP p.690-691).
- **[from source]** **Optimal (Belady)**: evicts the page used furthest in the future; unrealistic, serves as a comparison (OSTEP p.691-692). The book's reference stream: **0,1,2,0,1,3,0,3,1,2,1**, cache of 3: **OPT = 6 hits and 5 misses = 54.5% (85.7% excluding compulsory misses)**; **FIFO = 36.4% (57.1%)**; **LRU = OPT** in this example (OSTEP p.692-697). Three C's: compulsory, capacity, conflict (conflict does not occur in the OS page cache) (p.693).
- **[from source]** **Belady's Anomaly**: with the sequence 1,2,3,4,1,2,5,1,2,3,4,5 FIFO gets worse going from 3 to 4 pages; LRU has the **stack property** (OSTEP p.694).
- **[from source]** **Random**: over 10,000 trials, only slightly more than 40% of the time does it match the optimal (6 hits) (OSTEP p.695).
- **[from source]** Workloads (cache 1..100): **no-locality** (LRU = FIFO = Random); **80-20** (LRU better); **looping-sequential** over 50 pages is the worst case for LRU/FIFO (0% hit even with a cache of 49); Random has a non-zero hit rate (OSTEP p.697-699).
- **[from source]** Perfect LRU costs bookkeeping on every reference; with 4 GB and 4 KB pages that is 1 million pages (OSTEP p.700-701). **Approximation**: **use bit (reference bit)** set by the hardware and cleared only by the OS; **clock algorithm** (circular list + clock hand: if use=1 clear it and advance; if 0 it is the victim) (OSTEP p.701-702). Consider **dirty**: prefer evicting clean pages (OSTEP p.702).
- **[from source]** Other policies: **demand paging** vs **prefetching**; **clustering** of writes; **thrashing**: **admission control** or **out-of-memory killer** (OSTEP p.703); **scan resistance** (e.g., ARC) (p.704).
- **[inference]** The initial value of the use bit when a page is loaded in CLOCK is not specified; the script offers `--initial-use`.

## 3. Complete systems (ch.23)

- **[from source]** **VAX/VMS**: 512-byte pages; 23-bit VPN; 2 bits choose the segment (P0, P1, S); user page tables in kernel virtual memory (can be swapped); page 0 invalid (detects null pointer); kernel mapped into every address space; PTE without reference bit (OSTEP p.724-727).
- **[from source]** Replacement in VMS: reference bit emulated with protection bits; **segmented FIFO** with **resident set size (RSS)** and second-chance lists (clean and dirty); **clustering**; **demand zeroing** and **copy-on-write** (OSTEP p.727-730). TIP be lazy (p.730).
- **[from source]** **Linux VM** (x86): user/kernel split at 0xC0000000 (32 bits); **kernel logical** (kmalloc, direct mapping, contiguous, no swap) versus **kernel virtual** (vmalloc); x86-64 uses **4 levels** and only 48 bits; **huge pages** of 2 MB and 1 GB (TLB; cost: internal fragmentation, bad swapping); **transparent huge pages**; unified **page cache** with **2Q** (inactive/active lists); **mmap**; **NX bit**, ROP, **ASLR**/KASLR; **Meltdown/Spectre** and **KPTI** (August 2018) (OSTEP p.730-739). **[DATED]** The chapter reflects Linux/x86 of the time.
- **[extrapolation]** cgroups, NUMA balancing, container memory do not appear in the book (text search: "cgroup" and "container" absent).

## 4. VMM / hypervisor (appendix B)

- **[from source]** The VMM (hypervisor) extends LDE: the guest OS cannot execute privileged instructions; the VMM registers the OS's trap handlers and forwards traps with reduced privilege; the OS runs in supervisor mode (MIPS) or in user mode with page-table protection (OSTEP p.677-682).
- **[from source]** Memory: three levels of address (virtual → "physical" of the OS → **machine** of the VMM); on a TLB miss the VMM installs VPN→MFN; with a hardware TLB it uses a **shadow page table**; Disco uses a **software TLB**; **para-virtualization**; **information gap** (idle loop; pages zeroed twice) (OSTEP p.682-687). Modern Intel/AMD hardware reduces software techniques **[DATED]** (p.688).
- **[from source]** Does not cover containers; does not cover virtualized I/O (OSTEP p.687-688).

## 5. Decision roadmap (fault vs policy)

1. Page access: TLB → PTE → present? (ch.21).
2. If not present: find a free frame → otherwise **EvictPage** (policy: LRU/CLOCK/…; dirty requires a write).
3. Measure with AMAT: a disk miss dominates; "buy more memory" was the historical solution (OSTEP p.704).
