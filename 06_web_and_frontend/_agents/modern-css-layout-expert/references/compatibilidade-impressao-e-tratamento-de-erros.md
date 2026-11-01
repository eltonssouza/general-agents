# Compatibility, Normalization, Error Handling, Prefixes and Print CSS

Source: [CSSHB] p.204-212 (and history p.8-10; `@supports` p.173-174). MDN: "Supporting older browsers", "Organizing CSS", "Debugging CSS" as descriptions [from source] (MDNFS p.3; MDNL p.2-3).

## 1. History on one page

- Before CSS, styling came from HTML presentation tags; CSS separated presentation from structure [from source] (CSSHB p.8-9).
- CSS 1 (1996), CSS 2 (1998), CSS 3 split into modules; today there are no version numbers, but "snapshots" of stable modules (the book's is from 2018); CSS 2 is still the base [from source] (CSSHB p.9-10).
- IE implemented the box model incorrectly from the start, producing years of hacks; "today it is much better" [from source] (CSSHB p.10).
- Author's warning: CSS from five years ago may be outdated [from source] (CSSHB p.9). This applies to the book itself (2019).

## 2. Normalize (and do not reset)

- The browser's default stylesheet is useful, but varies; normalizing removes inconsistencies while keeping basic rules, unlike a reset, which removes everything [from source] (CSSHB p.204-205).
- Normalize.css is the most common solution; it must be loaded before any other CSS [from source] (CSSHB p.205).

## 3. CSS error handling

- CSS is resilient: on finding an error, it skips the line and carries on, unlike JS, which stops [from source] (CSSHB p.205).
- Forgetting the `;` on a line invalidates that declaration and the next one (the browser joins the two up to the next `;`), but the third is valid [from source] (CSSHB p.205-206).
- The browser gives no warning; that is why linters exist (CSS Lint is cited) [from source] (CSSHB p.206). The package's `css_lint.py` script performs this static check.
- Comments: only `/* */`; `//` is not a comment and may "seem" to work because the following line is discarded due to a syntax error; avoid it [from source] (CSSHB p.54-55).

## 4. Vendor prefixes

- Prefixes give access to still-unstable features; the practice is declining in favor of experimental flags, because devs were putting them in production (seen as harmful by the CSS WG) [from source] (CSSHB p.206).
- Historical example of `transition` with `-webkit-`, `-moz-`, `-ms-`, `-o-`; today `transition` alone is enough [from source] (CSSHB p.207).
- List in the book: `-webkit-` (Chrome, Safari, iOS, Android), `-moz-`, `-ms-`, `-o-`; the text attributes `-moz-` to "Safari", which is an error (it is Firefox's) `[inference]` [from source] (CSSHB p.207).
- Recommendation: automate with Autoprefixer (uses data from caniuse.com); create-react-app and Vue CLI already include it [from source] (CSSHB p.208). `[DATED]` the tools and browsers cited are from 2019.

## 5. Feature queries as progressive degradation

`@supports (display: grid) { ... }` and `and/or/not` operators [from source] (CSSHB p.173-174). MDN Layout frames the question: browsers prioritize different features, and you can use modern techniques while ensuring accessibility to older technology [from source] (MDNL p.3).

## 6. Print CSS

- Printing is still used, especially "print to PDF" [from source] (CSSHB p.208).
- Separate file loaded only for printing: `<link ... media="print">` [from source] (CSSHB p.209). The book's snippet writes `src="print.css"`; the correct `<link>` attribute is `href` `[inference]`.
- Alternative: `@media print { ... }` block [from source] (CSSHB p.210).
- Showing link destinations when printing with `a[href*='//']:after { content: " (" attr(href) ") " }` (external only) or `a:after` (all) [from source] (CSSHB p.210-211). The example uses `$primary` (a Sass variable) in `color`, which is invalid in plain CSS `[inference]`.
- `@page` for margins (cm or in are good units); `@page :first`, `:left`, `:right` [from source] (CSSHB p.211).
- Breaks: `page-break-after`, `page-break-before` (accept several values); `page-break-inside: avoid` avoids cutting images/text; in the author's example, wrap the image in a `p` [from source] (CSSHB p.211-212). `[DATED]` the `page-break-*` properties were replaced by `break-*` (`[extrapolation]`).
- Debug with "print" media emulation in Chrome DevTools [from source] (CSSHB p.212-213).

## 7. Organizing CSS (MDN, index)

Lesson "Organizing CSS": good practices for large stylesheets, keeping them maintainable [from source] (MDNFS p.3). No additional content in the PDFs.
