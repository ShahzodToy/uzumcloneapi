from pydantic import BaseModel,EmailStr
from datetime import date
from typing import Optional

class BaseUser(BaseModel):
    email:EmailStr
    username:str

class RegisterUser(BaseUser):
    hashed_password:str

class User(BaseUser):
    id:int
    is_active:bool
    is_superuser:bool
    created:str
    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type: str

#Product category

class ProductModel(BaseModel):
    
    name:str
    price:int
    quantity:int
    available_qauntity:int
    description:str
    
    class Config:
        from_attributes=True

class OrderItemModel(BaseModel):
    product_id:int
    quantity:int
    

    class Config:
        from_attributes=True

class PaymentProcess(BaseModel):
    order_id:Optional[int] = None
    card_num:int
    issue_num:int

    class Config:
        from_attributes = True