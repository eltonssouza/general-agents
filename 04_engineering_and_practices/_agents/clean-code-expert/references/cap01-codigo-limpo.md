# Chapter 1: Clean Code

Source: CL ch. 1, PDF p.11-25 (chapter opening on p.11; p.12 is the first with the header
"Capítulo 1"; bibliography on p.25).

## Why code will not go away
- Code represents the details of the requirements; specifying requirements precisely enough for a
  machine to execute is programming, and that specification is code (CL p.12).
- Higher-level and domain-specific languages are welcome, but what is written in them is also
  code, and must be precise and formal (CL p.12).
- Well-specified requirements are as formal as code and can serve as executable tests (CL p.12).

## Bad code and its cost
- Account of a company from the 1980s that went under: rushed release, messy code, each feature
  made everything worse until it became impossible to manage (CL p.13).
- We have all left a mess to clean up later; the book cites LeBlanc's law, translated as
  "Nunca é tarde" (literally "It is never too late") (CL p.13). From the context, the intended meaning is that "later" never comes
  [inference: the printed translation inverts the apparent meaning; see notes.md].
- As the mess grows, each change breaks two or three other parts and productivity drops
  asymptotically toward zero (Figure 1.1, productivity x time) (CL p.14).
- Management reacts by adding more people, who do not know the project and increase the confusion (CL p.14).
- The Grand Redesign: a new team rewrites the system while the old one maintains the old one; the race
  can last years (the author says he saw one that lasted 10 years) and ends in a new mess (CL p.15).
- Cleaning the code is not only cost-effective: it is a matter of professional survival (CL p.15).

## Professional attitude
- The blame for the mess lies with the programmers, not with requirements, deadlines, or managers: we are professionals and
  must tell the truth about risks (CL p.15).
- Managers defend deadlines and requirements passionately; the programmer must defend the code with the same
  passion (CL p.16).
- Analogy of the doctor who does not stop washing his hands just because the patient asks (Semmelweis, footnote)
  (CL p.16).
- The Primal Conundrum: the mess does not help meet deadlines; the only way to go fast is to keep the code
  clean at all times (CL p.16).
- Recognizing bad code is not enough: you need *code sense*, which shows alternatives and the
  sequence of transformations to reach clean code (CL p.16-17).

## What clean code is: the guests' definitions (p.17-21)
Paraphrases; the portraits and quotes appear on the pages indicated.
- **Bjarne Stroustrup** (creator of C++): elegant and efficient code; straightforward logic so bugs cannot
  hide; minimal dependencies; complete error handling following a clear strategy; performance
  close to optimal so as not to tempt people into messy optimizations; clean code does one thing well (CL p.17).
  - Author's comment: bad code invites chaos (broken windows, by Dave Thomas and Andy Hunt)
    (CL p.17); complete error handling = attention to detail (CL p.18); "do one thing" sums up
    many principles: each function, class, and module with a single task (CL p.18).
- **Grady Booch**: clean code is simple and direct and reads like well-written prose; it does not hide the author's
  intent; it has clear abstractions and direct control (CL p.18).
- **"Big" Dave Thomas** (founder of OTI, Eclipse): a developer other than the author can read and
  improve the code; it has unit and acceptance tests; meaningful names; one way of doing
  each thing; few dependencies, explicit; minimal, clear API; "literate" code (CL p.19).
  - Author's comment: code without tests is not clean, no matter how elegant (CL p.19).
- **Michael Feathers**: clean code always looks like it was written by someone who cared; there is no
  obvious improvement to make. Author's summary: *care* (CL p.19-20).
- **Ron Jeffries**: follows Kent Beck's simple code rules, in priority order (CL p.20):
  1. runs all the tests;
  2. contains no duplication;
  3. expresses all the design ideas of the system;
  4. minimizes the number of entities (classes, methods, functions).
  Ron focuses on duplication and expressiveness (names, Extract Method, objects with more than one task split)
  and on creating simple abstractions early, such as hiding collection lookups behind a method/class (CL p.20).
  The author says Ron summed up the book: no duplication, one task, expressiveness, small abstractions
  (CL p.20).
- **Ward Cunningham**: you know your code is clean when each routine you read is pretty much what you
  expected; it is beautiful when it makes it look like the language was made for the problem (CL p.21).
  - Author's comment: it is not the language that makes the program look simple, it is the programmer (CL p.21).

## Schools of thought
- What the book presents is the *Object Mentor School of Clean Code*, presented as absolute to the
  authors, but without any claim to being 100% right; other schools also have value (CL p.22).
- Many of the book's recommendations are contradictory and the reader may disagree with some of them (CL p.22).

## We are authors
- The Javadoc @author field reminds us that we are authors with readers (CL p.23).
- When replaying editing sessions, most of it is reading and navigating; the printed reading:writing ratio is 10x1
  (OCR: "I OXI"; checked against the image) (CL p.23).
- So making the code easy to read makes it easy to write (CL p.23).

## The Boy Scout Rule
- It is not enough to write well: the code must be kept clean over time (CL p.24).
- Boy Scouts of America rule: "Leave the campground cleaner than you found it"
  (CL p.24).
- The cleanup can be small: renaming a variable, splitting a large function, eliminating a bit of
  repetition, reducing a nested if (CL p.24).
- A footnote attributes the origin to a farewell message from Baden-Powell (text partially cut off
  in the scan) (CL p.24).

## Prequel and principles
- The book is a *prequel* to *Agile Software Development: Principles, Patterns, and Practices* (PPP, 2002)
  (CL p.24).
- There are sporadic references to design principles, with English acronyms: SRP, OCP, and DIP, described in
  detail in the PPP (CL p.24). The printed translation calls the DIP "Princípio da Inversão da Independência"
  (literally "Independence Inversion Principle") (CL p.24) [the usual name is Dependency Inversion: extrapolation].

## Conclusion
- Art books do not make artists; this book shows techniques and the line of thinking of good
  programmers, and the rest is practice (the violinist joke: practice) (CL p.24-25).

## Examples from the book
- Figure 1.1: productivity curve falling over time (CL p.14).
- Italic list narrating a replayed editing session to show how much
  is read (CL p.23).
- There are no code listings in this chapter.

## What the chapter does NOT say / common confusions
- It does not use the acronym SOLID; it cites only SRP, OCP, and DIP, "among others" (CL p.24). LSP and ISP are not
  named (Grep over the whole book: zero occurrences).
- The four simple code rules appear here in Ron Jeffries's voice, attributed to Kent Beck
  (CL p.20); the chapter on emergence comes from a different group.
- The broken windows phrase is attributed to Dave Thomas and Andy Hunt (Pragmatic), not to Bjarne (CL p.17).
- The Dave Thomas cited is the founder of OTI, not the coauthor of The Pragmatic Programmer (the book calls him
  "grande" — "big" — Dave Thomas) (CL p.19) [inference from the caption].
- "10x1" is the printed reading/writing ratio; the book gives no research source for it (CL p.23).

## [DATED]
- Tools cited as modern: Emacs (keystroke recording in the 1980s-1990s) and Eclipse for
  renaming (CL p.20, p.23).
- "Ten years ago" about TDD refers to the late 1990s (CL p.19).
