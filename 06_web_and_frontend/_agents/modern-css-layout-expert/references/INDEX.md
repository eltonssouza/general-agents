# Reference Index: Modern CSS Layout Expert

Lookup collection of the **modern-css-layout-expert** agent. Open only the file the topic requires.

## 1. Sources and acronyms

| Acronym | Work | Note |
|---|---|---|
| **CSSHB** | *The CSS Handbook: A Handy Guide to CSS for Developers*, Flavio Copes, freeCodeCamp, 04/24/2019, 214 pages | Real content source. 2019 edition: part of the content is dated. |
| **MDNFS** | MDN, *Core learning modules: CSS styling basics*, 4 pages | Index page: lesson titles and descriptions. |
| **MDNL** | MDN, *Core learning modules: CSS layout*, 3 pages | Index page: lesson titles and descriptions. |

Page numbering = PDF page number ("=== PAGE N ===" markers of the extracted text).

## 2. Citation conventions and labels

- `[from source] (CSSHB p.N)` or `(CSSHB p.N-M)`; MDN indexes: `(MDNFS p.N)`, `(MDNL p.N)`.
- `[inference]`: direct deduction from what the material says (includes caveats about errors in the text).
- `[extrapolation]`: modern CSS outside the collection; no page.
- `[DATED]`: 2019 content that has changed.

## 3. Topic map

| File | When to open | Source pages |
|---|---|---|
| [cascata-especificidade-e-heranca.md](cascata-especificidade-e-heranca.md) | style does not apply, which rule wins, `!important`, inheritance, `@import` | CSSHB p.19-30; MDNFS p.3 |
| [seletores-pseudoclasses-e-pseudoelementos.md](seletores-pseudoclasses-e-pseudoelementos.md) | selectors, combinators, attributes, pseudo-classes/elements | CSSHB p.5-19, 30-36, 58-59 |
| [box-model-borda-padding-margin-e-box-sizing.md](box-model-borda-padding-margin-e-box-sizing.md) | box size, border, spacing, `box-sizing` | CSSHB p.83-99 |
| [unidades-cores-url-e-calc.md](unidades-cores-url-e-calc.md) | px/rem/em/vw/fr, colors, `calc()`, `url()` | CSSHB p.36-50 |
| [backgrounds-e-filtros.md](backgrounds-e-filtros.md) | backgrounds and `filter` | CSSHB p.50-54, 174-182 |
| [display-fluxo-posicionamento-float-e-z-index.md](display-fluxo-posicionamento-float-e-z-index.md) | `display`, `position`, float/clear, `z-index` | CSSHB p.99-123 |
| [flexbox.md](flexbox.md) | one-dimensional layout | CSSHB p.141-156 |
| [grid.md](grid.md) | two-dimensional layout | CSSHB p.123-141 |
| [centralizacao-tabelas-e-listas.md](centralizacao-tabelas-e-listas.md) | centering, tables, lists | CSSHB p.156-168 |
| [responsividade-media-queries-e-feature-queries.md](responsividade-media-queries-e-feature-queries.md) | `@media`, `@supports`, RWD | CSSHB p.141, 168-174; MDNL p.2-3 |
| [tipografia-e-fontes.md](tipografia-e-fontes.md) | fonts, `@font-face`, text properties | CSSHB p.63-83 |
| [transforms-transicoes-e-animacoes.md](transforms-transicoes-e-animacoes.md) | `transform`, `transition`, `animation` | CSSHB p.182-204 |
| [custom-properties-variaveis-css.md](custom-properties-variaveis-css.md) | `--var`, `var()`, scope, JS | CSSHB p.55-63 |
| [compatibilidade-impressao-e-tratamento-de-erros.md](compatibilidade-impressao-e-tratamento-de-erros.md) | syntax errors, prefixes, normalize, print | CSSHB p.8-10, 204-213 |
| [mdn-modulos-e-lacunas-do-material.md](mdn-modulos-e-lacunas-do-material.md) | what the collection covers/does not cover, dated data, errors in the text | MDNFS p.1-4; MDNL p.1-3; CSSHB |
| [procedimentos.md](procedimentos.md) | procedures P1 to P10 | CSSHB (various) |
| [casos-e-antipadroes.md](casos-e-antipadroes.md) | pitfalls and solved recipes | CSSHB (various) |
| [glossario.md](glossario.md) | definitions | CSSHB, MDNFS, MDNL |

## 4. Scripts (folder `../scripts/`)

| Script | Function |
|---|---|
| `css_lookup.py` + `css_index.json` | topic/property and page lookup; warns "NOT COVERED" |
| `css_lint.py` (`lint`, `spec`) | static linter and specificity |
| `css_calc.py` (`units`, `box`, `flex`, `grid`) | calculations |

## 5. Summary of limits

- No container queries, subgrid, `clamp()`, `auto-fit`, `@layer`, `:is/:where/:has`, nesting, `prefers-*`, `dvh`, accessibility, or rendering performance.
- Tables and lists illustrated in the original PDF (pseudo-classes, pseudo-elements, transition/animation properties, Flexbox figures) are not in the extracted text.
- The MDN PDFs are indexes; they do not replace the lessons.
