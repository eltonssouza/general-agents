# Clean Architecture (2011 post): hiding the UI, framework and database from the application

Source: Robert C. Martin, **"Clean Architecture"**, post on The Clean Code Blog, November 22, 2011 (acronym `CA11`; 15-page PDF, browser printout).

> **Important correction relative to the previous version of the package.** The file `Clean-Architecture-UncleBob-2011.pdf` is **not** the essay "Architecture: The Lost Years" and does **not** contain the text of the post "Screaming Architecture". Pages p.1-5 contain the 11/22/2011 post (a response to the resistance to the idea of decoupling); pages p.6-15 are **only the blog sidebar** (a list of titles and dates of other posts). Titles such as "Screaming Architecture" (09/30/2011) appear only as an item in the sidebar list (last page of the PDF), with no content. Everything the old package attributed to `CA11 p.6-13` (the house/library blueprint metaphor, "the Web is an I/O device", use cases as the "center of the universe", Rails/Spring/Django in the directory tree) **is not in this PDF** and was removed or downgraded.

**Page convention**: `(CA11 p.N)` = PDF page. There is no printed numbering; the useful content is on p.1-5. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

---

## 1. What the post actually says

1. **Motivation (p.1)**: Martin notes "resistance" to the idea that it is good to hide the framework, UI or database from the application code `[from source] (CA11 p.1)`. He cites a critic (the blog "coding {the} architecture"), whose thesis is that if the UI and database are much larger parts than the business rules, the architecture should be oriented around them; Martin disagrees: however large a part is, the others should be decoupled from it `[from source] (CA11 p.1)`.
2. **The "Rails is special" objection (p.1-2)**: he was asked whether he had ever done this on a Rails project, as if the framework changed the rules of good design `[from source] (CA11 p.2)`.
3. **Fear of duplication (p.2)**: some people fear duplicated code and routine copying of data between structures across layers. Martin says he does not want that and that nothing he suggests inevitably leads to repeated structures and excessive field copying `[from source] (CA11 p.2)`.
4. **"It's not rocket science" (p.2)**: the basic idea is to separate the UI from the business rules by passing **simple data structures** between the two. Controllers do not know the business rules: they unpack the `HttpRequest` into a simple data structure and pass it to an *interactor* object that implements the use case by invoking business objects; the interactor gathers the response data into another simple structure and returns it to the UI; the views do not know the business objects, they only look at the response structure `[from source] (CA11 p.2)`.
5. **Benefits (p.2-3)**: the application code becomes completely decoupled from the UI; it can be tested without the UI, without starting a web server, a container or Rails; and if the UI is not satisfactory, it can be replaced by another `[from source] (CA11 p.2-3)`. Martin admits the scheme is not perfect: one kind of UI may be so different from another that they do not share a common interface `[from source] (CA11 p.3)`.
6. **"It will slow me down" (p.3)**: Martin replies that it speeds things up: tests run with no waiting and decisions about the UI can be deferred `[from source] (CA11 p.3)`.
7. **Deferring decisions (p.3-4)**: a good architecture *allows* deferring critical decisions (UI, frameworks, database), but does **not require** it. He agrees that agile practices call for thin, long slices cutting through the whole architecture, and says thin slices need not be coupled; he gives the example of a simple interim UI in the first sprints, replaced later `[from source] (CA11 p.3-4)`.
8. **Convention over configuration (p.4)**: he agrees with the Rails mantra, but conventions do not imply coupling; there is no reason for Rails models to contain business rule methods; keeping rules separate from ActiveRecord derivatives does not violate Rails conventions, and even if it did, he thinks **decoupling is worth more than convention** `[from source] (CA11 p.4)`.
9. **GOOS (p.4)**: he does not use the outside-in methodology of *Growing Object Oriented Software*; he prefers inside-out (business rules first, UI afterward), and considers the UI an "irritating detail"; he says there is nothing in GOOS against decoupling the rules from the UI `[from source] (CA11 p.4)`.
10. **Big Up Front Design? (p.5)**: no. Decoupling is done while writing the code and getting the tests to pass; he does not want months of UML, but accepts a few hours or a day or two of thought about the shape of the system `[from source] (CA11 p.5)`.
11. **"This is not new" (p.5)**: the ideas are old and come from people such as David Parnas, Tom DeMarco, Grady Booch and Ivar Jacobson; he wonders how he forgot the rules of coupling and cohesion `[from source] (CA11 p.5)`.

## 2. How to use this content

- For the **circle structure and the Dependency Rule**, use `CA12` (file `regras-de-dependencia-e-circulos-concentricos.md`): the 2011 post does not present the diagram or the four circles.
- The formula "controller -> interactor -> simple structures -> view" of `CA11 p.2` is the **embryo** of the flow detailed in `CA12 p.5-6` `[inference]`.
- "Testing without starting the web server" is supported by `CA11 p.2-3` (and, in other words, `CA12 p.2`). The formulation "100% of unit tests without web" is **not in** the PDFs `[extrapolation]`.

## 3. What is NOT in the CA11 PDF (use only as `[extrapolation]` or `not_in_book`)

- The title "Architecture: The Lost Years" (talk/essay) and its text.
- The post "Screaming Architecture" and the idea of the folder structure "screaming" the domain (only the title appears in the sidebar list, p.15; and `CA12 p.2` mentions it as a reference, without explaining it).
- The phrase "the Web is a delivery mechanism/I/O device", the house and library blueprint metaphor, Rails/Django/Spring MVC as a directory-tree case study, the term "Interactor" with a formal definition (it appears only within the description of the flow, p.2).
- Any claim that the database "is a detail" **in this PDF**: the equivalent claim exists in `CA12 p.5` ("the Web is a detail, the database is a detail").

## 4. [DATED]

Examples (Rails, ActiveRecord, `HttpRequest`, GOOS) reflect the 2011 context `[DATED]`. The principles (decoupling business rules from the UI and database) are applied today to other stacks by `[extrapolation]`.
