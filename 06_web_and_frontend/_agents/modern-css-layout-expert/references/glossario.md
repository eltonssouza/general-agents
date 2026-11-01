# Glossary: Modern CSS and Layout

Definitions in our own words, anchored in [CSSHB] (Handbook), [MDNFS] and [MDNL] (MDN indexes). English terms preserved as in the material.

**`@font-face`**: rule that creates a font family name and links it to a file downloaded by the browser [from source] (CSSHB p.71-72).

**`@import`**: directive that brings in another CSS file; must come before any other rule, or it is ignored [from source] (CSSHB p.29).

**`@keyframes`**: block that describes the states of a named animation; timing is defined in `animation` [from source] (CSSHB p.194-195).

**`@media`**: structure that applies CSS only if the media/feature meets the condition; basis of responsive design [from source] (CSSHB p.173).

**`@supports` (feature query)**: tests whether the browser supports a property/value before applying a block [from source] (CSSHB p.173-174).

**Adjacent sibling (`+`)**: combinator that selects the element immediately following another [from source] (CSSHB p.18).

**Alpha / alpha channel**: the transparency part of a color, from 0 to 1 [from source] (CSSHB p.43-44).

**`align-items` / `align-self`**: vertical alignment (in the `row` direction) of flex items; `-self` overrides it for one item [from source] (CSSHB p.148, 154).

**Animation (CSS Animation)**: movement orchestrated by keyframes, applied with `animation` [from source] (CSSHB p.194).

**Attribute selector**: selector that matches elements by attribute (`[href$='.pdf']`) [from source] (CSSHB p.30-31).

**Block**: `display` value in which elements stack vertically and take the full width [from source] (CSSHB p.101).

**`border-box` / `content-box`**: `box-sizing` modes; in `border-box`, width/height include padding and border [from source] (CSSHB p.97-98).

**Box model**: box model: content, padding, border, margin [from source] (CSSHB p.83-84).

**Cascade**: algorithm that resolves conflicts between rules according to specificity, importance, inheritance and order [from source] (CSSHB p.19).

**Cascade layers**: advanced feature presented in MDN as an extension of the cascade; no content in the collection beyond the title [from source] (MDNFS p.3).

**`calc()`**: calculation function; operators require spaces in addition/subtraction [from source] (CSSHB p.49).

**Clear**: property that prevents an element from sitting beside floats (`left`, `right`, `both`, `none`) [from source] (CSSHB p.121-122).

**Class selector**: `.name`; reusable; weighs in slot 2 of specificity [from source] (CSSHB p.13, 22).

**Combinator**: operator between selectors (space, `>`, `+`) that relates elements by their position in the tree [from source] (CSSHB p.17-18; MDNFS p.2).

**Content (property)**: defines the content inserted by `::before`/`::after` [from source] (CSSHB p.35-36).

**Custom property (CSS variable)**: value named with `--name`, read by `var()`; scoped by element; manipulable by JS [from source] (CSSHB p.56-63).

**Declaration / declaration block**: a property-value pair and the set of them inside braces [from source] (CSSHB p.5-6).

**`display`**: property that defines how the element is rendered [from source] (CSSHB p.99).

**Document flow / normal flow**: default arrangement of elements; `position: static` is in it [from source] (CSSHB p.102; MDNL p.1).

**`em` / `rem`**: units relative to the element's / the root's font size [from source] (CSSHB p.46).

**Feature descriptor (media feature)**: condition such as `width` or `orientation` used in media queries [from source] (CSSHB p.169-170).

**Filter**: property with visual-effect functions (`blur()`, `drop-shadow()`...) [from source] (CSSHB p.174-175).

**Flex container / flex item**: element with `display:flex` and its direct children [from source] (CSSHB p.143-144).

**`flex-grow` / `flex-shrink` / `flex-basis` / `flex`**: growth, shrink and base factors; shorthand `flex: 0 1 auto` [from source] (CSSHB p.155-156).

**Flexbox**: one-dimensional layout model [from source] (CSSHB p.141-142).

**Float**: take an element out of the flow and place it left/right, with content around it [from source] (CSSHB p.113-114, 117).

**`fr` (fraction unit)**: unit for a fraction of the space in Grid [from source] (CSSHB p.47, 135).

**Grid (CSS Grid)**: two-dimensional layout system [from source] (CSSHB p.123-124).

**`grid-template-areas` / `grid-area`**: defines named areas and associates items with them [from source] (CSSHB p.137-138).

**Inheritance**: passing of property values to children, for only some properties [from source] (CSSHB p.25-26).

**HSL / RGB / hex**: color notations [from source] (CSSHB p.43-45).

**`!important`**: marker that makes the declaration prevail over specificity [from source] (CSSHB p.24).

**Inline (display)**: default of elements; no controllable dimensions [from source] (CSSHB p.100-101).

**Inline styles**: style in the `style` attribute; slot 4 of specificity [from source] (CSSHB p.11-12, 24).

**`inline-block`**: like inline, but respects width/height [from source] (CSSHB p.101).

**Margin collapse**: collapsing of margins; **not covered** by the book (gap note).

**`minmax()`**: track function with a minimum and maximum [from source] (CSSHB p.136-137).

**Media query**: media condition applied to CSS [from source] (CSSHB p.173; MDNL p.2).

**Media types**: `all`, `print`, `screen`, `speech` [from source] (CSSHB p.168).

**Normalize (normalize.css)**: unify browser defaults without wiping everything [from source] (CSSHB p.204-205).

**Offset properties**: `top/right/bottom/left` used with `position` [from source] (CSSHB p.102-103).

**Padding**: inner space between content and border [from source] (CSSHB p.92).

**Pseudo-class**: selector of state or position with one colon [from source] (CSSHB p.31-32).

**Pseudo-element**: selector of a part of the element with `::` [from source] (CSSHB p.34).

**`:root`**: document root; in HTML, the `html` with higher specificity [from source] (CSSHB p.58-59).

**Position**: `static`, `relative`, `absolute`, `fixed`, `sticky` [from source] (CSSHB p.102).

**Responsive web design (RWD)**: practices for adapting the page to different widths and resolutions [from source] (MDNL p.2).

**Selector**: expression that identifies elements [from source] (CSSHB p.5-6).

**Specificity**: weight of the selector, calculated in four slots [from source] (CSSHB p.21-24).

**Transform**: move, rotate, scale, skew [from source] (CSSHB p.182-183).

**Transition**: gradual change of a property [from source] (CSSHB p.185).

**User agent stylesheet**: the browser's default stylesheet [from source] (CSSHB p.20).

**Vendor prefix**: prefix (`-webkit-`, `-moz-`...) for unstable features; declining [from source] (CSSHB p.206-207).

**Viewport units**: `vw`, `vh`, `vmin`, `vmax` [from source] (CSSHB p.47).

**Web safe fonts**: fonts preinstalled on several systems, used with a generic fallback [from source] (CSSHB p.65-67).

**Writing mode**: direction of text flow (horizontal, vertical); `writing-mode` [from source] (CSSHB p.80-81; MDNFS p.3).

**z-index**: order on the Z axis of overlapping elements [from source] (CSSHB p.122-123).
