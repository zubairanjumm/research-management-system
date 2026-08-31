from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookmarkCreate(BaseModel):
    project_id: int
    title: str = Field(min_length=1, max_length=200)
    url: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1, max_length=500)


class BookmarkUpdate(BaseModel):
    project_id: int | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    url: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )

    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )


class BookmarkResponse(BaseModel):
    id: int
    project_id: int
    title: str
    url: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )