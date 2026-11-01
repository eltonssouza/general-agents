---
name: cs-version-lookup
description: Read-only lookup of the C# version timeline according to the sources (The history of C#, What's new in C# 12 and 13). Use when asked in which version a feature appeared or what a version lists. Returns dates, features listed per version and PDF pages; answers "version not stated in the sources" for anything not listed.
---

# cs-version-lookup

Answers "in which version does the source list feature X?" and "what does the source list for C# N?", from C# 1.0 to C# 14. Pages are PDF pages: `CSHist` (16 p.; the PDFs `CSharp-9/10/11-WhatsNew.pdf` have the same text), `CS12` (6 p.), `CS13` (7 p.).

## Usage (from the root of the `csharp-expert/` package)

```bash
python -I skills/cs-version-lookup/scripts/cs_version_lookup.py --version 12
python -I skills/cs-version-lookup/scripts/cs_version_lookup.py --query records
python -I skills/cs-version-lookup/scripts/cs_version_lookup.py --query lock
python -I skills/cs-version-lookup/scripts/cs_version_lookup.py --all
```

Exit code: 0 = found; 1 = `NOT COVERED` (feature or version absent from the sources).

## Limits

- The sources only **list** features; any technical description beyond that is `[extrapolation]`.
- Visual Studio/.NET versions only appear when the source cites them (`platform` field); absent = "not stated in the sources" (e.g. .NET 7 for C# 11, .NET 10 for C# 14).
- Queries match the English feature names and the original Portuguese names (`features_pt`).
- Data in `scripts/cs_version_data.json`.
