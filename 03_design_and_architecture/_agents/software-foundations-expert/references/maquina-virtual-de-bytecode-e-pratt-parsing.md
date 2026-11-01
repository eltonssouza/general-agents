# Bytecode virtual machine (clox) and Pratt parsing

Source: CI Part III, chs. 14-25 (PDF p.233-505). Convention: PDF page (see `INDEX.md`). The motivation (why bytecode instead of an AST) is in `pipeline-de-compiladores-e-interpretadores.md`, section 4.

## 1. Bytecode chunks (CI ch. 14)
- `[from source]` (CI p.237): each instruction has a one-byte *opcode*; "chunk" is the name of the module/structure for sequences of bytecode.
- `[from source]` (CI p.237-238): the chunk is a dynamic array of bytes (`uint8_t* code`, with `count` and `capacity`); dynamic arrays give dense, cache-friendly storage, constant-time indexed access and constant-time (amortized) append.
- `[from source]` (CI p.247-248): constants go into a *constant pool* (`ValueArray constants` in the chunk), like the JVM's per class; the constant-load instruction looks up the value by index (CI p.247).
- `[from source]` (CI p.251): `OP_CONSTANT` takes two bytes (opcode + index).
- `[from source]` (CI p.252): line information: an array of integers parallel to the bytecode (`int* lines`); the author admits it is "embarrassingly inefficient" in memory, but simple.

## 2. The stack-based VM (CI ch. 15)
- `[from source]` (CI p.260-261): `interpret(Chunk*)` stores the chunk in the VM and points `ip` (instruction pointer) at the first byte; `ip` is a real C pointer (and not an index) because dereferencing a pointer is faster than indexing an array; the `ip` always points to the *next* instruction.
- `[from source]` (CI p.261-262): `run()` is a loop with a `switch` on the opcode read by `READ_BYTE()` (`*vm.ip++`); *decoding/dispatching* the instruction is the most performance-critical part; the fastest techniques require non-standard C extensions or assembly, so clox uses a simple `switch` (CI p.262).
- `[from source]` (CI p.267-268): temporaries have stack behavior (last in, first out); the value stack is a fixed array with `stackTop` pointing *just past* the last element (allows empty stack = index 0); `STACK_MAX` is 256 at the start of the book.
- `[inference]`: the v1 claim that `*vm.ip++` is fast "thanks to L1 cache alignment and predictive prefetching" is **not** in CI p.263 (the book's justification for a pointer instead of an index is at p.261); remove.

## 3. Single-pass compilation with Pratt parsing (CI ch. 17)
- `[from source]` (CI p.300): the chapter presents Vaughan Pratt's "top-down operator precedence parsing"; the author describes it as the most elegant way he knows to parse expressions, handling prefix, postfix, infix and "mixfix" and dealing with precedence and associativity. The book does not give the year of Pratt's publication (v1 said "1973" attributed to CI p.300-305).
- `[from source]` (CI p.300-301): "Pratt parsers are an oral tradition in the industry"; compiler books do not teach them because academia concentrates on generated parsers.
- `[from source]` (CI p.302-303): in *single-pass compilation* the compiler emits bytecode directly from the parser, with no intermediate AST.
- `[from source]` (CI p.315): the table is an array of `ParseRule`, one row per token type, with `prefix` (function that compiles an expression starting with that token), `infix` (function that compiles an expression whose left operand is followed by that token) and `precedence` (of the infix operator).
- `[from source]` (CI p.317-318): `parsePrecedence(precedence)` advances, calls the token's `prefix` function and, while the next token has precedence greater than or equal to the one allowed, consumes the operator and calls its `infix` function. `binary()` compiles the right operand with `rule->precedence + 1` (left associativity) and emits the opcode (CI p.314-315).
- `[from source]` (CI p.314): the bytecode order matches the execution order: the left operand is compiled first and its value stays on the stack; then comes the right operand; then the operator's opcode.
- `[inference]`: the book says a Pratt parser "is not recursive descent, but it is recursive" (CI p.310). The v1 comparison "cascade of functions vs table" summarizes CI p.82-84 and p.315-318.

## 4. Global and local variables (CI chs. 21-22)
- `[from source]` (CI p.381): in Lox, global variables are *late bound* (resolved dynamically, after compilation): code can refer to a global before it is defined, as long as it does not execute before the definition; in jlox the chain of environments with a hash table per scope is "slow"; in clox the globals live in a VM hash table (`vm.globals`, CI p.381, p.514).
- `[from source]` (CI p.400-401): locals live on the VM stack itself: allocating a local is incrementing `stackTop`, freeing is decrementing, and accessing a known slot is indexing an array; it works because blocks are strictly nested and statements do not nest inside expressions. Lexical scope allows resolving locals at compile time (CI p.400).
- `[from source]` (CI p.402): the compiler keeps a flat array of in-scope locals (`locals`), `localCount` and `scopeDepth`; since the instruction operand is one byte, there is a fixed limit on locals (`UINT8_COUNT`).
- `[from source]` (CI p.409-411): the instructions `OP_GET_LOCAL`/`OP_SET_LOCAL` use the slot index (constant-time access by index, `[inference]` from CI p.401).

## 5. Calls and CallFrames (CI ch. 24)
- `[from source]` (CI p.446, p.476): a `CallFrame` represents a function call in progress; it stores the pointer to the function (`ObjFunction*`, later `ObjClosure*` in ch. 25), the caller's `ip` (the caller saves its own ip) and `slots`, a pointer to the first slot of the value stack usable by the function.
- `[from source]` (CI p.446-447): the frames live in a fixed array in the VM (`frames[FRAMES_MAX]`, with `frameCount`), treated as a stack, instead of dynamic heap allocation (slow); there is a maximum call depth (`FRAMES_MAX` = 64; `STACK_MAX` = `FRAMES_MAX * UINT8_COUNT`, CI p.447).
- `[from source]` (CI p.476): in ch. 25 the compiler starts generating an `ObjClosure` for each function declaration (`ObjClosure` wraps `ObjFunction`).

## 6. Closures and upvalues (CI ch. 25, p.469-505)
- `[from source]` (CI p.476-477): captured variables can outlive the function that declares them, so they are not always on the stack; the solution comes from Lua: **upvalue**, an indirection that refers to a local of an enclosing function. Each closure has an array of upvalues (one per enclosing-function variable it uses).
- `[from source]` (CI p.492-493): the book decides that closures capture *variables*, not values (they capture "the place where the value lives"); therefore, when the variable moves to the heap, all closures must retain a reference to the single new location.
- `[from source]` (CI p.493): **open upvalue** = points to a local still on the stack; when the variable is moved to the heap, the upvalue is *closed* (**closed upvalue**).
- `[from source]` (CI p.494-500): `isCaptured` marks captured locals; at the end of the block the compiler emits `OP_CLOSE_UPVALUE` for them; `closeUpvalues` copies the value from the stack into the `closed` field of the `ObjUpvalue` and makes `location` point to that field (CI p.499-500); on function return the remaining upvalues are closed (`closeUpvalues(frame->slots)`, CI p.500).
- `[from source]` (CI p.500): in jlox closures "fall out naturally" from the representation of environments; in clox they required a lot of new code (new instructions, etc.).
- `[extrapolation]`: "guarantees zero heap allocation for normal functions" (v1, CI p.484-498) is **not** a claim of the book; the book only says that captured variables start on the stack (CI p.493) and are only moved if necessary.

## 7. Hash table (CI ch. 20, p.356-380) and strings (ch. 19)
- `[from source]` (CI p.360, p.368): hash table with *open addressing* and *linear probing*; load factor (`load factor`) discussed at p.357-374; deletion requires *tombstones* so as not to break probe sequences (CI p.372-375); strings are interned (*interning*, CI p.375-378) and the interning table is used by the GC as a weak reference (see `gerenciamento-de-memoria-e-coletor-de-lixo.md`).

## 8. What the book does not say
- It does not give Pratt's year, nor "predictive prefetching" for `*vm.ip++`, nor "zero heap allocation".
