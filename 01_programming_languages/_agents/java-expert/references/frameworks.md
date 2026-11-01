# Java: principles, mental models and decision trees

Reference base of the Java specialist agent. Sources: Think Java 6.1.3 (Java SE 8, introductory), Advanced Java (Java 7/8) and the JVM Troubleshooting Handbook (HotSpot, PermGen era).

## Contents

1. Reading conventions (labels, citations, limits of the base)
2. Debugging and incremental development
3. Primitive types, references, aliasing and `null`
4. Equality: `==`, `equals`, `hashCode`
5. Strings
6. Classes, construction and encapsulation
7. Inheritance vs composition; interfaces and abstract classes
8. Overloading vs overriding and `@Override`
9. Immutability
10. Generics, enums and annotations
11. Arrays and collections
12. Exceptions
13. Concurrency
14. Mental model of JVM memory, GC and threads
15. When to investigate what (JVM diagnosis)
16. Reflection, serialization and compiler-level tools
17. Methods, loops and style
18. Divergences between sources
19. Gaps in the base

---

## 1. Reading conventions

- Origin labels: **[introductory]** = Think Java; **[advanced]** = Advanced Java; **[JVM-handbook]** = JVM Troubleshooting Handbook.
- Era labels: **[DATED]** when the source ties the statement to Java 5 through 8 or to the environment of the time; **[DEPENDS ON VERSION]** when the behavior or the recommendation changes according to the Java or JVM version.
- Citations in the format (Think p.N), (Adv p.N), (JVM p.N), with the page of the statement.
- **[inference]** marks links that I make between sources; they are not written in the books.
- Nothing here comes from outside knowledge. Java features after 8 (records, `var`, streams as a topic of their own, virtual threads) do not appear because the sources do not cover them. Metaspace appears in the JVM handbook only as a Java 8 plan in a beta build (JVM p.21–26; see `jvm-troubleshooting.md`, section 2.6); the rest of the handbook deals with the permanent generation (PermGen).

---

## 2. Debugging and incremental development

### Principle: the error is in the last change, if the changes are small

**[introductory]** Start from a program that works and change little at a time, debugging at each step; that way there is always a working version and the error is isolated in the last line added (Think p.28, p.106–108). Writing a lot of code and then resorting to trial and error is the explicit anti-pattern (Think p.28).

### Mental model: debugging is the experimental method

- Form a hypothesis, change the program, predict the result; if you were wrong, formulate another (Think p.27).
- Programming requires a mental model of what the code does. If the result diverges, the defect may be in the model in your head, not in the program; fix the model by testing classes and methods in isolation (Think p.279).
- Making mistakes on purpose to learn the meaning of each compiler message is recommended (Think p.27, p.31).
- Compiler messages are evidence, not a prescription: they indicate where the compiler was when it noticed the problem, and the suggested remedies are not very reliable (Think p.44, p.272, p.275). At runtime, the line that breaks may not be the line to fix (Think p.45).
- Logic error: the program does exactly what it was told, just not what you wanted; no tool knows what the correct behavior is (Think p.45–46).

### Decision tree: how to attack a defect

1. Does the code compile?
   - No → read the message as a clue to where to look, not as an order; look above the indicated line (Think p.44).
   - Yes → continue.
2. Did you just add code to a program that worked?
   - Yes → suspect the last change first (Think p.106).
   - No → reduce: test isolated components (Think p.279).
3. Do you know the right answer for some input? If so, write it down before implementing (book example: 3-4-5 should give 5.0) and compare (Think p.107).
4. Suspicious intermediate value? Use a temporary variable and inspect it with `print` or a debugger; only then condense the expression (Think p.108).
5. Two composed methods fail? Test the first carefully before the second, so you do not debug two at the same time (Think p.119).
6. In a debugger session, do not edit code while the program is paused: changes on several lines produce confusing results (Think p.259).
7. In doubt about what is legal or what happens: try it in the compiler (Think p.118).

### Gap

The text recommends reading Think's debugging appendix several times (Think p.15, p.46). That appendix includes, among other points, debugging by **bisection** as a last resort for compilation errors: make a backup, delete about half the code, recompile and repeat depending on whether it compiles (Think p.274), and the **rubber duck**, which consists of explaining the problem out loud to a rubber duck (Think p.283). Isolation through small changes and component testing is also a method of the text (Think p.107).

---

## 3. Primitive types, references, aliasing and `null`

### Principles

- **[introductory]** Assignment is not mathematical equality: `a = b` copies the current value; changing `a` afterwards does not change `b` (Think p.35–36). The left side must be a storage location (Think p.35, p.43).
- **[introductory]** Array and object variables hold references (arrows), not the data. Assigning copies the reference, not the object (Think p.142, p.145, p.174, p.178).
- **[introductory]** Parameters: changing a primitive parameter does not affect the caller's variable (Think p.76), but a method that receives an object (book example: `Rectangle`) can change it; this is useful and makes debugging harder, since it is not clear which calls modify arguments (Think p.177–178). **[inference]** Arrays are also references (Think p.142, p.145), so the same consequence holds for them; pages 177–178 deal with objects, not arrays.
- **[advanced]** A local variable with the same name as a field shadows the field without warning; to use the field, qualify it with `this.` (Adv p.67).

### Rule: primitive or wrapper?

- If the value cannot be null → prefer a primitive in parameters and variables; a null wrapper passed where a primitive is expected causes `NullPointerException` on conversion (Adv p.68).
- If it is a generic type argument → a wrapper is mandatory (`List<Long>`); accept the implicit boxing/unboxing (Adv p.41, p.68).
- Trade-off: generics have the cost of boxing and erasure (Adv p.45).

### Rule: arithmetic and precision

**[introductory]**
- Integer division truncates. For percentages with integers, multiply before dividing: `minute * 100 / 60` gives 98, whereas `minute / 60` gives 0 (Think p.38, p.42).
- Converting `double` to `int` requires an explicit cast over the whole expression, and the cast truncates toward zero; for the nearest integer, use `Math.round`, which returns `long` (Think p.58–59, p.68).
- Amounts that require exactness (bank balance): use integers (cents), respecting the `int` limit of about 2 billion (Think p.41). `long` has 64 bits (Think p.68).
- Assigning an integer to a `double` (`double y = 1;`) is legal, but the book treats it as bad style (Think p.39–40).
- `double` is approximate: p.40–41 deal with rounding error; the comparison rule is in Think p.280: the book says you should probably never use `==` with `double` and suggests comparing the difference against a tolerance.
- Divisibility: `x % y == 0`; last digit: `x % 10` (Think p.59).

### Decision tree: absent value and `null`

1. Might the method have nothing to return?
   - Collection → return an empty collection (`Collections.emptyList()`), neither `null` nor `Optional` (Adv p.64).
   - Another type, Java 8 → `Optional<T>` removes the need to return `null` (Adv p.64). **[DEPENDS ON VERSION: Java 8]**
   - Java ≤ 7 → the absence of a value is `null`, the origin of the reputation of `NullPointerException` (Adv p.64). **[DATED]**
2. Is it a search in an array or string? The book's convention: return `-1` when not found (Think p.147, p.162). It is a sentinel value, not `null`.
3. `null` as an argument or return is legal and usually indicates a special condition or error, but using members of a null reference throws an exception (Think p.179).
4. A public method receives an argument: validate it (sanity checks) and throw `IllegalArgumentException` or equivalent (Adv p.64, p.73). Do not rely on `assert`, which can be turned off at runtime (Adv p.64).
5. Short-circuiting of `&&` and `||` is a tool against failure: the second operation may be one that would fail if the first were false (Think p.86–87). **[inference]** Applicable to `x != null && x.field`; the text gives the principle, not that example.
6. Early exit: `return` when an error condition is detected, as in the book's `printLogarithm` (Think p.90–91). "Guard clause" is the package's name, not the book's [inference].

---

## 4. Equality: `==`, `equals`, `hashCode`

### Principle

`==` compares identity (the same reference); `equals` compares value when the class defines it (Think p.198; Adv p.26). For Strings, `==` compiles but does not do what is expected (Think p.86). The default `equals` does the same as `==` (Think p.199; Adv p.22).

### Decision tree

1. Comparing Strings?
   - Content → `equals`; never `==` or `!=` (Think p.86, p.162). Adv example: `new String("bbb") == "bbb"` gives `false` and `equals` gives `true`, because they are two distinct instances (Adv p.26). On p.86 Think says only that `==`/`!=` with Strings "don't do what you expect" and postpones the explanation; it comes later, in the distinction between identity (same object) and equivalence (same content) (Think p.162–163, p.198), and String is immutable (Think p.159). The internal mechanism of String literals is not in the pages used.
   - Order → `compareTo` (Think p.162–163).
2. Comparing your own objects?
   - The intent is identity → `==` (Adv p.26).
   - The intent is value → `equals()` or `Objects.equals()` (Adv p.26; Think p.198). `Objects.equals` is Java 7+ **[DEPENDS ON VERSION]** (Adv p.26–27).
   - With primitives, `==` compares values (Adv p.26); primitives have no methods (`i.equals(5)` does not compile); wrappers (`Integer`, `Double`...) are `java.lang` classes (Think p.164–165). For `double`, Think says you should probably never use `==` and suggests comparing the difference with a tolerance, `Math.abs(d - 1.23) < .000001` (Think p.280).
3. Need to write your own `equals`?
   - The text warns to think twice about whether it is really necessary (Adv p.22).
   - If so → always `@Override` (Adv p.22–25).
   - Contrast between sources: Think's `equals` (class `Time`) takes a parameter of type `Time` and compares the fields (Think p.199; the inherited `equals` repeats `==` and, for your own types, it must be overridden for another equivalence, Think p.199, p.280). Adv uses `equals(Object obj)` with `@Override` and the five-rule contract: reflexive, symmetric, transitive, consistent and `equals(null)` false (Adv p.22). **[inference]** By the rule of Adv p.60–61 (another parameter type becomes an overload), `equals(Time that)` does not override `Object.equals(Object)`; no page makes that link.
4. Wrote `equals`?
   - Override `hashCode` along with it, with the same fields in both methods (Adv p.23–24).
   - Prefer `final` fields in these methods so the result does not vary with mutations (not always possible) (Adv p.23–24).
   - Compare the class with `getClass() != obj.getClass()` instead of `instanceof`, unless the class is `final`, to avoid problems in hierarchies (Adv p.23).
   - Java 7+: `Objects.hash` simplifies (Adv p.26–27). **[DEPENDS ON VERSION]**
5. `toString`: include the class and fields for debugging and troubleshooting; for arrays use `Arrays.toString`/`deepToString`, and `Objects.toString` for possibly null references (Adv p.24–25). Libraries cited as support: Guava and Apache Commons Lang (Adv p.24–25).
6. Copying an instance: avoid `clone()`/`Cloneable`; prefer a copy constructor or factory method (Adv p.26).

---

## 5. Strings

### Principles

- Strings that look like numbers are not numbers: `"123"` is a `String` (Think p.35).
- **[introductory]** Strings are immutable: no method (`toUpperCase`, `replace`...) changes the string, all return a new one; if you do not keep the return value, the call has no effect (Think p.159).
- **[advanced]** `String` is `final` by an old decision to prevent alternative implementations (Adv p.38).
- **[introductory]** Elements of `args` are always Strings; convert before using them numerically (Think p.166).

### Decision tree: building text

1. Two or three simple strings → the `+` operator is enough (Adv p.69–70).
2. Loop or many operations → `StringBuilder` (Adv p.69–70; Think p.232 suggests the same for the `toString` of a large deck).
3. Shared between threads → `StringBuffer` (Adv p.69–70).
4. Different types (numbers, dates, times) → `String.format`, described as an often better alternative to direct concatenation (Adv p.70); in Think, `String.format` takes the same arguments as `printf` and creates the string without displaying it (Think p.164).
5. Control over output format (decimal places, leading zeros) → `printf` (Think p.57–58).

### Query operations (Think)

- Traversing: `charAt(i)` with `length()`; to use the enhanced for, `toCharArray()` (Think p.159–160). Last character: `charAt(length - 1)` (Think p.160).
- `substring(i, j)`: end index exclusive (Think p.161).
- `indexOf` returns `-1` if it does not exist; a version with a start index for the next occurrences (Think p.162).
- `Integer.parseInt` (String to number) and `Integer.toString` (the inverse) (Think p.165).

---

## 6. Classes, construction and encapsulation

### Principles

- **Encapsulation = minimal public contract.** The fewer internal details exposed, the more freedom to evolve without breaking callers, which is crucial in libraries and frameworks; what does not need to be public should be `private` (or `protected`/package-private as appropriate); never expose fields directly (Adv p.37–38). **[advanced]**
- **Coupling.** If A directly accesses variables of B, A depends on B; if it uses only methods, they remain independent as long as the signatures do not change. This is the reason for `private` + getters/setters (Think p.194). **[introductory]**
- **Cohesion.** Grouping related data in an object and passing it makes the code more readable and less error-prone (Think p.175, p.190). Generic classes (`Card`, `Deck`) do not carry the rules of a game; specific rules live in other classes, which eases reuse (Think p.241). **[introductory]**
- **Dependencies come from outside.** A class that needs another receives the instance (preferably in the constructor) instead of creating it; gain: easy swapping of implementation and simple tests (Adv p.18–19). This is dependency injection, also called inversion of control: dependencies are supplied by constructor (or setters, strategies) and not created by the instance; the example is the `Dependant` class, which now receives the `DateFormat` in the constructor (Adv p.19). The sources contain no injection container or framework configuration. **[advanced]**
- **Cheap objects, expensive long-lived objects.** Creating objects is fast; what costs is needlessly creating long-lived objects, which fill the old generation and cause stop-the-world collection. The belief that instantiating is slow is described as false (Adv p.15). **[advanced]** See also section 14.

### Decision tree: access to fields

1. Instance variables → `private` (Think p.194).
2. Does external code need access? Three options from the book: make them public (simple, but creates dependency); provide getters/setters; do not allow access (Think p.194). Setters are a design decision: in the `Card` example, the book prefers not to offer them, since mutability is a source of error (Think p.214).
3. IDEs generate constructors, getters and setters from the variables (Think p.193, p.195).

### Decision tree: construction

1. Several constructors with combinations of arguments → chain with `this(...)` to a main constructor (Adv p.13).
2. Logic common to all constructors → an initialization block exists, is rare, runs before the constructors; the text does not recommend preferring it (Adv p.13–14).
3. Parameter names equal to the attributes' → `this.` undoes the shadowing (Think p.192–193).
4. More readable creation name → static factory method (`Book.newBook(...)`) with a private constructor; if the concrete class must stay hidden, a factory interface (Adv p.18–19).
5. Does the class create its dependencies internally (for example `DateFormat.getDateInstance()`)? Receive them by constructor (Adv p.18–19).
6. Singleton:
   - If unavoidable, the `static final` (eager) version is the correct and simple one.
   - The lazy version requires `synchronized` on `getInstance()`, with less concurrency.
   - The naive version (checks `null` without synchronizing) can create several instances under concurrency (Adv p.17).
   - Conclusion of the text: today singletons are not a good choice in most cases (they hinder testing; dependency injection makes them unnecessary) (Adv p.18).
7. Helper class of static methods: tends to become a dumping ground of unrelated methods; the text recommends avoiding it in most cases (Adv p.18).
8. Finalizers: avoid, except rare cases tied to native objects (Adv p.16). To release resources, `try-with-resources` + `AutoCloseable` (Java 7) (Adv p.16). **[DEPENDS ON VERSION: Java 7]**

### Constants and shared state

- Shared constants: `public static final`, uppercase name; does not recreate the array on each call and allows use in other classes. Exposing `public` is safe when the array is `final` and the strings are immutable (Think p.211–212). **[introductory]**
- Magic numbers become named `final` constants (Think p.56, p.60).

---

## 7. Inheritance vs composition; interfaces and abstract classes

### Principles

- **Composition tends to beat inheritance.** Reasons: more flexible design; more stable model (changes do not propagate through hierarchies); low coupling (inheritance tightly couples parent and children); simpler reasoning because dependencies are in one place. Inheritance has its place and should not be discarded (Adv p.37). **[advanced]**
- **Contract before implementation.** Interfaces are the basis of development by contract. The text strongly advises preferring interfaces to classes and abstract classes whenever possible: they are lightweight, easy to test with mocks and to maintain, and minimize the effect of changing implementation; class proxies in the standard library depend on interfaces (Adv p.34). The same idea in variables and parameters: prefer the interface type to the concrete type (Adv p.68–69). **[advanced]**
- **Subtype polymorphism.** Where a `CardCollection` is expected, `Hand`, `Deck` or `CardCollection` will do; the reverse does not hold (Think p.240–241). **[introductory]**

### Decision tree: inheritance or composition?

1. Apply the IS-A / HAS-A test; in most cases HAS-A is better (Adv p.37). Text example: `Vehicle` has an `Engine`; `Vehicle extends Engine` is the wrong choice.
2. Does the subclass differ only by a constructor or an extra method? Inheritance is suitable. Book example: `Deck` (another constructor) and `Hand` (a `display` method); `Hand` serves for hands and piles because there is almost no difference (Think p.238–239). **[introductory]**
3. Would inheritance force awkward methods (such as a static `cardMatches` in `Player`)? The book notes that the alternative would be subclasses such as `EightsCard` and `EightsHand` (Think p.250). **[introductory]**
4. Close extension with `final`? No general rule; it is hard to decide in advance and delicate for library authors, since it limits applicability (Adv p.38).

### Decision tree: interface, abstract class or concrete class

1. Default: interface (Adv p.34).
2. Can a considerable part of the implementation be shared by the subclasses, with customization points via abstract methods? Abstract class (Adv p.31).
3. In interfaces, omitting `public`/`abstract`/`static`/`final` is a personal preference (Adv p.29).
4. Expose the minimum of members to the public and to subclasses (Adv p.33).

### Gap

`default` and `static` methods in interfaces and the conversion of lambdas to functional interfaces are a Java 8 novelty presented in Adv (Adv p.30); `default` allows implementation inside the interface and creates the diamond conflict described in Adv p.36 **[advanced] [DEPENDS ON VERSION: Java 8]**. Adv does not give a decision tree for choosing between `default` and an abstract class; any rule beyond that is [inference].

---

## 8. Overloading vs overriding and `@Override`

### Principles

- **Overriding** replaces inherited behavior. Every subclass can override any inherited method, except those declared `final` (Adv p.34, p.38). Java has no dedicated syntax for marking an override, so `@Override` serves to guarantee the intent; the compiler reports a signature that does not match (Adv p.34, p.60–61). Always use it on `equals`, `hashCode`, `toString`, `clone` (Adv p.22–25). **[advanced]**
- **Covariant return.** `Child.toObject(Number)` returning `String` overrides `Parent.toObject(Number)` returning `Object`: the text says the signature is "a little bit different" and refers to a section "Covariant method return types", which does not appear in the extraction (Adv p.60). `toObject(Double)` in the child, on the other hand, is another signature: overloading, not overriding; with `@Override` on it, the compiler reports an error (Adv p.60–61). **[advanced]**
- **Overloading** is the same name with different parameters; on a call, Java (the compiler) chooses the version by the arguments supplied, or reports an error if none fits (Think p.110; Adv p.59). Adv example: constructors have the same name and different sets of arguments (Adv p.59).

### Decision tree

1. Do two methods do the same thing with distinct parameters? Overloading is suitable, but can confuse debugging if you think you are calling one version and call another (Think p.110). **[introductory]**
2. Does each type of argument require a specialized implementation? Overloading (Adv p.59–60). Combining with generics is powerful, but often impossible because of type erasure (Adv p.59–60). **[advanced]**
3. Want to replace an inherited method? Override with `@Override` (Adv p.34), unless the method is `final` (Adv p.38).
4. When reviewing: is a method not being called as expected? Think p.110 and Adv p.59 say the version is chosen by the arguments of the call (or a compilation error if none fits); Adv p.60–61 shows the `Number` vs `Double` trap, in which the version with another parameter type is an overload and does not override. The fine resolution rule (for example, which type counts: the declared or the dynamic one) is not in the pages used **[inference]**: check whether it is an overload and not an override, and consult the language specification.

---

## 9. Immutability

### Principles

- **Less mutable state → better scalability and simpler reasoning**, motivated by the multi-core era (Adv p.31). Immutability in Java takes work, but should not be ignored (Adv p.62). **[advanced]**
- **Immutability cures the complexity of concurrency**: immutable objects do not need synchronization and can be used anywhere without risk of concurrent modification (Adv p.71, p.81). **[advanced]**
- **Mutability is a source of error.** Modifiers can be more efficient (they do not create objects) but are error-prone, especially with aliased objects; immutable objects cost more at the start and avoid long debugging sessions (Think p.202, p.214). **[introductory]**
- **Immutability enables safe aliasing**: the `subdeck` shares cards with the original deck, harmless because `Card` is immutable (Think p.228). **[introductory]**

### Decision tree

1. Need to modify a value? Return a new instance instead of offering a setter (model of the Java 8 date/time API, `LocalDateTime`) (Adv p.62). **[DEPENDS ON VERSION: Java 8]**
2. Is not offering setters enough? No: someone may add a modifier later. Declare the fields `final` so the compiler blocks modifications outside the constructor (Think p.214).
3. Will you share references between structures (sublists, subdecks)? It is only safe if the elements are immutable (Think p.228).
4. Pure method or modifier? `selectionSort` modifies the deck (`deck.selectionSort();`); `mergeSort` is pure and returns a new one (`deck = deck.mergeSort();`); the choice changes how it is called (Think p.232).
5. Your own collection: the book does not offer a wrapper for `set`, to control how the collection is modified; only `popCard` and `swapCards` modify (Think p.237).
6. `String` is the example of an immutable in the sources: no method changes it, all return a new one (Think p.159). In the Adv class, the starting point is declaring all fields `final`, which alone does not guarantee immutability (Adv p.31); the other steps (defensive copies, accessors that do not leak mutable state) are in Adv p.32.
7. Declare the **class** `final`? Adv treats `final` classes (prevents subclasses; `String` is the example) as a design decision with no general rule (Adv p.38), but does not present it as a requirement of immutability; linking the two ideas is **[extrapolation]**: check the JDK documentation.

---

## 10. Generics, enums and annotations

### Generics

**[advanced]** Principle: type safety checked at compile time, at the cost of erasure and boxing; use them without expecting them to solve everything (Adv p.45).

Tree:
1. Raw type (`Collection`, `Callable`) or `Object` → switch to the generic type (`Collection<T>`, `Callable<T>`): clear contract, easier refactoring (Adv p.45).
2. Method receives and returns the same subtype → `<T extends Serializable> T performAction(T)` eliminates the cast (Adv p.45).
3. Require several interfaces without creating an intermediate interface → `<T extends Serializable & Runnable>` (Adv p.46).
4. Need the class of the type parameter at runtime? Pass `Class<T>` as an additional argument; the increase in parameters is acceptable with careful design. Discovering the concrete type of a generic instance requires reflection (`ParameterizedType`) (Adv p.44–45).
5. Primitive as a type argument → wrapper (Adv p.41).

### Enums

**[advanced]**
- Fixed set of constants → enum, not `int` constants: strong typing and compiler checking (Adv p.47–48, p.52). Since Java 5 it is the recommended form (Adv p.52). **[DATED]**
- Data per constant → instance fields + private constructor (Adv p.48–49).
- Behavior per constant → implement an interface; the version with a body per constant is verbose, and combining fields and an interface is leaner (Adv p.49–50).
- Collections of enums → `EnumSet` and `EnumMap`, and not general-purpose equivalents; they are not thread-safe (Adv p.51–52).
- Enums work in `switch/case` (Adv p.51).

### Annotations

**[advanced]**
- Principle: explicit configuration validated by the compiler, as opposed to the convention-over-configuration paradigm; misuse is detected early, at compile time (Adv p.55).
- Every annotation of your own declares `@Retention` and `@Target` (Adv p.54).
- A single mandatory attribute → name it `value` so the name can be omitted (Adv p.52). An attribute without a `default` is mandatory in every use (Adv p.52).
- Additional metadata associated with the code → annotation is the simple way (Adv p.56).

---

## 11. Arrays and collections

### Arrays (Think)

**[introductory]**
- Size: any non-negative integer expression, including zero; a negative size (for example −4) throws `NegativeArraySizeException` (Think p.142). Elements of an `int` array start at zero (Think p.142); those of an object array start `null` (Think p.215).
- `length` is a built-in constant, without parentheses and without arguments (`a.length`, not `a.length()`); `a[a.length]` would throw an exception (Think p.146). Legal indexes: 0 to `length - 1` (Think p.143).
- Iterate with `i < a.length` instead of a magic number (the book replaces the literal 3 with `a.length` to serve arrays of any size); last index `a.length - 1` (Think p.146).
- Traversing and reading the values (accumulating, printing) → enhanced for; needing the index (search by position, copy by index) → traditional `for` (Think p.151).
- A real copy: a new array and copy element by element, or `Arrays.copyOf(a, size)` (Think p.145–146). Assigning an array variable copies the arrow (Think p.145).
- Display: `println(a)` shows something like `[I@bf3f7e0` (bracket = array, `I` = integer, the rest is the address); `Arrays.toString(a)` (with `import java.util.Arrays`) shows `[1, 2, 3, 4]` (Think p.144).
- Search: return the index when found and `-1` at the end (Think p.147). Accumulator initialized before the loop (Think p.147); for a maximum, `Integer.MIN_VALUE` as the initial value (Think p.166).
### Search and sorting

**[introductory]**
- Without order, search is sequential; with a sorted array, use binary search (about log2 n comparisons versus n) (Think p.217, p.219).
- Selection sort is proportional to n²; merge sort, to n log2 n (for a million items: 1 trillion vs. 20 million steps) (Think p.226).
- To obtain the logarithmic gain, the halves must be sorted recursively; base case: 0 or 1 card (Think p.229).
- Computations such as `high - low + 1`: draw a diagram to prevent off-by-one errors (Think p.227).
- Removing the last position is the most efficient (no shifting); if order does not matter, use `popCard()` with no argument (Think p.236).

### `java.util` and concurrent collections

**[advanced]**
- Thread-safe collection → prefer those in `java.util.concurrent` over the `Collections.synchronizedXxx` wrappers, whose performance is only mediocre (Adv p.85).
- A returned collection is never `null`: use an empty one (Adv p.64).
- Enums as key/element → `EnumMap`/`EnumSet` (Adv p.51–52).
- Design of your own collection: encapsulate the array and control the modifiers (`CardCollection`) (Think p.237).

### Gap

The sources do not provide, in the pages used, a decision tree for choosing among `List`, `Set`, `Map` and their implementations, nor the `hashCode` contract in the practice of `HashMap`. The agent must resort to other references for that decision. **[inference]** The closest link is the `equals/hashCode` contract (section 4).

---

## 12. Exceptions

### Principles

**[advanced]**
- Single rule: never ignore an exception; at the very least, log it (Adv p.73). That includes not swallowing an exception in an empty `catch`.
- Unchecked for logic or premise errors (invalid argument, null, unsupported operation); checked for external environment failure (Adv p.73–74).
- `NullPointerException` is unchecked: the text shows the declaration `NullPointerException extends RuntimeException` and calls it the best known of the unchecked ones; it does not need to be caught or declared in `throws` (Adv p.73–74). The checked/unchecked distinction belongs to the compiler; the JVM does not make it (Adv p.73). `Error` (for example `OutOfMemoryError`, `StackOverflowError`) indicates a fatal failure (Adv p.74).
- In Think, `NullPointerException` appears when accessing an attribute or calling a method of a `null` reference (Think p.179); passing `null` as an argument or returning it is legal and usually signals a special condition or error (Think p.179).
- The text also says that checked exceptions in the signature turned out less useful than intended, generating more boilerplate than solution (Adv p.59). The tension between the two passages is recorded in section 18.

### Decision tree

1. Violation of a public method's precondition? Check at the start, before doing work, and throw an appropriate exception (`IllegalArgumentException`) (Adv p.64, p.73).
2. Going to create your own exception?
   - First, consider the JDK standard exceptions (Adv p.76).
   - If you do create one, the book strongly advises inheriting from `RuntimeException` (unchecked), admitting exceptions to the rule (Adv p.77).
   - Balance the hierarchy: too many classes complicate development and inflate the catching and propagation code (Adv p.76).
3. Lambda whose functional type does not declare a checked exception (example `Runnable`)? Catch inside the body and rethrow `RuntimeException` with the original cause (Adv p.76). **[DEPENDS ON VERSION: Java 8]**
4. Documentation: `@throws` for the checked ones (which appear in `throws`) and for the relevant unchecked ones (`IllegalArgumentException`, `NullPointerException`) (Adv p.77–78).
5. Resource to release (file, stream)? `try-with-resources` with `AutoCloseable`, not a finalizer (Adv p.16). **[DEPENDS ON VERSION: Java 7]**
6. Lock acquired? `try/finally` for the `unlock` (Adv p.82–83).
7. User input that may fail? Validate beforehand; in Think, `hasNextDouble()` before reading avoids `InputMismatchException`, and if it is not a number, consume the token with `in.next()` and warn (Think p.91–92). **[introductory]**
8. Error messages: write to `System.err` (Think p.91).

---

## 13. Concurrency

### Principles

**[advanced]**
- **High level over low level.** Prefer executors, pools, concurrent collections and atomic classes to direct threads, `wait/notify` and synchronized wrappers (Adv p.79–86).
- **Balanced synchronization.** Too little produces corrupted data; too much produces contention. Minimal critical regions, locks released early, prefer lock-free algorithms when possible (Adv p.86).
- **Immutability as an alternative to synchronizing** (Adv p.71, p.81).
- **Do not depend on the JVM scheduler**; design for the real hardware (number of CPUs obtained via `Runtime`) (Adv p.84).
### Decision tree: running concurrent work

1. Create a `Thread` directly? Generally no; use executors and pools (Adv p.79, p.81).
2. Is the task long-running? Executors are not recommended for that (Adv p.81).
3. Does the result matter?
   - No → `executor.execute(...)` (fire-and-forget).
   - Yes → `submit` with `Callable`, which returns `Future` (Adv p.81–82).
4. Will you wait on the `Future`? Prefer `get` with a timeout; the unbounded version is discouraged (Adv p.82).
5. Uncontrolled creation of pools and parallel streams can ruin performance; control them (Adv p.82). **[DEPENDS ON VERSION: Java 8]**

### Decision tree: protecting shared state

1. Is it possible not to share it or to make it immutable? Do that (Adv p.81).
2. Counter or simple shared value → atomic classes (CAS) instead of a lock (Adv p.84, p.86).
3. Need a timeout or fail-fast when acquiring? `ReentrantLock` with `tryLock(time, unit)`; monitors (`synchronized`) wait indefinitely (Adv p.83).
4. Every `lock()` with `unlock()` in `finally` (Adv p.82–83).
5. Concurrent reads and writes with many reads? The book points to `StampedLock` (Java 8) as a better alternative to `ReentrantReadWriteLock` (Adv p.86). **[DEPENDS ON VERSION: Java 8]**
6. Exchange of signals between threads → `java.util.concurrent` utilities, not `wait/notify` in modern code (Adv p.87).
7. Shared collection → concurrent collection, not `Collections.synchronizedXxx` (Adv p.85).
8. `EnumSet`/`EnumMap` are not thread-safe (Adv p.52).
9. `StringBuilder` is not safe between threads; `StringBuffer` when shared (Adv p.69–70).

### Gap: deadlock

In Adv, what there is about limiting waiting is: minimal critical regions, `tryLock` with a timeout and `Future.get` with a timeout (Adv p.82–83, p.86). **[inference]** These mechanisms limit waiting, but Adv does not present them as a solution to deadlock. Deadlock diagnosis and global lock ordering appear in the JVM Troubleshooting Handbook, **[DATED]** (JVM p.69–85; see `jvm-troubleshooting.md`, section 3.12).

---

## 14. Mental model of JVM memory, GC and threads

General label: **[JVM-handbook]** and **[DATED]** (HotSpot, PermGen era, common 32-bit JVMs). Where a statement is general, the section says so.

### 14.1 The process is the sum of competing parts

- In a 32-bit JVM, the Java heap and the native heap compete: the larger the heap, the less native memory remains; a heap of 2.5 GB or more on 32 bits raises the risk of native OOM, depending on the footprint and the number of threads (JVM p.9).
- Three regions compete on 32 bits: Java Heap, PermGen and C-Heap; increasing the heap reduces the C-Heap and reserves more OS memory (JVM p.88).
- A 64-bit JVM removes this limitation, but remains limited by physical resources and by the GC cost, which grows with size; major collections become more expensive. The text states that bigger is not always better and advises against running 20 Java EE applications in a single 16 GB process (JVM p.9). On 64 bits, the C-Heap concern becomes the OS capacity (physical, virtual, swap) (JVM p.90). **[DATED]**
- 32-bit process limit: in theory 4 GB, less on some old 32-bit Windows (2 GB by default in certain versions); 64 bits reaches 16 EB in theory; on Solaris, a 32-bit JVM reaches about 3.5 GB before native allocation failures (JVM p.88–90). **[DATED]**

### 14.2 What pressures each region (JVM p.10)

| Factor | Region under pressure |
|---|---|
| Number of applications (EAR/WAR/JAR) in the same process | Native heap |
| Number of classes and class loaders, including third-party ones | PermGen and internal JIT objects |
| Data caches (DB, files) | OldGen |
| Number of threads the middleware allows | Native memory (without it, `OutOfMemoryError`) |

**[DATED]** the mention of PermGen ties the statement to the era before this region was replaced; its successor (Metaspace) is treated only as a plan and a beta in Java 8 (JVM p.21–26); the agent must not state how it works in current JDKs.

### 14.3 Static and dynamic footprint

- Static: predictable (classes, caches, applications). Dynamic: comes from traffic, from users and concurrent requests, which generate the rate of creation and collection of short- and long-lived objects (JVM p.11).
- Typical YoungGen:OldGen ratio cited as 1:3 (33%); for a 2 GB heap on 32 bits with a generational and concurrent collector, about 500 MB of YoungGen and 1.5 GB of OldGen (JVM p.11). Note: 500 MB of 2 GB is 25%, not 33%; the text uses both numbers without reconciling them. Treat as an order of magnitude (JVM p.11).
- The application profile dictates the pressure: an application with large, non-serialized sessions (shopping-cart type) needs a lot of OldGen; a stateless application with a lot of XML (many ephemeral objects) needs an adequate YoungGen to reduce Full GCs (JVM p.11).

### 14.4 Frequency of major collections

- Minimizing the frequency of major collections is the key performance factor presented (JVM p.11).
- Author's rule of thumb: keep up to about 50% heap occupancy after a major collection, to reduce Full GC and leave headroom for failover (JVM p.12).
- OldGen at 80% or more with frequent GCs does not support failover: when instances are lost, the redirected load brings down the remaining ones (domino effect) (JVM p.13).

### 14.5 Link to Java code

**[inference]** The principle in Adv (short-lived objects are cheap; needlessly long-lived ones are expensive, since they occupy the old generation and cause stop-the-world collection, Adv p.15) is the same logic the JVM handbook uses to size YoungGen and OldGen. In-memory cache (JVM p.10) and retention of session objects (JVM p.11) are the concrete paths through which long-lived objects arise. The sources contain no table of code X leads to symptom Y; this is a link of mine.

### 14.6 Threads and GC

- Threads of a Java EE application are created mainly by the middleware kernel and by the JVM; some are internal (GC threads, VM Thread, VM Periodic Task Thread) (JVM p.41, p.45).
- Parallel collector: HotSpot creates N GC threads (default or by tuning), reducing GC time at the cost of more CPU (JVM p.45). High CPU consumption by GC threads can be correlated by the native thread id (example: `nid=0x3` for "GC task thread#0 (ParallelGC)") (JVM p.45).
- Creating a Java thread requires creating a native thread in the OS, with a stack reserved in the process's native memory; the OS refuses when the 32-bit address space is exhausted (2, 3 or 4 GB) or when the OS virtual memory is exhausted (JVM p.90). On Solaris, swap exhaustion can cause SIGBUS on access to the thread stack and bring down the JVM (JVM p.90).
- **Native OOM is usually a symptom, not a cause**: the frequent root is the application or the container creating too many threads on unhappy paths (thread stuck on remote IO, race conditions), pressuring the C-Heap (JVM p.92).

---

## 15. When to investigate what (JVM diagnosis)

### Decision tree: which symptom → where to look

1. **`OutOfMemoryError` / process crash.** Identify the region:
   - Java heap full? The book associates caches and sessions with OldGen and applications with a lot of ephemeral traffic with YoungGen (JVM p.10–11). Check occupancy after a major GC: above about 50% is a sign of pressure (JVM p.12).
   - PermGen? Associate with the number of classes and class loaders (JVM p.10). **[DATED]**
   - Native memory/C-Heap or thread creation fails? Increasing the heap makes it worse (JVM p.9, p.88). Investigate the number of threads and the root cause (stuck remote IO, race conditions) (JVM p.92). **[DATED]** as to the 32-bit numbers.
2. **High CPU.** Look at the GC threads by `nid` in the dump before blaming the application (JVM p.45).
3. **Many GCs, frequent Full GCs.** Check occupancy after major, the YoungGen:OldGen ratio and the application profile (JVM p.11–13).
4. **Stalled threads.** Read the dump classifying each thread: computing, blocking IO, GC, idle `wait()`, waiting on a monitor (JVM p.47–48). Many waiting on a monitor → contention on `synchronized` (Adv p.86 supports the contention logic).
5. **Possible leak in native code.** Track the count of global JNI references (JVM p.46).
6. **Class loading failure.**
   - `ClassNotFoundException`: the lookup by name failed (JVM p.93, p.98).
   - `NoClassDefFoundError`: the class referenced at compile time does not exist at runtime in the current tree, and may be a consequence of an earlier failure (static initializer, `ExceptionInInitializerError`) (JVM p.99, p.119).
   - Look first for the `ExceptionInInitializerError`: the first trigger is that error, the following ones are consistent `NoClassDefFoundError`s until fixed and the JVM restarted (or live redeploy by the container) (JVM p.103).
   - A class present in the parent and in the child is loaded by the parent (parent-first delegation); if it references classes only in the child, `NoClassDefFoundError` occurs (JVM p.126).

---

## 16. Reflection, serialization and compiler-level tools

### Reflection and invocation

**[advanced]**
- Powerful, but expensive, without type safety and subject to permissions; use only when necessary (Adv p.98–99).
- `setAccessible(true)` allows writing to a private field; used by test scaffolding and DI frameworks; avoid in your own application unless there is no alternative (Adv p.98).
- Concern with performance and type safety → method handles, at the cost of more verbose code (Adv p.99). **[DEPENDS ON VERSION: Java 7+]**
- Parameter names at runtime → compile with `-parameters` (Java 8) (Adv p.99). **[DEPENDS ON VERSION]**

### Serialization

**[advanced]**
- Native serialization is neither free nor interoperable; evaluate alternatives (Adv p.95).
- Every `Serializable` class declares `serialVersionUID` explicitly; the generated value depends on internal details and may vary with compiler and version (Adv p.89).
- Fine control → `Externalizable` or `writeObject`/`readObject` (Adv p.90–91). Reduce risk and vulnerabilities → Serialization Proxy pattern (Adv p.91–92).
- RMI: still used, less and less, because of complexity and port blocking by firewalls (Adv p.93). **[DATED]**

### Compiler/JVM tools

**[advanced]**
- They are low-level, tied to the version and dangerous; use them when the alternative is enormous boilerplate or the source code is unavailable (Adv p.107, p.114, p.120).
- Agent: changing behavior without access to the source code (Adv p.121).
- Standard libraries before third-party ones: milestones Java 5 `java.util.concurrent`, Java 6 `javax.script` and `javax.tools`, Java 7 `java.nio.file` and `java.lang.invoke`, Java 8 `java.time` (Adv p.71). **[DATED]**

---

## 17. Methods, loops and style

### Methods

**[advanced]**
- A method is an API entry point: meaningful name, few arguments (fewer than 6), short body, documentation, validation (Adv p.58, p.64).
- Names in camelCase and descriptive; parameters with an explanatory name (Adv p.58).
- Single responsibility and bodies that fit on one screen; balance so as not to explode the number of methods (Adv p.59).
- Declaring parameters `final` is advised (although rare) to avoid reassignment; Java 8 relaxed this with "effectively final" (Adv p.59). **[DEPENDS ON VERSION]**
- Javadoc on public methods (parameters, return, exceptions, preconditions, examples), especially in libraries and frameworks (Adv p.62–64).

### Loops and conditionals (Think, summary)

**[introductory]** `for` with initialization, condition and update; `do-while` if the body runs at least once; `while (true)` with `break` in moderation (Think p.132–135). Recursion requires a reachable base case (Think p.95) and fits when the problem's definition is already recursive (Think p.113, p.123). Always braces in `if/else` (Think p.88); booleans without `== true` (Think p.90).

### Style

- Minimal scope: declare the variable as close as possible to its use (Adv p.66). Divergence with Think recorded in section 18.
- Short, simple tests, one thing at a time; the standard library does not include a test framework, JUnit is used (Adv p.71). **[DATED]**

---

## 18. Divergences between sources

1. **Where to declare variables.** Think declares variables and constants at the top of `main` to show types and data (Think p.60), presented as a preference of the example, not a rule; Adv says minimal scope, near the use, is the only scope rule (Adv p.66). Recommendation: follow Adv in production code.
2. **Checked exceptions.** Adv says checked ones are for environment failure (Adv p.73–74), and elsewhere that they turned out less useful than expected (Adv p.59), advising your own unchecked exceptions (Adv p.77). The two texts coexist: checked at the boundary with the environment, unchecked for premises and for your own exceptions.
3. **Access to fields.** Think lists the option of public fields as simple, but creating dependency (Think p.194); Adv says never to expose fields directly (Adv p.37–38). Adv is more restrictive; Think is pedagogical.
4. **YoungGen:OldGen ratio** (JVM p.11): 1:3 (33%) vs. 500 MB of 2 GB (25%); the text does not reconcile them.

---

## 19. Gaps in the base

What the sources do not cover in the pages used; the agent must not present it as if it came from these sources:

- Choice among `List`/`Set`/`Map` and iteration of collections; the `hashCode` contract in hash collections.
- Deadlock in Adv: not treated as a topic of its own (the JVM handbook treats it, see `jvm-troubleshooting.md`).
- Specific collectors and tuning flags beyond what appears in the examples; Metaspace appears only in a prospective section of the handbook (JVM p.21–26).
- Records, `var`, streams as a topic of their own, virtual threads: absent because they postdate the sources.
- Frameworks (Spring, Hibernate etc.) are not taught. They appear only as context: Spring 2.0.5 and Spring JMS in a deadlock case study (JVM p.73, p.78), "Apache, Spring, Hibernate etc." as an example of third-party libraries in a `NoClassDefFoundError` case (JVM p.102) and, in Adv, `@Controller`/`@Entity` as examples of MVC and ORM framework conventions (Adv p.55) and dependency-injection frameworks as users of reflection (Adv p.98). Dependency injection as a good design practice, by constructor, is taught without a framework (Adv p.18–19).
- Tables and figures of Adv (for example the table of standard exceptions, Adv p.76) were not extracted.
- The numeric mapping of suits and ranks in Think's card example lost the numbers in extraction; only the order of the arrays was deduced (Think p.209–210).
