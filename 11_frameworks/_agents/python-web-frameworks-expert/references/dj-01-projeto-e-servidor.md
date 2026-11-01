# DJT part A: version, project, layout and server (DJT p.1-2)

Source: page "Writing your first Django app, part 1", **Django 5.0** docs. Pages = PDF.

## Version and scope
- Banner at the top: the document is for an insecure, unsupported version of Django; it asks you to upgrade (DJT p.1). **[DATED]**: treat everything as Django 5.0.
- The tutorial is written for **Django 5.0**, which supports **Python 3.10 or later** (DJT p.1). There is a version selector for other docs; the PDF only has 5.0.
- Example application: a **polls** app in two parts: a public site to view and vote, and an admin site to add, change and delete polls (DJT p.1).
- The tutorial **assumes Django is already installed**; to check it and see the version, run in the shell `python -m django --version`; if it is not installed, the message is "No module named django" (DJT p.1). Installing/removing old versions is referred to another guide (not reproduced): NOT COVERED.

## Create the project (DJT p.1)
- `django-admin startproject mysite` generates starter code: a **project** is a collection of settings for a Django instance, including database, Django options and app settings.
- If the command fails, the text refers to "Problems running django-admin" (content not included).
- **Names to avoid** (note): do not name projects after built-in Python or Django components; `django` conflicts with Django itself and `test` conflicts with a built-in Python package.

## Generated layout (DJT p.2)
```
mysite/            <- container (name irrelevant to Django; can be renamed)
    manage.py      <- command-line utility of the project
    mysite/        <- the project's Python package (name used in imports, e.g.: mysite.urls)
        __init__.py   <- empty; marks the directory as a package
        settings.py   <- project settings
        urls.py       <- URL declarations (the site's "table of contents")
        asgi.py       <- entry point for ASGI-compatible servers
        wsgi.py       <- entry point for WSGI-compatible servers
```
(Structure reproduced in summary form; the descriptions are a paraphrase of DJT p.2.)

## Development server (DJT p.2)
- In the outer directory (where `manage.py` is): `python manage.py runserver`.
- The example output shows: system check with no issues, a warning about **unapplied migrations** (instruction `python manage.py migrate`), date (April 2025 in the example), "Django version 5.0, using settings 'mysite.settings'" and "Starting development server at http://127.0.0.1:8000/".
- Visiting `http://127.0.0.1:8000/` shows the "Congratulations!" page with a rocket.
- It is a **lightweight web server, written in pure Python**, included for rapid development without configuring a production server such as Apache. **Do not use it in production**; the text says the team makes web frameworks, not web servers.
- Another port: see the `runserver` reference (not included; NOT COVERED for the syntax).
- Note: the migrations warning can be **ignored for now**; the database is handled next (part 2, outside the capture).

## Traps
- Naming the project `django` or `test` (DJT p.1). The linter detects this in command lines (`CMD-PROJNAME`).
- Using `runserver` in deployment (DJT p.2). The linter warns in Dockerfile/Procfile/YAML/service (`CMD-RUNSERVER-PROD`; file classification is [inference]).
- Confusing the outer directory (container) with the inner package: only the inner one enters the imports (DJT p.2).
