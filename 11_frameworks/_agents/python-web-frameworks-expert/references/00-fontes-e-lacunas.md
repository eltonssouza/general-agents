# Sources, gaps and capture defects

This agent gives an **overview based on captures of web documentation**. It is not a course on Django, Flask or FastAPI.

## 1. How much each source really covers
| Source | Useful content | What is missing |
|---|---|---|
| **DJT** (Django 5.0, tutorial part 1; 8 pp.) | p.1-5: checking the installation, `startproject`, layout, `runserver`, `startapp`, view, URLconf, `include()`, arguments of `path()` | p.6-8 are only sponsors/navigation. Tutorial parts 2+ (models, migrations, admin in use, templates, forms, tests) **are not there** (part 2 is only pointed to, DJT p.5). Installing Django is not taught (DJT p.1). |
| **FLT** (Flask 3.1.x, start of the Tutorial; 3 pp.) | Goal of the Flaskr blog, prerequisite, 11 section titles, flexibility philosophy (FLT p.1-3) | **All the content of the sections** (layout, factory, database, blueprints, templates, static files, tests, deploy). No code, no commands. |
| **FAPI** (FastAPI v0.141.1, overview; 21 pp.) | Features, `main.py` example, `async def`, `fastapi dev`, `/docs` and `/redoc`, Pydantic body, what the framework validates, `standard` dependencies, deploy (concept), license | Commands inside terminal blocks (empty in the capture); user guide (only cited as a "spoiler", FAPI p.18-19); any detail on DI, security, WebSockets, CORS. |

## 2. Capture defects that affect the answers
1. **Empty terminal blocks in the FAPI** (p.4-7 and p.19): the PDF body does not reveal the exact install command shown, nor the run command, nor the deploy command. What can be stated comes from the surrounding text: `uv add "fastapi[standard]"` (FAPI p.20), the quotes warning (FAPI p.5), "fastapi dev" (FAPI p.7) and "a single command" for deploy without the command (FAPI p.19).
2. **Swagger/ReDoc screenshots**: p.8 came out blank; p.12-14 have Swagger UI images with no extractable text; the interface version in them cannot be identified.
3. **Page breaks in the middle of code**: the app URLconf example (DJT p.3-4) and the example with `Item` (FAPI p.10-11) start on one page and end on the next.
4. **Banners**: DJT p.1 warns that the version is insecure and unsupported; p.5 carries a donation ad. This is not framework content.
5. **"??%" labels on the test-coverage badge and "passing"** (FAPI p.1) are badge residue: do not cite them as data.

## 3. Declared gaps (answer "NOT COVERED")
Run `python -I scripts/fw_lookup.py --gaps`. Summary:
- Flask tutorial content beyond the index; installing Django and Flask.
- Django from part 2 onward.
- FastAPI deploy command; details of the FastAPI user guide.
- Benchmarks and performance comparisons; which framework to choose (the sources do not compare).
- Any version other than Django 5.0, Flask 3.1.x and FastAPI 0.141.1, and what changed between versions.
- REST in general -> `web-api-rest-architecture-expert`; Python (the language) -> `python-expert`.

## 4. Internal divergences and traps
- **Django version**: the tutorial is for 5.0 and the banner says the version is no longer supported (DJT p.1); the example server output shows "Django version 5.0" and a date of April 2025 (DJT p.2). Do not extrapolate to newer versions.
- **Flask 3.1.x** comes from the PDF title (metadata) and the "stable" selector; the body text does not write the version number.
- **FastAPI performance and productivity claims** (speed "on par with NodeJS and Go", 200% to 300% faster to code, 40% fewer bugs) are **self-declared**; the percentage figures are marked in the text itself as an estimate from an internal team (FAPI p.1-2). They are not independent evidence.
- **Microsoft testimonial** (FAPI p.3) is an individual opinion quoted, not technical data.
- **"fastapi dev" vs. production**: the text says auto-reload is on "for local development" (FAPI p.7); it does not say how to serve in production.
- **FastAPI "aside from Python"**: the example uses `str | None`, which is type syntax; the badge lists Python 3.10-3.14 (FAPI p.1). That `X | None` requires 3.10 is language knowledge, [extrapolation].
