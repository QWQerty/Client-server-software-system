import tkinter as tk
from tkinter import ttk, messagebox
import requests

# API URLs
ORDER_API_URL = "http://127.0.0.1:8000"
AI_API_URL = "http://127.0.0.1:8001"

# Order Management Service
def create_order():
    try:
        order = {
            "id": int(entry_id.get()),
            "item_type": entry_item_type.get(),
            "quantity": int(entry_quantity.get()),
            "price_per_item": float(entry_price.get())
        }
        response = requests.post(f"{ORDER_API_URL}/orders/", json=order)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Order created successfully!")
        else:
            messagebox.showerror("Error", response.json().get("detail", "Unknown error"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_orders():
    try:
        response = requests.get(f"{ORDER_API_URL}/orders/")
        if response.status_code == 200:
            orders = response.json()
            output = "".join([f"ID: {o['id']}, Item: {o['item_type']}, Quantity: {o['quantity']}, Price: {o['price_per_item']}\n" for o in orders])
            text_output_orders.delete(1.0, tk.END)
            text_output_orders.insert(tk.END, output)
        else:
            messagebox.showerror("Error", "Failed to fetch orders")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def analyze_orders():
    try:
        response = requests.get(f"{ORDER_API_URL}/orders/analysis/")
        if response.status_code == 200:
            analysis = response.json()
            output = "".join([f"Item: {a['item_type']}, Avg Quantity: {a['average_quantity']:.2f}, Avg Price: {a['average_price']:.2f}\n" for a in analysis])
            text_output_orders.delete(1.0, tk.END)
            text_output_orders.insert(tk.END, output)
        else:
            messagebox.showerror("Error", "Failed to fetch analysis")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# AI Analysis Service
def predict_price():
    try:
        prediction_request = {
            "item_type": entry_ai_item_type.get(),
            "expected_quantity": int(entry_ai_quantity.get())
        }
        response = requests.post(f"{AI_API_URL}/predict_price/", json=prediction_request)
        if response.status_code == 200:
            prediction = response.json()
            output = f"Item: {prediction['item_type']}, Expected Quantity: {prediction['expected_quantity']}, Predicted Price: {prediction['predicted_price']:.2f}\n"
            text_output_ai.delete(1.0, tk.END)
            text_output_ai.insert(tk.END, output)
        else:
            messagebox.showerror("Error", response.json().get("detail", "Unknown error"))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Service Management System")

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Tab 1: Order Management
frame_orders = ttk.Frame(notebook)
notebook.add(frame_orders, text="Order Management")

frame_inputs_orders = tk.Frame(frame_orders)
frame_inputs_orders.pack(pady=10)

label_id = tk.Label(frame_inputs_orders, text="Order ID")
label_id.grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(frame_inputs_orders)
entry_id.grid(row=0, column=1, padx=5, pady=5)

label_item_type = tk.Label(frame_inputs_orders, text="Item Type")
label_item_type.grid(row=1, column=0, padx=5, pady=5)
entry_item_type = tk.Entry(frame_inputs_orders)
entry_item_type.grid(row=1, column=1, padx=5, pady=5)

label_quantity = tk.Label(frame_inputs_orders, text="Quantity")
label_quantity.grid(row=2, column=0, padx=5, pady=5)
entry_quantity = tk.Entry(frame_inputs_orders)
entry_quantity.grid(row=2, column=1, padx=5, pady=5)

label_price = tk.Label(frame_inputs_orders, text="Price Per Item")
label_price.grid(row=3, column=0, padx=5, pady=5)
entry_price = tk.Entry(frame_inputs_orders)
entry_price.grid(row=3, column=1, padx=5, pady=5)

frame_buttons_orders = tk.Frame(frame_orders)
frame_buttons_orders.pack(pady=10)

button_create = tk.Button(frame_buttons_orders, text="Create Order", command=create_order)
button_create.grid(row=0, column=0, padx=10)

button_get = tk.Button(frame_buttons_orders, text="Get Orders", command=get_orders)
button_get.grid(row=0, column=1, padx=10)

button_analyze = tk.Button(frame_buttons_orders, text="Analyze Orders", command=analyze_orders)
button_analyze.grid(row=0, column=2, padx=10)

frame_output_orders = tk.Frame(frame_orders)
frame_output_orders.pack(pady=10)

text_output_orders = tk.Text(frame_output_orders, width=60, height=15)
text_output_orders.pack()

# Tab 2: AI Analysis
frame_ai = ttk.Frame(notebook)
notebook.add(frame_ai, text="AI Analysis")

frame_inputs_ai = tk.Frame(frame_ai)
frame_inputs_ai.pack(pady=10)

label_ai_item_type = tk.Label(frame_inputs_ai, text="Item Type")
label_ai_item_type.grid(row=0, column=0, padx=5, pady=5)
entry_ai_item_type = tk.Entry(frame_inputs_ai)
entry_ai_item_type.grid(row=0, column=1, padx=5, pady=5)

label_ai_quantity = tk.Label(frame_inputs_ai, text="Expected Quantity")
label_ai_quantity.grid(row=1, column=0, padx=5, pady=5)
entry_ai_quantity = tk.Entry(frame_inputs_ai)
entry_ai_quantity.grid(row=1, column=1, padx=5, pady=5)

frame_buttons_ai = tk.Frame(frame_ai)
frame_buttons_ai.pack(pady=10)

button_predict = tk.Button(frame_buttons_ai, text="Predict Price", command=predict_price)
button_predict.grid(row=0, column=0, padx=10)

frame_output_ai = tk.Frame(frame_ai)
frame_output_ai.pack(pady=10)

text_output_ai = tk.Text(frame_output_ai, width=60, height=15)
text_output_ai.pack()

# Run the app
root.mainloop()
