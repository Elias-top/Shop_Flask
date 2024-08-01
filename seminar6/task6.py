# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from crud import create_user, get_user, create_product, get_products, create_order, get_order
from schemas import UserCreate, UserOut, ProductCreate, ProductOut, OrderCreate, OrderOut
from database import get_db

app = FastAPI()

# Маршруты для пользователей
@app.post("/users/", response_model=UserOut)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user

@app.get("/users/{user_id}", response_model=UserOut)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Маршруты для товаров
@app.post("/products/", response_model=ProductOut)
def api_create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = create_product(db=db, product=product)
    return db_product

@app.get("/products/", response_model=List[ProductOut])
def api_get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_products(db=db, skip=skip, limit=limit)
    return products

# Маршруты для заказов
@app.post("/orders/", response_model=OrderOut)
def api_create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = create_order(db=db, order=order)
    return db_order

@app.get("/orders/{order_id}", response_model=OrderOut)
def api_get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db=db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order