from typing import List
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False
    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int

class OrderSchema(BaseModel):
    user_id: int
    status: Optional[str] = "PENDING"
    items: List[OrderItemCreate]
    class Config:
        from_attributes = True

class ItemSchema(BaseModel):
    name: str
    price: float
    size: str
    class Config:
        from_attributes = True