# 04. Paging, TLB and smaller page tables (ch. 18, 19, 20)

PDF: ch.18 = p.479-493; ch.19 (TLB) = p.541-556; ch.20 = p.596-610.
Script: `python -I scripts/vm_sim.py linear|multilevel|tlb|sizes ...`.

## 1. Simple paging (ch.18)

- **[from source]** Divide the address space into fixed-size **pages** and physical memory into **page frames**; no external fragmentation and no assumptions about heap/stack direction (OSTEP p.479-481). Each process has a **page table** (exception: inverted page table) (p.481).
- **[from source]** Translation: VA = **VPN** + **offset**; example of 64 bytes, 16 B pages (2-bit VPN, 4-bit offset); VA 21 = 010101 → VPN 01, offset 0101; VPN 1 → PFN 7 (111); PA = 1110101 = 117; the offset does not change (OSTEP p.481-483).
- **[from source]** Size: 32 bits and 4 KB pages → 20-bit VPN, 12-bit offset; 2^20 PTEs × 4 B = 4 MB per process (100 processes = 400 MB) (OSTEP p.483-484). The page table lives in memory, not in dedicated hardware (p.484).
- **[from source]** **Linear page table** = array indexed by VPN. PTE bits: **valid** (essential for sparse spaces), protection, **present** (in memory or on disk), **dirty**, **reference/accessed**; x86 PTE: P, R/W, U/S, PWT, PCD, PAT, G, A, D, PFN; x86 has no separate valid bit (P=0 may mean invalid or not present) (OSTEP p.484-485).
- **[from source]** Translation algorithm (Fig.18.6): `VPN = (VA & VPN_MASK) >> SHIFT`; `PTEAddr = PTBR + VPN*sizeof(PTE)`; if !Valid → SEGMENTATION_FAULT; if protection is violated → PROTECTION_FAULT; otherwise `PA = (PFN << SHIFT) | offset`; **each reference requires an extra memory reference** (OSTEP p.486-487).
- **[from source]** Memory trace (array.c, 1000 integers, 1 KB page, table in 1 KB): 10 accesses per iteration (4 fetches, 1 update and 5 table accesses) (OSTEP p.487-490).
- **[from source]** Summary: paging avoids external fragmentation and is flexible, but it is slow (extra accesses) and wastes memory on tables (OSTEP p.490).

## 2. TLB (ch.19)

- **[from source]** **TLB** = hardware cache (in the MMU) of popular translations; "make VM possible" (OSTEP p.541).
- **[from source]** Flow (Fig.19.1): extract the VPN; **hit** → check protection and form the PA; **miss** (hardware-managed) → read the PTE, if invalid SEGMENTATION_FAULT, if no permission PROTECTION_FAULT, otherwise `TLB_Insert` and **retry**; the miss costs the extra reference (OSTEP p.542-543).
- **[from source]** Example: 10 integers of 4 bytes starting at VA 100, 16 B pages (VPN 6, 7, 8): **miss, hit, hit, miss, hit, hit, hit, miss, hit, hit = 70%** thanks to **spatial locality**; a second pass would have 100% (**temporal locality**) (OSTEP p.543-545).
- **[from source]** Who handles the miss: **hardware-managed** (x86, CR3; the hardware "walks" the table) or **software-managed** (MIPS R10k, SPARC v9: TLB_MISS exception, the OS handler updates the TLB with a privileged instruction; return-from-trap resumes at the **same** instruction; the handler must not cause an infinite chain of misses: use unmapped physical memory or **wired** entries) (OSTEP p.546-548).
- **[from source]** Contents: 32/64/128 entries, **fully associative**, fields VPN, PFN, valid, protection, ASID, dirty; the TLB valid ≠ the page table valid (OSTEP p.548).
- **[from source]** Context switch: **flush** (clears valid bits; cost of misses) or **ASID** (e.g., 8 bits versus 32-bit PID); shared pages may appear in two entries with different ASIDs (OSTEP p.549-550).
- **[from source]** Replacement: LRU or random; LRU behaves badly in a loop over n+1 pages with an n-entry TLB (OSTEP p.551). Real TLB (MIPS R4000): 19-bit VPN, 24-bit PFN, G (global) bits, 8-bit ASID, C, D, V, page mask; instructions TLBP/TLBR/TLBWI/TLBWR; **wired** register (OSTEP p.551-552).
- **[from source]** **TLB coverage**: exceeding the number of covered pages causes many misses; solution: large pages (OSTEP p.553). TIP "RAM isn't always RAM" (Culler's Law) (p.552).
- **[from source]** Measurement: <=8 pages ~5 ns, >=16 ~20 ns, ~1024 ~70 ns → two-level TLB (OSTEP p.555-556) **[DATED]**.

## 3. Smaller tables (ch.20)

- **[from source]** Problem: a 4 MB linear table per process (OSTEP p.596). **Bigger pages** (16 KB → 4× smaller table) bring internal fragmentation; systems use 4 KB or 8 KB; multiple sizes mainly serve to reduce TLB pressure (OSTEP p.596-597).
- **[from source]** **Hybrid paging+segmentation** (Multics): one table per segment, base points to the table and bounds is the number of valid pages; reintroduces external fragmentation and still requires segmentation (OSTEP p.597-600).
- **[from source]** **Multi-level page table**: splits the table into page-sized units; the **page directory** (PDEs with valid + PFN) only points to table pages that have at least one valid PTE; cost: **two loads** on a TLB miss (time-space trade-off) and more complexity (OSTEP p.600-602).
- **[from source]** Example (16 KB, 64 B pages → 14-bit VA = VPN 8 + offset 6): linear = 256 entries × 4 B = 1 KB = 16 pages of 64 B; directory of 16 entries; VPNs 0,1 (code), 4,5 (heap) and 254,255 (stack); 3 pages are allocated (1 directory and 2 table) instead of 16; VA 0x3F80 → PDIndex 1111 → PT at PFN 101; PTIndex 1110 → PFN 55 (0x37) → **PA 0x0DC0** (OSTEP p.602-605). Formulas: `PDEAddr = PageDirBase + PDIndex*sizeof(PDE)`; `PTEAddr = (PDE.PFN << SHIFT) + PTIndex*sizeof(PTE)` (p.603-604).
- **[from source]** More than two levels: 30-bit VA and 512 B page → 21-bit VPN; 128 PTEs per page → 7-bit PT index; 14 bits remain for the directory, which does not fit in a page → one more level (OSTEP p.606-607); Fig.20.6 shows the complete control flow (TLB + two levels) (p.607).
- **[from source]** **Inverted page table** (one entry per physical page, with hash; PowerPC) and swapping of the page tables themselves (kernel virtual memory) (OSTEP p.608). Conclusion: page tables are just data structures; with a software-managed TLB the OS can use any of them (p.608).
- **[extrapolation]** The 4-level x86-64 is described in ch.23 (p.732-733), not here.

## 4. Calculation roadmap

1. Define VA bits and page size → VPN/offset bits (`vm_sim.py sizes`).
2. Translate with `vm_sim.py linear` (one level) or `multilevel` (two levels).
3. For miss cost: linear = 1 extra access; 2 levels = 2 extra accesses (p.602, p.607).
4. TLB hit rate: `vm_sim.py tlb --page-size ... --entries ... --va ...`.
