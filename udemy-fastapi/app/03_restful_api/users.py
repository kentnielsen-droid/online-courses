from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Annotated

from .db import get_db
from . import schemas
from .crud import user_crud
from .security import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Get all users."""
    return user_crud.get_all(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
    current_user = Depends(get_current_active_user)
):
    """Get a specific user by ID."""
    # Users can only view their own profile unless they're superuser
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db_user = user_crud.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user = Depends(get_current_active_user)
):
    """Update a user."""
    # Users can only update their own profile unless they're superuser
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db_user = user_crud.update(db, user_id, user_update)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: int,
):
    """Delete a user."""
    if not user_crud.delete(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
