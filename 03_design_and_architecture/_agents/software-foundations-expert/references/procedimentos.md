# Operational procedures

Working procedures derived from the three books. Each step states what is `[from source]` (with a PDF page), `[inference]` or `[extrapolation]`. Page convention: PDF (see `INDEX.md`).

## 1. Implement a language (CI roadmap)
The book builds two interpreters: the tree-walk `jlox` (Part II) and the `clox` VM (Part III) (CI p.5, p.231-233). Order of the chapters `[from source]`:
1. **Scanner** (ch. 4, CI p.39-58): lexemes and tokens with type, literal and line (CI p.43-44); the scanner walks the source and ends with an EOF token (CI p.46).
2. **AST and grammar** (ch. 5, CI p.59-78) and **recursive-descent parser** (ch. 6, CI p.79-97), with precedence/associativity by levels (CI p.81-83) and *panic mode* recovery by synchronization (CI p.91-94).
3. **Evaluation** (chs. 7-8, CI p.98-139): `Interpreter` as Visitor, chained `Environment` (CI p.100-101, p.123).
4. **Functions** (ch. 10, CI p.140-162). Chapter 9 (Control Flow) is **not in the PDF** (CI p.139→140).
5. **Resolver** (ch. 11, CI p.163-186): static semantic analysis that computes scope distances (CI p.168-181) and detects static errors (CI p.182-185).
6. **Classes and inheritance** (chs. 12-13, CI p.187-230).
7. **Bytecode/VM** (chs. 14-25, CI p.233-505); **GC** (ch. 26, p.506-534); **classes in the VM** (chs. 27-29); **optimization** (ch. 30, p.594-617).

Checklist `[inference]` (each item points to its basis in the book):
- Tokens carry the line for error messages (CI p.44).
- The parser recovers from errors by synchronization, avoiding cascading errors (CI p.91-93).
- Resolve variables once, before executing, fixing the distance (CI p.168-169, p.179-181).
- In the VM, represent code as a dense array of bytes and keep constants in a pool (CI p.237-238, p.247).
- In the VM, mark roots: stack, globals, CallFrames, open upvalues and compiler roots (CI p.513-516).
- Test the GC in stress mode (CI p.525, p.531-533).

## 2. Build a Unix-style command-line tool
- `[from source]` (TAUP p.39-40): design for composition: read and write plain text streams, as a *filter* (TAUP p.305: a filter reads from standard input, transforms and writes to standard output).
- `[from source]` (TAUP p.327): status messages on standard output hinder composition; only real errors go to standard error.
- `[from source]` (TAUP p.306): the *cantrip* pattern (no input or output, only invocation and a numeric exit status) is the easiest to script.
- `[from source]` (TAUP p.45): follow Unix traditions for configuration files and command-line options ("learn and use"); (TAUP p.45: model the interface on known analogous programs).
- `[from source]` (TAUP p.46): fail transparently, early and with easy diagnosis when repair is not possible (Rule of Repair).
- `[extrapolation]`: "return 0 only on total success and nonzero codes for errors", "use `-v`/`--help`/`-f` as in the POSIX/GNU conventions" and "send diagnostics to stderr under `--verbose`" are common practices, **not** prescriptions with a page in TAUP; v1 cited them as TAUP p.42-44.
- `[from source]` (TAUP p.192-193, p.216): to divide a system, prefer simple cooperating processes before more complex techniques; threads as a last resort.

## 3. Analyze and debug evaluation models (SICP)
1. Is there assignment/mutation? If not, the substitution model suffices (SICP p.29, p.217). `[from source]`
2. If there is, adopt the environment model: one global frame; each evaluated `lambda` creates a procedure object (code + environment); each call creates a frame whose enclosing environment is the procedure's environment (not the caller's) (SICP p.225-227, p.232). `[from source]`
3. Track `set!` in the frame that contains the binding (SICP p.227). `[from source]`
4. In evaluators, separate analysis from execution when the code runs many times (SICP p.359-360). `[from source]`
5. In lazy evaluation, think in terms of thunks and when they are forced (SICP p.369) and avoid mixing with mutation (SICP p.325). `[from source]`
6. For search/backtracking, use `amb` and `require` (SICP p.380); assignments are undone on backtracking (SICP p.390, p.394). `[from source]`
7. The script `scripts/evaluator_trace.py` illustrates steps 1-3 with our own examples (see the origin declared in the script itself).
