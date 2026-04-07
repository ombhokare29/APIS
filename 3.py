from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ------------------ MODELS ------------------

class Item(BaseModel):
    name: str
    price: float
    quantity: int


class Order(BaseModel):
    user: str
    items: List[Item]


# ------------------ DATABASE ------------------

orders = []


# ------------------ BUSINESS LOGIC ------------------

def calculate_total(items: List[Item]):
    return sum(item.price * item.quantity for item in items)


# ------------------ CREATE ORDER ------------------

@app.post("/orders")
def create_order(order: Order):
    if len(order.items) == 0:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    total = calculate_total(order.items)

    new_order = {
        "id": len(orders) + 1,
        "user": order.user,
        "items": order.items,
        "total_amount": total
    }

    orders.append(new_order)

    return {
        "message": "Order created successfully",
        "data": new_order
    }


# ------------------ GET ALL ORDERS ------------------

@app.get("/orders")
def get_orders():
    return {
        "count": len(orders),
        "data": orders
    }


# ------------------ GET SINGLE ORDER ------------------

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order
    
    raise HTTPException(status_code=404, detail="Order not found")


# ------------------ DELETE ORDER ------------------

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for i, order in enumerate(orders):
        if order["id"] == order_id:
            deleted = orders.pop(i)
            return {
                "message": "Order deleted",
                "data": deleted
            }
    
    raise HTTPException(status_code=404, detail="Order not found")


# ------------------ ROOT ------------------

@app.get("/")
def home():
    return {"message": "E-commerce Order API running 🛒"}