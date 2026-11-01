# Box Model, Border, Padding, Margin and Box Sizing

Source: [CSSHB] p.83-98 (and p.164 for centering with margin). Introduction of the model in MDN: [MDNFS] p.2 (only the description of the lesson "The box model": everything in CSS has a box, and understanding it is the key to complex layouts and alignments).

## 1. The model

- Every element is a generic box; from the inside out: content area, padding, border, margin [from source] (CSSHB p.83-84).
- The book recommends inspecting in DevTools (layout panel) to visualize the layers [from source] (CSSHB p.84-85).
- By default, `width`/`height` apply to the **content area**; padding, border and margin are added on the outside, and the total size calculation needs them [from source] (CSSHB p.85).
- Derived formula `[inference]` (script `css_calc.py box`): in `content-box`, occupied width = width + left/right padding + left/right border + left/right margin.

## 2. `box-sizing`

- `content-box` is the old default; `border-box` makes width/height include padding and border (the margin stays outside) [from source] (CSSHB p.97-98).
- Author's recommendation: apply it to all elements with `*, *:before, *:after { box-sizing: border-box; }` [from source] (CSSHB p.98-99).
- `[inference]` In a grid of `1fr`/percentages with padding, `border-box` avoids overflow from the sum; the book motivates the change by the difficulty of the default calculation (p.98).

## 3. Border

- Properties: `border-style`, `border-color`, `border-width`; `border` shorthand; `border-radius` for corners; `border-image` (+ source, slice, width, outset, repeat) for images as borders, which the author does not detail [from source] (CSSHB p.85, 91-92).
- Styles: dotted, dashed, solid, double, groove, ridge, inset, outset, none, hidden. **The default is `none`**: without a style the border does not appear; `solid` is the common choice [from source] (CSSHB p.86-87).
- Per side: `border-top-style` etc. or `border-style` with 4 values in the order top-right-bottom-left [from source] (CSSHB p.87-88).
- Width: `thin`, `medium` (default), `thick` or a length; 4 values per side or `border-*-width` properties [from source] (CSSHB p.88-89).
- Color: if omitted, the border uses the element's text color; accepts 4 values [from source] (CSSHB p.89-90). (This relates to `currentColor`, p.43.)
- Shorthand: `border: 2px black solid`; per-side shorthands (`border-left`) [from source] (CSSHB p.90).
- `border-radius` defines the radius of the circle that rounds the corner; there are per-corner properties [from source] (CSSHB p.91).

## 4. Padding

- Space **inside** the border; margin is space **outside** [from source] (CSSHB p.92).
- Per-side properties `padding-top/right/bottom/left` [from source] (CSSHB p.92).
- Shorthand: 1 value = all; 2 values = vertical and horizontal; 3 values = top, sides, bottom; 4 values = top-right-bottom-left [from source] (CSSHB p.93-94).
- Accepts any length unit (px, em, rem...) [from source] (CSSHB p.94).

## 5. Margin

- Same scheme of sides and shorthands as padding [from source] (CSSHB p.94-96).
- Accepts lengths, percentages and `auto` [from source] (CSSHB p.96).
- `margin: 0 auto` centers a block horizontally; the author calls Flexbox the modern way and keeps the auto margin for old browsers [from source] (CSSHB p.96-97); for it to work the element needs a defined width and `display: block` if it is inline [from source] (CSSHB p.164).
- Negative margin: it is the only sizing property that accepts a negative value; it moves the element up over the previous ones (top), pulls the following ones (bottom), widens the content (right) or shifts it to the left [from source] (CSSHB p.97).

## 6. Practical cases

- "My 300px element overflows the parent": check `content-box` + padding/border; suggest a global `border-box` (p.98-99).
- "Border does not appear": `border-style` is missing (p.87).
- "I want to center a block": see `centralizacao-tabelas-e-listas.md`.

## 7. Boundary and dated

- There is no discussion of margin collapsing, `overflow`, `outline`, `box-shadow` (it appears only in the list of animatable properties, p.190) or logical properties (`margin-inline`); a text search confirms this. MDNFS p.2-3 lists the lessons "Overflowing content" and "Sizing items in CSS" only as titles. Answer this as `[extrapolation]`, if necessary.
- `[DATED]` The mention of IE hacks and the IE incorrect box model (p.10) is historical context.
