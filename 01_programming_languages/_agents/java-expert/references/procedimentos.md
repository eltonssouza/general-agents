# Procedures and checklists by task (Java)

Basis: Think Java 6.1.3 (Think; introductory, Java SE 8) and Advanced Java (Adv; Java 7/8). Each procedure gives: when to use, steps, how to verify, pitfalls, source and origin. Marks used:

- **[introductory]** = comes from Think; **[advanced]** = comes from Adv.
- **[DATED]** / **[DEPENDS ON VERSION]** = the source ties the practice to Java 7/8 or to a tool/path of that era. Before applying on a newer JDK, confirm in the official documentation of the version in use.
- **package heuristic, basis: (source p.N)** = item written by this package from the source; not book text.
- **[inference]** = link made by this package between two passages of the sources.
- **[extrapolation]** = knowledge external to the sources.

## Contents

1. Write-compile-run cycle and support tools
2. Automatic verification: redirection, Checkstyle, JUnit
3. Debugging: compilation, runtime and logic; when you are stuck
4. Data input with Scanner (including validation)
5. Methods: define, call, develop, encapsulate and generalize
6. Writing a simple class (constructors, encapsulation, toString)
7. Implementing equals and hashCode correctly
8. Designing an immutable class
9. Exceptions and resources (try-with-resources, custom exception)
10. Arrays and strings
11. Exercise algorithms: binary search, Deck, Crazy Eights
12. Beginner code review
13. Advanced code review
14. Basic concurrency and thread-safety checklist
15. Other advanced procedures (clone, singleton, enum, annotation, serialization, programmatic compilation, processors, agents)
16. Known gaps in the sources

---

## 1. Write-compile-run cycle and support tools [introductory]

**When to use:** when creating or changing any program, from the first one.

**Steps**
1. Write the public class in a file with the same name (for example `Hello.java`) (Think p.24). Minimal skeleton: public class with `public static void main(String[] args)` calling `System.out.println("Hello, World!")` (Think p.23).
2. Compile: generates the bytecode; then run on the JVM (Think p.22).
3. From the command line: go to the directory (`cd`), list (`ls`), `javac Hello.java` (accepts one or more file names; produces `Hello.class`) and `java Hello` (takes a single class name, without extension) (Think p.254).
4. To be sure which version of the program is running, change or add a `print` and check the output (Think p.31).
5. Work in increments: start from a program that compiles and runs, add a few statements at a time, print intermediate values, compile and run before continuing (Think p.28, p.48).

**How to verify:** the output shows the change just made; the compilation error, if any, points to the last modification.

**Pitfalls**
- The main text does not detail commands; it refers to Appendix A (DrJava and command line) (Think p.15, p.30).
- Same class name and file name: a mismatch prevents compiling (Think p.24).

**Source/origin:** Think p.15, 22-24, 28, 30, 31, 48, 254 [introductory]. DrJava and the appendix routine are **[DEPENDS ON VERSION]** (Java 8 book).

**To see the library source code (Think p.182):** locate the JDK's `src.zip` (Linux, for example under `/usr/lib/jvm/openjdk-8/`, which may require installing the `openjdk-8-source` package; macOS under `/Library/Java/JavaVirtualMachines/jdk.../Contents/Home/`; Windows under `C:\Program Files\Java\jdk...\`) and open, for example, `java/awt/Point.java`. **[DEPENDS ON VERSION]**: the paths cited are from JDK 8.

---

## 2. Automatic verification: redirection, Checkstyle, JUnit [introductory]

### 2.1 Testing by redirection (Think p.255-257)
**When to use:** a program that reads from `System.in` and prints, to repeat the same case every time.
1. Create `test.in` (input, for example `193.04`) and `test.exp` (expected output, for example `193.04 cm = 6 ft, 4 in`) next to chapter 3's `Convert.java` (Think p.255).
2. Run `java Convert < test.in > test.out`: `<` sends the file to `System.in`; `>` writes `System.out` to a file (Think p.255-256).
3. Compare: `diff test.exp test.out`. No output means no difference (Think p.256).
4. Graphical comparison tools cited: WinMerge (Windows), opendiff (Mac, with Xcode), meld (Linux) (Think p.257).

**Pitfall:** the expected file may also be wrong (Think p.256-257).

### 2.2 Checkstyle (Think p.257)
1. Download the JAR of the latest version, place it in the program's folder.
2. Run `java -jar checkstyle-*-all.jar -c /google_checks.xml *.java`.
3. Read the output (file:line:column and the problem, for example a missing Javadoc comment).
4. Alternative rules: `/sun_checks.xml` or your own configuration file; `/google_checks.xml` is inside the JAR.
**[DATED]**: the download address and the JAR name reflect the book's era; confirm in the current documentation.

### 2.3 JUnit (Think p.260-261)
1. Name the test class with the suffix `Test` (`Series` becomes `SeriesTest`) and the method with the prefix `test` (`fibonacci` becomes `testFibonacci`) (Think p.260).
2. The class extends `junit.framework.TestCase` and uses `assertEquals(expected, actual)`; equal values produce no output, different ones produce a detailed message. Also cited: `assertNull`, `assertSame`, `assertTrue` (Think p.260-261).
3. In DrJava: File > New JUnit Test Case creates the class; the Test button runs; a green bar indicates success; otherwise it leads to the first failed assertion (Think p.261).
**[DATED]**: the `TestCase` style shown is that of old JUnit; the naming convention is what the text teaches.

---

## 3. Debugging [introductory]

**When to use:** the program does not compile, crashes at runtime or produces a wrong result.

### 3.1 Classify the bug
Always state the type: compile-time, runtime or logic (classification in Think p.271; also p.43, p.45–46; ask the helper for the bug type: Think p.283).

### 3.2 Compilation error (Think p.43-44; checklist C.1, Think p.273)
1. Read the whole message: file, line, description, symbol and location (Think p.43).
2. Look at the indicated line and also the previous one: the error may have occurred before the point where it was detected (Think p.44).
3. Do not take the message literally (Think p.44).
4. Go through the list of nine items (Think p.273):
   1. parentheses and braces balanced and nested; methods inside classes; statements inside methods;
   2. uppercase differs from lowercase;
   3. semicolon at the end of statements and none after braces;
   4. matched quotes; double for strings, single for characters;
   5. in each assignment, compatible types and an assignable left side (variable or array element);
   6. in each call, arguments in the right order and types, on an object of the right type;
   7. value-returning method: use the result; `void` method: do not try to use a result;
   8. instance method: call on an object of the right type; static outside the class: use the class name;
   9. inside a static method, referring to an instance variable (with or without `this`) produces "non-static variable x cannot be referenced from a static context".

**How to verify:** recompile; a fixed error may reveal another hidden one.

### 3.3 Debugger (Think p.258-259; DrJava) **[DEPENDS ON ENVIRONMENT: DrJava]**
1. Set a breakpoint (DrJava: Ctrl+B on the line).
2. Turn on debug mode (Ctrl+Shift+D).
3. Run; the program pauses at the breakpoint and the panel shows the call stack, current method on top.
4. Step line by line with the buttons or use Automatic Trace.
5. Inspect, or even change, variables via the Interactions Pane.
6. Compare what the code does with what is expected; the divergence is the clue.
Shortcuts and panels are DrJava's; other IDEs differ.

### 3.4 Runtime and logic errors
- Print intermediate values in the right places and trace steps (Think p.28, p.48); faced with an exception, print right before the point of failure (Think p.277). In binary search, for example, print `low` and `high` at the start of the loop (Think p.219).
- Reduce: minimal program and smallest input that reproduces the problem (minimal test case: Think p.278; before asking for help: Think p.283).
- Test with known-answer values in `main` (Think p.106–107).
- Regression test by redirection (section 2.1) or JUnit (section 2.3).
- **Bisection (a compilation error that cannot be explained)**, last resort (Think p.274): back up the file; delete about half of the code and recompile; if it compiles, the error was in the deleted part, so restore about half of it and repeat; if it does not compile, the error is in what remains, so delete about half of the rest and repeat; once found and fixed, put the code back little by little. The book says it is ugly, but fast and reliable.

### 3.5 When you are stuck (Think p.282-284)
1. Step away from the computer; reconstruct your reasoning (when did it last work?).
2. Before asking for help: minimal program, smallest input that reproduces, prints in the right places, concise description.
3. Tell the helper: the bug type; what you did last (last lines or the failing test case); error message and indicated excerpt; what you have already tried and learned.
4. Rubber duck: explain the problem out loud to a rubber duck (Think p.283).
5. After fixing: reflect on the type of bug, why it occurred and what would have revealed it faster (Think p.284).

---

## 4. Data input with Scanner [introductory]

**When to use:** reading data from the keyboard.
1. `import java.util.Scanner;` at the start of the file, outside any class (Think p.53).
2. `Scanner in = new Scanner(System.in);` (Think p.53).
3. Prompt for the data with `System.out.print(...)` (Think p.55).
4. Read with `in.nextLine()` (String), `in.nextInt()` (int), `in.nextDouble()` (double) (Think p.53, 55, 60).
5. If reading a number and then a line, consume the remaining line break with an extra `in.nextLine()` (Think p.62).
6. If the input may be invalid, test with `hasNextDouble()` first (Think p.91-92).

**Valid input in a loop (Think p.134-135)**
- With `do-while`: `okay` flag; test `hasNextDouble()`; if invalid, consume the token with `next()` and warn via `System.err`.
- With `while (true)` and `break`: simpler. Consuming the invalid input with `next()` is still necessary; the final read of `nextDouble()` happens after leaving the loop.

**Conversion program (chapter 3 pattern, Think p.60)**
1. Declare variables and constants at the top.
2. Create the `Scanner`.
3. Prompt for and read the value.
4. Convert (cast if the target is `int`; `/` and `%` to separate units).
5. Display with `printf`.

**How to verify:** run with a known case (section 2.1).

---

## 5. Methods: define, call, develop [introductory]

### 5.1 Define and call (Think p.69-75)
1. Signature `public static void name(Type1 a, Type2 b)`: each parameter with its type (Think p.75).
2. Call without types in the arguments: `name(x, y)` (Think p.75).
3. Argument and parameter must have compatible types (Think p.74).
4. A method in the same class does not need the class name; for `Math`, `Math.` is required (Think p.69-70).

### 5.2 Read a method's documentation (Think p.77-79)
Find the package and class at the top; read the narrative and the examples; consult the method table and the detail: signature, description, "Returns" (success) and "Throws" (possible exceptions).

### 5.3 Develop a value method (example `distance`, Think p.106-108)
1. Define inputs (parameters) and output (return type).
2. Write the stub with a provisional `return` and compile.
3. Write a test in `main` with known-answer values.
4. Add one line at a time (dx, dy, sum of squares), with prints to check each value.
5. At the end, replace the provisional `return` with the calculation (`Math.sqrt`), remove the scaffolding and, if it still reads well, condense.

### 5.4 Encapsulate and generalize (multiplication table, Think p.127-131)
1. Make the loop work for a concrete case (multiples of 2 on one line, with `printf("%4d", ...)` and `println()` at the end).
2. Wrap it in a method (`printRow`).
3. Replace the literal 2 with a parameter `n`; then the limit 6 with `cols`.
4. Update all call sites when adding a parameter.
5. Encapsulate the outer loop in another method (`printTable(int rows)`).

Simple recursion (Think p.96): decimal to binary divides by 2 recursively, prints `value % 2` on the way back and ends the line with `println()`.

---

## 6. Writing a simple class [introductory]

**When to use:** modeling a type with state (Think p.190-195).

**Steps**
1. Declare the class and the `private` instance variables, outside any method.
2. Write a no-argument constructor and a value constructor (`this.field = parameter`).
3. Create objects with `new Class(...)` in another class (client).
4. If the client needs the data, add getters and setters.
5. Add `toString` for display.
6. If the class is compared or used in collections by equality: see section 7.
7. If it must not change after creation: see section 8.

**How to verify:** instantiate in a client and print the object; check each constructor.

**Pitfalls:** a parameter named like a field requires the correct `this.` (Adv p.67); an instance field in a static method does not compile (Think p.273).

**Source/origin:** Think p.190-195 [introductory]; Adv p.67 [advanced].

---

## 7. Implementing equals and hashCode correctly [advanced]

**When to use:** a class whose objects will be compared by content or used in hash collections.

**`equals` recipe (Adv p.22-23)**
0. Annotate with `@Override`.
1. If `obj == null`, return `false`.
2. If `this == obj`, return `true`.
3. If `getClass() != obj.getClass()`, return `false`. Do not use `instanceof`, except in a final class.
4. Cast and compare each field, handling `null` in each. In the Java 7 version, this is done with `Objects.equals` (Adv p.27).

**`hashCode` recipe (Adv p.23-24)**
- Use the same fields as `equals`.
- Manual version: constant 31 multiplied by the accumulator, adding the `hashCode` of each field (0 if null) (Adv p.23).
- Lean Java 7 version: `Objects.hash(email, firstName, lastName)` (Adv p.27).

**How to verify**
- **package heuristic, basis: (Adv p.22-24):** check that the fields listed in `equals` and in `hashCode` are the same; test with a `null` object, with the same object, with an object of another class and with `null` fields.
- For objects of classes with mutable fields used as keys, treat it as a risk; the source does not detail it, see section 16.

**Pitfalls**
- The recipe asks for `getClass()` and reserves `instanceof` for a final class (Adv p.23); the book says `instanceof` can cause problems in class hierarchies (Adv p.23), and calling this an asymmetry is an [inference]. Caution: Think's `equals(Time that)` (p.199) takes `Time`, not `Object`, and is therefore an overload, not an override ([inference] from the distinction in Adv p.60–61).
- `hashCode` without null fields handled (Adv p.23).
- Think's `equals(Time that)` (p.199) takes `Time`, not `Object`; linking this to the overloading described in Adv p.60–61 (a parameter of a different type creates an overloaded version, not an override) is an [inference]. Adv's recipe uses `Object` and `@Override` (Adv p.22).
- Violating the `equals` rules can cause odd, hard-to-diagnose problems that the compiler does not prevent (Adv p.22); the text does not describe the symptom. Associating them with hash-based collections is an [extrapolation].
- `Objects.equals` / `Objects.hash` are cited as a Java 7 feature: **[DEPENDS ON VERSION]** (Java 7/8 book).

**Source/origin:** Adv p.22-24, 27 [advanced].

---

## 8. Designing an immutable class [advanced]

**When to use:** a value object that must not change after construction.

**Checklist (Adv p.31-32)**
1. All fields `final`.
2. In the constructor, do not assign received arrays or collections directly; copy (`Arrays.copyOf`, `new ArrayList<>(...)`).
3. Collection getters return an immutable view (`Collections.unmodifiableXxx`).
4. Array getters return a copy, the only way to guarantee real immutability. The cost depends on size and may pressure the GC: a practical decision.
5. Fields referencing other classes: those must also be immutable, but Java has no way to enforce this.
6. Use static analyzers (FindBugs, PMD) to catch common flaws. **[DATED]**: tools cited at the time of the book.

**How to verify:** try to change the state through any public method or through the reference received in the constructor; if anything changes, the class is not immutable. **package heuristic, basis: (Adv p.31-32).**

**Pitfalls**
- Copying only on input or only on output (items 2 to 4).
- A final field pointing to a mutable class (item 5).

**Source/origin:** Adv p.31-32 [advanced].

---

## 9. Exceptions and resources [advanced]

**When to use:** any code that opens a resource or can fail in a recoverable way.

### 9.1 Steps
1. Check whether a suitable standard exception already exists (Adv p.76).
2. Do not ignore an exception in `catch` without a log; the only exception accepted by the book is a failure of `close()` (Adv p.73, 75).
3. Close resources with try-with-resources (Adv p.75).
4. Document exceptions with `@throws`; informative message; preserve the cause when rethrowing (Adv p.77-78).

### 9.2 Writing a custom exception (Adv p.76-77)
1. Extend `RuntimeException`; declare `serialVersionUID` (the example declares it) (Adv p.77).
2. Provide constructors: empty, with message, with message and cause (Adv p.77).
3. Throw with a message useful for production troubleshooting (Adv p.77).

**How to verify:** force the failure and read the message and cause in the log; check that the resource was closed on the error path too. **package heuristic, basis: (Adv p.75, 77-78).**

**Pitfalls**
- Swallowing an exception without logging (Adv p.73).
- Losing the original cause when rethrowing (Adv p.77-78).

**Source/origin:** Adv p.73-78 [advanced]. Think covers "Throws" in method documentation (Think p.77-79) [introductory].

---

## 10. Arrays and strings [introductory and advanced]

### 10.1 Arrays (Think)
- Create an array and histogram: `int[] counts = new int[100];` and `counts[score]++` for each element (Think p.141, p.150–151).
- Size: `length` is the array's built-in constant, with no parentheses or arguments (`a.length`, Think p.146); creating with a negative size throws `NegativeArraySizeException`, and zero elements is allowed (Think p.142). `println(a)` shows something like `[I@bf3f7e0`; `Arrays.toString(a)` shows the elements (Think p.144).
- Command-line arguments: `java Max 10 -3 55 0 14`; `args` is `String[]`; convert with `Integer.parseInt` per element; without arguments, `args` comes empty (`java Max`) (Think p.165-166).
- Balanced parentheses (exercise 9.3, Think p.168-169): walk the string, `count++` for `(` and `count--` for `)`; the statement asks to encapsulate, generalize and test with balanced and unbalanced strings.
- Received array assigned to a field without copying: see section 8 item 2 (Adv p.31).

### 10.2 Strings (Adv)
- Building in a loop: use `StringBuilder` (Adv p.69).
- Formatting with `String.format`: specifiers must match the arguments (Adv p.69-70).
- A possibly null wrapper passed to a primitive is a risk (Adv p.68).

**How to verify:** test an empty array, an empty string, input at the limits. **package heuristic, basis: (Think p.165-166, p.168-169).**


---

## 11. Exercise algorithms [introductory]

### 11.1 Binary search (Think p.218-220)
Iterative: `low = 0`, `high = length - 1`; while `low <= high`: `mid = (low + high) / 2`; compare with `compareTo`; if 0, return `mid`; if the middle card is less than the target, `low = mid + 1`; otherwise `high = mid - 1`; on leaving the loop, return -1 (Think p.218). Recursive: replace the `while` with `if (high < low) return -1;` and call with the new bounds (Think p.220). Trace by printing `low` and `high` at the start of the loop (Think p.219). Natural prerequisite: a sorted collection (**[inference]** from the use on a sorted deck).

### 11.2 Implementing `Deck` (Think p.223-232)
1. Field `private Card[] cards`; one constructor with `n` creates only the array (`null` elements); another creates 52 cards with two nested `for` loops (suit 0 to 3, rank 1 to 13) and a separate `index` (Think p.223-224).
2. Shuffle: for each `i`, a random integer and a swap. Helpers `randomInt(low, high)` (inclusive at both ends; do not create a `Random` on each call) and `swapCards(i, j)` (Think p.225, 231).
3. Sort: for each `i`, find the lowest card to the right (`indexLowest`) and swap with `i` (Think p.226).
4. Merge of sorted `d1` and `d2`: new result; indices `i`, `j` and `k`; if one subdeck is exhausted, the other wins; otherwise compare; the winner goes to `k` (Think p.228-229).
5. `mergeSort`: 0 or 1 card returns; divide, sort each half, interleave (Think p.230). Test `almostMergeSort` first, with selection sort on the halves (Think p.229, 232).
6. `subdeck(low, high)`: new `Deck` of size `high - low + 1` with copies of the references (Think p.227).

### 11.3 Crazy Eights (Think p.233, 242-247)
- Rules: play a card that matches in rank or suit, or an eight (wild); with no valid card, draw until one is found; empty draw pile: shuffle the discard pile (except the top); final penalties: eight 20, face cards 10, others by value (Think p.233).
- `Eights` pieces, from the bottom up: constructor (shuffled deck, 5 cards per player, 1 to the discard pile, rest to the draw pile, `Scanner`), `isDone`, `reshuffle`, `draw`, `nextPlayer`, `displayState`, `waitForUser`, `takeTurn`, `playGame` (Think p.244-247).
- `Player.play`: `searchForMatch` (first legal card, removed with `popCard(i)`, or `null`) and, with no match, `drawForMatch` (draws until it matches) (Think p.242-243).

**How to verify:** test the part before the whole (first `almostMergeSort`; small decks); trace with prints.

---

## 12. Beginner code review [introductory]

**When to use:** reviewing a student program or simple basic Java code.

Items extracted from the sources (each based on the passages):
1. Skeleton: public class in the file of the same name; `main` with the correct signature (Think p.23-24).
2. The nine compilation-error items of section 3.2 (Think p.273).
3. Input: `Scanner` imported outside a class; prompt before reading; extra `nextLine()` after `nextInt`/`nextDouble` when necessary; `hasNextDouble()` before reading error-prone input (Think p.53, 55, 62, 91-92).
4. Methods: argument types compatible with the parameters; result of a value method used; call without types in the arguments (Think p.74-75, 273).
5. Development in increments, with a stub and a test in `main` (Think p.106-108).
6. `private` attributes, constructors, `toString` (Think p.190-197).
7. Repeated loops encapsulated and generalized (Think p.127-131).
8. Style by Checkstyle and tests by redirection or JUnit (sections 2.1 to 2.3).

**package heuristic, basis: (Think p.28, 48, 106-108, 127-131, 273):** these items are a list organized by the package from scattered procedures; the book does not provide a review list of this form.

---

## 13. Advanced code review [advanced]

**When to use:** reviewing library classes, models, services or concurrent code.

### 13.1 Method review (summary of chapter 6, Adv p.65)
- Validate arguments and do sanity checks.
- Avoid `null` as a return.
- Design immutable methods when it makes sense.
- Use visibility rules to hide what should not be public.

### 13.2 API method checklist (Adv p.58–59, p.62–64)
Meaningful name; fewer than 6 arguments; short, readable method; Javadoc on public ones, with preconditions and examples; validate inputs; do not return `null` for collections.

### 13.3 Java code review (derived from chapters 7 and 8)
1. Local variable or parameter with the same name as a field? Is the `this.` correct? (Adv p.67)
2. Is any parameter reassigned? Make it `final` and use a local (Adv p.67-68).
3. Possibly null wrapper passed to a primitive? (Adv p.68)
4. Strings built in loops use `StringBuilder`? `String.format` with consistent specifiers? (Adv p.69-70)
5. Do names follow the conventions? (Adv p.70)
6. Does any `catch` ignore an exception without a log? (accepted exception: failure of `close()`) (Adv p.73, 75)
7. Resources closed by try-with-resources? (Adv p.75)
8. Exceptions documented with `@throws`; informative message; cause preserved when rethrowing? (Adv p.77-78)

### 13.4 Items by area (package heuristic)
- Equality: section 7 (basis: Adv p.22-24). Immutability: section 8 (basis: Adv p.31-32). Copy and singleton: section 15 (basis: Adv p.17-18, 25-26). Annotations: `@Retention` and `@Target` defined (basis: Adv p.52-55). Concurrency: section 14 (basis: Adv p.81-83, 87).

**Version mark:** the content is Java 7/8; `@Repeatable` is described as Java 8 (Adv p.52-55) **[DEPENDS ON VERSION]**.

---

## 14. Basic concurrency and thread-safety checklist [advanced]

**When to use:** when launching tasks in parallel or protecting shared state.

### 14.1 Executor with a result (Adv p.81-82)
1. Create the pool with `Executors` (for example `newFixedThreadPool(n)`) (Adv p.81).
2. `submit` a `Callable`, keeping the `Future` (Adv p.82).
3. `get` with timeout; handle `TimeoutException` (Adv p.82).

### 14.2 `ReentrantLock` pattern (Adv p.82-83)
- `lock.lock(); try { ... } finally { lock.unlock(); }`.
- With timeout: `if (lock.tryLock(1, TimeUnit.SECONDS)) { try { ... } finally { lock.unlock(); } }`; the method must handle `InterruptedException` (in the example, `throws InterruptedException`).

### 14.3 Diagnosis (Adv p.87)
JDK tools cited: JVisualVM, Java Mission Control and `jstack`, to see threads, states and deadlock. The book warns that reproducing and debugging can take "hours and even weeks". **[DATED]**: tool list from the book's era.

### 14.4 Thread-safety review checklist (package heuristic)
Each item below is the package's wording; the basis indicated is the point in the source it starts from.
1. Does every `lock()` have an `unlock()` in a `finally` immediately after? (basis: Adv p.82-83)
2. Do `tryLock` calls with timeout handle the case of not obtaining the lock and the `InterruptedException`? (basis: Adv p.83)
3. Does `Future.get` have a timeout and handle `TimeoutException`? (basis: Adv p.82)
4. Is the pool created with a defined size and does the task return its result through a `Callable`? (basis: Adv p.81-82)
5. Is state shared between threads immutable, when possible? [inference] from the immutability checklist (Adv p.31-32); the source read does not state that immutability suffices for thread-safety.
6. Lazy singleton: a synchronized `getInstance()` has a concurrency cost; an eager singleton avoids that cost (basis: Adv p.17-18).
7. Is there a plan to diagnose deadlock (thread dump with `jstack`, JVisualVM, Mission Control)? (basis: Adv p.87)

**Pitfalls:** forgetting the `finally` on unlock; forgetting that concurrent debugging is expensive (Adv p.87).

**How to verify:** exercise with several threads and use the diagnostic tools; the source read does not describe concurrency tests (section 16).

---

## 15. Other advanced procedures [advanced]

### 15.1 Singleton (Adv p.17-18)
- Eager: `private static final` field + private constructor + `getInstance()`.
- Lazy: `synchronized` `getInstance()` (concurrency cost).
- Before using, check whether DI solves it better: the text pushes toward DI.

### 15.2 Correct `clone`, when unavoidable (Adv p.25-26)
1. Implement `Cloneable`.
2. Override as `public` with the own type as the return.
3. Call `super.clone()` first.
4. Copy mutable fields (for example `persons.clone()`); the constructor is not called and `final` fields cannot be reassigned, which breaks the solution.
5. Better: a copy constructor or factory.

### 15.3 Enum with data (Adv p.48-50)
`private final` fields, private constructor and getter; optionally implement an interface; values as constructor calls without `new`.

### 15.4 Custom annotation (Adv p.52-55)
Declare `@interface`; attributes (primitives, `String`, `Class<?>`, arrays of these) with or without `default`; `@Retention` (RUNTIME if it is to be read by reflection); `@Target`; `@Inherited` if inheritable by subclasses; `@Repeatable` and a container if repetition is needed (Java 8). **[DEPENDS ON VERSION]** for `@Repeatable`.

### 15.5 Serialization with Serialization Proxy (Adv p.92)
1. Outer class: `writeReplace()` returns `new SerializationProxy(this)`.
2. Outer class: `readObject` throws `InvalidObjectException` (prevents direct deserialization).
3. Proxy (`private static`, `Serializable`, with `serialVersionUID`): copies the fields in the constructor; `readResolve()` rebuilds the outer class through the public constructor.

### 15.6 Compiling programmatically (Adv p.107-109)
`ToolProvider.getSystemJavaCompiler()`; `DiagnosticCollector<JavaFileObject>` and `StandardJavaFileManager` (try-with-resources); `getJavaFileObjectsFromFiles(...)`; `compiler.getTask(null, manager, diagnostics, null, null, sources).call()`; read errors from the collector (message, line, file).

### 15.7 Annotation processor (Adv p.115-119)
Extend `AbstractProcessor` (public no-argument constructor); `@SupportedAnnotationTypes(...)` (accepts `*`) and `@SupportedSourceVersion(...)`; implement `process(...)` with `roundEnv.getElementsAnnotatedWith(...)`; errors via `processingEnv.getMessager().printMessage(Diagnostic.Kind.ERROR, ...)`; return `true` when handling the annotations. Execution: `javac -processor <class> -cp <processors jar> -d <output> <sources>`; in Maven, `maven-compiler-plugin` with `<annotationProcessors>` (example with `source`/`target` 1.7 and plugin 3.1, Adv p.118-119). **[DATED]** regarding the versions.

### 15.8 Java agent (Adv p.120-123)
Class with `premain(String, Instrumentation)` registering a `ClassFileTransformer` via `inst.addTransformer(...)`; in the transformer, compare `className` (separator `/`, not `.`), change the bytecode (Javassist in the example) and return the new array, or `null` otherwise; minimal manifest `Manifest-Version: 1.0` and `Premain-Class: <class>`; run with `java -javaagent:<jar>[=options] ...`.

---

## 16. Known gaps in the sources

- Concurrency tests and general thread-safety rules beyond executor, `ReentrantLock` and diagnosis: not covered in the procedures material; consult other sections of Adv before asserting.
- `equals` with mutable classes as collection keys: not detailed here.
- Build and run commands for Maven or Gradle projects: only the `maven-compiler-plugin` excerpt (Adv p.118-119).
- Modern JUnit: the material provides only the `TestCase` style (Think p.260-261) **[DATED]**.
