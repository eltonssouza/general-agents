# The 17 rules of the Unix philosophy (TAUP ch. 1)

Source: Eric S. Raymond, *The Art of Unix Programming* (TAUP), ch. 1 "Philosophy" (PDF p.27-53). **Convention: PDF page; printed page = PDF − 2** (verified in the footers of PDF p.27-549). The quotations below are paraphrases; the statement of each rule appears in the list at PDF p.37-38.

## 0. Context and origin of the rules
- `[from source]` (TAUP p.37-38): the 17 rules are "abstracted" by the author from what the Unix "elders" said and did; before the list, the text reproduces Rob Pike's rules (Notes on C Programming) and Ken Thompson's maxim on brute force (TAUP p.36-37). Pike's Rule 5 ("data dominates") is at TAUP p.37.
- `[from source]` (TAUP p.36): McIlroy's philosophy (make each program do one thing well; the output of one becomes the input of another; build early and throw away the clumsy parts; prefer tools) is summarized on the same page.

## 1. The rules, one by one (PDF page where the rule is discussed)
| # | Rule | Summary (paraphrase) | PDF |
|---|---|---|---|
| 1 | Modularity | Simple parts connected by clean interfaces; only then do problems stay local and can one part be updated without breaking the whole. Quote from the book: Kernighan, "controlling complexity is the essence of computer programming". | p.38-39 |
| 2 | Clarity | Write for whoever will maintain the code; trading a small performance gain for great obscurity is a bad deal. | p.39 |
| 3 | Composition | Programs should be able to be connected; filters that read and write plain text streams; the text stream enforces encapsulation. | p.39-40 |
| 4 | Separation | Policy and mechanism change on different time scales; separate interfaces from engines; example of X and Emacs (embedded Lisp driving C primitives). | p.40-41 |
| 5 | Simplicity | Complexity only where inevitable; sources of excess: "technical machismo" and inflated requirements. | p.41-42 |
| 6 | Parsimony | A big program only when it is demonstrated that nothing smaller will do; big programs are hard to maintain and encourage over-investment in bad approaches. | p.42 |
| 7 | Transparency | Design for visibility (inspection and debugging); *transparent* = what it does can be understood by looking; *discoverable* = exposes its internal state. | p.42-43 |
| 8 | Robustness | Child of transparency and simplicity; avoid special cases; tolerate unusual inputs (for example, accept empty lists). | p.43-44 |
| 9 | Representation | Fold knowledge into data so the logic can be "stupid and robust"; prefer complexity in the data to complexity in the code (see Pike's Rule 5). | p.44 |
| 10 | Least surprise | Model the interface on known conventions and analogous interfaces; "also known as the principle of least surprise/astonishment" (TAUP p.44). | p.44-45 |
| 11 | Silence | If the program has nothing *surprising* to say, it says nothing; the book ties this to the economy of the user's attention and to composition (the output of one program is the input of another). | p.45-46 |
| 12 | Repair | Repair what you can; when you must fail, fail noisily and early; do not let the failure corrupt silently; mentions Postel's prescription and its counterpoint in HTML. | p.46-47 |
| 13 | Economy | Programmer time is expensive; conserve it rather than machine time; suggests higher-level languages. | p.47 |
| 14 | Generation | Avoid manual work; code generators (parser/lexer, makefile) when the specification is simpler than the generated code. | p.47-48 |
| 15 | Optimization | Prototype before polishing; quotes from Kernighan & Plauger, Knuth (attributed by him to Hoare, note 11) and Kent Beck; measure/unknown bottlenecks before optimizing. | p.48-49 |
| 16 | Diversity | Distrust "the one true way": several languages, open and extensible systems. | p.49-50 |
| 17 | Extensibility | Leave room to grow; self-describing formats, with a version number or self-contained clauses; not a license for features you do not yet need. | p.50 |

## 2. Notes that correct version 1
- `[from source]` (TAUP p.45): the Rule of Silence speaks of a program with nothing *surprising* to say (the book uses "nothing surprising to say" in the list, PDF p.38); the historical explanation is that Unix predates video terminals (slow printers of 1969) (TAUP p.45).
- `[from source]` (TAUP p.327): the interfaces chapter gives three reasons for silence: programs that "chatter" hinder composition (whoever reads the output must discard messages, even without an error), vertical screen space is precious, useless messages waste the user's attention; and it recommends sending **only real errors** to standard error (stderr).
- `[from source]` (TAUP p.46): the Rule of Repair says "fail early and noisily"; the expression "fail-fast" and the recommendation to "never silently catch exceptions", as in v1, are `[inference]`/`[extrapolation]` (the book speaks of software that fails transparently and diagnosably, TAUP p.46).
- `[from source]` (TAUP p.48): in the Rule of Optimization, the "90%" is from Kernighan & Plauger about delivered functionality ("90% now is better than 100% never"); the maxim about premature optimization is attributed by Knuth to C. A. R. Hoare (note 11, TAUP p.48). The general rule "90% of the execution time is spent in 10% of the code" **exists in the book, but elsewhere**: ch. 15, section *Profiling* (TAUP p.412); v1 attributed it to the Rule of Optimization (printed p.46), a wrong page.
- `[from source]` (TAUP p.44): "Fold knowledge into data" has as its example comparing an array initializer (conversion table) with an equivalent `switch`, and a 50-node tree diagram with a 50-line flowchart.
- `[from source]` (TAUP p.50): closing of the chapter: all the rules "boil down" to the KISS principle (TAUP p.50-51). v1 also put "KISS" in the Rule of Simplicity; the term is at p.50.

## 3. Mechanism vs policy (Rule 4) `[from source]` (TAUP p.40-41)
- The book explains that, in X, the decision was "mechanism, not policy"; that policy changes faster than mechanism; that separating allows experimenting with policies without breaking mechanisms and makes the mechanism easier to test (policy ages fast and rarely justifies the investment in tests).
- Two ways to separate: a library of C routines driven by an embedded scripting language (Emacs with Lisp), or front-end (policy) and back-end (mechanism) processes talking over a protocol (TAUP p.41).

## 4. `[DATED]`
Examples from 2003 (X, Usenet, sendmail, CORBA, Emacs) and opinions about languages (Perl, Tcl, Java) reflect the year of publication (TAUP p.47). The book was published in 2003 (TAUP p.2).
