from datetime import datetime,timedelta
from passlib.context import CryptContext
from jose import JWTError,jwt


SECRECT_KEY= "Secret_key"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_TIME=30


pwd_context =CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def hash_password(password :str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password :str , hashed_pasword:str)->bool:
    return pwd_context.verify(plain_password, hashed_pasword)

def create_access_token(data:dict)->str:
    to_encode=data.copy()
    expire_time= datetime.utcnow+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp :" :expire_time})
    return jwt.encode(to_encode,SECRECT_KEY,algorithm= [ALGORITHM])
def verify_token(token:str)->str | None:
    try:
        payload=jwt.decode(token,SECRECT_KEY,algorithms=[ALGORITHM] )
        username : str = payload.get("sub")
        return username
    except JWTError:
        return None
