# Capítulo 15: Características Internas do JUnit (JUnit Internals; refactoring of ComparisonCompactor)

Source: CL ch. 15, PDF p.248-262 (opening p.248; section "O framework JUnit" (The JUnit Framework) p.249; conclusion p.262).
Note: the running header of the even pages says "Capítulo 15: Testes de Unidade" (an error in the edition); the
chapter title at the opening is "Características Internas do JUnit" (CL p.248, p.249).

Convention: bullets with a page are `[from source]` unless labeled otherwise. Pages = PDF.

## Context
- JUnit is described as simple, precise in definition and elegant in implementation; the chapter examines a
  piece of its code (CL p.248).
- Origin story: Kent Beck and Eric Gamma, programming on a plane to Atlanta, created the basis of JUnit in
  about three hours (CL p.249).
- The module studied, `ComparisonCompactor`, helps identify string comparison errors: given
  ABCDE and ABXDE, it produces a string that highlights only the difference (CL p.249).
- The test cases (Listing 15-1) explain the requirements better than prose; the author invites the reader to
  judge whether the tests could be simpler or more obvious (CL p.249).
- The tests cover 100% of the code (every line, every if and for loop), which gives high confidence for
  refactoring (CL p.251).
- The original code (Listing 15-2) is considered well partitioned, reasonably expressive and of
  simple structure (CL p.251).
- For contrast, Listing 15-3 shows how the same module could look had it not been well
  written: abbreviated names and tangled logic (CL p.252-253).
- Motivation for touching code that is already good: the Boy Scout Rule — leave it cleaner than you found it
  (CL p.253).

## The refactoring, step by step
1. Remove the `f` prefix from member variables; today's environments make this scope encoding
   redundant [N6] (CL p.253).
2. Encapsulate the unencapsulated conditional at the start of `compact` in a method that explains the intent
   (`shouldNotCompact`) [G28] (CL p.254).
3. Disambiguate names: local variables with the same name as the members (`this.expected`) become
   `compactExpected`/`compactActual` [N4] (CL p.254).
4. Invert the negative condition: `canBeCompacted` instead of `shouldNotCompact` [G29] (CL p.254-255).
5. Rename `compact` to `formatCompactedComparison`: the old name hid the side effect of the
   check and the fact that it returns a formatted message [N7] (CL p.255).
6. Extract `compactExpectedAndActual`, separating compaction from formatting; the compaction function only
   compacts [G30] (CL p.255).
7. Make the conventions consistent: `findCommonPrefix`/`findCommonSuffix` now return values,
   like the last two lines [G11] (CL p.255).
8. More precise member names (`prefixIndex`, `suffixIndex`), since they are indexes [N1] (CL p.256).
9. Expose the hidden temporal coupling: `findCommonSuffix` depends on `prefixIndex` already being computed; first
   the author passes the index as a parameter [G31] (CL p.256).
10. Dissatisfied: the parameter became arbitrary and another programmer could undo it [G32]; the final solution
    creates `findCommonPrefixAndSuffix`, which calls `findCommonPrefix` first of all, expressing the order
    (CL p.257).
11. Clean up `findCommonPrefixAndSuffix` with `charFromEnd` and `suffixOverlapsPrefix`; this reveals that the
    suffix "index" is actually a length starting at 1, the origin of the many `+1`s [G33] (CL p.257-258).
12. Replace the `+1`s with a single `-1` in `charFromEnd` and adjust `suffixOverlapsPrefix`; renaming to
    `suffixLength` greatly improves reading (Listing 15-4, temporary) (CL p.258-259).
13. An `if` in `compactString` now seemed to require an operator change; analysis showed that before it
    was never true. The two `if`s were commented out, the tests passed, and they were removed (CL p.259).
14. Small final cleanups shown directly in the result (Listing 15-5) (CL p.260).

## Ch. 17 heuristics cited in Ch. 15
| Code | Heuristic (name in Ch. 17) | Use in ComparisonCompactor | Page |
|---|---|---|---|
| N6 | Avoid encodings | remove the `f` prefix from members | CL p.253 |
| G28 | Encapsulate conditionals | the initial condition becomes a named method | CL p.254 |
| N4 | Unambiguous names | locals vs. members with the same name | CL p.254 |
| G29 | Avoid negative conditionals | `canBeCompacted` | CL p.254 |
| N7 | Names should describe side-effects | `compact` becomes `formatCompactedComparison` | CL p.255 |
| G30 | Functions should do one thing | separate compacting from formatting | CL p.255 |
| G11 | Inconsistency | functions that return x vs. that assign | CL p.255 |
| N1 | Choose descriptive names | `prefixIndex`/`suffixIndex` | CL p.256 |
| G31 | Hidden temporal couplings | prefix-before-suffix order | CL p.256 |
| G32 | Don't be arbitrary | parameter passed only to enforce order | CL p.257 |
| G33 | Encapsulate boundary conditions | the scattered `+1`s | CL p.258 |

Heuristic names checked against Ch. 17 (CL p.283-308); the OCR of p.255 reads "G3()" and "CIII", the image
shows [G30] and [G11].

## Result and lessons
- The final module separates analysis functions (first) and synthesis functions (after), organized topologically:
  each declaration appears right after its use (CL p.262).
- The author reversed earlier decisions (put extracted methods back into `formatCompactedComparison`,
  inverted the sense of `shouldNotBeCompacted`); this is typical (CL p.262).
- Refactoring is an iterative process of trial and error that converges on something worthy of a professional;
  one refactoring leads to another that undoes the first (CL p.262).
- Conclusion: the Boy Scout Rule was fulfilled; the authors did excellent work, but no module is
  immune to improvement and each of us has a duty to leave the code a little better (CL p.262).
- `[inference]` Practical use: refactoring good code is legitimate when there are tests with high coverage
  (p.251) and small verified steps (p.259).

## Examples from the book (what each listing shows)
- 15-1 (p.249-250): `ComparisonCompactorTest` (JUnit 3, `extends TestCase`), cases of common prefix/suffix,
  overlap, nulls and context.
- 15-2 (p.251-252): the original `ComparisonCompactor`, with fields prefixed by `f`.
- 15-3 (p.252-253): a deliberately worse version (names such as `s1`, `pfx`, `sfx`, `ctxt`) for contrast.
- 15-4 (p.258-259): temporary version with `suffixLength`, `charFromEnd`, `suffixOverlapsPrefix`.
- 15-5 (p.260-262): final version; `compact` builds the result by concatenating ellipses, context and delta.

## What the chapter does NOT say / common confusions
- It does not say the original code was bad; it praises the authors and calls it well partitioned (CL p.251, p.262).
- It does not present the refactoring as linear: it admits back-and-forth (CL p.257, p.262).
- The header "Testes de Unidade" (Unit Tests) on the pages does not indicate that the chapter deals with unit tests in
  general; that is Ch. 9 (a header error of the edition) `[inference]`.
- The book spells "Eric Gamma"; the correct name of the JUnit co-author is Erich Gamma `[extrapolation]` (CL p.249).

## [DATED]
- JUnit 3 (`TestCase`, `testXxx` methods) and `Assert.format` internals of the time; the `ComparisonCompactor`
  of current JUnit differs `[extrapolation]`.
- The justification for abandoning the `f` prefix ("today's environments") was already valid in 2008 and still holds (CL p.253).
