# OCP (2014 post) and LSP, ISP, DIP ("Solid Relevance" post, 2020)

Sources (both posts from The Clean Code Blog, 15-page browser printouts):
- **`OCP`**: Robert C. Martin, "The Open-Closed Principle", May 12, 2014. Content on **p.1-4** (p.5-15: sidebar).
- **`SREL`**: Robert C. Martin, post titled "Solid Relevance" in the PDF (October 18, 2020); in the old package it was called "The Relevance of SOLID Principles". Content on **p.1-5** (p.6-15: sidebar).

**Convention**: `(OCP p.N)` and `(SREL p.N)` = PDF page. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

> **Corrections relative to the previous version of the package.** (1) The `OCP` PDF does **not** contain the "financial report case" with `WebPresenter`/`PdfPresenter`: that example is from another work by the author `[extrapolation]`. (2) The `SREL` PDF does **not** contain Liskov's formal definition (`S`/`T`/`o1`/`o2`), the Rectangle/Square example, the two-item statement of the DIP, nor the claims "microservices are an application of SRP/ISP" or "monads are the functional manifestation of DIP/OCP". On the contrary: p.2 says that **microservices do not solve** the mixing of reasons for change. Those items came from the pages "SREL p.5-15" attributed incorrectly.

---

## 1. Open-Closed Principle (`OCP`)

- **Origin**: Bertrand Meyer, 1988, in *Object Oriented Software Construction* `[from source] (OCP p.1)`. In Meyer's formulation, an **open** module = available for extension (e.g., adding fields to the structures or new elements to the set of functions); a **closed** module = available for use by other modules, with a stable, well-defined description (an interface in the sense of information hiding); Meyer's text mentions compiling and storing in a library, or approval by management and publication in the official repository `[from source] (OCP p.1-2)`.
- Martin considers this definition **dated** ("it smells of a waterfall mentality"), but says the essence remains: **you should be able to extend the behavior of a system without having to modify it** `[from source] (OCP p.2)`.
- Consequence: if every module could be extended without modification, new features would come only from new code; the old code would not change, would not need to be recompiled or redeployed; only the new code would be deployed (perhaps in a new jar, dll or gem). This suggests what a jar/dll/gem should be: **isolable features** `[from source] (OCP p.2)`.
- In day-to-day work, we add features with many changes scattered through the existing code, a practice Fowler named *Shotgun Surgery* `[from source] (OCP p.2-3)`.
- **Plugins** are "the consummation, the apotheosis" of the OCP and proof that open-closed systems are possible `[from source] (OCP p.3)`. How: they believed in the OCP and used the tools of object-oriented design to separate **high-level policy from low-level detail**, managing dependencies and **inverting those that cross architecturally significant boundaries in the wrong direction**; in a plugin architecture, all dependencies inside the plugin point toward the system, and nothing in the system points to the plugins `[from source] (OCP p.3)`.
- Martin proposes imagining systems in which the database and the GUI are pluggable, and concludes that, when the fundamental business rules are the core of a plugin architecture, one is never locked into a set of features, interface, database or framework `[from source] (OCP p.3-4)`. He states that a strong plugin architecture is "probably the most important aspect of future systems" `[from source] (OCP p.4)` (his opinion).

## 2. Why SOLID still matters (`SREL`)

- **Context**: a letter asks whether knowledge of SOLID should remain a hiring criterion; a manager argues that the OCP matters less (code in small microservices is safe to change), that the LSP is outdated (less inheritance) and cites Dan North: "just write simple code" `[from source] (SREL p.1)`.
- **Thesis**: the principles are as relevant as in the 1990s, because software has changed little (it is still sequence, selection and iteration: `if`, `while`, assignment) `[from source] (SREL p.1-2)`.
- **SRP** (p.2): "gather together the things that change for the same reasons, separate the things that change for different reasons"; microservices do **not** solve this: one can create a tangled microservice, or a set of them, if one mixes code with distinct reasons for change. "Simple code" is something he agrees with, and the SRP is one way of keeping code simple `[from source] (SREL p.2)`.
- **OCP** (p.2-3): "a module should be open for extension and closed for modification"; he illustrates with device independence (writing to a file, printer, screen or pipe) and with the cost of scattered `if`s; when requirements change, only part of the code is wrong and the rest remains right, and we want not to have to change the right code to fix the wrong; "simple code is open and closed" `[from source] (SREL p.2-3)`.
- **LSP** (p.3-4): "a program that uses an interface must not be confused by an implementation of that interface". The mistake, including his own, was thinking it is about inheritance; it is about **subtyping**: every implementation of an interface is a subtype, including duck types (implicit interface), and every user of the base type must agree on the meaning of the interface; if an implementation confuses the user, `if`/`switch` proliferate. It is about keeping abstractions **crisp** `[from source] (SREL p.3-4)`.
- **ISP** (p.4): "keep interfaces small so that users don't depend on things they don't need". Argument: compiled languages still depend on modification dates to recompile/redeploy; if A depends on B at compile time but not at run time, changing B forces recompiling and redeploying A; acute in statically typed languages (Java, C#, C++, Go, Swift), less so in dynamic ones, but they are not immune (the existence of Maven and Leiningen is the proof he gives). Splitting a class with two interfaces into two classes is a good idea (SRP), but is often neither feasible nor desirable `[from source] (SREL p.4)`.
- **DIP** (p.4-5): "depend in the direction of abstraction; high-level modules must not depend on low-level details". Hard to imagine an architecture without significant use of this principle: we want the rules that "make money" without pollution from SQL, low-level validations or formatting; this is achieved by isolating through source code dependencies, **especially those that cross architectural boundaries**, pointing toward high-level abstractions `[from source] (SREL p.4-5)`.
- **Closing** (p.5): simplicity requires disciplines guided by principles; it is the principles that define simplicity; the best way to create a complicated mess is to tell everyone to "be simple" without further guidance `[from source] (SREL p.5)`.

## 3. Links with Clean Architecture

- The `CA12` text invokes the DIP to make code dependencies oppose the flow of control (`CA12 p.5-6`), and `OCP p.3` describes the same mechanism for plugins: invert dependencies that cross significant boundaries `[inference]`.
- Saying that "the dependency rule is an application of DIP/OCP" is a reading `[inference]` (`CA12` explicitly cites only the DIP).

## 4. What the corpus does not cover about SOLID

- Liskov's formal statement (1988/1994), the Rectangle/Square example, LSP contracts/pre- and postconditions: `[extrapolation]`.
- The two-item statement of the DIP (Martin, 1996) and the expressions "Fat Interface": `[extrapolation]`.
- SOLID in functional programming or in microservices beyond what `SREL p.2` says about SRP: `[extrapolation]`.
- Code examples for OCP and SOLID in general: the `OCP` and `SREL` PDFs have no code blocks; only `SRP` (the `Employee` class) contains code.
