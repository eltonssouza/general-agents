---
name: python-code-review
description: Reviews Python code for pitfalls and idioms — mutable default argument, `is` vs `==`, `== None`, bare `except:`, swallowed exceptions, `return`/`break` in `finally`, `__eq__` without `__hash__`, collection modified during iteration, `eval`/`pickle`/`shell=True` — with an automatic AST scan (read-only) and a checklist. Use when the user asks "review this Python code", "is this Pythonic?", "code review of my module", "what should I improve in this script" or pastes Python code for evaluation. Do not use to interpret a traceback (use python-error-triage), to convert Python 2 (use python-py2-to-py3) or to pick a stdlib module (use python-stdlib-lookup).
---

# Python code review

Sources: Tut and Ref (official, release candidate 3.14.0rc3) and Notes (community, mixes Python 2/3). Details in `../../references/procedimentos.md` (section 20, "Checklist de revisão", i.e. review checklist), `frameworks.md`, `casos-e-antipadroes.md` and `fontes-comunitarias.md`.

## Procedure

1. **Find out the user's Python version.** Without it, keep version-dependent recommendations conditional (see `python-version-features`).
2. **Run the scan** (read-only; uses the `ast` module, does not run or import the code):
   ```bash
   python -I scripts/scan_python_smells.py PATH
   ```
   If the file is not valid Python 3 for the interpreter running the script, the report says so and scans for Python 2 constructs. **No findings is not approval**: the script does not cover logic, scope/closures in loops, types, concurrency or SQL built by string. Each finding prints the **origin of the rule** (official, community, inference or extrapolation) and the pages; pass that label on to the user. `weak-hash` (MD5/SHA1) is **[extrapolation]** and `except-pass` is **[inference]**.
3. **Walk through the checklist** and confirm or discard each finding by reading the code.
4. **Label the origin** of each recommendation: **[official]** (Tut/Ref) or **[community]** (Notes). If the Notes diverge from the official source, the official one wins **[DIVERGES]**.
5. **Deliver** prioritized findings (format below).

## Checklist (each item points to the source)

**Arguments and names**
- A `lambda`/`def` created in a loop resolves free variables **at run time**: all of them see the last value of the loop (Ref p.78, free-variable example). The text does not carry this example or the term "late binding": applying it to the loop is **[inference]**; fix shown in the sources: a function factory (Tut p.36, `make_incrementor`); the `lambda i=i` pattern **does not appear** in the sources — only the mechanism that the default value is evaluated at definition time (Ref p.103, 140) — so the application is **[inference]**. The scanner does not cover closures in loops.
- A mutable default value is computed **once**, at definition time; use `None` and create the object inside the function (Ref p.103; Notes p.207–208, 788–789).
- A mutable class attribute used as an instance default is shared: initialize it in `__init__` (Notes p.237, 788).

**Comparisons**
- `is None` / `is not None` instead of `== None` (Notes p.39, 105, 107). `is` compares identity, not equality (Ref p.31–32).
- `x or default` also replaces `0`, `''` and `[]`; if those values are valid, use `if x is None` (Notes p.104–105).
- If the class defines `__eq__`, define a consistent `__hash__`; `__eq__` alone leaves the instances out of dict/set (Ref p.52–53, 109).

**Exceptions**
- Catch specific types; bare `except:` and `except Exception: pass` mask bugs, and bare `except:` even catches `KeyboardInterrupt`/`SystemExit` (Notes p.448–449, 783).
- Order of `except` clauses: the first one that matches wins, so derived classes come before bases; a clause after `except Exception` or after a base is unreachable (Tut p.68–69). The `as` target is deleted at the end of the `except` block (Ref p.127–128).
- `return`/`break`/`continue` leaving a `finally` raise a `SyntaxWarning` in Python 3.14 (PEP 765, Tut p.73); the Tutorial also says the pending exception is not re-raised.
- Use `with` for resources (files, locks) instead of a manual `try/finally` (Tut p.74).

**Collections and loops**
- Do not modify the collection while iterating over it; iterate over a copy or build a new one (Tut p.23–24, 47; Notes p.143, 643).
- Shallow vs deep copy; `[[]] * n` repeats the same list (see `frameworks.md` §3).

**Unsafe items** (the community book shows them; **do not recommend them**): `eval`/`exec` on external input, `pickle.load` of untrusted data, `subprocess` with `shell=True` (the Notes p.434 say it raises security problems), MD5/SHA1 for security [extrapolation: the Notes p.694 list them without a warning], SQL built by string formatting. Details in `fontes-comunitarias.md` §4.

## Response format

- **Summary** (2–3 lines) and the Python version considered.
- **Findings** by severity: `file:line` — problem — why it matters — fix — source (Tut/Ref/Notes p.N), with **[official]/[community]**, **[DIVERGES]** or **[inference]**.
- **Not verified**: what could not be confirmed (I did not run the code, I did not run tests).

## Limits

- The scan is AST without flow analysis: it has false positives and negatives.
- The Tutorial and the Language Reference are from a release candidate. The Notes have errors of their own (see `fontes-comunitarias.md` §5).
