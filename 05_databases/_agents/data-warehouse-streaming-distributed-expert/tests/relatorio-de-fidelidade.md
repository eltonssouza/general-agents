# Fidelity report (audit v2): data-warehouse-streaming-distributed-expert

Audit of package v1 against the PDF text, correction and completion. Page convention adopted: **PDF** (`KIMBALL p.N`: printed = N − 3; `STREAM p.N`: PDF = printed). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Sources and inventory
| Abbreviation | File | PDF pages | Status |
|---|---|---|---|
| KIMBALL | `Kimball-Dimensional-Modeling-Techniques.pdf` | 24 (cover p.1, table of contents p.2-3, text p.4-24) | read in full |
| STREAM | `Stream-Processing-Evolution-Survey-arxiv.pdf` (arXiv:2008.00842v2) | 30 (text p.1-27, references p.27-30) | read in full (text p.1-27) |
| HELLAND | `Life-Beyond-Distributed-Transactions.pdf` | 4 | **is a different paper**: the astrophysics paper "HD 30963: A new HgMn star" (arXiv:1609.03542), checked on p.1-4. Source absent from the corpus |

The v1 package README already recorded the anomaly of the Helland file (correct finding, kept), but labeled the Helland content as `[inference]`; the correct label is `[extrapolation]` (external knowledge, not verifiable in the corpus).

## 2. Page convention in v1
It was never declared. The 143 KIMBALL citations in v1 used the **printed** page (1-21) under the caption "24 p." (the PDF count); in the PDF the text starts on p.4, so every citation was shifted by 3 (e.g., multipass SQL cited as p.17, actual: PDF p.20). The 109 STREAM citations used PDF = printed (consistent). No v1 citation fell outside the page range (252 citations in total), which shows that the old "19/19 passed" report could only validate range, not content.

## 3. Automatic audit
| Layer | v2 result |
|---|---|
| `verify_citations.py`: positive checks (terms on the cited page(s)) | 129, 0 failures |
| `verify_citations.py`: negative checks (plausible claims the text does not contain) | 28, 0 failures |
| page-range sweep of all package citations | 375 citations, 0 out of range, 0 Helland citations with a page |
| `audit_tokens.py` (backticked terms against the cited page) | 160 terms checked, 0 failures, 0 near |
| `run_script_tests.py` (scripts + references + prompt) | 42 checks, 0 failures |
| v1 baseline with `audit_tokens.py` (v1_backup, v1 pages) | 11 terms, 8 failures, 1 near (Portuguese/SQL terms with no basis on the page) |

Note: the negative checks catch exactly the wrong attributions of v1 (e.g., `jvm`, `off-heap`, `asynchronous barrier`, `cassandra`, `hdfs`, `session windows`, `1+2+3`, `9999-12-31`, negative keys, surrogate bytes).

## 4. Manual audit (sample of 75 v1 claims)
Full record in `scratch/audit/.../notes/achados-manuais.md`. Classification (one class per claim):

| Class | Count |
|---|---|
| OK (content supported; 3 of them with the printed page instead of the PDF page) | 26 |
| No basis on the cited page | 28 |
| Exaggeration / distortion | 12 |
| Error (contradicts the text) | 3 |
| Wrong page / convention | 2 |
| Relevant omission | 1 |
| Partial (rule correct, citation/origin to be fixed) | 2 |
| Not applicable (Helland, source absent) | 1 |

The sample covers all 13 thematic files, the agent prompt, the 4 scripts and the JSON index. Relevant examples:
1. **RocksDB "off the JVM heap, without GC pauses"** (agent, reference, glossary, script, test case): no basis; the survey only says that LSM-Tree variants (FASTER, RocksDB/LevelDB) are the most used out-of-core structure (STREAM p.13); GC appears only as a stall factor in availability (p.21).
2. **Watermark as a guarantee "no event with timestamp ≤ t will arrive"**: exaggeration; the survey defines low-watermark as probabilistic (STREAM p.7) and attributes the guarantee "all following tuples will be greater" to the heartbeat.
3. **Tumbling/sliding/session taxonomy and "session windows (STREAM p.7-9)"**: no basis; only one example tumbling window (p.6); session does not appear.
4. **"ABS (Asynchronous Barrier Snapshotting)" and "coordinator injects barriers"**: no basis; the survey describes unaligned/aligned Chandy-Lamport (STREAM p.15-16); v1 cited p.17-19.
5. **2PC sink with pre-commit at checkpoint** as a survey solution: no basis; the survey lists five solution categories and cites transactional sinks only as a pessimistic technique (STREAM p.20). v1 also omitted the central distinction **exactly-once on state vs on output** (p.17-18).
6. **Elasticity "without restarting the pipeline, in a few seconds"**: error; the survey says stop-and-restart is very common in modern systems (STREAM p.25).
7. **SCD type 6 "1+2+3=6"**: no basis (external mnemonic), present in the agent, the script and tests; the book describes type 6 as type 1 attributes in a type 2 dimension (KIMBALL p.16). v1 also omitted that type 1 requires recomputing aggregates and that type 3 is little used (p.15).
8. **Surrogate keys "orders of magnitude faster, 4 or 8 bytes", IDs -1/-2, "snowflake with negligible space savings", "snowflake [DATED]"**: no basis; the document says to avoid snowflake for usability and possible performance impact (KIMBALL p.12) and asks for a default row with a surrogate for unknown (p.7).
9. **Author name "Fragkouliss"** (throughout the package) and venue "ACM Computing Surveys": the author is Marios Fragkoulis (the "s" in the PDF is an affiliation mark) and the PDF is the arXiv v2 preprint with no venue.
10. **Procedures with Flink APIs and `state.backend: rocksdb` labeled [from source] (STREAM p.6-20)**: no basis; they became version-dependent `[extrapolation]`.

## 5. What was corrected
- **Pages**: all KIMBALL citations converted to PDF (+3) and checked; convention declared in the prompt, README, AGENTS.md, INDEX (with a page map per section) and scripts.
- **Rewritten**: the 13 thematic files + procedimentos, casos-e-antipadroes, glossary and INDEX: content without basis removed or downgraded to `[inference]`/`[extrapolation]`; added what the book says and v1 omitted (exactly-once on state/on output; five output commit solution categories; aligned/unaligned; Table 1; Tables 3 and 4; the 3-column minimum of type 2; pathstring/bridge; advanced fact and dimension techniques; HA).
- **Agent prompt**: from 75 to 104 lines, with scope/boundary, page convention, labels, decision rules with pages, a table of reference triggers and scripts with real files, response format, epistemic honesty (list of what the book does NOT say), anti prompt-injection and boundary with sibling agents.
- **Scripts**: `scd_type_selector.py` (types 5 and 7 included; invented mnemonic and examples removed; decision tree `[inference]`), `stream_semantics_calc.py` (distinguishes exactly-once on state and on output; no "ABS"; table `[inference]`), `entity_boundary_auditor.py` (all content `[extrapolation]`, no "as Pat Helland teaches"), `analytics_lookup.py` + `analytics_index.json` (correct PDF pages, 40 topics, `not_in_book` list with 23 terms, "NOT COVERED" output).
- **New**: `AGENTS.md` (Codex), `.github/agents/*.agent.md` (Copilot, valid YAML frontmatter), README with installation on the 3 platforms and instructions to reproduce the audit, `tests/verify_citations.py` + `citation-checks.json`, `tests/audit_tokens.py`, `tests/run_script_tests.py`, `plugin.json` v2.0.0.

## 6. Test case results
27 cases (see `casos-de-teste.md`): 11 conceptual, 3 practical, 10 edge case/false premise, 1 out of scope, 2 injection. Execution by the auditor against agent + references + scripts: 27/27 consistent with the expected; `run_script_tests.py` runs 42 automatic checks (16 for scripts, 23 for references, 3 for the prompt) with no failures.

## 7. What was NOT audited or could not be
- **Helland**: no source in the corpus; none of the content could be verified. It is suggested to obtain the correct PDF of the article (ACM Queue, 2007) and create a new set of checks.
- Figures and formulas in the PDFs: survey Fig. 2, 3, 8, 9 and 10 were read only through extracted text and captions; they were not checked visually.
- The survey's bibliographic reference sections (p.27-30) were not audited.
- The manual sample (75 claims) does not cover every sentence of the package; the automatic coverage (129 positive checks) is curated, not exhaustive.
- The test cases were executed by the auditor itself against the package files. **There was no blind run by an independent model** (no model answered the cases without seeing the answer key).

## 8. Pending items
- Obtain the correct Helland PDF and audit the reference `pat-helland-...md`.
- Run a blind battery with an independent model (the 27 cases) and compare with the criteria.
- Optional: visually check the survey figures (Fig. 2 and 8) and the numeric examples (slack, heartbeat).
