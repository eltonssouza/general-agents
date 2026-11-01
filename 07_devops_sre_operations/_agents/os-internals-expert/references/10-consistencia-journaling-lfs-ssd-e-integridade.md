# 10. Crash consistency (fsck, journaling), LFS, SSDs and data integrity (ch. 42, 43, 44, 45)

PDF: ch.42 = p.573-593; ch.43 = p.623-638; ch.44 = p.653-676; ch.45 = p.708-721; ch.46 (dialogue) = p.742-743.
Script: `python -I scripts/storage_calc.py amortize|checksum|parity ...`.

## 1. The problem (ch.42)

- **[from source]** Updating persistent structures when power fails in the middle: the **crash-consistency problem** (also "consistent-update") (OSTEP p.573, p.577). Example: appending one block requires three writes (inode I[v2], data bitmap B[v2], data Db), buffered for 5 to 30 s (OSTEP p.574-575).
- **[from source]** Six crash scenarios (p.576): only Db (as if it never happened); only I[v2] (points to garbage and is inconsistent with the bitmap); only B[v2] (**space leak**); I[v2]+B[v2] without Db (consistent metadata, garbage in the data); I[v2]+Db without B[v2] (inconsistency); B[v2]+Db without I[v2] (no owner).

## 2. fsck and journaling

- **[from source]** **fsck** is the "lazy" approach: runs before mount and only guarantees metadata consistency; phases: superblock, free blocks, inode state, **inode links** (orphans go to **lost+found**), duplicates, bad blocks, directory checks; problem: **slow** (minutes to hours) (OSTEP p.577-579).
- **[from source]** **Journaling (write-ahead logging)** (Cedar; ext3/ext4, reiserfs, JFS, XFS, NTFS): ext3 = ext2 + journal (OSTEP p.579). **Data journaling**: transaction with **TxB**, I[v2], B[v2], Db, **TxE**; **physical logging** (vs logical); **checkpointing** (OSTEP p.580).
- **[from source]** Ordering requires **write barriers** (disk caches with immediate reporting break the order; some disks ignore barriers); writing everything at once is unsafe because the disk reorders; solution: write the transaction without TxE and then TxE (an atomic 512-byte block); **checksum** in TxB/TxE (Prabhakaran) removes the wait and went into ext4 (OSTEP p.581-583).
- **[from source]** Protocol: (1) **journal write**, (2) **journal commit** (TxE), (3) **checkpoint**, (4) **free** (journal superblock); **recovery** by **redo logging**; batching; circular log (OSTEP p.583-585).
- **[from source]** **Metadata (ordered) journaling** avoids writing data twice: protocol (1) data write, (2) journal metadata write, (3) journal commit, (4) checkpoint metadata, (5) free; central rule: "write the pointed-to object before the object that points to it"; ext3 offers data, ordered and unordered modes (OSTEP p.585-587).
- **[from source]** **Block reuse**: replay may overwrite new data with an old directory; ext3 uses **revoke records** (OSTEP p.587-588). Alternatives: **soft updates**, **copy-on-write**, **backpointer-based consistency**, **optimistic crash consistency** (OSTEP p.589-590). Journaling reduces recovery from O(volume size) to O(log size) (p.590).

## 3. LFS (ch.43)

- **[from source]** Motivation (Berkeley, early 1990s): large memory makes performance write-dominated; gap between sequential and random I/O (OSTEP p.623). Idea: buffer all updates (metadata included) in a **segment** and write sequentially to a free area; never overwrite (OSTEP p.624-626).
- **[from source]** How much to buffer: `T_write = T_position + D/R_peak`; `R_effective = D/T_write`; for `R_effective = F × R_peak`: **`D = F/(1−F) × R_peak × T_position`**; 10 ms, 100 MB/s and F=0.9 → **9 MB** (OSTEP p.626-627).
- **[from source]** **Inode map (imap)** in pieces alongside the data; **checkpoint region (CR)** at a fixed location (updated every ~30 s); read: CR → cached imap → inode; **cleaner** compacts M segments into N < M; liveness via **segment summary block** (inode number + offset) and version number; hot/cold; **two CRs** and **roll forward** on recovery (OSTEP p.627-634).
- **[from source]** Legacy: WAFL, ZFS, btrfs, SSDs use COW; cleaning was the controversy (OSTEP p.635).

## 4. Flash SSDs (ch.44)

- **[from source]** **Block** (erase block, 128/256 KB) × **page** (a few KB); operations **read**, **erase** (block; ms), **program** (page; 100s of µs); states INVALID/ERASED/VALID; reprogramming without erasing is an error; **wear out** (MLC ~10,000 P/E cycles; SLC ~100,000); **disturbance** (OSTEP p.654-657). Timings: see table Fig.44.2 [DATED] (p.657).
- **[from source]** **FTL**; **write amplification** = traffic written by the FTL ÷ client traffic; **wear leveling**; **direct mapped** FTL is bad; **log-structured** FTL with in-memory mapping table and **OOB** for recovery; **garbage collection**; **TRIM**; **overprovisioning** (OSTEP p.658-664).
- **[from source]** Mapping table of 1 TB with a 4 B entry per 4 KB page = 1 GB; **block-based mapping** (chunk + offset) suffers with small writes; **hybrid mapping** with **log blocks** and **switch/partial/full merge**; page mapping + caching (OSTEP p.664-668).
- **[from source]** Cost and performance [DATED]: random SSD >> HDD; ~US$0.60/GB vs ~US$0.05/GB at the time; hot/cold hybrids (OSTEP p.669-670).

## 5. Integrity (ch.45)

- **[from source]** **Fail-partial** model: **LSE** (latent sector error) and silent **corruption**; frequencies: LSE 9.40% (cheap) and 1.40% (costly); corruption 0.50% and 0.05% **[DATED]** (OSTEP p.708-710). LSEs are handled with redundancy; an LSE during RAID-5 reconstruction motivated **RAID-DP** (OSTEP p.710-711).
- **[from source]** **Checksum**: **XOR** (example 0x201b9403), addition, **Fletcher** (`s1=(s1+d_i) mod 255; s2=(s2+s1) mod 255`), **CRC**; **collision**; layout with 520 bytes/sector; **stored × computed checksum** (OSTEP p.711-715).
- **[from source]** **Misdirected write** → store **physical ID** (disk and block); **lost write** → **write verify/read-after-write** or checksum elsewhere (ZFS in the inode); **scrubbing**; space overhead 0.19% (8 B per 4 KB) and CPU overhead (OSTEP p.715-717).

## 6. Practical use

- "Only the bitmap B[v2] reached the disk: now what?" → it is the **space leak** scenario (p.576); the ordered protocol avoids it by writing data before the metadata commit (p.586).
- "Does journaling double the writes?" → only data journaling; ordered journaling does not (p.585-586).
