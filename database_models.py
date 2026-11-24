from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base class for all declarative ORM models
Base = declarative_base()

# SQLAlchemy model for the 'Product' table in MySQL
class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing primary key with index
    name = Column(String(100))                          # Product name (max 100 characters)
    description = Column(String(255))                  # Short description (max 255 characters)
    price = Column(Float)                              # Product price as a float
    quantity = Column(Integer)                          # Available quantity in inventory
    owner_id=Column(Integer,ForeignKey("user.id"),nullable=False)
    owner= relationship("User",back_populates="products")


# SQLAlchemy model for the 'User' table in MySQL
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)               # Auto-incrementing primary key
    username = Column(String(100), unique=True, nullable=False)     # Unique username, cannot be empty
    hashed_password = Column(String(255), nullable=False)            # Securely hashed password, cannot be empty
    products= relationship("Product", back_populates="owner")