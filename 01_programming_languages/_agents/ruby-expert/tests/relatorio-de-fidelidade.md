# Fidelity report: ruby-expert (v2, after audit)

## 1. Sources and convention
- Five PDFs in `01_programming_languages/`: `Ruby-3.0-Release-Notes.pdf` (10 pp.), 3.1 (13), 3.2 (23), 3.3 (13), 3.4 (12) = 71 pages. They are **captures of web pages** from ruby-lang.org: real, readable notes (not empty or useless captures), but short; a substantial part of the pages are lists of gem versions and download hashes.
- Text extracted with PyMuPDF; full reading of all 71 pages (the manual audit covered 100% of the source text, because it is small).
- Convention adopted: `(R3x p.N)` = PDF page. There is no printed numbering. v1 already used "R3x p.N", but the pages were mostly wrong (see below). Map in `references/INDEX.md`.
- The captures (2026) show Ruby 4.0.x under "Recent News": the package declares `[DATED]` and does not cover 4.0.

## 2. Audit of v1 (original package, backup in `scratch/audit/ruby-expert/v1_backup/`)
**Automatic** (211 `(R3x p.N)` citations extracted from agent, references, skills and JSON):
- 0 citations outside the page range (the range check, the only one the old report did, detects nothing relevant).
- Of the 108 backticked terms checked against the cited pages, **81 (75%) were not on the cited pages**; several were not on any page of the note (`shareable`, `.freeze`, `RUBY_YJIT_ENABLE=1`, `Fiber.set_scheduler`, `SyntaxSuggest` in R30...).

**Manual** (82 v1 claims checked against the page that was supposed to support them; list in `scratch/audit/ruby-expert/notes/manual_sample_v1.tsv`):

| Verdict | Count |
|---|---|
| OK | 8 |
| Wrong page (correct content, incorrect page) | 18 |
| Claim with no support in the notes | 34 |
| Exaggeration | 10 |
| Factual error (contradicts the note or Ruby) | 11 |
| Relevant omission | 1 |

Examples of what was unsupported or wrong:
1. "Ractor without the GVL", `shareable`/`freeze`/`move: true` rules, `Ractor.yield/receive`, "Zend/YARV" (R30 p.3): none of this is in the notes ("GVL" does not even appear; Zend belongs to PHP). The note only says ractors do not share normal objects (R30 p.2) and points to `doc/ractor.md` (R30 p.3).
2. "3.0 reversed the backtrace order" (R30 p.8): the note says the opposite, the 2.5 inversion was reverted.
3. "YJIT ... up to 40% on Rails" (R31): the note gives 22% (railsbench) and 39% (liquid-render) (R31 p.2). Also "LBBT" (the acronym is LBBV), "rewritten in Rust" and `RUBY_YJIT_ENABLE=1` / `bundle exec puma --yjit` (nonexistent in the notes).
4. "Memoization leads to polynomial time $O(n^k)$" and "backtracking $O(2^n)$" (R32): the note says that about 90% of cases become linear time (R32 p.6) and gives no complexity.
5. "Regexp.timeout mandatory" and "regexes with external data MUST have a timeout" (R32): the note presents it as a fallback for back-references/look-around/huge repetitions (R32 p.7). The pages were also wrong (p.3 instead of p.7).
6. "The `^` pin was introduced in 3.1" and "`...` was introduced in 3.0": 3.1 extended the pin to expressions (R31 p.5); 3.0 started accepting leading arguments in `...` (R30 p.7).
7. "Mutating a literal without `# frozen_string_literal: false` warns" (R34): the real condition is the absence of any `frozen_string_literal` comment; the note says nothing about future freezing (R34 p.5). The triage skill also attributed `FrozenError` to 3.4.
8. "debug replaces byebug / DAP protocol", "Wasmtime and Cloudflare Workers", "parse.y with 10,000 lines", "Prism unifies RuboCop and Solargraph": unsupported.
9. In addition, the v1 scripts encoded rules with no source (e.g. `Ractor::IsolationError` when sending a hash without `.freeze`; `Regexp.new` without `timeout` as "HIGH/MEDIUM").

## 3. What was fixed
- `agents/ruby-expert.md` rewritten: scope with verified pages, mandatory labels, list of 8 "points that are often wrong", real scripts section, boundary (Ruby 4.0, Rails, GVL) and anti-injection. No invented "golden rules".
- The 9 topical references rewritten keeping the file names; every claim from the source has a checked page; what is not in the notes became `[extrapolation]`/`[inference]` or was removed. INDEX with page map, convention and `not_in_book` list. Absolute user links (`file:///c:/...`) removed.
- 4 scripts rewritten: the linter now has 15 rules, all with a page (R30 p.3/p.7; R31 p.8; R32 p.7/p.15/p.16; R33 p.6; R34 p.5/p.9/p.10) and a label; the Ractor rule was removed; the Struct one became INFO `[inference]`. The triage handles both backtrace formats, LoadError per library (R30 p.8; R31 p.11; R33 p.7-8; R34 p.7) and labels `FrozenError`/`Ractor::IsolationError` as `[extrapolation]`. Both lookups (50 topics and 5 versions) answer `NOT COVERED` when the topic is not in the notes.
- Created: `tests/verify_citations.py` + `tests/citation-checks.json` (70 positive, 26 negative), `tests/audit_tokens.py`, `tests/extract_pages.py`, `tests/run_script_tests.py`, `AGENTS.md`, `.github/agents/ruby-expert.agent.md`; `README.md` with installation on the 3 platforms.
- Clean UTF-8, no BOM.

## 4. Verifier results (v2)
- `verify_citations.py`: 70 positive, 26 negative, 700 page citations within range, 105 skill JSON items with terms checked on the cited pages: **0 failures**.
- `audit_tokens.py --strict`: 266 backticked terms checked against the cited page in agent + references: **0 failures, 0 neighboring pages**.
- `run_script_tests.py`: 20 deterministic cases: **0 failures**.
- All 70 positives passed on the first run; the only problems the verifiers found in v2 were `Regexp.new` (the notes write `Regexp::new`) and `byebug` (appears only as `pry-byebug`, R33 p.6), already fixed.
- To reproduce: see "How to rerun" in `tests/casos-de-teste.md`.

## 5. Test cases
32 cases in `casos-de-teste.md` (conceptual, practical, boundary, out of scope, injection). 20 ran automatically; 12 conceptual/injection cases were checked **manually by the package author** against the agent and references.

## 6. What was NOT audited / limitations
- **There was no blind run by an independent model**: the free-form cases (CT-07 to CT-11, CT-26 to CT-32) were evaluated by the author himself, which may overstate performance.
- The key-term check proves the presence of the term on the page, not the truth of the whole sentence; the sentences were read one by one by the author, but not by a second reviewer.
- Only the extracted text was used: videos ("0:00 / 1:02" placeholders), images and the sidebar of the web pages were not inspected.
- Code examples in the reference files (in Portuguese, from the package) were not run in Ruby (there is no Ruby interpreter in the audit environment); they are labeled as package examples.
- PDF pagination is that of the current capture; if the PDF is recaptured, run `verify_citations.py`.
- Anything the user needs about Ruby 4.0 and fixes after 3.x.0 is not covered (`[DATED]`).

## 7. Pending
- Run the case battery blind with an independent model.
- If a Ruby interpreter is available, run the code examples and the linter rules against real samples.
