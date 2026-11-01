# Transforms, Transitions and Animations

Source: [CSSHB] p.182-204. MDN: nothing beyond "Advanced styling effects" as a title [from source] (MDNFS p.3).

## 1. Transforms

- `transform` moves, rotates, scales and skews elements in 2D or 3D; combines well with animation [from source] (CSSHB p.182).
- 2D functions: `translate()`, `rotate()`, `scale()`, `skew()`, `matrix()` (6 elements); per-axis versions: `translateX/Y`, `scaleX/Y`, `skewX/Y` [from source] (CSSHB p.182-183).
- Example: `transform: scale(2, 0.5)` doubles the width and halves the height [from source] (CSSHB p.183).
- `transform-origin` changes the origin (center of rotation) [from source] (CSSHB p.183).
- Combine functions separated by a space: `rotateY(20deg) scaleX(3) translateY(100px)` [from source] (CSSHB p.184).
- 3D: Z axis; `perspective` (distance from the object to the observer) and `perspective-origin`; functions `translateZ`, `rotateZ`, `scaleZ` and shorthands `translate3d`, `rotate3d`, `scale3d`; the author considers 3D too advanced for the book [from source] (CSSHB p.184-185). `[inference]` The book's example uses the selector `.3Delement`, which is not a valid class name without escaping; treat it as an illustration.

## 2. Transitions

- It is the simplest way to animate: you change the value of a property and ask for the change to be gradual up to the final state [from source] (CSSHB p.185).
- Shorthand `transition: property duration timing-function delay` [from source] (CSSHB p.186). The table with all the individual properties is an image (p.185-186): gap.
- Example: `.one, .three { background: rgba(...); transition: background 1s ease-in; }` with `.circle:hover` changing the background; elements without `transition` change without animation [from source] (CSSHB p.186-187).
- Important: the transition goes on the rule of the initial state (not only on `:hover`); `[inference]` this follows from the example, which declares `transition` on the base elements and the change on `:hover`.
- `transition-timing-function`: `linear`, `ease`, `ease-in`, `ease-out`, `ease-in-out`; custom cubic Bézier curves exist (p.187). DevTools (Chrome/Firefox) have visual transition editors [from source] (CSSHB p.187-189).

## 3. Animatable properties

The book gives a "complete" list (the same for transitions and animations): colors and backgrounds, borders, `bottom/left/right/top`, `box-shadow`, `caret-color`, columns, `filter`, `flex*`, `font*`, `grid*`, `height/width`, `letter-spacing`, `line-height`, `margin*`, `max/min-*`, `opacity`, `order`, `outline*`, `padding*`, `perspective*`, `text-*`, `transform`, `vertical-align`, `visibility`, `word-spacing`, `z-index` [from source] (CSSHB p.189-194 and p.200-204). `[DATED]` 2019 list; the animatability of properties (for example `display`, `height: auto`) changed afterwards; the book does not discuss it.
- Performance boundary: the book does not distinguish cheap properties (transform, opacity) from those that trigger layout; `[extrapolation]`, route to `web-performance-networking-expert` for rendering.

## 4. Animations

- Applied with `animation`; the named animation is defined separately in `@keyframes` [from source] (CSSHB p.194).
- Example `animation: spin 10s linear infinite` (name, duration, timing function, repetition) [from source] (CSSHB p.194).
- `@keyframes spin { 0% { transform: rotateZ(0) } 100% { transform: rotateZ(360deg) } }`: as many intermediate points as you want; timing is defined in `animation`, not in the keyframes [from source] (CSSHB p.194-195, 197).
- Complete example: four circles at 0/90/180/-90 degrees, with `transform-origin`, `calc()` and `position:absolute`, rotating the container [from source] (CSSHB p.195-197).
- `animation` shorthand in the order: name, duration, timing-function, delay, iteration-count, direction, fill-mode, play-state [from source] (CSSHB p.198-199). The parameter table is an image (p.198).
- JavaScript events: `animationstart`, `animationend`, `animationiteration`; caution: if the animation starts on load, the JS runs after the CSS and does not intercept `animationstart` [from source] (CSSHB p.199-200).

## 5. Filters and animation

`filter` is among the animatable properties (p.191); see `backgrounds-e-filtros.md`.

## 6. Boundary

No `prefers-reduced-motion`, `will-change`, `animation-timeline`, `@starting-style`, `view transitions`, Web Animations API (a search confirmed the absence of `prefers`, `will-change`). Motion accessibility is `[extrapolation]`; flag it clearly.
