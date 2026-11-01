# Chapter 16: Refactoring SerialDate

Source: CL ch. 16, PDF p.263-279 (opening p.263; "Primeiro, faça-a funcionar" — "First, Make It Work" — p.264; "Então, torne-a
certa" — "Then, Make It Right" — p.266; Conclusion and Bibliography p.279). In this chapter the printed page matches the PDF page.
Note: the running header of the odd pages repeats "Primeiro, faça-a funcionar" to the end (an artifact
of the edition); the internal page cross-references (e.g., "Listagem B.1, página 349") do not match the PDF — see
`apendice-b-mapa-das-listagens.md`.

Convention: bullets with a page are `[from source]` unless labeled otherwise. Pages = PDF.

## Stance: professional review, not an attack
- `SerialDate` (JCommon library, package `org.jfree.date`) is by David Gilbert, a competent programmer;
  it is "good code", and even so it will be taken apart (CL p.263).
- It is not arrogance: it is a professional review, something we should do and welcome; doctors, pilots,
  and lawyers do it (CL p.264).
- The author praises Gilbert's courage in opening the code to the community (CL p.264).
- The class exists because they wanted to represent dates without times, which `java.util.Date`/`Calendar` do not
  do well (CL p.264).

## Phase 1 — First, make it work
- The existing tests (`SerialDateTests`) all passed, but did not test everything [T1]; e.g., the method
  `MonthCodeToQuarter` was not used by anyone [F4] (CL p.264).
- With Clover, the tests covered only 91 of 185 statements (about 50%) [T2], with holes scattered around
  (CL p.264).
- To understand and refactor, higher coverage was needed: the author wrote his own independent
  suite (`BobsSerialDateTest`, Listing B-4) (CL p.264).
- Failing tests that represent the desired behavior were left commented out until the refactoring made them
  pass; even so coverage rose to 170 of 185 (92%) (CL p.264).
- Tests of obvious behavior that the program was not designed to pass [G2]; creating them was simple
  [T3]; making them pass was a matter of switching to `equalsIgnoreCase` (CL p.264).
- The tests on lines 153-154 should indeed pass [G2]; fixed in `stringToMonthCode` (CL p.265).
- Bug: `getFollowingDayOfWeek` returned 12/25/2004 as the Saturday following 12/25/2004 — incorrect
  behavior [G3], [T1]; a typical boundary condition error [T5] (CL p.265).
- This function had already been the target of earlier fixes (change history): bugs congregate [T6]
  (CL p.265).
- `getNearestDayOfWeek`: the author added many cases and not all passed [T6]; the pattern of failures
  shows the problem [T7]: it fails when the nearest day is in the future, another boundary condition [T5]
  (CL p.265).
- Clover's coverage pattern revealed a line never executed: the `if` was always false [T8]; the
  algorithm was wrong and was rewritten (CL p.265-266).
- Tests now expect `IllegalArgumentException` instead of an error string (CL p.266).
- End of the phase: all tests pass, the class works; time to make it right (CL p.266).

## Phase 2 — Then, make it right (top to bottom)
- Method: walk through the class from top to bottom, running all the JCommon tests after each change
  (CL p.266).
- Initial comments: license and copyright stay; the change history is a relic of the 1960s and
  goes away [C1] (CL p.266).
- Imports can be reduced with `java.text.*` and `java.util.*` [J1] (CL p.266).
- HTML in Javadoc mixes languages in one file (Java, natural language, Javadoc, HTML) [G1]; he suggests `<pre>`
  (CL p.266).
- Name: "serial" (serial number) does not describe the measure of days since 12/30/1899; "ordinal" would be better
  [N1] (CL p.266). And the name suggests implementation in an abstract class [N2]; `DayDate` chosen (CL p.267).
- Inheriting from `MonthConstants` to avoid writing the prefix is an old trick and a terrible idea [J2]; it becomes `enum
  Month`, which eliminates `isValidMonthCode` and error checks [G5] (CL p.267).
- `serialVersionUID` removed: he prefers automatic control, which is safer [G4]; a footnote records that
  reviewers disagreed (CL p.268).
- Redundant comments only propagate lies [C2]; comments about "serial numbers" [C1]; names of the
  constants gain clarity [N1] (CL p.268).
- `EARLIEST_DATE_ORDINAL`/`LATEST_DATE_ORDINAL` concern the implementation and move down to
  `SpreadsheetDate` [G6]; minimum/maximum year create a dilemma, since `RelativeDayOfWeekRule` uses them (CL p.268).
- The base class created a `SpreadsheetDate` (base class knowing the derivative) [G7]; solution: ABSTRACT
  FACTORY (`DayDateFactory`), which also answers minimum/maximum year; `createInstance` becomes `makeDate` [N1]
  (CL p.269-270).
- Day constants become an enum [J3]; redundant comments on the tables go away [C3]; a table that already has an
  access function should be private [G8]; an unused table is deleted [G9]; consistency decides moving/
  privatizing another [G6], [G11] (CL p.270).
- Interval constants become `DateInterval` (CLOSED, CLOSED_LEFT, CLOSED_RIGHT, OPEN) using
  mathematical nomenclature [N3]; enums make renaming with the IDE easier [J3] (CL p.271).
- Deletions: unused description field [G9]; unnecessary default constructor [G12]; Javadoc that only repeats
  the signature [C3], [G12] and that became wrong [C2] (CL p.271).
- `final` on arguments and variables removed: it only adds clutter [G12]; the author disagrees with those who say to
  put `final` on everything and says his tests already catch these errors (CL p.272).
- Duplicate `if`s merged [G5]; the day parse moves to the `Day` enum, which gets its own file [G13]
  (CL p.272).
- Duplicate `getMonths` becomes one [G9], [G12], [F4], renamed [N1]; `monthCodeToQuarter` is FEATURE ENVY
  [G14] and becomes `Month.quarter`; `Month` moves to its own file [G11], [G13] (CL p.273).
- A flag that selects the output format is a terrible idea [G15]; it becomes `toString`/`toShortString` in `Month`
  (CL p.273).
- `isLeapYear` more expressive [G16]; `leapYearCount` moves down to `SpreadsheetDate` [G6]; `lastDayOfMonth`
  uses an array of `Month` [G17] (CL p.274).
- `addDays` operates on the instance, so it should not be static [G18]; `toSerial` becomes `toOrdinal` [N1]
  (CL p.274).
- `addMonths` gets EXPLANATORY TEMPORARY VARIABLES (a Beck pattern); `getYYYY` becomes `getYear` [N1]
  (CL p.275).
- `date.addDays(7)` suggests mutation [G20]; names `plusDays`/`plusMonths` remove the ambiguity [N4] (CL p.275).
- `getPreviousDayOfWeek`: understand the algorithm [G21], explanatory variables [G19], static to instance
  [G18], duplication [G5] (CL p.275-276).
- `getNearestDayOfWeek` redone to be consistent with its neighbors [G11], [G19]; `getEndOfCurrentMonth`
  envied its own class [G14] (CL p.276).
- `weekInMonthToString`: an elegant sequence of IDE refactorings, until he noticed that only the tests
  used it — deleted; likewise `relativeToString` (CL p.276-277).
- `toSerial` becomes `getOrdinalDay`; `toDate` did not depend on the implementation and moves up [G6] (CL p.277).
- `getDayOfWeek` had a logical dependency on the origin of the ordinal [G22]; the abstract
  `getDayOfWeekForOrdinalZero` is created and the generic algorithm moves up [G6] (CL p.277).
- `compare` moves up [G6] and becomes `daysSince` [N1]; it had no tests and the author wrote them (CL p.277-278).
- The `switch` of `isInRange` goes away: each case becomes a method in the `DateInterval` enum [G23] (CL p.278).
- Final pass: outdated opening comment shortened [C2]; enums in their own files [G12];
  static utilities to `DateUtil` [G6]; abstract methods at the top [G24]; `make` becomes `fromInt` [N1];
  duplication in `plusYears`/`plusMonths` extracted into `correctLastDayOfMonth` [G5] (CL p.278-279).
- Magic number 1 replaced by named constants [G25] (CL p.279).
- `DayDate` coverage dropped to 84.9% (45 of 53 statements) because the class shrank; the uncovered
  lines are trivial (CL p.279).
- Conclusion: the Boy Scout Rule again; higher coverage, bugs fixed, smaller and clearer code
  (CL p.279).

## Heuristics cited in Ch. 16 → page
| Page | Codes cited (text order) |
|---|---|
| CL p.264 | T1, F4, T2, G2, T3 |
| CL p.265 | G2, G3, T1, T5, T6, T6, T7, T5, T8 |
| CL p.266 | C1, J1, G1, N1 |
| CL p.267 | N2, J2, G5 |
| CL p.268 | G4, C2, C1, N1, G6, G6 |
| CL p.269 | G7, N1 |
| CL p.270 | G6, J3, C3, G8, G9, G6, G11 |
| CL p.271 | N3, J3, G9, G12, C3, G12, C2 |
| CL p.272 | G12, G5, G13 |
| CL p.273 | G9, G12, F4, N1, G9, G14, G11, G13, G15, N1, N3, C3, G14, G12 |
| CL p.274 | G16, G6, G17, G16, G18, N1 |
| CL p.275 | N1, G20, N4, G21 |
| CL p.276 | G19, G18, G5, G11, G19, G14 |
| CL p.277 | G6, G6, G22, G6, G6, N1 |
| CL p.278 | G23, C2, G12, G6, G24, N1, G5 |
| CL p.279 | G25 |
Codes on p.271-278 checked against the images (the OCR loses several, e.g., "[Gl" or drops the code).

## Examples from the book
- Short excerpts in the text: corrected `getNearestDayOfWeek` algorithm (p.266), `enum Month` (p.267),
  `DayDateFactory` and `SpreadsheetDateFactory` (p.269-270), `enum WeekInMonth` (p.271), `enum Day` (p.272),
  `isLeapYear`/`lastDayOfMonth`/`addDays` (p.274), `addMonths`/`plusYears` (p.275), day-of-week
  methods (p.276), generic `getDayOfWeek` (p.277), `enum DateInterval` and `isInRange` (p.278).
- Full listings in Appendix B (CL p.341-394).

## What the chapter does NOT say / common confusions
- It does not say that Gilbert's code is bad; it calls it good and still improvable (CL p.263-264).
- It does not say to maintain high coverage at all costs: it accepts 84.9% when the uncovered part is trivial (CL p.279).
- It does not forbid `final` altogether: it admits a few uses, such as constants (CL p.272).
- The position on `serialVersionUID` is personal and contested by the reviewers themselves (CL p.268).
- The title "Primeiro, faça-a funcionar" at the top of the pages does not mean the whole final part is still
  phase 1 (header artifact) `[inference]`.

## [DATED]
- Clover as a coverage tool (CL p.264); today there are others `[extrapolation]`.
- JCommon/`org.jfree.date` and `java.util.Date`/`Calendar`; Java 8+ brought `java.time` (not mentioned in the
  book) `[extrapolation]`.
- Enums presented as a new alternative to `int` constants, typical of the transition to Java 5 (CL p.267).
- Removing `serialVersionUID` depends on the Java serialization context of the time (CL p.268).
