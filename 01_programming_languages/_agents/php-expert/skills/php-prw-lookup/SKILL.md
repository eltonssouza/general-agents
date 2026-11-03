---
name: php-prw-lookup
description: "Topic search in the index of \"PHP: The Right Way\" (PRW), returning PDF pages or NOT COVERED when the book does not cover the subject (e.g. strict_types, Throwable, CSRF). Read-only, no network."
---

# php-prw-lookup

Use before citing `(PRW p.N)`. Pages = PDF (the book is a site capture, with no printed numbering).

```bash
python -I skills/php-prw-lookup/scripts/prw_lookup.py "pdo"
python -I skills/php-prw-lookup/scripts/prw_lookup.py "strict_types"   # NOT COVERED
python -I skills/php-prw-lookup/scripts/prw_lookup.py --list
python -I skills/php-prw-lookup/scripts/prw_lookup.py --not-in-book
```

Exit code: 0 = topic found; 2 = NOT COVERED. A topic found does not replace reading `references/`; "NOT COVERED BY THE BOOK" means it can only be answered as `[extrapolation]`. Queries may be in English or Portuguese.
