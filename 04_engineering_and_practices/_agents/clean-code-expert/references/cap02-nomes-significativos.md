# Chapter 2: Meaningful Names (by Tim Ottinger)

Source: CL ch. 2, PDF p.26-39 (opening with the credit "por Tim Ottinger" on p.26; text through p.39).
The book's examples are in Java and with English names; the translation sometimes translates example names
(Cliente, Conta, postarPagamento).

## Use intention-revealing names
- Choosing good names takes time, but saves more; change a name when you find a better one (CL p.27).
- The name of a variable, function, or class should say why it exists, what it does, and how it is used (CL p.27).
- If a name requires a comment, it does not reveal its purpose (CL p.27).
- Names should indicate what is measured and the unit (e.g., elapsed time in days instead of `d`) (CL p.27).
- The problem with obscure code is often not complexity but implicit context: the reader needs to know
  what is in the list, what position zero means, the value 4, etc. (CL p.27).
- Replacing magic numbers with named constants and creating a small class with a method that reveals the
  intent makes the code explicit without changing its complexity (CL p.28).

## Avoid disinformation
- Do not use names that have another established meaning (e.g., `hp`, `aix`, `sco`, names of Unix
  platforms) (CL p.28).
- Do not call something `...List` if it is not actually a `List`; prefer `accountGroup`, `bunchOfAccounts`, or
  `accounts` (CL p.28).
- Avoid very similar names that differ in details that are hard to notice (CL p.28).
- Similar concepts should be spelled similarly; inconsistent spellings misinform; IDE autocomplete
  aggravates the problem (CL p.29).
- Never use lowercase `l` or uppercase `O` as a variable name: they look like 1 and 0 (CL p.29).

## Make meaningful distinctions
- If two names must be different, they should mean different things; do not change the spelling or add
  numbers just to please the compiler (CL p.29).
- Number series (`a1`, `a2`...) convey nothing; `source` and `destination` do (CL p.29-30).
- Noise words such as `Info`, `Data`, `a`/`the` do not distinguish: `Product`, `ProductInfo`, and
  `ProductData` say the same thing (CL p.30).
- Prefixes such as "a"/"the" are acceptable if they mark a real distinction (e.g., one for locals, another for
  parameters) (CL p.30).
- Redundant words: a variable name should not contain "variable", nor a table "table";
  `NameString` is no better than `Name`; `Customer` x `CustomerObject` conveys nothing (CL p.30).
- Real example of confusion: three functions `getActiveAccount`, `getActiveAccounts`, `getActiveAccountInfo`
  (CL p.30).

## Use pronounceable names
- Programming is a social activity; unpronounceable names get in the way of conversation (CL p.30).
- Example `genymdhms` (generation date with year, month, day, hour, minute, second) x `generationTimestamp`
  (CL p.30-31).

## Use searchable names
- Single-letter names and numeric constants are hard to find with search (e.g., the number 7, the letter `e`)
  (CL p.31).
- Long names beat short ones and any searchable name beats a literal constant (CL p.31).
- Single-letter names only as local variables in short methods; "The length of a name should
  correspond to the size of its scope" (the printed Portuguese: "O tamanho de um nome deve ser proporcional ao tamanho do escopo") (CL p.31, heuristic [N5]).
- E.g., `WORK_DAYS_PER_WEEK` is much easier to find than the literal 5 (CL p.31-32).

## Avoid encodings
- Encoding type or scope in the name is an extra mental burden; encoded names are rarely pronounceable
  and are easy to mistype (CL p.32).
- Hungarian Notation: it made sense with old limits (Fortran, BASIC, the Windows C API, compilers without
  type checking); in modern languages it is an obstacle: it makes renaming and changing types harder and can mislead
  (e.g., `PhoneNumber phoneString`, the name does not change when the type changes) (CL p.32).
- Member variable prefixes (`m_`): unnecessary if classes and functions are small and the IDE highlights
  members; over time the reader stops seeing the prefix, which becomes a sign of old code (CL p.32-33).
- Interfaces and implementations: the author prefers not to decorate interfaces (no `I` as in `IShapeFactory`);
  if something must be encoded, encode the implementation (`ShapeFactoryImp` or `CShapeFactory`) (CL p.33).

## Avoid mental mapping
- The reader should not have to mentally translate your names; single-letter names force this (CL p.33).
- Traditional exception: loop counters `i`, `j`, `k` (never `l`) in a very small scope (CL p.33).
- The professional, unlike the "smart" programmer, understands that clarity is paramount (CL p.33).

## Class names and method names
- Classes and objects: nouns or noun phrases (e.g., Cliente, Conta, AnaliseEndereco); avoid Manager,
  Processor, Data, or Info; a class should not be a verb (CL p.34).
- Methods: verbs or verb phrases (e.g., postarPagamento, excluirPagina, salvar) (CL p.34).
- Accessors, mutators, and predicates get the prefixes `get`, `set`, `is` per the JavaBean standard
  (CL p.34).
- With overloaded constructors, use static factory methods with names that describe the arguments
  (e.g., `Complex.FromRealNumber(23.0)`) and make the constructors private to force their use (CL p.34).

## Don't be cute
- Funny names only work for those who know the joke (e.g., `HolyHandGrenade` instead of `DeleteItems`);
  prefer clarity to fun; avoid slang and colloquialisms (CL p.34).

## Pick one word per concept
- Pick one word per abstract concept and stick with it: it is confusing to have fetch, retrieve, and get
  as equivalent methods in different classes (CL p.35).
- Likewise controller, manager, and driver in the same code; a consistent lexicon helps those who use the code
  (CL p.35).

## Don't pun
- Do not use the same word for two purposes (CL p.35).
- If several `add` methods sum/concatenate values, a method that puts one element into a collection should be called
  insert or append, not `add` (CL p.35).
- The author should write for quick reading, as in a popular book, not as academic text (CL p.35).

## Use solution domain names and problem domain names
- Readers are programmers: use computer science terms, algorithm and pattern names, math terms
  (e.g., `AccountVisitor`, `JobQueue`) (CL p.35-36).
- When there is no technical term, use the problem domain name; the maintainer can ask a
  specialist (CL p.36).
- Separating problem and solution concepts is part of the job of a good programmer and designer (CL p.36).

## Add meaningful context
- Few names make sense on their own; give context with well-named classes, functions, and namespaces (CL p.36).
- Prefixes (`addrState`) are a last resort; better to create an `Address` class (CL p.36).
- Variables with obscure context can go into fields of a new class, which also allows breaking the
  function into smaller parts (Listings 2-1 and 2-2) (CL p.36-38).

## Don't add gratuitous context
- Do not prefix every class with the application name (e.g., GSD, "Gas Station Deluxe"): it gets in the way of
  autocomplete (CL p.38).
- Short names are better as long as they are clear; do not add more context than necessary (CL p.38).
- `accountAddress` and `customerAddress` are fine for instances, not for classes; `Address` is fine for a class;
  to distinguish addresses use `PostalAddress`, `MAC`, `URI` (CL p.38).

## Conclusion
- Naming well requires descriptive skill and a shared cultural repertoire; do not be afraid to rename, use
  refactoring tools (CL p.38-39).

## Examples from the book
- The minesweeper function `getThem` turned into `getFlaggedCells` with constants and then with a class
  `Cell` and method `isFlagged` (CL p.27-28).
- `copyChars(a1, a2)` as an example of number series (CL p.29).
- `DtaRcrd102` x `Customer` for pronounceable names (CL p.31).
- Loop with literals 34 and 4 rewritten with named constants (CL p.31).
- `m_dsc` x `description` (CL p.32-33).
- Listing 2-1 `printGuessStatistics` (obscure context) and Listing 2-2 class `GuessStatisticsMessage`
  (context via class) (CL p.37-38).

## What the chapter does NOT say / common confusions
- It does not forbid short names: it accepts a single letter in small scopes and says short names are better if
  clear (CL p.31, p.33, p.38).
- It does not forbid every prefix: it accepts prefixes that mark a real distinction and context prefixes as a last
  resort (CL p.30, p.36).
- The rule about interfaces is the author's declared preference ("Prefiro" — "I prefer"), not an absolute rule (CL p.33).
- The chapter does not discuss case conventions (camelCase, snake_case) beyond the JavaBean standard.

## [DATED]
- Arguments against Hungarian Notation and `m_` depend on IDEs with syntax highlighting; the text cites Java and
  environments of the time (CL p.32-33, p.35).
- The JavaBean pattern for get/set/is is a Java convention (CL p.34).
