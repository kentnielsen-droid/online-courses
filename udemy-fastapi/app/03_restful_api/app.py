from fastapi import FastAPI
from .db import engine, Base, SQLALCHEMY_DATABASE_URL
from . import todos
from .seed import init_db

# Create database tables
Base.metadata.create_all(bind=engine)

if "sqlite" in SQLALCHEMY_DATABASE_URL:
    init_db()

app = FastAPI(
    title="Todo API",
    description="A simple Todo API with SQLAlchemy",
    version="1.0.0"
)

# Include routers
app.include_router(todos.router)

@app.get("/")
def root():
    return {"message": "Welcome to Todo API"}
