# Compiler and interpreter pipeline

Source: Robert Nystrom, *Crafting Interpreters* (CI), ch. 2 "A Map of the Territory" (PDF p.10-21), ch. 4 (scanning), ch. 6 (parsing) and ch. 14 (why bytecode). Convention: PDF page (the PDF is a capture of the web edition, with no printed numbering; see `INDEX.md`). **Note: chapter 9 (Control Flow) is not in the PDF** (the text jumps from ch. 8, p.139, to ch. 10, p.140).

## 1. The map of the territory (CI ch. 2)
The book uses the metaphor of a mountain: one climbs from the "source as text" to increasingly semantic representations and descends to something executable (CI p.11).

| Phase | What the book says | PDF |
|---|---|---|
| Scanning (lexing) | Groups characters into *tokens* (words with meaning); whitespace and comments are normally discarded. | p.11-12 |
| Parsing | Builds a tree that mirrors the nesting of the grammar (syntax tree / AST, "parse tree" depending on how close to the syntax); also reports syntax errors. | p.12 |
| Static analysis | *Binding/resolution*: for each identifier, find out where it was defined (scope); *type check* if the language is statically typed; results are stored as attributes on the tree, in a *symbol table* or in a new structure. | p.12-13 |
| Front end / back end | Everything up to here is the *front end*; phases inserted afterwards formed the "middle end". | p.13-14 |
| Intermediate representation (IR) | Interface between source and target language; a shared IR reduces the work of N×M compilers (Pascal, C, Fortran vs x86, ARM, SPARC) to one front end per language and one back end per architecture. The book mentions styles such as *control flow graph*, *static single-assignment*, *continuation-passing style* and *three-address code*. | p.14 |
| Optimization | Swap the program for another with the same semantics and more efficient; the book's example: *constant folding*. The book says Lua and CPython generate relatively unoptimized code and invest in the runtime. | p.14 |
| Code generation | Instructions for a real CPU (fast, but laborious and tied to the architecture) or for a virtual machine; Wirth's "p-code", today called *bytecode*. | p.15 |
| Virtual machine | Translate the bytecode with a mini-compiler per architecture or write a VM; running bytecode on a VM is slower than native code, but simple and portable (a VM in C runs wherever there is a C compiler). | p.15-16 |
| Runtime | Services during execution (garbage collector, the type of each object for `instanceof`); in compiled languages it is embedded in the executable (example: Go); in an interpreter/VM, it lives in it. | p.16 |

Shortcuts and alternative paths (CI p.16-18):
- `[from source]` (CI p.16-17): *single-pass compilers* produce code directly in the parser, with no trees or IR; they constrain language design (Pascal and C were designed around this: type declarations first; forward declaration in C).
- `[from source]` (CI p.17): *tree-walk interpreters* execute after the parse, walking the AST; they are common in study projects and small languages, but are not widely used in general-purpose languages because they tend to be slow.
- `[from source]` (CI p.17-18): *transpilers* generate source code of another high-level language and use its compilation chain.
- `[from source]` (CI p.18): *JIT*: compile to native code at load time (HotSpot, CLR, most JavaScript interpreters); the most sophisticated JITs insert profiling hooks and recompile hot spots with more advanced optimizations.
- `[from source]` (CI p.18-20): "compiler" and "interpreter" are not mutually exclusive: compiling is translating into another form; interpreting is executing from the source; CPython is an interpreter and has a compiler (bytecode); `go run`/`go build` illustrate the same ambiguity (CI p.19-20).

## 2. Scanning and tokens (CI ch. 4)
- `[from source]` (CI p.43-44): a *lexeme* is the smallest sequence of characters with meaning; a *token* bundles the lexeme with other information: type (`TokenType`, with one type per keyword, operator, punctuation and literal type), literal value (converted during the scan) and location (in jlox, only the line). jlox's `Token` class has `type`, `lexeme`, `literal` and `line` (CI p.44).
- `[from source]` (CI p.45): the grouping rules form the *lexical grammar*; in Lox it is simple enough to be a *regular language* (the same "regular" as regular expressions); tools such as Lex/Flex generate scanners.
- `[from source]` (CI p.46): `scanTokens` walks the source to the end and appends an EOF token (not strictly necessary, but it makes the parser cleaner).
- `[inference]`: names such as `TOKEN_IDENTIFIER` (v1) belong to `clox` (see `maquina-virtual-de-bytecode-e-pratt-parsing.md`); in jlox they are `IDENTIFIER`, `NUMBER`, `WHILE`, etc. (CI p.43-44).

## 3. Parsing and errors (CI chs. 5-6)
- `[from source]` (CI p.60-62): a context-free grammar generates strings; the parser "plays the game in reverse" (CI p.80); an ambiguous grammar lets the parser misunderstand the code (CI p.80-81); precedence and associativity resolve it (CI p.81).
- `[from source]` (CI p.84): recursive descent is a top-down parser that translates grammar rules into code; the book cites GCC, V8 and Roslyn as users of recursive descent.
- `[from source]` (CI p.91-94): error recovery: *panic mode* (on detecting an error, the parser panics and *synchronizes*: discards tokens up to a point where the rule can continue, p.91); in jlox, it synchronizes at statement boundaries (semicolon or the keywords `class`, `fun`, `var`, `for`, `if`, `while`, `print`, `return`, p.93); this avoids cascading errors, at the cost of not reporting real errors inside the discarded tokens (p.91).

## 4. Tree-walk vs bytecode vs native code (CI ch. 14, "Why not walk the AST?")
- `[from source]` (CI p.232): jlox takes about 72 seconds on the author's laptop for `fib(40)` versus half a second for an equivalent C program; the author says the execution model (walking the AST) is "fundamentally the wrong design" for performance.
- `[from source]` (CI p.233-234): advantages of the tree-walker: it is already done, it is simple (the runtime representation maps the syntax) and portable; disadvantages: memory use (each AST node becomes objects with many pointers and headers, each pointer adds 32 or 64 bits) and poor **spatial locality** (nodes scattered across the heap); the CPU cache can be "more than 100 times faster"; there is also interface and Visitor dispatch overhead (p.234).
- `[from source]` (CI p.234-235): native code is the fastest, but compiling to it "is not easy" (complex architectures, register allocation, pipelining) and portability is lost. *Bytecode* sits in the middle: a dense, linear sequence of binary instructions, simple and higher-level than a real CPU's, which preserves the tree-walker's portability and sacrifices some simplicity for performance, "without being as fast as native" (CI p.235). The emulator that interprets the bytecode is the virtual machine (CI p.235).
- `[extrapolation]`: numbers such as "10x to 50x faster than tree-walk", "5x to 10x less memory" and "maximum/very low/very high complexity" in version 1's tables are **not** in the book and were removed. The book only gives the order of magnitude of CI p.232 (72 s vs 0.5 s for C) and the qualitative comparison of CI p.233-235.

## 5. When to use each `[inference]`
- Small DSL or prototype: the book says the tree-walker is common in study projects and small languages (CI p.17); therefore it is a reasonable starting point.
- General-purpose language where performance matters: bytecode VM (CI p.232-235).
- Maximum performance at the cost of portability and engineering: native code; JIT for dynamic languages (CI p.18).
- Examples "V8, Rust, C, CPython, Lua" in the same table are our organization: the book cites CPython and Lua in distinct contexts (CI p.14, p.19) and V8 in isolated mentions (recursive descent, p.84; scanner, p.297; benchmarks, p.596); Rust appears only in passing (CI p.71, p.126, p.407).

## 6. What the book does not say
- It does not claim that "bytecode is suited to scripting languages for enterprise systems and games"; it does not classify Rust as "JIT/AOT" compilation in this chapter.
