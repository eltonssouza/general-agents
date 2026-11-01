# INDEX of the references: software-foundations-expert

Revised package (v2). Sources (PDFs in `03_design_and_architecture/`, all complete with extractable text):
1. **SICP**: Abelson & Sussman with Julie Sussman, *Structure and Interpretation of Computer Programs*, 2nd ed. (MIT Press, 1996), file `SICP-Structure-and-Interpretation-of-Programs.pdf`: **634 pages**, online edition (each section of the web text becomes one or more pages; footnotes at the end of the section).
2. **TAUP**: Eric S. Raymond, *The Art of Unix Programming* (2003), file `The-Art-of-Unix-Programming.pdf`: **549 pages**, book version with printed-page footers.
3. **CI**: Robert Nystrom, *Crafting Interpreters*, file `Crafting-Interpreters-Nystrom.pdf`: **630 pages**, capture of the web edition (© 2015-2021), no printed numbering.

## Page convention (mandatory)
- **Every citation `(SICP p.N)`, `(TAUP p.N)`, `(CI p.N)` uses the PDF page** (same numbering as the `=== PAGE N ===` markers of the extracted text).
- **SICP** and **CI** have no printed numbering in the PDF; the PDF page is the only reference. Therefore, when citing to the user, write "SICP p.N (PDF)". Example: the substitution model is at SICP p.28-31, section 1.1.5.
- **TAUP**: printed page = PDF page − 2 (verified in the footers of PDF p.27-549; PDF p.1-26 are cover and table of contents). The table of contents (PDF p.3-11) lists printed numbers. Example: "Rule of Modularity" is at PDF p.38-39 (printed 36-37). Version 1 of the package cited the rules of ch. 1 with the **printed page** and the chapters with the **PDF page**, without warning: mix corrected.
- Version 1 cited SICP with numbers that match neither the PDF nor any identifiable numbering (for example, "SICP p.31" for the substitution model, which is at p.28-31; "SICP p.397" for `amb`, which is at p.379-381). All pages were recalculated.
- Figures (SICP environment diagrams, CI diagrams) are not in the extracted text: anything that depends only on a figure cannot be verified automatically.

## Gaps in the sources (verified)
- **CI**: **chapter 9 (Control Flow) is not in the PDF** (the text jumps from ch. 8, p.139, to ch. 10, p.140). The opening pages of Parts II and III appear out of order (p.231-232).
- **TAUP**: complete (chs. 1-20, appendices A-D and colophon).
- **SICP**: complete (chs. 1-5, references and index).

## Chapter map (PDF)
**SICP**: ch. 1 Procedures p.19-90 (1.1 p.22; 1.1.5 substitution model p.28; 1.2 p.45; 1.3 p.67; first-class p.84); ch. 2 Data p.88-206 (2.1 p.91; barriers p.94-96; 2.2 closure property p.104; 2.4 multiple representations p.168; data-directed p.175-182; 2.5 generics p.183; coercion p.188-193); ch. 3 State p.207-331 (3.1 p.209; costs of assignment p.217-224; 3.2 environment p.224-239; 3.4 concurrency p.279-296; 3.5 streams p.296-331); ch. 4 Metalinguistic p.332-446 (4.1 metacircular p.335; 4.1.7 analyze p.359; 4.2 lazy p.367; 4.3 amb p.379; 4.4 logic p.401); ch. 5 Machines p.446-545 (5.3 GC p.484-495; 5.4 explicit-control p.495-512; 5.5 compilation p.512-545).

**TAUP**: Part I Context: ch. 1 Philosophy p.27-53 (rules p.37-50); 2 History p.54-77; 3 Contrasts p.78-107. Part II Design: 4 Modularity p.109-131; 5 Textuality p.132-160; 6 Transparency p.161-189; 7 Multiprogramming p.190-216 (threads p.213-216); 8 Minilanguages p.217-250; 9 Generation p.251-266; 10 Configuration p.267-290; 11 Interfaces p.291-328 (Silence is Golden p.327); 12 Optimization p.329-336; 13 Complexity p.337-360. Part III Implementation: 14 Languages p.362-389; 15 Tools p.390-415; 16 Reuse p.416-433. Part IV Community: 17 Portability p.435-458; 18 Documentation p.459-480; 19 Open Source p.481-505; 20 Futures p.506-523. Appendices p.524-548.

**CI**: 1 Introduction p.2-9; 2 A Map of the Territory p.10-21; 3 The Lox Language p.22-38; 4 Scanning p.39-58; 5 Representing Code p.59-78; 6 Parsing Expressions p.79-97; 7 Evaluating Expressions p.98-112; 8 Statements and State p.113-139; [9 Control Flow: absent]; 10 Functions p.140-162; 11 Resolving and Binding p.163-186; 12 Classes p.187-214; 13 Inheritance p.215-230; 14 Chunks of Bytecode p.233-257; 15 A Virtual Machine p.258-278; 16 Scanning on Demand p.279-299; 17 Compiling Expressions p.300-322; 18 Types of Values p.323-337; 19 Strings p.338-355; 20 Hash Tables p.356-380; 21 Global Variables p.381-399; 22 Local Variables p.400-414; 23 Jumping Back and Forth p.415-435; 24 Calls and Functions p.436-468; 25 Closures p.469-505; 26 Garbage Collection p.506-534; 27 Classes and Instances p.535-548; 28 Methods and Initializers p.549-576; 29 Superclasses p.577-593; 30 Optimization p.594-617; Appendix I (grammar) p.618-620; Appendix II (AST classes) p.621-630.

## Files in `references/`
| File | Topic | Source (PDF) |
|---|---|---|
| [`modelos-de-avaliacao-substituicao-vs-ambiente.md`](modelos-de-avaliacao-substituicao-vs-ambiente.md) | Substitution, evaluation orders, `set!`, environment, lexical/dynamic scope | SICP p.28-31, p.217-234; CI p.131, p.163-164 |
| [`abstracao-procedural-e-dados-compostos.md`](abstracao-procedural-e-dados-compostos.md) | Higher-order, first-class, barriers, procedural pairs, closure property | SICP p.67-84, p.91-98, p.104-105, p.141 |
| [`programacao-orientada-a-dados-e-genericos.md`](programacao-orientada-a-dados-e-genericos.md) | Multiple representations, dispatch, operation×type table, message passing, coercion | SICP p.168-193 |
| [`estado-mutavel-concorrencia-e-streams.md`](estado-mutavel-concorrencia-e-streams.md) | Cost of assignment, concurrency, serializers, mutex, deadlock, streams | SICP p.217-221, p.279-306, p.325 |
| [`avaliadores-metacircular-lazy-e-amb.md`](avaliadores-metacircular-lazy-e-amb.md) | `eval`/`apply`, `analyze`, lazy/thunks, `amb`, tail recursion | SICP p.335-398, p.501-503 |
| [`as-17-regras-da-filosofia-unix.md`](as-17-regras-da-filosofia-unix.md) | The 17 rules | TAUP p.36-51, p.327 |
| [`textualidade-multiprocessamento-e-minilinguagens.md`](textualidade-multiprocessamento-e-minilinguagens.md) | Text vs binary, IPC and threads, minilanguages | TAUP p.132-149, p.190-216, p.217-250 |
| [`pipeline-de-compiladores-e-interpretadores.md`](pipeline-de-compiladores-e-interpretadores.md) | Phases, alternative paths, tree-walk vs bytecode | CI p.10-21, p.43-46, p.79-94, p.232-235 |
| [`interpretador-tree-walk-e-ast.md`](interpretador-tree-walk-e-ast.md) | CFG, expression problem, Visitor, recursive descent, Resolver | CI p.59-97, p.163-186 |
| [`maquina-virtual-de-bytecode-e-pratt-parsing.md`](maquina-virtual-de-bytecode-e-pratt-parsing.md) | Chunks, stack VM, Pratt, locals, CallFrames, upvalues | CI p.233-278, p.300-322, p.381-414, p.436-505 |
| [`gerenciamento-de-memoria-e-coletor-de-lixo.md`](gerenciamento-de-memoria-e-coletor-de-lixo.md) | Tricolor mark-sweep, stop-and-copy, NaN boxing | CI p.506-534, p.594-617; SICP p.484-495 |
| [`casos-e-antipadroes.md`](casos-e-antipadroes.md) | Anti-patterns tied to pages | several |
| [`procedimentos.md`](procedimentos.md) | Operational playbooks | several |
| [`glossario.md`](glossario.md) | Terms with page | several |

## Epistemic labels
- `[from source]`: read on the cited page. No literal copying (at most one quote of fewer than 15 words).
- `[inference]`: direct deduction from the book's premises.
- `[extrapolation]`: external knowledge (modern languages, JSON, POSIX, etc.).
- `[DATED]`: TAUP is from 2003 (X, Usenet, CORBA, state of threads and languages) and SICP is from 1996; CI uses Java and C in the state of 2015-2021.

## What the books do NOT contain (`not_in_book`)
- SICP: "dynamic scope"; "homoiconicity"; Cheney's algorithm; "several orders of magnitude" for `analyze`; an explicit relation of `amb` to the "Einstein problem"; any use of "closure" in the implementation sense (SICP p.141, note 6, rejects that use); a foundation "of OOP with actors/prototypes" for message passing.
- TAUP: "dynamic scope"; `copy-on-write`; JSON/YAML; `--help`/`-v` as a POSIX convention; fault isolation (*segfault*) as an explicit argument for processes vs threads.
- CI: "double dispatch" and "Open/Closed Principle" when explaining the Visitor; "10x to 50x faster" or "5x to 10x less memory" for bytecode; the year of Pratt's publication; prefetching for `*vm.ip++`; chapter 9 (Control Flow) (absent from the PDF); `NaN boxing` "eliminates misalignment".
- Outside the corpus (appear only in passing or not at all): Rust (CI p.71, p.126, p.407; TAUP p.510), WebAssembly (CI p.18), Go (CI p.16, p.20), LLVM (CI p.7, p.235), GCC/IR (CI p.14); not treated as a topic: monads, type inference, modern concurrency (CI only mentions 'async' and 'algebraic data type' in passing, p.299 and p.324).

## How to look things up
1. Open this INDEX, choose the file by trigger; read only what is needed.
2. To verify a page: `python -I scripts/foundations_lookup.py "<term>"` (or `--list`); "NOT COVERED" = the collection does not cover it.
3. To audit the package against the PDFs: `python -I tests/verify_citations.py --src <folder with sicp.txt, taup.txt, ci.txt>` and `python -I tests/audit_tokens.py --src <folder>` (see `README.md`).
