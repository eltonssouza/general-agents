# Databases and templates (PRW p.42-51)

Pages = PDF.

## 1. Access options and the `mysql` extension
- Up to PHP 5.1.0 the recommendation was native drivers (`mysqli`, `pgsql`, `mssql`); they work well with a single database, but with several you have to learn a new API for each `[from source] (PRW p.42)`.
- The `mysql` extension is "incredibly old", was superseded by **`mysqli`** and **PDO**, development stopped, and it was **officially removed in PHP 7.0** `[from source] (PRW p.42)`.
- How to find usage: search the editor for `mysql_*` (`mysql_connect()`, `mysql_query()`) `[from source] (PRW p.42)`.
- Migrate on your own, without a last-minute rush; **beware of guides that suggest replacing `mysql_*` with `mysqli_*` by search-and-replace**: it is a crude simplification and loses advantages such as *parameter binding* `[from source] (PRW p.42-43)`.
- `[DATED]`/`[extrapolation]`: today any supported PHP is already above 7.0; the practical point is that code with `mysql_*` does not run.

## 2. PDO
- PDO is a **connection** abstraction library, built in since PHP 5.1.0, with a common interface for several databases (MySQL and SQLite examples almost identical) `[from source] (PRW p.43)`.
- **PDO does not translate your SQL or emulate missing features**; it serves to connect to several databases with the same API `[from source] (PRW p.43)`.
- Security: with *statements* and **bound parameters**, PDO lets you inject external input (e.g. IDs) into queries without worrying about SQL Injection `[from source] (PRW p.43)`.
- The book's wrong code: `$pdo->query("SELECT name FROM users WHERE id = " . $_GET['id'])` ("NO!"); with `id=1;DELETE FROM users` all users are deleted `[from source] (PRW p.43-44)`.
- Right code: `$pdo->prepare('SELECT name FROM users WHERE id = :id')`, `bindParam(':id', $id, PDO::PARAM_INT)`, `execute()`; the book filters the data first with `filter_input(INPUT_GET, 'id', FILTER_SANITIZE_NUMBER_INT)` `[from source] (PRW p.44)`.
- On writes (`INSERT`/`UPDATE`) keep **filtering first** and sanitizing for other layers: PDO only sanitizes for SQL, **not for the application** `[from source] (PRW p.44)`.
- Connections: they use resources; PDO closes on object destruction (all references `NULL`), otherwise PHP closes at the end of the script, except persistent connections `[from source] (PRW p.44)`.
- Connection example with the book's options: `PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION` and `PDO::ATTR_PERSISTENT => false` `[from source] (PRW p.24)`.
- The book does **not** have `ATTR_EMULATE_PREPARES`, `FETCH_ASSOC` as a default, or an explanation of "execution plan". That is `[extrapolation]`.
- Overstatement to avoid: saying prepared statements make injection "technically impossible". The book states that bound parameters prevent SQL injection in this case, and keeps the rule of filtering input (p.44).

## 3. Separate data access from presentation
- Beginners mix query and HTML (`foreach ($db->query(...)) { echo "<li>..." }`); the book calls it bad practice: hard to debug, test and read `[from source] (PRW p.44-45)`.
- Minimal step: a `getAllFoos($db)` function; in separate files there is already a "clean separation"; a class with the method is a "Model" and a presentation `.php` is a "View", almost MVC `[from source] (PRW p.45)`. Example with `FooModel` receiving `PDO` via property promotion `[from source] (PRW p.46)`.
- Mixing too much presentation and database is a real problem for unit tests `[from source] (PRW p.46)`.

## 4. Abstraction layers
- Many frameworks have a layer that can sit on top of PDO and **emulates** features of one database that are missing in another, giving database abstraction (not just connection); cost: a bit of overhead, paid off if the app needs to run on MySQL, PostgreSQL and SQLite `[from source] (PRW p.46)`.
- Installable in any app (PSR-0/PSR-4): Atlas, Aura SQL, Doctrine2 DBAL, Medoo, Propel, laminas-db `[from source] (PRW p.46-47)`.
- The book does **not** compare Data Mapper and Active Record (v1 attributed this to the book).

## 5. Templates
- They separate controller/domain logic from presentation; "views" are part of M**V**C `[from source] (PRW p.47)`.
- Benefits: clear separation, each template only displays (does not fetch data or persist), useful in teams (back-end versus designers), organization in a `views` folder, reuse via partials (header/footer) and, **depending on the library**, automatic escaping of user content and *sandboxing* with whitelisted variables/functions `[from source] (PRW p.47)`.
- **Plain PHP**: PHP is itself a template language; no new syntax, editors already help, tends to be very fast (no compilation); libraries such as Plates and Aura.View add inheritance, layouts and extensions; every modern framework has a template system, most use plain PHP by default `[from source] (PRW p.48)`. Plates example with `$this->escape($name)` `[from source] (PRW p.48-49)`.
- **Compiled** (Twig, Brainy, Smarty; Mustache also in other languages): their own template syntax, with automatic escaping, inheritance and simplified control structures; small performance cost, minimal with caching `[from source] (PRW p.49)`. The book's caveat: in **Smarty automatic escaping exists but is NOT on by default** `[from source] (PRW p.49)`.
- Twig examples with `{{ name }}`, `{% include %}` and `{% extends %}` `[from source] (PRW p.49-50)`. List of libraries (Plates, Aura.View, laminas-view native; Twig, Blade, Latte, Mustache, PHPTAL, Smarty compiled) `[from source] (PRW p.50-51)`.
- On XSS in templates: the escape `htmlspecialchars($data, ENT_QUOTES, 'UTF-8')` appears in the UTF-8 example (PRW p.25) and XSS is covered in Data Filtering (PRW p.59). Saying `htmlspecialchars` is "mandatory" or "the only" escape is an exaggeration: the book cites `strip_tags()`, `htmlentities()` and `htmlspecialchars()` (p.59). That Twig/Blade escape by default is `[extrapolation]` (the book only says "depending on the library").
