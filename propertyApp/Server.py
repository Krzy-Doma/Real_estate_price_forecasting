from fastapi import FastAPI
from PriceEstimator import PriceEstimator
from PropertyInput import PropertyInput

app = FastAPI()


@app.post("/predict-price/")
async def predict_price(property: PropertyInput):
    estimated_price = PriceEstimator().estimate_price(property)
    return {"estimated_price": float(estimated_price * property.area)}

@app.get("/")
def read_root():
    return {"message": "Server is running"}