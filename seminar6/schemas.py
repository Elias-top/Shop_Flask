# schemas.py
from pydantic import BaseModel
import datetime
from typing import List

# Pydantic модели для пользователей
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

# Pydantic модели для товаров
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True

# Pydantic модели для заказов
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    status: str

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime.datetime
    status: str

    class Config:
        orm_mode = True