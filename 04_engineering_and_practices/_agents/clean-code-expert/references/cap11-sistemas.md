# Capítulo 11 — Sistemas (Systems; by Dr. Kevin Dean Wampler)

Source: CL ch. 11, PDF p.152-167 (opening and epigraph on p.152; text from p.153).

Chapter author: Kevin Dean Wampler, not Robert C. Martin (CL p.152). Theme: keeping the code clean at the
highest level, that of the system, using the city metaphor (specialized teams, modules, levels of abstraction).

## Separate constructing a system from using it
- Building a system is a different process from using it (hotel analogy: under construction versus finished) (CL p.153).
- The system should separate startup (creating objects and wiring dependencies) from the run-time logic that follows (CL p.153).
- Separation of concerns is one of the oldest and most important design techniques (CL p.153).
- Lazy initialization mixed into the logic has merits (it only builds when used, never returns null), but it creates a hard-coded dependency on the concrete implementation, complicates testing and gives the method two responsibilities, in a way violating the SRP (CL p.153-154).
- A single occurrence is not serious; the problem is the repetition of these expressions, spreading the configuration strategy across the application, with little modularity and duplication (CL p.154).
- Rule: modularize startup separately from the normal logic and have a global, consistent strategy for resolving the main dependencies (CL p.154).

### Separation of main
- Put all construction in `main` (or in modules called by it); the rest of the system assumes the objects have already been built and wired (CL p.154).
- The dependency arrows cross the main/application boundary in only one direction, away from main: the application does not know the construction process (CL p.154; Figure 11.1 on p.155).

### Factories
- When the application needs to decide when to create an object (e.g. creating a `LineItem` for an `Order`), use the Abstract Factory pattern: the application controls the moment, but the construction details stay on the main side (CL p.154-155).
- The application stays decoupled from how the object is created and can still pass specific arguments to the constructor (CL p.155).

### Dependency injection
- DI is the application of Inversion of Control (IoC) to dependency management; IoC hands secondary responsibilities to dedicated objects, supporting the SRP (CL p.155-156).
- The dominant mechanism that takes over the configuration is usually the main routine or a specific container (CL p.156).
- JNDI lookups are partial DI: the object still actively asks for the dependency by name (CL p.156).
- True DI: the class is completely passive and exposes setters and/or constructor arguments; the container instantiates and wires (CL p.156).
- The objects to use are defined in a configuration file or programmed in a specific construction module (CL p.156).
- Lazy initialization remains useful with DI: containers create objects on demand and offer factories and proxies (CL p.156).

## Scaling up
- It is a myth that you can get a system "right the first time"; implement today's needs and then refactor and expand (CL p.156-157).
- This is the essence of iterative and incremental agility; TDD, refactoring and clean code make it work at the code level (CL p.157).
- Unlike physical systems, software architectures can grow incrementally **if** there is adequate separation of concerns (CL p.157).
- Counterexample: EJB1/EJB2 do not separate concerns and block organic growth (CL p.157).
- In EJB2 the business logic is coupled to the container (subclasses of container types, lifecycle methods), which makes isolated unit testing and reuse difficult (CL p.158).
- EJB2 harms even object orientation (one bean does not inherit from another) and leads to redundant DTOs and copying code (CL p.159).

## Cross-cutting concerns
- Concerns such as persistence, security and transactions cut across the natural boundaries of domain objects; in practice the same code spreads over many objects (CL p.159).
- EJB2 comes close to separation by declaring security and part of persistence in deployment descriptors (CL p.159).
- Aspect-Oriented Programming (AOP) is the general approach to restoring modularity to cross-cutting concerns; aspects declare which points in the system change behavior, in a non-invasive way (CL p.159).
- The book presents three mechanisms in Java: proxies, pure Java AOP frameworks and AspectJ (CL p.159).

### Java proxies
- They serve simple cases, such as wrapping method calls of individual objects or classes (CL p.159).
- JDK dynamic proxies only work with interfaces; for classes a bytecode library is needed (CGLIB, ASM, Javassist) (CL p.159).
- Drawbacks: a lot of code and complexity even in a simple case, which makes clean code difficult; and there is no way to specify execution points across the whole system, which is needed for real AOP (CL p.161).

### Pure Java AOP frameworks
- Tools handle most of the proxies automatically (e.g. Spring AOP and JBoss AOP) (CL p.161).
- Business logic is written as POJOs, with no dependency on enterprise frameworks, simpler to test (CL p.161).
- The cross-cutting concerns (persistence, transactions, security, caching, failover) come in through declarative configuration or APIs; the DI container instantiates and wires the objects (CL p.161).
- The configuration forms a "Boneca Russa" (Russian doll) of decorators around the `Bank` POJO (CL p.162).
- Very little Spring-specific Java code: the application is almost completely decoupled from the framework (CL p.162).
- EJB3 followed the Spring model (XML configuration and/or Java 5 annotations), and the code is much cleaner than EJB2's (CL p.163-164).
- Persistence details in annotations are acceptable if they change little; they can also go into XML, leaving a pure POJO (CL p.164).

### AspectJ
- It is the most complete tool for separating concerns via aspects, an extension of the Java language (CL p.164).
- Pure Java AOP (Spring, JBoss) is enough for 80-90% of the cases in which aspects are useful (CL p.164).
- Cost of AspectJ: new tools and a new language; the annotation form reduces this in part (CL p.164).

## Test drive the system architecture
- With domain logic in POJOs decoupled from the architecture, it is possible to test-drive the architecture and evolve it from simple to sophisticated, adopting technologies on demand (CL p.164).
- BDUF (Big Design Up Front) is not necessary and is even harmful: it inhibits adaptation because of the psychological resistance to discarding effort and because the choice of architecture conditions the ideas that follow (CL p.164).
- You can start with a simple but well-decoupled architecture, deliver user stories and add infrastructure later (CL p.165).
- This does not mean starting without planning: there are expectations about scope, goals and general structure, but the ability to change is preserved (CL p.165).
- A good API should be mostly invisible, so the team can concentrate its effort on the user stories (CL p.165).
- Summary from the book: modularized domains of concern, each in POJOs, integrated by minimally invasive aspect tools, testable like code (CL p.165).

## Optimize decision making
- Modularity and separation of concerns decentralize management and decisions (CL p.165).
- Give responsibilities to the most qualified people and postpone decisions until the last possible moment, so as to decide with the best information (CL p.165).
- A premature decision is made with less customer feedback, less reflection and less implementation experience (CL p.165).

## Use standards wisely, when they add demonstrable value
- Use standards wisely, when they add demonstrable value (CL p.166).
- Teams used EJB2 only because it was a standard and lost focus on the customer; standards help reuse ideas and recruit, but can take long and drift from real needs (CL p.166).
- DSLs (separate languages, scripts or APIs in a standard language) allow code that reads like prose written by a domain expert (CL p.166).
- A good DSL minimizes the communication gap between a domain concept and the code that implements it, reducing translation errors (CL p.166).

## Chapter conclusion
- Systems must be clean too: an invasive architecture harms agility, hides bugs and nullifies the advantages of TDD (CL p.166).
- Create POJOs and use aspect mechanisms to incorporate other concerns without invasion (CL p.166).
- In systems or modules, "use a coisa mais simples que funcione" (use the simplest thing that can possibly work) (CL p.167).

## Examples from the book
- `getService()` excerpt with lazy initialization (CL p.153).
- Figures 11.1 (main separated from construction) and 11.2 (construction by factory) (CL p.155).
- Listings 11-1 and 11-2: local interface and `Bank` entity bean in EJB2 (CL p.157-158).
- Listing 11-3: JDK dynamic proxy for `Bank` persistence (CL p.160-161).
- Listing 11-4: Spring 2.x XML file and Figure 11.3, the "Boneca Russa" of decorators (CL p.162).
- Listing 11-5: `Bank` as an EJB3 entity with annotations (CL p.163-164).

## What the chapter does NOT say / common confusions
- It does not forbid lazy initialization; it criticizes mixing it into run-time logic and spreading it across the system (CL p.154, p.156).
- It does not reject planning; it rejects BDUF (CL p.164-165).
- It does not tell you to use Spring; Spring is an example of a DI container and of pure Java AOP (CL p.156, p.161).
- It does not mention Service Locator; JNDI is treated as "partial" DI [inference] (CL p.156).
- The chapter author is Kevin Dean Wampler (CL p.152).

## [DATED]
- EJB1/EJB2/EJB3, JNDI, deployment descriptors, entity beans and DTOs are the Java EE context of 2008 (CL p.157-164).
- Spring 2.5 with `XmlBeanFactory` and XML configuration; JBoss AOP; AspectJ with the then newly released annotation form (CL p.161-164).
- CGLIB, ASM and Javassist as bytecode libraries; Java 5 annotations presented as a novelty (CL p.159, p.163-164).
- The principles (separating construction from use, DI, POJOs, postponing decisions) do not depend on these technologies [inference].
