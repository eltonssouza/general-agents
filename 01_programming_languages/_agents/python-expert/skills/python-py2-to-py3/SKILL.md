---
name: python-py2-to-py3
description: Detects and converts Python 2 constructs to Python 3 (`print` as a statement, `raw_input`, `xrange`, `iteritems`, `has_key`, `except E, e`, integer division, `unicode`, renamed modules), with an automatic scan of .py files and a checklist of equivalents. Use when the user says "convert Python 2 code", "is this script Python 2?", "migrate to Python 3", "SyntaxError on print", "what does 2to3 do?". Do not use to upgrade between Python 3 versions (use python-version-features) or for style review (use python-code-review).
---

# Converting Python 2 to Python 3

Main source: Notes, chapters on 2→3 incompatibilities and `2to3` (p.620–646) — a **community** book and **[DATED]**. Full map in `../../references/versoes-e-datado.md` (section 3). The official documentation (Tut/Ref) describes only Python 3.

## Procedure

1. **Detect** what is Python 2 with the scan (read-only):
   ```bash
   python -I ../python-code-review/scripts/scan_python_smells.py PATH
   ```
   For a file that is not valid Python 3, the report lists `syntax-error` and the Python 2 constructs found (`py2-print`, `py2-raw-input`, `py2-xrange`, `py2-iter-dict`, `py2-has-key`, `py2-except-comma`, `py2-types`, `py2-long-literal`, `py2-module-names`…). Note: `except A, B:` **without** `as` is valid syntax in Python 3.14 and means a tuple of types (Ref p.127): confirm the intent before converting.
2. **Convert item by item** with the equivalents the Notes show (all **[DATED]** as an origin):
   - `print x` → `print(x)`; `print >>f, x` → `print(x, file=f)` (Notes p.626).
   - `raw_input` → `input`; do not replicate the old `input` (which evaluated the text) with `eval(input())` (Notes p.631).
   - `xrange` → `range`; `.next()` → `next(it)`; `iteritems/iterkeys/itervalues` → `items()/keys()/values()`; `has_key` → `in` (Notes p.627, 632–633, 642–643).
   - Division: Python 2 used `from __future__ import division` and `//` (Notes p.80–81); check the result of `/` in each case.
   - Unicode and bytes: see Notes p.653–656 and `versoes-e-datado.md` §3.
   **Mandatory items in the answer when the pasted code is Python 2** (confirm each one against the page):
   - `print()` with `sep`, `end`, `file` and `flush`; the trailing comma of Python 2 `print` becomes `end=""` (Notes p.186, 626);
   - `u'...'` is accepted in Python 3 and `ur'...'` is a `SyntaxError` (Notes p.624–625; Ref p.21);
   - `from __future__ import division` only makes sense in Python 2 (Notes p.80–81); the official confirmation of `/` and `//` is in Tut p.13 and p.129;
   - `.encode`/`.decode` and `bytes` vs `str` (Notes p.653–656);
   - `2to3 -w` creates a `.bak` copy of the file unless `-n` is used (Notes p.645–646).
3. **`2to3`**: the Notes describe the tool (p.645–646). **The sources do not say whether it exists in Python 3.14** and the Lib index does not list it: do not claim availability; suggest manual conversion guided by the report.
4. **What the Notes do not carry** (e.g. `functools.cmp_to_key` for `cmp`, `asyncio.run`) is **[extrapolation]**: label it.
5. **Verify**: run the tests/the script on Python 3 and compare behavior where semantics changed (division, strings/bytes, dict order).

## Response format

List of constructs found (file:line) → Python 3 equivalent → source (Notes p.N) with **[DATED]**, what is left for manual conversion and how to verify. Never present Python 2 code as current practice.

## Limits

- The origin is community-made and has errors (see `fontes-comunitarias.md`). The official source prevails for Python 3.
- The sources do not cover third-party libraries that changed between versions.
