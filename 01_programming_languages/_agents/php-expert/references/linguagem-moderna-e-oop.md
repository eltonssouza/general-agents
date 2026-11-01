# Paradigms, namespaces, SPL, CLI and Xdebug (PRW p.10-14)

Pages = PDF. The book is **short** on this topic: it does not teach typing, closures in detail or PHP 8.x features (see section 6).

## 1. Paradigms
- PHP is flexible and dynamic; it has evolved a lot: a solid object model in **PHP 5.0 (2004)**, anonymous functions and namespaces in **5.3 (2009)**, traits in **5.4 (2012)** `[from source] (PRW p.10)`.
- **OOP**: classes, abstract classes, interfaces, inheritance, constructors, cloning, exceptions; links to OOP and Traits `[from source] (PRW p.11)`.
- **Functional**: first-class functions (assign to a variable, pass as an argument, return), recursion is supported but PHP code usually uses iteration; anonymous functions with closures exist since 5.3 (2009); 5.4 allowed binding closures to an object's scope and improved `callables` `[from source] (PRW p.11)`.
- **Metaprogramming**: Reflection API and magic methods (`__get()`, `__set()`, `__clone()`, `__toString()`, `__invoke()`); the equivalent of Ruby's `method_missing` is `__call()` and `__callStatic()` `[from source] (PRW p.11)`.

## 2. Namespaces
- They exist so that two libraries with the same class name do not collide; compared to operating-system directories `[from source] (PRW p.12)`.
- Using namespaces in your code is recommended so that others can use it without fear of collision `[from source] (PRW p.12)`.
- For file/class/namespace convention and autoload, the book recommends **PSR-4**; in October 2014 PHP-FIG **deprecated PSR-0**, both still usable; PSR-4 requires PHP 5.3; for new code, PSR-4 `[from source] (PRW p.12)`.

## 3. Standard PHP Library (SPL)
- Ships with PHP; it gathers classes and interfaces, mainly data structures (stack, queue, heap) and iterators that traverse those structures or your classes that implement SPL interfaces `[from source] (PRW p.12)`.
- The book does **not** cite `SplFixedArray`, `SplDoublyLinkedList` or memory benchmarks (v1 claimed this as from the book).

## 4. CLI
- PHP was born for the web but serves command-line scripts (tests, deploy, administration); CLI programs use the application code without creating a web GUI; **do not put CLI scripts in the public web root** `[from source] (PRW p.12-13)`.
- `php -i` prints the configuration (like `phpinfo()`); `-a` opens an interactive shell `[from source] (PRW p.13)`.
- `$argc` is the count and `$argv` the array of arguments; the first argument is always the script name; `exit()` with a non-zero number signals failure to the shell `[from source] (PRW p.13)`.

## 5. Xdebug
- PHP debugger, used by IDEs for breakpoints and stack inspection; it also lets PHPUnit and KCacheGrind do coverage analysis and profiling `[from source] (PRW p.14)`.
- Mentions "Remote Debugging" for local code tested on a VM/another server `[from source] (PRW p.14)`.
- `[DATED]`: the book configures with `xdebug.remote_host`/`xdebug.remote_port` and `XDEBUG_SESSION_START` (p.14), Xdebug 2 names. `[extrapolation]`: Xdebug 3 uses `xdebug.mode` and `xdebug.client_host`/`client_port`; check the Xdebug documentation.

## 6. What the book does NOT cover here (`[extrapolation]` if asked)
Scalar and return typing, `declare(strict_types=1)`, nullable and union types, the `use` clause and variable capture in closures, `fn` arrow functions, `match`, enums, attributes, `readonly`, fibers. If the user asks, answer with general knowledge labeled `[extrapolation]` and `[VERSION-DEPENDENT]`, and say that the PRW does not teach it.
The only 8.x code snippets in the book: constructor property promotion, `public function __construct(protected AdapterInterface $adapter)` (PRW p.38, 41) and the `??` operator (PRW p.53).
