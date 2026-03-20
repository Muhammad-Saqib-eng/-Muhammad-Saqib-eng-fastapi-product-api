from fastapi import FastAPI, Depends
from models import Product
from db import session, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)
database_models.Base.metadata.create_all(bind=engine)

products=[
    Product(id=1,name="Laptop",description="A Good Laptop", price= 999.9,quantity=50),
    Product(id=2,name="Computer",description="A Good Comp", price= 199.9,quantity=30),
    Product(id=3,name="Mobile",description="A Good Phone", price= 2299.9,quantity=20)
    ]


def initialize_db():
    db=session()
    count= db.query(database_models.Product).count()
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()

initialize_db()

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return {"message": "hello there"}


@app.get("/products")
def return_all_products(min_price: float = None, max_prize: float = None ,db:Session = Depends(get_db)):
    if min_price != None and max_prize != None:
        db_products=db.query(database_models.Product).filter(database_models.Product.price>=min_price, database_models.Product.price<=max_prize).all()
    else:
        db_products= db.query(database_models.Product).all()
    return db_products

@app.get("/products/search")
def search_by_name(name:str, db:Session = Depends(get_db)):
    db_product_name=db.query(database_models.Product).filter(database_models.Product.name.contains(name)).all()
    if db_product_name:
        return db_product_name
    else:
        return "Product not foound "
    
@app.get("/products/{id}")
def return_product_by_id(id:int,db:Session = Depends(get_db)):
    db_product_id= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product_id:
        return db_product_id
    return "Product Not Found"


@app.post("/products")
def add_product(product:Product,db:Session = Depends(get_db)):  #the format we get the data is the product itself (product:Product)
    if product.price<=0 or not  product.name:
        return "crediantials wrong price or name."
    else:
        db.add(database_models.Product(**product.model_dump()))
        db.commit()
        return product

@app.put("/products/{id}")
def update_product(id:int , product:Product,db:Session = Depends(get_db)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name= product.name
        db_product.description=product.description
        db_product.price= product.price
        db_product.quantity= product.quantity
        db.commit()
        return "Product updated"
    else:  
        return "NO Product found"


@app.delete("/products/{id}")
def delete_product(id:int,db:Session = Depends(get_db)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    else:
        return "NO Product found"
