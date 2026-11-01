# JavaScript glossary

This file defines terms (concepts, Spec jargon and environment vocabulary), not the built-in methods, which have their own files. Sources: **Spec** = ECMA-262, 17th edition (ECMAScript 2026), normative; **EJ1** = *Eloquent JavaScript* in English, actually the 1st edition (2007/2013), so everything from it is **[DATED]**; **EJpt** = *Eloquent JavaScript* in Portuguese, modern edition (ES2015+). Pages are those of the PDF, not the printed ones. Each entry gives a short definition, pages and, when applicable, a label: **[DATED]**, **[VERSION-DEPENDENT]**, **[HOST]**, **[inference]**, **[extrapolation]**. The Spec almost never says in which edition a feature entered; when the source gives no date, "version not stated in the sources" applies. Terms are grouped by theme and, within each theme, follow the order of the original Portuguese headwords (so they may not be strictly alphabetical in English); use Grep on the `##` titles to reach the theme and on the bold term to reach the entry. When a term fits two themes, it sits in only one and the other refers to it.

## Contents

1. Types, values and coercion
2. Operators, expressions and equality
3. Objects, properties and prototypes
4. Functions, scope, closures, hoisting and TDZ
5. `this`
6. Classes
7. Iteration and generators
8. Asynchrony: Promise, Job, async/await, event loop
9. Modules
10. Text, Unicode, regular expressions, dates and JSON
11. Collections and binary data
12. Memory, garbage collection, WeakRef and concurrency
13. Errors and exceptions
14. Syntax and grammar
15. Strict mode and legacy
16. Spec jargon
17. Environment [HOST]: browser, DOM, Node, timers
18. Divergences and observations between sources

## 1. Types, values and coercion

- **Boolean** — type with two values, `true` and `false` (Spec p.50). "Falsy" values in conversion: `false`, `undefined`, `null`, `+0`, `-0`, `NaN`, `0n` and the empty string; everything else is truthy (Spec p.89). In browsers, objects with `[[IsHTMLDDA]]` are also falsy [HOST] (Spec p.89, p.858).
- **BigInt** — primitive for arbitrary-precision integers (Spec p.33). Literal with suffix `n` (Spec p.257); `>>>` on BigInt always throws (Spec p.54); `ToBigInt` with an invalid String throws `SyntaxError` (Spec p.95). The Spec does not define mixed Number/BigInt operands in mathematical notation (Spec p.48).
- **Type coercion** — silent conversion of values to the type an operator requires (EJpt p.24). In the Spec, conversions are explicit abstract operations (`ToNumber`, `ToString`, ...) (Spec p.88–97).
- **Identity effect (value with/without identity)** — with identity: objects and Symbols that did not come from `Symbol.for`; without: primitives such as Numbers and Strings (Spec p.49).
- **Infinity / -Infinity** — values of the number type, alongside `NaN` (EJpt p.15, p.17–18).
- **Integral Number** — finite Number whose mathematical value is an integer (Spec p.47).
- **Mutability / immutability** — ability to change a value after it is created; primitives are immutable, objects are not (EJpt p.81). Strings are immutable (EJ1 p.11–13) [DATED].
- **NaN** — "not a number", but of the number type; it is not equal to itself and contaminates calculations (EJpt p.18, p.22, p.24; EJ1 p.28 [DATED]). Tested with `isNaN` in the old book (EJ1 p.28) [DATED].
- **Null (type/value `null`)** — type with a single value, intentional absence of an object (Spec p.32, p.50). EJ1 only introduces it on p.26 and does not list it among the types on p.9 (EJ1 p.9, p.26) [DATED]. `typeof null` gives `"object"`, called a historical accident (EJpt p.104).
- **Number** — 64-bit value (EJpt p.15); in the Spec it is IEEE 754-2019 binary64 (Spec p.47). EJ1 says integers below 2^52 are exact and fractions approximate (EJ1 p.9–10) [DATED]. Safe limit: `Number.MAX_SAFE_INTEGER` = 2^53 − 1 (Spec p.489).
- **Object (type Object)** — member of the Object type; a function is a callable object (Spec p.34). Collection of properties (EJpt p.78). See section 3.
- **Primitive (primitive value)** — member of Undefined, Null, Boolean, Number, BigInt, Symbol or String; data represented at the lowest level of the implementation (Spec p.30–31).
- **Sentinel (value)** — unique object used only for comparison, as an end or found marker (EJ1 p.74, p.108) [DATED].
- **String** — sequence of 16-bit elements (UTF-16 code units), up to 2^53 − 1 elements; `length` counts units, not characters (Spec p.50–51; EJpt p.18–19). Single quotes, double quotes or backticks (EJpt p.18–19). See section 10.
- **Symbol** — unique, immutable primitive usable as a property key, with `[[Description]]` (Spec p.51). Introduced in 2015 according to the book **[VERSION-DEPENDENT]** (EJpt p.141–142). See **well-known symbol** (section 16).
- **Template literal** — string between backticks, with multiple lines and `${}` (EJpt p.20). See section 14.
- **ToBigInt** — strict conversion; an invalid String throws `SyntaxError` (Spec p.95).
- **ToBoolean** — see **Boolean** above (Spec p.89).
- **ToInt32 / ToUint32** — modular conversion to 32-bit integers, basis of the bitwise operators [inference] (Spec p.92–93).
- **ToLength / ToIndex / ToPropertyKey** — coercions for array-like size (ceiling 2^53 − 1), index (RangeError outside the range) and property key (Spec p.97).
- **ToNumber / StringToNumber** — conversion to Number; invalid text becomes `NaN`; Symbol and BigInt throw `TypeError` (Spec p.89–91).
- **ToNumeric** — conversion that returns Number or BigInt, used in arithmetic and update operators (Spec p.302, p.317).
- **ToObject** — `undefined`/`null` throw `TypeError`; primitives become wrapper objects with the corresponding data slot (Spec p.96–97).
- **ToPrimitive / OrdinaryToPrimitive** — conversion of an object to a primitive via `@@toPrimitive`, `valueOf`, `toString` (Spec p.88–89). With no hint, `Date` acts as a string and the others as a number (Spec p.318, p.537).
- **ToString** — String passes through; Symbol throws `TypeError`; `undefined`/`null`/booleans become the corresponding text; an object goes through ToPrimitive(STRING) (Spec p.96).
- **ToUint8Clamp** — clamps to 0–255 and rounds ties to even (Spec p.94).
- **typeof** — unary operator that returns a string with the type name (EJ1 p.12; EJpt p.20). For an array it gives `"object"` (EJpt p.80; EJ1 p.235).
- **Undefined (type/value `undefined`)** — type with a single value; it is the value of an unassigned variable (Spec p.50). EJ1 treats `undefined` and `null` as absence of value and `null == undefined` is true (EJ1 p.25–26) [DATED].
- **Wrapper (object)** — Boolean/Number/String/Symbol/BigInt object with an internal slot holding the primitive (Spec p.32–34, p.96–97).

## 2. Operators, expressions and equality

- **`??` (nullish coalescing)** — returns the right side only if the left is `null` or `undefined` (EJpt p.26). Also in `??=` (Spec p.316).
- **`?.` (optional access/chain)** — read that returns `undefined` if the base is `null`/`undefined`; the whole chain short-circuits (EJpt p.98; Spec p.297).
- **Destructuring assignment** — left side in an object/array pattern; requires `RequireObjectCoercible` on objects and an iterator on arrays (Spec p.319–323). See also **destructuring** (section 4).
- **Short-circuit** — not evaluating the right operand when the left already decides: `&&`, `||`, `??`, `?.`, `&&=`, `||=`, `??=` (Spec p.297, p.313, p.316; EJpt p.26–27; EJ1 p.28–29). In the old book `||` and `&&` return one of the operands (EJ1 p.28–29) [DATED].
- **Side effect** — change in the world or in the program state made by a statement or function (EJ1 p.14–15; EJpt p.29, p.35).
- **Expression** — code fragment that produces a value (EJ1 p.14; EJpt p.29).
- **Pure function** — same result for the same arguments and no side effects (EJ1 p.30; EJpt p.68).
- **Strict equality (`===`, `!==`)** — comparison without conversion (EJpt p.25; EJ1 p.26). In the Spec: `IsStrictlyEqual` (Spec p.101–102).
- **IsLooselyEqual** — semantics of `==` (Spec p.101–102). On objects, `==` compares identity (EJpt p.82).
- **Statement** — complete sentence of the program, a unit larger than the expression (EJ1 p.14; EJpt p.29).
- **Unary / binary / ternary operator** — operate on one, two or three values; `-` can be unary and binary; `?:` is the ternary (EJ1 p.12; EJpt p.20, p.23).
- **Precedence** — order in which operators are applied (EJ1 p.14).
- **SameValue / SameValueZero** — equality that distinguishes (SameValue) or does not (Zero) `+0` from `-0`; both treat `NaN` as equal to `NaN` (Spec p.99–100). SameValueZero is the one used by `includes` and by Map/Set (Spec p.628, p.675, p.682).
- **ToPrimitive with no hint in `+`** — see section 1.

## 3. Objects, properties and prototypes

- **`__proto__` (legacy)** — optional/legacy accessor to read and replace the prototype [DATED] (Spec p.468).
- **Accessor property / data property** — property with get/set functions vs with a direct value (Spec p.67). Getter/setter in classes (EJpt p.139–141).
- **Array** — sequence of values between square brackets, indices from 0 (EJpt p.75; EJ1 p.44, p.47–48). In the Spec it is an exotic object (see section 16).
- **Array index** — property name that is an integer from +0 to 2^32 − 2 (Spec p.67).
- **Array-like** — object whose `length` can be read and converted by ToLength (Spec p.107, p.616); it is what the generic methods of `Array.prototype` accept (Spec p.620).
- **Hole** — index without an own property; skipped by `forEach`/`map`/`indexOf`, read as `undefined` by `includes`/`find*` (Spec p.625, p.628, p.641).
- **Prototype chain** — sequence of objects consulted when resolving a property (Spec p.29). Reading goes up the chain; writing always goes to the object itself (EJ1 p.127–128 [DATED]; EJpt p.129).
- **Constructor / `new`** — function that initializes instances; `new` links the prototype and sets `this` (EJpt p.131; EJ1 p.56, p.126–127 [DATED]).
- **Property Descriptor** — Record/object with property attributes; can be data, accessor or generic (Spec p.82, p.462–463).
- **Destructuring** — see section 4.
- **Dictionary (EJ1)** — term from the old book for an object used as a name→value map (EJ1 p.132) [DATED].
- **Enumerable own property** — enumerable own property, basis of `Object.keys/values/entries/assign` (Spec p.461, p.462, p.465, p.466).
- **Extensible (`[[Extensible]]`)** — boolean slot; false prevents adding properties and replacing the prototype, and does not go back to true (Spec p.197).
- **Bound function** — exotic function created by `bind`, with `this` and initial arguments fixed and no `prototype` (Spec p.216–217, p.473).
- **GetPrototypeFromConstructor** — reads `constructor.prototype`, with fallback to the intrinsic of the constructor's realm (Spec p.203).
- **hasOwnProperty / propertyIsEnumerable** — test for own / enumerable property, to filter inherited and hidden ones in `for/in` (EJ1 p.130–131) [DATED].
- **Inheritance** — new type based on another; in EJ1 by `clone`, `inherit`, `create`, `extend` (EJ1 p.152, p.159, p.161) [DATED]; in EJpt by `extends`/`super` (EJpt p.146). Multiple inheritance is not supported by the chain (EJ1 p.164) [DATED]; a mix-in copies methods (EJ1 p.164) [DATED].
- **Object identity** — two bindings refer to exactly the same object (EJpt p.82).
- **instanceof** — tests whether a constructor's `prototype` is in the object's chain (EJ1 p.163) [DATED]; consults `Symbol.hasInstance` (Spec p.474–475).
- **Integrity level (SEALED/FROZEN)** — levels of fixing own properties, applied by `seal`/`freeze` (Spec p.106, p.463, p.465).
- **Interface / encapsulation** — small set of public operations and hiding of the rest (EJpt p.126; EJ1 p.133 [DATED]).
- **Method** — property that holds a function (EJpt p.75–77; EJ1 p.43, p.49).
- **Internal method / internal slot** — internal operation or state of objects, between `[[ ]]`, outside the language (Spec p.68–69). See section 16.
- **"Persistent" data object** — immutable structures treated as values; updating creates a new object (EJpt p.156, p.347).
- **Exotic object** — object without the default behavior of some internal method (Spec p.31, p.69). See section 16.
- **Own key order** — array indices ascending, then Strings by creation, then Symbols by creation (Spec p.202).
- **Polymorphism** — code that works with any value that offers the expected interface (EJpt p.138; EJ1 p.150–151 [DATED]).
- **Property** — associates a key (String or Symbol) with a value, directly or through accessor functions (Spec p.34); accessed with a dot or brackets (EJpt p.75–77).
- **Property attributes** — `[[Value]]`, `[[Writable]]`, `[[Get]]`, `[[Set]]`, `[[Enumerable]]`, `[[Configurable]]` (Spec p.68).
- **Hidden / "active" property** — in the old book: does not appear in `for/in` (EJ1 p.66); the one whose change has an effect, like `length` (EJ1 p.67) [DATED].
- **Private property (`#`)** — accessible only inside the class declaration (EJpt p.133). See **Private Name** (section 6).
- **Prototype** — object consulted when the property does not exist on the object itself (EJpt p.129; EJ1 p.127 [DATED]). A function's `prototype` is what instances inherit.
- **Property shorthand** — `{events}` is equivalent to `{events: events}` (EJpt p.83).
- **Spread / rest** — `...value` spreads elements or properties; `...name` in parameters collects the rest into an array (EJpt p.94–95).
- **Symbol.toStringTag** — string on the object that defines the tag of `Object.prototype.toString` (Spec p.468).
- **Symbol.unscopables / `@@unscopables`** — list of names ignored by `with`, e.g.: methods of `Array.prototype` (Spec p.169, p.643–644) [DATED].
- **ValidateAndApplyPropertyDescriptor** — central compatibility rule when defining properties, respecting `configurable`/`writable` (Spec p.199–200).

## 4. Functions, scope, closures, hoisting and TDZ

- **`arguments`** — array-like object with the call's arguments, with `length`, without array methods (EJ1 p.64) [DATED]. In the Spec there is the mapped arguments exotic object, linked to the parameters in sloppy functions with simple parameters (Spec p.221–224).
- **Arrow function** — function without its own `this`, `arguments`, `super`, `new.target` (Spec p.364); without its own `this` also in EJpt p.127–128. Concise body (expression) or block (Spec p.363).
- **Optional argument** — omittable parameter; in the old book detected by `arguments.length` (EJ1 p.64) [DATED].
- **Binding** — name bound to a value (variable); reassignable, except `const` (EJpt p.30–32). Immutable binding: assignment throws `TypeError` in strict mode (Spec p.167).
- **Block** — braces grouping statements (EJpt p.37). `let`/`const`/`class` create block scope (EJpt p.52–54; Spec p.326); in the old book a block does not create scope (EJ1 p.19, p.34) [DATED].
- **BlockDeclarationInstantiation** — creation of the block's bindings on entry (Spec p.326–327).
- **BoundNames / `*default*`** — names introduced by a declaration; `*default*` is the synthetic name of the anonymous `export default` (Spec p.118).
- **Callback** — function passed to be called when something finishes (EJpt p.238–239).
- **Closure** — function that keeps access to the environment in which it was created (EJpt p.60; EJ1 p.35 [DATED]). In the Spec, `[[Environment]]` is the captured environment and becomes the `[[OuterEnv]]` of the invocations (Spec p.180).
- **Composition / partial application** — `compose` and `partial` from the old book (EJ1 p.100–101) [DATED].
- **ContainsExpression / IsSimpleParameterList** — whether the parameters have defaults/computed keys; whether they only have simple names (Spec p.356–358).
- **CreatePerIterationEnvironment** — copy of the `for` loop's `let` bindings on each iteration; basis of closures in `for (let ...)` (Spec p.337).
- **Destructuring** — binding elements/properties by pattern in a declaration or parameter (EJpt p.97–98).
- **(Variable) environment** — set of bindings existing at a moment (EJ1 p.16, p.33; EJpt p.33). See **Environment Record** (section 16).
- **Scope (global / local / lexical)** — where a binding is visible; lexical depends on the position in the text (EJpt p.52–54; EJ1 p.34).
- **ExpectedArgumentCount** — parameters before the first default/rest; basis of `length` [inference] (Spec p.359).
- **Function expression / anonymous function** — function created where an expression is expected, name not required (EJ1 p.39).
- **Function** — piece of program wrapped in a value, invoked with parentheses (EJ1 p.16).
- **Higher-order function** — receives or returns functions (EJ1 p.79; EJpt p.110).
- **GetThisEnvironment** — finds the environment that provides `this`, skipping arrows (Spec p.186).
- **Hoisting** — function declarations apply across the whole scope, even above the text of the definition (EJpt p.55; EJ1 p.39). Neither book uses the word "hoisting" (EJpt p.55; EJ1 p.39). In the Spec: `var` hoisted to the function/script scope (Spec p.128–135) and functions instantiated at the start (Spec p.154, p.213).
- **LexicallyDeclaredNames / VarDeclaredNames** — names of lexical scope vs. hoisted by `var`; at the top of a Script functions count as `var`, in a Module as lexical (Spec p.124–131).
- **LoopContinues** — decides whether a `continue` completion keeps the loop going, considering labels (Spec p.334).
- **MakeMethod / home object (`[[HomeObject]]`)** — associates a method with the object that contains it; basis of the `super.prop` lookup (Spec p.204, p.366–367).
- **NamedEvaluation / IsAnonymousFunctionDefinition** — gives an inferred name to an anonymous function/class assigned to a name (Spec p.149–150, p.315, p.328).
- **Rest parameter / default value** — see **Spread / rest** (section 3) and **ExpectedArgumentCount**.
- **Call stack** — where the context of each call lives; overflow gives "too much recursion" (EJpt p.57–58; EJ1 p.36–37).
- **Polluting the global environment** — occupying too many names in the global scope (EJ1 p.65–66, p.170) [DATED].
- **Recursion** — function that calls itself (EJpt p.61; EJ1 p.36–37).
- **ResolveBinding / GetIdentifierReference** — lexical resolution of a name going up the chain; end of chain = unresolvable reference (Spec p.179, p.185).
- **Tail call / tail position** — final call that can reuse the current context; only in strict mode and outside async/generators (Spec p.392); `PrepareForTailCall` discards the context's resources (Spec p.397).
- **TDZ (Temporal Dead Zone)** — period in which `let`/`const`/`class` exist but cannot be accessed; reading or writing throws `ReferenceError` (Spec p.167–168). The name TDZ does not appear in any of the three sources **[extrapolation]** (the Spec speaks of an uninitialized binding, p.167–168); on Spec p.213 the text only says that lexical names are instantiated but not initialized, and the `ReferenceError` there is [inference]. The old book, which only has `var`, does not cover it.
- **VariableEnvironment / LexicalEnvironment** — environments of the context: one resolves identifiers, the other receives the `var`s, initialized with `undefined` (Spec p.185, p.328).
- **Variable (`var`)** — name that points to a value; tentacle metaphor (EJ1 p.15) [DATED]. In EJpt the central term is **binding** (EJpt p.30).

## 5. `this`

- **`this`** — binding of the method call that points to the receiver object; an arrow has none of its own (EJpt p.127–128). In EJ1, `this` lost in inner functions is worked around with `bind(func, object)` and `method(object, name)` (EJ1 p.142) [DATED].
- **`apply`** — function method that calls with a given `this` and arguments from an array (EJ1 p.79–80, p.126) [DATED].
- **Function Environment Record** — holds `this`, `new.target` and `super` state per invocation (Spec p.171–172).
- **`[[ThisMode]]`** — LEXICAL, STRICT or GLOBAL; defines how `this` is interpreted in the function (Spec p.204).
- **Uncoerced `this` (strict)** — in strict mode `this` is not coerced to an object (Spec p.861).
- **Module `this`** — `undefined` in module scope (Spec p.178–179).

## 6. Classes

- **Static block (`static { }`)** — executed once, during class evaluation (Spec p.376, p.386).
- **Class field** — `name = value`, evaluated as an internal function at instantiation (Spec p.382).
- **`class`** — introduced in the 2015 edition according to the book **[VERSION-DEPENDENT]** (EJpt p.132); before, plain function and `prototype` (EJpt p.132). Class expression possible (EJpt p.133).
- **ClassHeritage** — `extends Expr` clause (Spec p.375).
- **Default class constructor** — implicit; in derived classes it passes the arguments to the parent; throws `TypeError` without `new` (Spec p.384–385).
- **`extends` / `super`** — subclass that reuses the superclass (EJpt p.146); `super` uses the `[[HomeObject]]` (Spec p.204, p.366–367).
- **Getter / setter / `static`** — methods triggered on read/write and methods kept on the constructor (EJpt p.139–141).
- **`new.target`** — meta-property with the constructor invoked by `new` (Spec p.301).
- **Private Name (`#x`)** — unique key created per class, per evaluation; kept in the PrivateEnvironment Record and in PrivateElement (Spec p.86–87, p.181, p.384, p.387).
- **PrivateEnvironment Record** — see section 16.

## 7. Iteration and generators

- **Array Iterator** — iterator of `entries`/`keys`/`values`; walks an array-like by index recomputing `length` (Spec p.644–645).
- **Async-from-Sync Iterator** — adapter that makes a synchronous iterator asynchronous (Spec p.762–763).
- **Async Iterator** — iterator whose `next` returns a promise of IteratorResult (Spec p.751–752).
- **Async generator** — `async function*`; uses `yield` and `await` (Spec p.372–373); states and queue in section 8.
- **EnumerateObjectProperties** — keys visited by `for-in`: enumerable strings, own and inherited, without repetition (Spec p.343); For-In Iterator is an illustrative internal object (Spec p.344–345).
- **`for-in` with initializer** — removed in ES2015 and allowed again only in non-strict code in ES2017, according to Annex F (Spec p.868) **[VERSION-DEPENDENT]**.
- **Generator** — pausable `function*` function that returns an iterator and uses `yield` (EJpt p.250–251). States: SUSPENDED-START, SUSPENDED-YIELD, EXECUTING, COMPLETED (Spec p.369, p.786).
- **%GeneratorFunction% / %GeneratorPrototype%** — intrinsic constructor with no global name and prototype with `next`, `return`, `throw` (Spec p.781, p.785).
- **Iterable / Iterator / IteratorResult** — interfaces `[Symbol.iterator]`, `next`, `{done, value}` (Spec p.749–752; EJpt p.143).
- **Iterator Helper** — lazy iterator of `map`, `filter`, `take`, `drop`, `flatMap`, `concat` (Spec p.753–760). `Iterator.from` converts an iterable/iterator-like (Spec p.754).
- **Iterator Record** — record `[[Iterator]]`, `[[NextMethod]]`, `[[Done]]` (Spec p.113).
- **IteratorClose** — calls the iterator's `return` on early exit; the original throw takes priority (Spec p.116, p.320, p.343, p.756–760).
- **`yield`** — pauses the generator and hands a value to the iterator (EJpt p.251). **`yield*`** delegates to another iterable passing on `next`, `throw` and `return` (Spec p.371–372).

## 8. Asynchrony: Promise, Job, async/await, event loop

- **Asynchronous vs synchronous** — synchronous does one thing at a time and blocks; asynchronous starts the action, moves on and is notified later (EJpt p.237).
- **AsyncFunction / `async` function** — always returns a Promise; failures in the parameters become rejections (Spec p.389); it is not a constructor and has no `prototype` (Spec p.797). In the book, it returns a promise implicitly and allows `await` (EJpt p.249–250).
- **AsyncGeneratorRequest / DRAINING-QUEUE** — queued request (completion + capability) and extra state of the async generator while it empties the queue (Spec p.791–792).
- **Await** — suspends the async function until the value's promise settles (Spec p.798); rejection becomes an exception (EJpt p.250).
- **Event loop** — the environment runs one program/callback at a time from a queue **[HOST]** (EJpt p.257). The Spec only describes Jobs and hooks (Spec p.186–187).
- **HostPromiseRejectionTracker** — host hook that tracks unhandled rejections (Spec p.768).
- **Job** — closure scheduled by the host that runs to completion, without preemption, with the context stack empty (Spec p.186–187). Promise reactions run as Jobs, never synchronously (Spec p.768–769). Equivalent to what practice calls a microtask [inference] (Spec p.186).
- **JobCallback Record** — function + host value to propagate context in Jobs (Spec p.187–188).
- **Pending / fulfilled / rejected / settled / resolved** — mutually exclusive states of a promise; settled = not pending; resolved = settled or locked in to another promise (Spec p.764).
- **Promise** — object that represents a value that may not yet be available (EJpt p.240; Spec p.764). **`then`** registers a handler and returns a new promise (EJpt p.240–241); **`catch`** handles rejection (EJpt p.244).
- **Promise.all / allSettled / any / race** — combinators with different criteria (Spec p.771–776; `all` in EJpt p.254–255). **Promise.withResolvers** returns `{promise, resolve, reject}`; **Promise.try** converts a synchronous exception into a rejection (Spec p.777).
- **PromiseCapability Record / PromiseReaction Record** — records of promise+resolve/reject and of how to react (Spec p.765–766).
- **Thenable** — object with a callable `then` method; resolved by a dedicated Job, which costs extra Jobs [inference] (Spec p.766, p.769).
- **Thread** — flow of control that the OS can interleave (EJpt p.237). **Web worker** [HOST]: script on its own timeline, communicates through `postMessage` (EJpt p.334–335).
- **Promise `@@species`** — lets subclasses control derived promises (Spec p.778).

## 9. Modules

- **`"*default*"`** — synthetic name for anonymous `export default` values (Spec p.425, p.442).
- **AMBIGUOUS** — result of ResolveExport when two `export *` offer the same name with different bindings (Spec p.428).
- **Bundler / minifier** — combine modules into one file and reduce size (EJpt p.229).
- **CommonJS (`require`/`exports`)** — Node's module system (EJpt p.226); in the old book, `require`/`loadedFiles` is a home-made manager (EJ1 p.169) [DATED].
- **Cyclic / Source Text / Synthetic Module Record** — Module Record that admits cycles; created from source code; defined by the spec with fixed exports, e.g. JSON module (Spec p.407, p.422, p.430). Module Record is abstract (Spec p.405).
- **Dynamic import (`import()`)** — expression that returns a Promise with the namespace; failures reject (Spec p.299–300).
- **Export default** — single export imported without braces (EJpt p.222).
- **HostLoadImportedModule** — host operation that locates and loads the module (Spec p.432).
- **Import attributes (`with`)** — string key/value pairs that accompany an import; the host defines the accepted keys (Spec p.434, p.436). **ModuleRequest Record** = specifier + attributes (Spec p.403).
- **ImportEntry / ExportEntry** — records of declarative import/export (Spec p.423–424).
- **`import.meta`** — per-module object, `null` prototype, content defined by the host (Spec p.301), created only when the code accesses it (Spec p.423).
- **ES module** — module with its own scope and `import`/`export` (EJpt p.221). In Node, `.mjs` contrasts with CommonJS (EJpt p.461) [HOST].
- **Module Environment Record** — module scope with indirect import bindings (Spec p.178–179).
- **Module Namespace Object** — exotic object with the unambiguous exports; null prototype, non-extensible, `[[Set]]` always false, tag `"Module"` (Spec p.230–233, p.434, p.802).
- **Module (old book)** — part of the program with a defined interface; IIFE pattern and `provide` (EJ1 p.167, p.172) [DATED]; **eval** as a loader (EJ1 p.168) [DATED].
- **Package / NPM** — distributable code and repository/installation tool (EJpt p.223–224) [HOST].
- **ResolveExport** — finds the binding that defines an exported name: binding, null or AMBIGUOUS (Spec p.427).
- **Script Record / ScriptEvaluation / GlobalDeclarationInstantiation** — script record, evaluation and creation of the global bindings with conflict checks (Spec p.399–400).
- **Module status and lifecycle** — LoadRequestedModules, Link, Evaluate; states from NEW to EVALUATED (Spec p.406–408). Fields `[[HasTLA]]` (top-level await), `[[AsyncEvaluationOrder]]`, `[[CycleRoot]]`, `[[EvaluationError]]` (Spec p.408, p.413, p.426).
- **Circular dependency** — A depends on B and B on A; many systems forbid it (EJpt p.234, truncated text).

## 10. Text, Unicode, regular expressions, dates and JSON

- **Expanded year** — year with a sign and 6 digits; "-000000" is invalid (Spec p.520).
- **Backreference** — `\N` or `\k<name>`; matches the text of the earlier capture, and always matches if the capture is `undefined` (Spec p.584–586).
- **Backtracking** — the engine goes back when a branch fails (EJpt p.201–202).
- **BMP pattern / Unicode pattern** — pattern without `u`/`v` (code units) vs with `u`/`v` (code points) (Spec p.571).
- **Canonicalize / simple case folding** — case normalization for `i` matching; simple fold with `u`/`v` (Spec p.586–587).
- **Code unit vs code point** — String indexes 16-bit UTF-16 units (EJpt p.118; Spec p.538); `codePointAt`/`fromCodePoint` deal with code points (EJpt p.119; Spec p.541).
- **Canonical equivalence / normalization (NFC, NFD, NFKC, NFKD)** — required of `localeCompare`; `normalize` accepts the four forms, others give RangeError (Spec p.544–546).
- **Epoch / time value** — 1970-01-01T00:00Z; finite integer Number in ms (±8.64e15) or NaN (Spec p.509). EJ1 and EJpt: ms since 1970 (EJ1 p.56–57; EJpt p.197).
- **Flags** — `g`, `i`, `y`, `u` (EJpt p.214); `d` (hasIndices, Spec p.610–611); `s` (dotAll, Spec p.583); `v` (unicodeSets, incompatible with `u`, Spec p.598–599); `y` matches only at `lastIndex` (Spec p.610).
- **ECMAScript date format** — `YYYY-MM-DDTHH:mm:ss.sssZ`, simplification of ISO 8601 (Spec p.519). `Date.parse` accepts implementation heuristics outside it (Spec p.523).
- **Capture group / `(?:...)` / named group** — parentheses that capture; `?:` groups without capturing (EJpt p.196); `(?<name>...)` becomes a property of `groups` (Spec p.559, p.610).
- **Hashbang** — see section 14.
- **Lookahead / lookbehind** — zero-width assertions (Spec p.558, p.579–581; look-ahead in EJpt p.199).
- **`lastIndex`** — index of the next match with `g`/`y` (Spec p.613; EJpt p.208).
- **Inline modifiers** — `(?i:...)` / `(?-i:...)` turn `i`, `m`, `s` on/off for a stretch (Spec p.559, p.587).
- **Normalization** — see **Canonical equivalence**; no other operation normalizes strings implicitly (Spec p.50).
- **Surrogate pair** — two elements (high 0xD800–0xDBFF + low 0xDC00–0xDFFF) form a code point above 0xFFFF; lone surrogates are valid strings (Spec p.50). `toWellFormed` replaces lone ones with U+FFFD (Spec p.555).
- **`\p{...}` / property of strings** — class by Unicode property only with `u` or `v` (Spec p.561); properties of strings (e.g. `RGI_Emoji`) only in `v` (Spec p.565, p.596). `MayContainStrings` governs errors in `\P` and `[^...]` (Spec p.565, p.568).
- **Greedy / lazy quantifier** — repeats the maximum/minimum; a following `?` makes it lazy (Spec p.575, p.582; EJpt p.205–206).
- **RegExp** — pattern object (EJpt p.189). Set `[...]` with negating `^` (EJpt p.190, p.192). `RegExpExec` calls an overridable `exec` (Spec p.609); `AdvanceStringIndex` advances a code unit or code point (Spec p.611); RegExp String Iterator comes from `matchAll` (Spec p.613–614).
- **RepeatMatcher** — internal repetition; resets captures and rejects an empty iteration after the minimum (Spec p.575).
- **ParseJSON / reviver / replacer / toJSON** — validates JSON text (ECMA-404) and throws `SyntaxError` if invalid (Spec p.735); reviver receives `(key, value, context)` and `undefined` deletes (Spec p.735, p.737); `context.source` gives the original text (Spec p.735, p.737); `toJSON` consulted by `stringify` (Spec p.742); `space` limited to 10 (Spec p.739–740); `JSON.rawJSON` inserts raw text (Spec p.734, p.739, p.742). JSON in the old book was read with `eval` and parentheses (EJ1 p.234) [DATED].
- **Serialization** — converting data into a flat description; JSON is the textual format (EJpt p.99).
- **StringIndexOf / empty** — the empty string is "found" at every position, including after the last unit (Spec p.51).
- **SystemTimeZoneIdentifier / primary time zone** — environment time zone, implementation-defined (Spec p.515); primary identifier (IANA Zone) vs non-primary (Link) (Spec p.513) [HOST].
- **Timestamp** — milliseconds since 1970 UTC; `getTime()`/`Date.now()` (EJpt p.197).
- **TimeClip / MakeDay / MakeTime / MakeDate / MakeFullYear** — TimeClip nulls values outside ±8.64e15 (Spec p.518); MakeFullYear converts 0–99 into 1900+year (Spec p.518); LocalTime/UTC use the system time zone (Spec p.516–517). In ES2015 TimeClip never returns `-0`, according to Annex E (Spec p.865).
- **TV / TRV** — cooked value and raw value of a template component (Spec p.267–268); see section 14.

## 11. Collections and binary data

- **AddEntriesFromIterable** — feeds Map/WeakMap from an iterable of pairs; requires object items (Spec p.676).
- **Resizable / detached ArrayBuffer** — created with `maxByteLength`, changes via `resize` (Spec p.698, p.706–707); a detached one has `null` data and size 0 (Spec p.699–700, p.708); `transfer` moves content and detaches the original (Spec p.707–708). `[[ArrayBufferDetachKey]]` is only defined by the host [HOST] (Spec p.708).
- **ArraySpeciesCreate / `@@species`** — creates the derived array via `constructor[Symbol.species]` (Spec p.218–220); static getter that returns `this` (Spec p.677, p.684, p.705).
- **Atomics** — atomic and wait operations on shared memory (Spec p.723); `wait` returns `"ok"`, `"timed-out"` or `"not-equal"` (Spec p.727–728, p.733); `waitAsync` returns `{async, value}` (Spec p.728, p.733); `notify` returns the number woken, 0 if not shared (Spec p.733–734); `isLockFree` (Spec p.732).
- **BYTES_PER_ELEMENT** — element size of the TypedArray, not writable (Spec p.669).
- **CanBeHeldWeakly** — defines which values serve as a weak key/target: objects and Symbols outside the `Symbol.for` registry (Spec p.196, p.693–696).
- **CanonicalizeKeyedCollectionKey** — converts `-0` into `+0` before storing/looking up a key (Spec p.697).
- **Consistent comparator / stable sort** — for `sort` to have a defined order: deterministic, without mutation, reflexive, symmetric and transitive (Spec p.638); equal items keep their order (Spec p.638).
- **Content type (NUMBER/BIGINT)** — category of TypedArray values; mixing throws `TypeError` (Spec p.659, p.664, p.667).
- **DataView** — view over an ArrayBuffer with get/set per type and explicit endianness (Spec p.717–722). Default `littleEndian` is false (big-endian) (Spec p.719–722).
- **EMPTY (removed entry)** — internal marker that preserves indices for in-progress iterators (Spec p.678).
- **Out of bounds / AUTO** — view whose buffer was detached/shrunk; operations throw `TypeError` and sizes give 0 (Spec p.649, p.656, p.665, p.716–717); AUTO length tracks a resizable buffer (Spec p.667, p.716, p.718).
- **FlattenIntoArray / FindViaPredicate / IsConcatSpreadable** — routines behind `flat`/`flatMap`, `find*` and `concat` (Spec p.620, p.625–627).
- **getOrInsert / getOrInsertComputed** — existing value or direct/computed insertion (Spec p.679–680, p.694).
- **Map / Set** — collections by insertion in `[[MapData]]`/`[[SetData]]`, keys by SameValueZero (Spec p.675–676, p.682–683). `Map.groupBy` groups (Spec p.677); iterators see items added during traversal (Spec p.681, p.691). `Object.groupBy` returns an object without a prototype (Spec p.464).
- **Generic method** — `Array.prototype` method that uses `ToObject(this)` and accepts any array-like (Spec p.620).
- **Set Record / set methods** — summary of `size`/`has`/`keys` of a set-like for `union`, `intersection`, `difference`, `symmetricDifference`, `isSubsetOf`, `isSupersetOf`, `isDisjointFrom` (Spec p.682–690).
- **Growable SharedArrayBuffer** — only grows via `grow` up to `maxByteLength` (Spec p.709, p.712–713); host hooks `HostResizeArrayBuffer`/`HostGrowSharedArrayBuffer` [HOST] (Spec p.700, p.710).
- **Tearing** — mixing of bits in concurrent accesses; tear-free is required (Spec p.715, p.809).
- **TypedArray / %TypedArray%** — typed view over a buffer with one constructor per type; abstract non-global superclass (Spec p.646–647, p.669). Slots `[[ViewedArrayBuffer]]`, `[[ByteOffset]]`, `[[ArrayLength]]` (Spec p.669). `subarray` shares the buffer, `slice` copies (Spec p.661). `ValidateTypedArray` (Spec p.665); `TypedArraySpeciesCreate` vs `TypedArrayCreateSameType` (Spec p.664). `Uint8ClampedArray` uses clamp conversion (Spec p.646). Base64/hex: `fromBase64`, `setFromBase64`, `toBase64` with `alphabet`, `lastChunkHandling` (`loose`, `strict`, `stop-before-partial`), `omitPadding` (Spec p.670–671, p.674).
- **WeakMap / WeakSet** — weak collections of object/symbol keys, without enumeration or `size` (Spec p.692, p.695).

## 12. Memory, garbage collection, WeakRef and concurrency

- **Agent / Agent Record / agent cluster / signifier** — spec mechanism: execution contexts, stack and thread; cluster = agents that can share memory (Spec p.189–192). `[[CanBlock]]` says whether the agent can block (Spec p.190).
- **AddToKeptObjects / `[[KeptAlive]]` / ClearKeptObjects** — hold WeakRef targets strongly until the end of the synchronous work (Spec p.190, p.195–196, p.746–747).
- **Candidate execution / happens-before / synchronizes-with** — axiomatic model of shared-memory events (Spec p.808).
- **Garbage collection** — the Spec does not guarantee that any object is collected; it uses "may" (Spec p.193). Weak entries may vanish with arbitrary latency (Spec p.692). EJpt describes unused values dissipating without using the term [inference] (EJpt p.14–15).
- **Data race / data race free** — pair of events in a race; without races the program looks sequentially consistent (Spec p.802, p.810–811).
- **FinalizationRegistry / unregister token** — cleanup callbacks after targets are collected; a weak token cancels registrations (Spec p.747–749).
- **Liveness / WeakRef-oblivious execution** — "alive" criterion based on a hypothetical execution in which the WeakRefs of a set return `undefined` (Spec p.193–194).
- **Memory model / SEQ-CST / UNORDERED** — ordering levels of memory events (Spec p.802–803). `[[NoTear]]` is true for integer TypedArray and false for float TypedArray and DataView (Spec p.809).
- **Memory leak (IE)** — DOM–JS object cycle that IE's collector does not free (EJ1 p.227–228) [DATED] [HOST].
- **WeakRef** — weak reference to an object/symbol; `deref()` returns the target or `undefined` (Spec p.745–746).

## 13. Errors and exceptions

- **AggregateError** — aggregates several errors in `errors`; the first parameter is the iterable (Spec p.486); thrown by `Promise.any` (Spec p.774–775).
- **Assertion** — internal check that throws an error to catch programmer bugs (EJpt p.183).
- **Bug / debugging** — failure in a program; divided into errors of thought and of translation (EJpt p.167–168). **Breakpoint / `debugger`** pauses execution (EJpt p.174).
- **cause** — option that installs a non-enumerable `cause` property (Spec p.487).
- **Selective catching** — checking `instanceof` in the `catch` and rethrowing the unexpected (EJpt p.182–183).
- **`[[ErrorData]]`** — slot that identifies error instances (Spec p.483, p.486).
- **Error (object)** — object with `message`, via `new Error(...)` (EJ1 p.73) [DATED]; `stack` records the active calls (EJpt p.178).
- **Exception / `throw`** — interrupts the flow and unwinds the stack up to a `catch`; can be any value (EJpt p.176; EJ1 p.70–71 [DATED]).
- **Stack unwinding** — discarding call contexts until a `catch` is found (EJpt p.176; EJ1 p.70–71).
- **Abrupt `finally`** — an abrupt completion in `finally` replaces the result of `try`/`catch` (Spec p.354). **Optional `catch` parameter** (Spec p.353).
- **RangeError / ReferenceError / SyntaxError / TypeError / URIError** — standard errors; e.g.: ReferenceError for an unresolvable name (Spec p.81), URIError for invalid URI encoding (Spec p.456–457, p.484).
- **Automated test / test runner** — program that checks another (EJpt p.172).
- **`try/catch/finally`** — try, handle and clean up (EJpt p.177, p.179; EJ1 p.71–72).

## 14. Syntax and grammar

- **ASI (Automatic Semicolon Insertion)** — automatic insertion of `;` by three rules: offending token, end of input, restricted productions (Spec p.269). **Restricted production (`[no LineTerminator here]`)**: a line break triggers ASI, e.g.: `return`, `++`, `async` (Spec p.269–270, p.273).
- **Cover grammar** — ambiguous grammar refined later: parentheses vs arrow; object vs pattern (Spec p.276, p.281, p.289, p.291).
- **Directive / Use Strict Directive** — initial statements consisting only of string literals; exact `"use strict"`, without escapes (Spec p.246–247).
- **Early error** — syntax/static-semantic error detected before evaluation, prevents execution (Spec p.47, p.445). **Runtime error** is any other (Spec p.445).
- **Elision** — comma without an expression in an array literal/pattern; creates a hole or skips an element (Spec p.278, p.322).
- **Goal symbol** — initial nonterminal: `Script`, `Module`, `Pattern`; lexical: Div, RegExp, TemplateTail (Spec p.35–36, p.248–249).
- **Hashbang (`#!`)** — comment at the start of a script/module (Spec p.252).
- **Contextual keyword / ReservedWord** — contextual ones (`async`, `of`, `get`, `set`) are identifiers in some places; reserved ones are not (Spec p.255). Books list words reserved for future versions (EJ1 p.21; EJpt p.32).
- **LineContinuation / LineTerminator** — `\` + line break in a string/template contributes empty (Spec p.261–262); LF, CR, LS, PS (Spec p.250).
- **NotEscapeSequence** — malformed escape accepted only in tagged templates; cooked = `undefined` (Spec p.267, p.285).
- **NumericLiteralSeparator** — `_` between digits (Spec p.256). **Legacy octal literal** (`017`): error in strict mode **[DATED]** (Spec p.257–259).
- **Optional chain / tagged template / direct eval** — see sections 2 and 15; a tagged template calls a function with a template object + values (Spec p.300).
- **ParseText / SourceCharacter** — analysis of text against a goal symbol, returning a node or `SyntaxError`s; SourceCharacter is any code point (Spec p.243, p.245).
- **Labels** — static validations of duplicates and nonexistent `break`/`continue` targets (Spec p.139–144); target and current label set (Spec p.346, p.351). `BreakableStatement` = loops and `switch` (Spec p.352).
- **Switch / fall-through** — after a `case` matches, it continues through the following ones until an abrupt completion; uses `IsStrictlyEqual` (Spec p.349–350; EJ1 p.239–241).
- **Template object** — frozen array of cooked strings with `raw`, unique per code location and Realm (Spec p.286–287). Per-location canonicalization since ES2018 according to Annex F (Spec p.867) **[VERSION-DEPENDENT]**.
- **JSX** — non-standard dialect that allows HTML-like syntax in expressions; requires preprocessing (EJpt p.500) [HOST].

## 15. Strict mode and legacy

- **Annex B (normative optional)** — legacy features required in browsers, optional in other hosts [DATED] (Spec p.843). HTML-like comments `<!--`/`-->` only in scripts (Spec p.843–844); `escape`/`unescape` (Spec p.850–851); `substr` (Spec p.851); `CreateHTML` (Spec p.851–852); `trimLeft`/`trimRight` (Spec p.853–854); `getYear`/`setYear`/`toGMTString` (Spec p.854); `RegExp.prototype.compile` (Spec p.855). In modules and strict code, no Annex B extensions (Spec p.446).
- **Block-level function web legacy semantics** — in non-strict mode, creates a global var binding for functions declared in blocks of scripts (Spec p.400, p.855–856) [DATED] [HOST].
- **Strict mode code** — module, class, or code with a directive or inherited (Spec p.247). Strict variant chosen per source code unit (Spec p.30). In EJpt: `"use strict"` opt-in that turns silences into errors (EJpt p.168–170). Restrictions: no `with`, no legacy octal, uncoerced `this`, assignment to an undeclared name throws `ReferenceError` (Spec p.861).
- **Direct vs indirect eval** — direct inherits the caller's scope (Spec p.294, p.449); indirect runs in the global scope (Spec p.449). `eval` in the old book: variables stay local to the function (EJ1 p.168) [DATED]. `HostEnsureCanCompileStrings` can block `eval`/`Function` [HOST] (Spec p.450).
- **Forbidden extension** — change that hosts may not make, e.g.: own `caller`/`arguments` on strict functions (Spec p.445–446).
- **Legacy** — behavior kept for compatibility, not for new code (Spec p.25).
- **Normative Optional** — optional subclause, but if implemented it must be whole (Spec p.25).
- **`with`** — inserts an object in the scope chain; forbidden in strict mode **[DATED]** (Spec p.347; EJ1 p.239–241). Uses Object Environment Record.
- **%ThrowTypeError%** — per-realm built-in that always throws `TypeError`, used in restricted `caller`/`arguments`/`callee` (Spec p.209).

## 16. Spec jargon

- **Abrupt completion** — any completion that is not NORMAL (Spec p.79).
- **Abstract operation** — named, reusable algorithm of the spec, invisible to the program (Spec p.44). **Syntax-directed operation**: definition varies by production (Spec p.44, p.118). **Contains**: checks symbols in the subtree without entering functions (Spec p.150–152).
- **AssignmentTargetType** — classifies a target as SIMPLE, WEB-COMPAT or INVALID (Spec p.158–159).
- **Completion Record** — record `[[Type]]`/`[[Value]]`/`[[Target]]` of the normal or abrupt result (throw/return/break/continue) (Spec p.45–46, p.78, p.346). **`?` / `!`**: propagates abrupt / asserts normal (Spec p.45–46).
- **Conforming implementation** — implementation that complies with the spec and does not adopt forbidden extensions (Spec p.25).
- **Data Block / Shared Data Block** — sequence of bytes (shared in the second) (Spec p.85).
- **Declarative / Object / Function / Global / Module Environment Record** — scope records: direct bindings (Spec p.166); object properties, used by `with` and by the global part (Spec p.169); function invocation (Spec p.171–172); global = object part (var/function) + declarative (let/const/class) (Spec p.173–175); module (Spec p.178–179). **Global lexical vs var declaration** and **HasRestrictedGlobalProperty** (Spec p.173–176).
- **Enum / List / Record** — internal meta-values of the spec (`« »` for List) (Spec p.77). **Specification type**: not storable in JS variables (Spec p.77).
- **Environment Record** — associates identifiers with values in a scope; `[[OuterEnv]]` forms the chain (Spec p.162).
- **Execution context** — tracks the evaluation of code; the top of the stack is the one running (Spec p.184).
- **Host environment / host-defined / host hook** — definition deferred to the environment, listed in Annex D (Spec p.27–28, p.863); a host hook must return a normal completion or throw (Spec p.27) [HOST]. **Implementation-defined / approximated** (Spec p.27).
- **Intrinsics (well-known intrinsic, `%name%`)** — built-ins of a realm, one copy per realm (Spec p.74, p.183).
- **Invariants (of internal methods)** — guarantees upheld by objects and checked in Proxy; violation gives `TypeError` (Spec p.71, p.235).
- **Essential internal method** — `[[Get]]`, `[[Set]]`, `[[DefineOwnProperty]]`, `[[OwnPropertyKeys]]` etc.; ordinary ones delegate to `Ordinary*` (Spec p.197). **Ordinary / exotic object** (Spec p.31, p.69).
- **Exotic objects** — Array (keeps `length` ≥ largest index + 1, deletes when reduced; `length` < 2^32, Spec p.217–219); String (virtual indices and `length`, Spec p.219–221); mapped Arguments (Spec p.221–224); TypedArray (canonical numeric keys as indices, Spec p.225–227); Module namespace (Spec p.230–233); Immutable prototype (Spec p.233–234); Bound function (Spec p.216–217); Proxy (Spec p.234).
- **PrivateElement / Private Name** — record and key of private members (Spec p.86–87).
- **Property Descriptor / Fully populated descriptor** — Record of attributes; complete = data or accessor with all the fields (Spec p.82).
- **Proxy / trap / revoked** — object whose internal methods delegate to handler traps; if absent, uses the target (Spec p.234–235); slots `[[ProxyTarget]]`/`[[ProxyHandler]]` become `null` on revocation and then any operation throws `TypeError` (Spec p.234–235, p.243); `ProxyCreate` requires objects (Spec p.243); `Proxy.revocable` (Spec p.801–802). **Reflect** mirrors internal operations (Spec p.799).
- **Realm** — intrinsics + global environment + associated code (Spec p.182); the global object is neither callable nor constructible (Spec p.447–448); **globalThis** references the realm's global `this` (Spec p.448).
- **Reference Record** — resolution of a name/property binding: `[[Base]]`, `[[ReferencedName]]`, `[[Strict]]`, `[[ThisValue]]` (Spec p.79–80, p.289, p.293). **Super Reference** has `[[ThisValue]]` (Spec p.80). **GetValue / PutValue**: throw `ReferenceError` for an unresolvable name (reading always; writing in strict mode) and must be called even if the result is discarded, because of getter/Proxy effects (Spec p.81, p.305, p.324).
- **RequireObjectCoercible / RequireInternalSlot** — checks that throw `TypeError` for `null`/`undefined` when destructuring an object or for an object without a slot (Spec p.319–320, p.716–717).
- **Well-known symbol** — built-in Symbol that serves as an extension point (`%Symbol.iterator%`, `hasInstance`, `species`, `toPrimitive`, `toStringTag`, `unscopables` etc.), shared across realms (Spec p.52–53). Global symbol registry of `Symbol.for`/`keyFor` (Spec p.478–479).

## 17. Environment [HOST]: browser, DOM, Node, timers

Everything in this section is defined by the environment, not by the Spec, except where indicated.

- **Access-Control-Allow-Origin** — header that allows cross-domain requests (EJpt p.409).
- **bubbling (propagation)** — event rises from the target to the ancestors (EJ1 p.208 [DATED]; EJpt p.321–322; the EJpt book does not use the term "bubbling"). `stopPropagation` and `preventDefault` (EJ1 p.214; EJpt p.322–323). `target` (EJpt p.322); `srcElement`/`attachEvent` are IE's (EJ1 p.209, p.211) [DATED].
- **Canvas / 2D context** — drawing element and the `getContext("2d")` object (EJpt p.373–374); path with `beginPath`, `moveTo`, `lineTo`, `stroke`, `fill` (EJpt p.376–377); `drawImage`/sprite (EJpt p.382–383, p.392, p.396); `save`/`restore` (EJpt p.387–388); `getImageData` (EJpt p.447–448).
- **Debouncing** — postponing the action with `setTimeout`/`clearTimeout` until a pause in the events (EJpt p.336).
- **Event delegation** — using `target` to handle events from descendants (EJpt p.322).
- **DOM** — tree of document objects (EJpt p.295; EJ1 p.196 [DATED]). `nodeType`: 1 element, 3 text, 8 comment (EJpt p.296; EJ1 p.197 uses 9 for document). `childNodes`, `parentNode`, `firstChild` etc. (EJ1 p.196–197). Live collection (`getElementsByTagName`, `childNodes`) vs stable (`querySelectorAll`, `Array.from`) (EJpt p.302, p.310). `innerHTML` (EJ1 p.198).
- **encodeURIComponent / decodeURIComponent** — `%XX` encoding (EJpt p.405, p.485; Spec p.455 for `encodeURI`/`encodeURIComponent`). Spec: the first preserves URI delimiters, the second does not (Spec p.455).
- **Event handler / `addEventListener`** — function registered for an event type (EJpt p.319–320; EJ1 p.208–209 [DATED]). Keyboard events `keydown`/`keyup`, `key` (EJpt p.324–325); `keyCode`/`charCode` (EJ1 p.213–214) [DATED]; mouse `clientX/Y` vs `pageX/Y` (EJpt p.326–327); `button` vs `buttons` (EJpt p.321, p.328–329); `touches` (EJpt p.329–330); `focus`/`blur` do not propagate (EJpt p.332); `load`/`beforeunload` (EJpt p.333).
- **ETag / If-None-Match / long polling / WebSockets** — conditional caching (EJpt p.486); request pending until there is news (EJpt p.484); connections for arbitrary exchange (EJpt p.484).
- **fetch** — browser API that returns a promise of `Response`; resolves even with an error status, rejects only on network failure (EJpt p.406–407).
- **FileReader / localStorage / sessionStorage** — asynchronous file reading; per-domain string storage (EJpt p.422–425).
- **HTTP / TCP / URL / HTTPS** — protocol, methods GET/POST/PUT/DELETE, codes 2xx/4xx/5xx, headers (EJpt p.283–285, p.402–403, p.410). Codes used in the project: 204, 304, 400, 403, 404, 405 (EJpt p.472–475, p.493–494). **Idempotence**: repeating has the same effect (EJpt p.476).
- **HTML / tag / attribute / entity** — markup language (EJpt p.286–287). **CSS / specificity / selector** (EJpt p.308–309). **position** `static/relative/absolute/fixed` (EJpt p.311, p.331; EJ1 p.206).
- **Node.js** — `node:fs` (EJpt p.465); `node:fs/promises` (EJpt p.467); `Sync` variants block (EJpt p.467); `Buffer` (EJpt p.465–466); `node:http`/`createServer` (EJpt p.467–468); streams and `pipe` (EJpt p.469–472, p.476); `process.argv` with real arguments from index 2 (EJpt p.460–461); `package.json`, `node_modules` (EJpt p.462–464); semantic versioning and `^` (EJpt p.464–465); `npm publish` (EJpt p.465); `ENOENT` (EJpt p.475); directory traversal (EJpt p.473); `serve-static`, router (EJpt p.488–489).
- **requestAnimationFrame / cancelAnimationFrame** — schedules a function for the next repaint, receiving the time (EJpt p.312, p.335).
- **Sandbox** — isolation of browser JS (EJpt p.290).
- **setTimeout** — calls a function after N ms (EJpt p.239). In the old book, `setInterval`/`setTimeout` also accept a code string (EJ1 p.145) [DATED].
- **`window`** — browser global object, property of itself (EJ1 p.170) [DATED].
- **XMLHttpRequest** — HTTP request without reloading; `readyState` 0–4 and `onreadystatechange` (EJ1 p.231, p.233) [DATED].

## 18. Divergences and observations between sources

In conflicts, the Spec is the norm, EJpt is the modern explanation and EJ1 is dated.

**Conceptual divergences**

| Subject | EJ1 (dated) | EJpt | Spec | Prevails |
|---|---|---|---|---|
| Block scope | A block does not create scope (EJ1 p.19, p.34) | `let`/`const` are block-scoped (EJpt p.52–54) | A block creates a lexical environment (Spec p.326) | Spec/EJpt |
| Variable declaration | Only `var` (EJ1 p.15) | Binding, `let`/`const` (EJpt p.30–32) | `var` in VariableEnvironment; `let`/`const`/`class` lexical (Spec p.185, p.328) | Spec |
| Types listed | Six types, `null` only on p.26 (EJ1 p.9, p.26) | `number`, string, etc. (EJpt p.14–19) | Eight language types: Undefined, Null, Boolean, String, Symbol, Number, BigInt, Object (Spec p.50) | Spec |
| Number bits | 64 bits, 52 of mantissa; a note corrects to 53 (EJ1 p.9–10, p.29) | 64 bits (EJpt p.15) | binary64 (Spec p.47) | Spec |
| `typeof` of a native function in IE | `"object"` and without `apply` (EJ1 p.80) | not applicable | functions are callable objects (Spec p.34) | Spec; the IE case is [DATED] |
| Hoisting | Described without a name, only functions (EJ1 p.39) | Described without a name (EJpt p.55) | `var` and functions hoisted (Spec p.128–135, p.154) | Spec |
| Identifying an array | `instanceof Array` fails across windows (EJ1 p.235) | not covered | `IsArray` is used by the Spec, e.g. in `concat` (Spec p.620) | Spec |
| Quantifier `{,4}` | The book says four or fewer (EJ1 p.179) | not covered | Notes only record `{n}`, `{n,}`, `{n,m}` (Spec p.845–846) | Spec; treat `{,4}` as [DATED]/doubtful |
| `matchAll` | does not exist | text says "array of arrays", example uses `for...of` (EJpt p.210) | `matchAll` returns a RegExp String Iterator (Spec p.613–614) | Spec |
| EJpt edition | n/a | declares "versão 2024" ("version 2024") (EJpt p.9) | n/a | Exact edition is [inference]; analyses diverge between the 3rd and 4th edition |

**Observations about the Spec**
- Not every edition date is given: only Annexes E and F and occasional notes (for example, TimeClip in ES2015 in Spec p.865; for-in with initializer in Spec p.868; RegExp constructor in Spec p.869). For the rest, "version not stated in the sources".
- The module table (Spec p.408) describes `[[EvaluationError]]` as throw or EMPTY, but the meaning column says "undefined"; the algorithm uses EMPTY (Spec p.408, p.413). `ScriptIsStrict` with `Script : [empty]` returns `undefined` in an algorithm that returns Boolean, probably a slip (Spec p.398).
- Annex F, about `Object.isExtensible`, says to treat a non-object "as if it were" an ordinary non-extensible object, without stating the return value (Spec p.868).

**Truncated passages or errors in the sources (do not reproduce)**
- EJ1 p.17 and EJpt p.35–37: the example prints the square but the label says "raiz quadrada" ("square root"). Do not copy the label.
- EJ1 p.52: the real list separator is comma + space; EJ1 p.203 has a truncated "starting with ts"; EJ1 p.58 mixes slashes and hyphens in dates.
- EJpt p.210: `matchAll` described as an array; EJpt p.474: the text speaks of "mime" but the package is `mime-types`; EJpt p.398: cut-off comment ("loo"); EJpt p.234 and p.387: truncated texts; EJpt p.331, p.333, p.344, p.345, p.367, p.372, p.379: typos ("animaçãoões" etc.).
- Spec p.607: the `Symbol.split` example is truncated; Spec p.233, p.344, p.397, p.444, p.668: page cuts; Spec p.739: "the the"; Spec p.808: "execution execution". Spec p.813–842 (Annex A, grammar summary) were not distilled.

## Gaps

- Terms from Intl, Temporal and time-zone `Date` beyond what Spec p.513–517 describes are not in the sources read.
- The Spec does not date features; only EJpt dates `class` and Symbol as 2015 (EJpt p.132, p.141–142). For `?.`, `#private`, class fields, rest/spread and destructuring, the book gives no version (version not stated in the sources).
- Absent or only implicit concepts: the term "microtask" does not appear in any of the three sources (the Spec says Job); "hoisting" only appears in the Spec in notes about `var`/`let` conflicts and about reads in the memory model (Spec p.450, p.812), not as the name of the mechanism, and EJpt only says that function declarations are conceptually moved to the top of the scope (EJpt p.55); "bubble" only appears in EJ1, in English (EJ1 p.208–213), and EJpt describes event propagation without that name; TDZ is a term from practice, used by this package, and does not appear in any of the three sources **[extrapolation]**.
- The games, Egg and Skill Share chapters of EJpt only enter here through their general terms (see section 17).
