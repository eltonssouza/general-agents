# Creational patterns (RG) and Nystrom's criticisms (GPP)

Sources: **RG** = catalog of the Refactoring.Guru site captured as a PDF (279 pages; it is **not** the e-book "Dive Into Design Patterns") and **GPP** = *Game Programming Patterns* (Nystrom), web capture of the book (338 pages). Pages = **PDF** (see `INDEX.md`). The RG PDF covers 22 patterns; the *Interpreter* of the original GoF is not in it (RG p.2-3, 7).

Labels: `[from source]` direct reading of the cited page; `[inference]`; `[extrapolation]`; `[DATED]`.

## 1. Overview
- RG classifies patterns by complexity and scale: idioms (low level, a single language) and architectural patterns (high level); by intent, three groups: creational, structural and behavioral `[from source] (RG p.5)`.
- Creational patterns in the catalog: Factory Method, Abstract Factory, Builder, Prototype, Singleton (creation mechanisms that increase flexibility and code reuse) `[from source] (RG p.10-11)`. In the PDF the order of presentation is Abstract Factory (p.17-28), Builder (p.30-43), Factory Method (p.45-56), Prototype (p.58-69), Singleton (p.70-77).

## 2. Factory Method (RG p.45-56)
- Intent: creation interface in the superclass, subclasses alter the type created; also known as Virtual Constructor `[from source] (RG p.45)`.
- Illustrated problem: a logistics app coupled to `Truck`; adding `Ship` forces changes throughout the code and generates conditionals per transport type `[from source] (RG p.46)`.
- Solution: replace direct calls to `new` with a call to a factory method; subclasses override the method, as long as the products share a base class/interface `[from source] (RG p.46-47)`.
- Creating products is not the *creator*'s main responsibility (it usually already has business logic about products); the factory method may return existing objects from a cache or pool `[from source] (RG p.49, 51)`.
- When to use: exact types unknown in advance; let users of a library/framework extend internal components; reuse expensive objects instead of recreating them `[from source] (RG p.52-54)`.
- How to implement: common interface, empty factory method, replace constructors one by one (a temporary `switch` may appear), subclasses per type, optional control parameter `[from source] (RG p.54-55)`.
- Relations: many designs start with Factory Method and evolve to Abstract Factory, Prototype or Builder; Factory Method is a specialization of Template Method `[from source] (RG p.55)`. Con: more subclasses; the best case is to insert the pattern into an existing hierarchy of creators `[from source] (RG p.55)`.

## 3. Abstract Factory (RG p.17-28)
- Intent: produce **families of related objects** without specifying concrete classes `[from source] (RG p.17)`.
- Site example: furniture (Chair, Sofa, CoffeeTable) in the Modern, Victorian, ArtDeco variants; the client must not receive products of different variants `[from source] (RG p.18-19)`.
- Solution: an interface per product, a factory interface with creation methods for all products, a concrete factory per variant; the client uses only abstract types; the application creates the concrete factory at startup according to configuration/environment `[from source] (RG p.19-21)`.
- When to use: code that deals with families of products without depending on concrete classes; a class with several Factory Methods that obscure its main responsibility `[from source] (RG p.26)`. How to implement (6 steps; starts with the product x variant matrix) `[from source] (RG p.26-27)`.
- Pros: products compatible with each other, low coupling, SRP, Open/Closed; con: more interfaces and classes `[from source] (RG p.27)`.
- Relations: Builder returns the product after extra steps, Abstract Factory returns it immediately; abstract factories are often based on Factory Methods (Prototype can compose them); alternative to Facade when you only want to hide creation `[from source] (RG p.27-28)`.

## 4. Builder (RG p.30-43)
- Intent: build complex objects step by step, producing different representations with the same code `[from source] (RG p.30)`.
- Problem: a monstrous constructor with many parameters (most unused in most calls) or subclasses for every combination `[from source] (RG p.31-32)`.
- Solution: extract construction into *builder* objects with steps (`buildWalls`, `buildDoor`...); not all steps need to be called; several builders implement the same steps in different ways `[from source] (RG p.32-33)`.
- **Director**: optional class that fixes the order of the steps and reuses construction routines `[from source] (RG p.34)`. Builders can produce products without a common interface, so the method that returns the result lives in the concrete builder `[from source] (RG p.35, 37-39, 41-42)`.
- When to use: eliminate the "telescoping constructor" (`Pizza` example, possible in languages with overloading, such as C# or Java), build different representations with similar steps, build Composite trees (recursive steps) `[from source] (RG p.40-41)`.
- Con: overall complexity increases (several new classes) `[from source] (RG p.42)`. Relations: Builder + Composite; Builder + Bridge (director as the abstraction) `[from source] (RG p.43)`.
- `[extrapolation]`: fluent chaining `builder.setX().setY().build()` is a common idiom of modern languages; the RG text describes steps and director, not "fluent interface" (a term absent from the PDF).

## 5. Prototype (RG p.58-69) and Nystrom's view (GPP p.61-75)
- Intent: copy objects without depending on their classes; cloning is delegated to the object itself, through an interface with a `clone` method `[from source] (RG p.58-59)`.
- Problem with copying "from outside": private fields and dependence on the concrete class `[from source] (RG p.59)`. Pre-configured prototypes can replace subclasses; there is a variant with a **prototype registry** `[from source] (RG p.60, 62-63, 67)`.
- When to use: code independent of the classes of the objects being copied; reduce subclasses that differ only in initialization `[from source] (RG p.66-67)`. Con: cloning objects with circular references can be difficult `[from source] (RG p.68)`.
- **GPP**: example of monster *spawners* (Ghost, Demon, Sorcerer) and the parallel hierarchy of spawners; the prototype clones the class **and state** `[from source] (GPP p.61-64)`. Nystrom points out costs (writing `clone()` in every class; shallow vs. deep copy) and says that, with *spawn functions*, *templates* and first-class types, he did not find a case where the pattern was the best answer `[from source] (GPP p.64-67)`.
- GPP also covers **prototype as a language paradigm** (Self, delegation to the parent; JavaScript) and concludes that purely prototype-based languages were not pleasant to use `[from source] (GPP p.67-72)`; and **prototype delegation in game data** (JSON with a `"prototype"` field to reduce duplication among monsters and items) `[from source] (GPP p.73-75)`.

## 6. Singleton (RG p.70-77) and GPP p.77-91
- RG: the pattern solves two problems at the same time (a single instance and a global access point), violating SRP; private constructor and a static creation method with caching `[from source] (RG p.71-72)`. Implementation steps, with lazy initialization `[from source] (RG p.75)`. The RG pseudocode uses a thread lock and double checking of the field, without naming it `[from source] (RG p.74)`.
- RG, cons: violates SRP, can mask bad design, requires handling in multithreading, makes unit tests harder (private constructor; static methods not overridable) `[from source] (RG p.75-76)`. Relation to Flyweight: only one Singleton, which can be mutable; Flyweights are many and immutable `[from source] (RG p.76)`.
- **GPP** is emphatic: the chapter shows "how not to use" the pattern; the GoF recommends sparing use `[from source] (GPP p.77)`. Reasons to use (restrict to one instance, global access without passing the object, lazy creation, subclassable per platform) `[from source] (GPP p.77-81)`. Reasons for regret: it is a global variable (harder to reason about, encourages coupling, hostile to concurrency) `[from source] (GPP p.81-83)`; it solves two problems even when only one is needed (the `Log` example that later needs several instances) `[from source] (GPP p.83-84)`; lazy initialization takes away control over when memory is allocated in games `[from source] (GPP p.84-85)`.
- Nystrom's alternatives: check whether the class is needed ("manager" classes), a runtime `assert` of single instantiation, **pass the object as a parameter**, get it from the base class (Subclass Sandbox), from something already global or from a Service Locator; he never used the full GoF implementation in a game `[from source] (GPP p.85-91)`.
- Careful attribution: "test pollution" and "deadlocks from initialization order" are **not** GPP terms (which speaks of global state, coupling and concurrency, p.81-83). The difficulty of unit testing appears in RG (p.75-76); otherwise, label it `[inference]`.

## 7. What the PDF does NOT contain (do not attribute)
- Content of the "Factory Comparison" page (links only, RG p.28, 44, 56); *simple factory*/*static factory method* as a pattern.
- Interpreter (GoF). "Double-checked locking" and "fluent interface" as terms; DI as a container (GPP p.88-89 only covers passing dependencies as parameters).
- Examples in Unity, Godot, TypeScript etc.: `[extrapolation]`.
