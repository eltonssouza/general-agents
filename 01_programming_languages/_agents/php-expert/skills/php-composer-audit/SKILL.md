---
name: php-composer-audit
description: Read-only checklist for composer.json (composer.lock alongside, psr-4/psr-0 autoload, PEAR repository, PHP version, tools in require, '*'/dev-master constraints), with the origin of each rule (book with page, or extrapolation). No network; does not audit dependency vulnerabilities.
---

# php-composer-audit

```bash
python -I skills/php-composer-audit/scripts/audit_composer.py path/composer.json
python -I skills/php-composer-audit/scripts/audit_composer.py --rules
python -I skills/php-composer-audit/scripts/audit_composer.py --json path/composer.json
```
Rules with origin `book`: composer.lock (PRW p.16), PSR-4/PSR-0 (p.12), PEAR repository in Composer 2 (p.18). The others (`require-dev`, PHP version, `*`) are `extrapolation`. For vulnerabilities, the book mentions the Local PHP Security Checker over `composer.lock` (p.17, tool `[DATED]`); this script does not do that.
