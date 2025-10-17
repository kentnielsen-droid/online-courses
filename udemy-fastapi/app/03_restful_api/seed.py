from sqlalchemy.orm import Session
from .db import SessionLocal, engine, Base
from .models import Todo
from datetime import datetime, timedelta
import random

def check_if_seeded(db: Session) -> bool:
    """Check if database already has data."""
    return db.query(Todo).count() > 0

def seed_todos(db: Session):
    """Seed the database with dummy todo data."""
    
    dummy_todos = [
        {
            "title": "Complete FastAPI tutorial",
            "description": "Go through the official FastAPI documentation and build a sample project",
            "completed": True
        },
        {
            "title": "Set up SQLAlchemy models",
            "description": "Create database models for the todo application with proper relationships",
            "completed": True
        },
        {
            "title": "Implement CRUD operations",
            "description": "Build Create, Read, Update, Delete endpoints for todos",
            "completed": False
        },
        {
            "title": "Add authentication",
            "description": "Implement JWT-based authentication for the API",
            "completed": False
        },
        {
            "title": "Write unit tests",
            "description": "Create comprehensive test suite using pytest",
            "completed": False
        },
        {
            "title": "Set up CI/CD pipeline",
            "description": "Configure GitHub Actions for automated testing and deployment",
            "completed": False
        },
        {
            "title": "Deploy to production",
            "description": "Deploy the application to a cloud platform like AWS or Heroku",
            "completed": False
        },
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread, cheese, vegetables, and fruits",
            "completed": False
        },
        {
            "title": "Schedule dentist appointment",
            "description": "Call Dr. Smith's office for a checkup next week",
            "completed": False
        },
        {
            "title": "Review pull requests",
            "description": "Check and approve pending PRs from the team",
            "completed": True
        },
        {
            "title": "Update project documentation",
            "description": "Add API documentation and update README with new features",
            "completed": False
        },
        {
            "title": "Refactor database queries",
            "description": "Optimize slow queries and add proper indexing",
            "completed": False
        },
        {
            "title": "Plan team meeting",
            "description": "Schedule sprint planning for next week and prepare agenda",
            "completed": False
        },
        {
            "title": "Fix bug in user registration",
            "description": "Email validation not working properly for certain domains",
            "completed": True
        },
        {
            "title": "Learn Docker",
            "description": "Complete Docker tutorial and containerize the application",
            "completed": False
        },
    ]
    
    # Add todos with some variation in created_at dates
    for i, todo_data in enumerate(dummy_todos):
        todo = Todo(
            **todo_data,
            created_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        db.add(todo)
    
    db.commit()
    print(f"✅ Successfully seeded {len(dummy_todos)} todos!")

def init_db():
    """Initialize database with tables and seed data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Seed data if database is empty
    db = SessionLocal()
    try:
        if not check_if_seeded(db):
            print("📦 Seeding database with dummy data...")
            seed_todos(db)
        else:
            print("ℹ️  Database already contains data, skipping seed.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
