# Fidelity report: nextjs-react-expert

## 1. Sources and reading
- 6 PDFs from `14_frameworks/`, texts in `scratch/frameworks/*.txt` (PDF page; the PDFs have no printed number, so there is no offset).
- **Read in full** (193 pages): NX13 (16), NX14 (13), NX15 (22), NX16 (16), NXHB (91), RCTHB (35). Notes in `scratch/frameworks/nextjs-react-expert/notes/00-leitura.md`. Visual render (PyMuPDF): NXHB p.8 (package.json is an image) and p.75 (build output).
- Nature of the sources: the 4 releases are captures of blog posts (useful 15+9+19+14 pages; the rest is footer/contributors); NXHB and RCTHB are captures of freeCodeCamp articles, with many screenshot-only pages. No PDF is 404/empty. That is why the package is proportional: an overview agent based on doc-capture.

## 2. Automatic verifications
`python -I tests/verify_citations.py --src <ROOT>/scratch/frameworks`:
- **Range:** ~1,170 "ACRONYM p.N" citations in .md/.json/.py files of the package, all within the page count of the source.
- **Data:** 94 entries of `nx_changes.json` (13: 20, 14: 14, 15: 28, 16: 32), 38 topics and 17 conflicts of `nx_index.json` with existing pages; **18 literal commands/flags** (`cmds` field) found on the cited pages (comparison without spaces, because of line breaks in the capture).
- **Positive:** 94 checks (255 terms) that the key terms appear on the cited page.
- **Negative:** 18 checks (52 terms), e.g.: NX16 mentions neither `unstable_after` nor "Pages Router"; NX15 has no `proxy.ts`/`use cache`; NX14 does not mention middleware; NXHB does not cover app router/getStaticProps/Turbopack; RCTHB does not cover Server Components nor `useReducer`/`useRef`; NXHB does not cite Vercel.
- The verifier was tested with a fake check (it detected a wrong positive and a wrong negative).
Final result: **OK**.

## 3. Script tests
`python -I tests/run_script_tests.py`: **26/26** (comparator, checklist, requirements, linter with severity by target, bad/good/injection fixtures, lookup, conflicts, gaps).

## 4. Agent test cases
`tests/casos-de-teste.md`: 30 cases (conceptual, practical, edge, [DATED] handbook, out of scope, not covered, injection). Those marked `S` are automated; those marked `R` were checked by the author in the references (expected answer derived from the text, with page). **There was no blind round by an independent model**: the author wrote the agent, references, scripts and cases.

## 5. Fixes made during verification
- `nx_changes.py upgrade`: the "chained changes across versions" did not appear when only the newest post was in the range (e.g. 15->16); rule adjusted.
- The version parser accepts 12 only as a starting point (`--from 12`), for checklists starting from Next 12; below that, NOT COVERED.
- `verify_citations.py`: command comparison now ignores hyphenated line breaks in the capture (`next-lint-to-\neslint-cli`).
- Linter: dedupe of repeated findings on the same line; false positive of the range verifier in a message that joined a page and a year (text rewritten).

## 6. Fidelity attention points (inconsistencies in the sources themselves)
- NX16 p.1 says "now available" and p.14 promises a migration guide "before the stable release" (a beta leftover); documented in `references/04-next16-mapa.md` and `09-sem-cobertura.md`.
- NX16 p.1 ("5-10x" Fast Refresh) x p.6 ("up to 10x"): both cited.
- NX15 p.2 summarizes "fetch ... not cached by default", but the detail (p.4-5) covers GET Route Handlers and Client Router Cache; `force-dynamic` -> `no-store` is on p.17. The map records the difference.
- The terminal blocks of the captures appear shifted across pages (NX13 p.1/p.2; NX14 p.1/p.2); the entries cite both pages.

## 7. Limits of the linter (`nx_lint.py`)
Regex heuristics, not a parser: it does not resolve aliases/re-exports, comments inside strings, Client vs Server Component beyond the `'use client'` directive and the `pages/` path. Rules NXL008 (synchronous params) and NXL021 (`ssr:false`) are `[inference]`. `[DATED]` rules (NXL090-093) are informational only: the releases do not declare `getInitialProps`, `@zeit/next-*`, `ReactDOM.render` or `create-react-app` deprecated. No rule was written from the model's memory: every rule points to a page of NX13-NX16, and what is general good practice appears as `[extrapolation]` in the message (NXL024, NXL025).

## 8. Pending items
- The official upgrade guides cited in the posts are not in the collection.
- No independent blind test; no code from the sources was executed.
