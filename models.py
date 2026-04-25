from database import Base # Base para os modelos para a criação do banco de dados
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'users'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    name = Column("name",String,nullable=False)
    email = Column("email",String,nullable=False,unique=True)
    password = Column("password",String,nullable=False)
    active = Column("active",Boolean,nullable=False,default=True)
    admin = Column("admin",Boolean,nullable=False,default=False)

    orders = relationship("Order", back_populates="user")

    def __init__(self,name,email,password,active=True,admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Order(Base):
    __tablename__ = 'orders'

    #order_status = (
    #    ("PENDING","PENDING"),
    #    ("COMPLETED","COMPLETED"),
    #    ("CANCELLED","CANCELLED")
    #)

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    user_id = Column("user_id",Integer,ForeignKey("users.id"),nullable=False)
    total = Column("total",Float,nullable=False)
    status = Column("status",String,nullable=False,default="PENDING")
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

    def __init__(self,user_id,total,status="PENDING"):
        self.user_id = user_id
        self.total = total
        self.status = status

class Item(Base):
    __tablename__ = 'item'

    #item_size = (
    #    ("SMALL","SMALL"),
    #    ("MEDIUM","MEDIUM"),
    #    ("LARGE","LARGE")
    #)

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    name = Column("name",String,nullable=False)
    price = Column("price",Float,nullable=False)
    size = Column("size",String,nullable=False)
    
    order_items = relationship("OrderItem", back_populates="item")

    def __init__(self,name,price,size):
        self.name = name
        self.price = price
        self.size = size
        

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    order_id = Column("order_id",Integer,ForeignKey("orders.id"),nullable=False)
    item_id = Column("item_id",Integer,ForeignKey("item.id"),nullable=False)
    quantity = Column("quantity",Integer,nullable=False)
    total = Column("total",Float,nullable=False)

    order = relationship("Order", back_populates="items")
    item = relationship("Item", back_populates="order_items")

    def __init__(self,order_id,item_id,quantity,total):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity
        self.total = total