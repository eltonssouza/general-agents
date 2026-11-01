# Glossary

Convention: `(CSYB p.N)` = PDF page (printed = N − 5). The book's glossary occupies PDF **p.204-213** (printed 199-208). The entries below summarize, in English, those of the book; terms that the book does **not** define go in section 3 with the appropriate label. (v1 listed entries that the book's glossary does not have, such as *Block*, *Byte*, *Cast*, *Destructor*, *Encapsulation*, *Iterator*, *Keyword*, *Lock*, *Object*, *Thread* and *Type*; they were removed from section 1.)

## 1. Entries of the Yellow Book glossary

- **Abstract**: idealized description; a class is abstract if marked as such or if it has an `abstract` method; it is not instantiated, it serves as a base/model for the concrete one `[from source] (CSYB p.204)`.
- **Accessor**: method that gives access (read) to a value stored in the class; be careful when returning references `[from source] (CSYB p.204)`.
- **Base**: keyword: calls the parent's constructor and the overridden method `[from source] (CSYB p.204)`.
- **Call**: using a method; flow goes to the body and returns after the `return`/end `[from source] (CSYB p.204)`.
- **Class**: a set of behaviors (methods) and data (properties) that represents a real-world item `[from source] (CSYB p.204)`.
- **Code reuse**: writing each piece only once (methods, hierarchies) `[from source] (CSYB p.205)`.
- **Cohesion**: the glossary describes it as having little dependence on other classes; see also *Coupling*: "high cohesion, low coupling" `[from source] (CSYB p.205-206)`.
- **Collection**: a group of items stored together (array, *hashtable*); supports enumeration for the `foreach`; classes in `System.Collections` `[from source] (CSYB p.205)`.
- **Compiler**: program that reads the source and produces the executable; phases (preprocessor, parser, code generator) `[from source] (CSYB p.205)`.
- **Component**: class whose behavior is exposed through an interface; one thinks about what it **does** `[from source] (CSYB p.205)`.
- **Constructor**: method called when the instance is created; in hierarchies, the parent's must be called correctly `[from source] (CSYB p.205)`.
- **Coupling**: dependency between classes; aim for the minimum `[from source] (CSYB p.206)`.
- **Creative laziness**: code reuse and the right specification to save work `[from source] (CSYB p.206)`.
- **Declarative language**: only states that something exists (XAML); C# is not declarative `[from source] (CSYB p.206)`.
- **Delegate**: type-safe reference to a method with a given signature; holds instance and method; it is an object, can be passed around; tells event generators which method to call `[from source] (CSYB p.206)`.
- **Dependency**: relationship in which changing one class may require changing the other; generally bad `[from source] (CSYB p.207)`.
- **Event**: external occurrence (click, timer) linked to a method via delegates `[from source] (CSYB p.207)`.
- **Exception**: object that describes something bad; `throw`; `try`/`catch`/`finally`; `Message` `[from source] (CSYB p.207)`.
- **Functional Design Specification (FDS)**: description of what the system will do; the most crucial item of the project `[from source] (CSYB p.208)`.
- **GUID**: identifier created to be unique in the world (random + date/time) `[from source] (CSYB p.208)`.
- **Hierarchy**: parent extended by child; the top is more general/abstract `[from source] (CSYB p.208)`.
- **Immutable**: does not change; changing it creates a new object; `string` is immutable `[from source] (CSYB p.208)`.
- **Inheritance**: a class extends the parent and customizes it `[from source] (CSYB p.208)`.
- **Interface**: a set of actions (signatures); the class must implement all of them; it can be referenced by it alone `[from source] (CSYB p.208)`.
- **Library**: a set of classes used by other programs; `.dll`, no `Main` `[from source] (CSYB p.208)`.
- **Machine code**: the language the processor understands `[from source] (CSYB p.209)`.
- **Member**: declared in the class: method or data `[from source] (CSYB p.209)`.
- **Metadata**: "data about data" (type, valid range); collected with the client `[from source] (CSYB p.209)`.
- **Method**: block of code with signature, name, return and parameters; a public method exposes behavior `[from source] (CSYB p.209)`.
- **Mutator**: method that changes a member with validation `[from source] (CSYB p.209)`.
- **Namespace**: area in which a name has meaning; fully qualified name; `using` imports; it is logical, not physical `[from source] (CSYB p.209)`.
- **Overload**: same name with different parameters in the same class `[from source] (CSYB p.209-210)`.
- **Override**: the child replaces the parent's method; `base` accesses the original `[from source] (CSYB p.210)`.
- **Portable**: easy to move to another processor/OS `[from source] (CSYB p.210)`.
- **Private**: visible only inside the class; convention for data `[from source] (CSYB p.210)`.
- **Property**: an object's data; C# has its own construct `[from source] (CSYB p.210)`.
- **Protected**: visible to the class and the derived ones `[from source] (CSYB p.210)`.
- **Public**: visible outside the class; convention for methods `[from source] (CSYB p.210)`.
- **Reference**: label that points to an instance; assigning one reference to another creates two labels for the same object `[from source] (CSYB p.210-211)`.
- **Signature**: method name + types and order of the parameters (the return type does not count) `[from source] (CSYB p.211)`.
- **Source file**: text passed to the compiler `[from source] (CSYB p.211)`.
- **Static**: the member belongs to the class, not the instance; accessed by the class name `[from source] (CSYB p.211)`.
- **Stream**: connection to something that moves data (file, network, console) `[from source] (CSYB p.211)`.
- **Structure**: collection of data, copied on assignment, passed by value; less flexible than objects, but more efficient `[from source] (CSYB p.211)`.
- **Subscript**: integer that identifies the array element; starts at 0 and goes up to size − 1 `[from source] (CSYB p.211-212)`.
- **Syntax highlighting**: editor colors; they are not part of the source `[from source] (CSYB p.212)`.
- **Test harness**: simulates inputs/outputs to test the program in isolation `[from source] (CSYB p.212)`.
- **This**: keyword: calls another constructor of the class and references the current instance `[from source] (CSYB p.212)`.
- **Typesafe**: the compiler prevents nonsensical or lossy combinations (e.g. `double` into `byte` without a cast) `[from source] (CSYB p.212)`.
- **Unit test**: small test that exercises one component; written together with (or before, in TDD) the code `[from source] (CSYB p.212)`.
- **Value type**: simple value, copied on assignment; contrast with reference types `[from source] (CSYB p.213)`.
- **Virtual method**: only `virtual` methods can be overridden; makes access slightly slower `[from source] (CSYB p.213)`.

## 2. Terms of the book outside the glossary (in the body text)

- **Scope**: block of the declaration `[from source] (CSYB p.64)`. **Narrowing/widening**: `[from source] (CSYB p.35)`. **Cast**: `[from source] (CSYB p.35-36)`. **Literal**: `[from source] (CSYB p.28-31)`. **Enumerated type**: `[from source] (CSYB p.85-86)`. **Business object**: `[from source] (CSYB p.166)`. **Factory method**: `[from source] (CSYB p.157, 163-164)`. **Hash table / hash clash**: `[from source] (CSYB p.147-148)`. **Mutex/Monitor**: `[from source] (CSYB p.178)`. **Deadly embrace**: `[from source] (CSYB p.178, 180)`. **Garbage Collector**: `[from source] (CSYB p.96)`. **Boxing, IDisposable, CLR, CIL, JIT**: not defined in the book `[extrapolation]`.

## 3. Modern terms (CSHist, CS12, CS13)

The sources **name** them; the technical definition is `[extrapolation]` except where indicated.

- **Collection expression**: `[...]` syntax and spread `..e` `[from source] (CS12 p.2-3)`.
- **Primary constructor**: constructor in the `class`/`struct` header (C# 12); parameters in scope throughout the body; properties only in records `[from source] (CS12 p.1-2)`.
- **Record**: reference type with value semantics for equality (C# 9); `record struct` (C# 10) `[from source] (CSHist p.4, 6)`.
- **Init-only setter**: enables `with` (non-destructive mutation) `[from source] (CSHist p.6)`.
- **Nullable reference types**: C# 8 `[from source] (CSHist p.8)`.
- **`System.Threading.Lock`**: .NET 9 synchronization type that `lock` recognizes `[from source] (CS13 p.2)`.
- **`params` collections**: `params` with `Span<T>`, `ReadOnlySpan<T>`, `IEnumerable<T>`, etc. `[from source] (CS13 p.2)`.
- **`allows ref struct`**: generic anti-constraint `[from source] (CS13 p.4-5)`.
- **Inline array**: fixed-size array in a `struct` `[from source] (CS12 p.4-5)`.
- **Interceptor**: compile-time call substitution, experimental `[from source] (CS12 p.5-6)`.
- **Top-level statements**: program without an explicit `Main` (C# 9) `[from source] (CSHist p.6)`.
- **Pattern matching**: type, relational, logical, list patterns, etc. `[from source] (CSHist p.3, 6, 8)`.
