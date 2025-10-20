from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Annotated
from . import models, schemas, db
from .security import get_password_hash

# ============= User CRUD =============

class UserCRUD:
    """CRUD operations for User model."""
    
    @staticmethod
    def create(db: Annotated[Session, Depends(db.get_db)], user: schemas.UserCreate) -> models.User:
        """Create a new user with hashed password."""
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_by_id(db: Annotated[Session, Depends(db.get_db)], user_id: int) -> Optional[models.User]:
        """Get a user by ID."""
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Annotated[Session, Depends(db.get_db)], email: str) -> Optional[models.User]:
        """Get a user by email."""
        return db.query(models.User).filter(models.User.email == email).first()
    
    @staticmethod
    def get_by_username(db: Annotated[Session, Depends(db.get_db)], username: str) -> Optional[models.User]:
        """Get a user by username."""
        return db.query(models.User).filter(models.User.username == username).first()
    
    @staticmethod
    def get_all(
        db: Annotated[Session, Depends(db.get_db)],
        skip: int = 0,
        limit: int = 100
    ) -> List[models.User]:
        """Get all users with pagination."""
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(
        db: Annotated[Session, Depends(db.get_db)],
        user_id: int,
        user_update: schemas.UserUpdate
    ) -> Optional[models.User]:
        """Update a user."""
        db_user = UserCRUD.get_by_id(db, user_id)
        
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Hash password if it's being updated
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete(db: Annotated[Session, Depends(db.get_db)], user_id: int) -> bool:
        """Delete a user."""
        db_user = UserCRUD.get_by_id(db, user_id)
        
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True

# ============= Todo CRUD (Updated) =============

class TodoCRUD:
    """CRUD operations for Todo model."""
    
    @staticmethod
    def create(db: Annotated[Session, Depends(db.get_db)], todo: schemas.TodoCreate, owner_id: int) -> models.Todo:
        """Create a new todo for a specific user."""
        db_todo = models.Todo(**todo.model_dump(), owner_id=owner_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def get_by_id(db: Annotated[Session, Depends(db.get_db)], todo_id: int, owner_id: int) -> Optional[models.Todo]:
        """Get a todo by ID (only if owned by user)."""
        return db.query(models.Todo).filter(
            and_(models.Todo.id == todo_id, models.Todo.owner_id == owner_id)
        ).first()
    
    @staticmethod
    def get_all_for_user(
        db: Annotated[Session, Depends(db.get_db)],
        owner_id: int,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None
    ) -> List[models.Todo]:
        """Get all todos for a specific user."""
        query = db.query(models.Todo).filter(models.Todo.owner_id == owner_id)
        
        if completed is not None:
            query = query.filter(models.Todo.completed == completed)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update(
        db: Annotated[Session, Depends(db.get_db)],
        todo_id: int,
        owner_id: int,
        todo_update: schemas.TodoUpdate
    ) -> Optional[models.Todo]:
        """Update a todo (only if owned by user)."""
        db_todo = TodoCRUD.get_by_id(db, todo_id, owner_id)
        
        if not db_todo:
            return None
        
        update_data = todo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def delete(db: Annotated[Session, Depends(db.get_db)], todo_id: int, owner_id: int) -> bool:
        """Delete a todo (only if owned by user)."""
        db_todo = TodoCRUD.get_by_id(db, todo_id, owner_id)
        
        if not db_todo:
            return False
        
        db.delete(db_todo)
        db.commit()
        return True
    
    @staticmethod
    def search_for_user(
        db: Annotated[Session, Depends(db.get_db)],
        owner_id: int,
        search_term: str
    ) -> List[models.Todo]:
        """Search todos for a specific user."""
        search_pattern = f"%{search_term}%"
        return db.query(models.Todo).filter(
            and_(
                models.Todo.owner_id == owner_id,
                or_(
                    models.Todo.title.ilike(search_pattern),
                    models.Todo.description.ilike(search_pattern)
                )
            )
        ).all()

# Create instances
user_crud = UserCRUD()
todo_crud = TodoCRUD()