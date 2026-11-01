# Reference index — java-expert

Load **only** the file you need. Every claim cites `(Think p.N)`, `(Adv p.N)`, `(JVM p.N)` or `(RN JDK N)`, with the **PDF** page (the package's single convention; exact map in the "Page map" section below).

| Code | Work | Nature | Caveat |
|---|---|---|---|
| Think | *Think Java* 6.1.3 (291 PDF pages) | introductory, examples tested with **Java SE 8** | has its own inconsistencies (see `casos-e-antipadroes.md`, Part 4); error messages in DrJava-style format, not literal `javac` output |
| Adv | *Advanced Java* (Java Code Geeks, 124 pp.) | Java 7/8 e-book | editing errors; figures and tables not extracted |
| JVM | *JVM Troubleshooting Handbook* (127 pp.) | **PermGen**-era HotSpot, examples on HotSpot 1.5 to 1.7, with a forward-looking section on Metaspace in Java 8 (p.21–26) | **very dated**; figures p.29, 65, 67, 68 empty; case on p.74 truncated |
| RN | OpenJDK 11, 17, 21, 22, 26 release notes | only **JEP numbers and titles**, GA and schedule | **do not describe any feature** |

**Golden rule:** nothing in the sources describes how modern Java works (records, sealed, virtual threads, streams, modules, `var`, text blocks). JDKs 9, 10, 12–16, 18–20, 23–25 and above 26 **have no source**. Frameworks (Spring, Hibernate…) are not taught: they appear only as context for the handbook's case studies (JVM p.73, p.78, p.102) and in Adv examples (p.55, p.98); constructor dependency injection is shown without a framework (Adv p.18–19) — see `glossario.md`, section 10.

## When to open each file

| Question | File |
|---|---|
| "What is X?" (term, API, concept) | `glossario.md` |
| "Which approach should I choose?" (equality, inheritance vs composition, immutability, exceptions, concurrency) | `frameworks.md` |
| "How do I do it step by step?" (debugging, `equals`/`hashCode`, immutable class, Scanner, executor) | `procedimentos.md` |
| "Why do I get this error?" / "is this a mistake in the book?" | `casos-e-antipadroes.md` |
| OOM, thread dump, deadlock, high CPU, `ClassNotFoundException`, verbose GC | `jvm-troubleshooting.md` |
| "Which JDK introduced X?", LTS, what is dated | `versoes-e-datado.md` (and the `java-jdk-features` script) |

## How to read large files

List the sections with `Grep` (pattern `^#{2,3} `) and read only the relevant one with `Read` (`offset`/`limit`). Before saying "not covered", Grep the term across **all** files.

## Marking conventions

- **[introductory]** Think; **[advanced]** Adv; **[DATED]** tied to Java 8 or earlier (or to PermGen); **[DEPENDS ON VERSION]** holds from/until a given version; **[inference]** a link made by whoever built the collection or a deduction across pages; **[extrapolation]** knowledge outside the sources (label it and recommend checking the documentation).
- Quotation marks only for short literal quotes (English) and JEP titles; the rest is paraphrase.

## Reading cautions

- A JEP title without "(Preview)" or "(Incubator)" does **not prove** the feature is final: that is an [inference].
- LTS: only what the pages say counts (the JDK 17 page calls 11 the "previous LTS release"; the JDK 21 page calls 17 the "previous LTS"); the JDK 11, 22 and 26 pages say nothing; there is no JDK 25 page.
- The JVM handbook describes what the text said for the PermGen era (HotSpot 1.5 to 1.7); it does not hold as the current state (Metaspace appears only in one forward-looking section on Java 8).

## Page map (convention: every `p.N` citation is the PDF page)

| Code | Source file (in `01_programming_languages/`) | PDF pages | Relation to printed numbering | Check |
|---|---|---|---|---|
| Think | `Java-Think-Java-6e.pdf` | 291 | **printed = PDF − 18** (PDF 143 = printed 125; table of contents and index use the printed number: "11 Classes 171" starts at PDF 189) | 218 pages with chapter header checked: difference 18 in all |
| Adv | `Java-Advanced-Tutorial.pdf` | 124 | footer "N / 113" = **PDF − 11** (PDF 85 = footer 74); the printed table of contents follows the footer numbering, with a one-page divergence on some items ("Finalizers": contents 4, footer 5) | 113 pages with footer checked: difference 11 in all |
| JVM | `Java-JVM-Troubleshooting-Guide-Oracle.pdf` | 127 | footer "N of 127" = **PDF** (PDF 84 = footer 84) | 93 pages with footer checked: difference 0 in all |
| RN | `Java-11-…`, `Java-17-…`, `Java-21-…`, `Java-22-…`, `Java-26-JDK-Release-Notes-OpenJDK.pdf` | 3 each | no useful numbering; cite `(RN JDK N)` | text of the Features section and the schedule on page 1 of each PDF |

Rules: never mix the numberings; when citing a number from a book's index or table of contents, convert it to the PDF page first. If the page was not checked against the PDF, do not use the [from source] label.

## Scripts and verification

- `scripts/java_lookup.py TOPIC` and `scripts/java_index.json`: which reference to open and which PDF pages cover the topic; "NOT COVERED" when the collection does not cover it.
- Skills with scripts: `java-jdk-features` (`jdk_lookup.py`), `java-code-review` (`scan_java_smells.py`), `java-exception-triage` (`parse_stacktrace.py`), `java-jvm-troubleshooting` (`summarize_thread_dump.py`).
- `tests/verify_citations.py` (+ `citation-checks.json`) and `tests/audit_tokens.py` (+ `audit-allowlist.json`) check the citations against the text extracted from the PDFs; `tests/run_script_tests.py` runs the scripts; see `tests/relatorio-de-fidelidade.md` for the audit coverage.
