# Mutable state, concurrency and streams

Source: SICP ch. 3 (PDF pages; see `INDEX.md`). The substitution model and the environment model are in `modelos-de-avaliacao-substituicao-vs-ambiente.md`.

## 1. The cost of assignment (SICP 3.1.3)
- `[from source]` (SICP p.217): assignment allows modeling objects with local state, but at the price of the language no longer being interpretable by the substitution model; without assignment, procedures are seen as mathematical functions (functional programming).
- `[from source]` (SICP p.219-220): equality and identity ("sameness") become problematic: `D1` and `D2` (from `make-decrementer`) are interchangeable; `W1` and `W2` (from `make-simplified-withdraw`) are not. Two distinct accounts vs. a single object with two names (`peter-acc` and `paul-acc`) is the book's example (SICP p.220); note 10 (p.223) calls this *aliasing* and comments on side-effect bugs.
- `[from source]` (SICP p.220): referential transparency ("equals can be substituted for equals") is violated by `set!`; reasoning about programs with assignment becomes much harder.
- `[from source]` (SICP p.221): programming with heavy use of assignment is called *imperative*; it is subject to bugs that do not occur in functional programs (example: order of assignments in `factorial`).
- `[from source]` (SICP p.222, ex. 3.8): with assignment, the order of evaluation of the arguments can change the result.
- `[inference]`: "`(f x) + (f x)` ≠ `2 * (f x)`" when `f` changes state is a direct consequence of p.217-220, but is not a sentence from the book.

## 2. Concurrency: time becomes crucial (SICP 3.4)
- `[from source]` (SICP p.279): by introducing assignment we are forced to admit *time*; before, "any expression that has a value always has the same value".
- `[from source]` (SICP p.280-281): two processes doing `withdraw` on a shared `balance` can interleave the three steps of `(set! balance (- balance amount))` (read, compute, write); the book shows a catastrophic result in which the total money is not conserved (Peter $10, Paul $25, bank $75 after starting from $100; figure 3.29).
- `[from source]` (SICP p.282): restricting everything to one operation at a time would be inefficient; a less strict criterion is that the system produce the same result as *some* sequential execution of the processes, and there may be more than one correct result (example: $70 or $90, SICP p.282).
- `[from source]` (SICP p.283): there are even weaker requirements (heat-diffusion simulation converges regardless of order); with processes of 3 events each, there are 20 possible interleavings, which makes case-by-case analysis infeasible.
- `[from source]` (SICP p.284-285): **serializer** (`make-serializer`) creates sets of procedures of which only one execution at a time is allowed; `parallel-execute` creates concurrent processes. Without a serializer, `(set! x (* x x))` and `(set! x (+ x 1))` with `x = 10` can produce five values; with a serializer only 101 or 121 (SICP p.284-285).
- `[from source]` (SICP p.288-289): serializing deposits/withdrawals per account is not enough for `exchange`; the book deliberately exposes the account's serializer (breaking modularity) to serialize the entire exchange (`serialized-exchange`).
- `[from source]` (SICP p.290-291): serializers are implemented with a **mutex** (an object that can be acquired and released; while acquired, other acquisitions wait, SICP p.290), which in turn uses `test-and-set!`. `test-and-set!` **must be atomic** (SICP p.291); its implementation depends on how the system runs processes: on a sequential processor with time-slicing, it can disable time-slicing during the test and the assignment; on multiprocessors, there are atomic hardware instructions (SICP p.291).
- `[from source]` (SICP p.292): **deadlock**: Peter exchanges `a1`/`a2` while Paul exchanges `a2`/`a1`; each waits for the other. The book says this is a danger whenever there is concurrent access to several shared resources. One way out is to number the resources and always try to acquire the lowest-numbered one first; the book notes that there are situations that require more sophisticated techniques or in which deadlock cannot be avoided (SICP p.292).
- `[from source]` (SICP p.293): synchronization requires communication; "time" in concurrency control is tied to communication (SICP p.293).
- `[inference]`: the v1 interleaving diagram (withdrawal of 10 / deposit of 20) is our illustrative example, analogous to that of figure 3.29 of the book.

## 3. Streams (SICP 3.5)
- `[from source]` (SICP p.296): streams are presented as an alternative for modeling state without the cost of assignment, describing the history over time of a quantity as a (possibly infinite) sequence, instead of a changing variable.
- `[from source]` (SICP p.297): efficiency motivation: with lists, `(car (cdr (filter prime? (enumerate-interval 10000 1000000))))` builds a list of nearly a million integers; streams interleave enumeration and filtering.
- `[from source]` (SICP p.298-299): `cons-stream`, `stream-car`, `stream-cdr`, `the-empty-stream`; `(cons-stream <a> <b>)` is equivalent to `(cons <a> (delay <b>))`; `stream-cdr` is equivalent to `(force (cdr stream))`. With lists, car and cdr are evaluated at construction; with streams, the cdr is evaluated at selection. `cons-stream` and `delay` must be special forms (note 56, p.329).
- `[from source]` (SICP p.301): `delay` is sugar for `(lambda () <exp>)` and `force` calls that procedure; the idea of "demand-driven programming" decouples the actual order of computation from the apparent structure of the procedures.
- `[from source]` (SICP p.302): memoization optimization: `(delay <exp>)` can be `(memo-proc (lambda () <exp>))`, which stores the value on the first call (variables `already-run?` and `result`).
- `[from source]` (SICP p.303-306): infinite streams: `integers-starting-from`, `no-sevens`, `fibgen`, sieve of Eratosthenes (p.304-305), implicit definition `ones`, `integers` via `add-streams` and `fibs` via `add-streams` (p.305-306).
- `[from source]` (SICP p.325): converting to normal order (all arguments delayed) would simplify the use of delay, but "mutability and delayed evaluation do not mix well" (SICP p.325).
- `[from source]` (SICP p.325-326): 3.5.5 shows that streams allow modularity without assignment or local state (Monte Carlo example with `cesaro-stream`).

## 4. What the book does not say
- That streams "eliminate the need for mutable accumulators" in general: it says they mitigate part of the complexity (SICP p.296) and that there are limits to combining them with mutation (p.325).
- That a mutex is a "hardware register": it says that `test-and-set!` must be atomic and that the implementation depends on the system (SICP p.291).
