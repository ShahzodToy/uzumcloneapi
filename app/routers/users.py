from fastapi import APIRouter,status,HTTPException,Depends
from ..models import User
from datetime import timedelta
from ..schemas import RegisterUser,Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..crud import create_user,get_user_email,authenticate_user,create_access_token_for,get_user
from typing import Annotated
from ..database import SessionLocal
from sqlalchemy.orm import Session
import jwt
from .. import schemas 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]

SECRET_KEY = '3cd2cd5b769c8222191e07f60e2b713666993fb345243a62955b762e8190daf8'
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

auth_router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

@auth_router.post('/sign-up',status_code=201)
async def register_user(db:db_dependency,user:RegisterUser):
    db_user = get_user_email(db=db,email=user.email,username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_306_RESERVED,detail='User already registered with this email')
    return create_user(db=db,user=user)


@auth_router.post('/token',response_model=Token)
async def create_access_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid password and username')
    token = create_access_token_for(user.username,user.id,timedelta(days=30))
    return {'access_token':token,'token_type':'bearer'}


def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Unautherozired credientials')
        return {'username':username,'id':user_id}
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Borib royhatdan ot')
    
user_dependency = Annotated[dict,Depends(get_current_user)]

@auth_router.get('/user-profile/{user_id}',status_code=200)
async def profile_page(db:db_dependency,user_id:int):
    db_user = get_user(user_id,db)
    if db_user:
        return db_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')

@auth_router.get('/users-list',status_code=200)
async def all_users(db:db_dependency,user:user_dependency):
    users = db.query(User).all()
    return {
        'users':users,
        'user_login':user
    }
@auth_router.patch('/profile-update/{user_id}')
async def update_profile(db:db_dependency,user:schemas.BaseUser,user_id):
    user_db = db.query(User).filter(User.id == user_id).first()
    if user_db:
        for val, key in user.dict(exclude_unset=True).items():
            setattr(user_db,val,key)
        db.commit()
        return {'user':user,
                'message':'User updated successfully'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')

    
        
        