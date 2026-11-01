# Structural patterns (RG) and Flyweight according to Nystrom (GPP)

Sources: **RG** (Refactoring.Guru catalog as a 279-page PDF) and **GPP** (Nystrom, 338 pages). Pages = **PDF**. See `INDEX.md`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

RG defines the structural ones as those that explain how to assemble objects and classes into larger structures while keeping them flexible and efficient `[from source] (RG p.12)`. In the PDF: Adapter p.78-88, Bridge p.89-100, Composite p.101-111, Decorator p.112-126, Facade p.127-134, Flyweight p.135-146, Proxy p.147-156.

## 1. Adapter (RG p.78-88)
- Intent: let objects with incompatible interfaces collaborate; alias Wrapper `[from source] (RG p.78)`.
- Problem: an app that consumes XML data and an analysis library that only accepts JSON; changing the library may break code or be impossible without the source `[from source] (RG p.79)`.
- Solution: an object that converts the interface of one object so another can understand it; the wrapped object does not know about the adapter; can be bidirectional `[from source] (RG p.79-80)`.
- Two forms: *object adapter* (composition, works in all popular languages) and *class adapter* (inheritance; requires multiple inheritance, as in C++) `[from source] (RG p.81-83)`.
- When to use: an existing class with an incompatible interface; reuse several subclasses lacking a common functionality that does not fit in the superclass (similar to Decorator) `[from source] (RG p.85-86)`. Steps `[from source] (RG p.86-87)`.
- Pros: SRP (conversion separated from the logic) and Open/Closed. Con: complexity; sometimes it is simpler to change the service class `[from source] (RG p.87)`.
- Contrasts `[from source] (RG p.87)`: Bridge is usually designed up front, Adapter is applied to an existing app; Adapter changes the interface, Decorator keeps or extends it and allows recursive composition; Proxy keeps the interface; Facade defines a new interface for a whole subsystem, Adapter usually wraps a single object.

## 2. Bridge (RG p.89-100)
- Intent: split a large class (or closely related classes) into two hierarchies, abstraction and implementation, that can be developed independently `[from source] (RG p.89)`.
- Illustrated problem: `Shape` with `Circle` and `Square` x colors `Red` and `Blue` yields **four** combinations (e.g., `BlueCircle`); adding a triangle or a color makes the hierarchy grow geometrically `[from source] (RG p.90)`.
- Solution: replace inheritance with composition; extract one dimension into another hierarchy and reference it `[from source] (RG p.90-91)`. "Abstraction" = high-level control layer (e.g., GUI) that delegates to the "implementation" (platform/API); they are not the language's interfaces/abstract classes `[from source] (RG p.91-92)`.
- When to use: split a monolithic class with several variants; extend in orthogonal dimensions; swap implementations at runtime `[from source] (RG p.97-98)`. Runtime swapping is why many people confuse Bridge with Strategy `[from source] (RG p.98)`.
- Con: may complicate an already cohesive class `[from source] (RG p.98)`. Relations: Abstract Factory with Bridge; Builder with Bridge; Bridge, State, Strategy (and partly Adapter) have similar composition-based structures, but solve different problems `[from source] (RG p.99)`.

## 3. Composite (RG p.101-111)
- Intent: compose objects into trees and treat them as individual objects; alias Object Tree `[from source] (RG p.101)`.
- It only makes sense when the app's core model can be represented as a tree (Products and Boxes example, order total price) `[from source] (RG p.102-103)`.
- Solution: a common interface with one method (e.g., price); the leaf returns its own value, the container walks its children; the client does not need to know concrete classes `[from source] (RG p.103, 105)`.
- Implementation steps; declaring `add/remove` in the component interface violates ISP (empty methods in the leaf) but lets the client treat everything the same `[from source] (RG p.109)`.
- Con: it may be hard to define a common interface for very different classes, forcing excessive generalization `[from source] (RG p.109-110)`.
- Relations: Builder to assemble trees; Chain of Responsibility; Iterator and Visitor to traverse/operate; shared leaves as Flyweight; Composite x Decorator (Decorator is like a Composite with a single child and *adds* responsibilities, Composite merely "sums" results) `[from source] (RG p.110)`.

## 4. Decorator (RG p.112-126)
- Intent: attach behavior by placing the object in wrappers that contain the behavior; alias Wrapper `[from source] (RG p.112)`.
- Problem: notification library; subclasses for each channel (e-mail, SMS, Facebook, Slack) and combinations cause a subclass explosion `[from source] (RG p.113-114)`.
- Inheritance is static and a class has only one parent in most languages; aggregation/composition lets you swap the "helper" at runtime `[from source] (RG p.114-115)`.
- Solution: the wrapper implements the same interface as the wrapped object; several are stacked; the last on the stack is the one the client uses `[from source] (RG p.115-117)`. Structure `[from source] (RG p.118)`. Encryption + compression example over `DataSource` `[from source] (RG p.119-122)`.
- When to use: assign behaviors at runtime without breaking client code; when extending by inheritance is not viable (`final` class) `[from source] (RG p.122-123)`.
- Cons: hard to remove a specific wrapper from the stack, hard to make behavior independent of order, ugly initial configuration `[from source] (RG p.123)`.
- Relations: Decorator keeps/extends the interface (Adapter changes it; Proxy keeps it); CoR x Decorator (CoR handlers can interrupt the flow, decorators cannot); Decorator changes the "skin", Strategy changes the "guts"; Decorator x Proxy: similar structures, different intents; the Proxy usually manages the service's lifecycle, the composition of Decorators is controlled by the client `[from source] (RG p.124-125)`.

## 5. Facade (RG p.127-134)
- Intent: simplified interface to a library, framework or complex set of classes `[from source] (RG p.127)`.
- Solution: a class that exposes only what clients really use (example: `encode(filename, format)` over a video-conversion library) `[from source] (RG p.128)`. The subsystem does not know the facade; additional facades avoid bloating the first one `[from source] (RG p.129)`.
- When to use: a limited, direct interface to a complex subsystem; structure a subsystem in layers with one facade per level (similar to Mediator) `[from source] (RG p.131-132)`.
- Con: the facade can become a *god object* coupled to all the app's classes `[from source] (RG p.132)`.
- Relations: Facade x Adapter, Abstract Factory, Mediator (centralizes communication; the Facade adds no functionality and the subsystem communicates directly), Singleton, Proxy (same interface as the service) `[from source] (RG p.133)`.

## 6. Flyweight (RG p.135-146; GPP p.33-42)
- Intent: fit more objects in RAM by sharing common parts of the state; alias Cache `[from source] (RG p.135)`.
- Problem: a particle system (bullets, missiles, shrapnel) exhausts RAM on a weak machine `[from source] (RG p.136)`.
- **Intrinsic state** = constant data that stays in the object (others only read it); **extrinsic state** = what changes and is supplied by the user, passed to the methods `[from source] (RG p.137-138)`. Extrinsic state usually goes to the container or to a context class `[from source] (RG p.138-139)`. The flyweight must be **immutable** and initialized only in the constructor; a *flyweight factory* keeps the pool `[from source] (RG p.139-140)`.
- It is "merely an optimization": only use it if the app really has the RAM problem from many similar objects and there is no better solution `[from source] (RG p.140, 143-144)`.
- Cons: may trade RAM for CPU cycles; much more complicated code `[from source] (RG p.144-145)`. Relations: Composite leaves as Flyweight; Flyweight x Singleton (many x one; immutable x possibly mutable) `[from source] (RG p.145)`.
- **GPP**: forest example (`Tree` with mesh/textures shared in `TreeModel`) and *instanced rendering*; Nystrom says Flyweight may be the only GoF pattern with direct hardware support `[from source] (GPP p.33-36)`. He calls the intrinsic state "context-free" `[from source] (GPP p.36-37)`. Grid terrain example: instead of `enum` + `switch`, an immutable `Terrain` and a grid of pointers to a few shared instances (grass, hill, river) `[from source] (GPP p.37-41)`. On performance, in his tests there was no penalty compared to the `enum` and "profile first" `[from source] (GPP p.41-42)`. Contrast with Type Object: that one reduces classes; Flyweight is only about efficiency `[from source] (GPP p.35)`. *State* objects without their own fields can be flyweights `[from source] (GPP p.42)`.
- Numbers such as "1000 x 1000 tiles", "500 KB per texture" or "gigabytes" are **not** in GPP: do not attribute them.

## 7. Proxy (RG p.147-156)
- Intent: substitute or placeholder for another object, controlling access and allowing action before/after the request `[from source] (RG p.147)`.
- Problem: a heavy object (slow database queries) with lazy initialization duplicated in all clients `[from source] (RG p.148)`. Solution: a proxy with the **same interface** as the service, which creates the real object on demand and delegates `[from source] (RG p.148-149)`.
- Listed uses: virtual proxy (lazy), protection (access control), remote, logging, caching, smart reference `[from source] (RG p.153-154)`. Steps `[from source] (RG p.154-155)`.
- Pros: control without the clients knowing, lifecycle management, works even when the service is unavailable, Open/Closed; cons: more classes, response may be delayed `[from source] (RG p.155)`.
- Alternative when an interface cannot be extracted: the proxy inherits from the service class `[from source] (RG p.154)`.

## 8. Adapter x Facade x Proxy (summary)
`[inference]` from RG p.87, 124-125, 133, 155: Adapter changes the interface of an object; Facade creates a new, simple interface for a subsystem; Proxy keeps exactly the service's interface.

## 9. What the PDF does NOT contain
- Examples of Spring/Hibernate/Java dynamic proxies, Angular/React HOCs: `[extrapolation]`.
- Memory calculations such as "millions of tiles = gigabytes": not present.
