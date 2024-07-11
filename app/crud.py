from .schemas import RegisterUser,ProductModel
from .models import User,Product
from datetime import timedelta,datetime
from sqlalchemy.orm import Session
from .security import generate_hashpassword,chech_hashpassword
import jwt



SECRET_KEY = '3cd2cd5b769c8222191e07f60e2b713666993fb345243a62955b762e8190daf8'
ALGORITHM = "HS256"

def get_user_email(email:str,username:str,db:Session):
    return  db.query(User).filter(User.email == email,User.username == username).first()

def get_user(user_id:int,db:Session):
    return db.query(User).filter(User.id == user_id).first()
    
def create_user(db:Session,user:RegisterUser):
    hashed_pass = generate_hashpassword(user.hashed_password)
    db_user = User(hashed_password=hashed_pass,username=user.username,email = user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db:Session,username:str,password:str):
    db_user= db.query(User).filter(User.username == username).first()
    if not db_user:
        return False
    if not chech_hashpassword(password,db_user.hashed_password):
        return False
    return db_user

def create_access_token_for(username:str,user_id:int,expires_delta:timedelta):
    to_encode = {'sub':username,'id':user_id}
    expires = datetime.utcnow() + expires_delta
    to_encode.update({'exp':expires})
    return jwt.encode(to_encode,SECRET_KEY,ALGORITHM)


# Product category

def create_product(db:Session,product:ProductModel):
    new_product = Product(
        name = product.name,
        price = product.price,
        quantity = product.quantity,
        available_qauntity = product.available_qauntity,
        description = product.description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

