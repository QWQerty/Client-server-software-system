from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API URLs
ORDER_API_URL = "http://127.0.0.1:8000"
AI_API_URL = "http://127.0.0.1:8001"

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    try:
        response = requests.get(f"{ORDER_API_URL}/orders/")
        orders = response.json() if response.status_code == 200 else []
    except:
        orders = []

    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})

@app.post("/orders")
async def create_order(request: Request):
    form_data = await request.form()
    order_data = {
        "id": int(form_data["id"]),
        "item_type": form_data["item_type"],
        "quantity": int(form_data["quantity"]),
        "price_per_item": float(form_data["price"])
    }
    try:
        requests.post(f"{ORDER_API_URL}/orders/", json=order_data)
    except:
        pass
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ai-analysis", response_class=HTMLResponse)
async def ai_analysis_page(request: Request):
    return templates.TemplateResponse("ai_analysis.html", {"request": request})

@app.post("/ai-analysis")
async def predict_price(request: Request):
    form_data = await request.form()
    prediction_request = {
        "item_type": form_data["item_type"],
        "expected_quantity": int(form_data["quantity"])
    }
    try:
        response = requests.post(f"{AI_API_URL}/predict_price/", json=prediction_request)
        prediction = response.json() if response.status_code == 200 else {}
    except:
        prediction = {}

    return templates.TemplateResponse("ai_analysis.html", {"request": request, "prediction": prediction})

# Templates structure
# Place `index.html`, `orders.html`, and `ai_analysis.html` in the `templates` directory.
# Static files (e.g., CSS, JS) should be placed in the `static` directory.

# Example commands to run:
# `uvicorn web_interface:app --reload --port 8080`
# or `python -m uvicorn Webi:app --reload --port 8080`
