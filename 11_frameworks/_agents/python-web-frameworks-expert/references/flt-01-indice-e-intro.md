# FLT: introduction and index of the Flask Tutorial (FLT p.1-3)

**Central warning: this source is only a table of contents/introduction.** It is 3 pages: the list of tutorial section titles and two paragraphs of context. **There is no code, command, function name, or content of any section.** Everything not listed below is NOT COVERED.

Identification: start page of the "Tutorial" of the Flask documentation, "stable" brand (FLT p.1). The PDF title (metadata) is "Tutorial - Flask Documentation (3.1.x)"; the number 3.1.x **does not appear in the body text**. PDF generated on 2026-08-18.

## What the source says
- **Goal** (FLT p.1): build a basic blog application called **Flaskr**. Users will be able to **register, log in, create posts and edit or delete their own posts**. It will also be possible to **package and install** the application on other computers.
- **Prerequisite** (FLT p.1): familiarity with Python is assumed; the official Python tutorial is suggested for learning or reviewing.
- **Scope** (FLT p.1): the tutorial **does not cover all Flask features**; the Quickstart is suggested for an overview and then the documentation. The tutorial uses **only what Flask and Python provide**; in another project, you can use extensions or other libraries to simplify tasks.
- **Flexibility** (FLT p.2): Flask does not require a specific project or code layout. For beginners, however, the tutorial uses a **structured approach**, with a bit of initial **boilerplate**, to avoid common beginner pitfalls and produce a project that is easy to expand. With more comfort, you can leave this structure and take advantage of all the flexibility.
- **Ready example** (FLT p.3): the tutorial project is available as an example in the Flask repository, to compare with yours. Next step: "Project Layout".

## Section index (titles only; FLT p.1)
1. Project Layout
2. Application Setup
3. Define and Access the Database
4. Blueprints and Views
5. Templates
6. Static Files
7. Blog Blueprint
8. Make the Project Installable
9. Test Coverage
10. Deploy to Production
11. Keep Developing!

[inference] The titles suggest the topics (structure, app configuration, database, blueprints/views, templates, static files, packaging, tests, production), but **the text does not explain any of them**. Do not derive APIs, commands or names from them (for example, of an "application factory" or of `flask run`): **NOT COVERED**.

## How to answer
- Question about "how to do X in Flask": say the source is only an index; give the title of the corresponding section, if any, and **refuse to detail it**. Give `[extrapolation]` only if the user explicitly asks, labeled and without a page.
- Question "Flask vs. Django vs. FastAPI": use `scripts/compare_frameworks.py`; the Flask column will be almost entirely "NOT COVERED" or "section title only".
