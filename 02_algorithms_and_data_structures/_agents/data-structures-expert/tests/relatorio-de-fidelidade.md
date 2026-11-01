# Fidelity report: data-structures-expert (v2, after audit)

Source: *Open Data Structures* (Pat Morin, Edition 0.1Gβ), 326 pages, native text extracted per page with PyMuPDF. Package convention: `(ODS p.N)` = PDF page; printed = N − 12 (verified: PDF p.13 = printed 1; PDF p.326 = printed 314; PDF p.64 = printed 52 in the rendered image). Source note: the PDF title page says "in pseudocode", although the file is named `...-Python.pdf` and the v1 package called it "(in Python)".

## 1. What the previous report (v1) said and why it was rewritten
The v1 report declared 19 of 19 cases approved "blind" by an "independent evaluator" and validated precisely claims that a reading of the PDF does not support (for example "4 coloring invariants", "Φ = 2·|n − len(a)/2|", "α-weight-balanced", "primary clustering", "expected depth 2 ln n" and "insertion in 4 steps"). It mostly checked the page range. This version replaces the report and does **not** repeat the claim of a blind test.

## 2. Inventory
- Single source: `02_algorithms_and_data_structures\Open-Data-Structures-Python.pdf`, 326 pages. The PDF has 12 front-matter pages; chapters 1-14 occupy PDF p.13-311; the bibliography, p.313-320; the subject index, p.321-326 (the PDF table of contents/bookmarks point Bibliography at p.311 and Index at p.313, which is shifted; corrected in `morin_index.json`).
- v1 package convention: already PDF (the chapter ranges, such as "ODS p.43-72" and "p.287-310", match the PDF), but **inconsistent in several chapters**: Ch. 7 (rotations on p.161-163, actually p.165-166), Ch. 11 (lower bound on p.230-232, actually p.239-242; heap-sort on p.239-243, actually p.237-239), Chs. 5, 9, 10, 14 with deviations of 1 to 4 pages.
- Extracted text: `scratch\audit\data-structures-expert\src\odsp.txt` (326 `=== PAGE N ===` markers). Backup of the original package: `scratch\audit\data-structures-expert\v1_backup\`.

## 3. Method
1. **Backup** of the v1 package before any change.
2. **Full reading of the extracted text** of chapters 1-14 (PDF p.13-311) by the package author, page by page, with page notes for each claim in the package; bibliography and index only by sampling (publication years cited; 10 entries checked).
3. **Images**: pages 64 (RootishArrayStack formulas), 67 (space bound), 196 (red-black height) and 290 (B-tree height) were rendered and viewed; the formulas used in the package match the images. The remaining formulas were read from the extracted text.
4. **Two-layer automatic audit** (package scripts): `tests/audit_tokens.py` (backticked terms against the cited pages, with ±1 page tolerance reported as NEAR) and `tests/verify_citations.py` + `citation-checks.json` (curated checks).
5. **Manual audit by sampling**: 125 claims of the v1 package classified as OK / wrong page / unsupported / exaggeration, prioritizing the agent prompt, "always/never/mandatory", numbers, formulas and comparisons, and covering all 14 chapters (`scratch\audit\data-structures-expert\notes\manual_sample.tsv`).
6. **Correction** of the references (16 files), the agent, the scripts, README and adapters; creation of tests.

## 4. Audit results of the v1 package
### 4.1 Automatic layer (v1 baseline, `audit_tokens.py`)
- `(ODS p.…)` citations read in the agent files, references, skills and README: **395** (479 counting tests/, scripts and the full README as well). **5** with an invalid range: literal `(ODS p.N)` markers used as a format template.
- Backticked terms checked: **238**; **22 FAILURES** (term absent from the cited page(s)) and **19 NEAR** (only on the neighboring page). Examples: `rotate_left` and `rotate_right` cited on p.161-162 (they are on p.165-166); `remove_last`/`add_first` on p.75-80 (the book's DLList does not name the Deque operations this way on those pages); `ArrayQueue` cited for BFS (the book uses `SLList`, p.260); `LinearHashTable` on p.276-277 (XFastTrie uses a `USet` implemented by hashing); `ScapegoatTree`/`DLList` on p.32-33.
- This layer only checks backticked identifiers; it is a partial safeguard and **let most of the real errors in the next section through**.

### 4.2 Manual layer (125 v1 claims read against the page)
| Verdict | Count |
|---|---:|
| OK | 36 |
| Wrong page (content exists, cited page does not) | 23 |
| Unsupported claim (the book does not say it or says something else) | 44 |
| Exaggeration (the book says less or something more specific) | 22 |
Only 36 of 125 (29%) were correct as written; 89 (71%) were corrected.

Relevant examples of what was unsupported or wrong (v1):
1. "RedBlackTree has 4 coloring invariants" and "insertion with at most 2 rotations, removal with 3": the book has two properties (black-height and no-red-edge, ODS p.194), black root and black `nil` as conventions, the variant's left-leaning property (p.198) and **does not state** rotation ceilings (only Theorem 9.2, O(m) in fixups, p.208-209). The package also described the "classic" insertion (red/black uncle) and not the book's variant.
2. "Skiplist: expected steps ≤ 2 ln n + O(1)" (v1, ODS p.107-108) and "MeldableHeap: path ≤ 2 ln n + O(1)": the book says 2 log n (log₂) for the skiplist (p.96, 107-109) and ≤ 2 log n for merge (p.226); 2 ln n belongs to the Treap (p.164, 170).
3. "Universal 2-independent multiplicative hashing" and "under a 2-independent hash function linear probing is O(1)": the term does not exist in the book; the book proves Pr ≤ 2/2^d (p.116) and the linear probing analysis **assumes independent, uniform hashing** (p.124).
4. "Additive resizing Θ(n²)", "primary clustering", "tombstone", "real-time": terms/analyses the book does not contain (verified as negatives N01-N05 and N13).
5. YFastTrie with "blocks of w/4 to 2w, amortized split/merge": the book uses random sampling with probability 1/w and expected size ≤ 2w − 1 (p.279-284); space O(n + w), not O(n).
6. B-tree: "removal swaps with the predecessor", "merge produces a node with 2B−1 keys", "Bayer and McCreight, 1972", "B = 4096 words → 3 or 4 levels": the book uses the successor (p.299, 301), 2B−2 keys (p.303), 1970 (p.308, bibliography) and B = 256 for a 4096-byte block (p.291).
7. Heaps/sorting/graphs: BinaryHeap "worst case" (the book: O(log n) ignoring `resize`, amortized in Table 1.2); HeapSort with a "max-heap" (the book uses a min-heap and reverses, p.237); BFS with `ArrayQueue` and DFS with a boolean `seen` (book: `SLList` and white/grey/black colors, p.260-262); adjacency-list `out_edges` "O(degree)" (it returns `adj[i]`, p.258) and `in_edges` O(n+m) omitted; Θ(n²) BFS/DFS on a matrix (the book only analyzes lists).
8. Rootish: "only the last block wastes space" (the book: up to two non-full blocks, waste ≤ 2r−1, p.67).
9. Potential method "in Ch. 1" and Φ = 2·|n − len/2| for the ArrayStack: the book does not state the general method in Ch. 1 and the proof of Lemma 2.1 is by counting (p.47-48).

## 5. What was corrected (counts)
- **16 reference files** rewritten keeping their names; every v1 `[from source]` was reread: 89 problematic claims corrected (23 pages, 44 rewritten/removed/downgraded, 22 reduced to what the book says). New version (outside tests/): 440 `[from source]` markers, all with a page; in the references and the agent, 36 `[inference]`, 43 `[extrapolation]` and 14 `[DATED]`.
- **Page convention** standardized (PDF; printed = N − 12) with a chapter map in `references/INDEX.md` and the list of what the book does not contain.
- **Agent**: prompt rewritten (76 lines) with scope/boundary, golden rules with origin and label, a lookup table with real files, response format, epistemic honesty with the 4 labels, `[DATED]` content and anti prompt-injection; frontmatter with `tools: Read, Grep, Glob, Bash` (Edit and Write removed, unnecessary for a lookup specialist).
- **README** with installation for Claude Code, Codex and GitHub Copilot and a notice to check current documentation; `AGENTS.md` (Codex) and `.github/agents/data-structures-expert.agent.md` (Copilot) created.
- **Scripts**: 4 existing ones audited and fixed (`calculate_amortized.py`: Rootish now uses the book's bounds and the additive mode is labeled `[extrapolation]`; `simulate_rotation.py`: page 165-166, the "6 pointers" claim removed, checks depths; `analyze_hash_probes.py`: the book's rules with `del`/`q`/resize and an invariant demo; `morin_lookup.py`: index with curated topics and `NOT COVERED`) and **2 added**: `scripts/ods_cost_lookup.py` (+ `ods_costs.json`, 63 entries with page) and `scripts/structure_simulator.py` (ArrayStack, DualArrayDeque, SEList and ScapegoatTree checking the book's lemmas). `morin_index.json`: 143 of 145 table-of-contents entries were correct; Bibliography/Index fixed; 80 curated topics added.

## 6. Verifier results after the correction
- `tests/audit_tokens.py`: **499 citations**, **461 terms** checked, 0 invalid ranges, **0 NEAR**, **0 FAILURES** (also runs with `--strict`).
- `tests/verify_citations.py`: **122 positive checks** (key terms on the cited page) and **18 negative** (terms the book does not contain: tombstone, primary clustering, 2-independent, real-time, load factor, NP-completeness, flow, other graph algorithms, general potential formula, "3 rotations", w/4, α-weight-balanced, CPU cache, LSM, other open-addressing probes, Timsort/introsort, lock-free/tail latency, union-find): **0 failures**. The verifier has a self-test that confirms it **detects** a wrong page and a present negative term.
- `tests/run_script_tests.py`: 29 checks (24 script/inline cases, check of the 145 table-of-contents entries, index topics, verifiers and self-test), **0 failures**.
- Simulations (`structure_simulator.py ... --check`): ArrayStack, DualArrayDeque, SEList and ScapegoatTree with no violation of the lemma bounds in 12 standard pattern × structure combinations (m = 20 000; ArrayStack also with m = 100 000).

## 7. Test cases
25 cases in `tests/casos-de-teste.md` (7 C, 8 P, 6 B, 2 F, 2 S), with CT-01 to CT-25. The 16 cases with a script or calculation (CT-08 to CT-15 and the others marked) are reproduced by `run_script_tests.py`. The conceptual, edge-case and injection cases were **answered and evaluated by the package author**, from the agent, the references and the scripts, with each criterion checked against the PDF page.

## 8. Honesty about the validation (important)
- **There was no blind run by an independent model.** No different model answered the cases without access to the notes and the answer key; the "pass" result of the conceptual cases is a self-assessment and may overstate performance.
- The audit was done by **direct reading** of the extracted text; there was no review by a second auditor.
- The verifiers confirm the presence of terms on the page, not the truth of each sentence; the truth of the sentences not covered by the 122 checks depends on manual reading.
- The scripts simulate the book's **rules**; the numeric results are `[extrapolation]` demonstrations.

## 9. What was NOT audited
- Bibliography (PDF p.313-320) and subject index (p.321-326): samples only.
- Chapter exercises: read to confirm those mentioned (3.1, 4.7, 4.10, 4.15, 5.3, 5.5, 5.11, 7.5, 8.3-8.8, 10.3-10.11, 11.3-11.5, 11.10, 14.6-14.8), but not reviewed in detail; the package does not solve exercises.
- Complete proofs (for example Lemma 5.4, Lemma 7.1, Lemma 8.3, Lemma 14.1) were summarized, not reproduced; the final bounds were checked.
- Figures: there was no systematic check of tree drawings and numeric examples; only the four rendered pages.
- Comparison with other editions of the book (Java and C++ versions exist with different numbering): out of scope; the package is only valid for Edition 0.1Gβ of the audited PDF.
