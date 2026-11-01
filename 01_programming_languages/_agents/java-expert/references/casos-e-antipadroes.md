# Cases, errors and anti-patterns in Java (Think Java 6.1.3 and Advanced Java)

Quick-reference base: what usually goes wrong, why, how to fix it, and what the books show as examples. Pages are those of each work's PDF: (Think p.N) and (Adv p.N).

## Contents

- Conventions and how to read
- Part 1 — Errors and pitfalls by topic
  - 1.1 Syntax and compilation
  - 1.2 Types, arithmetic and data input
  - 1.3 References and null
  - 1.4 Strings
  - 1.5 Arrays
  - 1.6 Classes and constructors
  - 1.7 Equality
  - 1.8 Inheritance and overriding
  - 1.9 Exceptions
  - 1.10 Generics
  - 1.11 Concurrency
  - 1.12 Serialization, reflection and metaprogramming
  - 1.13 Recursion, loops and diagnosis
- Part 2 — Anti-patterns (what to do instead)
- Part 3 — Illustrative cases and the lesson of each
- Part 4 — Errors in the books themselves (do not reproduce)

## Conventions and how to read

- **Origin:** [introductory] = Think Java (Java SE 8, introductory course); [advanced] = Advanced Java (Java 7/8, best practices and advanced APIs).
- **Era:** "timeless" means the point does not depend on a version. **[DATED]** marks what the book ties to Java 8 or earlier and that may have changed. **[DEPENDS ON VERSION]** marks what holds only from or up to a certain version. [inference] marks a link of mine, with no direct statement in the text. [extrapolation] marks knowledge from outside the sources.
- **Think error messages:** they appear in the "File / [line] / Error:" format, typical of the DrJava environment. Do not treat them as literal `javac` output: the text and the order may differ in another compiler or IDE. Where the book says "something like", the message is only indicative.
- **Adv messages:** only those the text records are included; the book does not identify the tool that emitted them.
- Think contains inconsistencies of its own (see Part 4); Adv is an e-book with editing errors. In case of doubt between a passage in the book and the official documentation for the version in use, the documentation prevails.

---

## Part 1 — Errors and pitfalls by topic

### 1.1 Syntax and compilation

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `Error: ';' expected`, with the correct line indicated | Missing semicolon at the end of the statement | Add `;` | (Think p.44) | [introductory] | timeless |
| `Error: reached end of file while parsing` | A closing brace is missing (e.g., the one for `main`); the compiler only notices at the end of the file | Look for the missing brace, usually before the reported line | (Think p.44) | [introductory] | timeless |
| `Error: cannot find symbol` with `symbol: method pow(double,double)` and `location: class Test` | `pow` called without `Math.`; with no class name, the compiler looks in the current class | Write `Math.pow(...)`; the "location" line is the clue | (Think p.69) | [introductory] | timeless |
| `cannot find symbol` when using `Scanner` | Missing `import java.util.Scanner;` | Add the import | (Think p.53) | [introductory] | timeless |
| `Error: method printTwice in class Test cannot be applied to given types; required: java.lang.String found: int ...` | Argument incompatible with the parameter (`printTwice(17)`); `int` does not automatically become `String` | Pass an argument of the required type | (Think p.74) | [introductory] | timeless |
| Syntax error on `printTime(int hour, int minute);` in the call | Types written in the call are read as declarations | Call with expressions only: `printTime(hour, minute)` | (Think p.75) | [introductory] | timeless |
| Syntax error on `printTime(int hour, minute)` in the definition | Type omitted on the second parameter; the shorthand only applies to variable declarations | Declare the type of each parameter | (Think p.75) | [introductory] | timeless |
| Message "something like" `Bad types in assignment: from double to int` | `double` assigned to `int` (`int x = 1.1;`, `inch = cm / CM_PER_INCH;`) | Cast with `(int)` or change the variable's type | (Think p.39, p.58) | [introductory] | timeless |
| Error when reassigning a `final` variable (exact message not given) | A constant receives a value only once | Remove the reassignment or do not use `final` | (Think p.56) | [introductory] | timeless |
| Error on `minute + 1 = hour;` or `7 = a;` | The left side of an assignment must be a variable | Swap: `hour = minute + 1;`, `a = 7;` | (Think p.43, p.35) | [introductory] | timeless |
| `"Hello" - 1`, `"World" / 123`, `"Hello" * "World"`, `5 < "6"` | Mathematical and relational operators do not apply to incompatible types; between Strings only `+` works | Use operands of compatible types | (Think p.41, p.86) | [introductory] | timeless |
| `=<` or `=>` | These operators do not exist | Use `<=` and `>=` | (Think p.86) | [introductory] | timeless |
| `Int`, `string`, `system`, `SYSTEM`, `Println`, `mian` | Java is case-sensitive | Write `int`, `String`, `System`, `println`, `main` (the text asks the reader to try these errors and does not give the messages) | (Think p.23, p.31–33) | [introductory] | timeless |
| `pi`, `Pi`, `pie` or `Math.PI()` | The constant is `Math.PI`, without parentheses | Use `Math.PI` | (Think p.68) | [introductory] | timeless |
| Variable name equal to a reserved word (`class`, `void`) | Reserved words cannot be used as identifiers | Choose another name | (Think p.34, p.46) | [introductory] | timeless |
| `import` inside the class definition | Imports go at the start of the file | Move to the top | (Think p.53) | [introductory] | timeless |
| Error from a missing or wrongly typed `return` in a value-returning method (exact message does not appear) | The `return` does not match the declared type | Make the expression have the promised type | (Think p.105) | [introductory] | timeless |
| `unreachable statement` | Code after `return` in the same block | Remove the dead code or rearrange the flow | (Think p.105) | [introductory] | timeless |
| Possibly `missing return statement` (the text says "something like") | Not every path ends in `return` (`x < 0` and `x > 0` do not cover `x == 0`) | Ensure `return` on all paths, for example with a final `else` | (Think p.106) | [introductory] | timeless |
| Error when using the `for` variable `i` outside the loop | A variable declared in the initializer exists only in the loop | Declare `int i;` before the `for` | (Think p.133) | [introductory] | timeless |
| `non-static variable x cannot be referenced from a static context`; also the term "non-static" in other messages | Instance variable or method used without an object, in a static method | Use it through an instance | (Think p.273, p.197) | [introductory] | timeless |
| Dozens of cascading errors | The compiler gets lost after the first error | Only the first message is reliable: fix one error and recompile | (Think p.272) | [introductory] | timeless |
| The compiler insists on an error you cannot see | There are two copies of the file: one is edited and the other is compiled | Insert an obvious syntax error at the top; if it is not detected, the environment is misconfigured | (Think p.274) | [introductory] | timeless |
| "Class Golfer must be declared abstract..." | `compareTo` with an `Object` parameter is missing; the compiler's suggestion (make the class abstract) is not the fix | Implement `compareTo` with the required signature; do not blindly follow the suggestion | (Think p.274–275) | [introductory] | **[DATED]** (message with `Comparable` without generics) |

### 1.2 Types, arithmetic and data input

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `minute / 60` gives 0 | Integer division | Make the computation floating-point (`minute / 60.0`) or use `minute * 100 / 60` | (Think p.38–39) | [introductory] | timeless |
| `double y = 1 / 3;` is `0.0` | The integer division happens before the conversion to `double` | `1.0 / 3.0` | (Think p.39–40) | [introductory] | timeless |
| Sum of ten `0.1` gives `0.9999999999999999` | 0.1 is a repeating fraction in binary; floating point is approximate | Use integers when exactness is needed (e.g., cents) (Think p.41); the book says you should probably never use `==` with `double`; compare the difference against a tolerance, such as `Math.abs(d - 1.23) < .000001` (Think p.280). Pp.40–41 explain only the rounding error | (Think p.40–41, p.280) | [introductory] | timeless |
| `(int) pi * 20.0` gives 60.0, not 62.0 | The cast has precedence over `*` and converts only `pi` | Parentheses: `(int) (cm / CM_PER_INCH)` | (Think p.58–59) | [introductory] | timeless |
| `1 + 2 + "Hello"` gives `3Hello`; `"Hello" + 1 + 2` gives `Hello12` | Evaluation from left to right | Parentheses: `"Hello" + (1 + 2)` (deduction; the text only describes the rule) | (Think p.41–42) | [introductory] | timeless |
| `x / 2 * Math.PI` is not x/(2π) | `*` and `/` have the same precedence and proceed from left to right | `x / (2 * Math.PI)` | (Think p.281) | [introductory] | timeless |
| Sine, cosine, tangent with an absurd result | The arguments must be in radians | `Math.toRadians` or `/ 180.0 * Math.PI` | (Think p.68) | [introductory] | timeless |
| `Math.log` does not give the expected logarithm | It is the natural logarithm (base e) | Change base with `Math.log(x) / Math.log(2)` | (Think p.69, p.127) | [introductory] | timeless |
| `nextLine()` returns empty text after `nextInt()` | `nextInt` stops at the non-numeric character and leaves the line break in the stream | Call `in.nextLine();` right after `nextInt()` or `nextDouble()` to discard the rest of the line; a String followed by an `int` does not have the problem | (Think p.61–62) | [introductory] | timeless |
| `InputMismatchException` | `nextDouble()` with input that is not a number (the book's example; extending it to `nextInt()` is [inference]) | Test with `hasNextDouble()` and handle the case | (Think p.91–92) | [introductory] | timeless |
| `NoSuchElementException`, `IllegalStateException` in `nextInt()` | Input exhausted; `Scanner` already closed | Know the method's documented exceptions | (Think p.79) | [introductory] | timeless |
| `printf` with `%f` for `int`, `%d` for `double`, or more specifiers than values | The compiler does not check the format string; the exact errors are not given | Check the format; the text tells the reader to experiment | (Think p.64) | [introductory] | timeless |
| `printf` without a line break | `printf` does not add `\n` | Put `\n` at the end of the format | (Think p.57) | [introductory] | timeless |
| "Wrong" factorial from about 15 | The text asks why without answering; it suggests `BigInteger` as the solution | `BigInteger.valueOf`, `add`, `multiply`, `pow`; arithmetic operators do not work with it | (Think p.185–187) | [introductory] | timeless |
| `x++` is legal with `char`, but `x = x + 1` gives an error | Exercise that asks the reader to find the reason, with no answer in the text | Check the documentation/language | (Think p.168) | [introductory] | timeless |
| The value of `max` with empty `args` is the smallest `int` | The initial value is `MIN_VALUE` | Handle `args.length == 0` when that is not desired ([inference] from the text) | (Think p.166) | [introductory] | timeless |
| `int` constants accept any number: `isWeekend(100)` compiles | `int` constants are not type-safe | Use an enum | (Adv p.47–48) | [advanced] | timeless |

### 1.3 References and null

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `NullPointerException` when accessing an attribute or calling a method | The reference is `null`; elements of an object array start as `null` until given a value (e.g., `array[0].x` after `new Point[5]`, `cards[0].rank` before populating the cards) | Find which variable is `null` and how it got that way; ensure an object exists before use | (Think p.179, p.277, p.215) | [introductory] | timeless |
| `NullPointerException` with no apparent cause at the call | Auto-unboxing of a null `Long` to `long` | Prefer the primitive (Adv p.68); checking for `null` before converting is [inference], the book only recommends the primitive | (Adv p.68) | [advanced] | timeless |
| `NullPointerException` does not appear in the signature and is not required in a `catch` | It is an unchecked exception: a subclass of `RuntimeException`; the book gives it as the best-known example and shows its declaration | Fix the cause (`null` reference); do not expect the compiler to point it out | (Adv p.73–74) | [advanced] | timeless |
| Passing or returning `null` does not produce an error by itself | `null` means "no object"; it is legal to pass it as an argument or receive it as a return, and it usually indicates a special condition or error; the error comes when using the value | Handle the value before accessing an attribute or method | (Think p.179) | [introductory] | timeless |
| `NullPointerException` and scattered checks | Method returns `null` for "no value" or for an empty collection | `Optional<T>` for values; empty collection for collections | (Adv p.64) | [advanced] | **[DEPENDS ON VERSION]** (Optional comes from Java 8) |
| Changing an object or array and seeing the change under another name | Assignment copies the reference (alias): `double[] b = a;` | `Arrays.copyOf` or element-by-element copy | (Think p.145) | [introductory] | timeless |
| Output `java.io.PrintStream@685d72cd`, `Time@80cc7c0` or `[I@bf3f7e0` | The default `toString` shows the type and the address in hexadecimal | Override `toString`; for arrays, `Arrays.toString` | (Think p.51–52, p.196, p.144) | [introductory] | timeless |
| Modifying a parameter does not change the caller's variable | Pass by value: the parameter is a copy of the argument | Return the value or change the state of the referenced object. A method that changes the object it receives can make debugging harder, since it is not always clear which calls change the arguments (Think p.177, `Rectangle` example); extending this to arrays is [inference], since an array is also a reference (Think p.145) | (Think p.76, p.177) | [introductory] | timeless |
| Immutability with only `final` on fields | Internal arrays and collections leak state | Defensive copies and unmodifiable views | (Adv p.31–32) | [advanced] | timeless |

### 1.4 Strings

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `StringIndexOutOfBoundsException` on `fruit.charAt(fruit.length())` | Indexes go from 0 to `length - 1` | `charAt(length - 1)` | (Think p.160) | [introductory] | timeless |
| `toUpperCase`, `replace` "do not work" | Strings are immutable; the method returns a new String | Assign the return value: `text = text.replace(...)` | (Think p.159) | [introductory] | timeless |
| Comparison with `==` sometimes gives the wrong answer | `==` compares references; "most of the time" it is right, but it is not correct | `equals` (or `Objects.equals`); Adv example: `new String("bbb") == "bbb"` gives `false` and `equals` gives `true` | (Think p.162–163, p.86; Adv p.26) | both | timeless |
| Sorting puts uppercase before lowercase | `compareTo` and `equals` are case-sensitive ("Ada" before "ada") | Normalize with `toLowerCase` when the order should not depend on case | (Think p.163, p.171) | [introductory] | timeless |
| Error when calling a method on a primitive: `i.equals(5)` with `int i` | Primitives have no methods | Use operators or the wrapper class | (Think p.164) | [introductory] | timeless |
| `for (char letter : fruit)` does not compile | The enhanced for does not accept a String directly | `fruit.toCharArray()` | (Think p.160) | [introductory] | timeless |
| Elements of `args` do not add up as numbers | They are Strings | `Integer.parseInt(arg)` | (Think p.166) | [introductory] | timeless |
| Output without a space or with an unwanted space | The space at the end of the literal was left out (`"Goodbye, "`); a space after `\n` becomes a space at the start of the next line | Check the literals | (Think p.25) | [introductory] | timeless |
| Garbage and inefficiency in text built in a loop | Each concatenation creates an intermediate String | `StringBuilder` or `StringBuffer`; or `String.format` | (Adv p.69–70) | [advanced] | timeless |
| `print` without a final `println` seems to show nothing | In some environments the output is held until the next line break | Close the series with `println` | (Think p.37, p.282) | [introductory] | **[DEPENDS ON VERSION]** (depends on the environment) |
| `println` where `print` was intended splits the output into two lines | Classic logic error of hello world | Use `print` | (Think p.45–46) | [introductory] | timeless |

### 1.5 Arrays

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `NegativeArraySizeException` | Negative size at creation (for example, −4 elements) | Use a non-negative size; an array with zero elements is allowed | (Think p.142) | [introductory] | timeless |
| `a.length()` with parentheses on an array | An array's size is a built-in constant, `length`: it looks like a method call, but there are no parentheses or arguments (the error message is not given). On a String, `length()` is a method | `a.length` for an array; `s.length()` for a String | (Think p.146, p.160) | [introductory] | timeless |
| `ArrayIndexOutOfBoundsException` | Index negative or greater than `length - 1`, including `a[a.length]` | Indexes from 0 to `length - 1`; condition `i < a.length`. To diagnose: print the index and size before the point of failure and follow the assignments backward | (Think p.143, p.146, p.277–278) | [introductory] | timeless |
| The index cannot be found with an enhanced for | The enhanced for does not expose the index | Use the traditional `for` | (Think p.151) | [introductory] | timeless |
| Array of `Card` does not grow | Arrays have a fixed size | Switch to `ArrayList` | (Think p.234) | [introductory] | timeless |
| `[]` does not work on `ArrayList` | `ArrayList` uses methods | `get` and `set` | (Think p.236) | [introductory] | timeless |
| Off-by-one in subarrays | The range `[low, high]` has `high - low + 1` elements | Use that formula | (Think p.227) | [introductory] | timeless |
| Array getter exposes the internal array or copies expensively | Returning the reference leaks state; copying costs GC | Decide case by case (defensive copy vs cost) | (Adv p.32) | [advanced] | timeless |
| Original and clone share internal arrays and collections after `clone()` | `clone` does not call a constructor and copies only the fields | Clone mutable fields or, better, use a copy constructor or factory; a `final` field makes the fix impossible | (Adv p.25–26) | [advanced] | timeless |

### 1.6 Classes and constructors

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| "hour has private access in Time" | Access to a `private` instance variable of another class | Create a getter; making it public is less recommended | (Think p.194) | [introductory] | timeless |
| `return` at the end of the constructor | A constructor does not return a value | Remove the `return` | (Think p.191) | [introductory] | timeless |
| `new Time()` inside the `Time()` constructor | `new` already creates the object before the constructor; the call produces infinite recursion | Just assign the attributes on `this` | (Think p.192) | [introductory] | timeless |
| Assignment "does nothing" when the parameter and the attribute have the same name | The parameter shadows the attribute | `this.attribute = attribute` | (Think p.193) | [introductory] | timeless |
| Wrong result in a method with a local variable with the same name as the field | The local shadows the field and the compiler does not complain (the IDE may warn) | `this.field` or rename the local | (Adv p.67) | [advanced] | timeless |
| Hard-to-follow code | Parameter reassigned as if it were a local | `final` parameter and a new local variable | (Adv p.67–68) | [advanced] | timeless |
| Sum of times returns 20:66 for 18:50 + 2:16 | First draft of `add` without a "carry" | Handle seconds and minutes >= 60; the hour left over above 23 (the text notes that `sum.hour -= 24` would solve it) | (Think p.201) | [introductory] | timeless |
| Naive singleton creates several instances | `instance == null` checked without synchronization | `static final` initialization or `synchronized` | (Adv p.17) | [advanced] | timeless |
| Hard to test because of a dependency created inside the class (e.g., `DateFormat.getDateInstance()` in the field) | Coupling | Receive the dependency through the constructor | (Adv p.19) | [advanced] | timeless |
| Exposing fields directly | Breaks encapsulation | `private` with getters and setters | (Adv p.37) | [advanced] | timeless |

### 1.7 Equality

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `==` on objects gives an unexpected answer | `==` checks identity; the inherited `equals` does too (default `equals` = `==`), in both `Time` and `Card` | Override `equals` for the desired notion of equivalence (the book writes `equals(Card that)` in Think p.212) | (Think p.86, p.198–199, p.212, p.280) | [introductory] | timeless |
| `=` in place of `==` in a comparison | Frequent error | Use `==` | (Think p.86) | [introductory] | timeless |
| Operators `<` and `>` do not work on objects | Relational operators apply to primitives | Define your own `compareTo` | (Think p.212) | [introductory] | timeless |
| Weird problems that are hard to diagnose (the book does not describe the symptom) | Not following the rules of the `equals` contract (reflexive, symmetric, transitive, consistent, `equals(null)` always `false`); the compiler does not enforce the rules (Adv p.22). As for `hashCode`, the book says to override it together with `equals`: equal objects must have the same hash (Adv p.23), without describing a symptom. Linking this to hash-based collections is [extrapolation] | Follow the `equals` recipe and always implement the `equals`/`hashCode` pair | (Adv p.22–23) | [advanced] | timeless |
| Problems in class hierarchies | `instanceof` in `equals` of a non-final class (the book only says it can cause problems in hierarchies; calling this an asymmetry is [inference]) | Use `getClass()`; reserve `instanceof` for a final class | (Adv p.23) | [advanced] | timeless |
| Behavior changes when the field changes | Mutable fields in `equals`/`hashCode` | `final` fields when possible | (Adv p.23–24) | [advanced] | timeless |
| Useless `toString` (`Class@hash`) | Default implementation | Override (e.g., `Person[email=..., first name=..., last name=...]`, or `Arrays.toString` for arrays) | (Adv p.24) | [advanced] | timeless |

### 1.8 Inheritance and overriding

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| Method "does not override": `Child.toObject(Double)` against `Parent.toObject(Number)` | It is an overload, not an override; without `@Override` it compiles with no warning, with `@Override` the compiler reports the error (Adv p.61) | Always use `@Override`; the book says there is no dedicated syntax for marking an override (Adv p.34) | (Adv p.34, p.60–61) | [advanced] | timeless |
| Question: does `Child.toObject(Number)` returning `String` override `Parent.toObject(Number)` returning `Object`? | Yes: the signature differs only in the more specific return type and the book states that this overrides, with no complaint from the compiler; the term it refers to is "Covariant method return types" (section not extracted). It is the parameter type difference (`Double` instead of `Number`) that produces an overload | Use `@Override` so the compiler confirms the intent | (Adv p.60–61) | [advanced] | timeless |
| Choosing between overloaded versions | The compiler chooses the alternative according to the values of the arguments (Adv p.59; Think p.110 says Java chooses by the arguments); the fine rule by declared type is not in the sources | Caution: the book warns that it is easy to debug one version while calling another (Think p.110) | (Adv p.59; Think p.110) | both | timeless |
| Attempt to override a `final` method | Every inherited method can be overridden, except one declared `final` | Do not declare `final` what must be overridden | (Adv p.34, p.38) | [advanced] | timeless |
| Subtle logic error with inheritance | Inherited code runs without being noticed | Read the superclass; prefer composition when it makes sense | (Think p.280; Adv p.36–37) | both | timeless |
| Call `deck.deal(hand, 5)` seems wrong | A subtype (`Hand`) where a `CardCollection` is expected is legal | None; it is polymorphism | (Think p.240) | [introductory] | timeless |
| Interface E, which extends B and C (both override the same default from A), does not compile | Diamond with `default` methods | Override the method in the interface or class that inherits from both | (Adv p.36) | [advanced] | **[DEPENDS ON VERSION]** (Java 8) |
| Deep hierarchies (A, B, C) just to reuse implementation | No multiple inheritance of classes | Interfaces with `default` or composition | (Adv p.35–37) | [advanced] | **[DEPENDS ON VERSION]** (the `default` part) |
| Annotation is not inherited by subclasses | By default there is no inheritance | `@Inherited` (in the example with `@Target(TYPE)`, applied to class annotations) | (Adv p.54) | [advanced] | timeless |

### 1.9 Exceptions

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `Exception in thread "main" java.lang.ArithmeticException: / by zero`, followed by `at Hello.main(Hello.java:5)` | Integer division by zero | Read: exception name, message, method, file and line (Think p.45). The line of the failure may not be the one that needs fixing (Think p.45). `ArithmeticException` is also described as an error in an arithmetic operation (Think p.278) | (Think p.45, p.278) | [introductory] | timeless |
| `FileNotFoundException` | File not found | In a project-based IDE (such as Eclipse), import the file; otherwise, check existence and path | (Think p.278) | [introductory] | timeless |
| Swallowed exception | Empty `catch` block | At the very least log it; only ignore a failure of `close()` | (Adv p.73, p.75) | [advanced] | timeless |
| Boilerplate for checked exceptions | Checked exceptions force catching or propagating | Wrap in `RuntimeException` preserving the cause; design your own hierarchy carefully | (Adv p.74) | [advanced] | timeless |
| Handle or socket leak | An exception interrupts the flow before closing | `try-with-resources` or `finally` | (Adv p.74–75) | [advanced] | **[DEPENDS ON VERSION]** (try-with-resources: Java 7) |
| `Unhandled exception type IOException` inside a lambda | A functional interface (e.g., `Runnable`) does not declare a checked exception | Catch inside the lambda and rethrow `RuntimeException` with the cause | (Adv p.75–76) | [advanced] | **[DEPENDS ON VERSION]** (lambda: Java 8) |
| Exceptions without context | Message missing or cause lost when rethrowing | Informative message and cause in the constructor | (Adv p.77) | [advanced] | timeless |
| `assert` to validate arguments does not protect | It can be turned off at runtime | Explicit exception (e.g., `IllegalArgumentException`) | (Adv p.64) | [advanced] | timeless |
| `StackOverflowError` | Recursion with no base case or with a base case never reached (e.g., `forever(s)`) | Ensure a base case and that the argument approaches it | (Think p.95, p.220, p.276, p.278) | [introductory] | timeless |

### 1.10 Generics

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `Erasure of method ... is the same as another method` (message recorded in the text) | `sort(Collection<String>)` and `sort(Collection<Number>)` have the same signature after erasure | Different names or another structure | (Adv p.42) | [advanced] | timeless |
| Do not compile: `instanceof T`, `T.class`, `new T[0]`, instantiating `T` | The type parameter does not exist at runtime | Pass `Class<T>`, or reflect on `ParameterizedType` | (Adv p.42, p.44–45) | [advanced] | timeless |
| Primitives not accepted as a type argument | Generics require wrappers; there is implicit boxing/unboxing, at a cost | Use the wrapper, aware of the cost | (Adv p.41) | [advanced] | timeless |
| `performAction(strings, Collections.emptyList())` does not compile | Limited inference | Write `Collections.<String>emptyList()`; in Java 8 it compiles | (Adv p.44) | [advanced] | **[DATED]** (Java 7) |
| Cast needed in a method without generics | The type bound is missing | `<T extends Serializable>`; `<T extends Serializable & Runnable>` removes the need for an intermediate interface | (Adv p.45–46) | [advanced] | timeless |
| Warning on generic varargs | Potential heap pollution | `@SafeVarargs` (the text requires a `final` method) or `@SuppressWarnings("unchecked")` | (Adv p.59) | [advanced] | **[DEPENDS ON VERSION]** (requirement recorded for Java 7/8) |

### 1.11 Concurrency

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| Race condition | Uncoordinated modification of shared state | `synchronized`, locks, atomics, concurrent collections or immutability | (Adv p.80–81) | [advanced] | timeless |
| Deadlock | Two methods take `lock1` and `lock2` in opposite orders | The book only shows the example; always acquiring locks in the same order is a direct inference from the example, [inference]; `tryLock` with a timeout is the feature cited | (Adv p.83–84) | [advanced] | timeless |
| Performance drops from uncontrolled creation | Pools and parallel streams without limits (the book presents `parallelStream()` as a Java 8 novelty tied to "streams", Adv p.82; the Stream API appears with lambdas as a Java 8 novelty in Adv p.103; in Adv p.62 `strings.stream().forEach` is only a method-reference example, without explaining streams) | Manage and limit | (Adv p.62, p.82, p.103) | [advanced] | timeless |
| `Future.get()` blocks forever | Version without a timeout | `get(time, unit)` and handle `TimeoutException` | (Adv p.82) | [advanced] | timeless |
| Contention and performance drop | Excessive synchronization and large blocks | Minimal blocks, release early, lock-free, remove unnecessary synchronization | (Adv p.86) | [advanced] | timeless |
| Subtle bugs with `wait()` and `notify()` | Low-level API | Prefer `java.util.concurrent`; if you use them: inside `synchronized`, `wait()` always in a loop, `notify()` or `notifyAll()` when done | (Adv p.86–87) | [advanced] | timeless |
| Non-portable behavior | Depending on thread priority or on `yield()` | Avoid; use executors and design for the hardware | (Adv p.84) | [advanced] | timeless |
| Several instances of a singleton under several threads | See 1.6: `null` check without synchronization | `static final` initialization or `synchronized` | (Adv p.17) | [advanced] | timeless |

### 1.12 Serialization, reflection and metaprogramming

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `InvalidClassException` on deserialization | Incompatible `serialVersionUID`; without an explicit declaration, the default varies with compiler and version | Declare `serialVersionUID` in every serializable class | (Adv p.89) | [advanced] | timeless |
| Serialization fragile to model evolution | `Serializable` limits changing the internal representation; versioning is left to the developer | Serialization Proxy (introduced in Adv p.92), `Externalizable` or an alternative format | (Adv p.90, p.92, p.95) | [advanced] | timeless |
| More serialization code, more bugs and vulnerabilities | Manual use of the special methods | Serialization Proxy (Adv p.92) | (Adv p.91–92) | [advanced] | timeless |
| Failure reading an object in another language | Java serialization does not work well outside the JVM | Protocol Buffers, Avro, Thrift and the like | (Adv p.95) | [advanced] | timeless |
| Slow and unsafe reflection | Expensive calls, no type safety, subject to permissions | Method handles; avoid when possible | (Adv p.98–99) | [advanced] | **[DEPENDS ON VERSION]** (method handles: Java 7) |
| Runtime exception when accessing a private member | `setAccessible(true)` was missing | Use `setAccessible` only when there is no alternative | (Adv p.98) | [advanced] | timeless |
| Breakage of internal javac | The Compiler Tree API is proprietary, poorly documented and tied to the JDK | Accept the portability limitation; isolate its use | (Adv p.107) | [advanced] | **[DATED]** |
| Fragile "mutating" processor | It manipulates the AST with classes such as `JCCompilationUnit` and `TreeTranslator` (Adv p.117), which are not part of the Tree API described on p.107; calling them javac internals is [inference], since the book only says the Tree API is non-standard, proprietary or internal | Avoid, unless necessary; the book only demonstrates the possibility | (Adv p.116–117) | [advanced] | **[DATED]** |
| JVM crashes from invalid bytecode | Redefined or retransformed bytecode is not verified and installed immediately; the error throws an exception and can bring down the JVM | Extreme care with agents; test thoroughly | (Adv p.121, p.124) | [advanced] | timeless |
| Transformer does not match the class | The `className` uses `/` as the separator | Compare with `sun/net/www/...` | (Adv p.123) | [advanced] | timeless |
| Annotation of little use | `@Retention` or `@Target` missing | Always specify | (Adv p.54) | [advanced] | timeless |
| Repeating the same annotation | Was not allowed before Java 8 | `@Repeatable` with a container | (Adv p.55) | [advanced] | **[DATED]** |

### 1.13 Recursion, loops and diagnosis

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| Infinite loop | The body does not change the condition's variables | Ensure progress toward a false condition; print the variables and the condition's value at the end of the body | (Think p.124, p.276) | [introductory] | timeless |
| Program "hung" | Infinite loop or recursion | Prints "entering the loop" before and "exiting the loop" after the suspect loop; if only the first appears, it is stuck there | (Think p.275) | [introductory] | timeless |
| Uncertain execution flow | It is not known which methods run | Print at the start of each method, showing arguments; check for arguments in the wrong order | (Think p.277) | [introductory] | timeless |
| `if` without braces always executes the second line | Only the first statement belongs to the `if`, despite the indentation (the text cites Apple's "goto fail" bug) | Always use braces | (Think p.88) | [introductory] | timeless |
| Variables from different methods confused | They are independent | Reason by the flow of execution, not top to bottom | (Think p.72–73, p.76) | [introductory] | timeless |
| Deep recursion overflows the stack | Java does not do tail-call optimization; the text says that, "at the moment", neither the compiler nor the JIT supports it | Rewriting as tail-recursive does not solve it; prefer a loop ([inference]) | (Adv p.61) | [advanced] | **[DATED]** |
| Long methods | They hinder reasoning and prevent effective JIT inlining | Split | (Adv p.59, p.61) | [advanced] | timeless |
| Many compiler messages and debugging by bisection | Last resort: back up, delete half the code and recompile; if it compiled, the error was in the deleted part | Repeat until isolated; put the code back gradually | (Think p.274) | [introductory] | timeless |

---

## Part 2 — Anti-patterns (what to do instead)

**Structure and design**

1. **Singleton as the default tool.** It hinders testing and, with dependency injection, is unnecessary. Instead, inject the dependency (Adv p.18).
2. **"Dumping ground" helper class.** Unrelated methods piled up for lack of a better place. Instead, find another way to reuse, keeping the code cohesive (Adv p.18).
3. **Dependency created inside the class.** Instead, receive it through the constructor (Adv p.19).
4. **Exposing fields directly.** Instead, `private` with getters and setters (Adv p.37).
5. **Deep hierarchy just to reuse code.** Instead, interfaces with `default` or composition (Adv p.35–37) — **[DEPENDS ON VERSION]**.
6. **Many arguments and obscure names.** Instead, descriptive names and fewer than 6 arguments (Adv p.58).
7. **Belief that creating objects is slow.** The real cost is in unnecessary long-lived objects (Adv p.15).
8. **Finalizers.** Considered dangerous, with side effects and a performance cost. Instead, `try-with-resources` with `AutoCloseable` (Adv p.16) — **[DEPENDS ON VERSION]**.
9. **`int` constants instead of an enum.** Instead, an enum (with fields, interface, `EnumSet`, `EnumMap` as appropriate) (Adv p.47–52).

**Values, equality and immutability**

10. **`equals` without `hashCode`**, or `instanceof` in a non-final class, or mutable fields in the comparison. Instead, follow the recipe, use `getClass()` and `final` fields (Adv p.22–24).
11. **`clone` with shared state.** Instead, a copy constructor or factory (Adv p.25–26).
12. **"Fake" immutability.** `final` alone is not enough; copy arrays and collections on input and output or expose unmodifiable views (Adv p.31–32).
13. **Returning `null` as "no value".** Instead, `Optional<T>` or an empty collection (Adv p.64) — **[DEPENDS ON VERSION]**.

**Code and readability**

14. **Field shadowing or parameter reassignment.** Instead, `this.field` and `final` parameters (Adv p.67–68; Think p.193).
15. **Override without `@Override`.** Instead, always annotate (Adv p.34, p.60–61).
16. **Large, confusing expression.** Break it into temporary variables that document and allow inspection (Think p.280).
17. **Empty `catch`.** Instead, log it (Adv p.73, p.75).
18. **Exception with neither cause nor message.** Instead, an informative message and the cause preserved (Adv p.77).

**Concurrency**

19. **Manual `wait()` and `notify()`.** Instead, `java.util.concurrent` (Adv p.86–87).
20. **Excessive synchronization.** Instead, minimal blocks and lock-free structures where possible (Adv p.86).

**Platform**

21. **Reflection where static code would suffice.** Slow and without type safety; method handles are an alternative (Adv p.98–99).
22. **Java serialization as a long-lived or multilingual format.** Instead, Serialization Proxy or Protocol Buffers/Avro/Thrift (Adv p.90–91, p.95).
23. **Depending on the Compiler Tree API or on javac classes such as `JCCompilationUnit` (that they are internal is [inference]).** Ties the code to the JDK (Adv p.107, p.116–117) — **[DATED]**.
24. **Accepting the compiler's suggestion without thinking** (e.g., making the class abstract) (Think p.274–275).

---

## Part 3 — Illustrative cases and the lesson of each

**Introductory**

- **The Scanner bug (Think p.61–62).** Read an `int` and then a `String`: the name comes out empty and the age comes on the wrong line. Lesson: `nextInt` leaves the line break in the stream; discard it with `nextLine()`.
- **`1 + 2 + "Hello"` versus `"Hello" + 1 + 2` (Think p.41–42).** Same expression, different results. Lesson: left-to-right evaluation, parentheses.
- **`goto fail` (Think p.88).** `if` without braces and a second line that always runs. Lesson: always use braces.
- **Default `equals` (Think p.198–199).** `time1`, `time2`, `time3` illustrate identity versus equivalence. Lesson: override `equals`.
- **Sum of times (Think p.201).** 18:50 plus 2:16 becomes 20:66. Lesson: handle the "carry" and the valid range.
- **Binary search with an absent card (Think p.219).** Trace of the pairs until it ends at -1. Lesson: check the not-found case.
- **Golfer without a correct `compareTo` (Think p.274–275).** The compiler suggests an abstract class. Lesson: not every suggestion is the fix.

**Advanced**

- **`Person` with `equals`, `hashCode` and `toString` (Adv p.22–27).** Canonical recipe with 31 and a version with `Objects`. Lesson: always the `equals`/`hashCode` pair.
- **`Office` with an array of `Person` (Adv p.24–26).** `Arrays.toString` and `clone` with a shared array. Lesson: a shallow clone shares the mutable.
- **`ImmutableClass` (Adv p.31–32).** Copy in the constructor, `unmodifiableCollection` and `Arrays.copyOf` in the getter. Lesson: immutability requires defensive copying.
- **Diamond with defaults A/B/C/E (Adv p.36).** Interface E does not compile without an override. Lesson: resolve the conflict explicitly — **[DEPENDS ON VERSION]**.
- **`Parent.toObject(Number)` versus `Child.toObject(Double)` (Adv p.60–61).** Overload disguised as override. Lesson: `@Override`. In the same example, `Child.toObject(Number)` returning `String` overrides the `Parent.toObject(Number)` that returns `Object` (more specific return accepted, Adv p.60); it is the `Double` versus `Number` difference in the parameters that creates the overload.
- **Deadlock with `lock1` and `lock2` (Adv p.83–84).** Opposite orders lock up. Lesson: consistent acquisition order ([inference]).
- **`SerializationProxyExample` (Adv p.89–92).** Lesson: less manual serialization code, less bug surface.
- **`@Immutable` processors (Adv p.115–118).** Checker, mutator and generator. Lesson: the mutator uses javac classes (`JCCompilationUnit`, `TreeTranslator`) beyond the non-standard Tree API.
- **Javassist agent on `HttpURLConnection` (Adv p.122–123).** Captures every HTTP URL opened. Lesson: invalid bytecode can bring down the JVM.

---

## Part 4 — Errors in the books themselves (do not reproduce)

### Think Java 6.1.3

- **Type of the `second` attribute.** The text declares `second` as `double` (p.190), but the accessors shown (`getSecond()`, `setSecond(int second)`) use `int` (p.195). The book does not comment on the discrepancy. Do not copy: return and receive `double`, or declare the attribute as `int`.
- **`StackOverflowException` versus `StackOverflowError`.** Ch. 12 uses the first spelling (p.220); the rest of the text and the appendix use `StackOverflowError` (p.271, p.275, p.276, p.278). Use `StackOverflowError`, which is the spelling in the other passages.
- **`int[] array = new Point[5]` (p.277).** Assigning an array of `Point` to an `int[]` variable is not coherent; the idea is an array of objects (probable typo). Declare `Point[] array = new Point[5];`.
- **`intersection` computes the union (p.281–282).** The appendix example, as extracted, computes the union of the rectangles and has a missing comma. It serves only to illustrate the temporary-variables technique; do not use it as an implementation of intersection.
- **`printTime` in 11.5 (p.196).** It uses `println` for the minute and seconds, which would break the line, but the text says the output is `11:59:59.9`. The lines and the output do not match.
- **`toString` ending in `\n` (p.197).** The format ends with a line break and the text says the output is `11:59:59.9`; the `\n` is not commented on. Do not put `\n` in `toString`.
- **Section 9.4 (p.161).** The sentence about returning the empty String when the argument is the String's length was recorded as doubtful; confirm in the `String` documentation before repeating it.
- **`Golfer` message (p.274–275).** It shows `compareTo(java.lang.Object)` and `Comparable` without generics, without saying which version it applies to. Do not take the message as a current example.
- **`shuffle` versus the pseudocode (p.237 versus section 13.2).** The code draws `j` between 0 and `i - 1` (`random.nextInt(i)`), whereas the pseudocode speaks of drawing between `i` and `length - 1`; the book does not comment on the difference.
- **`score()` with negative values (p.243).** It accumulates with `sum -= ...`; the score becomes a numeric penalty. Treat as the example's choice, not as a pattern.
- **Unanswered questions.** The wrong factorial from about 15 (p.185) and `x = x + 1` with `char` (p.168) are left as exercises without explanation.

### Advanced Java

- **Deadlock and "the JVM usually detects it" (p.83–84).** The text asserts this detection. [inference] Do not assume the JVM resolves a deadlock on its own; treat the statement as doubtful and check.
- **Count of `try` blocks (p.112–113).** The text speaks of "empty try/catch" blocks, but the code tests whether the `try` block has no statements; the result 1 refers to that.
- **`@SafeVarargs` requires a `final` method (p.59).** Record specific to the Java 7/8 context of the text — **[DEPENDS ON VERSION]**.
- **`@Inherited` (p.54).** [inference] The restriction to class annotations comes from reading the example, not from a statement in the text.
- **E-book editing items without a confirmed page.** The points below must be checked in the PDF before any use: cross-references between chapters swapped; `DaysOfTheWeek` enum example inconsistent between the variants presented; Nashorn example without a binding for the `str` variable; `tryLock` example that does not handle the case of not obtaining the lock. All are recorded as review [inference], not as a fact asserted by the text.
