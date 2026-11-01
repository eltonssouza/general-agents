---
name: python-stdlib-lookup
description: Locates Python standard library modules and returns the pages of the PDF "The Python Library Reference 3.14.0rc3" where to read about them, from an index of the bookmarks (no distilled content). Use when the user asks "which module do I use to read CSV?", "where is pathlib documented?", "which module does regex/JSON/dates/threads?" or "on which page of the Library Reference is X?". Do not use to explain how the API works (the index does not have that), for third-party libraries or for language features (use the Language Reference references).
---

# Locating Standard Library modules

Source: **index** generated from the 2,082 bookmarks of the PDF (45 chapters, 293 modules/topics) — file `../../references/stdlib-indice.md` and data in `scripts/stdlib_index.json`. **There is no distilled standard library text**: the index only says where to read. The documentation is from a **release candidate** (3.14.0rc3).

## Procedure

1. **Extract keywords** from the request (module name, task, format). Prefer English terms, as in the PDF titles.
2. **Query the index** (read-only, no network):
   ```bash
   python -I scripts/stdlib_lookup.py csv
   python -I scripts/stdlib_lookup.py path file --limit 5
   python -I scripts/stdlib_lookup.py --list-chapters
   ```
   Several terms mean "all must match". With no result, try a synonym or a shorter term.
3. **Answer with module + page range** `(Lib p.X–Y)` and **list the module's sections with the exact page** that the script prints (e.g. csv: Module Contents p.665, Dialects p.669, Reader Objects p.670, Writer Objects p.671). Mention neighboring chapters when useful. Saying which page to read is **[from source]**.
4. **Do not describe the API** (functions, parameters, examples) as if it came from the sources. If you describe it from your own knowledge, label it **[extrapolation]** and recommend confirming on the indicated pages.
5. **Complement with the Notes** when there is a relevant chapter (e.g. JSON, `os.path`, `collections`, `itertools`, `asyncio`), always as **[community]** and checking `fontes-comunitarias.md`. The Notes do not cover everything: for example, they do not carry `csv.reader`, and their CSV writing example uses `"wb"`, a Python 2 idiom (Notes p.584).
6. **If the index finds nothing**, say that the module is not in the bookmarks of the supplied PDF; do not invent pages.

## Response format

`module — Lib p.X–Y (chapter)` for each candidate, one sentence on when to use it (labeled if it is extrapolation), and the warning that the index only locates.

## Limits

- The `p.X–Y` ranges are approximate (from the start of the module to the page before the next item).
- The numbering is the PDF's; the printed one differs.
- The index has no "versionadded": a module's version requires reading the page.
