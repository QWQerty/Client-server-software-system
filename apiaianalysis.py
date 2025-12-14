from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression
import requests

app = FastAPI()

# API URL for fetching orders
ORDER_API_URL = "http://127.0.0.1:8000/orders/"

# Models
class PredictionRequest(BaseModel):
    item_type: str
    expected_quantity: int

class PredictionResponse(BaseModel):
    item_type: str
    expected_quantity: int
    predicted_price: float

# Machine learning model training function
def train_model(item_type: str, orders: List[dict]):
    # Filter orders by item_type
    filtered_orders = [order for order in orders if order['item_type'] == item_type]
    if not filtered_orders:
        raise ValueError(f"No data available for item type: {item_type}")

    quantities = np.array([order["quantity"] for order in filtered_orders]).reshape(-1, 1)
    prices = np.array([order["price_per_item"] for order in filtered_orders])

    model = LinearRegression()
    model.fit(quantities, prices)
    return model

# Endpoint to predict price
@app.post("/predict_price/", response_model=PredictionResponse)
def predict_price(request: PredictionRequest):
    try:
        # Fetch orders from the external service
        response = requests.get(ORDER_API_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch orders from the external service")

        orders = response.json()
        model = train_model(request.item_type, orders)
        predicted_price = model.predict([[request.expected_quantity]])[0]

        return PredictionResponse(
            item_type=request.item_type,
            expected_quantity=request.expected_quantity,
            predicted_price=round(predicted_price, 2)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during prediction")

# Run the application
# Use `uvicorn filename:app --reload` to start the server
# or `python -m uvicorn apiaianalysis:app --reload --port 8001`