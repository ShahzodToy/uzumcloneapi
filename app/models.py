from sqlalchemy import Column, Integer, String, Float,ForeignKey,Boolean,DateTime,BIGINT
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date,timezone,datetime


class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True)
    username = Column(String,index=True)
    email = Column(String,unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    is_superuser = Column(Boolean,default=False)
    created = Column(DateTime,default=date.today())

    orders = relationship('Order',back_populates='user')

class Product(Base):
    __tablename__ ='products'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    available_qauntity = Column(Integer)
    description = Column(String,index=True)

    order_items = relationship('OrderItem',back_populates='product')

class Order(Base):
    __tablename__='orders'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    status = Column(String)
    total_amount = Column(Integer,nullable=False)

    user = relationship('User',back_populates='orders')
    order_items = relationship('OrderItem',back_populates='order',cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__='order_items'
    id = Column(Integer,primary_key=True)
    product_id = Column(Integer,ForeignKey('products.id'))
    order_id = Column(Integer,ForeignKey('orders.id'))
    quantity = Column(Integer,nullable=False)

    order = relationship('Order',back_populates='order_items')
    product = relationship('Product',back_populates='order_items')

class Payment(Base):
    __tablename__='payments'
    id = Column(Integer,primary_key=True)
    order_id = Column(Integer,ForeignKey('orders.id'))
    card_number = Column(Integer,index=True)
    issue_number = Column(Integer,index=True)
    price = Column(Float,index=True)

