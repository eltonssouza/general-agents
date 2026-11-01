# Cascade, Specificity, Inheritance and Import

Operational summary of what the Handbook teaches about how the browser decides which rule wins. All statements are paraphrases of *The CSS Handbook* (Flavio Copes, freeCodeCamp, Apr/2019) [CSSHB]; nothing here is an extensive quotation.

## 1. Cascade (the algorithm)

- The cascade is the process that decides which properties apply to each element when there are several rules coming from different places. It weighs specificity, importance, inheritance and order in the file, and also resolves conflicts [from source] (CSSHB p.19).
- Even with a single CSS file of your own, there are other layers in play: the browser's default stylesheet (user agent), which differs between browsers; then yours; then a user stylesheet (sometimes injected by extensions) [from source] (CSSHB p.20).
- The book does **not** describe the order of precedence among these origins, nor `@layer` (cascade layers). MDN First Steps only lists "Cascade layers" as an optional tutorial, described as an advanced feature that builds on the cascade and specificity [from source] (MDNFS p.3). Any detail beyond that is `[extrapolation]` and must be labeled.

## 2. Specificity

- Two or more rules with different selectors affecting the same property: the most specific wins; specificity tie: the one that appears last wins [from source] (CSSHB p.21).
- Calculation in the book: four "slots", all starting at 0; the leftmost weighs most, like decimal digits (1 0 0 0 > 0 1 0 0) [from source] (CSSHB p.21).

| Slot (right to left) | What increments it | Examples from the book | Page |
|---|---|---|---|
| 1st (least important) | element selectors (tag name), each adds 1 | `p` = 0001; `p span` = 0002; `div p > span` = 0003 | CSSHB p.22 |
| 2nd | classes, pseudo-classes and attribute selectors | `.name` = 0010; `.users .name` = 0020; `[href$='.pdf']` and `:hover` = 0010 | CSSHB p.22 |
| 3rd | `id` | `#name` = 0100; `.user #name` = 0110; `#name span` = 0101 | CSSHB p.23 |
| 4th (most important) | inline style in the `style` attribute | `<p style="color: red">` = 1000 | CSSHB p.24 |

- Combinations: `div .name` = 0011; `a[href$='.pdf']` = 0011; `.pictures img:hover` = 0021 [from source] (CSSHB p.23).
- Documented trick: repeating the same class adds to slot 2 (`.name.name` = 0020), useful for raising specificity without using an id [from source] (CSSHB p.23).
- Inline style beats any rule from an external file or `<style>`, unless there is `!important`, which the book treats as a "fifth slot" [from source] (CSSHB p.24).

## 3. `!important` and the golden rule

- `!important` ignores specificity: it only loses to another `!important` of higher specificity in the less important slots [from source] (CSSHB p.24).
- Author's recommendation: use the specificity you need, no more, so you can override rules later without pain [from source] (CSSHB p.25).
- `!important` is debated; the author admits using it to test styles, but says it should not stay in the CSS files [from source] (CSSHB p.25).
- `id` as a styling hook is also debated because of its high specificity; recommended alternative: classes, which are easier to override, reusable and combinable [from source] (CSSHB p.25).
- Tool cited for checking the calculation: an online specificity calculator [from source] (CSSHB p.25). In this package, `scripts/css_lint.py spec` does the same calculation offline.

`[extrapolation]` Modern notation usually uses three components (ids, classes/attributes/pseudo-classes, elements) and treats inline and `!important` as separate levels; it is equivalent in ordering to the book's slot scheme. The book is silent about `*`, combinators, pseudo-elements and `:not()`; the script follows the current convention and warns when it had to assume.

## 4. Inheritance

- Properties set on a selector pass to children, but only some properties inherit; this makes sense for font (set on `body`) and not for `background-color` [from source] (CSSHB p.25-26).
- List (declared non-exhaustive) of those that inherit: `color`, `cursor`, `direction`, `font*` (family, size, style, variant, weight, stretch, size-adjust), `letter-spacing`, `line-height`, `list-style*`, `text-align`, `text-indent`, `text-shadow`, `text-transform`, `visibility`, `white-space`, `word-break`, `word-spacing`, `quotes`, `tab-size`, `orphans`, `widows`, among others [from source] (CSSHB p.26-28).
- Special keywords:
  - `inherit` forces inheriting from the parent, even for properties that do not inherit [from source] (CSSHB p.28).
  - `revert` goes back to the browser's default stylesheet value; the author says it is rare and that normally you set another value [from source] (CSSHB p.28-29).
  - `initial` and `unset` are described on p.29. `[inference]` The book's description of `initial` (use the browser stylesheet, or inherit) is imprecise relative to the concept of the "initial value of the specification"; when teaching, prefer the book's text but warn about the imprecision.

## 5. `@import`

- Imports another CSS file from a CSS file; **must come before any other rule**, otherwise it is ignored; accepts media descriptors (`all`, `screen`, `print`) [from source] (CSSHB p.29-30).
- The performance cost of `@import` is not discussed in the book; `[extrapolation]` route the analysis of loading/render blocking to the `web-performance-networking-expert` agent (HPBN, p.186-188 of that book).

## 6. Syntax errors and the cascade

- An invalid line is silently discarded; a missing `;` discards the erroring declaration and the next one (see `compatibilidade-impressao-e-tratamento-de-erros.md`) [from source] (CSSHB p.205-206).
- An invalid value for a property (including via `var()`) invalidates the line [from source] (CSSHB p.61).

## 7. How the agent uses this

Diagnosing "my style does not apply": (1) did the rule reach the element? (selector, out-of-order `@import`, syntax error); (2) does another, more specific or later rule win? calculate slots; (3) is there inline or `!important`? (4) does the property inherit? (5) is a value via `var()` invalid? See `procedimentos.md`, procedure P1.
