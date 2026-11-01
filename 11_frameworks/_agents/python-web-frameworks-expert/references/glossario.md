# Glossary (only terms the sources use)

Each term carries its source/page; terms without a page are [extrapolation] and were avoided.

| Term | Meaning according to the text | Source |
|---|---|---|
| **Project (Django)** | Collection of settings for a Django instance (database, Django options, app settings); collection of configuration and apps of a site | DJT p.1, 3 |
| **App (Django)** | Web application that does something (blog, public records, polls); Python package that follows a convention; can be in several projects | DJT p.3 |
| **manage.py** | Command-line utility to interact with the project | DJT p.2 |
| **settings.py** | Django project settings | DJT p.2 |
| **asgi.py / wsgi.py** | Entry points for ASGI / WSGI-compatible servers | DJT p.2 |
| **runserver** | Lightweight Python development server, not for production | DJT p.2 |
| **View (Django)** | Function that receives an `HttpRequest` as the first argument (plus values captured from the route as keyword arguments) and returns a response | DJT p.3, 5 |
| **HttpResponse** | Response object used in the minimal view | DJT p.3 |
| **URLconf** | URL configuration: Python file `urls.py` with a `urlpatterns` list; exists per app and in the project | DJT p.3-4 |
| **path()** | Routing function with `route`, `view` (required), `kwargs`, `name` (optional) | DJT p.5 |
| **include()** | References another URLconf; chops off the already-matched part of the URL and passes the rest; always use it, except with `admin.site.urls` | DJT p.4 |
| **Unapplied migrations** | Warning on the first `runserver`; handled later (part 2) | DJT p.2, 5 |
| **Flaskr** | Blog application built in the Flask tutorial | FLT p.1 |
| **Boilerplate** | Initial code/structure the Flask tutorial adopts to avoid pitfalls | FLT p.2 |
| **Blueprint (Flask)** | Only appears as part of section titles ("Blueprints and Views", "Blog Blueprint"); no definition | FLT p.1 |
| **Type hints** | Basis of FastAPI: standard Python types used in declarations | FAPI p.1 |
| **Starlette** | Library used by FastAPI for the web parts | FAPI p.4 |
| **Pydantic** | Library used by FastAPI for the data parts; `BaseModel` declares the body | FAPI p.4, 10-11 |
| **OpenAPI / JSON Schema** | Open standards on which FastAPI is based | FAPI p.2 |
| **Swagger UI / ReDoc** | The two automatic documentation interfaces (`/docs`, `/redoc`) | FAPI p.8-9, 16-17 |
| **Path parameter** | Variable part of the path, e.g.: `item_id` in `/items/{item_id}`, typed `int` | FAPI p.8 |
| **Query parameter** | E.g.: `q`; optional when declared with `= None` | FAPI p.8, 17 |
| **Body** | JSON data of the request, declared with a Pydantic model (e.g.: `Item`) | FAPI p.10-11 |
| **fastapi dev** | CLI command: reads `main.py`, detects the app, starts with Uvicorn and auto-reload | FAPI p.7 |
| **Uvicorn** | Server used by `fastapi dev` | FAPI p.7 |
| **uv** | Tool used in installation (`uv add`) | FAPI p.4, 20 |
| **fastapi[standard]** | Group of optional dependencies (uvicorn, fastapi-cli, httpx, jinja2, python-multipart, email-validator...) | FAPI p.20 |
| **FastAPI Cloud** | Deploy service from the FastAPI authors; main sponsor | FAPI p.19 |
| **Typer** | "FastAPI of CLIs", sibling project for terminal applications | FAPI p.4 |
