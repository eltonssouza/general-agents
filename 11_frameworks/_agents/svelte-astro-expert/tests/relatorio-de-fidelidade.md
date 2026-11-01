# Fidelity report: svelte-astro-expert

Run date: 26 Oct 2026 (author's environment). Page convention: **PDF page** (the 3 sources have no printed book numbering).

## 1. Sources and reading
| Source | Pages | Reading | Visual check |
|---|---|---|---|
| SVHB (*The Svelte Handbook*) | 49 | in full, extracted text | rendered p.8, 15, 29, 33, 35 |
| SKGS (SvelteKit Introduction) | 3 | in full | rendered p.1-2 |
| ASTRO (landing) | 3 | in full | p.1 rendered; PDF links read as metadata |

Usefulness: SVHB is real content; SKGS is introduction only (p.3 has no content); ASTRO is a landing page (no technical content beyond one command and feature names). The agent was limited to stating only what each source says.

## 2. Citation verification (`tests/verify_citations.py`)
Command: `python -I tests/verify_citations.py --src <scratch/frameworks>`
- **Range:** all `SIGLA p.N` citations and loose `p.N` in the references/scripts/tests fall within 1-49 (SVHB), 1-3 (SKGS), 1-3 (ASTRO).
- **Positive:** 74 checks (key terms on the cited page), all pass.
- **Negative:** 25 checks (plausible claims that the collection does **not** contain: "Svelte 3/4/5", runes, snippets, TypeScript, tests, transitions, `+page.svelte`, SvelteKit creation command, `.astro`, `client:load`, Svelte in Astro, v7 upgrade content, deploy, Vue/Angular on the Astro landing...), all pass.
- **Verifier test:** a mutation (checks that should fail) was run and the verifier rejected them (4 expected failures), so it does discriminate.
- Limit: the verifier checks terms on the cited pages, not the whole paraphrase; the sentence-by-sentence reading of the references was done by the author.

## 3. Script tests (`tests/run_script_tests.py --src ...`)
44 automated cases (lookup 14, lint 14, compare 9, checklist 6, citations 2 including the minimum count): **44 pass, 0 fail**. They include exit codes (0/1/2), `--json`, stdin, nonexistent file, injection in a comment, `.astro`, `+page.svelte`, runes.

## 4. Conceptual tests (`tests/casos-de-teste.md`)
28 cases (conceptual, practical, borderline, out of scope, injection). Those depending only on scripts are automated; the conceptual ones were checked by the author against the references and pages. **There was no blind run by an independent model.**

## 5. Points of attention found while reading
1. The handbook **does not declare the Svelte version**; "Svelte 3" is only an [inference] from the (pre-runes) syntax and the date. The Vite/port 5173 setup postdates 2019: the text was updated after the header.
2. The SVHB text extraction loses `on:` and `bind:` in some examples (they appear loose at the end of the line); the rendered PDF is correct. The references use the syntax checked on the image.
3. The handbook's slot example (p.29-30) uses a lowercase `<button>` where `<Button>` is meant: recorded as an example flaw [inference].
4. The handbook shows `onMount(async ...)` returning a cleanup function (p.32); rule SVL-L03 warns, as an explicit `[extrapolation]` without a page, that other documentation may treat this differently. It is the **only** linter rule without page support.
5. The comparator uses columns of different eras (2019 book x 2026 pages); this is stated in the output and in the agent.
6. Astro "v7": only the banner; none of the content. The agent does not describe v7.

## 6. Labels used
`[from source]` (includes the SKGS/ASTRO web pages), `[inference]`, `[extrapolation]`, `[DATED]`, NOT COVERED. No long passages copied; literal quotes only short.

## 7. Limitations
- Heuristic linter (regex), not a Svelte parser; false positives/negatives possible (e.g. A01 only fires if the variable is a top-level `let` and appears in the template).
- Rules turned off for files with runes, `+page.svelte` and `.astro`.
- No change map by version (one era per framework).
- Pending: none known; a review by an independent model would be desirable.
