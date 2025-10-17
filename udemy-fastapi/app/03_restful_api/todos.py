from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .db import get_db
from . import schemas
from .crud import todo_crud

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db)
):
    """Create a new todo."""
    return todo_crud.create(db, todo)

@router.get("/", response_model=List[schemas.TodoResponse])
def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all todos with optional filtering."""
    return todo_crud.get_all(db, skip=skip, limit=limit, completed=completed)

@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific todo by ID."""
    db_todo = todo_crud.get_by_id(db, todo_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return db_todo

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """Update a todo."""
    db_todo = todo_crud.update(db, todo_id, todo)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """Delete a todo."""
    if not todo_crud.delete(db, todo_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

@router.get("/search/", response_model=List[schemas.TodoResponse])
def search_todos(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Search todos by title or description."""
    return todo_crud.search(db, q)
