---
name: python-version-features
description: Answers "in which Python version did X appear?", "does this work on my Python?", "what changed in 3.14?" using only the version marks in the text (Tutorial and Language Reference 3.14.0rc3) and stating "version not given in the text" when there is no mark; consults the 3.10–3.13 Tutorials as presence (not as a mark). Covers match, walrus, positional-only parameters, type, f-strings `{x=}`, t-strings, `except` without parentheses, disableable GIL, dict order. Use when the user asks for the minimum version of a feature, compatibility between Python 3 versions or what is new in 3.14. Do not use to convert Python 2 (use python-py2-to-py3), for Python 3.15 onward (no source) or for code review.
---

# Python feature versions (sources: 3.14.0rc3)

Master table in `../../references/versoes-e-datado.md` (§1 marks, §2 features without a mark, §5 release candidate, §6 gaps). This skill applies a strict procedure so as not to invent versions.

## Procedure

1. **Ask for the target version** (or the one the user runs). Without it, answer conditionally.
2. **Look up the feature** in the master table (`Grep` for the name in `versoes-e-datado.md`).
3. **If there is a mark** ("Added in", "Changed in", deprecated, removed), cite the version **and the exact source** (Tut or Ref, page). The **Ref marks** several features that the **Tut presents without a mark**; say which source the mark comes from. Marked examples: `match` 3.10 (Ref p.131), `type` 3.12 (Ref p.123), `:=` 3.8 (Ref p.110), `/` in parameters 3.8 (Ref p.140), `{x=}` 3.8 (Ref p.25), t-strings 3.14 (Ref p.26), `__annotate__`/PEP 649 3.14, `except A, B` without parentheses 3.14 (Ref p.127), disableable GIL since 3.13 (Tut p.130).
4. **If there is no mark**, write **"version not given in the text"**. Features in this situation: `ExceptionGroup`/`except*`, `add_note()`, `@dataclass`, `compression.zstd`, `sys._is_immortal()` and others listed in `versoes-e-datado.md` §2. **Do not invent the version.** If the user insists, offer what you know from outside the sources **labeled [extrapolation]** and recommend checking the documentation of their version.
5. **For "does it work on my Python?"**: compare the user's version with the mark; the result is an **[inference]** based on the mark, unless the source says it literally.
6. **Consult the 3.10–3.13 Tutorials only as presence** (optional, when the user compares versions):
   ```bash
   python -I scripts/tutorial_versions.py add_note dataclass
   python -I scripts/tutorial_versions.py --list
   ```
   The script shows in which of the 5 Tutorials (3.10, 3.11, 3.12, 3.13, 3.14.0rc3) the term appears and on which PDF page of each. **Presence in the Tutorial is not a version mark**: the Tutorial may mention a feature long after it existed (`@dataclass` only appears in the body from Tutorial 3.12). "Was introduced in X" from that is an **[inference]**; absence from the 5 Tutorials does not prove the feature does not exist; a term outside the curated index returns **NOT COVERED**.
7. **Remember the nature of the source**: the documentation is a **release candidate**. There is no "What's New", no release notes of any version and no 3.15 documentation.

## Dict order (typical case)

Described at three moments in the sources: Python 2 (no guarantee), 3.6 with a caveat (Notes p.793–794, community) and a guarantee from 3.7 by the Ref (Ref p.35, "Changed 3.7"). The official one prevails; `OrderedDict` for ordering is **[DATED]** as a justification.

## Response format

Feature → version and source (or "version not given in the text") → what that means for the user's version (**[inference]**) → gaps. No lists of "3.15 novelties" or of versions the sources do not cover.

## Limits

- Only what the text marks counts. The absence of a mark does not prove the feature is old or new.
- The 3.10–3.13 Tutorials were not distilled: there is only the presence index of 47 terms (`scripts/tutorial_index.json`, verified by `tests/verify_citations.py`).
- Marks from the Notes (e.g. "3.x Version ≥") are community-made; use them as a labeled complement.
