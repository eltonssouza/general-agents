from fastapi import FastAPI

app = FastAPI()


class Plain:
    name: str


@app.get("/a/{item_id}")
def a(q: str | None):
    return {"q": q}


@app.get("/b/{item_id}")
def b(item_id, q: str | None = None):
    return {"item_id": item_id}


@app.get("/c")
def c():
    data = await fetch()
    return data


@app.put("/d/{item_id}")
async def d(item_id: int, item: Plain):
    return {"ok": True}
