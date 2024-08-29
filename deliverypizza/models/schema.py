from typing import List
from sqlmodel import SQLModel


    
    

class UserUpdate(SQLModel):
    """User update model."""
    username:str
    email: str
    password: str
    
class OrderUpdate(SQLModel):
    """Order update model."""
    status:str
    

class PizzaUpdate(SQLModel):
    """Pizza update model."""
    name: str
    size:str
    price: float

class PaymentUpdate(SQLModel):
    """Payment update model."""
    payment_status:str
    payment_method:str
    
    
    
    
