---
name: orq-catalog
description: Checks and regenerates the catalog of specialist agents used by the orchestrator (scripts/catalog.json and references/catalogo.md) from the real frontmatters of folders 01_* to 99_*. Use when an agent is created, renamed or removed, when route.py does not find an agent that exists, or when asked "update the catalog", "is the catalog up to date?". Do not use to edit the specialist agents.
---

# Catalog maintenance

## Procedure
1. Check (read-only):
   ```bash
   python -I <PKG>/scripts/build_catalog.py --check
   ```
   exit 0 = up to date; exit 1 = stale; exit 2 = read error (missing frontmatter or `name` different from the folder, reported in the message).
2. If it is stale, regenerate: `python -I <PKG>/scripts/build_catalog.py` (overwrites only `scripts/catalog.json` and `references/catalogo.md`).
3. Run the package tests: `python -I <PKG>/tests/run_script_tests.py`. If a routing case fails because of the new agent, adjust `references/fronteiras.md` and the test case; do not adjust the catalog by hand.
4. Exit 2: report the file and the problem to the user. Fixing the specialist agent is outside the scope of this skill.

`<PKG>` = package root; from this skill, `../../`. `--root PATH` points to another collection root.

## Completion criterion
`--check` returns exit 0 and `run_script_tests.py` finishes with no FAIL.
