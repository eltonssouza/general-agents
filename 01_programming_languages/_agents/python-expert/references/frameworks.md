# Decision frameworks for Python: principles, mental models and decision trees

Reference base of the Python specialist agent. Derived from three PDFs: *The Python Tutorial* 3.14.0rc3 (**Tut**), *The Python Language Reference* 3.14.0rc3 (**Ref**) and *Python Notes for Professionals* (**Notes**, a community book that mixes Python 2 and 3).

## Contents

0. How to use this file (labels and precedence)
1. Fundamental mental models
2. Choosing a data structure
3. Mutability, aliasing and copying
4. Functions and arguments
5. Scope: global and nonlocal
6. Comparisons, identity and truthiness
7. Iteration: loops, comprehensions, generators
8. Strings, bytes, formatting and files
9. Exceptions
10. Classes and the data model
11. Modules and packages
12. Concurrency
13. Numbers and floating point
14. Choosing a tool in the standard library
15. "Pythonic" idioms from the Notes (quick list)
16. Register of divergences and dated items
17. Known gaps of this base

---

## 0. How to use this file

**Origin labels.** **[official]** = Tut or Ref. **[community]** = Notes. **[inference]** = a link made by whoever compiled this base, not stated literally by any source. **[DIVERGES]** = the Notes contradict an official source; the official one prevails. **[DATED]** = holds for Python 2 or for old versions of 3, or the book predates a new feature.

**Format of each item:** principle (the why), "If X → Y" rule, trade-off, source `(Tut p.N)` / `(Ref p.N)` / `(Notes p.N)`.

**Precedence:** official > community. Where the Notes agree with the official source, the item gets both labels. Where only the Notes speak, the item is the opinion of a community book and must be presented as such.

**Scope note:** the origin notes of this base brought citations from the Tut and the Notes; there is no Ref citation in this entry. Details of the language contract (for example `__hash__`/`__eq__`, descriptors, exact MRO) must be checked in the Ref before asserting with certainty.

---

## 1. Fundamental mental models

1. **Names bind to objects; assignment never copies.** Explains shared lists, argument passing and accumulation in mutable defaults (Tut p.19, p.30, p.31–32, p.79–80). **[official]**
2. **Mutable × immutable decides a lot.** `str` and tuple do not change in place; dict keys must be hashable, which follows from immutability (or from identity, in user classes) (Tut p.18, p.44–45, p.130). **[official]**
3. **Methods that mutate in place return `None`.** For a new sorted/reversed collection, use `sorted`/`reversed` (Tut p.40, p.46–47); `list.sort()` and `shuffle` follow the same rule (Notes p.138–139, p.150, p.319–320). **[official]** + **[community]**
4. **Iterable is the contract.** `range`, `zip`, `enumerate`, `dict.items()` serve `for`, `sum`, `list`. Iterable = something you can get an iterator from; an iterator is a single-pass stream; containers regenerate iterators, iterators do not (Tut p.25, p.131–132). **[official]**
5. **Syntax is sugar over protocols.** `for` uses `iter()`/`next()` until `StopIteration` (Tut p.89); `with`, decorators, slicing and descriptors do too (Tut p.126, p.127, p.131). **[official]**
6. **`def` and `class` are executed statements.** Parameter defaults are evaluated at `def` time (Tut p.30–31, p.50); a class is an object created at run time, modifiable afterwards (Tut p.79, p.82). **[official]**
7. **Scope: determined textually, looked up dynamically.** The global of a function is the module where it was defined (Tut p.80). Local variables are resolved at compile time (Tut p.134). **[official]**
8. **Privacy is convention.** A leading underscore = non-public, subject to change without notice (Tut p.85, p.87). **[official]**
9. **CPython details are not part of the language contract** (reference counting, immortals, bytecode, GIL): portable code must not depend on them (Tut p.125, p.131, p.137). **[official]**
10. **API guarantee levels:** stable, provisional, "soft deprecated". Do not use "soft deprecated" in new code, but there is no urgency to migrate existing code (Tut p.136–138). **[official]**
11. **Typing:** duck typing by default; ABCs when probing attributes is fragile; type hints are optional and not enforced at run time (Tut p.123, p.128, p.139). **[official]**

---

## 2. Choosing a data structure

**Principle:** choose the structure by the dominant operation (lookup by key, membership test, keeping order, taking from the end) and by the mutability needed.

```
What do I need to store?
├─ Key -> value pairs .................................. dict
│   ├─ read without changing ...... d.get(k, default)
│   ├─ read and store the default . d.setdefault(k, default)
│   └─ accumulate lists/counters many times .. defaultdict(list|int)
├─ Only uniqueness / fast membership ................... set
│   └─ empty set: set()   (never {})
├─ Count the frequency of all items .................... Counter
├─ Sequence
│   ├─ changes, homogeneous, walked in a loop ... list
│   ├─ fixed, heterogeneous (record), or dict key/set item ... tuple
│   ├─ FIFO / window of the last N ........... collections.deque (maxlen=N)
│   ├─ sorted, with lookups ................... list + bisect
│   ├─ smallest/largest N without sorting all . heapq
│   └─ compact homogeneous numeric data ....... array
└─ Record with named fields ............................ @dataclass
```

**Rules and trade-offs**

- **list** is a natural stack (the end); inserting/removing at the start is slow, so FIFO → `deque` (Tut p.40–41, p.103–104; Notes p.292, p.335). `list.pop(0)` and `insert(0, v)` cost O(n) (Notes p.292). **[official]** + **[community]**
- **deque:** access to the middle is slow; `append`/`popleft` are fast (Tut p.103–104). `queue.Queue` serves communication between threads; for BFS and ordinary queues use `deque` (Notes p.333, p.335). **[official]** + **[community]**
- **tuple × list:** tuple for heterogeneous items of fixed structure (access by unpacking/index); list for homogeneous items in a loop (Tut p.44). A tuple is a dict key/set item only if all its elements are hashable; a tuple with a mutable element is not (Tut p.130; Notes p.179, p.181–182). The Notes cite IP and port as an example of a tuple (Notes p.42–43). **[official]**
- **tuple with `+=`:** works (new tuple), but is slow and bad practice when repeated; convert to a list, append and convert back (Notes p.179). **[community]**
- **set:** for uniqueness and membership faster than a list at large volumes (Notes p.42–43, p.143). If there are many `in` tests over a large list, convert it to a set first (Notes p.143). Trade-off: no order (Notes p.76). **[community]**
- **Deduplicating:** `list(set(x))` loses the order; the Notes suggest `OrderedDict.fromkeys(...)` to preserve it (Notes p.76, p.145–146). **[community]** **[DATED]** (the `OrderedDict` suggestion for ordering is flagged as dated in the origin notes; check in the Ref whether `dict` already guarantees insertion order).
- **Set operations:** `&`, `|`, `-`, `^`, `<=`, `>=` are equivalent to `intersection`, `union`, `difference`, `symmetric_difference`, `issubset`, `issuperset`; in-place versions (`|=`, `update`...) mutate. For disjointness, `isdisjoint` is more efficient than `len(a & b) == 0` (Notes p.75, p.77–78). `set.remove` raises `KeyError` if missing; `discard` does not (Notes p.75). **[community]**
- **dict, sort by value:** sort `d.items()` with `key=itemgetter(1)`; sorting `d` directly sorts only the keys (Notes p.386–387). **[community]**
- **dict, merge:** `{**a, **b}` (last wins, does not mutate), `a.update(b)` (last wins, mutates `a`), `ChainMap` (the first wins) (Notes p.131, p.155). Preferable according to the Notes: `{**d1, **d2}` (PEP 448). **[community]**
- **dict, invert:** `{v: k for k, v in d.items()}`; duplicate values give an unexpected result (Notes p.155). **[community]**
- **`d[k]` × `get` × `setdefault` × `defaultdict`:** `get` reads without changing; `setdefault` reads and stores, but creates a new instance of the initial value on every call (matters at volume); `defaultdict` when you will accumulate many times (Notes p.129–131). `in` followed by access has a race window in multithreading (Notes p.129; Tut p.128, p.132). **[community]** + **[official]** (race)
- **Frequency × count:** one item or substring → `.count()`; full distribution → `Counter`; substring of more than one character → only `str.count()` (Notes p.390–391). **[community]**
- **Top-N:** `heapq.nlargest/nsmallest` when n is small relative to the total; `sorted` to sort everything (Notes p.388–389; Tut p.103–104 on `heapq`). **[community]** + **[official]**
- **Search in a large sorted sequence:** `bisect_left` with an equality check; the Notes measure a ~500x gain for an element in the middle/end, but it is slightly slower if the element is among the first ones (Notes p.382). **[community]**
- **Struct-style record:** `@dataclass` is called the idiomatic approach by the tutorial (Tut p.88). The Notes (in the origin notes) do not cover dataclass. **[official]**
- **Simple persisted data:** `pickle` for one object; `shelve` for dictionary-style access by key (Notes p.687, p.731). **[community]**

---

## 3. Mutability, aliasing and copying

**Principle:** since assignment binds (does not copy), two names can point to the same mutable object; the effect shows up for whoever changes it through one of the names (Tut p.79–80). **[official]**

```
Do I need a "copy" of a collection?
├─ Just another name for the same object ....... b = a   (aliasing, intentional)
├─ Flat container of immutables ................ shallow copy: a[:] | list(a) | a.copy() | copy.copy(a)
│     (copy.copy is slower: it discovers the type)
└─ Nested with mutables modified
   independently ............................. copy.deepcopy(a)   (slower, more memory)
```
Sources: Notes p.140, p.406; Tut p.23–24 (`.copy()` when iterating). **[community]** + **[official]**

**Rules**

- **List of independent lists:** `[[] for _ in range(n)]`; `[[]] * n` creates n references to the same object (Notes p.700, p.785). Initializing with N immutables: `[None] * n`; with mutables, a comprehension (Notes p.147–148). **[community]**
- **Mutable default in a parameter:** the default is evaluated once, at `def`, and accumulates across calls (Tut p.30–32). Fix: `None` as a sentinel and create inside (`if to is None: to = []`) (Notes p.207–208, p.789). Test with `is None`, not `if not li`, because `[]`, `""`, `0` are also falsy and trigger an unwanted replacement (Notes p.789). **[official]** + **[community]**
- **A mutable attribute on the class is shared** by all instances; per-instance data goes in `self.x` in `__init__` (Tut p.84; Notes p.237, p.788). **[official]** + **[community]**
- **Does the function change the argument or return a new structure?** Decide explicitly; if it changes in place, the `return` is superfluous and confusing (Notes p.700–701). `+=` on `str` does not affect the caller because `str` is immutable (Notes p.700–701). **[community]**
- **The loop variable does not change the list:** `item = 'even'` only rebinds the name; use `lst[i] = ...` with `enumerate` (Notes p.790–791). **[community]**
- **Modifying during iteration:** iterate over a copy or build a new collection (Tut p.23–24, p.47–48). Variants from the Notes: filter with a comprehension; iterate backwards; `while lista: pop` if you will empty almost everything (Notes p.790–792). **[official]** + **[community]**
- **Concatenating `str` in a loop with `+=`** creates a new object at every step; the Notes measure `"".join(lista)` as much faster (570 µs vs 16.1 µs) (Notes p.699, p.770). Trade-off: the benchmark is the book's data, not a general guarantee. **[community]**
- **Flattening a list of lists:** `[x for sub in l for x in sub]`; shortcuts with `+` (`sum(l, [])`, `reduce`) are O(L²) because they re-copy the partial result (Notes p.153–154). **[community]**
- **Reversing:** `reversed(x)` (iterator, does not change), `x.reverse()` (in place), `x[::-1]` (copy) (Notes p.144). **[community]**
- **Removing from a list:** `remove(v)` deletes the first occurrence and raises `ValueError` if absent; `pop(i)` removes and returns (default: the last); `del a[i]`/`del a[slice]` accepts slices with a step (Notes p.137, p.140). **[community]**
- **`append` × `extend` × `+`:** `append` adds ONE element (an appended list becomes nested); `extend` adds the items of any iterable; `+` creates a new list (Notes p.136–137). **[community]**

---

## 4. Functions and arguments

**Principle:** the signature is a contract; the positional-only (`/`) and keyword-only (`*`) syntax exists to fix the calling form (Tut p.35–36, p.135).

```
How do I declare each parameter?
├─ name does not matter / I want to enforce order / I want to be able to rename later
│     without breaking the API ............... positional-only  (before "/")
├─ names add clarity / avoid depending on position
│     ................................................ keyword-only    (after "*")
│     └─ no default => required (Notes p.521)
├─ variable number of positionals ........... *args
├─ variable number of keywords .............. **kwargs  (kwargs.get('v', 0) for a default)
└─ mutable default? ......................... None + create inside (section 3)
```
Sources: Tut p.35–36, p.135 **[official]**; Notes p.203, p.210, p.521–522 **[community]**.

**Rules**

- **A bare `*`** forces what comes after it to be keyword-only: `def f(a, b, *, c)` (Notes p.210). Use it when the order of the arguments would be confusing (Notes p.203). **[community]** (Python 3)
- **`*args`/`**kwargs`:** any name works, but follow the convention (Notes p.203). To pass optional arguments along, re-expand with `*args, **kwargs`; without the prefixes it would pass a tuple/dict as a single argument (Notes p.203, p.607). `zip(*zipped)` undoes a `zip` (Notes p.522). `f(**d)` unpacks a dict into keywords (Notes p.133–134). **[community]**
- **`*args` × list as a parameter:** if you already have the list, a plain parameter receives the list; `*args` serves calls with a variable number of arguments; `func(*lista)` expands at the call (Notes p.202, p.216). **[community]**
- **Argument passing** is by "object reference": mutations inside the function are seen by the caller (Tut p.30, p.80). **[official]**
- **`def` × named `lambda`:** prefer `def`; it gives a useful name in tracebacks (Notes p.206, citing PEP 8). **[community]**
- **`key=`:** pass a key function (lambda, `str.lower`, `operator.itemgetter`) instead of pre-processing data (Tut p.132). `itemgetter`/`attrgetter`/`methodcaller` are more readable and reusable; the Notes state that they are faster than lambda, with no measurement presented (Notes p.138–139, p.295–296, p.387). `key=itemgetter(1, 0)` sorts by multiple keys (Notes p.295). **[official]** + **[community]**
- **Fixing arguments:** `functools.partial` instead of lambda (Notes p.323, p.368). **[community]**
- **Memoization:** `@lru_cache(maxsize=None)` for expensive/recursive pure functions (Notes p.323–324). **[community]**
- **Decorators:** inner wrapper `(*args, **kwargs)`: pre-processes, calls the original, handles the return (Notes p.219–220); use `functools.wraps(func)` to preserve `__name__`, docstring, annotations and module (Notes p.223); with arguments there are three levels (factory → decorator → wrapper) (Notes p.222). A decorator function is the default; a decorator class changes the object's type, requires `__get__` to decorate methods and shares state between instances when decorating a method (Notes p.220–221). **[community]**
- **Recursion × iteration:** recursion "not often"; every recursive function becomes iterative; acceptable with few calls or naturally recursive structures (trees of unknown depth) (Notes p.440–441). Raising `setrecursionlimit` consumes more memory; prefer iteration or `lru_cache` (Notes p.440, p.443). **[community]**
- **Returning different types** is allowed, but the caller must handle it (Notes p.201). **[community]**
- **Docstrings:** PEP 257 defines what to say, not the format; one line for simple functions, imperative, ending with a period. Formats: Sphinx/reST or Google style (Notes p.63–64). A docstring is worth more than a `#` comment: in the latter case `__doc__` stays `None` and `help()` loses the text (Notes p.62). **[community]**
- **Type hints:** annotate the return of `__init__` as `None`, do not annotate `self`/`cls`, use a string for self-reference (Notes p.447); `x: int` syntax from 3.6 on, the `# type:` comment only for compatibility (Notes p.446). For long types, use an alias (Tut p.139). To read annotations at run time: `annotationlib.get_annotations()` or `typing.get_type_hints()`, knowing that locals are not accessible (Tut p.139). Hints do not validate at run time (Tut p.123, p.139). **[official]** + **[community]**
- **Paths:** accept path-like objects and normalize with `os.fspath()`/`os.fsdecode()`/`os.fsencode()` (Tut p.135). **[official]**

---

## 5. Scope: global and nonlocal

**Principle:** name lookup in a function follows local → enclosing → global → built-ins (Tut p.30). Reading an outer variable is free; **writing requires** a declaration (Tut p.126, p.134). **[official]**

```
Do I need to change a name that is not local?
├─ It is in an enclosing function ..... nonlocal name
├─ It is in the module ................. global name
└─ Can it be avoided? ................. [inference] return a value / use an explicit mutable object / class
```

- Every assignment, `import`, `def` and `del` operates in the innermost scope, except for `global`/`nonlocal` (Tut p.80). **[official]**
- The global scope of a function is that of the module that defined it, not that of the caller (Tut p.80). **[official]**
- The tutorial warns that the language is evolving toward static name resolution: do not depend on dynamic resolution (Tut p.80). **[official]**
- A comprehension does not leave the loop variable in the outer scope, unlike a `for` loop with `append` (Tut p.41). **[official]**
- A `lambda`/`def` created in a loop resolves free variables at run time and sees the last value of the loop. The rule (free variables are resolved at run time, with an example where `f()` prints the current value of `i`) is in Ref p.78 **[official]**; the application to the loop is [inference]. Fixes: a function factory, which fixes the value in the scope of the outer function (Tut p.36, `make_incrementor`) **[official]**; the default value `lambda i=i: ...`, which relies on the default being evaluated once, at definition (Tut p.31; Ref p.140) **[official for the mechanism]**, whereas the `i=i` pattern itself does not appear in the text [inference]. Note: the text does not include this example nor the term "late binding".
- Forgetting to indent/dedent changes the logic without an error: a `return False` indented too far inside the `if` makes the function return `None` (Notes p.60). **[community]**
- `break`/`continue` act only on the innermost loop; to leave several levels, refactor into a function and use `return` (Notes p.112). **[community]**

---

## 6. Comparisons, identity and truthiness

**Principle:** `==` compares value; `is` compares identity (`id(a) == id(b)`). The identity of small ints and strings is an artifact of the environment (Notes p.107). **[community]** (consistent with Tut p.125, p.131 on implementation details **[official]** [inference])

```
Do I need to compare?
├─ with None / True / False (singletons) .... is / is not
├─ with a sentinel (object()) ............... is
├─ numbers, strings, collections ............ ==   (never is)
├─ "has a value?" and 0, '', [] are invalid . if x:
├─ "has a value?" and 0, '' are VALID ....... if x is None:
├─ equal to one of several values ........... x in (1, 2, 3)   or any(...)
└─ range .................................... a < x < b   (chained)
```

- **Falsy:** `None`, `False`, numeric zeros (`0`, `0.0`, `0j`), empty sequences (`''`, `()`, `[]`), empty mappings (`{}`), objects whose `__bool__`/`__len__` returns false; everything else is truthy (Notes p.101–102). **[community]**
- **Implicit test:** prefer `if attr:` over comparing with `1`, `True` or `''`; for None use `is None` (Notes p.532–533). `== True` matches 1 and 1.0, `== False` matches 0 (Notes p.786–787). Empty list: `if not lst:` instead of `len(lst) == 0` (Notes p.142). **[community]**
- **Internal tension in the Notes:** the text says that the implicit test is "safer" with unexpected types (Notes p.533), but other passages show that `x or default` and `if x:` also replace/reject `0`, `''`, `[]` (Notes p.102, p.104–105, p.789). Safe rule: if those values are legitimate, compare explicitly with `None`.
- **Default value for None:** `x = x or default` is short but replaces `0`, `''`, `[]`; use `if x is None` if they are valid (Notes p.104–105). **[community]**
- **`and`/`or` return one of the operands** and short-circuit: `a or b` → `a` if truthy; `a and b` → `a` if falsy (Notes p.90–92, p.102). `reduce(or_/and_)` does not short-circuit; prefer `any/all` (Notes p.366). **[community]**
- **Classic error:** `if a == 1 or 2 or 3` and `if a or b or c == 3` do not test what they appear to (Notes p.794–795). **[community]**
- **Chaining:** `3.14 < x < 3.142` is equivalent to `and`, with the middle expression evaluated once; it short-circuits at the first false. Prefer the "directional" style; avoid elaborate chaining (Notes p.90, p.106). **[community]**
- **Ternary:** `v1 if cond else v2`; the order differs from C/Java and is a source of bugs; only for short cases (Notes p.101). Chain: `if/elif/else`; `else if` is a syntax error (Notes p.101). **[community]**
- **`if/elif` × `match`:** `if/elif` for general conditions; `match` to compare a value with several constants, check types/attributes/structure and extract components (Tut p.23, p.27). **[official]**. The Notes (predating 3.10) do not mention `match`: for dispatch they list `if/elif`, a dict of functions, `getattr` and a context manager (Notes p.600–603). **[DATED]** — see the switch tree in section 14.
- **Assignment in an expression:** only with `:=`, by design against `=`/`==` confusion (Tut p.48). **[official]**
- **Comparing floats:** `math.isclose()` (Tut p.116); see section 13. **[official]**
- **Hashability** (used in dict/set): check before asserting that an object works as a key (Tut p.130). The exact contract of `__hash__`/`__eq__` is not in this entry: consult the Ref. For ordering, `functools.total_ordering` requires equality and one ordering operator (Notes p.324, p.385). **[official]** (hashability) + **[community]** (`total_ordering`)

---

## 7. Iteration: loops, comprehensions, generators

**Principle:** iterate directly over the iterable (`for x in food`); indexes only when needed, via `enumerate` (Tut p.24, p.46, p.136). **[official]**

```
Do I need to walk through?
├─ elements .......................... for x in seq
├─ index + element ................... for i, x in enumerate(seq)       (never range(len(seq)))
├─ two+ sequences in parallel ........ zip (stops at the shortest) | itertools.zip_longest
├─ subset with a step ................ seq[1::2] | range(start, len, step)
├─ keys | pairs | values ............. for k in d | d.items() | d.values()
├─ do I need to change the collection? . see section 3 (copy / new collection)
└─ leave nested loops ................ function + return
```
Sources: Tut p.24, p.46, p.136 **[official]**; Notes p.114, p.119–120, p.117, p.129–130, p.142–145, p.786 **[community]**.

**for/else and while/else**

- The `else` runs when the loop ends **without `break`** (and without an exception). Read it as "not found"; the main use is search (Notes p.114–116). **[community]**
- There is no do-while: `while True:` with `break` at the end of the body (Notes p.118). **[community]**
- An empty block requires `pass` (Notes p.35, p.116). **[community]**
- Unpacking in `for`: `for a, b in items`; requires the same number of items on both sides, otherwise `ValueError`; `_` for discarded ones (Notes p.33, p.118–119). **[community]**

**Comprehension × loop × map/filter**

```
Am I building a collection from another?
├─ simple expression, no side effect ........ comprehension
│     └─ double for: same order as the spelled-out loops (outer first)
├─ side effect (print, sort(), I/O) ......... plain for
├─ complex logic or > 2 levels .............. plain for or generator function
├─ existing named function .................. map(f, xs) is acceptable
├─ transposed matrix ........................ zip(*matrix)  (Tut) instead of a nested comprehension
└─ expensive f(x) used in the value and the filter .. inner generator, map, for v in [f(x)], or lru_cache
```
Sources: Tut p.41, p.43 **[official]**; Notes p.150–156, p.159–160, p.162 **[community]**.

- A comprehension is more concise and readable than `append` in a loop and than `list(map(lambda...))` (Tut p.41). `map(F, S)` → `[F(x) for x in S]`; `filter(P, S)` → `[x for x in S if P(x)]` (Notes p.159–160). **[official]** + **[community]**
- Do not use a comprehension for side effects (`[print(x) for x in ...]`, `[x.sort() for ...]`) (Notes p.150–151). **[community]**
- Prefer a comprehension over `map(...)` for portability and readability (Notes p.639); `list(map(...))` removes the Py2/Py3 difference (Notes p.367). **[community]** **[DATED]** (the portability motivation is Python 2)
- `filter(None, xs)` discards falsy values; `next(filter(pred, xs))` finds the first one that satisfies and stops; `filterfalse` is the complement (Notes p.173–174). **[community]**
- Counting: `sum(1 for x in it if cond)` — a generator, no intermediate list (Notes p.160–161). Batch conversion: `[int(s) for s in items]` or `map` (Notes p.161). **[community]**
- `sort()` returns None; `sorted()` returns a new list (use inside expressions) (Notes p.150–151). **[community]**

**List × generator**

```
The values will be...
├─ indexed, reused, or expensive to generate .. list (store)
├─ iterated once / large volume / infinite .... generator (expression or function)
├─ consumed right away by sum/max/set/list .... generator expression
├─ only the first one that satisfies is needed . generator + next(..., default)
└─ generator too large to store ............... recreate the generator when needed again
```
Sources: Tut p.90–91 **[official]**; Notes p.149, p.156–158, p.356–358, p.363 **[community]**.

- A generator creates `__iter__`/`__next__`, keeps state in locals and raises `StopIteration` when it finishes; anything a generator does, a class-based iterator does, but the generator is more concise (Tut p.89–90). **[official]**
- Generator expression: more compact, less versatile, tends to save memory (Tut p.90–91). As the only argument it dispenses with double parentheses: `sum(i*i for i in r)` (Notes p.356, p.363). **[official]** + **[community]**
- Turning a function that accumulates into a list into one that yields values: replace `append` with `yield`; if recursive, `yield from` (Notes p.361–362). **[community]**
- A generator is not subscriptable (`TypeError`); slice with `itertools.islice(gen, n)` (Notes p.307–308). **[community]**
- `groupby` requires sorting by the same key beforehand (Notes p.308). `reduce` with an initializer applies the function first to it and to the first element (Notes p.365–366). **[community]**
- `range` produces items on demand (Tut p.25). **[official]**

---

## 8. Strings, bytes, formatting and files

**Principle:** text goes through encoding and line-ending conversion; binary does not. Choose the mode according to the content (Tut p.63, p.125, p.138). **[official]**

**Formatting tree**

```
Build text with values?
├─ embed expressions ..................... f-string  (first option in Tut p.59)
│     └─ quick debugging: f'{var=}'  (Tut p.61)
├─ separate data / position / name / dict ... str.format() ; format_map(d) for a dict
├─ manual layout ......................... ljust / rjust / center / zfill
├─ placeholders editable by the end user .. string.Template  ($x)
└─ % style  .............................. legacy only
```
- Tut: f-strings first; `str.format()` with reference by position/name and `**table`; `%` only mentioned (Tut p.59, p.61–63); `Template` for end users or to separate logic from format (Tut p.100–101). **[official]**
- Notes (formatting section): f-string (3.6+) > `.format` > `%`, with `format_map` (3.2+) for dicts (Notes p.247, p.249–250). **[community]**
- **Partial divergence:** another passage of the Notes treats `str.format` and f-strings as equivalent and says it prefers `.format` over `%` (Notes p.257). The tutorial, which prevails, puts f-strings as the first option. **[DIVERGES]**
- Literal braces: double them `{{`/`}}`; dynamic widths via nested formatting `{:>{}}`; number the fields to repeat a value (`{0}`) (Notes p.252, p.257). **[community]**
- `str()` for human display; `repr()` for debugging/recognizable output (Tut p.59–60). In classes: only `__repr__` if both forms coincide; `__str__` only if you want a different friendly form (Notes p.499–500). **[official]** + **[community]**
- `ljust/rjust/center` do not truncate; to truncate `x.ljust(n)[:n]`; `zfill` respects signs and does not truncate (Tut p.62–63). **[official]**

**String operations tree**

```
├─ compare ignoring case ..... casefold (3.3+), never just lower;  with accents: normalize("NFKD", ...) first
│                              lower is fine for display  (Notes p.265–266)
├─ "empty or only whitespace" . not s.strip()   (isspace() gives False for '')  (Notes p.263–264)
├─ join a list ............... sep.join(lista)   (the separator calls join)    (Notes p.264)
├─ contains? ................. "x" in s   ("" in s is always True)             (Notes p.264)
├─ several prefixes/suffixes . startswith/endswith with a tuple                 (Notes p.267)
├─ find position ............. index/rindex (ValueError) vs find/rfind (-1)  (Notes p.380)
├─ reverse ................... s[::-1] (concise) or ''.join(reversed(s)) (readable) (Notes p.260, p.343)
├─ complex matching .......... re ;  simple => string methods (more readable) (Tut p.94)
└─ concatenate in a loop ..... avoid += ; use join                         (Notes p.699, p.770)
```
Label: **[community]**, except the `re` × string methods rule, which is **[official]** (Tut p.94).

**Regex (Notes p.398–405) [community]:** always a raw string; `re.escape` when interpolating user text; `re.compile` if reusing; `match` (start) × `search` (any position) × `findall` (strings) × `finditer` (positions/match object); named groups for readability; `(?:...)` when the group only groups (Notes p.403).

**Files tree**

```
Open a file?
├─ always: with open(...) as f   (closes even with an exception; without with/close the write may not reach the disk)
├─ text   -> explicit encoding="utf-8" (the default depends on the platform)
│            JSON: UTF-8 mandatory, encoding on both ends
├─ binary ('b'): JPEG, EXE and the like; no encoding; text would corrupt
├─ large file -> for line in f  (not read() without a size, not readlines())
├─ exists? -> EAFP: try to open and handle OSError
├─ modes: r (must exist) | w (creates/erases) | a | r+ (without erasing) | w+ (erases) | x (fails if it exists)
└─ writing a non-string: convert first (str in text, bytes in binary)
```
Sources: Tut p.63–66 **[official]**; Notes p.183–184, p.188–193, p.654 **[community]**.

- `readline()` returns `''` at the end, whereas a blank line is `'\n'` (Tut p.64). `write` returns the number of characters (Tut p.64–65). `list(f)`/`readlines()` only if you want all of them in a list (Tut p.64). **[official]**
- Text mode: end lines with `\n`, not `os.linesep` (Notes p.191). `print(..., file=f)` adds a line break; `f.write` does not (Notes p.191–192). **[community]**
- Checking existence: EAFP avoids the race between checking and using (Notes p.192, p.787). `os.path.exists` is also False for a broken symbolic link; use `isfile`/`isdir`/`islink` for the type (Notes p.195–196). Non-empty file: `isfile(p) and getsize(p) > 0` (Notes p.193). **[community]**
- Paths: `os.path.join` is portable; `os.walk` recursive; `os.scandir` (3.5+) when you need metadata; `shutil` to copy/move (Notes p.190, p.194–195; Tut p.93); `glob` for wildcards (Tut p.93). `import os`, not `from os import *`, so that `os.open()` does not shadow `open()` (Tut p.93). **[official]** + **[community]**
- `mkdir` creates only the last level; `makedirs` creates the chain and fails if the target exists; `remove` is for files, `rmdir` for directories (Notes p.303–304). **[community]**
- Rewriting text in a file: `fileinput.input(name, inplace=True)` (Notes p.193). **[community]**
- **JSON × pickle:** JSON for interoperability and external data, basic types only (lists/dicts); instances require extra work. Pickle only between Python programs and trusted data: unpickling untrusted data can execute arbitrary code (Tut p.66; Notes p.534–535). `dump/load` with a file; `dumps/loads` with a string (Notes p.298). **[official]** + **[community]**
- **Bytes:** modes `'rb'/'wb'` deal with `bytes`; mixing them causes an error (Notes p.654). **[community]**
- **Data security:** randomness for security → `secrets` (3.6+) or `random.SystemRandom()`, never the default `random`; reproducibility → `seed` or `getstate/setstate` (Notes p.318–319, p.321–322). Password hashing: `pbkdf2_hmac` with a random salt per password, many iterations (bcrypt/scrypt cited as stronger); large file: `update` in blocks (Notes p.778–779). **[community]**
- **SQL:** parametrize (`?` or `:name`); `%s` to insert strings opens SQL injection; `executemany` accepts a sequence or an iterator (Notes p.670–671). **[community]**

---

## 9. Exceptions

**Principle:** exceptions are a flow tool: handle the specific, let the rest propagate, clean up with `finally`/`with`, preserve context with chaining and notes (Tut p.69, p.71–73, p.76). **[official]**

```
Can something fail?
├─ Do I know how to handle the error here? ── yes -> except SpecificType (tuple if the handling is the same)
│                                └ no -> let it propagate
├─ I only want to log and follow the error ─> except Exception: log; raise   (bare raise)
├─ I want to translate to a domain error ──> raise New(...) from e
├─ I want to hide the automatic context ───> raise New(...) from None  (3.3+)
├─ Code only for the success case ─────────> else block of the try
├─ Release a resource ─────────────────────> with (if there is a cleanup action) ; otherwise finally
├─ Several independent errors ─────────────> ExceptionGroup / except*
└─ Extra context after catching ───────────> e.add_note("...")
```

**Rules**

- **Be specific.** A bare `except:` masks bugs, catches `SystemExit` and `KeyboardInterrupt` and can raise a `NameError` that hides the original error (Tut p.69; Notes p.449, p.783). Broad catches only at the outermost level, logging details (Notes p.449). **[official]** + **[community]**
- **Order of the `except` clauses:** the first one that matches wins; derived classes BEFORE bases. An `except` of a derived class does not catch instances of the base (Tut p.68–69). Parenthesized tuple for several types (Tut p.68). **[official]**
- **`else` of the `try`:** code that only runs without an exception and whose exceptions must not be caught by the previous `except` (Tut p.70; Notes p.452). **[official]** + **[community]**
- **Bare `raise`** inside `except` observes and re-raises keeping the traceback (Tut p.71; Notes p.449). `raise Class` is equivalent to `raise Class()` (Tut p.70). **[official]**
- **`from exc` × `from None`:** `from exc` marks a direct cause when translating; `from None` turns off automatic chaining (Tut p.71–72; Notes p.629–630). **[official]** + **[community]**
- **Custom exceptions:** derive from `Exception`, keep them simple, name ending in `Error` (Tut p.72). **[official]**
- **Cleanup:** `finally` for external resources regardless of success (Tut p.73); `with` when the object documents predefined cleanup (Tut p.74). The Notes themselves say that the `try/finally` pattern of releasing a resource is usually better with a context manager (Notes p.455, p.408). **[official]** + **[community]**
- **Custom context manager:** `@contextlib.contextmanager` with `try/finally` around the `yield` if cleanup must happen even with an exception; class form (`__enter__`/`__exit__`) when there is state or reuse. Nested `with` and comma-separated `with` are equivalent (Notes p.409–411). **[community]**
- **EAFP × LBYL:** the tutorial calls EAFP the typically Python style; in multithreading, EAFP or locks avoid the race window of "check and then use" (Tut p.128, p.132). The Notes agree: try and handle the specific error when checking is expensive or the operation may fail anyway; better still, keep the result and test `is not None` (Notes p.783–784, p.787). **[official]** + **[community]**
- **Key access:** `try: d[k] except KeyError` avoids two lookups; `d.get(k, default)` when the handling is simple (Notes p.784). Another passage of the Notes uses `d['n'] = d.get('n', 0) + 1` instead of try/except (Notes p.532): both are valid, choose by readability. **[community]**
- **Validating user input:** `while True` + `try/except ValueError` + `break` on success; input always arrives as `str` (Notes p.46, p.453). **[community]**
- **Operators:** return `NotImplemented` (do not raise) when the other operand is not supported (Notes p.488–489). **[community]**
- **Tests:** use the most specific `unittest` assertion (better message and does not depend on `-O`, unlike `assert`); `assertRaises` with `with` allows checking more, but several calls may raise the same type; `addCleanup` runs even if `setUp` fails, `tearDown` does not (Notes p.757, p.759–760). `doctest` for simple cases; `unittest` for complete suites (Tut p.97). **[community]** + **[official]**
- **Debugging:** `python -m pdb` from the start; `pdb.set_trace()` at a specific point; `excepthook` with `call_pdb` for post-mortem (Notes p.501–502). **[community]**

---

## 10. Classes and the data model

**Principle:** a class is an object; a method is a function plus automatic binding of the instance; privacy is convention (Tut p.79, p.82, p.85–87). **[official]**

```
Do I need to model...
├─ data + behavior, "has a" relationship ....... composition (objects referencing objects)  [Notes p.238–239]
├─ "is a" relationship, reuse behavior ......... inheritance (super() for the parent)
│     ├─ capability that not every subclass has .. mixin  (order of the bases matters: MRO)
│     ├─ mandatory contract ..................... ABCMeta + @abstractmethod  (fails early, TypeError)
│     └─ no class relationship needed ........... duck typing
├─ simple record ................................ @dataclass
├─ derived/validated/read-only value ............ @property (start with a plain attribute)
├─ alternative constructor ...................... @classmethod returning cls(...)
├─ stateless utility function ................... @staticmethod
└─ single instance .............................. see singleton below
```

**Rules**

- **Instance variable × class variable:** `self.x` in `__init__` for what is per instance; a class variable for shared attributes/methods; never a mutable class-level list/dict if the intent is one per instance (Tut p.84; Notes p.788). **[official]** + **[community]**
- **Instance method × classmethod × staticmethod:** an instance method uses `self`; `classmethod` uses `cls` (alternative constructors, class attributes, works in subclasses); `staticmethod` receives nothing (Notes p.228, p.232–233). **[community]**
- **Property:** gives attribute syntax to something computed, validated or lazy; no setter = read-only (Notes p.235–236, p.481). Start with a plain attribute and promote it to a property when needed, because swapping an attribute for a method would break whoever uses the API (Notes p.612–613). Trade-off: do not write Java-style getters/setters. **[community]**
- **Inheritance, calling the parent:** `BaseClassName.method(self, args)` only works if the base is reachable by that name in the global scope (Tut p.86–87); `super()` without arguments in Python 3 (Notes p.229). With multiple inheritance, cooperative `super()` (Tut p.87). **[official]** + **[community]**
- **Multiple inheritance:** the lookup is linearized (MRO): it preserves left-to-right order, calls each parent once, is monotonic; every case has at least the diamond via `object` (Tut p.87). Each `__init__` only calls the next one if it uses `super()` (Notes p.234). The order of the bases decides which overridden method wins (Notes p.610–611; the Notes point out an MRO trap between p.611 and p.617). **[official]** + **[community]**
- **`isinstance` × `issubclass`:** `isinstance(obj, int)` for an instance; `issubclass(bool, int)` is True, `issubclass(float, int)` is False (Tut p.87). In conditionals the Notes discourage depending on the variable's type (Notes p.39). **[official]** + **[community]**
- **Duck typing × inheritance:** with no necessary relationship, duck typing is enough; if you want a contract and default behavior, a base class (Notes p.490–492). Duck typing avoids `if type(...)` chains. To check capabilities, when `hasattr()` is awkward or incorrect (magic methods), use ABCs from `collections.abc`, `numbers`, `io` (Tut p.123, p.128). **[official]** + **[community]**
- **Conversion × `isinstance`:** the Notes recommend converting (`str(x)`, `list(x)`) instead of checking the type (Notes p.787); treat with caution, since converting may accept inputs that should be rejected [inference]. **[community]**
- **ABC × `NotImplementedError`:** `NotImplementedError` in a stub only fails at the call; `ABCMeta` + `@abstractmethod` prevents instantiating an incomplete subclass, with `TypeError` (Notes p.615–616). **[community]**
- **Name mangling (`__x`):** only to avoid a real collision with subclass names; for non-public, one underscore (Tut p.87). **[official]**
- **Emulating a type:** code that expects a file-like object may receive a class with `read()` and `readline()` over a buffer (Tut p.88). **[official]**
- **Dunder methods:** the book advises implementing at least `__repr__` in your own classes (Notes p.500); `__str__` only if you need a distinct friendly form (Notes p.500). Operators: return `NotImplemented` and implement the reflected version when the object on the right must also work (Notes p.488–489). For custom falsy/truthy: `__bool__`/`__len__` (Notes p.101–102). **[community]**
- **Hash/eq:** gap in this entry; see section 6 and check the Ref.
- **Singleton** (the Notes observe that there are no private constructors in Python): `__new__` with a cache on the class, a class decorator, or a metaclass with `__call__` (Notes p.224, p.240–243, p.689–690). **[community]**
- **Patterns:** Strategy — functions outside the class attached with `types.MethodType`, in place of an abstract interface (Notes p.691–692); Proxy — same interface as the real object, concentrating access rules outside the business service (Notes p.692–693). **[community]**
- **Explicit `object` subclasses** only matter in code that runs on both 2 and 3 (Notes p.636). **[community]** **[DATED]**
- **Inspection:** `dir(obj)` filtered by `not m.startswith('__')` lists non-magic members (Notes p.239); `inspect.getsource` for functions of an ordinary module (Notes p.608–609). **[community]**
- **Class-based iterator × generator:** prefer the generator for conciseness (Tut p.90). **[official]**
- **`weakref`:** cache of expensive objects without a reference that keeps them alive (Tut p.102–103). **[official]**

---

## 11. Modules and packages

**Principle:** module = file + private namespace + single execution per session (Tut p.50–51). **[official]** Import in packages is explicit by default (Tut p.56).

```
How do I import?
├─ possible name collision ....... import mod  (namespace)   ; as to abbreviate/avoid a conflict
├─ certain it does not collide ... from mod import name
├─ import * ....................... avoid in code; tolerable in interactive mode
├─ name only at run time .......... importlib.import_module("pkg.sub")
└─ reload in the session .......... importlib.reload(mod)   (Python 3)
```
Sources: Tut p.50–51 **[official]**; Notes p.270, p.272–275 **[community]**.

**Rules**

- **Import order:** standard library, third party, local; one per line; avoid `import *` (Notes p.273–274). The Notes say that `from m import a, b` on the same line is discouraged by PEP 8, but the origin notes mark this as to be verified [VERIFICAR]; do not assert it as a rule. **[community]**
- **Entry point:** `if __name__ == '__main__':` makes the file both executable and importable; put the logic in `main()` that returns a code and call `sys.exit(main())` under that guard (Notes p.51, p.412, p.533). In `multiprocessing`, the Notes' examples use the guard (Notes p.536–537, p.547); the text shows this as an example, it does not state that it is required; `spawn` on Windows is cited in Notes p.547 [inference: the link between `spawn` and the need for the guard is not stated there]. **[community]**
- **Executable packages:** entry point in `__main__.py` and `python -m package` (Notes p.417). **[community]**
- **`__all__`:** `import *` does not scan directories; it only brings what is in the package namespace; control it with `__all__` or import submodules by name. Local names can shadow submodules (a `reverse` function in `__init__` versus `reverse.py`) (Tut p.56). **[official]**
- **`__init__.py`:** the tutorial says to use regular packages (with `__init__.py`) by default and namespace packages only when several installable packages share a common parent (Tut p.134). The Notes state that the directory "needs" `__init__.py` to be detected (Notes p.51): **[DIVERGES]** — the official source recognizes namespace packages (without `__init__.py`), so the absolute statement is incorrect as a general rule; `__init__.py` is the default choice, not the only possible one.
- **Own modules:** keep them in the same directory as the importer; avoid the Python lib (Notes p.50–51). **[community]**
- **Virtual environments:** isolate dependencies per application and avoid version conflicts (Tut p.107). The Tutorial uses only `venv` (Tut p.107), with `.venv` as a common directory (Tut p.107) and `requirements.txt` that can be versioned (Tut p.109) **[official]**. The Notes present `virtualenv` first (p.705), treat `venv` as built in since 3.3 (p.706) and call `virtualenvwrapper` "most recommended" (p.715) **[community]**; the Notes do not say they prefer `venv` over external tools. Installing with `pip` inside the environment: Notes p.710 **[community]**. With several versions, check which installation pip changes (`pip --version`, `sys.path`; `path/python -m pip`; on Windows `py -3 -m pip`) (Notes p.415, p.423). **[official]** + **[community]**
- **`virtualenv -p python3 foo`** as an alternative for another version (Notes p.707) **[DATED]** (predates the built-in `venv`).
- **Packaging:** `scripts=` × `entry_points` in `setup.py`; `entry_points` calls `main` by command name (Notes p.436). **[community]**
- **Logging per module:** `logging.getLogger(__name__)` (Notes p.412). **[community]**
- **CLI:** `sys.argv` for trivial cases (index 0 = script, arguments are strings), `argparse` for sophisticated ones; `docopt`/`click` (third party) in larger cases; `argparse.add_subparsers(dest="cmd")` for subcommands (Tut p.93–94; Notes p.427–429, p.665–667, p.718, p.795). Errors to `sys.stderr`, `sys.exit(code)` nonzero on failure (Tut p.94; Notes p.718). **[official]** + **[community]**
- **Subprocess:** `call` returns only the status; `check_output` captures stdout; `Popen` for fine control (non-blocking, `poll()`); `communicate()` for one round of input/output; `shell=True` has security problems; `shlex.split` to build the list (Notes p.433–434). **[community]**
- **Logging:** levels DEBUG..CRITICAL, by default INFO and DEBUG are suppressed and output goes to stderr (Tut p.102). Pass arguments for lazy formatting: `logger.debug('text %s', value)` (Notes p.595). Configuration: code, `fileConfig` (INI) or `dictConfig` (2.7+, PEP 391), the latter easier to maintain (Notes p.595–596). **[official]** + **[community]**
- **Time zones and dates:** fixed offset → `datetime.timezone(timedelta(...))` (3.2+); DST requires third parties (`pytz`/`dateutil`) according to the Notes (Notes p.65–66); `timedelta` between the same type, mixing `date` and `time` gives `TypeError` (combine with `datetime.combine`); there is no `timedelta` of months: `relativedelta` or `calendar.monthrange` (Notes p.68–69). The Tut indicates `datetime` with time zone support (Tut p.96). **[community]** + **[official]**
- **Source code of a function:** defined in the console, `dill.source.getsource` (third party); C built-ins only by reading CPython (Notes p.608–609). **[community]**
- **Measuring performance:** `timeit` for micro-snippets, `profile`/`pstats` for critical sections (Tut p.96); `cProfile` for where the script spends time, `line_profiler` for a few functions line by line (Notes p.770, p.776–777). First clean, correct code; measure before and after; undo if the gain is small (Notes p.772–773, p.776). **[official]** + **[community]**
- **pytest fixtures:** `yield` makes setup/test/cleanup readable and dispenses with `request.addfinalizer` (Notes p.768). **[community]**

---

## 12. Concurrency

**Principle:** coordination is the main challenge; design errors cause failures that are hard to reproduce (Tut p.101–102). **[official]** The GIL, reference counting and bytecode are CPython details, not the language contract (Tut p.125, p.131, p.137). **[official]** The performance numbers below come from measurements in the community book and hold for its machine and version.

```
What is the bottleneck?
├─ I/O or waiting (network, sleep) .... threads are effective
│       4 threads of 2 s sleeping took 2 s in total   (Notes p.543)
│       Tut: threading serves responsiveness and overlapping I/O with computation (Tut p.101–102)
├─ CPU in pure Python ................. multiprocessing   (Notes p.544, p.547)
│       Notes example: 4 threads ~14.4 s; 1 run ~2.05 s; 4 processes ~2.3 s (Notes p.543–544)
│       alternative: a C extension that releases the GIL (Py_BEGIN_ALLOW_THREADS) (Notes p.550)
│       independent tasks: multiprocessing.Pool().map(f, items); ~1.8x on 2 CPUs (Notes p.550);
│       the input must have at least as many items as cores (Notes p.591)
├─ many cooperative I/Os .............. asyncio: only cooperative I/O concurrency;
│       it does not get around the GIL nor parallelize blocking calls (Notes p.316–317)
└─ worker pool ........................ ThreadPoolExecutor(n).submit(...) (shorter than Queue + daemon Threads) (Notes p.540)
        └─ ProcessPoolExecutor only accepts "picklable" tasks/arguments (object methods generally are not);
           to schedule an object method, use a thread pool (Notes p.314–315)
```

**GIL in extensions:** a C extension that releases the GIL with `Py_BEGIN_ALLOW_THREADS`/`Py_END_ALLOW_THREADS` to parallelize: Notes p.550 (section 120.2) **[community]**. Do not use Notes p.796 for this: section 201.10 shows the opposite, `math.factorial` (a C function) **holding** the GIL and blocking the main thread, with the output "Calculating..." only after the calculation finished (Notes p.796). **[community]**

**Standard library (Lib), no source text read in this entry:** the stdlib index lists `concurrent.interpreters` ("Multiple interpreters in the same process", Lib p.1094–1097), `InterpreterPoolExecutor` inside `concurrent.futures` (Lib p.1085–1093) and the section "GIL and performance considerations" of `threading` (Lib p.1017–1033; the index does not give the exact page of the section). They serve as a starting point for alternatives to `multiprocessing` and as reading about the GIL; details and version were not checked here, consult `stdlib-indice.md` and the Lib before asserting behavior. **[official]** (existence of the modules, according to the index) [inference] (usefulness as an alternative)

**Labels:** the decision block above is **[community]** except where it cites Tut. asyncio appears only in the Notes in this entry; no official counterpart is cited [inference: consult the official `asyncio` documentation before asserting details].

**Communication and shared state**

```
How do I share data?
├─ concentrate the resource in one thread and feed it via queue.Queue .... preferred by the Tut (avoids locks/events/semaphores) (Tut p.101–102)
├─ threads, mutable state ............. threading.Lock in with                (Notes p.545)
├─ between processes, counter ......... multiprocessing.Value('d', 0) + Lock  (an ordinary global variable is not visible) (Notes p.546)
├─ threads: Queue ..................... producer put / consumer get (blocking) + task_done (Notes p.539–540)
└─ processes: multiprocessing.Queue ... (Notes p.548; "sticking with Queue is always safe", a claim by the Notes)
```

- **queue.Queue × deque:** `Queue` for communication between threads; `deque` for ordinary queues (Notes p.333, p.335). **[community]**
- **Stopping a thread:** there is no "kill"; subclass with `threading.Event` and the `run` loop checks `is_set()`; a thread that has run does not restart (`start` again → `RuntimeError`); `daemon=True` (set before `start`) does not prevent the program from ending (Notes p.538, p.542). **[community]**
- **Race window:** "check and then use" in multithreading; prefer EAFP or locks (Tut p.128, p.132; Notes p.129). **[official]** + **[community]**
- **Servers:** `TCPServer` serves one client at a time; `ThreadingTCPServer` for several; manual alternative: `socket` + one thread per connection (Notes p.554, p.564). UDP: no connection or acknowledgment, for latency/broadcast; TCP: reliable, requires a connection and closing (Notes p.552–553). **[community]**
- **`ExceptionGroup`/`except*`:** report several independent exceptions, typical of concurrency frameworks (Tut p.74–75). **[official]**
- **Close resources explicitly** (files, connections, sockets) with `with`, without waiting for the collector (Notes p.526). **[community]**

**Divergence**

- The Notes summarize: about using threads in Python, the answer is "Don't. Use processes, instead." (Notes p.591). **[community]** **[DIVERGES]** from the tutorial, which recommends `threading` for responsiveness and overlapping I/O (Tut p.101–102), and from the Notes themselves (threads effective for I/O, Notes p.543). The position is too absolute; it holds for CPU-bound work in pure Python. Furthermore, the asyncio item of the Notes cites "threads/multiprocessing" for CPU-bound work (Notes p.316–317), in tension with the measurement that threads make CPU-bound work worse (Notes p.543–544).

---

## 13. Numbers and floating point

**Principle:** a float is an approximate binary fraction; the short decimal that gets printed hides a slightly different real value. It is not a bug in Python or in the code; each operation can add error of up to ~1 part in 2**53 (Tut p.115–119). **[official]**

```
Which numeric type?
├─ finance / decimal exactness / legal rounding / matching a hand calculation ... Decimal
├─ exact rational arithmetic (1/3) ............................................. Fraction
├─ heavy floating-point use ................................................... NumPy/SciPy
├─ see the real value of a float ............ Decimal.from_float | Fraction.from_float | as_integer_ratio() | hex()
├─ float equality ........................... math.isclose()   (round() only for rough approximation; pre-rounding does not solve exact equality)
├─ sum many floats .......................... sum() (already reduces loss) ; math.fsum() (tracks lost digits, slower)
└─ display .................................. round only at the end: format(x, '.2f') / '.12g'
```
Sources: Tut p.104, p.116–119 **[official]**. `hex()`/`fromhex()` are useful for portability and exchange with Java/C99 (Tut p.117).

Rules from the Notes **[community]**:
- Division: in Python 3, `/` is true division and `//` is floor and keeps the type; in Python 2, `/` between integers was floor (Notes p.80–81) **[DATED]** for the Py2 behavior.
- `int('123.456')` fails with `ValueError`; convert to float first (Notes p.39).
- `**` and `pow` keep int with int; `math.pow` always returns float and rejects a complex result; `pow(a, b, m)` is more efficient than `(a ** b) % m` (Notes p.82, p.375–376).
- `math.sqrt`/`math.log` return float; `cmath` returns complex (Notes p.82, p.85). `math.sqrt` is indicated as faster than `x ** 0.5` (Notes p.374); `math.exp(x)` more reliable than `math.e ** x` (Notes p.375–376).
- Near zero/one: `expm1`/`log1p` preserve precision (Notes p.82–83, p.85, p.282, p.376). `hypot` for Euclidean distance (Notes p.83). `atan2(y, x)` determines the quadrant and avoids division by zero (Notes p.279).
- `random.randint(a, b)` includes `b`; `randrange` follows `range`; `choice` one element; `sample(seq, k)` k distinct (error if k > population); `shuffle` in place, returns `None` (Notes p.319–320).

---

## 14. Choosing a tool in the standard library

Official summary (Tut p.93–104) **[official]**: `os`, `shutil`, `glob` (files); `sys.argv`/`argparse`; `sys.stderr`/`sys.exit`; `re` (complex matching); `random`, `statistics`; `urllib.request`, `smtplib`, `email`; `datetime`; compression (`zlib`, `gzip`, `bz2`, `lzma`, `zipfile`, `tarfile`); `timeit`, `profile`, `pstats`; `doctest`, `unittest`; `threading`, `queue`; `logging`; `weakref`; `array`, `collections.deque`, `bisect`, `heapq`; `decimal`, `fractions`; `reprlib`, `pprint`, `textwrap`, `locale`; `struct` (binary records); IPython/bpython when the interpreter lacks features (Tut p.113).

**The "switch" tree** (Notes p.600–603) **[community]** **[DATED]** (the book predates `match`/`case` of 3.10 and does not mention it; the tutorial recommends `match` for multiple constants/structure, Tut p.23, p.27 **[official]**):

```
Dispatch by value?
1. if/elif (or if ... return) .............. most direct and, according to the Notes, the most efficient
2. dict of functions: d.get(key, default)() . many cases, dynamic dispatch
3. class with getattr(self, 'case_{}'.format(x), None) .. by introspection
4. "Switch" context manager with __call__ .. readable, far less efficient
```

**Sorting and higher-order functions (Notes p.138–139, p.295, p.386–391) [community]:** `l.sort(key=...)` mutates and returns `None`; `sorted` returns a new list; `itemgetter`/`attrgetter` for dicts/tuples/objects.

---

## 15. "Pythonic" idioms from the Notes (quick list)

All **[community]**, unless indicated.

1. **Indentation:** 4 spaces; an empty block requires `pass` (Notes p.35, p.116).
2. **Swap:** `x, y = y, x` (Notes p.532).
3. **Unpacking** in `for` instead of indexing (Notes p.118–119).
4. **`is None`** for None (Notes p.39, p.105, p.107; also p.532–533).
5. **`for elem in seq`**, or **`enumerate`** when you need index and element; the book discourages walking by index with `range(len(x))` (Notes p.142, p.147, p.786; also Tut p.24, p.46 **[official]**).
6. **`with`** for every resource (Notes p.183, p.190–191, p.526; Tut p.63 **[official]**).
7. **EAFP** (Notes p.192, p.783–784, p.787; Tut p.128, p.132 **[official]**).
8. **Comprehension** instead of `map`/`filter` with lambda (Notes p.159–160; Tut p.41 **[official]**).
9. **Generators** for large volume; `sum(1 for x in it if c)` to count (Notes p.158, p.160–161).
10. **`.join`** instead of `+=` in a loop (Notes p.699, p.770).
11. **`get`/`defaultdict`/`Counter`** instead of a manual `if k in d` (Notes p.129–131, p.288, p.290–291).
12. **`deque`** for FIFO; **`set`** for membership (Notes p.143, p.292, p.335).
13. **`if not lst`** for an empty list (Notes p.142).
14. **`next(..., default)`** for the first item that satisfies (Notes p.363, p.383).
15. **`casefold`** to compare text (Notes p.265–266).
16. **`f-string`** (3.6+) (Notes p.247, p.249; Tut p.59 **[official]**).
17. **`functools.wraps`**, **`partial`**, **`lru_cache`** (Notes p.223, p.323–324, p.368).
18. **`itemgetter`** in `key=` (Notes p.295, p.387).
19. **`if __name__ == '__main__':`** and `main()` with `sys.exit` (Notes p.51, p.412, p.533).
20. **`logging.getLogger(__name__)`** and lazy logging (Notes p.412, p.595).
21. **Property** instead of getter/setter (Notes p.612–613).
22. **`raise X from e`** when translating; bare `raise` when re-raising (Notes p.449, p.455, p.629–630).
23. **Avoid `import *` and a bare `except:`** (Notes p.272–274, p.449, p.783).
24. **Operators and types:** implement at least `__repr__` (Notes p.500); duck typing (Notes p.490–492).

---

## 16. Register of divergences and dated items

| Topic | Notes say | Official source | Label / conduct |
|---|---|---|---|
| Package requires `__init__.py` (Notes p.51) | "needs" `__init__.py` | Regular packages by default; namespace packages exist (Tut p.134) | **[DIVERGES]** — official prevails |
| Threads in Python | "Don't. Use processes" (Notes p.591) | `threading` for responsiveness and overlapping I/O (Tut p.101–102); GIL is a CPython detail (Tut p.137) | **[DIVERGES]** — too absolute; holds for CPU-bound in pure Python |
| Formatting | `str.format` is equivalent to f-string and preferred over `%` (Notes p.257) | f-strings as the first option (Tut p.59) | **[DIVERGES]** partial — use f-string first; another passage of the Notes (p.247, p.249) already agrees |
| Implicit test "safer" (Notes p.533) | claims greater safety with unexpected types | not covered; the Notes themselves show false positives (p.102, p.104–105, p.789) | internal tension; use `is None` when `0`/`''` are valid |
| Dict order / `OrderedDict` (Notes p.145–146, p.793) | `OrderedDict` for order | not verified in this entry | **[DATED]** (flagged in the origin notes); confirm in the Ref |
| `x = x or default` (Notes p.104–105) | short idiom | official does not cover | valid only if legitimate falsy values do not exist |
| `from m import a, b` discouraged (Notes p.273) | cites PEP 8 | not verified | **[VERIFICAR]**; do not treat as a rule |
| `map` Py2/Py3, `reload`, `object` in inheritance, `/` division, `virtualenv -p`, `dictConfig 2.7+`, `.upper().lower()` | Python 2 | — | **[DATED]** |
| `match`/`case` | absent | Tut p.23, p.27 | **[DATED]** (book predates 3.10) |
| Dataclass, `asyncio` | dataclass absent; `asyncio` only at p.316–317 | `@dataclass` idiomatic (Tut p.88) | use the official source for dataclass; asyncio has no official counterpart in this entry |
| CPU-bound with threads (Notes p.316–317) | cites threads/multiprocessing | Notes p.543–544 shows threads making it worse | internal tension; prefer multiprocessing |

---

## 17. Known gaps of this base

- **Ref:** no citations in this entry. Missing: contracts of `__hash__`/`__eq__`, descriptors, exact scope and MRO rules, `match` semantics, the complete data model.
- **dataclasses:** only the tutorial's mention (Tut p.88); no details on fields, `frozen`, `eq`.
- **asyncio:** only one sentence from the Notes (Notes p.316–317).
- **Dict order comparison**: not confirmed in an official source in this entry.
- **Security pitfalls** (pickle, `shell=True`, SQL injection, randomness) come mostly from the Notes; only pickle has official support (Tut p.66).
- Performance claims (e.g. 570 µs vs 16.1 µs, ~500x from bisect, `itemgetter` faster than lambda) are measurements or opinions of the community book; present them as indicative, not as guarantees.
