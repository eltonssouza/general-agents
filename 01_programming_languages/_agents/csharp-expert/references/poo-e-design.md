# OOP and design in C# (CSYB, ch. 4)

Convention: `(CSYB p.N)` = PDF page (printed = N − 5). Code examples are illustrative. What is not in the book is labeled and collected in section 11.

## 1. Structures (`struct`) vs classes (`class`)

- "Structures are managed by **value**, objects by **reference**" `[from source] (CSYB p.92)`. Both can have data and methods `[from source] (CSYB p.92)`.
- A `struct` groups fields into a cohesive block (record/fields) `[from source] (CSYB p.87-88)`; with `Account a;` the fields can already be assigned `[from source] (CSYB p.88-89)`.
- Assigning one struct to another **copies all the values** `[from source] (CSYB p.89)`; when passed to a method the value is passed `[from source] (CSYB p.90)`. Glossary: "copied on assignment; passed by value; less flexible than objects, but more efficient because no reference is followed" `[from source] (CSYB p.211)`; *value type* `[from source] (CSYB p.213)`.
- A local struct with unassigned fields: using the field gives a compile error `[from source] (CSYB p.89)`.
- `Account RobsAccount;` for a **class** creates only a *reference* (a label); `new` is needed to create the object `[from source] (CSYB p.93-94)`.
- Two references can point to the same object; a change through one shows up in the other `[from source] (CSYB p.94-95)`.
- An object with no references becomes the **Garbage Collector**'s job (also when the reference goes out of scope) `[from source] (CSYB p.96)`; the author asks for care not to overdo creating/discarding objects `[from source] (CSYB p.96)`.
- Why references: sorting without moving objects, several sorted lists, trees `[from source] (CSYB p.96-98)`.
- [extrapolation] struct "on the stack"/class "on the heap", immutability (`readonly struct`, CSHist p.9 only **lists** the C# 7.2 feature), "struct does not inherit" and "no null": outside the book. See §11.

## 2. Encapsulation and class design

- `private` data, `public` methods; exceptions are justified (performance, internal method) `[from source] (CSYB p.100-101)`. Convention: public names capitalized, private ones in lower case `[from source] (CSYB p.101)`.
- An access method (*accessor*) returns the value without allowing it to be changed (`GetBalance`) `[from source] (CSYB p.102, 204)`; a *mutator* changes it with validation `[from source] (CSYB p.209)`.
- Think about what should **not** be possible (e.g. changing the account number) `[from source] (CSYB p.99)`.
- The business object guarantees that its data is valid; the user interface uses its validation `[from source] (CSYB p.166-167, 172)`.
- Tests: write tests that call the methods and count errors `[from source] (CSYB p.102-103)`; TDD `[from source] (CSYB p.103)`; tests also "hang on" the interface `[from source] (CSYB p.120)`.
- Cohesion and coupling: high cohesion, low coupling `[from source] (CSYB p.205-206)`; dependency `[from source] (CSYB p.207)`.

## 3. `static` members

- `static` = member **of the class**, not of the instance; `Main` is the example; it does **not** mean "cannot change" `[from source] (CSYB p.104)`. Do not confuse it with `const` `[from source] (CSYB p.66)`.
- The book's example: a single interest rate for all accounts as `static decimal`, accessed by the class name `[from source] (CSYB p.104-105)`. The author says to keep static data private and change it through methods `[from source] (CSYB p.105)`.
- A static method does not see instance members (error CS0120) `[from source] (CSYB p.106)`; it serves for method libraries (e.g. `sin`, `cos`) `[from source] (CSYB p.107)`.

## 4. Constructors

- Every object is created by a constructor; same name as the class, no return `[from source] (CSYB p.107-108)`.
- If you write none, the compiler creates a public parameterless constructor; if you write one, the default **ceases to exist** `[from source] (CSYB p.108-109)`.
- Overloading of constructors and methods (same name, different parameters) `[from source] (CSYB p.110, 209-210)`.
- Chaining within the same type with `: this(...)`; plan: a "master" constructor `[from source] (CSYB p.111-112)`.
- A constructor cannot "fail": the only way is to throw an exception `[from source] (CSYB p.112-113)`; it can gather all the error messages before throwing `[from source] (CSYB p.113-114)`.
- In hierarchies, the parent's constructor runs first; use `: base(...)`; hierarchies are "fragile" `[from source] (CSYB p.127)`.
- `this` is also the reference to the current instance (`this.account.SetName("Rob")`, `bank.Store(this)`) `[from source] (CSYB p.135-136, 212)`.

## 5. Interfaces and components

- Interface = a set of method definitions; it describes **what** to do, not **how**; naming convention with `I` `[from source] (CSYB p.116)`.
- `class CustomerAccount : IAccount` forces implementing each member (otherwise error CS0535) `[from source] (CSYB p.117)`.
- A variable of interface type can reference any object that implements it; there is never an "instance of the interface" `[from source] (CSYB p.117-118)`. `IAccount[]` holds accounts of different types `[from source] (CSYB p.119)`.
- A class can implement several interfaces: `class BabyAccount : IAccount, IPrintToPaper` `[from source] (CSYB p.119-120)`.
- "Interfaces are just promises": the compiler does not enforce the behavior; tests do `[from source] (CSYB p.120)`. Component = a class treated by what it **does** `[from source] (CSYB p.205)`.
- Interfaces also declare properties (`int Age { get; set; }`) `[from source] (CSYB p.140-141)`.
- The book recommends referencing objects through the interface, even when using an abstract class `[from source] (CSYB p.130)`.
- [inference] "programming to the interface" makes it easier to swap implementations and to test (the book says that components are interchangeable and that tests attach to the interface, p.115, 120); "dependency inversion" and "mocks" are [extrapolation] vocabulary.

## 6. Inheritance, `virtual`, `override`, `new`, `abstract`, `sealed`

- Inheritance = code reuse (*creative laziness*); `class BabyAccount : CustomerAccount` `[from source] (CSYB p.121-122)`. Interface: "I do it because I said I would"; inheritance: "I do it because my parent does" `[from source] (CSYB p.121)`.
- `override` replaces the parent's behavior; the parent's method must be `virtual` ("if it isn't, you definitely can't override it") `[from source] (CSYB p.122-123)`.
- `protected`: visible to the class and the derived ones; the author prefers to reduce exposure (uses `base`) `[from source] (CSYB p.123-125, 210)`.
- `base.WithdrawFunds` (a `base.` call in the overridden method) calls the parent's method `[from source] (CSYB p.124-125)`; `: base(args)` in the constructor `[from source] (CSYB p.127)`.
- Without `virtual`/`override` the child's method is a **replacement** (the compiler warns and asks for `new`) `[from source] (CSYB p.125)`. The author is "very much against" replacing methods; prefer `override` `[from source] (CSYB p.126)`.
- `sealed` on a method (only a method that already overrides) or on a class (cannot be extended) `[from source] (CSYB p.126)`.
- `abstract`: a method without a body in the parent; a class with an abstract method is abstract and **cannot be instantiated**; concrete children implement it `[from source] (CSYB p.128, 204)`. An abstract class can mix ready-made and abstract methods; you only inherit from **one** parent `[from source] (CSYB p.128-130)`.
- Interface vs abstract: an interface describes behaviors; an abstract class is a model with code `[from source] (CSYB p.130)`.
- [extrapolation] In C#, when a method hidden by `new` is called through a variable of the base type, the **base** one runs; with `override`, the one of the real type. The book only shows the syntax and discourages it (p.125-126). The virtual dispatch table (*vtable*) is an implementation detail not cited.

## 7. Object etiquette (`object`)

- Every class is a child of `object`; an `object` reference accepts any class `[from source] (CSYB p.131)`.
- `ToString()` is `virtual`; the one in `object` returns the type description (`System.Object`); override it to show the content; `base.ToString()` accesses the parent's `[from source] (CSYB p.132-133)`.
- Comparing objects with `==` compares **references**; to compare content override `Equals(object obj)` (with a cast) and call `Equals` instead of `==` `[from source] (CSYB p.133-134)`. "Use the right *equals*" and "always provide an *equals* behavior" `[from source] (CSYB p.133-134)`. Good manners: `Equals` and `ToString` in your classes `[from source] (CSYB p.134)`.
- Strings are special: `==` compares the text `[from source] (CSYB p.137)`.
- [extrapolation] `GetHashCode` absent from the book. .NET rule: when overriding `Equals`, also override `GetHashCode` consistently (equal objects, same hash).

## 8. Properties

- Property = a member that stores a value; a public field does not allow control; `Get/Set` methods give control with more code `[from source] (CSYB p.139)`.
- Syntax with `get` and `set`; `value` is the assigned value; read-only by omitting `set`; computed properties are also possible (`AgeInMonths`) `[from source] (CSYB p.139-140)`.
- Problems: the `set` cannot tell the caller that it rejected the value (only an exception); if the assignment can fail the author does not expose it as a property; a property runs code while looking like a simple assignment `[from source] (CSYB p.141)`. In a UI, properties let the object react to the change (update the screen) `[from source] (CSYB p.195)`.
- Auto-implemented properties: C# 3.0 (CSHist p.13); different accessibility for `get`/`set`: C# 2.0 (CSHist p.14). The example `public decimal Saldo { get; private set; }` is illustrative `[extrapolation]` (the syntax is not in the book).

## 9. Delegates and events

- *Delegate* = **type-safe** reference to a method (unlike a C pointer) `[from source] (CSYB p.142, 206)`. Declaration `public delegate decimal CalculateFee(decimal balance);` and use `new CalculateFee(RipoffFee)` `[from source] (CSYB p.142-144)`.
- Events: the system receives delegates to know what to call when something happens (button, timer) `[from source] (CSYB p.142, 197-198, 207)`; `+=` registers and `-=` removes a handler `[from source] (CSYB p.198)`.
- The author uses delegates mainly in events and threads (`ThreadStart`), "not much beyond that" `[from source] (CSYB p.145, 174)`.
- [extrapolation] multicast delegates and the `event` restriction (only `+=`/`-=` from outside): not in the book.

## 10. Hash table (as motivation)

- Sequential search gets slow; a hash table computes a position from the key; a collision ("hash clash") is resolved by looking for the next free position `[from source] (CSYB p.147-148)`. `Hashtable` in `System.Collections` with `as IAccount` `[from source] (CSYB p.148)` `[DATED]` (see `avancado-e-execucao.md`).

## 11. Outside the book (labeled supplement)

| Topic | Status |
| :-- | :-- |
| Struct on the stack, class on the heap; struct does not inherit from a class; struct without `null` | [extrapolation] |
| `readonly struct`, `record struct`, immutability as a rule | `readonly struct` only listed in CSHist p.9; recommendation = [extrapolation] |
| Default modifier `private`; `internal` (assembly) | [extrapolation] |
| `GetHashCode` paired with `Equals` | [extrapolation] |
| Dispatch of `new` vs `override`; *vtable* | [extrapolation] |
| Dependency injection, mocks | [extrapolation] |
| Records, `init`, `with`, primary constructors | see `recursos-modernos.md` |
