from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from models import ProductCreate, ProductResponse,ProductUpdate
import database_models
from sqlalchemy.orm import Session
from db import get_db
from security import get_current_user

# APIRouter for product-related operations
router = APIRouter()

# Endpoint: GET /products - Retrieve all products (optionally filtered by price range)
@router.get("", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def return_all_products(min_price: float = None, max_price: float = None, db: Session = Depends(get_db)):
    # If both min_price and max_price query parameters are provided, filter the query
    if min_price is not None and max_price is not None:
        db_products = db.query(database_models.Product).filter(
            database_models.Product.price >= min_price, 
            database_models.Product.price <= max_price
        ).all()
    else:
        db_products = db.query(database_models.Product).all()
    return db_products

# Endpoint: GET /products/search - Search products containing a name substring
@router.get("/search", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def search_by_name(name: str, db: Session = Depends(get_db)):
    db_product_name = db.query(database_models.Product).filter(database_models.Product.name.contains(name)).all()
    if db_product_name:
        return db_product_name
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
        
# Endpoint: GET /products/{id} - Retrieve a specific product by its ID
@router.get("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def return_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product_id = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product_id:
        return db_product_id
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")

# Endpoint: POST /products - Create a new product ( Requires authentication

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    # Validate request payload inputs

    if product.price <= 0 or not product.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid price or name")
    else:

        user=db.query(database_models.User).filter(database_models.User.username==current_user).first()

        if not user:
            raise HTTPException(status_code=404,detail="User not found")
        

        
        # Convert Pydantic model to SQLAlchemy DB model and commit it
        product_data = product.model_dump()
        new_product= database_models.Product(**product_data,owner_id=user.id)
        db.add(new_product) 
        db.commit()
        db.refresh(new_product)
        return new_product

# Endpoint: PUT /products/{id} - Update an existing product by ID ( Requires authentication)
@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    
    user=db.query(database_models.User).filter(database_models.User.username==current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")

    if db_product.owner_id!=user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update this product"
        )

      # 4. Update fields (only update if provided)
    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.price is not None:
        db_product.price = product.price
    if product.quantity is not None:
        db_product.quantity = product.quantity
    db.commit()
    return {"message": "Product updated"}
    
        

# Endpoint: DELETE /products/{id} - Delete an existing product by ID ( Requires authentication)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    # 1. Fetch logged-in user
    user = db.query(database_models.User).filter(database_models.User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Fetch product
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")

    # 3.  IDOR Check: Does this user own this product?
    if db_product.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to delete this product"
        )

    db.delete(db_product)
    db.commit()