from fastapi import FastAPI, status

app_name = "quote"

app = FastAPI()


@app.post(f"/{app_name}", status_code=status.HTTP_201_CREATED)
def create_quote():
    return "create quote item"


@app.get(f"/{app_name}/{{id}}")
def read_quote(id: int):
    return f"read quote item with id {id}"


@app.get(f"/{app_name}")
def read_quotes():
    return "read quote list"


@app.put(f"/{app_name}/{{id}}")
def update_quote(id: int):
    return f"update quote item with id {id}"


@app.delete(f"/{app_name}/{{id}}")
def delete_quote(id: int):
    return f"delete quote item with id {id}"
