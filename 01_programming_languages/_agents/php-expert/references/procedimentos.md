# Procedures (step by step)

Only steps that the PRW offers are included (with PDF page). Useful variations outside the PDF are marked `[extrapolation]`.

## P1. Start a project with Composer
1. Install Composer following the official instructions (it verifies the installer) and, if you want it global, move `composer.phar` to a directory on the PATH `[from source] (PRW p.15)`.
2. `composer init` (wizard) or `composer require vendor/package` (creates `composer.json` if missing) `[from source] (PRW p.16)`.
3. `composer install` to download into `vendor/` `[from source] (PRW p.16)`.
4. In the main file: `require 'vendor/autoload.php';` `[from source] (PRW p.16)`.
5. Version `composer.lock`; on deploy use `composer install`, not `update` `[from source] (PRW p.16)`.
6. `[extrapolation]`: to autoload your own code, declare `autoload` → `psr-4` with the root namespace and the folder; run `composer dump-autoload`. The PDF recommends PSR-4 (p.12) without explaining the mapping.

## P2. Safe query with PDO
1. Connect: `new PDO('mysql:host=...;dbname=...;charset=utf8mb4', user, pass, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, ...])` `[from source] (PRW p.24)`.
2. Filter the input (`filter_input` in the book's example, p.44; `filter_var`, p.59) `[from source] (PRW p.44, 59)`.
3. `prepare()` with named placeholders, `bindParam()` with type, `execute()` `[from source] (PRW p.44)`.
4. Escape on output (HTML) `[from source] (PRW p.25)`.
5. `[extrapolation]`: `execute([':id' => $id])` is equivalent to `bindParam` for the common case.

## P3. Store and verify a password
1. `password_hash($password, PASSWORD_DEFAULT)` and store the whole result (salt and cost are already in it; no salt column) `[from source] (PRW p.58)`.
2. At login, `password_verify($typed, $storedHash)` `[from source] (PRW p.58)`.
3. Remember that the book's list of algorithms is "as of June 2018" `[DATED]` (PRW p.57-58).
4. `[extrapolation]`: `password_needs_rehash()` after a successful login; password length limits; rate-limit attempts.

## P4. Configure error reporting
1. Development: `display_errors = On`, `display_startup_errors = On`, `error_reporting = -1`, `log_errors = On` `[from source] (PRW p.61)`.
2. Production: `display_errors = Off`, `display_startup_errors = Off`, `error_reporting = E_ALL`, `log_errors = On` `[from source] (PRW p.62)`.
3. `[extrapolation]`: `php --ini` and `phpinfo()` show which `php.ini` is active (the book cites `phpinfo()` for OPcache, p.72).

## P5. End-to-end UTF-8 support
1. `mb_internal_encoding('UTF-8')` at the top and `mb_http_output('UTF-8')` `[from source] (PRW p.22-24)`.
2. `mb_*` functions for Unicode strings; `symfony/polyfill-mbstring` if `mbstring` may be missing `[from source] (PRW p.22-23)`.
3. Database/tables in `utf8mb4` and `charset=utf8mb4` in the DSN `[from source] (PRW p.23)`.
4. Header `Content-Type: text/html; charset=UTF-8` and `<meta charset="UTF-8">` `[from source] (PRW p.23, 25)`.

## P6. Test with PHPUnit (what the PDF lets you state)
1. Choose PHPUnit ("de facto" framework) `[from source] (PRW p.63)`.
2. One test per behavior: an invalid argument fails, a valid argument works `[from source] (PRW p.63)`.
3. Use DI and mocks/stubs to isolate dependencies `[from source] (PRW p.63)`.
4. `[extrapolation]`: install with `composer require --dev phpunit/phpunit`, extend `TestCase`, use `assertSame`/`expectException`. The PDF only shows `composer global require phpunit/phpunit` (p.17).

## P7. Run the application locally
1. `php -S localhost:8000` in the web root `[from source] (PRW p.4)`.
2. If you develop on Windows and deploy on Linux, use a VM/WSL/container `[from source] (PRW p.6, 70)`.
3. Quick Docker: `docker run -d --name my-php-webserver -p 8080:80 -v /path:/var/www/html/ php:apache` `[from source] (PRW p.71)`.

## P8. Enable the opcode cache
1. Since PHP 5.5 the Zend OPcache is built in; check `opcache.enable` and `phpinfo()` `[from source] (PRW p.72)`.
2. `[extrapolation]`: parameters such as `opcache.memory_consumption` and `validate_timestamps` depend on load and on the deploy process; see the documentation.
