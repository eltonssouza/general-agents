# Procedures (based on what the collection states)

## P1. Answer "what changed between Next X and Y?"
1. Confirm that X and Y are in 13-16; outside that, say "NOT COVERED" (the collection does not cover Next 12 or earlier, nor 17+).
2. Run `python -I scripts/nx_changes.py changes --from X --to Y` (optional `--kind breaking,removal`, `--thread caching`). Semantics: versions **greater than X and up to Y** are included (use `--inclusive` to include X).
3. Answer grouped by version and by type (requirement, breaking change, removal, behavior, deprecation, new feature), each item with `[from release] NXn p.N`.
4. If the user asks something the script did not return, say "the text does not say" instead of filling in from memory; offer `[extrapolation]` only if asked.

## P2. Upgrade checklist
1. `python -I scripts/nx_changes.py upgrade --from X --to Y` (accepts `--from 12` as "before 13"; older versions = NOT COVERED).
2. Check requirements (Node, React, TypeScript, browsers): `requirements`.
3. Run the static linter on the user's files with the right target: `python -I scripts/nx_lint.py PATH --target Y` and relate each finding to the checklist item.
4. Remember that each post says to read the official *upgrade guide* (not included in the collection); cited upgrade commands: `nx_changes.py commands`.
5. Do not execute commands or codemods; present them as data from the posts.

## P3. Review a Next.js snippet/project
1. Identify the target version (package.json: `next`, `react`, `typescript`, `eslint`, `engines.node`) and whether the code uses app/ or pages/.
2. `nx_lint.py` with `--target`. Each finding carries a `[from release]`, `[inference]` (heuristic) or `[DATED]` label.
3. A `[DATED]` finding (getInitialProps, @zeit/next-*, ReactDOM.render, create-react-app) is **informational**: the releases do not declare them deprecated.
4. Regex heuristics can give false positives/negatives (comments, aliases, Client vs Server Component); say so.

## P4. Handbook-based question (NXHB/RCTHB)
1. Mark the answer `[DATED]` with the date (NXHB Nov/2019, Next 9.1.2; RCTHB Nov/2020).
2. Consult `08-conflitos-datado-vs-releases.md` / `nx_lookup.py --conflicts` and cite the pages on both sides.
3. If the release is silent, write "the releases do not say whether this was deprecated".

## P5. Question about a version the collection does not have
Answer "NOT COVERED", offer what the collection says about the nearest version (with pages) and make clear that the model's prior knowledge does not count for versions the PDF does not include.
