from fastapi import APIRouter,HTTPException,Depends
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from .users import get_current_user
from ..schemas import PaymentProcess
from ..models import OrderItem,Order,Payment

pay_router = APIRouter(
    prefix='/payment',
    tags=['payment processs']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@pay_router.post('/payment-process',status_code=200)
async def payment_ok(db:db_dependency,user:user_dependency,payment:PaymentProcess):
    order_ok = db.query(Order).filter(Order.user_id == user['id']).all()
    total_amount = 0
    if order_ok:
        for order in order_ok:
            total_amount += order.total_amount
        new_pay = Payment(
            card_number = payment.card_num,
            issue_number = payment.issue_num,
            price=total_amount
        )
        
        db.add(new_pay)
        db.commit()
        db.refresh(new_pay)
        
        
        return {'message':'Successfully paid'}
    
