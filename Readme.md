# FastAPI Product API

A RESTful API built with FastAPI, SQLAlchemy, and MySQL — developed as a hands-on learning project covering core backend concepts from scratch.

---

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM for database interaction
- **PyMySQL** — MySQL driver
- **MySQL 8.0** — database
- **python-jose** — JWT token creation and verification
- **passlib + bcrypt** — password hashing

---

## Project Structure

```
D:\fast api\
├── main.py               # App entry point, router registration, CORS
├── models.py             # Pydantic models (request/response schemas)
├── database_models.py    # SQLAlchemy models (DB tables)
├── db.py                 # DB engine, session, table creation
├── security.py           # Password hashing, JWT creation/verification
└── routers/
    ├── __init__.py
    ├── product.py        # All product endpoints
    └── auth.py           # Register and login endpoints
```

---

## Features

### Products
- `GET /products` — get all products (supports price range filter via `min_price` & `max_price` query params)
- `GET /products/search` — search products by name
- `GET /products/{id}` — get single product by ID
- `POST /products` — add new product 🔒
- `PUT /products/{id}` — update product 🔒
- `DELETE /products/{id}` — delete product 🔒

### Authentication
- `POST /auth/register` — register a new user (password is hashed before saving)
- `POST /auth/login` — login and receive a JWT token

> 🔒 = requires valid JWT token in `Authorization: Bearer <token>` header

### Other
- Input validation (rejects empty name or price ≤ 0)
- Response models (sensitive fields like `quantity` hidden from public responses)
- Proper HTTP status codes (200, 201, 204, 400, 401, 404)
- CORS enabled
- Custom error messages via `HTTPException`

---

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Muhammad-Saqib-eng/-Muhammad-Saqib-eng-fastapi-product-api
cd fastapi-product-api
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] "passlib[bcrypt]" "bcrypt==4.0.1" cryptography
```

### 4. Configure database
Make sure MySQL is running and create the database:
```sql
CREATE DATABASE dbFastApi;
```
Create a .env file with your own DATABASE_URL and SECRET_KEY

### 5. Run the server
```bash
uvicorn main:app --reload
```

### 6. Open Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## Testing Authentication in Swagger

1. `POST /auth/register` — create a user
2. `POST /auth/login` — get your token
3. Click the **Authorize 🔒** button at the top of Swagger
4. Paste the token and click Authorize
5. Now protected routes will accept your requests

---

## Key Bugs Faced & Fixed

| Bug | Cause | Fix |
|-----|-------|-----|
| Stale data after manual DB update | MySQL Workbench doesn't auto-commit manual queries | Clicked commit button in Workbench |
| `cryptography` error on startup | Missing package for MySQL 8.0 auth | `pip install cryptography` |
| `bcrypt` 500 error on register | `passlib` incompatible with latest bcrypt | Pinned `bcrypt==4.0.1` |
| `datetime is not JSON serializable` | Passing datetime object to JWT encoder | Converted to integer timestamp with `.timestamp()` |
| `unhashable type: list` in JWT encode | Passed `algorithm` as a list instead of string | Changed `algorithms=[ALGORITHM]` to `algorithm=ALGORITHM` |
| `Depends()` in decorator instead of function params | Misunderstanding of FastAPI's dependency injection | Moved `current_user=Depends(...)` into function parameters |

|Extra characters in dict keys like "exp " or "sub :" | "Spaces/colons typed inside the key string |Cleaned keys to "exp" and "sub"
|500 error on registe | Used Pydantic model instead of SQLAlchemy model to create DB user | Used database_models.User() not models.UserCreate() for DB insert

---

## What I Learned

- Structuring a FastAPI project with routers
- SQLAlchemy ORM: models, sessions, queries
- Pydantic for request validation and response shaping
- JWT authentication flow: register → login → token → protected route
- Password hashing with bcrypt via passlib
- Dependency injection with `Depends()`
- Debugging real errors from tracebacks

---

## Author

**Muhammad Saqib**  
BS Software Engineering — Air University, Islamabad  
[GitHub](https://github.com/Muhammad-Saqib-eng) | [LinkedIn](https://www.linkedin.com/in/muhammad-saqib-947173386/)
[X](https://x.com/Saqib_stu)
