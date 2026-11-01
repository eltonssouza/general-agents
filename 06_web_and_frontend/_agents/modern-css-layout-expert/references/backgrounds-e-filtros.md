# Backgrounds and Filters

Source: [CSSHB] p.50-54 (backgrounds) and p.174-182 (filters). MDN First Steps cites the lessons "Backgrounds and borders" and "Advanced styling effects" (shadows, blend modes, filters) only as a description [from source] (MDNFS p.2-3).

## 1. Backgrounds

- Properties: `background-color`, `-image`, `-clip`, `-position`, `-origin`, `-repeat`, `-attachment`, `-size` and the `background` shorthand [from source] (CSSHB p.50).
- Color accepts a name, `rgb`, `hsl` [from source] (CSSHB p.50-51); image via `url()` [from source] (CSSHB p.51).
- `background-clip`: area in which the background appears; default `border-box`; also `padding-box`, `content-box` [from source] (CSSHB p.51).
- `background-position`: `left/right/center` on the X axis, `top/bottom` on the Y axis [from source] (CSSHB p.51-52).
- `background-repeat`: `repeat` (default), `repeat-x`, `repeat-y`, `no-repeat` [from source] (CSSHB p.52).
- `background-origin`: where the background is positioned from (padding-box by default; border-box; content-box) [from source] (CSSHB p.52).
- `background-attachment`: `scroll` (default), `fixed` (pins to the viewport) and `local` [from source] (CSSHB p.52).
- `background-size`: `auto` (default), `cover` (covers the whole element), `contain` (fits entirely); or length/percentage (one value = width; two = width and height) [from source] (CSSHB p.52-53).
- Shorthand: `background: url(bg.png) top left no-repeat`; fallback color in case the image fails to load: `background: url(image.png) yellow` [from source] (CSSHB p.53-54). Gradient: `linear-gradient(#fff, #333)` [from source] (CSSHB p.54).

## 2. Filters (`filter`)

- Image-editor-style operations applicable to any element: `blur()`, `brightness()`, `contrast()`, `drop-shadow()`, `grayscale()`, `hue-rotate()`, `invert()`, `opacity()`, `sepia()`, `saturate()`, `url()` [from source] (CSSHB p.174-175).
- Several filters combine, separated by spaces (`opacity(0.5) blur(2px)`) [from source] (CSSHB p.176).
- `blur(px|em|rem)` defines a radius [from source] (CSSHB p.176).
- `opacity()`: 0 to 1 or %; the book says `filter` may have hardware acceleration and so would be the preferred method over the `opacity` property [from source] (CSSHB p.177). `[DATED]` / `[inference]` This preference is the author's opinion, implementation-dependent; native `opacity` is also widely optimized today; when recommending, present it as the book's position and ask for measurement.
- `drop-shadow(x y [blur] [spread] [color])`: follows the alpha channel (the shadow follows the shape of a transparent image); minimum 2 and maximum 5 parameters [from source] (CSSHB p.177-178).
- `grayscale()`, `sepia()`, `invert()` (0 to 1 or %; 50% `invert` always gives medium gray), `hue-rotate(deg)`, `brightness()` (above 100% brightens), `contrast()`, `saturate()` [from source] (CSSHB p.178-181).
- Example error in the book: `filter: saturate();` appears without an argument (p.182) `[inference]`; when using it, supply a value.
- `url()` points to an SVG filter; outside the scope of the book [from source] (CSSHB p.182).

## 3. Boundary

No `backdrop-filter`, `mix-blend-mode`, explanation of `box-shadow` (it only appears in the list of animatable properties, p.190, and in one example, p.196), `background-blend-mode`, explained multiple backgrounds, `conic/radial-gradient`; a term search returns no content. Mark as `[extrapolation]`.
