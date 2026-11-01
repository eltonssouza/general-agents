# Fundamentals: what an algorithm is, how to describe it and how to analyze it (Ch. 0)

Source: *Algorithms*, Jeff Erickson (1st paperback ed., Jun 2019, 472 pp.), abbreviation **JE**. **Cited pages = PDF pages** (printed page = PDF − 18). Chapter 0 = PDF p.19-38 (exercises on p.35-38). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

---

## 1. What an algorithm is
- `[from source]` An algorithm is a sequence of elementary instructions that is explicit, precise, unambiguous and mechanically executable, generally aimed at a specific goal (JE p.19). The word derives from the name of al-Khwārizmī (JE p.19-20).
- `[from source]` The chapter compares several algorithms for the same problem (multiplication): the lattice method (*lattice multiplication*), which multiplies numbers of $m$ and $n$ digits in $O(mn)$ time (JE p.21-23); multiplication by duplication and mediation (*peasant multiplication*), based on the recursive identity for $x \cdot y$ and with time $O(\log x \cdot \log y)$ (JE p.23-25); and the compass-and-straightedge construction, where the model of computation is ideal geometric operations (JE p.25-26).
- `[from source]` Examples of reductions and of a "non-algorithm": the Huntington-Hill apportionment algorithm (priority queue, JE p.26-28) and "Martin's algorithm", which is not an algorithm because it is vague (JE p.28).

## 2. How to describe an algorithm (Ch. 0.5, JE p.29-32)
- `[from source]` A complete description has four components: *What* (precise specification of the problem), *How* (description of the algorithm), *Why* (proof that it solves the problem) and *How fast* (running-time analysis) (JE p.29).
- `[from source]` Specifying the problem: restate the statement in formal mathematical objects, make hidden assumptions explicit and include just enough detail to use the algorithm as a black box (JE p.30-31).
- `[from source]` Describing the algorithm: algorithms are not programs; the clearest combination is pseudocode with structured English; avoid language-specific syntax and never describe repetition informally ("do this, then that...") — if there is a loop, write the loop; if it is recursive, write it recursively (JE p.31-32).
- `[inference]` "Precondition" and "postcondition" are customary terminology, but they are **not** the book's terms; the book speaks of specifying the input and output (JE p.30-31).

## 3. Correctness and running time (Ch. 0.6, JE p.32-35)
- `[from source]` The book demands algorithms that are always correct, for all inputs, and **with a proof**; testing a few cases is not enough. Correctness proofs "usually involve induction" (JE p.32).
- `[from source]` Running time: the book wants efficient algorithms **even in the worst case**; it is measured by counting how many times an instruction or a landmark of the code is executed, and what matters is how the time grows with $n$, not the technology used (JE p.33).
- `[from source]` Nested loops lead to summations; recursive algorithms lead to recurrences; the result for peasant multiplication is $T(x,y) \le T(\lfloor x/2 \rfloor, 2y) + 2$, hence $O(\log x)$ (JE p.34). The time may depend on the implementation of an underlying structure: in the apportionment example, $O(Rn)$ with an unsorted array and $O(R \log n)$ with a binary heap (JE p.34-35). Other resources (space, etc.) are analyzed with the same techniques (JE p.35).

## 4. What Ch. 0 does NOT contain (corrected relative to the v1 package)
- `[from source]` The chapter uses $O$ and $\Theta$ **informally** (for example, the time to sing BottlesOfBeer is "asymptotically $\Theta(n)$") (JE p.33); there is **no** formal definition of the notations $O, \Omega, \Theta, o, \omega$ with constants $c$ and $n_0$ in this chapter. The Preface lists asymptotic notation ($o, O, \Theta, \Omega, \omega$) as a prerequisite (JE p.6). The formal table of definitions that was in the v1 package was removed as `[from source]`.
- `[from source]` The RAM model is only described in Ch. 12, in a footnote and in the section of formal definitions (JE p.402). Ch. 0 neither "defines the RAM model" nor stipulates unit cost for operations.
- `[extrapolation]` Customary formal definitions: $f=O(g)$ if there exist $c>0$ and $n_0$ such that $0 \le f(n) \le c\,g(n)$ for $n \ge n_0$; $\Omega$ is the analogous lower bound; $\Theta$ is $O$ and $\Omega$ at the same time; $o$ and $\omega$ are the strict bounds. Useful for explaining, but **not** content from the book.
- `[from source]` The book does **not** contain the sentence "if you can't prove it by induction, you don't understand why it works" attributed to Erickson in the v1 package (removed). What it says is that correctness proofs use induction and that "induction is our friend" (JE p.32).

## 5. Common pitfalls (all `[inference]` from JE p.32-35, 48-52)
1. $O$ is only a ceiling: saying an algorithm is $O(n^2)$ does not say it is $\Theta(n^2)$. For QuickSort with a bad pivot the book shows $O(n^2)$ and comments that the analysis is tight (JE p.48, 52).
2. Do the analysis in terms of how many times a subroutine is called when its cost is unknown (like `IsWord` in text segmentation, JE p.102; like the priority queue operations, JE p.34-35).
3. If the numbers are large, the arithmetic cost is no longer $O(1)$: the book shows this for Fibonacci (JE p.122-123).

## Outside the book (do not answer as `[from source]`)
In-depth amortized analysis, the formal substitution method, the growth hierarchy and proofs about asymptotic notation. The book mentions amortization in passing (JE p.282-283) and leaves the analysis of randomized QuickSort out of scope (JE p.49, note 7).
