# Reference index: os-internals-expert

Reference collection of the **os-internals-expert** agent. Open only the file that the topic requires.

## 1. Source and abbreviations

| Abbreviation | Work | Note |
|---|---|---|
| **OSTEP** | *Operating Systems: Three Easy Pieces*, Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau (Arpaci-Dusseau Books, ostep.org), 834-page PDF (extracted text of ~1.94 million characters); the footer pages show "VERSION 1.10" and some sections "VERSION 1.20" / © 2008-26; the security chapters (53-57) are by Peter Reiher (UCLA). | Single source of the collection. |

## 2. Page convention (IMPORTANT)

- **`p.N` = PDF page number** (the `=== PAGE N ===` marker of the extracted text). It is the only convention used throughout the package.
- The PDF is a **set of independent chapters**, each with its own printed numbering (1, 2, 3...), and the order of the chapters in the PDF **does not follow the book's order**. That is why the map below is mandatory.
- Printed page within the chapter = PDF page − chapter start page + 1 (e.g., p.183 of the PDF = page 2 of ch.6).
- For chapter numbers use the book's numbering (ch.7 = Scheduling: Introduction etc.).

## 3. Chapter → PDF pages map

| Ch. | Title | PDF pages |
|---|---|---|
| 1 | A Dialogue on the Book | 180-181 |
| 2 | Introduction to Operating Systems | 271-289 |
| 3 | A Dialogue on Virtualization | 4-5 |
| 4 | The Abstraction: The Process | 30-42 |
| 5 | Interlude: Process API | 106-120 |
| 6 | Mechanism: Limited Direct Execution | 182-197 |
| 7 | Scheduling: Introduction | 290-302 |
| 8 | Scheduling: The Multi-Level Feedback Queue | 380-391 |
| 9 | Scheduling: Proportional Share | 465-478 |
| 10 | Multiprocessor Scheduling (Advanced) | 528-540 |
| 11 | Summary Dialogue on CPU Virtualization | 594-595 |
| 12 | A Dialogue on Memory Virtualization | 6-7 |
| 13 | The Abstraction: Address Spaces | 43-51 |
| 14 | Interlude: Memory API | 121-132 |
| 15 | Mechanism: Address Translation | 198-212 |
| 16 | Segmentation | 303-314 |
| 17 | Free-Space Management | 392-409 |
| 18 | Paging: Introduction | 479-493 |
| 19 | Paging: Faster Translations (TLBs) | 541-556 |
| 20 | Paging: Smaller Tables | 596-610 |
| 21 | Beyond Physical Memory: Mechanisms | 640-650 |
| 22 | Beyond Physical Memory: Policies | 690-707 |
| 23 | Complete Virtual Memory Systems | 723-741 |
| 24 | Summary Dialogue on Memory Virtualization | 757-759 |
| 25 | A Dialogue on Concurrency | 10-11 |
| 26 | Concurrency: An Introduction | 52-67 |
| 27 | Interlude: Thread API | 133-144 |
| 28 | Locks | 213-234 |
| 29 | Lock-based Concurrent Data Structures | 315-330 |
| 30 | Condition Variables | 410-428 |
| 31 | Semaphores | 494-513 |
| 32 | Common Concurrency Problems | 557-572 |
| 33 | Event-based Concurrency (Advanced) | 611-622 |
| 34 | Summary Dialogue on Concurrency | 651-652 |
| 35 | A Dialogue on Persistence | 14-15 |
| 36 | I/O Devices | 68-81 |
| 37 | Hard Disk Drives | 145-160 |
| 38 | Redundant Arrays of Inexpensive Disks | 235-252 |
| 39 | Interlude: Files and Directories | 331-359 |
| 40 | File System Implementation | 429-446 |
| 41 | Locality and The Fast File System | 514-527 |
| 42 | Crash Consistency: FSCK and Journaling | 573-593 |
| 43 | Log-structured File Systems | 623-638 |
| 44 | Flash-based SSDs | 653-676 |
| 45 | Data Integrity and Protection | 708-721 |
| 46 | Summary Dialogue on Persistence | 742-743 |
| 47 | A Dialogue on Distribution | 760-761 |
| 48 | Distributed Systems | 764-780 |
| 49 | Sun’s Network File System (NFS) | 794-811 |
| 50 | The Andrew File System (AFS) | 816-829 |
| 51 | Summary Dialogue on Distribution | 833-834 |
| 52 | A Dialogue on Security | 16-17 |
| 53 | Introduction to Operating System Security | 82-94 |
| 54 | Authentication | 161-179 |
| 55 | Access Control | 253-270 |
| 56 | Protecting Information With Cryptography | 360-379 |
| 57 | Distributed System Security | 447-464 |
Appendices: A VMM dialogue = 639; B Virtual Machine Monitors = 677-689; C Monitors dialogue = 722; D Monitors (Deprecated) = 744-756; E Labs dialogue = 762-763; F Tutorial = 781-793; G Systems Projects = 812-815; H xv6 Projects = 830-832. Preface/educators/students = 18-29; table of contents = 95-105 (roman pages xvi-xxvi).

## 4. Citation and label conventions

- `[from source] (OSTEP p.N)` or `(OSTEP p.N-M)`.
- `[inference]`: direct deduction from what the book says (includes tie-break conventions in the scripts).
- `[extrapolation]`: general OS knowledge outside the book; no page. Always recommend checking current documentation.
- `[DATED]`: values/versions/hardware from the time of the book (Cheetah/Barracuda disks, prices, TLS 1.3 in 2020, Linux 2.x/x86, Meltdown/Spectre in 2018, SSDs of the time).

## 5. Thematic map (one file per group of chapters)

| File | When to open | Chapters / pages |
|---|---|---|
| [01-processos-api-e-limited-direct-execution.md](01-processos-api-e-limited-direct-execution.md) | process, states, fork/exec/wait, redirection, trap, syscall, timer, context switch | 2, 4, 5, 6 / p.30-42, 106-120, 182-197, 271-289 |
| [02-escalonamento-de-cpu.md](02-escalonamento-de-cpu.md) | FIFO/SJF/STCF/RR, MLFQ, lottery/stride/CFS, multiprocessor | 7-11 / p.290-302, 380-391, 465-478, 528-540, 594-595 |
| [03-address-space-traducao-segmentacao-e-free-space.md](03-address-space-traducao-segmentacao-e-free-space.md) | address space, base/bounds, segments, malloc/free, free list | 13-17 / p.43-51, 121-132, 198-212, 303-314, 392-409 |
| [04-paginacao-tlb-e-tabelas-de-paginas.md](04-paginacao-tlb-e-tabelas-de-paginas.md) | paging, PTE, TLB, ASID, multi-level/inverted tables | 18-20 / p.479-493, 541-556, 596-610 |
| [05-swapping-politicas-de-substituicao-e-vm-completo.md](05-swapping-politicas-de-substituicao-e-vm-completo.md) | swap, page fault, OPT/FIFO/LRU/CLOCK, VAX/VMS, Linux VM, VMM | 21-24, appendix B / p.640-650, 690-707, 723-741, 757-759, 677-689 |
| [06-concorrencia-threads-locks-e-estruturas.md](06-concorrencia-threads-locks-e-estruturas.md) | threads, pthread, locks, futex, counters/lists/queues/hash | 26-29 / p.52-67, 133-144, 213-234, 315-330 |
| [07-condition-variables-semaforos-bugs-e-eventos.md](07-condition-variables-semaforos-bugs-e-eventos.md) | CVs, semaphores, deadlock, bugs, event loop, monitors | 30-34, appendices C-D / p.410-428, 494-513, 557-572, 611-622, 651-652, 744-756 |
| [08-dispositivos-de-io-discos-e-raid.md](08-dispositivos-de-io-discos-e-raid.md) | polling/interrupt/DMA, HDD, disk scheduling, RAID | 36-38 / p.68-81, 145-160, 235-252 |
| [09-arquivos-diretorios-vsfs-e-ffs.md](09-arquivos-diretorios-vsfs-e-ffs.md) | file API, inodes, vsfs, I/O per operation, FFS | 39-41 / p.331-359, 429-446, 514-527 |
| [10-consistencia-journaling-lfs-ssd-e-integridade.md](10-consistencia-journaling-lfs-ssd-e-integridade.md) | crash consistency, fsck, journaling, LFS, SSD/FTL, checksums | 42-46 / p.573-593, 623-638, 653-676, 708-721, 742-743 |
| [11-sistemas-distribuidos-nfs-e-afs.md](11-sistemas-distribuidos-nfs-e-afs.md) | UDP, RPC, NFS, AFS | 47-51 / p.760-780, 794-811, 816-829, 833-834 |
| [12-seguranca-labs-e-lacunas-do-acervo.md](12-seguranca-labs-e-lacunas-do-acervo.md) | OS security, labs, what the book does NOT cover | 52-57, appendices E-H |
| [glossario.md](glossario.md) | definitions of the book's terms | whole book |
| [procedimentos.md](procedimentos.md) | procedures P1 to P10 | various |
| [casos-e-antipadroes.md](casos-e-antipadroes.md) | solved cases and pitfalls | various |

## 6. Scripts (folder `../scripts/`)

| Script | Function |
|---|---|
| `os_lookup.py` + `os_index.json` | topic and page lookup; says "NOT COVERED" when the collection does not cover it |
| `sched_sim.py` | FIFO/SJF/STCF/RR, MLFQ, stride, CFS (slice and vruntime) |
| `vm_sim.py` | base/bounds, segments, linear and multi-level translation, TLB, OPT/FIFO/LRU/CLOCK/RANDOM, AMAT, table sizes |
| `storage_calc.py` | disk time/rate, RAID, parity, amortization (FFS/LFS), inode, file size, checksums |

## 7. Summary of limits

- Does not cover: containers/cgroups/Docker/Kubernetes, systemd, epoll/io_uring, distributed consensus (Paxos/Raft), NUMA in depth, Linux io schedulers, Linux administration (refer to `linux-shell-administration-expert`).
- Figures and tables only partially extracted from the PDF (graph values, Fig.44.2 and 44.4 incomplete); the numbers used come from the running text.
- Ch.54-57 and appendices E-H were read by sampling (see `12-...`).
