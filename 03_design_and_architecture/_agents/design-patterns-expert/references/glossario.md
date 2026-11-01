# Glossary (terms with the PDF page where the text defines or uses them)

Pages = PDF (see `INDEX.md`). Definitions in English, paraphrased. Terms without a page in the sources appear under "Outside the sources".

### A
- **Abstract Factory**: interface for creating families of related products without concrete classes `[from source] (RG p.17)`.
- **Active Record**: domain object that knows how to load and save itself; suited to simple domains `[from source] (PEAA p.42-43)`.
- **Adapter**: makes objects with incompatible interfaces collaborate `[from source] (RG p.78)`.

### B
- **Bridge**: separates abstraction and implementation into independent hierarchies `[from source] (RG p.89)`.
- **Builder / Director**: step-by-step construction; the director fixes the order of the steps `[from source] (RG p.30, 34)`.
- **Bytecode**: instructions for a virtual machine that give behavior the flexibility of data `[from source] (GPP p.163, 169)`.

### C
- **Cache hit / miss, cache line**: success/failure when fetching from the cache; the CPU brings in a contiguous block (line) `[from source] (GPP p.270-271)`.
- **Chain of Responsibility**: pass the request along a chain of handlers `[from source] (RG p.157)`.
- **Command**: request as an object; "reified method call" `[from source] (RG p.172; GPP p.21-22)`.
- **Component (game pattern)**: entity that spans several domains without coupling them, through components `[from source] (GPP p.209, 213)`.
- **Composite**: part-whole tree with a common interface `[from source] (RG p.101)`.
- **Copy-down delegation**: copy attributes inherited from the parent type to the child at creation `[from source] (GPP p.201-202)`.

### D
- **Data Locality**: organize data in contiguous memory in the order of use for the cache `[from source] (GPP p.267, 273)`.
- **Data Mapper**: layer that isolates the Domain Model and the database, mapping between them `[from source] (PEAA p.43)`.
- **Decorator**: wrapper with the same interface that adds behavior `[from source] (RG p.112)`.
- **Dependency injection (as GPP uses it)**: external code "injects" the dependency (the provider registered in the locator) `[from source] (GPP p.255)`; passing dependencies as parameters `[from source] (GPP p.88-89)`.
- **Dirty flag**: indicates that derived data is out of date relative to the primary data `[from source] (GPP p.295-296)`.
- **Double buffer**: two buffers, *next* (write) and *current* (read), swapped atomically `[from source] (GPP p.116)`.
- **Double dispatch**: the element accepts the visitor and calls the method corresponding to its own class `[from source] (RG p.271)`.

### E
- **Embedded Value / Serialized LOB**: store a value object in the owner's fields / serialize a grouping into a column `[from source] (PEAA p.51-52)`.
- **Event queue**: queue that decouples when a message is sent from when it is processed `[from source] (GPP p.230, 235)`.
- **Intrinsic / extrinsic state**: what the Flyweight stores and shares / what is passed in by the context `[from source] (RG p.137; GPP p.36-37)`.

### F
- **Facade**: simple interface to a complex subsystem `[from source] (RG p.127)`.
- **Factory Method**: method that creates products, overridable by subclasses `[from source] (RG p.45)`.
- **Finite-state machine (FSM)**: finite number of states, one active at a time, predetermined transitions `[from source] (RG p.236; GPP p.96)`.
- **Flyweight**: share common state among many objects to save RAM `[from source] (RG p.135; GPP p.36-37)`.
- **Free list**: list of the free objects of a pool, stored in the memory of the dead objects themselves `[from source] (GPP p.315-316)`.

### G
- **Game loop**: loop that processes input without blocking, updates and renders, controlling the pace of time `[from source] (GPP p.132-133)`.
- **Gateway (Row/Table Data Gateway)**: class per table that isolates the SQL; per row or per table `[from source] (PEAA p.41)`.

### H
- **Hook (Template Method)**: optional step with an empty body `[from source] (RG p.261)`.
- **Hierarchical state machine / Pushdown automaton / Concurrent state machines**: extensions of the FSM `[from source] (GPP p.105-110)`.

### I
- **Identity Map**: registry of the rows read to avoid duplicate objects for one row `[from source] (PEAA p.46)`.
- **Iterator**: object that traverses a collection without exposing its representation `[from source] (RG p.187)`.

### L
- **Lag (in the game loop)**: how far the game clock is behind real time `[from source] (GPP p.138-139)`.
- **Lapsed listener problem**: an observer that was not unregistered is retained by the subject's list `[from source] (GPP p.56-57)`.
- **Lazy Load**: placeholder in place of a reference, loaded on demand `[from source] (PEAA p.46)`.

### M
- **Mediator**: central object that mediates communication between components `[from source] (RG p.199)`.
- **Memento (originator, caretaker)**: state snapshot created by the state owner and kept by a caretaker `[from source] (RG p.211, 214-215)`.

### N
- **Null Object**: object that implements the interface while doing nothing, avoiding null checks `[from source] (GPP p.24, 256)`.

### O
- **Object Pool**: fixed set of objects reused instead of allocating/freeing `[from source] (GPP p.307, 309)`.
- **Observer**: subscription and notification of interested parties `[from source] (RG p.223; GPP p.43-47)`.

### P
- **Prototype**: copy objects through a cloning interface `[from source] (RG p.58)`.
- **Proxy**: stand-in with the same interface as the service `[from source] (RG p.147)`.

### R
- **Record Set**: generic structure of tables and rows `[from source] (PEAA p.41)`.
- **Ring buffer**: queue in a circular array with head and tail `[from source] (GPP p.239-243)`.

### S
- **Service Locator**: global point that locates a service without coupling to the concrete class `[from source] (GPP p.251-252)`.
- **Singleton**: single instance with global access; criticisms `[from source] (RG p.70, 75-76; GPP p.77, 81-84)`.
- **Spatial partition**: structure that organizes objects by position for fast queries `[from source] (GPP p.322, 324)`.
- **State**: object changes behavior by delegating to state objects `[from source] (RG p.235, 238; GPP p.99-101)`.
- **Strategy**: family of interchangeable algorithms `[from source] (RG p.248)`.

### T
- **Template Method**: algorithm skeleton in the superclass `[from source] (RG p.258)`.
- **Type Object**: a "type" class whose instances represent types, instead of subclasses `[from source] (GPP p.191, 195)`.

### U
- **Unit of Work**: records what was read and modified and coordinates the write `[from source] (PEAA p.46)`.
- **Update Method**: the world tells each object to simulate one frame of behavior `[from source] (GPP p.146, 149)`.

### V
- **Visitor**: separates algorithms from the objects they operate on `[from source] (RG p.268)`.

## Outside the sources (do not attribute to any of the 4 PDFs)
Flag argument and CQS as Clean Code rules (table of contents/index only, CC p.8, 48, 54); Transaction Script, Table Module, Domain Model and Service Layer as definitions (PEAA Ch. 2 and 9 absent; they appear only as references in PEAA p.42, 55); Subclass Sandbox (GPP chapter absent, p.190); Interpreter (not in RG; described in passing in GPP p.164-167); SoA/AoS, "ECS" as a recommended technique (only mentioned in passing in GPP p.222), V-BLANK as part of Double Buffer, death spiral, projectile tunneling.
