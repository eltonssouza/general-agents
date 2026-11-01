# 05 - Swift: classes and objects (SWT p.8-11)

Source SWT (Swift version not stated). Code read by rendering; several boxes truncated (p.9-10: `Square`).

## Declaration and instance (SWT p.8-9)
- `class` + name creates a class. Properties are declared as constants/variables, but in the class context; methods and functions likewise (SWT p.8; code: `Shape` with `numberOfSides` and `simpleDescription()`) [from source]. Experiment: add a `let` property and a method with an argument (SWT p.9).
- Instance: parentheses after the class name; **dot syntax** for properties and methods (SWT p.9) [from source].

## Initializer, self, deinit (SWT p.9)
- The simple version of `Shape` has no initializer; use `init` (code: `NamedShape`) [from source].
- `self` distinguishes the `name` property from the `name` argument of `init`; initializer arguments are passed like a function call when creating the instance (SWT p.9) [from source].
- **Every property needs a value**: at declaration (like `numberOfSides`) or in the initializer (like `name`) (SWT p.9) [from source].
- `deinit` creates a **deinitializer** for cleanup before the instance is deallocated (SWT p.9) [from source].

## Inheritance and override (SWT p.9-10)
- Subclass: superclass name after the class name, separated by a colon. It is **not required** to inherit from a standard root class: you can include or omit a superclass (SWT p.9) [from source].
- Methods that override the superclass implementation take **`override`**; overriding **without** `override` is a compiler error, and `override` that overrides nothing is also detected as an error (SWT p.9) [from source].
- Code: `Square: NamedShape` with `init(sideLength:name:)`, `super.init(name:)` and `override func simpleDescription()` (SWT p.9-10) [from source]. Experiment: create `Circle` with radius and name, with `area()` and `simpleDescription()` (SWT p.10).

## Computed properties and initialization order (SWT p.10-11)
- Besides stored properties, properties can have a **getter and setter** (SWT p.10; code: `perimeter` in `EquilateralTriangle`) [from source]. In the setter, the new value has the implicit name **`newValue`**; an explicit name goes in parentheses after `set` (SWT p.10) [from source].
- The initializer of `EquilateralTriangle` has **three steps**: (1) set the properties declared by the subclass; (2) call the superclass initializer; (3) change properties defined by the superclass; other setup that uses methods, getters or setters can also be done at this point (SWT p.10-11) [from source].
- **willSet/didSet:** when you do not need to compute the property but need to run code before/after assigning a new value; it runs whenever the value changes **outside an initializer** (SWT p.11; code: `TriangleAndSquare` keeps the triangle's side equal to the square's) [from source].

## Optional chaining (SWT p.11)
- When working with optionals, `?` before methods, properties and subscripting: if the value before `?` is `nil`, the rest is ignored and the result of the whole expression is `nil`; otherwise the value is unwrapped and the rest acts on it; in both cases the result is an **optional** (SWT p.11; code: `optionalSquare?.sideLength`) [from source].

## Limits (NOT COVERED in the tour)
Access control, `final`, convenience/required/failable initializers in classes (only enum's `init?(rawValue:)` appears), ARC and reference cycles (`weak`/`unowned`), `static`/`class` members, `lazy` properties, property wrappers. Do not complete the truncated code as if it were from the tour.
