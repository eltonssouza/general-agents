# Community sources: reliability register for the Notes

Register for the agent to consult BEFORE repeating anything that comes from "Python Notes for Professionals" (Notes), a community book derived from Stack Overflow Documentation.

## Contents

1. Usage rule
2. Legend (problems, severity, actions)
3. Suspect claims by topic
   - 3.1 Data and structures
   - 3.2 Functions and classes
   - 3.3 Strings, regex and dates
   - 3.4 Modules and stdlib
   - 3.5 Concurrency
   - 3.6 Packaging and environments
   - 3.7 Testing and performance
   - 3.8 Security and cryptography (items not listed in section 4)
   - 3.9 SQL and I/O
   - 3.10 Cross-cutting (CPython, Python 2, quotations)
4. Security: examples from the book the agent must NOT recommend
5. Clear errors in the book itself
6. Quick procedure before citing the Notes

---

## 1. Usage rule

1. **The official documentation prevails.** Tutorial (Tut), Language Reference (Ref) and Library Reference outweigh the Notes. If they diverge, the official one holds; the Notes are not cited as proof.
2. **The Notes are only a complement.** They enter an answer only when the official docs do not cover the point or when the example illustrates something already confirmed.
3. **Always label** what comes from them with **[community]** and the page: `[community] (Notes p.N)`.
4. **Origin of the suspicions.** The distillers stated, in the verification blocks, that they only indicate the reason for the suspicion and do not correct it with a source (notes-3, notes-4). The suspicions come from the distiller's prior knowledge, not from the source text. Hence the correct classification is **"to confirm in the official docs"**, never "false". Exception: what carries the **[int]** mark (internal evidence, such as a contradiction between pages, an undefined name or an example that does not match its own output). That is a book error and is in section 5.
5. **No external knowledge here.** This file does not state what the correct behavior is; it only says where to be suspicious and what to do. The links between items are my [inference].
6. **Target version first.** A good part of the suspicions concerns dated content (Python 2, pre-3.6, old tools). Before citing, define the version and check the docs for that version.
7. **If you cannot confirm**, do not assert. Tell the user the information is community-sourced and unverified.

## 2. Legend

**Problem:** ERR = book error (see section 5) · DAT = dated / probably Python 2 · ABS = too absolute · NS = no source / no measurement · IMP = imprecise or ambiguous · INS = insecure · CONF = only the official docs settle it · [int] = evidence inside the book itself.

**Sev.:** H = high (may induce a serious error or risk) · M = medium · L = low.

**Action:** **DNR** = do not repeat · **VOD** = verify in the official docs before asserting · **WARN** = warn the user of the caveat · **ILL** = treat values/outputs as illustrative, do not cite as a guarantee.

---

## 3. Suspect claims by topic

Each row is a distiller's suspicion (to be confirmed), except where marked [int]. Duplicates across chapters were merged and the pages added up.

### 3.1 Data and structures

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| A1 | Dict is "unordered"; `OrderedDict` for order; outputs in arbitrary order | 38, 76, 118, 129–133, 146, 289, 298, 381, 793 | DAT/ABS. The distillers indicate that recent versions preserve insertion order; the text only cites 3.6 as an implementation detail. Literals: Notes p.289 (section 47.2) says "The order of keys in Python dictionaries is arbitrary" and Notes p.38 says "An unordered collection"; the counterpart to contrast is Ref p.35 (Changed 3.7: insertion order guaranteed). | H | DNR as a general rule; VOD from which version the order is guaranteed; ILL for the outputs |
| A2 | `defaultdict` "never raises KeyError"; with no argument "defaults to None" | 43, 290 | ABS/IMP. Does not say whether reading a missing key inserts it; with a `None` factory the missing key would still raise an error. | M | VOD role of `default_factory`; DNR the absolute sentence |
| A3 | `keys/values/items` in Py3 "are equivalent" to `iter*`; `sort()` to order a dict's result | 132 | IMP | M | VOD (PEP 3106/views) |
| A4 | Order of the combinations in section 19.14 shown as general | 135 | IMP: depends on the order of `options.keys()` | L | ILL |
| A5 | Table of `array` typecodes (`i`=2 B, `u`=2 B, `l`=4 B, `w`, `c`); `pop()` only removes the last | 122, 124 | CONF | M | VOD each code and size in the `array` docs |
| A6 | `reversed('hello')` listed as a sequence type | 37 | IMP | L | DNR |
| A7 | Backslash to break a multidimensional list | 127 | CONF (probably unnecessary) | L | VOD line-joining rules |
| A8 | `list.clear()` with no version; the copy section ends with no content | 139–140 | Truncated passage (probably a lost `list.copy()`) | L | VOD version; DNR the cut-off passage |
| A9 | `zip` returns a list; output of `reversed(numbers)` as a list; `map(float, items)` and `map` with list output | 144, 161, 217 | DAT: Py2 outputs | M | DNR; VOD returned type in the docs |
| A10 | `range` in Py3 "only returns a generator"; `map` in Py3 "is a generator" | 157–158, 638 | IMP | M | VOD types in the docs |
| A11 | `[e for x in y if c]` equals `list(filter(..., map(...)))`; "almost 2x faster" | 152 | The filter/map order looks swapped; performance NS | M | DNR the equivalence and the number |
| A12 | Double comprehension "gives the best time" for flattening; `sum(l, [])` quadratic | 154 | ABS/NS | M | DNR without measurement |
| A13 | `groupby`: "only the last element of the key appears"; `groupby` over `adict.items()` without sorting with result `{1:{...},5:{...}}` | 166–167, 295, 308 | IMP: mechanism poorly explained. [inference] If p.308 is right in saying "only consecutive", the result on p.295 is doubtful. | M | VOD `groupby` semantics in the `itertools` docs |
| A14 | `heapq`: intermediate heap states; without explaining `heappush` or "min-heap" | 176–177 | NS/gap | L | ILL |
| A15 | Comparison (`cmp`) of tuples: "if an element is a number, the other is returned" | 180–181 | DAT/IMP (Py2) | M | DNR |
| A16 | "PEP 8" requires parentheses on a singleton tuple; space between the trailing comma and the bracket | 178, 134 | NS: PEP 8 quotation without an excerpt | L | VOD in PEP 8 |
| A17 | Counter/defaultdict outputs omitted; `ChainMap` iteration shown in a certain order | 288, 293–294 | Incomplete / version dependent | L | ILL |
| A18 | `deque` "thread-safe", performance (Py2 docs); "the only structure with fast queue operations"; list-based `Deque` class mixed with the `collections.deque` table | 292, 335, 772 | DAT/ABS/IMP | M | DNR; VOD in the `collections` docs |
| A19 | `itemgetter`/`methodcaller` "faster" than lambda; `mul('a', 10)` and numeric input requirement | 295–296 | NS | L | DNR without measurement; VOD `operator` docs |
| A20 | `typing.get_type_hints(Foo)` returns `ChainMap` | 446 | CONF | L | VOD return type |

### 3.2 Functions and classes

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| B1 | `global foo` "can be at any point" of the function | 99 | CONF (example puts `global` after the use) | M | VOD rule for the position of `global` |
| B2 | "Control flow does not affect scope (except `except`)" | 96 | IMP: no explanation | M | VOD rule for the name in `except ... as` |
| B3 | `nonlocal` "better implemented with generators" | 94 | NS/opinion | L | DNR |
| B4 | `del v[a:b]` calls `__delslice__`; iterators with `next` | 97, 113 | DAT: Py2 protocol | M | VOD protocol in Py3 |
| B5 | PEMDAS as the precedence rule | 93 | IMP | L | VOD official precedence table |
| B6 | `==` equals "not `<` and not `>`"; overriding two methods is enough; `!=` derives from `__eq__` | 109 | IMP; depends on version and on `__ne__` | M | VOD semantics of `__ne__` and `functools.total_ordering` |
| B7 | `total_ordering` requires `__eq__` + 1 operator (p.324) or also `__ne__` (p.385); "needs all 6 methods" (p.384) | 324, 384–385 | [int] The pages contradict each other; p.384 contradicts the demonstration on p.385. | M | VOD requirements; DNR the counts |
| B8 | `aDate or today` and `if not aDate` "equivalent" to `is None` | 104–105 | ABS: only if no falsy non-None value is valid | M | WARN |
| B9 | "Iterable classes define `__iter__` and `__next__`"; `str` iterable via `__getitem__`; `collections.Iterator` | 197 | IMP/DAT: describes an iterator, not an iterable | M | VOD protocol; use `collections.abc` only after confirming |
| B10 | Recursion limit 1083/1997; 1000 frames; `setrecursionlimit(15000)` "is faster"; "tail recursion is bad practice"; advantages of recursion | 211–212, 442–443 | ABS/NS; values depend on the environment | M | VOD default and risks in the `sys` docs; DNR the opinions |
| B11 | Decorator: no reason to prefer a function over a class; singleton via decorator returns a function; `__get__` explains working in `__init__` | 221, 223, 224, 240–241 | NS/IMP; breaking `isinstance`/inheritance is not mentioned; "not thread-safe" incomplete | M | WARN; VOD |
| B12 | `time.time()` for timing | 224 | CONF | L | VOD which clock the `time` docs indicate |
| B13 | "Only the `__init__` of the first inherited class is called"; MRO "depth first unless a shared parent is blocked"; `FooBar.mro()` and `print` | 233–235 | IMP/DAT | M | VOD MRO and `super()` |
| B14 | Mixins: inheritance order right to left (p.611) versus left to right (p.617); `@property` with "same name because of decorators"; `super().__init__(*args, **kwarg)` in a `str` subclass | 607, 611, 613, 617 | [int] contradiction between pages; doubtful explanations | M | VOD MRO; DNR the explanation |
| B15 | `assert` to validate input; "`assert` + `except AssertionError` may be preferable" | 235–236, 784 | CONF. [inference] The suspicion is that `assert` disappears under interpreter optimization. | H | VOD effect of optimized mode; WARN; DNR for production validation |
| B16 | "Don't check the type, use `str()`/`list()`" | 787 | ABS; the example fails (see E-17) | M | DNR as a rule |
| B17 | "Do not initialize class attributes outside `__init__`" | 788 | ABS | M | DNR as a rule |
| B18 | Mutable defaults (`lst=[]`) in recursion examples; `pos or [0,0]` | 237, 441 | Bad practice in the example | M | DNR; WARN |
| B19 | "Immutables: all operations make copies" | 208 | ABS | L | DNR |
| B20 | Recursive lambda against the cited PEP 8 | 206, 212–213 | Incoherence with the citation | L | VOD |
| B21 | `Vector.__eq__` without discussing `__hash__` | 487 | Gap | M | VOD `__hash__` rules |
| B22 | "Unbound" methods; round-trip `__repr__` with `"Card(%s, %d)"` | 494–495, 500 | DAT (Py2); repr without quotes on the string | L | VOD |
| B23 | Exceptions: `IOError` does not catch `OSError`; Py3 exception tree "incomplete" (no `ModuleNotFoundError`); `raise Outra("...", e)` "reduces the trace" | 450–452, 449 | DAT/CONF | M | VOD hierarchy and chaining in the docs |
| B24 | `NotImplemented` in the area calculation and outputs "None"/"6.0" | 491–492 | See E-25 | M | DNR |
| B25 | Absolute/relative imports "PEP 404" | 636 | CONF: the distiller cites a different PEP | M | VOD PEP number |
| B26 | `unorderable types` examples with error messages | 632 | DAT (messages changed) | L | ILL |

### 3.3 Strings, regex and dates

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| C1 | `translate(None, 'aeiou')` next to the Py3 form; `deletechars` parameter | 256 | DAT: Py2 signature | M | DNR; VOD signature of `str.translate` |
| C2 | "Bytestrings only support `isdigit`"; `isalnum` = `isalpha` + `isnumeric`; `isdecimal/isdigit/isnumeric` table corrupted | 263 | IMP/corrupted passage | L | VOD |
| C3 | `[::-1]` "faster" than `reversed` | 260 | NS | L | DNR |
| C4 | Caseless comparison via normalization + `casefold` | 265–266 | CONF: the recipe may be incomplete | M | VOD recipe in the `unicodedata`/`str.casefold` docs |
| C5 | "The default literal in Py3 is UTF-8 Unicode" | 268 | IMP: mixes encoding and type | M | VOD |
| C6 | Default encoding of text `open()` is "utf8" | 654 | ABS: the distiller says it depends on locale/platform | H | DNR; VOD; WARN (passing an explicit `encoding=` is the practice suggested by the distiller) |
| C7 | "`format` is the successor of `%`"; `ljust` "deprecated since 2.5"; `.format(**data)` versus `format_map` | 248–250 | CONF/DAT | M | VOD status in the `str` docs |
| C8 | Sentence that Py3 requires `__format__` for objects with a specification | 253–254 | CONF | L | VOD `object.__format__` docs |
| C9 | `\10` read as group 1 + "0"; global flag in the middle of the regex "undefined"; `re.escape` "escapes all specials" | 401, 404 | CONF/DAT (behavior changed by version) | M | VOD `re` docs |
| C10 | Docstring treated as a "multiline comment"; `"""` "can be used as comments" | 61–62 | IMP | M | VOD concept in the docs |
| C11 | `strptime` does not accept an offset with `:`; ISO 8601 without citing `fromisoformat/isoformat` | 69–70 | CONF/DAT (version dependent) | M | VOD `%z` and ISO by version |
| C12 | `utcfromtimestamp` called "ITC datetime" and without `tzinfo`; `utcnow()` + `replace(tzinfo=...)` | 68–69 | IMP/CONF | M | VOD recommended "aware" form |
| C13 | `dateutil` 2.5.3; "all DST cases handled correctly with pytz" | 66 | ABS/DAT | M | DNR; VOD |

### 3.4 Modules and stdlib

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| D1 | A directory needs `__init__.py` to be a package; "every package must contain" | 51, 276 | ABS/DAT. The distiller cites PEP 420 (3.3+). | M | DNR; VOD namespace packages |
| D2 | `import imp`; `__import__(r"C:/.../module.py")`; `from math import sqrt, ceil` "not recommended"; avoid relative imports | 270, 273–275 | DAT/CONF. P.275 contradicts the warning on p.273. | M | VOD `importlib` and PEP 8 |
| D3 | `math.log1p` = "log base e − 1"; `log(1000,10) == 3.0`; `log2`/`log10` with no version; `cmath.log(1000,10)` → `(3+0j)` | 85 | IMP/ABS (floating point) | M | VOD definition; ILL |
| D4 | `floor`/`//` "rounds away from zero" | 278 | IMP | M | VOD |
| D5 | `math.pow` faster than `**` (measured with `xrange`); `math.sqrt` faster than `pow(x,0.5)` "with the same precision" | 279, 374 | DAT/NS | M | DNR |
| D6 | "There is no `cmath.inf`" | 285 | DAT | L | VOD |
| D7 | Result type of `**` "that of the widest operand"; 3-argument `pow` requires exponent ≥ 0 | 373–374 | DAT/ABS | M | VOD |
| D8 | `nth_root` by binary search (`mid + 1`); cube root via `**(1.0/3)` equal to the integer; `OverflowError: long int...` | 375, 378 | No proof; floating point; Py2 message | M | DNR; test first |
| D9 | `itertools.combinations` "returns a generator"; `zip_longest` with default `fillvalue` `''`; `accumulate` marked 3.2 with `func=` | 306–307, 310 | CONF (defaults and versions) | M | VOD `itertools` docs |
| D10 | JSON: supported types without `None`; tuple becomes list; use `encoder.encode(data)` | 300, 534 | Omission/IMP | L | VOD |
| D11 | `StringIO`: "must `seek` before reading or writing" | 298 | IMP | L | VOD |
| D12 | `sqlite3.Error` "built-in function" | 301 | IMP (it is an exception) | L | VOD |
| D13 | `os.makedirs` with `try/except OSError`; `os.name` lists `posix/nt/ce/java` | 303–304 | DAT/CONF | L | VOD |
| D14 | `os.access` "a much better solution" | 414 | ABS | M | VOD race-condition caveats |
| D15 | `reduce` "removed from the builtins"; comment "No import needed" | 325, 365 | [int] contradiction between pages | L | VOD |
| D16 | `base64` with `altchars` replacing `+` and `=`; "more than 2 characters, extras ignored"; ASCII85 "released in 3.4" | 328, 331 | CONF | M | VOD `base64` docs |
| D17 | Generator "cannot return values"; "only traverses once, unlike other iterators"; re-iterating "yields `None`"; `StopIteration` inside a generator not discussed | 356–357, 363–364 | DAT/IMP/gap | M | VOD; DNR |
| D18 | `contextmanager` without `try/finally`: does what comes after `yield` run if the block raises? | 409–410 | CONF | M | VOD `contextlib` docs |
| D19 | `random.uniform` "inclusive" at both ends | 321 | CONF | L | VOD |
| D20 | `struct`: `h`/`b` as unsigned; native prefix and alignment | 530 | CONF | M | VOD `struct` docs |
| D21 | `subprocess`: "command must be a list (at least with `shell_mode=True`)"; `stdin.write(str)`; `poll()` loop may lose output | 433–434 | IMP/DAT | M | VOD `subprocess` docs |
| D22 | `argparse`: `default='World'` on a required positional | 430–431 | CONF | L | VOD |
| D23 | `logging.exception(e)` breaks; use the root logger everywhere | 595, 597 | DAT/IMP (no `getLogger(__name__)`) | M | VOD |
| D24 | `http.server` on localhost only "requires a custom program"; `tarfile.TarFile` (`.tar.gz` name); `ZipFile` without `compression` | 566, 585, 587 | CONF | M | VOD docs |
| D25 | WSGI: example with undefined `environ` and `str`; truncated chapter | 599 | Incomplete passage | M | DNR; consult PEP 3333 |
| D26 | if/else "by far the most efficient" for switch | 600 | NS | L | DNR |
| D27 | ElementTree XPath: "`last` is the only function" | 473 | CONF | L | VOD |
| D28 | `2to3` without a deprecation notice; `visit_FunctionDef` without `async def`; `locale.getpreferredencoding(False)` as default | 640, 645, 651 | DAT/CONF | L | VOD |
| D29 | `pickle.HIGHEST_PROTOCOL` without warning about reading on old versions | pickle chapter (page not indicated) | Omission | M | WARN |
| D30 | Chapter 172 "(and Hashable)" with no content on hashability | 698 | Incomplete passage | L | DNR |

### 3.5 Concurrency

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| K1 | `ThreadPoolExecutor` "best for CPU-bound"; "cores × 5"; `ProcessPoolExecutor` "new process per task" | 314 | [int] contradicts p.316–317. The distiller suspects an inversion. | H | DNR; VOD in the `concurrent.futures` docs |
| K2 | `uvloop` "99% compatible, unavailable on Windows" | 315 | DAT | L | DNR |
| K3 | Event example without importing `functools`; `asyncio.wait` with coroutines and implicit `loop` | 315–316 | DAT/partial ERR | M | VOD current `asyncio` API |
| K4 | `aiohttp` websocket: `ClientSession` outside a coroutine, `send_str` without `await`; `echo.websocket.org` service | 316 | DAT/CONF | M | VOD aiohttp docs |
| K5 | GIL timings (14.42 s with 4 threads); 1.8x gain on a dual processor; `math.factorial` example with `sleep(0.001)` | 544, 550, 796–797 | NS/ILL (CPython version; `sleep` without import) | M | ILL; DNR numbers |
| K6 | `Thread.join(blocking=False)` | 539 | CONF: the distiller says `join` accepts `timeout` | H | DNR; VOD signature |
| K7 | `multiprocessing` start methods by platform (fork/spawn/forkserver) | 547 | DAT | M | VOD default by platform |
| K8 | `Queue.empty()` in the "Iftry" pattern; performance gain | 548–549 | CONF/NS | M | VOD reliability |
| K9 | "Don't. Use processes, instead."; `with Pool` still requires closing and joining; "Pool opens as many processes as cores" | 591–592 | ABS/CONF | M | VOD what `Pool.__exit__` does |
| K10 | Cython "alternative interpreter"; `with nogil:` applied to `threading.Thread` | 592 | IMP | M | VOD |

### 3.6 Packaging and environments

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| P1 | Python installation: Ubuntu 16.04 packages, Homebrew via remote script; OS Python "great for learning, not for development" | 52–53 | DAT/NS (see also section 4) | M | DNR; WARN |
| P2 | `pip search`; "upgrading all outdated packages is not standard" | 54–55 | DAT/CONF | M | VOD current state |
| P3 | "On Windows you must put pip on the PATH" | 30 | ABS | L | VOD |
| P4 | Publishing to PyPI: `register`, `description-file`, URLs, ".md becomes plain text", `.pypirc` | 415–417 | DAT | H | DNR; VOD current guide |
| P5 | `pip.main`; compiling a C extension with `gcc hello.c -o hello` (without `-shared`, `-fPIC`, include); C++ uses a different command | 419, 392, 394 | DAT/incomplete | M | VOD supported API; DNR the recipe |
| P6 | "Force install" by renaming a wheel | 420 | NS | M | DNR |
| P7 | `pip install SomePackage>=1.0.4` without quotes | 421 | CONF | M | VOD documented form |
| P8 | "pip follows SemVer"; "pip removes the old version before upgrading"; dependency upgrade | 422, 425 | CONF | M | VOD version specification and `--upgrade` |
| P9 | `sphinx.build_main` | 437 | DAT/CONF | L | VOD |
| P10 | `pyvenv`; "virtualenvwrapper is the most recommended"; `sys.real_prefix` as a venv test | 706, 711, 715 | DAT/opinion NS | M | DNR; VOD `venv` |

### 3.7 Testing and performance

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| T1 | `assertRaises(...) as ex` with `ex.message` | 758 | DAT (Py2); the distiller cites `.exception` | M | DNR; VOD `unittest` docs |
| T2 | `yield_fixture` | 768 | DAT | M | VOD pytest docs |
| T3 | `py.test` command, `pytest-2.9.2`, `__init__.py` in `tests/` | 765 | DAT | M | VOD current command |
| T4 | "`cProfile` generally preferable to `timeit`" (p.770) versus "each serves a purpose" (p.776) | 770, 776 | IMP/[int] | L | VOD; DNR the preference |
| T5 | Dict: `in` + index "costs a lot" because it looks up twice | 784 | NS/ABS | L | DNR |
| T6 | Measurements (`bisect` `%timeit`; `next` + genexp "more efficient in general") | 382–383 | NS/environment | L | ILL |

### 3.8 Security and cryptography (items not listed in section 4)

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| S1 | PBKDF2 with 100000 iterations, "as high as possible" | 778 | DAT: the distiller says the recommendation changes over time | H | DNR the number; VOD |
| S2 | "bcrypt and scrypt are not part of the stdlib" | 778 | CONF | M | VOD `hashlib` docs for the version |
| S3 | "AES is state of the art" without discussing modes | 779–781 | ABS | H | See section 4 (SEG-5) |
| S4 | `ast.literal_eval('()' * 1000000)` causes a segfault; "CPython does not consider parser bugs to be security flaws" | 505 | IMP/ABS: input is not a valid literal; 2nd sentence NS | M | DNR; VOD |
| S5 | `eval('a * b', globals=variables)` by keyword; "eval/exec are not used safely" | 505–506 | CONF/ABS | M | VOD signature and what the docs say about restricting `globals` |
| S6 | `hashlib`: named constructors "much faster" than `new()` | 695 | NS | L | DNR |
| S7 | Forced deallocation with `_Py_Dealloc` | 525 | The text itself warns | H | DNR |

### 3.9 SQL and I/O

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| Q1 | `fetchmany` without `size` "returns one row" | 672 | CONF (`arraysize`) | L | VOD |
| Q2 | "Closing the connection does an implicit rollback" | 674 | CONF per driver | M | VOD semantics; WARN |
| Q3 | psycopg2 "most popular"; `cx_Oracle`; `URL(drivername=...)` in SQLAlchemy | 675–678 | NS/DAT | M | VOD current names and API |
| Q4 | `tell()` as a character count in text | 184 | CONF | L | VOD |
| Q5 | "File iterator together with `readline()` is bad practice" | 190 | NS | L | DNR; VOD `io` docs |
| Q6 | EAFP with `IOError`; `os.path.isfile` "causes a race condition" | 192 | DAT/IMP | L | VOD |
| Q7 | `copytree`: destination must not exist | 194 | CONF (a newer parameter exists) | L | VOD |
| Q8 | Modes `'a'`/`'rb'`/`r+`/`w+` loosely described | 188 | See E-35 | M | DNR |

### 3.10 Cross-cutting (CPython, Python 2, quotations)

| ID | Claim in the Notes | Page | Problem | Sev. | Action |
|---|---|---|---|---|---|
| X1 | `is` with small integers/strings; cache from −5 to 256; example with 999999999; "Python keeps a reference to common strings" | 107, 523, 792–793 | CPython detail; the compiler may merge constants | M | DNR as a guarantee; WARN; VOD |
| X2 | Primitives reference-counted and destroyed immediately; "waiting for the GC to close a file"; generation thresholds; manual collection "discouraged" | 524–527 | CPython-specific/IMP/NS | M | WARN; VOD `gc` and `object.__del__` docs |
| X3 | Quotations pasted without a reference (Guido's letter on `filter/map`; `dir()` docs) | 159, 240 | NS | L | DNR as a quotation |
| X4 | Number types and exact floating-point outputs | 85, 378 | IMP | L | ILL |
| X5 | Statements with Py2 names: `xrange`, `raw_input`, `print` without parentheses, `long`, `itervalues`, `unicode` | 288, 457–458, 375 | DAT | M | Treat the passage as Py2 until verified |
| X6 | Truncated/corrupted chapters or passages | 139–140, 263, 599, 698 | Extraction or incomplete text | L | DNR the passage |

---

## 4. Security: examples from the book the agent must NOT recommend

These points appear as code or text in the Notes. The agent does not present them as good practice. When the user brings one of them, warn about the risk and point to the official docs. The corrections the text suggests are only the distillers'; the rest requires the docs.

| ID | Example in the Notes | Page | Why not to recommend | What the agent does |
|---|---|---|---|---|
| SEG-1 | `pickle`/`shelve` used in the examples on 687 and 731 without a security warning (the pickle chapter carries the warning on p.535, and the Tutorial on p.66) | 687, 731 | Gap in those examples: loading pickle from an untrusted source can execute code (Tut p.66; Notes p.535). | Warn; VOD the warning in the `pickle` docs; never suggest loading untrusted data |
| SEG-2 | `eval(object_type)` in a factory on user input | 690 | Arbitrary-execution risk. The distiller suggests an explicit name→class mapping. | DNR; propose an explicit mapping |
| SEG-3 | `eval`/`exec`, `ast.literal_eval` and "how to restrict" | 505–506 | The text (Notes p.505) says it is not possible to use `eval`/`exec` with untrusted user code safely; details about `globals`/`__builtins__` unconfirmed. | DNR eval/exec with external input; VOD |
| SEG-4 | MD5/SHA1 listed as "secure" algorithms; `hashlib.md5` in the examples | 694 | Missing warning that they are unsuitable for security purposes. | DNR for passwords, signatures and defensive integrity; VOD algorithms in the docs |
| SEG-5 | Cipher with `pycrypto` + AES in CFB, IV derived from the password, without authentication | 779–781 | Historically abandoned library, no authenticated cipher, "AES is state of the art" without addressing modes. | DNR; WARN; VOD maintained libraries and authenticated modes |
| SEG-6 | `paramiko` with `AutoAddPolicy` | 782 | Accepts unknown host keys: weakens the server's identity (MITM risk). The example also does not import `paramiko`. | DNR; VOD host-key policy |
| SEG-7 | SQL built by string formatting: `'SELECT * FROM %s' % tabela` (MySQL) and name interpolation in the SELECT (sqlite3) | 674, 301 | Contradicts the SQL injection warning on p.670; sqlite does not show placeholders. | DNR; VOD parameterized queries in the driver docs |
| SEG-8 | File hash with the file opened by `open('myfile', 'r')` | 779 | Hashing operates on bytes; it should be `'rb'` in Py3 (pointed out by the distiller). | DNR; use bytes |
| SEG-9 | `tarfile.extractall` without a warning | 585 | Paths outside the destination in untrusted archives (distiller); the text says nothing. | WARN; VOD `tarfile` docs |
| SEG-10 | Parsing untrusted XML without warnings | XML chapter (~473) | Gap: the module's docs carry warnings (pointed out by the distiller). | WARN; VOD |
| SEG-11 | `dis` "safe with untrusted code" because it does not import the module | 327 | The example uses `marshal.load`, whose docs warn against untrusted data; `read(8)` assumes an old `.pyc` header. | DNR the claim |
| SEG-12 | `rpdb` opens a network socket | 503 | Listening interface and exposure not discussed. | WARN |
| SEG-13 | Installation: `--no-check-certificate`; Homebrew via a downloaded script piped straight into Ruby | 52–53 | Turns off certificate verification and runs a remote script blindly (distiller's suspicion: dated, no official source). | DNR; WARN |
| SEG-14 | Plain-text password in `.pypirc` | 415–417 | Insecure credential practice. | DNR; VOD current guide |
| SEG-15 | `pip install` of a package with `>=` without quotes | 421 | Shell redirection can surprise (see P7). | VOD documented form |
| SEG-16 | `assert` as input validation | 235–236, 784 | See B15: validation may vanish in optimized mode (suspicion). | DNR in production |
| SEG-17 | "Force install" by renaming a wheel | 420 | Workaround with no source that bypasses the compatibility check [inference] | DNR |

Note [inference]: SEG-4 and S1 form the same family (hash and key derivation). If the user asks about passwords, the answer must come only from the `hashlib` docs, never from these examples.

---

## 5. Clear errors in the book itself

These are errors the distillers marked as errors (undefined names, typos, contradictions between pages, examples that do not match their own output), not just suspicions. The agent does not copy these passages; if the concept matters, it looks it up in the official docs.

**Data and structures**
- E-1 Ch. 2 says "four types" of number including `long` (p.57) and lists `long` among the immutables (p.40); contradicts p.37, where `long` is unified.
- E-2 `tuple1 = ('world')` is not a tuple; `tuple + tuple1` and `print(tuple[0])` with output `(123)` are wrong; `list`/`tuple` used as variable names (p.58, p.181).
- E-3 `set` "without insertion order but sorted order" contradicts the outputs on p.57 and p.76 (p.43).
- E-4 `my_array.index(5)` → `5` and `index(3)` → `3` (p.124).
- E-5 `for key, value in d.values()` with output of values only (p.130).
- E-6 `dict.fromkeys((milk, eggs))` without quotes; `dict(iterables)` with a mismatched name (p.133).
- E-7 Section 8.4: `len` outputs missing; `issuperset` described with the `issubset` sentence (p.77–78).
- E-8 Operator `~`: sign-magnitude comment against the two's complement explained on p.86; 8 bits versus arbitrary-size integers (p.87).
- E-9 `if a = b:` (p.163); `any(x = 0 for x in foo)` (p.356); unbalanced parenthesis in `print('Check ...` (p.174).
- E-10 `alist.insert(3, [2009])` with output `2009`; `zip_longest` without import (p.145).
- E-11 `reversed(lst)[0:2]` presented as slicing (p.141).
- E-12 Linked list: `is` for values, `pop` with `position=None`, `print` after `raise`, undefined `w(...)`, `display` without `self` (p.169–170, ch. 25).
- E-13 `sorted(f, key=len)[1000:]` does not give the "top-1000" (p.389).
- E-14 Set copy with `{()}`, `{[]}`, `{3,[]}` (lists are not hashable) (p.406–407).
- E-15 `getKeysForValue` uses `keys` and references `key`: NameError (p.381).
- E-16 Sum 1..n with `n = 0` gives an empty loop (p.442); `list_tree_names(node, lst=[])` (p.441).

**Functions and classes**
- E-17 Example of "don't check the type": `extend((1,2,3))` followed by `", ".join(l)` fails with integers (p.787).
- E-18 `func(*args=[1,2,3])` described as SyntaxError and, in the next sentence, as TypeError (p.202–203); `args['value1']` instead of `kwargs` (p.202).
- E-19 `unpacking(1, 2, **arg_dict, c=3)` given as valid with `c` already in the dictionary (p.214–215); nonexistent `optionalvalue1` (p.215).
- E-20 `reduce` without import (p.217); `from functors import partial`; `def raise`; undefined `NumberNotInRangeException` (p.218).
- E-21 "No intermediate scopes" (p.99) contradicts the closure example on the same page.
- E-22 "Since 2.2 all classes inherit from `object`" (p.229) contradicts p.230–231. `Character` example: `__init__` without `self`, a property that returns itself (recursion), read-only `hp` assigned, nonexistent `max_hp`, deleter named `x` (p.235–236). `name.split(" ", 2)` can break the unpacking (p.232).
- E-23 Defaults "bound at execution, not at declaration" (p.237), the opposite of what p.207 says. Composition uses undefined `person(i)` and `join_country` returns `None` (p.238–239).
- E-24 `__format__` fails with an empty `format_spec` (`format_spec[-1]`) (p.253–254).
- E-25 `raise NotImplemented`; `NotImplemented` is not an exception; outputs "None" and "6.0" do not match; `Square` uses `* 2` while the counterexample uses `** 2` (p.491–492).
- E-26 Mixins: right→left (p.611) against left→right (p.617). Division in Py2: "floor" against "rounding-towards-zero deprecated" (p.621).
- E-27 `except Exception` presented as catching `SystemExit`/`KeyboardInterrupt` (p.449), against the tree on p.451.
- E-28 "AssertError" (p.457); `xrange` with `float` (p.457–458); `return a += ...` is a syntax error, not an argument-count one (p.459); the Py3 "unindent" block repeats the previous example (p.461); `i += dic[i]` does not change the iteration (p.453–454).
- E-29 `fib.cache_info()` with a function called `fibonacci` (p.324).
- E-30 `__exit__(self)` without the three parameters of the protocol described on the same page (p.409); `import module2.py` (p.412).

**Strings and dates**
- E-31 `lstrip` example repeats `rstrip` (p.259); `isinstance(x, byte)` (p.268); `import random.randint, time, sys` and module `sockets` (p.271).
- E-32 `\r` called "form-feed"; `is_allowed` admits a dot and returns the strings `'True'/'False'`; `groups()` "list of tuples" but the example shows a tuple (p.398, p.402).
- E-33 `datetime`: `total_seconds()` 518399.0 against `timedelta(4, 1)` (p.73); section 5.8 "Subtracting months" returns the following month (p.69); section 5.3 calls `timedelta` a module, mixes `datetime.datetime.now()` and a stray `self` (p.67); `dt.tzname` without parentheses showing `'JST'` (p.65–66); `default_zone` in the text against `default_timezone` in the code (p.69–70).
- E-34 `math.cosh` labeled "inverse hyperbolic cosine" (p.83); `cmath.isnan(0.0, float('nan'))` with two arguments (p.285).

**I/O**
- E-35 File modes: `'a'` "must exist" against the table; `'rb'` "default" (p.188); `f.write('\\n' + newdata)` writes a backslash and n (p.188); mode `'x'` opens with `"r"` and the Py2 variant opens `"fname"` with `"w"` (p.189).
- E-36 `readlines` uses undefined `line` (p.190); `mmap` in text mode 'r' with `mm[5] = 'a'` (p.193); `os.stat(...).st_size == 0` and `getsize > 0` presented as "or" (p.193).
- E-37 `islice(f, 12, 30)` described as "lines 13 to 20" (p.194); output `'a\b\c'` without escaping (p.195); `dirname + 'main.py'` without a separator (p.196).

**Modules and tools**
- E-38 Line-by-line JSON with `open(file_path).splitlines()` (p.299); `secrets` without importing `choice` (p.318); `randrange(10)` described as "[0,20]" (p.319).
- E-39 `urllib` imported and used as `urllib.parse`/`request` (p.464); manual reading of `sys.argv` with `reversed(...)` and `arg = arg.pop()` (p.428).
- E-40 `os.E_OK` nonexistent in its own table; flags combined with `&` (p.414); `pip.main(['install'] + i.key + ...)` adds a list to a string (p.419); noisy text "kjhfkjdf" (p.420).
- E-41 `functools` used without import (p.315–316); GIL example without importing `sleep` (p.796–797).
- E-42 MySQL: `db.callproc` called on the `Dbconnect` object, which does not define the method (p.674); psycopg2 shows ID 2 with inserts of id 1 (p.675); `SELECT ... %s` contradicts the warning on p.670 (see SEG-7).

---

## 6. Quick procedure before citing the Notes

1. Look up the topic and page in the tables above. If it is in section 5, do not use the passage.
2. If it is in section 4, do not recommend it; warn and consult the docs.
3. If it is a suspicion (section 3), do "VOD": confirm in the official docs of the target version. Only then assert, citing the official source.
4. If there is no confirmation, label it [community], say it was not verified and avoid exact numbers, versions and values.
5. If the page is not listed, that does not prove the content is reliable: the list covers only what the distillers marked.
