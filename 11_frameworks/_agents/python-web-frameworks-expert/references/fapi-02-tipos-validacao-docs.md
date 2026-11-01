# FAPI part B: types, validation, Pydantic body and automatic docs (FAPI p.8-19)

Source: FastAPI v0.141.1 overview. Pages = PDF. The capture lost the image on p.8; the Swagger UI images on p.12-14 have no text.

## Interactive documentation (FAPI p.8-9)
- `http://127.0.0.1:8000/docs`: **automatic interactive** documentation (Swagger UI).
- `http://127.0.0.1:8000/redoc`: **automatic alternative** documentation (ReDoc).
- The documentation is generated with **OpenAPI**, which can be used by interactive documentation systems and by **automatic client generation** in many languages (FAPI p.17).

## Example upgrade: body in PUT (FAPI p.10-11)
- Modify `main.py` to receive a **body** in a **PUT** request, declaring the body with **standard Python types, thanks to Pydantic**.
- Code (p.11): import `BaseModel` from `pydantic`; class `Item(BaseModel)` with `name: str`, `price: float` and `is_offer: bool | None = None`; route `@app.put("/items/{item_id}")` with `item_id: int` and `item: Item`, returning `{"item_name": item.name, "item_id": item_id}`. The earlier GET routes remain. (Generate with `scaffold.py fastapi --variant body`.)
- The server started by `fastapi dev` **reloads automatically** (FAPI p.11).
- The interactive documentation is **updated automatically**, including the new body (FAPI p.11); with **"Try it out"** you can fill in the parameters and interact directly with the API (FAPI p.12); the **"Execute"** button makes the interface send the parameters, receive the results and show them (FAPI p.13). The alternative documentation (ReDoc) also reflects the new query parameter and the body (FAPI p.14).
- In the screenshots (FAPI p.12-14) the PUT operation shows `item_id` as a required integer path parameter and a required `application/json` body with an example containing `name`, `price`, `is_offer` [visual reading; the images have no text].

## Recap (FAPI p.15-16)
You **declare once** the types of parameters, body etc. as **function parameters**, with **modern standard Python types**, without learning the syntax, methods or classes of a specific library (e.g.: `item_id: int`, `item: Item`). With that single declaration you get:
- **Editor support**: autocompletion and type checking.
- **Data validation**: automatic, clear errors when the data is invalid, even for deeply nested JSON.
- **Conversion of input data** coming from the network into Python types, reading from: JSON, path parameters, query parameters, cookies, headers, forms and files.
- **Conversion of output data** from Python types to network data (JSON): basic types (`str`, `int`, `float`, `bool`, `list` etc.), `datetime` objects, `UUID` objects, database models and others.
- **Automatic interactive documentation**, with two alternative interfaces: Swagger UI and ReDoc (FAPI p.16-17).

## What FastAPI does in the example (FAPI p.17)
- Validates that there is an `item_id` in the path for GET and PUT and that it is an `int`; if not, the client sees a clear, useful error.
- Checks the optional query parameter `q` (GET): since it is declared with `= None`, it is **optional**; **without the `None` it would be required** (just as the body is in PUT).
- For PUT on `/items/{item_id}`, reads the body as JSON: `name` required (`str`), `price` required (`float`), `is_offer` optional (`bool`), if present. This also holds for deeply nested JSON.
- Converts from and to JSON automatically and documents everything with OpenAPI.
- P.17-18 suggests changing `item.name` to `item.price` in the return and seeing the editor autocomplete attributes and know the types (screenshot on p.18).

## User guide "spoiler" (FAPI p.18-19) — only cited
The user guide (not included) offers: parameters coming from headers, cookies, form fields and files; validation constraints such as `maximum_length` or `regex`; a "powerful and easy" **dependency injection** system; **security and authentication** with OAuth2 with JWT tokens and HTTP Basic; nested JSON models via Pydantic; **GraphQL integration** via Strawberry and other libraries; extras thanks to Starlette: **WebSockets**, tests based on **HTTPX and pytest**, **CORS**, **Cookie Sessions** and more.
**All of this is NOT COVERED in content**: the source only lists it.

## Linter rules that originate here
`FA-PATH-MISSING` [inference], `FA-PATH-UNTYPED`, `FA-OPTIONAL-NODEF`, `FA-BODY-NOT-MODEL` [inference].
