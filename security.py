from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from dotenv import load_dotenv
import os 

# Load environment variables
load_dotenv()

# Configuration variables for token signature and duration
SECRET_KEY = os.getenv("SECRET_KEY")
print("SECRET KEY LOADED:", SECRET_KEY)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30  # Token lifespan in minutes

# Password hashing context using the bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a plain text password using bcrypt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify if a plain password matches the stored bcrypt hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate a signed JWT token containing custom payload claims (username + expiration time)
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # Calculate token expiration timestamp
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    # Standard JWT claim for expiration timestamp ('exp')
    to_encode.update({"exp": int(expire_time.timestamp())})
    # Encode and sign the JWT payload using the secret key and signature algorithm
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode and verify the validity of a JWT token, returning the subject (username)
def verify_token(token: str) -> str | None:
    try:
        # Decodes token and automatically validates 'exp' signature
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except JWTError:
        return None  # Returns None if the signature is invalid or token is expired

# OAuth2 scheme config specifying where the login route is located to fetch tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# FastAPI Dependency to extract, verify token from headers, and return current authenticated user
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username