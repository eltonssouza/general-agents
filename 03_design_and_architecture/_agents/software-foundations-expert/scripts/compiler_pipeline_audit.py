# -*- coding: utf-8 -*-
"""
compiler_pipeline_audit.py - comparator of language implementation strategies (CI) with declared origin.

ORIGIN OF THE RULES (declared): each dimension carries the "origin" field:
  - "[from source] CI p.N": claim read on the cited page (PDF) of Crafting Interpreters (text in references/);
  - "[inference]": direct deduction from what the book says (explained on the line itself);
  - "[extrapolation]": external knowledge (deliberately not used in this script).
The unsupported numbers of version 1 were REMOVED ("5x to 10x less memory", "10x to 50x faster", "hundreds of
instructions", "doubles the density"...). The only book numbers used here: jlox ~72 s vs C ~0.5 s on fib(40) (CI p.232);
cache "more than 100 times faster" when the data is already in the cache (CI p.234); Value from 16 bytes to 8 bytes (CI p.601-604);
FRAMES_MAX 64 and STACK_MAX 256 (CI p.447, p.268); GC growth factor 2 (CI p.529).
Pages = PDF (see references/INDEX.md). No network; read-only.

Usage:
  python -I scripts/compiler_pipeline_audit.py --topic treewalk_vs_bytecode [--json]
  python -I scripts/compiler_pipeline_audit.py --list
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

TOPICS = {
    "treewalk_vs_bytecode": {
        "title": "Tree-walk interpreter (jlox) vs bytecode virtual machine (clox) vs native code",
        "citation": "CI p.17, p.232-235, p.260-262, p.446-447",
        "dimensions": [
            {"dimension": "Performance (the author's order of magnitude)",
             "jlox": "fib(40): about 72 s on the author's laptop; equivalent C: about 0.5 s; the execution model (walking the AST) is 'fundamentally the wrong design' for performance",
             "clox": "the book justifies bytecode as the middle ground; it gives no single multiplier in this passage",
             "origin": "[from source] CI p.232, p.235"},
            {"dimension": "Code representation",
             "jlox": "each piece of syntax becomes an AST node (objects with pointers and headers; each pointer adds 32 or 64 bits)",
             "clox": "dense, linear sequence of bytes (chunk) with a constant pool and a parallel line array",
             "origin": "[from source] CI p.233-235, p.237-238, p.247, p.252"},
            {"dimension": "Cache locality",
             "jlox": "nodes scattered on the heap; following references can leave the cache and stall the CPU; the book says data already in cache can be read 'more than 100 times' faster",
             "clox": "dense and ordered the way it will be read, which suits the cache",
             "origin": "[from source] CI p.234-235"},
            {"dimension": "Dispatch",
             "jlox": "interface dispatch and Visitor pattern overhead, in addition to locality",
             "clox": "loop with a switch over the opcode; decoding/dispatching is the most performance-critical part of the VM; faster techniques require C extensions or assembly",
             "origin": "[from source] CI p.234, p.261-262"},
            {"dimension": "Temporary state and calls",
             "jlox": "recursive AST evaluation keeps intermediate results in local variables on the host language's (Java) stack",
             "clox": "explicit value stack (STACK_MAX 256 at the start) and a CallFrames array with fixed depth (FRAMES_MAX 64)",
             "origin": "[from source] CI p.265, p.268, p.446-447; the link to 'recursion limits under the VM's control' is an [inference] from those pages"},
            {"dimension": "Engineering complexity and portability",
             "jlox": "simple (the runtime representation maps the syntax) and portable (runs wherever Java runs)",
             "clox": "bytecode gives up some simplicity for performance and keeps portability (a VM in C runs wherever a C compiler exists)",
             "origin": "[from source] CI p.233, p.235"},
            {"dimension": "Native code (for comparison)",
             "jlox": "-",
             "clox": "fastest, but compiling to it 'is not easy' (registers, pipelining, scheduling) and loses portability",
             "origin": "[from source] CI p.234-235"},
            {"dimension": "When to choose",
             "jlox": "tree-walk is common in study projects and small languages, but not in general-purpose languages because it tends to be slow",
             "clox": "for general use with performance: bytecode (or JIT for dynamic languages)",
             "origin": "[from source] CI p.17, p.18; the recommendation is an [inference]"},
        ],
    },
    "parsing_strategies": {
        "title": "Recursive descent (jlox) vs Pratt parsing (clox)",
        "citation": "CI p.79-94, p.300-303, p.310-318",
        "dimensions": [
            {"dimension": "Code structure",
             "recursive_descent": "one function per rule/precedence level: expression -> equality -> comparison -> term -> factor -> unary -> primary",
             "pratt_parsing": "a ParseRule table (prefix, infix, precedence) per token type and one parsePrecedence function",
             "origin": "[from source] CI p.82-84, p.315-318"},
            {"dimension": "Output production",
             "recursive_descent": "in jlox, builds the AST (Expr/Stmt)",
             "pratt_parsing": "in clox, single-pass compilation: emits bytecode directly from the parser, without an AST",
             "origin": "[from source] CI p.302-303, p.314"},
            {"dimension": "Precedence and associativity",
             "recursive_descent": "grammar stratified by level; left recursion avoided with the loop `( op operand )*`",
             "pratt_parsing": "binary() compiles the right operand with the rule's precedence + 1 (left associativity); loop in parsePrecedence",
             "origin": "[from source] CI p.82-83, p.314, p.318"},
            {"dimension": "Recursive nature",
             "recursive_descent": "recursive, top-down",
             "pratt_parsing": "the book says a Pratt parser 'is not recursive descent, but it is still recursive'",
             "origin": "[from source] CI p.84, p.310"},
            {"dimension": "Who uses it",
             "recursive_descent": "GCC, V8 and Roslyn, according to the book",
             "pratt_parsing": "the book calls Pratt parsing an 'oral tradition' in industry (hand-written parsers)",
             "origin": "[from source] CI p.84, p.300-301"},
        ],
    },
    "gc_architecture": {
        "title": "clox mark-sweep garbage collection (and comparison with SICP's stop-and-copy)",
        "citation": "CI p.506-534; SICP p.489-494",
        "dimensions": [
            {"phase": "Reachability and roots",
             "description": "Reachable = the program can reference it; all roots are reachable and so is everything a reachable object references.",
             "mechanic": "Roots in clox: value stack, globals table, CallFrames, open upvalues and the compiler's objects during execution.",
             "origin": "[from source] CI p.507-508, p.513-516"},
            {"phase": "Tricolor marking",
             "description": "White (not reached), gray (reached, not yet traced) and black (processed).",
             "mechanic": "Gray stack `grayStack` (managed with the system realloc, outside the GC); invariant: no black object points to a white one.",
             "origin": "[from source] CI p.517-518"},
            {"phase": "Weak references",
             "description": "The interned string table cannot be a root (no string would ever be collected) nor be left with dangling pointers.",
             "mechanic": "tableRemoveWhite(&vm.strings) between the end of tracing and the sweep.",
             "origin": "[from source] CI p.523-525"},
            {"phase": "Sweep",
             "description": "Walks the linked list of all objects; frees the unmarked ones and clears the mark of the marked ones.",
             "mechanic": "Marked object: isMarked=false; unmarked: unlinked from the list and freed with freeObject().",
             "origin": "[from source] CI p.522-523"},
            {"phase": "When to collect",
             "description": "Two metrics: throughput and latency; the book admits the literature answers the question poorly.",
             "mechanic": "Threshold nextGC = bytesAllocated * GC_HEAP_GROW_FACTOR (factor 2, 'basically arbitrary').",
             "origin": "[from source] CI p.525-529"},
            {"phase": "Stop-and-copy (SICP, for comparison)",
             "description": "Memory in two halves; copies useful objects to the free half and swaps the roles; broken heart + forwarding address.",
             "mechanic": "Examines only the useful part and compacts (SICP p.494); 'requires twice the memory' is an [inference] from splitting memory into two halves (SICP p.489).",
             "origin": "[from source] SICP p.489-494"},
        ],
    },
    "pipeline_phases": {
        "title": "Pipeline phases of a language implementation",
        "citation": "CI p.10-21",
        "dimensions": [
            {"phase": "Scanning", "description": "characters -> tokens; discards whitespace and comments", "origin": "[from source] CI p.11-12"},
            {"phase": "Parsing", "description": "tokens -> tree (AST) according to the grammar; reports syntax errors", "origin": "[from source] CI p.12"},
            {"phase": "Static analysis", "description": "binding/resolution; type check if statically typed; results in attributes, symbol table or a new structure", "origin": "[from source] CI p.12-13"},
            {"phase": "IR", "description": "interface between source and target language; styles cited: CFG, SSA, CPS, three-address code", "origin": "[from source] CI p.14"},
            {"phase": "Optimization", "description": "same semantics, more efficient; example: constant folding", "origin": "[from source] CI p.14"},
            {"phase": "Code generation", "description": "native code or bytecode (p-code)", "origin": "[from source] CI p.15"},
            {"phase": "Virtual machine", "description": "runs the bytecode; slower than native, but portable", "origin": "[from source] CI p.15-16"},
            {"phase": "Runtime", "description": "services during execution (GC, object types)", "origin": "[from source] CI p.16"},
            {"phase": "Shortcuts", "description": "single pass, tree-walk, transpilers, JIT", "origin": "[from source] CI p.16-18"},
        ],
    },
    "value_representation": {
        "title": "Representation of dynamic values: tagged union vs NaN boxing",
        "citation": "CI p.601-604",
        "dimensions": [
            {"dimension": "Size", "tagged_union": "16 bytes (tag + union, with alignment padding)", "nan_boxing": "8 bytes", "origin": "[from source] CI p.601-604"},
            {"dimension": "Cache", "tagged_union": "fewer values per cache line", "nan_boxing": "more values per cache line, fewer cache misses", "origin": "[from source] CI p.602"},
            {"dimension": "Numbers", "tagged_union": "double field inside the union", "nan_boxing": "plain doubles, no conversion", "origin": "[from source] CI p.604"},
            {"dimension": "Pointers and tags", "tagged_union": "pointer in the union", "nan_boxing": "48 pointer bits in the 51 free bits of a quiet NaN, leaving 3 bits for tags (nil, booleans, Obj)", "origin": "[from source] CI p.603-604"},
            {"dimension": "Portability", "tagged_union": "independent of low-level details", "nan_boxing": "depends on FP/pointer details; the book keeps both representations behind a compile flag", "origin": "[from source] CI p.604"},
        ],
    },
}


def main():
    ap = argparse.ArgumentParser(description="Architectural comparator of language implementations (CI), with origin per line.")
    ap.add_argument("--topic", choices=sorted(TOPICS), default="treewalk_vs_bytecode")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.list:
        for k, v in sorted(TOPICS.items()):
            print("%-24s %s [%s]" % (k, v["title"], v["citation"]))
        return 0
    res = TOPICS[a.topic]
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
    print("=== %s ===" % res["title"])
    print("Citation: [%s]  (PDF pages)\n" % res["citation"])
    for d in res["dimensions"]:
        head = d.get("dimension") or d.get("phase")
        print("* %s" % head)
        for k, v in d.items():
            if k in ("dimension", "phase"):
                continue
            print("    - %s: %s" % (k, v))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
