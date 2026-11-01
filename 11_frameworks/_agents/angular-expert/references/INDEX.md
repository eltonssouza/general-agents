# INDEX — angular-expert (overview based on doc-capture)

## 1. What the sources are (honest identification)

The five PDFs are **not books nor the complete Angular documentation**: they are **PDF captures of the "What is Angular?" page (Overview)** of the documentation site, each with the version label from the page menu (v18, v19, v20, v21, v22). Each capture is short, repetitive and contains interface noise (cookie banner on every page, menus, links without text). The useful content is only the overview: what Angular is, the high-level features and the community.

| Acronym | PDF (folder `14_frameworks`) | Pages | Label on the page | Footer (copyright) | Build stamp | Useless pages |
|---|---|---|---|---|---|---|
| NG18 | `Angular-18-Overview.pdf` | 6 | v18 | 2010-2024 | none | none (p.6 is only footer/links) |
| NG19 | `Angular-19-Overview.pdf` | 7 | v19 | 2010-2025 | none | **p.1** (only cookies and navigation) |
| NG20 | `Angular-20-Overview.pdf` | 7 | v20 | 2010-2025 | none | **p.7** (only a copyright line) |
| NG21 | `Angular-21-Overview.pdf` | 9 | v21 | 2010-2026 | v21.2.20 (+sha) | **p.9** (only footer) |
| NG22 | `Angular-22-Overview.pdf` | 9 | v22 | 2010-2026 | v22.1.2 (+sha) | **p.9** (only footer) |

- **Dates.** No capture shows a URL or publication date. The metadata of the five PDFs indicates creation on 18/08/2026 (all on the same day): it is the **capture** date, not the versions' dates. [DATED] everything is relative to that moment. Only NG21 and NG22 carry a build stamp (v21.2.20 and v22.1.2); this does **not** say which is the current Angular version.
- **Page convention:** PDF page = marker "=== PAGE N ===" of the extracted text. There is no printed numbering. Citation format: `NG21 p.3`.
- **Reading:** the 38 pages (6+7+7+9+9) were read **in full** in the extracted text. NG18 p.2, NG21 p.2 and NG21 p.3 were **rendered and looked at** (image); other pages were rendered only for a size check, without visual inspection. Result: (a) in NG18 p.2 the `@defer` snippet appears in code style at the start of the sentence "blocks in templates...", and the extracted text leaves it blank at that point (the same gap occurs in the NG19 and NG20 text, and before "runs" in the CLI sentence; that `ng update` is there is [inference], since the link with that name is right below); (b) in NG21 p.2-3 the features are cards with a title, description and "Explore ..." link. There are no diagrams or code blocks beyond that; the NG19, NG20 and NG22 captures had no visual inspection of their own.
- Intermediate notes: `scratch/frameworks/angular-expert/notes/`.

## 2. File map

| File | Content |
|---|---|
| `00-visao-geral.md` | what the captures say about Angular on 1 page; limits of the collection |
| `01-conceitos-por-tema.md` | each concept presented, with pages per version |
| `02-mapa-de-diferencas.md` | what changes between NG18, NG19, NG20, NG21 and NG22 (without concluding "removed") |
| `03-sem-cobertura.md` | topics that no Overview mentions (standalone, zoneless, control flow...) |
| `glossario.md` | terms that appear in the captures |
| `procedimentos.md` | how to answer: compare versions, audit a snippet, checklist |
| `casos-e-antipadroes.md` | typical mistakes when using this collection |

## 3. Scripts (Python 3 stdlib, `python -I`, no network; nothing from the target is executed)

| Script | Purpose |
|---|---|
| `scripts/ng_lookup.py TERM` | topic → pages per version, or NOT COVERED (`--gaps`, `--page V N`, `--versions`) |
| `scripts/ng_diff.py diff --from 18 --to 22` | difference map (`matrix`, `concept ID`, `meta`, `--raw --src DIR`) |
| `scripts/ng_lint.py FILE [--target V]` | static snippet linter; each rule declares its origin (from source / inference / extrapolation) |
| `scripts/ng_checklist.py --version V` | overview concept roadmap per version (`--known`, `--check`) |
| `scripts/ng_build_index.py --src DIR` | regenerates `ng_index.json` from the .txt files (maintenance) |
| `tests/verify_citations.py`, `tests/run_script_tests.py` | citation audit and script tests |

## 4. Origin labels
`[from source]` = read on the cited page. `[inference]` = direct deduction from the text. `[extrapolation]` = knowledge outside the collection, without a page. `[DATED]` = relative to the 18/08/2026 capture and to the version labels.
