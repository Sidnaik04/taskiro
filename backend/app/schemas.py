from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    deadline: datetime
    image_url: Optional[HttpUrl | str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: datetime | None = None
    image_url: Optional[HttpUrl | str] = None


class TaskOut(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
