from fastapi import APIRouter,Depends,HTTPException,status
from security import hash_password,verify_password,create_access_token
from database_models import User
from models import UserCreate,UserResponse,Token
from sqlalchemy.orm import Session
from db import get_db
import database_models

router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user:UserCreate,db: Session=Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail= "username already exits")
    
    new_user = database_models.User(username=user.username, hashed_password=hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login",response_model=Token ,status_code=status.HTTP_200_OK)
def login(user: UserCreate,db: Session =Depends(get_db)):
    db_user= db.query(User).filter(User.username==user.username).first()
    if not db_user or not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Crediantials")
    
    token= create_access_token(data= {"sub": db_user.username})
    return {"access_token" : token, "token_type" : "bearer"}

