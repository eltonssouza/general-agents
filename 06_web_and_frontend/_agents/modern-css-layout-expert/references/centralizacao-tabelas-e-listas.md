# Centering, Tables and Lists

Source: [CSSHB] p.156-168.

## 1. Centering (recipes from the book)

Author's premise: centering is different horizontally and vertically; where Flexbox offers a solution, he ignores the old techniques, since Flexbox has been supported for years (IE10 included) [from source] (CSSHB p.162-163).

| Goal | Recipe | Page |
|---|---|---|
| Text, horizontal | `text-align: center` | CSSHB p.163 |
| Block, horizontal (modern) | container `display:flex; justify-content:center` | CSSHB p.163 |
| Block, horizontal (without Flexbox) | `margin: 0 auto` + defined `width`; remember `display:block` if inline | CSSHB p.164 |
| Vertical | container `display:flex; align-items:center` | CSSHB p.165 |
| Vertical and horizontal (Flexbox) | `align-items:center; justify-content:center` | CSSHB p.165-166 |
| Vertical and horizontal (Grid) | `display:grid; place-items:center; height:100vh` | CSSHB p.166 |

- `[inference]` For vertical centering, the container needs a height (the Grid example uses `100vh`; the Flexbox one shows no height). Ask about the container's height.
- `margin: 0 auto` is equivalent to margin-top/bottom 0 and left/right auto [from source] (CSSHB p.164).

## 2. Tables

- Tables were overused for layout; with Grid and Flexbox, they return to their original function: tabular data [from source] (CSSHB p.156).
- Base HTML: `table`, `thead`, `tbody`, `tr`, `th scope="col|row"`, `td` [from source] (CSSHB p.156-157). The browser's default style is unattractive [from source] (CSSHB p.157).
- Border on `table, th, td { border: 1px solid #333 }` [from source] (CSSHB p.158).
- Alternating rows: `tbody tr:nth-child(odd)` (or even) [from source] (CSSHB p.159-160).
- `border-collapse: collapse` on the `table` merges the double borders into one [from source] (CSSHB p.161). It is also in the list of inherited properties (p.26).
- MDN: lesson "Styling tables" listed only as a description [from source] (MDNFS p.3).

## 3. Lists

- `list-style-type`: predefined marker (`disc`, `circle`, `square`, `none` among the popular ones) [from source] (CSSHB p.166-167).
- `list-style-image`: custom marker with `url()` [from source] (CSSHB p.167).
- `list-style-position`: marker `outside` (default) or `inside` [from source] (CSSHB p.167).
- Shorthand `list-style: url(list-image.png) inside` [from source] (CSSHB p.168).
- The `list-style-*` properties inherit (p.27).

## 4. Boundary

No `counter()`/`counter-reset`, no `::marker`, no `table-layout`, no responsive tables (horizontal scrolling etc.); a search confirmed the absence of counter and table-layout. MDNFS lists "Overflowing content" only as a title (p.2-3). Mark as `[extrapolation]`.
