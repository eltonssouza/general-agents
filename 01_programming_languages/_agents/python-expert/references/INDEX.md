# Reference index — python-expert

Load **only** the file you need. Every claim cites `(Tut p.N)`, `(Ref p.N)`, `(Notes p.N)` or `(Lib p.N)`, with the **PDF** page (the books' printed numbering is different; exact map in the "Page convention" section below).

| Abbrev. | Work | Nature | Caution |
|---|---|---|---|
| Tut | *The Python Tutorial* 3.14.0rc3 | **official**, distilled text | it is a **release candidate** (Oct/2025); it hardly marks versions; some examples (pip/venv) are old |
| Ref | *The Python Language Reference* 3.14.0rc3 | **official**, distilled text | release candidate; **marks** the version of several features; p.169–225 are glossary, appendices and index |
| Notes | *Python Notes for Professionals* (GoalKicker) | **community**, 588 of the 813 pages cited (measured in the audit) | mixes Python 2 and 3, has errors and unsafe examples; 58 of the 202 chapters have no citation at all (list below) |
| Lib | *The Python Library Reference* 3.14.0rc3 | official, **INDEX ONLY** (bookmarks) | **there is no distilled content**: the index only says which PDF page to read |

**Golden rule:** the **official** source prevails. The Notes only complement and always come labeled **[community]**; before repeating anything from them, check `fontes-comunitarias.md`.

## When to open each file

| I need… | Open | Size |
|---|---|---|
| What a term means (hashable, descriptor, GIL…) | [glossario.md](glossario.md) | ~4.5k words |
| Choosing between approaches (data structure, copying, exceptions, classes, concurrency) | [frameworks.md](frameworks.md) | ~8k |
| Step by step and checklists by area (includes the Ref "Review checklist") | [procedimentos.md](procedimentos.md) | ~5.6k |
| Pitfalls, error messages, anti-patterns, unsafe examples from the book | [casos-e-antipadroes.md](casos-e-antipadroes.md) | ~7.5k |
| Fine language rules: data model, scope, import, expressions, statements | [regras-da-linguagem.md](regras-da-linguagem.md) | ~7.3k |
| In which version X appeared; what stays "unmarked"; Python 2 vs 3; dated content | [versoes-e-datado.md](versoes-e-datado.md) | ~6.3k |
| Whether I can trust a claim from the Notes; examples NOT to recommend | [fontes-comunitarias.md](fontes-comunitarias.md) | ~6k |
| Which standard library module and which PDF page to read | [stdlib-indice.md](stdlib-indice.md) or the `python-stdlib-lookup` skill | index |

## Shortcuts by question

- "Which version brought X?" → `versoes-e-datado.md` §1 (marks) and §2 (unmarked); skill `python-version-features`.
- "Which module do I use for…?" → skill `python-stdlib-lookup` (returns PDF pages). The index does **not** explain the API.
- "Is what the book shows safe/correct?" → `fontes-comunitarias.md` (§3 suspicions, §4 security, §5 clear errors).
- "I got this error / traceback" → `casos-e-antipadroes.md` (Part 1) and skill `python-error-triage`.
- "Convert Python 2 code" → `versoes-e-datado.md` §3 and skill `python-py2-to-py3`.
- "Review this code" → `procedimentos.md` §20 and skill `python-code-review`.
- "`is` vs `==`, `__eq__`/`__hash__`, scope, descriptors" → `regras-da-linguagem.md`.

## How to read large files

The files exceed the single-read limit. List the sections with `Grep` (pattern `^#{2,3} `, with `-n`), pick the section and read only it with `Read` (`offset`/`limit`). Very long table lines come out truncated in Grep: use `Read` by offset. For a term, run `Grep` over **all** the files before concluding that something is not covered.

## Marking conventions

- **[official]** / **[community]**: origin of the claim (Tut/Ref vs Notes).
- **[DATED]**: Python 2 or a superseded practice.
- **[DIVERGES]**: Notes and the official source diverge; the official one prevails.
- **[inference]**: a link made during consolidation, not stated by the source.
- **[extrapolation]**: knowledge outside the sources (must be labeled and avoided as fact).
- **"version not stated in the text"**: the feature appears, but the source does not say since when it exists.
- **[to confirm in the official docs]**: a suspicion about a claim in the Notes, coming from the distiller's knowledge, not from the source text.

## Page convention (PDF × printed map)

Throughout the package `(Tut|Ref|Notes|Lib p.N)` is the **PDF** page (the `=== PAGE N ===` marker of the extracted text). Measured over all the numbered pages of the PDFs (`tests/verify_citations.py`):

| Abbrev. | PDF = printed + | PDF pages | Note |
|---|---|---|---|
| Tut | 6 | 167 | p.1–8 cover and table of contents; chapters 1–16 up to p.122; glossary from p.123 |
| Ref | 8 | 225 | p.169–225: glossary (p.169), licenses (p.189) and index (p.211; uses the **printed** numbering) |
| Notes | 25 | 813 | the printed number is at the **top** of the page; p.1–26 are cover and table of contents |
| Lib | 26 | 2,488 | index only (bookmarks); from p.2,313 on: glossary, licenses, bibliography and indexes (Index from p.2,361) |

For the Tutorials 3.10–3.13 (term presence only) the difference is also 6 (`tutorial_index.json`). Example: Ref p.26 (t-strings) is printed p.18. Citations with a **long range** (≥ 10 pages, e.g. `Notes p.621–646`) are section pointers, not claims about one page; the agent must cite the exact page when answering. Tolerance of ±1 page: the automatic audit accepts (and lists as PROXIMA) a term that is on the neighboring page because of a page break; the 36 initial occurrences were reviewed one by one, 10 were page errors and were fixed, and the remaining 24 are page breaks (term on the neighboring page).

## Measured coverage of the Notes (gaps)

Of the 813 pages, the package cites 588. The 58 chapters (of 202) with **no cited page at all** (measured; the earlier figure, "37 chapters left out", was not verifiable): 10 Bitwise Operators (p.86–89); 12 Operator Precedence (p.93); 18 Multidimensional arrays (p.126–127); 22 List slicing (selecting parts of (p.163–164); 27 Heapq (p.176–177); 42 Using loops within functions (p.269); 46 Complex math (p.286–287); 52 The locale Module (p.305); 58 The base64 Module (p.328–332); 61 Webbrowser Module (p.336–337); 62 tkinter (p.338–340); 63 pyautogui module (p.341); 65 Plotting with Matplotlib (p.346–353); 66 graph-tool (p.354–355); 93 Web scraping with Python (p.465–468); 94 HTML Parsing (p.469–470); 95 Manipulating XML (p.471–473); 96 Python Requests Post (p.474–478); 101 Method Overriding (p.493); 102 User-Deﬁned Methods (p.494–495); 107 PyInstaller - Distributing (p.507–508); 108 Data Visualization with (p.509–515); 122 Websockets (p.556–558); 123 Sockets And Message (p.559–562); 126 Flask (p.570–574); 127 Introduction to RabbitMQ (p.575–578); 129 tempﬁle (p.581); 130 Input, Subset and Output (p.582–583); 137 Deployment (p.593–594); 139 Web Server Gateway (p.599); 146 ArcPy (p.614); 149 Immutable datatypes(int, (p.620); 153 Abstract syntax tree (p.651–652); 156 Python Serial Communication (p.657–658); 157 Neo4j and Cypher using (p.659–660); 158 Basic Curses with Python (p.661); 159 Templates in python (p.662); 160 Pillow (p.663); 161 The pass statement (p.664); 164 Connecting Python to SQL (p.679); 165 PostgreSQL (p.680); 166 Python and Excel (p.681–685); 167 Turtle Graphics (p.686); 171 Creating a Windows service (p.696–697); 174 Optical Character (p.703–704); 178 Create virtual environment (p.717); 180 ChemPy - python package (p.719–721); 181 pygame (p.722–723); 182 Pyglet (p.724–725); 183 Audio (p.726–727); 184 pyaudio (p.728–730); 186 IoT Programming with Python (p.734–736); 187 kivy - Cross-platform Python (p.737–738); 188 Pandas Transform: Preform (p.739–740); 189 Similarities in syntax, (p.741); 190 Call Python from C# (p.742–743); 192 Python Lex-Yacc (p.748–756); 202 Hidden Features (p.799; p.800–813 are credits and ads). For any of them the answer is "the package does not cover it" (or direct reading of the PDF), not memory.

## Tutorials 3.10–3.13 and "version"

The PDFs `Python-3.10-Tutorial`, `3.11`, `3.12` and `3.13` exist in the PDF folder, but were **not distilled**. The package uses them only as a presence index for 47 terms (`skills/python-version-features/scripts/tutorial_versions.py`). Presence in the Tutorial is **not** a version mark (e.g. `@dataclass` only appears in the Tutorial body from 3.12 on, although the feature is older); any "introduced in X" derived from this is **[inference]**.

## Labels and [from source]

In the references, every sentence with a `(Tut|Ref p.N)` citation is **[official]** and with `(Notes p.N)` is **[community]**, and equals **[from source]** for the cited page; what the page does not say is marked **[inference]**, **[extrapolation]**, **[DATED]** or **[to confirm in the official docs]**. In the tables of `casos-e-antipadroes.md`, the correction column ("Do this instead") mixes what the book shows and the package's recommendation: it only counts as from the source when the source column confirms; the rest is **[inference]**.

## Reading cautions

- The text came from PDF: code indentation and some REPL outputs were lost.
- The index of the official books has numbers glued together by extraction error ("2527", "162165"): do not use them literally.
- The official documentation is a **release candidate**: the final 3.14 behavior may differ. There is no 3.15 documentation nor "What's New" in the sources.
- Free-threading: Tut p.130 says that, since 3.13, the GIL can be disabled with the build option `--disable-gil` and that the code runs with `-X gil=0` or `PYTHON_GIL=0`; the glossary (Tut p.124, 132) and the Lib (p.876, 1018, 2049, indexed only) mention "free-threaded builds". The text read **does not say** that the free-threaded build is the 3.14 default: do not assert it.
- The sources do not say whether `2to3` exists in 3.14 (the Lib index does not list it): do not assert availability.
