# External memory and B-trees (Ch. 14)

Pages = PDF (printed = N − 12). Source: ODS Ch. 14 (p.287-311). The chapter replaces the Word-RAM model with the external memory model.

## 1. External memory model
- Motivation: when the data does not fit in RAM, accessing external storage is extremely slow; when reading one byte, the disk delivers the whole **block** `[from source] (ODS p.287-288)`. The figures from the author's computer (HDD 19 ms, SSD 0.3 ms, RAM below 0.000113 ms; 4096-byte blocks) are `[DATED]` `[from source] (ODS p.287)`.
- Model: external memory divided into blocks of `B` words; the CPU has limited internal memory; transferring a block takes constant time; **computation in internal memory is free** `[from source] (ODS p.288)`. The book does not name the capacity of internal memory (it only says that, for the structures in the chapter, O(B + log_B n) suffices) `[from source] (ODS p.288-289)`.
- `BlockStore`: `read_block(i)`, `write_block(i,b)`, `place_block(b)` and `free_block(i)`; it can be a file partitioned into blocks with a list of free blocks `[from source] (ODS p.289)`.

## 2. B-tree
- For B ≥ 2: all leaves have the same depth and every internal node that is not the root has between B and 2B children; the root has between 2 and 2B children. The 2-4 tree is the case B = 2 `[from source] (ODS p.289-290)`.
- Height: with ℓ leaves and height h, 2B^(h−1) ≤ ℓ ≤ 2(2B)^(h−1), therefore h ≤ (log ℓ − 1)/(log B) + 1 ≤ log_B ℓ + 1 (checked on the rendered page) `[from source] (ODS p.290)`. Since each leaf stores at least one key, the height is O(log_B n) `[from source] (ODS p.294)`. `[inference]` In terms of the number n of keys (ℓ ≤ n), h ≤ log_B(n/2) + 1 holds; the book states the bound in ℓ.
- Each node stores an array of up to 2B−1 keys (`keys`) and of children (`children`); an internal node with k children has k−1 keys; a non-root leaf node has between B−1 and 2B−1 keys; the keys obey BST order `[from source] (ODS p.290)`.
- B is chosen so that a node fits in a block; book example: 4-byte keys and indices and B = 256 give 4096-byte nodes `[from source] (ODS p.291)`. (The phrase "B = 4096 words" is not in the book.)
- The BTree stores the `BlockStore`, the root index `ri` and `n`; the constructor parameter `b` is rounded to odd and `B = b div 2` `[from source] (ODS p.291)`.

## 3. Operations
- `find(x)`: starting at the root, searches for x in `keys` by binary search (`find_it`, O(log B)); if not found, follows the right child, remembering the last key greater than x; cost O(log_B n) block accesses (external memory) and O(log n) in the Word-RAM model `[from source] (ODS p.292-294)`.
- Addition: nodes **do not store a pointer to the parent**, which avoids updating B+1 children on a split (3 accesses instead of B+4); hence `add`/`remove` are recursive `[from source] (ODS p.294)`.
- Split: a node `u` with 2B keys and 2B+1 children creates `w`, which adopts the children at indices B to 2B of `u.children` and the B largest keys; `u` is left with B children and the extra key `u.keys[B−1]` goes up to the parent `[from source] (ODS p.294)`. As a result, the nodes have B−1 and B keys `[from source] (ODS p.306)`. If the root splits, a new root is created with the two nodes `[from source] (ODS p.296-298)`.
- Cost of `add`: descending phase O(log_B n) accesses; ascending phase at most O(log_B n) splits, each involving three nodes, that is O(log_B n) accesses; in the Word-RAM model, each split costs O(B) `[from source] (ODS p.298-299)`.
- Removal: reduces to removing a value x′ from a leaf `u`; if x is in an internal node `u.keys[i]`, it is swapped with **the smallest value of the subtree `u.children[i+1]`** (the successor) and that one is removed from the leaf `[from source] (ODS p.299, 301)`. If the leaf is left with fewer than B−1 keys (underflow): **borrowing** from the sibling if it has more than B−1 keys (the book calls the routine `shift`), or **merging** (`merge`) if it has exactly B−1 keys; the merge joins two nodes with 2B−3 keys into one node with 2B−2 (the extra key comes from the parent) `[from source] (ODS p.299, 302-304)`. The merge can propagate up to the root; if the root is left with a single child, that child becomes the new root `[from source] (ODS p.299)`.
- Book summary: `remove` traverses a path from the root to a leaf, removes a key, does zero or more merges and **at most one** borrow; O(log_B n) in external memory and O(B·log_B n) in the Word-RAM model, before the amortized analysis `[from source] (ODS p.305)`.

## 4. Amortized analysis
- **Lemma 14.1**: starting from an empty B-tree, m `add`/`remove` operations perform at most 3m/2 splits, merges and borrows (credit scheme; each operation creates at most 3 credits and each restructuring consumes 2) `[from source] (ODS p.305-307)`. The proof for B = 2 is that of Ch. 9 `[from source] (ODS p.209, 305)`.
- Consequence: in the Word-RAM model the amortized cost of `add`/`remove` is O(B + log n) `[from source] (ODS p.299, 307)`.
- **Theorem 14.1** (external memory): add/remove/find in O(log_B n) per operation. **Theorem 14.2** (Word-RAM): find in O(log n); add/remove in O(log n) ignoring splits/merges/borrows and O(Bm) in total for those over m operations `[from source] (ODS p.307-308)`.
- Exercises: a variant with B to 3B children that does only O(m/B) restructurings (14.6), redistribution among up to three nodes (14.7), B+-tree with linked leaves and `find_range` (14.8) `[from source] (ODS p.309-311)`.

## 5. Book discussion
- The external memory model is by Aggarwal and Vitter (1988); B-trees are by Bayer and McCreight, **1970** (the book says 1970; some sources cite other dates) `[from source] (ODS p.308, 313-314)`.
- B-trees are "ubiquitous": file systems (HFS+, NTFS, Ext4), databases and key-value stores; variants: B+-trees, B*-trees, counted B-trees `[from source] (ODS p.308)` `[DATED]`.
- Hashing in external memory exists (Jensen and Pagh), expected O(1) for USet, but many use B-trees anyway `[from source] (ODS p.308)`.
- With large B (hundreds or thousands), 99% to 99.9% of the data is in the leaves; the internal nodes can fit in RAM and a search becomes a fast RAM access plus one external access `[from source] (ODS p.308-309)`.
- `[extrapolation]` The book has no table of "3 or 4 levels for billions of keys"; do the computation with `h ≤ log_B ℓ + 1` and the chosen B.
