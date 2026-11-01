# Fundamentals, version, installation, directories and style (PRW p.4-10)

Pages = PDF (see `INDEX.md`). Labels: `[from source]` read on the page; `[extrapolation]` outside the PDF; `[DATED]` old text.

## 1. PHP version
- The book says to start with the current stable version, **PHP 8.5** in this capture; it says 8.x brings many new features over 7.x and 5.x and that the engine was largely rewritten `[from source] (PRW p.4)`.
- It says **PHP 7.4 is already End of Life** and that upgrading is easy because there are few compatibility breaks between 8.0 and 8.5 `[from source] (PRW p.4)`.
- To find out in which version a function appeared, consult the documentation on php.net `[from source] (PRW p.4)`.
- The text does **not** give the support cycle (active/security support time) or declare EOL for 8.0-8.3; it only cites 7.4. `[extrapolation]`: check the table of supported versions on php.net before stating any EOL.
- Shared hosting: the book asks you to check that the host offers the latest PHP version `[from source] (PRW p.67)`.

## 2. Built-in server
- With PHP 5.4 or higher you can learn without installing a full web server; the book's command is `php -S localhost:8000`, run in the project's web root `[from source] (PRW p.4)`. In the Windows section it repeats: for learning and developing locally the built-in server (PHP 5.4+) needs no configuration `[from source] (PRW p.6)`.
- `[extrapolation]`: the `-t public/` option (setting the document root) and the fact that the built-in server is not for production are in the PHP documentation, **not** in this PDF.

## 3. Installation by platform (summary)
- **macOS**: from macOS 12 PHP does not come pre-installed; Homebrew (`brew install php`, formulas 8.1 to 8.5), switch versions with `brew unlink`/`brew link --overwrite php@8.2`, MacPorts, phpbrew, Liip installer, compilation, all-in-one installers (MAMP, XAMPP) `[from source] (PRW p.4-6)`.
- **Windows**: binaries from php.net, put the PHP folder in the `PATH`; all-in-one (EasyPHP, OpenServer, WampServer) differs from production; if you develop on Windows and publish on Linux, consider a VM or WSL `[from source] (PRW p.6)`.
- **Linux**: distribution packages tend to lag behind stable; for Ubuntu, Ondřej Surý's PPA (`ppa:ondrej/php`); for Debian, his "bikeshed" repository; for RPM (CentOS, Fedora, RHEL), the Remi repository; or containers/compiling from source `[from source] (PRW p.6-8)`.
- `[DATED]`: the MacPorts list (p.5) goes up to `php84` and the Liip installer covers only 5.3 to 7.3.

## 4. Directory structure
- Where to put files: "where the DocumentRoot is" is a good start, though incomplete; for security, **configuration files must not be accessible to visitors**: public scripts go in a public directory, configuration and private data outside it `[from source] (PRW p.8)`.
- The book cites Paul M. Jones's *Standard PHP Package Skeleton*: the DocumentRoot points to `public/`, tests in `tests/`, libraries installed by Composer in `vendor/` `[from source] (PRW p.8)`.
- `[extrapolation]`: `src/`, `config/`, `templates/`, the `public/index.php` front controller and `.env` are common conventions, **not** in the PDF (v1 presented them as from the book).

## 5. Style guide (PHP-FIG)
- Why: the community combines many libraries and frameworks, so it is worth adhering to a common style `[from source] (PRW p.9)`.
- The FIG approved recommendations; those concerning code style are **PSR-1, PSR-12, PSR-4 and PER Coding Style**; projects such as Drupal, Symfony, Laravel, CakePHP, phpBB and the AWS SDK adopt them; you can use them or keep your own style `[from source] (PRW p.9)`.
- You can follow "any combination of PSRs" or the PEAR or Zend standards; the goal is for other developers to read the code easily `[from source] (PRW p.9)`.
- **The book does not describe the content of the PSRs** (tags, names, indentation, braces): it only points to links. `[extrapolation]`: PSR-1 requires `<?php`/`<?=` tags, classes in StudlyCaps, methods in camelCase; PSR-12/PER detail 4-space indentation and braces. See php-fig.org.
- Tools: `PHP_CodeSniffer` checks against any of these recommendations; the `PHP Coding Standards Fixer` and the `PHP Code Beautifier and Fixer` (included in CodeSniffer) fix the layout `[from source] (PRW p.9)`.
- Book commands: `phpcs -sw --standard=PSR1 file.php`; `phpcbf -w --standard=PSR1 file.php`; `php-cs-fixer fix -v --rules=@PSR1 file.php` `[from source] (PRW p.10)`.
- Book suggestion: run `phpcs` in a pre-commit hook with `--filter=GitStaged`, so code with violations does not enter the repository `[from source] (PRW p.10)`.
- Language: English preferred for symbol names and code infrastructure; comments in any language readable by everyone involved `[from source] (PRW p.10)`.
- Suggested further reading: *Clean Code PHP* `[from source] (PRW p.10)`.
