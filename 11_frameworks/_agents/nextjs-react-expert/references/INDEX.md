# INDEX — nextjs-react-expert

Agent providing an **overview based on documentation captures** (4 release posts + 2 old handbooks). It is not a complete manual for Next.js or React.

## 1. What each PDF really is

| Acronym | PDF (`14_frameworks/`) | Type and date | Pages | Useful content | Useless pages |
|---|---|---|---|---|---|
| NX13 | NextJS-13-Release.pdf | nextjs.org blog post, **2022-10-25** | 16 | p.1-15 | p.16 footer; contributor names on p.15-16 |
| NX14 | NextJS-14-Release.pdf | Blog post, **2023-10-26** | 13 | p.1-9 | p.10-13 contributors and footer |
| NX15 | NextJS-15-Release.pdf | Blog post, **2024-10-21** | 22 | p.1-19 | p.20-22 contributors and footer |
| NX16 | NextJS-16-Release.pdf | Blog post, **2025-10-21** | 16 | p.1-14 | p.15-16 footer and contributors |
| NXHB | NextJS-Handbook-freeCodeCamp.pdf | freeCodeCamp handbook (Flavio Copes), **2019-11-19**, Next 9.1.2 — **[DATED]** | 91 | p.3-91 | many screenshot-only pages (e.g. 9-11, 36, 40, 55) |
| RCTHB | React-Handbook-freeCodeCamp.pdf | freeCodeCamp handbook (Flavio Copes), **2020-11-13**, create-react-app — **[DATED]** | 35 | p.2-34 | p.7-10 screenshot only |

Native text (no OCR) in all of them; no PDF is 404/empty. The "© 2026 Vercel, Inc." footers of the releases indicate capture in 2026. In the release captures, terminal blocks appear out of order (see `01..04-*-mapa.md`).

## 2. Page convention
**PDF page** ("=== PAGE N ===" of the extracted text). The 6 PDFs have no printed number; there is no offset map. Citations: `NX15 p.3`, `NXHB p.58-60`.

## 3. Reading coverage (honest)
- **Read in full:** all pages of the 6 extracted texts (16+13+22+16+91+35 = 193 pages), in sequential blocks, with notes on disk.
- **Checked visually (render):** NXHB p.8 (package.json is an image) and p.75 (build output). No release diagram was left without an equivalent text; the missing figures are terminal/browser screenshots in the handbooks.
- **Not run:** no code from the sources was executed.

## 4. File map
| File | Contents |
|---|---|
| 01-next13-mapa.md | NX13 change map (new features, requirements, breaking changes, upgrade) |
| 02-next14-mapa.md | same for NX14 |
| 03-next15-mapa.md | same for NX15 |
| 04-next16-mapa.md | same for NX16 (removals, behavior and deprecations tables) |
| 05-trajetorias-e-requisitos.md | Requirements table (Node/React/TS/browsers) and trajectories by topic NX13→NX16; what the posts do NOT say |
| 06-nextjs-handbook-datado.md | NXHB [DATED], by section, with pages |
| 07-react-handbook-datado.md | RCTHB [DATED], by section, with pages |
| 08-conflitos-datado-vs-releases.md | 17 conflicts/evolutions/silences, pages on both sides |
| 09-sem-cobertura.md | Gaps in the collection |
| glossario.md / procedimentos.md / casos-e-antipadroes.md / datado.md | Cross-cutting |

## 5. Triggers
| Question | Open / run |
|---|---|
| "What changed from Next X to Y?" | `scripts/nx_changes.py changes --from X --to Y` + `05-trajetorias...` |
| "Upgrade checklist" | `scripts/nx_changes.py upgrade --from X --to Y` |
| "What is the minimum Node/React?" | `nx_changes.py requirements` |
| "Review this snippet/config" | `scripts/nx_lint.py PATH --target N` |
| "Where does the book/post talk about X?" | `scripts/nx_lookup.py X` |
| "Is the 2019 handbook still valid?" | `nx_lookup.py --conflicts` + `08-conflitos...` |
| "What is Server Action / use cache / proxy.ts?" | `glossario.md` + the version map |

## 6. Versions
Everything about Next versions comes **only from the text of the posts**. The model's prior knowledge about Next 13-16 (or later) **does not count** as a source.
