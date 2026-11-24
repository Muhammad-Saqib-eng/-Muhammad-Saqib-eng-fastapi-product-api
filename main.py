from fastapi import FastAPI
from models import ProductResponse
from db import session, engine
import database_models
from fastapi.middleware.cors import CORSMiddleware
from routers import product, auth
from db import get_db

# Initialize the main FastAPI application instance
app = FastAPI()

# Configure CORS middleware to permit requests from the frontend app (e.g., React on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Automatically create all tables defined in declarative database_models if they do not exist
database_models.Base.metadata.create_all(bind=engine)


# Database initialization function to seed default products
def initialize_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            # Unpack the validated Pydantic model dictionary to create SQLAlchemy record
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()

# Run the seeding script on app startup
initialize_db()

# Root endpoint for health check or testing server availability
@app.get("/")
def greet():
    return {"message": "hello there"}

# Mount router endpoints under their respective paths
app.include_router(product.router, prefix="/products", tags=["product"])
app.include_router(auth.router)
