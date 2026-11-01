# Memory management, garbage collector and value representation

Source: CI ch. 26 (PDF p.506-534) and ch. 30 (p.594-617); SICP 5.3 (PDF p.484-495). Convention: PDF page (see `INDEX.md`).

## 1. Why collect garbage (CI p.506-508)
- `[from source]` (CI p.506): dynamic allocation is a good candidate for automation: it is necessary, tedious to do by hand and error-prone, with consequences such as crashes, memory corruption and security violations. *Managed* languages (like Lox) give the illusion of infinite memory and the component that reclaims memory is the *garbage collector*.
- `[from source]` (CI p.506-507): since the VM cannot see the future, it uses a conservative approximation: memory is in use if it *could* be read in the future; a value is *reachable* if there is some way for the program to reference it.
- `[from source]` (CI p.507-508): **roots** are objects the VM reaches directly, without going through a reference in another object (global variables, the value stack and a few other places). Inductive definition of reachability: all roots are reachable; any object referred to by a reachable one is reachable (CI p.508). Two generic steps: traverse from the roots; free what was not reached (CI p.508).
- `[from source]` (SICP p.489): SICP arrives at the same criterion: only objects reachable by sequences of `car`/`cdr` from the pointers in the machine's registers can affect the future of the computation; the rest is garbage.

## 2. Mark-sweep and tricolor in clox (CI p.509-525)
- `[from source]` (CI p.509): *mark-and-sweep* was the first GC algorithm (McCarthy, Lisp); two phases: mark (trace from the roots and mark what it visits) and sweep (free the unmarked).
- `[from source]` (CI p.513): clox marks objects with the `isMarked` field of the `Obj` header; numbers, booleans and `nil` are inline in `Value` and do not need to be marked.
- `[from source]` (CI p.513-516): marked roots: the value stack, the `vm.globals` table, the `CallFrame`s (each references its closure), the list of *open upvalues* (`vm.openUpvalues`) and the "hidden" roots of the running compiler, because a collection can start at any allocation, including during compilation (CI p.515).
- `[from source]` (CI p.517): **tricolor abstraction**: white (not reached/processed; all start white), gray (reached, but what it references is not yet traced; it is the worklist) and black (processed). The process: all white; roots become gray; while there is gray, take one, turn the white objects it references gray and make it black. The note on p.518 calls the rule "no black points to white" the *tricolor invariant*.
- `[from source]` (CI p.518): the gray list is a *stack* (`grayStack`), managed with the system's `realloc` (and not the VM's `reallocate`) so that growing the stack during a collection does not trigger another collection.
- `[from source]` (CI p.522-523): `sweep()` walks the linked list of all objects (`vm.objects`): marked objects have the mark cleared (preparing the next cycle); unmarked ones are unlinked from the list and freed (`freeObject()`).
- `[from source]` (CI p.523-525): **weak reference**: the interned-string table (`vm.strings`) points to all strings, but cannot be a root (otherwise no string would be collected); and it cannot be left with dangling pointers; therefore, between the end of tracing and the start of the sweep, `tableRemoveWhite(&vm.strings)` is called, which removes the entries whose keys are white.
- `[from source]` (CI p.525-530): *when* to collect: two metrics, **throughput** (fraction of time running user code vs collection) and **latency** (longest continuous pause) (CI p.526); in clox, the threshold for the next GC is `bytesAllocated * GC_HEAP_GROW_FACTOR` with factor 2, "basically arbitrary" (CI p.528-529).
- `[from source]` (CI p.531-533): typical bugs: a newly created object only on the C stack during `addConstant`, `allocateString` or string concatenation: the collection sweeps it; the fix is to push the object onto the VM stack temporarily.
- `[from source]` (CI p.533-534): mark-sweep is one of several algorithms; the chapter points to reference counting and generational collection as alternatives (CI p.509, p.533-534), and cites Cheney's algorithm in an exercise (CI p.533).

## 3. Stop-and-copy in SICP (SICP 5.3.2)
- `[from source]` (SICP p.489): *stop-and-copy*: divide memory into two halves, "working memory" and "free memory"; `cons` allocates in the working one; when it fills up, the useful pairs are copied (tracing `car` and `cdr` from the registers) to consecutive positions of the free memory and the roles of the halves are swapped.
- `[from source]` (SICP p.490-491): two pointers, `free` and `scan`; the moved object leaves, at the old location, a *broken heart* marker in the `car` and a *forwarding address* in the `cdr`; the loop ends when `scan` reaches `free`.
- `[from source]` (SICP p.494, note 15): the Minsky-Fenichel-Yochelson algorithm (stop-and-copy) is dominant in large-memory systems because it examines only the useful part (the sweep of mark-sweep examines all memory) and is *compacting*, which can be important with virtual memory; the book also cites mark-sweep (Allen 1978). The book attributes the idea to Minsky, developed by Fenichel and Yochelson (1969) and Baker (1978) (SICP p.494).
- `[inference]`: "requires double the memory" (v1, SICP p.484) is a consequence of dividing memory into two halves (SICP p.489), not a sentence from the book. "Cheney's algorithm" does **not** appear in SICP; only in CI p.533.

## 4. NaN boxing and the cost of dynamic values (CI ch. 30, p.594-617)
- `[from source]` (CI p.601): on a 64-bit system the `Value` (tag + union) takes 16 bytes, because of alignment; a smaller representation means more values per cache line and fewer *cache misses* (CI p.602).
- `[from source]` (CI p.602-603): a 64-bit IEEE 754 double has 1 sign bit, 11 exponent bits and 52 fraction bits; if all the exponent bits are set, it is a NaN; if the highest fraction bit is also set, it is a *quiet NaN*; avoiding Intel's "QNaN Floating-Point Indefinite" value, 51 free bits remain.
- `[from source]` (CI p.603-604): pointers use only 48 bits on almost all relevant architectures; a 48-bit pointer fits in the 51 bits, leaving 3 bits for tags (`nil`, booleans and `Obj`); the representation is half the size and numbers are normal doubles, with no conversion.
- `[from source]` (CI p.604): the book keeps both representations (tagged union and NaN boxing) via a compile flag, because NaN boxing depends on low-level details.
- `[from source]` (CI p.597, p.601): the general lesson of the chapter is to measure: a `profiler` showed that `tableGet()` consumed 72% of the run time in a benchmark (CI p.597) and that the optimization (replacing the modulo with a bit mask, p.598-600) reduced it to 35% (CI p.601); the book says profilers also serve to verify solutions (CI p.601).
- `[extrapolation]`: "eliminates the misalignment penalty" (v1, CI p.606) is **not** in the book; the book talks about alignment only to explain why `Value` is 16 bytes (CI p.601).

## 5. What the book does not say
- CI does not treat use-after-free/`double-free` as a motivation (only "memory corruption", p.506); SICP does not name "Cheney"; neither claims that stop-and-copy "totally eliminates fragmentation" in those words (SICP says it is compacting, p.494).
