from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password:str
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str = "customer"
    orders: List["Order"] = Relationship(back_populates="user")


class OrderItem(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", primary_key=True)
    pizza_id: Optional[int] = Field(default=None, foreign_key="pizza.id", primary_key=True)
    quantity: int

class Pizza(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    size: str
    quantity: int
    price: float
    is_available: bool = True
    orders: List["Order"] = Relationship(back_populates="pizzas", link_model=OrderItem)

class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    pizza_id:int=Field(default=None,foreign_key="pizza.id")
    status: str = "pending"
    order_date: datetime = Field(default_factory=datetime.now)
    delivery_date: Optional[datetime] = Field(default_factory=datetime.now)
    user: "User" = Relationship(back_populates="orders")
    pizzas: List[Pizza] = Relationship(back_populates="orders", link_model=OrderItem)
    payments: List["Payment"] = Relationship(back_populates="order")


class Payment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    amount: float
    payment_status: str = "Done"
    payment_method: str = "cash"
    payment_date: datetime = Field(default_factory=datetime.now)
    order: "Order" = Relationship(back_populates="payments")

