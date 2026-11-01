# Cap. 6 — Objetos e Estruturas de Dados (Objects and Data Structures)

Source: CL ch. 6, PDF p.98-106 (chapter opening on p.98; bibliography on p.106).

## Starting point: why private variables
- Variables are private so that no one depends on them and so that the freedom to change the type or implementation is kept (CL p.98).
- The chapter criticizes the habit of automatically generating getters and setters, which exposes private variables as if they were public (CL p.98).

## Data abstraction
- It compares a concrete `Point`, with public `x` and `y` (Listing 6-1), to an abstract `Point` interface (Listing 6-2). The interface does not reveal whether the implementation is rectangular, polar or something else (CL p.99).
- The abstract interface imposes an access policy: it reads each coordinate separately, but sets the coordinates together, in an atomic operation (CL p.99).
- The concrete version exposes the implementation even if the variables were private and accessed through individual getters and setters (CL p.99).
- Hiding the implementation is not just putting a layer of functions over the variables. The class must expose abstract interfaces that let users manipulate the *essence* of the data without knowing the implementation (CL p.99).
- Vehicle: `getFuelTankCapacityInGallons()`/`getGallonsOfGasoline()` (concrete, Listing 6-3) versus `getPercentFuelRemaining()` (abstract, Listing 6-4). The abstract form is preferable (CL p.99-100).
- Expressing data abstractly requires thinking about the best representation. "A pior opção é adicionar levianamente métodos de escrita e leitura" (The worst option is to thoughtlessly add reader and writer methods) (CL p.100).

## Data/object anti-symmetry
- Complementary, practically opposite definitions: **objects** hide their data behind abstractions and expose functions that operate on it. **Data structures** expose their data and have no meaningful functions (CL p.100).
- Procedural shapes (Listing 6-5): `Square`, `Rectangle` and `Circle` are structures without behavior, and `Geometry.area()` decides through `instanceof`. To add a new function, such as `perimeter()`, it is enough to change `Geometry`, and the shapes do not change. To add a new shape, all the `Geometry` functions must be changed (CL p.100-101).
- Polymorphic shapes (Listing 6-6): `area()` in each class and no `Geometry`. A new shape does not affect existing functions. A new function forces changes to all the classes (CL p.101-102).
- Fundamental dichotomy (CL p.102):
  - Procedural code makes it easy to add **new functions** without changing the existing data structures and makes it hard to add **new data structures**, because all the functions change.
  - OO code makes it easy to add **new classes** without changing the existing functions and makes it hard to add **new functions**, because all the classes change.
- To add new data types, objects and OO are more appropriate. To add new functions, data structures and procedural code are more suitable (CL p.102).
- The idea that everything is an object is called a myth. Sometimes you really do want simple data structures with procedures operating on them (CL p.102).
- Footnote: experienced OO has ways out of this, such as the Visitor pattern or dual-dispatch (CL p.101).
- Conclusion: good developers choose, without prejudice, the approach that best fits the moment (CL p.106).

## Law of Demeter
- A module should not know the innards of the objects it manipulates. An object should not expose its internal structure through accessors (CL p.102).
- A method `f` of a class `C` should only call methods of **four** targets (CL p.102):
  1. `C`;
  2. an object created by `f`;
  3. an object passed as an argument to `f`;
  4. an object held in an instance variable of `C` (the translation says "um objeto dentro de uma instância da variável C", literally "an object inside an instance of variable C").
- It must not call methods on objects **returned** by those allowed calls. "fale apenas com conhecidos, não com estranhos" (talk only to friends, not to strangers) (CL p.103).
- The law is presented as a heuristic, with a Wikipedia reference in a footnote (CL p.102).

## Train wrecks
- `ctxt.getOptions().getScratchDir().getAbsolutePath()` is called a "train wreck" (carrinho de trem in the edition). Chains like this are considered sloppy and should be avoided, with a cross-reference to heuristic [G36] (CL p.103).
- It is generally better to break the chain into intermediate variables (`opts`, `scratchDir`, `outputDir`). Even broken up, the function still knows how to navigate many objects (CL p.103).
- The violation **depends** on what `ctxt`, `Options` and `ScratchDir` are. If they are objects, knowing their innards violates the law. If they are just data structures, exposing the structure is natural and the law does not apply (CL p.103).
- Accessors muddy the question. With public fields (`ctxt.options.scratchDir.absolutePath`) the doubt would not even arise. It would be clearer if structures had only public variables and objects only private variables and public functions, but frameworks and standards such as "beans" demand accessors even on simple structures (CL p.103).

## Hybrids
- Structures that are half object and half data structure have meaningful functions and also public variables or accessors that, in practice, make the private variables public (CL p.104).
- They make it hard both to add functions and to add structures: they are the worst of both worlds. Avoid creating them. They indicate a muddled design, in which the author did not know whether they needed protection from functions or from types (CL p.104).
- Footnote 4: this is sometimes called *Feature Envy* in [Refatoração] (Refactoring), by Fowler (CL p.104). The OCR reads "Emy". The term was checked on the image.

## Hiding structure
- If `ctxt` is an object with real behavior, one does not navigate through it. The two obvious ways out are bad: `ctxt.getAbsolutePathOfScratchDirectoryOption()` bloats the object with methods, and `ctxt.getScratchDirectoryOption().getAbsolutePath()` assumes the return is a data structure (CL p.104).
- Tell the object to **do something** instead of asking about its internal structure. Ask what the data is for. In the example, the path was used to create a scratch file, so the function becomes `ctxt.createScratchFileStream(classFileName)` (CL p.104).
- The code that built the file name mixed levels of detail (dots, slashes, extension, `File`), which the book also criticizes with a cross-reference to [G34][G6] (CL p.104).

## Data transfer objects (DTO)
- The perfect form of a data structure is a class with public variables and no functions: the DTO (CL p.105).
- DTOs are useful for communicating with databases, parsing messages from sockets, etc. They are often the first stage in translating raw data into application objects (CL p.105).
- The "bean" form (Listing 6-7, `Address`), with private variables and getters and setters, is more common. Its apparent encapsulation pleases OO purists, but in general it brings no advantage at all (CL p.105).

## Active Record
- Active Records are special DTOs: public variables or bean-style accessed variables, plus navigation methods such as `save` and `find`. They are direct translations of database tables or other data sources (CL p.106).
- Common mistake: putting business rules inside them, which creates a hybrid (CL p.106).
- Solution: treat the Active Record as a data structure and create separate objects with the business rules, which hide their internal data, probably instances of the Active Record itself (CL p.106).

## Examples from the book
- Listings 6-1 and 6-2: concrete `Point` versus abstract `Point`, Cartesian and polar coordinates (CL p.99).
- Listings 6-3 and 6-4: concrete `Vehicle`, with gallons, versus abstract, with fuel percentage (CL p.99-100).
- Listing 6-5: procedural shapes and `Geometry.area()` with an `instanceof` chain and `NoSuchShapeException` (CL p.100-101).
- Listing 6-6: polymorphic shapes implementing `Shape` (CL p.101-102).
- `ctxt.getOptions()...` excerpts (train wreck and broken-up version) and `ctxt.createScratchFileStream(...)` (CL p.103-104).
- Listing 6-7: `Address` as a bean (CL p.105).

## What the chapter does NOT say / common confusions
- It does not say that getters and setters are forbidden. It criticizes adding them "thoughtlessly" and exposing the implementation. For data structures, public fields are legitimate (CL p.100, p.103, p.105).
- It does not say that OO is always better than procedural. The choice depends on the expected axis of change: new types or new functions (CL p.102, p.106).
- The Law of Demeter does not forbid all dot chaining. It does not apply to pure data structures (CL p.103).
- It does not use the expression "Tell, Don't Ask". The idea appears as telling the object to do something instead of asking about its structure (CL p.104) [inference].
- It does not cite the author or the origin of the Law of Demeter. It only points to Wikipedia (CL p.102).
- Heuristic G36 of Ch. 17 ("Evite a navegação transitiva", Avoid transitive navigation) revisits the topic with `a.getB().getC().doSomething()` (CL p.301).

## [DATED]
- Pre-`record` Java examples: public fields and beans with getters and setters. Today immutable DTOs use `record` (Java 16+) or data classes [DATED][extrapolation].
- Frameworks that require beans (the JavaBeans/EJB of the time) motivate part of the confusion about accessors (CL p.103). Many current frameworks accept fields or records [DATED][extrapolation].
