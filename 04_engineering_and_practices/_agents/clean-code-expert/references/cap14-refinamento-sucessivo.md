# Chapter 14: Successive Refinement (Args case study)

Source: CL ch. 14, PDF p.188-247 (opening p.188; subtitle "Caso de estudo de um analisador sintático
de parâmetro em uma linha de comando" — a case study of a command-line argument parser; conclusion p.247).

Convention: bullets with a page are `[from source]` unless labeled otherwise. Pages = PDF.

## What Args is and how the chapter is organized
- The chapter presents a module that starts well, stops scaling, and is then refactored and cleaned (CL p.188).
- Args parses command-line arguments: it receives a format/schema string and the `main` array;
  it is then queried through `getBoolean`, `getInt`, `getString`. Example: schema `"l,p#,d*"` declares `-l`
  as boolean, `-p` as integer, and `-d` as string (CL p.189).
- An error in the schema or the arguments raises `ArgsException`; the `errorMessage` method describes the problem (CL p.189).
- Chapter order: first the final version (p.189-195), then the draft that already worked (p.196-207), and
  finally the incremental refactoring until it gets close to the final version (p.207-247) (CL p.189, p.196, p.207, p.247).

## The final version: what the author wants you to notice
- The final code can be read from top to bottom without jumps; only the definition of `ArgumentMarshaler` sits
  further ahead, on purpose (CL p.191).
- Adding a new argument type is cheap: a new derivative of `ArgumentMarshaler`, a new `getXXX`
  function, a new `case` in `parseSchemaElement`, and probably a new `ErrorCode` and message (CL p.195).
- Reread it paying attention to names, function size, and formatting (CL p.195).
- The verbosity comes partly from Java, a static language; in Ruby, Python, or Smalltalk the program would be
  much smaller (CL p.195). Footnote: rewritten in Ruby it came out at 1/7 of the size (CL p.247).

## Central lesson: draft first, clean later
- The author did not write Args clean the first time and does not expect you to; to create clean code
  you must first create dirty code and then clean it (CL p.195).
- Analogy: school essays done through successive drafts; writing cleanly is constant refinement (CL p.195).
- Beginners think the goal is just to make it work and move on to the next task; experienced
  programmers know this is "professional suicide" (CL p.195).

## Why the first draft degenerated
- Listing 14-8 works, but it is messy; the author calls it a mess (CL p.196).
- Symptoms pointed out: a frightening number of instance variables; strange strings like "TILT";
  `HashSet`/`TreeSet`; try-catch-catch blocks piled up (CL p.201).
- The author was trying to keep it organized (names, rough structure), but drifted away from the problem (CL p.201).
- The mess grew gradually: the booleans-only version (14-9) was reasonable; with strings (14-10)
  it started to get out of control; with integers it became a heap (CL p.201, p.207).
- Structural cause identified: each new type required code in three places — parsing the schema element
  (choosing the type's HashMap), converting the command-line argument, and a `getXXX` that
  returns the real type (CL p.207).
- Many different types with similar methods suggest a class: hence `ArgumentMarshaler` emerges
  (CL p.207).

## The decision to stop
- With two more types to add, the author realized he would force it to work, leaving a trail of
  mess too big to fix; "Portanto, eu parei" (printed: "So I stopped") (CL p.207).
- He stopped adding features and started refactoring — if the structure was ever going to be maintainable, that was the moment
  to fix it (CL p.207).
- `[inference]` Actionable rule: when each new feature increases the mess in several places,
  stop adding features and refactor before the next one.

## Incrementalism and TDD
- One of the best ways to ruin a program is to make massive structural changes in the name of
  improving it; some programs never recover and are hard to get working again as before (CL p.207-208).
- Central TDD doctrine cited: keep the system running at all times; no change may break it
  (CL p.208).
- Prerequisite: automated tests that can be run at any moment — unit tests in JUnit and acceptance
  tests as wiki pages in FitNesse (CL p.208).
- Technique: many tiny changes, each moving the structure toward `ArgumentMarshaler`,
  with the system working after each one (CL p.208).
- First change: append a skeleton of `ArgumentMarshaler` at the end of the file (breaks nothing); then
  the change that would break the least: the booleans map starts holding marshalers (CL p.208).
- When a test breaks, incrementalism demands fixing it before any other change (CL p.209-210).
- Strategy: first concentrate all the behavior in the base class, then push it down the hierarchy
  to the derivatives, keeping everything running (CL p.210, p.212).
- The three per-type maps were replaced by a single map of marshalers, method by method (CL p.216-218).
- Surprise: the FitNesse tests covered a behavior (getBoolean on a non-boolean argument returns
  false) that the unit tests did not cover; up to then he had only been running the unit tests (CL p.220). Afterwards he added
  a unit test that invokes all the FitNesse tests (CL p.247, note 2).
- After the first refactoring (Listing 14-12), the result is a bit disappointing: there are still variables at the
  top, a type `case` in `setArgument`, and horrible set functions (CL p.227).
- Refactoring is like solving a Rubik's cube: many small steps; putting things in and taking them out again is
  common; each step makes the next one possible (CL p.230).
- Numbers cited: swapping the array for a list + `Iterator` took ten steps with tests after each
  (CL p.227); separating the exceptions took about 30 small steps, with tests between each (CL p.239).

## Chapter 17 heuristics cited in Chapter 14
| Code | Heuristic (name in Ch. 17) | Where/why in Args | Page |
|---|---|---|---|
| N5 | Use Long Names for Long Scopes | `argumentMarshaller` shortened to `am` (minimal scope) | CL p.209 |
| G23 | Prefer Polymorphism to If/Else or Switch/Case | eliminate the type `case` in `setArgument` | CL p.227 |
| F1 | Too Many Arguments | passing `args` and `currentArg` dirties the code; use an `Iterator` | CL p.227 |

## Introducing ArgumentMarshaler (polymorphism)
- Goal: in `setArgument`, a single call to `ArgumentMarshaler.set` instead of the type `case` [G23] (CL p.227).
- An abstract `set` receives the iterator even where the boolean does not need it, because int and string
  will need it; so all implement the same abstract method (CL p.230).
- With the `set` methods in the derivatives, the type `case` finally goes away (CL p.233).
- `ArgumentMarshaler` becomes an interface (CL p.234).
- Proof of extensibility: adding `double` starts with a new test, then the schema parse, a
  `DoubleArgumentMarshaler`, a new `ErrorCode`, and `getDouble`; and tests for the error cases (CL p.234-236).

## Partitioning and exceptions
- The exception code is horrible and does not belong in Args; throwing `ParseException` is not the module's business;
  everything goes into a single `ArgsException` in its own module (CL p.236).
- Args now throws only `ArgsException`; the error codes leave the Args module (CL p.239).
- Most of the changes in Args were deletions; the marshalers moved into their own files (CL p.246).
- Good software design is largely about partitioning: appropriate places for each kind of code;
  this separation of concerns makes it easier to maintain and understand (CL p.246).
- `errorMessage` in Args would violate the SRP; putting it in `ArgsException` is debatable, but the convenience of
  ready-made user messages weighs in (CL p.246).

## Chapter conclusion
- It is not enough for the code to work; whoever is satisfied with merely working code is not acting professionally (CL p.247).
- Nothing degrades a project in the long run more than bad code: schedules, requirements, and team dynamics
  can be redone, but bad code rots and becomes a weight (CL p.247).
- Cleaning up bad code is expensive (hidden and intricate dependencies); keeping it clean is relatively easy —
  the mess from five minutes ago is easy to clean up now (CL p.247).
- Final rule: keep the code as clean and simple as possible, never letting it start to degrade (CL p.247).

## Examples from the book (what each listing shows)
- 14-1 (p.189): use of Args in `main`, with schema, getters, and catching `ArgsException`.
- 14-2 (p.189-191): final `Args.java`, with the marshaler map, schema parse, and argument parse.
- 14-3 to 14-6 (p.192-193): `ArgumentMarshaler` interface and the boolean, string, and integer marshalers;
  double and string array are left as an exercise (CL p.193).
- 14-7 (p.193-195): `ArgsException` with `ErrorCode` and `errorMessage`.
- 14-8 (p.196-200): first complete draft (boolean, string, integer), the messy version.
- 14-9 (p.201-203): old boolean-only version; 14-10 (p.203-207): boolean and string.
- 14-11 (p.208): `ArgumentMarshaler` skeleton appended to the end of `Args.java`.
- 14-12 (p.222-227): Args after the first refactoring.
- 14-13 to 14-16 (p.239-246): resulting `ArgsTest`, `ArgsExceptionTest`, `ArgsException`, and `Args`.

## What the chapter does NOT say / common confusions
- It does not say everything should be designed clean before coding; it advocates a draft followed by cleanup (CL p.195).
- It does not authorize rewriting from scratch: the refactoring is incremental, with tests passing at each step (CL p.208).
- It does not reach the final version on the page: the last modifications are left as an exercise (CL p.247).
- It does not use the term "red-green-refactor"; it speaks of TDD and of keeping the system running (CL p.208).
- It does not claim that Java is bad; only that it is verbose for this problem (CL p.195).

## [DATED]
- JUnit (the 3/4 versions of the time) and FitNesse as test infrastructure (CL p.208).
- `ParseException`, `StringBuffer`, arrays converted to `Iterator` — Java 5/6 idiom.
- The Java x Ruby/Python verbosity comparison reflects the Java of 2008, before lambdas, records, etc.
  `[extrapolation]`
