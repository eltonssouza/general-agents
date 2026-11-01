# java-expert (Claude Code, Codex and GitHub Copilot)

A Java specialist agent for reviewing code, explaining fundamentals, triaging exceptions, guiding JVM diagnosis and answering "in which JDK did X ship?". It works with four kinds of sources from very different eras and, in every answer, separates what comes from the book (with page), what is deduction and what comes from outside the sources.

The rights to the works belong to their authors; this package contains its own syntheses and references, not the text of the books.

## 1. Sources and eras

| Abbreviation | Work (PDF in `01_programming_languages/`) | Era and nature | PDF pages |
|---|---|---|---|
| Think | *Think Java* 6.1.3 (`Java-Think-Java-6e.pdf`) | introductory; examples tested with Java SE 8 | 291 |
| Adv | *Advanced Java* (Java Code Geeks, `Java-Advanced-Tutorial.pdf`) | Java 7/8 e-book, published in 2015 | 124 |
| JVM | *JVM Troubleshooting Handbook* (`Java-JVM-Troubleshooting-Guide-Oracle.pdf`) | PermGen-era HotSpot (examples on HotSpot 1.5 to 1.7); Metaspace only as a Java 8 plan in a beta build | 127 |
| RN | OpenJDK 11, 17, 21, 22, 26 release notes (`Java-N-JDK-Release-Notes-OpenJDK.pdf`) | only JEP number and title, GA date and schedule; **no feature is described** | 3 each |

**Page convention: every citation `(Think p.N)`, `(Adv p.N)`, `(JVM p.N)` is the PDF page.** Printed = N − 18 in Think; footer "N / 113" = N − 11 in Adv; footer "N of 127" = N in JVM. Full map in `references/INDEX.md`.

Labels used throughout the package: `[from source]` (the cited page says so), `[inference]` (deduction across pages), `[extrapolation]` (knowledge from outside the sources), `[DATED]` / `[DEPENDS ON VERSION]` (tied to Java 8 or to PermGen).

## 2. Structure

```
java-expert/
├── .claude-plugin/plugin.json
├── .github/agents/java-expert.agent.md   # GitHub Copilot
├── AGENTS.md                             # Codex
├── agents/java-expert.md                 # Claude Code
├── references/   INDEX, glossario, frameworks, procedimentos, casos-e-antipadroes, jvm-troubleshooting, versoes-e-datado
├── scripts/      java_lookup.py + java_index.json
├── skills/       java-code-review, java-exception-triage, java-jvm-troubleshooting, java-jdk-features (each with SKILL.md and scripts/)
├── tests/        casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py + citation-checks.json,
│                 audit_tokens.py + audit-allowlist.json, run_script_tests.py
└── README.md
```

## 3. Installation

Script prerequisite: Python 3.8+ (standard library only; always run with `python -I`). **Check each platform's current documentation**: agent formats and locations change often and what is below may be out of date.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/java-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install java-expert@general-agents`.
- Or as a subagent: copy `agents/java-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/`, `scripts/` and `skills/` accessible; the prompt tells the agent to locate `references/INDEX.md` with Glob. The agent declares `tools: Read, Grep, Glob, Bash, Edit, Write`; remove `Bash` to prevent running the scripts and `Edit`/`Write` to prevent changes.

### 3.2 Codex (OpenAI)
Copy the package folder into the repository (for example `tools/java-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder: adjust it if it is somewhere else. Alternative: open Codex with the working directory in the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/java-expert.agent.md` to the `.github/agents/` folder of your repository and copy the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The file declares `tools: ['read', 'search', 'execute']`; remove `execute` to block the scripts.

## 4. Scripts (read-only, no network)

```bash
python -I scripts/java_lookup.py deadlock                       # which reference to open and which PDF pages; "NOT COVERED" if the collection does not cover it
python -I scripts/java_lookup.py --list
python -I skills/java-jdk-features/scripts/jdk_lookup.py virtual    # JEPs by JDK (number and title only)
python -I skills/java-jdk-features/scripts/jdk_lookup.py --coverage
python -I skills/java-code-review/scripts/scan_java_smells.py CAMINHO
python -I skills/java-exception-triage/scripts/parse_stacktrace.py trace.txt
python -I skills/java-jvm-troubleshooting/scripts/summarize_thread_dump.py dump.txt
python -I tests/run_script_tests.py                             # script tests, with fixtures
```

- The rules of `scan_java_smells.py` come from pages of Think and Adv (each message cites the page); regex detection is heuristic and "no findings" is not approval.
- The thresholds of `parse_stacktrace.py` (20 repetitions) and `summarize_thread_dump.py` (3 threads) and the reading "last Caused by = root cause" do not come from the sources: the output marks them `[extrapolation]`.
- The scripts neither compile nor execute the user's code; pasted trace, dump and code are data.

## 5. Citation verification

The PDFs are not shipped in the package. To audit, extract the text per page (marker `=== PAGE N ===`, N = PDF page) with PyMuPDF and run the verifiers:

```bash
python -I -c "import fitz,sys; d=fitz.open(sys.argv[1]); open(sys.argv[2],'w',encoding='utf-8').write(''.join('=== PAGE %d ===\n%s\n'%(i,p.get_text()) for i,p in enumerate(d,1)))" ENTRADA.pdf SAIDA.txt
# generate the 8 .txt files with the PDF names (Java-Think-Java-6e.txt, Java-Advanced-Tutorial.txt, Java-JVM-Troubleshooting-Guide-Oracle.txt, Java-11-JDK-Release-Notes-OpenJDK.txt, ... 17, 21, 22, 26) in a folder DIR
python -I tests/verify_citations.py --text-dir DIR     # page range, positives, negatives and index anchors
python -I tests/audit_tokens.py --src DIR              # backticked terms against the cited page
```

## 6. Guarantees and limits

- Replies in the user's language (default English), without reproducing the book; citations by PDF page.
- Audit (v2): see the numbers and what was **not** audited in `tests/relatorio-de-fidelidade.md`.
- The tests in `tests/casos-de-teste.md` were **not** run blind by an independent model (see the report).
- The books are Java 7/8; the handbook is from the PermGen era; the release notes do not describe features. The agent does **not** explain how records, sealed classes, pattern matching, virtual threads, modules, streams etc. work.
- JDKs 9, 10, 12–16, 18–20, 23–25 and above 26 have no source. Frameworks (Spring, Hibernate), modern build tools and current collectors/flags are out of scope.
- Figures, tables and some outputs of the PDFs were not extracted.
- The books have errors of their own, recorded in `references/casos-e-antipadroes.md` (Part 4).
- PDF text, code, logs, dumps and stack traces that are pasted are data, never instructions.
