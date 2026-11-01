# Fidelity report: privacy-lgpd-engineering-expert

Date of execution: package build session (26/10/2026). Sources: `LGPD-Lei-13709-ptBR.pdf` (25 pages; text extracted with PyMuPDF per page, marker `=== PAGE N ===`) and `NIST-IR-8062-Privacy-Engineering.pdf` (49 pages). **Page convention: PDF** (LGPD has no printed numbering; NIST: printed = PDF − 8, checked by rendering: PDF 9 = printed 1, PDF 49 = printed 41).

## 1. Reading coverage (honesty)
- **LGPD**: read **in full, page by page (1-25)** in the extracted text; all amendment notes were swept by regex and checked against the reading (49 records curated in `scripts/privacy_index.json`, field `amendments`).
- **NIST IR 8062**: text read in full from pages 1-49, **except the detail of the reference lists (pages 39-43 of Appendix D), only skimmed by sampling**; pages 1-5 (cover and notices) read quickly. The **figures were read visually** (PyMuPDF rendering at 110 dpi): Fig. 2 (p.16), Fig. 3 (p.18), Fig. 4 (p.23), Figs. 6 and 7 (p.25), Fig. 8 (p.26), Fig. 9 (p.33). They cannot be verified by text search; what is claimed from them (categories of Fig. 3; matrix of Fig. 8; list of SPs of Fig. 9) is labeled as figure/image.
- Intermediate notes: `scratch/security/privacy-lgpd-engineering-expert/notes/` (compact NIST text, LGPD parse) and build scripts in `.../build/`.

## 2. Citation verification (`tests/verify_citations.py`)
Result of the last run: **OK, 0 failures**. The verifier checks, against the extracted text:
- **131 positive checks** (260 terms) in `citation-checks.json`: each claim cites the PDF page and all terms must appear on it (LGPD p.1-25; NIST p.6-49).
- **23 negative checks** (56 terms, whole word, full text or page) + **42 gap terms** (`privacy_index.json`, field `gaps`) verified as absent: examples "72 horas", "criptografia", "privacy by design", "DPO", "GDPR", "inteligência artificial", PRAM, "differential privacy", "encryption", "risk matrix", "incident". Total negative terms: 98.
- **133 terms of 72 checklist items** on the pages indicated for each item.
- **82 terms of the 33 rows of the LGPD-NIST map** (LGPD terms on the LGPD pages; NIST terms on the NIST pages).
- **181 index checks** (each article of each entry matches the indicated page; amendment notes with a page and law that exist in the text; valid NIST pages).
- **480 citations in Markdown** (`references/*.md`, `agents/*.md`, `README.md`, `AGENTS.md`): for each "(LGPD Art. N ... p.M)" article N appears on page M; "NIST8062 p.N" stays within the range 1-49. The verification of NIST citations is range-only; the semantics were checked by reading.

### Failures found during construction and fixed (proof that the verifier catches errors)
1. Art. 23, I cited at p.11; it is at p.10 (separate from inciso III, p.11).
2. Art. 43, III: the exact wording is "culpa exclusiva do titular dos dados ou de terceiro" (verbatim source text).
3. NIST p.9: the phrase "unauthorized access to personally identifiable information" is interleaved with sidebar text in the extract; term reduced to the contiguous passage.
4. NIST p.21: "(OASIS) Privacy Management" has a parenthesis.
5. Incorrect negative: I claimed that Art. 11 does not contain "legítimo interesse" on p.6, but p.6 also contains Art. 10; the negative was removed and the observation kept as `[inference]` in the prose.
6. Map M23: the term "security of PII" appears only in the image of Fig. 2; replaced by "unauthorized activity" (text of p.16).
7. Index entry with "Art. 57" (the PDF numbering "Art. 5 7." broke the parse); the article list was corrected.
8. Gap "empregado": the word appears (Art. 5º, XIV: "procedimento empregado"); replaced by "trabalhador".
9. Two citations in an amendments table paired the wrong article and page; rewritten item by item.
- **Mutation test** (copy of the package in `scratch`): 4 errors were injected (wrong page in a citation in the .md; invented term in a positive check; existing term declared "absent"; non-existent term in a checklist item); the verifier flagged **4/4**, exit 1.

## 3. Case tests (`tests/casos-de-teste.md`, `tests/casos.json`)
- **32 cases** (31 original + T32, an English-query case added in the English translation): 11 conceptual (T01-T10, T30), 9 practical (T11-T18, T32), 7 edge (T19-T24, T31), 3 out of scope (T25-T27), 2 injection (T28-T29).
- **`tests/run_script_tests.py`**: runs the cases against the scripts (expected content, absence of forbidden content, exit code) and checks JSON integrity, uniqueness of ids, valid pages, map levels and `-h` of each script. **Result: OK, all cases with a command passed (31 of 31 before the translation; 32 of 32 after).**
- Items exercised: search by article/inciso/§; NOT COVERED (72 horas, GDPR, PRAM, criptografia, Art. 99); NIST page conversion; amendment notes (Art. 5º, Art. 55-A); checklist, `pbd` and `evaluate --strict` (exit 1 with gaps); map (`by-objective`, `art 6`, `art 33` NO_SUPPORT); templates (RIPD, incident, record, data subject); injection (unknown id in the answers JSON is ignored with a notice; organization name with `; rm -rf /` is just printed text); English query expansion (T32).
- **Evaluation of the agent's behavior (natural-language answers)**: the criteria in the "Expected" column were checked **by the author** against the prompt (`agents/privacy-lgpd-engineering-expert.md`), the references and the script output. **There was no blind run by an independent model**: a blind test cannot be run here; treat this evaluation as a self-audit.

## 4. Fidelity: what is `[from source]`, `[inference]` and `[extrapolation]`
- Every `[from source]` in `references/` was written from reading the cited page; the citations "(LGPD Art. N ... p.M)" were automatically checked for the article/page pair.
- **Explicit and relevant `[inference]` items**: the literal reading that the list in Art. 11, II repeats neither legitimate interest nor credit protection (p.6 vs p.4); "privacy by design" as the name for the idea in Art. 46 §2º; the fields of the record (Art. 37 does not list them); the structure of the RIPD beyond Art. 38 sole paragraph; risk scales; the whole LGPD-NIST map beyond the Fig. 8 alignment; the link between revocation of consent and manageability (M18).
- **LGPD-NIST map (33 rows)**: 16 TEXTUAL, 11 INFERENCE, 6 NO_SUPPORT. TEXTUAL requires: NIST links the concept to an objective (Fig. 8, 3.1.1.x, glossary) and equivalent terms verified on the pages on both sides. Even so, the correspondence is the agent's (neither source cites the other) and the agent's text says so.
- **`[extrapolation]`**: ANPD resolutions (numbers cited only in `extrapolacoes-e-datado.md`, which itself warns that they were **not verified in this session**), GDPR, PRAM, Privacy Framework, SP 800-53 Rev. 5, ECA digital (the Brazilian digital children's statute), anonymization techniques, technical controls.
- **`[DATED]`**: NIST from 2017; validity of the law (the PDF incorporates amendments up to Lei 15.352/2026 and **was not compared with the official website**); regulations.

## 5. Points of attention and known limitations
- The LGPD in the PDF has "(Vigência)" markings and 2026 wordings that the author could not check outside the file; the agent says to confirm the current wording and consult a lawyer.
- The compiled text shows Art. 5º, VIII (encarregado) in the wording of Lei 15.352/2026 ("indicada pelo controlador e operador", verbatim source text) while Art. 41, caput still assigns the appointment to the controller; the reference records this and marks "check".
- NIST IR 8062 is introductory and from 2017; the agent must not present it as a complete method (it has no scales, PRAM or controls).
- The scripts are deterministic, stdlib-only, with no network; `privacy_lookup.py` uses a simple lexical ranking (ambiguous queries may bring low-relevance entries at the end of the list); the original text is not embedded, only paraphrased summaries and pages.
- Copyright: paraphrased content; no long literal quotation.
- Pending item that depends on the user: blind run by another model (not performed) and legal review of the intended use.
