from fastapi import APIRouter,Depends,HTTPException,status
from ..schemas import ProductModel
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from ..crud import create_product
from ..models import Product

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]

product_router = APIRouter(
    prefix='/products',
    tags = ['product']
)

@product_router.get('/product-list')
async def product_list(db:db_dependency):
    products = db.query(Product).all()
    return {'products':products}

@product_router.post('/create-product',status_code=201)
async def create_products(db:db_dependency,product:ProductModel):
    return create_product(db=db,product=product)

@product_router.put('/update-product/{product_id}',status_code=200)
async def update_product(db:db_dependency,product_id:int,product:ProductModel):
    product_ = db.query(Product).filter(Product.id == product_id).first()
    if product_:
        for val,key in product.dict(exclude_unset=True).items():
            setattr(product_,val,key)
        db.commit()
        return product_
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,detail='Product id not found')

@product_router.delete('/delete-product/{product_id}',status_code=200)
async def delete_product(db:db_dependency,product_id:int):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product:
        db.delete(product)
        db.commit()
        return {'message':'Product deleted successfully'}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='product not found from list')


