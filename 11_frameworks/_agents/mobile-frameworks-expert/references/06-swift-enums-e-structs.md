# 06 - Swift: enumerations and structures (SWT p.11-14)

Source SWT (Swift version not stated). Code read by rendering; the `Rank`, `Suit` and `Card` boxes appear truncated.

## Enumerations (SWT p.11-13)
- `enum` creates an enumeration; like classes and all other named types, **enums can have methods** (SWT p.11; code: `enum Rank: Int` with `simpleDescription()` and `switch self`) [from source].
- **Raw values:** by default they start at zero and increment by one; you can change this by specifying values (in the example `ace` is 1 and the rest follow in order). The raw type can be integer, **string or floating point**. `rawValue` accesses the value (SWT p.12) [from source]. Experiment: a function that compares two `Rank`s by their raw values.
- **`init?(rawValue:)`** creates the case from a raw value and returns **the case or `nil`** if nothing matches (SWT p.12; code: `Rank(rawValue: 3)` inside `if let`) [from source].
- The cases are **real values**, not just another way of writing the raw values; when there is no meaningful raw value, **you do not need to provide one** (SWT p.12; code: `Suit` without a raw type) [from source]. Experiment: `color()` method on `Suit` (SWT p.13).
- **Full vs. shorthand form:** when assigning the value to the constant without an explicit type, `Suit.hearts` is used; inside the `switch`, `.hearts` is enough because the type of `self` is already known; use the shorthand form whenever the type is known (SWT p.13) [from source].
- **Raw values vs. associated values:** with raw values, each case always has the same value, defined at declaration. Alternatively, the case can have **associated values**, set when the instance is created and which can differ between instances; they behave like stored properties of the case instance (SWT p.13) [from source]. Example from the text: a server response with sunrise/sunset times **or** an error description (code: `ServerResponse.result(String, String)` and `.failure(String)`; `case let .result(sunrise, sunset)` extracts the values when matching the pattern) (SWT p.13) [from source]. Experiment: add a third case and handle it in the switch.

## Structures (SWT p.13-14)
- `struct` creates a structure. Structures support much of what classes support, including **methods and initializers** (SWT p.13) [from source].
- **Most important difference:** structures are **always copied** when passed around in code; classes are **passed by reference** (SWT p.13) [from source].
- Code: `struct Card { var rank: Rank; var suit: Suit; func simpleDescription() ... }` and `Card(rank: .three, suit: .spades)` (SWT p.13-14) [from source]. Experiment: a function that returns a full deck (one card for each combination of rank and suit) (SWT p.14).

## Limits (NOT COVERED)
`indirect` enums, `CaseIterable`, enums as protocols, memberwise initializer (the tour uses `Card(rank:suit:)` but does not explain it), `Hashable`, conformance to `Equatable` as a subject (it only appears in the `where` code, SWT p.19), copy-on-write, `inout`.
