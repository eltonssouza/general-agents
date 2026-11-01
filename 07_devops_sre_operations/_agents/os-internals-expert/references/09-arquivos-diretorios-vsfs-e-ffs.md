# 09. Files and directories, implementation (vsfs) and Fast File System (ch. 39, 40, 41)

PDF: ch.39 = p.331-359; ch.40 = p.429-446; ch.41 = p.514-527.
Script: `python -I scripts/storage_calc.py inode|fsize|amortize|io-count ...`.

## 1. File and directory interface (ch.39)

- **[from source]** **File** = linear array of bytes with a low-level name (**inode number / i-number**); **directory** = list of (human-readable name, i-number) pairs; root `/`; extension (.txt) is only a convention (OSTEP p.331-333).
- **[from source]** `open()` (O_CREAT|O_WRONLY|O_TRUNC) returns a **file descriptor**, a per-process private integer that acts as a **capability**; in xv6 it is an index into `struct file *ofile[NOFILE]` (OSTEP p.333-334). fds 0, 1 and 2 are stdin/stdout/stderr (p.336). `strace` shows the syscalls (OSTEP p.335-336).
- **[from source]** **Open file table** (system-wide): each entry holds the file, the **current offset**, readable/writable and a reference count; `lseek` only changes this in-memory offset and **causes no disk I/O** (do not confuse with disk seek); `fork` and `dup`/`dup2` share the entry (offset visible to the parent; count = 2) (OSTEP p.337-341).
- **[from source]** `write()` only guarantees eventual writing (buffer of ~5 to 30 s); `fsync(fd)` forces dirty data out; sometimes the directory also needs `fsync` (OSTEP p.342). `rename()` is (normally) atomic with respect to crashes; editor pattern: write `foo.txt.tmp`, `fsync`, `close`, `rename` (OSTEP p.343-344).
- **[from source]** `stat`/`fstat` and **inode**: size, i-number, permissions, uid/gid, times (`st_atime`, `st_mtime`, `st_ctime`), number of links (OSTEP p.344-345). `rm` uses `unlink()`; **hard link** (`link`) creates another name for the same inode and there is a **link count**: only when it reaches zero are the inode and blocks freed; a hard link cannot point to directories or to another volume (OSTEP p.346-350). A **symbolic link** is a file of a different type whose data is the pathname; it can become **dangling** (OSTEP p.350-352).
- **[from source]** `rwx` permissions for owner/group/other; `chmod 600`; the x bit on a directory allows `cd`; AFS ACLs (`fs listacl`) (OSTEP p.352-354). `mkfs` and `mount` join file systems into one tree (OSTEP p.354-356). **TOCTTOU**: check and use separated in time allow a swap (e.g., root service, `lstat` and then update; partial mitigation: `O_NOFOLLOW`, fewer root services) (OSTEP p.355).

## 2. vsfs: structures and access paths (ch.40)

- **[from source]** Disk of 64 blocks of 4 KB: superblock, inode bitmap, data bitmap, inode table (5 blocks; 256-byte inode → 16 per block → 80 inodes) and data region (56 blocks) (OSTEP p.430-432). Mount reads the superblock first (p.432).
- **[from source]** Address of an inode: inode 32 → offset 32 × 256 = 8192; table at 12 KB → 20 KB → sector 40 (`blk = (inumber*sizeof(inode))/blockSize`; `sector = ((blk*blockSize)+inodeStartAddr)/sectorSize`) (OSTEP p.433). ext2 inode fields (Fig.40.1) (p.434).
- **[from source]** Pointers: **direct**, **indirect**, **double indirect**; with 12 direct + 1 indirect (4 KB blocks and 4 B pointers) the file reaches 4144 KB; with double indirect, a little over 4 GB; **extents** (pointer + length) in XFS and ext4; unbalanced tree because most files are small (OSTEP p.434-436) **[DATED]** (study statistics).
- **[from source]** Directory = list of entries (inum, reclen, strlen, name); FAT uses a linked list with an in-memory table; free space via bitmaps (or free list/B-tree) and preallocation of ~8 blocks (OSTEP p.436-438).
- **[from source]** **Access paths** (OSTEP p.438-442): `open` reads the root inode (well-known i-number = 2), the directory data and the inodes component by component; **the I/O of open grows with the path length**; `read` consults the inode and **updates the last-accessed time** (a write); **bitmaps are not consulted on reads**; `write` with allocation = **5 I/Os**; creating `/foo/bar` = **10 I/Os** in the example.
- **[from source]** Caching: fixed cache (~10% of memory) vs **unified page cache**; **write buffering** of 5 to 30 s; TIPs static vs dynamic partitioning and durability/performance; a DBMS uses `fsync`, direct I/O or raw disk (OSTEP p.442-444).

## 3. FFS (ch.41)

- **[from source]** The old UNIX FS delivered only ~2% of the bandwidth because it treated the disk like RAM, fragmented the free list and used 512-byte blocks (OSTEP p.514-515). **FFS** keeps the API and becomes "disk aware": **cylinder/block groups** with a copy of the superblock, bitmaps, inodes and data per group (OSTEP p.516-518).
- **[from source]** Policies: "keep related stuff together": directories in the group with few directories and many free inodes; a file in its inode's group; files of the same directory in the directory's group (OSTEP p.518-520). Locality measured with SEER traces (~40% of opens at distance 0 or 1; ~25% at distance 2) **[DATED]** (OSTEP p.520-521).
- **[from source]** **Large-file exception** (spread by chunks) and **amortization**: with 10 ms positioning and 40 MB/s, 50% of peak requires ~409.6 KB per chunk; 90% ≈ 3.6 MB; 99% ≈ 39.6 MB; the real FFS uses 12 direct blocks in the inode's group and each indirect block (4 MB with 4 KB blocks) in another group (OSTEP p.521-523).
- **[from source]** Other innovations: 512 B **sub-blocks**, **parameterization** (obsolete with track buffer), long names, **symbolic links**, **atomic rename** (OSTEP p.523-525). Lesson: "treat the disk like it's a disk" (p.525).
- **[extrapolation]** ext4 beyond "uses extents" and "journaling with checksum" (p.435, p.582) is not detailed.

## 4. Useful questions

- "How many I/Os to open /a/b/c and read 1 block?" → `storage_calc.py io-count` + p.439-441 (no cache).
- "Maximum file size?" → `fsize` with the inode parameters.
