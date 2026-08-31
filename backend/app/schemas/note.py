from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    project_id: int
    title: str = Field(
        min_length=1,
        max_length=200
    )
    content: str = Field(
        min_length=1
    )


class NoteUpdate(BaseModel):
    project_id: int | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    content: str | None = Field(
        default=None,
        min_length=1
    )


class NoteResponse(BaseModel):
    id: int
    project_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )