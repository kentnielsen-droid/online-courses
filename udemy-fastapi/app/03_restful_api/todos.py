from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated

from .db import get_db
from . import schemas
from .crud import todo_crud
from .security import get_current_active_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.post("/", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    db: Annotated[Session, Depends(get_db)],
    todo: schemas.TodoCreate,
    current_user = Annotated[dict, Depends(get_current_active_user)]
):
    """Create a new todo for the current user."""
    return todo_crud.create(db, todo, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.TodoResponse])
def get_todos(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    completed: Optional[bool] = None,
    current_user = Annotated[dict, Depends(get_current_active_user)]
):
    """Get all todos for the current user."""
    return todo_crud.get_all_for_user(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed
    )

@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(
    db: Annotated[Session, Depends(get_db)],
    todo_id: int,
    current_user = Annotated[dict, Depends(get_current_active_user)]
):
    """Get a specific todo by ID."""
    db_todo = todo_crud.get_by_id(db, todo_id, owner_id=current_user.id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return db_todo

@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    db: Annotated[Session, Depends(get_db)],
    todo_id: int,
    todo: schemas.TodoUpdate,
    current_user = Annotated[dict, Depends(get_current_active_user)]
):
    """Update a todo."""
    db_todo = todo_crud.update(db, todo_id, current_user.id, todo)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    db: Annotated[Session, Depends(get_db)],
    todo_id: int,
    current_user = Annotated[dict, Depends(get_current_active_user)]
):
    """Delete a todo."""
    if not todo_crud.delete(db, todo_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

@router.get("/search/", response_model=List[schemas.TodoResponse])
def search_todos(
    db: Annotated[Session, Depends(get_db)],
    q: str = Query(..., min_length=1),
    current_user = Annotated[dict, Depends(get_current_active_user)]
):
    """Search todos by title or description."""
    return todo_crud.search_for_user(db, current_user.id, q)
