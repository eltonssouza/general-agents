# CSS Cases and Antipatterns

Compilation of examples and pitfalls from the Handbook [CSSHB]. Each item: situation, why it fails, fix, source. Agent adjustments are labeled.

## A. Cascade and selector antipatterns

| # | Antipattern | Problem | Fix | Source |
|---|---|---|---|---|
| A1 | `!important` as the default solution | becomes the strongest rule and only another `!important` beats it | reduce/organize specificity; reserve it for tests | CSSHB p.24-25 |
| A2 | Styling everything by `id` | high specificity, not reusable, hard to override | use classes | CSSHB p.25 |
| A3 | Selectors with too much specificity | prevents overriding later | "use the specificity you need, no more" | CSSHB p.25 |
| A4 | `a { color }` without states | link changes color after click/visit | declare `a, a:visited, a:active` | CSSHB p.33 |
| A5 | `@import` in the middle of the file | it is ignored | put it at the top | CSSHB p.29 |
| A6 | Missing `;` | loses the declaration and the next one, with no visible error | always use `;` and run a linter | CSSHB p.7, 205-206 |
| A7 | `//` as a comment | the following line may be discarded due to a syntax error | use `/* */` | CSSHB p.54-55 |
| A8 | `ul:nth-child(odd)` to stripe rows | targets the `ul`, not the items `[inference]` | `li:nth-child(odd)`; in a table, `tbody tr:nth-child(odd)` | CSSHB p.34, 159-160 |
| A9 | Pseudo-element with one colon | exists only for compatibility | use `::` | CSSHB p.34 |

## B. Box model antipatterns

| # | Antipattern | Problem | Fix | Source |
|---|---|---|---|---|
| B1 | Width + padding + border in `content-box` | element wider than expected | global `box-sizing: border-box` | CSSHB p.85, 98-99 |
| B2 | `border-width/color` without `border-style` | border does not appear (default style `none`) | set `solid` etc. | CSSHB p.87 |
| B3 | `margin: 0 auto` without a width on a block | does not center `[inference]` from the text of p.164 | set `width`; `display:block` if inline | CSSHB p.164 |
| B4 | Shorthand values 3/4 in the wrong order | swapped spacing | order top-right-bottom-left | CSSHB p.93-94 |

## C. Layout antipatterns

| # | Antipattern | Problem | Fix | Source |
|---|---|---|---|---|
| C1 | Float, tables or clearfix for page layout | obsolete hacks | Flexbox/Grid | CSSHB p.113-114, 124, 142 |
| C2 | `position:absolute` without a positioned parent | reference becomes the nearest positioned ancestor or the window | `position:relative` on the parent | CSSHB p.109-110 |
| C3 | `z-index` without `position` | no effect in the book's model | make it relative/absolute/fixed (or, for flex/grid items, see `[extrapolation]`) | CSSHB p.122 |
| C4 | Consecutive `z-index` values | recalculation when inserting layers | use spacing (10, 20...) | CSSHB p.123 |
| C5 | Using Grid where one axis suffices (or vice versa) | wrong tool for the dimension | 1D = Flexbox; 2D = Grid | CSSHB p.124 |
| C6 | Saying "horizontal justify-content" in a column | axes swap with `flex-direction: column` | think in main/cross axis `[inference]` | CSSHB p.144-148 |
| C7 | Grid sidebar that collapses too much | | `minmax(200px, ...)` | CSSHB p.136 |
| C8 | Moving items with `grid-template-areas` without checking the HTML order | reading/keyboard follow the HTML `[inference]` | review the order; outside the book | CSSHB p.137-138 |

## D. Typography, fonts and values antipatterns

| # | Antipattern | Problem | Fix | Source |
|---|---|---|---|---|
| D1 | `font-family` without a final generic | no safe fallback | end with `sans-serif`/`serif`/`monospace` | CSSHB p.66-67 |
| D2 | Web font without thinking about performance | download cost | consider the load; consult the performance specialist | CSSHB p.72 |
| D3 | `calc(100%-20px)` without spaces | invalid | spaces around `+` and `-` | CSSHB p.49 |
| D4 | `var(--Name)` where `--name` exists | variable does not resolve (case sensitive) | match the case | CSSHB p.62 |
| D5 | `var()` with an improper value (px in `position`) | invalid line ignored | validate the type; use a fallback | CSSHB p.61, 63 |
| D6 | Reading `animationstart` of an animation that starts on load | JS runs after the CSS | register by other means or accept it | CSSHB p.199 |
| D7 | Hand-written prefixes | uncertainty and staleness | Autoprefixer | CSSHB p.208 |

## E. Solved cases

### E1. Header, sidebar, content, footer
Grid with areas and `grid-gap`; restacks at `max-width: 500px` [from source] (CSSHB p.139-141).

### E2. Center a card on the screen
`display:grid; place-items:center; height:100vh` on the container [from source] (CSSHB p.166) or flex with `align-items`+`justify-content` (p.165-166).

### E3. Icon in the corner of a card
Card `position:relative`; icon `position:absolute; top:0; left:0` (the book shows the top-left corner; other corners follow the same offset logic) [from source] (CSSHB p.109-110).

### E4. Alternating table rows
`tbody tr:nth-child(odd){...}` + `border-collapse: collapse` [from source] (CSSHB p.159-161).

### E5. Print links with URL
`@media print { a[href*='//']:after { content:" (" attr(href) ") " } }` [from source] (CSSHB p.210).

### E6. Text wrapping around an image
`img { float:left; padding: 20px 20px 0 0 }` [from source] (CSSHB p.115-116).

### E7. Smooth hover
`transition: background 1s ease-in` on the base state + change in `:hover` [from source] (CSSHB p.186-187).

### E8. Theme by variable
`:root{--primary-color: yellow}` and `p{color:var(--primary-color)}`; switch via JS with `setProperty` [from source] (CSSHB p.57, 60).

## F. Requests the collection does NOT support (answer with caution)

| Request | Stance |
|---|---|
| Responsive grid without a media query (`auto-fit`) | outside the book; `[extrapolation]` |
| Container queries / subgrid | outside the book; `[extrapolation]` |
| Fluid typography with `clamp()` | outside the book |
| Dark mode and reduced motion | outside the book |
| Contrast, visible focus, accessibility | outside the book; MDN only lists topics |
| CSS/rendering performance | route to `web-performance-networking-expert` |
| Advanced Sass/Less, Tailwind, CSS-in-JS | out of scope (the book only mentions preprocessors) |
| JavaScript beyond `setProperty`/animation events | out of scope |
