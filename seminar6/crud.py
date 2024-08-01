# crud.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import User, Product, Order
from schemas import UserCreate, ProductCreate, OrderCreate

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# CRUD для пользователей
def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# CRUD для товаров
def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

# CRUD для заказов
def create_order(db: Session, order: OrderCreate):
    db_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()