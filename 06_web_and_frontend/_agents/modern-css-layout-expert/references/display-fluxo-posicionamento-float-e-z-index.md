# Display, Normal Flow, Positioning, Float and z-index

Source: [CSSHB] p.99-123. MDN Layout (index) describes the lessons "Introduction to CSS layout" (`display` values and normal flow), "Floats", "Positioning" and "Practical positioning examples" [from source] (MDNL p.1-2). The body of those lessons is not in the PDF.

## 1. `display`

- Determines how the element is rendered; it is the property with the most values: `block`, `inline`, `none`, `contents`, `flow`, `flow-root`, `table` (+ `table-*`), `flex`, `grid`, `list-item`, `inline-block`, `inline-table`, `inline-flex`, `inline-grid`, `inline-list-item` (and other rare ones, such as `ruby`) [from source] (CSSHB p.99-100).
- `inline` is the default for every element, except those the browser defines as block (`div`, `p`, `section`, `ul`) [from source] (CSSHB p.100-101).
- Inline: does not take "visible" margin, padding, height and width; the browser computes it by itself [from source] (CSSHB p.100-101). `[inference]` The book simplifies; in practice the horizontal margin/padding of inline elements does have an effect. Use the book's text as a didactic rule and add the caveat.
- `inline-block`: like inline, but respects `width` and `height` [from source] (CSSHB p.101).
- `block`: elements stack vertically and each takes 100% of the width; respects width, height, margin, padding [from source] (CSSHB p.101).
- `none`: the element disappears from the browser, but stays in the HTML [from source] (CSSHB p.101).
- `visibility` only appears in two lists in the book (inherited properties, p.27; animatable properties, p.194), without an explanation of values. Comparisons such as `display:none` vs `visibility:hidden` (reserved space, accessibility) are `[extrapolation]`.

## 2. `position`

Five values: `static` (default, normal flow), `relative`, `absolute`, `fixed`, `sticky` [from source] (CSSHB p.102).

| Value | Behavior according to the book | Page |
|---|---|---|
| `static` | normal flow; `top/right/bottom/left` have no effect | CSSHB p.102-104 |
| `relative` | allows shifting with `top/right/bottom/left` (offset properties); the original space stays reserved; `z-index` starts to work | CSSHB p.102-106 |
| `absolute` | leaves the flow; the original space collapses; coordinates relative to the **nearest ancestor that is not static** | CSSHB p.106-111 |
| `fixed` | leaves the flow; relative to the window; not affected by scrolling | CSSHB p.111-113 |
| `sticky` | "sticks" when scrolling (like the letter headers of a contact list on iOS); at the time, poorly supported | CSSHB p.113 |

- Pattern for an absolute element to stay inside its container: give the parent `position: relative` (example `.child` with `.box` at 0,0) [from source] (CSSHB p.109-110). If the parent is static, the box goes to the corner of the nearest positioned container (or the window) [from source] (CSSHB p.109-110).
- Offsets accept a length or percentage; negative values move in the opposite direction [from source] (CSSHB p.103-105).
- `[DATED]` `sticky` today has wide support; treat "poorly supported" as 2019 context. Details of `sticky` (e.g. needs `top`, ancestor with overflow) are not in the book: `[extrapolation]`.

## 3. Float and clear

- Float was important for layouts (left sidebar, margin on the content); with Flexbox and Grid it returned to its original scope: placing content on one side and making siblings flow around it [from source] (CSSHB p.113-114). MDN Layout says the same in summary [from source] (MDNL p.1).
- Values: `left`, `right`, `none` (default) [from source] (CSSHB p.114).
- A floated element leaves the normal flow; content flows around it; not only images: a `span` also floats [from source] (CSSHB p.117-118).
- Several floats stack side by side until they no longer fit; `clear: left` stacks them vertically; `clear` accepts `left`, `right`, `both`, `none` [from source] (CSSHB p.119-122).
- Associated hacks: tables, clearfix and `display: table` for layout; the author says that, without a need for IE8/IE9, there is no reason for them [from source] (CSSHB p.124, 142).
- It does not cover `display: flow-root` as a containment solution (it only lists it, p.99). A historical reference for float layout appears in MDN Layout as "Legacy layout methods" (index) [from source] (MDNL p.2).

## 4. `z-index`

- Controls the order on the Z axis of overlapping elements; integer; higher = closer to the user; negatives allowed [from source] (CSSHB p.122-123).
- Default `auto`: order follows the position in the HTML [from source] (CSSHB p.122).
- With `position: static`, `z-index` has no effect; it must be relative, absolute or fixed (in the book's text) [from source] (CSSHB p.122). `[DATED]` Flex/grid items also respect `z-index` without `position`; the book does not mention it: `[extrapolation]`.
- Tip: use non-consecutive numbers (10, 20...) so layers can be inserted in the middle [from source] (CSSHB p.123).
- Stacking contexts are not covered; `[extrapolation]` if the user asks why a high z-index "does not work".

## 5. Quick decision

| Need | Book's choice | Note |
|---|---|---|
| Put an icon over a card | `position: relative` on the card + `absolute` on the icon | p.109-110 |
| Fixed bar at the top | `position: fixed; top: 0` | p.111-113 |
| Text wrapping around an image | `float` + padding/margin | p.115-117 |
| Column layout | Flexbox or Grid, not float | p.113-114, 124 |
| Overlap layers | `z-index` with a non-static position | p.122-123 |
