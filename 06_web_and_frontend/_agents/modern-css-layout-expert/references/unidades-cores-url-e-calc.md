# Units, Colors, `url()` and `calc()`

Source: [CSSHB] p.36-50. MDN First Steps lists "Values and units" and "Sizing items in CSS" only as descriptive titles [from source] (MDNFS p.2).

## 1. Colors

- Properties that take a color: `color`, `background-color`, `border-color` [from source] (CSSHB p.36).
- Color names: CSS started with 16 and today there is a long list (p.36-43), plus `transparent` and `currentColor` (points to the `color` property; useful for the border to inherit the text color); defined in CSS Color Level 4, case-insensitive [from source] (CSSHB p.43).
- `rgb()`: components 0 to 255; `rgba()` adds alpha from 0 to 1 (the book's example passes four arguments to `rgb()`) [from source] (CSSHB p.43-44).
- Hexadecimal: `#000`/`#000000`, `#fff`; alpha with 1 or 2 extra digits (e.g. `#00000033`); the author recommends 6 digits because the short form was not supported in all browsers [from source] (CSSHB p.44). `[DATED]` 2019 support.
- `hsl()`/`hsla()`: hue, saturation, lightness; black `hsl(0,0%,0%)`, white `hsl(0,0%,100%)` [from source] (CSSHB p.44-45).
- Does not cover: `oklch`, `color-mix()`, `color-scheme`, dark theme, accessibility contrast (a search confirms the absence). `[extrapolation]` if asked.

## 2. Units

| Unit | Meaning according to the book | Page |
|---|---|---|
| `px` | most used; does not correspond to a physical pixel, there is a convention for consistency across devices | CSSHB p.45 |
| `%` | percentage of the corresponding property of the parent (e.g. parent 400px, child 50% = 200px) | CSSHB p.45-46 |
| `cm`, `mm`, `q`, `in`, `pt`, `pc` | real-world units, useful in print: cm ~ 37.8px; in = 96px; 1in = 72pt; 1pc = 12pt; q = quarter of a mm | CSSHB p.46 |
| `em` | font size of the element itself; changes from element to element | CSSHB p.46 |
| `rem` | font size of the root element (`html`); defined once, it is consistent across the page | CSSHB p.46 |
| `ex` | height of the font's "x" | CSSHB p.46 |
| `ch` | width of the "0" | CSSHB p.46-47 |
| `vw`, `vh` | percentage of the viewport width/height | CSSHB p.47 |
| `vmin`, `vmax` | percentage of the smaller/larger viewport dimension | CSSHB p.47 |
| `fr` | fraction of space, used in CSS Grid | CSSHB p.47, 135 |

- `[DATED]` There is no `dvh/svh/lvh` or `cqw`; a search confirms. The book also describes `em` as the "width of the m" in typography, which is a historical explanation; for practical calculation use the font-size definition (p.46).
- `[inference]` For scalable text, the book offers `rem` as a consistent measure (p.46) and demonstrates sizes in `rem` in typography (p.35, 77); it does not discuss font-zoom accessibility.

## 3. `url()`

- Loads a resource in `background-image`, `@import` etc. Forms: relative to the CSS folder (`test.png`, `../test.png`, `subfolder/test.png`), from the domain root (`/test.png`) or absolute [from source] (CSSHB p.47-49).

## 4. `calc()`

- Does basic arithmetic with values; especially useful for adding/subtracting a length from a percentage; returns a length and can be used wherever a pixel value is expected [from source] (CSSHB p.49).
- Operators `+ - * /`; in addition and subtraction **the space around the operator is required** [from source] (CSSHB p.49).
- Examples: `max-width: calc(80% - 100px)`, `calc(50% / 3)`, `calc(50% + 3px)` [from source] (CSSHB p.49-50).
- `calc()` also serves for math in custom properties [from source] (CSSHB p.62). The centered positioning in the animation example uses `calc(50% - 6.25em)` [from source] (CSSHB p.196).
- Boundary: no `min()`, `max()`, `clamp()` (a search confirms); answers about fluid typography are `[extrapolation]`.

## 5. Conversions

The `css_calc.py units` script applies the p.46 equivalences (1in = 96px, 1cm ~ 37.8px, 1pt = 1/72in, 1pc = 12pt, 1mm = 0.1cm, 1q = 0.25mm) and the `rem`/`em` conversion given the base font size supplied by the user (`[inference]`: the book defines the base, the numeric value comes from the user).
