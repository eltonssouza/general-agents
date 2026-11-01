# Custom Properties (CSS Variables)

Source: [CSSHB] p.55-63.

## 1. Why they exist

- Preprocessors (Less, Sass) succeeded by nesting selectors, importing files and offering variables [from source] (CSSHB p.55-56).
- CSS is not a programming language; it is a declarative syntax. Even so, variables reduce repetition and inconsistency by centralizing values [from source] (CSSHB p.56).
- A differentiator that preprocessors lack: reading and changing the variable via JavaScript at runtime [from source] (CSSHB p.56).
- `[extrapolation]` The book cites nesting as an advantage of preprocessors; native CSS today also supports nesting, and the book does not cover that.

## 2. Syntax and usage

- Defined with two hyphens: `--name: value;`; read with `var(--name)` [from source] (CSSHB p.56-57).
- The value can be any valid CSS value (e.g. `30px 30px 20px 20px`, color, background) [from source] (CSSHB p.57).
- They can be defined inside any element; what changes is the **scope** [from source] (CSSHB p.57-58).
- Scope: available to the children of the selector where they were declared; `:root` (in HTML, the `html` element with higher specificity) makes them global [from source] (CSSHB p.58-59).
- They can be redefined in a more inner scope (`:root` yellow; `.container` blue) [from source] (CSSHB p.59).
- They can be assigned inline: `<main style="--primary-color: orange;">` [from source] (CSSHB p.60).
- They follow the normal rules of the cascade and specificity [from source] (CSSHB p.60).
- Case-sensitive: `--width` ≠ `--Width` [from source] (CSSHB p.62).
- Math requires `calc()`: `calc(10px * 2)` [from source] (CSSHB p.62).
- They work with media queries (redefine the variable by width) [from source] (CSSHB p.62-63).
- Fallback value: `var(--default-margin, 30px)` (second parameter) [from source] (CSSHB p.63).
- Invalid value for the property (px in `position`, rem in `color`): the line is considered invalid and ignored [from source] (CSSHB p.61).

## 3. Interaction with JavaScript

- Set: `element.style.setProperty('--name', 'value')` [from source] (CSSHB p.60).
- Read from `:root`: `getComputedStyle(document.documentElement).getPropertyValue('--name')`, trimming spaces with `trim` [from source] (CSSHB p.60).
- Read from a specific element (different scope): `getComputedStyle(element)` [from source] (CSSHB p.61).

## 4. Support and fallbacks

- "Very good" support at the time (no IE/older versions); for old browsers, libraries such as PostCSS or Myth transpile, but lose the interaction with JS and DevTools [from source] (CSSHB p.61). `[DATED]` Myth and the support assessment are from 2019.

## 5. Decisions

| Situation | Guidance | Page |
|---|---|---|
| Theme/repeated values | `:root { --color: ... }` + `var(--color)` | CSSHB p.56-58 |
| Per-component variation | redefine the variable on the component's selector | CSSHB p.58-59 |
| Optional value | `var(--x, fallback)` | CSSHB p.63 |
| Calculation | `calc()` | CSSHB p.62 |
| Value change per breakpoint | redefine the variable in `@media` (with a selector) | CSSHB p.62-63 |
| Change at runtime | `setProperty` | CSSHB p.60 |

## 6. Boundary

No `@property` (typing/animation of variables), no `color-mix`, no design tokens; a search for `@property` returned nothing. Mark as `[extrapolation]`. The package's linter warns about `var()` whose name differs in case from the definition and about `var()` with no definition and no fallback.
