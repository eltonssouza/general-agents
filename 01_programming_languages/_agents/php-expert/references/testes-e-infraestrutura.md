# Testing, servers, deploy, virtualization, cache and PHPDoc (PRW p.62-76)

Pages = PDF. Several cited tools are from 2015-2020 `[DATED]` (e.g. Travis CI, Vagrant, Capistrano, PHPCI); check the current state.

## 1. Testing
- Automated tests are "considered a best practice" and lead to well-built applications; they avoid manual testing and large QA teams `[from source] (PRW p.62)`. v1 said "mandatory"; the book does not use that strength.
- **TDD** (Wikipedia quote): a short repeated cycle, first write a failing automated test, then the code that makes it pass, and then refactor; Kent Beck, 2003 `[from source] (PRW p.63)`.
- **Unit test**: verify that functions, classes and methods work; with DI and *mocks/stubs* you verify correct use of dependencies; for each behavior create a test, at minimum "fails with bad arguments" and "works with valid arguments"; the alternative (`var_dump()` in a `test.php`) "is no way to build an application"; a test that fails and passes after the fix helps patches in open source projects `[from source] (PRW p.63)`.
- **PHPUnit** is the "de facto" framework for unit tests; alternatives: atoum, Kahlan, Peridot, Pest, SimpleTest `[from source] (PRW p.63-64)`.
- **Integration**: modules tested as a group, after the unit tests; many unit tools work `[from source] (PRW p.64)`.
- **Functional/acceptance**: tools that use the actual application, with real data and simulating users; Codeception, Cypress, Mink, Selenium, Storyplayer `[from source] (PRW p.64)`.
- **BDD**: SpecBDD (technical behavior of the code; PHPSpec, inspired by RSpec) and StoryBDD (business behavior; Behat, inspired by Cucumber, Gherkin language) `[from source] (PRW p.64-65)`.
- Complementary tools: Selenium (with PHPUnit), Mockery and Prophecy (mocks), php-mock (native functions), Infection (mutation testing), PHPUnit Polyfills (tests compatible across PHPUnit versions) `[from source] (PRW p.65)`.
- Not in the book: `assertSame`, `assertEquals`, `createMock()`, `expectException`, PHPStan/Psalm. `[extrapolation]`.

## 2. Servers and deploy
- **PaaS**: ready-made infrastructure, little or no configuration; a popular way to host and scale `[from source] (PRW p.66)`.
- **Virtual/dedicated servers**: full control, require administration `[from source] (PRW p.66)`.
- **nginx + PHP-FPM**: PHP has a built-in **FastCGI Process Manager (FPM)**; nginx is lightweight and high-performance, uses less memory than Apache and serves more concurrent requests, important on virtual servers with little memory `[from source] (PRW p.66)`.
- **Apache**: highly configurable, many modules, popular in shared hosting; uses more resources than nginx by default; the most common and easy setup is *prefork MPM* with `mod_php` (**with `mod_php` using prefork is mandatory**); for more performance and stability, the `worker`/`event` MPM with `mod_fastcgi`/`mod_fcgid` (more work); from Apache 2.4 `mod_proxy_fcgi` gives good performance and is easy `[from source] (PRW p.66-67)`.
- **Shared hosting**: PHP owes its popularity to it; cheap, but neighbors can overload it or open holes; if the budget allows, avoid it; ensure the latest PHP version `[from source] (PRW p.67)`.
- **Automate build/deploy**: each manual task (database schema, tests) increases the risk of a fatal error; automate dependencies, minification, tests, documentation, packaging, deploy `[from source] (PRW p.67)`.
- Deploy tools cited: Phing, Capistrano, Ansistrano, Deployer (PHP; atomic deploy, parallel tasks), Magallanes `[from source] (PRW p.68)`. Provisioning: Ansible, Puppet, Chef `[from source] (PRW p.69)`.
- **Continuous integration** (Martin Fowler quote); Travis CI (`[DATED]`) and GitHub Actions; Jenkins, PHPCI, PHP Censor, TeamCity as reading `[from source] (PRW p.69-70)`.
- The book does **not** describe the Share-Nothing philosophy or PHP-FPM pool tuning; labeled `[extrapolation]`.

## 3. Virtualization
- Running different environments in development and production causes strange bugs; if you develop on Windows and publish on Linux, or in a team, consider a VM `[from source] (PRW p.70)`.
- **Vagrant**: virtual boxes from a single configuration file, with provisioning by Puppet or Chef; shared folders between host and VM `[from source] (PRW p.70-71)`.
- **Docker**: a lightweight alternative to VMs, based on containers and images; a typical LAMP app with three containers (web server, PHP-FPM, MySQL); `docker-compose.yml` to orchestrate; containers use less RAM and share the kernel `[from source] (PRW p.71)`. Book command: `docker run -d --name my-php-webserver -p 8080:80 -v /path/to/your/php/files:/var/www/html/ php:apache` `[from source] (PRW p.71)`.
- Caution: do not run downloaded code without checking; unofficial images may lack security patches; prefer official repositories; PHPDocker.io generates the files of a LAMP/LEMP stack `[from source] (PRW p.72)`.

## 4. Cache
- Opcode cache: PHP compiles the file into opcodes; with no code changes, recompiling wastes CPU; the opcode cache stores them in memory and reuses them, checking the file signature or modification date `[from source] (PRW p.72)`.
- "Probably" a significant improvement; **since PHP 5.5 the Zend OPcache is built in**, normally on by default depending on the package/distribution: check `opcache.enable` and the output of `phpinfo()`; before that, a PECL extension `[from source] (PRW p.72)`. Also cited: WinCache (Windows) and *PHP Preloading* (PHP >= 7.4) `[from source] (PRW p.73)`.
- The book does **not** give gain figures (v1 claimed "200% to 300%") or the parameters `opcache.memory_consumption`, `validate_timestamps` etc. (`[extrapolation]`).
- **Object cache**: keeping expensive data in memory (queries whose result rarely changes); APCu and memcached are the most used; **APCu** is simple but tied to the server; **memcached** is a separate service, accessible over the network `[from source] (PRW p.73)`.
- APCu cache sharing: with PHP-FPM it is shared among all processes of all pools; with (Fast-)CGI on the web server it is not shared; in CLI it exists only during the command `[from source] (PRW p.73)`. APCu tends to be faster, memcached scales more; on a single server: APCu is probably the best choice `[from source] (PRW p.73)`. Example with `apcu_fetch` and `apcu_add` `[from source] (PRW p.74)`.

## 5. PHPDoc
- PHPDoc is an **informal** standard for commenting PHP code, with many tags (list in the PHPDoc manual) `[from source] (PRW p.74)`.
- Tags in the example: `@author` (repeatable), `@link`, `@param` (type, name, description), `@return`, `@throws`; `@return void` explicitly states there is no return; historically omitting `@return` is equivalent to no return `[from source] (PRW p.74-76)`.
- Not in the book: use of PHPDoc by IDEs/static analyzers nor generic types such as `array<int, User>` (`[extrapolation]`).
