# Practices: Date/Time, patterns, UTF-8, i18n, DI and SOLID (PRW p.20-41)

Pages = PDF. Items without a citation are `[extrapolation]` and say so.

## 1. Basics
- The "The Basics" section is just a reminder that basic practices get forgotten through shortcuts and bad habits; the content is in an external link `[from source] (PRW p.20)`.

## 2. Date and time (`DateTime`)
- The book presents the `DateTime` class (read, write, compare, calculate), with `createFromFormat()` to convert a string to an object, `new DateTime` for now and `format()` to go back to a string `[from source] (PRW p.20)`.
- Calculation with `DateInterval` and the `add()`, `sub()` and `diff()` methods; **"don't write code that expects the same number of seconds every day"** (daylight saving time and time zones break this; use date intervals) `[from source] (PRW p.20)`. Example of the `P1M6D` interval and `clone` before adding `[from source] (PRW p.20-21)`.
- Comparison with standard operators (`<`); `DatePeriod` iterates recurring events (e.g. `DatePeriod::EXCLUDE_START_DATE`) `[from source] (PRW p.21)`.
- `Carbon` extends `DateTime` and adds localization and extra ways to add/subtract/format, plus simulating date/time in tests `[from source] (PRW p.21)`.
- The book does **not** mention `DateTimeImmutable` or `DateTimeZone` (and says time zones are out of scope of the introduction, p.20). `[extrapolation]`: `DateTimeImmutable` returns a new instance instead of mutating, which avoids side effects when the object is shared; prefer it in new code. v1 treated this as "from the book".

## 3. Design patterns
- Common patterns make code easier to manage and for others to read; with a framework, many decisions come ready-made `[from source] (PRW p.21)`.
- Without a framework, you must choose patterns suited to the type and size of the application; the book only points to refactoring.guru and designpatternsphp `[from source] (PRW p.22)`.
- The book does **not** describe Singleton, Factory, Strategy or Decorator. `[extrapolation]`: Singleton is commonly criticized for global state and difficulty of testing.

## 4. UTF-8
- Opening: "there is no one-line solution"; PHP **does not support Unicode at a low level**; care is needed in every layer (HTML, SQL, PHP) `[from source] (PRW p.22)`.
- Basic operations (concatenating, assigning) need nothing special; `strpos()` and `strlen()`, however, have `mb_*` counterparts (`mb_strpos()`, `mb_strlen()`) from the **Multibyte String Extension** `[from source] (PRW p.22)`.
- Use `mb_*` whenever you operate on a Unicode string; `substr()` on UTF-8 can produce "half-characters", the right function is `mb_substr()`; not every string function has an `mb_*` version `[from source] (PRW p.22)`.
- Call `mb_internal_encoding()` at the top of every script (or of the global include) and `mb_http_output()` right after if there is output to the browser `[from source] (PRW p.22)`.
- Always pass UTF-8 explicitly when the function accepts the encoding parameter (e.g. `htmlentities()`); since PHP 5.4.0 UTF-8 is the default in `htmlentities()` and `htmlspecialchars()` `[from source] (PRW p.23)`.
- If you are not sure `mbstring` is enabled, consider `symfony/polyfill-mbstring` `[from source] (PRW p.23)`.
- Database: use `utf8mb4` (not `utf8`) in the database, tables, collation and in the PDO DSN ("critically important") `[from source] (PRW p.23)`.
- Browser: `header('Content-Type: text/html; charset=UTF-8')` or, historically, the charset meta tag `[from source] (PRW p.23)`. Complete example with `mb_internal_encoding('UTF-8')`, `mb_http_output('UTF-8')`, PDO with `charset=utf8mb4` and `htmlspecialchars($dirty, ENT_QUOTES, 'UTF-8')` `[from source] (PRW p.23-25)`.
- The book does not have the `strlen("maçã")` example; `[extrapolation]`: in UTF-8 each accented character takes more than one byte, which is why `strlen` counts bytes.

## 4.1 Internationalization and localization (i18n/l10n) with gettext
- Definitions: i18n organizes the code to adapt to languages without refactoring (ideally at the start); l10n is the adaptation of the interface (translations); pluralization varies by language (English 2 forms, Russian/Serbian 3, others up to 6) `[from source] (PRW p.26)`.
- Arrays of strings in templates are discouraged for serious projects (problems such as pluralization) `[from source] (PRW p.26)`. The book adopts **gettext** (from 1995) `[from source] (PRW p.27)`.
- Other libraries listed: `aura/intl`, `php-gettext/Gettext`, `symfony/translation`, `laminas/laminas-i18n`; Laravel and Yii have their own modules `[from source] (PRW p.27)`.
- Files: `PO` (readable), `MO` (binary), `POT` (template, optional); one PO/MO pair per language/region and one POT per domain; domains group translations (e.g. "main") `[from source] (PRW p.28)`.
- Locale code: ISO 639-1 + ISO 3166-1 alpha-2, e.g. `de_AT`, `pt_BR` `[from source] (PRW p.29)`. Structure `locales/<locale>/LC_MESSAGES/*.po|mo` `[from source] (PRW p.29)`.
- Plural forms: e.g. `nplurals=2; plural=(n != 1);` (English) and `plural=(n > 1)` (pt_BR) `[from source] (PRW p.30)`. `msgid` as a real sentence versus a structured key: gettext prefers a real sentence; Symfony prefers keys `[from source] (PRW p.31-32)`.
- Functions `gettext()`, `_()`, `ngettext()`, `dgettext()`; setup with `putenv`, `setlocale`, `bindtextdomain`, `textdomain` `[from source] (PRW p.33-34)`. Poedit tool (the book is based on 1.8, `[DATED]`) `[from source] (PRW p.34)`. `.mo` cache may require a restart under `mod_php` `[from source] (PRW p.36)`.

## 5. Dependency injection (DI)
- Definition: providing a component with its dependencies via **constructor**, **method call** or **property assignment**; "it's that simple" `[from source] (PRW p.37)`.
- Bad example: the `Database` class creates `new MySqlAdapter` in the constructor (rigid dependency, hard to test, tight coupling) `[from source] (PRW p.37-38)`. Refactored: the adapter is injected and uses constructor property promotion `[from source] (PRW p.38)`.
- **Inversion of Control** and **Dependency Inversion Principle** are the "complex problems" that DI solves; MVC frameworks with a super-object/base controller do IoC but only *move* the dependencies `[from source] (PRW p.38-39)`.
- **SOLID** in the book: SRP ("one reason to change"), OCP (open for extension, closed for modification; implement interfaces and type-hint against them), LSP (substitutable subtypes; `FileInterface` example with `embed()`), ISP (smaller, specific interfaces; `steeringWheel()`/`handlebars()` example), DIP (depend on abstractions) `[from source] (PRW p.39-40)`.
- Benefits of DIP: you can *mock* the interface while a colleague finishes the adapter, and switch databases by writing another adapter that implements the interface `[from source] (PRW p.41)`.
- **DI containers** are not the same thing as DI; they can be misused as a *Service Locator* (anti-pattern), which creates a stronger dependency on the container and less transparent code that is harder to test; most modern frameworks have a configurable container `[from source] (PRW p.41)`.
- The book does **not** cite PSR-11 or PHP-DI. `[extrapolation]`: PSR-11 defines the container interface.
