# Fidelity report: php-expert (audit v1 -> v2)

Date: 2026-10-26. Source: `PHP-PHP-The-Right-Way.pdf` (PRW, 82 pages, site capture "LAST UPDATED: 2026-04-27", PHP 8.5 as stable). Text extracted with PyMuPDF, markers `=== PAGE N ===` (N = PDF page; the PDF has no printed numbering). A backup of the original package (v1) is kept outside the package.

## 1. Inventory and page convention
- Substantive source: only the PRW. The PDFs `PHP-8.0-Release-Notes` (1 page, browser error screen) and `PHP-8.1` to `PHP-8.4-Release-Notes` (4 pages each, only the php.net side menu) **have no technical content** (verified). So there is no source for "what is new in PHP 8.x".
- v1: cited `(PRW p.N)` without declaring a convention and with ranges that match neither the PDF nor the printed numbering (nonexistent): e.g. `password_hash` at "p.54-56" (real: p.57-58), OPcache at "p.76-78" (real: p.72-73), PDO at "p.39-47" (real: p.43-44). The ranges were all within 1..82, and v1 only validated that.
- v2: PDF convention declared in the agent, INDEX (with a chapter map), README and adapters.

## 2. Audit findings
### 2.1 Automatic (v1)
- 266 citations in `agents/` and `references/` (283 counting scripts/JSON/skills). 184 backtick terms checked against the cited page: **146 failures (79%)** and 17 "neighboring page"; only 21 exact hits.
- Dominant cause: **content the book does not cover**, written as `[from source]` (see 2.3).
### 2.2 Manual (v1): 77 claims read against the cited page
| Class | Count |
|---|---|
| OK | 1 |
| Wrong page (content in the book, page not) | 20 |
| Unsupported claim (absent from the book) | 47 |
| Overstatement (book says less/weaker) | 9 |

It covered the agent prompt, all 10 references and the rules of the 4 scripts, prioritizing "always/never/mandatory", numbers, versions and comparisons.
### 2.3 Relevant examples of what was unsupported (v1)
1. `declare(strict_types=1)`, nullable/union types, arrow functions and closure `use` attributed to "PRW p.15-21": the book has none of them.
2. PSR-1/PSR-12 rules (omit `?>`, StudlyCaps, 4 spaces, braces) as "p.3-14"/"p.11-14": the book only **names** the PSRs (p.9).
3. The `Throwable`/`Error`/`TypeError` hierarchy and `set_error_handler` ("p.48-51"): absent.
4. "`password_hash` uses Argon2id/Bcrypt", "hundreds of billions of MD5/s", `password_needs_rehash`, constant time, CSRF with `hash_equals`/`random_bytes`: absent (the book says it uses BCrypt and is from 2018).
5. `DateTimeImmutable`, Singleton, Factory/Strategy/Decorator, PSR-11, `intl`/`Collator`: absent; the book uses `DateTime`.
6. Invented numbers: "OPcache +200% to 300% throughput", `opcache.*` parameters, "2-year + 1-year cycle and EOL of 8.0".
7. Overstatements: "TDD mandatory" (book: "best practice"), "PEAR extinction/DATED" (book: veteran manager), "SQL injection technically impossible", "Blade/Twig escape by default" (book: "depends on the library"; Smarty does not).
8. Scripts: the rule `\b(md5|sha1)\s*\(\s*.*password|senha` had a precedence error (`senha` alone matched); `strict_types`, `?>` and `DateTime` rules had no origin in the book; `parse_php_stack.py` cited "PRW p.48-50" for `ParseError`/`TypeError` (nonexistent) and printed a corrupted origin on `called in ... on line N and defined in ...`; `composer_audit` required `require-dev` and `php: ^8.2` as "from the book".
9. A `scratch/php/blind/` folder inside the package with "blind answers" written by the package's own author, and a v1 report with "19/19 PASS, 0 hallucinations": no evidentiary value; removed from the package (they stay in the backup).

## 3. What was fixed
- **All 10 references were rewritten** from the PDF text, with verified PDF pages and an explicit `[from source]` / `[inference]` / `[extrapolation]` / `[DATED]` separation; file names preserved. Content the book does not cover was removed or moved to short labeled `[extrapolation]` passages (e.g. `strict_types`, `Throwable`, `DateTimeImmutable`, CSRF).
- `INDEX.md`: page convention, text date (2026-04 / PHP 8.5), "what the book does not cover" section, `[DATED]` list, chapter map, diagnosis of the release-notes PDFs; relative links (v1 had `file:///c:/...`).
- Agent rewritten: epistemic honesty with the labels, `not_in_book`, boundary, `[DATED]` content, anti-injection, when to consult references/scripts (all existing). Frontmatter `description` in single quotes (valid YAML).
- Scripts: `prw_index.json` redone (45 topics with verified pages + 14 `not_in_book` groups); `prw_lookup.py` prints NOT COVERED; `scan_php_smells.py` (15 rules with origin `book`/`inference`/`extrapolation`, `--rules`, `--only-livro`, `--json`, exit codes); `parse_php_stack.py` (labeled origin, origin bug fixed); `audit_composer.py` (7 rules with origin).
- New: `README.md` with installation in the 3 environments, `AGENTS.md` (Codex), `.github/agents/php-expert.agent.md` (Copilot), `tests/verify_citations.py` + `citation-checks.json`, `tests/audit_tokens.py`, `tests/run_script_tests.py`, `tests/casos-de-teste.md` (26 cases).
- `plugin.json` 2.0.0 with a description free of unsupported claims.

## 4. Verifier results on v2
| Verifier | Result |
|---|---|
| `verify_citations.py --text prw.txt` | 96 positive, 26 negative, 296 citations with valid range: **0 failures** |
| `audit_tokens.py --src prw.txt` | 278 citations, 214 backtick terms: **0 failures, 0 neighboring page** |
| `run_script_tests.py --text prw.txt` | 46 tests (4 scripts, fixtures, isolated rules, false positives, injection, index vs. pages): **0 failures** |

During construction the verifiers caught errors in v2 itself (e.g. `filter_var` cited on the wrong page, `FETCH_ASSOC` and "Factory Method", which *exist* in the book and were removed from the negatives), all fixed.
Manual v2 sample: v2 was written directly from the pages read and the 96 positive checks are curated claims (terms and pages checked by machine). In addition, the author re-read about ten higher-risk claims (PSR-0/PSR-4, PDO since 5.1.0, Service Locator, hash/salt, error reporting in production, APCu/memcached, mod_php/prefork) and found no wrong page; a manual v2 sample of 60 items, **independent** of the author, **was not done**.

## 5. Audit coverage and limits
- Audited: agent prompt, 10 references, 4 scripts + fixtures, JSON index, README/AGENTS/Copilot, plugin.json. The book has 82 pages and was read in full.
- Not audited: the content of pages behind the book's external links (the PDF only carries the link labels); technical correctness of extrapolations outside the PRW (labeled, but not checked against php.net).
- There was **no blind run by an independent model**; the 26 cases were walked through by the auditor (the answer key knows the package). It is recommended to run the cases with a model that sees only the prompt and the references.
- The scripts are line-by-line heuristics; "no findings" does not prove safety; the linter does no flow analysis.

## 6. Pending
- Independent blind run of the cases (above).
- Check, once a source exists, the `[DATED]`/`[VERSION-DEPENDENT]` labels for PHP 8.0-8.5 (the collection's release-notes PDFs are empty; replacing them with real captures would allow a "what is new" reference).
