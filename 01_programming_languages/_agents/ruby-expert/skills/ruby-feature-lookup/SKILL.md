---
name: ruby-feature-lookup
description: Topic search (yjit, ractor, regexp timeout, prism, data, it...) in the index of the official Ruby 3.0 to 3.4 notes, returning version, summary and PDF page; answers NOT COVERED when the notes do not address the subject (GVL, shareable rules, RUBY_YJIT_ENABLE, Ruby 4.0...). Accepts Portuguese and English search terms.
---

# ruby-feature-lookup

JSON index (`scripts/ruby_feature_index.json`) with about 50 topics, each with the R30 to R34 pages (PDF page) and terms checked against the page text by `tests/verify_citations.py`. Read-only, no network.

```bash
python -I skills/ruby-feature-lookup/scripts/ruby_feature_lookup.py yjit
python -I skills/ruby-feature-lookup/scripts/ruby_feature_lookup.py "regexp timeout"
python -I skills/ruby-feature-lookup/scripts/ruby_feature_lookup.py --list
python -I skills/ruby-feature-lookup/scripts/ruby_feature_lookup.py gvl     # NOT COVERED (exit 1)
```

Rule: everything the script prints with a page is `[from source]`; `NOT COVERED` means the answer, if any, is `[extrapolation]`. The index is a memory aid: read the topical reference before asserting details.
