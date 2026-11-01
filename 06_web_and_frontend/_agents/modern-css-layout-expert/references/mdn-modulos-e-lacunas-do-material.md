# MDN Material (Indexes) and Collection Gaps

This file exists so the agent knows **exactly what the three sources cover and what they do not**. No gap may be filled from memory without an `[extrapolation]` label.

## 1. What the two MDN PDFs are

Both are index pages of MDN learning modules, not the articles themselves. They give the title and description of each lesson; there is no code, tables or operational rules.

### MDN First Steps (CSS styling basics), 4 pages [MDNFS]

| Lesson (title) | Summary of the description | Page |
|---|---|---|
| What is CSS? / Getting started with CSS | what CSS is, syntax and how the browser applies CSS to HTML | MDNFS p.1 |
| Basic CSS selectors / Attribute selectors | type, class and id selectors; attribute selectors | MDNFS p.1 |
| Pseudo-classes and pseudo-elements; Combinators | selection by state/part; selection by relative position in the DOM (child, sibling) | MDNFS p.2 |
| The box model | everything has a box; key to layouts and alignments | MDNFS p.2 |
| Handling conflicts | cascade, specificity and inheritance; conflict resolution | MDNFS p.2 |
| Values and units; Sizing items in CSS | value types; ways of sizing | MDNFS p.2 |
| Backgrounds and borders | gradients, images, rounded corners | MDNFS p.2 |
| Overflowing content | overflow = content larger than the box | MDNFS p.2-3 |
| Images, media, and form elements | special elements are styled differently | MDNFS p.3 |
| Styling tables | techniques for HTML tables | MDNFS p.3 |
| Debugging CSS | using DevTools to debug | MDNFS p.3 |
| Advanced styling effects (optional) | shadows, blend modes, filters | MDNFS p.3 |
| Cascade layers (optional) | advanced feature on the cascade and specificity | MDNFS p.3 |
| Handling different text directions (optional) | writing modes (RTL, vertical) | MDNFS p.3 |
| Organizing CSS (optional) | maintainability of large stylesheets | MDNFS p.3 |
| Challenges (biography, blog, dashboard) | practical exercises | MDNFS p.1-2 |

Declared prerequisites: basic environment, notions of files and HTML [from source] (MDNFS p.1).

### MDN Layout (CSS layout), 3 pages [MDNL]

| Lesson | Summary | Page |
|---|---|---|
| Introduction to CSS layout | `display` values and normal flow | MDNL p.1 |
| Floats | returned to its original purpose with flexbox/grid | MDNL p.1 |
| Positioning | taking elements out of the flow; `position` values | MDNL p.1 |
| Flexbox | 1D method; items grow and shrink | MDNL p.1 |
| CSS grid layout | 2D system of rows and columns | MDNL p.1-2 |
| Fundamental layout comprehension (challenge) | flexbox, floats, grid, positioning combined | MDNL p.2 |
| Responsive design; Media query fundamentals | RWD and media queries | MDNL p.2 |
| Multiple-column layout; Practical positioning examples | newspaper-style columns; real examples | MDNL p.2 |
| Legacy layout methods | float-based grid systems in old projects | MDNL p.2 |
| Supporting older browsers | degrading for old technologies | MDNL p.2-3 |
| CSS layout cookbook (see also) | recipes for common layout patterns | MDNL p.3 |

Prerequisites: HTML, CSS fundamentals, text styling [from source] (MDNL p.1). "Learn Flexbox/Learn CSS Grid" are partner courses (Scrimba), cited as "see also" [from source] (MDNL p.3).

## 2. Topic -> source map with real content

| Topic | Real content | MDN index only |
|---|---|---|
| Cascade/specificity/inheritance | CSSHB p.19-29 | MDNFS p.2-3 |
| Selectors | CSSHB p.12-19, 30-36 | MDNFS p.1-2 |
| Box model | CSSHB p.83-99 | MDNFS p.2 |
| Flexbox | CSSHB p.141-156 | MDNL p.1 |
| Grid | CSSHB p.123-141 | MDNL p.1-2 |
| Positioning/float | CSSHB p.102-123 | MDNL p.1-2 |
| Media queries | CSSHB p.168-174 | MDNL p.2 |
| Typography | CSSHB p.63-83 | MDNFS p.3 (text directions) |

## 3. Collection gaps (confirmed by searching the extracted text)

The Handbook (April/2019) has zero occurrences of: `clamp`, `subgrid`, `@container`/container queries, `@layer`, `:is()`, `:where()`, `:has()`, `:not()`, `focus-visible`, nesting, `auto-fit`/`auto-fill`, `dvh`, `prefers-*` (color-scheme, reduced-motion), `aspect-ratio` as a property (it appears only as a media descriptor), `object-fit`, `backdrop-filter`, `scroll-snap`, `will-change`, `min-content`/`max-content`, `@property`, `oklch`, "mobile", "accessibility". It has a single mention of the word "layer" (unrelated) and few of `overflow` (only `overflow-wrap`).

Consequences:
1. Accessibility (contrast, focus, reduced motion) is not a topic of the book; the agent treats it as `[extrapolation]` and routes it to an accessibility specialist, if one exists in the repository.
2. Modern intrinsic layout (grid with `auto-fit`, `minmax`, `clamp`, container queries) is `[extrapolation]`.
3. CSS/rendering performance: route to the `web-performance-networking-expert` agent (HPBN book).

## 4. Dated content in the Handbook (matrix)

| Passage | Why dated | Page |
|---|---|---|
| Support statistics (Flexbox 97.66% in Feb/2018; Grid 92% in Apr/2019) | numbers age | CSSHB p.124, 142 |
| `position: sticky` "poorly supported" | wide support today | CSSHB p.113 |
| `grid-gap`, `grid-column-gap`, `grid-row-gap` | current names without the `grid-` prefix (`gap`) | CSSHB p.129-131 |
| `device-width` etc. in media features | obsolete in later specifications | CSSHB p.169-170 |
| `page-break-*` | replaced by `break-*` | CSSHB p.211-212 |
| Vendor prefixes and their lists | decline and 2019 data | CSSHB p.206-208 |
| IE (hacks, box model, "IE10+ covered") | end of IE support | CSSHB p.10, 124, 142 |
| Short hex "not supported by all" | wide support today | CSSHB p.44 |
| Fonts only from the same origin | simplification; CORS | CSSHB p.72 |
| `filter: opacity()` preferable to `opacity` for hardware | implementation-dependent opinion | CSSHB p.177 |
| `z-index` only with non-static position | flex/grid items also respect it | CSSHB p.122 |
| List of inherited / animatable properties | 2019 lists | CSSHB p.26-28, 189-204 |
| Normalize.css as "most common" | the ecosystem changed | CSSHB p.205 |
| `blink` in `text-decoration` | practically obsolete feature | CSSHB p.74 |

## 5. Errors and imprecisions in the text itself (flag, do not propagate)

| Passage | Problem | Page |
|---|---|---|
| `font-weight` "sets the width" | describes weight, not width | CSSHB p.67 |
| `sans-serif` "without ligatures" / `serif` "with ligatures" | confuses serifs with ligatures | CSSHB p.66 |
| `-moz-` listed as Safari | it is Firefox | CSSHB p.207 |
| `<link ... src="print.css">` | correct attribute: `href` | CSSHB p.209 |
| `color: $primary` in CSS | Sass variable invalid in plain CSS | CSSHB p.210-211 |
| `filter: saturate();` without an argument | incomplete example | CSSHB p.182 |
| `ul:nth-child(odd)` to stripe rows | should target `li` | CSSHB p.34 |
| `.3Delement` as a selector | invalid name without escaping | CSSHB p.184 |
| Declaration `--width` directly in `@media` | needs a selector | CSSHB p.62-63 |
| Description of `initial` | imprecise | CSSHB p.29 |
| `inline` "without margin/padding" | simplification | CSSHB p.100-101 |

These caveats are `[inference]` of the agent (checked against the text of the book itself and general CSS knowledge), not statements by the author.

## 6. Figures/tables not extracted

Popular pseudo-classes (p.32-33), list of pseudo-elements (p.34-35), `transition` properties (p.185-186), `animation` parameters (p.198), Flexbox illustrations (p.144-150), DevTools screenshots (p.84, p.187-189, p.212-213). If the user asks for these items, say that the figure is not in the extracted text.
