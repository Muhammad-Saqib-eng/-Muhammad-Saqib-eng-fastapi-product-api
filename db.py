from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from dotenv import load_dotenv
import os 

# Load environment variables from the .env file
load_dotenv()

# Fetch the database connection URL from environment variables
db_url = os.getenv("db_url")

# Create the SQLAlchemy engine to manage connections to the MySQL database
engine = create_engine(db_url)

# Create a configured database Session class (autocommit/autoflush disabled)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency generator to yield database sessions per request and clean them up afterward
def get_db():
    db = session()
    try:
        yield db  # Provide the session to the route handler
    finally:
        db.close()  # Ensure the session is closed after the request is finished