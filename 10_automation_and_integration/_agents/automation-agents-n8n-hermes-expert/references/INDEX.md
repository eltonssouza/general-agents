# INDEX - n8n Docs and Hermes Agent Docs (landing pages)

This collection is NOT a book or a manual: it is two **captures of documentation home pages** (8 PDF pages in total). The agent provides an **overview based on a doc-capture**: it states only what the pages say and answers "NOT COVERED" for the rest.

## 1. What each PDF is

| Acronym | File | Pages | What it is | Usefulness |
|---|---|---|---|---|
| **N8N** | `n8n-Docs.pdf` | 4 | Home page of the n8n documentation ("n8n Docs", "Get started" tab). URL does not appear in the text. A cookie banner covers every page. | **Partial/low**: ~2 thousand useful characters: one definition sentence, section and link names, 3 cards for connecting to the MCP server. Almost everything is link titles, without content. |
| **HERMES** | `Hermes-Agent-Docs.pdf` | 4 | Home page of the "Hermes Agent" documentation (Nous Research); no page URL, but the installation commands point to `hermes-agent.nousresearch.com`. | **Good for an overview**: ~4 thousand characters with definition, installation (Desktop/CLI), `hermes setup --portal`, list of doc pages and list of features. It is **promotional text from the project itself**. |

Neither is useless (no 404, no navigation-only page). n8n is the weaker one: p.4 has only the copyright footer and the banner; the cookie banner is noise (N8N p.1-4).

## 2. Page convention
**PDF page** = the `=== PAGE N ===` marker of the extracted text. The n8n pages carry the printed number "1".."4" and coincide; the Hermes ones have no printed number. Always cite `N8N p.N` or `HERMES p.N`; no offset.

## 3. Reading coverage (honest)
- **Read in full:** all 8 pages (extracted text) and the 8 rendered with PyMuPDF.
- **Rendered and checked visually:** n8n p.1 and p.3 (banner covers part of the content), p.2 (card images: a "Schedule Trigger" node, a docker-style code snippet and a sign-up form at illegible resolution, and logos), Hermes p.1-2 and p.4 (installer code blocks, "Fastest path" box, feature list). Text and render agree, except: (a) "Schedule Trigger" exists only in the image; (b) the host of the URL in the n8n MCP commands is blank in the extraction; (c) the code in the n8n images is illegible and is **not** used.
- Dates: n8n p.4 "© 2026" and p.3 "Last updated 5 days ago" (relative, no absolute date); Hermes carries neither date nor version. Everything is [DATED] relative to a 2026 capture of unknown exact date.

## 4. File map
| File | Content |
|---|---|
| `01-n8n-docs-landing.md` | everything the N8N source says, by page |
| `02-hermes-agent-landing.md` | everything the HERMES source says, by page |
| `03-comparacao-e-fronteiras.md` | comparison restricted to the sources; boundary with other agents; NOT COVERED list |
| `glossario.md` | terms that appear in the sources (with what the source says, not what is known from memory) |
| `procedimentos.md` | P1-P6: how to answer with these sources |
| `casos-e-antipadroes.md` | typical mistakes (inventing link content, promotional as fact, etc.) |
| `datado.md` | what is dated/relative |

## 5. Scripts (in `../scripts/`)
`nh_lookup.py` (search; prints "NOT COVERED"), `nh_map.py` (page map and checklist), `nh_compare.py` (side-by-side comparator). Data in `nh_index.json`. Citation verification: `../tests/verify_citations.py`.
