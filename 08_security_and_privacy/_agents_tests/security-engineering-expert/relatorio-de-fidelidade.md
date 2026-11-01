# Fidelity report: security-engineering-expert

Source: *Security Engineering*, Ross Anderson, 3rd ed. (Wiley, 2020; abbreviation SE3). 1212-page PDF; text extracted with `=== PAGE N ===` markers (~3.37 million characters). **Page convention: PDF**; printed = PDF − chapter offset (48 in ch. 1-2 down to 31 in ch. 28; table in `references/INDEX.md`). This report describes what was and was **not** verified.

## 1. Honesty about the method
- **Who wrote and who tested:** the same model that read the book built the package and ran all the tests. **There was no blind test by an independent model**: the tables in `casos-de-teste.md` are evaluation criteria that were not executed independently. A "passed" score below means only a deterministic test (scripts and citation verifier).
- **Block reading, no subagents:** the text was read sequentially by chapter, with per-chapter notes saved to disk (intermediate, outside the package) and only then consolidated into the references.
- **What the verifier proves and does not prove:** that (a) every `SE3 p.N` citation in the package exists within the book's range (and, in the references, in the body 51-1091); (b) for 263 positive claims, the terms/names/numbers that the references attribute to those pages **are in fact on them**; (c) for 21 negative claims, plausible terms (SBOM, STRIDE, bcrypt, WebAuthn, LLM, EPSS...) are **not** on them. It does not prove that the Portuguese paraphrase is faithful in every sentence. Part of the positive checks (the "automatic" ones) was generated from the terms the references themselves cite; the ~30 "curated" ones test specific formulas, numbers and theses.
- **Additional heuristic audit (outside the package):** for each segment cited in the references I compared numbers and proper names with the cited pages (901 segments). It found the errors listed in §3; the remaining points are false positives from translation (e.g. "Holanda"/Holland, "Pentágono"/Pentagon) or formatting (exponents such as 2^64 become "264" in the text).

## 2. Test results (final run)
| Test | Result |
|---|---|
| `tests/run_script_tests.py --src <scratch/security>` | 43 deterministic cases (lookup 15, index 3, calculators 17, checklist 6, encoding 1, citations 1): **43 passed, 0 failed** |
| `tests/verify_citations.py` | 2428 cited pages in package text within range; **263 positive and 21 negative checks, 0 failures** |
| `tests/casos-de-teste.md` | 28 conceptual cases; **not run blind** |

After the English translation of the package, `tests/run_script_tests.py` has 46 cases (3 added: English and Portuguese lookup queries, English area alias and Portuguese checklist answers still accepted); the counts above describe the original run.

## 3. Errors found and corrected during verification
1. **HSM:** the sentence "chain of 17 transactions" and the one about "the least trusted one lies and cheats" are on **PDF p.712**, not p.716; corrected in refs 04 and 12 and in the ch. 20 coverage (now p.702-709, 712, 716-717, 730-733).
2. **Wirecard:** the text says €2.1 billion not found (a quarter of the assets), not €1.9 bn; corrected.
3. **UK smart meters:** "12.5 of 52 million" → the text says 12.5 million installed and 39 million still to be installed (SE3 p.545).
4. **GDPR/history:** "Convention 108" does not appear in the text; it is the Council of Europe convention of 1981 (SE3 p.987); Warren and Brandeis are on p.986.
5. **Chinese Wall:** Brewer-Nash are cited on p.412 (not only 413-415); **Lojack** on p.514; **Bezos's law** on p.1032-1033; CoBIT on p.455; Biobank on p.441.
6. **Terminology:** ch. 5 uses "forward security" (and "forward secrecy" in TLS, p.244); adjusted.
7. **Facts of the book with an inconsistency of its own:** in Fig. 27.1 (SE3 p.1000) the "ATM fraud (large)" row shows 250,000 × 0.2 = 100,000, but the product is 50,000. The book is inconsistent; `se3_calc.py ale --sample` shows and flags the divergence.

## 4. Reading coverage (precise statement)
- **Read in full:** ch. 1, 2, 3, 4, 5 (from 5.2.2; p.192-195 only the start), 6, 9, 11, 27; ch. 8 p.319-355; ch. 10 p.384-408 and 412-416 (p.409-411 only excerpts); ch. 12 p.446-501; ch. 21 p.748-762 and 765-770; ch. 28 p.1046-1083.
- **Read in part (sampling/excerpts):** ch. 7 p.288-314; ch. 13 p.511-516 and 532-535; ch. 14 p.536-546 and 564-566; ch. 15 p.567-569 and 578-585; ch. 16 p.599-607; ch. 17 p.608-615, 618-621, 625-627, 630-635; ch. 18 p.636-640 and 667-674; ch. 19 p.675-677, 685-686, 699-701; ch. 20 p.702-709, 712, 716-717, 730-733; ch. 22 p.771, 794-795, 808-810; ch. 25 p.907-915 (only 25.3 AI/ML); ch. 26 p.981-996; ch. 29 p.1090-1091.
- **Summaries only:** ch. 23 (p.846-847) and ch. 24 (p.896-897).
- **Not read:** the rest of ch. 7, 12, 13-26 not listed above (BGP/DNS/network DoS p.734-747; SSH/WiFi/Bluetooth/VPN p.762-764; GSM/3G/4G/5G; detailed timing/power/Rowhammer p.677-698; Tor, HSM API attacks, enclaves, blockchains p.709-715 and 718-729; autonomous vehicles, PETs/opsec, elections p.898-906 and 916-941; surveillance, crypto wars, terrorism, censorship p.942-980; locks, barriers and sensors p.517-531; nuclear C2 p.570-577; forensic fingerprints and voice; smartcards, probes, glitch, PUFs p.641-666; ch. 12 p.502-510), **Bibliography and Index (p.1092-1212)** and the preface/contents (p.1-50).
- **Consequence:** where a topic is on a page that was not read, the agent must say "the package does not cover it", **not** "the book does not say". `python -I scripts/se3_lookup.py --gaps` lists the ranges.
- **The book has no medicine chapter:** health is in ch. 10 (records, BMA, NPfIT) and 28 (medical devices); the premise of a dedicated chapter is not confirmed.

## 5. Labels and scope
- `[from source]` only for what was read on the cited page; `[inference]` for the organization into procedures/checklists; `[extrapolation]` for formulas and facts outside the book (e.g. the Laplace scale `b = Δ/ε`); `[DATED]` for statistics, incidents, products, standards and regulations (2020 book; see `references/datado-desde-2020.md`).
- The agent **does not replace a formal security review** (architecture, authorized penetration testing, audit, legal opinion). Defensive focus; no operational payloads; reminds scope and authorization.
- Copyright: paraphrase; literal quotations < 15 words and rare.

## 6. Known limitations
1. Semantic fidelity of the paraphrase verified only by a sample of terms, numbers and names; sentences without these markers were not audited automatically.
2. The offsets of ch. 23, 24 and 29 were inferred from the neighboring chapters; confirm with `se3_lookup.py --page N`.
3. The lookup index (103 topics) is manual; a non-indexed topic returns "NOT COVERED" even if the book treats it on a page that was read; in that case consult `references/INDEX.md`.
4. The calculators use the user's assumptions (e.g. detection = 1.0 in `bayes-alarm`); results are reasoning support, not a guarantee.
5. The README installation instructions must be checked against the tools' current documentation.
