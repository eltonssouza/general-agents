# FAPI part C: deploy, performance, dependencies and license (FAPI p.19-21)

Source: FastAPI v0.141.1 overview. Pages = PDF. **[DATED]** relative to the capture (2026-08-18).

## Deploy (FAPI p.19-20)
- Optional: deploy the app to **FastAPI Cloud** "with a single command". **The command is in an empty terminal block in the capture**: NOT COVERED for the exact command; do not invent it.
- The text says the CLI **automatically detects** the FastAPI app and deploys; if you are not logged in, the **browser opens** to complete authentication.
- **FastAPI Cloud** is made by the same author and team as FastAPI; it simplifies building, publishing and accessing an API; it is the **main sponsor and funder** of FastAPI and of the open-source "friends" projects (FAPI p.19).
- **Other providers**: FastAPI is open source and standards-based; it can be deployed on any cloud provider; follow the provider's guides (FAPI p.20). No provider guide is included.
- Conflict-of-interest alert [inference]: the source is the project's own doc, which promotes the product of its main sponsor.

## Performance (FAPI p.20)
- The text claims that independent **TechEmpower** benchmarks show FastAPI applications under **Uvicorn** as **one of the fastest Python frameworks**, below only **Starlette and Uvicorn** (used internally). The text refers to a "Benchmarks" section of the doc (not included).
- **No numbers** appear; do not cite values. Comparison with Django or Flask: NOT COVERED.

## Dependencies (FAPI p.20-21)
- FastAPI depends on **Pydantic** and **Starlette** (FAPI p.20).
- `uv add "fastapi[standard]"` installs the `standard` group of optional dependencies:
  - Used by Pydantic: `email-validator` (email validation).
  - Used by Starlette: `httpx` (required to use the `TestClient`), `jinja2` (required for the default template configuration), `python-multipart` (required for form "parsing" with `request.form()`).
  - Used by FastAPI: `uvicorn` (server that loads and serves the application; includes `uvicorn[standard]`, with dependencies such as `uvloop` for high performance), `fastapi-cli[standard]` (provides the `fastapi` command), which includes `fastapi-cloud-cli`, to deploy to FastAPI Cloud.
- Without the standard dependencies: `uv add fastapi` (FAPI p.21).
- Standard without `fastapi-cloud-cli`: `uv add "fastapi[standard-no-fastapi-cloud-cli]"` (FAPI p.21).
- **Additional optionals** (FAPI p.21): Pydantic: `pydantic-settings` (settings management), `pydantic-extra-types` (extra types). FastAPI: `orjson` (required for `ORJSONResponse`), `ujson` (required for `UJSONResponse`).

## License (FAPI p.21)
MIT.

## Usage notes
- Anyone using `fastapi dev` depends on the CLI package, which comes in the `standard` group (FAPI p.20) [direct inference: without the standard group the `fastapi` command may not exist]. The source does not state what happens without it.
- Versions and package names are those of the capture; check the current documentation before using [DATED].
