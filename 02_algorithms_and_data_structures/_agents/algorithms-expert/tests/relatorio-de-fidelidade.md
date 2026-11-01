# Fidelity report — algorithms-expert (audit v1 → v2)

**Source**: *Algorithms*, Jeff Erickson (1st paperback ed., 13/Jun/2019), 472-page PDF; abbreviation **JE**. **Page convention**: `(JE p.N)` = PDF page; printed = N − 18 (checked: Ch. 1 at printed page 21 = PDF 39). Package v1 already used PDF pages for the chapter boundaries; the pages *inside* the chapters were often shifted or were claims without support.
**Reference text**: PDF extracted with PyMuPDF (`tests/extract_pdf_text.py`) as `=== PAGE N ===`; formulas checked by **rendering** pages 111, 307, 330, 352, 359 (and reading the text of the others) when the extraction scrambled the notation.

> **Method notice (important)**: this audit was done by **direct reading of the pages and deterministic verifiers**. **There was no blind execution by an independent model** of the questions in `casos-de-teste.md`: the 28 cases were executed by the auditor himself against agent + references + scripts (24 of them automated in `run_script_tests.py`). The result measures the fidelity of the references and scripts to the source, not the performance of a model in production.

## 1. What package v1 contained
A 91-line agent (full prompt), 14 references (~1,000 lines), 4 skills with Python scripts (recurrence-solver, dp-table-analyzer, graph-complexity-audit, erickson-topic-lookup + 212-entry JSON index), 19 test cases and a report that "validated 19/19" without checking the page text (range only). **336 citations** `(JE p.N)`, all within 1..472 (the previous validation only checked that).

## 2. Findings in v1

### 2.1 Automatic audit (`tests/audit_tokens.py` over `v1_backup`)
336 citations; **123 terms/asymptotic expressions** extracted from the cited passage and checked against the cited pages: **55 OK (45%)**, 8 only on the neighboring page, **34 exist in the book but in another region** (ELSEWHERE) and **26 do not exist in the book** (ABSENT): 68 of 123 (55%) failed. Part of the ELSEWHERE/ABSENT is noise (math scrambled in the extraction; Θ where the book proves O), but the set covers the real failures below. Full output: `scratch/audit/algorithms-expert/notes/audit_tokens_v1.txt`.
Lookup index (`erickson_index.json`): **5 entries with the page shifted by 1** (Game Trees 91→92, Stable Matching 187→188, Tuple Selection 374→375, Graph Coloring 412→413, On Beyond Zebra 429→430) and **12 titles with a "♥" encoding artifact**.
Negative checks (`citation-checks.json`): **9 of the 24** claims that the book does not contain were asserted in v1 (minimax, patience sorting, Knuth-Yao, "greedy choice property", applicant-optimal/institution-pessimal, Menger, König, RAM unit cost, Master Theorem, "cut property").

### 2.2 Manual sample (106 claims read against the page; table in `notes/amostra_manual.json`)
| Verdict | Count | % |
|---|---|---|
| OK | 33 | 31% |
| Wrong page | 18 | 17% |
| Unsupported claim | 30 | 28% |
| Exaggeration / strong paraphrase | 25 | 24% |

The sample prioritized the agent prompt, sentences with "always/never/mandatory", numbers/complexities, comparisons, names of algorithms/theorems and the scripts, and covers **all 13 chapters** of the book and all 14 references.

### 2.3 Relevant examples of what was unsupported or wrong
1. **Invented Ch. 0**: the RAM model, the "formal table of $O,\Omega,\Theta,o,\omega$" and "Erickson's Golden Rule" (a quotation about induction) attributed to JE p.33-35 are **not** in the chapter; RAM only appears in note 6 on p.402 and the preface lists the notation as a prerequisite (p.6).
2. **Dijkstra with negative edges**: "fails catastrophically with any negative edge" (agent, p.301, 303-304) oversimplifies the book: only `NonnegativeDijkstra` is wrong; the full `Dijkstra` is correct without negative cycles, but may be **exponential** (p.306-307).
3. **"5-step" DP procedure** (p.123-125) with "DAG" as step 3: the book has **two stages** with sub-steps (a)-(f) and the dag appears in Ch. 5-6 (p.211, 252).
4. **Game trees as Max/Min Minimax with scores** (p.91-94): the book uses Zermelo's *good/bad* states (p.93); minimax does not occur in the text.
5. **Gale-Shapley with the roles swapped** (applicants proposing, "invariant: institution only improves") and the terms *applicant-optimal*: in the book the **hospitals** propose (p.191, 193-194).
6. **Edmonds-Karp "fattest finishes in $O(E^2\log E)$ augmentations"** (p.358-359): the book gives $E\ln|f^*|$ iterations and **running time** $O(E^2\log E\log|f^*|)$ (p.359, checked by rendering).
7. **Johnson $O(VE+V^2\log V)$ (p.331)**: the book gives $O(VE\log V)$ with a binary heap (p.330) and the Fibonacci form only in note 3 on p.329.
8. **König and Menger theorems** and the **Cook-Levin proof** attributed to the book (p.371-374, 404-406): the book does not state/prove them (Cook-Levin: "I won't even sketch a proof", p.401-402).
9. **Scripts**: `solve_recurrence` called the method "Master Theorem" (the book only mentions it in the index, p.454); `analyze_dp` stated LIS in $O(n\log n)$ (*patience sorting*), optimal BST in $O(n^2)$ (Knuth-Yao) and Subset Sum in $O(T)$ space as from the book, and used the invented constant `n*m*10` for 3D tables; `audit_graph_complexity` had "matrix" times (Kruskal $O(V^2+E\log V)$, Borůvka $O(V^2\log V)$, Bellman-Ford $O(V^3)$) and per-algorithm memory without support.
10. **Pages inside the chapter**: residual graph (v1 p.352-354, actual 349-350), integrality (354-355, actual 352), irrationals (356-358, actual 353-354), edge classification (246, actual 247), Kosaraju (256-257, actual 258-259), Dijkstra with a PQ (218, actual 220-221), Karp reductions (400-401, actual 402-403), pseudopolynomial (135, actual 422).

## 3. What was fixed (v2)
- **Page convention** declared and mapped in `references/INDEX.md` (table chapter → PDF → printed → file; list of what the book does NOT contain; [DATED] content).
- **14 references rewritten** from reading the pages (all `[from source]` claims checked against the cited page; outside knowledge downgraded to `[inference]`/`[extrapolation]` or removed): **73 of the 106** sampled claims rewritten, downgraded, removed or with the page corrected (30 unsupported, 25 exaggeration and 18 wrong page) and dozens of others outside the sample; "Outside the book" sections in each file.
- **Agent** rewritten (101 lines): page convention, labels, scope by pages, 8 corrected golden rules, when to consult real `references/` and scripts, format, epistemic honesty, boundary, [DATED], anti prompt-injection.
- **Structure**: `README.md` (3 platforms and a notice to check the current documentation), `AGENTS.md` (Codex), `.github/agents/algorithms-expert.agent.md` (Copilot), `plugin.json` 2.0.0.
- **Scripts** audited, corrected and run: `solve_recurrence.py` (recursion tree; `--terms` mode for unequal subproblems; no "Master Theorem"), **new** `check_recurrence.py` (exact numerical verifier of 12 recurrences of the book + `--div` and `--lin` modes), `analyze_dp.py` (11 worksheets with page and labels; `--custom` without an invented constant), `audit_graph_complexity.py` (19 algorithms; Dijkstra nuance; Johnson/Edmonds-Karp corrected), `erickson_lookup.py` + rebuilt index (88 curated topics with verifiable terms, 102 table-of-contents sections with corrected page, **16 "NOT COVERED" topics**).
- **Tests**: `verify_citations.py` + `citation-checks.json`, `audit_tokens.py` + triaged allow-list, `run_script_tests.py`, `casos-de-teste.md` (28 cases), this report; copies synchronized in `_agents_tests/algorithms-expert/`.

## 4. Verifier results (v2)
| Verifier | Result |
|---|---|
| `verify_citations.py` | **135 positive checks** (terms on the cited pages), **24 negative** (plausible claims that the book does NOT contain), **749 citations** with page range verified (0 invalid), 190 index entries checked; **0 failures** |
| `audit_tokens.py` | 506 citations; 349 terms/expressions checked: **330 OK**, 19 accepted in a documented allow-list (`tests/audit-tokens-allow.json`: math scrambled in the extraction, `[inference]` sentences that describe the v1 error), **0 NEARBY, 0 ELSEWHERE, 0 ABSENT** |
| `run_script_tests.py` | script cases, **0 failures** (includes `check_recurrence.py --all`: 12 recurrences, 0 failures); 21 cases when this report was written, 24 after the English-language query cases were added |
| Encoding | UTF-8 without BOM, no U+FFFD/mojibake, no absolute user paths in the package files |

## 5. Audit coverage (what was and was not audited)
- **Read and checked page by page** (extracted text; ambiguous formulas rendered): PDF p.5-6, 19-35, 39-62, 89-111, 115-141 (part of the exercises only the header and note 18/Nadiria), 177-194, 205-224, 243-262, 275-286, 291-315, 327-338, 345-362, 371-386, 397-433 (p.417 and 425-429 only in part: headers and first lines), plus p.253-255 and 454 (index).
- **Not audited**: the **exercises** (p.35-38, 62-88, 111-114, 141-176, 194-204, 225-242, 262-274, 286-290, 314-326 [p.316-326 not read], 338-344, 362-370, 386-396, 433-459), historical notes and marginal curiosities, the figures except the rendered ones, the index except "Master Theorem" and the pseudocode index. The package avoids citing exercises as the source of a claim (except Nadiria's, p.141, and the greedy strategies one, p.194-195).
- The automatic audit checks **terms and asymptotic expressions**, not the full meaning of the sentences; the manual reading covered 106 claims (not all ~500 `[from source]` claims in the package). The positive checks (135) were curated by me and may have selection bias.
- Not verified: reading the **diagrams in English** (recursion trees, example graphs) beyond the text; the correctness of **all** $O(\cdot)$ calculations by proof (`check_recurrence.py` only tests the requested $n$).

## 6. Open items and risks
1. No blind execution by an independent model (see notice). It is recommended to run the 28 cases with a model that sees only the package and compare with the answer key.
2. The 19 allow-list entries of `audit_tokens.py` are false positives **triaged by a person/auditor**; new edits to the references must keep citations and terms checkable.
3. The text extracted from the PDF is not distributed with the package (rights/license): whoever wants to reproduce must run `tests/extract_pdf_text.py` (PyMuPDF) locally.
4. The book is from 2019; "fastest known" is marked `[DATED]`.
