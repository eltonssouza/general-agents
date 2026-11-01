# DJT part B: app, view, URLconf and `path()` (DJT p.3-5)

Source: Django 5.0, tutorial part 1. Pages = PDF.

## Create the app (DJT p.3)
- An app is a Python package that follows a convention; Django ships a utility that generates the basic structure.
- Apps can live anywhere on the Python path. In the tutorial, the app sits next to `manage.py`, so it can be imported as a top-level module (and not as a submodule of `mysite`).
- Command, inside the `manage.py` directory: `python manage.py startapp polls`.
- Generated structure: `polls/` with `__init__.py`, `admin.py`, `apps.py`, `migrations/` (with `__init__.py`), `models.py`, `tests.py`, `views.py`.
- **Project vs. app** (note): an app is a web application that does something (blog, public records database, polls app); a project is the collection of configuration and apps of a site. A project can have several apps; an app can be in several projects.
- **Automatic reload** (note): the development server reloads Python code on each request, when needed; no restart is needed for code changes. **Adding files does not trigger a restart**: restart in those cases.

## First view (DJT p.3)
In `polls/views.py`, the most basic view: a function that receives `request` and returns an `HttpResponse` with a text (importing from `django.http`). To reach it in the browser, it must be mapped to a URL through a **URLconf**: Python files called `urls.py`, defined inside each app.

## App URLconf (DJT p.3-4)
- Create `polls/urls.py` with: `path` imported from `django.urls`, `views` imported from the current package (`from . import views`) and a `urlpatterns` list with `path("", views.index, name="index")`. (The code is on p.4; the sentence introducing it is on p.3.)
- Afterwards, the app has `urls.py` next to `views.py` (DJT p.4).

## Global URLconf and `include()` (DJT p.4)
- In `mysite/urls.py`, import `include` from `django.urls` and insert, in the `urlpatterns` list, `path("polls/", include("polls.urls"))`; the admin line (`path("admin/", admin.site.urls)`) stays.
- `include()` lets you reference other URLconfs. When it meets one, Django **chops off the part of the URL that already matched** and sends the remainder to the included URLconf.
- Idea: **plug-and-play URLs**. The app's URLs live in its own URLconf and can be mounted under `/polls/`, `/fun_polls/`, `/content/polls/` etc.
- **When to use** (note): **always** use `include()` when including other URL patterns; **`admin.site.urls` is the only exception**.
- Check: `python manage.py runserver` and open `http://localhost:8000/polls/`; the view's text should appear. If you get an error page, check that the URL is `/polls/` and not `/` (note "Page not found?").

## Arguments of `path()` (DJT p.5)
`path()` takes four arguments: **two required** (`route`, `view`) and **two optional** (`kwargs`, `name`).
- **route**: a string with a URL pattern. Django goes through `urlpatterns` from first to last and compares the requested URL with each pattern until it finds one that matches. Patterns **do not consider GET/POST parameters or the domain**: for `https://www.example.com/myapp/` and for `.../myapp/?page=3`, the URLconf looks for `myapp/`.
- **view**: when it finds the pattern, Django calls the view function with an `HttpRequest` object as the **first argument** and, as keyword arguments, the values "captured" from the route (the example comes later in the tutorial: NOT COVERED here).
- **kwargs**: arbitrary keyword arguments passed in a dictionary to the view; the tutorial does not use them.
- **name**: naming the URL lets you reference it unambiguously from elsewhere in Django, especially in templates, and change patterns globally by touching a single file.
- Next step pointed to: tutorial part 2, which works with the database (outside the capture).

## What the text does NOT cover (NOT COVERED)
Path converters (`<int:...>`), `re_path`, class-based views, models/ORM, `migrate` in use, templates, forms, admin in use, written tests, deployment with ASGI/WSGI (only the file names). If the user asks, answer with a labeled `[extrapolation]` or redirect.

## Linter rules that originate here
`DJ-PATH-ARGS`, `DJ-INCLUDE`, `DJ-ROUTE-QUERY`, `DJ-VIEW-REQUEST`, `DJ-NAME-MISSING` (see `python -I scripts/snippet_lint.py --rules`).
