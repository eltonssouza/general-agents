# Cases and anti-patterns (10 cases based on the PRW)

Pages = PDF. Each case separates what the book says from what is `[extrapolation]`.

## 1. SQL built by concatenation
**Problem.** `$pdo->query("SELECT name FROM users WHERE id = " . $_GET['id'])`: the book marks "NO!" and shows `id=1;DELETE FROM users` `[from source] (PRW p.43-44)`.
**Fix.** `prepare()` with the `:id` placeholder, `bindParam(':id', $id, PDO::PARAM_INT)`, `execute()`, filtering the input first with `filter_input` `[from source] (PRW p.44)`. Remember: PDO sanitizes only for SQL, not for the application `[from source] (PRW p.44)`.

## 2. Password with a fast general-purpose hash
**Problem.** Storing a password with a fast general-purpose hash function (the book cites SHA256 as an example of what **not** to use), without an individual salt `[from source] (PRW p.57)`.
**Fix.** A specialized algorithm; in PHP, `password_hash()` + `password_verify()`, which embed salt and cost in the hash `[from source] (PRW p.57-58)`. `[inference]`: `md5()` and `sha1()` fall in the same category (fast general hashes), although the book does not name them. `[extrapolation]`: use `password_needs_rehash` when raising the cost.

## 3. Unescaped output (XSS)
**Problem.** External input printed on the page can execute HTML and JavaScript `[from source] (PRW p.59)`.
**Fix.** Sanitize before output: `strip_tags()` or escape with `htmlentities()`/`htmlspecialchars()`; in the book's example, `htmlspecialchars($dirty, ENT_QUOTES, 'UTF-8')` `[from source] (PRW p.59)` and `(PRW p.25)`. Template engines can escape automatically, depending on the library (Smarty not by default) `[from source] (PRW p.47, 49)`.

## 4. `mysql_*` and "brute-force" migration
**Problem.** `mysql_connect()`/`mysql_query()` (extension removed in PHP 7.0) `[from source] (PRW p.42)`.
**Fix.** Migrate to `mysqli` or PDO; avoid the `mysql_*`→`mysqli_*` search-and-replace, which loses *parameter binding* `[from source] (PRW p.42-43)`.

## 5. Error silenced with `@`
**Problem.** `echo @$foo['bar'];` swallows the error (neither screen nor log) and costs performance `[from source] (PRW p.52-53)`.
**Fix.** Avoid it; `echo $foo['bar'] ?? '';` `[from source] (PRW p.53)`. To debug, a temporary `xdebug.scream` `[from source] (PRW p.53-54)`.

## 6. `display_errors` on in production
**Problem.** Errors on screen and in the log exposing the application structure `[from source] (PRW p.61)`.
**Fix.** Production: `display_errors = Off`, `display_startup_errors = Off`, `error_reporting = E_ALL`, `log_errors = On` `[from source] (PRW p.62)`.

## 7. `composer update` on deploy
**Problem.** Running `composer update` when publishing can bring different versions `[from source] (PRW p.16)`.
**Fix.** Version `composer.lock` and use `composer install` on deploy `[from source] (PRW p.16)`.

## 8. Dependency created with `new` inside the class
**Problem.** `Database` instantiates `MySqlAdapter` in the constructor: rigid dependency, hard to test `[from source] (PRW p.37-38)`.
**Fix.** Inject via constructor, typing by interface (`AdapterInterface`) `[from source] (PRW p.40-41)`. Beware of a container used as a Service Locator `[from source] (PRW p.41)`.

## 9. Query mixed with HTML
**Problem.** `foreach ($db->query(...)) { echo "<li>..." }` on the same page `[from source] (PRW p.44-45)`.
**Fix.** Separate into Model and View (distinct files) `[from source] (PRW p.45-46)`.

## 10. `unserialize()` of user data
**Problem.** It can instantiate objects whose destructors execute `[from source] (PRW p.60)`.
**Fix.** Avoid `unserialize` from an untrusted source; use JSON (`json_decode`/`json_encode`) `[from source] (PRW p.60)`.

## Pitfalls the book does NOT cover (answer only as `[extrapolation]`)
`strict_types`, Singleton, `DateTimeImmutable`, CSRF, `Throwable`, tuned OPcache, PHP-FPM tuning, Share-Nothing. Tell the user: "the PRW does not cover this; it follows general knowledge".
