# CSS Grid

Source: [CSSHB] p.123-141 (and centering p.166, animation p.195). MDN index: lesson "CSS grid layout", a two-dimensional system of rows and columns [from source] (MDNL p.1-2).

## 1. Context and dating

- Grid is described as "the new kid in town" and the future of layouts; not yet fully supported when the text was written [from source] (CSSHB p.123).
- Support cited: April/2019, all major browsers (except IE) already supported it, covering 92% of users [from source] (CSSHB p.124). `[DATED]` do not use as a current statistic.
- Grid does not compete with Flexbox: Grid is two-dimensional (rows AND columns), Flexbox is one-dimensional [from source] (CSSHB p.124).
- Without a need for IE8/IE9, there is no reason for layouts with tables, floats, clearfix and `display: table` [from source] (CSSHB p.124).
- **Important absences (search confirmed):** `subgrid`, `auto-fit`/`auto-fill`, `repeat()` with `minmax()` for automatic responsive columns, `gap` without the `grid-` prefix, `justify-items`/`place-items` beyond the centering example, `align-content`, `grid-auto-flow` (only in the animatable list). Mark as `[extrapolation]` when explaining.

## 2. Activation and tracks

- Activated on the container with `display: grid`; there are properties on the container and on the items [from source] (CSSHB p.125).
- `grid-template-columns` and `grid-template-rows` define the number and size of columns/rows (e.g. 4 columns of 200px and 2 rows of 300px) [from source] (CSSHB p.125-126).
- `auto` is for automatically sized tracks (e.g. header 100px, flexible middle, footer 100px) [from source] (CSSHB p.127).
- Columns and rows can have different sizes [from source] (CSSHB p.127-128).
- Space between cells: none by default; properties `grid-column-gap`, `grid-row-gap` and shorthand `grid-gap` [from source] (CSSHB p.129-131). `[DATED]` today `gap`, `column-gap`, `row-gap` are the current names (`[extrapolation]`); `grid-gap` remains as a legacy alias.

## 3. Item placement

- Items can span several cells with `grid-column-start/end` and `grid-row-start/end`; the numbers are the **lines** that separate the columns, starting at 1 [from source] (CSSHB p.131-133).
- Shorthands `grid-column` and `grid-row`: `2 / 4` (from line 2 to 4) or `2 / span 2` (starts at 2 and spans two) [from source] (CSSHB p.133-134).
- `fr`: fraction of the available space (`1fr 1fr 1fr` = three equal columns) [from source] (CSSHB p.134-135). Can mix fr, px, rem and % (`3rem 15% 1fr 2fr`) [from source] (CSSHB p.135).
- `repeat(4, 100px)` or `repeat(4, 1fr)` [from source] (CSSHB p.135-136).
- `minmax(min, max)`: minimum width (e.g. sidebar never smaller than 200px); accepts `auto` as maximum or minimum [from source] (CSSHB p.136-137).
- `grid-template-areas` + `grid-area`: name areas and position items independently of the HTML order; `.` marks an empty cell [from source] (CSSHB p.137-139).
- Fill the page: `height: 100vh` with tracks in `fr` [from source] (CSSHB p.139).

## 4. Canonical example from the book: header, sidebar, content, footer

`.wrapper` with `display: grid`, `grid-gap`, columns `1fr 3fr` and areas `"header header" / "sidebar content" / "footer footer"`; each tag receives `grid-area` with the area name [from source] (CSSHB p.139-141). On a narrow screen, a `max-width: 500px` media query redefines it to one column and stacks the areas (header, content, sidebar, footer) [from source] (CSSHB p.141). This is the only complete responsive pattern in the book; worth citing in responsive layout questions.

## 5. Centering with Grid

`body { display: grid; place-items: center; height: 100vh; }` centers on both axes [from source] (CSSHB p.166). Repeated in the animation example (p.195).

## 6. Decisions

| Situation | Book's guidance | Page |
|---|---|---|
| Page layout with areas (header/sidebar/footer) | Grid with `grid-template-areas` | CSSHB p.137-141 |
| Visually reorder without touching the HTML | `grid-area`/areas | CSSHB p.137-138 |
| Sidebar with a minimum width | `minmax(200px, 3fr) 9fr` | CSSHB p.136 |
| Equal columns | `repeat(n, 1fr)` | CSSHB p.135-136 |
| Single row of flexible items | Flexbox | CSSHB p.141-142 |
| Reflow on a small screen | media query redefining the template | CSSHB p.141 |

## 7. Cautions

- `[inference]` Moving items with `grid-template-areas` changes only the presentation; the HTML order remains the reading and tabbing order; the book does not discuss accessibility, so flag the limitation.
- `[inference]` `fr` divides the **remaining** space; the `css_calc.py grid` script calculates this (fixed tracks and gaps deducted first) and warns that the items' `min-content` may change the real result (`[extrapolation]`).
