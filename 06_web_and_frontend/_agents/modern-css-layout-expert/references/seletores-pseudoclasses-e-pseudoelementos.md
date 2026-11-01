# Selectors, Attributes, Pseudo-classes and Pseudo-elements

Source: [CSSHB] p.5-19 and p.30-36; index supplements in [MDNFS] p.1-2.

## 1. Anatomy of a rule

- A rule has two parts: the selector and the declaration block; each declaration is a property/value pair [from source] (CSSHB p.5-6).
- A selector can target one or several things (separated by commas): tags, classes (`.x`), ids (`#x`), attributes, pseudo-classes [from source] (CSSHB p.7).
- A semicolon ends each declaration and is optional only on the last one; the author recommends always using it [from source] (CSSHB p.7).
- Formatting is free, but it is worth following a convention (opening brace on the selector line, 2-space indentation) [from source] (CSSHB p.7-8).
- Ways of attaching CSS: `<link>` in the `<head>` (preferred, one file for the whole site), `<style>` (good for experimenting) and the inline `style` attribute [from source] (CSSHB p.10-12). See also the note that the `<link>` example for printing on p.209 uses `src` instead of `href`, which is an error in the text `[inference]`.

## 2. Basic selectors and combinations

| Need | Form | Book's note | Page |
|---|---|---|---|
| All tags | `p` | affects all elements of that tag | CSSHB p.12-13 |
| Class / id | `.a` / `#a` | a class can repeat; an id only once per document; an element can have several classes | CSSHB p.13 |
| Tag + class/id | `p.a`, `p#a` | used to gain specificity | CSSHB p.14-15 |
| Two classes on the same element | `.a.b` (no space) | | CSSHB p.15 |
| Class + id | `.a#b` | | CSSHB p.15 |
| Group | `p, .a` | same declaration for several selectors | CSSHB p.16 |
| Descendant | `p span` (space) | applies at any depth | CSSHB p.17 |
| Direct child | `p > span` | first level only | CSSHB p.17-18 |
| Adjacent sibling | `p + span` | span immediately after a `p` | CSSHB p.18 |

`[inference]` For `p + span` the book describes "spans preceded by p"; in practice, it is the immediately following sibling. Ask for an HTML example when diagnosing.

## 3. Attribute selectors

- Presence: `p[id]` matches any `p` with the attribute, any value [from source] (CSSHB p.30).
- Exact value: `p[id="x"]` [from source] (CSSHB p.30-31).
- Part of the value: `*=` contains; `^=` starts with; `$=` ends with; `|=` starts with and is followed by a hyphen (or is equal); `~=` space-separated word [from source] (CSSHB p.31).
- Comparisons are case-sensitive; the `i` suffix before the `]` makes them insensitive, with partial support at the time of the book [from source] (CSSHB p.31). `[DATED]` the 2019 support table has changed; confirm in a current source.

## 4. Pseudo-classes

- They are keywords with one colon that select by state or by position among children (active/visited links, hover, focus, first child, odd rows) [from source] (CSSHB p.31-32).
- **Extraction gap:** the table with the "most popular" pseudo-classes (p.32-33) is an image in the PDF and was not extracted; only the text examples are traceable. Do not attribute to the book a list that cannot be checked.
- Central example in the book: styling `a` only with `color` fails after a click, because the link becomes `:active` and then `:visited`; to cover the states, write `a, a:visited, a:active` [from source] (CSSHB p.33). `[inference]` If there is also `:hover`/`:focus` styling, the order of the rules matters because of specificity ties (p.21); the book does not discuss the recommended order.
- `:nth-child(odd|even)` for alternating rows; `:nth-child(-n+3)` for the first three; `:nth-child(5n)` for one in every five [from source] (CSSHB p.33-34). The book's literal example uses `ul:nth-child(odd)`, which targets an odd `ul` among siblings; to stripe items use `li:nth-child(odd)` `[inference]`; on p.159-160 the table correctly uses `tbody tr:nth-child(odd)`.
- `:first`, `:left`, `:right` are print pseudo-classes (first page, left/right pages) [from source] (CSSHB p.34).
- `:root` points to the root element (in HTML, the `html`, but with higher specificity; in SVG, the `svg`) [from source] (CSSHB p.58-59).

## 5. Pseudo-elements

- They style a part of the element; they use two colons; the one-colon form exists for compatibility [from source] (CSSHB p.34).
- `::before` and `::after` insert content before/after via the `content` property (icons, text, `url()`) [from source] (CSSHB p.34-36). Without `content`, the rule generates nothing (`[inference]`; the `css_lint.py` script warns).
- `::first-line` (e.g. increase the font) and `::first-letter` (e.g. bold) [from source] (CSSHB p.35).
- The complete list of pseudo-elements is an image in the PDF (p.34-35): gap.
- Use in printing: add the address of links with `a:after { content: attr(href) }` [from source] (CSSHB p.210-211).

## 6. What the book does not cover (boundary)

There is no `:is()`, `:where()`, `:has()`, `:not()`, `:focus-visible`, `::marker`, rule nesting, or container selectors; confirmed by searching the extracted text. If the user asks, answer as `[extrapolation]` or say it is outside the material, without attributing it to the book.

## 7. MDN material (index)

MDN First Steps only enumerates, with a short description each, the lessons: basic selectors, attribute selectors, pseudo-classes and pseudo-elements, combinators, handling conflicts, etc. [from source] (MDNFS p.1-2). The body of the lessons is not in the PDFs.
