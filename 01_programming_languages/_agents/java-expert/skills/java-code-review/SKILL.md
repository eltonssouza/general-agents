---
name: java-code-review
description: Reviews Java code for fundamentals and best practices from the books — `==` on String, `equals` without `hashCode`, missing `@Override`, `finalize`, empty `catch`, resource outside try-with-resources, `return null` for a collection, concatenation in a loop, immutability — with an automatic regex scan and a checklist. Use when the user asks "review this Java class", "is this correct?", "code review of my package", "what should I improve in this code" or pastes Java code. Do not use to interpret a stack trace (use java-exception-triage), for memory/thread problems at runtime (use java-jvm-troubleshooting) or for modern Java features (the sources do not describe them).
---

# Java code review

Sources: Think (introductory, Java SE 8) and Adv (e-book, Java 7/8). Details in `../../references/procedimentos.md`, `frameworks.md` and `casos-e-antipadroes.md`. **Everything is from a Java 7/8 era**: recommendations that depend on the version are **[DATED]** relative to the current JDK.

## Procedure

1. **Find out the user's JDK.** Without it, keep version-dependent recommendations conditional. The sources do not cover records, `var`, text blocks etc., and streams appear only in passing (method reference example in Adv p.62; `parallelStream()` as a Java 8 novelty in Adv p.82; "lambdas and Stream API in Java 8" in Adv p.103); if the code uses them, say that you **cannot review them based on the sources** (use `java-jdk-features` to locate the JDK).
2. **Run the scan** (read-only; regex, does not compile or execute):
   ```bash
   python -I scripts/scan_java_smells.py CAMINHO
   ```
   **No findings is not approval**: the script understands neither types nor flow and does not cover concurrency, generics, leaks or use of lambdas/streams.
3. **Walk through the checklist** and confirm or discard each finding by reading the code.
4. **Label the era** of each recommendation: **[introductory]** (Think), **[advanced]** (Adv), **[DATED]** / **[DEPENDS ON VERSION]** when the source ties it to Java 7/8.
5. **Deliver** prioritized findings (format below).

## Checklist (each item points to the source)

**Equality and identity**
- `==` and `!=` on String do not do what is expected: use `equals` (Think p.86; Adv p.26).
- Define `equals` together with `hashCode`: equal objects must have the same `hashCode` (Adv p.23). The `equals` contract has five properties (Adv p.22).
- Use `@Override` when overriding `equals`, `hashCode`, `toString`: without it, a signature error becomes an overload and goes unnoticed (the text about `@Override` is in Adv p.34; Adv p.22–25 show the annotation in the examples; overloading versus overriding in Adv p.60–61).

**Resources and exceptions**
- `finalize` is considered dangerous; to release resources use try-with-resources with `AutoCloseable` (Java 7) (Adv p.16, 75).
- Do not swallow exceptions with an empty `catch`; log them (the only exception the book accepts is a failure of `close()`) (Adv p.73, 75).

**API and data**
- Return an empty collection instead of `null`; for an absent value the book cites `Optional` (Java 8) (Adv p.64).
- In loops, build text with `StringBuilder`, not with `+=` on a String (Adv p.69–70).
- Strings are immutable: methods like `replace` return a new String; the return value must be assigned (Think p.159).
- Immutable classes: `final` fields, no setters, defensive copies, getters that do not leak mutable state (Adv p.31–32; Think p.202).

## Response format

- **Summary** (2–3 lines) and the JDK considered.
- **Findings** by severity: `file:line` — problem — why it matters — fix — source (Think/Adv p.N) with era label.
- **Not verified**: what could not be confirmed (I did not compile, I did not execute).

## Limits

- The books have errors of their own (see `casos-e-antipadroes.md`, "Erros do próprio livro" / the books' own errors); do not reproduce them.
- The scan is regex: false positives and negatives.
