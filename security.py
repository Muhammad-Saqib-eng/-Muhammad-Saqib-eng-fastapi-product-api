from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from dotenv import load_dotenv
import os 

load_dotenv()

SECRET_KEY= os.getenv("SECRET_KEY")
print("SECRET KEY LOADED:", SECRET_KEY)
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_TIME=30


pwd_context =CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def hash_password(password :str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password :str , hashed_pasword:str)->bool:
    return pwd_context.verify(plain_password, hashed_pasword)

def create_access_token(data:dict)->str:
    to_encode=data.copy()
    expire_time= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp " :int(expire_time.timestamp())})
    return jwt.encode(to_encode,SECRET_KEY,algorithm= ALGORITHM)
def verify_token(token:str)->str | None:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM )
        username : str = payload.get("sub")
        return username
    except JWTError:
        return None

oauth2_scheme= OAuth2PasswordBearer(tokenUrl= "/auth/login")

def get_current_user(token : str= Depends(oauth2_scheme))->str:
    username =verify_token(token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    return username                         