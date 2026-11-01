# Source and identification of the work (front matter)

Source: CL front matter, PDF p.1-10 (cover, preface, introduction, acknowledgments, "Sobre a capa" — "About the cover").
Convention: `(CL p.N)` = page of the scanned PDF, never the printed page.

## What the cover (p.1) shows
- Title: *Código Limpo*; subtitle: *Habilidades Práticas do Agile Software* (CL p.1).
- Top line: "Série de Robert C. Martin" (Robert C. Martin Series) (CL p.1). The author's name appears only as the series name; there is no
  separate authorship line on the scanned cover [inference, checked against the image].
- Logo of the publisher Alta Books in the upper right corner, visible in the image but not captured by OCR
  (CL p.1) [from source, checked against the image].
- Background image: the galaxy M104 (Sombrero), explained in "Sobre a capa" (CL p.10).

## What is NOT in the scan (confirmed)
- There is no title page, cataloging data page, credits page, ISBN, edition year, or translator's name
  on p.1-11; Grep over the whole text does not find "ISBN", "2009", "Alta Books" (only in the logo, outside the OCR),
  or a translation credit (CL p.1-11) [inference from the Grep and the images].
- There is no table of contents: after the cover (p.1) comes the Preface directly (p.2) (CL p.1-2).
- The original English title (*Clean Code*) does not appear in the text (Grep: zero occurrences).
- When citing the work, use the data present (title, subtitle, series, publisher via the logo) and say that
  year, ISBN, and translator are not in the PDF. Any editorial data beyond that is [extrapolation].

## Preface (p.2-6)
- The preface is signed by James O. Coplien, of Mordrup, Denmark (CL p.6).
- Motto: a Danish saying printed on a Ga-Jol candy box, about honesty in small things;
  the central idea is that details matter (CL p.2).
- It cites Mies van der Rohe ("God is in the details") and the door handles chosen one by one (CL p.2).
- It says that 80% or more of the work in software is maintenance and links the book to Total Productive Maintenance
  (TPM, c. 1951) and to the 5S (CL p.3).
- The 5S and their reading for code (CL p.3):
  - Seiri (organization): knowing where things are, for example through proper names.
  - Seiton (tidiness): code should be where you expect to find it; if it is not, refactor.
  - Seiso (cleaning): removing comments and commented-out code that only keep the past or wishes.
  - Seiketsu (standardization): the team agrees to keep the place clean (consistent style).
  - Shutsuke (discipline): following the practices, reflecting on them, and accepting change.
- It cites Fred Brooks: redoing major parts of the software every seven years (CL p.3-4).
- It reports Bell Labs research: a consistent indentation style was one of the most statistically
  significant indicators of few bugs (CL p.4-5).
- It argues for refactoring as part of "Done" in Scrum and for honesty about the state of the code (CL p.5).

## Introduction (p.7-9)
- It opens with a figure of the two code-review doors: "Good code" with few "WTF" and "Bad code" with
  many; the handwritten title, in English, says the only valid measure of quality is WTFs/minute
  (CL p.7) [from source, checked against the image; the figure's text is not captured by OCR].
- The figure is reproduced with permission from Thom Holwerda, (c) 2008 Focus Shift (CL p.7).
- The answer to standing behind the right door: professional skill, which has two strands,
  knowledge and work (CL p.7).
- Bicycle analogy: knowing the physics does not prevent a fall on the first try (CL p.8).
- Organization in three parts (CL p.8):
  1. principles, patterns, and practices for writing clean code (a lot of code);
  2. case studies of increasing complexity, each one a cleanup exercise;
  3. a single chapter with a list of heuristics and "smells" gathered from the case studies.
- In the case studies, the heuristics are cited by the code in brackets (the OCR garbled the printed
  example; in the body of the book forms such as [N5], [G23] appear) and there is a cross-reference at the end of the book
  with the page of each use (CL p.8; CL p.31, p.47).
- Reading only the first and third parts is still worthwhile, but the author says the real gain comes from following the
  case studies step by step (CL p.8-9).

## Acknowledgments and cover (p.9-10)
- Illustrations by Jeniffer Kohnke (chapter openers and portraits of Kent Beck, Ward Cunningham, Bjarne
  Stroustrup, Ron Jeffries, Grady Booch, Dave Thomas, Michael Feathers, and the author) and Angela Brooks, the author's
  daughter (CL p.9).
- "Sobre a capa" (About the cover): M104, an image combining a Hubble photo (visible light) and a Spitzer photo (infrared)
  (CL p.10).

## Chapter contributors (outside the range, for identification)
- Ch. 2 is "por Tim Ottinger" (by Tim Ottinger) (CL p.26). Other chapters carry credits for Michael Feathers (CL p.107),
  James Grenning (CL p.117), Dr. Kevin Dean Wampler (CL p.152), Jeff Langr (CL p.168), and Brett L. Schuchert
  (CL p.174, p.310). The topics of those chapters belong to the other groups.
- The author calls himself "Tio Bob" (Uncle Bob) in Ch. 1 (CL p.22); the preface uses "Uncle Bob" (CL p.3, p.6).
- The book presents itself as the "Escola de Código Limpo da Object Mentor" (Object Mentor School of Clean Code) (CL p.22).

## What this part does NOT say / common confusions
- The WTFs/minute figure is not the author's: it is by Thom Holwerda (CL p.7).
- The preface is not by Robert C. Martin or Kent Beck: it is by James O. Coplien (CL p.6).
- The book is not organized by "SOLID principles": the word SOLID does not appear on any page (Grep).

## [DATED]
- The date of the figure (2008) and the references to Scrum/Agile of the late 2000s place the work; the PDF does not
  carry the date of the Brazilian edition (CL p.7) [inference].
