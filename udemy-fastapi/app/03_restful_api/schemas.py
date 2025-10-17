from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# Base schema with common attributes
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False

# Schema for creating a todo
class TodoCreate(TodoBase):
    pass

# Schema for updating a todo
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None

# Schema for reading a todo (response)
class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
