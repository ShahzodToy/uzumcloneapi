from fastapi import FastAPI,Depends
from .database import Base,engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .routers import users,products,orders,payments

app = FastAPI()
app.include_router(users.auth_router)
app.include_router(products.product_router)
app.include_router(orders.order_router)
app.include_router(payments.pay_router)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(users.get_current_user)]

@app.get('/')
async def root(user:user_dependency):
    if user:
        return {'message':'Hello world'}
    return {'message':'You should register yourself'}