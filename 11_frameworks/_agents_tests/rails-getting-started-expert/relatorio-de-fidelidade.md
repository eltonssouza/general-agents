# Fidelity report - rails-getting-started-expert

## Source and reading
- Single source: `14_frameworks/Rails-Getting-Started-Guide.pdf` (72 pages; extracted text in `scratch/frameworks/Rails-Getting-Started-Guide.txt`, ~98 thousand bytes). Official Rails guide; "store" app (not "blog"). **Rails 8.1.0+, Ruby 3.2+**; **date not printed** (INDEX §1).
- **Read in full** (all 72 pages), in 3 sequential blocks; notes in `scratch/frameworks/rails-getting-started-expert/notes/notas-leitura.md`. **No page was rendered**: the text carries all the code; images are browser screenshots described in the text. All pages have useful content; none is 404/empty.
- Page convention: PDF = "Page N of 72", no offset.

## Citation verification (`tests/verify_citations.py`)
- Range: 244 pages in `RGS p.N` citations and ~600 bare `p.N` in the references, all within 1-72.
- 74 **positive** checks (key terms present on the cited pages) and 20 **negative** checks (plausible claims the guide does not make: scaffold, PostgreSQL, namespace/member, `permit!`, Devise, JS bundlers, RSpec, Heroku, uniqueness, polymorphic associations, `after_save`, scopes, Accept-Language, OWASP/XSS, "blog" outside p.20, "rails 7/9", `form_for`, `respond_to`...). Final result: **0 failures**.
- Failures found and fixed during construction: `params[:id]` is at the end of p.25 (citation widened to p.25-26); the `dev:cache` command is at the start of p.42 (citation widened to p.41-42); the word "format" appears on p.16-17 (negative check replaced by "length:").
- Limit: the verifier checks key terms per page, not the semantic correctness of each sentence in the references; the sentences were written while reading the pages and checked by manual sampling.

## Script tests (`tests/run_script_tests.py`)
36/36 pass (lookup, plan, lint with 10 fixtures, checklist with `store_ok` and `store_incompleto`, injection in a comment). The linter was also run on all `.rb/.erb` files of `store_ok` (reconstruction of the guide's code): no findings.

## Honesty
- There was no blind run by an independent model; the 30 cases in `casos-de-teste.md` were run by the author.
- The `store_ok` fixtures reproduce excerpts of the guide (rewritten in minimal form); they serve to test the scripts and do not replace the guide.
- Linter rules outside the guide (L14, L16) are `[extrapolation]` and are off by default; L13 is `[inference]`.
- Items not covered by the guide are listed in `scripts/rails_index.json` (`gaps`) and in `references/INDEX.md` §3.
- There is no map of changes between Rails versions: the PDF covers a single version (8.1.x).

## Open items
None known. If a PDF of another version of the guide becomes available, it is recommended to build a change map from its text.
