# Canonical Python glossary (Tut + Notes)

Citation abbreviations: (Tut p.N) = The Python Tutorial 3.14.0rc3; (Ref p.N) = The Python Language Reference 3.14.0rc3; (Notes p.N) = Python Notes for Professionals (community book, mixes Python 2 and 3); N = PDF page. The Standard Library (Lib) has only an index and is not cited here.
The official documentation (Tut, Ref) is a RELEASE CANDIDATE (3.14.0rc3): details may change until the final version. No entry in this glossary came from a Ref passage; all citations are Tut or Notes.
Marks: **[DATED]** (Python 2 or old practice), **[DIVERGES: official prevails]**, **[community]** (Notes only), **[inference]** (link made here), "version not stated" (official, with no version mark). Versions such as "3.3+" come from the Notes themselves.

## 1. Data model

- **Object** — any data with state and behavior; the ultimate base of every new-style class. (Tut p.134; version not stated)
- **New-style class** — old name for the class type that is now universal; in old versions only these had `__slots__`, descriptors, properties, `__getattribute__()`, classmethods and staticmethods. (Tut p.134; version not stated)
- **Type** — an object's type is in `__class__` or `type(obj)`. (Tut p.139; version not stated)
- **Attribute** — value associated with an object, accessed as `o.a`; a name that is not an identifier can be created with `setattr()` and read only with `getattr()`. Any name after a dot is an attribute, including in modules. (Tut p.80, 124–125; version not stated)
- **Special method (magic, dunder)** — method called implicitly by an operation, with a name between double underscores; "dunder" is the spoken form. (Tut p.128, 133, 138; Notes p.225)
- **Operator → method map** — `+` `__add__`, `-` `__sub__`, `*` `__mul__`, `//` `__floordiv__`, `%` `__mod__`, `**` `__pow__`, `[]` `__getitem__`, `in` `__contains__`, call `__call__`, comparisons `__lt__ __le__ __eq__ __ne__ __gt__ __ge__`; `@` → `__matmul__` (3.5+). Built-ins also delegate: `str`, `repr`, `len`, `hash`, `abs`, `int`, `format`. (Notes p.485–486) **[community]**
- **`__div__` and `__nonzero__`** — Python 2 equivalents of `/` and of `bool`; in Python 3 use `__truediv__` and `__bool__` [inference for the second name; the Notes only mention `__nonzero__`]. (Notes p.485–486) **[DATED]**
- **Reflected methods `__r…__` and in-place methods `__i…__`** — the reflected one is tried when the left operand does not know how to operate; the in-place one must return `self`. (Notes p.485–486) **[community]**
- **NotImplemented** — singleton that a special method returns to say it does not support those arguments; the interpreter tries the reflected operation and, if everything fails, raises `TypeError`. Not to be confused with `NotImplementedError`. (Notes p.38, 488–489) **[community]**
- **Built-in constants** — `True`, `False`, `None` (absence), `Ellipsis`/`...`, `NotImplemented`. The `...` is also the shell prompt and, by convention, a placeholder for an empty body, with no special meaning. (Notes p.38; Tut p.26, 123)
- **Descriptor** — object with `__get__`, `__set__` or `__delete__` placed as a class attribute; dotted access triggers those methods (basis of functions, methods, property, classmethod, staticmethod). A data descriptor beats the instance `__dict__`; a non-data descriptor loses to it; order for `foo.bar`: class data descriptor, `__dict__`, class attribute/descriptor, otherwise `AttributeError`. (Tut p.127; Notes p.241, 579)
- **`__slots__`** — declaration that reserves space for attributes and eliminates the instance dict, saving memory; the text warns that it is tricky and reserved for very many instances in critical applications. (Tut p.137; version not stated)
- **Namespace** — place where names live, a name→object mapping, today normally a dictionary (detail subject to change); avoids collisions (`builtins.open` vs `os.open()`); there is no relation between names in distinct namespaces. (Tut p.79–80, 134; version not stated)
- **Duck typing** — does not check the type, only uses the method/attribute; focuses on the interface and allows polymorphic substitution; avoids `type()`/`isinstance()`. In practice, it only fails at run time. (Tut p.128; Notes p.490)
- **Abstract base class (ABC)** — complements duck typing when `hasattr()` would be awkward; provides virtual subclasses recognized by `isinstance()`/`issubclass()` without inheritance; there are ABCs in `collections.abc`, `numbers`, `io`. In the Notes, it prevents instantiating subclasses that lack the `@abstractmethod`s. (Tut p.123; Notes p.615–616)
- **EAFP / LBYL** — EAFP assumes the key/attribute exists and catches the exception; LBYL tests first and, in multithreading, suffers a race between test and use; remedies: locks or EAFP. (Tut p.128, 132; version not stated)
- **Expression vs statement** — an expression evaluates to a value; `while` and assignment are statements. Assignment inside an expression only with the walrus `:=`, which avoids swapping `==` for `=`. (Tut p.48, 128, 138, 140; version not stated)

## 2. Objects, identity and mutability

- **Assignment as binding** — `=` binds a name to a reference; an object can have several names; the type lives in the object, so the name can be rebound to another type. There is no declaration without a value. Assignment never copies data. (Tut p.19; Notes p.31, 33–34)
- **Chained assignment** — `a = b = c = 1` points all names to the SAME object; rebinding one name does not affect the others, but mutating the shared object affects all. (Notes p.34) **[community]**
- **Immutable / mutable** — an immutable has a fixed value (numbers, str, tuple, bytes, frozenset, range); "changing" requires a new object. A mutable (list, dict, set, bytearray) changes while keeping its `id()`. `long` among the immutables is Python 2. (Tut p.131, 133; Notes p.40, 698–699) **[DATED]** only for `long`
- **`id()` / identity** — shows whether it is the same object; the Notes advise against reading `id` as an address. `is`/`is not` compare identity; `==` compares value. (Tut p.19, 48; Notes p.698)
- **Shallow vs deep copy** — `l[:]`, `copy()`, `dict.copy()`, `set.copy()`, `copy.copy()` create a new container with the same elements; `copy.deepcopy` clones the nested ones. (Tut p.19; Notes p.141, 406)
- **Hashable** — constant hash over the object's lifetime (`__hash__`) and comparable (`__eq__`); equal objects have the same hash; enables use as a dict key and set item. Built-in immutables usually are; list and dict are not; tuple and frozenset only if all elements are. Instances of user classes are hashable by default, with the hash derived from `id()`. (Tut p.130; Notes p.37–38, 181–182)
- **Reference count** — number of references; zero deallocates immediately. `sys.getrefcount()` queries it; in CPython it is neither stable nor well defined across versions. `del name` only removes one reference. (Tut p.137; Notes p.523–524)
- **Garbage collection / cyclic isolate** — reference counting plus a cyclic collector (`gc`), which targets the cyclic isolate (objects that only reference each other). In the Notes the collector is generational (0, 1, 2) and triggered by allocations minus deallocations, not by memory. (Tut p.127, 129; Notes p.524, 527)
- **Small integer cache (-5 to 256)** — reuse of the same object, making `is` return True; outside the range it usually returns False. Implementation detail not confirmed by the official source. (Notes p.523, 792–793) **[community]**
- **`bool`** — subclass of `int`, only `True` and `False`, worth 1 and 0 in arithmetic. (Notes p.36) **[community]**

## 3. Scope and names

- **Valid names** — start with a letter or `_`, then letters, digits and `_`; case-sensitive; keywords are not allowed (`keyword.kwlist`). (Notes p.32) **[community]**
- **Scope** — textual region in which a namespace is directly accessible. Read lookup: local, enclosing functions (nearest first), module global, built-ins; this name lookup order is in Tut p.30 and p.80 **[official]**. The acronym LEGB only appears in Notes p.458 **[community]**; the Tutorial and the Reference do not use it.
- **Local name rule** — inside a function, a name is local if it is the target of any binding (assignment, `for`, augmented, `del`) anywhere in the body, even in a branch that does not run. (Notes p.94–96, 100) **[community]**
- **`global` / `nonlocal`** — `global` redirects assignments to module level; `nonlocal` rebinds a variable of the nearest enclosing function. Without them, outer names are read-only and assigning creates a new local. (Tut p.30, 80; Notes p.95, 100)
- **Nested scope** — referencing variables of an enclosing definition; read-only by default. (Tut p.134; version not stated)
- **Optimized scope** — local names known at compile time; functions, generators, coroutines, comprehensions and generator expressions. (Tut p.134; version not stated)
- **Free variable / closure variable** — free: used without being local; closure: a free variable defined in an outer scope (`co_freevars` lists only these). (Tut p.126, 129; version not stated)
- **Class body scope** — the definition creates a namespace used as the local scope during the body. Functions, lambdas, comprehensions and generators inside it do not see the class names. (Tut p.82; Notes p.97–98)
- **`_`** — in interactive mode it holds the last result (treat as read-only; assigning creates a local that masks it). By convention, a throwaway name, but it is still assigned. (Tut p.14; Notes p.604)
- **`__name__`** — is `'__main__'` if the module is run directly, otherwise the module name; functions/classes have their own `__name__`, the one from the definition. Logging pattern: `logging.getLogger(__name__)`. (Tut p.49, 51; Notes p.412–413)

## 4. Functions and arguments

- **Function / method** — function: statements that return a value; method: function defined in a class, receives the instance as the first argument. `def` is an executable statement that binds the name to the function object; the body cannot be empty (use `pass`). Functions are first-class objects. (Tut p.30, 129, 133; Notes p.200–201, 211)
- **Argument passing** — "by value" where the value is an object reference (the text's note prefers "call by object reference"). Mutating a mutable parameter affects the caller; reassigning does not. (Tut p.30; Notes p.208)
- **Argument vs parameter** — an argument is the value passed (keyword: `name=` or `**dict`; positional: the rest or `*iterable`); a parameter is the name in the definition. Five kinds: positional-or-keyword, positional-only (before `/`), keyword-only (after `*`), var-positional (`*args`), var-keyword (`**kwargs`). (Tut p.123–124, 135)
- **Parameter order** — `pos1, pos2, /, pos_or_kw, *, kw1, kw2`; `*args` comes before `**kwargs`; whatever follows `*args` is keyword-only. Positional-only serves APIs: renaming does not break callers. (Tut p.33–36; Notes p.202–203)
- **Keyword argument rules** — keyword after positional; no duplicate value; the name must exist; order among keyword arguments is free and preserved in `**kwargs`. In `def foo(name, **kwds)` the key `name` never reaches `kwds`; with `/` it does. (Tut p.32–35)
- **Unpacking in calls** — `f(*seq)` spreads positionals, `f(**dict)` spreads keywords; `*args`/`**kwargs` in the definition collect a tuple and a dict. (Tut p.36; Notes p.605–607)
- **Default value** — evaluated only once, at definition, in the defining scope, stored in `__defaults__`; a mutable default accumulates state across calls. Idiom: default `None` and create inside (`if L is None`). (Tut p.31–32; Notes p.207, 789)
- **Return** — without `return` (or with a bare `return`) it returns `None`; several values form a tuple. Methods that only modify the list (`insert`, `remove`, `sort`) return `None`, a principle of mutable structures. (Tut p.30–31, 40; Notes p.201, 209)
- **Lambda** — anonymous single-expression function (`lambda [params]: expr`), syntactic sugar; can be a closure. (Tut p.36–37, 132)
- **Closure** — inner function that uses variables of the outer one; each call of the outer creates a new binding. (Notes p.209–210) **[community]**
- **Decorator** — `@dec` over `def f` is equivalent to `f = dec(f)`; it must return a callable (otherwise the name becomes `None`); can be a function or a class with `__call__`. A "decorator factory" receives arguments and returns the decorator, hence the parentheses are required. (Tut p.127; Notes p.219–222)
- **Key function** — callable that returns the sorting/grouping value; accepted by `min`, `max`, `sorted`, `list.sort`, `heapq`, `itertools.groupby`; can come from `operator.itemgetter`/`attrgetter`/`methodcaller`. (Tut p.132; Notes p.295–296, 387)
- **Docstring** — string literal as the first statement of a module, class or function; stored in `__doc__` and feeds `help()`; `#` is not stored. First line: short summary. `-OO` removes `__doc__`. (Tut p.37, 52, 127–128; Notes p.61–63)
- **Annotation** — label for a variable, class attribute or parameter/return, by convention a type hint; optional, does not affect the function, lives in `__annotations__`. Locals are not accessible at run time; the others via `annotationlib.get_annotations()`. (Tut p.37, 123; version not stated)
- **Annotate / evaluate function** — the annotate function retrieves annotations (`__annotate__`); evaluate functions evaluate lazy attributes, such as the value of aliases created with `type`. (Tut p.123, 128; version not stated)
- **Type hint / alias / generic** — a hint declares the expected type, is not enforced and serves static checkers and IDEs; alias: `Color = tuple[int, int, int]`; generic: parameterizable type (`list`, `dict`); read via `typing.get_type_hints()`. (Tut p.130, 138–139)
- **Hint syntax in the Notes** — `name: type`, `-> type`, `x: int = 3` (3.6+), `TypeVar`; do not annotate `self`; forward reference as a string `'A'`, since annotations are evaluated at definition. (Notes p.445–447) **[DIVERGES: official prevails]**: the official source describes lazy evaluation via `__annotate__`; [inference] the string is no longer the only way out.
- **`# type: int` comment** — old way of annotating variables. (Notes p.446) **[DATED]**
- **Recursion** — requires a base case; each call creates a new environment (`locals()`). A tail call is a recursive call as the last operation; Python does not optimize it (TCO). Limit ~a thousand frames (`sys.getrecursionlimit/setrecursionlimit`); overflow raises `RuntimeError`, and `RecursionError` (a subclass) since 3.5. (Notes p.438–443) **[community]**

## 5. Classes and protocols

- **Class / class object** — template of objects; the definition creates a local namespace for the body and, on exit, the class object (a wrapper around that namespace). The class object supports attribute references and instantiation. (Tut p.82, 125)
- **`__init__`, `self`** — `__init__` initializes; `self` is just a convention. The Notes recommend creating instance attributes in `__init__`. Python has no real privacy. (Tut p.85; Notes p.225)
- **Bound method** — `x.f` packs instance and function; `x.f()` is equivalent to `Class.f(x)`; the object is recreated on each access (`a.f is a.f` gives False). `classmethod` binds to the class (`cls`); `staticmethod` binds nothing. (Tut p.83; Notes p.227–228)
- **Class vs instance variable** — a class variable is shared; assigning through an instance creates an instance attribute that shadows the class one. (Tut p.84, 125; Notes p.237–238)
- **MRO** — search order over the bases; the Notes mention C3 linearization and `Class.mro()`. (Tut p.133; Notes p.233–234)
- **Metaclass** — class of a class (default `type`); `type(name, bases, dict)` creates a class; rarely needed. In the Notes, `type`'s `__new__`/`__init__` are overridden. (Tut p.133; Notes p.242–245)
- **`__init_subclass__`** — customizes subclasses without a metaclass (3.6, according to the Notes). (Notes p.618) **[community]**
- **Property** — computed attribute (`@property`, `@name.setter`); allows lazy evaluation; a subclass overrides it with `@Base.foo.setter`; decorator-free form `x = property(getX, setX)`. (Notes p.481–483) **[community]**
- **`__repr__` vs `__str__`** — `repr` tries to be read back by the interpreter (or fails with `SyntaxError`); `str` is readable; without `__str__`, it falls back to `repr`. Containers display elements with `repr`. Both must return a string; implement at least `__repr__`. (Tut p.59–60; Notes p.53, 497–500)
- **`__format__`** — the class defines its own formatting mini-language, distinct from `__str__`. (Notes p.253) **[community]**
- **Container protocol** — `__getitem__`, `__setitem__`, `__delitem__`, `__contains__`, `__len__`, `__iter__`; `__call__` makes instances callable. (Notes p.487–488) **[community]**
- **Context manager** — object with `__enter__`/`__exit__` used by `with`; `__exit__` runs even with an exception, and returning `True` suppresses it. Alternative: `@contextlib.contextmanager` (before the `yield` is entry; after, exit). Several managers in one `with` are equivalent to nested `with`s. Definition (object that implements the context management protocol, the `__enter__()`/`__exit__()` methods called by `with`): Tut p.126. Returning a true value in `__exit__` suppresses the exception: Ref p.68 and p.130 [official]; Notes p.409 [community] (not Tut p.126). `@contextlib.contextmanager` and nested `with`: Notes p.408–410 [community].

## 6. Iterables, generators and async

- **Iterable** — returns members one at a time: sequences, `dict`, files, classes with `__iter__()` or sequence-style `__getitem__()`. `iter()` gives a single-pass iterator; the `for` does it by itself. The old `__getitem__` protocol with `IndexError` still holds. (Tut p.131; Notes p.197)
- **Iterator** — data stream; `__next__()` returns items and, at the end, `StopIteration`; it must have `__iter__()` returning itself, hence every iterator is iterable (Tut p.89, 132). An exhausted iterator, reused in a second pass, returns the same exhausted iterator and looks like an empty container (Tut p.132; Ref p.178) **[official]**. "Iterator isn't reentrant!" is only a section title in Notes p.199 **[community]**; the Tutorial and the Reference do not use the term "reentrant". Notes p.197: an exhausted iterator "cannot be re-used" **[community]**.
- **Generator / generator function** — function with `yield` that returns a generator iterator (Tut p.129–130). Components the Tutorial lists (Tut p.89–90): use of `yield` to return data; `__iter__()` and `__next__()` created automatically; local variables and execution state saved between calls (each `yield` suspends and execution resumes where it stopped); `StopIteration` raised automatically on finishing. Creating the generator does not run the body; the generator can only be traversed once (recreate it or store it in a list): Notes p.356–357 **[community]**. (the recipe of recreating or storing in a list ends in Notes p.358).
- **Generator operations** — `next(it[, default])`; `send(x)` requires an initial `next()` to "prime" it; `yield from` delegates (3.3+). (Notes p.359–361) **[community]**
- **Generator expression** — `for`/`if` in parentheses, lazy iterator (`sum(i*i for i in range(10))`); not indexable. (Tut p.90, 130; Notes p.156–157)
- **Comprehension** — list/dict/set comprehensions produce a new collection; the list one evaluates everything and uses proportional memory. A trailing `if` filters; `x if c else y` before the `for` is a ternary. Nested yields a list of lists; with nested loops, a flat list. A tuple as an expression requires parentheses. (Tut p.41–43, 127, 132; Notes p.149–161)
- **`range`** — iterable that produces items on demand, not a list; exclusive end; accepts a negative step. `enumerate()` is usually better than `range(len(a))`. (Tut p.24–25)
- **`else` on a loop** — runs when the loop ends without `break` (does not run on `break`, `return` or exception). (Tut p.25–26)
- **Looping techniques** — `items()`, `enumerate()`, `zip()`, `reversed()`, `sorted()`; changing a collection during iteration is delicate: iterate over a copy. (Tut p.23–24, 46–47)
- **Coroutine / awaitable** — suspendable subroutine, defined with `async def` (accepts `await`, `async for`, `async with`); an awaitable is a coroutine or an object with `__await__()`. (Tut p.125–127; version not stated)
- **Async iterator / generator / context manager** — an async iterator has `__aiter__()`/`__anext__()` and ends with `StopAsyncIteration`; an async generator is an `async def` with `yield`; an async manager uses `__aenter__()`/`__aexit__()`. (Tut p.124; version not stated)
- **Context variable** — `ContextVar` holds a value that depends on the current context (`contextvars.Context`), isolating state between async tasks; each thread has a context. (Tut p.126–127; version not stated)

## 7. Exceptions

- **Syntax error vs exception** — syntax is detected when parsing; an exception arises when running valid code and is not always fatal. Traceback: the last line carries type and detail. (Tut p.67–68)
- **Hierarchy** — `BaseException` is the root; `Exception` is the base of the non-fatal ones; `SystemExit` (`sys.exit()`) and `KeyboardInterrupt` are normally not handled. `except Class` catches subclasses. Py3 tree: `OSError` with `FileNotFoundError`, `PermissionError`, `ConnectionError`. (Tut p.69; Notes p.448, 451)
- **try/except/else/finally** — `else` runs without an exception and stays outside the `except` protection; `finally` always runs. `except X as e` gives the object; arguments in `.args`. (Tut p.69–70; Notes p.452–455)
- **Re-raising and chaining** — a bare `raise` re-raises preserving the traceback; `raise New from e` sets the cause (`__cause__`, Python 3); implicit chaining in `__context__`; `from None` suppresses. (Tut p.71–72; Notes p.449, 455)
- **Custom exception** — inherits from `Exception` or from a more specific one. (Notes p.453, 456) **[community]**
- **ExceptionGroup / `except*`** — exception that wraps several; handled whole or selectively. **`add_note()`** adds notes displayed after the exception. (Tut p.74–76; version not stated)
- **`assert` / `__debug__`** — `assert c, msg` is equivalent to `if __debug__: if not c: raise AssertionError(msg)`; `-O` removes asserts and `__debug__` becomes `False`; assigning to `__debug__` is illegal. (Equivalence of `assert` and illegal assignment: Ref p.117; `-O` removes asserts: Tut p.52; Notes p.457)

## 8. Modules and packages

- **Module** — `.py` file with definitions and statements and a private namespace; used as the global one by its functions. The main one is `__main__`. (Tut p.49–50, 133; Notes p.276)
- **Import forms** — `import m` (access `m.name`), `from m import n` (does not define `m`), `import m as a`; `from m import *` imports names without a leading `_`, discouraged, and only at module level (otherwise `SyntaxError`). (Tut p.50–51; Notes p.270, 272; `SyntaxError` of `import *` outside module level: Notes p.273)
- **Single import** — the module runs on first import and stays in `sys.modules`; `importlib.reload()` re-executes. (Tut p.50–51; Notes p.274–275)
- **`if __name__ == "__main__":`** — makes the file a script and an importable module at the same time. (Tut p.51; Notes p.412)
- **`sys.path` and shadowing** — search first the built-ins, then `sys.path` (script directory, `PYTHONPATH`, installation default). A local file with the same name masks the stdlib. (Tut p.51–52)
- **Bytecode / `.pyc`** — source compiled into `__pycache__/module.version.pyc`, validated by date (or hash, in hash-based pyc); it only loads faster; `-O`/`-OO` and `compileall`. Not portable across VMs nor stable between releases; instructions in `dis`. (Tut p.52, 125, 130)
- **Package** — module with `__path__`. Regular: directory with `__init__.py`. Namespace package: only subpackages, no `__init__.py`; a **portion** contributes to it. (Tut p.54–55, 133–136)
- **Package requires `__init__.py`** — the Notes state that every package requires it (p.276). **[DIVERGES: official prevails]**: the official source admits namespace packages.
- **`__all__`** — lists what `from package import *` imports; without it, only names already present in the package namespace come in. (Tut p.55–56; Notes p.271)
- **Relative import** — `.` current package, `..` parent; based on the module's package name, so the main module uses absolute imports. (Tut p.56)
- **`dir()` / `builtins`** — `dir(m)` lists defined names; built-ins live in `builtins`. (Tut p.53–54)
- **Finder / loader / spec** — the finder finds the loader (`sys.meta_path`, `sys.path_hooks`); the loader loads (`exec_module()`); `ModuleSpec` gathers the data; the import path comes from `sys.path` or from the parent package's `__path__`. (Tut p.129–135; version not stated)
- **`__main__.py`** — enables `python -m package`. (Notes p.417–418) **[community]**
- **`setup.py`, `distutils`, `entry_points`** — describes the package; `sdist`, `install`, `develop`; commands via `scripts=[...]` or `console_scripts`. The batch's official source does not cover packaging. (Notes p.415, 435–436) **[community]**
- **Virtual environment / `pip`** — self-contained tree with one Python version and packages (`venv`); `pip` installs from PyPI by default. (Tut p.107–108, 140)
- **Standard library / extension module / CPython** — stdlib: packages and modules of the official interpreter, composition varies by platform (`sys.stdlib_module_names`); extension module: C/C++; CPython: canonical implementation. (Tut p.52, 122, 138)

## 9. Built-in types

- **int / float / floor division** — `/` always gives `float`; `//` rounds down (`(-11)//4` is -3); `%` remainder; `**` has precedence over unary `-` (`-3**2` is -9). `int` has arbitrary size. (Tut p.13–14, 129; Notes p.37)
- **float and representation error** — binary fractions (IEEE 754 binary64, 53 bits); 0.1 becomes `3602879701896397 / 2**55`. Inspect: `as_integer_ratio()`, `Fraction`, `Decimal`. The version in which the display changed from 17 digits is not stated. (Tut p.115–119)
- **NaN and infinity** — `float('inf')`, `float('nan')`; NaN is not equal to itself; use `math.isnan`. Float division by zero raises `ZeroDivisionError`; overflow becomes `inf`. (Notes p.279–281) **[community]**
- **round** — Py3: one argument returns an integer, ties go to even; Py2 returned a float and rounded away from zero. `floor` goes to the smaller integer, `trunc` discards the fraction. (Notes p.277) **[DATED]** for the Py2 behavior
- **Complex** — suffix `j`; `cmath` provides the functions (`math.sqrt(-1)` raises `ValueError`, `cmath.sqrt(-1)` gives `1j`); ordering comparison with `complex` raises `TypeError`. (Tut p.126; Notes p.37, 284)
- **Truth value** — zero and empty sequences are false; the rest, true. `and`/`or` short-circuit and return the last evaluated operand; `not` > `and` > `or`. Comparisons chain (`a < b == c`). (Tut p.20–21, 48)
- **Sequence comparison** — lexicographic; a prefix is smaller; strings by code point; incomparable types give `TypeError`. (Tut p.48; Notes p.146)
- **Sequence** — iterable with efficient integer indexing via `__getitem__()`/`__len__()`: `list`, `str`, `tuple`, `bytes`. `dict` is a mapping. Negative indices count from the end; `IndexError` when out of range. (Tut p.137; Notes p.141)
- **Slice** — `s[i:j:k]`; start included, end excluded, new list/string; out-of-range bounds are tolerated. Underneath, a `slice` object passed to `__getitem__`. Slice assignment can change the size. (Tut p.17–20, 137; Notes p.141–142)
- **List** — more an array than a linked list (O(1) access); mutable; methods `append`, `extend`, `insert`, `remove`, `pop`, `sort` etc. `len()` is an O(1) built-in function. Stack with `append`/`pop`; queue with `collections.deque`. (Tut p.39–41, 132; Notes p.145)
- **Tuple, packing and unpacking** — immutable (may contain mutables); the comma creates it (`t = 1,`); `a = 1, 2, 3` packs; `x, y, z = t` unpacks; multiple assignment evaluates the right-hand side first. `first, *rest` collects a list (one asterisk per assignment). (Tut p.20, 44; Notes p.179–180, 604)
- **Named tuple** — inherits from tuple with named fields: `collections.namedtuple()`, `typing.NamedTuple` or your own class; fields accept a list or a string. (Tut p.134; Notes p.291)
- **Set / frozenset** — unordered and without duplicates; operations `| & - ^`; the empty one is `set()`, not `{}`; frozenset is immutable and hashable. (Tut p.44–45; Notes p.76)
- **Dictionary** — hashable keys (`__hash__`/`__eq__`); `list(d)` gives the keys in insertion order; `in` tests keys; iterating gives only keys, so `min(d)` is the smallest key. (Tut p.45–46, 127; Notes p.379, 386)
- **Counter** — `dict` subclass for frequencies; a missing key gives 0; a mapping as argument only copies the pairs; `most_common(n)`; a count can be negative. (Notes p.288–290, 390) **[community]**
- **defaultdict / OrderedDict / deque / ChainMap** — defaultdict calls the factory with no arguments and already inserts the key; OrderedDict preserves insertion (so does the plain dict, per the official source [inference: only an API difference remains]); deque has O(1) ends, `maxlen`, `rotate`; ChainMap (3.3+) is a view over mappings, writing only to the first. (Notes p.289–293) **[community]**
- **Sorting, min and max** — `sorted` returns a new list and accepts any iterable; `key=` or `itemgetter` picks the criterion; `min/max` of an empty iterable raise `ValueError`, avoidable with `default=`. On a tie, `max` returns the first, `sorted(...)[-1]` the last of the tied. `heapq.nlargest/nsmallest` avoid sorting everything. (Notes p.384–390)

## 10. Strings, bytes and Unicode

- **str** — sequence of Unicode code points (U+0000 to U+10FFFF), immutable; no character type (a character is a str of length 1); literals with single or double quotes; adjacent literals concatenate. (Tut p.15–18, 138)
- **Raw string** — prefix `r`, `\` not interpreted; cannot end in an odd number of `\`. (Tut p.15; Notes p.39)
- **Triple-quoted string** — `"""`/`'''`: unescaped quotes and multiple lines. (Tut p.15–16, 139)
- **f-string, `str.format`, `Template`** — f-string evaluates expressions in `{}` with a specifier after `:`; `!r`, `!s`, `!a` convert; `f'{x=}'` shows the expression text and `repr` (debugging). `format` uses positional/named fields. `string.Template` uses `$x`. (Tut p.59–61; Notes p.247–249)
- **t-string** — prefix `t`/`T` (template string literal); the glossary only defines the prefix. (Tut p.138; version not stated)
- **Encode / decode** — `str.encode(enc)` gives `bytes`; `bytes.decode(enc)` gives `str` (you must know the encoding). Errors: `strict` (default), `replace`, `ignore`, `backslashreplace`, and in encoding `namereplace`, `xmlcharrefreplace`. (Tut p.138; Notes p.268, 653–655)
- **Python 2 str** — the default literal was bytes and Unicode used `u''`; `string.maketrans` instead of `str.maketrans`. (Notes p.114, 256, 267–268; `string.maketrans` and `str.maketrans`: p.256) **[DATED]**
- **Bytes-like object** — supports the buffer protocol: `bytes`, `bytearray`, `array.array`, `memoryview`; some operations require a mutable one. **Contiguous**: C-contiguous or Fortran. (Tut p.125–126; version not stated)
- **Text file / binary file** — text reads and writes `str` with an encoding; binary uses bytes-like objects. **File object**: `read()`/`write()` API over a resource, via `open()`. (Tut p.125, 128, 138)
- **Source code encoding** — UTF-8 by default; another via `# -*- coding: cp1252 -*-` on the first (or second, with a shebang) line. (Tut p.12)
- **str methods** — `casefold` (3.3+) compares ignoring case, more aggressive than `lower`; `strip(chars)` removes a set of characters, not a prefix; `split` without `sep` ignores whitespace and `maxsplit` counts splits; `isdecimal ⊂ isdigit ⊂ isnumeric`; `index` raises `ValueError`, `find` gives -1; `is*` predicates give `False` for an empty string. (Notes p.255–267, 380) **[community]**

## 11. Concurrency and the GIL

- **GIL** — only one thread executes bytecode at a time; makes the object model (including `dict`) implicitly safe, at the cost of parallelism; released during I/O and by extensions doing heavy work. Threads help with blocking I/O, not with pure computation. A long C call can hold up the main thread. (Tut p.130; Notes p.543–544, 796)
- **Free threading / `--disable-gil`** — from 3.13, a build without the GIL (`-X gil=0` or `PYTHON_GIL=0`); several threads execute bytecode at the same time (PEP 703). **[DIVERGES: official prevails]** over the Notes' universal claim that only one instruction runs at a time. (Tut p.129–130)
- **Thread state / attached** — runtime state per OS thread; the C API requires an attached state; in most builds this implies holding the GIL, in free-threaded builds it does not. (Tut p.124, 138–139; version not stated)
- **Threads vs processes** — threads share data (require a lock); each `multiprocessing` process has its own VM, no shared GIL, and uses `Value`, `Queue`, `Lock`. Start: `spawn` (Windows), `fork` (Unix; the only one until 3.3) and, since 3.4, `forkserver` via `set_start_method`. (Notes p.543–547) **[community]** [version dates only in the Notes]

## 12. Tools and library

- **Interpreter and REPL** — `python -c`, `-m`, `-i`; `sys.argv[0]` is `''`, `'-'`, `'-c'` or the module. Since 3.13 there is a new shell (color, multiline; disable with `PYTHON_BASIC_REPL`). REPL = read–eval–print loop. (Tut p.11–12, 121, 137)
- **PEP 8 / PEP** — 4 spaces, lines up to 79, `UpperCamelCase` for classes, `snake_case` for functions. PEP: design document and record of decisions. (Tut p.38, 135–136)
- **Files and `with`** — `open(name, mode, encoding=)`: `'r'`, `'w'` (erases), `'a'`, `'r+'`, `'b'` binary; text converts line endings; `with` closes even on exception; `seek` in text only accepts offsets from `tell()` or zero. (Tut p.63–65)
- **print (Py3)** — function; `sep`, `end`, `file`, `flush`; concatenating with `+` requires `str`. (Tut p.21; Notes p.395–397)
- **Serialization** — `json` converts object↔text. `pickle` serializes arbitrary objects and is unsafe with untrusted data; `__getstate__`/`__setstate__` control the state. `struct.pack/unpack` converts values and bytes. (Tut p.65–66; Notes p.528–531, 534)
- **Regular expressions (`re`)** — `match` anchors at the start, `search` anywhere, `findall`, `finditer`; patterns in `r"…"`; flags `I`, `S`, `M`; `sub`; named groups `(?P<name>…)`; `re.escape`. (Notes p.398–405) **[community]**
- **Debugging** — `pdb` (`python -m pdb`, `set_trace()`; `b c s n r l p q`; `!c` for a variable of the same name), `ipdb`, `rpdb`. (Notes p.501–503) **[community]**
