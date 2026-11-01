---
name: ruby-version-lookup
description: Shows what each official release note (Ruby 3.0, 3.1, 3.2, 3.3, 3.4) brings, with date and PDF page, and lets you search a term across all versions. Answers NOT COVERED for versions outside 3.0-3.4 and for terms the notes do not bring.
---

# ruby-version-lookup

Data in `scripts/ruby_version_data.json` (highlights per version, with pages checked by `tests/verify_citations.py`). Read-only, no network.

```bash
python -I skills/ruby-version-lookup/scripts/ruby_version_lookup.py --version 3.2
python -I skills/ruby-version-lookup/scripts/ruby_version_lookup.py --query yjit
python -I skills/ruby-version-lookup/scripts/ruby_version_lookup.py --all
```

Pages = PDF pages (the notes are captures of web pages, with no printed numbering). Printed items are `[from source]`; `NOT COVERED` = answer as `[extrapolation]` or say the notes do not address it. The highlights are a selection, not the whole note.
