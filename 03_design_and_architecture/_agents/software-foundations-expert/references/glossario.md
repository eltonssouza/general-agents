# Glossary

Terms of the package with the PDF page where the book defines or uses them in the sense described (SICP, TAUP, CI; convention in `INDEX.md`). Definitions in our own words. Terms that the book does **not** use are marked `[extrapolation]` at the end. The letter groups follow the original Portuguese headwords.

### A
- **Additivity**: ability to incorporate new modules without modifying the existing ones; explicit dispatch on type is not additive, data-directed programming is (SICP p.176, p.183).
- **Reachable / root**: an object the program can still reference; a root is what the VM reaches directly, without going through another object (CI p.507-508).
- **Environment**: sequence of frames, each with a table of bindings and a pointer to the enclosing environment (SICP p.224).
- **Abstract syntax tree** (AST): tree the parser builds from the tokens (CI p.12).

### B
- **Abstraction barrier**: separation between whoever uses a data abstraction and whoever implements it, made by constructors and selectors (SICP p.95).
- **Binding / resolution**: tying each identifier to the place where it was declared; the first static analysis in most languages (CI p.13).
- **Bytecode**: dense, linear binary instructions of an idealized machine, often one byte each (CI p.15, p.235).

### C
- **CallFrame**: structure representing a function call in progress: function, `ip` and `slots` pointer to the stack window (CI p.446).
- **Chunk**: sequence of bytecode and associated data (constants, lines) (CI p.237, p.247-252).
- **Closure** (CI sense): function that captures the variables of the environment where it was declared; in clox it uses upvalues (CI p.166, p.477). Note: SICP does **not** use "closure" in this sense (SICP p.141, note 6).
- **Closure property**: a combining operation has the property if its results can be combined by the same operation (SICP p.104, p.141).
- **Coercion**: transforming an object of one type into an equivalent object of another, via a coercion table (SICP p.189-190).
- **Compile / interpret**: compiling is translating into another form, interpreting is executing from the source; the two are not mutually exclusive (CI p.19-20).
- **Success / failure continuation**: in the `amb` evaluator, procedures that receive the value obtained and proceed (success) or try another alternative (failure) (SICP p.389-391).

### D
- **`delay` / `force`**: `delay` packages an expression for future evaluation; `force` evaluates it (SICP p.299, p.301).
- **Recursive descent**: top-down parser in which each grammar rule becomes a function (CI p.84).

### E
- **Lexical scope**: the scope of a name is determined by the program text; in SICP, associated with block structure (SICP p.42); in Lox, resolution rule at CI p.163-164.
- **Dynamic scope**: the meaning of a name is only known when the code runs; in Lox, it holds for methods and fields, not for variables (CI p.131).
- **Strict / non-strict**: a procedure is strict in an argument if it evaluates it before entering the body (SICP p.368).

### F
- **Frame**: table of bindings of an environment (SICP p.224).
- **First-class**: element without usage restrictions; it can be named, passed, returned and stored in structures (SICP p.84).
- **Filter**: program that reads from standard input, transforms and writes to standard output (TAUP p.194, p.305).

### G
- **Gray stack**: worklist of objects reached but not yet traced (CI p.518).

### L
- **Lazy evaluation**: delaying the evaluation of arguments until the value is needed (SICP p.367).
- **Lexeme / token**: a lexeme is the smallest sequence of characters with meaning; a token bundles the lexeme with type, literal and location (CI p.43-44).

### M
- **Mark-sweep**: two-phase collection, mark from the roots and sweep the heap freeing the unmarked (CI p.509).
- **Memoization**: storing the result of the first evaluation; in streams, `memo-proc` (SICP p.302); in thunks, `evaluated-thunk` (SICP p.372).
- **Metacircular**: evaluator written in the same language it evaluates (SICP p.335).
- **Minilanguage**: small domain-specific language; the book keeps the term to remind us to keep it small and simple (TAUP p.217).
- **Multiprogramming**: dividing programs into cooperating processes (a term TAUP revives) (TAUP p.190).
- **Mutex**: object that can be acquired and released; prevents concurrent acquisitions until released (SICP p.290).

### N
- **NaN boxing**: storing dynamic values in 64 bits using the free bits of IEEE 754 *quiet NaNs* (CI p.601-604).

### O
- **Applicative order / normal order**: evaluating arguments before applying vs. fully expanding and only then reducing (SICP p.30-31).

### P
- **Panic mode**: error recovery that discards tokens up to a synchronization point (CI p.91).
- **Pratt parsing** ("top-down operator precedence parsing"): expression parsing driven by a table of prefix/infix/precedence rules (CI p.300, p.315).

### R
- **Referential transparency**: "equals can be substituted for equals" without changing the value; violated by `set!` (SICP p.220).
- **Resolver pass**: static pass before execution that computes the scope distance of each local variable (CI p.169-170, p.179).
- **Rule of Silence** (Regra do Silêncio): a program with nothing surprising to say should keep quiet (TAUP p.45, p.327).

### S
- **Serializer**: set of procedures of which only one execution at a time is allowed (SICP p.284-285).
- **Stop-and-copy**: collection that copies the useful objects to the free half of memory and swaps the roles of the halves (SICP p.489).
- **Stream**: sequence whose `cdr` is evaluated on demand (`cons-stream`) (SICP p.298-299).
- **Substitution model**: applying a procedure by evaluating the body with parameters replaced by arguments (SICP p.29).

### T
- **Thunk**: delayed expression plus the environment, for on-demand evaluation (SICP p.369).
- **Tombstone**: marker of a deleted entry in an open-addressing hash table, so as not to break probe sequences (CI p.372).
- **Tree-walk interpreter**: interpreter that executes by walking the AST (CI p.17).
- **Tricolor**: white/gray/black abstraction for the state of each object during marking (CI p.517).

### U
- **Open / closed upvalue**: open points to a local still on the stack; closed stores the value in the heap object itself (CI p.493, p.499-500).

### V
- **Visitor**: pattern that allows adding new operations to a family of types without touching them (CI p.72-73).

### W
- **Weak reference**: reference that does not count toward reachability; used in the interned-string table (CI p.524).

### Terms that are NOT in the books (`[extrapolation]`)
- *Homoiconicity*, *double dispatch*, *Open/Closed Principle* (in CI), *Cheney's algorithm* (in SICP), *copy-on-write*, *NaN boxing eliminates misalignment*: used by v1 as if they were from the text; kept only with an explicit label.
