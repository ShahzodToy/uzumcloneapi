from fastapi import APIRouter,Depends,HTTPException,status
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from ..models import Product,Order,OrderItem
from .users import get_current_user
from ..schemas import OrderItemModel

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

order_router = APIRouter(
    prefix='/order',
    tags =['orders']
)

@order_router.post('/order-product/{product_id}')
async def create_orders(db:db_dependency,product_id:int,user:user_dependency):
    product_id = db.query(Product).filter(Product.id == product_id).first()
    if product_id:
        new_order = Order(
            user_id=user['id'],
            status = 'PENDING',
            total_amount = (product_id.quantity * product_id.price)
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    if new_order:
        new_order_item = OrderItem(
            product_id = product_id.id,
            order_id = new_order.id,
            quantity = product_id.quantity
        )
        db.add(new_order_item)
        db.commit()
        db.refresh(new_order_item)
        return {'order_item':new_order_item,
                'order':new_order}

    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail='Someting wrong with details that you input')

@order_router.delete('/delet-order/{order_id}',status_code=200)
async def delete_product_user(db:db_dependency,order_id:int,user:user_dependency):
    order_item = db.query(OrderItem).join(Order).filter(
        OrderItem.order_id == order_id,
    Order.user_id == user['id']).first()
    order = db.query(Order).filter(Order.id == order_id,Order.user_id == user['id']).first()
    if order and order:
        db.delete(order_item)
        db.delete(order)
        db.commit()
        db.commit()
        
        return {'message':'Deleted successfully'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='With this id is not found')

@order_router.get('/order-list',status_code=200)
async def order_list(db:db_dependency,user:user_dependency,):
    orders = db.query(Order).filter(Order.user_id == user['id']).all()
    if orders:
        return {'orders':orders}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User has no orders ')


@order_router.get('/orderitem-list',status_code=200)
async def order_list(db:db_dependency):
    orders = db.query(OrderItem).all()
    if orders:
        return {'orders':orders}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User has no orders ')

@order_router.put('/order-item-update/{order_id}',status_code=200)
async def order_update(db:db_dependency,order_id:int,user:user_dependency,order_i:OrderItemModel):
    order_item = db.query(OrderItem).join(Order).filter(
        OrderItem.order_id == order_id,
    Order.user_id == user['id']).first()
    order = db.query(Order).filter(Order.id == order_id,Order.user_id == user['id']).first()
    if order_item and order:
        for val,key in order_i.dict(exclude_unset=True).items():
            setattr(order_item,key,val)
        order.total_amount = order_item.quantity * order_item.price
        db.commit()
        return {'message':'Order has successfully updted'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Order not found')

    