from pydantic import BaseModel

# 1. Base schema with shared product fields
class ProductBase(BaseModel):
    name: str
    description: str | None = None  # Using 'str | None' fixes the Optional error!
    price: float

# 2. Schema for creating a product (POST payload) - No id, no owner_id!
class ProductCreate(ProductBase):
    quantity: int

# 3. Schema for updating a product (PUT/PATCH payload) - All fields optional
class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None

# 4. Schema returned to clients - Inherits from ProductBase + adds DB fields
class ProductResponse(ProductBase):
    id: int
    quantity: int
    owner_id: int
    class Config:
        from_attributes = True


# Pydantic schema for parsing user credentials during registration and login
class UserCreate(BaseModel):
    username: str
    password: str

# Pydantic schema for returning user profile details (excludes hashed_password for security)
class UserResponse(BaseModel):
    id: int
    username: str

# Pydantic schema returned upon successful login, containing the access token details
class Token(BaseModel):
    access_token: str
    token_type: str