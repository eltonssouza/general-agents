# Syntax and language features (Ruby 3.0 to 3.4)

Convention: `(R3x p.N)` = PDF page of the note (see `INDEX.md`). The code examples in Portuguese below are **from the package** (labeled `[extrapolation]` when they go beyond the note).

## 1. Pattern matching
- `[from source]` 3.0: one-line pattern matching was redesigned (experimental): `=>` works as rightward assignment (`0 => a`, `{b: 0, c: 1} => {b:}`); `in` now returns `true`/`false`, whereas in 2.7 it raised `NoMatchingPatternError` (R30 p.5-6).
- `[from source]` 3.0: find pattern (experimental), for example `in [*pre, String => x, String => y, *post]` (R30 p.6). It stops being experimental in 3.2 (R32 p.10).
- `[from source]` 3.0: `case`/`in` stops being experimental (R30 p.7).
- `[from source]` 3.1: the pin `^` now accepts an **expression** (Feature #17411), for example `^(n + 2)` (R31 p.5). Parentheses are optional in one-line pattern matching, as in `[0, 1] => _, x` and `{y: 2} => y:` (R31 p.5). One-line pattern matching (`ary => [x, y, z]`) stops being experimental (R31 p.8).
- `[extrapolation]` The use of `^variavel` to match against an existing local variable already worked before 3.1; the notes only say that 3.1 extended the pin to expressions. If the student asks "which version introduced the pin", answer that the notes do not bring the original introduction.
- `[extrapolation]` Examples with `case dados in { status: 200 ... }` are illustrations of the package, not of the notes.

## 2. Methods and arguments
- `[from source]` 3.0: "endless" method definition: `def square(x) = x * x` (R30 p.6).
- `[from source]` 3.0: keyword arguments separated from positional ones; "in principle, code that emitted a warning in 2.7 does not work" (R30 p.7). Argument forwarding with `...` now accepts leading arguments, for example `def method_missing(meth, ...)` (R30 p.7).
- `[from source]` 3.2: anonymous `*` and `**` can be forwarded to other calls (note's example: `def foo(*)` calling `bar(*)`) (R32 p.8-9). A proc that accepts one positional argument and keywords no longer autosplats (`proc{|a, **k| a}.call([1, 2])` returns `[1, 2]`) (R32 p.9). Methods with a rest parameter that forward keywords via `foo(*args)` must be marked with `ruby2_keywords`, "without exception" (R32 p.10).
- `[from source]` 3.2: the evaluation order in `foo::BAR = baz` and in multiple constant assignments becomes consistent (left to right) (R32 p.9). In 3.1, the evaluation order of multiple assignment such as `foo[0], bar[0] = baz, qux` changed (R31 p.8).
- `[from source]` 3.4: `**nil` is now accepted (equivalent to `**{}`); block and keyword arguments in an index (`a[...]`) are no longer allowed; the top-level name `::Ruby` is reserved (R34 p.5).
- `[from source]` 3.1: value omission in Hash literals and in calls: `{x:, y:}` is equivalent to `{x: x, y: y}` and `foo(x:, y:)` to `foo(x: x, y: y)` (Feature #14579) (R31 p.5).

## 3. The `it` parameter (Ruby 3.4)
- `[from source]` 3.3: `it` calls without arguments, in a block without ordinary parameters, are deprecated; in 3.4 `it` will be a reference to the first parameter (R33 p.6).
- `[from source]` 3.4: `it` references the unnamed block parameter: `ary.map { it.upcase }` (R34 p.1). It behaves like `_1`; the note recommends using `it` in simple cases, such as one-line blocks, and observes that, when only `_1` is intended, the possibility of `_2` appearing increases the cognitive load (R34 p.1).
- `[VERSION-DEPENDENT]` Only in Ruby 3.4 (in 3.3 it is a deprecation, R33 p.6). In RSpec tests, `it "..." do` is a method with arguments and is not affected (`[extrapolation]`).

## 4. String literals and freezing (Ruby 3.4)
- `[from source]` String literals in files **without** a `frozen_string_literal` comment now emit a deprecation warning when they are mutated. The warnings can be turned on with `-W:deprecated` or `Warning[:deprecated] = true`. To undo the change, run Ruby with `--disable-frozen-string-literal` (Feature #20205) (R34 p.5).
- `[inference]` The note does not say that literals will be frozen by default in the future; it says only that mutation already emits a warning (R34 p.5). Any claim of "mandatory freezing in the future" is `[extrapolation]`.
- `[extrapolation]` The unary prefix `+""`, `String.new` and interpolation as replacements to avoid the warning are not in the notes; they are general Ruby techniques.
- `[inference]` By the text, the effect described for 3.4 is a deprecation warning, not an exception (R34 p.5); `FrozenError` appears when the object is actually frozen, which the notes do not detail.

## 5. `Data`, `Struct` and collections (Ruby 3.2)
- `[from source]` `Data` is a new core class for simple immutable values; it is similar to `Struct` and shares part of the implementation, but has a leaner and stricter API (Feature #16122) (R32 p.11). Example from the note: `Measure = Data.define(:amount, :unit)`; `Measure.new(100, 'km')`; `Measure.new(amount: 50, unit: 'kg')`; `weight.with(amount: 40)`; `weight.amount = 40` results in `NoMethodError` (R32 p.11-12).
- `[from source]` `Struct` accepts keyword initialization without `keyword_init: true` (R32 p.15).
- `[inference]` For values that must not change, `Data` expresses this better than `Struct`; the note does not say that `Struct` should be abandoned. Value equality, `eql?` and destructuring of `Data` are **not** in the notes (`[extrapolation]`).
- `[from source]` `Set` becomes a built-in class without `require "set"` (autoload via `Set` or `Enumerable#to_set`) (R32 p.15). `Hash#except` has been native since 3.0 (R30 p.6). Other 3.2 items: `Hash#shift`, `MatchData#byteoffset`, `Module#refinements`, `Module#const_added`, `String#byteindex`, `String#bytesplice` (R32 p.12-15).
- `[from source]` 3.4: `Hash#inspect` now shows symbol keys in the style `{user: 1}` and other keys with spaces around `=>` (R34 p.8); `Range#size` raises `TypeError` if the range is not iterable (R34 p.6).

## 6. Compatibility
- `[from source]` Removed in 3.2: `Fixnum`, `Bignum`, `Dir.exists?`, `File.exists?`, `Kernel#taint` and related (R32 p.16). Removed in 3.4: `Refinement#refined_class` (R34 p.9); warnings for a block passed to a method that does not use it, in verbose mode `-w` (R34 p.10).
