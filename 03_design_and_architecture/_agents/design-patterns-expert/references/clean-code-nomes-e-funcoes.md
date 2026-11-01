# Clean Code, chapters 2 (Names) and 3 (Functions): what the sample does NOT allow us to state

**Central warning.** The PDF `Clean-Code-SampleChapter-Pearson.pdf` (67 pages) is a **sample** with cover, table of contents, foreword, introduction, the whole **Chapter 1** and the **Index**. **Chapters 2 (*Meaningful Names*) and 3 (*Functions*) are not in the PDF.** Therefore no rule on names or functions can be given as `[from source]` from this source: one can only state that the **topic exists**, based on the table of contents and the index. Earlier versions of this package attributed to the book rules such as "fewer than 20 lines", "maximum of 3 arguments", "ban on flag arguments", with pages that the sample does not contain; this was removed (see `tests/relatorio-de-fidelidade.md`).

Page convention: `(CC p.N)` = **PDF page**. For the body of the book, printed page = N − 30 (printed Chapter 1 p.1 is on PDF p.31). Citations from the table of contents/index carry the **printed page of the full book** in parentheses, which the PDF shows but whose content it does not provide.

## 1. What the table of contents proves (CC p.7-9)
The table of contents lists the subheadings below. This proves the existence of the topic and its printed page in the full book, **not** the content.

| Chapter / section | Printed (full book) | Where it appears in the PDF |
|---|---|---|
| Ch. 2 *Meaningful Names*: Use Intention-Revealing Names, Avoid Disinformation, Make Meaningful Distinctions, Use Pronounceable Names, Use Searchable Names | 17-22 | `[from source, table of contents only] (CC p.7)` |
| Avoid Encodings (Hungarian Notation, Member Prefixes, Interfaces and Implementations), Avoid Mental Mapping, Class Names, Method Names, Don't Be Cute, Pick One Word per Concept, Don't Pun, Solution/Problem Domain Names, Add Meaningful Context | 23-30 | `[from source, table of contents only] (CC p.8)` |
| Ch. 3 *Functions*: Small!, Blocks and Indenting, Do One Thing, Sections within Functions, One Level of Abstraction per Function, Stepdown Rule, Switch Statements, Use Descriptive Names | 31-39 | `[from source, table of contents only] (CC p.8)` |
| Function Arguments (Common Monadic Forms, Flag Arguments, Dyadic Functions, Triads, Argument Objects, Argument Lists, Verbs and Keywords), Have No Side Effects, Output Arguments, Command Query Separation | 40-45 | `[from source, table of contents only] (CC p.8)` |
| Prefer Exceptions to Returning Error Codes, Extract Try/Catch Blocks, Error Handling Is One Thing, The Error.java Dependency Magnet, Don't Repeat Yourself, Structured Programming, How Do You Write Functions Like This?, SetupTeardownIncluder | 46-52 | `[from source, table of contents only] (CC p.9)` |

## 2. What the index proves (CC p.47-65)
The index (PDF p.47-65, printed 413-431) contains entries such as: "argument(s) flag, 41", "monadic/dyadic/triadic/niladic argument, 40", "commands, separating from queries, 45-46", "one thing, functions doing, 35-36", "single-letter names, 22, 25", "Hungarian notation", "try/catch blocks, 46-47", "duplication of code, 48" `[from source, index only] (CC p.48, 50, 53, 54, 55, 59, 62, 64)`. They confirm that the full book covers these topics on the printed pages cited, but they do **not** say what it recommends.

## 3. What Chapter 1 (present) lets us say
See `clean-code-capitulo-1.md`. It contains, for example, Ron Jeffries' quote about methods that do more than one thing and the Boy Scout rule `[from source] (CC p.40-41, 44)`; and "Clean code does one thing well" in Stroustrup's definition `[from source] (CC p.37-38)`. This is the most the sample supports about "doing just one thing".

## 4. General knowledge (outside the PDF), always labeled
The points below are widely disseminated practices on names and functions. They appear here because they are useful, but they are **not verifiable in this source** and must not carry `[from source]`.
- `[extrapolation]` Names should reveal intent, avoid disinformation and type encodings (Hungarian notation, member prefixes), and be pronounceable and searchable.
- `[extrapolation]` Functions should be small, do one thing, at one level of abstraction, with few arguments; boolean arguments (*flag arguments*) tend to indicate that the function does two things; command-query separation; exceptions instead of error codes.
- `[extrapolation]` Numeric limits (lines per function, number of arguments, indentation levels) are **heuristics**; any number cited as a "rule of the book" must be checked against the full book.
- `[DATED]` The work is from 2008/2009 (CC p.4); recommendations sensitive to the tools and languages of the time should be reassessed.

## 5. How the agent should answer
- Question about a rule from Ch. 2 or 3: confirm that the topic appears in the table of contents (with the printed page) and say that the sample does not include the text; give the general guidance as `[extrapolation]`.
- Never cite `(CC p.17-50)` as `[from source]` for chapter content. Ask the user for the text or the full PDF if the exact statement is needed.
