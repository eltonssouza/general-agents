# Style Guides and Coding Rules (SWE-G Ch. 8)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`, Ch. 8 "Style Guides and Rules" (PDF p.105-120, author Shaindel Schwartz). All facts below hold for Google, as reported in the book.

## 1. Rules vs guidance
- [from source] (SWE-G p.105) Rules are law: mandatory, universally applicable, waived only by case-by-case approval. Guidance brings recommendations and best practices with room for variation. Style guides are treated as canon and go beyond formatting: they cover the whole set of code conventions. There are separate guides per language, with very variable scope and size (Dart, R and Shell concise; C++, Python and Java long).
- [from source] (SWE-G p.115) Guidance is the "shoulds"; the rules are the "musts". Examples of guidance: per-language primers, the C++ "Tip of the Week", "<Language>@Google 101" courses (p.115-116).
- Fidelity note: the v1 package had a table "Rules / Guidelines (cover 95% of cases) / Best Practices" with approval levels by OWNER. The book only distinguishes rules and guidance; "95%" and the requirement of OWNER approval to deviate from guidelines are NOT in it.

## 2. Principles that guide the rules (five, not six)
- [from source] (SWE-G p.106) Key question: "what goal do we want to promote?" and not "what rules should we have?". Rules should: pull their weight (be worth the cost), optimize for the reader, be consistent, avoid error-prone or surprising constructs and concede to practicalities when necessary.
- [from source] (SWE-G p.106) Numeric context cited by the book: more than 30,000 engineers, about 60,000 submissions per day, a codebase of more than two billion lines.
- [from source] (SWE-G p.106-107) "Pull their weight": every new rule has a learning cost; obvious rules are not included (example: there is no rule against `goto` in the C++ guide).
- [from source] (SWE-G p.107-108) Optimize for the reader: code is read more than written; "simple to read" is worth more than "simple to write"; leave evidence of the intended behavior (examples `override`, `std::unique_ptr` for transfer of ownership); goal of "local reasoning" at the call site.
- [from source] (SWE-G p.108-110) Consistency: allows "expert chunking", eases tools and mobility between projects; the advantage is in having one answer and not in which answer (example of indentation and line length). At scale the book admits that C++ stopped promising total consistency of old code (p.109). There is a hierarchy: file, team, project, codebase (p.109) and a preference for external conventions when the code lives long (example of Python indentation; p.109-110).
- [from source] (SWE-G p.110-111) Avoid error-prone constructs: example of Python's reflective functions (`hasattr`/`getattr`), discouraged because they make searching and validation difficult.
- [from source] (SWE-G p.111) Concede to practicalities: performance (`noexcept` despite the prohibition of exceptions in C++), interoperability, generated code out of scope (Java and JavaScript).

## 3. What goes into a guide
- [from source] (SWE-G p.111) Three categories of rule: avoid dangers, enforce best practices and ensure consistency.
- [from source] (SWE-G p.112) New features can be restricted at first, watching waiver requests until the practice becomes widespread (`std::unique_ptr` case).
- [from source] (SWE-G p.112) "Consistency" rules exist to decide and document the decision (names, indentation, import order); the important thing is to have chosen.
- [from source] (SWE-G p.113) There are best practices deliberately left out of the guide ("don't be clever", "don't fork the codebase", "don't reinvent the wheel").

## 4. Changing rules, arbiters and exceptions
- [from source] (SWE-G p.113-114) Rules change over time: a new language version, a rule that people work around, an expensive enforcement tool. The reasoning and the pros and cons are documented so you know when to reevaluate. CamelCase -> snake_case case in Python.
- [from source] (SWE-G p.114) "Solution based" process: proposals start from a problem demonstrated in existing code. Decisions belong to the "style arbiters" (long-time experts), by consensus; the C++ group cited had four members.
- [from source] (SWE-G p.114-115) Exceptions/waivers are granted by the arbiters and "are not granted lightly" (examples of macros and implicit conversions).

## 5. Applying the rules and automating
- [from source] (SWE-G p.116) Rules can be enforced by training or by tools; the book says it strongly prefers automating conformance checking. The Readability process acts as mentoring on the rules.
- [from source] (SWE-G p.117) Some rules require human judgment or are social. Explicit example: about the size of a change, "engineers should favor small changes", but Google does NOT have a tool to automatically reject changes above a line limit; the definition of "small" is fuzzy and the decision is left to author and reviewers.
- [from source] (SWE-G p.117) An informal 2018 survey estimated that about 90% of the C++ guide's rules could be checked automatically; clang-tidy (C++) and Error Prone (Java) are cited.
- [from source] (SWE-G p.117-118) Automatic formatters enforced by presubmit (rejects the submit if the formatter generates a diff); tools cited: clang-format, yapf wrapper, gofmt, dartfmt, buildifier. The book says that, on average, the "robots" format better than humans, with exceptions such as matrix formatting.
- [from source] (SWE-G p.118-119) gofmt case (no configuration options) and retrofit of about 200,000 BUILD files with buildifier in six weeks by one engineer, helped by LSC infrastructure.
- [from source] (SWE-G p.119) TL;DR: rules should support resilience to time and scale; know the data to adjust them; not everything should be a rule; consistency is key; automate.

## 6. What is NOT in the chapter
- The "six principles" and the "Style Arbiter submits the proposal to strict criteria" (v1's numbered list) do not exist; they are the five principles above.
- "Humans in code review should not discuss punctuation" appears only as a consequence of the automatic formatter (p.117: formatting stops being a review topic); the book does not use the word "mandatory".
- "Randomize hash seeds in tests" is NOT discussed in Ch. 8 (the v1 package cited p.105 for this).
