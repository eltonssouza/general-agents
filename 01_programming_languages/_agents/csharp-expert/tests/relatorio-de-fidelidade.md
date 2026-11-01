# Fidelity report (v2, post-audit): `csharp-expert`

Audit date: 26/10/2026. Package: `01_programming_languages/_agents/csharp-expert/`. This report **replaces** the v1 one, which declared "19 of 19 approved" while essentially validating the page range, not the content.

## 1. Sources and page convention

| Abbreviation | PDF | Pages | Note |
| :-- | :-- | :-: | :-- |
| CSYB | `CSharp-Yellow-Book.pdf` | 217 | Edition 8.1 (Dec/2019). Printed page = PDF − 5. |
| CSHist | `CSharp-9/10/11-WhatsNew.pdf` | 16 | Three PDFs with **identical text** (compared by hash of the extracted text): "The history of C#", updated on 18/11/2025, up to C# 14. There is no PDF with another name for the history. |
| CS12 | `CSharp-12-WhatsNew.pdf` | 6 | |
| CS13 | `CSharp-13-WhatsNew.pdf` | 7 | |

v1 used the PDF page in the body, but the **glossary cited the printed page** (199-211 instead of 204-213): a mixed convention. v2 standardizes on PDF and declares the map in `references/INDEX.md`.

Texts extracted with PyMuPDF (markers `=== PAGE N ===`). **CSYB (p.14-217), CSHist, CS12 and CS13 were read in full** for the audit; CSYB pages 1-13 were read by sampling (introduction and chapter 1).

## 2. What the audit found in v1

### 2.1 Automatic layer (v1)
Baseline script (outside the package, in `scratch/audit/csharp-expert/v1_audit.py`) over the v1 files: **476 citations**, none outside the page range (the ranges were too wide to fail), and **324 terms in backticks checked: 97 were not on the cited page** (30%) and 36 more were only on a neighboring page. The missing terms included `NullReferenceException`, `IndexOutOfRangeException`, `DivideByZeroException`, `GetHashCode`, `IDisposable`, `ArgumentException`, `System.Collections.ArrayList`.

### 2.2 Manual layer (v1): 105 claims read against the cited pages
Result: **19 OK, 22 wrong page, 42 unsupported, 22 exaggerated** (detail in `scratch/audit/csharp-expert/notes/03-amostra-manual-v1.md`). The sample covered the agent prompt, the eight references, the section index and the knowledge base of the error triager.

Relevant examples of what was **unsupported** (written as `[from source]`, but absent from the PDF):

1. **CIL, CLR and JIT** "CSYB p.10-14": the book only says the compiler converts the text into low-level instructions (p.16).
2. **`using`/`IDisposable`/`Dispose`** "CSYB p.80-84" and "the compiler translates `using` into try/finally": the book uses `Close()` (p.80) and manual `try/finally` (p.156, 158).
3. **`throw;` vs `throw ex;`** "CSYB p.183-184" ("forbidden" rule): the book never covers rethrowing; p.183 is about several `catch` blocks.
4. **`lock`, `lock(this)`, string interning** "CSYB p.175-177": the book uses `Monitor.Enter/Exit` (p.178); `lock` only exists in CS13 p.2.
5. **Boxing/unboxing, "the CLR synthesizes specialized native code"** "CSYB p.150-155": the book only talks about casts and typing (p.150-152).
6. **`GetHashCode` as a "mandatory CLR rule"** "CSYB p.131-135": `GetHashCode` appears on no page.
7. **Stack vs heap** for structs and objects (agent, `poo-e-design.md`, glossary): absent.
8. **Glossary "p.199-211"**: contained entries that the book's glossary does not have (Block, Byte, Cast, Destructor, Encapsulation, Iterator, Keyword, Lock, Object, Thread, Type...) and used the printed page.
9. **Visual Studio versions per release** (e.g. "C# 7.1: VS 2017 v15.3", "C# 11: VS 2022 v17.4", "C# 9: VS 2019 v16.8") and "C# 4.0: DLR": absent from CSHist/CS12/CS13.
10. **C# 14 "planned/preview"**: CSHist p.1 says "Released November 2025".
11. **`#nullable enable` and the "billion-dollar mistake"** (NRT, "CSHist p.7"): absent; NRT is only listed on p.8.
12. **`params` "forced a heap allocation"; `params ReadOnlySpan<T>` "zero allocations"** (CS13 p.1-2): CS13 does not claim this.

Examples of **wrong page** (the content exists, but on another page): integer table p.28 (v1: p.24-26); `float`/`double`/`decimal` p.29 (v1: p.25-29); comparing real numbers p.41 (v1: p.26-28); `switch` p.76-78 ok, but `while`/`do` p.45 (v1: p.41-44); `foreach` p.159 (v1: p.66-68); `virtual`/`override` p.122-123 (v1: p.127-130); `abstract` p.128-130 (v1: p.133-136); `protected` p.123 (v1: p.124-126); `using var` and *switch expressions* in C# 8 = CSHist p.8 (v1: p.7).

Examples of **exaggeration**: `double` "15 to 16 digits" (book: 15); `char` "UTF-16" (book: Unicode, more than 65,000 glyphs); `NullReferenceException` and `IndexOutOfRangeException` as names from the book (book: "the program fails"); records "immutable by default" (CSHist: value semantics in equality); "never `ArrayList`" (book: use `List`/`Dictionary` "in preference", p.153).

### 2.3 v1 scripts
The four scripts (cs-code-review, cs-error-triage, cs-version-lookup, cs-concept-lookup) encoded the same unsupported rules (`throw ex`, `lock(this)`, boxing, `IndexOutOfRange` etc., all with "[from source]") and the JSON index repeated wrong pages and summaries (e.g. "4.10: mandatory override of GetHashCode", "5.8: assertions, breakpoints"). The README listed 7 anti-patterns as "cataloged in the Yellow Book".

## 3. What was fixed in v2

- **Rewritten with page reading**: `agents/csharp-expert.md`, `references/` (INDEX + 8 files), 4 `SKILL.md`, 4 scripts, 2 JSON indexes, `plugin.json`, README.
- **Created**: `AGENTS.md` (Codex), `.github/agents/csharp-expert.agent.md` (Copilot), `tests/verify_citations.py` + `citation-checks.json`, `tests/audit_tokens.py`, `tests/run_script_tests.py`, `tests/extract_pdf_text.py`, fixture `trace_format.txt`.
- **Removal/downgrade**: every unsupported claim became `[extrapolation]` (when useful, in "Outside the book" blocks per file and in the INDEX `not_in_book` table) or was removed. Downgraded items include: stack/heap, boxing, `using`, `throw;`, `lock`, `GetHashCode`, `Math.Abs`, the `m` suffix, `TryParse`, `checked`, `%`, short-circuit, fall-through rule, exception names, `internal`, vtable, DLR, VS versions.
- **Pages corrected** to the PDF convention, with a section map in the INDEX; glossary rebuilt on the book's actual glossary (p.204-213), with 52 entries.
- **New supported content** that v1 lacked: `Monitor.Enter/Exit` and lost update (p.177-178), "do not catch everything" (p.74), custom exceptions (p.181-182), `Close()` in `finally` (p.80, 156-158), `Hashtable`/`ArrayList` with the author's recommendation (p.148-153), debugging (p.200-203), complete CSHist per version (C# 1.0 to 14), detailed CS12/CS13.
- **Agent prompt**: 73 lines (v1: 90, but with unsupported rules) with sections on scope, `not_in_book`, supported decision rules, consulting `references/` and real scripts, response format, epistemic honesty with the labels, boundary, `[DATED]` and prompt-injection defense.
- **Scripts**: the linter now declares the origin of each rule (7 `source`, 1 `inference`, 5 `extrapolation`) and ignores comments/strings; the triager separates what the book says (`FormatException` p.72, `KeyNotFoundException` p.153, `FileNotFoundException` p.186, *stack overflow* p.201) from what is `[inference]`/`[extrapolation]`; both lookups answer `NOT COVERED` (exit 1).
- **Cleanup**: removed the `scratch/csharp/blind/` folder from inside the package (it contained "blind answers" produced by the same model that wrote the package; kept in the backup); eliminated `file:///` links with a user path.
- **Encoding**: all files in UTF-8 without BOM; no mojibake or absolute paths (checked by `audit_tokens.py`).

## 4. Verifier results (v2)

| Verifier | Result |
| :-- | :-- |
| `verify_citations.py` | **153 positive and 28 negative checks; 0 failures.** The negative ones prove the absence from the PDF of: boxing, `IDisposable`/`.Dispose()`, `using (...)`, `throw;`, `lock (...)`, `GetHashCode`, `TryParse`, `Math.Abs`, common exception names, `checked`, CLR/JIT/CIL, heap, vtable, `internal`, `async`/`await`/lambda, `var`, short-circuit, the `m` suffix, `%`, VS 2019/2022 and .NET 7-10 in CSHist, among others. During construction, the negative checks caught 4 false positives of mine (e.g. "Dispose" in "disposing", "checked" in "error checked") which I fixed by refining the expressions. |
| `audit_tokens.py` | **577 citations; 388 terms checked; 0 failures; 0 "neighboring page"; range 0; encoding/path 0** (v1: 97 failures + 36 neighbors out of 324). Citations without an abbreviation (`p.N`) apply to CSYB. |
| `run_script_tests.py` | **31 checks (26 cases; some with two), 0 failures.** |

## 5. Audit coverage and what was NOT audited

- The automatic layer checks terms in backticks and numbers; **prose claims without a term in backticks** were checked by me while writing, by reading the pages, and by 153 curated checks, but **not by a second independent reader**.
- CSYB p.1-13 (chapter 1, computers and programming) were read by sampling; no rule in the package depends on them beyond what the INDEX maps (specification/tests, p.9-13).
- The version table was checked against the text of CSHist/CS12/CS13, but the feature lists are only names; technical explanations beyond that are `[extrapolation]` (labeled), not audited against the official Microsoft documentation.
- Code examples in the reference files are illustrative (written here); those for CS12/CS13 are adaptations of the examples on the pages.
- The PDFs were not altered; PDF text and package files were treated as data.

## 6. Honesty about the tests

The 26 cases in `casos-de-teste.md` were **run by the same model that audited and rewrote the package**: the machine-verifiable points (scripts and reference content) are in `run_script_tests.py`; the agent's conversational answers were **not** generated by an independent model. **There was no blind run.** The recommendation is to run the 26 cases with an independent model/session, without access to this report, before considering conversational fidelity validated.

## 7. Known pending items

- Blind run by an independent model (above).
- `skills/*/scripts` ran on Windows/Python 3.13; they were not tested on Linux/macOS.
- If the sources are updated (a new "What's new" PDF), regenerate the JSON indexes and rerun `verify_citations.py`.
