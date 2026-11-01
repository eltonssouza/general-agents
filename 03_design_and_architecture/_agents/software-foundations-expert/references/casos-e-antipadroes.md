# Practical cases and anti-patterns of foundations

This reference gathers recurring situations and ties them to what the books actually say. In each case, what is `[from source]` comes with a PDF page; the rest is `[inference]` or `[extrapolation]` (our advice). Convention: PDF page (see `INDEX.md`).

## 1. Hidden mutation in a "pure" function (SICP)
- Context `[inference]`: someone adds a global counter or mutable cache to a function to "help with logging".
- `[from source]` (SICP p.217-220): with assignment, two evaluations of the same procedure with the same arguments can differ; referential transparency is violated and reasoning about programs becomes much harder. (SICP p.219-220: objects with distinct effects stop being interchangeable.)
- `[from source]` (SICP p.221): the order of assignments starts to matter (example of the imperative `factorial`).
- `[inference]` (from SICP p.217-221): symptom: `f(x) + f(x)` ≠ `2 * f(x)`; consequence: automatic memoization and formal substitution are no longer safe.
- Ways out `[from source]`: use the environment model (SICP p.224-227) to reason about state; or model change with streams (SICP p.296), remembering that "mutability and delayed evaluation do not mix well" (SICP p.325).
- `[extrapolation]`: "rigidly separate the functional core from the layers with effects" is common practice, not a sentence from SICP.

## 2. The "chatty" command-line tool (TAUP)
- `[from source]` (TAUP p.45-46): the Rule of Silence says to shut up when there is nothing surprising to say; the book treats conciseness as a central feature of the Unix style (quote from Ken Arnold, p.46).
- `[from source]` (TAUP p.327): programs that "chatter" do not compose well; if they emit status messages on standard output, whoever reads must discard them even when nothing went wrong; better to send only real errors to standard error and not emit unsolicited data; vertical screen space and the user's attention are also arguments (TAUP p.327).
- `[inference]`: `tool input.txt | sort | uniq` suffers if "Success: 120 files processed" goes to standard output (direct application of TAUP p.327).
- `[extrapolation]`: a `-v/--verbose` flag for progress on stderr is a modern convention, not a prescription of the book.

## 3. The tree-walk interpreter with the scope bug (CI)
- `[from source]` (CI p.164-166): the `showA()` example prints `global` and then `block`, even without reassignment, because the closure captures the mutable `Environment` and a later declaration in the same block shows up for it.
- `[from source]` (CI p.167-168): ways out: persistent environments or resolving statically; the book opts for a resolution pass that fixes the distance (hops) of each use (CI p.169-181).
- `[from source]` (CI p.168): resolving once also avoids re-resolution on every execution.
- `[extrapolation]`: variations in other languages (for example, `for` loops and closures) are external knowledge; v1 attributed them to CI p.187.

## 4. Premature optimization and disregard for measurement (TAUP, CI)
- `[from source]` (TAUP p.48-49): the Rule of Optimization says to prototype before polishing and cites the maxim of premature optimization (Knuth, who attributes it to Hoare, note 11); "premature local optimization often gets in the way of global optimization".
- `[from source]` (TAUP p.192, p.133, p.135): in the book, using concurrency or a binary format for performance before having a clean architecture is treated as premature optimization.
- `[from source]` (CI p.597, p.601): a profiler pointed to `tableGet()` with 72% of the time and allowed a specific optimization (35% afterwards); "if we had guessed hot spots, we probably would not have noticed" (CI p.601).
- `[from source]` (TAUP p.412): general rule of ch. 15 (*Profiling*): about 90% of a program's execution time is spent in 10% of its code; profilers serve to identify those 10% of hot spots (the book says that, in the Unix tradition, their most important function is another, TAUP p.412).
- `[inference]`: the symptom "90% of the optimization effort on sections worth 1% of the time" is our illustration; **those numbers (90% of the effort, 1% of the time) are not in the book**; the "90%" of TAUP p.48 is about delivered functionality.

## 5. Mixing mechanism with policy (TAUP)
- `[from source]` (TAUP p.40-41): policy and mechanism change on different time scales; tying them together prevents experimenting with new policies without breaking the mechanism and makes it harder to test; separating front end (policy) from back end (mechanism) or using an embedded scripting language (Emacs) are the ways.
- `[inference]`: the example of the calculation engine tied to a screen and unusable in an API or worker is our illustration of the Rule of Separation.

## 6. Opaque binary format for data and configuration (TAUP)
- `[from source]` (TAUP p.134): when you feel the urge to design a complex binary format, you should "lie down until the feeling passes"; compression over text usually results in a cleaner design.
- `[from source]` (TAUP p.135-136): in the password file, the gain of about 8% from a binary format is small compared to being able to edit with any editor and filter with `grep`.
- `[from source]` (TAUP p.134-135): binaries are only justified with volumes that really matter or a time/instruction budget for interpreting data; even so, extensibility must be considered.
- `[extrapolation]`: "JSON and YAML" as an alternative is ours; the book cites DSV, RFC 822, XML and INI (TAUP p.139-146).

## 7. Threads as the first choice (TAUP)
- `[from source]` (TAUP p.192, p.214-216): threads are a "performance hack"; they share the whole address space; there is no automatic encapsulation; they generate timing bugs that are hard to reproduce; they should be a last resort (p.216).
- `[from source]` (SICP p.279-283, p.292): in SICP, the interleaving of processes with shared state and deadlock require explicit control (serializers/mutex); the idea of avoiding sharing appears in TAUP, that of controlling it in SICP.

## 8. Minilanguage that grows by accretion (TAUP)
- `[from source]` (TAUP p.218, p.245): arriving at a language by "extending, one feature at a time" is the dangerous path (`sendmail.cf`, TECO); languages that are only "accidentally Turing-complete" invite obfuscated code.

## 9. Type dispatch with `cond` in growing systems (SICP)
- `[from source]` (SICP p.175-176): explicit dispatch on type forces changing the generic selectors for every new representation and avoiding name collisions; the technique "is not additive"; data-directed programming (operation×type table) solves it (SICP p.176-179).

## 10. Root forgotten in the GC (CI)
- `[from source]` (CI p.515, p.531-533): objects referenced only by the C stack during an allocation (constants, interned strings, concatenation) are swept by the collection; the fix is to protect them temporarily on the VM stack.
- `[from source]` (CI p.524): treating the string table as a strong root would prevent collecting any string; it is a weak reference.
