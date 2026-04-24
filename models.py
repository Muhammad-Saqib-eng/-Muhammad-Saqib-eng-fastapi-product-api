from pydantic import BaseModel 
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity : int 

class ProductResponse(BaseModel):
    id:int
    name:str
    description: str
    price: float

class UserCreate(BaseModel):
    username: str
    password :str

class UserResponse(BaseModel):
    id :int
    username: str

class Token(BaseModel):
    access_token:str
    token_type : str