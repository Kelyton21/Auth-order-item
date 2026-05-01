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

    def calculate_total(self, price: float):
        return price * self.quantity

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

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    size: str
    class Config:
        from_attributes = True

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int
    total: float
    item: Optional[ItemResponse] = None
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: float
    status: str
    items: List[OrderItemResponse]
    class Config:
        from_attributes = True
