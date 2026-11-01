# Python cases, pitfalls and anti-patterns

Reference base of the Python specialist agent. It gathers pitfalls with their causes and fixes, anti-patterns and short cases, derived from the intermediate notes of the Tutorial 3.14.0rc3 and of the community book "Python Notes for Professionals".

## How to read this file

- **(Tut p.N)**: official Tutorial 3.14.0rc3, origin **[official]**. **(Notes p.N)**: "Python Notes for Professionals", origin **[community]**: a book by contributors, mixing Python 2 and 3, with errors and unsafe snippets presented without warning. The agent must not repeat something just because the book shows it.
- **(Ref p.N)**: Language Reference 3.14.0rc3, origin **[official]**. The original base did not contain it; it appears only in a few items (loop and comprehension in 1.4, `lambda` in a loop in 1.2), checked against the source. The rest of the file was not cross-checked against the Reference.
- **[DATED]**: Python 2 or old versions. **[inference]**: link made by whoever assembled this base. **[VERIFICAR]**: doubt already flagged in the notes. **[BUG-FONTE]**: wrong example in the book (Appendix A).
- "Version" column: "all" means the notes do not restrict the version. Error messages quoted are only those that appear in the notes; where the note gives only the exception type, the table carries the type without invented text.

## Contents

1. Part 1: pitfalls and error messages by topic (1.1 mutability, 1.2 arguments and scope, 1.3 comparisons, 1.4 iteration and collections, 1.5 strings and regex, 1.6 exceptions, 1.7 classes, 1.8 imports, 1.9 concurrency and networking, 1.10 files and persistence, 1.11 numbers and dates, 1.12 environment)
2. Part 2: anti-patterns (2.1 security, 2.2 style and robustness)
3. Part 3: illustrative cases
4. Appendix A: errors in the book itself (do not reproduce)
5. Appendix B: contradictions and items to verify
6. Appendix C: gaps

---

# Part 1: Pitfalls and error messages by topic

## 1.1 Mutability and aliasing

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `x = y = [7, 8, 9]` and then `x[0] = 13` also changes `y` | both variables point to the same object | create distinct lists or copy | Notes p.34 | [community] | all |
| Two variables for the same list: changing one shows up in the other | assignment binds names, it does not copy | `lista.copy()` or `lista[:]` (shallow copy) | Tut p.19, p.39; Notes p.140, p.343–344 | [official] + [community] | all |
| `[[]] * n` or `[obj] * n`: mutating one element mutates all | repeats n references to the same object | `[[] for _ in range(n)]` or `append` in a loop | Notes p.147–148, p.785–786, p.700 | [community] | all |
| `d2 = d1.copy()` and `d1[1] is d2[1]` is true | a shallow copy shares inner objects | `copy.deepcopy` | Notes p.406 | [community] | all |
| Results accumulate between calls (`f(a, L=[])` prints `[1]`, `[1, 2]`, `[1, 2, 3]`) | the default is evaluated only once, at definition time | default `None` and create the list inside the function | Tut p.31–32; Notes p.207–208, p.788–789 | [official] + [community] | all |
| Mutable default in `__init__` (`pos=[0,0]`) is shared between instances | same cause: default evaluated once | `None` and create it in the body | Notes p.237 | [community] | all |
| `tricks` list shared between instances | mutable list as a class variable | create `self.tricks = []` in `__init__` | Tut p.84; Notes p.238, p.788 | [official] + [community] | all |
| `self.x.append(...)` changes the class attribute for everyone; `c.x = v` only creates an instance attribute | mutating versus rebinding | initialize in `__init__` | Notes p.238 | [community] | all |
| Tuple containing a list and `+=`: raises `TypeError` but the inner list changed | the mutation happens before the attempt to rebind the name | avoid mutables inside tuples | Notes p.179 | [community] | all |
| `TypeError: 'str' object does not support item assignment` | `str` is immutable | build a new string | Tut p.18 | [official] | all |
| `('a')` or `('hello')` is not a tuple | the comma is missing | `('a',)` | Notes p.178; Tut p.44 | [community] + [official] | all |
| `sort`, `reverse`, `append`, `insert`, `remove` return `None`; assigning the result loses the list | methods that mutate return `None` | use `sorted()` to get a new list | Notes p.41, p.137–138, p.150; Tut p.40, p.46 | [community] + [official] | all |
| `{}` creates a dict, not an empty set | syntax reserved for dict | `set()` | Notes p.76; Tut p.45 | both | all |
| `TypeError: unhashable type: 'set'` in a set of sets; a list as a dict key raises `TypeError` | only hashable objects serve as key or member | `frozenset`; tuple (only with immutable items) | Notes p.76, p.132; Tut p.45, p.130 | both | all |
| `d['xx'].append(3)` on a `shelve` does not persist | `d['xx']` returns a copy | read, mutate the copy and reassign; or `writeback=True` (more memory and slower close) | Notes p.732–733 | [community] | all |

## 1.2 Arguments, functions, decorators and scope

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `NameError: name 'n' is not defined` | the name never received a value, an `import` is missing, or the scope does not see it | assign/import before use; function variables do not exist outside it | Tut p.14; Notes p.458–459 | both | all |
| `UnboundLocalError` when reading a global and then assigning it in the function; even an `if False:` branch with an assignment makes the name local | any assignment in the body creates a local name | declare `global` or pass it as a parameter | Notes p.95–96, p.99 | [community] | all |
| `UnboundLocalError` on `num += 1` in the inner function | assigns to the outer-scope variable without a declaration | `nonlocal num` | Notes p.94, p.210; Tut p.134 | both | Python 3 |
| `nonlocal` at module level or without an enclosing function is a `SyntaxError` | `nonlocal` requires an enclosing function | use `global` in the module | Notes p.94 | [community] | Python 3 |
| `del x` in the function makes `x` local | `del` is also a binding | declare `global` or `nonlocal` first | Notes p.96 | [community] | all |
| Lambda, comprehension or generator in the class body does not see class variables | the class scope is not enclosing for these | pass as an argument or use `Classe.nome` | Notes p.97–98 | [community] | all (the book says `[a for i in range(10)]` reads the class `a` in Python 2 and the global in Python 3) |
| `TypeError: function() got multiple values for argument 'a'` | positional and keyword for the same parameter | pass it only once | Tut p.32 | [official] | all |
| `*pair` plus a keyword for the same parameter: "multiple values for argument" | collision between unpacking and name | fix the call | Notes p.214–215 | [community] | all |
| `def foo(name, **kwds)` called with key `name`: `got multiple values for argument 'name'` | collision between parameter and `**kwds` key | `def foo(name, /, **kwds)` | Tut p.35 | [official] | 3.8+ [inference: `/` syntax] |
| `TypeError: ... got some positional-only arguments passed as keyword arguments: 'arg'` | parameter before `/` passed by name | pass by position | Tut p.34 | [official] | 3.8+ [inference] |
| `TypeError: kwd_only_arg() takes 0 positional arguments but 1 was given` | parameter after `*` passed by position | pass by name | Tut p.34; Notes p.210–211 | both | Python 3 |
| `TypeError: combined_example() takes 2 positional arguments but 3 were given` | the third is keyword-only | `kwd_only=3` | Tut p.35 | [official] | Python 3 |
| Multiple return assigned to a single variable | the value is a tuple; the error shows up far away | unpack: `a, b = xyz()` | Notes p.797 | [community] | all |
| `{my_var: api_key}` uses the value of `my_var` as the key | the key is an evaluated expression (unlike JavaScript) | string literal for a literal key | Notes p.797–798 | [community] | all |
| `RuntimeError` from deep recursion (`RecursionError` since 3.5) | implementation limit | iterate or `lru_cache`; `sys.setrecursionlimit` only with judgment (uses more memory) | Notes p.211–212, p.440, p.443 | [community] | 3.5+ for the new name |
| A decorator without `return` turns the function into `None` | the decorator returns `None` | return the wrapper | Notes p.219 | [community] | all |
| `@decoratorfactory` without parentheses gives `TypeError` | the factory must be called | `@decoratorfactory(...)` | Notes p.222 | [community] | all |
| A decorator without `wraps` loses `__name__` and docstring | the wrapper replaces the function | `@wraps(func)` | Notes p.223 | [community] | all |
| `lambda` or `def` created in a loop returns the last value of the loop variable (package example, not in the source: `fs = [lambda: i for i in range(3)]` and then `fs[0]()` gives 2) | free variables are resolved at run time, not at compile time (Ref p.78, example of a free variable that prints 42); applying it to the loop is [inference] | function factory that receives the value as a parameter (Tut p.36); or `lambda i=i: ...`, because the default value is evaluated once, at function definition (Tut p.31; Ref p.140; lambda uses the same parameter list, Ref p.111) | Ref p.78, p.111, p.140; Tut p.31, p.36 | [official] for the rules; [inference] for the application to the loop | all [inference] |

Note on the `lambda` in a loop row: the source text does not carry this example or the term late binding; the phenomenon is deduced from the official rules cited.

## 1.3 Comparisons, truthiness and identity

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `a == 3 or 4 or 6` (or `a == 1 or 2 or 3`) is always true; `a and b > 2` does not compare `a` | the bare operand is truthy; `or` has lower precedence than `==` | `a in (3, 4, 6)`, `any(...)`, repeat the comparison | Notes p.103, p.794–795 | [community] | all |
| `if foo():` treats legitimate `0`, `''`, `[]` as failure | truthiness does not distinguish absent from empty | compare with `None` | Notes p.102 | [community] | all |
| `0 and print_me()` never calls the function | short-circuit | do not put side effects to the right of `and`/`or` | Notes p.102–103 | [community] | all |
| `'short' is 'short'` and `5 is 5` give `True`, `1000 is 1000` and long strings give `False` | internal cache of integers (book: -5 to 256) and strings | `==` for value; `is` only for `None`, `True`, `False` and singletons | Notes p.107, p.792–793, p.523 [VERIFICAR] | [community] | CPython |
| `if x == True` also matches `1` | equality, not identity | `if x:` or `is True/False/None` depending on intent | Notes p.786–787 | [community] | all |
| `AttributeError` when comparing `Foo` with `Bar` in a naive `__eq__` | accesses an attribute the other type does not have | check `isinstance` first | Notes p.109–110 | [community] | all |
| `"gamma" < "OMEGA"` is `False` | lexicographic order by character; uppercase comes first | normalize case first | Notes p.108 | [community] | all |
| `0 != 1 != 0` is `True` | chaining does not mean all are distinct | compare pair by pair | Notes p.106 | [community] | all |
| `TypeError` when comparing different types (`[1,2] > 'foo'`) or sorting `[None, 'hello', 10]` | no ordering relation between the types | convert or use `key` (e.g. `key=str`) | Notes p.632; Tut p.40, p.48 | both | Python 3 |
| A class without `__lt__`/`__gt__` in `sorted`, `min`, `max` gives `TypeError` | missing ordering protocol | define the methods | Notes p.385 | [community] | all |
| `'a' in adict` is `False` even if `'a'` is a value | `in` on a dict tests keys | `in d.values()` | Notes p.379 | [community] | all |
| `-3**2` gives -9 | `**` takes precedence over unary `-` | `(-3)**2` | Tut p.14 | [official] | all |

## 1.4 Iteration, loops and collections

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| Removing items from a list during iteration skips elements (`pop` in the loop leaves `[1]` from `[0,1,2]`); `insert` can produce an infinite loop | the iteration walks the indices in order (`the iteration goes through the indices in order`, Notes p.790) and the removal or insertion shifts the following indices | iterate over a copy, backwards, or build a new list | Notes p.143, p.789–792; Tut p.23–24, p.47–48 | both | all |
| `RuntimeError: dictionary changed size` when removing keys while iterating `d.keys()` (this is how the source illustrates it) | the dict changed size during iteration; the source attributes the error to Python 3, where `keys()` returns a view and not a list | iterate `list(d)` | Notes p.643 | [community] | Python 3 |
| The same `RuntimeError` when iterating `d` directly and removing keys | same cause (the dict changed size during iteration) | iterate `list(d)` | not in the source: [inference/external knowledge] | [inference] | Python 3 [inference] |
| Reassigning the `for` variable does not change the list | the variable is just a name | assign by index with `enumerate` | Notes p.790–791 | [community] | all |
| A second pass over an iterator or generator produces nothing | exhausted iterator | recreate the iterator or store it in a container | Notes p.199, p.357; Tut p.132 | both | all |
| `StopIteration` from `next()` past the end, or from an exhausted generator without `default` | the iterator ran out | `next(it, default)`; the `for` handles it by itself | Notes p.357, p.361, p.363; Tut p.89 | both | all |
| `TypeError: 'generator' object is not subscriptable` on `g[0]` or `g[:3]` | a generator is not indexable | `next(g)`, `itertools.islice` or `list(g)` | Notes p.157, p.307–308 | [community] | all |
| `list(infinito)`, `cycle` or `count` without a limit never ends | infinite iterables | `islice` or `takewhile` | Notes p.310–312, p.358 | [community] | all |
| The `for` `else` does not run when there was a `break` or an exception | the `else` runs when no `break` occurred | use only when that is the intent | Notes p.115; Tut p.26 | both | all |
| `map`, `filter`, `zip` return single-use iterators | Python 3 change | `list(map(...))` when you need a list | Notes p.114, p.633, p.638 | [community] | Python 3 |
| `.keys()/.values()/.items()` return lists and `.iterkeys()` etc. are generators | old behavior | in new code, iterate the dict directly | Notes p.118 | [community] | **[DATED]** Python 2 |
| `a, b = 1, 2, 3` gives `ValueError`; `a, = iterable` with more than one element too | unpacking requires an exact count | `_` for the exact count or `*rest`; the `a, =` form can serve as an assertion that there is exactly one element | Notes p.33, p.198 | [community] | all |
| `[x, y for ...]` gives `SyntaxError: did you forget parentheses around the comprehension target?` | a tuple target needs parentheses | `[(x, y) for ...]` | Tut p.42; Notes p.160 | both | recent 3.x [inference: message text] |
| `if/else` after the `for` in a comprehension is a `SyntaxError` | the ternary goes before the `for` | move it before | Notes p.149–150 | [community] | all |
| `x.sort()` inside a comprehension returns `None` | method that mutates | `sorted(x)` | Notes p.150 | [community] | all |
| `groupby` without sorting groups only consecutive items; each group's iterator is invalidated when advancing (`sorted(groups)` becomes empty groups) | `groupby` contract | sort by the same key and materialize `list(group)` | Notes p.165–167, p.308–309 | [community] | all |
| A list used as a queue is slow | inserting or removing at the start shifts elements | `collections.deque` | Tut p.40–41 | [official] | all |
| `list.remove`/`index` without the value gives `ValueError`; `pop` on an empty list or invalid index gives `IndexError` | value or position absent | test with `in` or check the size; `index(value, start)` limits the search | Tut p.39; Notes p.137 | both | all |
| The `for` variable keeps existing after the loop; if the iterable is empty, the name is never even assigned. In a comprehension it does not leak in Python 3 (it leaked in Python 2) | the `for` target is not deleted at the end of the loop (Ref p.126; Tut p.41); the comprehension runs in an implicit nested scope, so the target names do not leak (Ref p.95) | use new names; do not read the loop variable after the `for` without making sure the iterable is not empty | Ref p.126, p.95; Tut p.41; Notes p.630–631, p.794 | both | `for`: all; comprehension: does not leak (Ref p.95); it leaked in **[DATED]** Py2 (Notes) |

## 1.5 Strings, Unicode, bytes, regex and formatting

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `IndexError: string index out of range` | simple index beyond the length | check the length; slices tolerate bounds | Tut p.17–18 | [official] | all |
| `'C:\some\name'` breaks the line at `\n` | escape interpreted | `r'...'` | Tut p.15 | [official] | all |
| `TypeError: can only concatenate str (not "int") to str` | `+` between different types | `str()` or commas in `print` | Tut p.67–68; Notes p.395 | both | Python 3 |
| `input()` evaluates the text as an expression | old behavior | use `raw_input` at that time; today, plain `input` | Notes p.46 | [community] | **[DATED]** Python 2 |
| `strip('abc')` does not remove the prefix "abc" | the argument is a set of characters | `startswith` plus slicing | Notes p.259 | [community] | all |
| `split(' ')` produces `''` between consecutive spaces | explicit separator | `split()` without an argument | Notes p.260 | [community] | all |
| `"".isalpha()`, `isupper`, `islower`, `isspace`, `istitle` give `False` | empty string | test for empty separately | Notes p.262–263 | [community] | all |
| `==` between accented strings in different forms (precomposed versus combining) gives `False` | distinct Unicode representations | normalize (`unicodedata`); for caseless, `casefold` and NFKD | Notes p.265–266 | [community] | Python 3 |
| `send`/`sendto` require bytes | strings are Unicode | `.encode('utf-8')` or `b'...'` | Notes p.552–553 | [community] | Python 3 |
| `urlopen().read()` returns bytes; a POST body needs `urlencode(...).encode('utf-8')` | HTTP carries bytes | decode with the correct charset | Notes p.463–464 | [community] | Python 3 |
| `{:x}` on a float (42.0) gives `ValueError` | integer format code | convert to `int` first | Notes p.251 | [community] | all |
| `'{0:.0%}'.format(42.12345)` produces '4212%' | `%` multiplies by 100 | pass a fraction (0.4212) | Notes p.250 | [community] | all |
| `re.match` fails when the pattern is not at the start | `match` anchors at the beginning | `re.search` | Notes p.398 | [community] | all |
| `"\\t"` and `r"\t"` match different things | string escapes versus regex escapes | raw strings | Notes p.398 | [community] | all |
| Reference `\10` in `re.sub` | the book states it is read as group 1 plus "0" [VERIFICAR] | `\g<n>` is unambiguous | Notes p.401 | [community] | all |
| User input interpolated into a regex: `.` and `[` become metacharacters | naive construction | `re.escape` | Notes p.404 | [community] | all |

## 1.6 Exceptions

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| A bare `except:` catches everything; the `try` variable (`res`) may not exist, and a `NameError` masks the original error | broad catch without re-raising | specific types, log the traceback, re-raise; separate `try` blocks for the call and for `res[0]` | Notes p.783, p.448–449 | [community] | all |
| `except Exception` swallows an unexpected error | broad wildcard | handle specific types; if catching `Exception`, log and `raise` | Tut p.69–70 | [official] | all |
| `except B` before `except C`/`D` catches the derived classes as the base | the first match wins | derived classes first | Tut p.69 | [official] | all |
| A handler does not handle an exception raised in another handler of the same `try` | handlers only handle the corresponding `try` | nest another `try` | Tut p.68 | [official] | all |
| An exception from an indirectly called function is caught | the `try` catches exceptions from direct and indirect calls | narrow the body; use `else` for the rest | Tut p.70 | [official] | all |
| The traceback shows two chained exceptions | automatic chaining when raising inside `except` | `raise ... from exc` marks the cause; `from None` suppresses | Tut p.71–72; Notes p.629–630 | both | Python 3 |
| `raise Outra("...", e)` reduces the traceback to that line | creates a new exception without re-raising | a plain `raise` keeps it; in Python 3 use `raise ... from e` | Notes p.449 | [community] | Python 3 |
| `return`, `break` or `continue` in `finally` discards the exception in flight and replaces the `try`'s `return` (`bool_return()` returns `False`) | `finally` semantics | do not use these statements in `finally` | Tut p.73 | [official] | since **3.14** the compiler emits `SyntaxWarning` (PEP 765) |
| A plain `except Exception` catches the whole `ExceptionGroup` | the group is an `Exception` | `except*` extracts by type; the rest is re-raised | Tut p.74–75 | [official] | 3.11+ [inference] |
| `SyntaxError` points to `print`, but a `:` was missing before | the parser points where it notices the error | also look at the immediately preceding line | Tut p.67; Notes p.460 | both | all |
| `IndentationError`: inconsistent indentation, line after `:` without indentation, extra indentation, dedent to a nonexistent level | wrong indentation | 4 spaces; `autopep8` converts | Notes p.59–60, p.462 | [community] | all |

## 1.7 Classes and dunder methods

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `__str__`/`__repr__` that prints instead of returning | side effect on every conversion | return the string | Notes p.497–498 | [community] | all |
| A list of objects shows hexadecimal junk | only `__str__` defined; lists use `__repr__` | define `__repr__` | Notes p.498–500 | [community] | all |
| `eval(str(s))` may give `SyntaxError`, `eval(repr(s)) == s` holds | `repr` aims to reconstruct, `str` is readable | reconstructible `__repr__`, readable `__str__` | Notes p.53–54 | [community] | all |
| `__exit__(self)` without the three arguments fails | the protocol passes type, value and traceback | `__exit__(self, exc_type, exc_value, traceback)` or `*args` | Notes p.408–409, p.411 [VERIFICAR] | [community] | all |
| Multiple inheritance: only the first `__init__` runs; `isinstance` stays true for all | `__init__` without chained `super()` | cooperative `super().__init__()` | Notes p.234–235 | [community] | Python 3 |
| The mixin's `__init__` does not run (`self.radio` does not exist) | `Vehicle.__init__` does not call `super().__init__()` | cooperative in all classes | Notes p.610–611 [inference from the code] | [community] | Python 3 |
| Two pages of the book disagree on the MRO direction | p.611 says right to left, p.617 says left to right | follow left to right [VERIFICAR] | Notes p.611, p.617 | [community] | Python 3 |
| A base class calls a method that lands on the derived class's override | all methods are effectively virtual | name mangling (`__update` in `Mapping`) | Tut p.86–88 | [official] | all |
| No `super()` in `setUp`/`tearDown` | TestCases take part in cooperative multiple inheritance | always call `super` | Notes p.757 | [community] | all |

## 1.8 Imports and modules

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| A local module named like a library module is loaded in its place | the script's directory comes first in `sys.path` | avoid identical names, unless intended | Tut p.52 | [official] | all |
| Editing a module and re-importing does not show the change | import happens once per session (`sys.modules`) | restart or `importlib.reload` | Tut p.51; Notes p.274–275 | both | all |
| `math.pi = 3` persists after re-importing | `sys.modules` prevents re-execution | `importlib.reload` | Notes p.274–275 | [community] | all |
| `from m import *` overwrites local names; inside a function or class it is a `SyntaxError` | imports everything except `_name` | import explicit names | Tut p.50, p.56; Notes p.122, p.272–273 | both | all |
| `from pacote import *` does not bring in a submodule | without `__all__`, only names already in the namespace come; a local name can shadow the submodule | correct `__all__` or import the submodule explicitly | Tut p.56 | [official] | all |
| `ImportError` on `from pacote import item` | item neither defined nor a module | check the name and structure | Tut p.55 | [official] | all |
| `import a.b.c` with `c` a function or class is not allowed | only a module or package in the last element | `from a.b import c` | Tut p.55 | [official] | all |
| A relative import fails in the main script | the main module has no package | absolute imports | Tut p.56 | [official] | all |
| `NameError` from forgetting `import random`; `from random import randint` does not make `random` available | only the imported name enters the namespace | import what you use | Notes p.274 | [community] | all |
| `__import__()` to import programmatically | the book literally says not to use it, but shows it later (p.275) | `importlib.import_module` | Notes p.273, p.275 | [community] | Python 3 |
| `reduce` without an import fails | it was moved to `functools` | `from functools import reduce` | Notes p.325, p.365 | [community] | Python 3 |

## 1.9 Concurrency and networking

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `RuntimeError` when reusing an already started thread | a thread starts only once | create a new `Thread` | Notes p.538 | [community] | all |
| Race condition on shared data | access without a lock | `with lock` | Notes p.545 | [community] | all |
| `if key in mapping: return mapping[key]` fails if another thread removes the key | LBYL in concurrent code | EAFP with `try/except` [inference] | Tut p.132 | [official] | all |
| Threads do not speed up CPU-bound work | GIL; in the book's benchmark, 1 run ≈ 2.05 s, 4 threads ≈ 14.42 s, 4 processes ≈ 2.30 s (values from the author's machine) | processes for CPU | Notes p.543–544 | [community] | CPython |
| A long C call in a thread (`math.factorial`) delays the main thread | the C function holds the GIL | pure-Python version (slower) or a short `sleep` before starting | Notes p.796–797 | [community] | CPython |
| With `fork`, a lock held by another thread is never released in the child | the child inherits locks, but only the main thread | `multiprocessing` handles it in pure Python; with other libraries it may hang | Notes p.547–548 | [community] | Unix |
| `asyncio` does not parallelize blocking functions (`time.sleep`, `requests`) | they block the loop | `asyncio.sleep`, `aiohttp` | Notes p.316–317 | [community] | Python 3 |
| JSON larger than the 1024 buffer truncated: `ValueError: Unterminated string` | single fixed-size read | read in a loop until the end or use a length-prefixed protocol [inference] | Notes p.555 | [community] | all |
| `socketserver` serves one client at a time | single-threaded server | `ThreadingTCPServer` | Notes p.564 | [community] | all |

## 1.10 Files and persistence

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `ValueError: I/O operation on closed file.` | using the file after `close()` or after the `with` | use it inside the block | Tut p.64 | [official] | all |
| Incomplete data written | `write()` without `with` or `close()`; with an exception before `close()` the file stays open | `with` | Tut p.64; Notes p.190–191 | both | all |
| Corrupted binary file | opened in text mode, with line-ending conversion | `'b'` mode | Tut p.63 | [official] | all |
| `encoding` with binary mode is not allowed | binary does not decode | omit `encoding` | Tut p.63 | [official] | all |
| `'w'` erases an existing file | mode semantics | `'a'` to append, `'r+'` to read and write | Tut p.63 | [official] | all |
| Undefined behavior with `seek` | in text mode, arbitrary offsets | only 0 or values from `tell()`; or binary | Tut p.65 | [official] | all |
| `read()` without a size blows up memory on a giant file | reads everything | read in blocks or by lines | Tut p.64 | [official] | all |
| Forgetting `\n` in `write` concatenates lines; `os.linesep` in text mode | text mode already translates | use `\n` | Notes p.191 | [community] | all |
| Closing `sqlite3` without `commit` loses changes; `close` does not commit | uncommitted transaction | explicit `commit` | Notes p.301, p.669, p.674–675 | [community] | all |
| `pickle` in text mode | the representation is bytes | `wb`/`rb` | Notes p.687 | [community] | Python 3 |
| The constructor is not called on deserialization (the book underlines this) | `unpickle` does not run `__init__` | `__setstate__` initializes what `__init__` would initialize | Notes p.529 | [community] | all |
| `json.dumps` of a `datetime` gives `TypeError` | non-serializable type | custom encoder with `default()` | Notes p.299–300 | [community] | all |
| Key order in `json.dumps` | the book says it is not guaranteed | `sort_keys=True` for deterministic output (see Appendix B) | Notes p.298 | [community] | marked as to verify |

## 1.11 Numbers, dates and specialized collections

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `0.1 + 0.1 + 0.1 == 0.3` is `False` | binary representation | `math.isclose` or `Decimal`; a prior `round()` does not solve it | Tut p.116 | [official] | all |
| `round(.70 * 1.05, 2)` gives 0.73 and `Decimal` gives 0.74; `1.00 % 0.10` gives `0.09999999999999995` | binary versus decimal | `Decimal` (including for money) | Tut p.104 | [official] | all |
| `//` is not truncation: `(-11) // 4` gives -3 | floor division rounds down | `int(a / b)` if you want to truncate [inference] | Tut p.129; Notes p.278 | both | Python 3 |
| `round(0.5)` is `0`, `round(1.5)` is `2`; `round(2.675, 2)` gives `2.67` | ties go to even, and binary representation | for exact decimals the book only warns about the imprecision | Notes p.277–278, p.639–640 | [community] | Python 3 |
| `/` division between ints is floor; `-3 / 2 = -2` | old semantics | `from __future__ import division` | Notes p.80 | [community] | **[DATED]** Python 2 |
| pytz: attaching `tzinfo` through the constructor gives the wrong zone | pytz localization model | `tz.localize(naive_datetime)`; after adding a `timedelta`, `tz.normalize(...)` or compute in UTC | Notes p.66–67 | [community] | pytz |
| `dateutil.parser.parse(..., tzinfos={'EST': pytz_tz})` ends up in "Local Mean Time" | combination of the libraries | re-localize | Notes p.71 | [community] | pytz + dateutil |
| `str()` of a datetime with a zero fraction omits microseconds; `strptime` does not accept `+03:00` (according to the book) | different formats between `str` and `strptime` | normalize the format before parsing | Notes p.69–70 | [community] | marked as to verify |
| `defaultdict`: reading a missing key creates it; `defaultdict()` without a factory ends up with `default_factory=None` | reading has a side effect | `in` or `get` to check existence | Notes p.290 | [community] | all |

## 1.12 Environment, installation and tools

| Symptom or message | Cause | Fix | Source | Origin | Version |
|---|---|---|---|---|---|
| `vcvarsall.bat not found` when installing a package with a C extension on Windows | no precompiled wheel and no compiler | a wheel whose name (`cpNN`, `win32`/`win_amd64`) matches the Python version and bitness; compatible toolchain; alternative version | Notes p.424 | [community] | **[DATED]** (the notes point to DATED) |
| ctypes: failure to load a library raises `OSError` ("invalid ELF header", `.dll` on Linux, 64 bits on 32-bit Python); a nonexistent function raises `AttributeError` | wrong file or format | check platform and bitness; declare the `CFUNCTYPE` prototype | Notes p.745–746 | [community] | all |
| Packages installed globally with `sudo pip` | lack of isolation [inference]. The Notes, on the contrary, recommend `sudo` on Linux when there is a permission error (Notes p.421, p.55, p.713 §176.1) **[DATED]** | inside the venv pip does not need root (Notes p.709, p.713 §176.3). Avoiding `sudo pip` is the package's guidance [inference], not the book's | Notes p.55, p.421, p.709, p.713 | [community] + [inference] | all |
| `del` does not free memory; waiting for the GC to close a file or connection | `del` only removes a reference | `with` for resources | Notes p.523, p.526 | [community] | CPython |
| `pdb` names (`c`, `n`, `s`) collide with commands | reserved shortcuts | prefix with `!` | Notes p.503 | [community] | all |

---

# Part 2: Anti-patterns (what to do instead)

## 2.1 Security issues the community book shows without adequate warning

**Rule for the agent:** the book "Python Notes for Professionals" **shows** the patterns below, sometimes without a warning, sometimes with a contradictory one. It does **NOT** recommend them in a safe way, and the agent **must NOT repeat them** in generated code, even if the book's example works.

| Pattern shown | What the book says | Why not to repeat it | Do this instead | Source |
|---|---|---|---|---|
| `pickle.load` of untrusted data | Notes p.535 says loading untrusted pickle is unsafe; the Tutorial also says never to trust `pickle` from an untrusted source | deserializing can execute code [inference: the text only says it is unsafe] | a pure data format, such as JSON [inference]; `pickle` only for data you generated yourself | Notes p.535; Tut p.66 |
| `eval`/`exec`/`literal_eval` on external input | Notes p.505 states it is not possible to safely execute untrusted code, and that not even `literal_eval` is free from crashing the parser (the segfault example with `'()' * 1000000` is debatable [VERIFICAR]) | passing a custom `globals` isolates names, but is not a sandbox [inference from p.505] | do not evaluate external input; own parser, third-party module or JSON | Notes p.505–506 |
| `eval(input())` to recover Python 2's `input` | Notes p.631 suggests it; contradicts the warning on p.505 | executes whatever the user types | `ast.literal_eval` (with the caveats above) or explicit conversion (`int`, `float`) | Notes p.631 |
| `input()` that evaluates an expression | described as a code-execution risk | same | `raw_input` at the time; today the standard `input` returns `str` | Notes p.46 (**[DATED]**) |
| `random` for passwords | Notes p.318 warns it is insecure (Mersenne Twister) | predictable | the notes give **no** alternative; [inference] the standard library `secrets` module is the usual path | Notes p.318 |
| `extractall` on an untrusted archive | the book **does not warn** [VERIFICAR] | malicious archives can write outside the destination [inference] | validate member names before extracting [inference] | Notes p.585 |
| `python -m http.server` and a server with `CGIHTTPRequestHandler` | the book celebrates access from any device on the network; the log shows `0.0.0.0`; the CGI handler **executes CGI**, and the text does not warn | exposes the directory to the local network; `CGIHTTPRequestHandler` executes programs | `SimpleHTTPRequestHandler` just to serve files; care with sensitive files; port 80 requires privilege | Notes p.563–564, p.568 |
| `ctypes._Py_Dealloc` to force deallocation | the book shows it; the text acknowledges instability | can crash without a traceback | do not use in real code | Notes p.525–526 |
| Renaming a `.whl` to force installation | the book describes it as a workaround | tricks pip about compatibility | a compatible wheel or another version | Notes p.420 |
| Passwords and cryptography (salt, file hash, AES with PBKDF2) | Notes p.778 says each password needs a different salt; p.779 shows a file hash in blocks of 65536 bytes; p.781 builds AES with a key and IV derived by PBKDF2 from a password and random salt | **the notes do not record** the hash algorithm or the AES mode, so the agent cannot attest that the example is secure | do not copy cryptography recipes from the book; [inference] prefer high-level libraries and authenticated modes, and confirm in the documentation | Notes p.778–781 |

**Other unsafe examples in the community book (do not repeat):** MD5/SHA1 treated as secure algorithms (Notes p.694), SQL built by string formatting (Notes p.674, 301), AES in CFB without authentication (Notes p.779–781) and `paramiko` with `AutoAddPolicy` (Notes p.782). They are not detailed in this section; see `fontes-comunitarias.md`, section 4 (SEG-4 to SEG-7).

## 2.2 Style and robustness

The advice below complements Part 1 (where causes and full sources are). Only items the book presents problematically, or that the agent must actively avoid, are included.

- Bare `except:` or `except Exception: pass`: catch specific types, log, re-raise (Notes p.448–449, p.783; Tut p.69–70).
- `raise Outra(..., e)`: use `raise ... from e` (Notes p.449; Tut p.71–72). `return`/`break`/`continue` in `finally`: avoid; in 3.14 it produces `SyntaxWarning` (Tut p.73).
- Mutable default, `[[]] * n`, mutable class attribute: `None` with internal creation and comprehensions (Tut p.31–32; Notes p.785–786).
- `is` with literals, `== True`, `a == 1 or 2 or 3`: `==`, truthiness and `in` (Notes p.786–795).
- `from m import *`, shadowing builtins, `__import__()`: explicit names, other names, `importlib.import_module` (Tut p.50, p.56; Notes p.58, p.273).
- File without `with`, `os.linesep` in text mode, hand-written CSV line: `with ... encoding="utf-8"`, `\n`, `csv.writer` [inference from Notes p.584].
- Tail recursion by stack trick, naive Fibonacci, `setrecursionlimit` without judgment: iteration or `lru_cache`; the book itself labels tail recursion as bad practice (Notes p.440, p.443–444).
- Monkey patching, lambda assigned to a name, `float(a) / b`, `isinstance` in branches as a style: the book shows them, but itself discourages or does not recommend them (Notes p.230, p.206, p.81, p.39).
- Didactic linked list (Python 2) as a code model: use `list`/`deque` (Notes p.168–172, **[DATED]**).
- Treating type hints as validation (Tut p.139) and LBYL in concurrent code (Tut p.132): validate explicitly; prefer EAFP [inference].

---

# Part 3: Illustrative cases

1. **Closure counter (Notes p.94).** `incrementer` uses `nonlocal num`; without it, `num += 1` raises `UnboundLocalError`. Lesson: assigning to the outer variable requires a declaration; reading does not.
2. **`f(a, L=[])` (Tut p.31–32).** Successive calls return `[1]`, `[1, 2]`, `[1, 2, 3]`. Lesson: the default is born once; use `None`.
3. **`Dog.tricks` (Tut p.84–85).** All dogs learn everyone's tricks. Lesson: a list as a class variable is shared; create it in `__init__`.
4. **`bool_return()` (Tut p.73).** The `finally`'s `return` beats the `try`'s and discards the exception in flight. Lesson: no `return` in `finally`.
5. **Order of the `except` clauses (Tut p.68–69).** With the base before the derived classes, it prints B, B, B. Lesson: derived classes first.
6. **`ExceptionGroup` (Tut p.74–75).** Each `except*` extracts one type; a plain `except Exception` catches the whole group. Lesson: use `except*` to handle the members.
7. **`sum` versus `math.fsum` (Tut p.117–118).** Summing floats in a loop accumulates error; `fsum` and `Fraction` do not. Lesson: for many floats, `fsum`.
8. **`(0.1).as_integer_ratio()` (Tut p.118–119).** Gives `(3602879701896397, 36028797018963968)`. Lesson: the float stores a fraction whose denominator is a power of 2.
9. **`groupby` without sorting (Notes p.165–167).** Groups with the same key show up separately; when turned into a dict, the last one overwrites. The review note says the loss comes from the dict, not from `groupby`. Lesson: sort by the same key and use `list(group)`.
10. **`shelve` without `writeback` (Notes p.732–733).** `d['xx'].append(3)` does not persist. Lesson: reassign the mutated copy or use `writeback=True`.
11. **pytz (Notes p.66–67).** Attaching the zone through the constructor is wrong; `tz.localize(...)` and, after adding a `timedelta`, `normalize`. Lesson: read the timezone library's rule.
12. **`strip('abc')` (Notes p.259).** Removes any of those characters from the ends, not the prefix. Lesson: a literal prefix calls for `startswith` plus a slice.
13. **Accents (Notes p.265–266).** Strings that look equal can differ in Unicode; `casefold` plus NFKD solves it. Lesson: normalize before comparing.
14. **GIL in numbers (Notes p.543–544).** Same CPU-bound task: 4 threads much slower than 1 run, 4 processes close (values from the author's machine). Lesson: threads do not speed up CPU work in CPython.
15. **`asyncio` with `requests` (Notes p.316–317).** The blocking call freezes the loop. Lesson: use asynchronous libraries.
16. **1024 buffer (Notes p.555).** Larger JSON is truncated: `ValueError: Unterminated string`. Lesson: delimit the network message.
17. **`eval` with custom globals (Notes p.506).** A `defaultdict(int)` makes undefined names evaluate to 0. Lesson: it isolates names, it does not protect (see 2.1).
18. **Pickle and the constructor (Notes p.528–529).** `__init__` does not run on deserialization; `__setstate__` recreates the state. Lesson: initialize there what the constructor would initialize.
19. **Cooperative mixin (Notes p.617–618).** Plugins that call `super().test()` chain together. Lesson: in multiple inheritance everyone calls `super()`.
20. **`match` and capture (Tut p.28–29).** A simple name in a `case` becomes a variable and always matches; `Color.RED` compares the value. Lesson: constants need a dotted name.

---

# Appendix A: Errors in the book itself (do not reproduce)

The items below are **wrong** examples in "Python Notes for Professionals". The agent must not copy them; the corrections come from the intermediate notes.

**Marked as [BUG-FONTE] in the notes**

| Where | Error | Correction indicated | Source |
|---|---|---|---|
| Serialization with pickle (ch. 115) | files opened with `'w'`/`'r'` (text) and `pickle.dump(families, ...)` serializes the wrong variable (`families` instead of `my_family`) | binary mode and the right variable | Notes p.535 |
| `csv_writer` | opens with `"wb"` (Python 2 mode) **[DATED]** | text mode `'w'`; section 105.2 uses `'wt'` with `delimiter='\t'`; the text does not mention `newline=''` [VERIFICAR] | Notes p.584, p.504 |
| `append_to_csv(input_string)` | uses `input_row`, a nonexistent name; writes the line by hand, without `csv` quoting | use `csv.writer` | Notes p.584 |
| Thread `join` example | `Thread(target=requests.get, args=(page_num,))` instead of `put_page_to_q`; missing parenthesis in `q.put(`; claims `join` accepts `blocking=False` (the parameter is `timeout`) [VERIFICAR] | fix the target and the parenthesis; use `timeout` | Notes p.538–539 |
| `StoppableThread` | `def run()` without `:` and `print("stopped!"` not closed | correct syntax | Notes p.542 |
| `threading` example | defines `counter` but uses `countdown` | unify the name | Notes p.548 |
| GIL example | `with multiprocessing.Pool as pool` (without parentheses); `COUNT/2` is a float in Python 3; `print end-start` is Python 2 **[DATED]** | `Pool()`, integer division, `print(...)` | Notes p.591 |
| Socket client server | Python 2 `print`; received `name` (`bytes`) used as a key and in `json.dumps`; `conn.sendall(json.dumps(...))` requires bytes | decode/encode | Notes p.554 |
| "Simplest client-server" | sends `'hello'` as `str`; fails in Python 3 [PY2] | `b'hello'` | Notes p.565 |
| `BaseHTTPRequestHandler` | `self.wfile.write("...")` with `str`; `self.headers.getheader(...)` is the Python 2 API **[DATED]**; port 80 requires privilege | bytes and `.get` | Notes p.568 |
| `DescPrinter` and `Hertz` | store the value in the descriptor itself, a class object shared by all instances | store in `obj.__dict__` or a per-instance dict | Notes p.579–580 |
| `Oscillator.__init__` | `self.freq = Hertz()` (instance attribute); descriptors only work as a class attribute | `freq = Hertz()` in the class body | Notes p.580 |
| `@property author` | the setter does `self.author = ...`, recursion in the setter itself; the getter returns `self.__author`; the previous example calls `self.setAuthor` but defines `set_author` | store in `self._author`; consistent names | Notes p.612–613 |
| ABC | `__metaclass__ = ABCMeta` (Python 2) **[DATED]**; `@abstractmethod` without the import; in the second example `punchline` is outside the class | `abc.ABC`, import, indent | Notes p.615–616 |
| `checkParenth` | returns `not stack.isEmpty()`, True when openings remain; rejects any character that is not a parenthesis | `stack.isEmpty()` | Notes p.590 |
| `CustomSwitcher` | does not inherit from `SwitchBase` | inherit | Notes p.602 |
| Switch with `case(1), case(2), case(3)` | the text's result "42" does not match the defined cases | (inconsistency) | Notes p.603 |
| ZIP | `zip[0].filename` where it should be `info[0]`; `print(zip)` inside `with ... as z` | fix the names | Notes p.586–587 |
| `open('arquivo', 'shift_jis')` | passes the encoding as the mode | `encoding='shift_jis'` | Notes p.640 |

**Errors pointed out in the notes without the [BUG-FONTE] tag**

| Where | Error | Source |
|---|---|---|
| Server with `socketserver` | typos: `from sockerserver import ...` (p.563), `sick.sendto` (p.564), `def handle` with an unindented body (p.564), use of `os` without import and an unclosed parenthesis in `Thread(...)` (p.564–565) | Notes p.563–565 |
| `partial` (p.218) | the idea (`partial(func, y=3)`) is valid, but the book's code has errors | Notes p.218 |
| `__exit__(self)` (p.409) | without the three protocol arguments [VERIFICAR] | Notes p.409 |
| `os.access` (p.414) | combines flags with `&`; the fix indicated is to use the bitwise "or" operator [VERIFICAR] | Notes p.414 |
| `raise NotImplemented` (p.491) | the correct one is `NotImplementedError` [VERIFICAR] | Notes p.491 |
| List as a default in recursion `lst=[]` (p.441) | the book does not comment on the risk; fix `lst=None` [verifiable inference] | Notes p.441 |
| Linked list (Ch. 24–25) | all the code is Python 2 **[DATED]**; didactic, do not use as a model | Notes p.168–172 |
| `print` and `struct` examples | use Python 2 `print` [PY2] **[DATED]** | Notes p.530–531 |
| `groupby` (p.166–167) | the book attributes the loss of groups to `groupby`, but the real cause is the dict overwriting repeated keys | Notes p.166–167 |
| Ch. 2, variables `list` and `tuple` | shadow builtins | Notes p.58 |

---

# Appendix B: Internal contradictions and items to verify

- **MRO:** p.611 says right to left, p.617 says left to right; follow left to right [VERIFICAR] (Notes p.611, p.617).
- **`__import__`:** forbidden on p.273 and shown on p.275; follow `importlib`.
- **`eval`:** p.505 warns; p.631 suggests `eval(input())`. Follow the warning.
- **`dict` order:** the book treats the 3.6 ordering as an implementation detail (Notes p.793–794); the notes do not carry the guarantee of newer versions, consult the documentation. The same applies to key order in `json.dumps` (Notes p.298).
- **Marked [VERIFICAR] by the notes:** `\10` in `re.sub` (p.401), `empty()` between threads (p.548–549), `join(blocking=False)` (p.538–539), Cython's `nogil` (p.592), `extractall` and `tarfile.TarFile` for `.tar.gz` (p.585), explanation of `property` through "decorators" (p.613), integer identity (p.523).
- **The book's micro-benchmarks** (Notes p.770–771): values from an old machine, order of magnitude only.

# Appendix C: Gaps in this base

- **Language Reference** only in a few items (1.2 `lambda` in a loop; 1.4 loop variable and comprehension); the rest was not cross-checked against it.
- **Security:** MD5/SHA1, SQL with `%s`, AES without authentication and `paramiko` with `AutoAddPolicy` do not appear in the notes (see 2.1).
- **Python 3.14:** the only version-specific mark recorded is the PEP 765 `SyntaxWarning` in `finally` (Tut p.73); in the other pitfalls the "Version" column says "all".
- **Error messages:** only those cited in the notes; for others, reproduce the error before quoting the text.
