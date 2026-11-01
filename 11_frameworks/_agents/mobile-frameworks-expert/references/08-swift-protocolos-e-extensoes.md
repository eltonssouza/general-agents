# 08 - Swift: protocols and extensions (SWT p.15-17)

Source SWT (Swift version not stated). Code read by rendering; the `SimpleClass`/`SimpleStructure` and `protocolValue` blocks appear truncated between p.15-17.

## Protocols (SWT p.15-16)
- `protocol` declares a protocol (SWT p.15; code: `ExampleProtocol` requires `var simpleDescription: String { get }` and `mutating func adjust()`) [from source].
- **Classes, enumerations and structures** can adopt protocols (SWT p.15; code: `SimpleClass`, `SimpleStructure`) [from source]. Experiment: add another requirement and see what changes in `SimpleClass` and `SimpleStructure` for them to remain conforming (SWT p.16).
- **`mutating`:** marks, in a structure, a method that **modifies the structure**. A class does not need to mark methods as `mutating`, because class methods **can always** modify it (SWT p.16) [from source].

## Extensions (SWT p.16)
- `extension` adds functionality to an existing type: new methods and **computed properties**. It can add **protocol conformance** to a type declared elsewhere or **imported from a library/framework** (SWT p.16; code: `extension Int: ExampleProtocol`) [from source]. Experiment: extension of `Double` with `absoluteValue` (SWT p.16).

## Protocol as a type (SWT p.16-17)
- The protocol name can be used like any named type, for example for a **collection of objects of different types that follow the same protocol** (SWT p.16; code: `let protocolValue: any ExampleProtocol = a`) [from source]. The text calls this a "boxed protocol" type.
- With a "boxed" protocol type value, **methods outside the protocol definition are not available**; even if the runtime type is `SimpleClass`, the compiler treats it as `ExampleProtocol`, preventing accidental access to the class's extra members (SWT p.16-17) [from source].

## Limits (NOT COVERED)
Protocol inheritance, `associatedtype`, conditional extensions, default implementations in extensions, `some`, `Codable`/`Hashable`, SwiftUI `View`. The use of `any` appears **only** in the code; the text does not explain the difference between `any` and `some`.
