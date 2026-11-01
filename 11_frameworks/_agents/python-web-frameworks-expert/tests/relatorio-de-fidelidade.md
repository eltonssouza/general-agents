# Fidelity report: python-web-frameworks-expert

Page convention: **PDF** (`DJT p.N`, `FLT p.N`, `FAPI p.N`). The sources are captures of web pages from 2026-08-18; there is no printed numbering.

## 1. What was read
- **32 pages** (DJT 8, FLT 3, FAPI 21) read in full as extracted text (PyMuPDF), with the marker "=== PAGE N ===".
- **Pages rendered and viewed as images**: FAPI p.4, 5, 6, 7, 8, 12, 13, 14, 18, 19. Findings: empty terminal blocks (p.4-7 and p.19); p.8 without the expected capture; p.12-14 with Swagger UI captures without text; p.18 with an editor capture. DJT and FLT only as text.
- No source code was executed; no framework was installed or run; no network was accessed.

## 2. Citation verification (`tests/verify_citations.py` + `tests/citation-checks.json`)
- **Range**: all `CODE p.N` citations in the package `.md/.py/.json` files fall within 1..8 (DJT), 1..3 (FLT) and 1..21 (FAPI).
- **Positive checks: 94** (key terms present on the cited page) and **negative: 22** (plausible statements the sources do NOT carry, e.g. `pip install django`, `makemigrations`, `create_app`, `render_template`, "microframework", `fastapi deploy`, `--port`, `Depends(`, `APIRouter`, `status_code`, "docker", direct comparison with Django/Flask, versions 1.0/6).
- Result of the last run: **0 failures** (116 checks). Two initial failures were due to whitespace normalization of the extracted text and were fixed in the check, not in the content.
- Limit: the checks cover the central statements, not every sentence of the references; the rest was checked during reading.

## 3. Script tests (`tests/run_script_tests.py`)
- **55 deterministic tests, all passing**, covering: lookup (including NOT COVERED, non-technical pages, JSON), comparator (NOT COVERED in cells, `--only`, `--json`, English criterion aliases, JSON integrity), scaffold (commands only from the sources, rejection of `django`/`test`/path-containing names, refusal to overwrite, Flask = NOT COVERED, generated files pass the linter), linter (positives and negatives per rule, Flask without rules, injection comment ignored, Dockerfile, whole folder, incorrect usage).
- One defect was found and fixed by the tests: the lookup matched "de" and "como" (common words) with topics; a stopword list was added.
- Another adjustment: rule `CMD-RUNSERVER-PROD` did not recognize the Dockerfile list form (`CMD ["python", ...]`); fixed.

## 4. Test cases (`tests/casos-de-teste.md`)
31 cases (conceptual, practical, edge, out of scope, injection). Those with a script were run and pass; the rest were verified **manually by the author** against the prompt, references and script outputs. **There was no blind round by an independent model.**

## 5. Origin of the linter rules
- **[from source]** (ERROR/WARNING): `DJ-PATH-ARGS`, `DJ-INCLUDE`, `DJ-ROUTE-QUERY`, `DJ-VIEW-REQUEST`, `DJ-NAME-MISSING` (INFO), `FA-AWAIT-IN-DEF`, `FA-PATH-UNTYPED`, `FA-OPTIONAL-NODEF`, `CMD-PROJNAME`, `CMD-QUOTE`.
- **[inference]**: `FA-PATH-MISSING`, `FA-BODY-NOT-MODEL`, and the "deployment file" part of `CMD-RUNSERVER-PROD`.
- Flask: no rule (FLT index only); the linter emits INFO NOT COVERED (`FLASK-NOT-COVERED`).
- Limits: the linter is static and heuristic; it does not detect everything and absence of a finding does not prove correctness. `FA-AWAIT-IN-DEF` only applies to functions with a route decorator; `DJ-VIEW-REQUEST` only to functions without decorators that return `HttpResponse` and have no parameters.

## 6. Known limitations and pending items
1. The FLT is only an index: the comparator's Flask column is almost entirely NOT COVERED or "only a section title". This is expected, not a package failure.
2. FAPI: installation (p.4), running (p.6) and deploy (p.19) commands were in empty blocks; only the text excerpts are asserted.
3. Django 5.0 is an unsupported version per the banner; the agent knows nothing of later versions or what changed.
4. The Flask "3.1.x" number comes from the PDF title (metadata), not from the body text; the verifier does not check it (and there is a negative check that the body does not contain it).
5. No map of changes between versions was built: there is one version per framework.
