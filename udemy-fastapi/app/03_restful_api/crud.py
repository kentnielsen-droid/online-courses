from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from . import models, schemas

class TodoCRUD:
    """
    CRUD operations for Todo model.
    Best practice: Separate business logic from route handlers.
    """
    
    @staticmethod
    def create(db: Session, todo: schemas.TodoCreate) -> models.Todo:
        """Create a new todo."""
        db_todo = models.Todo(**todo.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)  # Get the updated object with ID
        return db_todo
    
    @staticmethod
    def get_by_id(db: Session, todo_id: int) -> Optional[models.Todo]:
        """Get a single todo by ID."""
        return db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None
    ) -> List[models.Todo]:
        """Get all todos with optional filtering and pagination."""
        query = db.query(models.Todo)
        
        if completed is not None:
            query = query.filter(models.Todo.completed == completed)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update(
        db: Session,
        todo_id: int,
        todo_update: schemas.TodoUpdate
    ) -> Optional[models.Todo]:
        """Update a todo."""
        db_todo = TodoCRUD.get_by_id(db, todo_id)
        
        if not db_todo:
            return None
        
        # Only update fields that are provided
        update_data = todo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def delete(db: Session, todo_id: int) -> bool:
        """Delete a todo."""
        db_todo = TodoCRUD.get_by_id(db, todo_id)
        
        if not db_todo:
            return False
        
        db.delete(db_todo)
        db.commit()
        return True
    
    @staticmethod
    def search(db: Session, search_term: str) -> List[models.Todo]:
        """Search todos by title or description."""
        search_pattern = f"%{search_term}%"
        return db.query(models.Todo).filter(
            or_(
                models.Todo.title.ilike(search_pattern),
                models.Todo.description.ilike(search_pattern)
            )
        ).all()

# Create instance for easy import
todo_crud = TodoCRUD()