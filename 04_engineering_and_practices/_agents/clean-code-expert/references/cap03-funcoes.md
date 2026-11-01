# Chapter 3: Functions

Source: CL ch. 3, PDF p.40-58 and p.398 (opening on p.40; text through p.56; Listing 3-7 on p.57-58).
Printed page 42 of the chapter is out of place in the PDF, on p.398: it sits between p.50 and p.51.
The end of Listing 3-7 (printed p.51) is not in the scan.

## Small!
- First rule: functions should be small; second: smaller than that (CL p.43).
- The author admits to having no research to prove this; he relies on four decades of experience (monsters of
  3,000 lines, many of 100 to 300, others of 20 to 30) (CL p.43).
- Numbers from the book (CL p.43):
  - in the 1980s, "no larger than the screen" (VT100: 24 lines x 80 columns, 4 used by the editor);
  - line: up to 150 characters;
  - function: at most 20 lines, according to the printed translation;
  - in Kent Beck's *Sparkle* program (1999), each function was two, three, or four lines long, and that is the
    size the author recommends.
- Listing 3-2 is already too long; it should shrink to Listing 3-3 (CL p.43-44).

## Blocks and indenting
- Blocks of `if`, `else`, `while`, etc. should be one line long, probably a function call with a
  descriptive name (CL p.44).
- Functions should not have large nested structures: the indentation level should be at most one or two
  (CL p.44).

## Do one thing
- "FUNCTIONS SHOULD DO ONE THING. THEY SHOULD DO IT WELL." (and only it); the advice is 30 years old or more
  (CL p.44).
- Criterion: a function does one thing if its steps are one level of abstraction below the name, describable
  in a "TO" paragraph (LOGO style) (CL p.44-45).
- Another test: if you can extract from it another function with a name that is not merely a restatement of its
  implementation, it does more than one thing (heuristic G34) (CL p.45).
- A function divided into sections (declarations, initializations, selection...) does more than one thing; the example is
  `generatePrimes`, in Ch. 4 (CL p.45; listing on CL p.77).

## One level of abstraction per function
- All statements in a function should be at the same level of abstraction (CL p.45).
- Mixing levels (`getHtml()`, `PathParser.render(...)`, `.append("\n")`) confuses the reader about what is
  essential and attracts more details, like broken windows (CL p.45).

## Reading code from top to bottom: the stepdown rule
- Code should read from top to bottom like a narrative: each function followed by those at the next level of
  abstraction, like a series of TO paragraphs; the book calls this the Stepdown Rule (the printed Portuguese calls it "Regra Decrescente") (CL p.46).
- It is hard to learn, but it is the secret to keeping functions short and doing only one thing (CL p.46).

## Switch statements
- It is hard to make a small `switch` or one that does only one thing: by nature it does N things (CL p.46).
- The `calculatePay` example with a `switch` on the employee type: it is large, grows with new types, does
  more than one thing, violates SRP and OCP, and worst of all: other functions will repeat the same structure
  (`isPayday`, `deliverPay`) (CL p.47).
- Solution: hide the `switch` in an ABSTRACT FACTORY that creates the `Employee` subclasses; the rest of the
  system uses polymorphism (CL p.47).
- The author's general rule: `switch` is tolerable if it appears once, to create polymorphic objects, hidden
  behind inheritance (heuristic G23); he admits exceptions (CL p.47).

## Use descriptive names
- `testableHtml` became `SetupTeardownIncluder.render`; private methods such as `isTestable`,
  `includeSetupAndTeardownPages` (CL p.48).
- It returns to Ward's principle: each routine should be pretty much what you expected (CL p.48).
- The smaller and more focused the function, the easier it is to name (CL p.48).
- A long descriptive name is better than a short enigmatic name and better than a long comment (CL p.48).
- Try several names; IDEs such as Eclipse and IntelliJ make renaming easy; hunting for names often leads
  to restructuring the code (CL p.48).
- Be consistent: the same phraseology in the names within a module (`includeSetupPages`,
  `includeSuiteSetupPage`...) (CL p.48).

## Function arguments
- Ideal number: zero; then one (monadic), then two (dyadic); avoid three (triadic); more than three
  (polyadic) requires very special justification and even then should not be used (CL p.48).
- Arguments take conceptual effort and complicate testing: with more than two, testing all the combinations
  is daunting (CL p.48-49).
- Output arguments are even harder to understand than input arguments (CL p.49).
- Common monadic forms (CL p.49):
  - asking a question about the argument (e.g., `fileExists("MyFile")`);
  - transforming the argument and returning the result (e.g., `fileOpen` returns an `InputStream`);
  - event: input with no output, alters the system state; use with caution and make clear it is an event.
- Avoid monads outside these forms; a transformation should appear in the return value, not in an output
  argument (`transform(in)` that returns is better than `void transform(out)`) (CL p.49).
- Flag arguments are ugly: passing a boolean announces that the function does one thing if true and
  another if false; split it (e.g., `renderForSuite()` and `renderForSingleTest()`) (CL p.49-50).
- Dyads: harder than monads (`writeField(outputStream, name)`); acceptable when the two form
  one value (`new Point(0,0)`); even `assertEquals(expected, actual)` has the ordering problem; convert
  to a monad when you can (method of the object, field of the class, new class such as `FieldWriter`) (CL p.50).
- Triads: much harder; think hard before creating one; `assertEquals(message, expected, actual)` is
  problematic; `assertEquals(1.0, amount, .001)` is a triad worth having (CL p.50; CL p.398).
- Argument objects: if it needs more than two or three, group them into a class
  (`makeCircle(Point center, double radius)`) (CL p.398).
- Argument lists: variable arguments treated equally amount to a single list argument;
  `String.format` is a dyad; the same rules apply (CL p.398).
- Verbs and keywords: in a monad, function and argument form a verb/noun pair (`write(name)`,
  better `writeField(name)`); in the keyword form, the argument names go into the function name
  (`assertExpectedEqualsActual`) (CL p.398; CL p.51).

## Have no side effects
- Side effects are lies: the function promises one thing and secretly does others (CL p.51).
- Example: `checkPassword` that calls `Session.initialize()` creates temporal coupling; if unavoidable,
  the name must say so (`checkPasswordAndInitializeSession`), although this violates "do one thing" (CL p.51-52).

## Output arguments
- `appendFooter(s)` forces you to look at the signature, which is equivalent to rereading (CL p.52).
- In OO, `this` plays the role of output: `report.appendFooter()`; avoid output arguments and change the state
  of the owning object (CL p.52).

## Command query separation
- A function should do something or answer something, not both: either it changes state or it returns information (CL p.52).
- `set(attribute, value)` that returns a boolean produces an ambiguous `if (set(...))` (verb or adjective?); split into
  `attributeExists` and `setAttribute` (CL p.52-53).

## Prefer exceptions to returning error codes
- Returning an error code slightly violates command query separation and generates nesting, since the caller
  has to handle the error right away (CL p.53).
- With exceptions, error handling is separate from the main path (CL p.53).
- Extract try/catch blocks into their own functions: one function handles errors, another does the work
  (`delete`, `deletePageAndAllReferences`, `logError`) (CL p.54).
- Error handling is one thing: if `try` exists, it should be the first statement and nothing should come after
  the catch/finally blocks (CL p.54).
- An `Error` enum with all the codes is a dependency magnet: changing it requires recompiling and redeploying
  everything, which is why people reuse old codes; new exceptions derive from the exception class without
  that (CL p.54-55).

## Don't repeat yourself
- The algorithm repeated four times in Listing 3-1 (SetUp, SuiteSetUp, TearDown, SuiteTearDown) was
  eliminated with the `include` method of Listing 3-7 (CL p.55).
- Duplication may be the root of all evil in software; Codd's normal forms, OO, structured programming,
  AOP, and components are strategies against it (CL p.55).

## Structured programming
- Dijkstra: every function and every block with one entry and one exit, that is, one `return`, no `break`/`continue`
  in a loop, and never `goto` (CL p.55).
- For small functions these rules help little: multiple `return`, occasional `break` or `continue`
  can even be more expressive; `goto` only makes sense in large functions, so avoid it (CL p.55-56).

## How do you write functions like this?
- Writing code is like writing prose: a clumsy first draft, then refining (CL p.56).
- The author starts with long, nested functions with many arguments and arbitrary names, but with unit tests
  covering every line; then he splits, renames, eliminates duplication, always with the tests
  passing (CL p.56).
- He states that he does not apply the rules from the start and does not think that is possible (CL p.56).

## Conclusion
- Functions are the verbs and classes the nouns of the domain language the programmer builds; the
  goal is to tell the story of the system (CL p.56).

## Examples from the book
- Listing 3-1 `HtmlUtil.java` (FitNesse 20070619), long `testableHtml` function with several levels
  (CL p.41-42).
- Listing 3-2, refactored to nine lines; Listing 3-3, refactored again (CL p.42, p.44).
- Listing 3-4 `Payroll.java` with `switch` and Listing 3-5 with the abstract class `Employee` (the scan
  shows only the `Employee` class part) (CL p.47).
- Listing 3-6 `UserValidator.java`, side effect `Session.initialize()` (CL p.51).
- Examples of nested error codes x extracted try/catch (CL p.53-54).
- Listing 3-7 `SetupTeardownIncluder.java`, final version (CL p.57-58, incomplete in the scan).

## What the chapter does NOT say / common confusions
- It does not use the name or the acronym "DRY" in Ch. 3: the topic is called "Don't repeat yourself" in the printed Portuguese as "Evite repetição" (CL p.55). The acronym DRY
  appears in other chapters (CL p.178, p.284, p.324).
- It does not use the terms "SOLID", "Command Query Separation", or "CQS"; it uses "Separação comando-consulta"
  (command-query separation) (CL p.52).
- It does not forbid multiple `return`: it says that in small functions they do not cause problems (CL p.55-56).
- It gives no research basis for function size; it is declared personal experience (CL p.43).
- It does not forbid `switch`: it tolerates one per type, hidden in a factory (CL p.47).
- It does not say to apply the rules in the first version; it says the opposite (CL p.56).
- The 20-line limit comes from the printed translation ("no máximo" — "at most"); the book also recommends 2 to 4 lines
  (CL p.43).

## [DATED]
- Examples in Java with `StringBuffer`, 2007 FitNesse, and JUnit; `assertEquals` with a message as the first
  argument is the JUnit 3/4 signature [extrapolation] (CL p.41, p.43, p.50).
- VT100 screens and the "one screen" limit are historical references in the text itself (CL p.43).
- The argument about the `Error` enum depends on recompiling and redeploying Java classes (CL p.55).
