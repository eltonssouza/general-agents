# Appendix B: org.jfree.date.SerialDate — map of the listings

Source: CL Appendix B, PDF p.341-394 (p.395 is already Appendix C, "Referência Cruzada das Heurísticas" — Heuristics Cross-Reference).
Content: source code only (Java), no prose. Supports Ch. 16 (CL p.263-279).

Convention: pages = PDF. The printed page in Appendix B is PDF + 4 (e.g., PDF p.363 = printed 367).

## Map (start and end of each listing)
| Listing | File | State | PDF start-end | Role in Ch. 16 |
|---|---|---|---|---|
| B-1 | `SerialDate.java` | David Gilbert's original | p.341-357 | class analyzed line by line |
| B-2 | `SerialDateTest.java` | original JCommon tests | p.358-363 | ~50% coverage (91/185) |
| B-3 | `MonthConstants.java` | original (constants interface) | p.363-364 | target of [J2]; becomes `enum Month` |
| B-4 | `BobsSerialDateTest.java` | suite written by the author | p.364-372 | commented-out tests = desired behavior; 92% |
| B-5 | `SpreadsheetDate.java` | original (derived) | p.372-380 | destination of the implementation items [G6] |
| B-6 | `RelativeDayOfWeekRule.java` | original | p.380-383 | uses minimum/maximum year (dilemma of p.268) |
| B-7 | `DayDate.java (Final)` | refactored | p.384-386 | main result |
| B-8 | `Month.java (Final)` | refactored | p.386-387 | extracted enum |
| B-9 | `Day.java (Final)` | refactored | p.387-388 | extracted enum |
| B-10 | `DateInterval.java (Final)` | refactored | p.388 | enum with polymorphic `isIn` [G23] |
| B-11 | `WeekInMonth.java (Final)` | refactored | p.389 | enum |
| B-12 | `WeekdayRange.java (Final)` | refactored | p.389 | enum (LAST, NEXT, NEAREST) |
| B-13 | `DateUtil.java (Final)` | refactored | p.389 | static utilities [G6] |
| B-14 | `DayDateFactory.java (Final)` | refactored | p.390 | ABSTRACT FACTORY |
| B-15 | `SpreadsheetDateFactory.java (Final)` | refactored | p.390-391 | concrete factory |
| B-16 | `SpreadsheetDate.java (Final)` | refactored | p.391-394 | final implementation |

Boundaries checked in the OCR ("Listagem/Listing B-n" headers) and in the images of p.363, p.364, p.383, and
p.384. In the images, B-3, B-4, and B-7 start at line 1 but already carry the label "(continuação)" (continued)
(an error in the edition); B-1 and B-5 use "Listing" instead of "Listagem".

## What can be stated from the listings
- B-4 begins with tests of `isValidWeekdayCode` and `stringToWeekdayCode`, with several commented-out assertions
  (e.g., lowercase abbreviations) — the "desired" tests that Ch. 16 talks about (CL p.364; CL p.264-265).
- B-3 is a constants interface of `int` values for months (JANUARY = 1 etc.), with Javadoc warning that it differs from
  `java.util.Calendar` (CL p.364).
- B-6 shows `getDate` validating the year against `SerialDate.MINIMUM_YEAR_SUPPORTED`/`MAXIMUM_YEAR_SUPPORTED`
  and a `switch` that chooses between previous, nearest, or next day (CL p.383).
- B-7 opens with the abstract class `DayDate implements Comparable, Serializable`, abstract methods at the top
  (`getOrdinalDay`, `getYear`, `getMonth`, `getDayOfMonth`, `getDayOfWeekForOrdinalZero`) and `plusDays`/
  `plusMonths`/`plusYears` that delegate to `DayDateFactory.makeDate` and `correctLastDayOfMonth` (CL p.384).
- The final Javadoc of B-7 describes immutable dates with one-day precision and records Robert C. Martin as
  author of "a lot of refactoring" alongside David Gilbert (CL p.384).

## Cross-references in Ch. 16 vs. PDF (the pages cited in the text do not match)
| Ch. 16 text says | Where it actually is (PDF) | Citation |
|---|---|---|
| Listing B.1, page 349 | p.341 | CL p.264 |
| Listing B.2, page 366 | p.358 | CL p.264 |
| Listing B.4, page 374 | p.364 | CL p.264, p.277 |
| Listing B.3, page 372 | p.363 | CL p.267 |
| Listing B.5, page 382 | p.372 | CL p.268, p.277 |
| Listing B.6, page 390 | p.380 | CL p.268 |
| Listing B.7 (p. 394) through B.16 (p. 405) | p.384 to p.391-394 | CL p.279 |
`[inference]` The cited pages appear to be from the original English edition; the agent should cite the PDF.

## Examples from the book
- The whole appendix is an example; do not reproduce the listings. To explain a change, cite the corresponding
  passage of the Ch. 16 prose and point to the listing using the table above.

## What the appendix does NOT contain / common confusions
- It has no prose or justifications: the whys are in Ch. 16 (CL p.263-279).
- It does not contain the final version of `RelativeDayOfWeekRule` or of the tests; the final listings are B-7 to B-16.
- The line numbers cited in Ch. 16 (e.g., "linha 685" — line 685, "linhas 638-724" — lines 638-724) refer to B-1, except
  when the text indicates B-4 or B-5 `[inference]` (CL p.265, p.268).

## [DATED]
- JCommon Java 5 code (2005), with `java.util.Date`/`GregorianCalendar` and `DateFormatSymbols`
  (CL p.386, p.394); `java.time` (Java 8) does not exist in the book `[extrapolation]`.
- Tests in JUnit 3 (`extends TestCase`) (CL p.364).
