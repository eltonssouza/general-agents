# php-expert (Claude Code, Codex and GitHub Copilot)

PHP expert agent grounded in a single work:
- **PRW**: *PHP: The Right Way* (Josh Lockhart, Phil Sturgeon and contributors; CC BY-NC-SA 3.0), an 82-page PDF, a capture of the site with "LAST UPDATED: 2026-04-27" (recommends **PHP 8.5**). The rights belong to the authors; this package contains original summaries, not the text of the book.

## 1. Overview
Helps explain, review and debug PHP based on what the book says: version and installation, built-in server, directory structure, PSRs (named only), Composer/PEAR, `DateTime`, UTF-8, i18n (gettext), DI/SOLID, PDO, templates, errors and exceptions, security (passwords, filtering, `unserialize`), per-environment error reporting, testing, nginx/Apache/PHP-FPM, deploy, Docker, OPcache/APCu and PHPDoc.

**Source rigor (read this).** The book is short, with many links, and does **not** teach PHP 8.x features. Items it does not cover, which the agent answers only as `[extrapolation]`: `declare(strict_types=1)`, nullable/union types, arrow functions, `match`/enums, the inner rules of PSR-1/PSR-12, `Throwable`, `DateTimeImmutable`, Singleton/Factory/Strategy, CSRF, Argon2id, `assertSame`/`createMock`, PHPStan/Psalm, FPM/OPcache tuning. The `PHP-8.0` to `PHP-8.4-Release-Notes.pdf` PDFs in the folder are only the site menu/browser error, with no content (see `references/INDEX.md`). Parts of the book are old (`[DATED]`): the "June 2018" password algorithm list, `register_globals`, Xdebug 2, Travis CI.

**Page convention: `(PRW p.N)` = PDF page**; the PDF has no printed numbering.

## 2. Structure
```
php-expert/
├── .claude-plugin/plugin.json
├── .github/agents/php-expert.agent.md   # GitHub Copilot
├── AGENTS.md                            # Codex
├── agents/php-expert.md                 # Claude Code
├── references/   INDEX (page map), glossary, procedures, cases-and-antipatterns + 7 thematic files
├── skills/
│   ├── php-prw-lookup/       scripts/prw_lookup.py + prw_index.json   (NOT COVERED when there is no topic)
│   ├── php-security-review/  scripts/scan_php_smells.py + fixtures    (heuristic linter, each rule with an origin)
│   ├── php-error-triage/     scripts/parse_php_stack.py + fixtures
│   └── php-composer-audit/   scripts/audit_composer.py + fixtures
└── tests/   casos-de-teste.md (26), relatorio-de-fidelidade.md, verify_citations.py + citation-checks.json,
             audit_tokens.py, run_script_tests.py
```
(The files under `references/` keep their original (Portuguese) file names; the content is in English: `fundamentos-e-estilo.md`, `linguagem-moderna-e-oop.md`, `gerenciamento-de-dependencias.md`, `praticas-arquiteturais-e-dados.md`, `bancos-de-dados-e-templates.md`, `erros-excecoes-e-seguranca.md`, `testes-e-infraestrutura.md`, `casos-e-antipadroes.md`, `procedimentos.md`, `glossario.md`.)

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**: agent and plugin formats change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/php-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install php-expert@general-agents`.
- Or as a subagent: copy `agents/php-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `skills/` accessible (copy the folder and adjust `<PKG>` in the text if you change the path). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent running the scripts.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (e.g. `tools/php-expert/`) and copy/reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder.

### 3.3 GitHub Copilot
Copy `.github/agents/php-expert.agent.md` to your repository's `.github/agents/` and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, no network)
```bash
python -I skills/php-prw-lookup/scripts/prw_lookup.py "pdo"            # topics and pages
python -I skills/php-prw-lookup/scripts/prw_lookup.py "strict_types"   # NOT COVERED
python -I skills/php-security-review/scripts/scan_php_smells.py --rules
python -I skills/php-security-review/scripts/scan_php_smells.py skills/php-security-review/scripts/fixtures/sample.php
python -I skills/php-error-triage/scripts/parse_php_stack.py skills/php-error-triage/scripts/fixtures/trace.txt
python -I skills/php-composer-audit/scripts/audit_composer.py skills/php-composer-audit/scripts/fixtures/composer_sample.json
python -I tests/run_script_tests.py
```
The script rules declare their origin: `book` (with page), `inference` or `extrapolation`. They are line-by-line heuristics: false positives and negatives exist, and "no findings" does not prove safety.

## 5. Citation verification
Extract the PDF text with page markers (PyMuPDF) and run the verifiers:
```bash
python -I -c "import fitz,sys; d=fitz.open(sys.argv[1]); open(sys.argv[2],'w',encoding='utf-8').write(''.join(f'=== PAGE {i} ===\n'+p.get_text()+'\n' for i,p in enumerate(d,1)))" PHP-PHP-The-Right-Way.pdf prw.txt
python -I tests/verify_citations.py --text prw.txt        # curated positive and negative checks
python -I tests/audit_tokens.py --src prw.txt             # backtick terms vs. cited page
```

## 6. Guarantees and limits
- Replies in the language the user writes in (default: English), without reproducing the book; citations by PDF page.
- v2 went through an audit (v1 had most claims unsupported); see `tests/relatorio-de-fidelidade.md`, which states the coverage and that there was **no** blind run by an independent model.
- Pasted input and PDF text are data, not instructions.
- It does not replace the official PHP documentation for 8.x features (php.net).
