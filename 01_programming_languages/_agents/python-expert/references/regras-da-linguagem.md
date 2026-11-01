# Python Language Rules (Language Reference 3.14.0rc3): reference base of the specialist agent

Main source: "The Python Language Reference" 3.14.0rc3 (abbreviated **Ref**), a release candidate. This file merges the intermediate notes by topic. It contains no knowledge from outside the source.

## Contents

0. Conventions
1. "Where to look" map
2. Lexical structure
3. Data model
4. Attributes, descriptors, slots, class creation
5. Special methods and protocols
6. Execution model
7. Import system
8. Expressions
9. Simple statements
10. Compound statements
11. PEG grammar and top-level components
12. Glossary: terms that change decisions
13. Undefined, implementation-dependent and run-time errors
14. Review heuristics
15. Versions: items with and without a mark
16. Limitations of the source

---

## 0. Conventions

- **(Ref p.N)** is the **PDF** page, not the printed one (the back-of-book index uses the printed one; see section 16).
- **[inference]** marks a heuristic or consequence derived by the distillers, with no corresponding literal sentence in the source. The rest follows the cited text.
- Version marks ("Added in", "Changed in", "Deprecated since") follow the text. "Version not stated in the text" = the source does not mark it; the agent must not fill it in from memory without warning.
- "CPython" = the text labels the passage as an implementation detail, with no language guarantee.
- The source is the Language Reference: it does not cover the standard library (`importlib`, `functools`, `annotationlib`, `typing`...), only the point of contact with the language.

---

## 1. "Where to look" map (topic → Ref pages)

| Topic | Pages |
|---|---|
| Table of contents of the chapters | 1–10 |
| Introduction, alternative implementations, PEG notation, lexical vs. syntax | 11–13 |
| Lines, comments, encoding, joining, indentation | 15–18 |
| Names, keywords, soft keywords, `_*`, `__*__`, `__*` | 18–20 |
| Strings/bytes 20–24; f-strings 24–26; t-strings 26; numbers 26–29; operators 29–30 | 20–30 |
| Objects, identity, mutability, GC | 31–32 |
| Standard types: singletons, numbers, sequences, set, dict 32–35; callables 35–38; modules 38–41; classes and instances 41–43; code/frame/traceback/slice 43–49 | 32–49 |
| Special methods: principle 49–50; `__new__/__init__/__del__`, comparison, `__hash__`, `__bool__` 50–53; attributes 53–55; descriptors 55–56; `__slots__` 57 | 49–57 |
| Class creation 57–61; `__instancecheck__` 61; generics 61–63; `__call__` 63; containers 63–65; numeric 65–67 | 57–67 |
| Context managers 67–68; `__match_args__` 68; buffer 68–69; annotations 69; special-method lookup 69–70; coroutines 71–73 | 67–73 |
| Execution: blocks, binding, resolution, annotation scopes, builtins, `eval/exec` 75–78; exceptions 78–79 | 75–79 |
| Import: search, `sys.modules`, finders/loaders 81–87; path based finder 88–89; replacing, relative, `__main__` 89–91 | 81–91 |
| Expressions: atoms, mangling 93–95; displays 95–97; `yield` 97–101; primaries, calls, `await` 101–104; operators 105–112 | 93–112 |
| Simple statements 113–124; compound 125–148 (try 127–129, with 130–131, match 131–139, def 139–141, class 141–142, coroutines 142–144, type params 144–147, annotations 147–148) | 113–148 |
| Top-level components 149–150; full grammar 151–168 | 149–168 |
| Glossary 169–186 (from the start up to "argument" not distilled); appendices B–D 187–210; index 211–225 | 169–225 |

---

## 2. Lexical structure

### 2.1 Lines, encoding, joining

- `LF`, `CR LF` and `CR` become `LF`, including inside strings, and may be mixed in the file (Ref p.15).
- Encoding declaration: a comment on the first or second line matching `coding[=:]\s*([-\w.]+)`, on its own line; on the second, the first must also be only a comment. Without a declaration: UTF-8; a leading BOM is ignored; undecodable source is a `SyntaxError` (Ref p.15–16).
- Explicit joining (`\`): backslash at end of line, no comment after it, does not continue a comment or a token (except a string); illegal in other positions. A space after the backslash breaks the joining [inference] (Ref p.16).
- Implicit joining inside `()`, `[]`, `{}`: comments allowed, indentation irrelevant, blank lines allowed, no NEWLINE. Triple-quoted strings cannot hold comments (Ref p.16).
- Lines with only whitespace/comment are ignored. In the REPL, a completely empty line ends a multiline statement, behavior that may vary (Ref p.16).

### 2.2 Indentation

- Tabs expand to the next multiple of 8. A mix whose meaning depends on the tab value → `TabError`. Platforms may limit the depth (Ref p.16–17).
- The stack starts at 0: a greater level pushes and generates INDENT; a smaller one must match a value on the stack and generates one DEDENT per popped value; at end of file, a DEDENT for each value > 0 (Ref p.17).
- Formfeed outside the start of indentation: **undefined**. Between tokens, whitespace is only needed if joining would form another token (`ab` vs `a b`) (Ref p.17).

### 2.3 Names and reserved words

- ASCII `A-Z a-z _` (digits except at the start), no length limit, case-sensitive. Identifiers are normalized to **NFKC**; distinct compatibility spellings can be the same name (Ref p.18).
- 35 keywords: `False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield`. `print`, `exec`, `match`, `case`, `type`, `_` are not in the list (Ref p.19).
- Soft keywords: `match`, `case`, `_` only inside `match`; `type` only in the `type` statement (Changed in 3.12 for `type`). Decided in the parser, so they remain valid as ordinary names elsewhere (Ref p.19).
- `_*` is not imported by `import *`. `_` is a wildcard in `case`; in the REPL it holds the last result. `__*__` belongs to the interpreter: use outside the documented ones may break without warning; do not invent dunders. `__*` in a class undergoes mangling (section 8.1) (Ref p.19–20).

### 2.4 Strings and bytes

- Prefixes `b r f t u` (case-insensitive), attached to the quote; `r` combines with `f`, `t`, `b`; `u` has no effect; `rb` = `br` (Added in 3.3) (Ref p.21).
- Escapes: `\<newline>`, `\\ \' \"`, `\a \b \f \n \r \t \v`, `\ooo`, `\xhh`, `\N{name}`, `\uxxxx`, `\Uxxxxxxxx`. In bytes, `\N \u \U` count as an unrecognized escape (Ref p.21–23).
- Octal > `0o377`: `DeprecationWarning` (3.11), `SyntaxWarning` (3.12), **in the future `SyntaxError`**. Unrecognized escape (`'\q'`) keeps the backslash: `DeprecationWarning` (3.6), `SyntaxWarning` (3.12), in the future `SyntaxError` (Ref p.22–23). Typical case: regex and Windows paths without `r` (`\t` becomes a tab) [inference].
- Bytes: only ASCII in the literal, >= 128 by escape; produces `bytes` (Ref p.23–24).
- Raw: `r"\""` has 2 characters; `r"\"` is invalid (odd number of backslashes at the end); backslash+newline are two characters (Ref p.24).

### 2.5 f-strings (Added in 3.6; Ref p.24–26)

- Expressions evaluated at run time, left to right, in the context of the literal. Syntax `{expr[=][!conv][:spec]}`; `{{`/`}}` give literal braces.
- An empty expression is an error; `lambda` and `:=` require parentheses (otherwise the `:` starts the spec). Line breaks and comments in the field are allowed (comments: Changed in 3.12); after `#` everything is a comment, including `}` and quotes.
- `=` (Added in 3.8): shows the expression text, `=` and the value, with spaces preserved; uses `repr()`, but **with a format spec it uses `str()`** unless `!r`.
- `!s !r !a` and then `format()` calls `__format__` with the spec. The spec accepts nested fields, **not a second level**. A field cannot be split between concatenated literals.
- Changed in 3.12: the same quotes inside the field and backslashes in the field became valid; before that the code does not run [inference].
- An f-string is never a docstring (`__doc__` stays `None`).

### 2.6 t-strings (Added in 3.14; Ref p.26)

- Same syntax and evaluation, but the result is `string.templatelib.Template`, not `str`. It does not use `format()`: conversion and spec go to an `Interpolation` per expression; whoever processes the `Template` decides. Nested specs are evaluated first (`{amount:.{precision}f}` → `'.2f'`). With `=`, the text is appended to the previous literal and `conversion` is `'r'` by default. Source of the rules above: Ref p.26. The Reference's back-of-book index (Ref p.224) also lists t-strings, but with the printed numbering, which differs from the PDF's.

### 2.7 Numbers (Ref p.26–29)

- Literals have no sign (`-1` is unary). Not everything that `int()/float()/complex()` accept is a literal.
- Underscore only between digits (`_123`, `321_`, `123__321` invalid); one is allowed after the base (`0x_1f` ok; `0_x1f`, `0x__1f` not). Changed in 3.6.
- Leading zeros in a non-zero decimal are invalid (`0123`); `0`, `00` are valid. In floats they are valid (`077.010`); the integer or fractional part may be missing, not both.
- `3+4.2j` is three tokens; `j` does not separate from the number; `10j` is an imaginary based on float.

---

## 3. Data model

### 3.1 Identity, mutability, life cycle

- Every object has identity, type and value. `is` compares identity; `id(x)` is the address in CPython (Ref p.31).
- Mutability belongs to the type. An immutable container can "change value" if it holds a mutable that changes (tuple with a list) (Ref p.31–32).
- Objects are never explicitly destroyed; collection may be postponed or omitted. CPython: refcount + optional/delayed cycle detection, **no guaranteed cycle collection**. Do not depend on immediate finalization: close resources with `close()`, `try...finally` or `with`. Tracing and a caught exception can keep objects alive (Ref p.31).
- Immutables may be reused: `a = 1; b = 1` → `a is b` varies. **Do not use `is` for values.** `e = f = []` is the same object; `c = []; d = []` is not (Ref p.32).

### 3.2 Standard types

- `NotImplemented`: numeric and comparison methods **return** it (do not raise) to trigger the reflected method/fallback. Boolean context: deprecated (3.9) and, in 3.14, `TypeError` (Ref p.32).
- `bool` is a subtype of `int`; it only differs in conversion to string (Ref p.33). Float: range/overflow depend on the machine.
- Sequences: a negative index adds the length "in some, including built-ins"; a slice returns the same type. A one-element tuple requires a comma (Ref p.33–34).
- Sets: unordered, no index; `1` and `1.0` are equal, only one fits; `frozenset` is hashable (Ref p.34–35).
- Dict: constant hash in keys; `1`/`1.0` same entry. Insertion order: replacing a value does not change the order; removing and reinserting sends it to the end. Guaranteed since 3.7 (3.6: CPython detail; before: unordered) (Ref p.35).

### 3.3 Callables

- User function: `__globals__`, `__closure__` read-only (`cell_contents` is writable). Writable: `__doc__ __name__ __qualname__(3.3) __module__ __defaults__ __code__ __dict__ __annotations__ __annotate__(3.14) __kwdefaults__ __type_params__(3.12)`. Arbitrary attributes only on user functions (CPython) (Ref p.35–36).
- Method: obtained from a function/`classmethod` **as a class attribute**. `x.f(1)` ≡ `C.f(x, 1)`; in a classmethod, `__self__` is the class. A function stored in the **instance** `__dict__` does not become a method (Ref p.37).
- A function with `yield` always returns an iterator; `return` raises `StopIteration`. Classes pass arguments to `__new__` and `__init__`; an instance is only callable with `__call__` on the class (Ref p.37–38).

### 3.4 Modules as objects (Ref p.38–41)

- `m.x` ≡ `m.__dict__["x"]`. Creating dynamically: prefer `importlib.util.module_from_spec()` over `types.ModuleType`.
- Except for `__name__`, rely on `__spec__`; changing `__spec__.name` does not change `__name__`.
- `__package__`: default `None` (3.4); prefer `__spec__.parent`; `ImportWarning` (3.10), `DeprecationWarning` (3.12); **deprecated since 3.13, removal in 3.15**. `__file__`/`__cached__` are optional; setting `__cached__` without `__spec__.cached`: deprecated 3.13, removed in 3.15.
- Module `__dict__`: read-only, inaccessible as a global. CPython: the dict is **cleared** when the module goes out of scope, even with references; copy the dict or keep the module.

### 3.5 Classes and instances (Ref p.41–43)

- Lookup in the class and bases by **C3 MRO**. Assigning a class attribute writes to the class itself, never to the base.
- Attributes: `__name__ __qualname__ __module__ __dict__(mappingproxy) __bases__ __doc__(not inherited) __mro__`; `__annotations__` (use `annotationlib.get_annotations()`; direct access may return annotations of the wrong class under `from __future__ import annotations`); `__annotate__` (3.14); `__type_params__` (3.12); `__static_attributes__`, `__firstlineno__` (3.13).
- Instance: the instance dict first, then the class (a function becomes a bound method), lastly `__getattr__`. Assignment/`del` act on the instance, unless `__setattr__`/`__delattr__` is on the class. Not every instance has a `__dict__`.

### 3.6 Code, frame, traceback (Ref p.44–49)

- A code object does not store globals or defaults. `f_locals` is a proxy in optimized scopes (Changed in 3.13). `f_trace_opcodes` with a trace exception escaping: **undefined**. `frame.clear()` on an active frame: `RuntimeError`. Traceback instantiable and `tb_next` writable since 3.7; line number may diverge in `try` without a matching `except` or with `finally`.

### 3.7 Equality, ordering, hash

- `object`: `==` by identity; ordering raises `TypeError`. **No implicit relations** between operators; `functools.total_ordering()` completes ordering. Reflection: `__lt__`↔`__gt__`, `__le__`↔`__ge__`, `__eq__`/`__ne__` to themselves. A subclass (direct or indirect, not virtual) of the left operand has priority with the reflected method (Ref p.52).
- `__hash__`: equal ⇒ same hash; recommended `hash` of a tuple of the components of `__eq__`. Value truncated to `Py_ssize_t` (`sys.hash_info.width`) (Ref p.52–53).
- `__eq__` without `__hash__` → `__hash__` becomes `None` (instance not hashable; `Hashable` correct). Keep: `__hash__ = ParentClass.__hash__`; suppress: `__hash__ = None`. A `__hash__` that only raises `TypeError` is **misidentified**. A class without `__eq__` should not define `__hash__`; a mutable one with `__eq__` should not either (Ref p.52–53).
- Explicit `__hash__ = None` is only needed when the class does **not** override `__eq__` and wants to suppress the hash (Ref p.53); if it overrides `__eq__` without defining `__hash__`, the interpreter already sets it to `None` (Ref p.53). With value-based `__eq__`, `__hash__ = Parent.__hash__` (hash inherited by identity) tends to break the contract that equal objects have the same hash [inference]; the contract itself is Ref p.52.
- The hash of `str`/`bytes` is salted (randomized, 3.3); it affects set iteration order, never guaranteed (`PYTHONHASHSEED`).
- `__bool__`; otherwise `__len__`; otherwise always true (Ref p.53).

---

## 4. Attributes, descriptors, slots, class creation

### 4.1 Attribute hooks (Ref p.53–55)

- `__getattr__` only when the default access fails with `AttributeError` (including from a `property`); `__setattr__` is always called (intentional asymmetry).
- `__getattribute__` is unconditional; accessing via `object.__getattribute__`/`object.__setattr__` avoids recursion. Implicit special-method lookups **ignore** `__getattribute__` (section 5.1).
- Module: `__getattr__` and `__dir__` (Added in 3.7) only apply to access by attribute syntax, not to globals read inside the module or via `globals()`. Writable module `__class__`: Changed in 3.5.

### 4.2 Descriptors (Ref p.55–56)

- Defines `__get__`, `__set__` or `__delete__` and only acts as an attribute of the owning class. `instance` is `None` on access through the class; `__getattribute__` always passes both arguments.
- **Data descriptor** (`__set__`/`__delete__`) beats `instance.__dict__`; **non-data** (only `__get__`) can be shadowed. Functions, `staticmethod`, `classmethod` are non-data (the instance replaces the method); `property` is data.
- Without `__get__`, access returns the descriptor itself (unless there is a value in the instance dict).
- `a.x` → `type(a).__dict__['x'].__get__(a, type(a))`; `A.x` → `.__get__(None, A)`; `super(A, a).x` searches after `A` in the MRO. The lookup does not include metaclasses.

### 4.3 `__slots__` (Ref p.57)

- Prevents automatic `__dict__` and `__weakref__` (less memory). Outside the slots: `AttributeError`, unless `'__dict__'`/`'__weakref__'` is included. A subclass without `__slots__` gets `__dict__` back.
- Slots are class descriptors: **a same-named class attribute overrides the descriptor**. Redefining a base's slot: meaning **undefined**.
- `TypeError` with non-empty slots in a subclass of `int/bytes/tuple` or with several bases that create slot attributes. A dict in `__slots__` serves as docstring; an iterator leaves `__slots__` empty. Assigning `__class__` requires the same slots (`__slots__` rules: Ref p.57). The glossary says the technique is somewhat hard to get right and should be reserved for cases that justify it (Ref p.183).

### 4.4 Class creation (Ref p.57–61)

- `__init_subclass__` (Added in 3.6): called on the immediate parent via the MRO; implicit classmethod; receives kwargs from the `class` line (forward the rest with `super().__init_subclass__(**kwargs)`; the one from `object` rejects arguments). `metaclass=` never arrives. Different from a class decorator.
- `__set_name__(owner, name)` (Added in 3.6): called by `type.__new__`; assigning later (`A.x = c`) does **not** trigger it.
- Steps: `__mro_entries__` (an empty tuple ignores the base), metaclass, `__prepare__` (classmethod; without it, an empty ordered mapping), body, creation. Metaclass: `type` if none; an explicit one that is not `type` is used directly; otherwise the most derived, with no common candidate → `TypeError`.
- Body ≈ `exec(body, globals(), namespace)`: **methods do not see names from the class scope** (use `self`/`cls` or `__class__`). `__class__` is an implicit closure if any method uses `__class__`/`super`. CPython: the metaclass must propagate `__classcell__` to `type.__new__`, otherwise `RuntimeError` (since 3.8).
- Order: `__set_name__` hooks, then `__init_subclass__`, then class decorators, then the name binding. The final `__dict__` is an ordered copy in a read-only proxy.
- `__instancecheck__`/`__subclasscheck__` are looked up on the metaclass (`ABCMeta`: virtual bases) (Ref p.61).
- Generics: `C[int]` requires `__class_getitem__` (automatic classmethod). `obj[x]`: the type's `__getitem__`; otherwise `__class_getitem__` if it is a class; otherwise `TypeError`. `list[int]` returns `types.GenericAlias`. A metaclass with `__getitem__` (e.g. `EnumMeta`) has priority. Use outside type hints is discouraged (Ref p.61–63).

---

## 5. Special methods and protocols

### 5.1 Principle and lookup

- `x[i]` ≈ `type(x).__getitem__(x, i)`: lookup on the **type**. `c.__len__ = lambda: 5` and `len(c)` → `TypeError`. Implicit lookup ignores `__getattribute__`, even a metaclass's (Ref p.49, p.69–70).
- `None` in a special method = operation unavailable (`__iter__ = None` → `iter()` gives `TypeError` without falling back to `__getitem__`). **In numeric operators, `None` blocks the fallback to the reflected method** (Ref p.50, p.66).

### 5.2 Construction and destruction

- `__new__` returns the instance; if it is a `cls`, `__init__` runs; otherwise it does not. `__init__` must call the base and **may only return `None`** (`TypeError`) (Ref p.50).
- `__del__`: resurrection possible; a new `__del__` depends on the implementation (CPython: once); no guarantee at exit; alternative `weakref.finalize`; `del x` only decrements. Exceptions are ignored (warning on `sys.stderr`); can run in any thread (deadlock with locks) and at shutdown, with globals already deleted or `None` (Ref p.50–51).
- Cycles in CPython: a caught exception in a local → traceback → locals of all frames (Ref p.51).
- `__format__` returns a string; the one from `object` rejects a non-empty spec (3.4); `object.__format__(x,'')` = `str(x)` (3.7) (Ref p.51–52). Rich comparisons may return any value; in boolean context `bool()` applies.

### 5.3 Containers (Ref p.63–65)

- Complete mapping: `keys values items get clear setdefault pop popitem copy update` (`MutableMapping` helps). Sequences: concatenation/repetition, no other numeric operators. `in`/iteration: keys in mappings, values in sequences.
- `__len__` >= 0; CPython <= `sys.maxsize`, otherwise `OverflowError`; defining `__bool__` avoids this. `__length_hint__` is only an optimization (3.4).
- Slicing passes a `slice` to `__getitem__/__setitem__/__delitem__`, omitted parts `None`. Errors: `TypeError`, `IndexError`, `KeyError`. The old protocol depends on `IndexError`. `__missing__`: called by `dict.__getitem__` in subclasses.
- `__iter__` returns a **new** iterator. `reversed()`: `__reversed__`, otherwise `__len__`+`__getitem__`. `in`: `__contains__`, `__iter__`, `__getitem__` until `IndexError` (Ref p.65, p.109).

### 5.4 Numbers (Ref p.65–67)

- Unavailable operation: do not define. Incompatible operands: **return `NotImplemented`**. `__divmod__` ≡ `__floordiv__`+`__mod__`; `__pow__`/`__rpow__` accept a 3rd argument (3-argument `pow()` tries `__rpow__`: Changed in 3.14).
- Reflected only with different types and an unsupporting left operand, or a right operand that is a subclass; if the right one is a subclass with a **different** reflected method, it runs before the left one's direct method.
- `x += y`: `__iadd__` and **binds the result**; without it or with `NotImplemented`, falls back to `__add__`/`__radd__`.
- `__index__`: lossless conversion (slicing, `bin/hex/oct`) and fallback for `int()/float()/complex()`. `int()` no longer delegates to `__trunc__` (3.14).

### 5.5 Context manager (Ref p.67–68, p.130)

- `__enter__` returns the `as` value. `__exit__(type, value, tb)` receives `None`s without an exception. **A true return suppresses**; `__exit__` does not re-raise the exception it received. Methods come from the type. If `__enter__` returned, `__exit__` always runs; failing to assign to the target counts as an error in the suite.

### 5.6 Others

- `__match_args__` (3.10): tuple of strings; without it, no positional pattern (Ref p.68). Buffer (3.12): `__buffer__` returns `memoryview`; `__release_buffer__` returns `None` (Ref p.68–69).
- Annotations (3.14): `__annotations__` is lazy and can run code/raise. `__annotate__(format)` always supports `VALUE` (only there `NameError`); unsupported format: `NotImplementedError` (Ref p.69).

### 5.7 Iteration (glossary)

- Iterator: `__next__` raises `StopIteration` and keeps raising it; `__iter__` returns itself. A container produces a new iterator per `iter()`; **an iterator does not** (the second pass is empty). Iterable: sequences, dict, files, classes with `__iter__` or sequence-style `__getitem__` (Ref p.177–178).

### 5.8 Awaitables and async (Ref p.71–73)

- Awaitable (3.5): `__await__` returning an iterator; `async def` and `types.coroutine()` qualify. A coroutine ends with `StopIteration.value`, must not leak `StopIteration`, has `send/throw/close`. Double await: `RuntimeError` (3.5.2). 3-argument `throw` deprecated (3.12). `close()` raises `GeneratorExit` and marks it finished.
- Async iterator: `__aiter__` must return an async iterator (3.7: another return → `TypeError`); `__anext__` returns an awaitable and raises `StopAsyncIteration`. Async CM: `__aenter__`/`__aexit__`.

---

## 6. Execution model (Ref p.75–79)

- Blocks: module, function, class; also interactive command, script, `-c`, `-m`, string of `eval/exec`. Binding: parameters, `class`, `def`, `:=`, targets (`for`, `as` of with/except/except*/pattern, captures), `import`, `type`, type params; `del` counts for scope. `import *` only in a module.
- Binding at **any point** makes the name local in the whole block; reading before → `UnboundLocalError` (subclass of `NameError`). Locals come from the text; no declarations. (Ref p.76)
- `global`: module global, then builtins; if absent, creates it in the global; before any use (`global`: Ref p.76 and p.122). `nonlocal`: nearest enclosing function, otherwise `SyntaxError`; type params cannot be rebound with `nonlocal` (`nonlocal`: Ref p.76 and p.123).
- **Class scope does not reach** methods, nor comprehensions/generator expressions in the body (`b = list(a + i for i in range(10))` fails); does not apply to annotation scopes. Unbound class locals go to the global. (Ref p.76)
- Free variables resolve at **run time**: the function sees the current global value (Ref p.78). A nested scope reads; writing requires `nonlocal` (Ref p.123). "Optimized scope" (functions, generators, coroutines, comprehensions, genexps) has locals known at compile time (Ref p.180).
- Annotation scopes (3.12; type param defaults 3.13; annotations 3.14): function/variable annotations, type params, bounds/constraints/defaults, value of `type`. In a generic function, **defaults and decorators stay outside**; in a generic class, bases/kwargs inside, decorators outside. `yield`, `yield from`, `await`, `:=` are forbidden (allowed in nested scopes); they see the immediate class's namespace; the inner name does not enter `__qualname__`.
- Lazy: errors (`ZeroDivisionError` in the example) only on accessing `__value__`, `__bound__`, annotations; enables recursive aliases. In 3.14, an annotation with a name defined later only fails (`NameError`) when evaluated [inference]. (Ref p.78 for the lazy behavior of `__value__`/`__bound__` and recursive aliases)
- `__builtins__` is an implementation detail; change builtins via the `builtins` module. `eval/exec` resolve in the caller's local/global; free names go to the global, not to the enclosing one (Ref p.78).
- Exceptions: termination model. `except` matches a class or a **non-virtual** base (a virtual ABC does not count). **Exception messages are not API** (Ref p.79).

---

## 7. Import system (Ref p.81–91)

- `import` = search (`__import__`) + binding. Calling `__import__()` directly only searches (effects on `sys.modules`/parents). Not found → `ModuleNotFoundError`.
- Package = module with `__path__`. Regular: with `__init__.py`. Namespace (3.3, PEP 420): no `__init__.py`, portions in several locations, `__path__` redoes the search if the parent or `sys.path` changes. `foo.bar.baz` imports each level.
- **`sys.modules`** comes first: `None` → `ModuleNotFoundError`; absent → search. Deleting the key invalidates; **old reference + reimport = two modules**; `importlib.reload()` reuses the object.
- Finders return specs (Changed in 3.4); loaders execute. Hooks: `sys.meta_path` (before everything except the cache) and `sys.path_hooks`. `find_spec(name, path, target)`: `None` continues; end → `ModuleNotFoundError`; another exception aborts. **To block a module, raise `ModuleNotFoundError`.** `find_module` replaced (3.4), `ImportWarning` (3.10), removed (3.12).
- Loading: the module enters `sys.modules` **before** executing (avoids recursion in circular imports); if it fails, only the failed one leaves (on reload it stays). The return is re-read from `sys.modules`, so a module can replace itself: implementation-specific.
- Loader: `exec_module` (return ignored); `load_module()` deprecated. `create_module` (3.4); without it, `DeprecationWarning` (3.5) and `ImportError` (3.6); `ImportWarning` in `load_module` (3.10).
- A loaded submodule becomes an attribute of the parent; `from .foo import Foo` in `spam/__init__.py` leaves `spam.foo` accessible. `__spec__` (3.4) can be `None` in `__main__`. `module_repr()` removed (3.12).
- `.pyc`: timestamp+size; hash-based (3.7) "checked" re-hashes, "unchecked" trusts; `--check-hash-based-pycs`.
- Path based finder: `sys.path`/`__path__`, cache `sys.path_importer_cache` (can hold `None`; removing forces a new search); non-string items ignored; path hooks refuse with `ImportError`. The working directory (`''`) is handled separately, with no fixed cache. Path entry finder: `find_spec(name, target)`; `find_loader`/`find_module` removed (3.12).
- Replacing import: empty `sys.meta_path` and install a hook; replacing `__import__` only affects `import`. Relative: only `from ... import`.
- `__main__`: `__spec__` with `-m` or directory/zip; `None` in interactive, `-c`, stdin and direct file. `__main__` and the importable module are distinct; `if __name__ == "__main__"` only runs when it fills `__main__`.

---

## 8. Expressions

### 8.1 Atoms, literals, mangling (Ref p.93–95)

- Common real type: complex+complex without conversion; float if there is a complex or float; otherwise integers. Changed in 3.14: in `* + -` with a single `complex`, the other becomes `float`.
- **Mangling**: in a class, `__x` (without trailing `__`) becomes `_Class__x` (class name without leading `_`); a class of only underscores: no change; > 255 characters: implementation truncation. Applies to variables, attributes, `import __spam` (without a dot), `from spam import __f`; **not** to `__name__` of nested functions, classes and type aliases.
- Literals are immutable; repetition may or may not return the same object. Adjacent concatenation is syntactic (bytes only with bytes; t-string only with t-string); a forgotten comma in a list of strings merges them [inference]. The comma creates the tuple (except `()`).

### 8.2 Displays, comprehensions, generators (Ref p.95–97)

- Comprehension: the iterable of the leftmost `for` is evaluated in the enclosing scope, the rest in the nested one; the target does not leak; `yield` forbidden (3.8). Async (3.6) only in `async def`; since 3.11 also nested (Ref p.96). The comprehension's own scope (the target does not leak): Ref p.95.
- `{}` is an empty dict. Dict display: repeated key → the last wins, no detection; `**` (3.5). Dict comprehension: key before value (3.8; before, in CPython, value first).
- Generator expression: lazy **except the leftmost iterable**, evaluated immediately. Parentheses may be omitted as the sole argument.

### 8.3 Yield and generators (Ref p.97–101)

- `yield` only in a function; calling does not execute the body; suspension preserves locals, instruction pointer, stack and exception state. A generator not resumed is closed (`close()`) and runs pending `finally`s. The value of `yield` on resuming: `None` or that of `send()`.
- `yield from`: forwards `send/throw` if the subiterator has them; value = `StopIteration.value` (3.3).
- Running generator + any method → `ValueError`. The first `send()` requires `None`. `close()` returns a value if it catches and returns (3.13); `yield` on closing → `RuntimeError`.
- Async: `yield from` is a `SyntaxError`. **Early exit (`break`, cancellation, exception) can run cleanup in the wrong context; call `aclose()`**. The loop uses the finalizer from `sys.set_asyncgen_hooks()`; `aclose()` after termination is a no-op.

### 8.4 Primaries and calls (Ref p.101–104)

- Subscription accepts starred (3.11); a subclass that overrides `__getitem__` reimplements negatives and slices. Without `:` it is a subscription; with `:`, `slice(start, stop, step)` with `None`; with a comma, a tuple.
- Call: all arguments evaluated first; N positionals fill the first N slots; a keyword in a filled slot → `TypeError` (even `None`); an empty slot without a default → `TypeError`. Excess: `TypeError` unless `*id`/`**id`.
- **Defaults evaluated once; mutables shared** (Ref p.103 and p.140).
- **`*expr` is processed before keywords and `**`** even when written after: `f(b=1, *(2,))` → `2 1`; `f(a=1, *(2,))` → `TypeError`. `**expr` requires a mapping with string keys; duplicate → `TypeError`; a non-identifier key only fits in `**kwargs`. Multiple `*`/`**`: 3.5.
- CPython: C functions with `PyArg_ParseTuple()` can have unnamed positionals, not passable by keyword.

### 8.5 Operators (Ref p.105–107)

- `-1**2` = `-1`; `2**-1` = `0.5`; `**` is right-associative. `int ** int` negative → float; `0.0 ** negative` → `ZeroDivisionError`; negative base with fractional exponent → complex (old versions raised `ValueError`, no version stated).
- Sequence * negative = empty. `@` only via `__matmul__`. `/` gives float; `//` rounds toward minus infinity. `%` has the sign of the divisor; `x == (x//y)*y + x%y`. Float: `-1e-100 % 1e100` is exactly `1e100`; `math.fmod()` follows the first operand. No `//`, `%`, `divmod` on `complex`. `+` requires two numbers or two sequences of the same type.
- Bitwise above comparisons: `a & b == c` is `(a & b) == c`.

### 8.6 Comparisons (Ref p.107–110)

- Same precedence for `< > == >= <= != is in` and negations. Chaining ≡ `and` with each operand evaluated once and short-circuiting (Ref p.107).
- NaN: ordering false, `x == x` false, `x != x` true. `None`/`NotImplemented`: use `is` (Ref p.108). `complex` does not order. `str` by code point (`"Ç" == "Ç"` may be false without `unicodedata.normalize()`).
- Sequences only of the same type; equality between different types is false, ordering is `TypeError`; `range` does not order; containers skip equality for identical items. `set`: `<` is subset; `min/max/sorted` on sets **undefined**.
- Contract for your own classes (not enforced): reflexivity, symmetry, transitivity, inversion, consistent hash.
- `in`: list/tuple/set/dict/deque ≡ `any(x is e or x == e ...)`; str/bytes substring (`"" in "abc"` true, Ref p.109). `is` tests identity (Ref p.110); can surprise with GC and free lists (footnote, Ref p.110).

### 8.7 Logical, `:=`, order, precedence

- False: `False`, `None`, zero, empties; `__bool__` prevails. `and`/`or` return the last evaluated operand; `not` returns bool.
- `:=` (3.8) requires parentheses in an expression statement, slicing, conditional, lambda, keyword argument, comprehension `if`, `assert`, `with`, assignments; not needed in `if`/`while`.
- `x if C else y` evaluates `C` first. `lambda` without statements or annotations. Order left→right, but in assignment the right side comes first.
- Precedence (strong→weak): displays; subscription/call/attribute; `await`; `**`; unary; `* @ / // %`; `+ -`; shifts; `&`; `^`; `|`; comparisons; `not`; `and`; `or`; `if-else`; `lambda`; `:=`. They associate left, except `**` and conditional (Ref p.110–112).

---

## 9. Simple statements (Ref p.113–124)

- Expression statement: interactive mode prints `repr()` if not `None`.
- Assignment: `a = b = expr` evaluates `expr` once. Without `*` unpacking requires an equal count; the starred target receives a `list`. `inst.x = inst.x + 1` reads from the instance/class but **writes to the instance** (except descriptors). By index it never appends (`IndexError`); a slice accepts a different size. `a, b = b, a` is simultaneous, but targets are assigned left→right: `i, x[i] = 1, 2` with `x=[0,1]`, `i=0` leaves `x == [0, 2]`. CPython: the target is parsed as an expression and rejected late.
- Augmented: target evaluated once, in-place when possible (`x += 1` ≠ `x = x + 1`); left evaluated **before** right.
- Annotated: one target. In module/class, a simple target collects the annotation lazily (3.14); a non-simple target **never** evaluates it; in a function, never evaluated. Free RHS (3.8).
- `assert` ≡ `if __debug__: if not e: raise AssertionError`; under `-O` it generates no code (side effects vanish); assigning to `__debug__` is illegal.
- `del`: left→right; absent name → `NameError`; removing a local that is free in a nested block: Changed in 3.2.
- `return` only in a function; pending `finally` runs. Generator: `return v` → `StopIteration(v)`; async generator: `return v` is a `SyntaxError`.
- `raise`: without argument re-raises (`RuntimeError` with no active exception). `from Y` → `__cause__`; otherwise the active one becomes `__context__`; `from None` suppresses (3.3). A traceback modified in `except` is kept (3.11).
- `break`/`continue`: only in a loop, without crossing function/class; `break` skips `else`; they run `finally`.
- `import a.b.c` binds `a`; with `as` binds the submodule. `from m import n`: attribute, then submodule, otherwise `ImportError`. `import *`: `__all__` (names must exist) or without leading `_` (includes imported modules); only in a module.
- Future: only after docstring/comments/other futures; today only `annotations` matters; unknown → error; `exec/compile` inherit.
- `global`/`nonlocal`: apply to the whole body; before use, otherwise `SyntaxError` (`global`: Ref p.122; `nonlocal`: Ref p.123); `global` and `nonlocal` are parser directives (programmer's note, Ref p.123), with no effect between `exec()` and the caller (Ref p.123, for `global`). Reading a global does not need `global` (Ref p.122).
- `type` (3.12): `typing.TypeAliasType`, lazy value in `__value__` (Ref p.123).

---

## 10. Compound statements

### 10.1 Suites, if, while, for (Ref p.125–126)

- A one-line suite only with simple statements (`if a: if b:` illegal). A loop's `else` runs when it ends normally, **not after `break`**. `for`: iterable evaluated once; target is not erased; an empty iterable does not even assign the name (`NameError`/`UnboundLocalError` afterwards). `*` in the expression list: 3.11.

### 10.2 try (Ref p.127–129)

- An `except` without an expression is the last. An exception in the `except` expression counts as from the `try`. Optional parentheses for multiple types without `as` (3.14, PEP 758).
- `except E as N`: `N` is erased at the end; copy if needed (traceback-frame cycle) (Ref p.127–128). `sys.exception()` in the handler.
- `except*`: several can run, each once, with a group of the matched ones; a non-group becomes `ExceptionGroup`; leftovers re-raised; empty `except*:`, `break/continue/return` and mixing with `except` are forbidden. Introduction: version not stated in the text.
- `else`: no exception and no `return/continue/break`; its exceptions are not caught by the sibling `except`s.
- **`finally`**: a saved exception is re-raised afterwards; if the `finally` raises, the saved one becomes `__context__`. **`return/break/continue` in `finally` discards the exception** (`try: 1/0 finally: return 42` → 42) and its `return` beats the `try`'s. `continue` in `finally`: legal since 3.8; `SyntaxWarning` for all three in 3.14 (PEP 765).

### 10.3 with (Ref p.130–131)

- Order in section 5.5. Several items ≡ nested (3.1); parentheses to break lines (3.10).

### 10.4 match (Added in 3.10; Ref p.131–139)

- Cases tested in order; the first with a matching pattern and a true guard runs. Bindings survive the block. Failing patterns may have bound names: **implementation-dependent**, as is the effective evaluation of patterns (caching).
- The guard only runs if the pattern matched and may have effects. Irrefutable case without a guard: only one, at the end. OR: only the last subpattern irrefutable; all bind the same names. `as` does not accept `_`.
- Literals: signed numbers, `3 + 4j`, strings, bytes, `None/True/False`; **f/t-strings not**. `==`; singletons with `is`.
- Capture is a simple name, always matches; `_` is a wildcard; a name is bound once (`case x, x` invalid); follows the `:=` rules. **Value requires a dotted name** (`A.B`); without a dot it is a capture.
- Sequence: `()` ≡ `[]`; one star (receives `list`); `str/bytes/bytearray` **never** match; `Sequence` or built-ins with the CPython flag; `len` may be cached.
- Mapping: `Mapping` or flag (`dict`, `MappingProxyType`); literal or dotted keys; `**rest` unique and last; duplicate literal → `SyntaxError`; equal named values → `ValueError`; uses the two-argument `get()` (does not trigger `__missing__`).
- Class: non-type → `TypeError`; `isinstance`; keyword reads attribute (`AttributeError` = failure, another exception propagates); positional via `__match_args__` (errors → `TypeError`). Built-ins (`bool bytearray bytes dict float frozenset int list set str tuple`) accept one positional that matches the whole.

### 10.5 def and class (Ref p.139–142)

- `def` executes: binds the name to a function with the current global; body only on call. Decorators evaluated at `def`, applied bottom-up; any expression (3.9).
- **Defaults evaluated once**, left→right; use `None` and create in the body. A default followed by parameters without default only up to `*`. `*name` tuple; `**name` new ordered mapping; after `*` only keyword; before `/` only positional (3.8). `*args: *expr` (3.11); `def f[T]` (3.12).
- `class` executes in a new frame; no base → `object`. `__dict__` order only reliable right after creation and with `class`. Body attributes are **class** attributes; `self.name = v` creates an instance attribute; **a mutable as a class default surprises**.

### 10.6 Coroutines (3.5; Ref p.142–144)

- `await`, `async for`, `async with` only in a coroutine (`SyntaxError`). `async def` is a coroutine even without `await`. `yield from` in a coroutine: `SyntaxError`. `async`/`await` keywords (3.7). `async for`: `__aiter__` returns the iterator directly; `StopAsyncIteration` triggers `else`.

### 10.7 Type parameters (3.12; defaults 3.13; Ref p.144–147)

- `TypeVar` (`T`), `TypeVarTuple` (`*Ts`), `ParamSpec` (`**P`). Only `TypeVar` has bound/constraints; nothing enforced at run time. Names only exist inside the generic. Bound, constraints and default are not evaluated at creation (without default: `typing.NoDefault`). A generic class implicitly inherits `typing.Generic`.

### 10.8 Annotations (Ref p.147–148)

- 3.14: lazy evaluation; `annotationlib` evaluates. They do not affect execution unless inspected (`dataclasses`, `functools.singledispatch`). `from __future__ import annotations` stores strings; deprecation and removal planned, not before the end of life of 3.13 (PEP 749); with it `get_annotations()`/`get_type_hints()` resolve worse.

---

## 11. PEG grammar and top-level components

- `|` is ordered choice; single quotes keyword, double quotes soft keyword; `~` (cut) commits; `invalid_*` only in a second pass, for messages (Ref p.12, p.151).
- The `:=` target is only `NAME` (p.161). `del` requires end of statement (p.154). Decorator: `'@' named_expression` (p.155).
- In comprehensions `in` and `if` use `disjunction`: ternary/`:=` need parentheses (p.165). `genexp` can be the sole argument (p.163). Subscription accepts `*` (p.163).
- `strings`: (f-string|string)+ or tstring+, without mixing; literal patterns reject f/t (p.134, p.165). `with_item` with `as` requires `,`, `)` or `:` afterwards (p.157). `lambda` without annotations (p.164). Capture/value in patterns have negative lookahead for `.`, `(`, `=` (p.159–160).
- Complete program: only `sys`, `builtins`, `__main__`; interactive requires a trailing blank line in a compound statement; `eval()` ignores leading whitespace (p.149–150). The lexer/parser boundary may be a CPython detail (p.13).

---

## 12. Glossary: terms that change decisions (Ref p.170–186)

- Five kinds of parameter: positional-or-keyword, positional-only (before `/`), keyword-only, `*args`, `**kwargs`; `/` and `*` change the call contract (p.181).
- A closure variable is a free variable defined in an outer function scope; `co_freevars` lists only closure variables (p.172, p.175).
- Hashable: constant hash, `__hash__` and `__eq__`; instances of user classes are hashable by default, with the hash coming from `id()` (p.176).
- Sequence (`__getitem__`+`__len__`) vs. Mapping: `dict` has both but is a mapping. Dict views are dynamic and `list(view)` converts them into a complete list (Ref p.173).
- Decorator `@w` is `f = w(f)` (p.173). EAFP vs. LBYL: in threads, `if key in m: return m[key]` has a race (p.174, p.178). Duck typing avoids `type()`/`isinstance()`.
- Soft deprecated: safe in existing code, no warnings or removal; provisional API: no compatibility guarantee (p.182–184).
- Refcount is not stable across versions; immortal objects (PEP 683). GIL; free threading since 3.13 (`--disable-gil`, `-X gil=0`, `PYTHON_GIL=0`) (p.175–177). At shutdown, destructors and weakref callbacks may find modules unavailable (p.177).
- Text without `encoding=` depends on the locale encoding [inference] (p.179). Type hints are not enforced; `get_type_hints()` does not cover locals (p.185). Alias via `type`: the value is not evaluated at creation, only on accessing `__value__` (Ref p.123); the glossary speaks of a "lazily evaluated" attribute (Ref p.174). The glossary defines "type alias" as a synonym "created by assigning the type to an identifier" (Ref p.185); that an alias by assignment is evaluated immediately is [inference] (the Reference does not use that word at this point).

---

## 13. Undefined, implementation-dependent and run-time errors

Consolidated index; the details are in the indicated sections.

- **Undefined**: formfeed outside the start of indentation (2.2); redefined slot (4.3); `f_trace_opcodes` (3.6); undocumented `__*__` (2.3); `min/max/sorted` on sets (8.6); bindings after a failed `match` (10.4).
- **CPython/implementation**: `id()` and cycle GC (3.1); identity of immutables and literals (3.1, 8.1); function attributes (3.3); clearing of the module dict (3.4); resurrected `__del__` (5.2); `__len__` <= `sys.maxsize` (5.3); `__classcell__` (4.4); `__builtins__` (6); a module that replaces itself in `sys.modules` (7); mangling truncation (8.1); unnamed positionals in C functions (8.4); targets parsed as expressions and `assert` under `-O` (9); `__dict__` order (10.5); sequence/mapping flags in match (10.4); set order and hash (3.7); indentation limit and REPL (2.1, 2.2); borderline float `%`/`//` cases (8.5).
- **Syntax/compilation errors**: undecodable source; stray backslash; `TabError`; `r"\"`; malformed numbers (`0123`, `321_`, `0x__1f`); separated `j`; bytes >= 128 without escape; empty f-string or `lambda`/`:=` without parentheses; late or unbound `global/nonlocal`; `import *` outside a module; `return v` in an async generator; `yield from` in a coroutine/async generator; `await`/`async` outside a coroutine; `yield`/`await`/`:=` in an annotation scope; `yield` in a comprehension; malformed `except*`; unknown future; compound statement in a one-line suite; assigned `__debug__`; `match` with an irrefutable pattern not at the end, OR with distinct names, repeated name, duplicate keys. Unrecognized escape and large octal: `SyntaxWarning` today, `SyntaxError` in the future; `finally` with `return/break/continue`: `SyntaxWarning` in 3.14, not an error.
- **Execution**: `TypeError` (boolean `NotImplemented` in 3.14; non-`None` `__init__`; `__iter__ = None`; `__hash__ = None`; default ordering; slots in `int/bytes/tuple`; incompatible metaclasses; positional patterns; arguments; not subscriptable; invalid `__aiter__`); `RuntimeError` (double await; yield in `close()`; `__classcell__`; `raise` without an active exception; `frame.clear()`); `ValueError` (running generator; equal mapping-pattern keys); `ZeroDivisionError`; `IndexError`; `NameError`/`UnboundLocalError`; `ImportError`/`ModuleNotFoundError`; `AttributeError` outside the slots. An exception in `__del__` is ignored with a warning.
- **C extensions**: a borrowed reference can dangle; the C API without an attached thread state is a fatal error or undefined (Ref p.170–171, p.184).

---

## 14. Review heuristics ("if X, check Y")

No mark = derived directly from a citation; [inference] = derived by the distillers.

1. `is` with numbers, strings, literals → should be `==`; only `None`/`NotImplemented`/singletons (3.1, 8.6).
2. Class with `__eq__` → check `__hash__` and use in set/dict (3.7).
3. Operator/`__eq__` that raises `TypeError` for a strange type → should return `NotImplemented` (5.4).
4. `if`/`bool()` on the result of a hand-called `__eq__`/`__lt__` → `TypeError` in 3.14 if `NotImplemented` [inference].
5. `__init__` with `return value`; `__new__` returning another type (5.2).
6. Custom `__getattribute__`/`__setattr__` → recursion; use `object.*` (4.1).
7. A method overridden by an instance attribute only works because a function is non-data; `property` does not (4.2).
8. Descriptor assigned after the class → call `__set_name__` by hand (4.4).
9. `__slots__` with a same-named class attribute, inheritance with `__dict__`, subclass of `tuple/int/bytes` (4.3).
10. Metaclass + `super()` without arguments → propagate `__classcell__` (4.4).
11. Method or comprehension in the class body reading a class variable → `NameError` (6).
12. Name assigned anywhere in the function and read before → `UnboundLocalError`; external write requires `global`/`nonlocal`, before use (6, 9).
13. Mutable default (`[]`, `{}`) or mutable class attribute as instance state → shared (8.4, 10.5).
14. `inst.x += 1` with a class `x` → writes to the instance (9).
15. `except ... as e` and using `e` afterwards → erased (10.2).
16. `return/break/continue` in `finally` → swallows the exception; `SyntaxWarning` in 3.14 (10.2).
17. `__exit__` with an unintended truthy return → suppresses the exception [inference] (5.5).
18. `except` with a virtual ABC → does not match; logic over `str(e)` → fragile (6).
19. Iterator consumed twice → second time empty (5.7). Genexp with an iterable that may fail → error at creation (8.2).
20. `yield` in a comprehension, `await` outside a coroutine, `yield from` in async → `SyntaxError` (8.2, 10.6).
21. Async generator that may exit early → `aclose()` (8.3).
22. `f(a=1, *args)`, `**` with duplicate keys → `TypeError`; `*` comes before keywords (8.4).
23. `case Name:` meaning to compare → it is a capture; use a dot or a literal (10.4). Irrefutable not at the end or OR with distinct names → `SyntaxError`. A sequence pattern over `str/bytes` never matches. `case C(x)` without `__match_args__` → use keyword.
24. Code that assumes bindings after a failed pattern or the number of pattern/guard evaluations → implementation-dependent (10.4).
25. Strings with `\d`, `\w`, path `\t`, large octal without `r` → `SyntaxWarning` [inference] (2.4). List of strings without a comma → merge [inference] (8.1).
26. f-string with the same quotes, backslash or comment in the field → requires 3.12 [inference] (2.5). Target `t""` → `Template`, not `str` (2.6).
27. `assert` to validate input or with a side effect → vanishes under `-O` (9).
28. `__del__` or GC to release a resource → use `with`/`close()` (3.1, 5.2). Exception stored in a local → cycle (5.2).
29. `import *`/`__all__` → `_x` not exported (2.3, 9). Circular import → module already in `sys.modules`, attributes may be missing [inference] (7). Deleting from `sys.modules` and reimporting → two modules (7). Hiding a module in the finder → `ModuleNotFoundError`.
30. Use of `__package__`, `__cached__`, `find_module`, `load_module`, `module_repr`, 3-arg `throw` → replace with the new equivalent (3.4, 7, 8.3).
31. `if __name__ == "__main__"` and importing the same file → two modules (7).
32. In 3.14, reading `__annotations__` directly or using `from __future__ import annotations` → prefer `annotationlib.get_annotations()`; annotations can run code (3.5, 5.6, 10.8).
33. `if key in m: m[key]` with threads → race (12).
34. Deterministic output by set order → never guaranteed; dict preserves insertion (3.2, 3.7).
35. `-1**2`, `a & b == c`, `not` with comparison → check precedence (8.5, 8.7).

---

## 15. Versions: items with and without a mark

### 15.1 With a mark in the text

- **3.1** multiple items in `with`. **3.2** `del` of a free local. **3.3** `rb`; `__qualname__`; aliases in `\N{}`; randomized hash; namespace packages and `sys.meta_path`; `yield from`; `from None`.
- **3.4** strict `object.__format__`; `__package__` default `None`; finders with specs, `__spec__`, `create_module`, `exec_module`; `__length_hint__`.
- **3.5** PEP 448 (`**` in dict, multiple `*`/`**`, `*` in lists); writable module `__class__`; coroutines, `async for/with`, `await`; `DeprecationWarning` without `create_module`. **3.5.2** double await → `RuntimeError`.
- **3.6** f-strings; underscores; `DeprecationWarning` for escapes; `__init_subclass__`, `__set_name__`; `__package__` ~ `__spec__.parent`; `ImportError` without `create_module`; async comprehensions; `__classcell__`; ordered dict (CPython detail).
- **3.7** guaranteed ordered dict; module `__getattr__`/`__dir__`; instantiable traceback; `object.__format__(x,'')`; hash-based pyc; `async`/`await` keywords; strict `__aiter__`; async genexp in any function.
- **3.8** `:=`; `f"{x=}"`; positional-only; key before value in dict comp; `yield` forbidden in comp; `continue` in `finally`; free RHS in annotated; `RuntimeError` for `__classcell__`.
- **3.9** boolean `NotImplemented` deprecated; decorators with any expression. **3.10** `match`/`case`; `__match_args__`; parentheses in `with`; `ImportWarning` (`find_module`, `load_module`, `__package__`).
- **3.11** large octal with `DeprecationWarning`; starred in subscription and `for`; `*args: *expr`; nested async comprehensions; modified traceback preserved.
- **3.12** `type` soft keyword and statement; type params, annotation scopes, `__type_params__`; new f-strings; `SyntaxWarning` on escapes; 3-arg `throw` deprecated; `__buffer__`; removal of `module_repr`, `find_module`, `find_loader`; `DeprecationWarning` for `__package__`.
- **3.13** `__static_attributes__`, `__firstlineno__`; `f_locals` proxy; type param defaults; `close()` returns a value; `__package__`/`__cached__` deprecated; GIL can be disabled.
- **3.14** t-strings; boolean `NotImplemented` → `TypeError`; lazy annotations and `__annotate__`; `f_generator`; `pow()` with `__rpow__`; `int()` without `__trunc__`; complex+float; `except` without parentheses; `SyntaxWarning` in `finally`.
- **3.15** planned removal of `__package__` and `__cached__` without a spec. **Future version not stated**: large octal and unrecognized escape → `SyntaxError`.

### 15.2 Without a mark (version not stated in the text)

The source describes the rule without saying when it appeared; do not state a version:

- Basic data model: identity, `__new__/__init__/__del__`, comparisons and reflection, `__bool__`, `__len__`, `__getitem__`, `__missing__`, `__contains__`, `__index__`, reflected and in-place operators, `__call__`.
- Attribute hooks, descriptors, `__slots__`, metaclasses, `__prepare__`, `__mro_entries__`, `__class_getitem__`, `__instancecheck__`, mangling.
- Scopes, `global`, `nonlocal`, `eval/exec`; `sys.modules`, `reload`, `__all__`, relative imports.
- Comparison chaining, evaluation order, precedence, lambda, conditional, call semantics and defaults.
- `assert`, `__debug__`, `del`, `raise`, `finally`, `break/continue`, loop `else`, **`except*`/`ExceptionGroup`**, extended unpacking.
- Lexical: NFKC, `TabError`, encoding, line joining, raw, bytes.
- Glossary: GIL, EAFP/LBYL, soft deprecated, provisional API.
- Negative base with fractional exponent: "old versions" with no version (Ref p.105).
- Because it is a release candidate, no statement guarantees the final 3.14 [inference].

---

## 16. Limitations of the source

- **Release candidate** (3.14.0rc3): the final version may differ.
- **PDF extraction**: the back-of-book index has run-together numbers: "len, 2527, 56", "subscription, 2527, 94", "PEP 492, ..., 162165" (probably 25, 27 and 162, 165). Do not use literally (Ref p.215, p.222, p.224).
- **Printed page → PDF**: the index uses the printed numbering. Per the glossary the offset is +8 (async context manager: 162 → 170; `__slots__`: 175 → 183; "Zen of Python": 178 → 186). Applying it to the body is an **unverified** heuristic [inference] (Ref p.170, p.183, p.186, p.214, p.225).
- **Block 4** (p.170–225) is glossary, appendices and index; the language is in p.1–169. The glossary before "argument" (p.169) was not distilled; appendices B–D are almost useless.
- **Gaps in the notes**: section 2.7 of the source (operators and delimiters, p.29–30) was left without rules; details of `str/bytes/int/float/complex` as types, `slice` objects and `staticmethod`/`classmethod` beyond the essentials are missing; the grammar (p.151–168) was summarized only in what changes decisions.
- **Scope**: the source refers to the stdlib without describing it; for APIs of `importlib`, `functools`, `annotationlib`, `typing`, `collections.abc` the Language Reference is not enough.
- **Intermediate notes**: condensed per block; merging by topic may have lost nuances. Version marks copied from the notes, not re-checked against the PDF. The section 14 heuristics without [inference] follow sentences from the text, which rarely phrases review recommendations.
