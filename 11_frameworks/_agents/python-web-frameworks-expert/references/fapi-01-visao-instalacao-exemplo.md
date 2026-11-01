# FAPI part A: overview, installation and minimal example (FAPI p.1-7)

Source: start page of the FastAPI documentation, badge **v0.141.1**, Python 3.10 to 3.14 (FAPI p.1). Pages = PDF. **[DATED]** relative to the capture (2026-08-18).

## What it is (FAPI p.1)
A **modern, fast (high-performance)** web framework for building **APIs with Python**, based on standard Python **type hints**. Links: documentation (fastapi.tiangolo.com) and source code (GitHub fastapi/fastapi).

## Key features as declared (FAPI p.1-2)
These are **the project's own claims**; read them as marketing, not as independent measurement.
- **Fast**: very high performance, "on par with NodeJS and Go" thanks to Starlette and Pydantic; one of the fastest Python frameworks.
- **Fast to code**: increase development speed by about 200% to 300% (estimate).
- **Fewer bugs**: reduce about 40% of developer-induced errors (estimate).
- **Intuitive**: great editor support, autocompletion everywhere. **Easy**, **Short** (less code duplication; multiple features from each parameter declaration), **Robust** (production-ready code with automatic interactive documentation).
- **Standards-based**: based on (and compatible with) the open standards **OpenAPI** (formerly Swagger) and **JSON Schema** (FAPI p.2).
- The asterisk explains that the percentages are **estimates** from tests by an **internal team** on production applications (FAPI p.2).
- Sponsors (FAPI p.2-3) and the testimonial from a Microsoft engineer (FAPI p.3) are not technical content.

## Requirements (FAPI p.4)
FastAPI "stands on the shoulders of giants": **Starlette** for the web parts and **Pydantic** for the data parts. **Typer** is cited as "the FastAPI of CLIs" (little sibling) for those building terminal applications instead of a web API.

## Installation (FAPI p.4-5, 20-21)
- First install **uv** and then add FastAPI to the project (FAPI p.4). **The terminal block with the command came out empty in the capture**; the text on p.20 shows `uv add "fastapi[standard]"`.
- Note: put `"fastapi[standard]"` **in quotes** so it works in all terminals (FAPI p.5).
- Those who prefer **pip**: install `fastapi[standard]` **inside a virtual environment**; there is an installation guide with alternative steps (not included) (FAPI p.5).
- Without the standard group: `uv add fastapi`; standard without the cloud client: `uv add "fastapi[standard-no-fastapi-cloud-cli]"` (FAPI p.21). Details in `fapi-03-deps-deploy-desempenho.md`.

## Minimal example: `main.py` (FAPI p.5)
Create `main.py` with: `from fastapi import FastAPI`, `app = FastAPI()`, a route `@app.get("/")` that returns `{"Hello": "World"}` and a route `@app.get("/items/{item_id}")` with `item_id: int` and `q: str | None = None`, which returns `{"item_id": item_id, "q": q}`. (Generate with `python -I scripts/scaffold.py fastapi`.)

## `async def` variant (FAPI p.6)
If the code uses `async`/`await`, declare the functions with `async def`; the example repeats the two routes this way. For those who do not know it, the text refers to the "In a hurry?" section on `async` and `await` in the documentation (not included: NOT COVERED for the detail). **Linter**: `FA-AWAIT-IN-DEF`.

## Run (FAPI p.6-7)
- "Run the server with:" and the **command is in an empty terminal block in the capture**. The surrounding text says: the `fastapi dev` command **reads `main.py` automatically, detects the FastAPI app and starts a server using Uvicorn**; by default it starts with **auto-reload** enabled, **for local development** (FAPI p.7). More details in the FastAPI CLI documentation (not included).
- Do not state flags (`--port`, `--host`) or other subcommands: NOT COVERED.

## Check (FAPI p.7-8)
- Open `http://127.0.0.1:8000/items/5?q=somequery`; the JSON response is `{"item_id": 5, "q": "somequery"}`.
- The created API receives HTTP requests on the paths `/` and `/items/{item_id}`; both accept **GET**; `item_id` is a **path** parameter that must be `int`; `q` is an optional `str` **query** parameter (FAPI p.7-8).
