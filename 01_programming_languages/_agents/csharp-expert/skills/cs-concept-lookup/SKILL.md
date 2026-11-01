---
name: cs-concept-lookup
description: Looks up a topic in the section map of the C# Yellow Book (PDF pages). Use when you need to know where the book covers a topic. Answers NOT COVERED when the book does not cover it (boxing, using/Dispose, lock, throw;, GetHashCode, TryParse etc.). Accepts English or Portuguese keywords.
---

# cs-concept-lookup

Locates **where** the *C# Yellow Book* (CSYB, Rob Miles, 217 p.) covers a topic and returns the section and PDF pages (printed = PDF − 5). The summary is a guide; **read the page** before stating something as `[from source]`.

## Usage (from the root of the `csharp-expert/` package)

```bash
python -I skills/cs-concept-lookup/scripts/cs_concept_lookup.py struct
python -I skills/cs-concept-lookup/scripts/cs_concept_lookup.py threads
python -I skills/cs-concept-lookup/scripts/cs_concept_lookup.py 4.9
python -I skills/cs-concept-lookup/scripts/cs_concept_lookup.py --list
python -I skills/cs-concept-lookup/scripts/cs_concept_lookup.py boxing      # NOT COVERED (exit 1)
```

## Output and limits

- Topic absent from the book: prints `NOT COVERED` and a note on what the book says instead; answer with `[extrapolation]` or say the book does not cover it.
- Version features (record, nullable, `async`, LINQ) are not in the CSYB; use `skills/cs-version-lookup`.
- The index lives in `scripts/cs_concept_index.json` (sections, keywords in English and Portuguese, `not_in_book` list).
