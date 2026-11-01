# Ch. 4 — Comments

Source: CL ch. 4, PDF p.59-80 (opening with an epigraph from Kernighan and Plaugher on p.59; bibliography on p.80).

Convention: bullets with a page are `[from source]`; exceptions are labeled.

## Central thesis
- Comments are, at best, a "necessary evil"; with expressive languages and mastery of them, they would hardly be needed (CL p.59).
- The proper use of a comment is to make up for our failure to express ourselves in code: "Comments are always failures." (printed: "Comentários são sempre fracassos.") (CL p.60)
- Before commenting, try to express the idea in the code itself; commenting should be the exception (CL p.60).
- Comments lie over time: the older they are and the farther from the code they describe, the greater the chance they are wrong, since nobody keeps them up to date (CL p.60).
- Inaccurate comments are far worse than no comments at all (CL p.60).
- "The truth can only be found in one place: the code." (printed: "Só se pode encontrar a verdade em um lugar: no código.") (CL p.60)
- **Comments Do Not Make Up for Bad Code** (printed: "Comentários Compensam um Código Ruim"): the most common motivation for commenting is confusing code; instead of commenting the mess, clean it up (CL p.60-61).
- **Explain yourself in code** (printed: "Explique-se no código"): in many cases it is enough to create a function whose name says what the comment would say (e.g., replacing the commented condition with `isEligibleForFullBenefits()`) (CL p.61).

## Good Comments (section "Comentários Bons", CL p.61-65)
The author's caveat: the only truly good comment is the one you found a way not to write (CL p.61).

1. **Legal Comments** — copyright and authorship required by corporate standards, at the start of the file; they should not become contracts: prefer to reference a standard license or external document (CL p.61).
2. **Informative Comments** — useful basic information (e.g., value returned by an abstract method; format expected by a regex); even so, prefer a function name that carries the information or moving the code to its own class (CL p.62).
3. **Explanation of Intent** — the comment explains the reason behind a decision (e.g., `compareTo` that declares itself "greater" than other types; test that tries to force a race condition with many threads) (CL p.62-63).
4. **Clarification** — translates an obscure argument or return value when it belongs to the standard library or to code that cannot be changed; high risk of being wrong, so verify its accuracy (CL p.63).
5. **Warning of Consequences** — warns other programmers (e.g., test that takes a long time; `SimpleDateFormat` is not thread-safe, create an instance per call) (CL p.64).
6. **TODO Comments** — `// TODO` notes for tasks that cannot be done now; they do not justify leaving bad code; look for them regularly and eliminate the ones you can (CL p.64-65).
7. **Amplification** — stresses the importance of something that seems irrelevant (e.g., why the `trim()` matters) (CL p.65).
8. **Javadocs in Public APIs** — write good javadocs for a public API, but they can be as misleading, nonlocal, and dishonest as any other comment (CL p.65).

## Bad Comments (section "Comentários Ruins", CL p.65-77)
Most comments fall into this category: crutches or excuses for bad code (CL p.65). Names follow the headings of the Brazilian edition:

1. **Mumbling** (printed "Murmúrio") — a comment made only because you "should" or because the process requires it; if you are going to comment, do it well. Example: empty `catch` with a cryptic comment about "default values loaded"; if the reader has to open another module to understand, the comment failed (CL p.65-66).
2. **Redundant Comments** — say the same as the code and take longer to read than it (Listing 4-1); useless variable javadocs in Tomcat (Listing 4-2) (CL p.66-68).
3. **Misleading Comments** — inaccurate statement: the comment in Listing 4-1 suggests the method returns when `this.closed` becomes true, but it waits for a timeout and throws an exception (CL p.69).
4. **Mandated Comments** — a rule that every function must have a Javadoc or every variable a comment is silly; it produces abominations such as Listing 4-3 (obvious `@param`) (CL p.69).
5. **Journal Comments** — change log accumulated at the top of the module, like a diary; today version control does this, remove them (CL p.69-70).
6. **Noise Comments** — state the obvious ("Default constructor", "The day of the month"); we learn to ignore them and they start to lie. Instead of venting in a comment (Listing 4-4), refactor (Listing 4-5) (CL p.70-72).
7. **Scary noise** — noisy javadocs with a cut-and-paste error in a well-known library; if the author does not pay attention, the reader should not expect anything from them (CL p.72).
8. **Don't use a comment when you can use a function or a variable** — extracting explanatory variables (`moduleDependees`, `ourSubSystem`) eliminates the comment (CL p.72-73).
9. **Position Markers** — banners such as `// Actions /////`; rarely useful, use sparingly or they become noise; remove the slashes especially (CL p.73).
10. **Closing Brace Comments** — `} //while`; if you feel like writing them, shorten the functions (Listing 4-6, `wc.java`) (CL p.73-74).
11. **Attributions and Bylines** — `/* Added by Rick */`; version control keeps track of who did what (CL p.74).
12. **Code explanation in comments** (printed "Explicação do código em comentários") — the heading translates the original *Commented-Out Code*: it is about **commented-out code** (lines of code disabled with `//`). Nobody has the courage to delete it; delete it, version control remembers (CL p.74-75).
13. **HTML Comments** — HTML in comments makes reading in the editor harder; formatting for the web is the job of the tool (e.g., Javadoc) (CL p.75).
14. **Nonlocal Information** — the comment should stay next to the code it describes; do not describe system information (e.g., default port) in a local comment (CL p.75).
15. **Too Much Information** — no historical discussions or irrelevant details (e.g., excerpt of RFC 2045 about base64; the RFC number would suffice) (CL p.76).
16. **Inobvious Connection** — the connection between comment and code should be obvious; a comment that needs explaining has failed (e.g., "filter bytes", "+1", "*3", "200") (CL p.76).
17. **Function Headers** — short functions need no explanation; a good name is better than a header comment (CL p.76).
18. **Javadocs in Nonpublic Code** — Javadoc formality in internal code is clutter and distraction (CL p.77).

## Examples from the book
- p.60: a comment that ended up far from the `HTTP_DATE_REGEXP` constant because variables were inserted between them.
- p.61: employee benefits condition replaced by `isEligibleForFullBenefits()`.
- p.62-65: one short example for each type of good comment (FitNesse, JUnit, `SimpleDateFormat`, `ListItemWidget`).
- p.66-68: Listing 4-1 (`waitForClose`, redundant and misleading) and Listing 4-2 (`ContainerBase.java`, Tomcat, useless javadocs).
- p.69: Listing 4-3 (`addCD` with mandated `@param`). p.70: module changelog (journal).
- p.71-72: Listing 4-4 (`startSending` with "Give me a break!") and Listing 4-5 (refactored, extracting `addExceptionAndCloseResponse`).
- p.73-74: Listing 4-6 (`wc.java`, closing brace comments); commented-out code in Apache Commons (p.74).
- p.77-80 (**Example**): Listing 4-7 `GeneratePrimes.java`, created for the first XP Immersion as an example of bad programming and comments; it would previously have been considered "well documented". Kent Beck refactored the module in front of students, and the author later adapted it for another book and an article in the Craftsman column. Listing 4-8 `PrimeGenerator.java` (refactored version) with only two comments: the algorithm header (redundant, but kept because it eases reading) and the justification of the square root as the iteration limit (practically necessary). The author still questions whether the square-root optimization is worth the effort of understanding it (CL p.77-80).

## What the chapter does NOT say / common confusions
- It does not say "never write comments": it lists 8 categories of good comments (CL p.61-65). `[inference]`
- "Explicação do código em comentários" ("code explanation in comments", p.74) is **not** about explaining code in prose; it is the item about commented-out code, a misleading translation. `[inference]` (CL p.74)
- It does not condemn Javadoc in general: only in nonpublic code (p.77) and when imposed by rule (p.69); for public APIs it is recommended (p.65).
- It does not forbid TODO; it asks for periodic review (CL p.65).
- It defines no minimum or maximum comment size, nor style (`//` vs `/* */`). `[inference]`
- It does not discuss docstrings, linters, or specific tools beyond IDEs, Javadoc, and version control. `[inference]`
- The Ch. 17 heuristics about comments use other names (C1 Inappropriate Information, C2 Obsolete Comment, C3 Redundant Comment, C4 Poorly Written Comment, C5 Commented-Out Code) (CL p.281-282).

## [DATED]
- JUnit 4 `@Ignore` cited as "nowadays" for disabling a test; before, a `_` prefix on the method name (JUnit 3) (CL p.64). `[DATED]`
- Javadoc and HTML in comments as the reference for Java API documentation (CL p.65, p.75). `[DATED]` partially: the principle holds; the tool is from 2008.
- Source control systems presented as the reason to remove changelogs, bylines, and commented-out code (CL p.70, p.74-75): still valid.
