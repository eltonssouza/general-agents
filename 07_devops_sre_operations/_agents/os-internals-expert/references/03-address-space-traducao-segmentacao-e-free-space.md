# 03. Address space, translation (base/bounds), segmentation, Memory API and free-space (ch. 13-17)

PDF: ch.13 = p.43-51; ch.14 (Memory API) = p.121-132; ch.15 (translation) = p.198-212; ch.16 (segmentation) = p.303-314; ch.17 (free-space) = p.392-409.
Script: `python -I scripts/vm_sim.py base-bounds|segments ...`.

## 1. Address space (ch.13)

- **[from source]** Early systems: the OS was a library in memory and there was a single program; multiprogramming and time sharing required keeping several processes in memory (saving all memory to disk on each switch would be far too slow) and brought the protection problem (OSTEP p.43-45).
- **[from source]** **Address space** = the program's view of memory: code, stack and heap (and static data); in the 16 KB example the heap grows in one direction and the stack in the other (convention only; with threads it no longer holds) (OSTEP p.45-46).
- **[from source]** VM goals: **transparency**, **efficiency** (time and space, with hardware support such as TLBs) and **protection/isolation** (OSTEP p.47-48). Process A's virtual load at 0 landing at physical 320 KB illustrates virtualization (p.47).
- **[from source]** Every address a user program prints is virtual (OSTEP p.49).

## 2. Memory API (ch.14)

- **[from source]** Stack memory (automatic) × heap (explicit: `malloc`/`free`); `sizeof` is a compile-time operator; `strlen(s)+1` for strings; `malloc`/`free` are library calls, not syscalls; they use `brk`/`sbrk` and `mmap()` (OSTEP p.121-124, 128).
- **[from source]** Common errors: not allocating, allocating too little (buffer overflow), not initializing, leaking (memory leak), freeing too early (dangling pointer), double free, invalid free; in a short program the OS reclaims everything on exit; tools: valgrind, purify (OSTEP p.124-128).

## 3. Base and bounds (ch.15)

- **[from source]** Hardware-based address translation; **dynamic relocation** with **base** and **bounds** registers: `physical address = virtual address + base`; VA ≥ bounds or negative raises an exception (OSTEP p.202-204). Example: base 32 KB, PC 128 → 32896; load of 15 KB → 47 KB (p.203-204).
- **[from source]** Example with a 4 KB space loaded at 16 KB: VA 0→16 KB; 1 KB→17 KB; 3000→19384; 4400→fault (OSTEP p.204-205).
- **[from source]** Hardware support: user/kernel modes, base/bounds pair, privileged instructions to change them and to register handlers, exceptions; the OS uses a **free list** to find slots, saves/restores base/bounds on context switch (PCB) and installs handlers at boot (OSTEP p.205-209).
- **[from source]** Limit: **internal fragmentation** (space between heap and stack wasted in the slot) → segmentation (OSTEP p.210).

## 4. Segmentation (ch.16)

- **[from source]** One base/bounds pair per logical segment (code, heap, stack) allows **sparse address spaces**; example: code base 32K/2K, heap 34K/3K, stack 28K/2K (OSTEP p.303-305).
- **[from source]** Translations: VA 100 (code) → 100+32 KB = 32868; heap VA 4200 → offset 104 → 34920 (not 39016); VA ≥ 7 KB → **segmentation violation** (OSTEP p.305-306).
- **[from source]** Segment identification: **explicit** (high bits; 2 of 14; `SEG_MASK 0x3000`, `SEG_SHIFT 12`, `OFFSET_MASK 0xFFF`; pseudo-code with `Offset >= Bounds[Segment]` → exception) or **implicit** (by how the address was formed) (OSTEP p.306-308).
- **[from source]** The stack grows downward: "grows positive?" bit; VA 15 KB = 0x3C00 → offset 3 KB − 4 KB (maximum segment size) = −1 KB → PA 28 KB − 1 KB = 27 KB (OSTEP p.308). Protection bits (code Read-Execute) allow sharing code (p.309).
- **[from source]** Coarse × fine granularity (Multics, Burroughs B5000: thousands of segments); OS issues: saving segment registers, growth via `sbrk()`, **external fragmentation** (24 KB free in 3 pieces do not satisfy 20 KB), **compaction** (expensive); algorithms: best/worst/first fit, buddy (OSTEP p.309-312).
- **[from source]** Summary: segmentation is not enough (a large, sparse heap in a single segment must be entirely in memory) → paging (OSTEP p.312).

## 5. Free-space management (ch.17)

- **[from source]** With variable-size units, **external fragmentation** arises; example: 20 free bytes in two 10-byte pieces do not satisfy 15 (OSTEP p.392). Chapter assumptions: malloc/free interface, no relocation after handing out, contiguous region (p.393-394).
- **[from source]** Mechanisms: **splitting** and **coalescing**; **header** with size (and magic number) before the returned block; a request for N bytes searches for N + header; free list embedded in the free space (4096 heap via `mmap` → node of 4088; a request for 100 consumes 108) (OSTEP p.394-400). Without coalescing the list becomes fragmented (p.401). Growing the heap: fail or `sbrk` (p.402).
- **[from source]** Strategies: **best fit**, **worst fit** (most studies: bad), **first fit** (fast; pollutes the beginning), **next fit**; list 10-30-20 and request of 15: best uses 20, worst and first use 30 (OSTEP p.402-404). Others: segregated lists / **slab allocator** (Bonwick), **buddy** (blocks of 2^N; recursive coalescing; buddies differ in 1 bit) (OSTEP p.404-406).
- **[inference]** The book does not compare the fits numerically; the choice depends on the workload (p.406-407).
