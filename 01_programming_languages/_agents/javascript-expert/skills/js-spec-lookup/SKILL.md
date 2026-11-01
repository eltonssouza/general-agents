---
name: js-spec-lookup
description: Locates clauses, sections, abstract operations and built-in methods in the ECMA-262 17th edition specification (ES2026) and returns the section number, the title and the exact PDF page, using an index of 2,224 sections extracted from the PDF bookmarks. Use when the user asks "where in the Spec is X?", "which clause defines Y?", "what does ECMA-262 say about Z?" or when you need to confirm the exact Spec page for an abstract operation, grammar production or built-in method. Do not use to find out the edition/version in which a feature appeared (use js-version-features) nor to look for host environment APIs such as DOM, fetch or Node.js (they are not in ECMA-262).
---

# Locating sections and pages in ECMA-262 (ES2026)

Source: index `scripts/spec_toc.json` with the **2,224 sections** extracted from the bookmarks of the PDF `JavaScript-ECMA-262-Spec.pdf` (17th edition, ECMAScript 2026, 876 PDF pages).
**Note:** the script reports **in which clause and PDF page** each section starts; to learn what the rule says, then consult the corresponding file in `../../references/` (`linguagem-valores-e-execucao.md`, `linguagem-sintaxe-e-estruturas.md`, `builtins-objetos.md`, `builtins-texto-colecoes.md` or `versoes-e-datado.md`).

## Procedure

1. **Identify the term in English** as it appears in the ECMA-262 titles (e.g. `SameValue`, `IsLooselyEqual`, `Array.prototype.sort`, `Promise.all`, `Proxy`, `ForIn/OfBodyEvaluation`, `Automatic Semicolon Insertion`).
2. **Run the search script** (read-only, no network):
   ```bash
   python -I scripts/spec_lookup.py SameValue
   python -I scripts/spec_lookup.py Array.prototype.toSorted
   python -I scripts/spec_lookup.py --section 13.11
   python -I scripts/spec_lookup.py --page 310
   python -I scripts/spec_lookup.py --top
   ```
   - Passing several terms requires that **all** of them appear in the section title (case-insensitive).
   - `--section N.M` lists the clause and its immediate subsections.
   - `--page N` shows which section was already in progress on page `N` and which sections start on it.
   - `--top` lists the level-1 clauses (1 to 30 and Annexes A to F).
3. **Confirm the content in the distilled references:** use the page and section name found to run `Grep` over `../../references/*.md` and read the faithful summary of the algorithm.
4. **Beware of Spec page breaks:** in the ECMA-262 PDF, a section title often appears in the last lines of a page while the algorithm steps are on the next page. If the index points to `p.N`, check in the references whether the cited steps are on `p.N` or `p.N+1`.
5. **If the script returns no results:** this only means that no section title contains all the searched terms — **it does not prove that the feature does not exist in the Spec**. Try a shorter term, the name of the abstract operation, or `Grep` directly in `../../references/`.

## Limits

- The Spec does not cover **[HOST]** APIs (`fetch`, `setTimeout`, `console`, DOM, `localStorage`, Node.js): they will not appear in the index (except abstract hooks such as `HostEnqueuePromiseJob` and `HostEnqueueTimeoutJob`).
- PDF pages 813–842 (end of the memory model and Annex A, grammar summary) exist, but were not distilled into `references/`; if the index points to a section in that range, report the clause and the page from the index (**[from source]**) and warn that the details of that specific section are not distilled in the package (read the PDF).
- Being in the 2026 Spec index **does not tell in which ECMAScript version the feature appeared** (use `js-version-features`).
