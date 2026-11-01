# Collective Wisdom: "97 Things Every Programmer Should Know - Extended" (97TH)

> Convention: pages = PDF page (see `INDEX.md`). Relation: printed page = PDF page - 8 (for example, printed 142 = PDF 150). Source: `97-Things-Every-Programmer-Should-Know.pdf` (151 pages).

## 0. What this PDF actually is (important correction)
- [from source] (97TH p.9) The text is the **"Extended" edition** compiled by Shirish Padalkar (Leanpub, version of 09/23/2014, p.2). The preface says the book gathers **68 additional essays** from the site *97 Things Every Programmer Should Know* that were NOT included in Kevlin Henney's book (O'Reilly). Each essay is licensed under Creative Commons Attribution 3.0 and individually authored.
- Consequence: the v1 package treated this PDF as "Kevlin Henney (Ed.), O'Reilly, 151 pages" and attributed the wrong authors to essays. Henney is the author of ONE essay here ("Restrict Mutability of State", p.108). The essays are cited below with the author printed in the PDF.
- The essays of the O'Reilly book (the "97") are not in this PDF. Any claim about them must be treated as [extrapolation] or declined.

## 1. Verified essays (author as printed)
- [from source] (97TH p.68-69) "Implicit Dependencies Are also Dependencies", Klaus Marquardt: told through the story of two teams that followed the protocol specification and still integrated poorly; the moral is that there are more dependencies than attempts at decoupling suggest; changing the meaning of a parameter is equivalent to changing the interface; "application dependencies" are the ones that matter. Note: the v1 package attributed it to Steve Berczuk and gave examples (`init()` before `process()`, environment variables, `/tmp/cache`) that do NOT appear in the essay.
- [from source] (97TH p.90-91) "Leave It in a Better State", Patrick Kua: asks how the process let the code get into a mess; proposes small improvements on each pass (rename a variable to a clearer name, add a small automated test, extract a method). The PDF does NOT use the expression "Boy Scout Rule" nor attribute the idea to Robert C. Martin. [extrapolation] "Boy Scout Rule" is the popular name (from Robert C. Martin) for the same idea and may be mentioned as general knowledge, without a page.
- [from source] (97TH p.108-109) "Restrict Mutability of State", Kevlin Henney: many defects stem from incorrect modification of state; immutability (immutable objects can be shared without concern for aliasing or synchronization; thread-safe by construction); `const` restricts access, it is not equivalent to immutability; copying values is another technique; make state local and declare variables as late as possible; resist mirroring every getter with a setter. The author says it is not a "silver bullet".
- [from source] (97TH p.150-151) "Write Code for Humans not Machines", Mario Fusco: carefully chosen names; readability tips with explicit numbers from the author: short methods ("15 lines of code is a reasonable upper limit"), one responsibility per method, at most about 3 parameters (more than that may justify grouping into an object), avoid nested loops and conditions, comment only when necessary, shared code standards. These numbers are the essay author's (97TH p.150), not from Code Complete nor from Google.
- [from source] (97TH p.116) "Small!", "Uncle Bob": example of a short function that reveals intent after extracting functions.
- [from source] (97TH p.125) "Talk about the Trade-offs", Michael Harmer: list of attributes to negotiate (correctness, modifiability, performance, speed of production, reusability, "approachability").
- [from source] (97TH p.131) "There Is No Such Thing as Self-Documenting Code", Carroll Robinson: every program needs comments; comment to complement the code, to explain the unusual (example of the function that traverses the array in reverse order).
- [from source] (97TH p.54) "Don't Use too Much Magic", Mario Fusco: abusing "convention over configuration" without knowing what happens underneath can lead to losing control of the application.
- [from source] (97TH p.50) "Don't Be too Sophisticated", Ralph Winzinger: the average team treats sophisticated code as "magic"; hide details and publish a simple API; bring the team along.
- [from source] (97TH p.114) "Simple Is not Simplistic", Giovanni Asproni: distinguishes simple from simplistic.
- [from source] (97TH p.98) "Programmers Who Write Tests Get More Time to Program", Johannes Brodwall: writing tests before code can improve design; example of reducing coupling to ease testing.
- [from source] (97TH p.146-147) "Work with a Star and Get Rid of the Truck Factor", Cecilia Sjolin and Ida Hveding Huse: pair rotation in pair programming (two-day rule; "rotation star") to spread knowledge and reduce the "truck factor". The v1 package cited p.138 (printed) for a story about a "lone genius" that is not in the essay.
- [from source] (97TH p.143) "Who Will Test the Tests Themselves?", Filip van Laenen: the third law of TDD is hard to follow in practice (example of the `max` of an array).

## 2. Literal quotes from the v1 package that do NOT exist in the PDF
- The v1 package delivered as literal English quotes: "Implicit dependencies are also dependencies" (exists only as a title), "Restrict mutability of state" (idem, title) and "Write code for humans not machines" (title). The Portuguese sentence attributed to the Boy Scout Rule ("leave the campground cleaner...") is not in the PDF.

## 3. Coverage
- The essays listed in the table of contents (PDF p.5-8) total 68; only 13 were read and cited here. The rest were not audited and may be consulted with `scripts/eng_lookup.py` only as "no detailed coverage".
