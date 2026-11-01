# INDEX of the `php-expert` references

Single substantive source: **PRW** = *PHP: The Right Way* (Josh Lockhart, Phil Sturgeon and contributors; license CC BY-NC-SA 3.0), file `PHP-PHP-The-Right-Way.pdf` (82 pages, capture of the `phptherightway.com` site with "LAST UPDATED: 2026-04-27", p.1).

## Page convention (mandatory)
- `(PRW p.N)` = **PDF page** (the same numbering as the `=== PAGE N ===` markers of the extracted text). The PDF is a site capture and **has no printed numbering**; chapters appear as "CHAPTER N" in the footer of the page where they end/begin. Pages 1-2 are the table of contents.
- When citing to the user, say at least once "PRW p.N (PDF page)".
- The v1 of this package cited ranges that match no numbering of the PDF (e.g. `password_hash` at "p.54-56"; the text is on p.57-58). All pages were redone in v2.

## Date and PHP version carried by the text (important)
- The capture is from **April 2026** and recommends **PHP 8.5** as the current stable version; it says PHP 7.4 is already End of Life; it lists Homebrew with 8.1 to 8.5 (PRW p.1, 4). The book, however, **does not teach PHP 8.x features** (union types, `match`, enums, attributes, `readonly`...). Isolated 8.x code exceptions: constructor property promotion (p.38, 41, 46) and `??` (p.53). Statements of the kind "in PHP 8.x feature X exists" can only be `[extrapolation]`.
- Several passages are **old** and count as `[DATED]`: "(as of June 2018)" for password algorithms (p.57-58), `password_hash` "uses BCrypt" (p.58), notes on PHP 5.x, Xdebug with `xdebug.remote_host`/`remote_port` and `XDEBUG_SESSION_START` (p.14), PoEdit 1.8 (p.34), Travis CI (p.70), `~/.composer` (p.17), `E_STRICT` (p.52, 61), `Notice: Undefined index` (p.53).

## Other PHP PDFs in the folder (no technical content)
- `PHP-8.0-Release-Notes.pdf` (1 page): browser error screen (ERR_TIMED_OUT), no content.
- `PHP-8.1` to `PHP-8.4-Release-Notes.pdf` (4 pages each): only the php.net side menu ("PHP 8.6.0 Beta 1 is available for testing"), no feature descriptions. Verified on 2026-10-26.
- Therefore, **the package has no source for "what's new in PHP 8.0-8.4"**: answer `[extrapolation]` or "the collection does not cover it".

## Page map (PDF)
| Chapter | Topic | PDF |
|---|---|---|
| 1 Welcome | purpose, translations | 2-3 |
| 2 Getting Started | stable version 8.5, built-in server, macOS/Windows/Linux, directory structure | 4-8 |
| 3 Code Style Guide | PSRs, phpcs, php-cs-fixer | 9-10 |
| 4 Language Highlights | paradigms, namespaces, SPL, CLI, Xdebug | 10-14 |
| 5 Dependency Management | Composer, Packagist, PEAR | 15-19 |
| 6 Coding Practices | basics, Date/Time, patterns, UTF-8, i18n/l10n (gettext) | 20-37 |
| 7 Dependency Injection | DI, SOLID, containers | 37-41 |
| 8 Databases | mysql extension, PDO, separation, abstraction | 42-46 |
| 9 Templating | benefits, plain PHP, compiled | 47-51 |
| 10 Errors and Exceptions | severity, `@`, ErrorException, exceptions, SPL | 51-56 |
| 11 Security | OWASP, passwords, filtering, config, register_globals, error reporting | 56-62 |
| 12 Testing | TDD, unit/integration/functional, BDD, tools | 62-65 |
| 13 Servers and Deployment | PaaS, nginx/FPM, Apache, shared, deploy, provisioning, CI | 65-70 |
| 14 Virtualization | Vagrant, Docker | 70-72 |
| 15 Caching | opcode cache, object cache (APCu, memcached) | 72-74 |
| 16 Documenting your Code | PHPDoc | 74-76 |
| 17-18 Resources, Community | frameworks, components, books, community | 76-82 |

## Thematic documents (`references/`)
| File | Content | PDF |
|---|---|---|
| [fundamentos-e-estilo.md](fundamentos-e-estilo.md) | version, built-in server, installation, directories, PSRs, style tools | 4-10 |
| [linguagem-moderna-e-oop.md](linguagem-moderna-e-oop.md) | paradigms, namespaces, SPL, CLI, Xdebug | 10-14 |
| [gerenciamento-de-dependencias.md](gerenciamento-de-dependencias.md) | Composer, composer.json/lock, PEAR | 15-19 |
| [praticas-arquiteturais-e-dados.md](praticas-arquiteturais-e-dados.md) | Date/Time, patterns, UTF-8, i18n, DI and SOLID | 20-41 |
| [bancos-de-dados-e-templates.md](bancos-de-dados-e-templates.md) | mysql, PDO, separation, abstraction, templates | 42-51 |
| [erros-excecoes-e-seguranca.md](erros-excecoes-e-seguranca.md) | errors, exceptions, security, passwords, filtering, error reporting | 51-62 |
| [testes-e-infraestrutura.md](testes-e-infraestrutura.md) | testing, servers, deploy, Docker, cache, PHPDoc | 62-76 |
| [casos-e-antipadroes.md](casos-e-antipadroes.md) | 10 practical cases with page | various |
| [procedimentos.md](procedimentos.md) | step by step with what the book offers + labeled extensions | various |
| [glossario.md](glossario.md) | terms from the book | various |

## What the book does NOT cover (not_in_book; only `[extrapolation]`)
`declare(strict_types=1)`, scalar/return/nullable/union types, arrow functions and the `use` clause of closures, `match`, enums, attributes, `readonly`, fibers; PSR-1/PSR-12 rules (omitted `?>` tag, StudlyCaps, 4 spaces, braces) — the book only **names** the PSRs (p.9); the `Throwable`/`Error` hierarchy; `DateTimeImmutable` and `DateTimeZone`; the Singleton, Factory, Strategy, Decorator patterns (links only, p.22); PSR-11; `intl`/`Collator`; `set_error_handler`; CSRF; `hash_equals`, `random_bytes`, `password_needs_rehash`, Argon2**id**; `assertSame`/`createMock`; PHPStan/Psalm; PHP-FPM tuning, Share-Nothing, `opcache.*` parameters beyond `opcache.enable`; detailed Docker Compose; Laravel/Symfony in depth; async (Swoole, Fibers); what's new in PHP 8.0-8.4.

## Epistemic labels
`[from source]` (read on the cited page) · `[inference]` (direct deduction from the text) · `[extrapolation]` (useful external knowledge, not in the PDF) · `[DATED]` (old text, 2018 or PHP 5.x) · `[VERSION-DEPENDENT]` · `[HOST]`.

## Verification
`python -I tests/verify_citations.py --text <prw.txt>` (positive/negative checks), `python -I tests/audit_tokens.py --src <prw.txt>` (backticked terms vs. the cited page), `python -I tests/run_script_tests.py`. The `prw.txt` text is obtained with PyMuPDF (markers `=== PAGE N ===`; see README).
