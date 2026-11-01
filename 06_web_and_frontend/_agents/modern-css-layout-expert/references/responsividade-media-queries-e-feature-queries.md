# Responsiveness, Media Queries and Feature Queries

Source: [CSSHB] p.168-174 (and p.141, p.62-63); MDN index [MDNL] p.2 (lessons "Responsive design" and "Media query fundamentals", "Supporting older browsers", "Multiple-column layout") and [MDNL] p.3.

## 1. What MDN Layout (index) says

- Responsive web design (RWD) is a set of practices for the page to adapt layout and appearance to different widths and resolutions [from source] (MDNL p.2).
- Media queries apply CSS only when the browser/device environment meets the rules; they are a key piece of RWD for varying layouts according to the viewport [from source] (MDNL p.2).
- "Supporting older browsers": lesson on ensuring access for users of old browsers that do not support the features used [from source] (MDNL p.2-3).
- Multiple columns (newspaper-style) is an optional feature [from source] (MDNL p.2).
- **Note:** these are only descriptions from an index page; there is no syntax, breakpoints or examples in these PDFs.

## 2. Media types and descriptors (Handbook)

- Media types: `all`, `print`, `screen`, `speech` (screen readers); `screen` is the default; others were discontinued as ineffective [from source] (CSSHB p.168). `[inference]` The book says "default"; in practice, without a type, it applies to all media. Add the caveat.
- They can be used in `@import` and in the `media` attribute of `<link>`; several separated by commas [from source] (CSSHB p.168-169).
- Feature descriptors: `width`, `height`, `device-width`, `device-height`, `aspect-ratio`, `device-aspect-ratio`, `color`, `color-index`, `monochrome`, `resolution`, `orientation`, `scan`, `grid`; each has `min-` and `max-` [from source] (CSSHB p.169-170).
- `[DATED]` `device-width`/`device-height`/`device-aspect-ratio` were marked obsolete in later specifications; prefer `width`/`height` (`[extrapolation]`). The book makes no such caveat.
- Values: lengths (px, rem...) for width/height; `portrait|landscape` for orientation; `progressive|interlace` for scan; integer for color/grid/monochrome; ratio `4/3` for aspect-ratio; `dpi` for resolution [from source] (CSSHB p.170-172).
- Each feature block goes in parentheses [from source] (CSSHB p.171).
- Logic: `and`; comma = "or"; `not` negates the whole query and must come at the beginning (or after a comma) [from source] (CSSHB p.172).

## 3. `@media` in CSS

- The same conditions inside CSS with `@media (...) { ... }`, "the basis of responsive design" [from source] (CSSHB p.173).
- Compound example: screen, width between 600 and 800px, landscape orientation [from source] (CSSHB p.173).
- Book's pattern for reflow: grid with areas and a `max-width: 500px` media query stacking the sidebar below the content [from source] (CSSHB p.141).
- Custom properties can be redefined inside media queries (`--width` example); the book's example puts the `--width` declaration directly inside `@media`, without a selector (p.62-63). `[inference]` declarations need to be in a rule with a selector (e.g. `body`); treat the example as a sketch.

## 4. Feature queries (`@supports`)

- They check whether the browser supports a property/value; the author cites checking `display: grid`; operators `and`, `or`, `not` [from source] (CSSHB p.173-174).
- Practical use: deliver a Grid layout only when supported, keeping a fallback (`[inference]`, an idea consistent with MDNL p.2-3 on older browsers).

## 5. Print as a "medium"

See `compatibilidade-impressao-e-tratamento-de-erros.md` (`@media print`, p.208-212).

## 6. Relevant gaps (confirmed by search)

- Nothing about `<meta name="viewport">`, a mobile-first approach, recommended breakpoints, responsive images, fluid typography (`clamp`), `prefers-color-scheme`, `prefers-reduced-motion`, container queries, `@container`, `dvh` units. The Handbook has 0 occurrences of "mobile" and "clamp". `[extrapolation]` is mandatory on these topics, with an explicit label that the material does not cover them.
- For modern media queries (range syntax `width >= 600px`), `[extrapolation]`.

## 7. Procedure

See `procedimentos.md`, P5 (responsiveness): start from the Grid/Flexbox layout, choose the breakpoint by content (`[inference]`, the book only illustrates 500px, 700/1000px and 600/800px), redefine templates inside `@media`, test with emulation in DevTools (the book cites DevTools for the box model and printing: p.84, p.212-213).
