from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, Base, SQLALCHEMY_DATABASE_URL
from . import todos, auth, users
from .seed import init_db

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed database if using SQLite (development)
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    init_db()

app = FastAPI(
    title="Todo API with Authentication",
    description="A Todo API with user authentication using JWT",
    version="2.0.0"
)

# CORS middleware (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Todo API with Authentication",
        "docs": "/docs",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
