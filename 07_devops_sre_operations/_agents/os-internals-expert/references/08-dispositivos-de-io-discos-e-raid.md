# 08. I/O devices, hard disks and RAID (ch. 36, 37, 38)

PDF: ch.36 = p.68-81; ch.37 = p.145-160; ch.38 = p.235-252; persistence dialogue = p.14-15.
Script: `python -I scripts/storage_calc.py disk|raid|raid-map|parity ...`.

## 1. I/O devices (ch.36)

- **[from source]** Bus hierarchy: memory bus, general I/O bus (PCI), peripheral bus (SCSI, SATA, USB); modern system with DMI and PCIe (NVMe via PCIe) (OSTEP p.68-70) **[DATED]**.
- **[from source]** Canonical device: interface (**status**, **command**, **data** registers) + internals; 4-step protocol: poll until not BUSY, data into the data register (**programmed I/O**), command, poll until done (OSTEP p.70-71).
- **[from source]** **Interrupts** free the CPU (overlap), but only pay off for slow devices; an interrupt flood can cause **livelock**; hybrid poll-then-interrupt (two-phase); interrupt **coalescing** (OSTEP p.72-73). **DMA** takes the data copying off the CPU (p.73-74).
- **[from source]** How to talk to the device: I/O instructions (x86 `in`/`out`, privileged) or **memory-mapped I/O** (OSTEP p.74-75). **Device driver**: abstraction; FS stack in Linux (generic block layer); >70% of the kernel code is in drivers; detail is lost (SCSI → only EIO) (OSTEP p.75-76). IDE case study (registers 0x1F0-0x1F7, 0x3F6) and xv6 driver (OSTEP p.76-79).

## 2. Hard disks (ch.37)

- **[from source]** Interface: array of 512 B sectors; only the 512-byte write is atomic (**torn write** for larger ones); sequential access is faster (OSTEP p.145-146).
- **[from source]** Geometry: platter, surface, spindle, RPM (7,200-15,000; 10,000 RPM ≈ 6 ms/rotation), track, head, arm; **rotational delay**, **seek** (acceleration, coasting, deceleration, settling of 0.5-2 ms), transfer; **track skew**; **multi-zoned**; cache/track buffer with **write-back** vs **write-through** (OSTEP p.146-149).
- **[from source]** **T_I/O = T_seek + T_rotation + T_transfer** (Eq.37.1); **R_I/O = size/T_I/O** (Eq.37.2) (OSTEP p.150). Cheetah 15K.5 (seek 4 ms, 15,000 RPM, 125 MB/s) and Barracuda (9 ms, 7,200 RPM, 105 MB/s) **[DATED]**: random 4 KB ≈ 6 ms and ≈ 0.66 MB/s (Cheetah); ≈ 13.2 ms and ≈ 0.31 MB/s (Barracuda); sequential 100 MB ≈ 800 ms and ≈ 950 ms; sequential/random ratio ≈ 200 to 300+ (OSTEP p.151-152). Average seek = 1/3 of the full seek (distance) (p.153).
- **[from source]** Disk scheduling: **SSTF** (starvation; the OS does not see the geometry → nearest-block-first), **SCAN/elevator** (F-SCAN, C-SCAN), **SPTF/SATF** considers rotation and runs on the disk; **I/O merging**; **work-conserving** vs not (anticipatory) (OSTEP p.154-158).

## 3. RAID (ch.38)

- **[from source]** RAID looks like one big disk; **transparency enables deployment**; **fail-stop** failure model (OSTEP p.235-237). Axes: capacity, reliability, performance; **S** (sequential) and **R** (random) with S ≫ R (OSTEP p.237-241). Example: seek 7 ms, rotation 3 ms, 50 MB/s: S = 10 MB/210 ms = 47.62 MB/s and R = 10 KB/10.195 ms = 0.981 MB/s (OSTEP p.241).
- **[from source]** **RAID-0**: `Disk = A % N`, `Offset = A / N` (block 14 on 4 disks → disk 2, offset 3); chunk size; capacity N·B; reliability 0 (OSTEP p.238-241). **RAID-1** (RAID-10 and RAID-01); consistent-update problem with write-ahead log in NVRAM (OSTEP p.242-244). **RAID-4** with **XOR**, full-stripe write, additive and **subtractive** parity: `P_new = (C_old ⊕ C_new) ⊕ P_old`; **small-write problem** (R/2); **RAID-5** with rotated parity (N/4·R on random writes) (OSTEP p.244-249).
- **[from source]** **Table (Fig.38.8, p.249)**: capacity R0 N·B, R1 N·B/2, R4/R5 (N−1)·B; reliability R0 0, R1 1 (up to N/2 with luck), R4/R5 1; seq read/write R0 N·S, R1 (N/2)·S, R4/R5 (N−1)·S; random read R0 N·R, R1 N·R, R4 (N−1)·R, R5 N·R; random write R0 N·R, R1 (N/2)·R, R4 R/2, R5 (N/4)·R; write latency T (R0, R1) and 2T (R4, R5). Conclusions: striping if only performance matters; mirroring for random I/O and reliability; RAID-5 for capacity + reliability (OSTEP p.249-250).
- **[from source]** Hot spare, reconstruction, "Level 6" (tolerating multiple failures) mentioned without detail, software RAID (OSTEP p.250). **[extrapolation]** MTTR/URE during reconstruction, RAID-Z and erasure codes are not developed (ch.46 only mentions "erasure codes", p.742).

## 4. Heuristics

- Quantify before deciding: `storage_calc.py disk` (HDD) and `raid` (comparison).
- "Use disks sequentially" (p.152): group I/O.
- In RAID-4/5, small writes cost 4 I/Os; prefer full-stripe writes (p.246-249).
