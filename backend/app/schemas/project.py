from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=10)
    progress: int = Field(default=0, ge=0, le=100)
    status: str = Field(default="active")


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1)
    symbol: str | None = Field(default=None, min_length=1, max_length=10)
    progress: int | None = Field(default=None, ge=0, le=100)
    status: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    symbol: str
    progress: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)