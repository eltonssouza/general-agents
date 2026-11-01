# Cap. 5 — Formatação (Formatting)

Source: CL ch. 5, PDF p.81-97 (opening on p.81; Listing 5-6 ends on p.97).

Pattern: bullets with a page are `[from source]`; exceptions are labeled.

## Opening and goal
- Sloppy code makes the reader assume sloppiness in the whole design; well-formatted code shows professionalism (CL p.81-82).
- Choose a set of simple rules and apply it consistently; in a team, everyone agrees on a single set; ideally an automated tool applies the rules (CL p.82).
- **The purpose of formatting**: formatting is too important to ignore and too important to treat religiously; it is communication, and communication is the first rule of the professional developer, not "making it work" (CL p.82).
- Functionality changes; readability affects every future change. Style and discipline survive even if the code does not (CL p.82).

## Vertical formatting: file size (Figure 5.1)
- In Java, file size is tied to class size; classes are left for Ch. 10 (CL p.82).
- Seven projects analyzed: JUnit, FitNesse, testNG, Time and Money, JDepend, Ant and Tomcat (CL p.82).
- Chart on a logarithmic scale; vertical lines = minimum and maximum; the box covers about one third of the files (one standard deviation), with the mean in the middle (CL p.82-83).
- FitNesse: average of about 65 lines; about one third of the files between 40 and 100+ lines; largest file about 400 lines, smallest 6 (CL p.82).
- JUnit, FitNesse and Time and Money: no file exceeds 500 lines and most have fewer than 200. Tomcat and Ant have files with thousands of lines, and nearly half exceed 200 (CL p.82).
- Conclusion: it is possible to build significant systems (FitNesse with almost 50,000 lines) with files of about 200 lines and a limit of 500. It is not a fixed rule, but small files are easier to understand (CL p.82).

## Vertical formatting: organization
- **The newspaper metaphor**: a simple, descriptive name as the headline; the top holds high-level concepts and algorithms; details increase as you go down, until the low-level functions at the end. A newspaper is made of many small articles (CL p.83).
- **Vertical openness between concepts**: each group of lines is a complete thought; separate thoughts with blank lines (between package, imports and each function). Compare Listing 5-1 with 5-2, without blank lines (CL p.83-84).
- **Vertical density**: closely related lines stay vertically together; useless comments between two instance variables break that proximity (Listings 5-3 and 5-4) (CL p.84-85).
- **Vertical distance**: closely related concepts stay vertically close [G10]; do not separate them into different files without a good reason, and this is one of the reasons to avoid protected variables. The distance should measure how important one is to understanding the other (CL p.85).
- **Variable declarations**: as close as possible to their use; in short functions, local variables at the top of the function (CL p.85). Loop control variables inside the iteration statement; rarely, at the start of a block or just before a loop in a long function (CL p.86).
- **Instance variables**: at the top of the class, in Java. In C++ there was the "scissors rule" (all at the bottom). What matters is a well-known place; bad example: JUnit 4.3.1's `TestSuite` with variables hidden in the middle of the class (CL p.86-87).
- **Dependent functions**: if one function calls another, keep them close, with the caller above the callee when possible (Listing 5-5, `WikiPageResponder`). The same excerpt shows the "FrontPage" constant kept at the appropriate level [G35] (CL p.87-89).
- **Conceptual affinity**: the greater the affinity, the smaller the vertical distance. Affinity comes from direct dependency or from functions that perform similar operations (the `assertTrue`/`assertFalse` family of JUnit 4.3.1, same naming convention) (CL p.89).
- **Vertical ordering**: call dependencies point downward; the called function sits below the caller, from high level to low level, as in the newspaper (CL p.89-90). This is the opposite of Pascal, C and C++, which require a definition or declaration before use (CL p.90).

## Horizontal formatting
- **Line width (Figure 5.2)**: across the seven projects, regularity is high, with lines around 45 characters; each width between 20 and 60 represents about 1% of the lines, adding up to 40%; perhaps another 30% have fewer than 10 characters; above 80 the drop is significant. Programmers prefer short lines (CL p.90).
- The old Hollerith limit of 80 is somewhat arbitrary; the author does not object to 100 or 120 characters, but going beyond that is probably carelessness (CL p.90).
- He abandoned the "never scroll to the right" rule because monitors are wide, and advises against shrinking the font to fit 200 characters: "Eu, pessoalmente, determinei 120 como meu limite." (I personally set 120 as my limit.) (CL p.90)
- **Horizontal openness and density**: white space associates what is related and separates what is weakly related. Spaces around the assignment operator; no space between the function name and the opening parenthesis; a space after the commas between arguments (CL p.91).
- Spacing also shows precedence: factors (multiplication) without spaces, terms (addition and subtraction) separated by spaces (`Quadratic` example). Reformatting tools tend to lose this subtlety (CL p.91).
- **Horizontal alignment**: the author abandoned aligning names and values in columns (assembly style): it draws attention to the wrong place and tools undo it. Long lists that "ask" for alignment indicate that the problem is the size of the list; the `FitNesseExpediter` class should be split (CL p.92-93).
- **Indentation**: the file is a hierarchy of scopes (file, class, method, block); indent each level one step to the right of its container. Without indentation the code is almost unintelligible (`FitNesseServer` example with and without indentation) (CL p.93-94).
- **Breaking indentation**: avoid collapsing short `if`s, small `while`s or short functions onto one line; the author always ends up going back to expand and indent (`CommentWidget` example) (CL p.94).
- **Dummy scopes**: avoid empty `while`/`for` bodies; if unavoidable, indent and put the semicolon on its own line, since a `;` at the end of the `while` line is deceptive (CL p.95).

## Team rules and Uncle Bob's rules
- **Team rules**: each programmer has preferences, but in a team the rules are the team's; a single style, used by everyone, so the code does not look like it was written by people in disagreement (CL p.95).
- In FitNesse, in 2002, the team chose the style in 10 minutes (brace position, indentation size, names of classes, variables and methods), configured the IDE formatter, and the author followed rules that were not his preferred ones (CL p.95).
- The reader must be able to trust that a formatting means the same thing in all files (CL p.95).
- **Uncle Bob's formatting rules**: the author's rules are simple and illustrated in the code of Listing 5-6 (`CodeAnalyzer.java`); the code is the best coding standard document (CL p.95-97).

## Examples from the book
- Figure 5.1 (p.83): file size distribution, log scale, seven projects. Figure 5.2 (p.90): line width distribution in Java.
- Listings 5-1/5-2 (`BoldWidget.java`, p.83-84): the same code with and without blank lines.
- Listings 5-3/5-4 (`ReporterConfig`, p.84-85): useless javadocs breaking vertical density.
- JUnit 4.3.1 and TestNG excerpts (p.85-87): position of local, loop and instance variables.
- Listing 5-5 (`WikiPageResponder.java`, p.88): dependent functions ordered top to bottom; the book cites Listings 15-5 and 3-7 as even better examples (p.90).
- JUnit `Assert` (p.89): conceptual affinity. `Quadratic` (p.91): spaces and precedence.
- `FitNesseExpediter` (p.92-93): aligned vs. unaligned. `FitNesseServer` (p.93-94): with and without indentation. `CommentWidget` (p.94).
- Listing 5-6 (`CodeAnalyzer.java`, p.96-97): the author's style in code.

## What the chapter does NOT say / common confusions
- It does not fix 80 columns: it calls the Hollerith limit arbitrary and uses 120 as a personal limit (CL p.90).
- 200/500 lines per file is not a "fixed rule"; it is an observation about the projects analyzed (CL p.82).
- It does not prescribe tabs vs. spaces, nor indentation size (2 or 4); the size is a team decision (CL p.95). `[inference]`
- It does not say that brace position has a right form; Listing 5-6 shows the author's preference, not a universal standard (CL p.95). `[inference]`
- It does not cite specific linters or formatters; it talks about an "automated tool" and the IDE formatter (CL p.82, p.95). `[inference]`
- The "Stepdown Rule" is from Ch. 3 (CL p.46); here the equivalent topic is called "Vertical ordering" (CL p.89). `[inference]`

## [DATED]
- 2008 data from seven Java projects (JUnit, FitNesse, testNG, Time and Money, JDepend, Ant, Tomcat) (CL p.82, p.90). `[DATED]`
- Examples with JUnit 4.3.1 and TestNG of that period (CL p.85-89). `[DATED]`
- Remarks about wide monitors and reformatting tools that destroy alignment or precedence-based spacing (CL p.90-92) reflect the IDEs of 2008. `[DATED]`
