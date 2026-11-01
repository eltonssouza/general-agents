# Clean Code, Chapter 1 and Introduction (what the sample really contains)

Source: **CC** = *Clean Code: A Handbook of Agile Software Craftsmanship* (Robert C. Martin; credits page: Pearson Education, copyright 2009, cataloging 2008, CC p.4), **67-page sample**: table of contents, foreword, introduction, **Chapter 1** and index. Pages = **PDF**; printed page = N − 30 for the body (Ch. 1: PDF 31-45 = printed 1-15); the introduction uses Roman numerals (xxv to xxix = PDF 25-29). See `INDEX.md`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Introduction (CC p.25-27)
- "Clean" code depends on **craftsmanship**: knowledge of principles, patterns, practices and heuristics, plus hands-on work (bicycle analogy) `[from source] (CC p.26)`.
- The book has three parts: chapters on principles/patterns/practices, case studies of cleaning up code of increasing complexity, and a final chapter of heuristics and *smells* collected from the studies `[from source] (CC p.26-27)`. The "[H22]" references link decisions to the heuristics `[from source] (CC p.27)`.

## 2. Chapter 1: Clean Code (CC p.31-45)
- "There will always be code": code represents the details of the requirements; well-made specifications are as formal as code and can work as executable tests `[from source] (CC p.32)`.
- **Bad code** brings companies down: example of a product whose messy code prevented its evolution; "wading" through bad code; "Later equals never" (LeBlanc's law) `[from source] (CC p.33-34)`.
- **Total cost of owning a mess**: teams that are fast at first become slow; every change breaks other parts; productivity tends asymptotically to zero; adding people without knowing the design makes it worse `[from source] (CC p.34)`. The "grand redesign in the sky" (a tiger team racing the old system; the author saw it take 10 years) `[from source] (CC p.35)`.
- **Attitude**: the author puts the blame on the programmers' lack of professionalism, not on managers or deadlines; it is the programmer's duty to defend the code with the same passion with which managers defend the schedule (surgeon and hand-washing analogy) `[from source] (CC p.35-36)`.
- **Primal conundrum**: "they don't take the time to go fast"; the only way to meet the deadline is to keep the code as clean as possible at all times `[from source] (CC p.36)`. Writing clean code is like painting: recognizing good art does not teach you to paint; you need the "code sense" (*code-sense*) `[from source] (CC p.36-37)`.
- **What clean code is**: there is no single definition; the author gathers opinions `[from source] (CC p.37-42)`:
  - Bjarne Stroustrup: elegant and efficient, straightforward logic, minimal dependencies, complete error handling, performance close to optimal; "does one thing well" `[from source] (CC p.37)`; the broken windows metaphor (Thomas and Hunt) `[from source] (CC p.38)`.
  - Grady Booch: simple and direct, reads like well-written prose, crisp abstractions `[from source] (CC p.38-39)`.
  - "Big" Dave Thomas: readable and extensible by others, with unit and acceptance tests, meaningful names, one way of doing something, minimal dependencies; **"without tests, the code is not clean"** is the author's reading `[from source] (CC p.39)`.
  - Michael Feathers: care (*care*) `[from source] (CC p.40)`.
  - Ron Jeffries: Beck's simple code rules, in priority order (runs all the tests; no duplication; expresses the design ideas; minimizes the number of entities); focuses on duplication, expressiveness (names), `Extract Method` when something does more than one thing, and small abstractions `[from source] (CC p.40-41)`.
  - Ward Cunningham: each routine is "pretty much what you expected"; it is beautiful when the language looks made for the problem `[from source] (CC p.41-42)`.
- **Schools of thought**: the book is the "Object Mentor" school of clean code; the recommendations are presented as absolute out of conviction, but the author admits they are not absolutely right and that many are controversial `[from source] (CC p.42-43)`.
- **We are authors**: we read much more than we write (the reading:writing ratio is "well over 10:1"); therefore making reading easy makes writing easy `[from source] (CC p.43-44)`.
- **Boy Scout rule**: leave the campground cleaner than you found it; small improvements with each commit (renaming a variable, breaking up a large function, eliminating a duplication) `[from source] (CC p.44)`.
- **Prequel and principles**: the book is a prequel to *Agile Software Development: Principles, Patterns, and Practices* (PPP); it cites SRP, OCP and DIP as described there `[from source] (CC p.45)`. Conclusion: art books do not make anyone an artist; this one shows tools and thought processes `[from source] (CC p.45)`.

## 3. Overall table of contents of the book (CC p.7-17)
Chapters listed in the table of contents (printed): 1 Clean Code (1), 2 Meaningful Names (17), 3 Functions (31), 4 Comments (53), 5 Formatting (75), 6 Objects and Data Structures (93), 7 Error Handling (103), 8 Boundaries (113), 9 Unit Tests (121), 10 Classes (135), 11 Systems (153), 12 Emergence (171), 13 Concurrency (177), 14 Successive Refinement (193), 15 JUnit Internals (251), 16 Refactoring SerialDate (267), 17 Smells and Heuristics (285), Appendix A (317), Appendix C (409), Epilogue (411), Index (413) `[from source, table of contents only] (CC p.7-17)`. **Only Ch. 1 is present with text.**

## 4. What is NOT included (do not attribute)
- Rules for names (Ch. 2), functions (Ch. 3), comments, formatting, objects, error handling, classes, systems, emergence, concurrency, lists of G1-G36 *smells* etc.: **outside the sample** (see `clean-code-nomes-e-funcoes.md`).
- Numbers such as "20 lines per function" or "at most 3 arguments".
- `[DATED]` The work is from 2008/2009 (CC p.4); the mention of modern tools such as Eclipse (CC p.40) and of Emacs/editors of the 80s-90s (CC p.43) reflect that context.
