from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def home():
    return "Hola"


@app.get("/item/{id}")
def query_path_params(id: int, name: str):
    return f"Hello {name}, your id is {id}"


@app.post("/convertidor")
async def convertidor(request: Request):
    body = await request.json()
    amount = body.get("name")
    to_currency = body.get("amount")
