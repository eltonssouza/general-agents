# Python: versions, marked features and dated content

Support reference of the Python specialist agent. It serves to answer "since which version?", "is this still valid?" and "is this Python 2?" without inventing anything. All data comes from the intermediate notes derived from three sources. Each claim carries its source page in parentheses.

## Contents

0. How to read this file (sources, labels, golden rule)
1. Master table: feature → version (only what the text marks)
   - 1.1 Lexical elements and literals
   - 1.2 Expressions and statements
   - 1.3 Data model
   - 1.4 Execution model and import system
   - 1.5 Interpreter, free-threading, licenses and tutorial
   - 1.6 Marks in the Notes (community source) for Python 3 features
   - 1.7 Agreements and divergences between the sources
2. Features presented without a version mark: "version not stated in the text"
3. Python 2 versus Python 3 (everything [DATED])
4. Dated content in general
5. Warnings about the release candidate nature
6. Gaps: what the sources do not cover
7. Response procedure for the agent

---

## 0. How to read this file

**Sources**

- **Tut** = Python Tutorial 3.14.0rc3, released on October 1, 2025 (Tut p.1). Official, but a release candidate.
- **Ref** = Language Reference 3.14.0rc3 (Ref p.1). Official, but a release candidate.
- **Notes** = "Python Notes for Professionals". Community source that mixes Python 2 and 3. Its version table goes from 3.0 to "[3.7]" (this one in brackets, i.e. still in the future at the time) and from 2.0 to 2.7 (Notes p.27).

**Labels used**

- **[DATED]**: specific to Python 2 or to an old ecosystem; do not present as current practice.
- **[inference]**: a link made by whoever assembled this file, not stated by the text.
- **[extrapolation]**: information that is not in the sources provided. The agent may only use it if it labels it as such.
- **version not stated in the text**: the feature appears, but no "Added in", "Changed in" etc. mark accompanies the passage consulted.

**Golden rule.** If the mark is not in the table of section 1, the correct answer is "version not stated in the text". Do not complete from memory without the [extrapolation] label.

**Warning about the entry itself.** The material consulted is already a summary of marks, not the full text. The notes say that the PDF extraction lost alignments, outputs and indentation in some places (Tut p.60, 62, 96, 122). For any exact number or output, confirm in the original source.

---

## 1. Master table: feature → version

Conventions: "Added" = added; "Changed" = changed; "Deprecated" = marked as obsolete; "Removed" = removed. The Source column gives the page of the text that carries the mark.

### 1.1 Lexical elements and literals (Ref ch. 2)

| Feature | Mark | Source |
|---|---|---|
| Soft keywords | Added 3.10 | Ref p.19 |
| `type` as a soft keyword | Changed 3.12 | Ref p.19 |
| `rb` prefix in literals | Added 3.3 | Ref p.21 |
| `u'...'` prefix reintroduced | no version marked in the Ref (the Notes say 3.3, see 1.6) | Ref p.21 |
| Octal escape above `0o377` | Changed 3.11: `DeprecationWarning`; Changed 3.12: `SyntaxWarning`, with a future `SyntaxError` | Ref p.22 |
| Name aliases in `\N{}` | Changed 3.3 | Ref p.23 |
| Unknown escape sequence | Changed 3.6: `DeprecationWarning`; Changed 3.12: `SyntaxWarning`, future `SyntaxError` | Ref p.23 |
| f-strings | Added 3.6 | Ref p.24 |
| `await` and `async for` in f-strings | Changed 3.7 | Ref p.25 |
| `=` in an f-string (`{x=}` format) | Added 3.8 | Ref p.25 |
| Comments, same quotes and backslashes inside the f-string field | Changed 3.12 | Ref p.25–26 |
| t-strings (template strings) | Added 3.14 | Ref p.26 |
| Underscores in numeric literals | Changed 3.6 | Ref p.27–28 |

### 1.2 Expressions and statements (Ref ch. 6 and 7 and related)

| Feature | Mark | Source |
|---|---|---|
| `yield from` | Added 3.3 | Ref p.98 |
| Dict unpacking in displays (PEP 448) | Added 3.5 | Ref p.96 |
| Several `*` and `**` in calls, flexible order | Changed 3.5 | Ref p.104 |
| `await` as an expression | Added 3.5 | Ref p.104 |
| Asynchronous comprehensions | Added 3.6 | Ref p.96 |
| Asynchronous generator expressions | Added 3.6; Changed 3.7 (allowed in any function) | Ref p.97 |
| `yield` and `yield from` prohibited in comprehensions and genexps | Changed 3.8 | Ref p.96–98 |
| Key→value order in a dict comprehension | Changed 3.8 | Ref p.97 |
| Async comprehensions inside comprehensions in an async function | Changed 3.11 | Ref p.96 |
| Items with `*` in subscription | Changed 3.11 | Ref p.102 |
| 2nd signature of `generator.throw()` and `athrow()` | Deprecated 3.12 (marked "Changed") | Ref p.99, 101 |
| `generator.close()` returns the return value | Changed 3.13 | Ref p.99 |
| `*`, `+`, `-` with a `complex` operand: the other becomes `float` | Changed 3.14 | Ref p.105–106 |
| `@` operator | Added 3.5 | Ref p.106 |
| Iterable unpacking in expression lists | Added 3.5; Added 3.11 (any item may take `*`) | Ref p.111 |
| Walrus operator `:=` | Added 3.8 | Ref p.110 |
| Annotated assignment with a free right-hand side | Changed 3.8 | Ref p.116 |
| Lazy annotations; a non-simple target is never evaluated | Changed 3.14 | Ref p.116, 147 |
| `del` of a name that is a free variable | Changed 3.2 | Ref p.117 |
| `raise ... from None` and `__suppress_context__` | Changed 3.3 | Ref p.119 |
| Bare `raise` re-raises with a modified traceback | Changed 3.11 | Ref p.119 |
| `*` in the `for` expression | Changed 3.11 | Ref p.126 |
| `except` without parentheses (PEP 758) | Changed 3.14 | Ref p.127 |
| `continue` legal inside `finally` | Changed 3.8 | Ref p.129 |
| `SyntaxWarning` for `return`, `break`, `continue` in `finally` (PEP 765) | Changed 3.14 | Ref p.129; confirmed in Tut p.73 |
| Several items in `with` | Changed 3.1 | Ref p.131 |
| Parentheses in `with` | Changed 3.10 | Ref p.131 |
| `match` statement | Added 3.10 | Ref p.131 |
| Positional-only parameters (`/`) | Changed 3.8 | Ref p.140 |
| `*args: *expr` | Changed 3.11 | Ref p.140 |
| Decorators with any `assignment_expression` | Changed 3.9 | Ref p.140, 142 |
| `type` statement and type parameter lists | Added 3.12 | Ref p.123, 140, 142, 144 |
| Defaults in type parameters | Changed 3.13 | Ref p.144 |
| Coroutines (`async def`) | Added 3.5 | Ref p.142 |
| `async` and `await` become keywords | Changed 3.7 | Ref p.142 |
| `from __future__ import annotations` | Warning: it will be deprecated and removed, "not before" the end of life of 3.13; no date | Ref p.147–148 |

### 1.3 Data model (Ref ch. 3)

| Feature | Mark | Source |
|---|---|---|
| `dict` insertion order | Changed 3.7: becomes a guarantee (in 3.6 it was a CPython detail) | Ref p.35 |
| `NotImplemented` in a boolean context | Deprecated 3.9; Changed 3.14: raises `TypeError` | Ref p.32 |
| `function.__qualname__` | Added 3.3 | Ref p.36 |
| `__type_params__` on function and class | Added 3.12 | Ref p.36, 42 |
| Lazy annotations (PEP 649) on function, module and class | Changed 3.14 | Ref p.36, 40–42, 69 |
| `__annotate__` | Added 3.14 | Ref p.36, 40–42, 69 |
| `module.__spec__` | Added 3.4 | Ref p.39 |
| `__package__` and `__loader__` default `None` in `ModuleType` | Changed 3.4 | Ref p.39–40 |
| `__package__` equal to `__spec__.parent` | Changed 3.6 | Ref p.39 |
| Fallback of `__package__`: `ImportWarning` / `DeprecationWarning` | Changed 3.10 / Changed 3.12 | Ref p.39 |
| `__package__` and `__cached__` without a corresponding `__spec__` | Deprecated 3.13; removal planned 3.15 | Ref p.39–40 |
| `__loader__` without `__spec__.loader` | Deprecated 3.12; removal planned 3.16 | Ref p.40 |
| `type.__static_attributes__`, `type.__firstlineno__` | Added 3.13 | Ref p.42 |
| `co_qualname`, `co_positions()` | Added 3.11 | Ref p.45–46 |
| `co_lnotab` | Deprecated 3.12; possible removal 3.15 | Ref p.45 |
| `co_lines()` | Added 3.10 | Ref p.47 |
| `code.replace()` | Added 3.8 | Ref p.47 |
| `f_locals` as a proxy in optimized scopes | Changed 3.13 | Ref p.47 |
| `f_generator` | Added 3.14 | Ref p.47 |
| `frame.clear()` | Added 3.4; Changed 3.13 (suspended frame raises `RuntimeError`) | Ref p.48 |
| Instantiable traceback, writable `tb_next` | Changed 3.7 | Ref p.48–49 |
| `object.__format__` | Changed 3.4 and 3.7 | Ref p.52 |
| Hash randomization by default | Changed 3.3 | Ref p.53 |
| Writable module `__class__` | Changed 3.5 | Ref p.55 |
| Module `__getattr__` and `__dir__` | Added 3.7 | Ref p.55 |
| `__init_subclass__`, `__set_name__` | Added 3.6 | Ref p.58 |
| `__classcell__` not propagated to the metaclass | no "Added/Changed" mark: the text says that, in CPython 3.6+, the cell reaches the metaclass and that not propagating it gives `RuntimeError` in 3.8 | Ref p.60 |
| `__length_hint__` | Added 3.4 | Ref p.64 |
| 3-argument `pow()` tries `__rpow__` | Changed 3.14 | Ref p.66 |
| `int()` no longer delegates to `__trunc__` | Changed 3.14 | Ref p.67 |
| `__match_args__` | Added 3.10 | Ref p.68 |
| `__buffer__`, `__release_buffer__` | Added 3.12 | Ref p.69 |
| `__await__` | Added 3.5 | Ref p.71 |
| `RuntimeError` when awaiting the same coroutine twice | Changed 3.5.2 | Ref p.71 |
| 2nd signature of `coroutine.throw` | Deprecated 3.12 ("may be removed in a future version") | Ref p.71 |
| `__aiter__` and `__anext__` | Added 3.5; Changed 3.7 (`__aiter__` must return an asynchronous iterator, otherwise `TypeError`) | Ref p.72 |
| Async context managers | Added 3.5 | Ref p.73 |

### 1.4 Execution model and import system (Ref ch. 4 and 5)

| Feature | Mark | Source |
|---|---|---|
| Annotation scopes and lazy evaluation (PEP 695) | Added 3.12 | Ref p.77–78 |
| Annotation scopes for type parameter defaults (PEP 696) | 3.13 | Ref p.77 |
| Annotation scopes for annotations (PEP 649/749) | 3.14 | Ref p.77 |
| Import system exposed via `sys.meta_path`; native namespace packages (PEP 420) | Changed 3.3 | Ref p.81, 91 |
| Finders return specs; `find_spec()` replaces `find_module()` | Changed 3.4 | Ref p.83–84, 89 |
| `create_module()` and `exec_module()` (the latter replaces `load_module()`) | Added/Changed 3.4 | Ref p.85–86 |
| Module spec | Added 3.4 | Ref p.87 |
| `DeprecationWarning` if `exec_module()` exists without `create_module()` | Changed 3.5; becomes `ImportError` in 3.6 | Ref p.86 |
| Hash-based `.pyc` | Changed 3.7 | Ref p.87 |
| Use of `find_module()`, `load_module()`, `find_loader()` by import | Changed 3.10: `ImportWarning` | Ref p.84, 86, 89 |
| `find_module()`, `find_loader()` of path entry finders and `module_repr()` | Removed 3.12 | Ref p.84, 87, 89 |

### 1.5 Interpreter, free-threading, licenses and tutorial

| Feature | Mark | Source |
|---|---|---|
| New interactive shell (color, multiline editing, history, paste mode) | Default since 3.13 on Windows and on Unix with curses | Tut p.121 |
| Shortcuts of ch. 16.1 | Only valid in the new shell (3.13+); not valid in the basic REPL | Tut p.121 |
| Disableable GIL (free threading, PEP 703) | 3.13: `--disable-gil` build; run with `-X gil=0` or `PYTHON_GIL=0` | Tut p.130; Ref p.176 |
| "Free-threaded" in the glossary | Cited in *attached thread state* and in *iterator* (no thread-safety guarantee for iterator operations in CPython free-threading) | Tut p.124, 132 |
| Documentation example code with dual license (PSF v2 and Zero-Clause BSD) | Since 3.8.6 | Tut p.144; Ref p.190 |
| MRO algorithm | Used since version 2.3 | Tut p.133; Ref p.179 |
| Compiler `SyntaxWarning` for leaving `finally` | From 3.14 on (PEP 765) | Tut p.73 |
| `repr()` of a float picks the shortest decimal string that identifies the value | From 3.1 on, on most systems | Tut p.116 |
| `-O` and `-OO` options | "Future releases may change the effects of optimization" (warning of a future change, no version) | Tut p.52 |

### 1.6 Marks in the Notes (community source) for Python 3 features

These marks come from a book of the 3.5/3.6 era. They count as "the book says", not as official authority. Where the Ref agrees, the agreement is in 1.7.

| Feature | Mark in the Notes | Source |
|---|---|---|
| `%z` in `strptime`; `datetime.timezone` | 3.x ≥ 3.2 | Notes p.65 |
| `{**d}` and `{**a, **b}` | 3.x ≥ 3.5 | Notes p.128, 155 |
| `collections.ChainMap` | 3.3+ ("new in 3.3") | Notes p.131, 293 |
| `enum` module | 3.4+ (via `enum34` for 2.4–3.3) | Notes p.74 |
| pip included with Python | 2.7.9+ and 3.4+ | Notes p.54 |
| `functools.lru_cache` | 3.2+; `typed` parameter in 3.3 | Notes p.153, 323–324 |
| `str.format_map` | 3.2+ | Notes p.250 |
| f-strings (PEP 498) | 3.6 and above | Notes p.249, 256 |
| `str.casefold` | 3.3 | Notes p.255, 265 |
| `math.isclose` with keyword-only | "3.5 and above" | Notes p.203, 285 |
| `math.inf`, `math.nan` | 3.5 | Notes p.278–282 |
| `math.isfinite` | 3.2 | Notes p.279–282 |
| `itertools.accumulate` | 3.2 | Notes p.310 |
| `async`/`await` | 3.5; `@asyncio.coroutine` with `yield from` was valid from 3.3 until before 3.5 | Notes p.313 |
| `secrets` | 3.6 | Notes p.318 |
| `os.scandir` | 3.5 | Notes p.190 |
| `pathlib` | 3.4 | Notes p.192 |
| `'x'` mode and `FileExistsError` | 3.3 | Notes p.189 |
| `RecursionError` | "from 3.5 on" | Notes p.212, 443 |
| Annotated variables | 3.6 | Notes p.446 |
| `__init_subclass__` (PEP 487) | 3.6 | Notes p.618 |
| Multiple unpackings in the same expression (PEP 448) | 3.5 | Notes p.623 |
| `u` prefix accepted again; `from None`; `flush` in `print` | 3.3 | Notes p.625, 626, 630 |
| `range` with slicing, `index`, `count` | 3.2 | Notes p.627 |
| `@` operator and `__matmul__`; `__truediv__` | 3.5; `__truediv__` marked "Python 3" | Notes p.485–486 |
| `venv` and the `pyvenv` command | 3.3 | Notes p.706 |
| Dictionaries with a new implementation; kwargs order preserved | 3.6, with the caveat of "implementation detail" | Notes p.793–794 |
| `ZipFile` with `with` | 2.7 and Python 3 later than 3.2 | Notes p.586 |
| `nonlocal` | 3.0 | Notes p.94, 100, 210 |

### 1.7 Agreements and divergences between the sources

- **They agree:** `yield from` 3.3 (Ref p.98; Notes p.313, 357); `raise ... from None` 3.3 (Ref p.119; Notes p.626); `__init_subclass__` 3.6 (Ref p.58; Notes p.618); PEP 448 unpacking 3.5 (Ref p.96, 104; Notes p.623); `async`/`await` 3.5 (Ref p.142; Notes p.313); f-strings 3.6 (Ref p.24; Notes p.249).
- **Divergence on dict order:** the Ref marks the guarantee in 3.7 (Ref p.35). The Notes cite 3.6, but with the caveat of "implementation detail" (Notes p.793–794). There is no contradiction: the Ref confirms that in 3.6 it was a CPython detail. For answers, use 3.7 as the start of the language guarantee (source: Ref). The Tut states the order as a current guarantee, without a version (Tut p.45).
- **`u` prefix:** the Ref says it was reintroduced without marking the version (Ref p.21); the Notes say 3.3 (Notes p.625). Cite it as "Notes, community".
- **`long`/`int`:** ch. 1 of the Notes says they were unified (Notes p.37), but ch. 2 still lists four numeric types with `long` (Notes p.57). This is an internal inconsistency of the book; prioritize ch. 1 and treat `long` as [DATED].

---

## 2. Features presented without a version mark

In this section the rule is strict: where the table says "version not stated in the text", the agent must not infer the version. The "Mark in another source" column shows when a different source (almost always the Ref) marks something that the Tut presents without a mark. When no source marks it, the only permitted answer is "version not stated in the text". If the agent offers a number coming from its own knowledge, it must label it [extrapolation].

### 2.1 Table of features

| Feature | Where the sources present it | Version mark | Mark in another source |
|---|---|---|---|
| `match` / `case` statement | Tut p.27–29 (PEP 636) | None in the Tut | Ref: Added 3.10 (p.131) |
| `__match_args__` | Tut p.28 | None in the Tut | Ref: Added 3.10 (p.68) |
| Walrus operator `:=` | Tut p.48 | None in the Tut | Ref: Added 3.8 (p.110) |
| Positional-only parameters (`/`) | Tut p.33–35 | None in the Tut | Ref: Changed 3.8 (p.140) |
| Keyword-only parameters (`*`, PEP 3102) | Tut p.33–35 | None in the Tut nor in the Ref notes consulted | none; the Notes only say that Python 2 does not support keyword-only (Notes p.203) |
| `ExceptionGroup` and `except*` | Tut p.74–76 | version not stated in the text | none |
| `add_note()` | Tut p.74–76 | version not stated in the text | none |
| `@dataclass` | Tut p.88 | version not stated in the text | none |
| f-strings with `=` (`{x=}`) | Tut p.61, 116 | None in the Tut | Ref: Added 3.8 (p.25) |
| `math.isclose` | Tut (examples) | None in the Tut | Notes: "3.5 and above" (p.203, 285) |
| t-strings | Tut glossary (p.123 onward); Ref p.94–95 | None in the Tut | Ref: Added 3.14 (p.26) |
| `type` statement | Tut glossary | None in the Tut | Ref: Added 3.12 (p.123, 140, 142, 144) |
| PEP 649, `annotationlib`, `__annotate__`, "evaluate function" | Tut glossary (p.123, 128, 131, 138, 161) | None in the Tut | Ref: lazy Changed 3.14; `__annotate__` Added 3.14 (p.36, 40–42, 69) |
| `compression.zstd` / `_zstd` / "Zstandard bindings" | Table of contents (Tut p.5–6); glossary and licenses (p.161) | version not stated in the text | none |
| `sys._is_immortal()` and immortal reference (PEP 683) | Tut glossary; PEP cited in the Ref | version not stated in the text | none |
| mimalloc, GUS (Global Unbounded Sequences), `qsbr.c` | Table of contents and licenses (Tut p.5–6, 153, 158, 160–161) | version not stated in the text | none |
| `SyntaxError` message about parentheses in the comprehension target | Tut p.42 | version not stated in the text | none |
| `list(d)` in insertion order | Tut p.45 | Presented as a current guarantee, without a version | Ref: Changed 3.7 (p.35) |
| Guaranteed order of keyword arguments | Tut p.33 | Presented as a guarantee, without a version | Notes: 3.6 with a caveat (p.793–794) |
| Template strings only concatenable with each other | Ref p.94–95 | No "Added in" in that block | The t-strings mark is in ch. 2 (Ref p.26) |
| PEPs of the Ref glossary (492, 525, 683, 703, 519, 362, 420, 3155, 411, 387, 443, 302, 343, 498, 526, 484, 278, 3116, 238) | Ref p.170–185 | No version number in the text | none |

### 2.2 Summary: new features with and without a mark

The Tutorial presents almost everything without a version mark; the Language Reference marks several features. The real situation is mixed:

- **No mark in any source provided:** `ExceptionGroup`/`except*`, `add_note()`, `@dataclass`, `compression.zstd`, `sys._is_immortal()`, mimalloc/GUS, the glossary PEPs, keyword-only `*`.
- **No mark in the Tut, but a mark in the Ref:** `match` (3.10), `:=` (3.8), `/` (3.8), `{x=}` (3.8), t-strings (3.14), `type` statement (3.12), PEP 649/`__annotate__` (3.14). For these, the agent may cite the version provided it says the source is the Ref, not the Tut.

### 2.3 Instruction to the agent for this section

Model answer when the mark is missing: "The text consulted presents `except*` without indicating the version; version not stated in the text." If the user insists, the agent may add, clearly labeled: "[extrapolation] from what I know outside the sources provided, ...", and recommend checking the official documentation.

---

## 3. Python 2 versus Python 3 (everything [DATED])

Everything in the "Python 2 in the Notes" column is [DATED]. The text of the Notes mixes the two worlds; in many examples the code is Python 2 even in sections that look neutral (Notes p.169–170, 190, 193, 198–199, 224, 234, 248, 254). Python 3 equivalents are only given when the sources show them. Where they do not appear, the cell says so.

| Topic | Python 2 in the Notes [DATED] | Python 3 equivalent shown in the sources | Source |
|---|---|---|---|
| `print` | Statement: `print x`, `print >> f, s`, trailing comma to suppress newline; present in dozens of examples | `print(...)` function; `print(file=...)`; `end=` to avoid the line break; `flush` (3.3). In Python 3 the old form is a `SyntaxError` | Notes p.29, 183, 186, 191–192, 460, 626 |
| Bridge between versions | `from __future__ import print_function` (available since 2.6) | Unnecessary in Python 3-only code [inference] | Notes p.28, 183 |
| Division | `/` between integers gives floor; `operator.div`, `__div__`; `from __future__ import division` (2.2+) | `/` is true division; `//` for floor; `__truediv__` | Notes p.80–81, 84, 485–486 |
| Input | `raw_input()` reads text; `input()` evaluates | `input()` | Notes p.46, 185 |
| Text | `str` is bytes; `unicode` and `u''` as a separate type | `str` is Unicode; `bytes` separate | Notes p.37, 39, 267–268 |
| `long` and the `L` suffix | `1234567L`, `0L` | `int` and `long` unified (ch. 1); ch. 2 still lists `long` (inconsistency) | Notes p.37, 57, 102 |
| `range` | `xrange` (lazy); `range` returns a list | `range` is a special type (lazy) | Notes p.114, 157 |
| Dict keys and items | `iterkeys`, `itervalues`, `iteritems`, `has_key`, `viewkeys`, `viewitems`; `d.keys()` returns a list | `.items()` (and so on) | Notes p.130, 155, 642–643 |
| `izip`, `imap`, `ifilter`, `ifilterfalse`, `izip_longest` | `itertools` module and `future_builtins` | `zip`, `map`, `filter` are already lazy; `filterfalse` appears with the mark "3.x ≥ 3.0.0" in the Notes | Notes p.173–174, 307, 364, 367–370 |
| `map`, `filter`, `zip` | Return lists | Return iterators | Notes p.114, 173 |
| `map(None, *seq)` | Used to transpose | Gives `TypeError` in Py3 | Notes p.370 |
| `reduce` | Built in | Not built in; the importable version appears as `functools.reduce` (mark 2.6) | Notes p.159, 217, 325, 627 |
| `cmp()` and `__cmp__` | `cmp(x, y)` and tricks with it | Removed; the Notes say `cmp` was removed (p.104). The distiller's note suggests `functools.cmp_to_key` to adapt old comparators; that name is not cited with a page in the Notes | Notes p.104, 180–181 |
| Comparison between types | `None < number` and "types ordered alphabetically" | `None` is not orderable; `TypeError: unorderable types` (old Py3 message) | Notes p.38, 192, 385 |
| Iterators | `next` method; `g.next()`; compat via `__next__ = next` | `next(g)` and `__next__` | Notes p.113, 157, 197–198, 357 |
| Classes | Old-style (`class Old:`) vs new-style (`class X(object)`); "unbound" methods/`instancemethod` | All new-style; methods are functions | Notes p.226–227, 230–231, 492, 788 |
| `super` | `super(Class, self)` | `super()` without arguments | Notes p.229 |
| Metaclass | `__metaclass__ = X` in the body | `metaclass=X` in the base list | Notes p.242–244, 615, 690 |
| Exceptions: syntax | `except X, e`; `raise E, "x"`; classes that do not inherit from `Exception` | `except E as e` (mark 2.6 in the Notes); `raise ... from` | Python 2 syntax (`except X, e`, `raise E, "x"`): central occurrence in Notes p.628 (section 150.6, "This is the Python 2 syntax"); incidental occurrence in p.444 (`except TailRecurseException, e`). `raise ... from`: Notes p.455 (section 89.12) and p.629. Notes p.455 does not bring the `except X, e` syntax. |
| Exceptions: hierarchy | `StandardError`, `EnvironmentError`, `WindowsError`, `IOError` distinct from `OSError` | Py3 tree with `OSError` and subclasses; `IOError` is a synonym of `OSError` (distiller's observation) | Notes p.450–451 |
| Octals | `0700`, `0755`; leading zeros in `datetime.date(2017, 01, 01)` | `0o700`; a leading zero in a decimal is an error | Notes p.67, 73, 304 |
| Backticks, `<>`, `exec` as a statement, `.encode('hex')` | Old syntax | Py3 equivalents not detailed in the block | Notes p.621–643 |
| Special methods | `__nonzero__`, `__unicode__`, `__div__`, `__delslice__` | `__truediv__` appears; the equivalent of `__nonzero__` does not appear in the block; `__unicode__` with no equivalent given | Notes p.97, 485–486 |
| Renamed imports | `Queue`, `SocketServer`, `SimpleHTTPServer`, `BaseHTTPServer`, `cPickle`, `ConfigParser`, `urllib`/`urllib2` | `queue`, `configparser` (the Notes say this); the other equivalents are not given in the block | Notes p.333, 463–464, 534, 541, 566–569, 702 |
| Reloading a module | built-in `reload()`; `imp` | `importlib.reload` | Notes p.273, 275 |
| Strings | `string.maketrans`, `translate(None, ...)`, `ljust` "deprecated since 2.5" | `str.maketrans` | Notes p.249, 256 |
| Rounding | `round`, `floor`, `ceil`, `trunc` return float; ties round away from zero | Return integers; ties round to even | Notes p.277 |
| Leak in comprehensions | The list comprehension variable leaks | Does not leak (mark "≥ 3.0") | Notes p.794 |
| Power | Negative base and fractional exponent: `ValueError` before 3.0.0 | The Py3 result is not given in the block; it only says that it used to raise an error | Ref p.105; Notes p.373 |
| `hasattr` with a property that raises | Returns `False` | Returns `True` in 3 (according to the Notes) | Notes p.644 |
| `hashlib` | `update("text")` with `str` | `update` requires bytes (`b'...'`) | Notes p.694, 778–779 |
| Representations | `<type 'int'>`, `set(['a','c','b'])`, `<... instance at 0x...>`, `_sre.SRE_Match` | `<class 'int'>` and modern forms [inference: the text only points to the format as Py2] | Notes p.32–33, 78, 398, 496–498 |
| Compatibility libraries | `six`, `future`, `past.builtins`, `from builtins import range`, `six.with_metaclass` | Only relevant in code that must still run on both versions | Notes p.243, 628, 630, 634 |
| Conversion tool | 2to3 (example with `print` and `raw_input`) | Converted code shown as "3.x ≥ 3.0" | Notes p.645–646 |

**Safe use.** If an example in the Notes has `print x`, the agent rewrites it with `print(x)` when reusing it and warns that the original was Python 2. If the example uses a module or function whose Py3 equivalent does not appear in the block, the agent says "equivalent not stated in the sources" and, if it fills it in, labels it [extrapolation].

---

## 4. Dated content in general

### 4.1 Packaging, environments and tools [DATED]

- **Publishing to PyPI:** `.pypirc` with username and password in plain text, URLs `pypi.python.org` and `testpypi.python.org`, `python setup.py register`, `setup.cfg` with `description-file`, "PyPI reads Markdown as plain text" (Notes p.415–417, 436). Treat as historical; check the current flow in the official packaging documentation (the sources provided do not bring the current flow).
- **`distutils.core.setup`, `setup_requires`, `setup.py install` and `develop`:** obsolete in current guidance, according to the distiller's note, which asks for verification (Notes p.435–436).
- **`pip`:** `pip.main([...])` and `pip.get_installed_distributions()` used as an API (Notes p.419–420); `pip list` format with parentheses `docutils (0.9.1)` and `--outdated` with "Current/Latest" (Notes p.421); recipe to update everything by pipe with `cut -d =` (Notes p.422); `pip search` (Notes p.54); `sudo pip` and installation into the system Python (Notes p.421).
- **`easy_install`, `py2app`, `cx_Freeze` via `setup.py install`**, and a note about El Capitan/SIP (Notes p.479–480).
- **`venv`:** `pyvenv` (Notes p.706–707); `execfile(activate_this)` and `lib/python2.7/site-packages` (Notes p.706, 710); conda's `source activate` (Notes p.708); `sys.real_prefix` (Notes p.711).
- **Windows and compilers:** Visual Studio 2008/2010/2015 depending on the Python version, Christoph Gohlke's site, `vcvarsall.bat` (Notes p.424).
- **Installing Python 2.7:** MSI, `C:\Python27`, `wget --no-check-certificate`, build with `make`, "macOS comes with 2.7.10", `brew install python` installing 2.7, "the most recent distributions come with 2.7" (Notes p.51–53).
- **CPython hosting on Mercurial** (`hg.python.org`) (Notes p.568, 609).
- **Third parties with maintenance not confirmed in the text:** `docopt`, `docopt_dispatch` (Notes p.429–432); `MySQLdb`, `cx_Oracle` reflect the ecosystem of the time (Notes p.673, 676).

### 4.2 Tutorial examples that contain old leftovers

- pip/venv example with `Python 3.5.1`, `python35.zip` (Tut p.108).
- Old packages and versions in the pip output: `Requests 2.6.0/2.7.0`, `pip (7.0.3)`, `setuptools (16.0)` and "Running setup.py install" (Tut p.108–109).
- Reference to `comp.lang.python` and a mailing list (Tut p.111).
- URL `worldtimeapi.org` and a 2022 date in the `urlopen` example; current availability is not stated in the text (Tut p.95).
- `locale.setlocale(locale.LC_ALL, 'English_United States.1252')`: Windows-specific (Tut p.100).
- `from decimal import *` in the example (Tut p.104), although the Tut itself discourages `import *` (Tut p.56).
- `AsyncZip` with inheritance from `threading.Thread` and manual `f.close()` (Tut p.101–102), although the Tut recommends `with` (Tut p.63).
- `os.system('mkdir today')` is illustrative; the text points to `shutil` (Tut p.93).
- Outputs of `dir(sys)` and `dir(builtins)`: snapshots of an unstated version; do not use as an inventory (Tut p.53–54).
- Cache name `spam.cpython-33.pyc`: illustrates the module.version.pyc format, not the current version (Tut p.52).
- Section 14.2 of the Tut lists REPL "wishes" (suggested indentation, parenthesis checking). It may be outdated compared to the new shell, but the text does not say so; version not stated (Tut p.113).

### 4.3 Python 3.5 era in the Notes [DATED]

- **asyncio:** `get_event_loop()`, `run_until_complete`, `asyncio.wait([...])` with coroutines, `loop.run_in_executor` with an explicit `loop`, `set_default_executor`; `@asyncio.coroutine` with `yield from` (Notes p.313–316). The distiller says there are strong indications that newer APIs (`asyncio.run`, `gather`, `create_task`) are the current ones and orders checking the official documentation before recommending. Those three names have no version mark in the sources. Treat as [extrapolation] if the agent recommends them.
- **Example outputs of `help()`, console text and the `py` launcher:** reflect 3.4 (Notes p.516–519). Prompt `Python 3.4.3`, dates from 2015–2016 (Notes p.516, 586, 595).
- **`typing`:** `typing.NamedTuple('Point', [...])` and annotation by a `# type:` comment are old forms (Notes p.446). Annotated variables appear with mark 3.6 (Notes p.446).
- **`collections.Iterator` and `collections.Mapping`:** the ABCs were moved to `collections.abc` (Notes p.197, 390). The source points to the change without giving a version.
- **`dis` and `.pyc`:** `PRINT_ITEM`, opcode constants and `code_f.read(8)` to skip the `.pyc` header are Py2/old (Notes p.326–327). Compare with hash-based `.pyc`, Changed 3.7 (Ref p.87).
- Outputs of `argparse` with "optional arguments:", of `timeit`/IPython with "best of 3" and of pytest 2.9.2 on Python 2.7.10 (Notes p.427, 430–431, 765, 769–771).
- **Environments of the time:** Ubuntu 12.04/16.10/17.04, Python 3.4/3.5.1, Django 1.1.1 with py2.6, Sphinx 1.7.dev and pip 9.0.1 in sessions and logs (Notes p.53, 393, 416, 425–426, 656, 716, 745).
- **Missing coverage of a modern feature:** the book does not cite `match`/`case`, which the Ref marks as 3.10 (Notes p.600–603; Ref p.131).
- IronPython and Jython "only 2.7" (Notes p.647) and Python 2 "with updates until 2020" (Notes p.27): state of the time; do not assert the current state.
- `os.system("python child.py &")` (Notes p.551) is considered fragile by the reviewer's observation; `subprocess` would be the way (not confirmed by page). The `ctypes` trick to force deallocation is Py2 (Notes p.525–526).

### 4.4 Dict order: three moments in the sources

1. **Community book, Python 2 world:** `d.keys()` returns a list (Notes p.642–643); for insertion order, `OrderedDict` is recommended (Notes p.793). The distiller's note classifies this recommendation as pre-3.7 context.
2. **Python 3.6 in the Notes:** the "new implementation" preserves kwargs order, with the caveat that it would be an implementation detail (Notes p.793–794).
3. **Ref 3.14:** insertion order is a guarantee since 3.7 (Ref p.35). The Tut treats this as a current fact (Tut p.33, 45).

On dict order: the notes describe the contrast with `OrderedDict` and with lists returned by `keys()`. The literal text of Notes p.289 (section 47.2) says "The order of keys in Python dictionaries is arbitrary", and Notes p.38 calls the dict "An unordered collection". That is the pair to contrast with Ref p.35 (Changed 3.7: insertion order becomes a guarantee). The agent must describe the evolution through the marks above, citing the Notes only with those literal sentences.

### 4.5 Other legacy forms

- `%` operator for formatting: legacy style in examples of the Notes (p.184, 228); the book also shows `str.format` (2.6, PEP 3101) and f-strings (3.6) (Notes p.256–257).
- `with` "added in Python 2.5" (Notes p.408); "Python 2.6+" for `with open` (Notes p.787).
- Tail call decorator (Notes p.443–444): Python 2.4 code. Tail recursion as bad practice remains valid in the sense that Python does not optimize it, according to the Notes (p.443); the stack introspection hack is Py2.

---

## 5. Warnings about the release candidate nature

1. **Document label.** Tut and Ref are "3.14.0rc3" (Tut p.1; Ref p.1). A release candidate is a version under candidacy; the Tut says this only through the "rc3" label, without commenting on the consequences (Tut p.1). The conclusion that details may change before the final version is [inference] from the label; the notes of the Tut and the glossary repeat the same warning (Tut p.119–167; assumptions block).
2. **What is specific to 3.14 and therefore more subject to adjustment.** According to the marks: t-strings (Ref p.26), `__annotate__` and lazy annotations (Ref p.36, 40–42, 69), `except` without parentheses (Ref p.127), `SyntaxWarning` in `finally` (Ref p.129; Tut p.73), boolean `NotImplemented` that raises `TypeError` (Ref p.32), `int()` without delegating to `__trunc__` (Ref p.67), `pow()` with `__rpow__` (Ref p.66), `f_generator` (Ref p.47), arithmetic with `complex` (Ref p.105–106). That they are "more subject to adjustment" is [inference]; the text does not point to any of them as unstable.
3. **Items that the text qualifies as unstable or future.** `-O`/`-OO`: effects may change in future releases (Tut p.52). `from __future__ import annotations`: will be deprecated and removed (Ref p.147–148). Planned removals: `__package__`, `__cached__` (3.15) and `__loader__` (3.16); possible removal of `co_lnotab` (3.15) (Ref p.39–40, 45).
4. **Recommendation to the agent.** When talking about 3.14 behaviors marked in these sources, say "according to the 3.14.0rc3 documentation" and recommend confirming in the documentation of the final version. Do not assert that the final version keeps the behavior (the source does not cover the final).
5. **Warnings that become errors.** The warnings for invalid escape and large octal (Changed 3.12) foresee a future `SyntaxError`, without a version (Ref p.22–23). For new code, avoid.
6. **Free-threading.** Marked 3.13, with `-X gil=0`/`PYTHON_GIL=0` (Tut p.130; Ref p.176). The glossary notes that iterators have no thread-safety guarantee in CPython free-threading (Tut p.132). The text does not say whether this changes in 3.14.
7. **Unresolved references.** The Tut contains loose Sphinx labels (`library-index`, `textseq`, `sys-path-init`, `formatspec`, `bltin-exceptions`) with no content (Tut p.60–61, 72, 117). Do not invent what they say.

---

## 6. Gaps: what the sources do not cover

**Versions and release notes**

- **Python 3.15:** nothing beyond planned removals cited by the Ref (`__package__`, `__cached__`, `co_lnotab`) (Ref p.39–40, 45). No 3.15 release notes.
- **Release notes of versions 3.10 to 3.13:** not provided. The "What's New" documentation is absent. The marks in sections 1.1 to 1.4 come only from "Added/Changed in" scattered through the Ref and the Tut. This means the agent knows the start of each listed feature, but not the set of changes of each release, nor the versions of new standard libraries.
- **Standard library:** the Tut and the Ref are not the Library Reference. Modules appear only as examples. Version marks of modules (`pathlib`, `zoneinfo`, `tomllib` etc.) only exist when the Notes mention them (section 1.6). Any other module version is "version not stated in the text".
- **Python 3.7 to 3.9 in general:** only isolated marks appear in the Ref (section 1). The community book has coverage up to about 3.6/3.7 (Notes p.27, 793).
- **Final Python 3.14:** not covered; only the rc3.

**Content of the sources**

- Coverage of the Tut: the Tutorial was distilled from beginning to end (p.1–167), in three blocks (p.1–55, p.56–118 and p.119–167). Only Appendix B (about the documentation, p.141–142), the text of the licenses and the list of incorporated software (Tut p.143–163, only what has a date or practical impact) and the index (used only as a page map) were left out or summarized. Do not assert that chapters of the Tutorial "were not consulted". 
- External documents cited by the glossary and not provided: annotations-howto, FAQ on arguments vs parameters, Descriptor How To, Sorting HOW TO (Tut p.123, 127, 132). The agent must not invent the content.
- The C API only appears in glossary terms (strong/borrowed reference, thread state) (Tut p.125).
- The Ref's historical table of releases goes from 0.9.0 to 2.2+ (Ref p.189). It is of historical interest and does not cover the 3.x versions.
- Data on current packaging, current static typing, current `asyncio` and modern environment tools: the sources do not provide the current version of these flows. When the agent replaces a dated flow with another, it must label it [extrapolation] and recommend the official source.
- PDF extraction loss: tables of names and phone numbers, squares and cubes, `len` outputs in zlib, results of `random.randrange(6)` and `sum(a)` (Tut p.60, 62, 95, 96); indentation of `with` in PYTHONSTARTUP (Tut p.122). Exact numeric results must be checked in the source.
- Pending checks noted by the distillers ("see verification"): `collections.Iterator` vs `collections.abc`, `IOError` vs `OSError`, `ljust` "deprecated since 2.5" (Notes p.197, 192, 249). The notes ask for confirmation; the sources provided do not bring the answer with a version mark.

---

## 7. Response procedure for the agent

1. **Question "since when does X exist?"** Look for X in section 1. Found: cite the mark and the source. Not found: check section 2. If it is in neither, answer "version not stated in the text".
2. **Community source.** If the only mark is from the Notes, say "according to the community book Python Notes for Professionals". If the Ref diverges, the Ref prevails (as with dict order, section 1.7).
3. **Code with Python 2 syntax.** Recognize it by the signs in section 3 (`print x`, `raw_input`, `xrange`, `iteritems`, `except X, e`, `__metaclass__`, `<type '...'>`, `cmp`). Warn [DATED] and deliver the Python 3 version only when the source shows the equivalent; otherwise mark [extrapolation].
4. **Packaging, pip, venv recipes.** Treat as [DATED] (section 4.1) and point to the official packaging documentation for the current flow, without describing it from memory without a label.
5. **Everything that is 3.14.** Say "3.14.0rc3" and the release candidate caveat (section 5).
6. **Compiler warning messages.** `SyntaxWarning` in `finally` (3.14) must be flagged in code review as a defect/warning (Tut p.73); invalid escape and large octal have the same character (Ref p.22–23).
7. **The agent's links.** Any link not stated by the text carries [inference]; any external information carries [extrapolation].
