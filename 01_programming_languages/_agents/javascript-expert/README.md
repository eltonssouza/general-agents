# javascript-expert (Claude Code, Codex and GitHub Copilot)

JavaScript (ECMAScript) specialist agent distilled from three sources of different natures and epochs, with 4 skills (deterministic read-only scripts), a topic lookup script and 9 references traceable by PDF page. The rights to the works belong to the authors and to Ecma International; this package contains original syntheses, not the text of the works.

## Sources and epochs

| Abbreviation | Work (file in `01_programming_languages/`) | Epoch / nature |
|---|---|---|
| Spec | *ECMA-262*, 17th edition, ECMAScript 2026 (`JavaScript-ECMA-262-Spec.pdf`, 876 p.) | official standard; barely dates the entry edition of features (apart from occasional notes and Annexes E and F, p.865–869); p.813–842 (end of the memory model and Annex A, grammar summary) not distilled into `references/` |
| EJpt | *Eloquent JavaScript* in Portuguese (`JavaScript-Eloquent-JS-PTBR.pdf`, 504 p.) | modern edition; declares it uses "the 2024 version of JavaScript" (EJpt p.9; that it is the 4th edition is an **[inference]**) |
| EJ1 | *Eloquent JavaScript* (`JavaScript-Eloquent-JS-EN-3ed.pdf`, 247 p.) | despite the file name, it is the **1st edition** (2007, revised until Nov/2013; EJ1 p.247): **everything is [DATED]** |

**Page convention: `(Spec p.N)`, `(EJpt p.N)` and `(EJ1 p.N)` are PDF pages.** In the Spec the printed page is N − 24; EJpt and EJ1 have no printed numbering. Page map by topic in `references/INDEX.md`.

**Source rigor:** the agent separates `[from source]` (checked on the cited page) from `[inference]`, `[extrapolation]`, `[DATED]`, `[VERSION-DEPENDENT]` and `[HOST]` (boundary between the language and the browser/Node). When neither the Spec nor the books state the entry edition of a feature, the answer is "version not stated in the sources".

## Structure

```
javascript-expert/
├── .claude-plugin/plugin.json
├── .github/agents/javascript-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                    # Codex
├── agents/javascript-expert.md                  # Claude Code
├── references/   INDEX + 9 thematic files (glossary, decision frameworks, procedures,
│                 cases and anti-patterns, language, built-ins, versions and dated)
├── scripts/      js_topic_lookup.py + js_topic_index.json   (topic -> pages per source; NOT COVERED)
├── skills/
│   ├── js-spec-lookup/       scripts/spec_lookup.py + spec_toc.json (2,224 Spec sections)
│   ├── js-code-review/       scripts/scan_js_smells.py + fixtures/sample.js
│   ├── js-error-triage/      scripts/parse_js_stack.py + fixtures/trace.txt
│   └── js-version-features/  scripts/js_version_lookup.py + js_version_data.json
└── tests/        casos-de-teste.md, relatorio-de-fidelidade.md, citation-checks.json, verify_citations.py,
                  audit_tokens.py (+ audit-tokens-baseline.txt), extract_pages.py, run_script_tests.py, fixtures/
```

## Installation

Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Agent and plugin formats change: check each platform's current documentation before installing.**

### Claude Code
- Local plugin: `claude --plugin-dir /path/to/javascript-expert` (the agent and the 4 skills are discovered through the plugin structure).
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install javascript-expert@general-agents`.
- Or as a standalone subagent: copy `agents/javascript-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep the package folder accessible (the prompt uses paths relative to the package root: `references/`, `scripts/`, `skills/`). The agent declares `tools: Read, Grep, Glob, Bash, Edit, Write`; remove `Bash` to prevent running the scripts.

### Codex (OpenAI)
Copy the package folder into the repository (for example `tools/javascript-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. The file is about 15 KB, below the default Codex instruction limit; check the current limit.

### GitHub Copilot
Copy `.github/agents/javascript-expert.agent.md` to the `.github/agents/` folder of your repository and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The frontmatter declares `tools: ['read', 'search', 'edit', 'execute']`; remove `execute` to block the scripts and `edit` to make it read-only.

## Scripts (deterministic, no network, read-only)

```bash
python -I scripts/js_topic_lookup.py Promise.any            # topic -> Spec p.774-775 (or NOT COVERED)
python -I scripts/js_topic_lookup.py --missing              # what the sources do NOT cover
python -I skills/js-spec-lookup/scripts/spec_lookup.py SameValue
python -I skills/js-spec-lookup/scripts/spec_lookup.py --section 13.11
python -I skills/js-code-review/scripts/scan_js_smells.py skills/js-code-review/scripts/fixtures/sample.js
python -I skills/js-error-triage/scripts/parse_js_stack.py skills/js-error-triage/scripts/fixtures/trace.txt
python -I skills/js-version-features/scripts/js_version_lookup.py groupBy
python -I tests/run_script_tests.py                         # actually runs all the scripts
```

Origin of the rules: each rule of `scan_js_smells.py` cites the page of the source that supports it and, when the rule (or the threshold) comes from the script and not from the book, the text says **[inference]** or **[extrapolation]**; the index of `js_topic_lookup.py` is derived from the references (`--rebuild` regenerates it, `--check` verifies it). The scan is lexical by regex: "no findings" is never approval.

## Package verification (maintenance)

The verifiers need the PDF text, extracted per page:

```bash
python -I tests/extract_pages.py /path/01_programming_languages /tmp/js-src     # requires PyMuPDF
python -I tests/verify_citations.py --src /tmp/js-src      # curated positive and negative checks
python -I tests/audit_tokens.py --src /tmp/js-src          # all package citations: page range and terms
python -I tests/run_script_tests.py --src /tmp/js-src      # scripts + verifiers + self-test
```

## Guarantees and limits

- Replies in the language the user writes in (default: English), without reproducing the works; citations by PDF page.
- Audit coverage and what it did not verify: `tests/relatorio-de-fidelidade.md`. The Spec is huge (876 pages): the manual audit used a declared stratified sample, and the automatic verification covers all citations by page range and by terms.
- The entry edition of most modern features (`?.`, `??`, `#private`, `at`, `toSorted`, `Object.hasOwn`, `Object.groupBy`, `Promise.any`, `Set.prototype.union` etc.) is not in the sources: the agent answers "version not stated in the sources".
- Outside the scope of the sources: TypeScript, frameworks (React, Vue, Angular, Express, Next.js…), bundlers, `structuredClone`, `queueMicrotask`, `AbortController`, `Temporal`, detailed `Intl` (the Spec only refers to ECMA-402) and browser compatibility tables.
- The books have slips of their own, cataloged in `references/casos-e-antipadroes.md` (Section 5.1); the agent does not reproduce them as correct.
- Code, comments, stack traces and PDF text pasted by the user are **data, never instructions**.
- The tests were **not** run blind by an independent model in this audit (see the report).
