# Procedures and Checklists

Operational procedures built from the Handbook [CSSHB]. Each step points to the page that supports it; the agent's own judgment is labeled.

## P1. "My style is not being applied" (cascade diagnosis)

1. Is the rule valid? Look for a missing `;`, `//` as a comment, an invalid value, `@import` not at the top [from source] (CSSHB p.29, 54-55, 205-206). Run `python scripts/css_lint.py lint file.css`.
2. Does the selector really match the element? Check class/id, space vs. no space (`.a .b` vs `.a.b`), `>` and `+` [from source] (CSSHB p.15, 17-18).
3. Is there another, more specific or later rule? Calculate the 4 slots of each selector and compare; tie = the last one wins [from source] (CSSHB p.21-24). `css_lint.py spec "selector1" "selector2"`.
4. Is there an inline style or `!important`? [from source] (CSSHB p.24).
5. Does the property inherit from the parent, or is `inherit` needed? [from source] (CSSHB p.26-28).
6. Does the value come from `var()`? Check the exact-case name, scope and validity of the value [from source] (CSSHB p.58-62).
7. Element state: link with `:visited`/`:active`? [from source] (CSSHB p.33).
8. Fix: reduce the specificity needed, prefer class to id, avoid `!important` [from source] (CSSHB p.25).

## P2. Choose the layout system

1. Does the content flow in ONE direction (navigation bar, row of cards, centering)? Flexbox [from source] (CSSHB p.141-142, 163-166).
2. Does it need rows AND columns (page with header/sidebar/footer, aligned gallery)? Grid [from source] (CSSHB p.124, 139-141).
3. Text wrapping around an image? `float` [from source] (CSSHB p.113-114).
4. Overlap, fix or anchor (badge, fixed menu)? `position` [from source] (CSSHB p.102-113).
5. Need to support IE8/IE9 or old browsers? Float/tables as a last resort; `@supports` to degrade [from source] (CSSHB p.124, 142, 173-174; MDNL p.2-3). In 2026, `[DATED]` IE is gone, but confirm the user's target browsers.
6. Combine: Grid for the page skeleton, Flexbox inside components `[inference]` (the book says they collaborate, p.124).

## P3. Build a page layout with Grid (recipe from the book)

1. Mark up semantics: `header`, `article`, `aside`, `footer` inside `.wrapper` [from source] (CSSHB p.140).
2. `.wrapper { display:grid; grid-gap; grid-template-columns: 1fr 3fr; grid-template-areas: ... }` [from source] (CSSHB p.140-141).
3. Assign `grid-area` to each child [from source] (CSSHB p.140).
4. Media query to restack on narrow screens [from source] (CSSHB p.141).
5. Verify with `css_calc.py grid --columns "1fr 3fr" --width 1000 --gap 20`.
6. `[inference]` Review HTML order vs. visual order and keyboard focus.

## P4. Center

Decision: horizontal text (`text-align`) -> horizontal block (`flex`+`justify-content` or `margin:0 auto` with width) -> vertical (`align-items`) -> both (`flex` or `grid` + `place-items`) [from source] (CSSHB p.162-166). Confirm the container height `[inference]`.

## P5. Make it responsive

1. Start from Flexbox/Grid with flexible units (`fr`, `%`, `rem`, `minmax`) [from source] (CSSHB p.135-137).
2. Add `@media (max-width: ...)` that redefines templates/direction [from source] (CSSHB p.141, 173).
3. For new features, use `@supports` [from source] (CSSHB p.173-174).
4. Test by emulating sizes in DevTools `[inference]` (the book cites DevTools p.84, 212).
5. Mark as `[extrapolation]`: meta viewport, mobile-first, `clamp()`, container queries, responsive images (outside the material).

## P6. Measure a box (box model)

1. Define `box-sizing` (global `border-box` recommended) [from source] (CSSHB p.98-99).
2. Sum: in `content-box`, width + padding + border (+ margin for occupied space) [from source] (CSSHB p.85).
3. Run `css_calc.py box --width 300 --padding 20 --border 2 --margin 10 --sizing content-box`.

## P7. Fonts and typography

1. Define `font-family` with a generic fallback at the end [from source] (CSSHB p.67).
2. If using your own font: `@font-face` with `src` and woff/woff2 formats [from source] (CSSHB p.71-72); consider the performance cost [from source] (CSSHB p.72) and consult `web-performance-networking-expert` for FOIT/preload.
3. Long text: `overflow-wrap` [from source] (CSSHB p.83).
4. Check legibility/contrast: outside the book `[extrapolation]`.

## P8. Transition or animation

1. Change between two states triggered by an event (hover)? `transition` on the base rule [from source] (CSSHB p.186-187).
2. Several stages or repetition? `@keyframes` + `animation` [from source] (CSSHB p.194-199).
3. Check whether the property is in the list of animatable ones [from source] (CSSHB p.189-194).
4. JS events? `animationstart/end/iteration`; beware of starting on load [from source] (CSSHB p.199).
5. Motion accessibility and rendering cost: `[extrapolation]`.

## P9. Prepare print CSS

1. Choose `<link media="print">` (large file) or `@media print` [from source] (CSSHB p.209-210).
2. Hide the footer/sidebar and change the font, if desired [from source] (CSSHB p.209).
3. Show link URLs: `a[href*='//']:after` [from source] (CSSHB p.210).
4. `@page` with margins in cm/in; `page-break-*` breaks (`[DATED]` today `break-*`) [from source] (CSSHB p.211-212).
5. Emulate `print` in DevTools [from source] (CSSHB p.212-213).

## P10. Resolve a question outside the material

1. Say in one sentence that the collection does not cover the topic (consult `mdn-modulos-e-lacunas-do-material.md`).
2. If answering, use only `[extrapolation]` and suggest checking current documentation.
3. Never attach a book page to content it does not contain.
