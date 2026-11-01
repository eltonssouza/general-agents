# Python procedures and checklists

Reference base for the Python specialist agent. Sources: Tutorial 3.14.0rc3 (Tut), Language Reference 3.14.0rc3 (Ref), both **[official]**, and "Python Notes for Professionals" (Notes), **[community]**, which mixes Python 2 and 3. Pages in parentheses, for example (Tut p.29), (Ref p.32), (Notes p.95).

## Contents

1. Conventions and usage notes
2. Environment and execution
3. Functions and arguments
4. Scope
5. Comparisons and conditions
6. Loops and comprehensions
7. Dictionaries and lists
8. Strings
9. Exceptions
10. Classes and special (dunder) methods
11. Modules and packages
12. File I/O and serialization
13. Dates and time zones
14. Virtual environments and pip
15. Testing
16. Concurrency
17. Debugging, logging, memory and performance
18. Practical security (randomness and passwords)
19. Migrating Python 2 to 3
20. Review checklist ("if X, check Y" heuristics)
21. Gaps and pending checks

---

## 1. Conventions and usage notes

- Each procedure carries: when to use, steps, how to verify, pitfalls, source and origin.
- **[official]** = Tutorial or Language Reference 3.14. **[community]** = Notes. Ideas present in both families were merged.
- **[DATED]** = Python 2 step or old tool; recognize it in legacy code, do not adopt it as current practice.
- **[inference]** = link made by this document. **[VERIFICAR]** = doubtful claim from the source.
- The Notes are community-sourced: where they diverge from the official sources, the official one prevails.

---

## 2. Environment and execution

### 2.1 Find out which Python is running
**When to use:** `python` command behaving unexpectedly, "not recognized" error, doubt between 2 and 3. **Origin:** [community]
1. `python --version` and `python3 --version`; if `python` shows 2.x and 3 exists, use `python3` (Notes p.28).
2. Windows: launcher `py -3` or `py -2`; `py -3 -m pip` uses the pip of the same interpreter (Notes p.45, p.52).
3. Debian/Ubuntu/macOS: `which python` shows the chosen executable (Notes p.45).
4. On Windows, "'python' is not recognized" points to a PATH without the Python directory and `Scripts` (Notes p.45).

**Verify:** the printed version and path match what is expected. **Source:** Notes p.28, 45, 52.

### 2.2 Run code
Script `python hello.py`; REPL `python`; file and then REPL `python -i hello.py`; snippet `python -c '...'`. Exit: `exit()`, `quit()` or Ctrl+D; Ctrl+C cancels the line (Notes p.29–30). In the new REPL, `exit`/`quit` work without parentheses; F1 help, F2 history, F3 paste; `PYTHON_BASIC_REPL` disables the new shell (Tut p.121). **Origin:** [official]/[community].

### 2.3 Make a script executable
**Origin:** [official] (Tut p.121)
1. Unix/BSD: first line `#!/usr/bin/env python3`; `#!` must be the first two characters.
2. Unix line ending (`\n`) on that line; `\r\n` fails on some platforms.
3. `chmod +x myscript.py`.
4. Windows has no executable mode: the `.py` extension is associated with `python.exe` for double-click; `.pyw` suppresses the console window.

**Pitfall:** with `#!/usr/bin/env python` the active venv is respected (Notes p.707) [community].

### 2.4 Make a module executable as a script
**Origin:** [official] (Tut p.51)
1. End of the file: `if __name__ == "__main__":`.
2. Inside, `import sys` and read `sys.argv` (the example converts with `int(sys.argv[1])`).
3. **Verify:** importing the module does not run the block; running it as a script does.

### 2.5 Startup file and customization
**Origin:** [official] (Tut p.122)
1. `PYTHONSTARTUP` points to a file read only in an interactive session, in the same namespace as the session (it allows changing `sys.ps1`/`sys.ps2`). Outside interactive mode, only with an explicit `exec` of the contents.
2. Per user: `site.getusersitepackages()` shows the directory where to create `usercustomize.py`; it applies to every invocation, except with `-s`. `sitecustomize` is analogous, global, imported earlier.

### 2.6 Run with the GIL disabled
Build with `--disable-gil` (since 3.13) and run with `-X gil=0` or `PYTHON_GIL=0` (Tut p.130). **Origin:** [official].

### 2.7 Find out what exists
`dir(obj)` or `dir(modulo)` lists attributes; `help(obj)` shows docstrings; `help()` opens the interactive utility; for a module, only after `import` (Notes p.46–50, 56). `globals()` and `locals()` return the scope dictionaries (Notes p.98). **Origin:** [community].

### 2.8 Inspect the real value of a float
`x.as_integer_ratio()` (exact ratio), `Decimal.from_float(x)` (all digits), `format(x, '.17f')` (17 places) (Tut p.119). **Origin:** [official].

---

## 3. Functions and arguments

### 3.1 Write a function
**When to use:** any new `def`. **Origin:** [official] + [community]
1. Docstring as the first statement (Tut p.29–38; Notes p.62).
2. Decide on `/` (positional-only) and `*` (keyword-only) using the Tutorial's recap guidelines (Tut p.35–36) and to stabilize the API (Ref p.181).
3. Parameter order in the Notes: required, optional with default, `*args`, keyword-only, `**kwargs` (Notes p.202–203, 521).
4. Mutable default: use `None` and create the object inside (Tut p.30–32; Notes p.207–208).
5. Decide between printing (returns `None`) and returning the result. Annotations have no effect at run time (Tut p.37); follow PEP 8 (Tut p.38).

**Verify:** `f.__defaults__` shows the stored default, computed once at definition (Ref p.36, 44). **Pitfall:** `a = b = []` also shares the object (Ref p.32).

### 3.2 Document a function
Docstring in the first statement; single imperative line with a period, or summary + details + parameters/return; a single format (Sphinx/reST or Google); check with `help(func)` and `func.__doc__` (Notes p.61–64). **Origin:** [community].

### 3.3 Call and receive variable arguments
**Origin:** [community] (Notes p.202, 214–215, 521, 606–607) + [official] (Ref p.103–104)
1. Reference signature: `def f(a, *args, so_nome, opcional=1, **kwargs)`.
2. Call with `*seq` and `**d` for data already assembled.
3. Keys of `**d` must match the parameters: a missing required one gives `missing`; an extra one gives `unexpected keyword argument`; a repeated one gives `multiple values for argument` (the Reference explains: `*` is processed before keywords).

### 3.4 Write a decorator
**Origin:** [community] (Notes p.219–223) + [official] (Ref p.139–140, 173)
1. Wrapper `(*args, **kwargs)`: calls the original function and returns the result; apply `@wraps(func)`.
2. Decorator with arguments: create the factory and always use it with parentheses (`@d(...)`); the decorator returns something callable.

**Verify:** `@d` over `def f` is equivalent to `f = d(f)`; several decorators apply from bottom to top and the factory runs at the `def`.

### 3.5 Sort objects by attribute
`key=attrgetter('campo')` for objects, `itemgetter('campo')` for dicts; `reverse=True` for descending; `sort` is in-place and returns `None` (Notes p.138–139). **Origin:** [community].

---

## 4. Scope

### 4.1 Diagnose `UnboundLocalError` and scope-related `NameError`
**Origin:** [community] (Notes p.94–99) + [official] (Ref p.76; Tut p.80–81)
1. Read the whole function. Is there a `global x`? Then it is global. `nonlocal x`? Then it belongs to the enclosing function. Is there any binding of `x` (`x = ...`, `for x in`, `x += 1`, `del x`, `import`, `with ... as`, `:=`)? Then `x` is local throughout the function. Otherwise it resolves in the enclosing, global or builtin scope.
2. A name read before being assigned in the same function is `UnboundLocalError`: add `global`/`nonlocal` or rename the local.
3. Closure counter: `nonlocal` in the inner function.

**Verify:** `locals()`/`globals()` help see who owns the name. **Pitfall:** in a class body, methods do not see a class variable by its simple name (NameError), and a comprehension in the class body fails when using a class variable outside the first iterable (Ref p.60, 76).

### 4.2 Choose between `global`, `nonlocal` and local assignment
Simple assignment creates or changes the local; `nonlocal nome` rebinds a variable of the enclosing function; `global nome` rebinds the module's; the Tutorial's `scope_test` example shows the three effects (Tut p.80–81). **Origin:** [official]. A declaration after the name is used is an error (Ref p.122–123).

---

## 5. Comparisons and conditions

### 5.1 Choose `==` or `is`
**Origin:** [official] (Ref p.32, 108, 110)
1. Compare values (numbers, strings, literals) with `==`; identity of immutables depends on the implementation.
2. Reserve `is` for `None`, `True`, `False`, `NotImplemented` and real identity.

### 5.2 Make a class comparable, hashable and sortable
**Origin:** [official] (Ref p.52–53, 66, 109) + [community] (Notes p.384–385)
1. Define `__eq__` and an ordering operator (`__lt__` is enough, since `sorted` uses it).
2. Apply `@functools.total_ordering` to derive the others; full ordering is not implicit (Ref p.52).
3. If it defines `__eq__`, define a consistent `__hash__`. The Reference only requires that equal objects have the same hash and advises combining the components that take part in the comparison, packed in a tuple (Ref p.52). A class that overrides `__eq__` without defining `__hash__` ends up with `__hash__` equal to `None` and its instances stop being hashable; a mutable object with `__eq__` should not implement `__hash__` (Ref p.53). Inheriting the parent's hash requires the explicit assignment `__hash__ = Pai.__hash__` (Ref p.53); with a by-value `__eq__`, that inheritance breaks the contract that equal objects have the same hash [inference about breaking; contract in Ref p.52]. The explicit `__hash__ = None` is only necessary when the class does NOT override `__eq__` and wants to suppress the hash (Ref p.53).
4. For an unknown type, return `NotImplemented`: the Reference says comparison and numeric methods should return this value if they do not implement the operation for the given operands, and that the interpreter then tries the reflected operation or another fallback (Ref p.32, 66).

**Verify:** `a == b` and `b == a` coincide; equal hash for equal objects; no `bool()` on `NotImplemented` (error in 3.14).

### 5.3 Read a `match` pattern
**Origin:** [official] (Tut p.28–29; Ref p.132–138)
1. Read the pattern as the left side of an assignment.
2. Bare names are bound (they capture); dotted names, class names or attribute names do not bind.
3. `_` is the wildcard; `str`, `bytes` and iterators do not match sequence patterns.
4. Guards run after the capture.
5. Constants: use dotted names (e.g. `Enum` members) or literals.
6. `case Classe(x, y)` with positionals requires `__match_args__`; otherwise, use keywords.

**Pitfall:** a capture or `_` before other cases makes the following ones unreachable; a simple name always matches.

---

## 6. Loops and comprehensions

### 6.1 Write a comprehension
**Origin:** [community] (Notes p.149–156)
1. Identify the transformation (expression), the source (iterable) and the filter (final `if`).
2. Choice between two values: `x if c else y` comes before the `for`, not after.
3. Nested loops: write the `for` clauses out in full and copy the same order.
4. Expression that calls an expensive function: compute once (inner generator, `map`, `lru_cache`).
5. More than two layers or too long: break lines or refactor into a `for` or generator.

### 6.2 Remove items during iteration
**Origin:** [official] (Tut p.23–24, 47)
- Option A: iterate over `collection.copy()` (or `.copy().items()` for a dict) and remove from the original.
- Option B: build a new collection with only what should stay.

### 6.3 Traverse iterators safely
**Origin:** [official] (Ref p.126, 178, 182) + [community] (Notes p.358–359)
1. An iterator traversed twice comes back empty the second time: materialize with `list()`.
2. Infinite generator: never in `list()`/`sum()`; use `itertools.islice(gen, n)` or `next()`; in a `for`, a conditional `break`.
3. The loop's `else` runs when there was NO `break`. `for i in range(len(x))` is non-idiomatic: use `for item in x`.

### 6.4 Use `send()` on a generator
**Origin:** [community] (Notes p.359) + [official] (Ref p.99)
1. Create the generator. 2. Advance to the first `yield` with `next(gen)`. 3. Send with `gen.send(valor)`. 4. `next(gen)` is equivalent to `send(None)`; the first send must be `None`.

**Pitfall:** `return valor` in a generator goes to `StopIteration.value` (Ref p.118). Async generator consumed with `break` or cancellation: call `aclose()` (Ref p.100).

---

## 7. Dictionaries and lists

### 7.1 Find a key by value
All keys: `[k for k in d if d[k] == v]`. Just one: `next(k for k in d if d[k] == v)`, which raises `StopIteration` if there is none (Notes p.381–382). **Origin:** [community].

### 7.2 Cartesian product of a dict's options
`itertools.product(*valores)` with `dict(zip(chaves, combinacao))` in a list comprehension (Notes p.135). **Origin:** [community].

### 7.3 Dict and set: order and hashability
**Origin:** [official] (Ref p.35, 53, 176)
1. Dict preserves insertion order since 3.7: reinserting moves to the end; updating keeps the position. A set never guarantees order.
2. A dict key or set member must be hashable: tuples only if all their elements are; `list` and `dict` never.
3. A one-element tuple requires a comma (`(x,)`); `(x)` is not a tuple (Ref p.34, 111).
4. `*resto` in unpacking is always a `list` (Ref p.114).

---

## 8. Strings

### 8.1 Compare text ignoring case
**Origin:** [community] (Notes p.265–266)
1. Normalize: `unicodedata.normalize("NFKD", texto.casefold())`.
2. Compare the normalized forms of both sides.
3. Do not limit yourself to `lower`: `"ß".upper().lower()` differs from `"ß".lower()`, and a precomposed "ê" differs from "e" + combining accent.

### 8.2 Split and clean
`split()` without an argument suits text with irregular spaces; `split(',')` uses an exact delimiter (watch out for empty fields). Limiting from the end (extension): `rsplit(sep, maxsplit=1)`. `replace(old, new[, count])` for simple substitutions; `re.sub` for complex cases (Notes p.260–261). **Origin:** [community].

### 8.3 Write string literals and f-strings
**Origin:** [official] (Ref p.18–26, 27)
1. Backslashes in regexes or Windows paths: use a raw string. Unknown escapes give `SyntaxWarning` (future `SyntaxError`); `\t`, `\n`, `\b` silently change the content. A raw string ending in `\` is invalid.
2. f-string: nested identical quotes, `\` or a comment inside `{}` require 3.12+; `=` requires 3.8+; `lambda` and `:=` need parentheses; an f-string is not a docstring. With `=` and no format spec the default is `repr()`; with a spec, `str()`.
3. `t"..."` requires 3.14 and produces a `Template`, not a `str`.
4. An integer with a leading zero is an error; octal is `0o7`.
5. Non-ASCII identifiers go through NFKC and can merge distinct names.

---

## 9. Exceptions

### 9.1 Structure `try`
**Origin:** [official] (Tut p.68–73; Ref p.127–130)
1. `try`: only the code that can raise what you want to handle.
2. Specific `except` clauses; order matters: the search walks the clauses in sequence and the first that matches wins, and a clause matches the named class and its derived classes, not the other way round (Tut p.68–69; Ref p.127). So, derived classes before bases (in the Tutorial's example, with `except B` first it would print B, B, B). Consequence: a clause written after `except Exception` is unreachable for any exception that is `Exception` or derived [inference from Tut p.69 and Ref p.127]. An `except` without an expression, if present, must be last (Ref p.127).
3. A final `except Exception as err` only to log and then `raise`.
4. `else`: what depends on the success of the `try` (after all the `except` clauses); errors there are not handled by the sibling `except` clauses.
5. `finally`: unconditional cleanup.

**Pitfalls:** the target of `as` in `except ... as e` is deleted at the end of the `except` block, as if the body were inside a `try/finally` with `del e`; to use the exception after the block, assign it to another name (Ref p.127–128); `return/break/continue` in `finally` discards the exception (`SyntaxWarning` in 3.14); `except A, B:` without parentheses only in 3.14+ and without `as`; `assert` vanishes with `-O`, so validate input with `raise` (Ref p.117, 127–129).

### 9.2 Convert or chain an exception
Inside the `except`: `raise Nova("msg") from exc`; to hide the original, `from None`; a bare `raise` re-raises (Tut p.71–72; Ref p.118–119). The name bound by `as` (`exc`) is only valid inside the `except` block: it is deleted at its end (Ref p.127–128). **Origin:** [official].

### 9.3 Aggregate errors with `ExceptionGroup`
**Origin:** [official] (Tut p.74–76; Ref p.128–129)
1. Collect the caught instances in a list (loop with `try/except Exception as e`).
2. Optional: `e.add_note(...)` per item.
3. If the list is not empty: `raise ExceptionGroup("title", excs)`.
4. Handle selectively with `except*`: what does not match propagates and is re-raised. Each exception in the group is handled by at most one `except*` clause, the first that matches it, so the order of the clauses also counts (Ref p.128).

**Pitfalls:** in `except*`, `e` is a group; `break`, `continue` or `return` are not used.

---

## 10. Classes and special (dunder) methods

### 10.1 Create a correct class
**Origin:** [official] (Tut p.82–90) + [community] (Notes p.225–237)
1. Per-instance data in `__init__` via `self.attr = ...`; constants and shared data in the class body.
2. Mutables (lists, dicts) initialized inside `__init__`, never as a class variable, unless sharing is intended.
3. Every method has `self` as its first parameter; it calls others via `self.metodo()`.
4. `__str__` for the readable form; `__repr__` unambiguous; both (and `__format__`) must return `str` (Ref p.51–52).
5. Alternative constructors with `@classmethod`; `property` for validated or derived fields.
6. Simple record: `@dataclass` with annotations (Tut p.88).
7. Make it iterable: `__iter__` returning an object with `__next__`, or, more simply, a generator (Tut p.89–90).

**Pitfalls:** `obj.attr = obj.attr + 1` on a class attribute creates an instance attribute (Ref p.114); `obj.f = func` on an instance does not receive `self` (Ref p.37); `__slots__` only with justification (Ref p.183).

### 10.2 Implement special methods safely
**Origin:** [official] (Ref p.50–54, 58–70)
1. `__init__` never returns a value; the derived one calls the base's; `__new__` returns an instance of `cls`, otherwise `__init__` does not run.
2. Arithmetic and comparison operators return `NotImplemented` for unknown types. Assigning `None` to the method (e.g. `__add__ = None`) blocks the reflected fallback; `None` has a defined effect only for `__hash__`, `__iter__`, `__reversed__`, `__contains__`, `__class_getitem__`, `__fspath__`.
3. `__pow__` must accept the 3rd argument if `pow(a, b, m)` is used; in 3.14 `__rpow__` is also consulted in that case.
4. `__iadd__` and the like return the object (normally `self`); a forgotten `return None` makes `x` become `None`.
5. `__exit__` returning a true value swallows the exception; do not re-raise the received exception, return false instead.
6. A class with a potentially huge `__len__`, used in `if obj:`: consider `__bool__`.
7. `__getattribute__`/`__setattr__` accessing `self.x` directly recurse endlessly: use `object.__getattribute__`/`object.__setattr__`. `__getattr__` only runs after a normal failure and must raise `AttributeError`.
8. A descriptor assigned to the class after it was created: `__set_name__` is not called; call it by hand.
9. A metaclass that overrides `__new__`: forward `**kwargs` and propagate `__classcell__`.
10. Magic methods must be defined on the class; assigning on an instance (`obj.__len__ = ...`) does not count for `len()` or `with`.
11. Releasing a resource: replace `__del__` with `with`/`try...finally` or `weakref.finalize`.

**Verify:** test `len(obj)`, `with obj`, `obj == outro` and `hash(obj)` explicitly.

---

## 11. Modules and packages

### 11.1 Create a package
A directory with `__init__.py` (can be empty); subpackages with their own; `__all__` if you want to support `import *`; import by full name or `from ... import` (Tut p.54–55). **Origin:** [official]. Check `__all__` when there is `from x import *`; if `from pkg import nome` gives `ImportError`, both the attribute and the submodule are missing (Ref p.121).

### 11.2 Import a module outside `sys.path`
**Origin:** [community] (Notes p.272)
1. `sys.path.append(<directory that CONTAINS the module>)`, not the file path.
2. `import nomedomodulo`.

### 11.3 Reload a module
Python 3: `from importlib import reload; reload(mod)`. Manual alternative: `del sys.modules['mod']` and import again (Notes p.274–275). **Origin:** [community].

### 11.4 Dynamic modules and circular imports
**Origin:** [official] (Ref p.38–41, 85, 90–91)
1. Prefer `importlib.util.module_from_spec()` to `types.ModuleType`; read metadata through `__spec__.*`, not `__package__`, `__loader__`, `__cached__`, `__path__` (deprecated).
2. Circular imports: the partial module is already in `sys.modules`, avoiding infinite recursion.
3. A finder that blocks a module: raise `ModuleNotFoundError`, do not return `None`.
4. A module run by file path has `__main__.__spec__` `None`; use `-m` when you need valid metadata.

### 11.5 Create and publish a package (according to the text)
**Origin:** [community] (Notes p.415–417, 435–437). **[DATED]** in large part: based on `setup.py`, `Command`/`cmdclass` and the old upload method (`setup.py register/upload`). Do not treat it as current practice without checking the current documentation [inference].
1. Package folder with `__init__.py` and `setup.py` next to it; in `setup.py`: `name`, `version`, `description`, `url`, `install_requires`, `packages` (or `find_packages()`).
2. Test the installation in a fresh virtualenv.
3. Define the versioning scheme (semantic or calendar-based) before uploading: PyPI does not allow overwriting an uploaded version; test first on the test server.
4. Upload with `twine upload dist/*` (safer than the old method) and test `pip install` in a clean environment.
5. Include a README and a license; executable: `__main__.py`; terminal command: `entry_points={'console_scripts': ['greetings=greetings.hello_world:main']}`.
6. Custom `setup.py` commands **[DATED]**: subclass of `Command` (`initialize_options`, `finalize_options`, `run`) in `cmdclass`.

---

## 12. File I/O and serialization

### 12.1 Read and write files safely
**Origin:** [official] (Tut p.63–66) + [community] (Notes p.184–194)
1. `with open(path, mode, encoding="utf-8")`; omit `encoding` only in binary.
2. Text: `read()` (all), `readline()` (one) or `for linha in f` (preferable for large files; `strip()` removes line breaks).
3. Write only `str` (text) or `bytes` (binary); convert first; write `\n` explicitly with `write`.
4. Avoid overwriting an existing file: mode `'x'` (Python 3).
5. Do not mix direct iteration over the file with `readline()`.
6. Existence: prefer EAFP when possible.

**Verify:** after the `with` the file is closed; `f.read()` on it gives `ValueError: I/O operation on closed file` (Tut p.64). **Pitfall:** the default text encoding is the locale's (Windows: ANSI code page), so make it explicit for portable data (Ref p.179) [inference]; a file without `with`/`close()` is a review point (Ref p.31); mixing `bytes` and `str` calls for checking binary/text mode (Ref p.171, 184).

### 12.2 Persist and read JSON
**Origin:** [official] (Tut p.66) + [community] (Notes p.297–300)
1. Write: `with open(nome, 'w') as f: json.dump(obj, f)`; read: `json.load(f)`. Use UTF-8.
2. Readable output: `indent=2`; stable order: `sort_keys=True`; compact: `separators=(',', ':')`.
3. Non-serializable type (e.g. `datetime`): subclass of `json.JSONEncoder` with `default()` that returns a serializable representation (e.g. `isoformat()`) and delegates to `super().default` for the rest.
4. Format from the command line: `python -m json.tool arquivo.json`.
5. Line-by-line JSON: one `dumps` per line with `\n`, reading line by line.

### 12.3 Use SQLite
**Origin:** [community] (Notes p.301–302, 668–673)
1. `conn = sqlite3.connect('arquivo.db')` (or `':memory:'`); `cur = conn.cursor()`; `execute` with placeholders.
2. `conn.commit()` before closing: `close()` does not commit and discards pending changes; `executescript` issues a COMMIT before running.
3. Read: iterate the cursor, `fetchone()` (`None` at the end), `fetchmany(n)` or `fetchall()`. Errors: `sqlite3.Error`.
4. Types: None↔NULL, int↔INTEGER, float↔REAL, str↔TEXT, bytes↔BLOB.

### 12.4 Serialize with pickle
**Origin:** [community] (Notes p.528–529, 535)
1. Open in binary mode (`'wb'`/`'rb'`).
2. `pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)`; read with `pickle.load(f)`.
3. Non-picklable or ephemeral parts: `__getstate__` (only what is needed) and `__setstate__` (recreates the rest); the text suggests a dictionary of values instead of a list.
4. **Never** load untrusted pickle.

### 12.5 ZIP, gzip and tar
**Origin:** [community] (Notes p.585–588)
1. `with zipfile.ZipFile(nome) as z`; inspect with `printdir()`, `namelist()`, `infolist()`.
2. Extract: `extractall(path)` or `extract(name, path)`.
3. Create: `ZipFile(nome, mode='w')` with `write(file, name_in_zip)` or `writestr(name, bytes)`.
4. gzip: `gzip.open(nome, 'wb')`; tar: `tarfile` + `extractall`.

### 12.6 Directories, subprocesses and local server
- Create a directory idempotently (the text's version): `try: os.makedirs(p)` and, in `except OSError`, re-raise unless `os.path.isdir(p)` is true (Notes p.303–304) [VERIFICAR whether there is a simpler form in the official documentation]. **Origin:** [community].
- Subprocess output line by line: `Popen(cmd, stdout=PIPE)`; `while process.poll() is None:` with `readline()`; if the output does not end in a line break, `read(1)`; the same for stderr (Notes p.433–434). **Origin:** [community].
- Serve files in development: `python3 -m http.server [port]` (default 8000), serves the current directory on all interfaces (0.0.0.0) (Notes p.563, 566). Py2: `python -m SimpleHTTPServer` **[DATED]** (Notes p.566). **Origin:** [community].

---

## 13. Dates and time zones

### 13.1 Parse a date with a time zone
**Origin:** [community] (Notes p.65, 68, 71–72)
1. Python 3.2+: `strptime(texto, "%Y-%m-%dT%H:%M:%S%z")` (offset `+HHMM`).
2. Free formats or old versions: `dateutil.parser.parse`.
3. Time-zone abbreviations (EST, CST) are ambiguous: pass `tzinfos={...}` mapping abbreviation to `tzinfo`.
4. Free-text date: `parse(texto, fuzzy=True)`.
5. Convert zones: make the datetime "aware" (`replace(tzinfo=...)`) and use `astimezone(destination)`.

**Verify:** the result has a non-null `tzinfo` before converting.

### 13.2 Iterate over a date range
`passo = timedelta(days=1)` and `for i in range((fim - inicio).days): inicio + i*passo` (Notes p.72). **Origin:** [community].

---

## 14. Virtual environments and pip

### 14.1 Virtual environment cycle
**Origin:** [official] (Tut p.107–109) + [community] (Notes p.705–711)
1. Create: `python -m venv .venv`. **[official]** The Tutorial calls `.venv` a common location for the environment (not mandatory): the name is usually hidden in the shell and avoids collision with `.env` files (Tut p.107). The venv installs the Python version that ran the command (Tut p.107). Notes: `python3 -m venv foo` (≥ 3.3) or `virtualenv foo`.
2. Activate: Windows `tutorial-env\Scripts\activate`; Unix/macOS `source tutorial-env/bin/activate`. The Tutorial's activation script is for bash; for csh or fish there are `activate.csh` and `activate.fish` (Tut p.107).
3. Check with `which python`/`which pip` that they point inside the environment.
4. Install: `python -m pip install nome`; pinned version `nome==x.y.z`; `--upgrade`; `pip uninstall`; inspect with `pip show` and `pip list`.
5. Freeze: `python -m pip freeze > requirements.txt`; reinstall: `python -m pip install -r requirements.txt`. **[official]** The Tutorial calls it a common convention to save the `freeze` output in `requirements.txt` and says the file can be versioned and distributed with the application (Tut p.109).
6. Leave: `deactivate`.

**Illustrative and old Tutorial outputs:** the Tutorial's terminal examples show Python 3.5.1 (Tut p.108) and pip 7.0.3, requests 2.7.0, numpy 1.9.2 (Tut p.109). They are old illustrations; do not treat the versions or the text of pip's messages as current.

**Verify you are in a venv:** with `venv`, `sys.base_prefix` differs from `sys.prefix`; in the old `virtualenv` there is `sys.real_prefix` **[DATED]** (Notes p.711). **Pitfalls:** `freeze` lists transitive dependencies and the text suggests writing only the top-level ones by hand (Notes p.706); `--local` restricts to the current virtualenv (Notes p.423–424).

### 14.2 Install and upgrade packages with pip
**Origin:** [community] (Notes p.54–55, 421–426) + [official] (Tut p.108–109)
1. Prefer `python -m pip ...`: avoids PATH problems on Windows and chooses the interpreter (Notes p.30, 55); on Windows, `py -3 -m pip`.
2. Forms: `pip install pacote`, `pacote==x.y.z`, `'pacote>=x.y.z'`, `-r requirements.txt`; `pip list --outdated` to see outdated ones; `--upgrade` per package. Upgrading all at once is not a standard pip function.
3. Proxy: `pip --proxy http://<server>:<port> install ...`.
4. Pre-releases: `--pre`; test first in a virtual environment.
5. Repository: `pip install git+URL`, or clone and `pip install path` (allows `git pull` and `git checkout` of earlier versions).

**Pitfalls:** with Python 2 and 3 installed, `pip` usually points to 2 and `pip3` to 3 **[DATED]** (Notes p.54); pip is bundled with python.org builds since Python 2.7.9 and 3.4. Do not use `pip.main` or `distutils` as current practice **[DATED]** [inference]: the material used does not detail them.

---

## 15. Testing

### 15.1 Basic stdlib tests
`doctest.testmod()` validates examples in docstrings; `unittest.TestCase` with `assertEqual` and `assertRaises`; `unittest.main()` runs when the file is invoked (Tut p.97). **Origin:** [official].

### 15.2 Write a test with pytest
**Origin:** [community] (Notes p.762–769)
1. File `test_*.py`, functions `test_*`, plain `assert`; pytest explains the failure by showing values and the call.
2. Repeated setup: `@pytest.fixture` with a noun name, declared as a parameter of the same name.
3. Cleanup: `yield` in the fixture and the cleanup after it.
4. Replace an external dependency: fixture with `monkeypatch.setattr(modulo, 'Popen', MockPopen)`.
5. Run: the text uses `py.test` at the root and `-k nome` to filter [VERIFICAR the current name of the executable].

### 15.3 Mock a function with `create_autospec`
1. `import custom_math` (the whole module) and `custom_math.multiply = create_autospec(custom_math.multiply)` before importing the module under test.
2. Check with `assert_called_with`; the signature is respected, so wrong arguments raise `TypeError` (Notes p.763–764). **Origin:** [community].

---

## 16. Concurrency

### 16.1 Choose and implement
**Origin:** [community] (Notes p.536–550, 591–592) + [official] (Ref p.172–178)
1. Determine whether the bottleneck is I/O or CPU.
2. I/O: `threading.Thread` or `ThreadPoolExecutor`. CPU: `multiprocessing.Pool` or `Process`.
3. In `multiprocessing`, create processes under `if __name__ == "__main__":`.
4. `start()` on all and then `join()` on all.
5. Shared state: `Queue`/`Value` between processes, `Lock` between threads.
6. Pool: finish with `close()`/`join()` (the author says that, without it, processes may persist) [VERIFICAR] (Notes p.591–592).

**Pitfalls:** see 20.8 (LBYL on shared structures, `contextvars`, thread-safety limits in free-threaded builds).

---

## 17. Debugging, logging, memory and performance

### 17.1 Debug with pdb
**Origin:** [community] (Notes p.501–503)
1. `import pdb; pdb.set_trace()` (on one line, easy to comment out) or `python -m pdb arq.py`.
2. Navigate: `n`, `s`, `r`, `c`; inspect `p`; list `l`; stack `bt`/`up`/`down`.
3. Variable named like a command: `!nome`.

### 17.2 Handle an unknown error
**Origin:** [community] (Notes p.458–462)
1. Read the message. `NameError`: undefined name, used before, no `import` or out of scope (apply 4.1). `TypeError`: argument count, incompatible operands, object not iterable/subscriptable/callable. A `SyntaxError` on a seemingly correct line usually comes from unclosed parentheses or brackets on the previous one.
2. `IndentationError`: no tabs, editor at 4 spaces, replace tabs and display tab as 8 spaces.

### 17.3 Set up logging
**Origin:** [community] (Notes p.595–598)
1. `logger = logging.getLogger()`; `StreamHandler`; `Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')`; `setLevel`.
2. Or `dictConfig({... 'version': 1 ...})`.
3. In `except`, `logging.exception('msg')` logs with the traceback; for another level, `logging.warning('msg', exc_info=1)` and equivalents.

### 17.4 Free memory and investigate a leak
**Origin:** [community] (Notes p.525–527)
1. `sys.getrefcount(obj)` inspects references (the value usually comes out +1 because of the argument; reviewer's observation). Do not base business logic on it: it is an implementation detail (Ref p.171, 177).
2. Cycles: `gc.collect()` collects them.
3. Many small objects not being freed and the collector running too much: `gc.set_threshold(g0, g1, g2)`.
4. Manual `gc.collect()` with large objects (the trigger is by count, not by memory); the text discourages it: it is a patch until the leak is found. In long-running servers, it can be triggered by time, requests or event type.

### 17.5 Measure performance
**Origin:** [community] (Notes p.770–777)
1. `python -m timeit "expr"` or `%timeit` in IPython.
2. `python -m cProfile -s time main.py` (`ncalls`, `tottime`, `cumtime`).
3. `kernprof -l -v script.py` with `@profile` on the suspect functions (time per line).
4. In the text's example, 89.9% of the time was in a network request and 10% in computation: I/O usually dominates.

---

## 18. Practical security (randomness and passwords)

### 18.1 Secure random value
**Origin:** [community] (Notes p.318–319)
1. Alphabet: `string.ascii_letters + string.digits + string.punctuation`.
2. `secure = random.SystemRandom()` and `''.join(secure.choice(alphabet) for _ in range(n))`.
3. In 3.6+, prefer the `secrets` module. The official recipe cited repeats until the character-class requirements are met.

### 18.2 Password hash
`salt = os.urandom(16)`; `hashlib.pbkdf2_hmac('sha256', password_in_bytes, salt, iterations)`; store the salt next to the hash; verify by recomputing with the same salt (Notes p.778). **Origin:** [community].

---

## 19. Migrating Python 2 to 3

**Notice:** everything here is for recognizing and converting legacy code. The Python 2 snippets (the source side of each conversion) are **[DATED]**. **Origin:** [community] (Notes p.621–646).

### 19.1 Manual checklist
1. `print x` becomes `print(x)`; `print >>f, x` becomes `print(x, file=f)` (Notes p.626). A trailing comma (`print x,`) becomes `print(x, end="")` (Notes p.186, 626); in Py2 that comma also adds a space (Notes p.186), so the exact equivalent keeps the space in the text or uses `end=" "` [inference]. The function accepts `sep`, `end`, `file` and `flush` (`flush` since 3.3) (Notes p.626); in Py2.6+ the function only exists with `from __future__ import print_function` and without `flush` (Notes p.627) **[DATED]**. Pitfall: `print(1, 2, 3)` prints a tuple in Py2 and `1 2 3` in Py3 (Notes p.626).
2. `/` between integers: in Py2 it gives floor and in Py3 it gives `float`; decide whether it was integer division and use `//` (Notes p.80–81). The Tutorial confirms that `/` always returns `float` and that `//` does floor division (Tut p.13 and glossary, Tut p.129) **[official]**. `from __future__ import division` only makes sense in code still on Py2 and is unnecessary in Py3 (Notes p.80–81) **[DATED]**.
3. `raw_input` becomes `input`; the old `input`, which evaluated, should not be replicated with `eval(input())` thoughtlessly.
4. `xrange` becomes `range`; `.next()` becomes `next(it)`; `iteritems/iterkeys/itervalues` become `items()/keys()/values()` or `iter(d)`; `has_key` becomes `in`.
5. `map`, `filter`, `zip` are now iterators: `list(...)` if you will index or iterate twice.
6. `except E, e` becomes `except E as e`; `raise E, "msg"` becomes `raise E("msg")`.
7. Renamed modules (Queue→queue, SocketServer→socketserver, ConfigParser→configparser, urllib/urllib2 reorganized, Tkinter→tkinter, etc.).
8. `reduce` becomes `functools.reduce`.
9. `__nonzero__` becomes `__bool__`; `__cmp__`/`cmp` removed: use rich comparisons or `functools.cmp_to_key`.
10. Octal `0755` becomes `0o755`.
11. Text vs bytes: in Py3 `str` is Unicode text and `bytes` is a sequence of bytes; in Py2 the plain `str` was bytes and text was `unicode` (Notes p.624–625, 655). Convert explicitly: `.encode(encoding)` goes from text to bytes and `.decode(encoding)` from bytes to text, and on the way back you need to know the encoding; the default error mode is `strict` (Notes p.653–656). Indexing `bytes` in Py3 gives `int` (Notes p.625). Open in text/binary mode as appropriate and declare `encoding=`; binary mode does not accept `encoding` (Notes p.654).
11a. Literals: `u'...'` is accepted in Py3.3+ and has no effect (Notes p.625; Ref p.21, which lists it as a prefix allowed for compatibility); Py2's `ur'...'` gives `SyntaxError` (Notes p.625); the Reference's list of allowed prefixes does not include `ur` (Ref p.21) [inference that this explains the error].
12. Implicit relative imports become explicit (`from . import x`).
13. `.encode('hex')`/`.decode('hex')` become `codecs.encode/decode(..., 'hex')` or equivalents.
14. Parameters unpacked in the signature or in a lambda (`lambda (x, y): ...`) were removed: receive one argument and unpack in the body.
15. `exec "code"` becomes `exec("code", globals, locals)` (a form that works in both).

### 19.2 With 2to3 **[DATED]** as a tool
1. `2to3 arquivo.py` shows the diff without changing anything; `-w` writes and creates a `.bak` backup (e.g. `example.py.bak`), unless `-n` is used (Notes p.645–646). The sources used do not say whether `2to3` exists in Python 3.14; check the current documentation before depending on it [VERIFICAR].
2. Options: `-f/--fix` and `-x/--nofix` choose transformations, `-l` lists, `-j` parallelizes, `-o DIR` with `-n` writes to another directory, `-W` writes without change, `--add-suffix` (Notes p.645–646).

**Verify:** run the tests after conversion (section 15) [inference].

---

## 20. Review checklist ("if X, check Y" heuristics)

The items below are **package heuristics** ("if X, check Y" rules), assembled from the Language Reference 3.14 pages **[official]** indicated under "basis". The review rule is the package's; what the Reference actually states is on each page cited, and the wording here does NOT imitate the Reference's. Where an item includes a link made by the package, it carries [inference]. Items already detailed in a procedure appear only as a cross-reference.

### 20.1 Identity, equality and operators
- Package heuristic, basis: Ref p.108, 110. `==` against `None`/`True`/`False`/`NotImplemented`: replace with `is`; `is` with numbers, strings or methods: probable bug. See 5.1, 5.2.
- Package heuristic, basis: Ref p.108–109. `sorted`/`min`/`max` over sets, dicts or heterogeneous types: partial order or `TypeError`; NaN in `==`, `in`, sets and dicts is surprising.
- Package heuristic, basis: Ref p.105, 107, 112. `-x ** n`, `a ** -b`, `a & b == c`, `x | y < z`: parenthesize.
- Package heuristic, basis: Ref p.106, 175. `//` and `%` with negatives or floats: floor and the divisor's sign (`(-11)//4 == -3`); `math.fmod` when the dividend's sign matters.
- Package heuristic, basis: Ref p.110, 165. `x or default` also fires on zero and empty; `:=` in the listed contexts requires parentheses.
- Package heuristic, basis: Ref p.111, 115–116. Assignment with effects on both sides (`i, x[i] = ...`, `a[i] += f()`): check the evaluation order.
- Package heuristic, basis: Ref p.67, 115. `x += y` on a shared mutable affects all references; `__iadd__` without a return leaves `x` as `None` [inference about the forgotten `None`].

### 20.3 Flow, exceptions and `match`
- Package heuristic, basis: Ref p.117. If `assert` validates input or has a side effect, it vanishes with `-O`. See 9.1.
- Package heuristic, basis: Ref p.118–119. If there is a `raise` inside `except`, consider `from exc`/`from None`.
- Package heuristic, basis: Ref p.129. If `finally` has `return/break/continue`, the exception is discarded.
- Package heuristic, basis: Ref p.129. If the `try`'s `else` contains cleanup, errors there are not handled by the sibling `except` clauses.
- Package heuristic, basis: Ref p.68, 130. In `__exit__`, the Reference says a true return value suppresses the exception in flight and a false one lets it propagate; when reviewing, check that each `__exit__` that returns true does so on purpose.
- Package heuristic, basis: Ref p.126. The Reference says the names of the `for` target are not deleted at the end of the loop and that, with an empty sequence, the name is never even assigned. When reviewing, be suspicious of use of the loop variable after the `for` and of any reading of the loop's `else` as if it meant an empty loop.
- Package heuristic, basis: Ref p.132–138. If `match` uses a simple name, it is a capture; a capture or `_` before other cases leaves the following ones unreachable; `str`/`bytes` do not match as a sequence; `Classe(x, y)` requires `__match_args__`; do not rely on effects of patterns or guards. See 5.3.

### 20.4 Scope, functions and decorators
- Package heuristic, basis: Ref p.76. If a function reads and then assigns the same name (including by `import`, `for`, `with ... as`, `:=`, `del`), probable `UnboundLocalError`. See 4.1.
- Package heuristic, basis: Ref p.36, 44, 140, 142. If there is a mutable default in `def` or a mutable attribute in the class body, classic bug.
- Package heuristic, basis: Ref p.103–104. If a call mixes `*args` with keywords or uses `**mapping` with non-string/duplicate keys, expect `TypeError`.
- Package heuristic, basis: Ref p.181. If there are many parameters with the same passing form, consider `/` and `*`.
- Package heuristic, basis: Ref p.20, 93–94. If `__x` appears, remember the mangling applies to textual identifiers in the class, not to names built as strings.
- Package heuristic, basis: Ref p.171. If attributes are created by `setattr` with a non-identifier name, read them with `getattr()`.

### 20.5 Classes and special methods
- See 10.2 (basis: Ref p.50–70). Async protocol: `__aenter__`/`__aexit__` and `__aiter__`/`__anext__` (end via `StopAsyncIteration`) (basis: Ref p.170).
- Package heuristic, basis: Ref p.183. `__slots__` requires justification.
- Package heuristic, basis: Ref p.174. `type()`/`isinstance()` deciding behavior: consider duck typing, EAFP or ABCs.
- Package heuristic, basis: Ref p.109. `in` without `__contains__` falls back to `__iter__` and `__getitem__`.

### 20.6 Annotations, types and versions
- Package heuristic, basis: Ref p.144, 147. `[T]` in def/class/type requires 3.12+; type parameter defaults, 3.13+; lazy annotations, 3.14.
- Package heuristic, basis: Ref p.36, 40, 42, 69, 147–148. Direct reading of `__annotations__` or dependence on effects at definition: use `annotationlib.get_annotations()`; do not delete `__annotate__`, use `None`; `from __future__ import annotations` in new code is expected to be deprecated.
- Package heuristic, basis: Ref p.174, 185. Python does not enforce annotations; `get_type_hints()` does not cover locals. On type aliases: the Reference says the value of an alias created with the `type` statement is evaluated lazily (Ref p.123, 174) and defines "type alias" as a synonym "created by assigning" the type to an identifier (Ref p.185). That an alias by assignment is evaluated immediately is the package's [inference]: the Reference does not use that word at this point.
- Package heuristic, basis: Ref p.142–144. `async for/with/await` outside `async def`: `SyntaxError`.
- Package heuristic, basis: Ref p.45–47. `co_lnotab` deprecated since 3.12 (use `co_lines()`); `frame.f_locals` may be a proxy since 3.13.
- Package heuristic, basis: Ref p.182–184. A "soft deprecated" API remains valid (avoid only in new code); "provisional" may break between versions.
- Package heuristic, basis: Ref p.171, 177, 183. Logic dependent on `sys.getrefcount()`, bytecode or immortality: implementation detail.
- Strings, modules and I/O: see 8.3, 11.1, 11.4 and 12.1 (basis: Ref p.18–27, 38–41, 85, 90–91, 121, 171, 179, 184).

### 20.8 Concurrency and async
- Package heuristic, basis: Ref p.178. The Reference says a container (such as a list) produces a new iterator on each `for`, while an iterator returns the same, already exhausted iterator, looking like an empty container. When reviewing, be suspicious of a collection that may be an iterator and is traversed twice.
- Package heuristic, basis: Ref p.178. The Reference illustrates the LBYL risk in a threaded environment with `if key in mapping: return mapping[key]`, which fails if another thread removes the key between the test and the read, and cites locks or EAFP as ways out. When reviewing, treat this pattern on a shared structure as suspect.
- Package heuristic, basis: Ref p.176, 178. If the code assumes the GIL for data safety, the manual only says that thread-safety of iterator operations is not guaranteed in free-threaded CPython (Ref p.178); the GIL entry (Ref p.176) says it makes the object model, including types such as `dict`, implicitly safe against concurrent access, and that it can be disabled since 3.13; under free-threading that premise no longer holds [inference].
- Package heuristic, basis: Ref p.172–173, 99–100. If tasks share global state, use `contextvars`. If an async generator is interrupted, `aclose()`; the initial `send()` is `None`.

The Reference's pointer map for `match`, `try/except*`, multiple `with`, `def`/`class` and type parameters is in Ref p.211–225.

---

## 21. Gaps and pending checks

- The Notes have no uniform versioning: treat a passage without a version mark as possibly Py2 and confirm in the Tutorial or the Reference.
- The material has no procedure on `pip.main`, `distutils` or `setup.py register`; they were marked **[DATED]** by inference.
- There is no procedure for `zoneinfo`/IANA zones; dates only have the Notes' `strptime`/`dateutil`/`astimezone` flow.
- [VERIFICAR]: current name of the pytest executable (`py.test`) and `close()`/`join()` on Pool.
- The Reference does not detail the attribute errors of circular imports (Ref p.85).
