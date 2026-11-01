# INDEX: python-web-frameworks-expert

Package **proportional to three captures of web pages** (official documentation). Read §1 and §2 before citing anything: two of the three sources are short, and the Flask one is only an index.

## 1. Sources (identification verified in the text and in the PDF metadata)

| Abbrev. | File | What it really is | Pages | Version / date | Usefulness |
|---|---|---|---|---|---|
| **DJT** | `Django-Tutorial01-Docs.pdf` | Capture of the **"Writing your first Django app, part 1"** page of the Django documentation, **version 5.0** (footer "Documentation version: 5.0"). A banner at the top warns that it is an insecure, unsupported version (DJT p.1). | 8 | Tutorial for Django 5.0, Python 3.10+ (DJT p.1). Example server output dated "April 02, 2025" (DJT p.2). Footer "© 2005-2026" (DJT p.8). PDF generated on 2026-08-18 (metadata). | **Medium**: p.1-5 are useful content (project, runserver, app, view, URLconf, include, path). **p.6-8 are sponsors, navigation links and footer: no technical content.** |
| **FLT** | `Flask-Tutorial-Docs.pdf` | Capture of the **start page of the "Tutorial"** of the Flask documentation ("stable" brand; the PDF title, in the metadata, says "Flask Documentation (3.1.x)"). **It is only an introduction and a list of sections: there is no code, no command and no section content.** | 3 | Flask 3.1.x [metadata datum, not from the body text]. PDF generated on 2026-08-18. | **Low**: goal of the tutorial (Flaskr blog), the titles of the 11 sections, prerequisites and the "Flask is flexible" philosophy. |
| **FAPI** | `FastAPI-Docs-Overview.pdf` | Capture of the **start page of the FastAPI documentation** (overview): features, installation, minimal example, example with Pydantic body, automatic docs, recap, dependencies, deploy, license. | 21 | Badge **v0.141.1**, Python 3.10 to 3.14 (FAPI p.1). Cites a mini-documentary "from late 2025" (FAPI p.3). PDF generated on 2026-08-18. | **Medium-high** for an overview. **Capture defects:** the terminal (bash) blocks on p.4, 5, 7 and 19 came out **empty** (only the "bash" label or a dark box), so the install, run and deploy commands **are not legible in those blocks** (only what the surrounding text cites). Screenshots exist (p.12-14: Swagger UI of `PUT /items/{item_id}` with "Try it out"/"Execute"; p.18: editor with autocomplete) but p.8 came out blank where the Swagger screenshot should be. |

Metadata convention: the three PDFs were printed from a browser (headless Chrome, Skia/PDF) on 2026-08-18. Relative dates ("[DATED]") hold **as of that capture**, without asserting what changed afterwards.

## 2. Page convention
- Always cite the **PDF page** (`DJT p.N`, `FLT p.N`, `FAPI p.N`). The sources are printed web pages: **there is no printed numbering**; the page number is only the order of the PDF sheets.
- Page breaks fall in the middle of sentences and code (e.g., `polls/urls.py` starts on DJT p.3 and the code is on p.4; the `Item` example starts on FAPI p.10 and the code is on p.11). The citation verifier handles this by citing the page where the term actually appears.
- Pages without technical content: **DJT p.6, 7, 8** (sponsors, navigation, footer) and **FAPI p.3** (silver sponsors, testimonial). `scripts/fw_lookup.py --page N --source S` reports this.

## 3. What was read (precise statement)
- **In full** (text extracted from the 8 + 3 + 21 pp. = 32 pp.): DJT, FLT and FAPI.
- **Rendered and viewed as an image** (to check what the text did not capture): FAPI p.4, 5, 6, 7, 8, 12, 13, 14, 18, 19. Result: empty terminal blocks on p.4, 5, 6, 7 and 19; p.8 without the expected screenshot; p.12-14 show Swagger UI screenshots with the PUT operation (required integer path parameter `item_id`, required `application/json` body, Try it out/Execute buttons, 200 response and a curl command); p.18 shows the editor suggesting `price` when typing `item.pr`. The interface version in the screenshots cannot be identified: use them only as illustration, without attributing version v0.141.1 to them. DJT and FLT were read only as text (the pages have only text and code).
- No code from the sources was executed; no framework was installed or run.
- Reading notes: `scratch/frameworks/python-web-frameworks-expert/notes/` and images in `notes/render/`.
- There was **no** validation by an independent "blind" model; the tests were run by the package's own author (see `tests/relatorio-de-fidelidade.md`).

## 4. References by topic

| File | Content | Source/pages |
|---|---|---|
| `00-fontes-e-lacunas.md` | Nature of the sources, gaps, capture defects, divergences | all |
| `dj-01-projeto-e-servidor.md` | Version notice, create project, layout, runserver | DJT p.1-2 |
| `dj-02-app-view-urlconf.md` | `polls` app, view, URLconf, `include()`, arguments of `path()` | DJT p.3-5 |
| `flt-01-indice-e-intro.md` | Goal of the Flaskr tutorial, section index (titles only), flexibility | FLT p.1-3 |
| `fapi-01-visao-instalacao-exemplo.md` | Features, requirements, installation, example, `async def`, `fastapi dev` | FAPI p.1-7 |
| `fapi-02-tipos-validacao-docs.md` | Typed parameters, Pydantic body, `/docs` and `/redoc`, recap, user-guide spoiler | FAPI p.8-19 |
| `fapi-03-deps-deploy-desempenho.md` | FastAPI Cloud, performance, `standard` dependencies, license | FAPI p.19-21 |
| `glossario.md`, `procedimentos.md`, `casos-e-antipadroes.md`, `datado.md` | terms, recipes, cases, dated items | all |

## 5. Scripts (Python 3, stdlib, no network; they never run the frameworks)
`scripts/fw_lookup.py` (search + NOT COVERED), `scripts/compare_frameworks.py` (DJT x FLT x FAPI comparator), `scripts/scaffold.py` (command outline and skeletons that the sources show), `scripts/snippet_lint.py` (static linter for snippets and commands). Indexes: `scripts/fw_index.json`, `scripts/compare_data.json`.

## 6. Boundary with other agents
- REST in general (API design, versioning, status codes): **web-api-rest-architecture-expert** (`ROOT\06_web_and_frontend\_agents\`).
- Python as a language (type hints, async, virtual environments, packaging): **python-expert** (`ROOT\01_programming_languages\_agents\`).
- These sources show, of Python, only what appears in the examples; nothing beyond that is asserted here.
