from fastapi import FastAPI
from PriceEstimator import PriceEstimator
from PropertyInput import PropertyInput

app = FastAPI()


@app.post("/predict-price/")
async def predict_price(property: PropertyInput):
    estimator = PriceEstimator()
    estimated_price = estimator.estimate_price(property)
    return {"estimated_price": float(estimated_price * property.area)}
