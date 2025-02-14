from fastapi import APIRouter,Depends,status, Response,HTTPException
from typing import List

from ..import schemas,database,models
from sqlalchemy.orm import Session
from . import JWTtoken

from passlib.context import CryptContext


router = APIRouter(
    prefix="/user",
    tags=['users']
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

get_db=database.get_db

@router.post('/register', response_model=schemas.ShowAppUser)
def create(request: schemas.AppUser,db: Session=Depends(get_db)):

    hashed_passowrd=pwd_context.hash(request.password)    
    newuser=models.AppUser(name=request.name,email=request.email,password=hashed_passowrd)
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

@router.post('/login')
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user=db.query(models.AppUser).filter(models.AppUser.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")    
    if not pwd_context.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    
    access_token = JWTtoken.create_access_token(
        data={"sub": user.email}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
    
