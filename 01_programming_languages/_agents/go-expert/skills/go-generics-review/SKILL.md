---
name: go-generics-review
description: Reviews and explains generics in Go — type parameters, constraints, type sets (`~T`, unions), `comparable`, instantiation, type inference, generic aliases and limits (no methods with their own type parameters). Use when the user says "how do I write this constraint", "cannot infer T", "empty type set", "why doesn't `any` satisfy `comparable`", "what is `~int`", "can I have a generic method?" or pastes code with `[T any]`/`[K comparable, V any]`. Do not use for generics in other languages nor for general review (use go-code-review).
---

# Generics in Go (Spec go1.26)

Source: Spec, p.20–24 (type sets), 30–40 (declarations), 36–39 (constraints, `comparable`), 58–63 (instantiation and inference) and the version appendix (p.114–117); release notes 1.20–1.24 for changes. Detail and pages in `../../references/regras-da-spec.md` (section 4, Generics). **Effective Go (2009) and the Little Go Book do not cover generics.**

## Procedure

1. **Identify the version** (go.mod). General rule of the Spec: a feature is rejected if the required language version is earlier than that of the feature, and the table on p.115–116 lists the minimum version (for example, `any` in `[K comparable]` requires 1.20). Versions: generics from 1.18; `comparable` satisfied by interfaces (e.g. `any`) from 1.20; extended inference in 1.21; generic type alias in 1.24 (Spec p.115–116; RN1.20 p.2; RN1.21 p.2; RN1.24 p.1).
2. **Read the constraint as an interface**: it defines a type set. A type-element constraint (`~int`, `int|string`, `[]P`) may omit `interface{}` in a parameter list; outside a list it is illegal (Spec p.37–38). In `type T[P *C] ...` the parse becomes an array: resolve with `interface{*C}` or a trailing comma (`[P *C,]`) (Spec p.37).
3. **Check the type set**: `~T` requires the underlying type of T to be T itself and T not to be an interface (`~MyInt` is illegal); non-interface terms of a union must be disjoint (`~int | MyInt` is illegal); unions with more than one term cannot contain `comparable` or interfaces with methods (Spec p.22–23). `interface{ int; string }` compiles but has an empty type set and cannot be instantiated (Spec p.22, 43).
4. **`comparable`**: strictly comparable types; interfaces are comparable but not strictly, and satisfy `comparable` since Go 1.20, so `any` works in `[K comparable]`; comparing values of a type parameter may panic at run time if the dynamic value is not comparable (Spec p.38–39).
5. **Operations on type parameters** require compatibility with the whole type set (index, range, receive, literals, operators); type assertion and type switch require `x` to be an interface, not a type parameter (Spec p.44, 53, 56, 66, 71, 85, 92).
6. **Limits**: a method uses only the receiver's type parameters, and there is no method with its own type parameters (Spec p.41–42); a function literal does not declare type parameters (Spec p.46); a generic type requires explicit type args in every instantiation (Spec p.36, 60).
7. **Inference** (`cannot infer`): type args may be omitted if inferable from arguments, assignment or return; a partial list is a prefix (omit from the right); an empty list `f[]` is illegal (Spec p.58–59). Two phases: typed operands, then untyped constants (Spec p.61–62). Example from the Spec itself: `f1 := apply[[]int]` supplies only `S` and infers `E` from the constraint `~[]E` (Spec p.59). A conflict between kinds of untyped constants also makes inference fail (Spec p.62). The exact text of the message "cannot infer T" is **not in any source**: say so. With no argument that fixes the parameter, supply the type arg explicitly.

## Response format

Rewritten constraint or explanation, the Spec rule that supports it (page) and the Go version the feature requires. Mark your deductions [inference] (e.g. an empty type set as a sign of a design error). Reply in the language the user writes in (default: English).

## Limits

- The Spec defines what is legal; it gives **no** style or performance guide for generics. Do not invent "when to use generics" recommendations.
- The formal unification rules (appendix p.116–117) are only mapped; the Spec says they can be ignored when writing code (Spec p.116).
- Items with no version stated by the Spec (e.g. `min`, `max`, `clear`, `[...]T`) → use the version table of the release notes in `versoes-e-migracao.md`.
