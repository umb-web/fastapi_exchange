from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


@app.get("/")
def home():
    return "Hola"


@app.get("/item/{id}")
def query_path_params(id: int, name: str):
    return f"Hello {name}, your id is {id}"


def convertir_moneda(amount: float, from_currency: str, to_currency: str):
    tasas_cambio = {
        ("USD", "EUR"): 0.52,
        ("EUR", "USD"): 1.099,
        ("USD", "COP"): 4000,
        ("COP", "USD"): 0.0025,
    }

    tasa = tasas_cambio.get((from_currency, to_currency))
    return round(amount * tasa) if tasa else None


@app.post("/convertidor")
async def convertidor(request: Request):
    body = await request.json()
    amount = body.get("amount")
    from_currency = body.get("from_currency")
    to_currency = body.get("to_currency")

    if amount is None or from_currency is None or to_currency is None:
        raise HTTPException(status_code=400, detail="Faltan datos")

    resultado = convertir_moneda(amount, from_currency, to_currency)

    if resultado is None:
        raise HTTPException(status_code=400, detail="Moneda no soportada")

    return JSONResponse(
        content={
            "cantidad": amount,
            "moneda_origen": from_currency,
            "moneda_destino": to_currency,
            "resultado": resultado,
        },
        status_code=200,
    )
