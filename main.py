from fastapi import FastAPI
from models import Product,ProductResponse
from db import session, engine
import database_models
from fastapi.middleware.cors import CORSMiddleware
from routers import product,auth
from db import get_db

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

@app.get("/")
def greet():
    return {"message": "hello there"}

app.include_router(product.router,prefix="/products",tags=["product"])
app.include_router(auth.router)
