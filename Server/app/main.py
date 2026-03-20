from fastapi import FastAPI, HTTPException
from .db import init_db
from .schemas import OrderCreate, OrderOut
from .crud import create_order as crud_create, get_order as crud_get, list_orders as crud_list, mark_order_completed as crud_mark


app = FastAPI(title="Red's Printing Shop API")


@app.on_event("startup")
def startup():
    init_db()


@app.post("/orders", response_model=OrderOut)
def create_order(order: OrderCreate):
    created = crud_create(order.dict())
    return created


@app.get("/orders", response_model=list[OrderOut])
def get_orders():
    return crud_list()


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int):
    order = crud_get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}/complete")
def complete_order(order_id: int):
    ok = crud_mark(order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": "completed"}