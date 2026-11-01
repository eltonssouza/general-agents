---
name: python-error-triage
description: Diagnoses Python errors and tracebacks following the message → cause → fix flow (NameError, UnboundLocalError, TypeError in calls, KeyError, IndexError, RuntimeError from modifying a dict during iteration, SyntaxError, ImportError, unexpected "shared reference"). Use when the user pastes a traceback or says "I got an error", "why did my list change by itself?", "UnboundLocalError", "dictionary changed size during iteration", "SyntaxError on print". Do not use for general review without an error (use python-code-review) or for converting Python 2 code in bulk (use python-py2-to-py3).
---

# Python error and traceback triage

Sources: Tut (exceptions, p.69–76), Ref (execution model and names) and Notes (community). Table of messages and fixes in `../../references/casos-e-antipadroes.md` (Part 1); rules in `../../references/regras-da-linguagem.md`.

## Procedure

1. **Read the traceback from the bottom up**: the last line has the type and the message; the lines above show the call chain. Ask for the full traceback if it is missing (Tut, chapter on errors and exceptions).
2. **Find out the Python version**: the same code may work in one version and give a `SyntaxError` in another. A `SyntaxError` on `print "x"` points to probable Python 2 (see `python-py2-to-py3`).
3. **Look up the message** in `casos-e-antipadroes.md` (Part 1, by topic) with Grep. Only quote messages that are in the sources; if the exact message is not there, say that the message text is not in the sources.
4. **Classify the cause** in terms of the object and name model: undefined name or scope (`global`/`nonlocal`, Tut/Ref); mutability and aliasing; argument type; collection modified during iteration; import; syntax from another version.
5. **Propose the minimal fix**, with the source and the origin **[official]**/**[community]**. Suspicions that the Notes raise about themselves ("to confirm") do not become statements.
6. **Verify**: ask the user to run it again and confirm that the error is gone and no new one appeared.

## Frequent families (each points to the source)

- **Shared reference / "the list changed by itself"**: assignment does not copy; `[[]] * n`; mutable default evaluated once (Ref p.32, 103; Notes p.207–208, 788–789).
- **Modification during iteration**: skips items in a list; in a dict it raises `RuntimeError` ("dictionary changed size"); iterate over a copy (`list(d)`) or build a new collection (Tut p.23–24, 47; Notes p.143, 643).
- **Scope**: assigning to a name inside a function makes it local; `global`/`nonlocal` to rebind (Tut and Ref, names and scopes; Notes p.94–100).
- **Python 2**: `print` as a statement, `raw_input`, `xrange`, `iteritems`, `except E, e` (Notes p.626–633, 642–643) — **[DATED]**.
- **Import**: module name from another version (`Queue`, `urllib2`, `ConfigParser`); package and `__init__.py` (Tut p.134 prevails over Notes p.51) — **[DIVERGES]**.

## Response format

1. **Cause** in 1–2 sentences.
2. **Fix** (minimal diff); if there is more than one option, order them by preference.
3. **Why**, with the source (Tut/Ref/Notes p.N).
4. **Marking**: separate what comes from the source from your own inference about the user's code.

## Limits

- Without the traceback and the pointed-to snippet, do not propose a fix: ask for what is missing.
- The message table covers only what the sources show; errors from third-party libraries are out.
