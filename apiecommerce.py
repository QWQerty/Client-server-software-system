from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
orders = []

# Models
class Order(BaseModel):
    id: int
    item_type: str
    quantity: int
    price_per_item: float

class AnalysisResult(BaseModel):
    item_type: str
    average_quantity: float
    average_price: float

# Endpoints
@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    # Check for duplicate order ID
    if any(o['id'] == order.id for o in orders):
        raise HTTPException(status_code=400, detail="Order ID already exists")
    
    orders.append(order.dict())
    return order

@app.get("/orders/", response_model=List[Order])
def get_orders():
    return orders

@app.get("/orders/analysis/", response_model=List[AnalysisResult])
def analyze_orders():
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    analysis = {}

    # Group by item type and calculate averages
    for order in orders:
        item_type = order['item_type']
        if item_type not in analysis:
            analysis[item_type] = {'total_quantity': 0, 'total_price': 0, 'count': 0}
        
        analysis[item_type]['total_quantity'] += order['quantity']
        analysis[item_type]['total_price'] += order['price_per_item'] * order['quantity']
        analysis[item_type]['count'] += 1

    # Convert to list of AnalysisResult
    results = []
    for item_type, data in analysis.items():
        results.append(AnalysisResult(
            item_type=item_type,
            average_quantity=data['total_quantity'] / data['count'],
            average_price=data['total_price'] / data['total_quantity']
        ))

    return results

# Run the application
# Use `uvicorn filename:app --reload` to start the server
# or `python -m uvicorn apiecommerce:app --reload --port 8000`


# curl -X POST http://127.0.0.1:8000/orders/ -H "Content-Type: application/json" -d "{\"id\": 1, \"item_type\": \"A1\", \"quantity\": 10, \"price_per_item\": 250.0}"
# curl -X GET "http://127.0.0.1:8000/orders/"
# curl -X GET "http://127.0.0.1:8000/orders/analysis/"
