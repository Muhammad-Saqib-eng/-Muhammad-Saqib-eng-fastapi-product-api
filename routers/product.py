from fastapi import APIRouter
from fastapi import  Depends , status ,HTTPException
from models import Product,ProductResponse
import database_models
from sqlalchemy.orm import Session
from db import get_db
from security import get_current_user

router = APIRouter()

@router.get("",response_model=list[ProductResponse],status_code=status.HTTP_200_OK)
def return_all_products(min_price: float = None, max_prize: float = None ,db:Session = Depends(get_db)):
    if min_price != None and max_prize != None:
        db_products=db.query(database_models.Product).filter(database_models.Product.price>=min_price, database_models.Product.price<=max_prize).all()
    else:
        db_products= db.query(database_models.Product).all()
    return db_products

@router.get("/search",response_model=list[ProductResponse],status_code=status.HTTP_200_OK)
def search_by_name(name:str, db:Session = Depends(get_db)):
    db_product_name=db.query(database_models.Product).filter(database_models.Product.name.contains(name)).all()
    if db_product_name:
        return db_product_name
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Product Not Found")
        
    
@router.get("/{id}",response_model=ProductResponse,status_code=status.HTTP_200_OK)
def return_product_by_id(id:int,db:Session = Depends(get_db)):
    db_product_id= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product_id:
        return db_product_id
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Product Not Found")


@router.post("",status_code=status.HTTP_201_CREATED)
def add_product(product:Product,db:Session = Depends(get_db),current_user :str  = Depends(get_current_user)):  #the format we get the data is the product itself (product:Product)
    if product.price<=0 or not  product.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid price or name")
    else:
        db.add(database_models.Product(**product.model_dump())) 
        db.commit()
        return product

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_product(id:int , product:Product,db:Session = Depends(get_db),current_user :str  = Depends(get_current_user)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name= product.name
        db_product.description=product.description
        db_product.price= product.price
        db_product.quantity= product.quantity
        db.commit()
        return "Product updated"
    else:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Product Not Found")


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_product(id:int,db:Session = Depends(get_db),current_user : str = Depends(get_current_user)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
