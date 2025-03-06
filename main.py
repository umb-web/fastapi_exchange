from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


def convert_currency(amount: float, from_currency: str, to_currency: str):
    exchange_rates = {
        ("USD", "EUR"): 0.92,
        ("EUR", "USD"): 1.08,
        ("USD", "COP"): 4104,
        ("COP", "USD"): 0.00024,
        ("USD", "GBP"): 0.78,
        ("GBP", "USD"): 1.28,
        ("EUR", "COP"): 4441,
        ("COP", "EUR"): 0.00023,
        ("EUR", "GBP"): 0.85,
        ("GBP", "EUR"): 1.18,
        ("COP", "GBP"): 0.00019,
        ("GBP", "COP"): 5299,
    }

    if from_currency == to_currency:
        return amount

    rate = exchange_rates.get((from_currency, to_currency))
    if rate is None:
        raise ValueError(f"exchange not available {from_currency} a {to_currency}")

    return amount * rate


@app.post("/exchange_currency")
async def exchange(request: Request):

    try:
        body = await request.json()
        amount = body.get("amount")
        from_currency = body.get("from_currency")
        to_currency = body.get("to_currency")

        if amount is None or from_currency is None or to_currency is None:
            raise HTTPException(status_code=400, detail="data missing")

        total = convert_currency(amount, from_currency, to_currency)

        if total is None:
            raise HTTPException(status_code=400, detail="currency not available")

        return JSONResponse(
            content={
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "total": total,
            },
            status_code=200,
        )

    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
