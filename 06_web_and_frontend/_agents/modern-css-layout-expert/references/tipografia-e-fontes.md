# Typography and Fonts

Source: [CSSHB] p.63-83. MDN: "Handling different text directions" (writing modes) and "Debugging CSS" are listed only as a description [from source] (MDNFS p.3).

## 1. Fonts

- The `font` property is a shorthand for `font-family`, `font-weight`, `font-stretch`, `font-style`, `font-size` (and `font-variant`) [from source] (CSSHB p.63-64, 70).
- `font-family`: a "family" groups subfonts (bold, italic, light) [from source] (CSSHB p.64). Fallback list: if the first does not exist or the download fails, the next is used [from source] (CSSHB p.65). Web safe fonts (preinstalled) by category serif/sans-serif/monospace [from source] (CSSHB p.65-66), with no guarantee on every system [from source] (CSSHB p.66).
- Generic names: `sans-serif`, `serif`, `monospace`, `cursive`, `fantasy`; they should be at the end of the list as a last resort, e.g. `Helvetica, Arial, sans-serif` [from source] (CSSHB p.66-67). `[inference]` The book's explanation ("with/without ligatures") does not correctly describe the serif/sans difference (serifs); use the practical rule (generic last), and add the caveat.
- `font-weight`: `normal`, `bold`, `bolder`, `lighter` (relative to the parent) and 100 to 900 (400 = normal, 700 = bold); if there is no face for a number, one at least as bold as the previous is used [from source] (CSSHB p.67-68). The text on p.67 says "width" but describes weight (book error `[inference]`).
- `font-stretch`: from `ultra-condensed` to `ultra-expanded`; requires the font to have the faces [from source] (CSSHB p.68).
- `font-style`: `italic`, `oblique`, `normal` (minimal difference between italic and oblique) [from source] (CSSHB p.68-69).
- `font-size`: length/percentage or keywords (`xx-small` to `xx-large`, `smaller`, `larger`) [from source] (CSSHB p.69-70).
- `font-variant`: originally `normal`, `inherit`, `small-caps` [from source] (CSSHB p.70).
- `font` shorthand: at minimum `font-size` and `font-family`; the others optional, in a defined order (examples `italic bold 20px Helvetica`, `small-caps bold 20px Helvetica`) [from source] (CSSHB p.70-71). The line with the full order is truncated in the extraction; trust the examples.

## 2. Custom fonts

- `@font-face` creates a family name and maps it to a file; it can live in the CSS or in a dedicated CSS imported with `@import` [from source] (CSSHB p.71-72).
- `src` points to one or more URIs; formats: woff, woff2, eot, otf, ttf; properties `font-family`, `font-weight`, `font-style`, `font-stretch` describe the font [from source] (CSSHB p.72).
- The book states that fonts can only be downloaded from the current origin (same origin) [from source] (CSSHB p.72). `[DATED]` / `[inference]` cross-origin fonts require a CORS header on the server; warn that the statement is simplified.
- "Performance note": the book only points out that loading a font has a cost, without detail [from source] (CSSHB p.72). Route to `web-performance-networking-expert` (HPBN covers FOIT/FOUT and `preload` for fonts, p.194 and p.274-275 of that book).
- Does not cover `font-display`, variable fonts, `unicode-range`, `size-adjust` (a search for "font-display" returned nothing).

## 3. Text properties

| Property | Effect according to the book | Page |
|---|---|---|
| `text-transform` | `capitalize`, `uppercase`, `lowercase`, `none` (avoids inheriting) | CSSHB p.73-74 |
| `text-decoration` | `underline`, `overline`, `line-through`, `blink`, `none`; style (`solid`, `double`, `dotted`, `dashed`, `wavy`) and color; sub-properties `-line`, `-color`, `-style` | CSSHB p.74-75 |
| `text-align` | default `start`; `end`, `left`, `right`, `center`, `justify` | CSSHB p.75-76 |
| `vertical-align` | aligns inline: length/%, `baseline` (default), `sub`, `super`, `top`, `text-top`, `middle`, `bottom`, `text-bottom` | CSSHB p.76-77 |
| `line-height` | line height (vertical space between lines) | CSSHB p.77 |
| `text-indent` | indentation of the first line (length or %) | CSSHB p.77 |
| `text-align-last` | alignment of the last line | CSSHB p.77-78 |
| `word-spacing`, `letter-spacing` | `normal` or length, including negative | CSSHB p.78-79 |
| `text-shadow` | x, y, blur, optional color (default: text color) | CSSHB p.79 |
| `white-space` | collapse: `normal`, `nowrap`, `pre-line`; preserve: `pre`, `pre-wrap` | CSSHB p.79-80 |
| `tab-size` | tab width (default 8) | CSSHB p.80 |
| `writing-mode` | `horizontal-tb` (default), `vertical-rl`, `vertical-lr` | CSSHB p.80-81 |
| `hyphens` | `none` (default), `manual`, `auto` | CSSHB p.81 |
| `text-orientation` | in vertical mode: `mixed`, `upright`, `sideways` | CSSHB p.81-82 |
| `direction` | `ltr`, `rtl` | CSSHB p.82 |
| `word-break` | `normal`, `break-all`, `keep-all` (CJK) | CSSHB p.82 |
| `overflow-wrap` | `normal`, `break-word`, `anywhere`; alias `word-wrap`; prefer for Western languages; none adds a hyphen | CSSHB p.82-83 |

- `[inference]` The book's `line-height` example uses `0.9rem` (p.77); the book does not discuss unitless values or legibility/accessibility (WCAG), only the definition.
- Many of these properties inherit (p.26-28): `line-height`, `text-align`, `text-indent`, `letter-spacing`, `white-space`, etc.
- The book lists `line-break` but states it does not cover it (p.82).

## 4. Recipes

- Long text that overflows the container: `overflow-wrap: break-word` (or `anywhere`) (p.83).
- Larger first line: `p::first-line { font-size: 2rem }` (p.35).
- Font fallback: always end with a generic (p.67).
