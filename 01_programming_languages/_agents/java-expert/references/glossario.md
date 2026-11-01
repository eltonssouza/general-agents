# Canonical Java glossary

Citation abbreviations: **Think** = "Think Java" 6.1.3 (introductory, examples tested with Java SE 8); **Adv** = "Advanced Java" (Java Code Geeks, Java 7/8); **JVM** = "JVM Troubleshooting Handbook" (HotSpot, PermGen era, JDK 6/7).
The number after "p." is the PDF page, not the book's printed numbering.
Marks: **[DATED]** = tied to Java ≤ 8 or to the PermGen era; **[DEPENDS ON VERSION]** = the source ties the feature to a version; **[introductory]** = term found only in Think Java; **[inference]** = link I made between sources.

---

## 1. Types and values

- **Program / algorithm** — a program is a sequence of instructions that describes a computation; an algorithm is the sequence of steps that solves a problem, and can vary in speed and memory use. The basic instructions are input, output, math, decision and repetition (Think p.20). [introductory]
- **Bug / debugging** — a program error and the act of locating and fixing it (Think p.20–21). [introductory]
- **Source code / bytecode / executable** — Java is both compiled and interpreted: the compiler converts the source into portable bytecode, and the JVM interprets it; compiling on one machine and running on another is possible (Think p.22, p.29). [introductory]
- **Statement** — an instruction ended with a semicolon; methods are made of statements and classes of methods (Think p.23). [introductory]
- **main** — the starting point: execution begins at its first instruction; signature presented: `public static void main(String[] args)` (Think p.23). [introductory]
- **Variable** — a named, typed storage location; declaring creates it, assigning changes the value, and it must be initialized before use (Think p.33–35). [introductory]
- **Reserved words (keywords)** — about 50 terms that cannot be used as variable names (`public`, `class`, `static`, `void`, `int`...) (Think p.34). [introductory]
- **Program state** — the set of variables with their values at an instant; the state diagram is a snapshot of that, at runtime (Think p.36, p.181). [introductory]
- **Primitive types** — `int`, `double`, `boolean`, `char` (and `long`): they are not objects (Think p.33, p.157, p.166). Primitive values (the page cites ints, doubles and chars) have no methods: `i.equals(5)` with `int i` is a compilation error (Think p.164). With primitives, `==` compares values (Adv p.26).
- **char / Unicode** — `char` holds one character, a literal in single quotes; Java uses Unicode, and each code unit can be read as an integer (Think p.157–158).
- **Default value** — uninitialized instance and static fields automatically receive: false, 0 (0L for long), `'\u0000'`, 0.0f, 0.0d, and null for references (Adv p.14–15). Difference of emphasis: Think requires initializing *variables* before use (Think p.35); the Adv default applies to *fields*.
- **Arithmetic operators** — `+ - * /` and modulo `%` (Think p.37, p.59). [introductory]
- **Expression** — a combination of values, variables and operators that produces a single value, with a type dictated by the operands (Think p.38, p.47). [introductory]
- **Integer vs. floating-point division** — two integer operands give an integer result, rounded toward zero; a single `double` is enough to make the division floating-point (Think p.38–39). [introductory]
- **double** — the default floating-point type (Think p.39, p.47). [introductory]
- **Precedence** — `*` and `/` before `+` and `-`; ties are resolved left to right; parentheses rule (Think p.42). [introductory]
- **Literal / magic number** — a literal is a value written in the code; a magic number is an unexplained literal, which should become a named constant (Think p.56, p.63). [introductory]
- **Constant (`final`)** — a variable that cannot be reassigned; name in uppercase with `_` (Think p.56). `static` (shared) and `final` (constant) are independent ideas (Think p.211–212).
- **Type cast** — explicit conversion, written as the type in parentheses (Think p.58, p.63). [introductory]
- **Boolean and relational operators** — `boolean` can only be `true` or `false`; relational: `== != > < >= <=` (`=<` and `=>` do not exist) (Think p.85–86). [introductory]
- **Logical operators / short-circuit** — `&&`, `||`, `!`; the second operand is evaluated only if necessary (Think p.86–87, p.97). [introductory]
- **De Morgan's laws** — `!(A && B)` ≡ `!A || !B`; `!(A || B)` ≡ `!A && !B` (Think p.87, p.97). [introductory]
- **Flag** — a boolean variable that signals a condition (Think p.90, p.97). [introductory]
- **Boxing / unboxing** — automatic conversion between primitives and wrappers (`int`↔`Integer`, etc.) done by the compiler (Adv p.68).
- **Wrapper classes** — `Integer`, `Double`, `Character`, `Boolean`, `Long`...; they live in `java.lang`, have `MIN_VALUE`/`MAX_VALUE` and converters such as `parseInt` and `parseDouble` (Think p.164–165). Not to be confused with a "wrapper method" (section 4).
- **Total / partial / absent ordering** — integers and strings are totally ordered; `boolean` has no order (comparing with `<` is an error); types such as cards require choosing a criterion (Think p.212–213). [introductory]
- **Encode** — define a mapping between numbers and the concepts one wants to represent; it is not encryption, and the mapping is a design decision outside the code (Think p.208, p.220). [introductory]
- **Binary** — conversion by successive divisions by 2, reading remainders from bottom to top (Think p.96). [introductory]
- **Array** — a sequence of elements of the same type, indexed from 0; `length` is a built-in attribute, without parentheses; the variable holds a reference (Think p.141–142, p.146, p.152). An array with zero elements is allowed (Think p.142), and that its `length` is 0 is [inference]; a negative size throws `NegativeArraySizeException` (Think p.142). `println(array)` prints something like `[I@bf3f7e0`; `Arrays.toString` shows the elements (Think p.144).
- **Array of objects** — contains references, not the objects, and the elements start as `null` (Think p.215).
- **Traversal, search, reduce, accumulator** — go through all elements; go through looking for something; go through combining into a single value; a variable that accumulates the result (Think p.146–147, p.152). [introductory]
- **Enhanced for** — `for (type e : array)`; convention: plural for the array, singular for the element (Think p.151). [introductory]
- **Loops** — `while` (pre-test), `for` (initializer, condition, update), `do-while` (post-test, body at least once); `++ -- += -=`; `break` exits the loop, `continue` skips to the next iteration; infinite loop = the condition never becomes false (Think p.124, p.132–135). [introductory]
- **Recursion / base case / leap of faith** — a method that calls itself with other arguments; the base case stops the chain; when reading recursive code, one assumes the inner call works (Think p.92, p.95, p.97, p.115–116). Adv also cites *recursion* and *tail call optimization* only as method topics (Adv p.61).

## 2. References, objects and null

- **Object** — a collection of data with methods; an instance of a class (Think p.157, p.189).
- **Attribute (field)** — a variable belonging to an object, accessed with dot notation (Think p.174). [introductory]
- **new** — instantiates and returns a reference to the new object (Think p.174, p.189).
- **Instance vs. class variables** — instance: declared outside methods, one copy per object; class (`static`): a single shared copy, created at program start or on the first use of the class (Think p.190, p.211, p.220).
- **Mutable / immutable** — an object is mutable if its attributes can be changed (Think p.177). To make a class immutable: only getters, no setter or modifier, pure methods (Think p.202). Adv adds `final` fields, defensive copies and accessors that do not leak mutable state (Adv p.31–32).
- **Alias** — two variables pointing to the same object; changing through one is visible through the other (Think p.178–179). [introductory]
- **null** — a special value that means "no object"; using a `null` (accessing an attribute or calling a method) throws `NullPointerException`, while passing it as an argument or returning it is legal and usually indicates a special condition or error (Think p.179). Elements of an object array start as `null` (Think p.215). Adv advises `Optional<T>` as an alternative to returning `null` (Adv p.64) **[DEPENDS ON VERSION: Java 8]**.
- **Identity vs. equivalence (`==` vs. `equals`)** — `==` on references compares whether they are the same object; `equals` compares content according to the class (Think p.198–199; Adv p.26). The `equals` inherited from `Object` repeats `==` (Think p.199; Adv p.22).
- **`equals` contract** — the text defines five rules (Adv p.22): reflexive (x equals itself); symmetric (if x.equals(y) is true, y.equals(x) is too); transitive (if x.equals(y) and y.equals(z), then x.equals(z)); consistent (repeated calls give the same result, unless the properties used in the comparison change); and `equals(null)` is always false. The compiler does not enforce them, and not following them can cause strange, hard-to-diagnose problems (Adv p.22). As for `hashCode`, the rule is the one on the next line; the text does not link its absence to symptoms in collections.
- **`equals`/`hashCode` contract** — equal objects must have the same hash; the converse is not required (Adv p.23).
- **`equals` as an instance method** — without `static`; `this` is the receiver and the parameter is the other object (Think p.199–200). Converting static to instance: remove `static`, remove the first parameter, use `this` (Think p.200–201).
- **compareTo** — returns 1, -1 or 0 depending on whether `this` wins, loses or is equivalent; basis of binary search (Think p.213, p.221). [introductory]
- **toString** — returns the textual representation; `println` calls it on its own (Think p.175–176). The default includes the class name, `@` and the hash, of little use (Adv p.24).
- **`Objects` class** — utilities `equals(a,b)`, `hash(...)`, `hashCode(o)` (null → 0) (Adv p.26). **[DEPENDS ON VERSION: Java 7]**
- **clone / Cloneable** — `clone` is `protected` in `Object`; the class must implement the marker interface `Cloneable`, otherwise `CloneNotSupportedException` occurs; the implementation must call `super.clone()` (Adv p.25). The source gives it a bad reputation.
- **Garbage collection (GC)** — the runtime reclaims objects with no references (Think p.180). Adv adds that GC is generational, betting that most objects die early (Adv p.15). Details of generations in section 8.
- **Finalizers** — look like destructors, but serve resource cleanup; the source treats them as dangerous (Adv p.16). **[DATED]** as to the Java 7/8-era framing.
- **Stack diagram / frame** — a frame is the box with the parameters and variables of a call (Think p.76, p.81). [introductory]
- **UML class diagram** — top half attributes, bottom half methods; shows the code at compile time, unlike the state diagram (Think p.181, p.248). Composition = plain arrow; inheritance = hollow triangle (Think p.248). [introductory]

## 3. Strings

- **String** — immutable: no method changes it, all return a new one (Think p.159); represented in UTF-16 (Adv p.69). The class is `final` (Adv p.38). Comparison: `==` and `!=` compile with Strings but do not do what is expected; use `equals` (Think p.86, p.162; Adv p.26).
- **Concatenation** — `+` between strings joins the ends (Think p.41). [introductory]
- **Empty string** — `""`, length zero (Think p.167). [introductory]
- **String literal vs. char** — double quotes for String, single for char (Think p.157–158).
- **StringBuilder vs. StringBuffer** — the only difference pointed out: `StringBuffer` is thread-safe, `StringBuilder` is not (Adv p.69).
- **String↔number conversions** — `parseInt`, `parseDouble`, `parseBoolean`, `toString` on the wrappers (Think p.164–165).
- **System.out / System.in / System.err** — output `PrintStream`, input `InputStream` and output normally meant for errors and warnings (Think p.51–52, p.91). [introductory]

## 4. Classes, inheritance, interfaces and generics

### 4.1 Classes and members

- **Class** — a template that defines a new type; as many objects as desired are created from it; without other indication, it is a collection of methods (Think p.23, p.189).
- **Method** — a named sequence of statements (Think p.23, p.29). The name starts in lowercase, in camelCase; it cannot be `main` or a keyword (Think p.70).
- **Argument / parameter / passing** — an argument is the value in the call; a parameter is the method variable that receives it; passing is the assignment between them (Think p.73–74, p.81).
- **Local variable / scope** — exists from the point of declaration to the end of the block or method (Adv p.66; Think p.74, p.81). With lambdas (Java 8), the `for` loop becomes a parameter of the function passed to `forEach` (Adv p.66). **[DEPENDS ON VERSION: Java 8]**
- **Signature** — Think: the first line of the method, with name, return type and parameters (Think p.78, p.81). Adv: return type, arguments and list of checked exceptions (Adv p.58). Divergence in the scope of the term, see section 10.
- **Value method / void** — value: declares a return and uses `return` with an expression, and the result should be used; `void` returns nothing (Think p.104, p.116–117, p.70). [introductory]
- **Dead code, stub, scaffolding** — code that never runs (e.g., after `return`); a method skeleton just to compile; temporary development support (Think p.105, p.107–108). [introductory]
- **Pure method / modifier** — pure: does not change parameters, has no side effects and the return depends only on the parameters; a modifier changes the object's state (Think p.202–203). [introductory]
- **Instance vs. static method** — an instance method is invoked on an object and has `this`; error messages may cite "non-static" (Think p.197).
- **Helper / wrapper method** — helper: small, supports a complex method (Think p.225, p.230); wrapper: only delegates to another method, like `addCard` (Think p.236, p.249). [introductory]
- **Functional decomposition** — break a task into simple methods, test in isolation and compose (Think p.109). [introductory]
- **Overloading** — same name, different parameters; the version is chosen by the arguments (Think p.110; Adv p.59–61). Overriding: replacing the inherited implementation, as in `toString` (Think p.203; Adv p.59–61).
- **Varargs** — a variable list of arguments of a type, converted into an array (Adv p.58–59). **[DEPENDS ON VERSION: Java 5]**
- **Inlining** — a JIT optimization that replaces the call with the method body, guided by frequency and size (Adv p.61).
- **Sanity checks** — validating arguments in public methods (Adv p.64).
- **Constructor** — initializes instance variables; same name as the class, no return type and no `static` (Think p.191). If none is declared, the compiler generates an implicit one (Adv p.12); the explicit form without arguments is the no-arg constructor (Adv p.12–13).
- **Constructor chaining (`this(...)`)** — good practice: a single point of initialization (Adv p.13).
- **Constructor visibility** — follows `public` / `protected` / package / `private` (Adv p.15).
- **Initialization block** — `{ ... }` in the class, works as an anonymous constructor, runs before any constructor, in declaration order (Adv p.13–14).
- **Static initializer** — `static { }`, executed once per class loader, in declaration order, thread-safe by the runtime (Adv p.16). JVM describes it the same way: once, at class load, thread-safe (JVM p.103, p.112–113).
- **this** — a reference to the current object; it is neither declared nor assigned (Think p.191). **Shadowing**: a local variable or parameter with the same name as an instance variable (Think p.203). [introductory]
- **private / information hiding** — `private` limits access to the class itself and reduces dependencies between classes (Think p.190). For Adv, encapsulation is hiding implementation through visibility rules (Adv p.37).
- **Getters and setters** — accessors and mutators `getX`/`setX` (Think p.195); JavaBeans are classes that follow such conventions (Adv p.37).
- **Client** — a class that uses objects defined in another (Think p.194). [introductory]
- **Singleton** — guarantee a single instance (Adv p.17). **Utility class** — private constructor, maybe `final`, only static methods (Adv p.18). **Factory** — from static method (factory method) to factory interface (abstract factory) (Adv p.18–19).
- **Dependency injection / inversion of control** — good design practice: dependencies are handed to the instance, by constructor (or setters, strategies), and not created by it; example: `Dependant` receives the `DateFormat` in the constructor, which makes it easier to change the format and write tests (Adv p.18–19). Injection containers and frameworks are not described in the sources (see section 10).
- **Anonymous class** — definition and instance at the same point; before Java 8 it was the only way to do so (Adv p.32). **[DEPENDS ON VERSION]**
- **`final` modifier** — on a class prevents subclasses; on a method prevents overriding (Adv p.38).
- **Naming conventions** — packages in lowercase; classes, enums, interfaces and annotations in CapitalizedCase; methods, fields and locals in camelCase; constants in UPPERCASE with `_`; type parameters in one letter (`T`, `U`, `E`) (Adv p.70; Think p.34, p.56).

### 4.2 Inheritance, composition and interfaces

- **Inheritance** — the subclass extends the superclass and receives its attributes and methods (Think p.234, p.249). Adv: what is public and protected is inherited, plus package-private if in the same package (Adv p.33).
- **Constructors are not inherited; `super(...)`** — the `super(...)` call invokes the superclass constructor; only one class is extended; everything that does not declare `extends` inherits from `Object` (Think p.238; Adv p.21, p.35).
- **Multiple inheritance** — Java admits a single class parent; stacking interfaces is the possible imitation (Adv p.35).
- **IS-A vs. HAS-A** — inheritance: the subclass is a type of the parent (`Hand` is a `CardCollection`); composition: the class owns objects (`Eights` has a `Scanner`) (Think p.248; Adv p.37).
- **Top-down / bottom-up development** — top-down: pseudocode first, then the methods; bottom-up: simple pieces first and assembly afterwards; the final result is similar (Think p.225, p.230, p.244, p.249). **Pseudocode**: a draft mixing English and Java (Think p.225). [introductory]
- **Interface** — basis of development by contract: methods every implementing class must provide; may contain constants and nested types (Adv p.28).
- **Implicit interface modifiers** — `public` members; `abstract` methods; `public static final` fields; `public static` nested types (Adv p.29).
- **Marker interface** — no methods, only tags a trait (`Cloneable`, `Serializable`) (Adv p.29–30).
- **Functional interface** — exactly one abstract method; lambdas convert to it; `@FunctionalInterface` asks the compiler to check (Adv p.30–31). **[DEPENDS ON VERSION: Java 8]**
- **Default and static methods in interfaces** — `default` gives an overridable implementation; interfaces can also have `static` methods (Adv p.30). **[DEPENDS ON VERSION: Java 8]**
- **Abstract class** — not instantiable, mixes abstract and concrete methods and can use all visibility levels; Adv compares it with Java 7 interfaces and, even more, with Java 8 ones (Adv p.31). **[DEPENDS ON VERSION]**
- **Method references** — four forms: `Class::static`, `obj::method`, `Type::instanceMethod`, `Class::new` (Adv p.61–62). **[DEPENDS ON VERSION: Java 8]**
- **Optional<T>** — an alternative to returning `null` (Adv p.64). **[DEPENDS ON VERSION: Java 8]**

### 4.3 Enums and annotations

- **Enum** — a fixed set of values, each an instance of the enum class (Adv p.47–48). **[DATED]** as a Java 5 novelty.
- **Annotation** — metadata with no direct effect on the element; read by the compiler, by processors or by reflection (Adv p.52).
- **Retention policy** — `SOURCE` (discarded), `CLASS` (in the `.class`, not necessarily in the VM), `RUNTIME` (readable by reflection) (Adv p.53, p.115).
- **@Target / element types** — ANNOTATION_TYPE, CONSTRUCTOR, FIELD, LOCAL_VARIABLE, METHOD, PACKAGE, PARAMETER, TYPE; TYPE_PARAMETER and TYPE_USE came in Java 8 (Adv p.53–54). **[DEPENDS ON VERSION]**
- **@Inherited / @Repeatable** — `@Inherited` makes the parent class's annotation reach the subclasses (by default it does not) (Adv p.54); `@Repeatable` allows repeating the annotation, via a container (Adv p.55). **[DEPENDS ON VERSION: Java 8]**
- **Standard annotations** — `@Deprecated`, `@Override`, `@SuppressWarnings`, `@SafeVarargs`, `@Retention`, `@Target`, `@Documented`, `@Inherited`; from Java 8: `@FunctionalInterface`, `@Repeatable` (Adv p.56).
- **Annotation processor** — a compiler plugin (`-processor`) that generates sources/resources, changes code or emits diagnostics (Adv p.55, p.114). Runs in rounds, including a final one; needs a public no-arg constructor; sequence: constructor, `init`, `getSupported...` methods, `process` per round (Adv p.114–115).

### 4.4 Generics

- **Generics** — abstraction over types (comparable to C++ templates); interfaces, classes and methods can be parameterized (Adv p.39–41). **[DATED / DEPENDS ON VERSION: Java 5]**
- **Type erasure** — generics exist only at compile time; in the bytecode they become `Object` (Adv p.42).
- **Bounds** — `extends` (upper bound), `super` (lower), several bounds with `&` (several interfaces, at most one class) (Adv p.42–43).
- **Wildcards** — `?`, `? extends X`, `? super X` (Adv p.43).
- **Diamond operator `<>`** — the compiler infers type arguments (Adv p.44). **[DEPENDS ON VERSION: Java 7]**
- **Improved inference** — in Java 8 cases such as `Collections.emptyList()` as an argument compile without a type annotation (Adv p.44). **[DEPENDS ON VERSION: Java 8]**
- **Annotations on type uses** — only from Java 8 (Adv p.44). **[DEPENDS ON VERSION]**

## 5. Collections

The sources here are scarce: there is no collections chapter in the material (Think only uses `ArrayList`; Adv uses `Set`, `Map`, `HashSet` and `HashMap` merely as examples of generics and concurrency, without explaining the structures).

- **Collection** — an object that contains other objects; Think chooses `ArrayList` (`java.util`), which grows and shrinks on its own (Think p.234). [introductory]
- **Sequential and binary search** — sequential goes through until it finds and depends on `equals`; binary requires order, discards half at each step and depends on `compareTo` (Think p.216–218, p.221). [introductory]
- **Selection sort / merge sort** — the first repeatedly selects the smallest remaining and swaps it with position `i`; the second divides, sorts recursively and merges (Think p.226–227, p.230). [introductory]
- **hashCode and collections** — the `equals`/`hashCode` contract (section 2) is the source's link to hash-based structures; the source does not name `HashMap` in this passage [inference].
- **EnumSet and EnumMap** — collections specialized for enum constants; `EnumSet` is not instantiated by a constructor and uses factory methods (Adv p.51–52). They are not thread-safe (Adv p.52). [advanced]
- **Collections.synchronizedSet/synchronizedMap** — wrap a collection to make it thread-safe, but with mediocre performance according to the book; the library has dedicated concurrent collections (Adv p.85). [advanced]
- **parallelStream()** — parallel processing of a collection (Adv p.82). **[DEPENDS ON VERSION: Java 8]**

## 6. Exceptions

- **Exception** — an event during execution that interrupts the normal flow; it came as a substitute for error codes (Adv p.73). It can be fatal or recoverable (Adv p.73).
- **Checked vs. unchecked** — a separation imposed by the language and the compiler; the JVM does not distinguish (Adv p.73).
- **Unchecked (`RuntimeException`)** — logic errors or premises (invalid argument, null, unsupported operation); they require neither catching nor `throws` (Adv p.73). `NullPointerException` is the best known of them and `extends RuntimeException` (Adv p.73–74).
- **Checked (`Exception` outside `RuntimeException`)** — conditions outside immediate control (network, disk, memory); they must be caught or declared (Adv p.74).
- **Error** — fatal failure, no recovery (`OutOfMemoryError`, `StackOverflowError`) (Adv p.74).
- **Stack unwinding** — on throw, the stack is unwound and native resources (files, sockets) can leak if not released (Adv p.74).
- **try-with-resources** — the resource only needs to implement `AutoCloseable` (Adv p.75). **[DEPENDS ON VERSION: Java 7]**
- **Kinds of error (Think)** — compile-time (syntax), runtime (e.g., infinite recursion produces `StackOverflowError`) and logic (Think p.271). [introductory] Link with Adv's `Error`: [inference].
- **OutOfMemoryError: Java heap space** — allocation failure in the Java heap (Young/Old), raised by HotSpot's native code (JVM p.86). It can occur without a real leak, through prolonged retention in slow threads (JVM p.14–15).
- **PermGen OutOfMemoryError** — PermGen exhaustion (JVM p.85). **[DATED]**
- **OutOfMemoryError: Out of swap space** — failure to allocate OS native memory for the C-Heap or to expand the heap; distinct from the ordinary OOM (JVM p.87–88).
- **OutOfMemoryError: unable to create new native thread** — the JVM could not create a native thread in the OS; related to the thread stack size (JVM p.15, p.89–90).
- **ClassNotFoundException** — class loading by name (string) failed: `Class.forName`, `loadClass`, `findSystemClass` (JVM p.93).
- **NoClassDefFoundError** — thrown by the JVM when the definition of a class, which existed at compile time, is not found in the class loader tree at runtime (JVM p.99, p.103).
- **InvalidClassException** — `serialVersionUID` mismatch on deserialization (Adv p.89).

## 7. Concurrency

- **Java thread** — exists only inside the JVM and may not correspond to an OS thread; every application has at least `main` (Adv p.79). The thread dump brings a native id (`nid`) to correlate with the OS (JVM p.42) [inference: the correspondence exists in HotSpot practice].
- **Thread group** — a set of threads in a tree; not recommended today, since executors/pools are better (Adv p.80). **[DATED]**
- **Race condition** — uncoordinated modification of shared data (Adv p.80); distinct from deadlock and from contention (JVM p.69).
- **synchronized** — mutual exclusion on an instance method, static method or block; it also creates happens-before, making changes visible (Adv p.80). Constructors cannot be `synchronized` (Adv p.80).
- **Monitor (intrinsic lock)** — basis of synchronization; per instance for instance methods, per class for static ones; reentrant (Adv p.81). JVM calls the monitor of an object acquired by `synchronized` a flat lock (FLAT) (JVM p.80–81, p.84).
- **Thread pool / Executors** — a list of ready threads, borrowed and returned; `Executors` builds common configurations (Adv p.81).
- **Future / CompletableFuture** — `Future` represents a future computation (`get` waits); `CompletableFuture` chains actions on completion (Adv p.82). **[DEPENDS ON VERSION: Java 8]** as to the second.
- **ReentrantLock** — explicit, reentrant lock from `java.util.concurrent.locks`, with more features (Adv p.82).
- **StampedLock** — a lock based on "stamps", with three read/write modes; presented as a replacement because the `ReentrantReadWriteLock` implementation was considered weak (Adv p.86). **[DEPENDS ON VERSION: Java 8]**
- **ReentrantReadWriteLock** — read locks have no recorded owner, so HotSpot's deadlock detector does not see them; write locks are tracked as flat locks (JVM p.83–84). **[DEPENDS ON VERSION: HotSpot 1.7]**
- **Deadlock** — threads waiting for each other forever, usually with more than one lock (Adv p.83). In the JVM: A waits for B's monitor and B for A's (JVM p.75). Kinds: lock-ordering (different orders, no recovery) and resource deadlock (e.g., exhausted JDBC pool), the latter the most common and, according to the author, not a true Java deadlock (JVM p.70, p.72).
- **HotSpot deadlock detector** — detects monitors and ownable synchronizers of write locks; does not detect read locks (JVM p.79, p.83–84). **[DEPENDS ON VERSION: HotSpot 1.7]**
- **Thread scheduler** — decides which thread runs and for how long; priority and `yield()` are not portable (Adv p.84).
- **CAS (compare-and-swap)** — an atomic instruction that only writes if the current value matches; generally lock-free; basis of `java.util.concurrent.atomic`, extended in Java 8 with accumulators and adders (Adv p.84). **[DEPENDS ON VERSION]** as to the extension.
- **Biased locking** — a JVM optimization that reduces the cost of uncontended synchronization (Adv p.86).
- **wait / notify** — a mechanism that predates `java.util.concurrent`; requires owning the monitor (Adv p.21, p.86).
- **Thread dump** — a snapshot of the threads: name, priority, `tid`, `nid`, state, stack trace (about 90% of the information) and, since HotSpot 1.6, a heap summary (JVM p.42). **[DATED]** as to the format.
- **Short-lived retention by threads** — ephemeral objects (XML/JSON payloads) retained by slow threads are promoted to OldGen, increase Full GCs and can cause OOM without a leak (JVM p.14–15).

## 8. JVM memory and GC

- **HotSpot's three spaces** — Java Heap, PermGen and Native Heap (C-Heap) (JVM p.3, p.9). **[DATED]**
- **Java Heap** — holds the instances; sized by `-Xmx` and `-Xms`; divided into YoungGen (nursery) and OldGen (tenured) for all vendors (JVM p.3, p.9). Agrees with the generational premise of Adv p.15.
- **PermGen** — specific to HotSpot: Class objects, internal objects and JIT data; sized by `-XX:PermSize` and `-XX:MaxPermSize`; reasonably static, except for dynamic class loading (JVM p.3–5). **[DATED]**
- **Native Heap (C-Heap)** — not directly configurable; holds mapped files and native code; on 32 bits, 4 GB minus heap and PermGen; on 64 bits, RAM plus virtual memory minus heap, PermGen and process (JVM p.4, p.90). Monitored by `pmap`, `svmon` or process size (JVM p.4).
- **Memory lifecycle** — libraries and threads go to the Native Heap, class metadata to PermGen, dynamic objects to the heap; the JVM frees what is unused via GC (JVM p.4).
- **IBM JVM** — nursery and tenured plus Native Heap, no PermGen; `-Xgcpolicy:gencon` cited to reduce pauses in Java EE (JVM p.6). **[DATED]**
- **Oracle JRockit** — no PermGen, compile-only (no interpreted mode), larger processes; risk of native OOM on 32 bits with a large heap (JVM p.7–8). **[DATED]**
- **Thread stack** — holds the calls; the objects created live in the heap, and increasing the stack does not reduce heap retention (JVM p.15). Relevant for `StackOverflowError` and for "unable to create new native thread".
- **Metaspace** — according to the handbook, in Java 8 (then in the future) class metadata moves to native memory; `PermSize`/`MaxPermSize` are ignored with a warning; `MaxMetaspaceSize` limits and, without it, resizes on demand (JVM p.22). **[DEPENDS ON VERSION: Java 8]**
- **Class loader and delegation** — an object that locates class definition data; each loader delegates first to its parent, up to the bootstrap; the parent does not see the children; Java EE containers may change this (JVM p.104–105, p.120).
- **Loader chain** — Bootstrap → `sun.misc.Launcher$ExtClassLoader` (`lib/ext`) → `sun.misc.Launcher$AppClassLoader` (classpath) → children such as `URLClassLoader` (JVM p.112, p.124). **[DATED]**
- **Static initializer (JVM)** — a `static {}` block or static variable, executed once at class load, thread-safe (JVM p.103, p.112–113).

## 9. Tools, build and metaprogramming

- **JDK / JVM / JAR** — the JDK brings a compiler, a JVM that interprets bytecode and tools such as Javadoc; a JAR is essentially a ZIP of classes and resources (Think p.251–252, p.261). [introductory]
- **Library vs. language; package** — the language defines syntax and meaning; a library provides ready-made classes; a package groups related classes (`java.io`, `java.util`); `java.lang` is imported automatically (Think p.51–55, p.67). The documentation cited is the Java SE 8 API (Think p.54–55). **[DATED]**
- **Javadoc and tags** — labels `@param`, `@return` organize the documentation into sections (Think p.112). [introductory]
- **IDE / debugger / breakpoint / call stack** — integrated editing, compiling and debugging; the debugger runs step by step; a breakpoint pauses; the call stack lists active calls (Think p.261–262). [introductory]
- **Unit test** — code that exercises a single method for correctness and/or efficiency (Think p.262). [introductory]
- **Serialization** — translating objects into a storable, reconstructible format (Adv p.89). `serialVersionUID` is `static final long` and validates compatibility (Adv p.89). `Externalizable` hands control to the class (Adv p.90).
- **Special serialization methods** — `writeObject`/`readObject` (private, with `defaultWriteObject`/`defaultReadObject`), `readObjectNoData`, `writeReplace`, `readResolve` (Adv p.91). **Serialization Proxy**: a pattern with `writeReplace`/`readResolve` and a serialized companion class (Adv p.92).
- **JAXB / JSON-P / JSON-B** — XML via annotations (JSR-222) and JSON processing (JSR-353) cited in Adv p.89; JAXB in Adv p.93; JSON-P in 2013 and JSON binding then in progress (JSR-367) in Adv p.94–95. **[DATED]**
- **Reflection** — the program examines itself at runtime; API in `java.lang.reflect`, starting from `Class<?>` (Adv p.96). Parameter names are recorded only with `-parameters` (Java 8) (Adv p.99). **[DEPENDS ON VERSION]**
- **Method handle** — a typed, executable reference to a method, constructor or field (Adv p.99). **[DEPENDS ON VERSION: Java 7]**
- **invokedynamic** — an instruction that customizes the binding between call site and implementation (Adv p.101). **[DEPENDS ON VERSION: Java 7]**
- **Static vs. dynamic typing** — Java checks types at compile time; dynamic languages, at runtime (Adv p.101).
- **Scripting API (`javax.script`)** — `ScriptEngineManager` locates engines; `ScriptEngine.eval` executes; `Bindings` passes variables (Adv p.101–102). **[DEPENDS ON VERSION: Java 6]**
- **Compiler API** — packages `javax.annotation.processing`, `javax.lang.model`, `javax.tools`; the Compiler Tree API (`com.sun.source`) is non-standard and tied to the JDK version (Adv p.107).
- **Element scanner / TreePathScanner** — visitors; the first goes through language elements (`ElementScannerN` family per version), the second through the AST with about 50 `visitXxx` methods (Adv p.110, p.112). **[DEPENDS ON VERSION]**
- **Java agent** — a class that follows strict conventions and changes bytecode at runtime; entries `premain` (at startup) and `agentmain` (afterwards); packaged in a JAR with manifest attributes; `ClassFileTransformer` receives and returns bytecode, or `null` to leave it unchanged (Adv p.120–123).

## 10. Divergences and observations between sources

- **Encapsulation** has three senses: wrapping code in a method (Think p.127); grouping related data in an object (Think p.190); hiding implementation through visibility (Adv p.37). In code review, prefer the third and say which sense you are using.
- **Signature**: Think includes name and parameters (p.78); Adv includes return and checked exceptions (p.58). Both uses coexist in the sources.
- **GC**: Think describes only automatic reclamation (p.180); Adv and JVM add generations (Adv p.15; JVM p.9). Complementary, not conflicting.
- **Static initializer**: Adv says "per class loader" (p.16); JVM says "once in the lifecycle" (p.103). The per-class-loader view is more precise [inference].
- **Deadlock**: Adv treats it generically (p.83); JVM separates true deadlock from resource deadlock (p.70, p.72).
- **Wrapper**: wrapper classes (Think p.164) and wrapper methods (Think p.236) are distinct ideas.
- **Memory**: the handbook applies PermGen to HotSpot; IBM and JRockit have no PermGen (JVM p.6–7). Metaspace is described as the future of Java 8 (JVM p.22), and there is no confirmation of implementation in the other sources.
- **Frameworks**: Spring and Hibernate are not taught in any source; they appear only as context in the handbook's case studies (Spring 2.0.5 and Spring JMS in a deadlock, JVM p.73, p.78; "Apache, Spring, Hibernate etc." as third-party libraries, JVM p.102) and, in Adv, `@Controller`/`@Entity` appear as examples of framework conventions (Adv p.55), and dependency-injection frameworks are cited as users of `setAccessible` (Adv p.98). What the sources teach is the idea of dependency injection by constructor, without a framework (Adv p.18–19).
- **Think examples** were tested with Java SE 8; Adv covers Java 7/8; JVM, JDK 6/7. Features from later versions do not appear in the sources and are not included here.
