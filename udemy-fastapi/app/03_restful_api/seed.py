from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from .db import SessionLocal, engine, Base, get_db
from .models import Todo, User
from .security import get_password_hash
from datetime import datetime, timedelta, timezone
import random

def check_if_seeded(db: Annotated[Session, Depends(get_db)]) -> bool:
    """Check if database already has data."""
    return db.query(User).count() > 0

def seed_users(db: Annotated[Session, Depends(get_db)]):
    """Seed users."""
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "hashed_password": get_password_hash("admin123"),
            "is_superuser": True
        },
        {
            "email": "john@example.com",
            "username": "john_doe",
            "hashed_password": get_password_hash("pass123"),
            "is_superuser": False
        },
        {
            "email": "jane@example.com",
            "username": "jane_smith",
            "hashed_password": get_password_hash("mypass1"),
            "is_superuser": False
        },
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)
    
    db.commit()
    for user in users:
        db.refresh(user)
    
    print(f"✅ Successfully seeded {len(users)} users!")
    return users

def seed_todos(db: Annotated[Session, Depends(get_db)], users):
    """Seed todos for users."""
    todos_templates = [
        ("Complete FastAPI tutorial", "Go through the official FastAPI documentation", True),
        ("Set up SQLAlchemy models", "Create database models for the application", True),
        ("Implement CRUD operations", "Build Create, Read, Update, Delete endpoints", False),
        ("Add authentication", "Implement JWT-based authentication", False),
        ("Write unit tests", "Create comprehensive test suite using pytest", False),
        ("Deploy to production", "Deploy the application to cloud platform", False),
        ("Buy groceries", "Milk, eggs, bread, cheese, vegetables", False),
        ("Schedule dentist appointment", "Call Dr. Smith's office for checkup", False),
        ("Review pull requests", "Check and approve pending PRs from team", True),
        ("Update documentation", "Add API documentation and update README", False),
    ]
    
    todos = []
    for user in users:
        # Give each user 5-8 random todos
        num_todos = random.randint(5, 8)
        user_todos = random.sample(todos_templates, num_todos)
        
        for title, description, completed in user_todos:
            todo = Todo(
                title=title,
                description=description,
                completed=completed,
                owner_id=user.id,
                created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))
            )
            db.add(todo)
            todos.append(todo)
    
    db.commit()
    print(f"✅ Successfully seeded {len(todos)} todos!")

def init_db():
    """Initialize database with tables and seed data."""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if not check_if_seeded(db):
            print("📦 Seeding database with dummy data...")
            users = seed_users(db)
            seed_todos(db, users)
            print("\n🎉 Database seeding complete!")
            print("\n📝 Test credentials:")
            print("   Admin: username='admin', password='admin123'")
            print("   User1: username='john_doe', password='password123'")
            print("   User2: username='jane_smith', password='password123'")
        else:
            print("ℹ️  Database already contains data, skipping seed.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
