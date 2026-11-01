# Procedures (recipes the sources support)

The commands below come from the sources and are **not executed** by the agent or the scripts. [DATED]: Django 5.0, FastAPI v0.141.1, capture of 2026-08-18. Run `python -I scripts/scaffold.py ...` to generate the outline with pages.

## P1. Check the Django installation (DJT p.1)
`python -m django --version`. If Django is missing: error "No module named django". Installing: NOT COVERED (the DJT refers to another guide).

## P2. Create a project and run the Django development server (DJT p.1-2)
1. `django-admin startproject mysite` (avoid the names `django` and `test`).
2. Enter the outer directory (where `manage.py` is).
3. `python manage.py runserver` and open `http://127.0.0.1:8000/` ("Congratulations!" page).
4. The unapplied-migrations warning can be ignored for now.
5. Never use this server in production.

## P3. Create the `polls` app and the first view (DJT p.3-4)
1. In the `manage.py` directory: `python manage.py startapp polls`.
2. `polls/views.py`: function `index(request)` returning an `HttpResponse` with a text.
3. `polls/urls.py`: `urlpatterns = [path("", views.index, name="index")]`.
4. `mysite/urls.py`: `path("polls/", include("polls.urls"))` besides the admin.
5. `python manage.py runserver` and open `http://localhost:8000/polls/` (not the root `/`).
Generator: `python -I scripts/scaffold.py django --project mysite --app polls [--out DIR]`.

## P4. Install and run FastAPI (FAPI p.4-7, 20)
1. Install `uv` (FAPI p.4) and add FastAPI: `uv add "fastapi[standard]"` (quotes, FAPI p.5; command legible on p.20). Alternative with pip: inside a virtual environment (FAPI p.5).
2. Create `main.py` (example on p.5; `async def` variant on p.6).
3. `fastapi dev` (FAPI p.7): reads `main.py`, detects the app, uses Uvicorn, with auto-reload.
4. Open `http://127.0.0.1:8000/items/5?q=somequery`, `/docs` and `/redoc`.
Generator: `python -I scripts/scaffold.py fastapi --variant basic|async|body`.

## P5. Add a body to a FastAPI route (FAPI p.10-11)
Import `BaseModel` from `pydantic`; declare `class Item(BaseModel)` with `name: str`, `price: float`, `is_offer: bool | None = None`; add `@app.put("/items/{item_id}")` with `item_id: int, item: Item`. The server reloads and the docs (`/docs`, `/redoc`) update.

## P6. Deploy FastAPI (FAPI p.19-20)
NOT COVERED for the command. Known: FastAPI Cloud with a single command (detects the app; opens the browser for login if needed) or other providers following their guides.

## P7. Flask (FLT p.1-3)
NOT COVERED for procedures. There is only the tutorial index.

## P8. Review snippets and commands (linter)
`python -I scripts/snippet_lint.py FILE_OR_FOLDER`: ERROR contradicts the source; WARNING is partly supported or [inference]; INFO is an observation. The absence of a finding does not prove correctness. `--rules` lists rules with origin and page.

## P9. Compare the three frameworks (comparator)
`python -I scripts/compare_frameworks.py compare [ID ...] [--only DJT,FAPI]`. A cell without a source = NOT COVERED. Do not recommend a framework based on missing cells.
