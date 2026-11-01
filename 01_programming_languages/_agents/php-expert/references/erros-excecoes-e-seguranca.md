# Errors, exceptions and security (PRW p.51-62)

Pages = PDF. Passages "as of June 2018" and those about PHP 5.x are `[DATED]`.

## 1. Errors
- PHP is "exception-light": most of the core keeps processing after problems unless a fatal error occurs; e.g. `echo $foo;` with an undefined variable only produces a Notice in the `php -a` shell; in Python it would raise an exception `[from source] (PRW p.51)`. The book's text gives the message as "Notice: Undefined variable" `[DATED]` (current versions classify it as a Warning; `[extrapolation]`).
- Common severities: `E_ERROR` (fatal, halts), `E_NOTICE` (advisory notice, does not halt), `E_WARNING` (non-fatal); `E_STRICT` is compile-time and suggests changes for interoperability `[from source] (PRW p.52)` (`E_STRICT` is `[DATED]`).
- `error_reporting()` adjusts the level at runtime, e.g. `error_reporting(E_ERROR | E_WARNING)`; showing errors on screen is good in development, hiding and **logging** them is good in production `[from source] (PRW p.52)`.
- **`@` operator** (suppression): silences the expression's error; it has a performance cost, swallows the error (it neither appears nor goes to the log) and a "stock" production PHP system has no way to turn it off; avoid it when there is an alternative, e.g. `$foo['bar'] ?? ''` `[from source] (PRW p.52-53)`. Defensible case cited: `fopen()` of a file deleted between the check and the open `[from source] (PRW p.53)`.
- `xdebug.scream` (ini) disables the effect of `@`; use it as a **temporary** debugging tool, since libraries may not work without the operator `[from source] (PRW p.53-54)`.
- **`ErrorException`** extends `Exception`; it allows turning "errors" into exceptions (Symfony and Laravel practice); in dev those frameworks show a stack trace; Whoops! helps with reporting; throwing errors as exceptions in dev makes them easier to handle `[from source] (PRW p.54)`. The book does **not** show `set_error_handler` (that is `[extrapolation]`: it is the usual mechanism to convert errors into `ErrorException`).

## 2. Exceptions
- Heavily used in other languages (Ruby) but neglected in PHP; PHP is "lax": `file_get_contents()` usually returns `FALSE` and a warning `[from source] (PRW p.54-55)`.
- Older frameworks (e.g. CodeIgniter) return `false` and write to their own log: the problem is having to hunt for the error `[from source] (PRW p.55)`.
- Another problem: classes that throw the error onto the screen and `exit` prevent the developer from handling it; **throw exceptions** so the developer decides `[from source] (PRW p.55)`. Example with `try`/`catch`/`finally` (Fuel\Email) `[from source] (PRW p.55)`.
- **SPL Exceptions**: the generic `Exception` gives little context; creating subclasses (`class ValidationException extends Exception {}`) allows several `catch` blocks; to avoid creating too many exceptions, use those from the SPL, e.g. `BadMethodCallException` in `__call()` `[from source] (PRW p.55-56)`.
- The book does **not** have the `Throwable`/`Error`/`TypeError`/`ParseError` tree. `[extrapolation]`: since PHP 7, engine errors throw `Error` (which implements `Throwable`, as does `Exception`).

## 3. Web security
- Resource recommended by the book: *The 2018 Guide to Building Secure PHP Software* (Paragon Initiative) `[from source] (PRW p.56)`.
- Four major themes: (1) code-data separation (data executed as code becomes SQL Injection, XSS, file inclusion; code printed as data becomes a leak); (2) application logic (authentication/authorization, input validation); (3) environment (PHP versions, third-party libraries, OS); (4) cryptography (weak random numbers, chosen-ciphertext, side-channel) `[from source] (PRW p.56-57)`.
- OWASP is "required reading" for anyone who cares about security; another guide: *Survive The Deep End: PHP Security* (Padraic Brady) `[from source] (PRW p.57)`.

## 4. Password hashing
- Hash passwords **before storing**; hash ≠ encryption: a hash is a one-way, fixed-output, irreversible function; encryption is reversible with the key and "is a poor strategy" for storing passwords `[from source] (PRW p.57)`.
- Each password must have an individual **salt** (random string), which prevents dictionary attacks and *rainbow tables* `[from source] (PRW p.57)`.
- Use a **specialized password-hashing algorithm**, not a fast general-purpose hash function (the book gives SHA256 as an example) `[from source] (PRW p.57)`. The book does **not** name `md5()` or `sha1()`; considering them unsuitable for passwords is a direct `[inference]` from the previous point (they are fast general hashes).
- List "as of June 2018" `[DATED]`: **Argon2** (PHP 7.2+), **Scrypt**, **Bcrypt** (PHP provides it) and **PBKDF2** with HMAC-SHA256/SHA512 `[from source] (PRW p.57-58)`.
- `password_hash()` appeared in **PHP 5.5**; "at the moment it uses BCrypt" (`[DATED]`) and will be updated in the future; `password_compat` gives compatibility for PHP >= 5.3.7 `[from source] (PRW p.58)`. `[extrapolation]`: in current PHP `PASSWORD_DEFAULT` is bcrypt and `PASSWORD_ARGON2ID` exists if PHP was compiled with support; check the documentation.
- `password_hash()` handles the salt; the salt, the algorithm and the "cost" live inside the hash and `password_verify()` extracts them, so **no separate column is needed for the salt** `[from source] (PRW p.58)`. The book's example: `password_hash('secret-password', PASSWORD_DEFAULT)` and `password_verify(...)` `[from source] (PRW p.58)`.
- Not in the book: `password_needs_rehash`, constant-time comparison, "billions of hashes per second", `PASSWORD_ARGON2ID` (v1 claimed all of this as from the book). If you cite them, label `[extrapolation]`.

## 5. Data filtering
- "Never, ever trust" external input: sanitize and validate; `filter_var()` and `filter_input()` sanitize text and validate formats (e.g. email) `[from source] (PRW p.59)`.
- External input includes `$_GET`, `$_POST`, `$_SERVER` values, the HTTP body (`php://input`), uploaded/downloaded files, session, cookies and third-party service data; external data stored and used later is still external `[from source] (PRW p.59)`.
- XSS: one way to prevent it is to sanitize before output, removing tags with `strip_tags()` or escaping with `htmlentities()` or `htmlspecialchars()` `[from source] (PRW p.59)`. External command: `escapeshellarg()`; file path coming from input: remove `/`, `../`, null bytes `[from source] (PRW p.59)`.
- **Sanitization** removes/escapes illegal or unsafe characters (before raw HTML or SQL); with bound parameters PDO sanitizes for SQL; allowing safe HTML is very hard (alternatives: Markdown, BBCode, or a whitelist library such as HTML Purifier) `[from source] (PRW p.59-60)`.
- **`unserialize()`** of untrusted data is dangerous (it instantiates objects whose destructors execute); prefer JSON (`json_decode`/`json_encode`) `[from source] (PRW p.60)`.
- **Validation** ensures the input is what is expected (email, phone, age) `[from source] (PRW p.60)`.
- The book does **not** cover CSRF (tokens, `hash_equals`, `random_bytes`) or `magic_quotes_gpc`. `[extrapolation]` if asked.

## 6. Configuration files
- Keep them out of direct reach and load them through the file system; if they must stay in the document root, name them with a `.php` extension so they are not shown as text; protect them with encryption or permissions; **do not version** configuration with sensitive data (passwords, API tokens) `[from source] (PRW p.60)`.

## 7. `register_globals` `[DATED]`
- Removed in PHP 5.4.0; the warning serves those upgrading legacy systems; it exposed `$_GET['foo']` as `$foo`, possibly overwriting variables; if PHP < 5.4.0, make sure it is off `[from source] (PRW p.60-61)`.

## 8. Error reporting per environment
- Development (`php.ini`): `display_errors = On`, `display_startup_errors = On`, `error_reporting = -1`, `log_errors = On`; `-1` shows every error even with new levels in the future; `E_ALL` too (from PHP 5.4) `[from source] (PRW p.61)`. `E_STRICT` table by version `[DATED]` `[from source] (PRW p.61-62)`.
- **Production**: `display_errors = Off`, `display_startup_errors = Off`, `error_reporting = E_ALL`, `log_errors = On`; errors remain in the web server log but do not appear to the user `[from source] (PRW p.62)`. The book's reason: the log can expose the application structure to the outside world `[from source] (PRW p.61)`.
- Not in the book: `error_log = /var/log/php/error.log` (example path) nor the "Information Disclosure" label.
