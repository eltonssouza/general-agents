# Composer, Packagist and PEAR (PRW p.15-19)

## 1. Overview
- PHP projects use many libraries (dependencies); managing them used to be hard and there was also the worry about autoloaders, "this is no longer a problem" `[from source] (PRW p.15)`.
- Today there are two systems: **Composer** (the most popular) and **PEAR** (for a long time the main one; worth knowing its history because references are still found) `[from source] (PRW p.15)`.

## 2. Composer and Packagist
- Composer is "the recommended dependency manager"; you list dependencies in `composer.json` and Composer downloads and sets up the autoload; analogous to NPM (node) and Bundler (Ruby) `[from source] (PRW p.15)`.
- **Packagist** is the official repository of Composer-compatible libraries `[from source] (PRW p.15)`.
- Installation: follow the official instructions (it verifies the installer was not corrupted/tampered with); generates `composer.phar`; the book recommends a global install, e.g. `mv composer.phar /usr/local/bin/composer`, and `php composer.phar` for the local install `[from source] (PRW p.15)`. On Windows, `ComposerSetup` does the global install and adjusts `$PATH` `[from source] (PRW p.16)`.
- Defining dependencies: `composer require` adds the dependency (and creates `composer.json` if missing); book example `composer require twig/twig:^2.0` (the example's version is old `[DATED]`); `composer init` guides the creation of the file `[from source] (PRW p.16)`.
- `composer install` downloads into the `vendor/` directory, also in downloaded projects that already have `composer.json` `[from source] (PRW p.16)`.
- Autoload: add `require 'vendor/autoload.php';` to the main PHP file; classes are loaded on demand `[from source] (PRW p.16)`.

## 3. `composer.lock` and updating
- `composer.lock` stores the exact version of each package downloaded on the first `composer install`; if you share the project, **include `composer.lock`** so others get the same versions `[from source] (PRW p.16)`.
- To update: `composer update`. **Do not use `composer update` when deploying, only `composer install`**, otherwise different versions may appear in production `[from source] (PRW p.16)`.
- Flexible constraints: `~1.8` means "newer than 1.8.0, but lower than 2.0.x-dev"; the wildcard `1.8.*` also works `[from source] (PRW p.17)`.
- New-version notifications: the libraries.io service; security check: *Local PHP Security Checker*, which examines `composer.lock` `[from source] (PRW p.17)`.
- Globals: prefix with `global`, e.g. `composer global require phpunit/phpunit`; creates `~/.composer` (`[DATED]`: in current installations the path may differ) and you must put `~/.composer/vendor/bin` in `$PATH` `[from source] (PRW p.17)`.
- The book does **not** mention `--no-dev`, `--optimize-autoloader`, `require-dev`, `autoload-dev`, `composer validate` or the rule "lock only in applications, not in libraries". Labeled `[extrapolation]` if needed.

## 4. PSR-4 in `composer.json`
- The book recommends PSR-4 for autoloading new code (PRW p.12). The only example of an `autoload` block with `psr-4` in the PDF appears in the PEAR-via-Composer trick `[from source] (PRW p.19)`. The namespace→folder mapping rules are **not** explained in the PDF. `[extrapolation]`: a namespace prefix points to a base folder, and the rest of the class name becomes subfolders and `.php`.

## 5. PEAR
- A "veteran" manager that some developers like; requires the package to have its own structure and be prepared for PEAR; **installs globally** (one package serves all projects on the server), good if everyone uses the same version, problematic if there are version conflicts between projects `[from source] (PRW p.17)`.
- Installation via `.phar` or the distribution's manager (`php-pear` package on Debian/Ubuntu); `pear install foo`; packages from other channels require discovering the channel `[from source] (PRW p.18)`.
- With Composer: PEAR repositories are **no longer supported directly by Composer 2**, so the book shows manually adding a `repositories` entry of type `package` (example `pear2/pear2-http-request`) `[from source] (PRW p.18-19)`.
- Judgment: the book does **not declare PEAR extinct/obsolete**; it describes it as a veteran option with trade-offs. Saying "PEAR is obsolete" is a weak `[inference]`; as `[extrapolation]`, the ecosystem has mostly migrated to Composer.
