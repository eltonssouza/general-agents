# Fidelity report: os-internals-expert

Source: *Operating Systems: Three Easy Pieces* (OSTEP), 834-page PDF, text extracted with PyMuPDF per page (marker `=== PAGE N ===`, ~1.94 million characters). Page convention used throughout the package: **PDF page** (the PDF is a collection of chapters with their own numbering and out of the book's order; the map is in `references/INDEX.md`).

## 1. How the work was done

- **Book map (phase 1):** chapters were located by a program from the pattern of the opening pages (chapter number + title + page-1 mark); 57 chapters/dialogues mapped and checked by verification 5 below.
- **Block reading with intermediate notes (map):** the attempt to parallelize with subagents was blocked (the environment's limit on simultaneous subagents). Reading was then done sequentially, chapter by chapter, with a page reader that removes repeated headers/footers and the reference lists; after each chapter, notes with page numbers were saved in `scratch/devops/os-internals-expert/notes/` (47 files, ~148 KB) **before** writing the references (reduce).
- **Reading coverage:** chs. 2, 4-11, 13-24, 26-34, 36-46, 48-51 and appendices A-B were read page by page (except reference lists; the "Homework" exercises were read only in summary). Appendices C and D: C only the opening and D (monitors, "Deprecated") in part (p.744-748 and 754-755 read; 749-753 and 756 only by titles). The ch.1 dialogue (p.180-181) and the ch.52 one (p.16-17) were read only partially. **Partial reading:** chs. 54-57 (authentication, access control, cryptography, distributed security) by key sections and sampling; appendices E-H (labs) by sampling; preface, "To Educators/To Students" and acknowledgments only as a sample. Ch.53 was read in full. Partial results are labeled in the references.
- **Figures:** the extracted text does not contain the values of graphs and some tables (e.g. Fig.44.2 incomplete, Fig.44.4 absent, hit-rate graphs). Only numbers present in the running text were used.
- **Simulators:** written according to the definitions and numeric examples of the pages read (turnaround/response p.291/295; MLFQ rules p.389; stride p.470-471; CFS weights p.473; translations p.205, 306-308, 481-483, 605; TLB p.544; replacement p.692-697; disk p.150-152; RAID p.239-249; amortization p.522, 627; inode p.433; checksum p.712-713).

## 2. Automatic checks (all run)

| Check | Result |
|---|---|
| `verify_citations.py` range (every `p.N` citation between 1 and 834) | 2,831 page numbers checked; 0 out of range |
| Positive content (exact terms on the cited page) | **196/196 OK** (items in `citation-checks.json`) |
| Negative content (plausible claims the book does NOT make) | **38/38 OK** (26 terms absent from the whole book by regex: cgroups, Docker, Kubernetes, epoll, io_uring, Paxos, Raft, CAP, systemd, KVM, lockdep, seqlock, memory barrier, TLB shootdown, PCID, vDSO, posix_spawn, RAID-Z, CFQ, BFQ, swappiness, readahead, containers, NUMA balancing, eBPF, SELinux; + 12 per-chapter absences, e.g. "waiting time" as a metric in ch.7, QLC/ZNS in ch.44) |
| Topic index (`os_index.json`: terms within the page range) | **95/95 OK** |
| Index gaps (`sem_cobertura`) absent from the book | **27/27 OK** |
| Chapter map (title on the starting page) | **57/57 OK** |
| `audit_numbers.py --strict` (numbers in the references on the cited pages ±1) | 357 numbers audited, 357 confirmed (9 manually reviewed exceptions in `numeros-ok.txt`: lists, pt-BR decimals and numbers spelled out in the book) |
| `run_tests.py` (scripts against the book's numeric examples) | **37/37 OK** |

## 3. Failures found during construction and fixes

1. The first version of the reader removed isolated numeric lines (losing one-column tables, e.g. p.205); fixed to remove only the page number at the top.
2. The verifier flagged 8 items of the first list of positive checks: subscripts and underscores lost in extraction (`T_completion` appears as "Tcompletion"; `pthread_join` as "pthread join"), end-of-line hyphen ("memory-mapped"), and three pages off by one (Hoare semantics is on p.419, not 418; "105 total bugs" is on p.557; "gaming the scheduler" is on p.384). All fixed and re-run.
3. The first disk calculation used 1 MB = 1024 KB and gave 0.648 MB/s on the Cheetah example; the book uses the decimal calculation (≈0.66 MB/s). The script now uses `--kb-per-mb 1000` by default (option 1024). Even so, the PDF rounds the Barracuda to 0.31 MB/s (the calculation gives 0.30); the script declares the difference.
4. Reference 08 said "RAID-6 cited"; the text only has "Level 6" (the term "RAID-6" does not appear). Fixed.
5. The case "power lost after writing only the bitmap" was labeled with the wrong scenario number; fixed to space leak (p.576).
6. Interface bug in `vm_sim.py multilevel` (page-table entry separator); fixed and tested (T15).
7. CLOCK depends on a convention the book does not specify (use bit on load): different results (36.4% × 54.5%) on the book's sequence. Documented as `[inference]` and exposed through `--initial-use`.

## 4. Dated content or content needing care

- Disk hardware and numbers (Cheetah/Barracuda), SSD tables, prices (US$0.60/GB × US$0.05/GB), file statistics (Agrawal et al.), SEER traces, Solaris TS tables, Linux 5.2 lock order, TLS 1.3 in 2020, Meltdown/Spectre in 2018, gRPC/Thrift as "modern": all marked `[DATED]`.
- The book expresses opinions (e.g. about fork, p.115); the agent says so.
- The PDF mixes passages with "VERSION 1.10" and "VERSION 1.20"/© 2008-26; it does not affect the content used, but INDEX records the fact.

## 5. Limitations and pending items

- Partial reading of chs. 54-57 and appendices E-H (see above): answers in those areas have a lower fidelity guarantee.
- Values that exist only in graphs/figures are not available (e.g. Fig.44.4).
- The tests of the 32 cases were **run by the package's own author** (scripts and verifiers did run), **not** by an independent blind model. A future blind round with new questions is recommended.
- The page checks confirm the presence of key terms on the cited page; they do not replace a critical reading of each paraphrase. The number audit reduces, but does not eliminate, the risk of an imprecise paraphrase.
- There are no separate SKILLs: the four scripts serve as deterministic skills and are declared in `.claude-plugin/plugin.json`.
