# Cases and anti-patterns (what the sources support)

Labels: `[from source]` (on the cited page), `[inference]` (direct deduction), `[extrapolation]` (outside the sources; avoided here).

## Django anti-patterns (DJT)
| Anti-pattern | Why | Origin |
|---|---|---|
| Naming the project `django` or `test` | Conflicts with Django itself / a built-in Python package | [from source] DJT p.1 |
| Serving production with `runserver` | The server is for development only | [from source] DJT p.2 |
| Passing `polls.urls` straight to `path()` instead of `include()` | The text says to **always** use `include()`; only `admin.site.urls` is an exception | [from source] DJT p.4 |
| Expecting the route pattern to match `?page=3` or the domain | Patterns do not consider GET/POST or the domain | [from source] DJT p.5 |
| View without a parameter for the request | The view is called with `HttpRequest` as the first argument | [from source] DJT p.5 |
| Visiting `/` expecting the `polls` view | The view is at `/polls/` | [from source] DJT p.4 |
| Expecting a new file to trigger a reload | Adding files does not restart the server | [from source] DJT p.3 |
| Confusing the outer directory with the package | Only the inner one is the project's Python package | [from source] DJT p.2 |

## FastAPI anti-patterns (FAPI)
| Anti-pattern | Why | Origin |
|---|---|---|
| Pasting `pip install fastapi[standard]` without quotes | The text says to use quotes so it works in all terminals | [from source] FAPI p.5 |
| Using `await` in a route declared with `def` | The text says to use `async def` when the code uses `async`/`await` | [from source] FAPI p.6 |
| Expecting `q: str \| None` without `= None` to be optional | The text ties optionality to `= None` | [from source] FAPI p.17 |
| Path parameter without a type | Validation and conversion come from the type declaration | [from source] FAPI p.16-17 |
| `{item_id}` in the path without a matching parameter | The example always declares both | [inference] FAPI p.8, 17 |
| Body declared with a class that does not inherit `BaseModel` | The text declares the body with Pydantic | [inference] FAPI p.10-11 |
| Treating the percentages and "on par with NodeJS and Go" as measurement | They are project claims / internal estimate | [from source] FAPI p.1-2 |
| Stating the deploy or install command "from the block" | Terminal blocks are empty in the capture | [from source] FAPI p.4-7, 19 |

## Anti-patterns in using the agent
- Answering "how to do X in Flask" as if there were a tutorial: the source is only an index (FLT p.1-3).
- Concluding "FastAPI is better than Django" from FastAPI's performance claims: no source compares; Django and Flask have no performance cells.
- Attributing newer-version behavior to Django just because the PDF was generated in 2026: the text is for Django 5.0 (DJT p.1).
- Citing p.6-8 of the DJT or p.3 of the FAPI as a technical source.

## Resolved cases
1. *"I ran `django-admin startproject test`."* -> ERROR in the linter; DJT p.1 says to avoid `test` and `django`.
2. *"I want the polls view at `/`."* -> The tutorial mounts it at `/polls/` with `include()`; to change the root, the source only states that the mount folder is free (`/polls/`, `/fun_polls/`...) (DJT p.4).
3. *"What is the FastAPI Cloud deploy command?"* -> NOT COVERED (empty block, FAPI p.19).
4. *"What does FastAPI validate in `/items/{item_id}`?"* -> `item_id` present and `int`, `q` optional because of `= None`; clear error to the client (FAPI p.17).
