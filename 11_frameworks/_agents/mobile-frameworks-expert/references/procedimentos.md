# Procedures

All start from the three sources (RN, FLT, SWT). Where the text gives no steps, the procedure says "NOT COVERED". Nothing here runs the framework or accesses the network.

## P1 - Answer "what is X?" for RN, Flutter or Swift
1. Run `python -I scripts/mob_lookup.py X` and open the topic file.
2. State the **nature of the source** (RN = docs introduction, FLT = landing page, SWT = language tour) and the date/version: RN 0.87 / Aug 12, 2026; FLT no version; SWT no version.
3. Answer only with what the text says (`references/01`, `02`, `03-09`); the rest is NOT COVERED.

## P2 - Compare RN, Flutter and Swift
1. `python -I scripts/mob_compare.py list`, then `show CRITERION` for each requested criterion.
2. Each cell is a citation or NOT COVERED. State that Swift is a language and the other two are frameworks: the tour does not cover UI or platforms.
3. **Do not recommend.** "Which is better/faster/should I use" is NOT COVERED; offer only the criteria and, if the user asks, decision questions labeled [extrapolation] without picking a winner.

## P3 - Review a Swift snippet
1. Run `python -I scripts/swift_lint.py FILE.swift` (or `-` with stdin). Never compile/execute the pasted code.
2. Report each finding with its origin and page: `[from source]` (SWT p.N), `[inference]`, `[extrapolation]`.
3. Always say that the linter is heuristic and that "no findings" does not prove it compiles; real validation is the compiler (outside the collection).
4. For rules outside the tour (`!`, `try!`, `++`, C-style for) use the label [extrapolation].

## P4 - Study the tour in order
1. `python -I scripts/swift_tour_checklist.py list` shows the 38 topics and pages.
2. `scan FILE.swift` marks what the student's code already exercises; `next --done 1,2,3` suggests the next ones; `experiments` lists the tour's 20 exercises.
3. Remember that detection is heuristic and that part of the tour's code is truncated in the capture.

## P5 - Question about something the tour only mentions
Examples: `any ExampleProtocol` (only in the code, SWT p.16), `if` as an expression (SWT p.3), `willSet` (SWT p.11). Explain what the text says, cite the page and **do not** assert the Swift version in which the feature appeared (the tour does not state it; it would be [extrapolation]).

## P6 - Installation/setup question (RN or Flutter)
The text only points to links ("Install Flutter", RN's local environment guide). Answer NOT COVERED for steps/commands; cite that RN says getting started is in another section (RN p.1) and that Flutter recommends setting up the environment and following the learning pathway (FLT p.1).

## P7 - Request for web/React or native Android content
React web/Next.js: refer to `nextjs-react-expert`. Kotlin/native Android: outside the collection; say so.
