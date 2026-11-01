# Flexbox

Source: [CSSHB] p.141-156 (and centering p.162-166). MDN index: lesson "Flexbox" described as a one-dimensional method, items that grow to fill and shrink to fit [from source] (MDNL p.1).

Warning about the source: the figures on p.144-150 (direction, justify-content, align-items) are images; only the surrounding text was extracted. The data below come from the text.

## 1. Nature and context

- Flexbox (Flexible Box Module) is one of the two modern layout tools, along with Grid; it is **one-dimensional**: it controls a row or a column, not both at the same time [from source] (CSSHB p.141-142). MDN: "one-dimensional method" [from source] (MDNL p.1).
- Main goal: make items fill the whole container space according to rules [from source] (CSSHB p.142).
- Those who do not need to support IE8/IE9 can forget tables, floats, clearfix and `display: table` for layout [from source] (CSSHB p.142).
- `[DATED]` Support cited: 97.66% of users in Feb/2018, IE10+ covered [from source] (CSSHB p.142). Do not use as a current number.
- Activation: `display: flex` or `inline-flex` on the container [from source] (CSSHB p.143-144).

## 2. Container properties

| Property | Values cited | Effect | Page |
|---|---|---|---|
| `flex-direction` | `row`, `row-reverse`, `column`, `column-reverse` | main axis and direction | CSSHB p.144 |
| `justify-content` | `flex-start`, `flex-end`, `center`, `space-between`, `space-around` | horizontal alignment (row axis), five values | CSSHB p.145-147 |
| `align-items` | `flex-start`, `flex-end`, `center`, `baseline`, `stretch` | vertical alignment | CSSHB p.148-151 |
| `flex-wrap` | `wrap`, `wrap-reverse` | by default everything on one line, shrinking items; `wrap` distributes across several lines | CSSHB p.151 |
| `flex-flow` | `flex-direction` + `flex-wrap` | shorthand, e.g. `row wrap` | CSSHB p.151 |

- By default, items start at the left (row) or at the top (column) [from source] (CSSHB p.145).
- `[inference]` The book describes `justify-content` as "horizontal" and `align-items` as "vertical"; this holds for `flex-direction: row`. With `column` the axes swap: when teaching, say "main/cross axis" and note that the book uses the `row` case. See `casos-e-antipadroes.md`.
- `baseline` looks like `flex-start` in simple examples; the author points to a Codepen for a useful case [from source] (CSSHB p.151).
- Absent: `space-evenly`, `align-content`, `gap` in flex, `justify-items` (a search confirms). `[extrapolation]`.

## 3. Item properties

| Property | Default / behavior | Page |
|---|---|---|
| `order` | default 0; the HTML order decides; a negative value brings the item before the others | CSSHB p.153 |
| `align-self` | overrides `align-items` for one item (same 5 values) | CSSHB p.154 |
| `flex-grow` | default 0; if all are 1 and one is 2, that one takes the space of two | CSSHB p.155 |
| `flex-shrink` | default 1; if one is 3, it shrinks 3x more; when space runs out, it takes 3x less | CSSHB p.155 |
| `flex-basis` | `auto` = uses width/height and adds extra space according to flex-grow; `0` = does not add extra space in the calculation; px value = initial size (width or height depending on the axis) | CSSHB p.155-156 |
| `flex` | shorthand for grow, shrink, basis; default `0 1 auto` | CSSHB p.156 |

- `[inference]` The book presents the factors in terms of simple proportion. The real shrink calculation weights `flex-shrink` by the item's base size; the `css_calc.py flex` script implements factor-proportional distribution for grow (as in the book) and, for shrink, base-size weighting marked as `[extrapolation]`.

## 4. Centering with Flexbox

- Horizontal: `display:flex; justify-content:center` on the container; vertical: `align-items:center`; both together center completely [from source] (CSSHB p.163-166). See `centralizacao-tabelas-e-listas.md`.

## 5. Flexbox or Grid?

They are not competitors: they collaborate in complex layouts; Flexbox operates in one dimension and Grid in two [from source] (CSSHB p.124). Rule of thumb from the book: 1D (row OR column) → Flexbox; 2D (rows AND columns) → Grid [from source] (CSSHB p.124, 141-142).

## 6. Boundary

No `flex-basis` with `min-width: 0`, no `gap` in flex, no `margin: auto` on flex items, no "holy grail" patterns. Answer as `[extrapolation]`, noting that the book does not cover it.
